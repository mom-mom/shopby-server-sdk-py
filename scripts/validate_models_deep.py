"""
복잡 모델(order/product) 심층 검증 하네스

- 리스트 엔드포인트는 전체 페이징하여 모든 레코드의 list-item 모델을 개별 validate
- 상세 엔드포인트(복잡 모델)는 대량 샘플로 validate (커버리지 명시)
- 레코드 단위로 개별 검증하여 첫 실패에서 멈추지 않고 모든 불일치 패턴을 집계

Usage:
    uv run --env-file prod-workspace-token.env python scripts/validate_models_deep.py \
        [--order-days 90] [--order-detail 2000] [--product-detail 2000] [--concurrency 16]
"""

import argparse
import asyncio
import os
from collections import defaultdict
from datetime import date, timedelta

import httpx
from pydantic import BaseModel, ValidationError

from shopby_sdk.clients.order import Order, OrderDetailResponse
from shopby_sdk.clients.products import (
    ProductDetailV1Response,
    ProductDetailV3Response,
    ProductSearchItem,
)


def _headers(version: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {os.environ['SHOPBY_SERVER_ACCESS_TOKEN']}",
        "systemKey": os.environ["SHOPBY_SERVER_SYSTEM_KEY"],
        "version": version,
    }


BASE = os.environ.get("SHOPBY_BASE_URL", "https://server-api.e-ncp.com")


class Agg:
    """모델별 검증 결과 집계"""

    def __init__(self, name: str):
        self.name = name
        self.ok = 0
        self.fail = 0
        # (loc, type) -> {count, sample_msg, sample_input, sample_id}
        self.patterns: dict[tuple, dict] = defaultdict(lambda: {"count": 0})

    def validate(self, model: type[BaseModel], data: dict, rec_id: str) -> None:
        try:
            model.model_validate(data)
            self.ok += 1
        except ValidationError as e:
            self.fail += 1
            for err in e.errors():
                loc = ".".join(str(x) for x in err["loc"] if not isinstance(x, int))
                key = (loc, err["type"])
                p = self.patterns[key]
                p["count"] += 1
                if "sample_msg" not in p:
                    p["sample_msg"] = err.get("msg", "")[:80]
                    inp = err.get("input")
                    p["sample_input"] = (repr(inp)[:80]) if inp is not None else "None"
                    p["sample_id"] = rec_id

    def report(self) -> str:
        total = self.ok + self.fail
        lines = [f"\n## {self.name}: {self.ok}/{total} OK, {self.fail} fail, {len(self.patterns)} 패턴"]
        for (loc, typ), p in sorted(self.patterns.items(), key=lambda kv: -kv[1]["count"]):
            lines.append(
                f"   {p['count']:6}x  {loc}  [{typ}]  msg={p['sample_msg']}  "
                f"input={p['sample_input']}  (예: {p['sample_id']})"
            )
        return "\n".join(lines)


async def paginate_list(
    client: httpx.AsyncClient,
    path: str,
    version: str,
    base_params: dict,
    page_param: str,
    size_param: str,
    page_size: int,
    items_key: str,
    total_key: str,
    item_model: type[BaseModel],
    id_field: str,
    agg: Agg,
    id_sink: list,
    label: str,
) -> None:
    """리스트 엔드포인트 전체 페이징 + 레코드별 검증"""
    page = 1
    total = None
    while True:
        params = {**base_params, page_param: page, size_param: page_size}
        r = await client.get(path, headers=_headers(version), params=params)
        r.raise_for_status()
        body = r.json()
        items = body.get(items_key, []) if isinstance(body, dict) else body
        if total is None:
            total = body.get(total_key) if isinstance(body, dict) else len(items)
        if not items:
            break
        for it in items:
            agg.validate(item_model, it, str(it.get(id_field, "?")))
            if id_field in it and it[id_field] is not None:
                id_sink.append(it[id_field])
        done = agg.ok + agg.fail
        print(f"  [{label}] page {page} | 누적 {done}/{total} (fail={agg.fail})", flush=True)
        if done >= (total or 0) or len(items) < page_size:
            break
        page += 1


async def validate_details(
    client: httpx.AsyncClient,
    ids: list,
    make_path,
    version: str,
    model: type[BaseModel],
    agg: Agg,
    concurrency: int,
    label: str,
) -> None:
    """상세 엔드포인트 샘플 검증 (동시성 제한)"""
    sem = asyncio.Semaphore(concurrency)
    done = 0

    async def one(rec_id):
        nonlocal done
        async with sem:
            try:
                r = await client.get(make_path(rec_id), headers=_headers(version))
                if r.status_code != 200:
                    agg.fail += 1
                    p = agg.patterns[("<http>", str(r.status_code))]
                    p["count"] += 1
                    p.setdefault("sample_msg", r.text[:80])
                    p.setdefault("sample_input", "")
                    p.setdefault("sample_id", str(rec_id))
                    return
                agg.validate(model, r.json(), str(rec_id))
            except Exception as e:  # noqa: BLE001
                agg.fail += 1
                p = agg.patterns[("<exc>", type(e).__name__)]
                p["count"] += 1
                p.setdefault("sample_msg", str(e)[:80])
                p.setdefault("sample_input", "")
                p.setdefault("sample_id", str(rec_id))
            finally:
                done += 1
                if done % 200 == 0:
                    print(f"  [{label}] {done}/{len(ids)} (fail={agg.fail})", flush=True)

    await asyncio.gather(*[one(i) for i in ids])
    print(f"  [{label}] 완료 {done}/{len(ids)} (fail={agg.fail})", flush=True)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--order-days", type=int, default=90)
    ap.add_argument("--order-detail", type=int, default=2000)
    ap.add_argument("--product-detail", type=int, default=2000)
    ap.add_argument("--concurrency", type=int, default=16)
    args = ap.parse_args()

    end = date.today()
    start = end - timedelta(days=args.order_days)

    aggs = {
        "Order(list)": Agg("Order (목록)"),
        "OrderDetail": Agg("OrderDetailResponse (상세)"),
        "ProductSearchItem(list)": Agg("ProductSearchItem (목록)"),
        "ProductDetailV1": Agg("ProductDetailV1Response (상세)"),
        "ProductDetailV3": Agg("ProductDetailV3Response (상세)"),
    }
    order_nos: list = []
    product_nos: list = []

    async with httpx.AsyncClient(base_url=BASE, timeout=60.0) as client:
        # 1) 주문 목록 전체 페이징
        print("=== 1) 주문 목록 전체 페이징 검증 ===", flush=True)
        await paginate_list(
            client, "/orders", "1.1",
            {"startYmd": start.strftime("%Y-%m-%d"), "endYmd": end.strftime("%Y-%m-%d")},
            "pageNumber", "pageSize", 200, "contents", "totalCount",
            Order, "orderNo", aggs["Order(list)"], order_nos, "orders",
        )
        # 2) 상품 목록 전체 페이징
        print("\n=== 2) 상품 목록 전체 페이징 검증 ===", flush=True)
        await paginate_list(
            client, "/products/search/engine/", "2.0", {},
            "pageNumber", "pageSize", 100, "items", "totalCount",
            ProductSearchItem, "productNo", aggs["ProductSearchItem(list)"], product_nos, "products",
        )
        # 3) 주문 상세 샘플 검증
        sample_orders = order_nos[: args.order_detail]
        print(f"\n=== 3) 주문 상세 검증 ({len(sample_orders)}/{len(order_nos)}) ===", flush=True)
        await validate_details(
            client, sample_orders, lambda no: f"/orders/{no}", "1.0",
            OrderDetailResponse, aggs["OrderDetail"], args.concurrency, "order-detail",
        )
        # 4) 상품 상세 V1/V3 샘플 검증
        sample_products = product_nos[: args.product_detail]
        print(f"\n=== 4) 상품 상세 V1 검증 ({len(sample_products)}/{len(product_nos)}) ===", flush=True)
        await validate_details(
            client, sample_products, lambda no: f"/products/{no}", "1.0",
            ProductDetailV1Response, aggs["ProductDetailV1"], args.concurrency, "product-v1",
        )
        print(f"\n=== 5) 상품 상세 V3 검증 ({len(sample_products)}/{len(product_nos)}) ===", flush=True)
        await validate_details(
            client, sample_products, lambda no: f"/products/{no}/", "3.0",
            ProductDetailV3Response, aggs["ProductDetailV3"], args.concurrency, "product-v3",
        )

    print("\n" + "=" * 78)
    print("검증 결과 요약")
    print("=" * 78)
    for a in aggs.values():
        print(a.report())


if __name__ == "__main__":
    asyncio.run(main())

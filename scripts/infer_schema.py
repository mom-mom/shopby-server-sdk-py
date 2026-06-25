"""
실데이터 기반 JSON 스키마 추론 도구

dict[str, Any] 로 남아있는 필드의 실제 구조를 운영 데이터 N개 샘플로 추론한다.
각 키별로 타입/존재율/null율을 union 집계하고, 중첩 object/array 를 재귀 추론한다.

Usage:
    uv run --env-file prod-workspace-token.env python scripts/infer_schema.py <target> \
        [--samples 300] [--path certificationInfo] [--concurrency 16]

targets:
    product_v3   : GET /products/{no}/ (v3)  — 상품 상세 v3
    product_v1   : GET /products/{no}  (v1)  — 상품 상세 v1
    order_detail : GET /orders/{orderNo}     — 주문 상세
    claim        : GET /claims (목록 contents) — 클레임(claimData 등)
"""

import argparse
import asyncio
import os
from collections import Counter, defaultdict
from datetime import date, timedelta

import httpx

BASE = os.environ.get("SHOPBY_BASE_URL", "https://server-api.e-ncp.com")


def _h(version: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {os.environ['SHOPBY_SERVER_ACCESS_TOKEN']}",
        "systemKey": os.environ["SHOPBY_SERVER_SYSTEM_KEY"],
        "version": version,
    }


def _pytype(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "str"
    if isinstance(v, list):
        return "array"
    if isinstance(v, dict):
        return "object"
    return type(v).__name__


class Node:
    """한 위치(키)에서 관측된 값들의 통계"""

    def __init__(self):
        self.seen = 0
        self.types: Counter = Counter()
        self.children: dict[str, "Node"] = defaultdict(Node)  # object 키별
        self.item: "Node | None" = None  # array 아이템
        self.examples: list = []

    def observe(self, v):
        self.seen += 1
        t = _pytype(v)
        self.types[t] += 1
        if t == "object":
            for k, vv in v.items():
                self.children[k].observe(vv)
        elif t == "array":
            if self.item is None:
                self.item = Node()
            for it in v:
                self.item.observe(it)
        elif t not in ("null",) and len(self.examples) < 3 and v != "":
            if v not in self.examples:
                self.examples.append(v)


def render(node: Node, parent_total: int, name: str, indent: int, lines: list, max_depth: int):
    pad = "  " * indent
    types = ", ".join(f"{t}:{c}" for t, c in node.types.most_common())
    presence = f"{node.seen}/{parent_total}"
    nullable = "null" in node.types
    ex = ""
    if node.examples:
        ex = "  ex=" + ", ".join(repr(e)[:40] for e in node.examples[:2])
    flag = " ⚠️optional" if node.seen < parent_total else ""
    flag += " ?null" if nullable else ""
    lines.append(f"{pad}{name}: [{types}] ({presence}){flag}{ex}")
    if indent >= max_depth:
        if node.children or node.item:
            lines.append(f"{pad}  … (max-depth)")
        return
    # object children
    for k in sorted(node.children, key=lambda k: -node.children[k].seen):
        render(node.children[k], node.seen, k, indent + 1, lines, max_depth)
    # array item
    if node.item is not None:
        render(node.item, sum(node.item.types.values()) or node.seen, "[items]", indent + 1, lines, max_depth)


# ---------------- 데이터 소스 ----------------
async def collect(target: str, samples: int, concurrency: int) -> list:
    end = date.today()
    async with httpx.AsyncClient(base_url=BASE, timeout=60.0) as c:
        if target == "claim":
            # 목록 contents 를 직접 수집 (페이지 단위)
            out = []
            page = 1
            while len(out) < samples:
                r = await c.get(
                    "/claims", headers=_h("1.0"),
                    params={"startYmd": (end - timedelta(days=3650)).strftime("%Y-%m-%d"),
                            "endYmd": end.strftime("%Y-%m-%d"),
                            "searchDateType": "APPLY_YMDT", "searchType": "ALL",
                            "page": page, "size": 100},
                )
                r.raise_for_status()
                items = r.json().get("contents", [])
                if not items:
                    break
                out.extend(items)
                page += 1
            return out[:samples]

        # 상세형: 먼저 id 목록 확보 후 상세 N개 수집
        if target in ("product_v3", "product_v1"):
            ids = []
            page = 1
            while len(ids) < samples:
                r = await c.get("/products/search/engine/", headers=_h("2.0"),
                                params={"pageNumber": page, "pageSize": 100})
                r.raise_for_status()
                items = r.json().get("items", [])
                if not items:
                    break
                ids += [it["productNo"] for it in items if it.get("productNo")]
                page += 1
            ids = ids[:samples]
            ver, path = ("3.0", lambda n: f"/products/{n}/") if target == "product_v3" else ("1.0", lambda n: f"/products/{n}")
        elif target == "order_detail":
            ids = []
            r = await c.get("/orders", headers=_h("1.1"),
                            params={"startYmd": (end - timedelta(days=90)).strftime("%Y-%m-%d"),
                                    "endYmd": end.strftime("%Y-%m-%d"), "pageNumber": 1, "pageSize": min(samples, 200)})
            r.raise_for_status()
            ids = [o["orderNo"] for o in r.json().get("contents", []) if o.get("orderNo")][:samples]
            ver, path = "1.0", lambda n: f"/orders/{n}"
        else:
            raise SystemExit(f"unknown target: {target}")

        sem = asyncio.Semaphore(concurrency)
        out = []

        async def one(i):
            async with sem:
                try:
                    r = await c.get(path(i), headers=_h(ver))
                    if r.status_code == 200:
                        out.append(r.json())
                except Exception:  # noqa: BLE001
                    pass

        await asyncio.gather(*[one(i) for i in ids])
        return out


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--samples", type=int, default=300)
    ap.add_argument("--path", default=None, help="특정 top-level 키만 추론 (예: certificationInfo)")
    ap.add_argument("--depth", type=int, default=6)
    ap.add_argument("--concurrency", type=int, default=16)
    args = ap.parse_args()

    print(f"수집 중: target={args.target} samples={args.samples} ...", flush=True)
    data = await collect(args.target, args.samples, args.concurrency)
    print(f"수집 완료: {len(data)}건\n", flush=True)

    root = Node()
    for d in data:
        root.observe(d)

    if args.path:
        node = root.children.get(args.path)
        if node is None:
            print(f"'{args.path}' 키가 샘플에 없음. 사용 가능한 top-level 키:")
            print("  " + ", ".join(sorted(root.children)))
            return
        lines = []
        render(node, root.seen, args.path, 0, lines, args.depth)
        print("\n".join(lines))
    else:
        lines = []
        for k in sorted(root.children, key=lambda k: -root.children[k].seen):
            render(root.children[k], root.seen, k, 0, lines, args.depth)
        print("\n".join(lines))


if __name__ == "__main__":
    asyncio.run(main())

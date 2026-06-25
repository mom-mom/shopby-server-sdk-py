"""
신규/확장 SDK 읽기 전용(GET) 라이브 스모크 테스트

실제 API를 호출해 각 도메인의 응답이 모델로 정상 파싱되는지 검증한다.
⚠️ 생성/수정/삭제(POST/PUT/PATCH/DELETE)는 실데이터를 변경하므로 호출하지 않는다.

Usage:
    uv run --env-file .env.local python scripts/smoke_test_readonly.py
"""

import asyncio
import os
import traceback
from datetime import date, timedelta

from shopby_sdk.clients.admin import ShopbyServerAdminApiClient
from shopby_sdk.clients.claim import ShopbyServerClaimApiClient
from shopby_sdk.clients.delivery import ShopbyServerDeliveryApiClient
from shopby_sdk.clients.display import ShopbyServerDisplayApiClient
from shopby_sdk.clients.manage import ShopbyServerManageApiClient
from shopby_sdk.clients.member import ShopbyServerMemberApiClient
from shopby_sdk.clients.order_friends import ShopbyServerOrderFriendsApiClient
from shopby_sdk.clients.products import ShopbyServerProductsApiClient
from shopby_sdk.clients.promotion import ShopbyServerPromotionApiClient


def _summary(result) -> str:
    if result is None:
        return "None (204/빈본문)"
    if isinstance(result, list):
        return f"list[{len(result)}]" + (f" 첫항목={type(result[0]).__name__}" if result else "")
    # pydantic 모델
    fields = getattr(type(result), "model_fields", None)
    if fields:
        # totalCount/contents 류가 있으면 표시
        for k in ("total_count", "totalCount"):
            if hasattr(result, k):
                return f"{type(result).__name__}(total_count={getattr(result, k)})"
        return f"{type(result).__name__}({', '.join(list(fields)[:4])}...)"
    return type(result).__name__


async def run(label: str, coro):
    try:
        result = await coro
        print(f"  ✅ {label:42} -> {_summary(result)}")
        return True
    except Exception as e:  # noqa: BLE001
        msg = str(e).splitlines()[0][:160]
        print(f"  ❌ {label:42} -> {type(e).__name__}: {msg}")
        if os.environ.get("SMOKE_VERBOSE"):
            traceback.print_exc()
        return False


async def main():
    kw = dict(
        server_access_token=os.environ["SHOPBY_SERVER_ACCESS_TOKEN"],
        server_system_key=os.environ["SHOPBY_SERVER_SYSTEM_KEY"],
        base_url=os.environ.get("SHOPBY_BASE_URL"),
    )
    end = date.today()
    start = end - timedelta(days=30)

    products = ShopbyServerProductsApiClient(**kw)
    member = ShopbyServerMemberApiClient(**kw)
    display = ShopbyServerDisplayApiClient(**kw)
    claim = ShopbyServerClaimApiClient(**kw)
    admin = ShopbyServerAdminApiClient(**kw)
    delivery = ShopbyServerDeliveryApiClient(**kw)
    manage = ShopbyServerManageApiClient(**kw)
    of = ShopbyServerOrderFriendsApiClient(**kw)
    promotion = ShopbyServerPromotionApiClient(**kw)

    ok = 0
    total = 0
    checks = [
        # products (확장)
        ("products.get_brands", products.get_brands()),
        ("products.get_duty_categories", products.get_duty_categories()),
        ("products.get_custom_properties", products.get_custom_properties()),
        # member (확장)
        ("member.get_grades", member.get_grades()),
        # display (확장)
        ("display.get_categories", display.get_categories()),
        # claim (신규)
        ("claim.get_claims", claim.get_claims(start, end, "APPLY_YMDT", "ALL", 1, 10)),
        # admin (신규)
        ("admin.get_currencies", admin.get_currencies()),
        ("admin.get_mall_detail", admin.get_mall_detail()),
        ("admin.get_service_detail", admin.get_service_detail()),
        ("admin.get_md_admins", admin.get_md_admins()),
        # delivery (신규)
        ("delivery.get_warehouses", delivery.get_warehouses(1, 10)),
        ("delivery.get_area_fees", delivery.get_area_fees(1, 10)),
        ("delivery.get_deliveries", delivery.get_deliveries()),
        ("delivery.get_template_groups", delivery.get_template_groups()),
        # manage (신규)
        ("manage.get_inquiry_types", manage.get_inquiry_types()),
        ("manage.get_terms", manage.get_terms(["USE"])),
        # order_friends (신규)
        ("order_friends.get_settlement", of.get_settlement(end.year, end.month)),
        # promotion (신규)
        ("promotion.search_coupons", promotion.search_coupons(1, 10, "REGISTER_YMD", start, end)),
    ]

    print(f"\n읽기 전용 라이브 스모크 테스트 ({len(checks)}건)\n" + "=" * 70)
    for label, coro in checks:
        total += 1
        if await run(label, coro):
            ok += 1

    print("=" * 70)
    print(f"결과: {ok}/{total} 통과")


if __name__ == "__main__":
    asyncio.run(main())

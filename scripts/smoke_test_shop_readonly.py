"""shop API 공개(인증불필요) 클라이언트 라이브 스모크 — dev 몰(mommomdev) 대상.

분류:
  ✅ 200 + 모델 파싱 성공
  🟡 API 4xx (몰 미설정/파라미터 필요 등 — SDK 직렬화/경로는 정상)
  ❌ 모델 ValidationError(=모델 버그) 또는 5xx

실행: SHOPBY_SHOP_CLIENT_ID(.env.local) 필요.
  set -a; source .env.local; set +a; uv run python scripts/smoke_test_shop_readonly.py
"""

import asyncio
import os

import httpx
from pydantic import ValidationError

from shopby_sdk.shop.admin import ShopbyShopAdminApiClient
from shopby_sdk.shop.display import ShopbyShopDisplayApiClient
from shopby_sdk.shop.manage import ShopbyShopManageApiClient
from shopby_sdk.shop.marketing import ShopbyShopMarketingApiClient
from shopby_sdk.shop.member import ShopbyShopMemberApiClient
from shopby_sdk.shop.order import ShopbyShopOrderApiClient
from shopby_sdk.shop.product import ShopbyShopProductApiClient
from shopby_sdk.shop.promotion import ShopbyShopPromotionApiClient

KW = dict(
    client_id=os.environ["SHOPBY_SHOP_CLIENT_ID"],
    base_url=os.environ.get("SHOPBY_SHOP_BASE_URL"),
)

bug_count = 0


async def probe(label, coro):
    """단건 호출 분류."""
    global bug_count
    try:
        res = await coro
        n = len(res) if isinstance(res, list) else ""
        print(f"  ✅ {label}  -> {type(res).__name__}{f'[{len(res)}]' if isinstance(res, list) else ''}")
        return res
    except ValidationError as e:
        bug_count += 1
        print(f"  ❌MODEL {label}  -> ValidationError({e.error_count()}): {str(e).splitlines()[0][:140]}")
    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        mark = "🟡" if code < 500 else "❌"
        if code >= 500:
            bug_count += 1
        print(f"  {mark} {label}  -> HTTP {code}: {e.response.text[:90]}")
    except Exception as e:
        bug_count += 1
        print(f"  ❌ {label}  -> {type(e).__name__}: {str(e).splitlines()[0][:120]}")
    return None


async def main():
    print(f"=== shop 공개 API 스모크 (clientId={KW['client_id'][:6]}…, base={KW['base_url']}) ===")

    print("\n--- admin ---")
    a = ShopbyShopAdminApiClient(**KW)
    await probe("admin.get_malls", a.get_malls())
    await probe("admin.get_malls_internationalization", a.get_malls_internationalization())
    await probe("admin.get_service_basic_info", a.get_service_basic_info())
    await probe("admin.get_malls_ssl", a.get_malls_ssl())
    await probe("admin.get_malls_partners", a.get_malls_partners())

    print("\n--- order ---")
    o = ShopbyShopOrderApiClient(**KW)
    await probe("order.get_order_configuration", o.get_order_configuration())
    await probe("order.get_cart_configuration", o.get_cart_configuration())
    await probe("order.get_shippings_enums", o.get_shippings_enums())

    print("\n--- member ---")
    m = ShopbyShopMemberApiClient(**KW)
    await probe("member.get_member_grades", m.get_member_grades())
    await probe("member.get_member_groups", m.get_member_groups())
    await probe("member.get_member_extra_info_config", m.get_member_extra_info_config())
    await probe("member.get_profile_id_exist", m.get_profile_id_exist("nonexistent_test_id_xyz"))
    await probe("member.get_profile_nickname_exist", m.get_profile_nickname_exist("nonexist_nick_xyz"))

    print("\n--- product ---")
    p = ShopbyShopProductApiClient(**KW)
    await probe("product.get_favorite_keywords", p.get_favorite_keywords(size=5))
    await probe("product.get_custom_properties", p.get_custom_properties())
    await probe("product.get_naver_shopping_configuration", p.get_naver_shopping_configuration())
    await probe("product.get_brand_tree", p.get_brand_tree())
    search = await probe(
        "product.search_products", p.search_products(params={"pageNumber": 1, "pageSize": 5})
    )
    product_no = None
    if search is not None and getattr(search, "items", None):
        first = search.items[0]
        product_no = first.get("productNo") if isinstance(first, dict) else getattr(first, "product_no", None)
    print(f"  (검색된 product_no={product_no})")
    if product_no:
        await probe("product.get_product", p.get_product(product_no))
        await probe("product.get_product_options", p.get_product_options(product_no))
        await probe("product.get_public_infos", p.get_public_infos([product_no]))
        await probe("product.get_related_products", p.get_related_products(product_no))
        await probe("product.get_product_display_categories", p.get_product_display_categories(product_no))
        await probe("product.get_product_standard_category", p.get_product_standard_category(product_no))
        await probe("product.get_additional_discounts_by_product_no", p.get_additional_discounts_by_product_no(product_no))
        await probe("product.get_shipping_infos", p.get_shipping_infos([product_no]))
        await probe("product.get_products_options", p.get_products_options([product_no]))

    print("\n--- display ---")
    d = ShopbyShopDisplayApiClient(**KW)
    await probe("display.get_categories_by_keyword", d.get_categories_by_keyword())
    await probe("display.get_categories_simple_1depth", d.get_categories_simple_1depth())
    await probe("display.get_stickers", d.get_stickers())
    await probe("display.get_popups", d.get_popups())
    await probe("display.get_sections", d.get_sections())
    await probe("display.get_product_reviews_configurations", d.get_product_reviews_configurations())
    await probe("display.get_inquiries_configurations", d.get_inquiries_configurations())
    await probe("display.get_inquiries_tags", d.get_inquiries_tags())
    await probe("display.get_reviews_tags", d.get_reviews_tags())
    await probe("display.get_products_inquiries", d.get_products_inquiries(has_total_count=True, page_size=5))
    if product_no:
        await probe("display.get_product_reviews", d.get_product_reviews(product_no, page_size=5, has_total_count=True))
        await probe("display.get_products_photo_reviews", d.get_products_photo_reviews(str(product_no), page_size=5))
        await probe("display.get_product_inquiries", d.get_product_inquiries(product_no, page_size=5))
        await probe("display.get_events_by_product_no", d.get_events_by_product_no(product_no))

    print("\n--- promotion ---")
    pr = ShopbyShopPromotionApiClient(**KW)
    await probe("promotion.get_promotion_configs_coupon", pr.get_promotion_configs_coupon())
    if product_no:
        await probe("promotion.get_issuable_coupon_by_products", pr.get_issuable_coupon_by_products([product_no]))

    print("\n--- manage ---")
    mg = ShopbyShopManageApiClient(**KW)
    await probe("manage.get_inquiry_types", mg.get_inquiry_types())
    await probe("manage.get_inquiry_configuration", mg.get_inquiry_configuration())
    await probe("manage.get_board_config", mg.get_board_config())
    await probe("manage.search_addresses", mg.search_addresses(keyword="서울"))
    await probe("manage.search_holiday", mg.search_holiday())

    print("\n--- marketing ---")
    mk = ShopbyShopMarketingApiClient(**KW)
    if product_no:
        await probe("marketing.get_sns_share", mk.get_sns_share(product_no))

    print(f"\n=== 모델/서버 버그(❌) 총 {bug_count}건 ===")


if __name__ == "__main__":
    asyncio.run(main())

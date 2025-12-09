"""
상품 검색 예제

Usage:
    uv run --env-file .env.local python scripts/search_products.py [검색어]
"""

import asyncio
import os
import sys

from shopby_sdk.clients.products import ShopbyServerProductsApiClient


async def main():
    keywords = sys.argv[1] if len(sys.argv) > 1 else None

    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServerProductsApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    result = await client.search_products_v2(
        keywords=keywords,
        page_number=1,
        page_size=10,
    )

    print(f"총 {result.total_count}개 상품 검색됨")
    print("-" * 50)

    for item in result.items:
        print(f"[{item.mall_product_no}] {item.product_name} - {item.sale_price}원")


if __name__ == "__main__":
    asyncio.run(main())

"""
상품 상세 조회 예제 (Version 3.0)

Usage:
    uv run --env-file .env.local python scripts/get_product_detail_v3.py <mall_product_no>
"""

import asyncio
import os
import sys

from shopby_sdk.clients.products import ShopbyServerProductsApiClient


async def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/get_product_detail_v3.py <mall_product_no>")
        sys.exit(1)

    mall_product_no = int(sys.argv[1])

    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_SERVER_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SERVER_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServerProductsApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    product = await client.get_product_detail_v3(mall_product_no)
    print(f"상품명: {product.product_name}")
    print(f"판매상태: {product.sale_status_type}")
    print(f"판매가: {product.sale_price}")
    print(f"옵션 수: {len(product.options)}개")


if __name__ == "__main__":
    asyncio.run(main())

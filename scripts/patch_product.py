"""
상품 수정 예제

Usage:
    uv run --env-file .env.local python scripts/patch_product.py <product_no> <new_product_name>
"""

import asyncio
import os
import sys

from shopby_sdk.clients.products import ShopbyServerProductsApiClient
from shopby_sdk.clients.products.models import PatchProductV2Request


async def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/patch_product.py <product_no> <new_product_name>")
        sys.exit(1)

    product_no = int(sys.argv[1])
    new_name = sys.argv[2]

    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServerProductsApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    request = PatchProductV2Request(product_name=new_name)

    await client.patch_product_v2(product_no, request)
    print(f"상품 {product_no} 이름이 '{new_name}'으로 변경되었습니다.")


if __name__ == "__main__":
    asyncio.run(main())

"""
변경된 상품 조회 예제

Usage:
    uv run --env-file .env.local python scripts/get_changed_products.py
"""

import asyncio
import os
from datetime import datetime, timedelta

from shopby_sdk.clients.products import ShopbyServerProductsApiClient


async def main():
    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServerProductsApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    # 최근 7일간 수정된 상품 조회
    as_of = datetime.now() - timedelta(days=7)

    result = await client.get_changed_product_nos(
        as_of=as_of,
        sort_by="UPDATED_AT",
        size=50,
        direction="DESC",
    )

    print(f"최근 7일간 수정된 상품: {result.total_count}개")
    print("-" * 50)

    for item in result.items:
        print(f"상품번호: {item.mall_product_no}")


if __name__ == "__main__":
    asyncio.run(main())

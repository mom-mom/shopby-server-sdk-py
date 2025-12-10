"""
기획전 단건 조회 예제

Usage:
    uv run --env-file .env.local python scripts/get_event_detail.py <event_no>
"""

import asyncio
import os
import sys

from shopby_sdk.clients.display import ShopbyServerDisplayApiClient


async def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/get_event_detail.py <event_no>")
        sys.exit(1)

    event_no = int(sys.argv[1])

    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_SERVER_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SERVER_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServerDisplayApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    result = await client.get_event_detail(event_no)
    print(f"기획전명: {result.event_name}")
    print(f"기획전 유형: {result.event_type}")
    print(f"이벤트 여부: {result.event_yn}")
    print(f"등록일: {result.register_ymdt}")
    print(f"섹션 수: {len(result.event_sections)}개")

    if result.event_sections:
        print("\n=== 섹션 목록 ===")
        for section in result.event_sections:
            product_count = len(section.event_section_value.mall_products) if section.event_section_value else 0
            print(f"  - {section.event_section_name} (상품 {product_count}개)")


if __name__ == "__main__":
    asyncio.run(main())

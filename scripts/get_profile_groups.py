"""
회원의 그룹 조회

Usage:
    # 회원 번호로 조회
    uv run --env-file .env.local python scripts/get_profile_groups.py --member-no <member_no>

    # 회원 아이디로 조회
    uv run --env-file .env.local python scripts/get_profile_groups.py --member-id <member_id>
"""

import asyncio
import os
import sys

from shopby_sdk.clients.member import ShopbyServerMemberApiClient


async def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python scripts/get_profile_groups.py --member-no <member_no>")
        print("  python scripts/get_profile_groups.py --member-id <member_id>")
        sys.exit(1)

    option = sys.argv[1]
    value = sys.argv[2]

    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_SERVER_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SERVER_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServerMemberApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    if option == "--member-no":
        result = await client.get_profile_groups(member_no=int(value))
    elif option == "--member-id":
        result = await client.get_profile_groups(member_id=value)
    else:
        print(f"Unknown option: {option}")
        sys.exit(1)

    print(f"회원번호: {result.member_no}")
    print(f"소속 그룹 수: {len(result.items)}")
    print()

    for item in result.items:
        print(f"  - 그룹 #{item.member_group_no}: {item.member_group_name}")


if __name__ == "__main__":
    asyncio.run(main())

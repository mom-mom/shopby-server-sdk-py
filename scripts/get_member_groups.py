"""
회원 그룹 목록/단건 조회

Usage:
    # 전체 목록 조회
    uv run --env-file .env.local python scripts/get_member_groups.py

    # 단건 조회
    uv run --env-file .env.local python scripts/get_member_groups.py <group_no>
"""

import asyncio
import os
import sys

from shopby_sdk.clients.member import ShopbyServerMemberApiClient


async def main():
    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_SERVER_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SERVER_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServerMemberApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    if len(sys.argv) > 1:
        # 단건 조회
        group_no = int(sys.argv[1])
        group = await client.get_member_group(group_no)

        print(f"=== 회원 그룹 #{group.no} ===")
        print(f"  이름: {group.name}")
        print(f"  설명: {group.description}")
        print(f"  적립금 혜택 사용: {group.reserve_benefit.used}")
        print(f"  적립률: {group.reserve_benefit.reserve_rate}%")
    else:
        # 목록 조회
        groups = await client.get_member_groups()

        print(f"총 회원 그룹 수: {len(groups)}")
        print()

        for group in groups:
            print(f"=== 그룹 #{group.no}: {group.name} ===")
            print(f"  설명: {group.description}")
            print(f"  적립금 혜택: {'사용' if group.reserve_benefit.used else '미사용'}")
            if group.reserve_benefit.used:
                print(f"  적립률: {group.reserve_benefit.reserve_rate}%")
            print()


if __name__ == "__main__":
    asyncio.run(main())

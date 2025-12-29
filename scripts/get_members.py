"""
회원 목록 조회하기 V1.2

Usage:
    uv run --env-file .env.local python scripts/get_members.py [page_size]
"""

import asyncio
import os
import sys
from datetime import date, timedelta

from shopby_sdk.clients.member import ShopbyServerMemberApiClient


async def main():
    page_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10

    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_SERVER_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SERVER_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServerMemberApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    # 최근 30일간 가입한 회원 조회
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    result = await client.get_members(
        start_sign_up_date=start_date,
        end_sign_up_date=end_date,
        page_size=page_size,
        includes_count=True,
    )

    print(f"총 회원 수: {result.total_count}")
    print(f"조회된 회원 수: {len(result.contents)}")
    print(f"다음 페이지 조회용 lastId: {result.last_id}")
    print()

    for member in result.contents:
        print(f"=== 회원번호: {member.member_no} ===")
        print(f"  아이디: {member.member_id}")
        print(f"  이름: {member.member_name}")
        print(f"  이메일: {member.email}")
        print(f"  휴대폰: {member.mobile_no}")
        print(f"  상태: {member.member_status} ({member.member_status_name})")
        print(f"  등급: {member.member_grade_name}")
        print(f"  그룹: {member.member_group_name} ({member.member_group_count}개)")
        print(f"  가입일: {member.join_ymdt}")
        print(f"  최종로그인: {member.last_login_ymdt}")
        print()


if __name__ == "__main__":
    asyncio.run(main())

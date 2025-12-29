"""Member API 클라이언트"""

from datetime import date

import httpx

from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.member.models import (
    AddMemberToGroupResponse,
    MemberGroup,
    MemberSearchType,
    MembersListResponse,
    MemberStatus,
    MemberType,
    ProfileGroupsResponse,
)


class ShopbyServerMemberApiClient(ShopbyServerApiClient):
    """
    Shopby Member Server API 클라이언트

    쇼핑몰 회원(member) 관련 서버 API를 호출하는 클라이언트입니다.
    API 스펙: shopby-docs/member-server-public.yml
    """

    # ------------------------------------
    #  회원 목록 조회
    # ------------------------------------

    async def get_members(
        self,
        *,
        # 필수: 가입일자 또는 수정일자 중 하나는 반드시 입력
        start_sign_up_date: date | None = None,
        end_sign_up_date: date | None = None,
        start_update_date: date | None = None,
        end_update_date: date | None = None,
        # 선택 파라미터
        search_type: MemberSearchType | None = None,
        keywords: str | None = None,
        status: MemberStatus | None = None,
        member_type: MemberType | None = None,
        blacklisted: bool | None = None,
        email_agreed: bool | None = None,
        sms_agreed: bool | None = None,
        grade_no: int | None = None,
        group_no: int | None = None,
        # 마지막 로그인일자 (가입일자 필수)
        start_last_login_date: date | None = None,
        end_last_login_date: date | None = None,
        # V1.2 전용 파라미터
        includes_count: bool | None = None,
        search_after: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> MembersListResponse:
        """
        회원 목록 조회하기 V1.2

        회원 목록을 조회합니다.
        - 가입일자 또는 수정일자 중 하나는 반드시 입력해야 합니다.
        - 마지막 로그인일자 검색 시, 가입일자 기간을 필수로 입력해야 합니다.
        - includesCount를 false로 하면 조회 속도가 향상됩니다.
        - keySet search 방식: searchAfter 사용 (최초 조회 시 생략 가능, response의 lastId 값 사용)

        Args:
            start_sign_up_date: 가입일자 검색 시작일
            end_sign_up_date: 가입일자 검색 종료일
            start_update_date: 수정일자 검색 시작일
            end_update_date: 수정일자 검색 종료일
            search_type: 검색 유형 (기본값: USER_ID)
            keywords: 검색어 (최대 100개)
            status: 회원상태
            member_type: 회원타입
            blacklisted: 블랙리스트 여부
            email_agreed: 이메일 수신 동의 여부
            sms_agreed: SMS 수신 동의 여부
            grade_no: 등급 번호
            group_no: 그룹 번호
            start_last_login_date: 마지막 로그인일자 검색 시작일
            end_last_login_date: 마지막 로그인일자 검색 종료일
            includes_count: totalCount 포함 여부 (기본값: false)
            search_after: keySet search용 값 (response의 lastId 사용)
            page_number: 페이지 번호
            page_size: 페이지 크기 (기본 10, 최대 10000)

        Returns:
            MembersListResponse: 회원 목록 조회 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.2"}

            params: dict[str, str | int | bool] = {}

            # 날짜 파라미터 (yyyy-MM-dd 형식)
            if start_sign_up_date is not None:
                params["startSignUpDate"] = start_sign_up_date.isoformat()
            if end_sign_up_date is not None:
                params["endSignUpDate"] = end_sign_up_date.isoformat()
            if start_update_date is not None:
                params["startUpdateDate"] = start_update_date.isoformat()
            if end_update_date is not None:
                params["endUpdateDate"] = end_update_date.isoformat()
            if start_last_login_date is not None:
                params["startLastLoginDate"] = start_last_login_date.isoformat()
            if end_last_login_date is not None:
                params["endLastLoginDate"] = end_last_login_date.isoformat()

            # 검색 파라미터
            if search_type is not None:
                params["searchType"] = search_type
            if keywords is not None:
                params["keywords"] = keywords
            if status is not None:
                params["status"] = status
            if member_type is not None:
                params["type"] = member_type
            if blacklisted is not None:
                params["blacklisted"] = blacklisted
            if email_agreed is not None:
                params["emailAgreed"] = email_agreed
            if sms_agreed is not None:
                params["smsAgreed"] = sms_agreed
            if grade_no is not None:
                params["gradeNo"] = grade_no
            if group_no is not None:
                params["groupNo"] = group_no

            # V1.2 전용 파라미터
            if includes_count is not None:
                params["includesCount"] = str(includes_count).lower()
            if search_after is not None:
                params["searchAfter"] = search_after
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size

            resp = await client.get("/members", headers=headers, params=params)

            return self.handle_resp(resp, MembersListResponse)

    # ------------------------------------
    #  회원 그룹 API
    # ------------------------------------

    async def get_member_groups(self) -> list[MemberGroup]:
        """
        회원 그룹 목록 조회

        모든 회원 그룹 목록을 조회합니다.

        Returns:
            list[MemberGroup]: 회원 그룹 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get("/member-groups", headers=headers)
            resp.raise_for_status()

            return [MemberGroup.model_validate(item) for item in resp.json()]

    async def get_member_group(self, group_no: int) -> MemberGroup:
        """
        회원 그룹 단건 조회

        특정 회원 그룹의 상세 정보를 조회합니다.

        Args:
            group_no: 회원 그룹 번호

        Returns:
            MemberGroup: 회원 그룹 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get(f"/member-groups/{group_no}", headers=headers)

            return self.handle_resp(resp, MemberGroup)

    # ------------------------------------
    #  회원 프로필 그룹 API
    # ------------------------------------

    async def get_profile_groups(
        self,
        *,
        member_no: int | None = None,
        member_id: str | None = None,
    ) -> ProfileGroupsResponse:
        """
        회원의 그룹 조회

        특정 회원이 속한 그룹 목록을 조회합니다.
        member_no 또는 member_id 중 하나를 입력해야 합니다.

        Args:
            member_no: 회원 번호
            member_id: 회원 아이디

        Returns:
            ProfileGroupsResponse: 회원의 그룹 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int] = {}
            if member_no is not None:
                params["memberNo"] = member_no
            if member_id is not None:
                params["memberId"] = member_id

            resp = await client.get("/profile/groups", headers=headers, params=params)

            return self.handle_resp(resp, ProfileGroupsResponse)

    async def add_member_to_group(
        self,
        member_group_no: int,
        *,
        member_no: int | None = None,
        member_id: str | None = None,
    ) -> AddMemberToGroupResponse:
        """
        회원을 그룹에 추가하기

        특정 회원을 지정된 그룹에 추가합니다.
        member_no 또는 member_id 중 하나를 입력해야 합니다.

        Args:
            member_group_no: 회원 그룹 번호
            member_no: 회원 번호
            member_id: 회원 아이디

        Returns:
            AddMemberToGroupResponse: 추가된 회원 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body: dict[str, str | int] = {"memberGroupNo": member_group_no}
            if member_no is not None:
                body["memberNo"] = member_no
            if member_id is not None:
                body["memberId"] = member_id

            resp = await client.post("/profile/groups", headers=headers, json=body)

            return self.handle_resp(resp, AddMemberToGroupResponse)

    async def remove_member_from_group(
        self,
        member_group_no: int,
        *,
        member_no: int | None = None,
        member_id: str | None = None,
    ) -> None:
        """
        회원을 그룹에서 삭제하기

        특정 회원을 지정된 그룹에서 삭제합니다.
        member_no 또는 member_id 중 하나를 입력해야 합니다.

        Args:
            member_group_no: 회원 그룹 번호
            member_no: 회원 번호
            member_id: 회원 아이디
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int] = {"memberGroupNo": member_group_no}
            if member_no is not None:
                params["memberNo"] = member_no
            if member_id is not None:
                params["memberId"] = member_id

            resp = await client.delete("/profile/groups", headers=headers, params=params)
            resp.raise_for_status()

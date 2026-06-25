"""Member API 클라이언트"""

from datetime import date, datetime

import httpx

from shopby_sdk.base.kst import to_kst_string
from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.member.models import (
    AddMemberToGroupResponse,
    AppCardStoreIdRequest,
    BlockedReleaseRequest,
    BulkDeleteProfileRequest,
    CommonJoinConfigResponse,
    DormantMembersResponse,
    DormantReleaseRequest,
    ExpelledMember,
    ExternalMemberIdUpdateRequest,
    ExternalMemberRequest,
    ExternalMemberResponse,
    ExtraInfoConfigResponse,
    Grade,
    MemberGroup,
    MemberGroupRequest,
    MemberProhibitRequest,
    MemberProhibitResponse,
    MemberSearchType,
    MembersListResponse,
    MemberStatus,
    MemberType,
    OpenIdConfigResponse,
    OpenIdConfigUpdateRequest,
    PendingProviderRequest,
    ProfileGradesRequest,
    ProfileGradesResponse,
    ProfileGroupsResponse,
    ProfileResponse,
    ProfileUpdateRequest,
    ProfileBulkUpdateResponse,
    ProfileUpdateResponse,
    ProviderType,
)


class ShopbyServerMemberApiClient(ShopbyServerApiClient):
    """
    Shopby Member Server API 클라이언트

    쇼핑몰 회원(member) 관련 서버 API를 호출하는 클라이언트입니다.
    API 스펙: docs/api/member-server-public.yml
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

    # ------------------------------------
    #  Configuration (회원가입 / 간편로그인 설정) API
    # ------------------------------------

    async def get_common_join_config(self) -> CommonJoinConfigResponse:
        """
        회원가입항목 config 조회

        회원가입 시 노출/필수 여부 등 회원가입 항목 설정을 조회합니다.

        Returns:
            CommonJoinConfigResponse: 회원가입항목 config
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get("/configurations/member/common-join-config", headers=headers)

            return self.handle_resp(resp, CommonJoinConfigResponse)

    async def get_extra_info_config(self) -> ExtraInfoConfigResponse:
        """
        추가항목 config 조회

        회원정보 추가항목 설정을 조회합니다.

        Returns:
            ExtraInfoConfigResponse: 추가항목 config
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get("/configurations/member/extra-info-config", headers=headers)

            return self.handle_resp(resp, ExtraInfoConfigResponse)

    async def get_openid_config_by_provider(self, provider_type: ProviderType) -> OpenIdConfigResponse:
        """
        프로바이더별 간편회원가입 config 조회

        Args:
            provider_type: 프로바이더 타입 (PAYCO, NAVER, KAKAO, KAKAO_SYNC, FACEBOOK, LINE, APPLE, GOOGLE)

        Returns:
            OpenIdConfigResponse: 간편회원가입 config
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get(f"/configurations/member/open-id/{provider_type}", headers=headers)

            return self.handle_resp(resp, OpenIdConfigResponse)

    async def update_openid_config_by_provider(
        self,
        provider_type: ProviderType,
        request: OpenIdConfigUpdateRequest,
    ) -> None:
        """
        프로바이더별 간편회원가입 config 수정

        Args:
            provider_type: 프로바이더 타입 (PAYCO, NAVER, KAKAO, KAKAO_SYNC, FACEBOOK, LINE, APPLE, GOOGLE, APP_CARD)
            request: 수정할 config 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.patch(
                f"/configurations/member/open-id/{provider_type}", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    async def delete_openid_provider_client_secret(self, provider_type: ProviderType) -> None:
        """
        간편 회원가입 프로바이더 clientId, secretKey 제거

        Args:
            provider_type: 프로바이더 타입 (PAYCO, NAVER, KAKAO, KAKAO_SYNC, FACEBOOK, LINE, APPLE, GOOGLE, APP_CARD)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.delete(
                f"/configurations/member/open-id/{provider_type}", headers=headers
            )
            self.raise_for_status(resp)
            return None

    async def patch_app_card_store_id(self, request: AppCardStoreIdRequest) -> None:
        """
        앱카드 storeId 수정

        Args:
            request: 수정할 앱카드 storeId 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.patch("/configurations/member/app-card", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def patch_open_id_pending_provider(self, request: PendingProviderRequest) -> None:
        """
        간편회원 로그인 일시중지 프로바이더 추가/제거

        Args:
            request: 프로바이더 및 액션(ADD/REMOVE) 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.patch(
                "/configurations/member/open-id/pending-provider", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  회원등급 API
    # ------------------------------------

    async def get_grades(self) -> list[Grade]:
        """
        회원등급 목록 조회하기

        Returns:
            list[Grade]: 회원등급 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get("/grades", headers=headers)

            return self.handle_resp(resp, list[Grade])

    async def update_profile_grades(self, request: ProfileGradesRequest) -> ProfileGradesResponse:
        """
        회원등급 수정하기

        회원들의 회원등급을 수정합니다. (최대 1000명)

        Args:
            request: 변경 등급 및 대상 회원 목록

        Returns:
            ProfileGradesResponse: 등급 변경완료 회원번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/profile/grades", headers=headers, json=body)

            return self.handle_resp(resp, ProfileGradesResponse)

    # ------------------------------------
    #  회원 그룹 생성/수정/삭제 API
    # ------------------------------------

    async def create_member_group(self, request: MemberGroupRequest) -> None:
        """
        회원 그룹 생성

        Args:
            request: 생성할 회원 그룹 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/member-groups", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def update_member_group(self, group_no: int, request: MemberGroupRequest) -> None:
        """
        회원 그룹 수정

        Args:
            group_no: 회원 그룹 번호
            request: 수정할 회원 그룹 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(f"/member-groups/{group_no}", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def delete_member_group(self, group_no: int) -> None:
        """
        회원 그룹 삭제

        Args:
            group_no: 회원 그룹 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.delete(f"/member-groups/{group_no}", headers=headers)
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  회원 목록/탈퇴/외부연동/정지 API
    # ------------------------------------

    async def post_members(
        self,
        status: MemberStatus,
        *,
        search_type: MemberSearchType | None = None,
        keywords: list[str] | None = None,
        start_sign_up_date_time: datetime | None = None,
        end_sign_up_date_time: datetime | None = None,
        start_update_date_time: datetime | None = None,
        end_update_date_time: datetime | None = None,
        start_last_login_date_time: datetime | None = None,
        end_last_login_date_time: datetime | None = None,
        start_grade_update_date_time: datetime | None = None,
        end_grade_update_date_time: datetime | None = None,
        member_type: MemberType | None = None,
        blacklisted: bool | None = None,
        email_agreed: bool | None = None,
        sms_agreed: bool | None = None,
        grade_no: int | None = None,
        group_no: int | None = None,
        search_after: str | None = None,
        includes_count: bool | None = None,
        page_size: int | None = None,
    ) -> MembersListResponse:
        """
        회원 목록 조회하기 V1.3 (POST, Elasticsearch 기반)

        - status는 필수입니다. (WAITING, ACTIVE, PAUSED, PENDING 중 하나)
        - keywords는 배열로 전달합니다. (최대 1000개)
        - 날짜는 LocalDateTime(yyyy-MM-dd HH:mm:ss)으로 전달합니다.
        - keySet 방식 페이징만 지원합니다. (searchAfter 사용, pageSize 최대 500)

        Args:
            status: 회원상태 (필수)
            search_type: 검색 유형 (미입력 시 키워드 검색 제외)
            keywords: 검색어 배열 (최대 1000개)
            start_sign_up_date_time: 가입일시 검색 시작
            end_sign_up_date_time: 가입일시 검색 종료
            start_update_date_time: 수정일시 검색 시작
            end_update_date_time: 수정일시 검색 종료
            start_last_login_date_time: 마지막 로그인일시 검색 시작
            end_last_login_date_time: 마지막 로그인일시 검색 종료
            start_grade_update_date_time: 등급변경일시 검색 시작
            end_grade_update_date_time: 등급변경일시 검색 종료
            member_type: 회원타입
            blacklisted: 블랙리스트 여부
            email_agreed: 이메일 수신 동의 여부
            sms_agreed: SMS 수신 동의 여부
            grade_no: 등급 번호
            group_no: 그룹 번호
            search_after: keySet 커서 값 (이전 응답의 lastId)
            includes_count: totalCount 포함 여부 (기본 false)
            page_size: 페이지 사이즈 (기본 10, 최대 500)

        Returns:
            MembersListResponse: 회원 목록 조회 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.3"}

            body: dict = {"status": status}
            if search_type is not None:
                body["searchType"] = search_type
            if keywords is not None:
                body["keywords"] = keywords
            if start_sign_up_date_time is not None:
                body["startSignUpDateTime"] = to_kst_string(start_sign_up_date_time)
            if end_sign_up_date_time is not None:
                body["endSignUpDateTime"] = to_kst_string(end_sign_up_date_time)
            if start_update_date_time is not None:
                body["startUpdateDateTime"] = to_kst_string(start_update_date_time)
            if end_update_date_time is not None:
                body["endUpdateDateTime"] = to_kst_string(end_update_date_time)
            if start_last_login_date_time is not None:
                body["startLastLoginDateTime"] = to_kst_string(start_last_login_date_time)
            if end_last_login_date_time is not None:
                body["endLastLoginDateTime"] = to_kst_string(end_last_login_date_time)
            if start_grade_update_date_time is not None:
                body["startGradeUpdateDateTime"] = to_kst_string(start_grade_update_date_time)
            if end_grade_update_date_time is not None:
                body["endGradeUpdateDateTime"] = to_kst_string(end_grade_update_date_time)
            if member_type is not None:
                body["type"] = member_type
            if blacklisted is not None:
                body["blacklisted"] = blacklisted
            if email_agreed is not None:
                body["emailAgreed"] = email_agreed
            if sms_agreed is not None:
                body["smsAgreed"] = sms_agreed
            if grade_no is not None:
                body["gradeNo"] = grade_no
            if group_no is not None:
                body["groupNo"] = group_no
            if search_after is not None:
                body["searchAfter"] = search_after
            if includes_count is not None:
                body["includesCount"] = includes_count
            if page_size is not None:
                body["pageSize"] = page_size

            resp = await client.post("/members", headers=headers, json=body)

            return self.handle_resp(resp, MembersListResponse)

    async def get_expelled_members(
        self,
        target_date: date,
        *,
        member_type: MemberType | None = None,
        additional_info_used: bool | None = None,
    ) -> list[ExpelledMember]:
        """
        탈퇴 회원 조회하기 V1.1

        특정 날짜에 탈퇴한 회원을 조회합니다.
        (회원 탈퇴 후 5일이 지나면 정보가 파기됩니다.)

        Args:
            target_date: 회원 탈퇴일시 (yyyy-MM-dd)
            member_type: 회원 타입
            additional_info_used: 추가 정보 사용 여부

        Returns:
            list[ExpelledMember]: 탈퇴 회원 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.1"}

            params: dict[str, str | bool] = {"targetDate": target_date.strftime("%Y-%m-%d")}
            if member_type is not None:
                params["memberType"] = member_type
            if additional_info_used is not None:
                params["additionalInfoUsed"] = additional_info_used

            resp = await client.get("/members/expelled-members", headers=headers, params=params)

            return self.handle_resp(resp, list[ExpelledMember])

    async def create_external_member(self, request: ExternalMemberRequest) -> ExternalMemberResponse:
        """
        외부회원연동 회원가입

        자체회원연동(외부회원연동)을 사용하는 몰의 회원을 직접 가입시킵니다.

        Args:
            request: 외부회원 정보

        Returns:
            ExternalMemberResponse: 가입된 회원 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/members/external", headers=headers, json=body)

            return self.handle_resp(resp, ExternalMemberResponse)

    async def update_external_member_id(self, request: ExternalMemberIdUpdateRequest) -> None:
        """
        외부회원 아이디 변경

        Args:
            request: 현재/변경할 Oauth ID 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/members/external/id", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def prohibit_members(self, request: MemberProhibitRequest) -> MemberProhibitResponse:
        """
        회원 이용 정지

        회원을 이용 정지(또는 정지 해제)시킵니다.

        Args:
            request: 정지 대상 회원 및 정지 정보

        Returns:
            MemberProhibitResponse: 처리 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/members/prohibit", headers=headers, json=body)

            return self.handle_resp(resp, MemberProhibitResponse)

    # ------------------------------------
    #  회원 정보(Profile) API
    # ------------------------------------

    async def get_profile(
        self,
        *,
        member_id: str | None = None,
        member_no: int | None = None,
        oauth_id_no: str | None = None,
        email: str | None = None,
        representative_member_no: int | None = None,
    ) -> ProfileResponse:
        """
        회원 정보 조회하기

        memberId, memberNo, oauthIdNo, email, representativeMemberNo 중 하나로 조회합니다.

        Args:
            member_id: 아이디
            member_no: 회원 번호
            oauth_id_no: oauth 인증번호
            email: 이메일
            representative_member_no: 대표몰회원번호

        Returns:
            ProfileResponse: 회원 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int] = {}
            if member_id is not None:
                params["memberId"] = member_id
            if member_no is not None:
                params["memberNo"] = member_no
            if oauth_id_no is not None:
                params["oauthIdNo"] = oauth_id_no
            if email is not None:
                params["email"] = email
            if representative_member_no is not None:
                params["representativeMemberNo"] = representative_member_no

            resp = await client.get("/profile", headers=headers, params=params)

            return self.handle_resp(resp, ProfileResponse)

    async def update_profile(self, request: ProfileUpdateRequest) -> ProfileUpdateResponse:
        """
        회원 정보 수정하기

        Args:
            request: 수정할 회원 정보

        Returns:
            ProfileUpdateResponse: 수정된 회원 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/profile", headers=headers, json=body)

            return self.handle_resp(resp, ProfileUpdateResponse)

    async def delete_profile(
        self,
        *,
        member_id: str | None = None,
        member_no: int | None = None,
        oauth_id_no: str | None = None,
    ) -> None:
        """
        회원 탈퇴 시키기

        memberNo, memberId, oauthIdNo 중 하나는 필수입니다.

        Args:
            member_id: 회원 아이디
            member_no: 회원 번호
            oauth_id_no: oauth 인증 일련번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int] = {}
            if member_id is not None:
                params["memberId"] = member_id
            if member_no is not None:
                params["memberNo"] = member_no
            if oauth_id_no is not None:
                params["oauthIdNo"] = oauth_id_no

            resp = await client.delete("/profile", headers=headers, params=params)
            self.raise_for_status(resp)
            return None

    async def restore_profile(
        self,
        *,
        member_id: str | None = None,
        member_no: int | None = None,
        oauth_id_no: str | None = None,
    ) -> None:
        """
        회원 탈퇴 철회시키기

        memberNo, memberId, oauthIdNo 중 하나는 필수입니다.
        (이미 삭제된 회원인 경우 철회가 불가능합니다.)

        Args:
            member_id: 회원 아이디
            member_no: 회원 번호
            oauth_id_no: oauth 인증 일련번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int] = {}
            if member_id is not None:
                params["memberId"] = member_id
            if member_no is not None:
                params["memberNo"] = member_no
            if oauth_id_no is not None:
                params["oauthIdNo"] = oauth_id_no

            resp = await client.put("/profile/restore", headers=headers, params=params)
            self.raise_for_status(resp)
            return None

    async def logout_profile(
        self,
        *,
        member_no: int | None = None,
        oauth_id_no: str | None = None,
    ) -> None:
        """
        회원 로그아웃 시키기

        회원번호 혹은 oauthId 둘 중 하나는 존재해야 합니다.

        Args:
            member_no: 회원 번호
            oauth_id_no: oauth 인증 일련번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int] = {}
            if member_no is not None:
                params["memberNo"] = member_no
            if oauth_id_no is not None:
                params["oauthIdNo"] = oauth_id_no

            resp = await client.delete("/profile/logout", headers=headers, params=params)
            self.raise_for_status(resp)
            return None

    async def bulk_update_profile(
        self, requests: list[ProfileUpdateRequest]
    ) -> ProfileBulkUpdateResponse:
        """
        대량 회원 정보 수정하기

        최대 1000명의 회원까지 가능합니다.

        Args:
            requests: 수정할 회원 정보 목록

        Returns:
            ProfileBulkUpdateResponse: 수정된 회원 번호 목록 (memberNos)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = [item.model_dump(by_alias=True, exclude_none=True, mode="json") for item in requests]
            resp = await client.put("/profile/bulk", headers=headers, json=body)

            return self.handle_resp(resp, ProfileBulkUpdateResponse)

    async def bulk_delete_profile(self, request: BulkDeleteProfileRequest) -> None:
        """
        복수의 회원 탈퇴 처리하기

        최대 500명의 회원을 동시에 탈퇴시킵니다.

        Args:
            request: 탈퇴시킬 회원 번호 리스트
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/profile/bulk-delete", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def release_blocked_member(self, request: BlockedReleaseRequest) -> None:
        """
        차단 회원 해제

        차단자가 차단한 회원을 차단 해제합니다.
        targetMemberNo 혹은 targetMemberId 둘 중 하나는 존재해야 합니다.

        Args:
            request: 차단자 및 차단 대상 회원 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/profile/blocked-release", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  휴면 회원 API
    # ------------------------------------

    async def get_dormant_members(
        self,
        start_dormant_date: date,
        end_dormant_date: date,
        *,
        page: int | None = None,
        size: int | None = None,
    ) -> DormantMembersResponse:
        """
        휴면 회원 조회하기 V1.1

        Args:
            start_dormant_date: 휴면전환일시 검색 시작일 (yyyy-MM-dd)
            end_dormant_date: 휴면전환일시 검색 종료일 (yyyy-MM-dd)
            page: 페이지 번호 (1 based index)
            size: 페이지 사이즈

        Returns:
            DormantMembersResponse: 휴면 회원 조회 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.1"}

            params: dict[str, str | int] = {
                "startDormantDate": start_dormant_date.strftime("%Y-%m-%d"),
                "endDormantDate": end_dormant_date.strftime("%Y-%m-%d"),
            }
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size

            resp = await client.get("/profile/dormant", headers=headers, params=params)

            return self.handle_resp(resp, DormantMembersResponse)

    async def convert_dormant_member(
        self,
        *,
        member_id: str | None = None,
        member_no: int | None = None,
    ) -> None:
        """
        휴면 회원 전환하기

        회원을 휴면 회원으로 전환합니다.

        Args:
            member_id: 회원 아이디
            member_no: 회원 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int] = {}
            if member_id is not None:
                params["memberId"] = member_id
            if member_no is not None:
                params["memberNo"] = member_no

            resp = await client.put("/profile/dormant", headers=headers, params=params)
            self.raise_for_status(resp)
            return None

    async def release_dormant_member(self, request: DormantReleaseRequest) -> None:
        """
        휴면 회원 해제

        회원의 휴면 상태를 해제합니다.
        회원 아이디 혹은 회원번호 둘 중 하나는 존재해야 합니다.

        Args:
            request: 회원 아이디/번호 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/profile/dormant-release", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

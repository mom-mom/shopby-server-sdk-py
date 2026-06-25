"""Shopby Shop(Client) Member API 클라이언트.

shop-api(`https://shop-api.e-ncp.com`) member 도메인의 공개(인증 불필요) 엔드포인트를
호출한다. 회원 토큰(accessToken / Shop-By-Authorization)은 전송하지 않으며,
clientId/platform/language 헤더는 base(`ShopbyShopApiClient`)가 주입한다.

대응 OpenAPI 스펙: docs/api/member-shop-public.yml
"""

import httpx

from shopby_sdk.shop.base import ShopbyShopApiClient
from shopby_sdk.shop.member.models import (
    BusinessExistResponse,
    ExternalMemberExistRequest,
    ExternalMemberExistResponse,
    MemberExtraInfoConfigResponse,
    MemberExtraInfosResponse,
    MemberGrade,
    MemberGroup,
    ProfileExistResponse,
    ProfileMobileExistResponse,
)


class ShopbyShopMemberApiClient(ShopbyShopApiClient):
    """Shopby Shop(Client) Member API 클라이언트.

    쇼핑몰 회원(member) 관련 공개 shop API 를 호출하는 클라이언트.
    """

    # ------------------------------------------------------------------
    #  Company
    # ------------------------------------------------------------------

    async def check_duplicated_business(self, registration: str) -> BusinessExistResponse:
        """사업자회원 사업자등록번호 중복체크 (Version 1.0).

        Args:
            registration: 사업자등록번호 (10자리)

        Returns:
            BusinessExistResponse: 중복 여부
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"registration": registration}
            resp = await client.get("/companies/business-exist", headers=headers, params=params)
            return self.handle_resp(resp, BusinessExistResponse)

    # ------------------------------------------------------------------
    #  Member-Config
    # ------------------------------------------------------------------

    async def get_member_extra_info_config(self) -> MemberExtraInfoConfigResponse:
        """회원정보 추가항목 Config 조회 (Version 1.0).

        Returns:
            MemberExtraInfoConfigResponse: 회원정보 추가항목 설정
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/config/member-extra-info", headers=headers)
            return self.handle_resp(resp, MemberExtraInfoConfigResponse)

    # ------------------------------------------------------------------
    #  Member-Grade
    # ------------------------------------------------------------------

    async def get_member_grades(self, *, grade_nos: list[int] | None = None) -> list[MemberGrade]:
        """회원 등급 정보 조회하기 (Version 1.0).

        Args:
            grade_nos: 회원 등급 번호 리스트. 미입력 시 쇼핑몰의 모든 등급 조회.

        Returns:
            list[MemberGrade]: 회원 등급 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {}
            if grade_nos is not None:
                params["gradeNos"] = ",".join(str(no) for no in grade_nos)
            resp = await client.get("/member-grades", headers=headers, params=params)
            return self.handle_resp(resp, list[MemberGrade])

    # ------------------------------------------------------------------
    #  Member-Group
    # ------------------------------------------------------------------

    async def get_member_groups(self, *, group_nos: list[int] | None = None) -> list[MemberGroup]:
        """회원 그룹 정보 조회하기 (Version 1.0).

        Args:
            group_nos: 회원 그룹 번호 리스트. 미입력 시 쇼핑몰의 모든 그룹 조회.

        Returns:
            list[MemberGroup]: 회원 그룹 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {}
            if group_nos is not None:
                params["groupNos"] = ",".join(str(no) for no in group_nos)
            resp = await client.get("/member-groups", headers=headers, params=params)
            return self.handle_resp(resp, list[MemberGroup])

    # ------------------------------------------------------------------
    #  Profile — 중복/검증 확인
    # ------------------------------------------------------------------

    async def get_profile_email_exist(
        self,
        email: str,
        *,
        member_types: list[str] | None = None,
    ) -> ProfileExistResponse:
        """해당 쇼핑몰에 이메일 중복여부 체크하기 (Version 1.0).

        Args:
            email: 회원 이메일 주소
            member_types: 회원 유형 리스트 (MALL/SYNC_ID/OPEN_ID). 미입력 시 MALL.

        Returns:
            ProfileExistResponse: 중복 여부 및 회원 상태
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {"email": email}
            if member_types is not None:
                params["memberTypes"] = ",".join(member_types)
            resp = await client.get("/profile/email/exist", headers=headers, params=params)
            return self.handle_resp(resp, ProfileExistResponse)

    async def get_profile_id_exist(self, member_id: str) -> ProfileExistResponse:
        """해당 쇼핑몰에 아이디 중복여부 체크하기 (Version 1.0).

        Args:
            member_id: 회원 ID

        Returns:
            ProfileExistResponse: 중복 여부 및 회원 상태
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"memberId": member_id}
            resp = await client.get("/profile/id/exist", headers=headers, params=params)
            return self.handle_resp(resp, ProfileExistResponse)

    async def get_profile_nickname_exist(self, nickname: str) -> ProfileExistResponse:
        """해당 쇼핑몰에 닉네임 중복여부 체크하기 (Version 1.0).

        Args:
            nickname: 회원 닉네임

        Returns:
            ProfileExistResponse: 중복 여부 및 회원 상태
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"nickname": nickname}
            resp = await client.get("/profile/nickname/exist", headers=headers, params=params)
            return self.handle_resp(resp, ProfileExistResponse)

    async def get_profile_mobile_exist(self, mobile_no: str) -> ProfileMobileExistResponse:
        """해당 쇼핑몰에 휴대폰 번호 중복여부 확인하기 (Version 1.0).

        Args:
            mobile_no: 휴대전화 번호

        Returns:
            ProfileMobileExistResponse: 번호 존재 여부, 회원 상태, 마스킹된 회원 ID
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"mobileNo": mobile_no}
            resp = await client.get("/profile/mobile/exist", headers=headers, params=params)
            return self.handle_resp(resp, ProfileMobileExistResponse)

    async def get_profile_member_equals_with_email(
        self,
        member_id: str,
        member_name: str,
        email: str,
    ) -> ProfileExistResponse:
        """해당 쇼핑몰 아이디, 이름, 이메일 검증하기 (Version 1.0).

        입력한 아이디/이름/이메일과 동일한 회원 존재 여부를 확인한다.

        Args:
            member_id: 아이디
            member_name: 이름
            email: 이메일

        Returns:
            ProfileExistResponse: 일치 회원 존재 여부
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"memberId": member_id, "memberName": member_name, "email": email}
            resp = await client.get(
                "/profile/member/equals/with-email", headers=headers, params=params
            )
            return self.handle_resp(resp, ProfileExistResponse)

    async def get_profile_member_equals_with_mobile(
        self,
        member_id: str,
        member_name: str,
        mobile_no: str,
    ) -> ProfileExistResponse:
        """해당 쇼핑몰 아이디, 이름, 휴대폰 번호 검증하기 (Version 1.0).

        입력한 아이디/이름/휴대폰 번호와 동일한 회원 존재 여부를 확인한다.

        Args:
            member_id: 아이디
            member_name: 이름
            mobile_no: 휴대폰 번호

        Returns:
            ProfileExistResponse: 일치 회원 존재 여부
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"memberId": member_id, "memberName": member_name, "mobileNo": mobile_no}
            resp = await client.get(
                "/profile/member/equals/with-mobile", headers=headers, params=params
            )
            return self.handle_resp(resp, ProfileExistResponse)

    # ------------------------------------------------------------------
    #  Profile — 회원별 추가항목 조회
    # ------------------------------------------------------------------

    async def get_extra_info_members(self, member_nos: list[int]) -> MemberExtraInfosResponse:
        """회원별 추가항목 조회 (Version 1.0).

        추가항목 공개여부가 Y 인 항목만 조회된다.

        Args:
            member_nos: 회원 번호 목록

        Returns:
            MemberExtraInfosResponse: 회원별 추가항목 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"memberNos": ",".join(str(no) for no in member_nos)}
            resp = await client.get("/profile/member/extra-infos", headers=headers, params=params)
            return self.handle_resp(resp, MemberExtraInfosResponse)

    # ------------------------------------------------------------------
    #  Profile — 외부회원 중복확인
    # ------------------------------------------------------------------

    async def post_profile_external_member_exists(
        self, request: ExternalMemberExistRequest
    ) -> ExternalMemberExistResponse:
        """외부회원 중복확인하기 (Version 1.0).

        전달한 openAccessToken 에 해당하는 회원이 이미 가입되어 있는지 확인한다.
        외부회원연동을 사용하는 몰에서만 사용 가능.

        Args:
            request: 외부회원(IdP) 엑세스 토큰 정보

        Returns:
            ExternalMemberExistResponse: 중복확인 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/profile/external-member/exist", headers=headers, json=body)
            return self.handle_resp(resp, ExternalMemberExistResponse)

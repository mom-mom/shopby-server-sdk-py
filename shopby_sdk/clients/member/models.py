"""Member API 모델 정의"""

from typing import Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime

# ------------------------------------
#  Request Enum 타입 정의
# ------------------------------------

MemberSearchType = Literal[
    "MEMBER_NO",
    "USER_ID",
    "EMAIL",
    "MOBILE",
    "NAME",
    "NICKNAME",
]
"""회원 검색 유형"""

MemberStatus = Literal[
    "WAITING",
    "ACTIVE",
    "WITHDRAWN",
    "FREEZE",
    "DORMANT",
    "PAUSED",
    "PENDING",
]
"""회원 상태 (WAITING: 가입대기, ACTIVE: 가입완료, WITHDRAWN: 탈퇴, FREEZE/DORMANT: 휴면, PAUSED: 일시정지, PENDING: 승인대기)"""

MemberType = Literal[
    "MALL",
    "SYNC_ID",
    "OPEN_ID",
]
"""회원 타입 (MALL: 일반회원, SYNC_ID: 연동형회원, OPEN_ID: 간편로그인회원)"""

ProviderType = Literal[
    "PAYCO",
    "NAVER",
    "KAKAO",
    "KAKAO_SYNC",
    "FACEBOOK",
    "LINE",
    "APPLE",
    "GOOGLE",
    "APP_CARD",
    "IAMSCHOOL",
    "UNIONE",
    "NCPSTORE",
]
"""SNS 프로바이더 타입"""


# ------------------------------------
#  회원 그룹 관련 모델
# ------------------------------------


class ReserveBenefit(BaseDto):
    """적립금 혜택 정보"""

    used: bool = Field(..., description="적립금 혜택 사용 여부")
    reserve_rate: float = Field(..., description="적립금 혜택 적립률")


class MemberGroup(BaseDto):
    """
    회원 그룹 정보

    OpenAPI Schema: member-groups-groupNo-1944155955
    """

    no: int = Field(..., description="회원 그룹 번호")
    name: str = Field(..., description="회원 그룹 이름")
    description: str = Field(..., description="회원 그룹 상세 설명")
    reserve_benefit: ReserveBenefit = Field(..., description="적립금 혜택 정보")


# ------------------------------------
#  회원 프로필 그룹 관련 모델
# ------------------------------------


class ProfileGroupItem(BaseDto):
    """회원의 그룹 항목"""

    member_group_no: int = Field(..., description="회원 그룹 번호")
    member_group_name: str = Field(..., description="회원 그룹 이름")


class ProfileGroupsResponse(BaseDto):
    """
    회원의 그룹 조회 응답

    OpenAPI Schema: profile-groups-1410096186
    """

    member_no: int = Field(..., description="회원 번호")
    items: list[ProfileGroupItem] = Field(default_factory=list, description="회원 그룹 목록")


class AddMemberToGroupRequest(BaseDto):
    """
    회원을 그룹에 추가하기 요청

    OpenAPI Schema: profile-groups-1583052347
    """

    member_group_no: int = Field(..., description="회원 그룹 번호")
    member_no: int | None = Field(None, description="회원 번호 (memberId와 배타적)")
    member_id: str | None = Field(None, description="회원 아이디 (memberNo와 배타적)")


class AddMemberToGroupResponse(BaseDto):
    """
    회원을 그룹에 추가하기 응답

    OpenAPI Schema: profile-groups-64494364
    """

    member_no: int = Field(..., description="회원 번호")


# ------------------------------------
#  회원 목록 관련 모델
# ------------------------------------


class OpenIdProvider(BaseDto):
    """연동된 오픈아이디 정보"""

    provider: str | None = Field(None, description="오픈아이디 프로바이더명")
    oauth_id_no: int | None = Field(None, description="OAuth ID 번호")


class Member(BaseDto):
    """회원 정보"""

    member_no: int = Field(..., description="회원번호")
    member_id: str = Field(..., description="아이디")
    member_name: str = Field(..., description="이름")
    first_name: str = Field(..., description="이름(성 제외)")
    last_name: str = Field(..., description="성")
    nickname: str = Field(..., description="닉네임")
    email: str | None = Field(None, description="이메일")
    mobile_no: str = Field(..., description="휴대전화번호")
    mobile_country_code: str | None = Field(None, description="국제전화번호 코드")
    phone_no: str = Field(..., description="전화번호")
    birthday: str | None = Field(None, description="생년월일")
    sex: str = Field(..., description="성별 (M/F)")

    # 주소 정보
    country_code: str = Field(..., description="거주 국가")
    zip_code: str | None = Field(None, description="우편번호")
    address: str | None = Field(None, description="도로명 주소")
    detail_address: str | None = Field(None, description="도로명 상세주소")
    jibun_address: str | None = Field(None, description="지번주소")
    jibun_detail_address: str | None = Field(None, description="지번 상세주소")
    city: str | None = Field(None, description="도시")
    state: str | None = Field(None, description="국내: 군/구, 해외: 주")

    # 회원 상태/등급/그룹
    member_status: MemberStatus = Field(..., description="회원 상태")
    member_status_name: str | None = Field(None, description="회원 상태 표기명")
    member_type: MemberType = Field(..., description="회원 타입")
    member_grade_name: str = Field(..., description="회원등급명")
    member_group_name: str | None = Field(None, description="회원그룹명")
    member_group_count: int = Field(..., description="회원그룹 갯수")

    # SNS/연동 정보
    provider_type: ProviderType | None = Field(None, description="마지막 연동 SNS")
    provider_type_label: str = Field(..., description="연동 SNS 명")
    member_provider: str | None = Field(None, description="회원 OpenID")
    open_id_providers: list[OpenIdProvider] = Field(default_factory=list, description="연동된 오픈아이디 리스트")
    linked: bool = Field(..., description="회원 연동여부")
    linked_yn: Literal["Y", "N"] = Field(..., description="회원 연동여부 (Y/N)")
    link_ymdt: KstDatetime | None = Field(None, description="회원 연동일자")

    # 일시/로그인 정보
    join_ymdt: KstDatetime = Field(..., description="회원가입일자")
    last_login_ymdt: KstDatetime | None = Field(None, description="최종로그인일자")
    last_update_ymdt: KstDatetime | None = Field(None, description="최종업데이트일자")
    login_count: int = Field(..., description="로그인 횟수")

    # 동의 정보
    is_push_notification_agreed: bool = Field(..., description="푸시 알림 동의 여부")
    is_sms_agreed: bool = Field(..., description="SMS 알림 동의 여부")
    is_direct_mail_agreed: bool = Field(..., description="이메일 알림 동의 여부")

    # 기타
    representative_member_no: int | None = Field(None, description="대표몰 회원번호")


class MembersListResponse(BaseDto):
    """
    회원 목록 조회 응답

    OpenAPI Schema: members-1662571364
    """

    contents: list[Member] = Field(..., description="조회 결과")
    total_count: int | None = Field(None, description="총 개수 (includesCount=true일 때만 포함)")
    last_id: str | None = Field(None, description="마지막 ID (다음 페이지 조회용)")

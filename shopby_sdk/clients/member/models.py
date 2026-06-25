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


# ====================================================================
#  추가 Enum 타입 정의
# ====================================================================

JoinConfigItemStatus = Literal["USED", "NOT_USED", "REQUIRED"]
"""회원가입 항목 설정 상태 (USED: 사용, NOT_USED: 미사용, REQUIRED: 필수)"""

PendingProviderAction = Literal["ADD", "REMOVE"]
"""간편회원 로그인 일시중지 프로바이더 추가/제거 액션"""

ProhibitStatus = Literal["PAUSED", "BLOCKED"]
"""회원 이용정지 시 변경할 상태 (PAUSED: 일시정지, BLOCKED: 영구정지)"""

NotificationType = Literal["KAKAO", "SMS", "EMAIL", "ALL"]
"""회원 이용정지 알림 종류"""

JoinTermsAgreementType = Literal[
    "MALL_INTRODUCTION",
    "USE",
    "E_COMMERCE",
    "PI_PROCESS",
    "PI_COLLECTION_AND_USE_REQUIRED",
    "PI_COLLECTION_AND_USE_OPTIONAL",
    "PI_PROCESS_CONSIGNMENT",
    "PI_THIRD_PARTY_PROVISION",
    "PI_COLLECTION_AND_USE_FOR_GUEST_ON_ARTICLE",
    "ACCESS_GUIDE",
    "WITHDRAWAL_GUIDE",
    "PI_SELLER_PROVISION",
    "PI_COLLECTION_AND_USE_ON_ORDER",
    "ORDER_INFO_AGREE",
    "CLEARANCE_INFO_COLLECTION_AND_USE",
    "TRANSFER_AGREE",
]
"""선택동의항목 타입"""


# ====================================================================
#  Configuration (회원가입 / 간편로그인 설정) 모델
# ====================================================================


class CommonJoinConfigResponse(BaseDto):
    """
    회원가입항목 config 조회 응답

    OpenAPI Schema: configurations-member-common-join-config18446488
    """

    used: bool = Field(..., description="설정 사용 여부")
    member_id: JoinConfigItemStatus = Field(..., description="아이디")
    member_name: JoinConfigItemStatus = Field(..., description="이름")
    nickname: JoinConfigItemStatus = Field(..., description="닉네임")
    password: JoinConfigItemStatus = Field(..., description="비밀번호")
    email: JoinConfigItemStatus = Field(..., description="이메일")
    email_agreement: JoinConfigItemStatus = Field(..., description="이메일 수신 동의 사용")
    mobile_no: JoinConfigItemStatus = Field(..., description="휴대폰번호")
    sms_agreement: JoinConfigItemStatus = Field(..., description="SMS 수신 동의 사용")
    address: JoinConfigItemStatus = Field(..., description="주소")
    phone_no: JoinConfigItemStatus = Field(..., description="전화번호")
    birthday: JoinConfigItemStatus = Field(..., description="생년월일")
    sex: JoinConfigItemStatus = Field(..., description="성별")


class ExtraInfoOptionSummary(BaseDto):
    """추가항목 옵션 요약 정보"""

    extra_info_option_no: int = Field(..., description="옵션 번호")
    extra_info_option_name: str = Field(..., description="옵션 명")


class ExtraInfoSummaryContent(BaseDto):
    """회원정보 추가항목 요약"""

    extra_info_no: int = Field(..., description="항목 번호")
    extra_info_name: str = Field(..., description="항목 명")
    extra_info_type: str = Field(..., description="항목 타입 (예: TEXTBOX)")
    status: str = Field(..., description="사용 상태 (예: USED)")
    extra_info_options: list[ExtraInfoOptionSummary] = Field(
        default_factory=list, description="옵션 목록"
    )


class ExtraInfoConfigResponse(BaseDto):
    """
    추가항목 config 조회 응답

    OpenAPI Schema: configurations-member-extra-info-config-1692811019
    """

    extra_info_contents: list[ExtraInfoSummaryContent] = Field(
        default_factory=list, description="회원정보 추가항목 목록"
    )


class AppleLoginConfig(BaseDto):
    """애플 간편로그인 config"""

    key_id: str | None = Field(None, description="애플인 경우 config 의 keyId")
    team_id: str | None = Field(None, description="애플인 경우 config 의 teamId")
    enc_key: str | None = Field(None, description="애플인 경우 config 의 시크릿")


class OpenIdConfigResponse(BaseDto):
    """
    프로바이더별 간편회원가입 config 조회 응답

    OpenAPI Schema: configurations-member-open-id-providerType2005268368
    """

    client_id: str = Field(..., description="간편로그인 client id")
    client_secret: str | None = Field(None, description="간편로그인 clientSecret (마스킹)")
    # 운영데이터 전부 null(8개 프로바이더 모두) → 응답 실데이터 추론 불가.
    # 스펙 example 이 ["id", "name"] (문자열 scope) 이므로 list[str] 로 타입화.
    scopes: list[str] | None = Field(None, description="간편로그인 scopes (예: id, name)")
    apple_config: AppleLoginConfig | None = Field(None, description="애플인 경우 config")


class AppCardStoreIdRequest(BaseDto):
    """
    앱카드 storeId 수정 요청

    OpenAPI Schema: configurations-member-app-card-743079106
    """

    store_id: str | None = Field(None, description="앱카드 store id")


class PendingProviderRequest(BaseDto):
    """
    간편회원 로그인 일시중지 프로바이더 추가 요청

    OpenAPI Schema: configurations-member-open-id-pending-provider-1763264321
    """

    provider_type: ProviderType = Field(..., description="간편회원 프로바이더")
    action: PendingProviderAction = Field(..., description="프로바이더 추가/제거 여부")


class OpenIdConfigUpdateRequest(BaseDto):
    """
    프로바이더별 간편회원가입 config 수정 요청

    OpenAPI Schema: configurations-member-open-id-providerType-1864141721
    """

    client_id: str = Field(..., description="간편로그인 client id")
    client_secret: str | None = Field(None, description="간편로그인 clientSecret (마스킹)")
    # 요청 전용. 스펙 example 이 ["id", "name"] (문자열 scope) 이므로 list[str] 로 타입화.
    scopes: list[str] | None = Field(None, description="간편로그인 scopes (예: id, name)")
    apple_config: AppleLoginConfig | None = Field(None, description="애플인 경우 config")


# ====================================================================
#  회원등급 (Grade) 모델
# ====================================================================


class GradeImage(BaseDto):
    """등급 이미지"""

    original_file_name: str | None = Field(None, description="원본 파일명")
    uploaded_file_name: str | None = Field(None, description="업로드 파일명")


class Grade(BaseDto):
    """
    회원등급 정보

    OpenAPI Schema: grades1273037573 (배열 항목)
    """

    grade_no: int = Field(..., description="등급 번호")
    grade_name: str = Field(..., description="등급 이름")
    used: bool = Field(..., description="사용 여부")
    image: GradeImage = Field(..., description="등급 이미지")


# ====================================================================
#  회원 그룹 (생성/수정 요청) 모델
# ====================================================================


class MemberGroupRequest(BaseDto):
    """
    회원 그룹 생성/수정 요청

    OpenAPI Schema: member-groups-67331454
    """

    name: str = Field(..., description="회원 그룹 이름")
    description: str = Field(..., description="회원 그룹 상세 설명")
    reserve_benefit: ReserveBenefit = Field(..., description="적립금 혜택 정보")


# ====================================================================
#  탈퇴 회원 조회 모델
# ====================================================================


class ExpelledMember(BaseDto):
    """
    탈퇴 회원 정보

    OpenAPI Schema: members-expelled-members2118687990 (배열 항목)
    """

    member_no: int = Field(..., description="회원번호")
    member_id: str = Field(..., description="아이디")
    member_type: MemberType = Field(..., description="회원 구분")
    member_status: MemberStatus = Field(..., description="회원 상태")
    provider_type: ProviderType | None = Field(None, description="마지막 연동 SNS")
    join_type_name: str | None = Field(None, description="가입 경로")
    join_ymdt: KstDatetime = Field(..., description="가입 일시")
    last_login_ymdt: KstDatetime | None = Field(None, description="최근 접속 시간")
    last_login_ip: str | None = Field(None, description="마지막 접속 IP")
    login_count: int = Field(..., description="로그인 횟수")
    additional_info: str | None = Field(None, description="추가 정보(JSON)")
    member_grade_name: str = Field(..., description="회원등급이름")
    member_group_names: str = Field(..., description="회원그룹이름")
    withdrawal_date_time: KstDatetime = Field(..., description="탈퇴 일시")
    withdrawal_reason: str = Field(..., description="탈퇴 사유")


# ====================================================================
#  외부회원연동 모델
# ====================================================================


class ExternalMemberRequest(BaseDto):
    """
    외부회원연동 회원가입 요청

    OpenAPI Schema: members-external1437284076
    """

    id: str = Field(..., description="회원 아이디(업체에서 관리하는 회원의 유일값)")
    name: str | None = Field(None, description="사용자 이름")
    nickname: str | None = Field(None, description="사용자 별명, 별칭")
    email: str | None = Field(None, description="이메일")
    phone: str | None = Field(None, description="휴대전화번호")
    ci: str | None = Field(None, description="ci")
    birthday: str | None = Field(None, description="생년월일")
    gender: str | None = Field(None, description="성별")
    grade_no: int | None = Field(None, description="회원 등급")
    # 요청 전용. 회원 그룹 번호 목록. 스펙 example "groupNos":[] (회원그룹 번호) → list[int].
    group_nos: list[int] | None = Field(None, description="회원 그룹 번호 목록")
    adult_certified: bool | None = Field(None, description="성인 인증 여부")
    privacy_policy_agreed: bool | None = Field(None, description="본인 인증 여부")
    push_policy_agreed: bool | None = Field(None, description="앱푸시 동의 여부")
    sms_policy_agreed: bool | None = Field(None, description="광고성 SMS 수신동의 여부")
    email_policy_agreed: bool | None = Field(None, description="광고성 Email 수신동의 여부")
    extra_json: str | None = Field(None, description="추가정보 (입점사 회원 커스텀 정보)")
    business_name: str | None = Field(None, description="사업자 명")
    business_registration_number: str | None = Field(None, description="사업자 등록번호")
    nation: str | None = Field(None, description="국가 코드")
    zip_code: str | None = Field(None, description="우편번호")
    street_address: str | None = Field(None, description="도로명 주소")
    street_address_detail: str | None = Field(None, description="도로명 상세 주소")
    land_lot_address: str | None = Field(None, description="지번 주소")
    land_lot_address_detail: str | None = Field(None, description="지번 상세 주소")
    city: str | None = Field(None, description="도, 시")
    state: str | None = Field(None, description="구, 군, 읍")


class ExternalMemberResponse(BaseDto):
    """
    외부회원연동 회원가입 응답

    OpenAPI Schema: members-external-562353168
    """

    member_no: int = Field(..., description="가입된 회원 번호")


class ExternalMemberIdUpdateRequest(BaseDto):
    """
    외부회원 아이디 변경 요청

    OpenAPI Schema: members-external-id510313064
    """

    current_oauth_id: str = Field(..., description="현재 Oauth ID")
    new_oauth_id: str = Field(..., description="변경할 새로운 Oauth ID")


# ====================================================================
#  회원 이용 정지 모델
# ====================================================================


class MemberProhibitRequest(BaseDto):
    """
    회원 이용 정지 요청

    OpenAPI Schema: members-prohibit-849892994
    """

    member_nos: list[int] = Field(..., description="정지시킬 회원번호 리스트")
    prohibition: bool = Field(..., description="회원 정지(true) / 정지 해제(false)")
    status: ProhibitStatus | None = Field(None, description="변경시킬 회원 상태")
    notification_types: list[NotificationType] | None = Field(None, description="알림 종류")
    expire_date: str | None = Field(None, description="회원 이용 정지 기간 (yyyy-MM-dd)")
    reason: str | None = Field(None, description="정지 사유")


class MemberProhibitResultRow(BaseDto):
    """회원 정지(정지 해제) 결과 행"""

    member_no: int = Field(..., description="회원 번호")
    success: bool = Field(..., description="회원 정지(정지 해제) 성공 여부")
    message: str = Field(..., description="실패 사유 (성공 시 빈 문자열)")


class MemberProhibitResponse(BaseDto):
    """
    회원 이용 정지 응답

    OpenAPI Schema: members-prohibit1975347019
    """

    value: str = Field(..., description="회원 정지 / 정지 해제")
    rows: list[MemberProhibitResultRow] = Field(default_factory=list, description="처리 결과")


# ====================================================================
#  회원 정보 조회/수정 (Profile) 모델
# ====================================================================


class ProfileMemberGroup(BaseDto):
    """회원 정보 조회 시 회원 그룹"""

    member_group_no: int = Field(..., description="회원 그룹 번호")
    member_group_name: str = Field(..., description="회원 그룹 이름")
    member_group_description: str = Field(..., description="회원 그룹 설명")


class ProfileAgreedTerms(BaseDto):
    """기본 동의 항목"""

    terms_no: int = Field(..., description="기본 동의 항목 번호")
    terms_type: str = Field(..., description="동의 타입")
    is_agree: bool = Field(..., description="기본 동의 항목 동의 여부")
    agreement_ymdt: KstDatetime = Field(..., description="기본 동의 항목 동의 시각")


class ProfileCustomAgreedTerms(BaseDto):
    """추가 동의 항목"""

    custom_terms_no: int = Field(..., description="추가 동의 항목 번호")
    is_agree: bool = Field(..., description="추가 동의 항목 동의 여부")
    agreement_ymdt: KstDatetime = Field(..., description="추가 동의 항목 동의 시각")


class ProfileExtraInfo(BaseDto):
    """회원 추가항목 정보"""

    extra_info_no: int = Field(..., description="추가항목 번호")
    extra_info_option_nos: list[int] = Field(default_factory=list, description="추가항목 옵션 번호 목록")
    extra_info_option_text_content: str | None = Field(None, description="추가항목 옵션 텍스트 답변 내용")


class ProfileResponse(BaseDto):
    """
    회원 정보 조회 응답

    OpenAPI Schema: profile-1050061699
    """

    member_no: int = Field(..., description="회원번호")
    member_id: str = Field(..., description="아이디")
    member_name: str | None = Field(None, description="회원이름")
    member_grade_no: int = Field(..., description="회원 등급 번호")
    member_grade_name: str = Field(..., description="회원 등급 이름")
    member_group_names: str = Field(..., description="회원 그룹 이름")
    member_groups: list[ProfileMemberGroup] = Field(default_factory=list, description="회원 그룹 목록")
    member_status: str = Field(..., description="회원 상태")
    member_type: str = Field(..., description="회원 구분")
    nickname: str | None = Field(None, description="닉네임")
    gender: str | None = Field(None, description="성별")
    birthday: str | None = Field(None, description="생년월일")
    mobile_country_code: str | None = Field(None, description="국제전화번호 코드")
    mobile_no: str | None = Field(None, description="휴대폰번호")
    email: str | None = Field(None, description="이메일")
    ci: str | None = Field(None, description="CI")
    join_type_name: str | None = Field(None, description="가입 경로")
    join_ymdt: KstDatetime = Field(..., description="가입 일시")
    last_login_ymdt: KstDatetime | None = Field(None, description="최근 접속 시간")
    last_login_ip: str = Field(..., description="마지막 접속 IP")
    login_count: int = Field(..., description="로그인 횟수")
    push_notification_agreed: bool = Field(..., description="푸시 알림 동의 여부")
    push_notification_agree_ymdt: KstDatetime | None = Field(None, description="푸시 알림 동의 시각")
    sms_agreed: bool = Field(..., description="SMS 동의 여부")
    sms_agree_ymdt: KstDatetime | None = Field(None, description="SMS 동의 시각")
    direct_mail_agreed: bool = Field(..., description="광고 우편물(DM) 수신 동의 여부")
    direct_mail_agree_ymdt: KstDatetime | None = Field(None, description="광고 우편물(DM) 수신 동의 시각")
    oauth_id_no: str | None = Field(None, description="외부 서비스 고유 식별값")
    additional_info: str | None = Field(None, description="추가 정보")
    adult_certificated: bool = Field(..., description="성인 인증 여부")
    adult_certificated_ymdt: KstDatetime | None = Field(None, description="성인 인증 일시")
    principal_certificated: bool = Field(..., description="본인인증 여부")
    provider_type: str | None = Field(None, description="마지막 연동 SNS")
    blacklisted: bool = Field(..., description="블랙리스트 여부")
    representative_member_no: int | None = Field(None, description="대표몰 회원번호")
    business_name: str | None = Field(None, description="사업자 회원 회사명")
    registration_no: str | None = Field(None, description="사업자 회원 사업자등록번호")
    extra_info: list[ProfileExtraInfo] = Field(default_factory=list, description="회원 추가항목 정보")
    agreed_terms: list[ProfileAgreedTerms] = Field(default_factory=list, description="기본 동의 항목 목록")
    custom_agreed_terms: list[ProfileCustomAgreedTerms] = Field(
        default_factory=list, description="추가 동의 항목 목록"
    )


class ProfileExtraInfoRequest(BaseDto):
    """회원 정보 수정 시 추가 항목"""

    extra_info_no: int = Field(..., description="추가항목 번호")
    extra_info_option_nos: list[int] = Field(default_factory=list, description="추가항목 옵션 번호 목록")
    extra_info_option_text_content: str | None = Field(None, description="추가항목 옵션 텍스트 답변 내용")


class ProfileUpdateRequest(BaseDto):
    """
    회원 정보 수정 요청

    OpenAPI Schema: profile-2036449977
    profile-bulk 의 항목 (profile-bulk-1153989928) 과 동일한 구조입니다.
    """

    member_id: str | None = Field(None, description="회원 아이디")
    member_no: int | None = Field(None, description="회원 번호")
    member_name: str | None = Field(None, description="회원 성명")
    first_name: str | None = Field(None, description="이름")
    last_name: str | None = Field(None, description="성")
    mobile_country_code: str | None = Field(None, description="국제전화번호 코드")
    mobile_no: str | None = Field(None, description="휴대전화번호")
    telephone_no: str | None = Field(None, description="일반전화번호")
    ci: str | None = Field(None, description="CI")
    birthday: str | None = Field(None, description="생일 yyyyMMdd")
    sex: str | None = Field(None, description="성별 (F:여성/M:남성)")
    email: str | None = Field(None, description="이메일 주소")
    zip_cd: str | None = Field(None, description="우편번호")
    address: str | None = Field(None, description="도로명 주소")
    detail_address: str | None = Field(None, description="도로명 주소 상세")
    jibun_address: str | None = Field(None, description="도로명 주소 (지번 주소)")
    jibun_detail_address: str | None = Field(None, description="도로명 주소 상세 (지번 주소)")
    city: str | None = Field(None, description="도시")
    state: str | None = Field(None, description="국내: 군/구, 해외: 주")
    country_code: str | None = Field(None, description="거주 국가")
    nickname: str | None = Field(None, description="닉네임")
    push_notification_agreed: bool | None = Field(None, description="푸시 알림 동의 여부")
    sms_agreed: bool | None = Field(None, description="SMS 알림 동의 여부")
    direct_mail_agreed: bool | None = Field(None, description="이메일 알림 동의 여부")
    business_name: str | None = Field(None, description="회사명")
    registration_no: str | None = Field(None, description="사업자 등록 번호")
    refund_bank: str | None = Field(None, description="환불 계좌 은행")
    refund_bank_account: str | None = Field(None, description="환불 계좌 번호")
    refund_bank_depositor_name: str | None = Field(None, description="환불 계좌 예금주명")
    certificated: bool | None = Field(None, description="인증확인 여부")
    blacklisted: bool | None = Field(None, description="블랙리스트 등록 여부")
    join_terms_agreements: list[JoinTermsAgreementType] | None = Field(None, description="선택동의항목")
    # 요청 전용. 추가 선택 동의 항목 번호 목록. 스펙 example "customTermsNos":[1] → list[int].
    custom_terms_nos: list[int] | None = Field(None, description="추가 선택 동의 항목 번호 목록")
    additional_info: str | None = Field(None, description="추가 정보 (JSON)")
    extra_info: list[ProfileExtraInfoRequest] = Field(default_factory=list, description="추가 항목 정보")
    is_adult_certified: bool | None = Field(None, description="성인인증 여부")


class ProfileUpdateResponse(BaseDto):
    """
    회원 정보 수정 응답

    OpenAPI Schema: profile-1775399877
    """

    member_no: int = Field(..., description="회원 번호")


class ProfileBulkUpdateResponse(BaseDto):
    """
    대량 회원 정보 수정 응답

    OpenAPI Schema: profile-bulk-786404190
    """

    member_nos: list[int] = Field(default_factory=list, description="회원 번호 목록")


class BulkDeleteProfileRequest(BaseDto):
    """
    복수의 회원 탈퇴 처리 요청

    OpenAPI Schema: profile-bulk-delete-722054971
    """

    member_nos: list[int] = Field(..., description="회원 번호 리스트 (최대 500명)")


class BlockedReleaseRequest(BaseDto):
    """
    차단 회원 해제 요청

    OpenAPI Schema: profile-blocked-release452550290
    """

    member_no: int = Field(..., description="차단자 회원 번호")
    target_member_no: int | None = Field(None, description="차단 대상 회원 번호")
    target_member_id: str | None = Field(None, description="차단 대상 회원 아이디")


# ====================================================================
#  휴면 회원 모델
# ====================================================================


class DormantMemberInner(BaseDto):
    """휴면 회원 내부 회원 정보"""

    member_no: int = Field(..., description="회원 번호")
    member_type: MemberType = Field(..., description="회원 유형")
    provider_type: ProviderType | None = Field(None, description="연동 유형")
    join_ymdt: KstDatetime = Field(..., description="가입일시")


class DormantMemberContent(BaseDto):
    """휴면 회원 항목"""

    member_no: int = Field(..., description="회원 번호")
    member_id: str = Field(..., description="아이디")
    member_name: str = Field(..., description="이름")
    dormant_ymdt: KstDatetime = Field(..., description="휴면전환일시")
    member: DormantMemberInner | None = Field(None, description="회원 정보")


class DormantMembersResponse(BaseDto):
    """
    휴면 회원 조회 응답 (Spring Page 구조)

    OpenAPI Schema: profile-dormant-71216701
    """

    content: list[DormantMemberContent] = Field(default_factory=list, description="조회 결과")
    total_pages: int = Field(..., description="전체 페이지 수")
    total_elements: int = Field(..., description="전체 조회건수")


class DormantReleaseRequest(BaseDto):
    """
    휴면 회원 해제 요청

    OpenAPI Schema: profile-dormant-release909502051
    """

    member_no: int | None = Field(None, description="회원 번호")
    member_id: str | None = Field(None, description="회원 아이디")


# ====================================================================
#  회원등급 수정 모델
# ====================================================================


class GradeUpdateMember(BaseDto):
    """등급 변경 대상 회원"""

    member_no: int = Field(..., description="등급 변경대상 회원 번호 (memberId와 배타적으로 필수)")
    member_id: str = Field(..., description="등급 변경대상 회원 아이디 (memberNo와 배타적으로 필수)")


class ProfileGradesRequest(BaseDto):
    """
    회원등급 수정 요청

    OpenAPI Schema: profile-grades508071144
    """

    grade_no: int = Field(..., description="변경 등급 번호")
    members: list[GradeUpdateMember] = Field(default_factory=list, description="등급 변경 대상 회원 목록")
    issue_coupon: bool | None = Field(None, description="쿠폰 발행 여부")


class ProfileGradesResponse(BaseDto):
    """
    회원등급 수정 응답

    OpenAPI Schema: profile-grades1340609570
    """

    member_nos: list[str] = Field(default_factory=list, description="등급 변경완료 회원번호목록")

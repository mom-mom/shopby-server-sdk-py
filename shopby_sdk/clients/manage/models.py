"""Manage API 모델

쇼핑몰 운영(manage) 관련 server API의 요청/응답 모델 정의.
"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


# ------------------------------------
#  Literal 타입 별칭
# ------------------------------------
AccumulationPeriodType = Literal["REGISTER", "START", "EXPIRE"]
"""적립금 조회 기간 설정 타입 (REGISTER: 등록일, START: 생성일, EXPIRE: 만료일)"""

AccumulationStatus = Literal[
    "GIVE",
    "GIVE_BY_CANCELED",
    "SUBTRACTION",
    "SUBTRACTION_BY_CANCELED",
]
"""적립 상태 (GIVE: 지급, GIVE_BY_CANCELED: 차감롤백, SUBTRACTION: 차감, SUBTRACTION_BY_CANCELED: 지급롤백)"""

AccumulationReserveReason = Literal[
    "ADD_AFTER_PAYMENT",
    "ADD_AFTER_EVENT_PAYMENT",
    "ADD_AFTER_REPLACE_PAYMENT",
    "ADD_POSTING",
    "ADD_CANCEL",
    "ADD_RETURN",
    "ADD_MANUAL",
    "ADD_EVENT",
    "ADD_SIGNUP",
    "ADD_BIRTHDAY",
    "ADD_APP_INSTALL",
    "ADD_APP_ORDER",
    "ADD_APP_NOTIFICATION",
    "ADD_GRADE",
    "ADD_GRADE_BENEFIT",
    "ADD_COUPON",
    "SUB_PAYMENT_USED",
    "SUB_EXTRA_PAYMENT_USED",
    "SUB_CANCEL",
    "SUB_RETURN",
    "SUB_DELETE_POSTING",
    "SUB_EXPIRED",
    "SUB_MANUAL",
    "SUB_DELETE_ACCOUNT",
    "EXTERNAL_ACCUMULATION",
]
"""적립 사유 코드"""

AssembleSearchType = Literal["ALL", "REASON", "REGISTER", "UPDATER", "REQUEST_NO"]
"""적립금 변동 요청 검색 유형 (ALL: 전체, REASON: 지급사유, REGISTER: 지급등록자, UPDATER: 최종수정자, REQUEST_NO: 적립금번호)"""

AssemblePeriodType = Literal["REGISTER", "PAYMENT", "REQUEST", "UPDATE"]
"""적립금 변동 요청 검색 기간 유형 (REGISTER: 등록일시, PAYMENT: 지급일시, REQUEST: 예약일시, UPDATE: 최종수정일)"""

RequestGroupType = Literal["ALL", "ADD", "SUB"]
"""적립금 변동 요청 그룹 타입 (ALL: 전체, ADD: 지급, SUB: 차감)"""

AssembleRequestType = Literal["DIRECT_ADD", "DIRECT_SUB", "RESERVE_ADD", "ORDER_RESERVE_ADD"]
"""적립금 변동 요청 타입 (DIRECT_ADD: 즉시지급, DIRECT_SUB: 즉시차감, RESERVE_ADD: 예약지급, ORDER_RESERVE_ADD: 주문예약지급)"""

AssembleStatus = Literal["WAITING", "COMPLETED", "CANCELED", "PROCESSING"]
"""지급 요청 상태 (WAITING: 지급대기, COMPLETED: 지급완료, CANCELED: 지급취소, PROCESSING: 지급처리중)"""

ValidPeriodType = Literal["NONE", "PERIOD", "DATETIME", "NO_LIMIT"]
"""유효기간 설정 타입 (NONE: 별도 유효기간 지정, PERIOD: 기간지정, DATETIME: 만료일지정, NO_LIMIT: 제한없음)"""

ExternalRequestType = Literal["ADD", "SUB", "SUB_ROLLBACK"]
"""외부적립금 요청 타입 (ADD, SUB, SUB_ROLLBACK)"""

ExternalMappingKeyType = Literal["REVIEW", "ORDER", "ORDER_OPTION"]
"""외부적립금 매핑키 종류 (REVIEW, ORDER, ORDER_OPTION)"""

InquirySearchType = Literal[
    "ALL", "INQUIRY_NO", "TITLE", "CONTENT", "ISSUER", "ASSIGNEE"
]
"""1:1문의 검색 유형 (ALL: 전체, INQUIRY_NO: 문의번호, TITLE: 문의제목, CONTENT: 문의내용, ISSUER: 문의자, ASSIGNEE: 담당자명)"""

InquiryStatus = Literal["ISSUED", "ASKED", "IN_PROGRESS", "ANSWERED"]
"""1:1문의 상태 (ISSUED/ASKED: 답변대기, IN_PROGRESS: 진행중, ANSWERED: 답변완료)"""

InquirySearchDateType = Literal["REGISTER", "ANSWER"]
"""1:1문의 날짜 검색 유형 (REGISTER: 등록일, ANSWER: 답변일)"""

NotificationChannel = Literal["EMAIL", "SMS"]
"""만료 알림 수단 (EMAIL, SMS)"""

TermsType = Literal[
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
    "REGULAR_PAYMENT_USE",
    "AUTO_APPROVAL_USE",
    "PI_LIQUOR_PURCHASE_PROVISION",
    "PI_RESTOCK_NOTICE",
    "PI_14_AGE",
    "PI_GIFT_ACCEPT_COLLECTION_AND_USE",
    "MARKETING_RECEIVE",
    "MARKETING_INFO_USAGE",
]
"""약관 유형"""


# ------------------------------------
#  GET /accumulations (적립금 조회하기)
# ------------------------------------
class AccumulationItem(BaseDto):
    """적립금 내역 항목 (accumulations177281248 items)"""

    member_no: int = Field(..., description="회원번호")
    accumulation_no: int = Field(..., description="적립금 번호")
    accumulation_amt: float = Field(..., description="적립/차감 금액")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    start_ymdt: KstDatetime | None = Field(None, description="시작일")
    expire_ymdt: KstDatetime | None = Field(None, description="만료일")
    accumulation_reserve_reason: AccumulationReserveReason | None = Field(
        None, description="적립 사유"
    )
    reason_detail: str | None = Field(None, description="적립 사유 상세")
    accumulation_status: AccumulationStatus | None = Field(None, description="적립 상태")
    order_no: str | None = Field(None, description="주문번호")
    product_display_name: str | None = Field(None, description="상품명 표시")
    rest_amount: float | None = Field(None, description="남은 적립금")
    external_key: str | None = Field(None, description="외부 키(조회용)")


class AccumulationsResponse(BaseDto):
    """
    적립금 조회 응답

    OpenAPI Schema: accumulations177281248
    """

    items: list[AccumulationItem] = Field(default_factory=list, description="적립금 내역")
    total_count: int = Field(..., description="전체 조회건수")


# ------------------------------------
#  GET /accumulations/assembles (적립금 변동 요청 조회)
# ------------------------------------
class AssembleTarget(BaseDto):
    """적립금 변동 요청 지급 대상 (assembles targets)"""

    type: str | None = Field(None, description="지급 대상 유형")
    # 스펙상 items 가 oneOf(object/boolean/string/number) 자유형식 → 타입화 불가.
    # 운영데이터(targets 24건)는 전부 type=MEMBER_NO 이며 values 항목이 모두 int(회원번호)였으나,
    # 지급 대상 유형에 따라 값 형태가 달라질 수 있어 list[Any] 유지.
    values: list[Any] = Field(default_factory=list, description="지급 대상 값 리스트")


class AssembleOrderRequest(BaseDto):
    """적립금 변동 요청 주문 정보 (assembles orderRequest)"""

    order_no: str | None = Field(None, description="변동 대상 주문번호")
    order_product_option_no: int | None = Field(None, description="변동 대상 주문상품옵션번호")


class AssembleItem(BaseDto):
    """적립금 변동 요청 항목 (accumulations-assembles-982240398 contents)"""

    no: int = Field(..., description="지급 요청 번호")
    mall_no: int | None = Field(None, description="쇼핑몰 번호")
    mall_name: str | None = Field(None, description="쇼핑몰 이름")
    request_type: AssembleRequestType | None = Field(None, description="적립금 변동 요청 타입")
    request_group: RequestGroupType | None = Field(
        None, description="적립금 변동 요청 형태 지급 / 차감"
    )
    request_group_label: str | None = Field(
        None, description="적립금 변동 요청 형태 지급 / 차감 라벨"
    )
    request_date_time: KstDatetime | None = Field(None, description="적립금이 지급될 날짜")
    immediately: bool | None = Field(None, description="즉시 적립 여부")
    amount: float | None = Field(None, description="적립금 금액")
    reason: str | None = Field(None, description="지급 사유 코드")
    reason_label: str | None = Field(None, description="지급 사유")
    reason_detail: str | None = Field(None, description="지급 상세 사유 - 주문 지급 요청 시 사용")
    valid_period_type: ValidPeriodType | None = Field(None, description="유효 기간 설정 타입")
    valid_period: int | None = Field(None, description="만료 기간 (월)")
    expire_date_time: KstDatetime | None = Field(None, description="지정 만료 기간")
    targets: list[AssembleTarget] = Field(default_factory=list, description="지급 대상 목록")
    # 스펙상 items 가 oneOf(object/boolean/string/number) 자유형식이고,
    # 운영데이터 24건 모두 빈 배열([])이라 항목 구조를 추론할 수 없어 list[Any] 유지.
    exclude_member_nos: list[Any] = Field(
        default_factory=list, description="지급 대상 중 제외된 회원 번호"
    )
    order_request: AssembleOrderRequest | None = Field(None, description="주문 정보")
    review_no: int | None = Field(None, description="상품후기 일련번호")
    product_display_name: str | None = Field(None, description="상품노출명")
    register_admin_no: int | None = Field(None, description="등록 어드민 번호")
    register_admin_name: str | None = Field(None, description="등록 어드민 이름")
    register_admin_status: str | None = Field(None, description="등록 어드민 상태")
    register_date_time: KstDatetime | None = Field(None, description="등록일")
    update_admin_no: int | None = Field(None, description="수정 어드민 번호")
    update_admin_name: str | None = Field(None, description="수정 어드민 이름")
    update_admin_status: str | None = Field(None, description="수정 어드민 상태")
    update_date_time: KstDatetime | None = Field(None, description="수정일")
    payment_date_time: KstDatetime | None = Field(None, description="실 지급 날짜")
    payment_count: int | None = Field(None, description="지급 성공 건수")
    try_count: int | None = Field(None, description="지급 시도 건수")
    status: AssembleStatus | None = Field(None, description="지급 상태 코드")
    status_label: str | None = Field(None, description="지급 상태")


class AssemblesResponse(BaseDto):
    """
    적립금 변동 요청 조회 응답

    OpenAPI Schema: accumulations-assembles-982240398
    """

    total_count: int = Field(..., description="전체 조회건수")
    contents: list[AssembleItem] = Field(default_factory=list, description="조회 결과")


# ------------------------------------
#  GET /accumulations/externals (외부적립금 연동 이력 조회)
# ------------------------------------
class ExternalAccumulationItem(BaseDto):
    """외부적립금 연동 이력 항목 (accumulations-externals320580630 items)"""

    seq: int = Field(..., description="트랜잭션 아이디")
    request_type: ExternalRequestType | None = Field(None, description="요청타입")
    mapping_key_type: ExternalMappingKeyType | None = Field(None, description="매핑키 종류")
    mapping_key: str | None = Field(None, description="매핑키")
    member_key: str | None = Field(None, description="회원 연동 키")
    request_json: str | None = Field(None, description="request 값")
    amount: float = Field(..., description="적립금")
    request_date_time: KstDatetime | None = Field(None, description="요청일시")
    external_no: str | None = Field(None, description="외부연동키")
    success: bool | None = Field(None, description="성공여부")
    response_json: str | None = Field(None, description="response 값")


class ExternalAccumulationsResponse(BaseDto):
    """
    외부적립금 연동 이력 조회 응답

    OpenAPI Schema: accumulations-externals320580630
    """

    items: list[ExternalAccumulationItem] = Field(
        default_factory=list, description="적립금 내역"
    )
    total_count: int = Field(..., description="전체 조회건수")


# ------------------------------------
#  GET /accumulations/settlement (적립금 지급/차감 이력 조회)
# ------------------------------------
class SettlementItem(BaseDto):
    """적립금 지급/차감 이력 항목 (accumulations-settlement146719745 items)"""

    seq: int = Field(..., description="트랜잭션 아이디")
    register_ymdt: KstDatetime | None = Field(None, description="적립/차감 시간")
    accumulation_status: AccumulationStatus | None = Field(None, description="적립/차감 유형")
    reason: str | None = Field(None, description="적립/차감 사유")
    reason_detail: str | None = Field(None, description="적립/차감 상세 사유")
    amount: float = Field(..., description="적립금")
    member_no: int = Field(..., description="회원번호")
    accumulation_no: int = Field(..., description="적립금 번호")
    related_accumulation_no: int | None = Field(None, description="연관 적립금 번호")
    coupon_no: int | None = Field(None, description="쿠폰 번호")
    coupon_issue_no: int | None = Field(None, description="쿠폰 지급 번호")
    mapping_type: str | None = Field(None, description="매핑키")
    mapping_value: str | None = Field(None, description="매핑값")
    description: str | None = Field(None, description="설명")


class SettlementResponse(BaseDto):
    """
    적립금 지급/차감 이력 조회 응답

    OpenAPI Schema: accumulations-settlement146719745
    """

    items: list[SettlementItem] = Field(
        default_factory=list, description="적립금 지급/차감 내역"
    )
    total_count: int = Field(..., description="전체 조회건수")


# ------------------------------------
#  GET /accumulations/usage (적립금 사용처 추적하기)
# ------------------------------------
class AccumulationUsage(BaseDto):
    """적립금 사용 내역 (accumulations-usage usages)"""

    accumulation_no: int = Field(..., description="적립금번호")
    order_no: str | None = Field(None, description="주문번호")
    use_date_time: KstDatetime | None = Field(None, description="사용일시")
    use_amount: float = Field(..., description="사용금액")


class AccumulationUsageItem(BaseDto):
    """
    적립금 사용처 추적 항목

    OpenAPI Schema: accumulations-usage-1532805667 (items)
    """

    accumulation_no: int = Field(..., description="적립금 번호")
    start_amount: float = Field(..., description="최초 받은 적립금")
    rest_amount: float = Field(..., description="남은 적립금")
    usages: list[AccumulationUsage] = Field(default_factory=list, description="사용된 곳")


# ------------------------------------
#  POST /accumulations/members/available (회원 보유 적립금 조회 다건)
# ------------------------------------
class MemberAvailableAccumulationRequest(BaseDto):
    """
    회원 보유 적립금 조회(다건) 요청

    OpenAPI Schema: accumulations-members-available-650045292
    """

    member_ids: list[str] = Field(default_factory=list, description="회원 아이디 리스트")
    member_nos: list[int] = Field(default_factory=list, description="회원 번호 리스트")


class MemberAvailableAccumulationItem(BaseDto):
    """회원 보유 적립금 항목 (accumulations-members-available-1413144932 items)"""

    member_id: str | None = Field(None, description="회원 아이디")
    member_no: int | None = Field(None, description="회원 번호")
    amount: float = Field(..., description="가용 적립금")


class MemberAvailableAccumulationResponse(BaseDto):
    """
    회원 보유 적립금 조회(다건) 응답

    OpenAPI Schema: accumulations-members-available-1413144932
    """

    items: list[MemberAvailableAccumulationItem] = Field(
        default_factory=list, description="조회 결과 목록"
    )
    count: int = Field(..., description="조회된 항목 수")


# ------------------------------------
#  GET /profile/accumulations (적립금 상태 조회하기)
# ------------------------------------
class ProfileAccumulationItem(BaseDto):
    """회원 적립금 상태 항목 (profile-accumulations-301787378 items)"""

    accumulation_no: int = Field(..., description="적립금 번호")
    accumulation_amt: float = Field(..., description="적립금액")
    rest_accumulation_amt: float | None = Field(None, description="적립금액 중 사용 가능 금액")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    start_ymdt: KstDatetime | None = Field(None, description="시작일")
    expire_ymdt: KstDatetime | None = Field(None, description="만료일")
    accumulation_reserve_reason: AccumulationReserveReason | None = Field(
        None, description="적립 사유"
    )
    reason_detail: str | None = Field(None, description="적립 사유 상세")
    accumulation_status: AccumulationStatus | None = Field(None, description="적립 상태")
    order_no: str | None = Field(None, description="주문번호")
    product_display_name: str | None = Field(None, description="상품명 표시")
    external_key: str | None = Field(None, description="외부 키(조회용)")


class ProfileAccumulationsResponse(BaseDto):
    """
    회원 적립금 상태 조회 응답

    OpenAPI Schema: profile-accumulations-301787378
    """

    total_amt: float | None = Field(
        None, description="전체 기간 중 해당 고객이 최종적으로 사용 가능한 적립금 금액"
    )
    member_no: int = Field(..., description="회원 번호")
    items: list[ProfileAccumulationItem] = Field(
        default_factory=list, description="적립금 내역"
    )
    total_count: int = Field(..., description="전체 조회건수")
    items_total_rest_amt: float | None = Field(
        None, description="검색조건을 기준으로 조회된 items 목록의 restAccumulationAmt 합계금액"
    )


# ------------------------------------
#  POST /profile/accumulations (적립금 지급하기)
# ------------------------------------
class CreateAccumulationRequest(BaseDto):
    """
    적립금 지급 요청

    OpenAPI Schema: profile-accumulations-750189433
    """

    member_no: int | None = Field(None, description="회원 번호(회원 조회용)")
    member_id: str | None = Field(None, description="회원 아이디(회원 조회용)")
    accumulation_amt: float = Field(..., description="적립금 지급 금액")
    reason_detail: str | None = Field(
        None, description="지급 상세사유. 생략하면 '운영자 지급'으로 저장. 200자까지 입력가능"
    )
    expire_ymd: str | None = Field(
        None, description="적립금 만료일. 생략하면 몰 적립금 기본 설정의 적립금 유효기간 반영 (YYYY-MM-DD)"
    )
    external_key: str | None = Field(None, description="외부 키(조회용)(최대 60자)")
    notification_channels: list[NotificationChannel] = Field(
        default_factory=list, description="만료 알림 수단 (복수 설정)"
    )
    is_manual: bool | None = Field(
        None, description="운영자 수동 지급 여부 (true: 수동, false: 자동)"
    )


class CreateAccumulationResponse(BaseDto):
    """
    적립금 지급 응답

    OpenAPI Schema: profile-accumulations-339742700
    """

    member_no: int = Field(..., description="회원번호")
    accumulation_no: int = Field(..., description="생성된 적립금 번호")


# ------------------------------------
#  DELETE /profile/accumulations (적립금 차감하기)
# ------------------------------------
class SubtractionRelatedAccumulation(BaseDto):
    """차감 적립금 관련 적립금 정보 (profile-accumulations1700228947 subtractionRelatedAccumulations)"""

    accumulation_no: int = Field(..., description="적립금 번호")
    change_amt: float | None = Field(None, description="변동금액(차감)")
    register_date_time: KstDatetime | None = Field(None, description="생성일자")
    expire_date_time: KstDatetime | None = Field(None, description="만료일자")


class SubtractAccumulationResponse(BaseDto):
    """
    적립금 차감 응답

    OpenAPI Schema: profile-accumulations1700228947
    """

    subtracted_amt: float | None = Field(None, description="차감금액")
    member_no: int = Field(..., description="회원번호")
    accumulation_no: int = Field(..., description="생성된 적립금 번호(차감)")
    subtraction_related_accumulations: list[SubtractionRelatedAccumulation] = Field(
        default_factory=list, description="차감 적립금 관련 적립금정보"
    )


# ------------------------------------
#  GET /inquiries (1:1문의 조회하기)
# ------------------------------------
class InquiryIssuer(BaseDto):
    """1:1문의 문의자 정보 (inquiries521925742 issuer)"""

    issuer_no: int | None = Field(None, description="문의자 번호")
    issuer_id: str | None = Field(None, description="문의자 아이디")
    issuer_type: str | None = Field(None, description="문의자 타입")
    issuer_email: str | None = Field(None, description="문의자 이메일")
    issuer_status: str | None = Field(None, description="문의자 상태")
    issuer_team_name: str | None = Field(None, description="문의자 팀명")
    issuer_mobile_no: str | None = Field(None, description="문의자 전화번호")


class InquiryAssignee(BaseDto):
    """1:1문의 담당자 정보 (inquiries521925742 assignee)"""

    assignee_no: int | None = Field(None, description="담당자 번호")
    assignee_name: str | None = Field(None, description="담당자 아이디")
    assignee_status: str | None = Field(None, description="담당자 상태")


class InquiryNaverPay(BaseDto):
    """1:1문의 네이버페이 정보 (inquiries521925742 external.naverPay)"""

    naver_id: str | None = Field(None, description="네이버 아이디")
    writer_name: str | None = Field(None, description="작성자명")


class InquiryExternal(BaseDto):
    """1:1문의 외부 정보 (inquiries521925742 external)"""

    naver_pay: InquiryNaverPay | None = Field(None, description="네이버페이 문의 정보")


class InquiryAnswerFile(BaseDto):
    """1:1문의 답변 첨부파일 (inquiries521925742 answerFiles)"""

    original_file_name: str | None = Field(None, description="답변 첨부파일 원본 파일명")
    uploaded_file_name: str | None = Field(None, description="답변 첨부파일 업로드된 파일명")


class InquiryItem(BaseDto):
    """1:1문의 항목 (inquiries521925742 contents)"""

    inquiry_no: int = Field(..., description="문의번호")
    inquiry_type_no: int | None = Field(None, description="문의유형 번호")
    inquiry_type_name: str | None = Field(None, description="문의유형 이름")
    inquiry_type_channel: str | None = Field(None, description="문의 유입 경로 (NCP|NAVER_PAY|SYSTEM_KEY)")
    inquiry_title: str | None = Field(None, description="문의 제목")
    inquiry_content: str | None = Field(None, description="문의 내용")
    inquiry_status: InquiryStatus | None = Field(None, description="문의 상태")
    inquiry_send_email: bool | None = Field(None, description="답변 등록 시 email 알림 여부")
    inquiry_send_sms: bool | None = Field(None, description="답변 등록 시 sms 알림 여부")
    issuer: InquiryIssuer | None = Field(None, description="문의자 정보")
    assignee: InquiryAssignee | None = Field(None, description="담당자 정보")
    delayed: bool | None = Field(None, description="답변 지연 여부")
    issued_date_time: KstDatetime | None = Field(None, description="문의 일시")
    answered_date_time: KstDatetime | None = Field(None, description="답변 일시")
    answer_content: str | None = Field(None, description="답변 내용")
    external: InquiryExternal | None = Field(None, description="외부 문의 정보")
    image_urls: list[str] = Field(default_factory=list, description="이미지 url")
    original_image_urls: list[str] = Field(default_factory=list, description="원본 이미지 url")
    answer_files: list[InquiryAnswerFile] = Field(
        default_factory=list, description="답변 첨부파일 목록"
    )
    product_no: int | None = Field(None, description="상품번호")
    order_no: str | None = Field(None, description="주문번호")
    order_option_no: int | None = Field(None, description="주문옵션 번호")


class InquiriesResponse(BaseDto):
    """
    1:1문의 조회 응답

    OpenAPI Schema: inquiries521925742
    """

    total_count: int = Field(..., description="전체 조회건수")
    contents: list[InquiryItem] = Field(default_factory=list, description="조회 결과")


# ------------------------------------
#  GET /inquiries/types (1:1문의 유형 조회하기)
# ------------------------------------
class InquiryType(BaseDto):
    """
    1:1문의 유형 항목

    OpenAPI Schema: inquiries-types15782989 (items)
    """

    inquiry_type_no: int = Field(..., description="1:1문의 유형 번호")
    inquiry_type_name: str | None = Field(None, description="1:1문의 유형 제목")
    inquiry_type_description: str | None = Field(None, description="1:1문의 유형 설명")


# ------------------------------------
#  POST /inquiries/types (1:1문의 유형 생성하기)
# ------------------------------------
class CreateInquiryTypeRequest(BaseDto):
    """
    1:1문의 유형 생성 요청

    OpenAPI Schema: inquiries-types-1290331578
    """

    inquiry_type_name: str = Field(..., description="1:1문의 유형 제목")
    inquiry_type_description: str | None = Field(None, description="1:1문의 유형 설명")


# ------------------------------------
#  POST /inquiries/{inquiryNo}/answer (1:1 문의 답변 등록)
# ------------------------------------
class InquiryAnswerFileInput(BaseDto):
    """1:1문의 답변 첨부파일 (inquiries-inquiryNo-answer-495205860 files)"""

    original_file_name: str | None = Field(None, description="원본 파일명")
    uploaded_file_name: str | None = Field(None, description="업로드된 파일명")


class AnswerInquiryRequest(BaseDto):
    """
    1:1 문의 답변 등록 요청

    OpenAPI Schema: inquiries-inquiryNo-answer-495205860
    """

    content: str = Field(..., description="답변 내용")
    email: str | None = Field(None, description="답변자 이메일")
    mobile_no: str | None = Field(None, description="답변자 전화번호")
    completed: bool | None = Field(None, description="임시저장 여부")
    files: list[InquiryAnswerFileInput] = Field(
        default_factory=list, description="파일 목록"
    )


# ------------------------------------
#  POST /kakao/send (카카오 알림톡 메시지 수동 전송)
# ------------------------------------
class SendKakaoMessageRequest(BaseDto):
    """
    카카오 알림톡 메시지 수동 전송 요청

    OpenAPI Schema: kakao-send296080162
    """

    template_code: str = Field(..., description="템플릿 코드")
    # 키가 동적(템플릿별 치환 변수명)이고 값은 1depth 치환 텍스트(문자열) → dict[str, str].
    replace_map: dict[str, str] = Field(
        default_factory=dict, description="치환 텍스트(1depth만 허용)"
    )
    reserved_time: str | None = Field(None, description="예약전송 시간 (YYYY-MM-DD HH:mm:ss)")
    phone_num: str = Field(..., description="수신자 번호")


# ------------------------------------
#  GET /sms/unsubscribe (080 수신거부 목록 조회)
# ------------------------------------
class SmsUnsubscribeItem(BaseDto):
    """080 수신거부 항목 (sms-unsubscribe-363361024 contents)"""

    no: int = Field(..., description="수신거부 일련번호")
    mall_no: int | None = Field(None, description="쇼핑몰 번호")
    unsubscribe_phone_no: str | None = Field(None, description="수신거부 전화번호")
    register_date_time: KstDatetime | None = Field(None, description="수신거부 등록일시")


class SmsUnsubscribeResponse(BaseDto):
    """
    080 수신거부 목록 조회 응답

    OpenAPI Schema: sms-unsubscribe-363361024
    """

    total_count: int = Field(..., description="전체 조회건수")
    contents: list[SmsUnsubscribeItem] = Field(default_factory=list, description="조회 결과")


# ------------------------------------
#  GET /terms (유형별 약관 조회)
# ------------------------------------
class TermsItem(BaseDto):
    """
    유형별 약관 항목

    OpenAPI Schema: terms1337711918 (items)
    """

    terms_type: TermsType | None = Field(None, description="약관 유형")
    used: bool | None = Field(None, description="사용 여부")
    contents: str | None = Field(None, description="약관 내용")
    is_visible: bool | None = Field(None, description="노출 여부")


# ------------------------------------
#  GET /terms/custom/{customTermsNo}/members (추가 약관 동의 회원 목록 조회)
# ------------------------------------
class CustomTermsMember(BaseDto):
    """추가 약관 동의 회원 항목 (terms-custom-customTermsNo-members2042102439 contents)"""

    custom_terms_no: int | None = Field(None, description="추가 약관 번호")
    member_no: int | None = Field(None, description="회원 번호")
    mall_no: int | None = Field(None, description="몰 번호")
    agree: bool | None = Field(None, description="동의 여부")
    agree_date_time: KstDatetime | None = Field(None, description="동의 일시")
    mobile_no: str | None = Field(None, description="회원 전화번호")
    email: str | None = Field(None, description="회원 이메일")


class CustomTermsMembersResponse(BaseDto):
    """
    추가 약관 동의 회원 목록 조회 응답

    OpenAPI Schema: terms-custom-customTermsNo-members2042102439
    """

    total_count: int = Field(..., description="전체 데이터 개수")
    contents: list[CustomTermsMember] = Field(default_factory=list, description="회원 목록")

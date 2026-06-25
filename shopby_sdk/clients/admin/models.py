"""Admin API 모델 정의"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


# ------------------------------------
#  Literal 타입 별칭 (Enum)
# ------------------------------------
SettlementPeriodType = Literal["DAY", "WEEK", "MONTH"]
"""정산 유형 - DAY: 일 정산, WEEK: 주 정산, MONTH: 월 정산"""

SettlementHolidayType = Literal["TOMORROW", "YESTERDAY"]
"""정산 타입 - TOMORROW: 익일, YESTERDAY: 전일"""

SettlementDayOfWeek = Literal[
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
    "SUNDAY",
]
"""정산 요일"""

SellerTaxationType = Literal[
    "NORMAL",
    "SIMPLE",
    "VAT_FREE",
    "CORPORATION",
    "FREE_CORPORATION",
    "ETC",
]
"""과세 형태 - NORMAL: 일반과세자, SIMPLE: 간이과세자, VAT_FREE: 부가세 면세사업자,
CORPORATION: 법인사업자, FREE_CORPORATION: 면세법인사업자, ETC: 기타"""

ContractStatusUpdateType = Literal["APPROVAL", "DISAPPROVAL", "SUSPEND", "UNSUSPEND"]
"""계약 상태 변경 - APPROVAL: 계약 동의, DISAPPROVAL: 계약 반려,
SUSPEND: 계약 일시정지, UNSUSPEND: 계약 일시정지 해제"""

ContractType = Literal["ELECTRONIC", "HANDWRITING"]
"""거래 유형 - ELECTRONIC: 전자계약, HANDWRITING: 수기계약"""

AdminStatus = Literal[
    "WAITING",
    "INVESTIGATION",
    "ACTIVE",
    "DELETE",
    "LOCKED",
    "DORMANT",
]
"""어드민 상태 - WAITING: 등록대기, INVESTIGATION: 검토중, ACTIVE: 등록완료,
DELETE: 삭제, LOCKED: 로그인 잠금, DORMANT: 휴면"""

AdminRole = Literal["MASTER", "NORMAL"]
"""어드민 권한 - MASTER: 마스터, NORMAL: 일반"""

AdminType = Literal["PLATFORM", "SERVICE", "PARTNER", "SHOPBY", "DEVELOPER"]
"""어드민 타입 - PLATFORM: 플랫폼 어드민, SERVICE: 서비스 어드민,
PARTNER: 파트너 어드민, SHOPBY: 샵바이 어드민, DEVELOPER: 개발자"""

PartnerType = Literal["NORMAL", "MALLDELIVERY", "DELIVERY", "SHOPBY"]
"""파트너 유형 - NORMAL: 일반, MALLDELIVERY: 배송파트너(deprecated),
DELIVERY: 배송파트너, SHOPBY: 샵바이 파트너"""

PartnerStatus = Literal["WAITING", "INVESTIGATION", "ACTIVE"]
"""파트너 상태 - WAITING: 등록대기, INVESTIGATION: 검토중, ACTIVE: 등록완료"""

BankCode = Literal[
    "ANONYMOUS",
    "KDB",
    "IBK",
    "KB",
    "KEB",
    "SUHYUP",
    "SUHYUP_LOCAL_BANK",
    "KEXIM",
    "NH",
    "NHLOCAL",
    "WOORI",
    "SC",
    "CITY",
    "DAEGU",
    "PUSAN",
    "GWANGJU",
    "JEJU",
    "JEONBUK",
    "GYEONGNAM",
    "KFCC",
    "CU",
    "SANGHO",
    "HSBC",
    "DEUTSCHE",
    "NFCF",
    "EPOST",
    "KEBHANA",
    "SHINHAN",
    "KBANK",
    "KAKAO",
    "TOSS",
    "YUANTA",
    "KBSEC",
    "MIRAE",
    "MIRAEDAEWOO",
    "SAMSUNG",
    "HANKOOK",
    "NH_INVEST",
    "KYOBO",
    "HI_INVEST",
    "HMC_INVEST",
    "KIWOOM",
    "EBEST",
    "SK",
    "DAISHIN",
    "SOLOMON_INVEST",
    "HANHWA",
    "HANA_INVEST",
    "SHINHAN_INVEST",
    "DONGBU",
    "EUGENE_INVEST",
    "MERITZ_COMPREHENSIVE",
    "BOOKOOK",
    "SHINYOUNG",
    "CAPE",
    "MIZUHO",
    "UFJ",
    "SMBC",
    "RESONA",
]
"""은행 코드"""

ProductAuthorityType = Literal[
    "REGISTER_PRODUCT",
    "MODIFY_PRODUCT",
    "SELL_SETTING",
    "DISPLAY_SETTING",
]
"""운영그룹 권한타입 - REGISTER_PRODUCT: 상품 등록, MODIFY_PRODUCT: 상품 수정,
SELL_SETTING: 판매설정, DISPLAY_SETTING: 전시설정"""

ProductAuditType = Literal[
    "SALE_METHOD_TYPE",
    "MANUFACTURE_NAME",
    "PRODUCT_MODEL_NAME",
    "SERIAL_NUMBER",
    "ADMIN_NO",
    "CATEGORY_NO",
    "DISPLAY_CATEGORY_NOS",
    "REPRESENTATIVE_DISPLAY_CATEGORY_NO",
    "PLATFORM_DISPLAY_INFO",
    "URL_DIRECT_DISPLAY_YN",
    "PRODUCT_NAME",
    "PRODUCT_NAME_EN",
    "PROMOTION_TEXT_INFO",
    "BRAND_NO",
    "PAYMENT_MEANS_CONTROL_YN",
    "PAYMENT_MEANS",
    "NONMEMBER_PURCHASE_YN",
    "NAVER_PAY_LIMIT_YN",
    "KAKAO_PAY_LIMIT_YN",
    "MINOR_PURCHASE_YN",
    "CART_INFO",
    "KEYWORDS",
    "RESERVATION_INFO",
    "SALE_PERIOD_INFO",
    "COMMISSION_INFO",
    "SALE_PRICE",
    "UNIT_PRICE_INFO",
    "CONTENTS_IF_PAUSING",
    "IMMEDIATE_DISCOUNT_INFO",
    "PURCHASE_PRICE",
    "ACCUMULATION_RATE",
    "ACCUMULATION_USE_YN",
    "PROMOTION_INFO",
    "USE_RESTOCK_NOTI_YN",
    "MIN_BUY_CNT",
    "MAX_BUY_COUNT_INFO",
    "OPTION_USE_YN",
    "DUTY_CONTENT",
    "CERTIFICATION_INFO",
    "PLACE_ORIGIN_INFO",
    "SUPPLIER_PRODUCT_NAME",
    "MANUFACTURE_YMDT",
    "EXPIRATION_YMDT",
    "VALUE_ADDED_TAX_TYPE",
    "PRODUCT_MANAGEMENT_CD",
    "EXTRA_MANAGEMENT_CD",
    "HS_CODE",
    "REFUNDABLE_YN",
    "STICKER_MAPPINGS",
    "EXTRA_PRODUCT_ONLY",
    "EXTRA_PRODUCT_CONFIG",
    "PRODUCT_MAIN_IMAGE",
    "PRODUCT_ADDITIONAL_IMAGES",
    "MALL_PRODUCT_LIST_IMAGE",
    "CONTENT_HEADER",
    "CONTENT",
    "CONTENT_FOOTER",
    "GUIDE_DELIVERY",
    "GUIDE_AFTER_SERVICE",
    "GUIDE_REFUND",
    "GUIDE_EXCHANGE",
    "SHIPPING_AREA_TYPE",
    "DELIVERY_DUE_DATE",
    "DELIVERY_COMBINATION_YN",
    "DELIVERY_INTERNATIONAL_YN",
    "TOTAL_WEIGHT",
    "DELIVERY_TEMPLATE_NO",
    "DELIVERY_CUSTOMER_INFO",
    "PROP_NO_VALUE_MAP",
]
"""운영그룹 심사항목 타입 (상품 등록/수정 시 심사 대상 필드)"""


# ------------------------------------
#  공통 중첩 객체
# ------------------------------------
class SettlementConfig(BaseDto):
    """정산 설정 (응답용 - 지급비율 포함)"""

    settlement_period_type: SettlementPeriodType | None = Field(
        None, description="정산유형"
    )
    domestic_provision_rate: float | None = Field(None, description="국내파트너 지급비율")
    domestic_settlement_day: int | None = Field(None, description="국내파트너 정산예정일")
    domestic_settlement_holiday_type: SettlementHolidayType | None = Field(
        None, description="국내파트너 휴일 정산타입"
    )
    domestic_settlement_day_of_week: SettlementDayOfWeek | None = Field(
        None, description="국내파트너 주 정산요일"
    )
    overseas_provision_rate: float | None = Field(None, description="해외파트너 지급비율")
    overseas_settlement_day: int | None = Field(None, description="해외파트너 정산예정일")
    overseas_settlement_holiday_type: SettlementHolidayType | None = Field(
        None, description="해외파트너 휴일 정산타입"
    )
    overseas_settlement_day_of_week: SettlementDayOfWeek | None = Field(
        None, description="해외파트너 주 정산요일"
    )


class SettlementConfigRequest(BaseDto):
    """정산 설정 (요청용 - 지급비율 제외)"""

    settlement_period_type: SettlementPeriodType | None = Field(
        None, description="정산유형"
    )
    domestic_settlement_day: int | None = Field(None, description="국내파트너 정산예정일")
    domestic_settlement_holiday_type: SettlementHolidayType | None = Field(
        None, description="국내파트너 휴일 정산타입"
    )
    domestic_settlement_day_of_week: SettlementDayOfWeek | None = Field(
        None, description="국내파트너 주 정산요일"
    )
    overseas_settlement_day: int | None = Field(None, description="해외파트너 정산예정일")
    overseas_settlement_holiday_type: SettlementHolidayType | None = Field(
        None, description="해외파트너 휴일 정산타입"
    )
    overseas_settlement_day_of_week: SettlementDayOfWeek | None = Field(
        None, description="해외파트너 주 정산요일"
    )


# ------------------------------------
#  Admin (어드민) 관련
# ------------------------------------
class AdminAuthorityResponse(BaseDto):
    """
    샵바이 어드민 권한 조회 응답

    OpenAPI Schema: admins1091512367
    """

    authority_group_name: str | None = Field(None, description="권한그룹명")
    permits_private_information: bool | None = Field(
        None, description="개인정보 열람가능 여부"
    )


class MerchandiserAdmin(BaseDto):
    """
    상품담당 MD 운영자

    OpenAPI Schema: admins-merchandisers-1458267913 (items)
    """

    admin_no: int = Field(..., description="운영자 번호")
    name: str = Field(..., description="운영자 이름")
    id: str = Field(..., description="운영자 아이디")


class AdminDetailResponse(BaseDto):
    """
    샵바이 어드민 조회 응답

    OpenAPI Schema: admins-adminNo933950945
    """

    admin_no: int = Field(..., description="어드민 번호")
    admin_name: str | None = Field(None, description="운영자명")
    admin_id: str | None = Field(None, description="어드민 Id")
    job_position_name: str | None = Field(None, description="직급")
    department_name: str | None = Field(None, description="부서")
    job_duty_name: str | None = Field(None, description="직책")
    email: str | None = Field(None, description="이메일")
    phone_no: str | None = Field(None, description="전화번호")
    mobile_no: str | None = Field(None, description="휴대전화번호")
    external_access_enabled: bool | None = Field(None, description="외부접속 가능 여부")
    # 운영데이터 전부 빈 배열([]) + 스펙상 items 가 oneOf(object/boolean/string/number)
    # 자유형식 → 타입화 불가, list[Any] 유지
    permitted_ip_addresses: list[Any] = Field(
        default_factory=list, description="접속 가능 IP"
    )
    phone_certification_yn: bool | None = Field(None, description="휴대폰 인증 여부")
    expire_date_time: KstDatetime | None = Field(None, description="만료일")
    admin_status: AdminStatus | None = Field(None, description="어드민 상태")
    admin_type: AdminType | None = Field(None, description="어드민 타입")
    admin_role: AdminRole | None = Field(None, description="어드민 권한")
    service_no: int | None = Field(None, description="서비스 번호")
    partner_no: int | None = Field(None, description="파트너 번호")


# ------------------------------------
#  Mall-Domain / Mall / Service 관련
# ------------------------------------
class MallDomain(BaseDto):
    """
    몰 도메인 정보

    OpenAPI Schema: configurations-admin-domains1790762806 (items)
    """

    mall_no: int = Field(..., description="쇼핑몰 번호")
    mall_id: str = Field(..., description="쇼핑몰 ID")
    domain: str = Field(..., description="대표 도메인")
    device_type: str = Field(..., description="디바이스 타입")
    ssl: bool = Field(..., description="보안서버 사용여부")


class MallUrl(BaseDto):
    """몰 URL 정보"""

    pc: str | None = Field(None, description="PC 웹 도메인")
    mobile: str | None = Field(None, description="모바일 웹 도메인")
    android: str | None = Field(None, description="AOS 모바일 앱 정보")
    ios: str | None = Field(None, description="iOS 모바일 앱 정보")


class MallProductDetailUrl(BaseDto):
    """몰 상품 상세페이지 URL 정보"""

    pc: str | None = Field(None, description="PC 상품 상세페이지 URL")
    mobile: str | None = Field(None, description="모바일 상품 상세페이지 URL")


class MallDetailResponse(BaseDto):
    """
    쇼핑몰 상세 조회 응답

    OpenAPI Schema: malls-1901494364
    """

    mall_name: str = Field(..., description="몰 이름")
    mall_type: str | None = Field(None, description="몰 타입(deprecated)")
    url: MallUrl | None = Field(None, description="몰 URL 정보")
    product_detail_url: MallProductDetailUrl | None = Field(
        None, description="상품 상세페이지 URL 정보"
    )


class ShopbyPartnerResponse(BaseDto):
    """
    쇼핑몰 자체 파트너 조회 응답

    OpenAPI Schema: malls-shopby-partner1061824175
    """

    partner_no: int = Field(..., description="파트너 번호")
    partner_name: str = Field(..., description="파트너 이름")


class ServiceRepresentative(BaseDto):
    """서비스 대표자 정보"""

    name: str | None = Field(None, description="대표자명")
    phone_no: str | None = Field(None, description="대표 전화번호")
    email: str | None = Field(None, description="대표 이메일")


class ServiceAddress(BaseDto):
    """서비스 주소 정보"""

    zip_code: str | None = Field(None, description="우편번호")
    address: str | None = Field(None, description="도로명주소")
    detail_address: str | None = Field(None, description="도로명주소 상세")
    jibun: str | None = Field(None, description="지번주소")
    jibun_detail: str | None = Field(None, description="지번주소 상세")


class ServiceBusiness(BaseDto):
    """서비스 사업자 정보"""

    registration_no: str | None = Field(None, description="사업자 등록번호")
    online_marketing_declaration_no: str | None = Field(
        None, description="통신판매신고번호"
    )
    condition: str | None = Field(None, description="업태")
    type: str | None = Field(None, description="업종")


class ServiceDetailResponse(BaseDto):
    """
    서비스 상세 조회 응답

    OpenAPI Schema: services-1386425601
    """

    service_name: str | None = Field(None, description="서비스 이름")
    service_plan: str | None = Field(None, description="서비스 플랜")
    representative: ServiceRepresentative | None = Field(None, description="대표자 정보")
    address: ServiceAddress | None = Field(None, description="주소 정보")
    business: ServiceBusiness | None = Field(None, description="사업자 정보")


# ------------------------------------
#  Currency (환율) 관련
# ------------------------------------
class Currency(BaseDto):
    """
    몰 환율 설정

    OpenAPI Schema: currencies495944049 (items)
    """

    exchange_to: str = Field(..., description="통화 - cny, usd, jpy, krw")
    exchange_rate: float = Field(..., description="비율")


class CurrencyUpdateRequest(BaseDto):
    """
    몰 환율 설정 수정 요청

    OpenAPI Schema: currencies-currencyCode-1479264625
    """

    exchange_rate: float = Field(..., description="비율")


# ------------------------------------
#  Contract (계약서) 관련
# ------------------------------------
class ContractListItem(BaseDto):
    """
    계약서 목록 항목

    OpenAPI Schema: contracts1337707563 (contents items)
    """

    contract_no: int = Field(..., description="계약서 번호")
    mall_no: int = Field(..., description="쇼핑몰 번호")
    partner_no: int = Field(..., description="파트너 번호")
    merchandiser_no: int | None = Field(None, description="담당MD 번호")
    commission_rate: float | None = Field(None, description="수수료율")
    memo: str | None = Field(None, description="전달할 메모")
    contract_type: int | None = Field(None, description="거래 유형")
    promotion_agreed: bool | None = Field(None, description="프로모션 동의 여부")
    status: str | None = Field(None, description="계약서 상태")
    additional_info: str | None = Field(
        None, description="추가 정보(jsonString 형식)"
    )
    settlement_config: SettlementConfig | None = Field(None, description="정산 설정")


class ContractListResponse(BaseDto):
    """
    계약서 조회 응답

    OpenAPI Schema: contracts1337707563
    """

    total_count: int = Field(..., description="전체 조회건수")
    contents: list[ContractListItem] = Field(
        default_factory=list, description="조회 결과"
    )


class ContractStatusUpdateRequest(BaseDto):
    """
    계약서 상태 수정 요청

    OpenAPI Schema: contracts-925074272
    """

    status: ContractStatusUpdateType = Field(..., description="변경할 상태")
    contract_nos: list[int] = Field(
        default_factory=list, description="계약서 번호 목록"
    )


class ContractCreateRequest(BaseDto):
    """
    신규 계약 등록 요청

    OpenAPI Schema: contracts-1430861437
    """

    partner_no: int = Field(..., description="파트너 번호")
    commission_rate: float | None = Field(None, description="수수료율")
    merchandiser_no: int | None = Field(
        None, description="신규 거래 진행 쇼핑몰 MD 의 운영자 번호"
    )
    contract_content: str | None = Field(None, description="입점 계약서")
    memo: str | None = Field(None, description="전달 메모")
    contract_type: ContractType | None = Field(None, description="계약 유형")
    additional_info: str | None = Field(
        None, description="추가 정보(jsonString 형식)"
    )
    settlement_config: SettlementConfigRequest | None = Field(
        None, description="정산 설정"
    )


class ContractUpdateRequest(BaseDto):
    """
    계약서 수정 요청

    OpenAPI Schema: contracts-partnerNo1004672849
    """

    merchandiser_no: int | None = Field(
        None, description="신규 거래 진행 쇼핑몰 MD 의 운영자 번호"
    )
    commission_rate: float | None = Field(None, description="수수료율")
    contract_content: str | None = Field(None, description="입점 계약서")
    memo: str | None = Field(None, description="전달 메모")
    contract_type: ContractType | None = Field(None, description="계약 유형")
    additional_info: str | None = Field(
        None, description="추가 정보(jsonString 형식)"
    )
    settlement_config: SettlementConfigRequest | None = Field(
        None, description="정산 설정"
    )


class EntryContract(BaseDto):
    """입점 계약서 항목"""

    contents: str | None = Field(None, description="입점계약서 내용")
    change_reason: str | None = Field(None, description="입점계약서 변경 사유")
    agreed: bool | None = Field(None, description="입점계약서 동의 여부")
    created_date_time: KstDatetime | None = Field(None, description="생성일시")
    agreed_date_time: KstDatetime | None = Field(None, description="동의일시")


class ContractDetailResponse(BaseDto):
    """
    계약서 상세 조회 응답

    OpenAPI Schema: contracts-partnerNo981751615
    """

    contract_no: int = Field(..., description="계약번호")
    mall_no: int = Field(..., description="쇼핑몰 번호")
    partner_no: int = Field(..., description="파트너 번호")
    merchandiser_no: int | None = Field(None, description="담당MD 번호")
    contract_type: str | None = Field(None, description="거래 유형")
    contract_status: str | None = Field(None, description="거래 상태")
    commission_rate: float | None = Field(None, description="수수료율")
    promotion_agreed: bool | None = Field(None, description="프로모션 동의 여부")
    created_date_time: KstDatetime | None = Field(None, description="생성일시")
    started_date_time: KstDatetime | None = Field(None, description="거래일시")
    entry_contracts: list[EntryContract] = Field(
        default_factory=list, description="입점계약서 목록"
    )
    external_api_key: str | None = Field(None, description="쇼핑몰 외부 연동 키")
    settlement_config: SettlementConfig | None = Field(None, description="정산 설정")


# ------------------------------------
#  Partner (파트너) 관련 - 조회/목록
# ------------------------------------
class ContractedPartner(BaseDto):
    """
    계약된 파트너 정보

    OpenAPI Schema: malls-contracts-partners129363156 (items)
    """

    partner_no: int = Field(..., description="파트너 번호")
    partner_name: str | None = Field(None, description="파트너 이름")
    company_name: str | None = Field(None, description="회사 이름")
    partner_mapping_key: str | None = Field(None, description="파트너 매핑키")
    commission_rate: float | None = Field(None, description="수수료율")
    promotion_agreed: bool | None = Field(None, description="프로모션 동의 여부")
    started_date_time: KstDatetime | None = Field(None, description="거래일시")
    external_api_key: str | None = Field(None, description="외부시스템 연동코드")
    partner_type: PartnerType | None = Field(None, description="파트너 타입")
    agreement_date_time: KstDatetime | None = Field(
        None, description="최종 입점 계약서 동의 날짜"
    )
    settlement_config: SettlementConfig | None = Field(None, description="정산 설정")


class PartnerBusiness(BaseDto):
    """파트너 사업자 정보 (조회)"""

    condition: str | None = Field(None, description="업태")
    registration_no: str | None = Field(None, description="사업자 등록번호")
    type: str | None = Field(None, description="업종")
    online_marketing_declaration_no: str | None = Field(
        None, description="통신판매 신고번호"
    )


class PartnerOffice(BaseDto):
    """파트너 사무실 주소 정보 (조회)"""

    country: str | None = Field(None, description="국가")
    zip_code: str | None = Field(None, description="우편번호")
    address: str | None = Field(None, description="도로명주소 (한국)")
    detail_address: str | None = Field(None, description="도로명주소 상세 (한국)")
    jibun: str | None = Field(None, description="지번주소 (한국)")
    jibun_detail: str | None = Field(None, description="지번주소 상세 (한국)")
    city: str | None = Field(None, description="도시 (해외)")
    state_or_region: str | None = Field(None, description="주 (해외)")


class PartnerRepresentative(BaseDto):
    """파트너 대표자 정보 (조회)"""

    name: str | None = Field(None, description="대표자명")
    phone_no: str | None = Field(None, description="대표전화번호")
    email: str | None = Field(None, description="대표 e메일")


class PartnerManager(BaseDto):
    """파트너 담당자 정보 (조회)"""

    name: str | None = Field(None, description="담당자명")
    department: str | None = Field(None, description="담당자 부서")
    job_duty: str | None = Field(None, description="담당자 직책")
    job_position: str | None = Field(None, description="담당자 직급")
    phone_no: str | None = Field(None, description="담당자 전화번호")
    email: str | None = Field(None, description="담당자 e메일 주소")


class PartnerPrivacyManager(BaseDto):
    """파트너 개인정보 관리 책임자 정보 (조회)"""

    name: str | None = Field(None, description="개인정보 관리 담당자명")
    phone_no: str | None = Field(None, description="개인정보 관리 담당자 전화번호")


class PartnerSettlementManager(BaseDto):
    """파트너 정산담당자 정보 (조회)"""

    name: str | None = Field(None, description="정산담당자")
    email: str | None = Field(None, description="정산담당자 e메일")
    phone_no: str | None = Field(None, description="정산담당자 전화번호")


class PartnerTradeBank(BaseDto):
    """파트너 계좌 정보 (조회)"""

    bank: str | None = Field(None, description="은행 코드")
    bank_name: str | None = Field(None, description="은행명")
    account: str | None = Field(None, description="계좌번호")
    depositor_name: str | None = Field(None, description="예금주명")


class PartnerInternationalCode(BaseDto):
    """파트너 해외 코드 정보 (조회)"""

    swift_code: str | None = Field(None, description="SWIFT Code")
    aba_routing_no: str | None = Field(None, description="ABA / Routing No.")
    iban_code: str | None = Field(None, description="IBAN Code")
    bsb_code: str | None = Field(None, description="BSB Code")


class PartnerCsManager(BaseDto):
    """파트너 CS 운영자 정보 (조회)"""

    name: str | None = Field(None, description="담당자명")
    phone_no: str | None = Field(None, description="담당자 전화번호")
    email: str | None = Field(None, description="담당자 email")
    operation_info: str | None = Field(None, description="CS 운영시간")


class PartnerDetailResponse(BaseDto):
    """
    몰과 계약된 파트너 조회 응답

    OpenAPI Schema: partners-partnerNo-1657211906
    """

    partner_no: int = Field(..., description="파트너 번호")
    partner_type: PartnerType | None = Field(None, description="파트너 타입")
    partner_name: str | None = Field(None, description="파트너명")
    company_name: str | None = Field(None, description="회사명")
    partner_status: PartnerStatus | None = Field(None, description="파트너 상태")
    fax_no: str | None = Field(None, description="팩스 번호")
    sample_url: str | None = Field(None, description="샘플 URL")
    permitted_ip_address: str | None = Field(None, description="접속 허용 IP 주소")
    country_code: str | None = Field(None, description="국가 코드")
    seller_taxation_type: SellerTaxationType | None = Field(
        None, description="과세 형태"
    )
    supports_international_shipping: bool | None = Field(
        None, description="해외배송 여부"
    )
    business: PartnerBusiness | None = Field(None, description="사업자 정보")
    office: PartnerOffice | None = Field(None, description="사무실 주소 정보")
    representative: PartnerRepresentative | None = Field(
        None, description="대표자 정보"
    )
    manager: PartnerManager | None = Field(None, description="담당자 정보")
    privacy_manager: PartnerPrivacyManager | None = Field(
        None, description="개인정보 관리 책임자 정보"
    )
    settlement_manager: PartnerSettlementManager | None = Field(
        None, description="정산담당자 정보"
    )
    trade_bank: PartnerTradeBank | None = Field(None, description="계좌 정보")
    international_code: PartnerInternationalCode | None = Field(
        None, description="해외 코드 정보"
    )
    master_admin_no: int | None = Field(
        None, description="계약 담당자(마스터 어드민) 번호"
    )
    master_admin_summary: AdminDetailResponse | None = Field(
        None, description="마스터 어드민 요약 정보"
    )
    settlement_config: SettlementConfig | None = Field(None, description="정산 설정")
    cs_manager: PartnerCsManager | None = Field(
        None, description="고객 CS 운영자 정보"
    )


# ------------------------------------
#  Partner (파트너) 관련 - 등록 요청
# ------------------------------------
class PartnerCsManagerCreate(BaseDto):
    """파트너 CS 담당자 정보 (등록 요청)"""

    cs_manager_name: str | None = Field(None, description="파트너 CS 담당자명")
    cs_manager_phone_no: str | None = Field(
        None, description="파트너 CS 담당자 전화번호"
    )
    cs_manager_email: str | None = Field(None, description="파트너 CS 담당자 email")
    cs_manager_operation_info: str | None = Field(
        None, description="파트너 CS 운영시간"
    )


class PartnerManagerCreate(BaseDto):
    """파트너 담당자 정보 (등록/수정 요청)"""

    name: str | None = Field(None, description="담당자 이름")
    job_duty: str | None = Field(None, description="담당자 직책")
    job_position: str | None = Field(None, description="담당자 직급")
    department: str | None = Field(None, description="담당자 부서")
    phone_no: str | None = Field(None, description="담당자 전화번호")
    email: str | None = Field(None, description="담당자 이메일")


class PartnerBusinessCreate(BaseDto):
    """파트너 사업자 정보 (등록 요청)"""

    registration_no: str = Field(..., description="사업자 등록번호")
    condition: str = Field(..., description="업태")
    type: str = Field(..., description="업종")
    online_marketing_declaration_no: str = Field(
        ..., description="통신판매 신고번호"
    )


class PartnerPrivacyManagerCreate(BaseDto):
    """파트너 개인정보 관리 담당자 정보 (등록/수정 요청)"""

    name: str | None = Field(None, description="개인정보 관리 담당자명")
    phone_no: str | None = Field(None, description="개인정보 관리 담당자 전화번호")


class PartnerSettlementManagerCreate(BaseDto):
    """파트너 정산담당자 정보 (등록 요청)"""

    name: str = Field(..., description="정산담당자 이름")
    phone_no: str = Field(..., description="정산담당자 전화번호")
    email: str = Field(..., description="정산담당자 이메일")


class PartnerOfficeCreate(BaseDto):
    """파트너 사무실 주소 정보 (등록 요청)"""

    zip_code: str = Field(..., description="우편번호")
    street_address1: str = Field(..., description="도로명주소")
    street_address2: str = Field(..., description="도로명주소 상세")
    jibun_address1: str | None = Field(None, description="지번주소")
    jibun_address2: str | None = Field(None, description="지번주소 상세")


class PartnerTradeBankCreate(BaseDto):
    """파트너 계좌 정보 (등록/수정 요청)"""

    bank: BankCode | None = Field(None, description="은행코드")
    bank_name: str | None = Field(None, description="은행명")
    account: str = Field(..., description="계좌번호")
    depositor_name: str = Field(..., description="예금주 명")


class PartnerRepresentativeCreate(BaseDto):
    """파트너 대표자 정보 (등록 요청)"""

    name: str = Field(..., description="대표자 이름")
    phone_no: str = Field(..., description="대표자 전화번호")
    email: str = Field(..., description="대표자 이메일")


class PartnerAdminCreate(BaseDto):
    """파트너 마스터 어드민 정보 (등록 요청)"""

    id: str = Field(..., description="마스터 어드민 아이디")
    password: str = Field(..., description="마스터 패스워드")
    name: str = Field(..., description="마스터 어드민 이름")
    email: str = Field(..., description="마스터 어드민 이메일")
    job_duty: str | None = Field(None, description="마스터 어드민 직책")
    department_name: str | None = Field(None, description="마스터 부서")
    job_position: str | None = Field(None, description="마스터 직급")
    phone_no: str | None = Field(None, description="마스터 어드민 전화번호")
    mobile_no: str | None = Field(None, description="마스터 어드민 핸드폰번호")
    external_access_enabled: bool | None = Field(
        None, description="마스터 어드민 외부 접속 허용 여부"
    )


class PartnerCreateRequest(BaseDto):
    """
    파트너 등록 요청

    OpenAPI Schema: partners-1165227605
    """

    partner_name: str = Field(..., description="파트너명")
    operation_group_no: int = Field(..., description="운영그룹 번호")
    merchandiser_no: int | None = Field(None, description="담당 MD")
    promotion_agreed_yn: bool | None = Field(
        None, description="마케팅 수신동의 여부"
    )
    commission_rate: float | None = Field(None, description="수수료율")
    company_name: str | None = Field(None, description="회사명")
    fax_no: str | None = Field(None, description="팩스 번호")
    seller_taxation_type: SellerTaxationType | None = Field(
        None, description="과세 형태"
    )
    business: PartnerBusinessCreate | None = Field(None, description="사업자 정보")
    office: PartnerOfficeCreate | None = Field(None, description="사무실 주소 정보")
    representative: PartnerRepresentativeCreate | None = Field(
        None, description="대표자 정보"
    )
    settlement_manager: PartnerSettlementManagerCreate | None = Field(
        None, description="정산담당자 정보"
    )
    settlement_config: SettlementConfigRequest | None = Field(
        None, description="정산 설정"
    )
    trade_bank: PartnerTradeBankCreate | None = Field(None, description="계좌 정보")
    privacy_manager: PartnerPrivacyManagerCreate | None = Field(
        None, description="개인정보 관리 담당자 정보"
    )
    manager: PartnerManagerCreate | None = Field(None, description="담당자 정보")
    cs_manager: PartnerCsManagerCreate | None = Field(
        None, description="파트너 CS 담당자 정보"
    )
    admin: PartnerAdminCreate | None = Field(
        None, description="마스터 어드민 정보"
    )
    partner_mapping_key: str | None = Field(None, description="파트너 매핑키")


class TempPartnerCreateRequest(BaseDto):
    """
    임시 파트너 등록 요청

    OpenAPI Schema: partners-temp1179850777
    """

    partner_name: str = Field(..., description="파트너명")
    operation_group_no: int = Field(..., description="운영그룹 번호")
    admin_name: str = Field(..., description="운영자명")
    admin_email: str = Field(..., description="운영자 이메일")
    merchandiser_no: int | None = Field(None, description="담당MD 운영자 번호")
    memo: str | None = Field(None, description="전달 메모")
    commission_rate: float | None = Field(None, description="수수료율")
    contract_content: str | None = Field(None, description="입점 계약서")
    dependency_yn: bool | None = Field(None, description="파트너 노출 설정 여부")
    settlement_config: SettlementConfigRequest | None = Field(
        None, description="정산 설정"
    )


class PartnerCreateResponse(BaseDto):
    """
    파트너 등록 응답

    OpenAPI Schema: partners-temp970273924
    """

    partner_no: int = Field(..., description="생성된 파트너 번호")


# ------------------------------------
#  Partner (파트너) 관련 - 수정 요청
# ------------------------------------
class PartnerOfficeUpdate(BaseDto):
    """파트너 사무실 주소 정보 (수정 요청)"""

    zip_code: str | None = Field(None, description="우편번호")
    address: str | None = Field(None, description="도로명주소")
    detail_address: str | None = Field(None, description="도로명주소 상세")
    jibun: str | None = Field(None, description="지번주소")
    jibun_detail: str | None = Field(None, description="지번주소 상세")


class PartnerBusinessUpdate(BaseDto):
    """파트너 사업자 정보 (수정 요청)"""

    registration_no: str | None = Field(None, description="사업자 등록번호")
    condition: str | None = Field(None, description="업태")
    type: str | None = Field(None, description="업종")
    online_marketing_declaration_no: str | None = Field(
        None, description="통신판매 신고번호"
    )


class PartnerRepresentativeUpdate(BaseDto):
    """파트너 대표자 정보 (수정 요청)"""

    name: str | None = Field(None, description="대표자 이름")
    phone_no: str | None = Field(None, description="대표자 전화번호")
    email: str | None = Field(None, description="대표자 이메일")


class PartnerSettlementManagerUpdate(BaseDto):
    """파트너 정산담당자 정보 (수정 요청)"""

    name: str | None = Field(None, description="정산담당자 이름")
    phone_no: str | None = Field(None, description="정산담당자 전화번호")
    email: str | None = Field(None, description="정산담당자 이메일")


class PartnerCsManagerUpdate(BaseDto):
    """파트너 CS 운영자 정보 (수정 요청)"""

    name: str | None = Field(None, description="파트너 CS 담당자명")
    phone_no: str | None = Field(None, description="파트너 CS 담당자 전화번호")
    email: str | None = Field(None, description="파트너 CS 담당자 email")
    operation_info: str | None = Field(None, description="파트너 CS 운영시간")


class PartnerUpdateRequest(BaseDto):
    """
    파트너 수정 요청

    OpenAPI Schema: partners-partnerNo370412418
    """

    office: PartnerOfficeUpdate | None = Field(None, description="사무실 주소 정보")
    company_name: str | None = Field(None, description="회사명")
    seller_taxation_type: SellerTaxationType | None = Field(
        None, description="과세 형태"
    )
    fax_no: str | None = Field(None, description="팩스 번호")
    representative: PartnerRepresentativeUpdate | None = Field(
        None, description="대표자 정보"
    )
    business: PartnerBusinessUpdate | None = Field(None, description="사업자 정보")
    settlement_manager: PartnerSettlementManagerUpdate | None = Field(
        None, description="정산 담당자 정보"
    )
    trade_bank: PartnerTradeBankCreate | None = Field(None, description="계좌정보")
    permitted_ip_address: str | None = Field(None, description="접속 허용 IP 주소")
    privacy_manager: PartnerPrivacyManagerCreate | None = Field(
        None, description="개인정보 관리 책임자 정보"
    )
    manager: PartnerManagerCreate | None = Field(None, description="담당자 정보")
    sample_url: str | None = Field(None, description="샘플 URL")
    cs_manager: PartnerCsManagerUpdate | None = Field(
        None, description="고객 CS 운영자 정보"
    )


class ExistResultResponse(BaseDto):
    """
    중복 체크 결과 응답

    OpenAPI Schema: partners-exist-admin-id1887798343
    """

    result: bool = Field(..., description="중복 확인 결과")


# ------------------------------------
#  Operation (운영그룹) 관련
# ------------------------------------
class OperationGroupSalesCommission(BaseDto):
    """운영그룹 판매수수료 설정"""

    type: str | None = Field(None, description="판매 수수료 타입")
    is_fixed: bool | None = Field(None, description="판매 수수료 고정 여부")


class OperationGroupShippingArea(BaseDto):
    """운영그룹 배송구분 설정"""

    type: str | None = Field(None, description="배송구분 타입")
    is_fixed: bool | None = Field(None, description="배송구분 고정 여부")


class OperationGroupDefaultConfig(BaseDto):
    """운영그룹 기본값 설정"""

    sales_commission: OperationGroupSalesCommission | None = Field(
        None, description="판매수수료"
    )
    shipping_area: OperationGroupShippingArea | None = Field(
        None, description="배송구분"
    )


class OperationGroupAuthority(BaseDto):
    """운영그룹 권한 정보"""

    authority_group_type: str | None = Field(None, description="권한그룹 타입")
    authority_types: list[ProductAuthorityType] = Field(
        default_factory=list, description="권한타입 목록"
    )


class OperationGroupItem(BaseDto):
    """
    운영그룹 목록 항목

    OpenAPI Schema: operation-groups125425807 (contents items)
    """

    operation_group_no: int = Field(..., description="운영그룹 번호")
    name: str | None = Field(None, description="운영그룹 명")
    description: str | None = Field(None, description="운영그룹 설명")
    audit_step: str | None = Field(None, description="심사 절차")
    audit_types: list[ProductAuditType] = Field(
        default_factory=list, description="심사 항목"
    )
    default_config: OperationGroupDefaultConfig | None = Field(
        None, description="기본값 지정"
    )
    authorities: list[OperationGroupAuthority] = Field(
        default_factory=list, description="권한 정보"
    )
    creator_name: str | None = Field(None, description="등록자")
    created_date_time: KstDatetime | None = Field(None, description="등록일시")
    modifier_name: str | None = Field(None, description="최종 수정자")
    modified_date_time: KstDatetime | None = Field(None, description="최종 수정일자")


class OperationGroupListResponse(BaseDto):
    """
    운영그룹 목록 조회 응답

    OpenAPI Schema: operation-groups125425807
    """

    total_count: int = Field(..., description="전체 조회건수")
    contents: list[OperationGroupItem] = Field(
        default_factory=list, description="조회 결과"
    )

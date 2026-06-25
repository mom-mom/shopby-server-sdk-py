"""Delivery API 모델 정의"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


# ------------------------------------
#  Literal 타입 별칭 (Enum)
# ------------------------------------
ShippingAreaType = Literal["MALL_SHIPPING_AREA", "PARTNER_SHIPPING_AREA"]
"""배송 구분 (MALL_SHIPPING_AREA: 쇼핑몰 배송, PARTNER_SHIPPING_AREA: 파트너사 배송)"""

GroupDeliveryAmtType = Literal["MAXIMUM_SELECTED", "MINIMUM_SELECTED"]
"""배송비 템플릿 그룹 선택 유형 (MAXIMUM_SELECTED: 최대부과, MINIMUM_SELECTED: 최소부과)"""

DeliveryConditionType = Literal[
    "FREE",
    "CONDITIONAL",
    "FIXED_FEE",
    "QUANTITY_PROPOSITIONAL_FEE",
    "PRICE_FEE",
    "QUANTITY_FEE",
    "WEIGHT_FEE",
]
"""배송비 유형 (FREE: 무료, CONDITIONAL: 조건부 무료, FIXED_FEE: 유료(고정 배송비),
QUANTITY_PROPOSITIONAL_FEE: 수량 비례, PRICE_FEE: 금액별 차등, QUANTITY_FEE: 수량별 차등,
WEIGHT_FEE: 중량별 차등)"""

DeliveryType = Literal["PARCEL_DELIVERY", "DIRECT_DELIVERY"]
"""배송 방법 (PARCEL_DELIVERY: 택배/등기/소포, DIRECT_DELIVERY: 직접배송(화물배달))"""

DeliveryCompanyType = Literal[
    "CJ",
    "POST",
    "HANJIN",
    "GTX",
    "LOTTE",
    "KGB",
    "LOGEN",
    "GSI",
    "KGL",
    "INTRAS",
    "UPS",
    "JAPANPOST",
    "YAMATO",
    "SAGAWA",
    "CHUNIL",
    "KDEXP",
    "HDEXP",
    "ILYANG",
    "POST_EMS",
    "DAESIN",
    "CVS",
    "DHL",
    "FEDEX",
    "GSM",
    "WARPEX",
    "WIZWA",
    "ACI",
    "PANTOS",
    "CJ_INTERNATIONAL",
    "TNT",
    "CU",
    "KUNYOUNG",
    "LOTTE_INTERNATIONAL",
    "HONAM",
    "HANIPS",
    "IPARCEL",
    "SLX",
    "USPS",
    "WONDERS",
    "REGISTPOST",
    "DHLDE",
    "EZUSA",
    "SWGEXP",
    "DAEWOON",
    "DODOFLEX",
    "NH_LOGIS",
    "UFO",
    "TODAY_PICKUP",
    "QEXPRESS",
    "PINGPONG",
    "CR_LOGITECH",
    "TODAY",
    "SELLUV",
    "EXMATE",
    "WINION_LOGIS",
    "ETC",
]
"""배송 회사 (택배사 코드)"""

CountryCode = Literal[
    "AX", "AD", "AU", "AT", "BH", "BE", "BZ", "BR",
    "BN", "BG", "CA", "ES_CANARY", "CL", "CN", "CO", "CR",
    "CY", "CZ", "DK", "EC", "EG", "SV", "EE", "FR",
    "GF", "DE", "GR", "GL", "GU", "GT", "GG", "GY",
    "HK", "HU", "IS", "ID", "IE", "IL", "IT", "JP",
    "JE", "JO", "KR", "KW", "LV", "LB", "LI", "LT",
    "LU", "MO", "PT_MADEIRA", "MY", "NL", "NZ", "GB_NORTHERN_ISLAND", "NO",
    "PY", "PE", "PL", "PT", "RO", "RU", "SM", "SA",
    "GB_SCOTLAND", "SG", "SK", "SI", "ES", "CH", "TW", "TH",
    "TR", "AE", "GB", "US", "U2", "UY", "VN", "GB_WALES",
    "YE", "HR", "MT", "FI", "SE", "AF", "AL", "DZ",
    "AS", "AO", "AI", "AQ", "AG", "AR", "AM", "AW",
    "AZ", "BS", "BD", "BB", "BY", "BJ", "BM", "BT",
    "BO", "BA", "BW", "IO", "VG", "BF", "BI", "KH",
    "CM", "CV", "KY", "CF", "TD", "CX", "CC", "KM",
    "CK", "CU", "CW", "CD", "DJ", "DM", "DO", "TL",
    "GQ", "ER", "ET", "FK", "FO", "FJ", "PF", "GA",
    "GM", "GE", "GH", "GI", "GD", "GN", "GW", "HT",
    "HN", "IN", "IR", "IQ", "IM", "CI", "JM", "KZ",
    "KE", "KI", "XK", "KG", "LA", "LS", "LR", "LY",
    "MK", "MG", "MW", "MV", "ML", "MH", "MR", "MU",
    "YT", "MX", "FM", "MD", "MC", "MN", "ME", "MS",
    "MA", "MZ", "MM", "NA", "NR", "NP", "AN", "NC",
    "NI", "NE", "NG", "NU", "KP", "MP", "OM", "PK",
    "PW", "PS", "PA", "PG", "PH", "PN", "PR", "QA",
    "CG", "RE", "RW", "BL", "SH", "KN", "LC", "MF",
    "PM", "VC", "WS", "ST", "SN", "RS", "SC", "SL",
    "SX", "SB", "SO", "ZA", "SS", "LK", "SD", "SR",
    "SJ", "SZ", "SY", "TJ", "TZ", "TG", "TK", "TO",
    "TT", "TN", "TM", "TC", "TV", "VI", "UG", "UA",
    "UZ", "VU", "VA", "VE", "WF", "EH", "ZM", "ZW",
]
"""국가코드 (ISO 기반 Shopby 국가코드)"""


# ------------------------------------
#  공용 중첩 모델
# ------------------------------------
class WarehouseAddress(BaseDto):
    """입출고/창고 주소"""

    address: str | None = Field(None, description="기본 주소")
    detail_address: str | None = Field(None, description="상세 주소")
    zip_cd: str | None = Field(None, description="우편번호(zip/postal code)")
    address_str: str | None = Field(None, description="전체 주소")
    jibun_address: str | None = Field(None, description="지번 주소")
    oversea_address1: str | None = Field(None, description="Street Address1(해외)")
    oversea_address2: str | None = Field(None, description="Street Address2(해외)")
    oversea_city: str | None = Field(None, description="City(해외)")
    oversea_region: str | None = Field(None, description="State(해외)")
    country_cd: CountryCode | None = Field(None, description="국가코드")
    country_cd_label: str | None = Field(None, description="국가명")


class WarehouseSummary(BaseDto):
    """배송비 템플릿 내 출고지/반품지 요약 정보"""

    warehouse_no: int | None = Field(None, description="입출고 주소 번호")
    name: str | None = Field(None, description="입출고 주소 명")
    substitution_text: str | None = Field(None, description="대체문구")
    address: WarehouseAddress | None = Field(None, description="주소")
    default_release_warehouse: bool | None = Field(None, description="대표 출고지 여부")
    default_return_warehouse: bool | None = Field(None, description="대표 반품지 여부")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    summary: str | None = Field(None, description="요약")


class DeliveryFeeRange(BaseDto):
    """차등 조건 구간"""

    above_or_equal: float | None = Field(None, description="~이상")
    below: float | None = Field(None, description="~미만")
    delivery_amt: float | None = Field(None, description="해당 구간에서의 배송비")


class DeliveryFee(BaseDto):
    """배송비 설정"""

    delivery_condition_type: DeliveryConditionType | None = Field(None, description="배송비 유형")
    delivery_amt: float | None = Field(None, description="배송비(조건부 무료, 유료일 때)")
    return_delivery_amt: float | None = Field(None, description="반품 배송비")
    criteria: float | None = Field(None, description="조건부 무료 조건")
    per_order_cnt: int | None = Field(None, description="수량 비례 조건에서 수량")
    remote_area_fee_condition_check: bool | None = Field(
        None, description="지역별 추가 배송비 조건부 무료 체크 여부(NCP는 현재 false 고정)"
    )
    delivery_fee_ranges: list[DeliveryFeeRange] | None = Field(
        None, description="차등 조건 구간"
    )
    delivery_condition_type_label: str | None = Field(None, description="배송비 유형 라벨")


# ------------------------------------
#  지역별 추가배송비 (AreaFee)
# ------------------------------------
class AreaFeeDetail(BaseDto):
    """지역별 추가배송비 상세 (응답)"""

    area_no: int = Field(..., description="지역번호")
    default_area: bool | None = Field(None, description="기본 지역 여부")
    address: str | None = Field(None, description="지역 주소")
    road_address: str | None = Field(None, description="도로명 주소")
    jibun_address: str | None = Field(None, description="지번 주소")
    state: str | None = Field(None, description="주 (미국, 캐나다, 일본 필수)")
    extra_delivery_amt: float = Field(..., description="추가배송비")


class AreaFee(BaseDto):
    """
    지역별 추가배송비 설정

    OpenAPI Schema: areafees-642934700
    """

    area_fee_no: int = Field(..., description="지역별 추가배송비 번호")
    name: str | None = Field(None, description="지역별 추가배송비 명")
    country_cd: CountryCode | None = Field(None, description="국가코드")
    country_cd_label: str | None = Field(None, description="국가명")
    details: list[AreaFeeDetail] = Field(default_factory=list, description="지역별 추가배송비 상세")
    area_cnt: int | None = Field(None, description="추가배송비 설정 지역수")
    currency_code: str | None = Field(None, description="통화 정보")
    admin_name: str | None = Field(None, description="등록 어드민 명")
    register_ymdt: KstDatetime | None = Field(None, description="등록일시")


class AreaFeesResponse(BaseDto):
    """
    지역별 추가배송비 설정 내역 조회 응답

    OpenAPI Schema: areafees-82223564
    """

    total_count: int = Field(..., description="지역별 추가배송비 설정 개수")
    contents: list[AreaFee] = Field(default_factory=list, description="지역별 추가배송비 내역")


class AreaFeeDetailRequest(BaseDto):
    """지역별 추가배송비 상세 (요청)"""

    area_no: int = Field(..., description="지역번호")
    extra_delivery_amt: float = Field(..., description="추가배송비")


class AreaFeeRequest(BaseDto):
    """
    지역별 추가배송비 설정 생성/수정 요청

    OpenAPI Schema: areafees20396953
    """

    name: str = Field(..., description="지역별 추가배송비 명")
    country_cd: CountryCode = Field(..., description="국가코드")
    details: list[AreaFeeDetailRequest] = Field(
        default_factory=list, description="지역별 추가배송비 상세"
    )
    currency_code: str | None = Field(None, description="통화 정보 (nullable)")


# ------------------------------------
#  배송비 설정 지역 (Area)
# ------------------------------------
class Area(BaseDto):
    """
    배송비 설정을 위한 지역

    OpenAPI Schema: areas864143670 (items)
    """

    area_no: int = Field(..., description="지역 번호")
    address: str | None = Field(None, description="주소")
    road_address: str | None = Field(None, description="도로명 주소")
    jibun_address: str | None = Field(None, description="지번 주소")
    zip_cd: str | None = Field(None, description="우편번호")
    country_cd: str | None = Field(None, description="국가코드")
    state: str | None = Field(None, description="주 (미국, 캐나다, 일본 필수)")
    city: str | None = Field(None, description="도시 (해외용)")
    is_default_area: bool | None = Field(None, description="기본으로 제공되는 지역 여부")


# ------------------------------------
#  배송비 템플릿 (Delivery)
# ------------------------------------
class DeliveryTemplate(BaseDto):
    """
    배송비 템플릿 (간략 조회)

    OpenAPI Schema: deliveries-323369351 (items)
    """

    delivery_template_no: int = Field(..., description="배송비템플릿 번호")
    template_name: str | None = Field(None, description="배송비 템플릿 이름")
    release_warehouse_address_str: str | None = Field(None, description="출고지 주소")
    shipping_area_type: ShippingAreaType | None = Field(None, description="배송 구분")


class TemplateDetail(BaseDto):
    """
    배송비 템플릿 상세

    OpenAPI Schema: deliveries-templates-templateNo-820869304
    """

    template_no: int = Field(..., description="배송비 템플릿 번호")
    partner_no: int | None = Field(None, description="파트너번호")
    name: str | None = Field(None, description="배송비 템플릿명")
    group_name: str | None = Field(None, description="배송 그룹 명")
    default: bool | None = Field(None, description="기본 템플릿 여부")
    release_warehouse: WarehouseSummary | None = Field(None, description="출고지")
    return_warehouse: WarehouseSummary | None = Field(None, description="반품지")
    delivery_type: DeliveryType | None = Field(None, description="배송 방법")
    delivery_company_type: DeliveryCompanyType | None = Field(None, description="배송 회사")
    delivery_fee: DeliveryFee | None = Field(None, description="배송비 설정")


class TemplateGroupTemplate(BaseDto):
    """배송비 템플릿 그룹 내 템플릿 항목"""

    template_no: int = Field(..., description="배송비 템플릿 번호")
    name: str | None = Field(None, description="배송비 템플릿 명")
    group_name: str | None = Field(None, description="배송 그룹 명")
    partner_no: int | None = Field(None, description="파트너 번호")
    default: bool | None = Field(None, description="기본 템플릿 여부")
    release_warehouse: WarehouseSummary | None = Field(None, description="출고지")
    return_warehouse: WarehouseSummary | None = Field(None, description="반품지")
    delivery_type: DeliveryType | None = Field(None, description="배송 방법")
    delivery_type_label: str | None = Field(None, description="배송 방법 라벨")
    delivery_company_type: DeliveryCompanyType | None = Field(None, description="배송 회사")
    delivery_fee: DeliveryFee | None = Field(None, description="배송비 설정")


class TemplateGroup(BaseDto):
    """
    배송비 템플릿 그룹 상세

    OpenAPI Schema: deliveries-template-groups1180750672 (단건),
    deliveries-template-groups1699109495 (items, shippingAreaType 포함)
    """

    template_group_no: int = Field(..., description="배송비 템플릿 그룹번호")
    name: str | None = Field(None, description="배송비 템플릿 그룹명")
    display_no: int | None = Field(None, description="그룹 노출 순서")
    group_delivery_amt_type: GroupDeliveryAmtType | None = Field(
        None, description="배송비 템플릿 그룹 선택 유형"
    )
    prepaid: bool | None = Field(None, description="배송비 선결제 여부")
    shipping_area_type: ShippingAreaType | None = Field(None, description="배송 구분")
    area_fee: AreaFee | None = Field(None, description="지역별 추가배송비 상세")
    templates: list[TemplateGroupTemplate] = Field(
        default_factory=list, description="템플릿 내역"
    )
    currency_code: str | None = Field(None, description="통화 정보")
    summary: str | None = Field(None, description="배송비 템플릿 그룹 요약")


# ------------------------------------
#  배송비 템플릿 그룹 생성/수정 요청
# ------------------------------------
class TemplateRequest(BaseDto):
    """배송비 템플릿 생성 요청 (그룹 생성/추가용)"""

    name: str = Field(..., description="배송비 템플릿 명")
    delivery_type: DeliveryType = Field(..., description="배송 방법")
    delivery_company_type: DeliveryCompanyType | None = Field(None, description="배송 회사")
    delivery_fee: DeliveryFee = Field(..., description="배송비 설정")
    release_warehouse_no: int | None = Field(None, description="출고지 번호")
    return_warehouse_no: int | None = Field(None, description="반품지 번호")
    default: bool | None = Field(None, description="기본 템플릿 여부")


class TemplateModifyRequest(BaseDto):
    """배송비 템플릿 수정 요청"""

    template_no: int = Field(..., description="배송비 템플릿 번호")
    name: str = Field(..., description="배송비 템플릿 명")
    delivery_type: DeliveryType = Field(..., description="배송 방법")
    delivery_company_type: DeliveryCompanyType | None = Field(None, description="배송 회사")
    delivery_fee: DeliveryFee = Field(..., description="배송비 설정")
    release_warehouse_no: int | None = Field(None, description="출고지 번호")
    return_warehouse_no: int | None = Field(None, description="반품지 번호")
    default: bool | None = Field(None, description="기본 템플릿 여부")


class TemplateGroupCreateRequest(BaseDto):
    """
    배송비 템플릿 그룹 생성 요청

    OpenAPI Schema: deliveries-template-groups1608125329
    """

    name: str = Field(..., description="그룹명")
    group_delivery_amt_type: GroupDeliveryAmtType = Field(
        ..., description="배송비 템플릿 그룹 선택 유형"
    )
    prepaid: bool = Field(..., description="배송비 결제 선불 여부")
    uses_area_fee: bool | None = Field(None, description="지역별 추가배송비 사용 여부")
    area_fee_no: int | None = Field(None, description="사용할 지역별 추가배송비 번호")
    templates: list[TemplateRequest] = Field(default_factory=list, description="추가할 템플릿 내역")
    # request-only 필드 + 스펙 items 가 oneOf[object|boolean|string|number] (자유형식) →
    # 운영 응답에 미노출(검증 100+건 hit=0)이라 실데이터 추론 불가, dict/Any 유지
    undeliverable_countries: list[Any] = Field(
        default_factory=list, description="배송 불가능한 국가 리스트"
    )
    currency_code: str | None = Field(None, description="통화 정보 (nullable)")


class TemplateGroupUpdateRequest(BaseDto):
    """
    배송비 템플릿 그룹 수정 요청

    OpenAPI Schema: deliveries-template-groups-templateGroupNo1392913703
    """

    name: str = Field(..., description="그룹명")
    group_delivery_amt_type: GroupDeliveryAmtType = Field(
        ..., description="배송비 템플릿 그룹 선택 유형"
    )
    prepaid: bool = Field(..., description="배송비 결제 선불 여부")
    uses_area_fee: bool | None = Field(None, description="지역별 추가배송비 사용 여부")
    area_fee_no: int | None = Field(None, description="사용할 지역별 추가배송비 번호")
    delete_template_nos: list[int] = Field(
        default_factory=list, description="삭제할 템플릿 번호"
    )
    add_templates: list[TemplateRequest] = Field(
        default_factory=list, description="추가할 템플릿 리스트"
    )
    modify_templates: list[TemplateModifyRequest] = Field(
        default_factory=list, description="수정할 템플릿 리스트"
    )
    # request-only 필드 + 스펙 items 가 oneOf[object|boolean|string|number] (자유형식) →
    # 운영 응답에 미노출(검증 100+건 hit=0)이라 실데이터 추론 불가, dict/Any 유지
    undeliverable_countries: list[Any] = Field(
        default_factory=list, description="배송 불가능한 국가 리스트"
    )


# ------------------------------------
#  입출고 주소 (Warehouse)
# ------------------------------------
class Warehouse(BaseDto):
    """
    입출고 주소

    OpenAPI Schema: warehouses530577803
    """

    warehouse_no: int = Field(..., description="입출고 주소 번호")
    name: str | None = Field(None, description="입출고 주소명")
    substitution_text: str | None = Field(None, description="대체문구")
    address: WarehouseAddress | None = Field(None, description="주소")
    default_release_warehouse: bool | None = Field(None, description="대표 출고지 여부")
    default_return_warehouse: bool | None = Field(None, description="대표 반품지 여부")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    summary: str | None = Field(None, description="요약")


class WarehousesResponse(BaseDto):
    """
    입출고 주소 내역 조회 응답

    OpenAPI Schema: warehouses-445768110
    """

    total_count: int = Field(..., description="입출고 주소 개수")
    contents: list[Warehouse] = Field(default_factory=list, description="입출고 주소 내역")


class WarehouseAddressRequest(BaseDto):
    """입출고 주소 생성/수정 요청 내 주소"""

    address: str | None = Field(None, description="기본 주소")
    detail_address: str | None = Field(None, description="상세 주소")
    zip_cd: str | None = Field(None, description="우편번호(zip/postal code)")
    address_str: str | None = Field(None, description="전체 주소")
    jibun_address: str | None = Field(None, description="지번 주소")
    oversea_address1: str | None = Field(None, description="Street Address1(해외)")
    oversea_address2: str | None = Field(None, description="Street Address2(해외)")
    oversea_city: str | None = Field(None, description="City(해외)")
    oversea_region: str | None = Field(None, description="State(해외)")
    country_cd: CountryCode | None = Field(None, description="국가코드")
    country_cd_label: str | None = Field(None, description="국가명")


class WarehouseRequest(BaseDto):
    """
    입출고 주소 생성/수정 요청

    OpenAPI Schema: warehouses-605800327
    """

    name: str = Field(..., description="입출고 주소명")
    uses_substitution_text: bool | None = Field(None, description="대체문구 사용 여부")
    substitution_text: str | None = Field(None, description="대체문구(대체문구 사용 시)")
    address: WarehouseAddressRequest | None = Field(
        None, description="주소(대체문구 사용하지 않을 시)"
    )
    default_release_warehouse: bool | None = Field(None, description="대표 출고지 여부")
    default_return_warehouse: bool | None = Field(None, description="대표 반품/교환지 여부")

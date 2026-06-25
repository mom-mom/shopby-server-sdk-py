"""미구현 엔드포인트용 추가 모델 모음

product-server-public.yml 의 브랜드/추가항목/우선구매권한/재고/심사/옵션 등
엔드포인트에 대응하는 요청/응답 모델을 정의합니다.
"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime

# ------------------------------------
#  공통 Literal 별칭
# ------------------------------------
BrandNameType = Literal["NAME_KO", "NAME_EN", "NONE"]
"""브랜드명 타입 (NAME_KO: 한글, NAME_EN: 영문, NONE: 없음)"""

DiscountUnitType = Literal["WON", "RATE"]
"""할인 단위 타입 (WON: 정액, RATE: 정률)"""

ImmediateDiscountAmountUnitType = Literal["AMOUNT", "PERCENT"]
"""즉시할인 단위 (AMOUNT: 원, PERCENT: %)"""

SaleStatusType = Literal[
    "READY",
    "ONSALE",
    "FINISHED",
    "STOP",
    "PROHIBITION",
    "RESERVATION_ONSALE",
    "RESERVATION_FINISHED",
]
"""판매상태"""

PartialSaleStatusType = Literal["READY", "STOP", "PROHIBITION"]
"""부분수정용 판매상태 (READY: 판매가능, STOP: 판매중지, PROHIBITION: 판매금지)"""

OptionSaleType = Literal["AVAILABLE", "SOLD_OUT", "UNAVAILABLE"]
"""옵션 재고수량에 따른 상태"""

OptionSelectType = Literal["MULTI", "FLAT"]
"""옵션 선택 방식 (MULTI: 분리형, FLAT: 일체형)"""

OptionType = Literal["STANDARD", "COMBINATION", "DEFAULT", "MAPPING", "REQUIRED"]
"""옵션 타입"""

InputMatchingType = Literal["OPTION", "PRODUCT", "AMOUNT"]
"""구매자작성형 매칭타입"""

DeliveryConditionType = Literal[
    "FREE",
    "CONDITIONAL",
    "FIXED_FEE",
    "QUANTITY_PROPOSITIONAL_FEE",
    "PRICE_FEE",
    "QUANTITY_FEE",
    "WEIGHT_FEE",
]
"""배송비 타입"""

SalePeriodType = Literal["REGULAR", "PERIOD"]
"""판매기간 타입 (REGULAR: 상시 판매, PERIOD: 기간지정 판매)"""

ProductGuideType = Literal[
    "DELIVERY", "AFTER_SERVICE", "REFUND", "EXCHANGE", "DELEGATION_BY_LIQUOR"
]
"""상품 안내 타입"""

PartialQuickStatus = Literal["SUCCESS", "PARTIAL_SUCCESS", "FAILURE"]
"""상품 부분수정(quick) 처리 결과 상태"""


# ------------------------------------
#  브랜드 (Brand)
# ------------------------------------
class BrandTreeItem(BaseDto):
    """
    브랜드 전체 조회(트리 구조) 응답 항목

    OpenAPI Schema: brands488206837
    """

    no: int | None = Field(None, description="전시브랜드 번호")
    display_brand_no: int | None = Field(None, description="몰별 전시브랜드 번호")
    brand_no: int | None = Field(None, description="표준 브랜드 번호 (deprecated)")
    name: str | None = Field(None, description="브랜드 명")
    name_ko: str | None = Field(None, description="한글 브랜드명")
    name_en: str | None = Field(None, description="영문 브랜드명")
    name_type: BrandNameType | None = Field(None, description="브랜드명 타입")
    main_name: str | None = Field(None, description="메인 브랜드명")
    sub_name: str | None = Field(None, description="부가 브랜드명")
    maker_name: str | None = Field(None, description="메이커 명")
    logo_image_url: str | None = Field(None, description="로고 주소")
    homepage_url: str | None = Field(None, description="브랜드 홈페이지 주소")
    description: str | None = Field(None, description="브랜드 설명")
    display_area_content_url: str | None = Field(None, description="브랜드 이미지/동영상 url")
    extra_info: str | None = Field(None, description="추가 설명")
    main_image_contents: str | None = Field(None, description="메인 이미지(html, deprecated)")
    detail_contents: str | None = Field(None, description="상세(html, deprecated)")
    children: list["BrandTreeItem"] = Field(default_factory=list, description="하위 브랜드 목록")


class BrandDetailResponse(BaseDto):
    """
    브랜드 상세 조회 응답

    OpenAPI Schema: brands-displayBrandNo-94055997
    """

    no: int = Field(..., description="전시브랜드 번호")
    depth: int = Field(..., description="depth")
    main_name: str | None = Field(None, description="메인 브랜드명")
    sub_name: str | None = Field(None, description="부가 브랜드명")
    description: str | None = Field(None, description="브랜드 추가 설명")
    extra_info: str | None = Field(None, description="브랜드관련 추가 정보")
    display_area_content_url: str | None = Field(None, description="브랜드 이미지/동영상 url")
    main_image_contents: str | None = Field(None, description="브랜드 설명")
    detail_contents: str | None = Field(None, description="브랜드 상세 설명")
    children: list["BrandDetailResponse"] = Field(default_factory=list, description="하위 브랜드 목록")


class CreateBrandItem(BaseDto):
    """브랜드 생성 요청 항목 (brands 배열 내부)"""

    brand_name_ko: str = Field(..., description="한글 브랜드명(최대 200자)")
    brand_name_en: str | None = Field(None, description="영문 브랜드명(최대 200자)")
    brand_name_type: BrandNameType = Field("NAME_KO", description="브랜드명 타입(기본값: NAME_KO)")


class CreateBrandsRequest(BaseDto):
    """
    브랜드 생성 요청

    OpenAPI Schema: brands1145846976
    """

    brands: list[CreateBrandItem] = Field(default_factory=list, description="생성할 브랜드 목록")


class CreatedBrandItem(BaseDto):
    """브랜드 생성 결과 항목"""

    brand_no: int | None = Field(None, description="표준 브랜드 번호")
    display_brand_no: int | None = Field(None, description="몰별 전시브랜드 번호")
    brand_name: str | None = Field(None, description="브랜드명")
    brand_name_ko: str | None = Field(None, description="한글 브랜드명")
    brand_name_en: str | None = Field(None, description="영문 브랜드명")


class CreateBrandsResponse(BaseDto):
    """
    브랜드 생성 응답

    OpenAPI Schema: brands-795781552
    """

    brands: list[CreatedBrandItem] = Field(default_factory=list, description="생성 성공 브랜드 목록")
    failure_brands: list[CreatedBrandItem] = Field(
        default_factory=list, description="생성 실패(기존 존재) 브랜드 목록"
    )


class ModifyBrandItem(BaseDto):
    """
    브랜드 수정 요청 항목 (배열 body)

    OpenAPI Schema: brands-1783285449
    """

    no: int = Field(..., description="전시브랜드 번호")
    parent_no: int | None = Field(None, description="상위 브랜드 번호 (없으면 0)")
    depth: int | None = Field(None, description="depth")
    main_name: str | None = Field(None, description="메인 브랜드명(최대 30자)")
    sub_name: str | None = Field(None, description="부가 브랜드명(최대 30자)")
    description: str | None = Field(None, description="브랜드 설명")
    extra_info: str | None = Field(None, description="브랜드관련 추가 정보")
    display_area_content_url: str | None = Field(None, description="브랜드 이미지/동영상 url")
    brand_use_yn: str | None = Field(None, description="브랜드 사용 여부")


# ------------------------------------
#  상품 추가항목 (Custom Property)
# ------------------------------------
class CustomPropertyValue(BaseDto):
    """상품 추가항목 값"""

    value_no: int = Field(..., description="항목값 번호")
    value_name: str = Field(..., description="항목 값")


class CustomPropertyItem(BaseDto):
    """
    상품 추가항목 전체 조회 응답 항목

    OpenAPI Schema: custom-properties-53274064
    """

    property_no: int = Field(..., description="항목 번호")
    property_name: str = Field(..., description="항목명")
    multi_selection_enabled: bool = Field(..., description="복수 선택 가능 여부")
    values: list[CustomPropertyValue] = Field(default_factory=list, description="항목 값 목록")


class AddCustomPropertyMappingRequest(BaseDto):
    """
    상품 추가항목 매핑 추가 요청

    OpenAPI Schema: custom-properties-productNo-mappings-1712002327
    """

    prop_value_nos: list[int] = Field(default_factory=list, description="추가할 추가항목 값 번호 목록")


class CustomPropertyMappingResponse(BaseDto):
    """
    상품 추가항목 매핑 추가/삭제 응답

    OpenAPI Schema: custom-properties-productNo-mappings1661982912
    """

    success_prop_value_nos: list[int] = Field(default_factory=list, description="성공한 추가항목 값 번호 목록")
    failed_prop_value_nos: list[int] = Field(default_factory=list, description="실패한 추가항목 값 번호 목록")


# ------------------------------------
#  상품 정보 고시 항목 (Duty Category)
# ------------------------------------
class DutyCategoryContent(BaseDto):
    """상품 정보 고시 항목 내용"""

    display_order: int = Field(..., description="노출 순서")
    content_name: str = Field(..., description="항목값")
    data_type: str = Field(..., description="항목 타입")
    max_length: int = Field(..., description="최대 길이")
    descriptions: list[str] = Field(default_factory=list, description="설명 목록")


class DutyCategoryItem(BaseDto):
    """
    상품 정보 고시 항목 조회 응답 항목

    OpenAPI Schema: duty-categories1409269806
    """

    duty_category_no: int = Field(..., description="고시 항목 번호")
    duty_category_name: str = Field(..., description="고시 항목명")
    duty_category_description: str | None = Field(None, description="고시 항목 설명")
    duty_category_contents: list[DutyCategoryContent] = Field(
        default_factory=list, description="고시 항목 내용 목록"
    )


# ------------------------------------
#  회원이 좋아하는 상품 (Like Products)
# ------------------------------------
class LikeProductHasCoupons(BaseDto):
    """좋아요 상품 쿠폰 태그 정보"""

    product: bool = Field(..., description="상품쿠폰 태그")
    brand: bool = Field(..., description="브랜드쿠폰 태그")
    category: bool = Field(..., description="카테고리쿠폰 태그")
    partner: bool = Field(..., description="파트너쿠폰 태그")
    event: bool = Field(..., description="기획전쿠폰 태그")


class LikeProductStickerInfo(BaseDto):
    """좋아요 상품 스티커 정보"""

    no: int | None = Field(None, description="스티커 번호")
    label: str | None = Field(None, description="스티커 라벨")
    type: str | None = Field(None, description="스티커 타입")


class LikeProductOptionValue(BaseDto):
    """좋아요 상품 옵션값 정보"""

    mall_product_no: int | None = Field(None, description="상품번호")
    option_value: str | None = Field(None, description="옵션명")
    stock_cnt: int | None = Field(None, description="재고")


class LikeProductReservationData(BaseDto):
    """좋아요 상품 예약판매 정보"""

    reservation_start_ymdt: KstDatetime | None = Field(None, description="예약판매 시작일")
    reservation_end_ymdt: KstDatetime | None = Field(None, description="예약판매 종료일")
    reservation_delivery_ymdt: KstDatetime | None = Field(None, description="예약판매 배송시작일")
    reservation_stock_cnt: int | None = Field(None, description="예약판매 재고수량")


class LikeProductItem(BaseDto):
    """회원이 좋아하는 상품 항목"""

    product_no: int = Field(..., description="상품번호")
    product_name: str | None = Field(None, description="상품명")
    product_name_en: str | None = Field(None, description="영문 상품명")
    partner_name: str | None = Field(None, description="파트너명")
    promotion_text: str | None = Field(None, description="홍보문구")
    sale_price: float | None = Field(None, description="상품판매가")
    immediate_discount_amt: float | None = Field(None, description="즉시할인가")
    immediate_discount_unit_type: DiscountUnitType | None = Field(None, description="즉시할인 타입")
    addition_discount_amt: float | None = Field(None, description="추가상품할인가")
    addition_discount_unit_type: DiscountUnitType | None = Field(None, description="추가상품할인 타입")
    min_sale_price: float | None = Field(None, description="추가할인 최소 기준금액")
    max_sale_price: float | None = Field(None, description="추가할인 최대 기준금액")
    max_discount_amount: float | None = Field(None, description="추가할인 정률 최대 할인 금액")
    liked: bool | None = Field(None, description="좋아요 여부")
    like_count: int | None = Field(None, description="좋아요 수")
    review_rating: float | None = Field(None, description="상품평 평균점수")
    total_review_count: int | None = Field(None, description="총 상품평 수")
    delivery_condition_type: DeliveryConditionType | None = Field(None, description="배송비 타입")
    sale_cnt: int | None = Field(None, description="구매 수량")
    stock_cnt: int | None = Field(None, description="재고")
    main_stock_cnt: int | None = Field(None, description="대표 옵션 재고")
    brand_no: int | None = Field(None, description="브랜드 번호")
    brand_name: str | None = Field(None, description="브랜드 명")
    brand_name_en: str | None = Field(None, description="브랜드 영문 명")
    brand_name_ko: str | None = Field(None, description="브랜드 한글 명")
    sticker_infos: list[LikeProductStickerInfo] = Field(default_factory=list, description="스티커 정보 목록")
    sticker_labels: list[str] = Field(default_factory=list, description="스티커 라벨 목록")
    adult: bool | None = Field(None, description="성인 상품 여부")
    product_sale_period_type: SalePeriodType | None = Field(None, description="상품섹션 상품 노출 타입")
    sale_start_ymdt: KstDatetime | None = Field(None, description="판매시작일시")
    sale_end_ymdt: KstDatetime | None = Field(None, description="판매종료일시")
    sale_status_type: SaleStatusType | None = Field(None, description="판매상태")
    reservation_data: LikeProductReservationData | None = Field(None, description="예약판매 정보")
    image_urls: list[str] = Field(default_factory=list, description="이미지 URL 목록")
    list_image_urls: list[str] = Field(default_factory=list, description="리스트 이미지 URL 목록")
    has_coupons: LikeProductHasCoupons | None = Field(None, description="쿠폰 태그 정보")
    max_coupon_amt: float | None = Field(None, description="최대 쿠폰 할인 금액")
    coupon_discount_amt: float | None = Field(None, description="적용 가능한 최대 쿠폰 할인가")
    register_ymdt: KstDatetime | None = Field(None, description="상품 등록일")
    contents_if_pausing: str | None = Field(None, description="가격대체문구")
    display_category_nos: str | None = Field(None, description="전시카테고리 번호 정보")
    front_display_yn: bool | None = Field(None, description="전시 여부")
    url_direct_display_yn: bool | None = Field(None, description="상품조회화면 노출 여부")
    product_management_cd: str | None = Field(None, description="판매자 관리코드")
    main_best_product_yn: bool | None = Field(None, description="메인 베스트 상품 여부")
    coupon_tag: str | None = Field(None, description="쿠폰 태그")
    sale_period_type: SalePeriodType | None = Field(None, description="상품 노출 타입")
    option_values: list[LikeProductOptionValue] = Field(default_factory=list, description="옵션값 목록")
    section_product_start_ymdt: KstDatetime | None = Field(None, description="상품섹션 시작일")
    section_product_end_ymdt: KstDatetime | None = Field(None, description="상품섹션 종료일")
    hs_code: str | None = Field(None, description="HS CODE")
    enable_coupons: bool | None = Field(None, description="사용가능쿠폰 존재 여부")


class LikeProductsResponse(BaseDto):
    """
    회원이 좋아하는 상품목록 조회 응답

    OpenAPI Schema: like-products321647820
    """

    items: list[LikeProductItem] = Field(default_factory=list, description="상품 목록")
    total_count: int = Field(..., description="전체 상품 수")


# ------------------------------------
#  스티커 번호로 상품 조회 (by-stickers)
# ------------------------------------
class ProductByStickerItem(BaseDto):
    """스티커 번호로 조회된 상품 항목"""

    product_no: int = Field(..., description="상품 번호")
    product_name: str | None = Field(None, description="상품명")
    sticker_nos: list[int] = Field(default_factory=list, description="스티커 번호 목록")


class ProductByStickersResponse(BaseDto):
    """
    스티커 번호로 상품 정보 조회 응답

    OpenAPI Schema: products-by-stickers-835861226
    """

    total_count: int = Field(..., description="총 상품 개수")
    total_page: int = Field(..., description="총 페이지 수")
    contents: list[ProductByStickerItem] = Field(default_factory=list, description="상품 목록")
    last_id: str | None = Field(None, description="검색 기준 값")


# ------------------------------------
#  삭제된 상품 조회 (deleted)
# ------------------------------------
class DeletedProductItem(BaseDto):
    """삭제된 상품 항목"""

    product_no: int = Field(..., description="상품 번호")
    product_name: str | None = Field(None, description="상품명")
    deleted_by_admin_no: int | None = Field(None, description="삭제처리한 운영자 번호")
    deleted_ymdt: KstDatetime | None = Field(None, description="삭제된 날짜")


class DeletedProductsResponse(BaseDto):
    """
    삭제된 상품 정보 조회 응답

    OpenAPI Schema: products-deleted382191942
    """

    total_count: int = Field(..., description="총 개수")
    total_page: int = Field(..., description="총 페이지 수")
    contents: list[DeletedProductItem] = Field(default_factory=list, description="상품 목록")
    last_id: str | None = Field(None, description="검색 기준 값")


# ------------------------------------
#  추가정보 조회 (extraInfo)
# ------------------------------------
class ProductExtraInfoItem(BaseDto):
    """
    추가정보 조회 응답 항목

    OpenAPI Schema: products-extraInfo-1123228438
    """

    product_no: int = Field(..., description="상품 번호")
    extra_info: str | None = Field(None, description="추가 정보")


# ------------------------------------
#  글로벌 번호 매핑 조회
# ------------------------------------
class GlobalNoToProductNosItem(BaseDto):
    """글로벌 번호별 상품 번호 매핑"""

    global_product_no: int = Field(..., description="글로벌 상품 번호")
    product_nos: list[int] = Field(default_factory=list, description="상품 번호 목록")


class ProductNosByGlobalNosResponse(BaseDto):
    """
    글로벌 번호로 상품 번호 조회 응답

    OpenAPI Schema: products-global-by-global-nos-1784100189
    """

    items: list[GlobalNoToProductNosItem] = Field(default_factory=list, description="매핑 목록")


class ProductNoToGlobalNoItem(BaseDto):
    """상품 번호별 글로벌 번호 매핑"""

    product_no: int = Field(..., description="상품 번호")
    global_product_no: int = Field(..., description="글로벌 상품 번호")


class GlobalNosByProductNosResponse(BaseDto):
    """
    상품 번호로 글로벌 번호 조회 응답

    OpenAPI Schema: products-global-by-product-nos448016303
    """

    items: list[ProductNoToGlobalNoItem] = Field(default_factory=list, description="매핑 목록")


# ------------------------------------
#  심사대상 상품 조회 (inspections/approval-waiting)
# ------------------------------------
class InspectionGlobalProductName(BaseDto):
    """심사대상 상품 글로벌 몰별 상품명"""

    mall_name: str | None = Field(None, description="글로벌 몰 이름")
    product_name: str | None = Field(None, description="글로벌 상품 이름")


class InspectionWaitingItem(BaseDto):
    """심사대상 상품 항목"""

    mall_no: int | None = Field(None, description="쇼핑몰 번호")
    mall_name: str | None = Field(None, description="쇼핑몰명")
    product_no: int = Field(..., description="상품번호")
    product_name: str | None = Field(None, description="상품명")
    management_code: str | None = Field(None, description="상품관리코드")
    partner_name: str | None = Field(None, description="파트너명")
    brand_name: str | None = Field(None, description="브랜드명")
    representative_name: str | None = Field(None, description="담당자명")
    commission_rate: float | None = Field(None, description="수수료율")
    sale_start_date_time: KstDatetime | None = Field(None, description="판매 시작일")
    sale_end_date_time: KstDatetime | None = Field(None, description="판매 종료일")
    register_date_time: KstDatetime | None = Field(None, description="상품 등록일")
    apply_status: str | None = Field(None, description="승인 상태")
    approval_requested_date_time: KstDatetime | None = Field(None, description="승인 요청일")
    global_product_no: int | None = Field(None, description="글로벌 번호")
    global_product_names: list[InspectionGlobalProductName] = Field(
        default_factory=list, description="글로벌 몰별 상품명 목록"
    )


class InspectionWaitingResponse(BaseDto):
    """
    심사대상 상품 조회 응답

    OpenAPI Schema: products-inspections-approval-waiting1125661658
    """

    total_count: int = Field(..., description="전체 상품수")
    total_page: int = Field(..., description="전체 페이지수")
    contents: list[InspectionWaitingItem] = Field(default_factory=list, description="상품 목록")
    last_id: str | None = Field(None, description="검색 기준 값")


class InspectionViewResponse(BaseDto):
    """
    상품 심사 상세 조회 응답

    OpenAPI Schema: products-inspections-productNo-view140297670

    inspectionProductInfo / originProductInfo 는 전체 상품 객체로 매우 방대하여
    dict[str, Any] 로 노출합니다.
    """

    inspection_status: str | None = Field(None, description="승인상태")
    inspection_product_info: dict[str, Any] | None = Field(None, description="심사 대상 상품 정보")
    origin_product_info: dict[str, Any] | None = Field(None, description="원본 상품 정보")
    modified_param: list[str] = Field(default_factory=list, description="수정된 항목 목록")
    invalid_params: list[str] = Field(default_factory=list, description="유효하지 않은 항목 목록")


# ------------------------------------
#  상품재고관리 옵션 리스트 (options/stocks)
# ------------------------------------
class OptionStockView(BaseDto):
    """상품재고관리 옵션 항목"""

    mall_no: int | None = Field(None, description="몰 번호")
    mall_product_no: int | None = Field(None, description="상품 번호")
    product_name: str | None = Field(None, description="상품명")
    mall_option_no: int | None = Field(None, description="몰 옵션 번호")
    option_name: str | None = Field(None, description="옵션명")
    option_value: str | None = Field(None, description="옵션값")
    stock_no: int | None = Field(None, description="재고 번호")
    stock_cnt: int | None = Field(None, description="재고량")
    safety_stock_cnt: int | None = Field(None, description="안전재고량")
    safety_stock_sync_yn: str | None = Field(None, description="안전재고연동여부")
    delivery_waiting_stock_cnt: int | None = Field(None, description="배송대기재고량")
    stock_sync_yn: str | None = Field(None, description="재고 연동 여부")
    forced_sold_out: bool | None = Field(None, description="임시품절여부")
    partner_no: int | None = Field(None, description="파트너 번호")
    partner_name: str | None = Field(None, description="파트너 명")
    brand_no: int | None = Field(None, description="브랜드 번호")
    brand_name: str | None = Field(None, description="브랜드명")
    option_management_cd: str | None = Field(None, description="옵션관리코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")
    product_management_cd: str | None = Field(None, description="상품 관리 코드")
    sale_status_type: str | None = Field(None, description="판매 상태")
    sale_setting_status_type: str | None = Field(None, description="판매 설정 상태")
    apply_status_type: str | None = Field(None, description="승인 상태")
    front_display_yn: str | None = Field(None, description="전시 여부")
    sale_start_ymdt: KstDatetime | None = Field(None, description="판매 시작일")
    sale_end_ymdt: KstDatetime | None = Field(None, description="판매 종료일")


class OptionStocksResponse(BaseDto):
    """
    상품재고관리 옵션 리스트 조회 응답

    OpenAPI Schema: products-options-stocks-572756840
    """

    stock_views: list[OptionStockView] = Field(default_factory=list, description="옵션 재고 목록")
    mall_product_count: int = Field(..., description="조회된 상품 개수")


# ------------------------------------
#  필수 항목 조회 (required-properties)
# ------------------------------------
class RequiredPropertiesResponse(BaseDto):
    """
    필수 항목 조회 응답

    OpenAPI Schema: products-required-properties-541064860
    """

    mall_no: int | None = Field(None, description="몰 번호")
    required_properties: list[Any] = Field(default_factory=list, description="필수 항목 목록")


# ------------------------------------
#  예약배송 정보 벌크 조회 (reservation-infos)
# ------------------------------------
class ReservationInfoItem(BaseDto):
    """상품별 예약배송 정보"""

    product_no: int = Field(..., description="상품 번호")
    reservation_start_ymdt: KstDatetime | None = Field(None, description="예약 판매 시작일시")
    reservation_end_ymdt: KstDatetime | None = Field(None, description="예약 판매 종료일시")
    reservation_delivery_ymdt: KstDatetime | None = Field(None, description="예약 배송 시작일시")
    reservation_stock_cnt: int | None = Field(None, description="예약 재고 수량")


# ------------------------------------
#  상품 검색 (search)
# ------------------------------------
class ProductSearchElement(BaseDto):
    """상품 검색 결과 항목"""

    mall_product_no: int = Field(..., description="몰상품번호")
    product_name: str | None = Field(None, description="상품명")
    product_name_en: str | None = Field(None, description="영문상품명")
    sale_price: float | None = Field(None, description="판매가")
    sale_status_type: SaleStatusType | None = Field(None, description="판매 상태")
    sale_period_type: SalePeriodType | None = Field(None, description="판매기간 타입")
    class_type: str | None = Field(None, description="상품유형")
    sale_start_ymdt: KstDatetime | None = Field(None, description="판매시작일시")
    sale_end_ymdt: KstDatetime | None = Field(None, description="판매종료일시")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    update_ymdt: KstDatetime | None = Field(None, description="수정일")
    product_management_cd: str | None = Field(None, description="상품관리코드")
    platform_display_yn: str | None = Field(None, description="플랫폼 노출 설정 여부")
    platform_display_pc_yn: str | None = Field(None, description="플랫폼 - PC 여부")
    platform_display_mobile_yn: str | None = Field(None, description="플랫폼 - 모바일 앱 여부")
    platform_display_mobile_web_yn: str | None = Field(None, description="플랫폼 - 모바일 웹 여부")
    immediate_discount_unit_type: str | None = Field(None, description="즉시할인 단위")
    immediate_discount_value: float | None = Field(None, description="즉시할인가")
    immediate_discount_apply_price: float | None = Field(None, description="즉시할인 적용가")
    immediate_discount_period_yn: str | None = Field(None, description="즉시할인 기간 여부")
    immediate_discount_start_ymdt: KstDatetime | None = Field(None, description="즉시할인 시작 시간")
    immediate_discount_end_ymdt: KstDatetime | None = Field(None, description="즉시할인 종료 시간")


class ProductSearchResponse(BaseDto):
    """
    상품 검색 응답

    OpenAPI Schema: products-search1245134831
    """

    total_count: int = Field(..., description="총 개수")
    total_page: int = Field(..., description="총 페이지 수")
    elements: list[ProductSearchElement] = Field(default_factory=list, description="검색 결과 목록")
    last_id: int | None = Field(None, description="검색 기준 값(상품번호)")


# ------------------------------------
#  옵션 조회 (productNo/options)
# ------------------------------------
class ProductOptionImage(BaseDto):
    """옵션 이미지"""

    url: str | None = Field(None, description="이미지 URL")
    main: bool | None = Field(None, description="메인이미지 여부")


class ProductOptionRentalInfo(BaseDto):
    """옵션 렌탈 정보"""

    monthly_rental_amount: float | None = Field(None, description="월 렌탈 금액")
    rental_period: int | None = Field(None, description="렌탈 기간")
    credit_rating: int | None = Field(None, description="서비스 가능 최저 신용 등급")


class ProductFlatOption(BaseDto):
    """일체형(flat) 옵션 항목"""

    option_no: int = Field(..., description="옵션번호")
    label: str | None = Field(None, description="옵션명")
    value: str | None = Field(None, description="옵션값")
    add_price: float | None = Field(None, description="추가금액")
    buy_price: float | None = Field(None, description="할인적용가")
    stock_cnt: int | None = Field(None, description="재고수량")
    reservation_stock_cnt: int | None = Field(None, description="예약재고수량")
    sale_cnt: int | None = Field(None, description="판매수량")
    sale_type: OptionSaleType | None = Field(None, description="판매타입")
    main: bool | None = Field(None, description="대표 옵션 여부")
    forced_sold_out: bool | None = Field(None, description="임시 품절 여부")
    is_required_option: bool | None = Field(None, description="필수 옵션 여부")
    option_management_cd: str | None = Field(None, description="옵션 판매자 관리 코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")
    images: list[ProductOptionImage] = Field(default_factory=list, description="옵션 이미지 목록")
    rental_info: list[ProductOptionRentalInfo] = Field(default_factory=list, description="렌탈 정보 목록")


class ProductMultiLevelOptionChild(BaseDto):
    """다단계 옵션 하위 항목"""

    option_no: int = Field(..., description="옵션번호")
    label: str | None = Field(None, description="옵션명")
    value: str | None = Field(None, description="옵션값")
    add_price: float | None = Field(None, description="추가금액")
    buy_price: float | None = Field(None, description="할인적용가")
    stock_cnt: int | None = Field(None, description="재고수량")
    reservation_stock_cnt: int | None = Field(None, description="예약재고수량")
    sale_cnt: int | None = Field(None, description="판매수량")
    sale_type: OptionSaleType | None = Field(None, description="판매타입")
    main: bool | None = Field(None, description="대표 옵션 여부")
    forced_sold_out: bool | None = Field(None, description="임시 품절 여부")
    is_required_option: bool | None = Field(None, description="필수 옵션 여부")
    option_management_cd: str | None = Field(None, description="옵션 판매자 관리 코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")
    images: list[ProductOptionImage] = Field(default_factory=list, description="옵션 이미지 목록")
    rental_info: list[ProductOptionRentalInfo] = Field(default_factory=list, description="렌탈 정보 목록")
    children: list["ProductMultiLevelOptionChild"] = Field(
        default_factory=list, description="하위 옵션 목록"
    )


class ProductMultiLevelOption(BaseDto):
    """다단계(분리형) 옵션 항목"""

    label: str | None = Field(None, description="옵션명")
    value: str | None = Field(None, description="옵션값")
    is_required_option: bool | None = Field(None, description="필수 옵션 여부")
    children: list[ProductMultiLevelOptionChild] = Field(default_factory=list, description="하위 옵션 목록")


class ProductOptionInput(BaseDto):
    """구매자작성형(input) 옵션"""

    input_no: int = Field(..., description="텍스트 옵션 번호")
    input_label: str | None = Field(None, description="텍스트 옵션 입력 문구")
    input_matching_type: InputMatchingType | None = Field(None, description="매칭타입")
    required: bool | None = Field(None, description="필수 여부")


class ProductOptionsResponse(BaseDto):
    """
    옵션 조회 응답

    OpenAPI Schema: products-productNo-options54526912
    """

    type: OptionType | None = Field(None, description="옵션 타입")
    select_type: OptionSelectType | None = Field(None, description="옵션 선택 타입")
    labels: list[str] = Field(default_factory=list, description="옵션명 목록")
    flat_options: list[ProductFlatOption] = Field(default_factory=list, description="일체형 옵션 목록")
    multi_level_options: list[ProductMultiLevelOption] = Field(
        default_factory=list, description="다단계 옵션 목록"
    )
    inputs: list[ProductOptionInput] = Field(default_factory=list, description="구매자작성형 옵션 목록")


# ------------------------------------
#  상품우선구매권한 (Purchase Permission)
# ------------------------------------
class PurchasePermissionMember(BaseDto):
    """상품우선구매권한 회원 정보 (조회)"""

    member_no: int = Field(..., description="상품우선구매가능한 회원번호")
    purchase_cnt: int | None = Field(None, description="상품우선구매가능 개수")
    purchased_cnt: int | None = Field(None, description="회원이 구매한 개수")


class PurchasePermissionItem(BaseDto):
    """
    상품우선구매권한 조회 응답 항목

    OpenAPI Schema: purchase-permission-productNo (배열)
    """

    permission_no: int = Field(..., description="상품우선구매권한 번호")
    product_no: int = Field(..., description="상품번호")
    option_no: int | None = Field(None, description="옵션번호")
    stock_changeable: bool | None = Field(None, description="재고반영여부")
    purchase_start_at: KstDatetime | None = Field(None, description="상품구매가능시작일")
    purchase_end_at: KstDatetime | None = Field(None, description="상품구매가능종료일")
    member_permissions: list[PurchasePermissionMember] = Field(
        default_factory=list, description="회원 권한 목록"
    )


class PurchasePermissionMemberInput(BaseDto):
    """우선구매권한 회원 입력 항목 (생성/수정)"""

    member_no: int = Field(..., description="회원번호")
    purchase_cnt: int = Field(..., description="구매가능개수")


class ProductPermissionInput(BaseDto):
    """상품우선구매권한 상품 정보 (생성/수정)"""

    product_no: int = Field(..., description="상품번호")
    option_no: int | None = Field(None, description="옵션번호")
    stock_changeable: bool | None = Field(None, description="재고반영여부")
    purchase_start_at: KstDatetime | None = Field(None, description="구매가능시작일")
    purchase_end_at: KstDatetime | None = Field(None, description="구매가능종료일")


class CreatePurchasePermissionRequest(BaseDto):
    """
    상품우선구매권한 생성 요청

    OpenAPI Schema: purchase-permission-2025784983
    """

    product_permission: ProductPermissionInput = Field(..., description="상품 권한 정보")
    member_permissions: list[PurchasePermissionMemberInput] = Field(
        default_factory=list, description="회원 권한 목록"
    )


class CreatePurchasePermissionResponse(BaseDto):
    """
    상품우선구매권한 생성 응답

    OpenAPI Schema: purchase-permission380827083
    """

    permission_no: int = Field(..., description="상품우선구매권한 번호")


class UpdatePurchasePermissionProductRequest(BaseDto):
    """
    상품우선구매권한 수정 요청

    OpenAPI Schema: purchase-permission-product-permissionNo-968471606
    """

    product_no: int = Field(..., description="상품번호")
    option_no: int | None = Field(None, description="옵션번호")
    stock_changeable: bool | None = Field(None, description="재고반영여부")
    purchase_start_at: KstDatetime | None = Field(None, description="구매가능시작일")
    purchase_end_at: KstDatetime | None = Field(None, description="구매가능종료일")


# ------------------------------------
#  상품 부분수정 quick (partial/quick)
# ------------------------------------
class PartialQuickImmediateDiscount(BaseDto):
    """부분수정(quick) 즉시할인 정보"""

    unit_type: ImmediateDiscountAmountUnitType | None = Field(None, description="즉시 할인 단위")
    amount: float | None = Field(None, description="즉시 할인 금액")
    period_yn: str | None = Field(None, description="즉시 할인 기간 여부")
    start_ymdt: KstDatetime | None = Field(None, description="즉시 할인 시작 일시")
    end_ymdt: KstDatetime | None = Field(None, description="즉시 할인 종료 일시")


class PartialQuickPrice(BaseDto):
    """부분수정(quick) 가격 정보"""

    sale_price: float | None = Field(None, description="판매가")
    immediate_discount_info: PartialQuickImmediateDiscount | None = Field(
        None, description="즉시할인 정보"
    )


class PartialQuickItem(BaseDto):
    """
    상품 부분수정(quick) 요청 항목 (배열 body)

    OpenAPI Schema: products-partial-quick (요청)
    """

    product_no: int = Field(..., description="상품번호")
    front_display_yn: str | None = Field(None, description="전시 여부")
    use_restock_noti_yn: str | None = Field(None, description="재입고 알림 사용 여부")
    merchandiser_no: int | None = Field(None, description="상품 담당자")
    sale_status_type: SaleStatusType | None = Field(None, description="판매상태")
    price: PartialQuickPrice | None = Field(None, description="가격 정보")
    display_category_nos: list[int] = Field(default_factory=list, description="전시카테고리 번호 목록")


class PartialQuickSuccess(BaseDto):
    """부분수정(quick) 성공 항목"""

    product_no: int = Field(..., description="업데이트 성공한 상품번호")


class PartialQuickFailure(BaseDto):
    """부분수정(quick) 실패 항목"""

    product_no: int = Field(..., description="업데이트 실패한 상품번호")
    reason: str | None = Field(None, description="실패사유")


class PartialQuickResponse(BaseDto):
    """
    상품 부분수정(quick) 응답

    OpenAPI Schema: products-partial-quick471880406
    """

    status: PartialQuickStatus | None = Field(None, description="성공여부")
    success_list: list[PartialQuickSuccess] = Field(default_factory=list, description="성공 목록")
    failure_list: list[PartialQuickFailure] = Field(default_factory=list, description="실패 목록")


# ------------------------------------
#  네이버 쇼핑 인증키 설정
# ------------------------------------
class NaverShoppingConfigRequest(BaseDto):
    """
    네이버 쇼핑 인증키 설정 요청

    OpenAPI Schema: naver-shopping-sno-config823235906
    """

    use_yn: str = Field(..., description="네이버 쇼핑 사용 여부")
    common_auth_key: str = Field(..., description="네이버 쇼핑 인증키 (최대 20자)")


# ------------------------------------
#  상품 이용안내 템플릿 등록/수정 (guides)
# ------------------------------------
class ProductGuideRequest(BaseDto):
    """
    상품 이용안내 템플릿 등록/수정 요청

    OpenAPI Schema: products-guides-1895346613
    """

    type: str = Field(..., description="안내 타입")
    content: str = Field(..., description="내용")
    partner_no: int | None = Field(None, description="파트너 번호")


# ------------------------------------
#  상품 등록/수정 응답 (공통)
# ------------------------------------
class SavedProductResponse(BaseDto):
    """
    상품 등록/수정 응답 (공통)

    OpenAPI Schema: products-productNo-1357611564
    """

    mall_product_no: int = Field(..., description="저장된 상품번호")
    mall_product_input_nos: list[int] = Field(default_factory=list, description="저장된 구매자작성형 번호 목록")
    mall_product_option_nos: list[int] = Field(default_factory=list, description="저장된 옵션 번호 목록")


# ------------------------------------
#  옵션(구매자작성형) 수정 (PUT /products/options)
# ------------------------------------
class PutOptionImage(BaseDto):
    """옵션 수정 이미지"""

    image_url: str = Field(..., description="이미지 주소")
    main_yn: str | None = Field(None, description="대표이미지 여부")
    order: int | None = Field(None, description="전시순서")


class PutOptionInput(BaseDto):
    """옵션 수정 - 구매자작성형"""

    input_matching_type: InputMatchingType = Field(..., description="구매자작성형 매칭타입")
    input_text: str | None = Field(None, description="구매자작성형 텍스트 내용")
    use_yn: str | None = Field(None, description="사용여부")
    required: bool | None = Field(None, description="필수 여부")


class PutOption(BaseDto):
    """옵션 수정 - 옵션 항목"""

    mall_option_no: int | None = Field(None, description="옵션번호(수정 시)")
    option_name: str | None = Field(None, description="옵션명(조합형일 경우 |로 구분)")
    option_value: str | None = Field(None, description="옵션값(조합형일 경우 |로 구분)")
    add_price: float | None = Field(None, description="옵션 추가 가격")
    stock_cnt: int | None = Field(None, description="재고 수량")
    use_yn: str | None = Field(None, description="사용여부")
    option_type: OptionType | None = Field(None, description="옵션 타입")
    option_select_type: str | None = Field(None, description="옵션 선택 방식")
    option_management_cd: str | None = Field(None, description="옵션 판매자 관리코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")
    forced_sold_out: bool | None = Field(None, description="임시 품절 여부")
    item: bool | None = Field(None, description="자재상품 여부")
    order: int | None = Field(None, description="옵션 순서")
    option_images: list[PutOptionImage] = Field(default_factory=list, description="옵션 이미지 목록")


class PutProductOptionsRequest(BaseDto):
    """
    옵션(구매자작성형) 수정 요청

    OpenAPI Schema: products-options203128518
    """

    mall_product_no: int = Field(..., description="상품번호")
    options: list[PutOption] = Field(default_factory=list, description="옵션 목록")
    inputs: list[PutOptionInput] = Field(default_factory=list, description="구매자작성형 목록")


# ------------------------------------
#  옵션/상품 재고 변경 (stock)
# ------------------------------------
class OptionStockByIdItem(BaseDto):
    """옵션 번호 기준 재고 변경 항목"""

    option_no: int = Field(..., description="재고 변경할 옵션 번호")
    stock: int = Field(..., description="수정할 재고")


class PutStockByOptionNoRequest(BaseDto):
    """
    옵션 번호로 재고 변경 요청

    OpenAPI Schema: products-options-stock-with-id260366706
    """

    options: list[OptionStockByIdItem] = Field(default_factory=list, description="옵션 재고 목록")


class StockByOptionNoFailure(BaseDto):
    """옵션 번호 재고 변경 실패 항목"""

    option_no: int = Field(..., description="재고 변경에 실패한 옵션 번호")
    error_code: str | None = Field(None, description="에러 코드")


class PutStockByOptionNoResponse(BaseDto):
    """
    옵션 번호로 재고 변경 응답 (207)

    OpenAPI Schema: products-options-stock-with-id1338458380
    """

    failures: list[StockByOptionNoFailure] = Field(default_factory=list, description="실패 목록")


class OptionStockByCodeItem(BaseDto):
    """옵션 관리코드 기준 재고 변경 항목"""

    management_code: str = Field(..., description="재고 변경할 옵션 관리 코드")
    stock: int = Field(..., description="수정할 재고")


class PutStockByOptionCodeRequest(BaseDto):
    """
    옵션 관리코드로 재고 변경 요청

    OpenAPI Schema: products-options-stock-with-management-code227008429
    """

    options: list[OptionStockByCodeItem] = Field(default_factory=list, description="옵션 재고 목록")


class StockByOptionCodeFailure(BaseDto):
    """옵션 관리코드 재고 변경 실패 항목"""

    management_code: str | None = Field(None, description="재고 변경에 실패한 옵션 관리 코드")
    error_code: str | None = Field(None, description="에러 코드")


class PutStockByOptionCodeResponse(BaseDto):
    """
    옵션 관리코드로 재고 변경 응답 (207)

    OpenAPI Schema: products-options-stock-with-management-code1059532249
    """

    failures: list[StockByOptionCodeFailure] = Field(default_factory=list, description="실패 목록")


class ProductStockByCodeItem(BaseDto):
    """상품 관리코드 기준 재고 변경 항목"""

    product_management_code: str = Field(..., description="재고 변경할 상품 관리 코드")
    stock: int = Field(..., description="수정할 재고")


class PutStockByProductCodeRequest(BaseDto):
    """
    상품 관리코드로 재고 변경 요청

    OpenAPI Schema: products-stock-with-product-management-code-234899303
    """

    products: list[ProductStockByCodeItem] = Field(default_factory=list, description="상품 재고 목록")


class StockByProductCodeFailure(BaseDto):
    """상품 관리코드 재고 변경 실패 항목"""

    product_management_code: str | None = Field(None, description="재고 변경에 실패한 상품 관리 코드")
    mall_product_no: int | None = Field(None, description="재고 변경에 실패한 상품 번호")
    mall_product_nos: list[int] = Field(default_factory=list, description="재고 변경에 실패한 상품 번호 목록")
    error_code: str | None = Field(None, description="에러 코드")
    message: str | None = Field(None, description="에러 내용")


class PutStockByProductCodeResponse(BaseDto):
    """
    상품 관리코드로 재고 변경 응답 (207)

    OpenAPI Schema: products-stock-with-product-management-code-811127546
    """

    failures: list[StockByProductCodeFailure] = Field(default_factory=list, description="실패 목록")


class ProductStockByNoItem(BaseDto):
    """상품 번호 기준 재고 변경 항목"""

    product_no: int = Field(..., description="재고 변경할 상품 번호")
    stock: int = Field(..., description="수정할 재고")


class PutStockByProductNoRequest(BaseDto):
    """
    상품 번호로 재고 변경 요청

    OpenAPI Schema: products-stock-with-product-no745913430
    """

    products: list[ProductStockByNoItem] = Field(default_factory=list, description="상품 재고 목록")


class StockByProductNoFailure(BaseDto):
    """상품 번호 재고 변경 실패 항목"""

    product_no: int | None = Field(None, description="재고 변경에 실패한 상품 번호")
    error_code: str | None = Field(None, description="에러 코드")
    message: str | None = Field(None, description="에러 내용")


class PutStockByProductNoResponse(BaseDto):
    """
    상품 번호로 재고 변경 응답 (207)

    OpenAPI Schema: products-stock-with-product-no-1878434066
    """

    failures: list[StockByProductNoFailure] = Field(default_factory=list, description="실패 목록")


# ------------------------------------
#  상품 부분(판매상태/전시/품절/옵션) 수정 (partial)
# ------------------------------------
class PartialPrice(BaseDto):
    """부분 수정 가격 정보"""

    sale_price: float | None = Field(None, description="판매가")
    unit_price: float | None = Field(None, description="단위가격")


class PartialSaleStatus(BaseDto):
    """부분 수정 판매상태 정보"""

    display: bool | None = Field(None, description="전시여부 (null인 경우 기존값 유지)")
    soldout: bool | None = Field(None, description="품절처리 (TRUE일 경우만 품절처리)")
    sale_status_type: PartialSaleStatusType | None = Field(None, description="판매상태")


class PartialOption(BaseDto):
    """부분 수정 옵션 정보"""

    mall_option_no: int | None = Field(None, description="옵션번호")
    add_price: float | None = Field(None, description="옵션추가금액")
    stock_cnt: int | None = Field(None, description="재고수량")
    management_cd: str | None = Field(None, description="고객사 관리 옵션번호")
    forced_sold_out: bool | None = Field(None, description="임시 품절 여부")


class PutProductPartialRequest(BaseDto):
    """
    상품 부분(판매상태/전시상태/품절/옵션) 수정 요청

    OpenAPI Schema: products-partial1135875633
    """

    mall_product_no: int = Field(..., description="상품번호")
    price: PartialPrice | None = Field(None, description="가격 정보")
    sale_status: PartialSaleStatus | None = Field(None, description="판매상태 정보")
    options: list[PartialOption] = Field(default_factory=list, description="옵션 목록")


# ------------------------------------
#  상품 상태 변경 (mallProductNo/status)
# ------------------------------------
class PutProductStatusRequest(BaseDto):
    """
    상품 상태 변경 요청

    OpenAPI Schema: products-mallProductNo-status1461747417
    """

    display: bool | None = Field(None, description="전시여부")
    soldout: bool | None = Field(None, description="품절처리 (TRUE일 경우만 품절처리)")
    sale_status_type: PartialSaleStatusType | None = Field(None, description="판매상태")


# ------------------------------------
#  상품 판매합의 승인/거절 (sale-agreements)
# ------------------------------------
class PutSaleAgreementRequest(BaseDto):
    """
    상품 판매합의 승인/거절 요청

    OpenAPI Schema: products-sale-agreements-1087821627
    """

    is_confirm: bool = Field(..., description="합의여부")
    product_nos: list[int] = Field(default_factory=list, description="상품번호 목록")
    reason: str | None = Field(None, description="거절 시 사유 (합의시에는 미입력)")


class SaleAgreementFailure(BaseDto):
    """판매합의 실패 항목"""

    product_no: int = Field(..., description="수정에 실패한 상품 번호")
    message: str | None = Field(None, description="실패 사유")


class PutSaleAgreementResponse(BaseDto):
    """
    상품 판매합의 승인/거절 응답

    OpenAPI Schema: products-sale-agreements171660186
    """

    total_count: int = Field(..., description="총 상품 개수")
    success_product_nos: list[int] = Field(default_factory=list, description="성공한 상품 번호 목록")
    failures: list[SaleAgreementFailure] = Field(default_factory=list, description="실패 목록")


# ------------------------------------
#  상품 심사 승인/거절 (inspections)
# ------------------------------------
class InspectionConfirmRequest(BaseDto):
    """
    상품 심사 승인 요청

    OpenAPI Schema: products-inspections-confirm-389794168
    """

    product_nos: list[int] = Field(default_factory=list, description="상품번호 목록")


class InspectionRejectReason(BaseDto):
    """상품 심사 거절 사유 항목"""

    product_no: int = Field(..., description="상품번호")
    comment: str | None = Field(None, description="거절사유")


class InspectionRejectRequest(BaseDto):
    """
    상품 심사 거절 요청

    OpenAPI Schema: products-inspections-reject-491696779
    """

    reasons: list[InspectionRejectReason] = Field(default_factory=list, description="거절 사유 목록")


class InspectionResultFailure(BaseDto):
    """상품 심사 처리 실패 항목"""

    mall_product_no: int = Field(..., description="수정에 실패한 상품 번호")
    apply_status_type: str | None = Field(None, description="심사승인상태")
    error_code: str | None = Field(None, description="실패 에러코드")
    message: str | None = Field(None, description="실패 사유")


class InspectionResultResponse(BaseDto):
    """
    상품 심사 승인/거절 응답

    OpenAPI Schema: products-inspections-reject-626466228
    """

    total_count: int = Field(..., description="수정 요청한 상품 수")
    success_nos: list[int] = Field(default_factory=list, description="성공한 상품 번호 목록")
    failures: list[InspectionResultFailure] = Field(default_factory=list, description="실패 목록")

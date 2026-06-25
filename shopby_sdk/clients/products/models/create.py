"""상품 등록/수정 요청 모델

OpenAPI Schemas:
- CreateProductRequest          (products-1263807508)            POST /products (마스터, 113필드, version 2.0)
- UpdateProductRequest          (products-1116277168)            PUT  /products (DEPRECATED, 90필드)
- UpdateProductV2Request        (products-productNo2036855991)   PUT  /products/{productNo} (41필드, version 2.0)
- CreateProductTemporaryRequest (products-temporary-1953288861)  POST /products/temporary (78필드)
- CreateCopiedProductRequest    (products-productNo-1790230091)  POST /products/{productNo} (재고연동상품, 80필드)

설계 원칙:
- 마스터 스키마(CreateProductRequest)를 superset으로 두고, 중첩 모델을 재사용합니다.
- 중첩 객체의 하위 필드는 스키마마다 required/optional 차이가 있어 모두 Optional 로 정의하여
  여러 스키마에서 공유합니다(쓰기 모델이므로 안전).
- 재고연동상품(CreateCopiedProductRequest)은 구조가 완전히 다른 별도 스키마라
  자체 중첩 모델(Copied*)을 사용합니다.
- 직렬화는 client 에서 model_dump(by_alias=True, exclude_none=True, mode="json") 로 처리합니다.
"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


# ======================================================================
#  공통 Enum (Literal)
# ======================================================================
ProductGroupType = Literal["DELIVERY", "SERVICE"]
"""상품군 (DELIVERY: 배송상품군, SERVICE: 서비스상품군)"""

ProductClassType = Literal["DEFAULT", "OFFLINE", "RENTAL", "EVENT"]
"""상품분류 (DEFAULT: 일반상품, OFFLINE: 오프라인상품, RENTAL: 렌탈상품)"""

ProductSaleMethodType = Literal["PURCHASE", "CONSIGNMENT"]
"""판매방식 (PURCHASE: 사입, CONSIGNMENT: 위탁)"""

ProductSalePeriodType = Literal["REGULAR", "PERIOD"]
"""판매기간설정 (REGULAR: 상시 판매, PERIOD: 기간지정 판매)"""

ProductOptionType = Literal["COMBINATION", "NONE", "DEFAULT", "REQUIRED"]
"""옵션 유형 (COMBINATION: 조합형, NONE/DEFAULT: 기본생성, REQUIRED: 필수/선택형)"""

ProductValueAddedTaxType = Literal["DUTY", "DUTYFREE", "SMALL"]
"""과세 적용 기준 (DUTY: 과세, DUTYFREE: 면세, SMALL: 영세)"""

ProductShippingAreaType = Literal["PARTNER_SHIPPING_AREA", "MALL_SHIPPING_AREA"]
"""출고유형 (PARTNER_SHIPPING_AREA: 파트너 배송, MALL_SHIPPING_AREA: 쇼핑몰 배송)"""

ProductImmediateDiscountUnitType = Literal["WON", "RATE"]
"""즉시할인 단위 (WON: 원, RATE: %)"""

ProductImageUrlType = Literal["IMAGE_URL", "VIDEO_URL"]
"""이미지 url 타입 (IMAGE_URL: 이미지, VIDEO_URL: 비디오)"""

YnFlag = Literal["Y", "N"]
"""Y/N 플래그"""


# ======================================================================
#  공통 중첩 모델 (마스터/업데이트/임시 스키마에서 재사용)
#  접두사 PC = ProductCreate
# ======================================================================
class PCContentDetail(BaseDto):
    """상품 내용 설정 (contentDetail)"""

    uses_option_image_instead_of_content: bool | None = Field(
        None, description="옵션 이미지로 상품 내용 대체 여부"
    )
    content_header: str | None = Field(None, description="상품 상단 내용 (html)")
    content: str | None = Field(None, description="상품 상세 내용")
    content_footer: str | None = Field(None, description="상품 하단 내용 (html)")


class PCUnitPriceInfo(BaseDto):
    """가격 단위 정보 (price.unitPriceInfo)"""

    unit_name: str | None = Field(None, description="단위 값")
    unit_name_type: str | None = Field(None, description="단위 유형")
    unit_price: float | None = Field(None, description="단위 가격")
    unit_total_quantity: float | None = Field(None, description="단위 총 수량")
    unit_base_quantity: float | None = Field(None, description="단위 기준 수량")


class PCImmediateDiscountInfo(BaseDto):
    """즉시 할인 정보 (price.immediateDiscountInfo)"""

    unit_type: Literal["AMOUNT", "PERCENT"] | None = Field(None, description="즉시 할인 단위")
    amount: float | None = Field(None, description="즉시 할인 값")
    period_yn: YnFlag | None = Field(None, description="즉시 할인 기간 여부")
    start_ymdt: KstDatetime | None = Field(None, description="즉시 할인 시작 일시")
    end_ymdt: KstDatetime | None = Field(None, description="즉시 할인 종료 일시")


class PCAccumulationLimitInfo(BaseDto):
    """적립금 사용 한도율 (accumulationLimitInfo / price.accumulationLimitInfo)"""

    unit_type: Literal["AMOUNT", "PERCENT"] | None = Field(None, description="적립금 사용 금액 단위")
    limit_value: float | None = Field(None, description="적립금 사용 양")


class PCCommissionInfo(BaseDto):
    """수수료 정보 (price.commissionInfo)"""

    type: Literal["PRODUCT", "CATEGORY", "PARTNER", "PURCHASE_PRICE"] | None = Field(
        None, description="판매수수료 타입"
    )
    rate: float | None = Field(None, description="판매수수료")


class PCPriceInfo(BaseDto):
    """가격 관련 설정 (price)"""

    sale_price: float | None = Field(None, description="판매가")
    purchase_price: float | None = Field(None, description="공급가/매입가")
    partner_charge_amt: float | None = Field(None, description="정산시 파트너 분담금")
    commission_info: PCCommissionInfo | None = Field(None, description="수수료 정보")
    immediate_discount_info: PCImmediateDiscountInfo | None = Field(None, description="즉시 할인 정보")
    unit_price_info: PCUnitPriceInfo | None = Field(None, description="가격 단위 정보")
    accumulation_rate: float | None = Field(None, description="적립률(%)")
    accumulation_use_yn: YnFlag | None = Field(None, description="적립금 사용 여부")
    accumulation_limit_info: PCAccumulationLimitInfo | None = Field(None, description="적립금 사용 한도율")
    surtax_type: ProductValueAddedTaxType | None = Field(None, description="과세 적용 기준")


class PCMemberDisplayInfo(BaseDto):
    """회원 등급/그룹 노출 설정 정보 (display.memberGradeDisplayInfo / memberGroupDisplayInfo)"""

    check: Literal["NONE", "ANY", "ALL"] | None = Field(None, description="노출 설정")
    info: list[int] | None = Field(None, description="노출 설정할 회원 등급/그룹 번호 리스트")


class PCPlatformDisplayInfo(BaseDto):
    """플랫폼 별 노출 설정 (display.platformDisplayInfo)"""

    is_all: bool | None = Field(None, description="전체 노출 여부 (false인 경우 anyValues 필수)")
    any_values: list[Literal["PC", "MOBILE_WEB", "MOBILE"]] | None = Field(
        None, description="노출할 플랫폼 리스트"
    )


class PCDisplayInfo(BaseDto):
    """노출 관련 설정 (display)"""

    platform_display_info: PCPlatformDisplayInfo | None = Field(None, description="플랫폼 별 노출 설정")
    search_engine_displayable: bool | None = Field(None, description="검색엔진 노출 여부")
    guest_purchasable: bool | None = Field(None, description="비회원 구매 가능 여부")
    minor_purchasable: bool | None = Field(None, description="미성년자 구매가능 여부")
    only_url_accessible: bool | None = Field(None, description="프론트 미노출 여부")
    member_group_display_info: PCMemberDisplayInfo | None = Field(None, description="회원 그룹 노출 설정 정보")
    member_grade_display_info: PCMemberDisplayInfo | None = Field(None, description="회원 등급 노출 설정 정보")


class PCProductImage(BaseDto):
    """상품 이미지 (image.images[])"""

    image_no: int | None = Field(None, description="이미지 번호 (신규 생성 시 0)")
    url: str | None = Field(None, description="이미지 URL")
    is_main: bool | None = Field(None, description="대표 이미지 여부")
    url_type: ProductImageUrlType | None = Field(None, description="url 타입")


class PCListImage(BaseDto):
    """리스트 이미지 (image.listImage)"""

    image_no: int | None = Field(None, description="리스트 이미지 번호 (신규 생성 시 0)")
    url: str | None = Field(None, description="리스트 이미지 URL")
    url_type: ProductImageUrlType | None = Field(None, description="url 타입")


class PCImageInfo(BaseDto):
    """상품 이미지 관련 설정 (image)"""

    uses_external_image: bool | None = Field(None, description="외부 이미지 URL 사용 여부")
    images: list[PCProductImage] | None = Field(None, description="상품 이미지 리스트")
    list_image: PCListImage | None = Field(None, description="리스트 이미지")


class PCSalePeriod(BaseDto):
    """판매 기간 (salePeriodInfo.salePeriod)"""

    start_ymdt: KstDatetime | None = Field(None, description="판매 시작일시")
    end_ymdt: KstDatetime | None = Field(None, description="판매 종료일시")


class PCSalePeriodInfo(BaseDto):
    """판매 기간 정보 (salePeriodInfo)"""

    sale_period_type: ProductSalePeriodType | None = Field(None, description="판매 기간 유형")
    sale_period: PCSalePeriod | None = Field(None, description="판매 기간")


class PCPlaceOriginInfo(BaseDto):
    """원산지 정보 (placeOriginInfo)"""

    place_origin_seq: int | None = Field(None, description="원산지 번호")
    place_origins_yn: YnFlag | None = Field(None, description="원산지 직접 입력 사용 유무")
    place_origin: str | None = Field(None, description="원산지 직접 입력인 경우, 원산지 입력")


class PCDutyContent(BaseDto):
    """상품정보고시 (dutyContent)"""

    category_no: int | None = Field(None, description="상품 정보 고시 항목 번호")
    category_name: str | None = Field(None, description="상품 정보 고시 항목명")
    contents: list[dict[str, Any]] | None = Field(None, description="상품 정보 고시 상세 내용")


class PCProductGuide(BaseDto):
    """상품 안내 정보 (productGuides[])"""

    template_no: int | None = Field(None, description="상품 안내 정보 - 템플릿 번호")
    type: Literal["DELIVERY", "AFTER_SERVICE", "REFUND", "EXCHANGE", "DELEGATION_BY_LIQUOR"] | None = Field(
        None, description="상품 안내 정보 - 템플릿 유형"
    )
    content: str | None = Field(None, description="상품 안내 정보 - 직접 입력하는 경우에만 입력")


class PCUnavailablePeriod(BaseDto):
    """장바구니 불가 기간 (cartInfo.unavailablePeriod)"""

    start_ymdt: KstDatetime | None = Field(None, description="장바구니 불가 시작일시")
    end_ymdt: KstDatetime | None = Field(None, description="장바구니 불가 종료일시")


class PCCartInfo(BaseDto):
    """장바구니 설정 (cartInfo)"""

    is_available_cart: bool | None = Field(None, description="장바구니 가능 여부")
    unavailable_period: PCUnavailablePeriod | None = Field(None, description="장바구니 불가 기간")


class PCRefundableInfo(BaseDto):
    """환불 정보 (refundableInfo)"""

    refundable: bool | None = Field(None, description="환불 가능 여부")
    refundable_yn: YnFlag | None = Field(None, description="환불가능 여부")
    non_refund_types: list[Literal["RETURN", "EXCHANGE"]] | None = Field(
        None, description="환불 불가인 경우, 불가능 항목"
    )
    non_refundable_info: list[Literal["CANCEL", "RETURN", "EXCHANGE"]] | None = Field(
        None, description="환불 불가능 항목"
    )


class PCBrandNoInfo(BaseDto):
    """브랜드 번호 정보 (brand.brandNoInfo)"""

    brand_no: int | None = Field(None, description="브랜드 번호")
    display_brand_no: int | None = Field(None, description="전시 브랜드 번호")


class PCBrandNameInfo(BaseDto):
    """브랜드명 정보 (brand.brandNameInfo)"""

    main_name: str | None = Field(None, description="메인 브랜드명")
    sub_name: str | None = Field(None, description="서브 브랜드명")


class PCBrandInfo(BaseDto):
    """브랜드 정보 (brand)"""

    input_type: Literal["NO", "NAME"] | None = Field(None, description="브랜드 입력 유형")
    brand_no_info: PCBrandNoInfo | None = Field(None, description="브랜드 번호 정보")
    brand_name_info: PCBrandNameInfo | None = Field(None, description="브랜드명 정보")


class PCOptionImage(BaseDto):
    """옵션 이미지 (option.options[].images[])"""

    url: str | None = Field(None, description="옵션 이미지 URL")
    is_main: bool | None = Field(None, description="옵션 대표 이미지 여부")


class PCOption(BaseDto):
    """옵션 정보 (option.options[])"""

    option_no: int | None = Field(None, description="옵션 번호 (신규 생성 0)")
    option_name: str | None = Field(None, description="옵션명")
    option_value: str | None = Field(None, description="옵션값")
    add_price: float | None = Field(None, description="옵션 추가 금액")
    usable: bool | None = Field(None, description="옵션 사용 여부")
    stock_quantity: int | None = Field(None, description="옵션 재고 수량")
    management_code: str | None = Field(None, description="옵션 판매자 관리 코드")
    extra_management_code: str | None = Field(None, description="옵션 추가 관리 코드")
    forced_sold_out: bool | None = Field(None, description="옵션 임시 품절 여부")
    purchase_price: float | None = Field(None, description="매입가/공급가")
    images: list[PCOptionImage] | None = Field(None, description="옵션 이미지")
    is_required_option: bool | None = Field(None, description="필수 옵션 여부")


class PCCustomerDemand(BaseDto):
    """구매자 작성형 옵션 (option.customerDemands[])"""

    customer_demand_no: int | None = Field(None, description="작성형 옵션 번호 (신규 생성 0)")
    content: str | None = Field(None, description="작성형 옵션 텍스트 내용")
    target_type: Literal["OPTION", "PRODUCT", "AMOUNT"] | None = Field(None, description="작성형 옵션 매칭 유형")
    required: bool | None = Field(None, description="작성형 옵션 입력 필수 여부")
    usable: bool | None = Field(None, description="작성형 옵션 사용 여부")


class PCOptionInfo(BaseDto):
    """옵션 설정 (option)"""

    options: list[PCOption] | None = Field(None, description="옵션 목록")
    option_select_type: Literal["MULTI", "FLAT"] | None = Field(None, description="옵션 노출 유형")
    customer_demands: list[PCCustomerDemand] | None = Field(None, description="구매자 작성형 옵션")


class PCDeliveryInfo(BaseDto):
    """배송 관련 설정 (delivery)"""

    uses_delivery: bool | None = Field(None, description="배송 여부")
    shipping_area_type: ProductShippingAreaType | None = Field(None, description="출고유형")
    shipping_area_partner_no: int | None = Field(None, description="출고지 파트너 번호")
    delivery_template_no: int | None = Field(None, description="배송비 템플릿 번호")
    can_delivery_combination: bool | None = Field(None, description="묶음 배송 가능 여부")
    can_delivery_international: bool | None = Field(None, description="해외 배송 가능 여부")
    delivery_customer_info: str | None = Field(None, description="배송관련 판매자 특이사항/고객안내사항")


class PCMarketingDisplayPeriod(BaseDto):
    """홍보 문구 노출 기간 (marketing.marketingPhraseInfo.marketingDisplayPeriod)"""

    start_ymdt: KstDatetime | None = Field(None, description="홍보 문구 노출 시작일시")
    end_ymdt: KstDatetime | None = Field(None, description="홍보 문구 노출 종료일시")


class PCMarketingPhraseInfo(BaseDto):
    """홍보 문구 정보 (marketing.marketingPhraseInfo)"""

    marketing_phrase: str | None = Field(None, description="홍보 문구")
    marketing_display_period: PCMarketingDisplayPeriod | None = Field(None, description="홍보 문구 노출 기간")


class PCMarketingInfo(BaseDto):
    """마케팅 관련 설정 (marketing)"""

    marketing_phrase_info: PCMarketingPhraseInfo | None = Field(None, description="홍보 문구 정보")
    is_available_promotion: bool | None = Field(None, description="프로모션 사용 여부")


class PCCustomProperty(BaseDto):
    """추가 항목 (customProperties[])"""

    property: str | None = Field(None, description="추가 항목 - 항목명")
    values: list[str] | None = Field(None, description="추가 항목 - 항목값명")


class PCStickerDisplayPeriod(BaseDto):
    """스티커 노출 기간 (stickers[].displayPeriod)"""

    start_ymdt: KstDatetime | None = Field(None, description="스티커 노출 시작일시")
    end_ymdt: KstDatetime | None = Field(None, description="스티커 노출 종료일시")


class PCSticker(BaseDto):
    """스티커 정보 (stickers[])"""

    sticker_no: int | None = Field(None, description="스티커 번호")
    display_period: PCStickerDisplayPeriod | None = Field(None, description="스티커 노출 기간")
    display_start_date_time: KstDatetime | None = Field(None, description="스티커 노출 시작일")
    display_end_date_time: KstDatetime | None = Field(None, description="스티커 노출 종료일")


class PCExtraJson(BaseDto):
    """추가설정 (extraJson / extraJsonMap)"""

    naver_display_yn: YnFlag | None = Field(None, description="네이버 쇼핑 EP - 노출 여부")
    serial_number: str | None = Field(None, description="제품 일련번호")
    naver_pay_limit_yn: YnFlag | None = Field(None, description="네이버 페이 결제 제한 여부")
    kakao_pay_limit_yn: YnFlag | None = Field(None, description="카카오 페이 결제 제한 여부")
    manufacture_name: str | None = Field(None, description="제조사명 (렌탈상품의 경우 필수)")
    product_model_name: str | None = Field(None, description="제품모델명 (렌탈상품의 경우 필수)")


class PCRelatedProduct(BaseDto):
    """관련 상품 (relatedProductInfo.products[])"""

    product_no: int | None = Field(None, description="관련 상품 번호")
    display_order: int | None = Field(None, description="노출 순서")


class PCRelatedProductInfo(BaseDto):
    """관련 상품 정보 (relatedProductInfo)"""

    config_type: Literal["DISPLAY_CATEGORY", "SELECTED"] | None = Field(None, description="관련 상품 설정")
    sort_criterion: Literal["LATEST_REGISTER_DATE", "SALES_COUNT", "REVIEW_COUNT", "CUSTOM_ORDER"] | None = Field(
        None, description="관련 상품 진열 순서"
    )
    product_nos: list[int] | None = Field(None, description="상품 번호 리스트 (configType=SELECTED)")
    products: list[PCRelatedProduct] | None = Field(None, description="관련 상품 목록")


class PCMaxBuyQuantityInfo(BaseDto):
    """최대구매수량 정보 (purchaseLimitQuantity.maxBuyQuantityInfo)"""

    type: Literal["PER_TIME", "PER_PERIOD", "PER_PERSON", "PER_DAY"] | None = Field(
        None, description="최대구매수량 유형"
    )
    max_buy_quantity: int | None = Field(None, description="최대구매수량")
    max_buy_days: int | None = Field(None, description="PER_PERIOD인 경우 최대 구매 기간")


class PCPurchaseLimitQuantity(BaseDto):
    """구매 수량 제한 설정 (purchaseLimitQuantity)"""

    min_buy_quantity: int | None = Field(None, description="최소구매수량")
    max_buy_quantity_info: PCMaxBuyQuantityInfo | None = Field(None, description="최대구매수량 정보")


class PCProductListImageInfo(BaseDto):
    """리스트 이미지 정보 (productListImageInfo)"""

    image_url_type: ProductImageUrlType | None = Field(None, description="이미지 url 타입")
    url: str | None = Field(None, description="리스트 이미지 URL")


# --- 레거시(flat) 스키마용 중첩 모델 ---
class PCOptionDataInput(BaseDto):
    """구매자작성형 (optionData.inputs[])"""

    input_matching_type: Literal["OPTION", "PRODUCT", "AMOUNT"] | None = Field(None, description="구매자작성형 매칭타입")
    input_text: str | None = Field(None, description="구매자작성형 텍스트 내용")
    use_yn: YnFlag | None = Field(None, description="사용여부")
    required: bool | None = Field(None, description="필수 여부")


class PCOptionDataOptionImage(BaseDto):
    """옵션 이미지 (optionData.options[].optionImages[])"""

    main_yn: YnFlag | None = Field(None, description="대표이미지 여부")
    image_url: str | None = Field(None, description="이미지 주소")
    order: int | None = Field(None, description="전시순서")


class PCOptionDataOption(BaseDto):
    """옵션 (optionData.options[])"""

    option_name: str | None = Field(None, description="옵션명 (조합형일 경우 |로 구분)")
    option_value: str | None = Field(None, description="옵션값 (조합형일 경우 |로 구분)")
    option_type: Literal["COMBINATION", "DEFAULT", "REQUIRED"] | None = Field(None, description="옵션 타입")
    option_select_type: Literal["MULTI", "FLAT"] | None = Field(None, description="옵션 선택 방식")
    add_price: float | None = Field(None, description="옵션 추가 가격")
    purchase_price: float | None = Field(None, description="매입가/공급가")
    stock_cnt: int | None = Field(None, description="재고 수량")
    use_yn: YnFlag | None = Field(None, description="사용여부")
    option_management_cd: str | None = Field(None, description="옵션 판매자 관리코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")
    forced_sold_out: bool | None = Field(None, description="임시 품절 여부")
    is_required_option: bool | None = Field(None, description="필수 옵션 여부")
    order: int | None = Field(None, description="옵션 순서")
    option_images: list[PCOptionDataOptionImage] | None = Field(None, description="옵션 이미지")


class PCOptionData(BaseDto):
    """옵션 데이터 (optionData) - 레거시 스키마용"""

    inputs: list[PCOptionDataInput] | None = Field(None, description="구매자작성형 목록")
    options: list[PCOptionDataOption] | None = Field(None, description="옵션 목록")


class PCProductImageItem(BaseDto):
    """상품 이미지 (productImages[]) - 레거시 스키마용"""

    image_url: str | None = Field(None, description="이미지 URL")
    image_url_type: ProductImageUrlType | None = Field(None, description="이미지 url 타입")
    main_yn: YnFlag | None = Field(None, description="대표이미지 여부")
    is_external: bool | None = Field(None, description="외부 이미지 사용 여부")
    order: int | None = Field(None, description="전시순서")


class PCCustomPropertyValue(BaseDto):
    """추가항목 값 (customProperty[].propValues[])"""

    prop_value: str | None = Field(None, description="항목 값명")


class PCCustomPropertyItem(BaseDto):
    """상품항목추가정보 (customProperty[])"""

    prop_name: str | None = Field(None, description="항목명")
    prop_values: list[PCCustomPropertyValue] | None = Field(None, description="항목 값 목록")


class PCDisplayPeriodSticker(BaseDto):
    """스티커 (stickers[]) - 레거시 스키마용"""

    sticker_no: int | None = Field(None, description="스티커 번호")
    display_period: PCStickerDisplayPeriod | None = Field(None, description="스티커 노출 기간")
    display_start_date_time: KstDatetime | None = Field(None, description="스티커 노출 시작일")
    display_end_date_time: KstDatetime | None = Field(None, description="스티커 노출 종료일")


# ======================================================================
#  CreateProductRequest (마스터, products-1263807508, 113필드)
#  POST /products (version 2.0)
# ======================================================================
class CreateProductRequest(BaseDto):
    """상품(옵션포함) 등록하기 (version 2.0) 요청 모델 - 마스터(superset)

    OpenAPI Schema: products-1263807508

    레거시(flat) 필드와 v2 스타일 중첩 필드를 모두 포함합니다. 실제 요청 시
    필요한 필드만 채우면 되며, exclude_none 으로 직렬화됩니다.
    """

    # --- 기본 정보 ---
    product_name: str = Field(..., description="상품명")
    product_name_en: str | None = Field(None, description="영문상품명")
    supplier_product_name: str | None = Field(None, description="매입처 상품명")
    group_type: ProductGroupType | None = Field(None, description="상품군 (default: DELIVERY)")
    class_type: ProductClassType | None = Field(None, description="상품분류")
    sale_method_type: ProductSaleMethodType | None = Field(None, description="판매방식 (default: CONSIGNMENT)")
    merchandiser_no: int | None = Field(None, description="상품 담당자")
    management_code: str | None = Field(None, description="판매자 관리 코드")
    extra_management_code: str | None = Field(None, description="추가관리코드")
    product_management_cd: str | None = Field(None, description="판매자 관리코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")

    # --- 카테고리 ---
    category_no: int = Field(..., description="표준카테고리")
    standard_category_no: int | None = Field(None, description="표준 카테고리")
    display_category_no: list[int] = Field(default_factory=list, description="전시카테고리")
    display_category_nos: list[int] | None = Field(None, description="전시 카테고리 리스트")
    representative_display_category_no: int = Field(..., description="대표 전시카테고리")

    # --- 상품 내용 ---
    content_detail: PCContentDetail = Field(..., description="상품 내용 설정")
    content: str | None = Field(None, description="상품상세 본문(HTML)")
    content_header: str | None = Field(None, description="상품상세 헤더(HTML)")
    content_footer: str | None = Field(None, description="상품상세 푸터(HTML)")

    # --- 가격 (v2 nested) ---
    price: PCPriceInfo = Field(..., description="가격 관련 설정")
    sale_price: float = Field(..., description="판매가")
    purchase_price: float | None = Field(None, description="매입가/공급가")
    partner_charge_amt: float | None = Field(None, description="정산시 파트너 분담금")
    accumulation_rate: float | None = Field(None, description="적립률(%)")
    accumulation_use_yn: YnFlag | None = Field(None, description="적립금 사용여부")
    accumulation_limit_info: PCAccumulationLimitInfo = Field(..., description="적립금 사용 한도율")
    value_added_tax_type: ProductValueAddedTaxType | None = Field(None, description="과세 적용 기준")
    commission_rate: float | None = Field(None, description="판매수수료 비율")
    commission_rate_type: Literal["PRODUCT", "CATEGORY", "PARTNER", "PURCHASE_PRICE"] | None = Field(
        None, description="판매수수료타입"
    )

    # --- 즉시할인 (flat) ---
    immediate_discount_unit_type: ProductImmediateDiscountUnitType = Field(..., description="즉시할인 단위")
    immediate_discount_value: float | None = Field(None, description="즉시할인 값")
    immediate_discount_period_yn: YnFlag | None = Field(None, description="즉시할인 기간 설정 여부")
    immediate_discount_start_ymdt: KstDatetime | None = Field(None, description="즉시할인 시작일자")
    immediate_discount_end_ymdt: KstDatetime | None = Field(None, description="즉시할인 종료일자")

    # --- 단위 가격 (flat) ---
    unit_price: float | None = Field(None, description="단위 가격")
    unit_name: str | None = Field(None, description="단위 값")
    unit_name_type: str | None = Field(None, description="단위 유형")

    # --- 재고/구매제한 ---
    stock_quantity: int = Field(..., description="재고 수량 (옵션 사용 시, 옵션 재고 사용)")
    product_stock_cnt: int | None = Field(None, description="상품 재고 수량 (단독형)")
    is_option_used: bool | None = Field(None, description="옵션 사용 유무")
    option_type: ProductOptionType = Field(..., description="옵션 유형")
    option: PCOptionInfo | None = Field(None, description="옵션 정보 (v2 nested)")
    option_data: PCOptionData | None = Field(None, description="옵션 데이터 (레거시)")
    purchase_limit_quantity: PCPurchaseLimitQuantity | None = Field(None, description="구매 수량 제한 설정")
    min_buy_cnt: int | None = Field(None, description="최소구매수량")
    max_buy_time_cnt: int | None = Field(None, description="1회최대구매수량")
    max_buy_person_cnt: int | None = Field(None, description="1인최대구매수량")
    max_buy_period_cnt: int | None = Field(None, description="최대구매기간(수량)")
    max_buy_days: int | None = Field(None, description="최대구매기간(일)")

    # --- 노출 (v2 nested + flat) ---
    display: PCDisplayInfo = Field(..., description="노출 관련 설정")
    minor_purchase_yn: YnFlag = Field(..., description="미성년자 구매가능 여부")
    nonmember_purchase_yn: YnFlag = Field(..., description="비회원 구매가능 여부")
    platform_display_yn: YnFlag | None = Field(None, description="플랫폼 노출 설정 여부")
    platform_display_pc_yn: YnFlag | None = Field(None, description="플랫폼 - PC 노출 여부")
    platform_display_mobile_web_yn: YnFlag | None = Field(None, description="플랫폼 - 모바일 웹 노출 여부")
    platform_display_mobile_yn: YnFlag | None = Field(None, description="플랫폼 - 모바일 앱 노출 여부")
    url_shortening_yn: YnFlag | None = Field(None, description="단축URL 사용여부")

    # --- 이미지 (v2 nested + flat) ---
    image: PCImageInfo = Field(..., description="상품 이미지 관련 설정")
    product_images: list[PCProductImageItem] | None = Field(None, description="상품 이미지 목록 (레거시)")
    product_list_image: str | None = Field(None, description="리스트 이미지 URL")
    product_list_image_info: PCProductListImageInfo | None = Field(None, description="리스트 이미지 정보")
    use_origin_product_image_url: bool | None = Field(None, description="원본 이미지 url 그대로 사용 여부")
    add_option_image_yn: YnFlag | None = Field(None, description="등록된 옵션이미지 사용")

    # --- 판매 기간 (v2 nested + flat) ---
    sale_period_info: PCSalePeriodInfo = Field(..., description="판매 기간 정보")
    sale_period_type: ProductSalePeriodType = Field(..., description="판매기간설정")
    sale_start_ymdt: KstDatetime = Field(..., description="판매시작일")
    sale_end_ymdt: KstDatetime = Field(..., description="판매종료일")

    # --- 제조/유효기간 ---
    manufactured_date_time: KstDatetime | None = Field(None, description="제조일자")
    expiration_date_time: KstDatetime | None = Field(None, description="유효기간(유통기한)")
    manufacture_ymdt: KstDatetime | None = Field(None, description="제조일자 (flat)")
    expiration_ymdt: KstDatetime | None = Field(None, description="유효기간 (flat)")
    manufacturer: str | None = Field(None, description="제조사명")

    # --- 원산지 ---
    place_origin_info: PCPlaceOriginInfo = Field(..., description="원산지 정보")
    place_origin: str | None = Field(None, description="원산지 직접입력 값")

    # --- 상품정보고시 ---
    duty_content: PCDutyContent | None = Field(None, description="상품정보고시 (v2 nested)")
    duty_info: str | None = Field(None, description="상품정보고시 (json 문자열, 레거시)")

    # --- 상품 안내 ---
    product_guides: list[PCProductGuide] = Field(default_factory=list, description="상품 안내 정보")

    # --- 재입고 알림 ---
    uses_restock_notification: bool = Field(..., description="재입고 알림 사용설정")
    use_restock_noti_yn: YnFlag | None = Field(None, description="재입고 알림 사용설정 (flat)")

    # --- 장바구니 (v2 nested + flat) ---
    cart_info: PCCartInfo | None = Field(None, description="장바구니 설정")
    cart_use_yn: YnFlag | None = Field(None, description="장바구니 사용 여부")
    cart_off_period_yn: YnFlag | None = Field(None, description="장바구니 불가 기간 설정")
    cart_off_start_ymdt: KstDatetime | None = Field(None, description="장바구니 불가 시작일자")
    cart_off_end_ymdt: KstDatetime | None = Field(None, description="장바구니 불가 종료일자")

    # --- 환불 (v2 nested + flat) ---
    refundable_info: PCRefundableInfo = Field(..., description="환불가능 세부정보")
    refundable_yn: YnFlag | None = Field(None, description="환불가능여부")

    # --- 브랜드 (v2 nested + flat) ---
    brand: PCBrandInfo | None = Field(None, description="브랜드 정보 (v2 nested)")
    brand_no: int | None = Field(None, description="브랜드 번호")
    brand_name: str | None = Field(None, description="브랜드 이름")

    # --- 배송 (v2 nested + flat) ---
    delivery: PCDeliveryInfo = Field(..., description="배송 관련 설정")
    delivery_yn: YnFlag | None = Field(None, description="배송 여부")
    delivery_template_no: int = Field(..., description="배송비 템플릿 번호")
    delivery_combination_yn: YnFlag = Field(..., description="묶음배송 가능 여부")
    delivery_international_yn: YnFlag = Field(..., description="해외배송 여부")
    shipping_area_type: ProductShippingAreaType = Field(..., description="출고유형")
    delivery_customer_info: str | None = Field(None, description="배송관련 판매자 특이사항/고객안내사항")

    # --- 마케팅/프로모션 (v2 nested + flat) ---
    marketing: PCMarketingInfo = Field(..., description="마케팅 관련 설정")
    promotion_yn: YnFlag | None = Field(None, description="프로모션 적용 가능여부")
    promotion_text: str | None = Field(None, description="홍보문구")
    promotion_text_yn: YnFlag | None = Field(None, description="프로모션 기간 사용 여부")
    promotion_text_start_ymdt: KstDatetime | None = Field(None, description="프로모션 홍보문구 노출 시작일")
    promotion_text_end_ymdt: KstDatetime | None = Field(None, description="프로모션 홍보문구 노출 종료")

    # --- 검색어 ---
    keywords: list[str] = Field(default_factory=list, description="검색어 리스트")
    keyword: str | None = Field(None, description="검색어 (,로 구분)")
    hs_code: str | None = Field(None, description="hs code")

    # --- 추가 항목/스티커/추가설정 ---
    custom_properties: list[PCCustomProperty] | None = Field(None, description="추가 항목 (v2 nested)")
    custom_property: list[PCCustomPropertyItem] | None = Field(None, description="상품항목추가정보 (레거시)")
    stickers: list[PCSticker] | None = Field(None, description="스티커 정보")
    extra_json: PCExtraJson | None = Field(None, description="추가설정 (v2 nested)")
    extra_json_map: PCExtraJson | None = Field(None, description="추가설정 (레거시)")
    related_product_info: PCRelatedProductInfo | None = Field(None, description="관련 상품 정보")
    extra_info: str | None = Field(None, description="추가 정보")


# ======================================================================
#  UpdateProductRequest (products-1116277168, 90필드, DEPRECATED)
#  PUT /products
# ======================================================================
class UpdateProductRequest(BaseDto):
    """상품(옵션포함) 수정하기 (DEPRECATED) 요청 모델

    OpenAPI Schema: products-1116277168

    flat(레거시) 스키마입니다. version 2.0(UpdateProductV2Request) 사용을 권장합니다.
    """

    mall_product_no: int = Field(..., description="상품번호")
    product_name: str = Field(..., description="상품명")
    product_name_en: str | None = Field(None, description="영문상품명")
    supplier_product_name: str | None = Field(None, description="매입처 상품명")
    group_type: ProductGroupType = Field(..., description="상품군")
    class_type: ProductClassType = Field(..., description="상품분류")
    sale_method_type: ProductSaleMethodType | None = Field(None, description="판매방식")
    merchandiser_no: int | None = Field(None, description="상품 담당자")
    category_no: int = Field(..., description="표준카테고리")
    display_category_no: list[int] = Field(default_factory=list, description="전시카테고리")
    representative_display_category_no: int = Field(..., description="대표 전시카테고리")
    product_management_cd: str | None = Field(None, description="판매자 관리코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")

    # 상품 내용
    content: str | None = Field(None, description="상품상세 본문(HTML)")
    content_header: str | None = Field(None, description="상품상세 헤더(HTML)")
    content_footer: str | None = Field(None, description="상품상세 푸터(HTML)")
    add_option_image_yn: YnFlag = Field(..., description="등록된 옵션이미지 사용")

    # 가격
    sale_price: float = Field(..., description="판매가")
    purchase_price: float | None = Field(None, description="매입가/공급가")
    partner_charge_amt: float = Field(..., description="정산시 파트너 분담금")
    accumulation_rate: float = Field(..., description="적립률(%)")
    accumulation_use_yn: YnFlag = Field(..., description="적립금 사용여부")
    accumulation_limit_info: PCAccumulationLimitInfo = Field(..., description="적립금 사용 한도율")
    value_added_tax_type: ProductValueAddedTaxType | None = Field(None, description="과세 적용 기준")
    commission_rate: float | None = Field(None, description="판매수수료 비율")
    commission_rate_type: str | None = Field(None, description="판매수수료타입")

    # 즉시할인
    immediate_discount_unit_type: ProductImmediateDiscountUnitType = Field(..., description="즉시할인 단위")
    immediate_discount_value: float = Field(..., description="즉시할인 값")
    immediate_discount_period_yn: YnFlag = Field(..., description="즉시할인 기간 설정 여부")
    immediate_discount_start_ymdt: KstDatetime | None = Field(None, description="즉시할인 시작일자")
    immediate_discount_end_ymdt: KstDatetime | None = Field(None, description="즉시할인 종료일자")

    # 단위 가격
    unit_price: float | None = Field(None, description="단위 가격")
    unit_name: str | None = Field(None, description="단위 값")
    unit_name_type: str | None = Field(None, description="단위 유형")

    # 재고/옵션
    is_option_used: bool = Field(..., description="옵션 사용 유무")
    product_stock_cnt: int = Field(..., description="상품 재고 수량")
    option_data: PCOptionData | None = Field(None, description="옵션 데이터")

    # 구매 제한
    min_buy_cnt: int = Field(..., description="최소구매수량")
    max_buy_time_cnt: int = Field(..., description="1회최대구매수량")
    max_buy_person_cnt: int = Field(..., description="1인최대구매수량")
    max_buy_period_cnt: int = Field(..., description="최대구매기간(수량)")
    max_buy_days: int = Field(..., description="최대구매기간(일)")

    # 노출
    minor_purchase_yn: YnFlag = Field(..., description="미성년자 구매가능 여부")
    nonmember_purchase_yn: YnFlag = Field(..., description="비회원 구매가능 여부")
    platform_display_yn: YnFlag = Field(..., description="플랫폼 노출 설정 여부")
    platform_display_pc_yn: YnFlag = Field(..., description="플랫폼 - PC 노출 여부")
    platform_display_mobile_web_yn: YnFlag = Field(..., description="플랫폼 - 모바일 웹 노출 여부")
    platform_display_mobile_yn: YnFlag = Field(..., description="플랫폼 - 모바일 앱 노출 여부")
    url_shortening_yn: YnFlag | None = Field(None, description="단축URL 사용여부")
    url_direct_display_yn: YnFlag | None = Field(None, description="프론트 미노출 여부")

    # 이미지
    product_images: list[PCProductImageItem] | None = Field(None, description="상품 이미지 목록")
    product_list_image: str | None = Field(None, description="리스트 이미지 URL")
    product_list_image_info: PCProductListImageInfo | None = Field(None, description="리스트 이미지 정보")

    # 판매 기간
    sale_period_type: ProductSalePeriodType = Field(..., description="판매기간설정")
    sale_start_ymdt: KstDatetime = Field(..., description="판매시작일")
    sale_end_ymdt: KstDatetime = Field(..., description="판매종료일")

    # 제조/유효기간
    manufacture_ymdt: KstDatetime | None = Field(None, description="제조일자")
    expiration_ymdt: KstDatetime | None = Field(None, description="유효기간")
    manufacturer: str | None = Field(None, description="제조사명")

    # 원산지/정보고시
    place_origin_info: PCPlaceOriginInfo = Field(..., description="원산지 정보")
    duty_info: str | None = Field(None, description="상품정보고시 (json 문자열)")
    product_guides: list[PCProductGuide] | None = Field(None, description="상품 안내 정보")
    use_restock_noti_yn: YnFlag | None = Field(None, description="재입고 알림 사용설정")

    # 장바구니
    cart_use_yn: YnFlag = Field(..., description="장바구니 사용 여부")
    cart_off_period_yn: YnFlag = Field(..., description="장바구니 불가 기간 설정")
    cart_off_start_ymdt: KstDatetime | None = Field(None, description="장바구니 불가 시작일자")
    cart_off_end_ymdt: KstDatetime | None = Field(None, description="장바구니 불가 종료일자")

    # 환불
    refundable_info: PCRefundableInfo = Field(..., description="환불가능 세부정보")
    refundable_yn: YnFlag = Field(..., description="환불가능여부")

    # 브랜드
    brand_no: int = Field(..., description="브랜드 번호")
    brand_name: str = Field(..., description="브랜드 이름")

    # 배송
    delivery_yn: YnFlag = Field(..., description="배송 여부")
    delivery_template_no: int = Field(..., description="배송비 템플릿 번호")
    delivery_combination_yn: YnFlag = Field(..., description="묶음배송 가능 여부")
    delivery_international_yn: YnFlag = Field(..., description="해외배송 여부")
    shipping_area_type: ProductShippingAreaType | None = Field(None, description="출고유형")
    shipping_area_partner_no: int | None = Field(None, description="출고지 파트너 번호")
    delivery_customer_info: str | None = Field(None, description="배송관련 판매자 특이사항/고객안내사항")

    # 마케팅/프로모션
    promotion_yn: YnFlag = Field(..., description="프로모션 적용 가능여부")
    promotion_text: str | None = Field(None, description="홍보문구")
    promotion_text_yn: YnFlag = Field(..., description="프로모션 기간 사용 여부")
    promotion_text_start_ymdt: KstDatetime | None = Field(None, description="프로모션 홍보문구 노출 시작일")
    promotion_text_end_ymdt: KstDatetime | None = Field(None, description="프로모션 홍보문구 노출 종료")

    # 검색어/추가
    keyword: str | None = Field(None, description="검색어 (,로 구분)")
    hs_code: str | None = Field(None, description="hs code")
    custom_property: list[PCCustomPropertyItem] | None = Field(None, description="상품항목추가정보")
    stickers: list[PCDisplayPeriodSticker] | None = Field(None, description="스티커 정보")
    extra_json_map: PCExtraJson = Field(..., description="추가설정")
    related_product_info: PCRelatedProductInfo | None = Field(None, description="관련 상품 정보")
    extra_info: str | None = Field(None, description="추가 정보")


# ======================================================================
#  UpdateProductV2Request (products-productNo2036855991, 41필드)
#  PUT /products/{productNo} (version 2.0)
# ======================================================================
class UpdateProductV2Request(BaseDto):
    """상품(옵션포함) 수정하기 (version 2.0) 요청 모델

    OpenAPI Schema: products-productNo2036855991

    v2 스타일 중첩 스키마입니다(마스터의 부분집합).
    """

    product_name: str = Field(..., description="상품명")
    product_name_en: str | None = Field(None, description="영문 상품명")
    supplier_product_name: str | None = Field(None, description="매입처 상품명")
    group_type: ProductGroupType | None = Field(None, description="상품군")
    class_type: ProductClassType | None = Field(None, description="상품분류")
    sale_method_type: ProductSaleMethodType | None = Field(None, description="판매방식")
    merchandiser_no: int = Field(..., description="상품 담당자")
    standard_category_no: int | None = Field(None, description="표준 카테고리")
    representative_display_category_no: int | None = Field(None, description="대표 전시 카테고리")
    display_category_nos: list[int] | None = Field(None, description="전시 카테고리 리스트")
    management_code: str | None = Field(None, description="판매자 관리 코드")
    extra_management_code: str | None = Field(None, description="추가관리코드")
    manufacturer: str | None = Field(None, description="제조사명")

    content_detail: PCContentDetail = Field(..., description="상품 내용 설정")
    price: PCPriceInfo = Field(..., description="가격 관련 설정")
    stock_quantity: int = Field(..., description="재고 수량")
    option_type: ProductOptionType = Field(..., description="옵션 유형")
    option: PCOptionInfo | None = Field(None, description="옵션 정보")
    purchase_limit_quantity: PCPurchaseLimitQuantity | None = Field(None, description="구매 수량 제한 설정")

    display: PCDisplayInfo = Field(..., description="노출 관련 설정")
    image: PCImageInfo = Field(..., description="상품 이미지 관련 설정")
    sale_period_info: PCSalePeriodInfo = Field(..., description="판매 기간 정보")

    manufactured_date_time: KstDatetime | None = Field(None, description="제조일자")
    expiration_date_time: KstDatetime | None = Field(None, description="유효기간(유통기한)")
    place_origin_info: PCPlaceOriginInfo = Field(..., description="원산지 정보")
    duty_content: PCDutyContent | None = Field(None, description="상품정보고시")
    product_guides: list[PCProductGuide] = Field(default_factory=list, description="상품 안내 정보")
    uses_restock_notification: bool = Field(..., description="재입고 알림 사용설정")

    cart_info: PCCartInfo | None = Field(None, description="장바구니 설정")
    refundable_info: PCRefundableInfo = Field(..., description="환불 정보")
    brand: PCBrandInfo | None = Field(None, description="브랜드 정보")
    delivery: PCDeliveryInfo = Field(..., description="배송 관련 설정")
    marketing: PCMarketingInfo = Field(..., description="마케팅 관련 설정")

    keywords: list[str] = Field(default_factory=list, description="검색어 리스트")
    hs_code: str | None = Field(None, description="HS CODE")
    custom_properties: list[PCCustomProperty] | None = Field(None, description="추가 항목")
    stickers: list[PCSticker] | None = Field(None, description="스티커 정보")
    extra_json: PCExtraJson | None = Field(None, description="추가설정")
    related_product_info: PCRelatedProductInfo | None = Field(None, description="관련 상품 정보")
    extra_info: str | None = Field(None, description="추가 정보")
    url_shortening_yn: YnFlag | None = Field(None, description="단축URL 사용여부")


# ======================================================================
#  CreateProductTemporaryRequest (products-temporary-1953288861, 78필드)
#  POST /products/temporary
# ======================================================================
class CreateProductTemporaryRequest(BaseDto):
    """상품 임시 등록하기 요청 모델

    OpenAPI Schema: products-temporary-1953288861

    flat(레거시) 스키마입니다(마스터의 부분집합).
    """

    product_name: str = Field(..., description="상품명")
    product_name_en: str | None = Field(None, description="영문상품명")
    supplier_product_name: str | None = Field(None, description="매입처 상품명")
    group_type: ProductGroupType | None = Field(None, description="상품군")
    class_type: ProductClassType | None = Field(None, description="상품분류")
    category_no: int | None = Field(None, description="표준카테고리")
    display_category_no: list[int] | None = Field(None, description="전시카테고리")
    representative_display_category_no: int | None = Field(None, description="대표 전시카테고리")
    product_management_cd: str | None = Field(None, description="판매자 관리코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")

    # 상품 내용
    content: str | None = Field(None, description="상품상세 본문(HTML)")
    content_header: str | None = Field(None, description="상품상세 헤더(HTML)")
    content_footer: str | None = Field(None, description="상품상세 푸터(HTML)")
    add_option_image_yn: YnFlag = Field(..., description="등록된 옵션이미지 사용")

    # 가격
    sale_price: float | None = Field(None, description="판매가")
    partner_charge_amt: float | None = Field(None, description="정산시 파트너 분담금")
    accumulation_rate: float | None = Field(None, description="적립률(%)")
    accumulation_use_yn: YnFlag | None = Field(None, description="적립금 사용여부")
    accumulation_limit_info: PCAccumulationLimitInfo = Field(..., description="적립금 사용 한도율")
    value_added_tax_type: ProductValueAddedTaxType | None = Field(None, description="과세 적용 기준")

    # 즉시할인
    immediate_discount_unit_type: ProductImmediateDiscountUnitType | None = Field(None, description="즉시할인 단위")
    immediate_discount_value: float | None = Field(None, description="즉시할인 값")
    immediate_discount_period_yn: YnFlag | None = Field(None, description="즉시할인 기간 설정 여부")
    immediate_discount_start_ymdt: KstDatetime | None = Field(None, description="즉시할인 시작일자")
    immediate_discount_end_ymdt: KstDatetime | None = Field(None, description="즉시할인 종료일자")

    # 단위 가격
    unit_price: float | None = Field(None, description="단위 가격")
    unit_name: str | None = Field(None, description="단위 값")
    unit_name_type: str | None = Field(None, description="단위 유형")

    # 재고/옵션
    is_option_used: bool | None = Field(None, description="옵션 사용 유무")
    product_stock_cnt: int | None = Field(None, description="상품 재고 수량")
    option_data: PCOptionData = Field(..., description="옵션 데이터")

    # 구매 제한
    min_buy_cnt: int | None = Field(None, description="최소구매수량")
    max_buy_time_cnt: int | None = Field(None, description="1회최대구매수량")
    max_buy_person_cnt: int | None = Field(None, description="1인최대구매수량")
    max_buy_period_cnt: int | None = Field(None, description="최대구매기간(수량)")
    max_buy_days: int | None = Field(None, description="최대구매기간(일)")

    # 노출
    minor_purchase_yn: YnFlag | None = Field(None, description="미성년자 구매가능 여부")
    nonmember_purchase_yn: YnFlag | None = Field(None, description="비회원 구매가능 여부")
    platform_display_yn: YnFlag | None = Field(None, description="플랫폼 노출 설정 여부")
    platform_display_pc_yn: YnFlag | None = Field(None, description="플랫폼 - PC 노출 여부")
    platform_display_mobile_web_yn: YnFlag | None = Field(None, description="플랫폼 - 모바일 웹 노출 여부")
    platform_display_mobile_yn: YnFlag | None = Field(None, description="플랫폼 - 모바일 앱 노출 여부")

    # 이미지
    product_images: list[PCProductImageItem] = Field(default_factory=list, description="상품 이미지 목록")
    product_list_image: str | None = Field(None, description="리스트 이미지 URL")
    product_list_image_info: PCProductListImageInfo | None = Field(None, description="리스트 이미지 정보")

    # 판매 기간
    sale_period_type: ProductSalePeriodType | None = Field(None, description="판매기간설정")
    sale_start_ymdt: KstDatetime | None = Field(None, description="판매시작일")
    sale_end_ymdt: KstDatetime | None = Field(None, description="판매종료일")

    # 제조/유효기간
    manufacture_ymdt: KstDatetime | None = Field(None, description="제조일자")
    expiration_ymdt: KstDatetime | None = Field(None, description="유효기간")
    manufacturer: str | None = Field(None, description="제조사명")

    # 정보고시
    duty_info: str | None = Field(None, description="상품정보고시 (json 문자열)")
    product_guides: list[PCProductGuide] | None = Field(None, description="상품 안내 정보")
    use_restock_noti_yn: YnFlag | None = Field(None, description="재입고 알림 사용설정")

    # 장바구니
    cart_use_yn: YnFlag | None = Field(None, description="장바구니 사용 여부")
    cart_off_period_yn: YnFlag | None = Field(None, description="장바구니 불가 기간 설정")
    cart_off_start_ymdt: KstDatetime | None = Field(None, description="장바구니 불가 시작일자")
    cart_off_end_ymdt: KstDatetime | None = Field(None, description="장바구니 불가 종료일자")

    # 환불
    refundable_yn: YnFlag | None = Field(None, description="환불가능여부")

    # 브랜드
    brand_no: int | None = Field(None, description="브랜드 번호")

    # 배송
    delivery_yn: YnFlag | None = Field(None, description="배송 여부")
    delivery_template_no: int = Field(..., description="배송비 템플릿 번호")
    delivery_combination_yn: YnFlag | None = Field(None, description="묶음배송 가능 여부")
    delivery_international_yn: YnFlag | None = Field(None, description="해외배송 여부")
    shipping_area_type: ProductShippingAreaType | None = Field(None, description="출고유형")
    delivery_customer_info: str | None = Field(None, description="배송관련 판매자 특이사항/고객안내사항")

    # 마케팅/프로모션
    promotion_yn: YnFlag | None = Field(None, description="프로모션 적용 가능여부")
    promotion_text: str | None = Field(None, description="홍보문구")
    promotion_text_yn: YnFlag | None = Field(None, description="프로모션 기간 사용 여부")
    promotion_text_start_ymdt: KstDatetime | None = Field(None, description="프로모션 홍보문구 노출 시작일")
    promotion_text_end_ymdt: KstDatetime | None = Field(None, description="프로모션 홍보문구 노출 종료")

    # 검색어/추가
    keyword: str | None = Field(None, description="검색어 (,로 구분)")
    hs_code: str | None = Field(None, description="hs code")
    custom_property: list[PCCustomPropertyItem] = Field(default_factory=list, description="상품항목추가정보")
    stickers: list[PCDisplayPeriodSticker] | None = Field(None, description="스티커 정보")
    extra_json_map: PCExtraJson = Field(..., description="추가설정")
    related_product_info: PCRelatedProductInfo | None = Field(None, description="관련 상품 정보")
    extra_info: str | None = Field(None, description="추가 정보")


# ======================================================================
#  CreateCopiedProductRequest (products-productNo-1790230091, 80필드)
#  POST /products/{productNo} (재고연동상품)
#  접두사 Copied = 재고연동상품 전용 중첩 모델
# ======================================================================
class CopiedProductGuide(BaseDto):
    """상품 안내 (productGuides[])"""

    template_no: int | None = Field(None, description="상품 안내 템플릿 번호")
    type: Literal["DELIVERY", "AFTER_SERVICE", "REFUND", "EXCHANGE", "DELEGATION_BY_LIQUOR"] | None = Field(
        None, description="상품 안내 타입"
    )
    content: str | None = Field(None, description="상품 안내 내용")


class CopiedPromotionTextInfo(BaseDto):
    """홍보문구 등록 정보 (promotionTextInfo)"""

    start_ymd: str | None = Field(None, description="홍보문구 노출 시작 시간")
    end_ymd: str | None = Field(None, description="홍보문구 노출 종료 시간")
    period_yn: YnFlag | None = Field(None, description="홍보문구 기간설정 유무")
    text: str | None = Field(None, description="홍보문구")


class CopiedDeliveryDueDatePeriod(BaseDto):
    """배송지정일 기간 (deliveryDueDate.period)"""

    start_date: str | None = Field(None, description="시작일")


class CopiedDeliveryDueDate(BaseDto):
    """배송지정일 (deliveryDueDate)"""

    days_of_the_week: list[Literal["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]] | None = Field(
        None, description="요일"
    )
    period: CopiedDeliveryDueDatePeriod | None = Field(None, description="기간")
    days_after_purchase: int | None = Field(None, description="주문일 기준")


class CopiedMaxBuyCountInfo(BaseDto):
    """최대 구매수량 정보 (maxBuyCountInfo)"""

    max_buy_time_cnt: int | None = Field(None, description="1회당 최대 구매 수량")
    max_buy_days: int | None = Field(None, description="최대구매수량 기간 제한 - 기간")
    max_buy_period_cnt: int | None = Field(None, description="최대구매수량 기간 제한 - 제한 수량")
    max_buy_person_cnt: int | None = Field(None, description="1인당 최대 구매 수량")


class CopiedOptionImage(BaseDto):
    """옵션 이미지 (options[].optionImages[])"""

    main_yn: YnFlag | None = Field(None, description="메인 옵션 이미지 여부")
    mall_option_image_url: str | None = Field(None, description="옵션 이미지 URL")


class CopiedOptionMapping(BaseDto):
    """옵션 맵핑 정보(세트옵션) (options[].mappings[])"""

    mall_option_no: int | None = Field(None, description="타겟 옵션 번호")
    sale_price: float | None = Field(None, description="타겟 옵션의 개당 판매 가격")
    mapping_count: int | None = Field(None, description="판매 시 타겟옵션이 팔리는 개수")
    mall_product_no: int | None = Field(None, description="타겟 상품 번호")


class CopiedOption(BaseDto):
    """옵션정보 (options[])"""

    mall_option_no: int | None = Field(None, description="옵션번호")
    option_name: str | None = Field(None, description="옵션명")
    option_value: str | None = Field(None, description="옵션값")
    display_order: int | None = Field(None, description="전시 순서")
    add_price: float | None = Field(None, description="옵션 추가 가격")
    purchase_price: float | None = Field(None, description="공급가/매입가")
    stock_cnt: int | None = Field(None, description="옵션 재고 수량")
    reservation_stock_cnt: int | None = Field(None, description="예약 재고 수량")
    use_yn: YnFlag | None = Field(None, description="옵션 사용여부")
    sku: str | None = Field(None, description="재고 관리 단위")
    option_management_cd: str | None = Field(None, description="옵션 관리코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")
    stock_no: int | None = Field(None, description="재고번호")
    forced_sold_out: bool | None = Field(None, description="임시 품절 여부")
    option_images: list[CopiedOptionImage] | None = Field(None, description="옵션 이미지")
    mappings: list[CopiedOptionMapping] | None = Field(None, description="옵션 맵핑 정보(세트옵션)")


class CopiedMarketingSetting(BaseDto):
    """마케팅 채널 별 설정 정보 (marketingSettings[])"""

    channel_type: str | None = Field(None, description="채널 유형")
    displayable: bool | None = Field(None, description="노출 여부")
    additional_info: str | None = Field(None, description="부가 정보 (json)")


class CopiedMallProductImage(BaseDto):
    """상품 이미지 (mallProductImages[])"""

    image_id: str | None = Field(None, description="이미지 ID")
    image_url: str | None = Field(None, description="이미지 URL")
    origin_image_url: str | None = Field(None, description="원본 이미지 URL")
    main_yn: YnFlag | None = Field(None, description="메인 이미지 여부")
    display_order: int | None = Field(None, description="전시순서")
    is_external: bool | None = Field(None, description="외부 이미지 여부")
    image_url_type: ProductImageUrlType | None = Field(None, description="이미지 URL 타입")


class CopiedCommissionInfo(BaseDto):
    """판매수수료 정보 (commissionInfo)"""

    rate: float | None = Field(None, description="수수료율")
    type: Literal["PRODUCT", "CATEGORY", "PARTNER", "PURCHASE_PRICE"] | None = Field(
        None, description="판매수수료타입"
    )


class CopiedSalePeriodInfo(BaseDto):
    """판매기간 정보 (salePeriodInfo)"""

    period_type: ProductSalePeriodType | None = Field(None, description="판매기간설정")
    start_ymdt: KstDatetime | None = Field(None, description="판매 시작 시간")
    end_ymdt: KstDatetime | None = Field(None, description="판매 종료 시간")


class CopiedCertificationDataItem(BaseDto):
    """인증정보 데이터 (certificationInfo.data[])"""

    certification_category_no: int | None = Field(None, description="인증유형 번호")
    certification_contents: list[str] | None = Field(None, description="인증기관, 인증번호, 인증상호")


class CopiedCertificationInfo(BaseDto):
    """인증정보 (certificationInfo)"""

    type: Literal["TARGET", "NOT_TARGET", "DETAIL_PAGE"] | None = Field(None, description="인증정보타입")
    data: list[CopiedCertificationDataItem] | None = Field(None, description="인증정보")


class CopiedComparingPriceSiteInfo(BaseDto):
    """가격비교사이트 정보 (comparingPriceSiteInfo, deprecated)"""

    check: Literal["NONE", "ANY", "ALL"] | None = Field(None, description="전체설정 여부")
    info: list[str] | None = Field(None, description="가격비교사이트")


class CopiedImmediateDiscountInfo(BaseDto):
    """즉시할인 정보 (immediateDiscountInfo)"""

    unit_type: Literal["AMOUNT", "PERCENT"] | None = Field(None, description="즉시할인 단위")
    amount: float | None = Field(None, description="즉시할인 양")
    period_yn: YnFlag | None = Field(None, description="즉시할인 기간설정 여부")
    start_ymdt: KstDatetime | None = Field(None, description="즉시할인 시작 시간")
    end_ymdt: KstDatetime | None = Field(None, description="즉시할인 종료 시간")


class CopiedRelatedProduct(BaseDto):
    """관련 상품 (relatedProductInfo.products[])"""

    product_no: int | None = Field(None, description="관련 상품 번호")
    display_order: int | None = Field(None, description="노출 순서")


class CopiedRelatedProductInfo(BaseDto):
    """관련 상품 정보 (relatedProductInfo)"""

    config_type: Literal["DISPLAY_CATEGORY", "SELECTED"] | None = Field(None, description="관련 상품 설정")
    sort_criterion: Literal["LATEST_REGISTER_DATE", "SALES_COUNT", "REVIEW_COUNT", "CUSTOM_ORDER"] | None = Field(
        None, description="진열 순서"
    )
    products: list[CopiedRelatedProduct] | None = Field(None, description="관련 상품")


class CopiedPlatformDisplayInfo(BaseDto):
    """플랫폼별 노출 설정 정보 (platformDisplayInfo)"""

    display_yn: YnFlag | None = Field(None, description="플랫폼별 노출 설정")
    pc_yn: YnFlag | None = Field(None, description="PC 설정여부")
    mobile_web_yn: YnFlag | None = Field(None, description="모바일 웹 설정여부")
    mobile_yn: YnFlag | None = Field(None, description="모바일 앱 설정여부")


class CopiedCartInfo(BaseDto):
    """장바구니 정보 (cartInfo)"""

    use_yn: YnFlag | None = Field(None, description="장바구니 사용 여부")
    off_period_yn: YnFlag | None = Field(None, description="장바구니 담기 불가능한 기간 설정 여부")
    off_start_ymd: str | None = Field(None, description="장바구니 담기 불가능한 시작 시간")
    off_end_ymd: str | None = Field(None, description="장바구니 담기 불가능한 종료 시간")


class CopiedCustomerDemand(BaseDto):
    """구매자 작성형 (customerDemands[])"""

    input_no: int | None = Field(None, description="구매자작성형 번호 (신규생성: 0)")
    input_text: str | None = Field(None, description="구매자작성형 문구")
    use_yn: YnFlag | None = Field(None, description="사용 여부")
    matching_type: Literal["OPTION", "PRODUCT", "AMOUNT"] | None = Field(None, description="매칭타입")
    required: bool | None = Field(None, description="필수 여부")


class CopiedDutyContent(BaseDto):
    """상품정보고시 (dutyInfo.dutyContent)"""

    category_no: int | None = Field(None, description="상품정보제공고시 - 상품군 번호")
    category_name: str | None = Field(None, description="상품정보제공고시 - 상품군 이름")
    contents: list[dict[str, Any]] | None = Field(None, description="상품정보제공고시 내용")


class CopiedDutyInfo(BaseDto):
    """상품정보고시 정보 (dutyInfo)"""

    save_title: str | None = Field(None, description="상품정보고시 저장 title")
    duty_content: CopiedDutyContent | None = Field(None, description="상품정보고시")


class CopiedMemberDisplayInfo(BaseDto):
    """회원등급/그룹 노출 설정 정보 (memberGradeDisplayInfo / memberGroupDisplayInfo)"""

    check: Literal["NONE", "ANY", "ALL"] | None = Field(None, description="노출 설정")
    info: list[int] | None = Field(None, description="회원 등급/그룹 리스트")


class CopiedUnitPriceInfo(BaseDto):
    """단위별 가격 정보 (unitPriceInfo)"""

    name: str | None = Field(None, description="단위별 가격 - 기준 수량")
    type: str | None = Field(None, description="단위별 가격 - 단위")
    price: float | None = Field(None, description="단위별 가격")
    total_quantity: float | None = Field(None, description="총 수량 (개발중)")
    base_quantity: float | None = Field(None, description="기준 수량 (개발중)")


class CopiedExtraJson(BaseDto):
    """상품 추가 정보들 (extraJson)"""

    naver_display_yn: YnFlag | None = Field(None, description="네이버 쇼핑 EP - 노출 여부")
    naver_pay_limit_yn: YnFlag | None = Field(None, description="네이버 페이 결제 제한 여부")
    kakao_pay_limit_yn: YnFlag | None = Field(None, description="카카오 페이 결제 제한 여부")


class CopiedPlaceOriginInfo(BaseDto):
    """원산지번호 (placeOriginInfo)"""

    place_origins_yn: YnFlag | None = Field(None, description="복수 원산지 여부")
    place_origin: str | None = Field(None, description="직접입력 / 수입사")
    place_origin_seq: int | None = Field(None, description="원산지번호")


class CopiedPromotionInfo(BaseDto):
    """프로모션 적용 정보 (promotionInfo)"""

    promotion_yn: YnFlag | None = Field(None, description="프로모션 적용 설정 여부")
    coupon_yn: YnFlag | None = Field(None, description="쿠폰 프로모션 적용 가능 여부")
    free_gift_yn: YnFlag | None = Field(None, description="사은품 프로모션 적용 가능 여부")
    additional_discount_yn: YnFlag | None = Field(None, description="추가할인 프로모션 적용 가능 여부")


class CopiedSticker(BaseDto):
    """스티커 정보 (stickerInfos[])"""

    sticker_no: int | None = Field(None, description="스티커 번호")
    display_started_at: KstDatetime | None = Field(None, description="스티커 노출 시작일")
    display_ended_at: KstDatetime | None = Field(None, description="스티커 노출 종료일")


class CopiedReservationInfo(BaseDto):
    """예약판매 정보 (reservationInfoModel)"""

    delivery_ymdt: KstDatetime | None = Field(None, description="예약배송시작일")
    start_ymdt: KstDatetime | None = Field(None, description="예약판매 시작일")
    end_ymdt: KstDatetime | None = Field(None, description="예약판매 종료일")
    stock_cnt: int | None = Field(None, description="예약재고수량")


class CreateCopiedProductRequest(BaseDto):
    """재고연동상품 등록하기 요청 모델

    OpenAPI Schema: products-productNo-1790230091

    POST /products/{productNo} - 원본(마스터) 상품번호의 재고를 연동한 상품 등록.
    """

    mall_no: int = Field(..., description="몰 번호")
    partner_no: int = Field(..., description="파트너사 번호")
    admin_no: int = Field(..., description="담당자 번호")

    product_name: str = Field(..., description="상품명")
    product_name_en: str | None = Field(None, description="영문 상품명")
    supplier_product_name: str | None = Field(None, description="매입처 상품명")
    group_type: ProductGroupType = Field(..., description="상품군")
    class_type: Literal["DEFAULT", "OFFLINE", "RENTAL"] = Field(..., description="상품유형")
    sale_method_type: ProductSaleMethodType = Field(..., description="판매방식")
    category_no: int = Field(..., description="표준 카테고리 번호")
    display_category_nos: list[int] = Field(default_factory=list, description="전시 카테고리 번호")
    product_management_cd: str | None = Field(None, description="상품관리코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")
    ean_code: str | None = Field(None, description="EAN CODE")

    # 상품 내용
    content: str | None = Field(None, description="상품 상세")
    content_header: str | None = Field(None, description="상품 상세 상단")
    content_footer: str | None = Field(None, description="상품 상세 하단")
    add_option_image_yn: YnFlag = Field(..., description="등록된 옵션 이미지 사용 여부")

    # 가격
    sale_price: float = Field(..., description="판매가")
    purchase_price: float | None = Field(None, description="공급/매입가")
    partner_charge_amt: float | None = Field(None, description="파트너사 분담금")
    commission_info: CopiedCommissionInfo = Field(..., description="판매수수료 정보")
    accumulation_use_yn: YnFlag = Field(..., description="적립금 사용 가능 여부")
    accumulation_rate: float | None = Field(None, description="적립금적립 (%)")
    value_added_tax_type: ProductValueAddedTaxType = Field(..., description="부가세")
    unit_price_info: CopiedUnitPriceInfo = Field(..., description="단위별 가격 정보")
    immediate_discount_info: CopiedImmediateDiscountInfo = Field(..., description="즉시할인 정보")
    comparing_price_site_info: CopiedComparingPriceSiteInfo = Field(..., description="가격비교사이트 정보(deprecated)")

    # 재고/옵션
    product_stock_cnt: int = Field(..., description="상품 재고수량")
    option_type: Literal["COMBINATION", "DEFAULT", "REQUIRED"] = Field(..., description="옵션타입")
    option_select_type: Literal["MULTI", "FLAT"] | None = Field(None, description="옵션 선택 유형")
    options: list[CopiedOption] | None = Field(None, description="옵션정보")
    customer_demands: list[CopiedCustomerDemand] | None = Field(None, description="구매자 작성형")

    # 구매 제한
    min_buy_cnt: int | None = Field(None, description="최소 구매수량")
    max_buy_count_info: CopiedMaxBuyCountInfo | None = Field(None, description="최대 구매수량 정보")

    # 노출
    minor_purchase_yn: YnFlag = Field(..., description="미성년자 구매 가능 여부")
    nonmember_purchase_yn: YnFlag = Field(..., description="비회원구매 가능여부")
    platform_display_info: CopiedPlatformDisplayInfo = Field(..., description="플랫폼별 노출 설정 정보")
    url_direct_display_yn: YnFlag = Field(..., description="프론트 미노출 여부")
    member_grade_display_info: CopiedMemberDisplayInfo = Field(..., description="회원등급 노출 설정 정보")
    member_group_display_info: CopiedMemberDisplayInfo = Field(..., description="회원그룹 노출 설정 정보")

    # 이미지
    mall_product_images: list[CopiedMallProductImage] = Field(default_factory=list, description="상품 이미지")
    mall_product_list_image: str | None = Field(None, description="리스트 이미지 URL")

    # 판매 기간
    sale_period_info: CopiedSalePeriodInfo = Field(..., description="판매기간 정보")

    # 제조/유효기간
    manufacture_ymdt: KstDatetime | None = Field(None, description="제조일자")
    expiration_ymdt: KstDatetime | None = Field(None, description="유효일자")

    # 원산지/정보고시/인증
    place_origin_info: CopiedPlaceOriginInfo = Field(..., description="원산지번호")
    duty_info: CopiedDutyInfo = Field(..., description="상품정보고시 정보")
    certification_info: CopiedCertificationInfo = Field(..., description="인증정보")
    product_guides: list[CopiedProductGuide] | None = Field(None, description="상품 안내")
    use_restock_noti_yn: YnFlag | None = Field(None, description="재입고 알림 사용설정")

    # 장바구니
    cart_info: CopiedCartInfo = Field(..., description="장바구니 정보")

    # 환불
    refundable_yn: YnFlag = Field(..., description="환불가능여부")

    # 브랜드
    brand_no: int = Field(..., description="브랜드 번호")
    brand_name: str = Field(..., description="브랜드 이름")
    display_brand_no: int = Field(..., description="전시브랜드 번호")

    # 배송
    delivery_yn: YnFlag = Field(..., description="배송 여부")
    delivery_template_no: int | None = Field(None, description="배송 템플릿 번호")
    delivery_combination_yn: YnFlag | None = Field(None, description="묶음배송 가능여부")
    delivery_international_yn: YnFlag | None = Field(None, description="해외배송 여부")
    shipping_area_type: ProductShippingAreaType | None = Field(None, description="배송 구분")
    shipping_area_partner_no: int | None = Field(None, description="배송지 파트너 번호")
    delivery_customer_info: str | None = Field(None, description="판매자 특이사항/고객안내사항")
    delivery_due_date: CopiedDeliveryDueDate | None = Field(None, description="배송지정일")

    # 결제수단
    payment_means: list[
        Literal[
            "PAYCO",
            "CREDIT",
            "REALTIME_TRANSFER",
            "DEPOSIT",
            "ESCROW_REALTIME_TRANSFER",
            "ESCROW_VIRTUAL_ACCOUNT",
            "RENTAL",
        ]
    ] = Field(default_factory=list, description="결제수단항목")
    payment_means_control_yn: YnFlag = Field(..., description="결제수단제어 여부")

    # 마케팅/프로모션
    promotion_info: CopiedPromotionInfo = Field(..., description="프로모션 적용 정보")
    promotion_text_use_yn: YnFlag = Field(..., description="홍보문구 등록 여부")
    promotion_text_info: CopiedPromotionTextInfo | None = Field(None, description="홍보문구 등록 정보")
    marketing_settings: list[CopiedMarketingSetting] | None = Field(None, description="마케팅 채널 별 설정 정보")

    # 검색어/추가
    keywords: list[str] | None = Field(None, description="검색어")
    hs_code: str | None = Field(None, description="HS CODE")
    custom_property_values: list[int] | None = Field(None, description="상품추가항목")
    sticker_infos: list[CopiedSticker] | None = Field(None, description="스티커 정보")
    extra_json: CopiedExtraJson | None = Field(None, description="상품 추가 정보들")
    related_product_info: CopiedRelatedProductInfo | None = Field(None, description="관련 상품 정보")
    reservation_info_model: CopiedReservationInfo | None = Field(None, description="예약판매 정보")
    extra_info: str | None = Field(None, description="추가 정보")
    copies_review: bool | None = Field(None, description="상품평 복사 여부")
    temp_save: bool | None = Field(None, description="임시저장여부")

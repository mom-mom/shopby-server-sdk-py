"""상품 부분 수정하기 (version 2.0) 요청 모델"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto


class PatchContentDetail(BaseDto):
    """상품 내용 설정"""

    uses_option_image_instead_of_content: bool | None = Field(
        None, description="옵션 이미지로 상품 내용 대체 여부"
    )
    content_header: str | None = Field(None, description="상품 상단 내용 (html)")
    content: str | None = Field(None, description="상품 상세 내용")
    content_footer: str | None = Field(None, description="상품 하단 내용 (html)")


class PatchUnitPriceInfo(BaseDto):
    """가격 단위 정보"""

    unit_name: str | None = Field(None, description="단위 값")
    unit_name_type: str | None = Field(None, description="단위 유형")
    unit_price: float | None = Field(None, description="단위 가격")


class PatchImmediateDiscountInfo(BaseDto):
    """즉시 할인 정보"""

    unit_type: Literal["AMOUNT", "PERCENT"] | None = Field(None, description="즉시 할인 단위")
    amount: float | None = Field(None, description="즉시 할인 값")
    period_yn: Literal["Y", "N"] | None = Field(None, description="즉시 할인 기간 여부")
    start_ymdt: str | None = Field(None, description="즉시 할인 시작 일시")
    end_ymdt: str | None = Field(None, description="즉시 할인 종료 일시")


class PatchAccumulationLimitInfo(BaseDto):
    """적립금 사용 한도율"""

    unit_type: Literal["AMOUNT", "PERCENT"] | None = Field(None, description="적립금 사용 금액 단위")
    limit_value: float | None = Field(None, description="적립금 사용 양")


class PatchCommissionInfo(BaseDto):
    """수수료 정보"""

    type: Literal["PRODUCT", "CATEGORY", "PARTNER", "PURCHASE_PRICE"] | None = Field(
        None, description="판매수수료 타입"
    )
    rate: float | None = Field(None, description="판매수수료")


class PatchPriceInfo(BaseDto):
    """가격 관련 설정"""

    sale_price: float | None = Field(None, description="판매가")
    purchase_price: float | None = Field(None, description="공급가")
    partner_charge_amt: float | None = Field(None, description="정산시 파트너 분담금")
    commission_info: PatchCommissionInfo | None = Field(None, description="수수료 정보")
    immediate_discount_info: PatchImmediateDiscountInfo | None = Field(None, description="즉시 할인 정보")
    unit_price_info: PatchUnitPriceInfo | None = Field(None, description="가격 단위 정보")
    accumulation_rate: float | None = Field(None, description="적립률(%)")
    accumulation_use_yn: Literal["Y", "N"] | None = Field(None, description="적립금 사용 여부")
    accumulation_limit_info: PatchAccumulationLimitInfo | None = Field(None, description="적립금 사용 한도율")
    surtax_type: Literal["DUTY", "DUTYFREE", "SMALL"] | None = Field(None, description="과세 적용 기준")


class PatchMaxBuyQuantityInfo(BaseDto):
    """최대구매수량 정보"""

    type: Literal["PER_TIME", "PER_PERIOD", "PER_PERSON", "PER_DAY"] | None = Field(
        None, description="최대구매수량 유형"
    )
    max_buy_quantity: int | None = Field(None, description="최대구매수량 유형에 따른 최대구매수량")
    max_buy_days: int | None = Field(None, description="최대구매수량 유형이 PER_PERIOD인 경우, 최대 구매 기간 입력")


class PatchPurchaseLimitQuantity(BaseDto):
    """구매 수량 제한 설정"""

    min_buy_quantity: int | None = Field(None, description="최소구매수량")
    max_buy_quantity_info: PatchMaxBuyQuantityInfo | None = Field(None, description="최대구매수량 정보")


class PatchPlatformDisplayInfo(BaseDto):
    """플랫폼 별 노출 설정"""

    is_all: bool | None = Field(None, description="전체 노출 여부")
    any_values: list[Literal["PC", "MOBILE_WEB", "MOBILE"]] | None = Field(
        None, description="노출할 플랫폼 리스트"
    )


class PatchMemberDisplayInfo(BaseDto):
    """회원 등급/그룹 노출 설정 정보"""

    check: Literal["NONE", "ANY", "ALL"] | None = Field(None, description="노출 설정")
    info: list[int] | None = Field(None, description="노출 설정할 회원 등급/그룹 번호 리스트")


class PatchDisplayInfo(BaseDto):
    """노출 관련 설정"""

    platform_display_info: PatchPlatformDisplayInfo | None = Field(None, description="플랫폼 별 노출 설정")
    search_engine_displayable: bool | None = Field(None, description="검색엔진 노출 여부")
    guest_purchasable: bool | None = Field(None, description="비회원 구매 가능 여부")
    minor_purchasable: bool | None = Field(None, description="미성년자 구매가능 여부")
    only_url_accessible: bool | None = Field(None, description="프론트 미노출 여부")
    member_group_display_info: PatchMemberDisplayInfo | None = Field(None, description="회원 그룹 노출 설정 정보")
    member_grade_display_info: PatchMemberDisplayInfo | None = Field(None, description="회원 등급 노출 설정 정보")


class PatchProductImage(BaseDto):
    """상품 이미지"""

    image_no: int | None = Field(None, description="이미지 번호 (신규 생성 시 0)")
    url: str | None = Field(None, description="이미지 URL")
    is_main: bool | None = Field(None, description="대표 이미지 여부")
    url_type: Literal["IMAGE_URL", "VIDEO_URL"] | None = Field(None, description="url 타입")
    is_external: bool | None = Field(None, description="외부이미지 사용여부")


class PatchListImage(BaseDto):
    """리스트 이미지"""

    image_no: int | None = Field(None, description="리스트 이미지 번호 (신규 생성 시 0)")
    url: str | None = Field(None, description="리스트 이미지 URL")
    url_type: Literal["IMAGE_URL", "VIDEO_URL"] | None = Field(None, description="url 타입")
    is_external: bool | None = Field(None, description="외부이미지 사용여부")


class PatchImageInfo(BaseDto):
    """상품 이미지 관련 설정"""

    uses_external_image: bool | None = Field(None, description="외부 이미지 URL 사용 여부")
    images: list[PatchProductImage] | None = Field(None, description="상품 이미지 리스트")
    list_image: PatchListImage | None = Field(None, description="리스트 이미지")


class PatchSalePeriod(BaseDto):
    """판매 기간"""

    start_ymdt: str | None = Field(None, description="판매 시작일시")
    end_ymdt: str | None = Field(None, description="판매 종료일시")


class PatchSalePeriodInfo(BaseDto):
    """판매 기간 정보"""

    sale_period_type: Literal["REGULAR", "PERIOD"] | None = Field(None, description="판매 기간 유형")
    sale_period: PatchSalePeriod | None = Field(None, description="판매 기간")


class PatchPlaceOriginInfo(BaseDto):
    """원산지 정보"""

    place_origin_seq: int | None = Field(None, description="원산지 번호")
    place_origins_yn: Literal["Y", "N"] | None = Field(None, description="원산지 직접 입력 사용 유무")
    place_origin: str | None = Field(None, description="원산지 직접 입력인 경우, 원산지 입력")


class PatchDutyContent(BaseDto):
    """상품정보고시"""

    category_no: int | None = Field(None, description="상품 정보 고시 항목 번호")
    category_name: str | None = Field(None, description="상품 정보 고시 항목명")
    contents: list[dict[str, Any]] | None = Field(None, description="상품 정보 고시 상세 내용")


class PatchProductGuide(BaseDto):
    """상품 안내 정보"""

    template_no: int | None = Field(None, description="상품 안내 정보 - 템플릿 번호")
    type: Literal["DELIVERY", "AFTER_SERVICE", "REFUND", "EXCHANGE", "DELEGATION_BY_LIQUOR"] | None = Field(
        None, description="상품 안내 정보 - 템플릿 유형"
    )
    content: str | None = Field(None, description="상품 안내 정보 - 직접 입력하는 경우에만 입력")


class PatchUnavailablePeriod(BaseDto):
    """장바구니 불가 기간"""

    start_ymdt: str | None = Field(None, description="장바구니 불가 시작일시")
    end_ymdt: str | None = Field(None, description="장바구니 불가 종료일시")


class PatchCartInfo(BaseDto):
    """장바구니 설정"""

    is_available_cart: bool | None = Field(None, description="장바구니 가능 여부")
    unavailable_period: PatchUnavailablePeriod | None = Field(None, description="장바구니 불가 기간")


class PatchRefundableInfo(BaseDto):
    """환불 정보"""

    refundable: bool | None = Field(None, description="환불 가능 여부")
    non_refund_types: list[Literal["RETURN", "EXCHANGE"]] | None = Field(
        None, description="환불 불가인 경우, 불가능 항목"
    )


class PatchBrandNoInfo(BaseDto):
    """브랜드 번호 정보"""

    brand_no: int | None = Field(None, description="브랜드 번호")
    display_brand_no: int | None = Field(None, description="전시 브랜드 번호")


class PatchBrandNameInfo(BaseDto):
    """브랜드명 정보"""

    main_name: str | None = Field(None, description="메인 브랜드명")
    sub_name: str | None = Field(None, description="서브 브랜드명")


class PatchBrandInfo(BaseDto):
    """브랜드 정보"""

    input_type: Literal["NO", "NAME"] | None = Field(None, description="브랜드 입력 유형")
    brand_no_info: PatchBrandNoInfo | None = Field(None, description="브랜드 번호 정보")
    brand_name_info: PatchBrandNameInfo | None = Field(None, description="브랜드명 정보")


class PatchOptionImage(BaseDto):
    """옵션 이미지"""

    url: str | None = Field(None, description="옵션 이미지 URL")
    is_main: bool | None = Field(None, description="옵션 대표 이미지 여부")


class PatchOption(BaseDto):
    """옵션 정보"""

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
    images: list[PatchOptionImage] | None = Field(None, description="옵션 이미지")
    is_required_option: bool | None = Field(None, description="필수 옵션 여부")


class PatchCustomerDemand(BaseDto):
    """구매자 작성형 옵션"""

    customer_demand_no: int | None = Field(None, description="작성형 옵션 번호 (신규 생성 0)")
    content: str | None = Field(None, description="작성형 옵션 텍스트 내용")
    target_type: Literal["OPTION", "PRODUCT", "AMOUNT"] | None = Field(None, description="작성형 옵션 매칭 유형")
    required: bool | None = Field(None, description="작성형 옵션 입력 필수 여부")
    usable: bool | None = Field(None, description="작성형 옵션 사용 여부")


class PatchOptionInfo(BaseDto):
    """옵션 설정"""

    options: list[PatchOption] | None = Field(None, description="옵션 목록")
    option_select_type: Literal["MULTI", "FLAT"] | None = Field(None, description="옵션 노출 유형")
    customer_demands: list[PatchCustomerDemand] | None = Field(None, description="구매자 작성형 옵션")
    sets: list[dict[str, Any]] | None = Field(None, description="세트 옵션")


class PatchDeliveryInfo(BaseDto):
    """배송 관련 설정"""

    uses_delivery: bool | None = Field(None, description="배송 여부")
    shipping_area_type: Literal["PARTNER_SHIPPING_AREA", "MALL_SHIPPING_AREA"] | None = Field(
        None, description="출고유형"
    )
    shipping_area_partner_no: int | None = Field(None, description="출고지 파트너 번호")
    delivery_template_no: int | None = Field(None, description="배송비 템플릿 번호")
    can_delivery_combination: bool | None = Field(None, description="묶음 배송 가능 여부")
    can_delivery_international: bool | None = Field(None, description="해외 배송 가능 여부")
    delivery_customer_info: str | None = Field(None, description="배송관련 판매자 특이사항/고객안내사항")


class PatchMarketingDisplayPeriod(BaseDto):
    """홍보 문구 노출 기간"""

    start_ymdt: str | None = Field(None, description="홍보 문구 노출 시작일시")
    end_ymdt: str | None = Field(None, description="홍보 문구 노출 종료일시")


class PatchMarketingPhraseInfo(BaseDto):
    """홍보 문구 정보"""

    marketing_phrase: str | None = Field(None, description="홍보 문구")
    marketing_display_period: PatchMarketingDisplayPeriod | None = Field(None, description="홍보 문구 노출 기간")


class PatchMarketingInfo(BaseDto):
    """마케팅 관련 설정"""

    marketing_phrase_info: PatchMarketingPhraseInfo | None = Field(None, description="홍보 문구 정보")
    is_available_promotion: bool | None = Field(None, description="프로모션 사용 여부")


class PatchCustomProperty(BaseDto):
    """추가 항목"""

    property: str | None = Field(None, description="추가 항목 - 항목명")
    values: list[str] | None = Field(None, description="추가 항목 - 항목값명")


class PatchStickerDisplayPeriod(BaseDto):
    """스티커 노출 기간"""

    start_ymdt: str | None = Field(None, description="스티커 노출 시작일시")
    end_ymdt: str | None = Field(None, description="스티커 노출 종료일시")


class PatchSticker(BaseDto):
    """스티커 정보"""

    sticker_no: int | None = Field(None, description="스티커 번호 (신규 생성 0)")
    display_period: PatchStickerDisplayPeriod | None = Field(None, description="스티커 노출 기간")


class PatchExtraJson(BaseDto):
    """추가설정"""

    naver_display_yn: str | None = Field(None, description="네이버 쇼핑 EP - 노출 여부")
    serial_number: str | None = Field(None, description="제품 일련번호")
    naver_pay_limit_yn: str | None = Field(None, description="네이버 페이 결제 제한 여부")
    naver_product_status: Literal["NEW", "USED", "REFURB", "DISPLAY", "RETURN", "SCRATCH"] | None = Field(
        None, description="네이버 쇼핑 EP - 상품 상태"
    )
    naver_category_id: str | None = Field(None, description="네이버 쇼핑 EP - 카테고리 ID")
    manufacture_name: str | None = Field(None, description="제조사명")
    naver_product_flag: Literal[
        "WHOLESALE", "RENTAL", "LENT", "INSTALLMENT", "RESERVATION_SALE", "SUBSTITUTION", "RESERVATION_BUY"
    ] | None = Field(None, description="네이버 쇼핑 EP - 상품 판매 종류")
    naver_extra: str | None = Field(None, description="네이버 쇼핑 EP 기타 정보")
    product_model_name: str | None = Field(None, description="제품모델명")
    price_compare_page_id: str | None = Field(None, description="네이버 쇼핑 EP - 가격 비교 페이지 ID")
    naver_point_accum_locations: str | None = Field(None, description="네이버포인트 적립 가능 플랫폼")


class PatchRelatedProductInfo(BaseDto):
    """관련 상품 정보"""

    config_type: Literal["DISPLAY_CATEGORY", "SELECTED"] | None = Field(None, description="관련 상품 설정")
    sort_criterion: Literal["LATEST_REGISTER_DATE", "SALES_COUNT", "REVIEW_COUNT", "CUSTOM_ORDER"] | None = Field(
        None, description="관련 상품 진열 순서"
    )
    product_nos: list[int] | None = Field(None, description="상품 번호 리스트")


class PatchProductV2Request(BaseDto):
    """
    상품 부분 수정하기 (version 2.0) 요청 모델

    OpenAPI Schema: products-productNo-911598269

    모든 필드는 선택적입니다. 수정이 필요한 필드만 입력합니다.
    """

    # 기본 정보
    group_type: Literal["DELIVERY", "SERVICE"] | None = Field(None, description="상품군")
    class_type: Literal["DEFAULT", "EVENT", "OFFLINE", "RENTAL"] | None = Field(None, description="상품분류")
    sale_method_type: Literal["PURCHASE", "CONSIGNMENT"] | None = Field(None, description="판매방식")
    standard_category_no: int | None = Field(None, description="표준 카테고리")
    display_category_nos: list[int] | None = Field(None, description="전시 카테고리 리스트")
    representative_display_category_no: int | None = Field(None, description="대표 전시 카테고리")
    merchandiser_no: int | None = Field(None, description="상품 담당자")

    # 상품명
    product_name: str | None = Field(None, description="상품명")
    product_name_en: str | None = Field(None, description="영문 상품명")
    supplier_product_name: str | None = Field(None, description="매입처 상품명")

    # 상품 내용
    content_detail: PatchContentDetail | None = Field(None, description="상품 내용 설정")

    # 관리 코드
    management_code: str | None = Field(None, description="판매자 관리 코드")
    extra_management_code: str | None = Field(None, description="추가관리코드")

    # 가격
    price: PatchPriceInfo | None = Field(None, description="가격 관련 설정")

    # 재고
    stock_quantity: int | None = Field(None, description="재고 수량")

    # 구매 제한
    purchase_limit_quantity: PatchPurchaseLimitQuantity | None = Field(None, description="구매 수량 제한 설정")

    # 노출 설정
    display: PatchDisplayInfo | None = Field(None, description="노출 관련 설정")

    # 이미지
    image: PatchImageInfo | None = Field(None, description="상품 이미지 관련 설정")

    # 기타 정보
    hs_code: str | None = Field(None, description="HS CODE")
    keywords: list[str] | None = Field(None, description="검색어 리스트")

    # 판매 기간
    sale_period_info: PatchSalePeriodInfo | None = Field(None, description="판매 기간 정보")

    # 제조/유효기간
    manufactured_date_time: str | None = Field(None, description="제조일자 (YYYY-MM-DD HH:00:00)")
    expiration_date_time: str | None = Field(None, description="유효기간 (YYYY-MM-DD HH:00:00)")

    # 원산지
    place_origin_info: PatchPlaceOriginInfo | None = Field(None, description="원산지 정보")

    # 상품정보고시
    duty_content: PatchDutyContent | None = Field(None, description="상품정보고시")

    # 상품 안내
    product_guides: list[PatchProductGuide] | None = Field(None, description="상품 안내 정보")

    # 재입고 알림
    uses_restock_notification: bool | None = Field(None, description="재입고 알림 사용설정")

    # 장바구니
    cart_info: PatchCartInfo | None = Field(None, description="장바구니 설정")

    # 환불
    refundable_info: PatchRefundableInfo | None = Field(None, description="환불 정보")

    # 브랜드
    brand: PatchBrandInfo | None = Field(None, description="브랜드 정보")

    # 옵션
    option_type: Literal["COMBINATION", "NONE", "REQUIRED"] | None = Field(None, description="옵션 유형")
    option: PatchOptionInfo | None = Field(None, description="옵션 설정")

    # 배송
    delivery: PatchDeliveryInfo | None = Field(None, description="배송 관련 설정")

    # 마케팅
    marketing: PatchMarketingInfo | None = Field(None, description="마케팅 관련 설정")

    # 추가 속성
    custom_properties: list[PatchCustomProperty] | None = Field(None, description="추가 항목")

    # 스티커
    stickers: list[PatchSticker] | None = Field(None, description="스티커 정보")

    # 추가 설정
    extra_json: PatchExtraJson | None = Field(None, description="추가설정")

    # 관련 상품
    related_product_info: PatchRelatedProductInfo | None = Field(None, description="관련 상품 정보")

    # 기타
    extra_info: str | None = Field(None, description="추가 정보")
    url_shortening_yn: Literal["Y", "N"] | None = Field(None, description="단축URL 사용여부")

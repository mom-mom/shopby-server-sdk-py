"""상품 상세 조회하기 (Version 1.0) 응답 모델"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDate, KstDatetime


class V1RefundableInfo(BaseDto):
    """환불 정보 (V1)"""

    refundable_yn: str = Field(..., description="환불가능여부")
    non_refundable_info: list[str] = Field(default_factory=list, description="환불불가 항목")


class V1AccumulationLimitInfo(BaseDto):
    """적립금 사용 한도 (V1)"""

    unit_type: Literal["AMOUNT", "PERCENT"] | None = Field(None, description="적립금 단위")
    limit_value: float | None = Field(None, description="적립금 제한값")


class V1DisplayCategory(BaseDto):
    """전시 카테고리 (V1)"""

    display_category_no: int = Field(..., description="전시카테고리 번호")
    mall_no: int = Field(..., description="몰 번호")
    display_category_name: str = Field(..., description="전시카테고리명")
    icon: str = Field(..., description="아이콘")
    top_image_content: str = Field(..., description="상단이미지 내용")
    display_order: int = Field(..., description="전시순서")
    display_yn: str = Field(..., description="전시여부")
    delete_yn: str = Field(..., description="삭제여부")
    depth: int = Field(..., description="뎁스")


class V1StickerDisplayPeriod(BaseDto):
    """스티커 노출 기간 (V1)"""

    start_date_time: KstDatetime | None = Field(None, description="스티커 노출 시작일")
    end_date_time: KstDatetime | None = Field(None, description="스티커 노출 종료일")


class V1Sticker(BaseDto):
    """스티커 정보 (V1)"""

    sticker_no: int = Field(..., description="스티커 번호")
    label: str = Field(..., description="스티커 라벨")
    delete_yn: str = Field(..., description="삭제여부")
    sticker_exposure_position: str | None = Field(None, description="스티커 노출 위치")
    display_order: int = Field(..., description="전시순서")
    sticker_type: str = Field(..., description="스티커 유형")
    image_url: str | None = Field(None, description="스티커 이미지 URL")
    mall_no: int = Field(..., description="몰 번호")
    display_period: V1StickerDisplayPeriod | None = Field(None, description="스티커 노출 기간")


class V1CustomPropertyValue(BaseDto):
    """커스텀 속성 값 (V1)"""

    prop_value_no: int = Field(..., description="항목값 번호")
    prop_value: str = Field(..., description="항목값")
    prop_name: str = Field(..., description="항목명")
    display_order: int = Field(..., description="전시순서")
    register_ymdt: KstDatetime = Field(..., description="등록일")
    register_admin_no: int = Field(..., description="등록자 번호")
    modify_ymdt: KstDatetime | None = Field(None, description="수정일")
    modify_admin_no: int | None = Field(None, description="수정자 번호")
    delete_yn: bool = Field(..., description="삭제여부")


class V1ReservationInfo(BaseDto):
    """예약 정보 (V1)"""

    start_date_time: KstDatetime = Field(..., description="예약판매 시작일")
    end_date_time: KstDatetime = Field(..., description="예약판매 종료일")
    delivery_date_time: KstDatetime = Field(..., description="예약판매 배송시작일")


class V1RelatedProductInfo(BaseDto):
    """관련 상품 정보 (V1)"""

    config_type: str | None = Field(None, description="관련 상품 설정 유형")
    sort_criterion: str | None = Field(None, description="관련 상품 정렬 기준")
    products: list[Any] = Field(default_factory=list, description="관련 상품 목록")
    mall_no: int | None = Field(None, description="몰 번호")


class V1ImageUrlMappingInfo(BaseDto):
    """이미지 URL 매핑 정보 (V1)"""

    content_header: dict[str, Any] = Field(default_factory=dict, description="상단 내용 이미지 매핑")
    content: dict[str, Any] = Field(default_factory=dict, description="본문 내용 이미지 매핑")
    content_footer: dict[str, Any] = Field(default_factory=dict, description="하단 내용 이미지 매핑")


class V1MallProduct(BaseDto):
    """상품 정보 (V1)"""

    mall_product_no: int = Field(..., description="상품번호")
    product_no: int = Field(..., description="원본 상품번호")
    parent_mall_product_no: int | None = Field(None, description="부모 상품번호")
    mall_no: int = Field(..., description="몰 번호")
    master_yn: str = Field(..., description="마스터 상품 여부")
    partner_no: int = Field(..., description="파트너 번호")
    category_no: int = Field(..., description="표준 카테고리 번호")
    product_name: str = Field(..., description="상품명")
    product_type: str = Field(..., description="상품 유형")
    class_type: str = Field(..., description="클래스 유형")
    mapping_type: str = Field(..., description="매핑 유형")
    apply_status_type: str = Field(..., description="승인 상태")
    sale_status_type: str = Field(..., description="판매 상태")
    sale_setting_status_type: str = Field(..., description="판매 설정 상태")
    group_type: str = Field(..., description="상품군")
    sale_method_type: str = Field(..., description="판매방식")
    payment_means_control_yn: str = Field(..., description="결제수단 제어 여부")
    payment_means: str = Field(..., description="결제수단")
    refundable_yn: str = Field(..., description="환불 가능 여부")
    refundable_info: V1RefundableInfo | None = Field(None, description="환불 정보")
    display_brand_no: int = Field(..., description="전시브랜드 번호")
    brand_no: int = Field(..., description="브랜드 번호")
    admin_no: int = Field(..., description="관리자 번호")
    sale_period_type: str = Field(..., description="판매기간 유형")
    sale_start_ymdt: KstDatetime = Field(..., description="판매 시작일")
    sale_end_ymdt: KstDatetime = Field(..., description="판매 종료일")
    manufacture_ymdt: KstDatetime | None = Field(None, description="제조일")
    register_ymdt: KstDatetime = Field(..., description="등록일")
    register_admin_no: int = Field(..., description="등록자 번호")
    update_ymdt: KstDatetime | None = Field(None, description="수정일")
    update_admin_no: int | None = Field(None, description="수정자 번호")
    sale_price: float = Field(..., description="판매가")
    min_buy_cnt: int = Field(..., description="최소 구매 수량")
    max_buy_person_cnt: int = Field(..., description="1인당 최대 구매 수량")
    max_buy_time_cnt: int = Field(..., description="1회 최대 구매 수량")
    max_buy_days: int = Field(..., description="최대 구매 기간")
    max_buy_period_cnt: int = Field(..., description="최대 구매 기간 수량")
    immediate_discount_apply_price: float = Field(..., description="즉시할인 적용가")
    immediate_discount_value: float = Field(..., description="즉시할인 값")
    immediate_discount_unit_type: Literal["WON", "RATE"] = Field(..., description="즉시할인 단위")
    immediate_discount_period_yn: str = Field(..., description="즉시할인 기간설정 여부")
    immediate_discount_start_ymdt: KstDatetime | None = Field(None, description="즉시할인 시작일")
    immediate_discount_end_ymdt: KstDatetime | None = Field(None, description="즉시할인 종료일")
    comparing_price_site: str | None = Field(None, description="가격비교 사이트 (deprecated)")
    nonmember_purchase_yn: str = Field(..., description="비회원 구매 가능 여부")
    minor_purchase_yn: str = Field(..., description="미성년자 구매 가능 여부")
    unit_name: str = Field(..., description="단위명")
    unit_name_type: str | None = Field(None, description="단위명 유형")
    unit_price: int = Field(..., description="단위가격")
    point_rate: int = Field(..., description="포인트율")
    accumulation_rate: float | None = Field(None, description="적립률")
    accumulation_use_yn: str = Field(..., description="적립금 사용 여부")
    accumulation_limit_info: V1AccumulationLimitInfo | None = Field(None, description="적립금 제한 정보")
    certification_json: str = Field(..., description="인증정보 JSON")
    certification_type: str = Field(..., description="인증유형")
    place_origin: str | None = Field(None, description="원산지")
    place_origins_yn: str = Field(..., description="복수 원산지 여부")
    expiration_ymdt: KstDatetime | None = Field(None, description="유효기간")
    value_added_tax_type: str = Field(..., description="부가세 유형")
    product_management_cd: str = Field(..., description="판매자 관리코드")
    cart_use_yn: str = Field(..., description="장바구니 사용 여부")
    cart_off_period_yn: str = Field(..., description="장바구니 OFF 기간설정 여부")
    cart_off_start_ymdt: KstDatetime | None = Field(None, description="장바구니 OFF 시작일")
    cart_off_end_ymdt: KstDatetime | None = Field(None, description="장바구니 OFF 종료일")
    commission_rate_type: str = Field(..., description="수수료율 유형")
    commission_rate: float = Field(..., description="수수료율")
    keyword: str = Field(..., description="검색 키워드")
    extra_json: str = Field(..., description="추가 JSON 정보")
    product_name_en: str = Field(..., description="영문 상품명")
    hs_code: str = Field(..., description="HS코드")
    ean_code: str = Field(..., description="EAN코드")
    promotion_yn: str = Field(..., description="프로모션 사용 여부")
    additional_discount_yn: str = Field(..., description="추가할인 사용 여부")
    coupon_yn: str = Field(..., description="쿠폰 사용 여부")
    free_gift_yn: str = Field(..., description="사은품 사용 여부")
    promotion_text_yn: str = Field(..., description="홍보문구 사용 여부")
    promotion_text: str = Field(..., description="홍보문구")
    promotion_text_start_ymdt: KstDatetime | None = Field(None, description="홍보문구 노출 시작일")
    promotion_text_end_ymdt: KstDatetime | None = Field(None, description="홍보문구 노출 종료일")
    platform_display_yn: str = Field(..., description="플랫폼 전시 여부")
    platform_display_pc_yn: str = Field(..., description="PC 전시 여부")
    platform_display_mobile_yn: str = Field(..., description="모바일앱 전시 여부")
    platform_display_mobile_web_yn: str = Field(..., description="모바일웹 전시 여부")
    searchengine_display_yn: str = Field(..., description="검색엔진 전시 여부")
    duty_info: str | None = Field(None, description="상품정보고시 JSON")
    content_header: str = Field(..., description="상품 상세 상단")
    content: str = Field(..., description="상품 상세")
    content_footer: str = Field(..., description="상품 상세 하단")
    partner_charge_amt: float = Field(..., description="파트너 부담금")
    front_display_yn: str = Field(..., description="전면 전시 여부")
    url_direct_display_yn: str = Field(..., description="URL 직접 전시 여부")
    delivery_yn: str = Field(..., description="배송 여부")
    shipping_area_type: str = Field(..., description="출고 유형")
    shipping_area_partner_no: int = Field(..., description="출고지 파트너 번호")
    delivery_combination_yn: str = Field(..., description="묶음배송 가능 여부")
    delivery_international_yn: str = Field(..., description="해외배송 가능 여부")
    delivery_template_no: int = Field(..., description="배송템플릿 번호")
    delivery_customer_info: str = Field(..., description="배송 고객 정보")
    is_option_used: bool = Field(..., description="옵션 사용 여부")
    add_option_image_yn: str = Field(..., description="옵션 이미지 추가 여부")
    place_origin_seq: int | None = Field(None, description="원산지 순번")
    sync_wms_yn: str = Field(..., description="WMS 동기화 여부")
    delete_yn: str = Field(..., description="삭제 여부")
    temp_save: str = Field(..., description="임시저장 여부")
    item_yn: str = Field(..., description="아이템 여부")
    member_grade_display_info: str | None = Field(None, description="회원등급 전시 정보 JSON")
    member_group_display_info: str | None = Field(None, description="회원그룹 전시 정보 JSON")
    register_site_type: str = Field(..., description="등록 사이트 유형")
    image_url_mapping_info: V1ImageUrlMappingInfo | None = Field(None, description="이미지 URL 매핑 정보")
    stickers: list[V1Sticker] | None = Field(None, description="스티커 목록")
    custom_property_values: list[V1CustomPropertyValue] | None = Field(None, description="커스텀 속성 값")
    display_categories: list[V1DisplayCategory] | None = Field(None, description="전시 카테고리 목록")
    partner_name: str = Field(..., description="파트너명")
    mapping_key: str = Field(..., description="매핑 키")
    reservation_info: V1ReservationInfo | None = Field(None, description="예약 정보")
    visible_sale_status: str = Field(..., description="노출 판매상태")
    liquor_delegation_guide: str | None = Field(None, description="주류 통신판매 위임 고시")
    related_product_info: V1RelatedProductInfo | None = Field(None, description="관련 상품 정보")
    sale_start_ymd: KstDate = Field(..., description="판매 시작일 (날짜만)")
    sale_end_ymd: KstDate = Field(..., description="판매 종료일 (날짜만)")


class V1MallProductImage(BaseDto):
    """상품 이미지 (V1)"""

    mall_image_no: int = Field(..., description="이미지 번호")
    product_image_no: int = Field(..., description="원본 이미지 번호")
    mall_product_no: int = Field(..., description="상품번호")
    image_url: str = Field(..., description="이미지 URL")
    origin_image_url: str = Field(..., description="원본 이미지 URL")
    main_yn: str = Field(..., description="메인 이미지 여부")
    display_order: int = Field(..., description="전시순서")
    image_id: str = Field(..., description="NHN Cloud 이미지 ID")
    main_image: bool = Field(..., description="메인 이미지 여부 (bool)")


class V1MallProductInput(BaseDto):
    """구매자 작성형 정보 (V1)"""

    mall_product_input_no: int = Field(..., description="구매자작성형 번호")
    input_text: str = Field(..., description="구매자작성형 텍스트")
    input_matching_type_label: str = Field(..., description="매칭 유형 라벨")
    use_yn: str = Field(..., description="사용여부")
    required: bool = Field(..., description="필수 여부")


class V1OptionImage(BaseDto):
    """옵션 이미지 (V1)"""

    mall_option_image_no: int = Field(..., description="옵션 이미지 번호")
    mall_option_no: int = Field(..., description="옵션 번호")
    mall_option_image_url: str = Field(..., description="옵션 이미지 URL")
    origin_mall_option_image_url: str = Field(..., description="원본 옵션 이미지 URL")
    main_yn: str = Field(..., description="메인 이미지 여부")
    display_order: int = Field(..., description="전시순서")
    mall_option_image_id: str = Field(..., description="NHN Cloud 이미지 ID")


class V1MappingOption(BaseDto):
    """매핑 옵션 (V1)"""

    mall_option_no: int = Field(..., description="상품 옵션 번호")
    item_mall_product_no: int = Field(..., description="매핑 상품번호")
    item_mall_option_no: int = Field(..., description="매핑 옵션 번호")
    sku: str | None = Field(None, description="SKU")
    item_stock_no: int = Field(..., description="매핑 옵션 재고번호")
    item_stock_cnt: int = Field(..., description="매핑 옵션 재고수량")
    item_safety_stock_cnt: int = Field(..., description="매핑 옵션 안전재고 수량")
    item_delivery_waiting_stock_cnt: int = Field(..., description="매핑 옵션 출고대기 재고 수량")
    product_name: str = Field(..., description="매핑 상품명")
    product_management_cd: str = Field(..., description="매핑 상품 관리코드")
    option_management_cd: str = Field(..., description="매핑 옵션 관리코드")
    original_mapping_option_sale_price: float = Field(..., description="매핑 옵션 원판매가")
    mapping_cnt: int = Field(..., description="매핑 옵션 판매 수량")
    mapping_option_sale_price: float = Field(..., description="매핑 상품 판매가")
    mapping_display_order: int = Field(..., description="순서")
    option_name: str = Field(..., description="옵션명")
    option_value: str = Field(..., description="옵션값")
    apply_status_type: str = Field(..., description="등록 상태")
    sale_status_type: str = Field(..., description="판매 상태")
    sale_start_ymdt: KstDatetime | None = Field(None, description="판매 시작일")
    sale_end_ymdt: KstDatetime | None = Field(None, description="판매 종료일")
    reservation_start_ymdt: KstDatetime | None = Field(None, description="예약 구매 시작일")
    reservation_end_ymdt: KstDatetime | None = Field(None, description="예약 구매 종료일")
    before_onsale: bool = Field(..., description="판매일 시작 여부")
    delete_yn: bool | None = Field(None, description="삭제 여부")
    option_name_value_pair: str = Field(..., description="옵션명 옵션값 페어")
    option_sale_status_type: str = Field(..., description="옵션 판매 상태")
    option_reservation_sale_status_type: str | None = Field(None, description="옵션 예약 구매 상태")


class V1MallProductOption(BaseDto):
    """상품 옵션 (V1)"""

    mall_product_no: int = Field(..., description="상품번호")
    mall_no: int = Field(..., description="몰 번호")
    stock_no: int = Field(..., description="재고번호")
    option_type: str = Field(..., description="옵션 유형")
    option_no: int = Field(..., description="옵션번호")
    mall_option_no: int = Field(..., description="쇼핑몰 옵션번호")
    option_name: str = Field(..., description="옵션명")
    option_value: str = Field(..., description="옵션값")
    display_order: int = Field(..., description="전시순서")
    add_price: float = Field(..., description="옵션 추가 가격")
    commission_rate: float = Field(..., description="수수료율")
    sale_status_type: str = Field(..., description="판매상태")
    use_yn: str = Field(..., description="사용여부")
    option_management_cd: str = Field(..., description="판매자 관리코드")
    extra_management_cd: str | None = Field(None, description="추가 관리코드")
    register_ymdt: KstDatetime = Field(..., description="등록일")
    register_admin_no: int = Field(..., description="등록자 번호")
    update_ymdt: KstDatetime | None = Field(None, description="수정일")
    update_admin_no: int | None = Field(None, description="수정자 번호")
    master_yn: str = Field(..., description="마스터 옵션 여부")
    delete_yn: str = Field(..., description="삭제여부")
    stock_cnt: int = Field(..., description="재고수량")
    delivery_waiting_stock_cnt: int = Field(..., description="출고대기 재고수량")
    safety_stock_cnt: int = Field(..., description="안전재고 수량")
    reservation_stock_cnt: int = Field(..., description="예약재고 수량")
    sale_cnt: int = Field(..., description="판매수량")
    weight: float = Field(..., description="무게")
    purchase_price: float = Field(..., description="공급/매입가")
    sku: str | None = Field(None, description="SKU")
    edit_price_yn: str | None = Field(None, description="가격 변동 여부")
    edit_yn: str = Field(..., description="옵션 수정 여부")
    deletable: str = Field(..., description="삭제 가능 여부")
    slave_mall_option_nos: list[int] = Field(default_factory=list, description="매칭 옵션 번호 목록")
    item_yn: str = Field(..., description="자재상품 여부")
    option_images: list[V1OptionImage] = Field(default_factory=list, description="옵션 이미지 목록")
    delete_option_image_no_list: list[int] = Field(default_factory=list, description="삭제 옵션 이미지 번호 목록")
    mapping_options: list[V1MappingOption] | None = Field(None, description="매핑 옵션 목록")
    edit_mapping_options: bool = Field(..., description="매핑 옵션 수정 여부")
    standard_option: bool = Field(..., description="단독형 여부")
    forced_sold_out: bool = Field(..., description="임시품절 여부")
    option_select_type: str = Field(..., description="옵션 선택 방식")
    is_required_option: bool = Field(..., description="필수 옵션 여부")
    edit: bool = Field(..., description="수정 여부")
    represent_yn: str = Field(..., description="대표 여부")


class ProductDetailV1Response(BaseDto):
    """
    상품 상세 조회하기 (Version 1.0) 응답 모델

    OpenAPI Schema: products-mallProductNo80080068
    """

    mall_product: V1MallProduct = Field(..., description="상품 정보")
    mall_product_images: list[V1MallProductImage] = Field(default_factory=list, description="상품 이미지 목록")
    mall_product_inputs: list[V1MallProductInput] = Field(default_factory=list, description="구매자 작성형 정보")
    mall_product_option_web_models: list[V1MallProductOption] = Field(
        default_factory=list, description="상품 옵션 목록"
    )

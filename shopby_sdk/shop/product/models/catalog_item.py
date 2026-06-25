"""shop 상품 카탈로그 공통 아이템 모델.

`/products/search`, `/products/best-review|best-seller/search`,
`/products/search-by-nos`, `/products/bundle-shipping`, 기획전/진열 상품 목록 등
**여러 엔드포인트가 공유하는 상품 표현**을 실데이터 기반으로 타입화한 것.

엔드포인트마다 노출 필드가 조금씩 달라(flat 필드 vs `baseInfo/price/status` 중첩)
모든 필드를 Optional 로 둔다(합집합). BaseDto 는 정의되지 않은 추가 필드를 무시하므로
진열/기획전 등 약간 다른 변형도 안전하게 수용한다.
"""

from __future__ import annotations

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDate, KstDatetime


class ImageUrlInfo(BaseDto):
    """이미지 URL 정보 (url/type)."""

    url: str | None = None
    type: str | None = Field(None, description="예: IMAGE_URL, VIDEO_URL")
    is_main: bool | None = Field(None, description="대표 이미지 여부(진열/기획전 상품)")


class StickerInfo(BaseDto):
    """상품 스티커 정보."""

    no: int | None = None
    type: str | None = Field(None, description="예: TEXT, IMAGE")
    label: str | None = None
    name: str | None = None


class HasCoupons(BaseDto):
    """쿠폰 존재 여부(대상 유형별)."""

    product: bool | None = None
    brand: bool | None = None
    category: bool | None = None
    partner: bool | None = None
    event: bool | None = None


class ItemAccumulationInfo(BaseDto):
    """적립 정보."""

    amount: float | None = None
    reward_rate_of_product: float | None = None
    reward_rate_of_member_benefit: float | None = None


class AccumulationLimitInfo(BaseDto):
    """적립금 사용 한도 정보(unitType/limitValue)."""

    unit_type: str | None = Field(None, description="PERCENT/WON")
    limit_value: float | None = None


class ItemAccumulationUseInfo(BaseDto):
    """적립금 사용 정보."""

    usable: bool | None = None
    accumulation_info: AccumulationLimitInfo | None = Field(None, description="적립 한도 정보")


class UnitPrice(BaseDto):
    """단위가격 정보."""

    type: str | None = Field(None, description="단위 (예: 개)")
    price: float | None = None
    name: str | None = None


class DeliveryConditionInfo(BaseDto):
    """배송 조건 요약 정보."""

    summary: str | None = Field(None, description="예: 무료배송")
    delivery_fee_ranges: list | None = None
    criteria: float | None = None
    range_summaries: list | None = None
    per_order_cnt: int | None = None


class ItemPrice(BaseDto):
    """상품 가격 정보(search-by-nos 등의 price 중첩 객체)."""

    sale_price: float | None = None
    immediate_discount_amt: float | None = None
    immediate_discount_unit_type: str | None = Field(None, description="WON/RATE")
    immediate_discount_start_ymdt: KstDatetime | None = None
    immediate_discount_end_ymdt: KstDatetime | None = None
    addition_discount_amt: float | None = None
    addition_discount_unit_type: str | None = Field(None, description="WON/RATE")
    addition_discount_value: float | None = None
    min_sale_price: float | None = None
    max_sale_price: float | None = None
    max_addition_discount_amt: float | None = None
    max_discount_amount: float | None = None
    unit_name: str | None = None
    unit_name_type: str | None = None
    unit_price: UnitPrice | None = None


class ItemStatus(BaseDto):
    """상품 상태 정보."""

    sale_status_type: str | None = Field(None, description="ONSALE/STOP 등")
    soldout: bool | None = None
    display: bool | None = None
    product_class_type: str | None = Field(None, description="DEFAULT 등")


class ReservationData(BaseDto):
    """예약판매 정보(reservationData).

    상품 목록 아이템과 상품 상세가 공유. 미설정(예약상품 아님) 시 전체가 null.
    """

    reservation_start_ymdt: KstDatetime | None = Field(None, description="예약판매 시작일")
    reservation_end_ymdt: KstDatetime | None = Field(None, description="예약판매 종료일")
    reservation_delivery_ymdt: KstDatetime | None = Field(None, description="예약판매 배송시작일")
    reservation_stock_cnt: int | None = Field(None, description="예약판매 재고수량")


class ItemBaseInfo(BaseDto):
    """search-by-nos 등에서 내려오는 baseInfo 중첩 객체(상품 기본정보)."""

    product_no: int | None = None
    sale_start_ymdt: KstDatetime | None = None
    sale_end_ymdt: KstDatetime | None = None
    sale_period_type: str | None = None
    register_ymdt: KstDatetime | None = None
    product_name: str | None = None
    product_name_en: str | None = None
    image_urls: list[str] | None = None
    review_rating: float | None = None
    total_review_count: int | None = None
    product_type: str | None = None
    partner_name: str | None = None
    promotion_text: str | None = None
    liked: bool | None = None
    like_count: int | None = None
    sale_cnt: int | None = None
    stock_cnt: int | None = None
    main_stock_cnt: int | None = None
    brand_no: int | None = None
    brand_name: str | None = None
    brand_name_ko: str | None = None
    brand_name_en: str | None = None
    brand_name_type: str | None = None
    sticker_infos: list[StickerInfo] | None = None
    sticker_labels: list[str] | None = None
    adult: bool | None = None
    reservation_data: ReservationData | None = None
    list_image_urls: list[str] | None = None
    has_coupons: HasCoupons | None = None
    max_coupon_amt: float | None = None
    coupon_discount_amt: float | None = None
    coupon_discount_unit_type: str | None = None
    contents_if_pausing: str | None = None
    display_category_nos: str | None = None
    url_direct_display_yn: bool | None = None
    product_management_cd: str | None = None
    hs_code: str | None = None
    group_management_code: str | None = None
    group_management_code_name: str | None = None
    accumulation_info: ItemAccumulationInfo | None = None
    accumulation_use_info: ItemAccumulationUseInfo | None = None
    accumulation_amt_when_buy_confirm: float | None = None
    can_add_to_cart: bool | None = None
    image_url_info: list[ImageUrlInfo] | None = None
    list_image_url_info: ImageUrlInfo | list[ImageUrlInfo] | None = None
    rental_infos: list | None = None
    enable_coupons: bool | None = None
    main_best_product_yn: bool | None = None
    coupon_tag: str | None = None


class ShopProductItem(BaseDto):
    """shop 상품 목록/검색/진열 공통 상품 아이템 (실데이터 합집합, 전부 Optional).

    OpenAPI schema 들(products-search*/search-by-nos/best-*/bundle-shipping/event·section
    products)에서 공유되는 상품 표현. 엔드포인트별 노출 필드 차이를 합집합으로 흡수한다.
    """

    product_no: int | None = None
    product_name: str | None = None
    product_name_en: str | None = None
    product_management_cd: str | None = None
    product_type: str | None = Field(None, description="DEFAULT 등")
    sale_status_type: str | None = Field(None, description="ONSALE 등")
    sale_period_type: str | None = None
    product_sale_period_type: str | None = None
    sale_start_ymdt: KstDatetime | None = None
    sale_end_ymdt: KstDatetime | None = None
    register_ymdt: KstDatetime | None = None
    expiration_date: KstDate | None = None

    # 브랜드/파트너
    brand_no: int | None = None
    brand_name: str | None = None
    brand_name_ko: str | None = None
    brand_name_en: str | None = None
    brand_name_type: str | None = None
    partner_no: int | None = None
    partner_name: str | None = None

    # 가격/할인
    sale_price: float | None = None
    min_sale_price: float | None = None
    max_sale_price: float | None = None
    immediate_discount_amt: float | None = None
    immediate_discount_unit_type: str | None = None
    immediate_discount_start_ymdt: KstDatetime | None = None
    immediate_discount_end_ymdt: KstDatetime | None = None
    addition_discount_amt: float | None = None
    addition_discount_unit_type: str | None = None
    max_discount_amount: float | None = None
    unit_price: UnitPrice | None = None

    # 쿠폰
    coupon_discount_amt: float | None = None
    coupon_discount_unit_type: str | None = None
    max_coupon_amt: float | None = None
    has_coupons: HasCoupons | None = None
    enable_coupons: bool | None = None
    coupon_tag: str | None = None

    # 재고/판매
    stock_cnt: int | None = None
    main_stock_cnt: int | None = None
    sale_cnt: int | None = None
    is_sold_out: bool | None = None
    can_add_to_cart: bool | None = None

    # 리뷰/좋아요
    review_rating: float | None = None
    total_review_count: int | None = None
    recent_review_cnt: int | None = None
    recent_review_rating: float | None = None
    recent_review_no: int | None = None
    review_content: str | None = None
    liked: bool | None = None
    like_count: int | None = None

    # 적립
    accumulation_info: ItemAccumulationInfo | None = None
    accumulation_use_info: ItemAccumulationUseInfo | None = None
    accumulation_amt_when_buy_confirm: float | None = None

    # 이미지
    image_urls: list[str] | None = None
    list_image_urls: list[str] | None = None
    image_url_info: list[ImageUrlInfo] | None = None
    list_image_url_info: ImageUrlInfo | list[ImageUrlInfo] | None = None

    # 스티커
    sticker_infos: list[StickerInfo] | None = None
    sticker_labels: list[str] | None = None

    # 배송
    shipping_area: str | None = Field(None, description="MALL_SHIPPING_AREA 등")
    delivery_condition_type: str | None = None
    delivery_condition_info: DeliveryConditionInfo | None = None

    # 전시/카테고리/그룹
    display_category_nos: str | None = None
    front_display_yn: bool | None = None
    url_direct_display_yn: bool | None = None
    main_best_product_yn: bool | None = None
    section_product_start_ymdt: KstDatetime | None = None
    section_product_end_ymdt: KstDatetime | None = None
    group_management_code: str | None = None
    group_management_code_name: str | None = None
    custom_properties: list | None = None

    # 기타
    promotion_text: str | None = None
    contents_if_pausing: str | None = None
    hs_code: str | None = None
    adult: bool | None = None
    reservation_data: ReservationData | None = None
    rental_infos: list | None = None
    option_values: list | None = None
    search_product_id: str | None = None
    sticker_no: int | None = None

    # search-by-nos 등 중첩 변형
    base_info: ItemBaseInfo | None = None
    price: ItemPrice | None = None
    status: ItemStatus | None = None

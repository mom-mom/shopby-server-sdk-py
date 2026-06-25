"""상품 상세(Product Detail) 모델.

대응 OpenAPI schema: products-productNo318672107.

상품 상세는 baseInfo/price/stock/brand/deliveryFee/limitations/status 등 깊게 중첩된
하위 객체로 구성된다. 실데이터(dev+prod) + OpenAPI 스펙 정의 기반으로 각 하위 객체를
타입화했다(reservationData/deliveryDate/regularDelivery/partnerNotice 포함 — 실데이터는
항상 null 이지만 스펙에 스키마가 정의되어 있어 타입화).
"""

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime
from shopby_sdk.shop.product.models.catalog_item import ImageUrlInfo, ReservationData, StickerInfo
from shopby_sdk.shop.product.models.shipping import ReturnWarehouse, ShippingConfig


class AccumulationUseLimitInfo(BaseDto):
    """적립금 사용 한도 정보."""

    unit_type: str | None = Field(None, description="PERCENT/WON")
    limit_value: float | None = None


class ProductDetailBaseInfo(BaseDto):
    """상품 상세 기본정보(baseInfo)."""

    product_no: int | None = None
    sale_start_ymdt: KstDatetime | None = None
    sale_end_ymdt: KstDatetime | None = None
    sale_period_type: str | None = None
    register_ymdt: KstDatetime | None = None
    promotion_text: str | None = None
    product_name: str | None = None
    product_name_en: str | None = None
    image_urls: list[str] | None = None
    place_origin_label: str | None = None
    place_origin_etc_label: str | None = None
    manufacture_ymdt: KstDatetime | None = None
    expiration_ymdt: KstDatetime | None = None
    content_header: str | None = None
    content: str | None = Field(None, description="상품 상세 설명(HTML)")
    content_footer: str | None = None
    duty_info: str | None = Field(None, description="고시정보(JSON 문자열)")
    sticker_labels: list[str] | None = None
    sticker_infos: list[StickerInfo] | None = None
    option_image_viewable: bool | None = None
    product_management_cd: str | None = None
    purchase_guide: str | None = None
    accumulation_use_yn: str | None = Field(None, description="Y/N")
    accumulation_use_limit_info: AccumulationUseLimitInfo | None = None
    delivery_customer_info: str | None = None
    certification_type: str | None = Field(None, description="NOT_TARGET 등")
    certifications: list | None = None
    product_group: str | None = Field(None, description="SERVICE/GOODS 등")
    hs_code: str | None = None
    usable_restock_noti: bool | None = None
    product_type: str | None = None
    product_class_type: str | None = None
    mapping_type: str | None = Field(None, description="SINGLE/MULTI 등")
    custom_propertise: list | None = Field(None, description="(API 원문 오타 키) 상품 추가항목")
    custom_properties: list | None = None
    coupon_use_yn: str | None = Field(None, description="Y/N")
    minor_purchase_yn: str | None = Field(None, description="Y/N")
    url_direct_display_yn: str | None = Field(None, description="Y/N")
    image_url_info: list[ImageUrlInfo] | None = None
    payment_means: list | None = None


class ProductDetailStock(BaseDto):
    """재고 정보(stock)."""

    sale_cnt: int | None = None
    stock_cnt: int | None = None
    main_stock_cnt: int | None = None


class ProductDetailPrice(BaseDto):
    """가격 정보(price)."""

    sale_price: float | None = None
    immediate_discount_amt: float | None = None
    immediate_discount_unit_type: str | None = None
    immediate_discount_start_ymdt: KstDatetime | None = None
    immediate_discount_end_ymdt: KstDatetime | None = None
    addition_discount_amt: float | None = None
    addition_discount_unit_type: str | None = None
    addition_discount_value: float | None = None
    min_sale_price: float | None = None
    max_sale_price: float | None = None
    max_addition_discount_amt: float | None = None
    max_discount_amount: float | None = None
    unit_name: str | None = None
    unit_name_type: str | None = None
    unit_price: float | None = None
    unit_total_quantity: float | None = None
    unit_base_quantity: float | None = None
    max_coupon_amt: float | None = None
    coupon_discount_amt: float | None = None
    coupon_discount_unit_type: str | None = None
    accumulation_amt_when_buy_confirm: float | None = None
    accumulation_rate: float | None = None
    accumulation_rate_of_member: float | None = None
    photo_review_accumulation_amt: float | None = None
    contents_if_pausing: str | None = None


class ProductDetailDeliveryFee(BaseDto):
    """배송비 정보(deliveryFee)."""

    delivery_condition_type: str | None = Field(None, description="FREE/CONDITIONAL 등")
    delivery_amt: float | None = None
    above_delivery_amt: float | None = None
    return_delivery_amt: float | None = None
    delivery_type: str | None = Field(None, description="PARCEL_DELIVERY 등")
    delivery_company_type: str | None = None
    per_order_cnt: int | None = None
    default_delivery_condition_label: str | None = None
    delivery_amt_labels: str | None = None
    delivery_company_type_label: str | None = None
    delivery_condition_details: list | None = None
    remote_delivery_area_fees: list | None = None
    delivery_pre_payment: bool | None = None
    return_warehouse: ReturnWarehouse | None = Field(None, description="반품지 정보")
    delivery_customer_info: str | None = None
    total_weight: float | None = None
    delivery_template_name: str | None = None


class ProductDetailLimitations(BaseDto):
    """구매 제한 정보(limitations)."""

    min_buy_cnt: int | None = None
    max_buy_person_cnt: int | None = None
    max_buy_time_cnt: int | None = None
    max_buy_days: int | None = None
    max_buy_period_cnt: int | None = None
    member_only: bool | None = None
    can_add_to_cart: bool | None = None
    refundable: bool | None = None
    non_refund_types: list | None = None
    naver_pay_handling: bool | None = None


class ProductDetailCounter(BaseDto):
    """카운터 정보(counter)."""

    like_cnt: int | None = None
    review_cnt: int | None = None
    inquiry_cnt: int | None = None
    my_inquiry_cnt: int | None = None


class ProductDetailCategory(BaseDto):
    """카테고리 정보(categories[])."""

    full_category_label: str | None = None
    representative_yn: str | None = Field(None, description="Y/N")
    categories: list | None = Field(None, description="depth 별 카테고리 노드")


class ProductDetailBrand(BaseDto):
    """브랜드 정보(brand)."""

    brand_no: int | None = None
    name: str | None = None
    name_ko: str | None = None
    name_en: str | None = None
    name_type: str | None = None
    logo_image_url: str | None = None


class ProductDetailPartner(BaseDto):
    """파트너(판매자) 정보(partner)."""

    partner_no: int | None = None
    partner_name: str | None = None
    business_registration_no: str | None = None
    company_name: str | None = None
    online_marketing_business_declaration_no: str | None = None
    owner_name: str | None = None
    office_address_label: str | None = None
    phone_no: str | None = None
    fax_no: str | None = None
    email: str | None = None


class ProductDetailStatus(BaseDto):
    """상품 상태(status)."""

    sale_status_type: str | None = Field(None, description="ONSALE 등")
    soldout: bool | None = None
    display: bool | None = None
    product_class_type: str | None = None


class ProductDetailShippingInfo(BaseDto):
    """배송 정보(shippingInfo)."""

    shipping_available: bool | None = None
    shipping_config: ShippingConfig | None = None


class DeliveryDatePeriod(BaseDto):
    """배송일 기간(deliveryDate.period)."""

    start_ymdt: KstDatetime | None = None
    end_ymdt: KstDatetime | None = None


class ProductDeliveryDate(BaseDto):
    """상품 배송일 정보(deliveryDate)."""

    period: DeliveryDatePeriod | None = None
    days_of_week: str | None = Field(None, description='요일 (예: "[MON,TUE]")')
    days_after_purchase: int | None = Field(None, description="주문일 기준 배송 소요일")


class RegularDeliveryDiscountInfo(BaseDto):
    """정기결제 즉시 할인 정보(regularDelivery.discount)."""

    type: str | None = Field(None, description="AMOUNT(원)/PERCENT(%)")
    value: float | None = Field(None, description="즉시 할인 금액/율")


class ProductRegularDelivery(BaseDto):
    """정기 결제 정보(regularDelivery).

    이 값이 null 이면 정기결제 상품이 아님.
    """

    discount: RegularDeliveryDiscountInfo | None = None


class ProductPartnerNotice(BaseDto):
    """파트너사 공지(partnerNotice)."""

    title: str | None = None
    content: str | None = None


class ProductDetailResponse(BaseDto):
    """상품 상세 조회 응답 (OpenAPI: products-productNo318672107)."""

    # 타입화된 중첩 객체
    base_info: ProductDetailBaseInfo | None = None
    price: ProductDetailPrice | None = None
    stock: ProductDetailStock | None = None
    brand: ProductDetailBrand | None = None
    delivery_fee: ProductDetailDeliveryFee | None = None
    counter: ProductDetailCounter | None = None
    partner: ProductDetailPartner | None = None
    limitations: ProductDetailLimitations | None = None
    status: ProductDetailStatus | None = None
    shipping_info: ProductDetailShippingInfo | None = None
    categories: list[ProductDetailCategory] | None = None

    # 스펙 정의 기반 타입화 (실데이터는 항상 null 이나 스펙에 스키마 존재)
    delivery_date: ProductDeliveryDate | None = Field(None, description="배송 예정일 정보(미설정 시 null)")
    regular_delivery: ProductRegularDelivery | None = Field(None, description="정기배송 정보(미설정 시 null)")
    partner_notice: ProductPartnerNotice | None = Field(None, description="파트너 공지(미설정 시 null)")
    reservation_data: ReservationData | None = Field(None, description="예약판매 정보(미설정 시 null)")
    rental_infos: list | None = None
    related_product_nos: list[int] | None = None

    # 스칼라/가이드 필드
    group_management_code: str | None = None
    group_management_code_name: str | None = None
    sale_method_type: str | None = Field(None, description="PURCHASE/CONSIGNMENT 등")
    delivery_guide: str | None = None
    exchange_guide: str | None = None
    refund_guide: str | None = None
    after_service_guide: str | None = None
    liquor_delegation_guide: str | None = None
    review_available: bool | None = None
    review_rate: float | None = None
    liked: bool | None = None
    main_best_product_yn: bool | None = None
    displayable_stock: bool | None = None

"""정기 결제(Regular/Recurring Delivery) 상품 모델.

대응 OpenAPI schema:
- products-regular-delivery-1597014301 (변경 가능한 정기 결제 상품 목록)
- products-regular-delivery-search243194228 (상품번호 리스트 정기결제 조회)
"""

from shopby_sdk.base.dto import BaseDto


class RegularDeliveryProductView(BaseDto):
    """정기 결제 상품 뷰.

    OpenAPI: products-regular-delivery-1597014301 recurringDeliveryProductViews[]
    """

    product_no: int | None = None
    product_name: str | None = None
    image_url: str | None = None
    display_category_no: int | None = None
    sale_status: str | None = None
    sale_price: int | None = None
    discounted_price: int | None = None
    immediate_discount_type: str | None = None
    immediate_discount_amount: int | None = None
    applied_immediate_discount_price: int | None = None
    is_sold_out: bool | None = None
    option_yn: str | None = None
    delivery_cycle_types: list[str] | None = None
    day_of_week_cycles: list[str] | None = None
    week_delivery_cycles: list[int] | None = None
    month_delivery_cycles: list[int] | None = None


class RegularDeliveryListResponse(BaseDto):
    """변경 가능한 정기 결제 상품 조회 응답.

    OpenAPI: products-regular-delivery-1597014301
    """

    recurring_delivery_product_views: list[RegularDeliveryProductView] | None = None
    total_count: int | None = None
    total_page: int | None = None


class RegularDeliveryDiscount(BaseDto):
    """정기결제 할인 정보."""

    type: str | None = None
    value: int | None = None


class RegularDeliverySearchItem(BaseDto):
    """상품번호 리스트로 조회한 정기 결제 상품.

    OpenAPI: products-regular-delivery-search243194228 item
    """

    product_no: int | None = None
    mall_no: int | None = None
    discounted_price: int | None = None
    discount: RegularDeliveryDiscount | None = None

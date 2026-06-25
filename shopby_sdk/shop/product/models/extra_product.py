"""추가상품(Extra Products) 모델.

대응 OpenAPI schema: products-productNo-extra-products-267375444.
extraProducts[] 항목(price/optionInfo(multiOptions/flatOptions/inputs)/limitations 등)을
OpenAPI 스펙 정의 기반으로 타입화한다.
"""

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime
from shopby_sdk.shop.product.models.detail import ProductDetailLimitations


class ExtraProductDiscountInfo(BaseDto):
    """즉시/추가 할인 정보(price.immediateDiscountInfo / additionalDiscountInfo)."""

    discount_amt: float | None = None
    start_date_time: KstDatetime | None = None
    end_date_time: KstDatetime | None = None


class ExtraProductCouponDiscountInfo(BaseDto):
    """쿠폰 할인 정보(price.couponDiscountInfo)."""

    max_coupon_amt: float | None = None
    coupon_discount_amt: float | None = None


class ExtraProductPrice(BaseDto):
    """추가상품 가격 정보(price)."""

    sale_price: float | None = None
    immediate_discount_info: ExtraProductDiscountInfo | None = None
    coupon_discount_info: ExtraProductCouponDiscountInfo | None = None
    additional_discount_info: ExtraProductDiscountInfo | None = None


class ExtraProductOptionChild(BaseDto):
    """추가상품 조합형 옵션 하위 값(multiOptions[].children[])."""

    option_no: int | None = None
    option_name: str | None = None
    option_value: str | None = None
    buy_price: float | None = None
    add_price: float | None = None
    stock_cnt: int | None = None
    reservation_stock_cnt: int | None = None
    sale_type: str | None = None
    is_required_option: bool | None = None
    forced_sold_out: bool | None = None
    extra_management_cd: str | None = None


class ExtraProductMultiOption(BaseDto):
    """추가상품 조합형 옵션(multiOptions[])."""

    option_name: str | None = None
    option_value: str | None = None
    is_required_option: bool | None = None
    children: list[ExtraProductOptionChild] | None = None


class ExtraProductInput(BaseDto):
    """추가상품 작성형 옵션(inputs[])."""

    input_no: int | None = None
    input_label: str | None = None
    input_matching_type: str | None = None
    required: bool | None = None


class ExtraProductOptionInfo(BaseDto):
    """추가상품 옵션 정보(optionInfo)."""

    option_type: str | None = None
    option_select_type: str | None = None
    multi_options: list[ExtraProductMultiOption] | None = None
    # flatOptions 는 children 없는 단층 옵션 (children 외 동일 필드)
    flat_options: list[ExtraProductOptionChild] | None = None
    inputs: list[ExtraProductInput] | None = None


class ExtraProductItem(BaseDto):
    """추가상품 항목(extraProducts[])."""

    product_no: int | None = None
    product_name: str | None = None
    image_url: str | None = None
    payment_means: str | None = Field(None, description="결제수단 (CREDIT/PAYCO 등)")
    minor_purchase_yn: str | None = Field(None, description="Y/N")
    displayable_stock: bool | None = None
    price: ExtraProductPrice | None = None
    option_info: ExtraProductOptionInfo | None = None
    limitations: ProductDetailLimitations | None = None


class ExtraProductsResponse(BaseDto):
    """추가상품 조회 응답.

    OpenAPI: products-productNo-extra-products-267375444.
    """

    extra_product_title: str | None = None
    extra_products: list[ExtraProductItem] | None = None

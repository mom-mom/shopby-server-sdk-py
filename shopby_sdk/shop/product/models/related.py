"""관련 상품(Related Products) 모델.

대응 OpenAPI schema: products-productNo-related-products793389923
"""

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class RelatedProductCustomProperty(BaseDto):
    """관련 상품 커스텀 속성."""

    prop_no: int | None = None
    prop_name: str | None = None
    prop_value_no: int | None = None
    prop_value: str | None = None
    prop_type: str | None = None
    multiple_selection_yn: str | None = None


class RelatedProductSticker(BaseDto):
    """관련 상품 스티커."""

    type: str | None = None
    name: str | None = None
    label: str | None = None


class RelatedProductItem(BaseDto):
    """관련 상품 항목.

    OpenAPI: products-productNo-related-products793389923 item
    """

    product_no: int | None = None
    product_name: str | None = None
    product_name_en: str | None = None
    image_url: str | None = None
    image_url_type: str | None = None
    sale_price: int | None = None
    immediate_discount_amt: int | None = None
    immediate_discount_unit_type: str | None = None
    immediate_discount_start_ymdt: KstDatetime | None = None
    immediate_discount_end_ymdt: KstDatetime | None = None
    additional_discount_amt: int | None = None
    additional_discount_unit_type: str | None = None
    review_rating: float | None = None
    total_review_count: int | None = None
    like_count: int | None = None
    liked: bool | None = None
    can_add_to_cart: bool | None = None
    requires_age_verification: bool | None = None
    contents_if_pausing: str | None = None
    display_category_nos: list[int] | None = None
    custom_properties: list[RelatedProductCustomProperty] | None = None
    stickers: list[RelatedProductSticker] | None = None

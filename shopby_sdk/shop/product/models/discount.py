"""추가할인(Additional Discount) 관련 모델.

대응 OpenAPI schema:
- additional-discounts-by-product-no-812009938
- additional-discounts-by-product-nos-527021542
"""

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class QuantityDiscountInfo(BaseDto):
    """구매수량할인 정보."""

    sort_no: int | None = None
    min_quantity: int | None = None
    max_quantity: int | None = None
    is_fixed_discount: bool | None = None
    discount_amount: int | None = None
    discount_rate: float | None = None
    max_discount_amount: int | None = None


class MemberDiscountInfo(BaseDto):
    """회원할인 정보."""

    sort_no: int | None = None
    member_group_target_type: str | None = None
    member_grade_target_type: str | None = None
    member_group_nos: list[int] | None = None
    member_grade_nos: list[int] | None = None
    is_fixed_discount: bool | None = None
    discount_amount: int | None = None
    discount_rate: float | None = None
    max_discount_amount: int | None = None


class AdditionalDiscountResponse(BaseDto):
    """추가할인 정보 (단건).

    OpenAPI: additional-discounts-by-product-no-812009938
    """

    product_no: int | None = None
    discount_no: int | None = None
    discount_name: str | None = None
    min_sale_price: int | None = None
    max_sale_price: int | None = None
    is_fixed_discount: bool | None = None
    discount_amount: int | None = None
    discount_rate: float | None = None
    max_discount_amount: int | None = None
    is_quantity_discount: bool | None = None
    start_date_time: KstDatetime | None = None
    end_date_time: KstDatetime | None = None
    quantity_discount_infos: list[QuantityDiscountInfo] | None = None
    is_member_discount: bool | None = None
    member_discount_infos: list[MemberDiscountInfo] | None = None


class AdditionalDiscountsResponse(BaseDto):
    """추가할인 정보 다건 조회 응답.

    OpenAPI: additional-discounts-by-product-nos-527021542
    """

    data: list[AdditionalDiscountResponse] | None = None

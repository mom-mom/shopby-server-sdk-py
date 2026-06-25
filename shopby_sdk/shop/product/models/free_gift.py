"""사은품(Free Gift) 지급조건 모델.

대응 OpenAPI schema: free-gift-condition-order-amount654441236
(주문금액기준 / 상품금액기준 동일 응답 스키마)
"""

from typing import Literal

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime

FreeGiftLimitedMemberType = Literal["ALL", "MEMBER", "TARGET"]
FreeGiftOptionCountType = Literal["ALL", "SELECT"]


class FreeGiftItem(BaseDto):
    """사은품 옵션 정보."""

    product_no: int | None = None
    product_name: str | None = None
    option_no: int | None = None
    option_name: str | None = None
    option_value: str | None = None
    image_url: str | None = None


class FreeGiftLimitedMember(BaseDto):
    """사은품 지급 대상 회원 제한 정보."""

    member_grade: list[int] | None = None
    member_group: list[int] | None = None


class FreeGiftCondition(BaseDto):
    """사은품 지급조건."""

    give_condition_no: int | None = None
    give_condition_name: str | None = None
    give_condition_explain: str | None = None
    give_start_date_time: KstDatetime | None = None
    give_end_date_time: KstDatetime | None = None
    upper_price: int | None = None
    free_gift_option_count: int | None = None
    free_gift_option_count_type: FreeGiftOptionCountType | None = None
    limited_member_type: FreeGiftLimitedMemberType | None = None
    limited_member: FreeGiftLimitedMember | None = None
    free_gifts: list[FreeGiftItem] | None = None


class FreeGiftConditionResponse(BaseDto):
    """사은품 지급가능 조건 조회 응답.

    OpenAPI: free-gift-condition-order-amount654441236
    """

    free_gift_conditions: list[FreeGiftCondition] | None = None
    total_count: int | None = None

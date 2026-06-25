"""상품 변경 히스토리 조회 응답 모델"""

from typing import Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class ProductHistoryItem(BaseDto):
    """
    상품 변경 히스토리 아이템

    OpenAPI Schema: products-productNo-histories-2022409867 > items
    """

    modified_date: KstDatetime = Field(..., description="변경일")
    apply_status_type: Literal[
        "REGISTRATION_READY",
        "APPROVAL_READY",
        "APPROVAL_REJECTION",
        "SALE_AGREEMENT_READY",
        "SALE_AGREEMENT_REJECTION",
        "FINISHED",
        "AFTER_APPROVAL_READY",
        "AFTER_APPROVAL_REJECTION",
    ] = Field(..., description="승인상태")
    sale_status_type: Literal[
        "READY",
        "ONSALE",
        "FINISHED",
        "STOP",
        "PROHIBITION",
        "RESERVATION_ONSALE",
        "RESERVATION_FINISHED",
    ] = Field(..., description="판매상태")
    sale_setting_status_type: Literal[
        "AVAILABLE_FOR_SALE",
        "STOP_SELLING",
        "PROHIBITION_SALE",
    ] = Field(..., description="판매설정")
    admin_name: str = Field(..., description="요청 담당자")
    confirm_admin_name: str = Field(..., description="처리 담당자")
    # 운영데이터(717개 히스토리 모두 문자열 배열) → list[str]
    change_properties: list[str] = Field(default_factory=list, description="변경내역 (변경된 항목명 목록)")


# Response is a list of ProductHistoryItem
ProductHistoriesResponse = list[ProductHistoryItem]

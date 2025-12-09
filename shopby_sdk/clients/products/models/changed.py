"""변경된 상품 번호 목록 조회 응답 모델"""

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class ChangedProductItem(BaseDto):
    """
    변경된 상품 아이템

    OpenAPI Schema: products-changed-756650823 > contents
    """

    product_no: int = Field(..., description="상품 번호")
    mall_product_no: int = Field(..., description="몰 상품 번호")
    registered_at: KstDatetime = Field(..., description="등록일")
    updated_at: KstDatetime | None = Field(None, description="수정일")


class ChangedProductsResponse(BaseDto):
    """
    변경된 상품 번호 목록 조회 응답 모델

    OpenAPI Schema: products-changed-756650823
    """

    total_count: int = Field(..., description="전체 상품수")
    total_page: int = Field(..., description="전체 페이지수")
    last_id: str = Field(..., description="검색 기준 값")
    items: list[ChangedProductItem] = Field(default_factory=list, description="변경된 상품 목록")

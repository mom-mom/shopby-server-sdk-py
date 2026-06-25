"""상품 진열(ProductSection) 모델."""

from __future__ import annotations

from typing import Any

from shopby_sdk.base.dto import BaseDto


class SectionSummary(BaseDto):
    """상품 진열 요약 (schema: display-sections129922044 sections[])."""

    section_no: int | None = None
    section_id: str | None = None
    section_name: str | None = None
    section_explain: str | None = None
    promotion_text: str | None = None
    image_url: str | None = None
    left_space_color: str | None = None
    right_space_color: str | None = None


class SectionListResponse(BaseDto):
    """상품 진열 리스트 조회 응답 (schema: display-sections129922044)."""

    sections: list[SectionSummary] | None = None


class SectionResponse(BaseDto):
    """단일 상품 진열 조회 응답 (schema: display-sections-sectionNo1428912410)."""

    section_no: int | None = None
    label: str | None = None
    section_explain: str | None = None
    promotion_text: str | None = None
    image_url: str | None = None
    left_space_color: str | None = None
    right_space_color: str | None = None


class SectionProductsResponse(BaseDto):
    """상품 진열 내 상품 상세 조회 응답 (schema: display-sections-sectionNo-products).

    products[] 는 전시 상품 카탈로그의 거대 중첩 페이로드(50+ 필드)라 ``dict[str, Any]`` 로 둔다.
    """

    product_total_count: int | None = None
    displayable_stock: bool | None = None
    products: list[dict[str, Any]] | None = None

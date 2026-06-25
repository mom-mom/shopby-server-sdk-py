"""상품 진열(ProductSection) 모델."""

from __future__ import annotations


from shopby_sdk.base.dto import BaseDto
from shopby_sdk.shop.product.models.catalog_item import ShopProductItem


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

    products[] 는 product 도메인과 공유하는 상품 카탈로그 표현(ShopProductItem).
    """

    product_total_count: int | None = None
    displayable_stock: bool | None = None
    products: list[ShopProductItem] | None = None

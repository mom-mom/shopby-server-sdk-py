"""상품 검색 결과 Summary(집계) 모델.

대응 OpenAPI schema: products-search-summary1814999444.
브랜드/카테고리/커스텀속성 집계는 묶음배송 응답에서도 재사용된다.
"""

from typing import Any

from shopby_sdk.base.dto import BaseDto


class BrandSummary(BaseDto):
    """검색결과 브랜드 집계."""

    brand_no: int | None = None
    brand_name: str | None = None
    brand_name_ko: str | None = None
    brand_name_en: str | None = None
    brand_name_type: str | None = None
    count: int | None = None


class CategorySummary(BaseDto):
    """검색결과 카테고리 집계 (depth별)."""

    category_no: int | None = None
    parent_category_no: int | None = None
    label: str | None = None
    display_order: int | None = None
    count: int | None = None


class MultiLevelCategorySummary(BaseDto):
    """다단계 카테고리 집계 (자기참조).

    childCategories 는 동일 구조의 재귀라 dict[str, Any] 로 둔다.
    """

    category_no: int | None = None
    parent_category_no: int | None = None
    label: str | None = None
    display_order: int | None = None
    count: int | None = None
    child_categories: list[dict[str, Any]] | None = None


class CustomPropertyValueSummary(BaseDto):
    """커스텀 속성 값 집계."""

    prop_value_no: int | None = None
    prop_value: str | None = None


class CustomPropertySummary(BaseDto):
    """커스텀 속성 집계."""

    prop_no: int | None = None
    prop_name: str | None = None
    prop_type: str | None = None
    prop_values: list[CustomPropertyValueSummary] | None = None


class SearchSummaryResponse(BaseDto):
    """상품 검색 결과 Summary 정보 조회 응답.

    OpenAPI: products-search-summary1814999444
    """

    total_count: int | None = None
    min_price: int | None = None
    max_price: int | None = None
    displayable_stock: bool | None = None
    corrected_keyword: str | None = None
    click_url_prefix: dict[str, Any] | None = None
    brands: list[BrandSummary] | None = None
    custom_properties: list[CustomPropertySummary] | None = None
    depth1_categories: list[CategorySummary] | None = None
    depth2_categories: list[CategorySummary] | None = None
    depth3_categories: list[CategorySummary] | None = None
    depth4_categories: list[CategorySummary] | None = None
    depth5_categories: list[CategorySummary] | None = None
    multi_level_categories: list[MultiLevelCategorySummary] | None = None

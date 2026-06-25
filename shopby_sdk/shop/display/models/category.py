"""카테고리(Category) 모델."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto

CategoryViewType = Literal["ALL", "MULTI_LEVEL", "FLAT"]


class MultiLevelCategory(BaseDto):
    """트리 구조 카테고리 노드 (multiLevelCategories[])."""

    category_no: int | None = None
    label: str | None = None
    depth: int | None = None
    icon: str | None = None
    content: str | None = None
    management_code: str | None = None
    children: list["MultiLevelCategory"] | None = None


class FlatCategory(BaseDto):
    """평탄화 카테고리 (flatCategories[]) - 최대 5depth 컬럼이 평탄하게 펼쳐진 구조."""

    full_category_name: str | None = None
    depth1_category_no: int | None = None
    depth1_label: str | None = None
    depth1_display_order: int | None = None
    depth1_icon: str | None = None
    depth1_content: str | None = None
    depth1_management_code: str | None = None
    depth2_category_no: int | None = None
    depth2_label: str | None = None
    depth2_display_order: int | None = None
    depth2_icon: str | None = None
    depth2_content: str | None = None
    depth2_management_code: str | None = None
    depth3_category_no: int | None = None
    depth3_label: str | None = None
    depth3_display_order: int | None = None
    depth3_icon: str | None = None
    depth3_content: str | None = None
    depth3_management_code: str | None = None
    depth4_category_no: int | None = None
    depth4_label: str | None = None
    depth4_display_order: int | None = None
    depth4_icon: str | None = None
    depth4_content: str | None = None
    depth4_management_code: str | None = None
    depth5_category_no: int | None = None
    depth5_label: str | None = None
    depth5_display_order: int | None = None
    depth5_icon: str | None = None
    depth5_content: str | None = None
    depth5_management_code: str | None = None


class CategoryBrand(BaseDto):
    """카테고리 내 브랜드 정보."""

    brand_no: int | None = None
    name: str | None = None
    product_cnt: int | None = None


class CategoriesResponse(BaseDto):
    """전체 카테고리 조회 응답 (schema: categories-238649777)."""

    multi_level_categories: list[MultiLevelCategory] | None = None
    flat_categories: list[FlatCategory] | None = None


class CategoryResponse(BaseDto):
    """카테고리 번호 단건 조회 응답 (schema: categories-categoryNo-675990724)."""

    multi_level_categories: list[MultiLevelCategory] | None = None
    flat_categories: list[FlatCategory] | None = None
    brands: list[CategoryBrand] | None = None
    requested_category_no: int | None = None


class SimpleCategory(BaseDto):
    """1차 카테고리 간단 정보 (schema: categories-simple-1depth1374229175[])."""

    display_category_no: int | None = None
    display_category_name: str | None = None
    display_management_code: str | None = None


class CategoryDisplaySetting(BaseDto):
    """카테고리 진열 설정 (schema: categories-categoryNo-display-setting)."""

    display_type: Literal["AUTO", "MANUAL"] | str | None = None
    pin_enabled: Literal["Y", "N"] | str | None = None


class CategoryNosByCodesRequest(BaseDto):
    """관리코드로 카테고리 번호 조회 요청 (schema: categories-search-by-management-code1690049551)."""

    codes: list[str] = Field(..., description="전시카테고리 관리코드 목록")


class CategoryNoByCode(BaseDto):
    """관리코드 -> 카테고리 번호 매핑 (schema: categories-search-by-management-code1438015983[])."""

    display_category_no: int | None = None
    code: str | None = None

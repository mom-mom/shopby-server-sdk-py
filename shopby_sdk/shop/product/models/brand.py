"""브랜드(Brand) 관련 모델.

대응 OpenAPI schema:
- display-brands-764911083 (브랜드 목록 - 상품 색인 기준)
- display-brands-extraInfo-1018337533 (브랜드 추가정보)
- display-brands-search-860864492 (브랜드 색인 기준 검색)
- display-brands-search-by-nos-460729423 (브랜드번호로 조회)
- display-brands-tree-1949059840 (브랜드 트리)
- display-brands-displayBrandNo-1536879905 (브랜드 상세)
- display-brands-displayBrandNo-children124042645 (자식 브랜드)
"""

from typing import Literal

from shopby_sdk.base.dto import BaseDto

BrandNameType = Literal["NAME_KO", "NAME_EN", "NONE"]


class BrandItem(BaseDto):
    """브랜드 목록 항목 (상품 색인 기준).

    OpenAPI: display-brands-764911083 items
    """

    brand_no: int | None = None
    display_brand_no: int | None = None
    name_type: BrandNameType | None = None
    main_brand_name: str | None = None
    sub_brand_name: str | None = None
    description: str | None = None
    display_area_content_url: str | None = None


class BrandListResponse(BaseDto):
    """브랜드 목록 조회 응답.

    OpenAPI: display-brands-764911083
    """

    items: list[BrandItem] | None = None
    total_count: int | None = None


class BrandExtraInfoItem(BaseDto):
    """브랜드 추가정보 항목.

    OpenAPI: display-brands-extraInfo-1018337533 item
    """

    display_brand_no: int | None = None
    extra_info: str | None = None


class BrandSearchItem(BaseDto):
    """브랜드 검색 항목 (브랜드 색인 기준).

    OpenAPI: display-brands-search-860864492 item
    """

    brand_no: int | None = None
    main_brand_name: str | None = None


class BrandByNoItem(BaseDto):
    """브랜드번호로 조회한 브랜드 정보.

    OpenAPI: display-brands-search-by-nos-460729423 brands[]
    """

    display_brand_no: int | None = None
    parent_no: int | None = None
    depth: int | None = None
    main_brand_name: str | None = None
    sub_brand_name: str | None = None
    display_area_content_url: str | None = None
    extra_info: str | None = None


class BrandsByNoResponse(BaseDto):
    """브랜드번호 리스트로 브랜드정보 조회 응답.

    OpenAPI: display-brands-search-by-nos-460729423
    """

    brands: list[BrandByNoItem] | None = None


class BrandTreeItem(BaseDto):
    """브랜드 트리 항목 (자기참조).

    OpenAPI: display-brands-tree-1949059840 item
    """

    no: int | None = None
    name: str | None = None
    depth: int | None = None
    children: list["BrandTreeItem"] | None = None


class BrandChildItem(BaseDto):
    """자식 브랜드 항목.

    OpenAPI: display-brands-displayBrandNo-children124042645 item
    """

    display_brand_no: int | None = None
    depth: int | None = None
    main_brand_name: str | None = None
    sub_brand_name: str | None = None
    display_area_content_url: str | None = None


class BrandDetailResponse(BaseDto):
    """브랜드 상세 조회 응답.

    OpenAPI: display-brands-displayBrandNo-1536879905
    """

    brand_no: int | None = None
    name_type: BrandNameType | None = None
    main_brand_name: str | None = None
    sub_brand_name: str | None = None
    description: str | None = None
    display_area_content_url: str | None = None
    extra_info: str | None = None

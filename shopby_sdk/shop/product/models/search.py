"""상품 검색/목록(Search & List) 응답 모델.

검색/베스트/묶음배송 응답의 상품 항목(`items[]`/`products[]`)은 엔드포인트마다 일부
필드가 다르지만 대부분 동일한 상품 표현이라, 실데이터(dev+prod) 합집합으로 타입화한
공통 모델 `ShopProductItem` 으로 받는다(전부 Optional, 추가 필드는 무시).

대응 OpenAPI schema:
- products-search-2030927223
- products-search-by-nos-787933423
- products-best-review-search-389327599
- products-best-seller-search670757123
- products-bundle-shipping-373153341
"""

from shopby_sdk.base.dto import BaseDto

from shopby_sdk.shop.product.models.catalog_item import ShopProductItem
from shopby_sdk.shop.product.models.summary import (
    BrandSummary,
    ClickUrlPrefix,
    CategorySummary,
    CustomPropertySummary,
    MultiLevelCategorySummary,
)


class ProductSearchResponse(BaseDto):
    """상품 검색(search engine) 응답.

    OpenAPI: products-search-2030927223.
    """

    items: list[ShopProductItem] | None = None
    total_count: int | None = None
    page_count: int | None = None
    corrected_keyword: str | None = None
    displayable_stock: bool | None = None
    click_url_prefix: ClickUrlPrefix | None = None


class ProductSearchByNosResponse(BaseDto):
    """상품번호 리스트로 상품 조회 응답.

    OpenAPI: products-search-by-nos-787933423.
    """

    products: list[ShopProductItem] | None = None
    invalid_products_nos: list[int] | None = None


class BestReviewSearchResponse(BaseDto):
    """베스트 리뷰 상품 검색 응답.

    OpenAPI: products-best-review-search-389327599.
    """

    items: list[ShopProductItem] | None = None
    total_count: int | None = None
    page_count: int | None = None
    displayable_stock: bool | None = None


class BestSellerSearchResponse(BaseDto):
    """베스트 셀러 상품 검색 응답.

    OpenAPI: products-best-seller-search670757123.
    """

    items: list[ShopProductItem] | None = None
    total_count: int | None = None
    page_count: int | None = None
    displayable_stock: bool | None = None


class BundleShippingResponse(BaseDto):
    """묶음 배송 상품 목록 조회 응답.

    OpenAPI: products-bundle-shipping-373153341.
    집계 필드도 타입화.
    """

    items: list[ShopProductItem] | None = None
    total_count: int | None = None
    page_count: int | None = None
    min_price: int | None = None
    max_price: int | None = None
    displayable_stock: bool | None = None
    brands: list[BrandSummary] | None = None
    depth1_categories: list[CategorySummary] | None = None
    depth2_categories: list[CategorySummary] | None = None
    depth3_categories: list[CategorySummary] | None = None
    depth4_categories: list[CategorySummary] | None = None
    multi_level_categories: list[MultiLevelCategorySummary] | None = None


class ProductSearchByNosRequest(BaseDto):
    """상품번호 리스트로 상품 조회 요청.

    OpenAPI: products-search-by-nos-2032023721
    """

    product_nos: list[int]
    has_option_values: bool | None = None


__all__ = [
    "ShopProductItem",
    "ClickUrlPrefix",
    "ProductSearchResponse",
    "ProductSearchByNosResponse",
    "ProductSearchByNosRequest",
    "BestReviewSearchResponse",
    "BestSellerSearchResponse",
    "BundleShippingResponse",
    "BrandSummary",
    "CategorySummary",
    "CustomPropertySummary",
    "MultiLevelCategorySummary",
]

"""상품 부가/카탈로그 정보 모델 (카테고리/추가정보/설정/항목/단축URL 등).

대응 OpenAPI schema:
- products-configuration-naver-shopping-293908981
- products-custom-properties-898470951
- products-extraInfo375807320
- products-productNo-display-categories-1237636422
- products-productNo-standard-category1365440212
- products-productNo-url-shortening-1808461975
- products-search-keywords226225576
- products-favoriteKeywords682143570 (응답: list[str])
"""

from shopby_sdk.base.dto import BaseDto


class NaverShoppingConfigResponse(BaseDto):
    """네이버 쇼핑 설정정보.

    OpenAPI: products-configuration-naver-shopping-293908981
    """

    supports_naver_shopping: bool | None = None
    agreed_to_collecting_cpa_order: bool | None = None
    authentication_key: str | None = None


class CustomPropertyValue(BaseDto):
    """상품 항목 값."""

    no: int | None = None
    value: str | None = None
    display_order: int | None = None


class CustomProperty(BaseDto):
    """상품 항목(커스텀 속성)."""

    no: int | None = None
    name: str | None = None
    display_order: int | None = None
    values: list[CustomPropertyValue] | None = None


class CustomPropertiesResponse(BaseDto):
    """상품 항목 조회 응답.

    OpenAPI: products-custom-properties-898470951
    """

    custom_properties: list[CustomProperty] | None = None


class ProductExtraInfoItem(BaseDto):
    """상품 추가 정보 항목.

    OpenAPI: products-extraInfo375807320 item
    """

    product_no: int | None = None
    extra_info: str | None = None


class DisplayCategoryItem(BaseDto):
    """상품의 전시카테고리 (depth1~5).

    OpenAPI: products-productNo-display-categories-1237636422 item
    """

    full_category_name: str | None = None
    depth1_no: int | None = None
    depth1_name: str | None = None
    depth2_no: int | None = None
    depth2_name: str | None = None
    depth3_no: int | None = None
    depth3_name: str | None = None
    depth4_no: int | None = None
    depth4_name: str | None = None
    depth5_no: int | None = None
    depth5_name: str | None = None


class StandardCategoryResponse(BaseDto):
    """상품의 표준카테고리.

    OpenAPI: products-productNo-standard-category1365440212
    """

    full_category_name: str | None = None
    depth1_no: int | None = None
    depth2_no: int | None = None
    depth3_no: int | None = None
    depth4_no: int | None = None


class UrlShorteningResponse(BaseDto):
    """상품 단축 URL.

    OpenAPI: products-productNo-url-shortening-1808461975
    """

    url: str | None = None


class ProductKeywordsItem(BaseDto):
    """상품번호별 검색어 목록.

    OpenAPI: products-search-keywords226225576 item
    """

    product_no: int | None = None
    keywords: list[str] | None = None

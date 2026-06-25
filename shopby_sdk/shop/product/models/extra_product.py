"""추가상품(Extra Products) 모델.

대응 OpenAPI schema: products-productNo-extra-products-267375444.
extraProducts[] 항목은 price/optionInfo(multiOptions/flatOptions/inputs)/limitations 등
깊은 중첩 구조이므로 가이드 2장에 따라 항목 본문은 dict[str, Any] 로 둔다.
"""

from typing import Any

from shopby_sdk.base.dto import BaseDto


class ExtraProductsResponse(BaseDto):
    """추가상품 조회 응답.

    OpenAPI: products-productNo-extra-products-267375444.
    extraProducts[] 는 거대 중첩 구조라 dict[str, Any].
    """

    extra_product_title: str | None = None
    extra_products: list[dict[str, Any]] | None = None

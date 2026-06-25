"""상품 상세(Product Detail) 모델.

대응 OpenAPI schema: products-productNo318672107.

상품 상세는 baseInfo/price/stock/brand/deliveryFee/limitations/status 등 30여 개의
깊게 중첩된 하위 객체로 구성된 가장 거대한 스키마다. 가이드 2장 규칙에 따라
스칼라/문자열 가이드 필드는 타입화하고, 거대 중첩 객체/배열은 dict[str, Any]/list[Any]
로 두며 그 사유를 본 docstring 에 남긴다. 필요 시 점진적 타입화 가능.
"""

from typing import Any

from shopby_sdk.base.dto import BaseDto


class ProductDetailResponse(BaseDto):
    """상품 상세 조회 응답.

    OpenAPI: products-productNo318672107.

    아래 중첩 객체 필드는 깊은 중첩/가변 구조라 dict[str, Any] 로 둔다:
    baseInfo, price, stock, brand, deliveryFee, deliveryDate, regularDelivery,
    counter, partner, partnerNotice, reservationData, shippingInfo,
    limitations, status. categories/rentalInfos 는 list[Any].
    """

    # 거대 중첩 객체 (동적/가변)
    base_info: dict[str, Any] | None = None
    price: dict[str, Any] | None = None
    stock: dict[str, Any] | None = None
    brand: dict[str, Any] | None = None
    delivery_fee: dict[str, Any] | None = None
    delivery_date: dict[str, Any] | None = None
    regular_delivery: dict[str, Any] | None = None
    counter: dict[str, Any] | None = None
    partner: dict[str, Any] | None = None
    partner_notice: dict[str, Any] | None = None
    reservation_data: dict[str, Any] | None = None
    shipping_info: dict[str, Any] | None = None
    limitations: dict[str, Any] | None = None
    status: dict[str, Any] | None = None
    categories: list[Any] | None = None
    rental_infos: list[Any] | None = None
    related_product_nos: list[int] | None = None

    # 스칼라/가이드 필드
    group_management_code: str | None = None
    group_management_code_name: str | None = None
    sale_method_type: str | None = None
    delivery_guide: str | None = None
    exchange_guide: str | None = None
    refund_guide: str | None = None
    after_service_guide: str | None = None
    liquor_delegation_guide: str | None = None
    review_available: bool | None = None
    review_rate: float | None = None
    liked: bool | None = None
    main_best_product_yn: bool | None = None
    displayable_stock: bool | None = None

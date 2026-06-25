"""배송(Shipping) 정보 모델.

대응 OpenAPI schema: products-shipping-info597838419
"""

from typing import Literal

from shopby_sdk.base.dto import BaseDto

DeliveryConditionType = Literal[
    "FREE",
    "CONDITIONAL",
    "FIXED_FEE",
    "QUANTITY_PROPOSITIONAL_FEE",
    "PRICE_FEE",
    "QUANTITY_FEE",
    "WEIGHT_FEE",
]
DeliveryType = Literal["PARCEL_DELIVERY", "DIRECT_DELIVERY"]
ShippingAreaType = Literal["PARTNER_SHIPPING_AREA", "MALL_SHIPPING_AREA"]


class RemoteDeliveryAreaFee(BaseDto):
    """지역별 추가배송비."""

    address: str | None = None
    extra_delivery_amt: int | None = None


class DeliveryConditionDetail(BaseDto):
    """금액/수량 구간별 배송비."""

    delivery_amt: int | None = None
    below: int | None = None
    above_or_equal: int | None = None


class ReturnWarehouse(BaseDto):
    """반품/출고 창고 정보."""

    warehouse_no: int | None = None
    warehouse_name: str | None = None
    warehouse_address_type: Literal["ADDRESS", "SUBSTITUTION"] | None = None
    partner_no: int | None = None
    country_cd: str | None = None
    zip_cd: str | None = None
    address: str | None = None
    detail_address: str | None = None
    address_str: str | None = None
    default_release_warehouse_yn: str | None = None
    default_return_warehouse_yn: str | None = None


class DeliveryFee(BaseDto):
    """배송비 정보."""

    delivery_condition_type: DeliveryConditionType | None = None
    delivery_type: DeliveryType | None = None
    delivery_company_type: str | None = None
    delivery_company_type_label: str | None = None
    default_delivery_condition_label: str | None = None
    delivery_amt: int | None = None
    delivery_amt_labels: list[str] | None = None
    above_delivery_amt: int | None = None
    delivery_pre_payment: bool | None = None
    return_delivery_amt: int | None = None
    per_order_cnt: int | None = None
    delivery_customer_info: str | None = None
    remote_delivery_area_fees: list[RemoteDeliveryAreaFee] | None = None
    delivery_condition_details: list[DeliveryConditionDetail] | None = None
    return_warehouse: ReturnWarehouse | None = None


class ShippingConfig(BaseDto):
    """배송 설정."""

    template_no: int | None = None
    shipping_area_partner_no: int | None = None
    shipping_area_type: ShippingAreaType | None = None
    international_shipping_available: bool | None = None
    combinable: bool | None = None


class ShippingInfo(BaseDto):
    """배송 가능 여부 + 설정."""

    shipping_available: bool | None = None
    shipping_config: ShippingConfig | None = None


class ProductShippingInfo(BaseDto):
    """상품별 배송 정보 및 배송 불가 국가.

    OpenAPI: products-shipping-info597838419 item.
    """

    product_no: int | None = None
    delivery_fee: DeliveryFee | None = None
    shipping_info: ShippingInfo | None = None
    # 스펙 예시가 국가코드 문자열(["KR", "CN"]) → list[str]
    undeliverable_countries: list[str] | None = None

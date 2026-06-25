"""Shopby Delivery Server API 클라이언트 패키지"""

from shopby_sdk.clients.delivery.client import ShopbyServerDeliveryApiClient
from shopby_sdk.clients.delivery.models import (
    Area,
    AreaFee,
    AreaFeeDetail,
    AreaFeeDetailRequest,
    AreaFeeRequest,
    AreaFeesResponse,
    CountryCode,
    DeliveryCompanyType,
    DeliveryConditionType,
    DeliveryFee,
    DeliveryFeeRange,
    DeliveryTemplate,
    DeliveryType,
    GroupDeliveryAmtType,
    ShippingAreaType,
    TemplateDetail,
    TemplateGroup,
    TemplateGroupCreateRequest,
    TemplateGroupTemplate,
    TemplateGroupUpdateRequest,
    TemplateModifyRequest,
    TemplateRequest,
    Warehouse,
    WarehouseAddress,
    WarehouseAddressRequest,
    WarehouseRequest,
    WarehouseSummary,
    WarehousesResponse,
)

__all__ = [
    "ShopbyServerDeliveryApiClient",
    # Literal 별칭
    "ShippingAreaType",
    "GroupDeliveryAmtType",
    "DeliveryConditionType",
    "DeliveryType",
    "DeliveryCompanyType",
    "CountryCode",
    # 공용 모델
    "WarehouseAddress",
    "WarehouseSummary",
    "DeliveryFee",
    "DeliveryFeeRange",
    # AreaFee
    "AreaFee",
    "AreaFeeDetail",
    "AreaFeesResponse",
    "AreaFeeDetailRequest",
    "AreaFeeRequest",
    # Area
    "Area",
    # Delivery template
    "DeliveryTemplate",
    "TemplateDetail",
    "TemplateGroup",
    "TemplateGroupTemplate",
    "TemplateRequest",
    "TemplateModifyRequest",
    "TemplateGroupCreateRequest",
    "TemplateGroupUpdateRequest",
    # Warehouse
    "Warehouse",
    "WarehousesResponse",
    "WarehouseAddressRequest",
    "WarehouseRequest",
]

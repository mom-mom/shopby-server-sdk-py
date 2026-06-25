"""그룹관리코드(Group Management Code) 모델.

대응 OpenAPI schema:
- products-group-management-code-959194716 (요청)
- products-group-management-code-1465298211 (응답)
"""

from typing import Literal

from shopby_sdk.base.dto import BaseDto

GroupMgmtOptionType = Literal[
    "STANDARD", "COMBINATION", "DEFAULT", "MAPPING", "REQUIRED"
]


class GroupManagementCodeRequest(BaseDto):
    """그룹관리코드 조회 요청.

    OpenAPI: products-group-management-code-959194716.
    groupManagementCodes/isSoldOut/saleStatus 모두 스펙상 string.
    """

    group_management_codes: str | None = None
    is_sold_out: str | None = None
    sale_status: str | None = None


class GroupMappingProductOption(BaseDto):
    """그룹 매핑 상품 옵션."""

    option_no: int | None = None
    name: str | None = None
    value: str | None = None
    forced_sold_out: bool | None = None


class GroupMappingProduct(BaseDto):
    """그룹관리코드 매핑 상품."""

    product_no: int | None = None
    product_name: str | None = None
    main_image_url: str | None = None
    image_urls: list[str] | None = None
    option_type: GroupMgmtOptionType | None = None
    has_option: bool | None = None
    is_minor_purchase: bool | None = None
    options: list[GroupMappingProductOption] | None = None


class GroupManagementCodeItem(BaseDto):
    """그룹관리코드 항목.

    OpenAPI: products-group-management-code-1465298211 item
    """

    group_management_code: str | None = None
    group_management_code_name: str | None = None
    group_management_code_description: str | None = None
    group_management_mapping_products: list[GroupMappingProduct] | None = None

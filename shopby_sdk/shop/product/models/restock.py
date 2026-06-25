"""재입고 알림(Restock) 모델.

대응 OpenAPI schema:
- products-restock-1401232336 (조회 응답)
- products-restock1510916953 (신청 요청)
"""

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class RestockItem(BaseDto):
    """재입고 알림 항목.

    OpenAPI: products-restock-1401232336 items[]
    """

    restock_no: int | None = None
    product_no: int | None = None
    option_no: int | None = None
    register_ymdt: KstDatetime | None = None


class RestockListResponse(BaseDto):
    """재입고 알림 조회 응답.

    OpenAPI: products-restock-1401232336
    """

    items: list[RestockItem] | None = None
    total_count: int | None = None
    total_page: int | None = None


class RestockRequest(BaseDto):
    """재입고 알림 신청 요청.

    OpenAPI: products-restock1510916953
    """

    option_nos: list[int]
    name: str
    phone: str
    privacy_info_agreement: bool

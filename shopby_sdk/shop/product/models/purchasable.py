"""상품 우선구매권한(Purchasable) 모델.

대응 OpenAPI schema: products-productNo-purchasable1717862054
"""

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class PurchasePermissionItem(BaseDto):
    """상품 우선구매권한 항목.

    OpenAPI: products-productNo-purchasable1717862054 item
    """

    permission_no: int | None = None
    option_no: int | None = None
    purchase_cnt: int | None = None
    purchased_cnt: int | None = None
    purchase_start_at: KstDatetime | None = None
    purchase_end_at: KstDatetime | None = None

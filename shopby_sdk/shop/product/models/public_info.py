"""상품 공개용 기본정보(Public Info) 모델.

대응 OpenAPI schema: products-public-info1328647758
"""

from typing import Any

from shopby_sdk.base.dto import BaseDto


class PublicInfoItem(BaseDto):
    """상품 공개용 기본정보 항목.

    OpenAPI: products-public-info1328647758 item.
    publicInfo 는 스펙상 manufactureYmdt 하나만 정의된 동적 객체라 dict[str, Any] 로 둔다.
    """

    product_no: int | None = None
    public_info: dict[str, Any] | None = None

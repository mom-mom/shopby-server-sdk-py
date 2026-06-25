"""상품 공개용 기본정보(Public Info) 모델.

대응 OpenAPI schema: products-public-info1328647758
"""

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class PublicInfoItem(BaseDto):
    """상품 공개용 기본정보 항목.

    OpenAPI: products-public-info1328647758 item.
    publicInfo 는 스펙상 manufactureYmdt 만 정의된 객체(추가 필드는 무시).
    """

    product_no: int | None = None
    public_info: "PublicInfo | None" = None


class PublicInfo(BaseDto):
    """상품 공개 기본정보 본문."""

    manufacture_ymdt: KstDatetime | None = None

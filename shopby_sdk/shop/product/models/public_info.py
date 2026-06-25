"""상품 공개용 기본정보(Public Info) 모델.

대응 OpenAPI schema: products-public-info1328647758
"""

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class PublicInfo(BaseDto):
    """상품 공개 기본정보 본문 (publicInfo).

    스펙상 manufactureYmdt 만 정의된 객체(추가 필드는 BaseDto 가 무시).
    """

    manufacture_ymdt: KstDatetime | None = None


class PublicInfoItem(BaseDto):
    """상품 공개용 기본정보 항목.

    OpenAPI: products-public-info1328647758 item.
    """

    product_no: int | None = None
    public_info: PublicInfo | None = None

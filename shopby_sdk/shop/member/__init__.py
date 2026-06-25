"""Shopby Shop(Client) Member API SDK.

shop-api(`https://shop-api.e-ncp.com`) member 도메인의 공개(인증 불필요) 엔드포인트
클라이언트와 모델을 제공한다.
"""

from shopby_sdk.shop.member.client import ShopbyShopMemberApiClient
from shopby_sdk.shop.member.models import (
    AutoSupplyingType,
    BusinessExistResponse,
    ExternalMemberExistRequest,
    ExternalMemberExistResponse,
    ExtraInfoOptionSummary,
    ExtraInfoStatus,
    ExtraInfoSummaryContent,
    ExtraInfoType,
    GradeCouponAutoSupplying,
    GradeEvaluationCondition,
    GradeReserveAutoSupplying,
    GradeReserveBenefit,
    MemberExtraInfo,
    MemberExtraInfoConfigResponse,
    MemberExtraInfosResponse,
    MemberGrade,
    MemberGroup,
    MemberSummaryExtraInfo,
    ProfileExistResponse,
    ProfileMobileExistResponse,
)

__all__ = [
    "ShopbyShopMemberApiClient",
    "AutoSupplyingType",
    "BusinessExistResponse",
    "ExternalMemberExistRequest",
    "ExternalMemberExistResponse",
    "ExtraInfoOptionSummary",
    "ExtraInfoStatus",
    "ExtraInfoSummaryContent",
    "ExtraInfoType",
    "GradeCouponAutoSupplying",
    "GradeEvaluationCondition",
    "GradeReserveAutoSupplying",
    "GradeReserveBenefit",
    "MemberExtraInfo",
    "MemberExtraInfoConfigResponse",
    "MemberExtraInfosResponse",
    "MemberGrade",
    "MemberGroup",
    "MemberSummaryExtraInfo",
    "ProfileExistResponse",
    "ProfileMobileExistResponse",
]

"""Shopby Shop(Client) Promotion(쿠폰) API.

shop-api(`https://shop-api.e-ncp.com`) 의 공개(인증 불필요) 쿠폰 조회/설정 API 클라이언트.
"""

from .client import ShopbyShopPromotionApiClient
from .models import (
    CouponSubType,
    CouponTargetItem,
    CouponTargetsResponse,
    CouponTargetType,
    CouponType,
    IssuableCoupon,
    IssuableCouponBenefitInfo,
    IssuableCouponDateInfo,
    IssuableCouponDiscountInfo,
    IssuableCouponIssueConstraint,
    IssuableCouponsResponse,
    IssuableCouponStatus,
    IssuableCouponUseConstraint,
    IssueLimitType,
    PayType,
    PlatformType,
    PromotionCouponConfig,
)

__all__ = [
    "ShopbyShopPromotionApiClient",
    # 발급 가능 쿠폰
    "IssuableCoupon",
    "IssuableCouponsResponse",
    "IssuableCouponDiscountInfo",
    "IssuableCouponDateInfo",
    "IssuableCouponUseConstraint",
    "IssuableCouponIssueConstraint",
    "IssuableCouponStatus",
    "IssuableCouponBenefitInfo",
    # 타겟/제외 상품
    "CouponTargetItem",
    "CouponTargetsResponse",
    # 쿠폰 설정
    "PromotionCouponConfig",
    # Literal 타입 별칭
    "CouponType",
    "CouponSubType",
    "CouponTargetType",
    "PlatformType",
    "IssueLimitType",
    "PayType",
]

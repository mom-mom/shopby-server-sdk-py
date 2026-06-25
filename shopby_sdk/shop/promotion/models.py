"""Shopby Shop(Client) Promotion(쿠폰) API 모델 정의.

shop-api(`https://shop-api.e-ncp.com`) 의 공개(인증 불필요) 쿠폰 조회/설정 API 응답 모델.
대응 OpenAPI: docs/api/promotion-shop-public.yml
"""

from typing import Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime

# ------------------------------------
#  Literal 타입 별칭 (Enum)
# ------------------------------------
CouponType = Literal["PRODUCT", "CART", "CART_DELIVERY", "GIFT"]
"""쿠폰 종류 (PRODUCT: 상품적용, CART: 주문적용, CART_DELIVERY: 장바구니 배송비, GIFT: 기프트)"""

CouponSubType = Literal["CART", "DELIVERY_DEFAULT", "DELIVERY_ALL", "NONE"]
"""쿠폰 하위 타입"""

CouponTargetType = Literal["ALL_PRODUCT", "PRODUCT", "BRAND", "CATEGORY", "PARTNER"]
"""쿠폰 대상 타입"""

PlatformType = Literal["PC", "MOBILE_WEB", "MOBILE_APP"]
"""쿠폰 발급/사용 플랫폼 타입"""

IssueLimitType = Literal["PRODUCT_DETAIL"]
"""발급위치 제한 타입 (PRODUCT_DETAIL: 상품상세 미노출)"""

PayType = Literal[
    "CREDIT_CARD",
    "ACCOUNT",
    "MOBILE",
    "REALTIME_ACCOUNT_TRANSFER",
    "VIRTUAL_ACCOUNT",
    "GIFT",
    "ATM",
    "PAYCO",
    "ZERO_PAY",
    "ACCUMULATION",
    "PHONE_BILL",
    "POINT",
    "YPAY",
    "KPAY",
    "PAYPIN",
    "INIPAY",
    "PAYPAL",
    "STRIPE",
    "NAVER_PAY",
    "KAKAO_PAY",
    "NAVER_EASY_PAY",
    "SAMSUNG_PAY",
    "CHAI",
    "TOSS_PAY",
    "SK_PAY",
    "APPLE_PAY",
    "ESCROW_REALTIME_ACCOUNT_TRANSFER",
    "ESCROW_VIRTUAL_ACCOUNT",
    "VERITRANS_CARD",
    "TOASTCAM",
    "UNION_PAY",
    "ALIPAY",
    "WECHAT_PAY",
    "PINPAY",
    "EXTERNAL_PAY",
    "HMG_PAY",
    "APP_CARD",
    "PAY_PAY",
    "E_CONTEXT",
    "HAPPY_VOUCHER",
    "ETC",
]
"""쿠폰 사용가능 결제수단 타입"""


# ------------------------------------
#  발급 가능 쿠폰 조회 (issuable coupons)
#  schema: coupons-targets-issuable-coupons-2069395255 (items)
# ------------------------------------
class IssuableCouponDiscountInfo(BaseDto):
    """쿠폰 할인정보 (discountInfo)."""

    discount_rate: float | None = Field(None, description="쿠폰 할인율")
    discount_amt: float | None = Field(None, description="쿠폰 할인액")
    use_other_coupon: bool | None = Field(None, description="타 쿠폰과 함께 사용가능 여부")
    skipped_accumulation_amt: bool | None = Field(None, description="적립금 지급 불가 여부")
    use_product_coupon: bool | None = Field(None, description="상품 쿠폰 사용가능 여부")
    free_delivery: bool | None = Field(None, description="배송비 무료 여부(배송비쿠폰인경우)")
    max_discount_amt: float | None = Field(None, description="최대 할인액")
    use_cart_coupon: bool | None = Field(None, description="장바구니 쿠폰 사용가능 여부")
    fixed_amt: bool | None = Field(None, description="정액여부 (true: 정액 / false: 정률)")


class IssuableCouponDateInfo(BaseDto):
    """쿠폰 발급시간정보 (dateInfo)."""

    issue_start_ymdt: KstDatetime | None = Field(None, description="발급 시작 일")
    issue_end_ymdt: KstDatetime | None = Field(None, description="발급 제한 일")
    issue_days_of_week: str | None = Field(None, description="발급가능요일 (JSON 문자열)")
    issue_start_hour: int | None = Field(None, description="발급 시작 시간")
    issue_end_hour: int | None = Field(None, description="발급 종료 시간")


class IssuableCouponUseConstraint(BaseDto):
    """쿠폰 사용제약조건 (useConstraint)."""

    limit_pay_type: PayType | None = Field(None, description="쿠폰 사용가능 결제수단")
    limit_pay_types: list[PayType] | None = Field(None, description="쿠폰 사용가능 결제수단 리스트")
    use_days: int | None = Field(None, description="사용가능 기간 (31: 월말까지, -1: 제한없음)")
    use_end_ymdt: KstDatetime | None = Field(None, description="사용 종료 일")
    min_sale_price: float | None = Field(None, description="쿠폰 사용조건 최소 구매액")
    max_sale_price: float | None = Field(None, description="쿠폰 사용조건 최대 구매액")
    min_delivery_amt: float | None = Field(None, description="쿠폰 사용조건 최소 배송비")
    usable_platform_types: list[PlatformType] | None = Field(None, description="사용가능 플랫폼")


class IssuableCouponIssueConstraint(BaseDto):
    """쿠폰 발급제약조건 (issueConstraint)."""

    member_grade_name: str | None = Field(None, description="발급대상 회원 등급")
    member_grade_names: list[str] | None = Field(None, description="발급대상 회원 등급 목록")
    member_group_names: list[str] | None = Field(None, description="발급대상 회원 그룹 목록")
    issuable_platform_types: list[PlatformType] | None = Field(None, description="발행가능 플랫폼")
    channel_types: list[str] | None = Field(None, description="발급/사용 채널")
    daily_issue_limit: bool | None = Field(None, description="1일내 발급 수량 제한 여부")
    daily_issue_limit_cnt: int | None = Field(None, description="1일내 발급 제한 수량")
    issue_per_person_limit: bool | None = Field(None, description="1인당 발급 수량 제한 여부")
    issue_per_person_limit_cnt: int | None = Field(None, description="1인당 발급 제한 수량(총기간)")
    daily_issue_per_person_limit_cnt: int | None = Field(
        None, description="1인당 발급 제한 수량(1일간)"
    )


class IssuableCouponStatus(BaseDto):
    """쿠폰 발급상태 (couponStatus)."""

    total_issuable_cnt: int | None = Field(None, description="쿠폰 발행가능 수량")
    total_issued_cnt: int | None = Field(None, description="총 발행수량")
    total_issued_cnt_today: int | None = Field(None, description="총 발행수량(오늘)")
    issuable_cnt: int | None = Field(None, description="발급가능수량")
    my_issued_cnt: int | None = Field(None, description="내가 발급 받은 개수")
    my_issued_cnt_today: int | None = Field(None, description="내가 발급 받은 개수(오늘)")


class IssuableCouponBenefitInfo(BaseDto):
    """기프트 쿠폰 혜택정보 (benefitInfo)."""

    benefit_amt: float | None = Field(None, description="혜택 금액")
    benefit_end_ymdt: KstDatetime | None = Field(None, description="혜택 만료일자")
    benefit_expiration_days: int | None = Field(
        None, description="혜택 지급 시점으로부터 혜택 만료일"
    )


class IssuableCoupon(BaseDto):
    """발급 가능 쿠폰 단건 (coupons-targets-issuable-coupons-2069395255 items)."""

    coupon_no: int | None = Field(None, description="쿠폰 번호")
    coupon_name: str | None = Field(None, description="쿠폰 이름")
    coupon_type: CouponType | None = Field(None, description="쿠폰 종류")
    coupon_sub_type: CouponSubType | None = Field(None, description="쿠폰 하위 타입")
    coupon_target_type: CouponTargetType | None = Field(None, description="쿠폰 대상 종류")
    downloadable: bool | None = Field(None, description="다운로드 가능여부")
    alliance_referer_type: str | None = Field(
        None, description="(deprecated) 제휴 방문처 타입"
    )
    issue_limit_types: list[IssueLimitType] | None = Field(
        None, description="발급위치 제한"
    )
    discount_info: IssuableCouponDiscountInfo | None = Field(None, description="할인정보")
    date_info: IssuableCouponDateInfo | None = Field(None, description="발급시간정보")
    use_constraint: IssuableCouponUseConstraint | None = Field(None, description="사용제약조건")
    issue_constraint: IssuableCouponIssueConstraint | None = Field(
        None, description="발급제약조건"
    )
    coupon_status: IssuableCouponStatus | None = Field(None, description="쿠폰발급상태")
    benefit_info: IssuableCouponBenefitInfo | None = Field(
        None, description="기프트 쿠폰 혜택정보"
    )


# 발급 가능 쿠폰 조회 응답은 배열(top-level array)이다.
IssuableCouponsResponse = list[IssuableCoupon]
"""발급 가능 쿠폰 목록 응답 (top-level JSON array)."""


# ------------------------------------
#  쿠폰 타겟/제외상품 조회
#  schema: coupons-couponNo-exclude-targets1178057331
# ------------------------------------
class CouponTargetItem(BaseDto):
    """쿠폰 타겟/제외 상품 단건 (items)."""

    target_no: int | None = Field(None, description="상품 번호")
    target_name: str | None = Field(None, description="상품 이름")
    target_type: CouponTargetType | None = Field(None, description="상품 타입")


class CouponTargetsResponse(BaseDto):
    """쿠폰 타겟/제외 상품 목록 응답 (coupons-couponNo-exclude-targets1178057331)."""

    total_count: int | None = Field(None, description="총 상품 개수")
    items: list[CouponTargetItem] | None = Field(None, description="상품 내역")


# ------------------------------------
#  쿠폰 설정 조회
#  schema: promotion-configs-coupon1107775460
# ------------------------------------
class PromotionCouponConfig(BaseDto):
    """쿠폰 설정 응답 (promotion-configs-coupon1107775460)."""

    allow_cart_coupon_when_unusable_products_exist: bool | None = Field(
        None,
        description=(
            "주문적용 쿠폰 사용가능여부 "
            "(주문에 쿠폰 사용 불가 상품이 포함된 경우에도 주문적용 쿠폰을 사용 가능합니다.)"
        ),
    )

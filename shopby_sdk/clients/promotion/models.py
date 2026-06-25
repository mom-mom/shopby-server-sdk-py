"""Promotion(쿠폰) API 모델 정의"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime

# ------------------------------------
#  Literal 타입 별칭 (Enum)
# ------------------------------------
CouponType = Literal["PRODUCT", "PRODUCT_PLUS", "CART", "CART_DELIVERY", "GIFT"]
"""혜택 구분 타입 (PRODUCT: 상품적용, CART: 주문적용, CART_DELIVERY: 장바구니 배송비, GIFT: 기프트)"""

CouponSubType = Literal["CART", "DELIVERY_DEFAULT", "DELIVERY_ALL", "NONE"]
"""쿠폰 하위 타입"""

IssueType = Literal[
    "DOWNLOAD",
    "CODE_DESIGNATE",
    "CODE_RANDOM",
    "INSERT",
    "CODE_DESIGNATE_ADMIN_ONLY",
]
"""쿠폰 발급 타입"""

CouponStatusType = Literal["ISSUE_READY", "ISSUE_ING", "ISSUE_STOP", "ISSUE_END"]
"""쿠폰 상태 타입"""

CouponTargetType = Literal["ALL_PRODUCT", "PRODUCT", "BRAND", "CATEGORY", "PARTNER"]
"""쿠폰 대상 타입"""

PlatformType = Literal["PC", "MOBILE_WEB", "MOBILE_APP"]
"""플랫폼 타입"""

GiftCouponType = Literal["ACCUMULATION"]
"""기프트 쿠폰 타입"""

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
"""결제수단"""

# 검색 파라미터용 Literal
CouponSearchDateType = Literal["REGISTER_YMD", "ISSUE_START_YMD", "ISSUE_END_YMD", "UPDATE_YMD", "USE_END_YMD"]
"""쿠폰 검색 날짜 타입"""

CouponSearchKeywordType = Literal["ALL", "COUPON_NAME", "COUPON_NO", "REGISTER_ADMIN"]
"""쿠폰 검색어 타입"""

CouponIssueSearchDateType = Literal["ISSUE_START_YMD", "ISSUE_END_YMD", "ISSUE_YMD", "USE_END_YMD"]
"""지급 쿠폰 검색 날짜 타입"""

CouponUseSearchKeywordType = Literal["ORDER_NO", "COUPON_NO"]
"""사용 쿠폰 검색어 타입"""

CouponUseSearchDateType = Literal["ISSUE_YMD", "USE_YMD"]
"""사용 쿠폰 검색 날짜 타입"""


# ------------------------------------
#  쿠폰 검색 응답 (coupons579437697)
# ------------------------------------
class SearchCouponContent(BaseDto):
    """쿠폰 검색 결과 단건"""

    no: int = Field(..., description="쿠폰 번호")
    mall_name: str | None = Field(None, description="쇼핑몰 이름")
    coupon_name: str | None = Field(None, description="쿠폰명")
    coupon_type: CouponType | None = Field(None, description="혜택 구분 타입")
    coupon_sub_type: CouponSubType | None = Field(None, description="쿠폰 하위 타입")
    issue_type: IssueType | None = Field(None, description="발급 타입")
    coupon_status_type: CouponStatusType | None = Field(None, description="쿠폰 상태 타입")
    uses_min_limit: bool | None = Field(None, description="최소 기준 금액 사용여부")
    min_sale_price: float | None = Field(None, description="최소 기준 금액")
    uses_max_limit: bool | None = Field(None, description="최대 기준 금액 사용여부")
    max_sale_price: float | None = Field(None, description="최대 기준 금액")
    fixed: bool | None = Field(None, description="정액 할인 여부")
    discount_amt: float | None = Field(None, description="할인금액(정액)")
    discount_percent: float | None = Field(None, description="할인금액(정률)")
    max_discount_amt: float | None = Field(None, description="최대할인금액")
    issue_limit_cnt: int | None = Field(None, description="발행수량")
    uses_daily_issue_limit: bool | None = Field(None, description="일별 발급 수량 제한 여부")
    daily_issue_limit_cnt: int | None = Field(None, description="일별 발급 제한 수량")
    uses_personal_issue_limit: bool | None = Field(None, description="회원별 발급 수량 제한 여부")
    issue_per_person_limit_cnt: int | None = Field(None, description="회원별 발급 제한 수량")
    daily_issue_per_person_limit_cnt: int | None = Field(None, description="1인당 발급 제한 - 1일발급제한")
    total_issue_cnt: int | None = Field(None, description="발급현황")
    total_issue_cnt_by_admin: int | None = Field(None, description="관리자 - 발급현황")
    total_use_cnt: int | None = Field(None, description="사용현황")
    issue_start_ymdt: KstDatetime | None = Field(None, description="쿠폰 발행 시작일시")
    issue_end_ymdt: KstDatetime | None = Field(None, description="쿠폰 발행 종료일시")
    service_share_rate: float | None = Field(None, description="쇼핑몰 비용 분담율")
    register_ymdt: KstDatetime | None = Field(None, description="쿠폰 등록일시")
    update_ymdt: KstDatetime | None = Field(None, description="쿠폰 수정일시")
    promotion_code: str | None = Field(None, description="관리자가 직접 입력한 프로모션 코드")
    issue_stopped: bool | None = Field(None, description="발급 일시중지 여부")
    scheduled_issue_plan: bool | None = Field(None, description="예약 지급 계획에 설정된 쿠폰 여부")
    member_grade_nos: list[int] = Field(default_factory=list, description="발급 대상 회원등급 번호 리스트")
    member_group_nos: list[int] = Field(default_factory=list, description="발급 대상 회원그룹 번호 리스트")
    benefit_amt: float | None = Field(None, description="혜택 금액")
    use_days: int | None = Field(None, description="사용가능 기간 - 발급받은 날부터 / 31: 말일 / -1: 제한 없음")
    use_end_ymdt: KstDatetime | None = Field(None, description="사용가능 기간 - 특정 일시 지정")


class SearchCouponResponse(BaseDto):
    """
    쿠폰 검색 응답

    OpenAPI Schema: coupons579437697
    """

    total_count: int = Field(..., description="전체 쿠폰 수")
    contents: list[SearchCouponContent] = Field(default_factory=list, description="쿠폰 검색 결과 리스트")


# ------------------------------------
#  쿠폰 대상/제외 대상 조회 응답 (coupons-exclude-targets616348469)
# ------------------------------------
class CouponTargetContent(BaseDto):
    """쿠폰 대상/제외대상 단건"""

    coupon_no: int | None = Field(None, description="쿠폰 번호")
    target_no: int | None = Field(None, description="대상 번호")
    target_name: str | None = Field(None, description="대상 이름")
    target_type: str | None = Field(None, description="대상 타입")


class CouponTargetsResponse(BaseDto):
    """
    쿠폰 대상/제외 대상 조회 응답

    OpenAPI Schema: coupons-exclude-targets616348469
    """

    total_count: int = Field(..., description="총 개수")
    total_page: int | None = Field(None, description="총 페이지")
    contents: list[CouponTargetContent] = Field(default_factory=list, description="대상 리스트")


# ------------------------------------
#  사용된 쿠폰 검색 응답 (coupons-use628303737)
# ------------------------------------
class UsedCouponContent(BaseDto):
    """
    사용된 쿠폰 정보 단건

    OpenAPI Schema: coupons-use628303737 (array item)
    """

    coupon_no: int = Field(..., description="쿠폰 번호")
    coupon_issue_no: int | None = Field(None, description="쿠폰 발급 번호")
    coupon_name: str | None = Field(None, description="쿠폰명")
    coupon_type: CouponType | None = Field(None, description="혜택 구분 타입")
    coupon_sub_type: CouponSubType | None = Field(None, description="쿠폰 하위 타입")
    issue_type: IssueType | None = Field(None, description="발급 타입")
    coupon_status_type: CouponStatusType | None = Field(None, description="쿠폰 상태 타입")
    uses_min_limit: bool | None = Field(None, description="최소 기준 금액 사용여부")
    min_sale_price: float | None = Field(None, description="최소 기준 금액")
    uses_max_limit: bool | None = Field(None, description="최대 기준 금액 사용여부")
    max_sale_price: float | None = Field(None, description="최대 기준 금액")
    fixed: bool | None = Field(None, description="정액 할인 여부")
    discount_amt: float | None = Field(None, description="할인금액(정액)")
    discount_percent: float | None = Field(None, description="할인금액(정률)")
    max_discount_amt: float | None = Field(None, description="최대할인금액")
    coupon_discount_amt: float | None = Field(None, description="할인 적용된 금액")
    service_share_rate: float | None = Field(None, description="쇼핑몰 비용 분담율")
    issue_start_ymdt: KstDatetime | None = Field(None, description="쿠폰 발행 시작일시")
    issue_end_ymdt: KstDatetime | None = Field(None, description="쿠폰 발행 종료일시")
    register_ymdt: KstDatetime | None = Field(None, description="쿠폰 등록일시")
    update_ymdt: KstDatetime | None = Field(None, description="쿠폰 수정일시")
    use_ymdt: KstDatetime | None = Field(None, description="쿠폰 사용일시")
    issue_stopped: bool | None = Field(None, description="발급 일시중지 여부")
    promotion_code: str | None = Field(None, description="관리자가 직접 입력한 프로모션 코드")
    order_no: str | None = Field(None, description="주문 번호")
    order_product_no: int | None = Field(None, description="주문 상품 번호(상품 쿠폰이 아닌 경우 0)")
    pay_amt: float | None = Field(None, description="결제 금액")
    total_count: int | None = Field(None, description="전체 수량")


# ------------------------------------
#  지급된 쿠폰 검색 응답 (coupons-issues-1405023554)
# ------------------------------------
class CouponIssueContent(BaseDto):
    """지급된 쿠폰 단건"""

    member_no: int | None = Field(None, description="회원 번호")
    coupon_no: int | None = Field(None, description="쿠폰 번호")
    coupon_issue_no: int | None = Field(None, description="쿠폰 발행 번호")
    coupon_name: str | None = Field(None, description="쿠폰 이름")
    coupon_type: CouponType | None = Field(None, description="혜택 구분 타입")
    coupon_sub_type: CouponSubType | None = Field(None, description="쿠폰 하위 타입")
    issue_type: IssueType | None = Field(None, description="발급 타입")
    fixed: bool | None = Field(None, description="정액 할인 여부")
    discount_amt: float | None = Field(None, description="할인금액(정액)")
    discount_rate: float | None = Field(None, description="할인금액(정률)")
    max_discount_amt: float | None = Field(None, description="최대 할인금액")
    coupon_discount_amt: float | None = Field(None, description="쿠폰 할인 금액")
    benefit_amt: float | None = Field(None, description="혜택 금액")
    use_end_ymdt: KstDatetime | None = Field(None, description="쿠폰 만료일시")
    register_ymdt: KstDatetime | None = Field(None, description="쿠폰 지급일시")
    use_ymdt: KstDatetime | None = Field(None, description="사용일시")
    used: bool | None = Field(None, description="쿠폰 사용 여부")
    withdrawn: bool | None = Field(None, description="쿠폰 철회 여부")
    admin_issued: bool | None = Field(None, description="어드민 발급 여부")


class SearchCouponIssueResponse(BaseDto):
    """
    지급된 쿠폰 검색 응답

    OpenAPI Schema: coupons-issues-1405023554
    """

    total_count: int = Field(..., description="총 개수")
    contents: list[CouponIssueContent] = Field(default_factory=list, description="지급된 쿠폰 리스트")


# ------------------------------------
#  쿠폰 발급 응답 (coupons-issues-194375905)
# ------------------------------------
class IssueCouponResult(BaseDto):
    """
    쿠폰 발급 결과 단건

    OpenAPI Schema: coupons-issues-194375905 (array item)
    """

    coupon_no: int | None = Field(None, description="쿠폰 번호")
    member_no: int | None = Field(None, description="회원 번호")
    coupon_issue_no: int | None = Field(None, description="쿠폰 지급 번호")
    use_end_ymdt: str | None = Field(None, description="쿠폰 만료 일시")
    issue_fail: bool | None = Field(None, description="쿠폰 지급 실패 여부")


# ------------------------------------
#  쿠폰 생성 응답 (coupons-1711516014)
# ------------------------------------
class CreateCouponResponse(BaseDto):
    """
    쿠폰 생성 응답

    OpenAPI Schema: coupons-1711516014
    """

    coupon_no: int = Field(..., description="생성된 쿠폰 번호")


# ------------------------------------
#  쿠폰 공통 상세 구성요소 (생성/수정/조회 공용)
# ------------------------------------
class CouponTargetItem(BaseDto):
    """쿠폰 대상/제외대상 항목"""

    coupon_target_type: CouponTargetType | None = Field(None, description="쿠폰 대상 타입")
    target_no: int | None = Field(None, description="쿠폰 대상 번호")
    target_name: str | None = Field(None, description="쿠폰 대상 이름")
    register_ymdt: KstDatetime | None = Field(None, description="타겟 등록 날짜")


class CartCouponDetail(BaseDto):
    """장바구니 쿠폰 상세"""

    usable_other_coupon: bool | None = Field(None, description="상품쿠폰 사용 제한 여부")
    skips_accumulation: bool | None = Field(None, description="적립금 적립 제한 여부")
    coupon_issue_limit_types: list[str] = Field(default_factory=list, description="발급위치 제한 (PRODUCT_DETAIL 등)")
    coupon_target_type: CouponTargetType | None = Field(None, description="쿠폰 대상 타입")
    coupon_targets: list[CouponTargetItem] = Field(default_factory=list, description="쿠폰 할인 대상 정보")
    excludes_target: bool | None = Field(None, description="할인 대상 제외 설정 여부")
    coupon_exclude_targets: list[CouponTargetItem] = Field(default_factory=list, description="쿠폰 할인 제외 대상 정보")


class ProductCouponDetail(BaseDto):
    """상품 쿠폰 상세"""

    skips_accumulation: bool | None = Field(None, description="적립금 제한 여부")
    usable_cart_coupon: bool | None = Field(None, description="주문쿠폰 사용 제한 여부")
    service_share_percent: float | None = Field(None, description="비용분담 설정-쇼핑몰 부담")
    coupon_issue_limit_types: list[Any] = Field(default_factory=list, description="발급위치 제한")
    coupon_target_type: CouponTargetType | None = Field(None, description="할인쿠폰 대상 타입")
    coupon_targets: list[CouponTargetItem] = Field(default_factory=list, description="쿠폰 대상 리스트")
    excludes_target: bool | None = Field(None, description="할인 대상 제외 설정 여부")
    coupon_exclude_targets: list[CouponTargetItem] = Field(default_factory=list, description="쿠폰 제외 대상 리스트")


class GiftCouponDetail(BaseDto):
    """기프트 쿠폰 상세"""

    gift_coupon_type: GiftCouponType | None = Field(None, description="기프트 쿠폰 타입")
    benefit_end_ymdt: KstDatetime | None = Field(None, description="혜택 만료일자")
    benefit_amt: float | None = Field(None, description="혜택 금액")
    benefit_expiration_days: int | None = Field(None, description="혜택 지급 시점으로부터 혜택 만료일")


class UsableConstraint(BaseDto):
    """사용 제약사항"""

    usable_platform_types: list[PlatformType] = Field(default_factory=list, description="사용가능 플랫폼")
    use_end_ymdt: KstDatetime | None = Field(None, description="사용가능 기간 - 특정 일시 지정")
    use_days: int | None = Field(None, description="사용가능 기간 - 발급받은 날부터 / 31: 말일 / -1: 제한 없음")
    limit_pay_type: PayType | None = Field(None, description="사용가능 결제수단")
    limit_pay_types: list[PayType] = Field(default_factory=list, description="사용가능 결제수단 리스트")
    use_stopped: bool | None = Field(None, description="사용가능 여부 (true: 사용불가)")


class IssuableConstraint(BaseDto):
    """발급 제약사항"""

    issue_type: IssueType | None = Field(None, description="발급 타입")
    issue_start_ymdt: KstDatetime | None = Field(None, description="쿠폰발행 기간-시작일시")
    issue_end_ymdt: KstDatetime | None = Field(None, description="쿠폰발행 기간-종료일시")
    member_grade_no: int | None = Field(None, description="발급대상 회원등급")
    member_grade_nos: list[int] = Field(default_factory=list, description="발급대상 회원등급 리스트")
    member_group_nos: list[int] = Field(default_factory=list, description="발급대상 회원그룹 리스트")
    issue_limit_cnt: int | None = Field(None, description="발급 제한 수량")
    issue_start_hour: int | None = Field(None, description="발급시간대 - 시작 시")
    issue_end_hour: int | None = Field(None, description="발급시간대 - 종료 시")
    issue_stopped: bool | None = Field(None, description="발급 일시중지 여부")
    finishes_issuing: bool | None = Field(None, description="발급 종료여부")
    uses_daily_issue_limit: bool | None = Field(None, description="1일 발급 제한 여부")
    daily_issue_limit_cnt: int | None = Field(None, description="1일 발급 제한 개수")
    uses_personal_issue_limit: bool | None = Field(None, description="1인당 발급 제한 여부")
    issue_per_person_limit_cnt: int | None = Field(None, description="1인당 발급 제한 수량")
    daily_issue_per_person_limit_cnt: int | None = Field(None, description="1인당 발급 제한 - 1일 발급 제한 개수")
    issuable_platform_types: list[PlatformType] = Field(default_factory=list, description="발급가능 플랫폼")
    channel_types: list[str] = Field(default_factory=list, description="채널타입 리스트")
    possible_days_of_week: list[int] = Field(default_factory=list, description="발급가능 요일")
    promotion_code: str | None = Field(None, description="프로모션코드 - 지정코드 발급인 경우")
    coupon_code_length: int | None = Field(None, description="난수 자리수 - 난수코드 발급인 경우")
    is_period_end: bool | None = Field(None, description="발행기간 만료")


class CouponDiscount(BaseDto):
    """쿠폰 할인정보"""

    uses_min_limit: bool | None = Field(None, description="최소 기준 금액 제한여부")
    min_sale_price: float | None = Field(None, description="최소 기준 상품 금액")
    uses_max_limit: bool | None = Field(None, description="최대 기준 금액 제한여부")
    max_sale_price: float | None = Field(None, description="최대 기준 상품 금액")
    fixed: bool | None = Field(None, description="정액 할인 여부")
    discount_amt: float | None = Field(None, description="할인 금액")
    discount_percent: float | None = Field(None, description="정률")
    max_discount_amt: float | None = Field(None, description="최대할인금액")


class CouponSummary(BaseDto):
    """쿠폰 요약"""

    total_issue_cnt: int | None = Field(None, description="쿠폰 발급 개수")
    total_use_cnt: int | None = Field(None, description="쿠폰 사용 개수")
    total_normal_issue_cnt: int | None = Field(None, description="일반 발급 쿠폰 개수")
    total_issue_cnt_by_admin: int | None = Field(None, description="관리자가 지급한 쿠폰 총 지급 개수")


# ------------------------------------
#  쿠폰 상세 조회 응답 (coupons-couponNo269484807)
# ------------------------------------
class CouponDetailResponse(BaseDto):
    """
    쿠폰 정보 조회 응답

    OpenAPI Schema: coupons-couponNo269484807
    """

    coupon_name: str | None = Field(None, description="쿠폰 이름")
    status_type: CouponStatusType | None = Field(None, description="쿠폰상태")
    reason: str | None = Field(None, description="쿠폰 사유")
    coupon_type: CouponType | None = Field(None, description="혜택 구분 타입")
    coupon_sub_type: CouponSubType | None = Field(None, description="쿠폰 하위 타입")
    usable_constraint: UsableConstraint | None = Field(None, description="사용 제약사항")
    issuable_constraint: IssuableConstraint | None = Field(None, description="발급 제약사항")
    coupon_summary: CouponSummary | None = Field(None, description="쿠폰 요약")
    discount: CouponDiscount | None = Field(None, description="쿠폰 할인정보")
    cart_coupon_detail: CartCouponDetail | None = Field(None, description="장바구니 쿠폰상세")
    product_coupon_detail: ProductCouponDetail | None = Field(None, description="상품쿠폰 상세")
    gift_coupon_detail: GiftCouponDetail | None = Field(None, description="기프트 쿠폰 상세")
    today_issue_cnt: int | None = Field(None, description="오늘 발급 수")
    is_scheduled_issue_plan: bool | None = Field(None, description="예약 지급 여부")
    is_count_over: bool | None = Field(None, description="수량 만료 여부")


# ------------------------------------
#  요청 모델
# ------------------------------------
class CreateCouponRequest(BaseDto):
    """
    쿠폰 생성 요청

    OpenAPI Schema: coupons-1368241265
    """

    mall_no: int = Field(..., description="몰정보")
    coupon_name: str = Field(..., description="쿠폰 이름")
    reason: str | None = Field(None, description="쿠폰 발급 사유")
    coupon_type: CouponType = Field(..., description="혜택 구분 타입")
    coupon_sub_type: CouponSubType | None = Field(None, description="쿠폰 하위 타입")
    usable_constraint: UsableConstraint | None = Field(None, description="사용 제약사항")
    issuable_constraint: IssuableConstraint | None = Field(None, description="발급 제약사항")
    discount: CouponDiscount | None = Field(None, description="쿠폰 할인정보")
    cart_coupon_detail: CartCouponDetail | None = Field(None, description="장바구니 쿠폰상세")
    product_coupon_detail: ProductCouponDetail | None = Field(None, description="상품쿠폰 상세")
    gift_coupon_detail: GiftCouponDetail | None = Field(None, description="기프트 쿠폰 상세")


class UpdateCouponRequest(BaseDto):
    """
    쿠폰 수정 요청

    OpenAPI Schema: coupons-couponNo-659846160
    """

    coupon_name: str | None = Field(None, description="쿠폰명")
    reason: str | None = Field(None, description="쿠폰 사유")
    coupon_type: CouponType | None = Field(None, description="혜택 구분 타입")
    coupon_sub_type: CouponSubType | None = Field(None, description="쿠폰 하위 타입")
    usable_constraint: UsableConstraint | None = Field(None, description="사용 제약사항")
    issuable_constraint: IssuableConstraint | None = Field(None, description="발급 제약사항")
    discount: CouponDiscount | None = Field(None, description="쿠폰 할인정보")
    cart_coupon_detail: CartCouponDetail | None = Field(None, description="장바구니 쿠폰 상세")
    product_coupon_detail: ProductCouponDetail | None = Field(None, description="상품 쿠폰 상세")
    gift_coupon_detail: GiftCouponDetail | None = Field(None, description="기프트 쿠폰 상세")


class IssueCouponRequest(BaseDto):
    """
    쿠폰 발급 요청

    OpenAPI Schema: coupons-issues1966572697
    """

    coupon_no: int | None = Field(None, description="쿠폰 번호")
    coupon_nos: list[int] = Field(default_factory=list, description="쿠폰 번호 리스트")
    member_nos: list[int] = Field(default_factory=list, description="회원 번호 리스트")
    member_ids: list[str] = Field(default_factory=list, description="회원 ID 리스트")
    reason: str | None = Field(None, description="발급 사유")
    is_admin_issue: bool | None = Field(None, description="어드민 발급 여부")


class UseCouponItem(BaseDto):
    """
    쿠폰 사용 요청 항목

    OpenAPI Schema: coupons-use-458945078 (array item)
    """

    coupon_issue_no: int = Field(..., description="쿠폰 지급 번호")
    coupon_discount_amt: float | None = Field(None, description="쿠폰 할인 금액")


class WithdrawCouponRequest(BaseDto):
    """
    쿠폰 철회 요청

    OpenAPI Schema: coupons-withdraw187298523
    """

    coupon_issue_no: int = Field(..., description="쿠폰 지급 번호")
    reason: str | None = Field(None, description="철회 사유")


class WithdrawCouponBulkRequest(BaseDto):
    """
    쿠폰 번호로 지급 철회 요청 (bulk)

    OpenAPI Schema: coupons-withdraw-bulk1123368312

    참고: issue_start_ymd/issue_end_ymd 는 스펙 example 상 [yyyy, M, d] 정수 배열로 전송됩니다.
    """

    coupon_no: int = Field(..., description="쿠폰 번호")
    issue_start_ymd: list[int] = Field(default_factory=list, description="지급 조회 시작일 ([yyyy, M, d])")
    issue_end_ymd: list[int] = Field(default_factory=list, description="지급 조회 종료일 ([yyyy, M, d])")
    withdraw_reason: str | None = Field(None, description="지급 철회 사유")


class RollbackCouponRequest(BaseDto):
    """
    쿠폰 취소(오프라인 전용) 요청

    OpenAPI Schema: coupons-use-rollback-141309845
    """

    coupon_issue_nos: list[int] = Field(default_factory=list, description="쿠폰 지급 번호 리스트")


class UseStopCouponRequest(BaseDto):
    """
    쿠폰 사용 중지/재개 요청

    OpenAPI Schema: coupons-couponNo-use-stop1789105598
    """

    use_stopped: bool = Field(..., description="쿠폰 사용중지 여부 (사용중지: true, 사용재개: false)")

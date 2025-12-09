"""공통으로 사용하는 모델들"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDate, KstDatetime


class PlatformDisplayInfo(BaseDto):
    """플랫폼별 전시 정보"""

    display_yn: str = Field(..., description="전시여부")
    pc_yn: str = Field(..., description="PC 전시여부")
    mobile_yn: str = Field(..., description="모바일앱 전시여부")
    mobile_web_yn: str = Field(..., description="모바일웹 전시여부")


class PromotionTextInfo(BaseDto):
    """홍보문구 정보"""

    text: str = Field(..., description="홍보문구")
    period_yn: str = Field(..., description="홍보문구 기간설정 유무")
    start_ymd: KstDate | None = Field(None, description="홍보문구 노출 시작 시간")
    end_ymd: KstDate | None = Field(None, description="홍보문구 노출 종료 시간")


class SalePeriodInfo(BaseDto):
    """판매기간 정보"""

    period_type: Literal["REGULAR", "PERIOD"] = Field(..., description="판매기간설정")
    start_ymdt: KstDatetime = Field(..., description="판매 시작 시간")
    end_ymdt: KstDatetime = Field(..., description="판매 종료 시간")


class ImmediateDiscountInfo(BaseDto):
    """즉시할인 정보"""

    unit_type: Literal["AMOUNT", "PERCENT"] = Field(..., description="즉시할인 단위")
    amount: float = Field(..., description="즉시할인 양")
    period_yn: str = Field(..., description="즉시할인 기간설정 여부")
    start_ymdt: KstDatetime | None = Field(None, description="즉시할인 시작 시간")
    end_ymdt: KstDatetime | None = Field(None, description="즉시할인 종료 시간")


class CommissionInfo(BaseDto):
    """판매수수료 정보"""

    type: Literal["PRODUCT", "CATEGORY", "PARTNER", "PURCHASE_PRICE"] = Field(..., description="판매수수료타입")
    rate: float = Field(..., description="수수료율")


class MaxBuyCountInfo(BaseDto):
    """최대 구매 수량 정보"""

    max_buy_person_cnt: int = Field(..., description="1인당 최대 구매 수량")
    max_buy_time_cnt: int = Field(..., description="1회당 최대 구매 수량")
    max_buy_days: int = Field(..., description="최대구매수량 기간 제한 - 기간")
    max_buy_period_cnt: int = Field(..., description="최대구매수량 기간 제한 - 제한 수량")


class CartInfo(BaseDto):
    """장바구니 정보"""

    use_yn: str = Field(..., description="장바구니 사용 여부")
    off_period_yn: str = Field(..., description="장바구니 OFF 기간 설정 여부")
    off_start_ymd: KstDate | None = Field(None, description="장바구니 OFF 시작일")
    off_end_ymd: KstDate | None = Field(None, description="장바구니 OFF 종료일")


class MemberGradeDisplayInfo(BaseDto):
    """회원등급 전시 정보"""

    check: str = Field(..., description="회원등급 전시 체크")
    info: list[Any] = Field(default_factory=list, description="회원등급 정보")


class MemberGroupDisplayInfo(BaseDto):
    """회원그룹 전시 정보"""

    check: str = Field(..., description="회원그룹 전시 체크")
    info: list[Any] = Field(default_factory=list, description="회원그룹 정보")


class PromotionInfo(BaseDto):
    """프로모션 정보"""

    promotion_yn: str = Field(..., description="프로모션 사용 여부")
    additional_discount_yn: str = Field(..., description="추가할인 사용 여부")
    coupon_yn: str = Field(..., description="쿠폰 사용 여부")
    free_gift_yn: str = Field(..., description="사은품 사용 여부")

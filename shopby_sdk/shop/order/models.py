"""Shopby Shop(Client) Order API 모델.

order-shop-public.yml 의 공개(인증 불필요) 엔드포인트 응답 모델 모음.
필드는 snake_case 로 정의하고 BaseDto 가 camelCase alias 를 자동 생성한다.
"""

from typing import Any

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


# ---------------------------------------------------------------------------
# AppCard - 간편결제 카드사 목록 (schema: app-card-cards1239894424)
# ---------------------------------------------------------------------------
class AppCardCard(BaseDto):
    """앱카드 간편결제 카드사."""

    card_name: str = Field(..., description="카드사 명 (예: 신한카드)")
    card_code: str = Field(..., description="간편결제 카드사 코드 (예: 2088)")


class AppCardCardsResponse(BaseDto):
    """앱카드 간편결제 카드사 목록 조회 응답 (schema: app-card-cards1239894424)."""

    cards: list[AppCardCard] = Field(..., description="간편결제 카드 리스트")


# ---------------------------------------------------------------------------
# AppCard - 할부정보 (schema: app-card-inst-plan1540047407)
# ---------------------------------------------------------------------------
class AppCardInstInfo(BaseDto):
    """앱카드 카드사별 할부 정보."""

    card_code: str = Field(..., description="간편결제 카드사 코드 (예: 2004)")
    free_inst_min: float = Field(..., description="무이자할부 가능 최소금액 (예: 0)")
    # spec items 가 oneOf(object/boolean/string/number) 라 정수 개월 수로 단정하지 않고
    # list[Any] 로 둔다. 실데이터는 [1, 2, 3] 형태의 개월 수 배열.
    free_inst_list: list[Any] = Field(
        ..., description="무이자할부 가능 개월 수 (예: [1, 2, 3])"
    )
    inst_min: float = Field(..., description="할부 가능 최소금액 (예: 50000)")
    inst_list: list[Any] = Field(..., description="할부 개월 수 (예: [1, 2, 3])")


class AppCardInstPlanResponse(BaseDto):
    """앱카드 할부정보 조회 응답 (schema: app-card-inst-plan1540047407)."""

    pg: str = Field(..., description="조회 PG 사 명 (예: KGI)")
    inst_info: list[AppCardInstInfo] = Field(..., description="할부정보")


# ---------------------------------------------------------------------------
# Cart - 장바구니 설정 (schema: cart-config868453615)
# ---------------------------------------------------------------------------
class CartConfigResponse(BaseDto):
    """장바구니 설정 값 조회 응답 (schema: cart-config868453615)."""

    storage_period: int | None = Field(
        None, description="장바구니 보관 기간 (최대 30일, nullable)"
    )
    cart_equivalent_option_unit_type: str | None = Field(
        None, description="장바구니 동일 옵션 표기 단위 (예: QUANTITY, nullable)"
    )
    storage_period_no_limit: bool | None = Field(
        None, description="장바구니 보관기간 제한없음 여부 (nullable)"
    )
    storage_max_quantity: int | None = Field(
        None, description="장바구니 보관 수량 (기본 10개, 최대 100개, nullable)"
    )


# ---------------------------------------------------------------------------
# OrderConfiguration - 주문 설정 (schema: order-configs-2077774300)
# ---------------------------------------------------------------------------
class OrderConfigNaverPay(BaseDto):
    """네이버페이 설정 정보."""

    button_key: str = Field(
        ..., description="네이버페이 결제버튼 노출에 필요한 button key"
    )


class OrderConfigVisibleReceiptBtn(BaseDto):
    """영수증 보기 버튼 사용 여부."""

    pg_receipt: bool = Field(..., description="PG사 매출전표")
    specification: bool = Field(..., description="거래명세서")
    specification_brief: bool = Field(..., description="간이 영수증")


class OrderConfigShippingEmptyAutoCancel(BaseDto):
    """나중배송지 주문 자동 취소 설정."""

    use: bool = Field(..., description="나중배송지 주문 자동 취소 설정 여부")
    cancel_days: float | None = Field(
        None,
        description="자동 취소 처리 기간 - 해당 영업일 이후 자동 취소 처리 (미설정 시 null)",
    )


class OrderConfigEscrow(BaseDto):
    """에스크로 설정 정보."""

    escrow_info_key: str | None = Field(
        None, description="에스크로 정보 확인 키 (nullable)"
    )
    logo: str | None = Field(None, description="이니시스 에스크로 표시 로고 (nullable)")
    expose_logo: bool = Field(..., description="에스크로 로고 노출 여부")


class OrderConfigResponse(BaseDto):
    """주문 설정 값 조회 응답 (schema: order-configs-2077774300)."""

    pg_type: str = Field(..., description="pg사 (예: KCP, INICIS, TOSS_PAYMENTS)")
    mall_transfer_ymdt: KstDatetime | None = Field(
        None, description="쇼핑몰 이전 일자"
    )
    # 배송국가 별 구매제한 금액 (개발중). 스펙상 자유 형태 object 라 dict[str, Any].
    purchase_limit_by_country: dict[str, Any] = Field(
        ..., description="배송국가 별 구매제한 금액 (개발중, 예: {CN=100000})"
    )
    shop_specification_fields: list[str] = Field(
        ..., description="거래명세서 쇼핑몰 출력 항목 설정"
    )
    naver_pay: OrderConfigNaverPay | None = Field(
        None,
        description="네이버페이 설정정보 (사용안함 설정이거나 설정이 없을 경우 null)",
    )
    cash_receipt_required: bool = Field(
        ..., description="무통장입금 시 현금영수증 신청 필수 여부"
    )
    use_app_card: bool = Field(..., description="앱카드 사용 여부")
    visible_receipt_btn: OrderConfigVisibleReceiptBtn = Field(
        ..., description="영수증 보기 버튼 사용 여부"
    )
    includes_previous_order: bool = Field(
        ..., description="이전주문 내역 존재 여부"
    )
    shipping_empty_auto_cancel: OrderConfigShippingEmptyAutoCancel | None = Field(
        None, description="나중배송지 주문 자동 취소 설정"
    )
    use_my_pay: bool = Field(..., description="마이페이 사용여부")
    specification_additional_info: str = Field(
        ..., description="거래명세서 하단 추가 정보 (빈값: 사용안함)"
    )
    use_payment_receipt: bool = Field(..., description="결제영수증 사용 여부")
    use_recurring_payment: bool = Field(..., description="몰 정기배송(결제) 사용 여부")
    escrow: OrderConfigEscrow | None = Field(None, description="에스크로 설정 정보")
    use_simple_receipt: bool = Field(..., description="간이영수증 사용 여부")
    recurring_payment_free_gift_issue_type: str = Field(
        ..., description="정기결제 사은품 지급 기준"
    )
    view_shop_specification: bool = Field(
        ..., description="거래명세서 쇼핑몰 노출 설정"
    )
    cash_receipt: bool = Field(..., description="무통장입금 시 현금영수증 사용 여부")


# ---------------------------------------------------------------------------
# ShippingAddress - 배송 enum (schema: shippings-enums-1588224597)
# ---------------------------------------------------------------------------
class ShippingEnumItem(BaseDto):
    """배송 enum 단일 항목 (name/label)."""

    name: str = Field(..., description="Enum Name (예: KR)")
    label: str = Field(..., description="Enum Label (예: 대한민국)")


class ShippingEnumsResponse(BaseDto):
    """배송 enum 정보 조회 응답 (schema: shippings-enums-1588224597)."""

    country_cd: list[ShippingEnumItem] = Field(..., description="국가 코드")
    us_state_cd: list[ShippingEnumItem] = Field(..., description="미국 주(state) 코드")
    jp_state_cd: list[ShippingEnumItem] = Field(..., description="일본 주(state) 코드")
    ca_state_cd: list[ShippingEnumItem] = Field(
        ..., description="캐나다 주(state) 코드"
    )

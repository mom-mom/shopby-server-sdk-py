"""GET /orders/{orderNo} (주문 상세 조회) 응답 모델"""

from typing import Any

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime
from shopby_sdk.clients.order.models.base import (
    Balance,
    ClaimStatusType,
    ClaimType,
    DeliveryCompanyType,
    ExternalPayInfo,
    PaymentInfo,
    PayType,
    PlatformType,
)


class Orderer(BaseDto):
    """주문자 정보"""

    name: str | None = Field(None, description="주문자명")
    contact1: str | None = Field(None, description="연락처1")
    contact2: str | None = Field(None, description="연락처2")
    email: str | None = Field(None, description="이메일")
    refund_account: str | None = Field(None, description="환불계좌")


class Receiver(BaseDto):
    """수령자 정보"""

    name: str | None = Field(None, description="수령자명")
    zip_cd: str | None = Field(None, description="우편번호")
    address: str | None = Field(None, description="주소")
    detail_address: str | None = Field(None, description="상세주소")
    jibun_address: str | None = Field(None, description="지번주소")
    contact1: str | None = Field(None, description="연락처1")
    contact2: str | None = Field(None, description="연락처2")


class Shipping(BaseDto):
    """배송 정보"""

    shipping_no: int | None = Field(None, description="배송번호")
    mall_no: int | None = Field(None, description="몰번호")
    partner_no: int | None = Field(None, description="파트너번호")
    delivery_template_group_no: int | None = Field(None, description="배송템플릿그룹번호")
    delivery_template_no: int | None = Field(None, description="배송템플릿번호")
    delivery_amt: float | None = Field(None, description="배송비")
    adjusted_amt: float | None = Field(None, description="조정금액")
    return_delivery_amt: float | None = Field(None, description="반품배송비")
    remote_delivery_amt: float | None = Field(None, description="도서산간배송비")
    receiver: Receiver | None = Field(None, description="수령자정보")
    delivery_type: str | None = Field(None, description="배송타입")
    prepaid: bool | None = Field(None, description="선불여부")
    requires_shipping: bool | None = Field(None, description="배송필요여부")
    combined: bool | None = Field(None, description="합배송여부")
    devided: bool | None = Field(None, description="분할배송여부")
    original_shipping_no: int | None = Field(None, description="원배송번호")
    invoice_no: str | None = Field(None, description="송장번호")
    customs_id_number: str | None = Field(None, description="통관고유부호")
    delivery_company_type: DeliveryCompanyType | None = Field(None, description="택배사타입")
    delivery_company_type_label: str | None = Field(None, description="택배사라벨")
    uses_shipping_info_later_input: bool | None = Field(None, description="배송지나중입력여부")
    memo: str | None = Field(None, description="배송메모")


class PaymentBalance(BaseDto):
    """결제 금액 정보"""

    pay_amt: float | None = Field(None, description="결제금액")
    main_pay_amt: float | None = Field(None, description="실결제금액")
    sub_pay_amt: float | None = Field(None, description="보조결제금액")


class Payment(BaseDto):
    """결제 정보"""

    no: int | None = Field(None, description="결제번호")
    balance: PaymentBalance | None = Field(None, description="결제금액정보")
    payment_info: PaymentInfo | None = Field(None, description="결제정보")


class ClaimedOption(BaseDto):
    """클레임 옵션"""

    order_option_no: int | None = Field(None, description="주문옵션번호")
    claim_reason_type: str | None = Field(None, description="클레임사유타입")
    claim_reason_detail: str | None = Field(None, description="클레임사유상세")


class ClaimInfo(BaseDto):
    """클레임 정보"""

    claim_no: int | None = Field(None, description="클레임번호")
    claim_ymdt: KstDatetime | None = Field(None, description="클레임일시")
    claim_complete_ymdt: KstDatetime | None = Field(None, description="클레임완료일시")
    claim_type: ClaimType | None = Field(None, description="클레임타입")
    mall_no: int | None = Field(None, description="몰번호")
    member_no: int | None = Field(None, description="회원번호")
    order_no: str | None = Field(None, description="주문번호")
    refund_pay_type: PayType | None = Field(None, description="환불결제수단")
    claim_status_type: ClaimStatusType | None = Field(None, description="클레임상태")
    claim_amt: float | None = Field(None, description="클레임금액")
    return_way_type: str | None = Field(None, description="반품수거방법")
    order_option_nos: list[Any] = Field(default_factory=list, description="주문옵션번호목록")
    responsible_object_type: str | None = Field(None, description="귀책대상")
    claim_reason_type: str | None = Field(None, description="클레임사유타입")
    claim_reason_detail: str | None = Field(None, description="클레임사유상세")
    accumulation_pay_amt: float | None = Field(None, description="복원적립금")
    claimed_options: list[ClaimedOption] = Field(default_factory=list, description="클레임옵션목록")
    withdraw_reason: str | None = Field(None, description="철회사유")
    treatment_status_type: str | None = Field(None, description="처리상태")
    treatment_ymdt: KstDatetime | None = Field(None, description="처리일시")


class OrderDetailResponse(BaseDto):
    """
    주문 상세 조회 응답

    OpenAPI Schema: orders-orderNo-1195378051
    """

    order_no: str | None = Field(None, description="주문번호")
    mall_no: int | None = Field(None, description="몰번호")
    pg_type: str | None = Field(None, description="PG사")
    pay_type: PayType | None = Field(None, description="결제수단")
    platform_type: PlatformType | None = Field(None, description="플랫폼타입")
    member_no: int | None = Field(None, description="회원번호")
    is_member_order: bool | None = Field(None, description="회원주문여부")
    last_main_pay_amt: float | None = Field(None, description="최종실결제금액")
    currency_code: str | None = Field(None, description="통화코드")
    exchange_rate: float | None = Field(None, description="환율")
    orderer: Orderer | None = Field(None, description="주문자정보")
    first_balance: Balance | None = Field(None, description="최초결제정보")
    last_balance: Balance | None = Field(None, description="최종결제정보")
    register_ymdt: KstDatetime | None = Field(None, description="등록일시")
    update_ymdt: KstDatetime | None = Field(None, description="수정일시")
    extra_json: str | None = Field(None, description="추가정보JSON")
    channel_type: str | None = Field(None, description="채널타입")
    tracking_key: str | None = Field(None, description="추적키")
    external_order_no: str | None = Field(None, description="외부주문번호")
    order_memo: str | None = Field(None, description="주문메모")
    first_pay_ymdt: KstDatetime | None = Field(None, description="최초결제일시")
    order_products: list[dict[str, Any]] = Field(default_factory=list, description="주문상품목록")
    shippings: list[Shipping] = Field(default_factory=list, description="배송정보목록")
    payments: list[Payment] = Field(default_factory=list, description="결제정보목록")
    claim_infos: list[ClaimInfo] = Field(default_factory=list, description="클레임정보목록")
    first_external_pay_infos: list[ExternalPayInfo] = Field(default_factory=list, description="최초외부결제정보")
    last_external_pay_infos: list[ExternalPayInfo] = Field(default_factory=list, description="최종외부결제정보")

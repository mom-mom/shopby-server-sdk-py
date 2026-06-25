"""Order API 추가 엔드포인트용 요청/응답 모델

35개 미구현 엔드포인트(무통장입금, 앱카드, 장바구니, 배송, 이전주문, 정기결제,
배송지, 업무메시지, 쿠폰, 주문상태변경 등)의 request/response 모델 정의.
기존 base.py / list.py / detail.py 의 enum·모델을 재사용하며, 신규 모델만 추가한다.
"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime
from shopby_sdk.clients.order.models.base import (
    OrderStatusType,
    PlatformType,
)


# ============================================
#  추가 Enum 타입 정의
# ============================================

CartSearchDateType = Literal["REGISTER_YMDT", "UPDATE_YMDT"]
"""장바구니 날짜 검색 조건"""

DeliverySearchType = Literal[
    "ALL",
    "DELIVERY_NO",
    "ORDER_NO",
    "MALL_PRODUCT_NO",
]
"""배송 조회 검색 유형 (배송번호, 주문번호, 상품번호)"""

PreviousOrderSearchType = Literal[
    "ORDER_NO",
    "ORDERER_NAME",
    "ORDERER_CONTACT1",
    "PRODUCT_NAME",
    "RECEIVER_NAME",
    "RECEIVER_CONTACT1",
    "MEMBER_NO",
]
"""이전주문 검색 타입"""

RecurringPaymentSearchType = Literal["RECURRING_PAYMENT_NO"]
"""정기결제 검색 타입"""

ShippingAddressType = Literal[
    "BOOK",
    "RECENT",
    "RECURRING_PAYMENT",
    "RECURRING_PAYMENT_PRESENT",
]
"""배송지 타입"""

TaskMessageDateType = Literal["REGISTER", "UPDATE", "COMPLETE"]
"""업무메시지 기간 검색 타입"""

TaskMessageTargetType = Literal["PARTNER", "SERVICE"]
"""업무메시지 담당자 타입"""

PgType = Literal[
    "DUMMY",
    "PAYCO",
    "PAYPAL",
    "STRIPE",
    "KCP",
    "INICIS",
    "NONE",
    "KCP_MOBILE",
    "KCP_APP",
    "NAVER_PAY",
    "LIIVMATE",
    "PAYPALPRO",
    "ATHOR_NET",
    "KAKAO_PAY",
    "NAVER_EASY_PAY",
    "LG_U_PLUS",
    "TOSS_PAYMENTS",
    "CHAI",
    "SMARTRO_PAY",
    "NICEPAY",
    "MY_PAY",
    "EXIMBAY_GLOBAL",
    "EASY_PAY",
    "GALAXIA_MONEY_TREE",
    "KSNET",
    "EASY_PAY_OVERSEAS",
    "BLUE_WALNUT",
    "HMG_PAY_H",
    "HMG_PAY_K",
    "APP_CARD",
    "TOSS_EASY_PAY",
    "VERITRANS",
]
"""PG 구분"""


# ============================================
#  무통장 미입금 주문 (/accounts/orders)
# ============================================


class AccountOrderProduct(BaseDto):
    """무통장 주문 상품"""

    product_name: str | None = Field(None, description="상품명")


class AccountOrder(BaseDto):
    """
    무통장 미입금 주문

    OpenAPI Schema: accounts-orders-1235877951 (item)
    """

    order_no: str | None = Field(None, description="주문번호")
    orderer_name: str | None = Field(None, description="주문자 이름")
    orderer_email: str | None = Field(None, description="주문자 이메일")
    orderer_contact: str | None = Field(None, description="주문자 연락처")
    register_ymdt: KstDatetime | None = Field(None, description="주문일자")
    remitter_name: str | None = Field(None, description="입금자명")
    account: str | None = Field(None, description="입금 계좌번호")
    bank_name: str | None = Field(None, description="입금 은행명")
    bank_amt: float | None = Field(None, description="주문금액")
    products: list[AccountOrderProduct] = Field(default_factory=list, description="상품 목록")


class AccountOrderConfirmRequest(BaseDto):
    """무통장 입금 확인 요청 항목"""

    order_no: str = Field(..., description="주문번호")


class AccountOrderConfirmResult(BaseDto):
    """
    무통장 입금 확인 결과

    OpenAPI Schema: accounts-orders-confirmation1583574419 (item)
    """

    order_no: str | None = Field(None, description="주문번호")
    result: bool | None = Field(None, description="처리결과")
    description: str | None = Field(None, description="설명")


# ============================================
#  앱카드 (/app-card)
# ============================================


class AppCardPaymentKey(BaseDto):
    """
    앱카드 결제 키 조회 응답

    OpenAPI Schema: app-card-payment-key2056412445
    """

    pg_type: PgType | None = Field(None, description="PG 구분")
    key: str | None = Field(None, description="PG 결제 키")
    etc_infos: dict[str, Any] | None = Field(None, description="추가 정보")


# ============================================
#  장바구니 (/cart)
# ============================================


class PurchaserInput(BaseDto):
    """사용자 입력형 옵션"""

    input_no: int | None = Field(None, description="사용자 입력 번호")
    input_label: str | None = Field(None, description="사용자 입력 항목")
    input_value: str | None = Field(None, description="사용자 입력 문구")
    required: bool | None = Field(None, description="사용자 입력 필수 여부")


class CartItem(BaseDto):
    """장바구니 항목"""

    cart_no: int | None = Field(None, description="장바구니 번호")
    member_no: int | None = Field(None, description="회원 번호")
    mall_product_no: int | None = Field(None, description="상품 번호")
    mall_option_no: int | None = Field(None, description="옵션 번호")
    order_option_type: str | None = Field(None, description="옵션 형태")
    payment_period_type: str | None = Field(None, description="결제 주기")
    order_cnt: int | None = Field(None, description="주문 수량")
    group_id: str | None = Field(None, description="장바구니 그룹 아이디")
    purchaser_inputs: list[PurchaserInput] = Field(default_factory=list, description="사용자 입력형 옵션")
    register_ymdt: KstDatetime | None = Field(None, description="등록 일시")
    update_ymdt: KstDatetime | None = Field(None, description="수정 일시")


class CartResponse(BaseDto):
    """
    장바구니 조회 응답

    OpenAPI Schema: cart-1890208080
    """

    total_count: int = Field(..., description="장바구니 크기")
    contents: list[CartItem] = Field(default_factory=list, description="장바구니 목록")


# ============================================
#  위시리스트 (/wish)
# ============================================


class WishItem(BaseDto):
    """위시리스트 항목"""

    wish_no: int | None = Field(None, description="위시리스트 번호")
    member_no: int | None = Field(None, description="회원 번호")
    mall_product_no: int | None = Field(None, description="상품 번호")
    mall_option_no: int | None = Field(None, description="옵션 번호")
    order_option_type: str | None = Field(None, description="옵션 형태")
    order_cnt: int | None = Field(None, description="주문 수량")
    purchaser_inputs: list[PurchaserInput] = Field(default_factory=list, description="사용자 입력형 옵션")
    register_ymdt: KstDatetime | None = Field(None, description="등록 일시")
    update_ymdt: KstDatetime | None = Field(None, description="수정 일시")


class WishResponse(BaseDto):
    """
    위시리스트 조회 응답

    OpenAPI Schema: wish53840767
    """

    total_count: int = Field(..., description="위시리스트 크기")
    contents: list[WishItem] = Field(default_factory=list, description="위시리스트 목록")


# ============================================
#  배송번호 기준 주문 조회 (/orders/deliveries)
# ============================================


class OrderDeliveryItem(BaseDto):
    """
    배송번호 기준 주문 조회 항목

    중첩된 주문/주문상품 구조가 매우 깊어 핵심 배송 필드만 명시하고,
    nested 컬렉션은 dict[str, Any]로 처리한다.
    """

    delivery_no: int | None = Field(None, description="배송번호")
    original_delivery_no: int | None = Field(None, description="원배송번호")
    encrypted_shipping_no: str | None = Field(None, description="암호화 된 배송번호")
    invoice_no: str | None = Field(None, description="송장번호")
    invoice_register_ymdt: KstDatetime | None = Field(None, description="송장번호등록일시")
    delivery_company_type: str | None = Field(None, description="택배사타입")
    delivery_type: str | None = Field(None, description="배송구분")
    delivery_template_no: int | None = Field(None, description="배송 템플릿 번호")
    delivery_template_group_no: int | None = Field(None, description="배송 템플릿 그룹번호")
    delivery_condition_no: int | None = Field(None, description="배송 조건 번호")
    delivery_amt: float | None = Field(None, description="배송비")
    return_delivery_amt: float | None = Field(None, description="반품배송비")
    remote_delivery_amt: float | None = Field(None, description="추가배송비")
    adjusted_amt: float | None = Field(None, description="조정 금액")
    delivery_yn: str | None = Field(None, description="배송 여부")
    combine_delivery_yn: str | None = Field(None, description="묶음배송 여부")
    divide_delivery_yn: str | None = Field(None, description="분할배송 여부")
    delivery_combination_yn: str | None = Field(None, description="묶음배송 가능 여부")
    delivery_amt_in_advance_yn: str | None = Field(None, description="배송비 선결제 여부")
    shipping_method_type: str | None = Field(None, description="배송서비스타입")
    uses_shipping_info_later_input: bool | None = Field(None, description="배송지 나중입력 여부")
    receiver_name: str | None = Field(None, description="수령자 명")
    receiver_contact1: str | None = Field(None, description="연락처1")
    receiver_contact2: str | None = Field(None, description="연락처2")
    receiver_zip_cd: str | None = Field(None, description="배송지 우편 번호")
    receiver_address: str | None = Field(None, description="배송지 주소")
    receiver_jibun_address: str | None = Field(None, description="배송지 지번")
    receiver_detail_address: str | None = Field(None, description="배송지 상세 주소")
    receiver_state: str | None = Field(None, description="(해외) 주")
    receiver_city: str | None = Field(None, description="(해외) 도시")
    country_cd: str | None = Field(None, description="국가코드")
    customs_id_number: str | None = Field(None, description="개인고유통관부호")
    delivery_memo: str | None = Field(None, description="배송메모")
    shipping_etc_info: dict[str, Any] | None = Field(None, description="해외배송지 기타정보")
    order_products: list[dict[str, Any]] = Field(default_factory=list, description="주문 상품")
    orders: list[dict[str, Any]] = Field(default_factory=list, description="주문 목록")


class OrderDeliveriesResponse(BaseDto):
    """
    주문 조회하기 (배송번호 기준) 응답

    OpenAPI Schema: orders-deliveries-1070248065
    """

    total_count: int = Field(..., description="총 건수")
    contents: list[OrderDeliveryItem] = Field(default_factory=list, description="배송 목록")


# ============================================
#  이전주문 (/previous-orders)
# ============================================


class PreviousOrderPayDetail(BaseDto):
    """결제 상세"""

    pay_type: str | None = Field(None, description="결제방법")
    pay_type_label: str | None = Field(None, description="결제방법 라벨")
    order_ymdt: KstDatetime | None = Field(None, description="주문일시")
    pay_ymdt: KstDatetime | None = Field(None, description="결제일시")
    bank: str | None = Field(None, description="은행명")
    account: str | None = Field(None, description="계좌 번호")
    account_holder: str | None = Field(None, description="예금주")
    depositor: str | None = Field(None, description="입금자")
    discount_amt: float | None = Field(None, description="할인 금액")


class PreviousOrderItem(BaseDto):
    """
    이전주문 검색 항목

    중첩 구조(orderer/receiver/payment 등)는 dict[str, Any]로 처리한다.

    OpenAPI Schema: previous-orders1028372904 (item)
    """

    order_no: str | None = Field(None, description="주문 번호")
    mall_no: int | None = Field(None, description="몰 번호")
    accumulation_amt: float | None = Field(None, description="적립혜택")
    orderer: dict[str, Any] | None = Field(None, description="주문자 정보")
    receiver: list[dict[str, Any]] = Field(default_factory=list, description="수령자 정보")
    order_product: list[dict[str, Any]] = Field(default_factory=list, description="주문상품 정보")
    payment_method: dict[str, Any] | None = Field(None, description="결제 정보")
    first_payment: dict[str, Any] | None = Field(None, description="최초 결제 정보")
    last_payment: dict[str, Any] | None = Field(None, description="최종 결제 정보")
    refund: dict[str, Any] | None = Field(None, description="환불 정보")
    admin_memo: list[dict[str, Any]] = Field(default_factory=list, description="관리자 메모")


class PreviousOrdersResponse(BaseDto):
    """
    이전주문 검색 응답

    OpenAPI Schema: previous-orders1028372904
    """

    total_count: int = Field(..., description="전체 주문수")
    contents: list[PreviousOrderItem] = Field(default_factory=list, description="이전주문 목록")


class PreviousOrderRegisterItem(BaseDto):
    """
    이전주문 등록 항목

    OpenAPI Schema: previous-orders-1128182648 (item)
    """

    order_no: str | None = Field(None, description="주문 번호")
    member_no: int | None = Field(None, description="회원번호")
    member_id: str | None = Field(None, description="아이디")
    temporary_password: str | None = Field(None, description="임시 비밀번호")
    order_ymdt: KstDatetime | None = Field(None, description="주문 일시")
    pay_ymdt: KstDatetime | None = Field(None, description="결제일시")
    pay_type: str | None = Field(None, description="결제방법")
    order_status_type: str | None = Field(None, description="주문상태")
    platform_type: str | None = Field(None, description="플랫폼 구분")
    orderer_name: str | None = Field(None, description="주문자명")
    orderer_email: str | None = Field(None, description="주문자 이메일")
    orderer_phone_number: str | None = Field(None, description="주문자 전화번호")
    orderer_mobile_number: str | None = Field(None, description="주문자 휴대폰번호")
    receiver_name: str | None = Field(None, description="수령자명")
    receiver_phone_number: str | None = Field(None, description="수령자 전화번호")
    receiver_mobile_number: str | None = Field(None, description="수령자 휴대폰번호")
    receiver_zip_cd: str | None = Field(None, description="우편번호")
    receiver_address: str | None = Field(None, description="배송지 주소")
    receiver_detail_address: str | None = Field(None, description="배송지 상세 주소")
    delivery_info: str | None = Field(None, description="배송지 정보")
    delivery_memo: str | None = Field(None, description="배송메모")
    delivery_company_type: str | None = Field(None, description="택배사")
    invoice_no: str | None = Field(None, description="송장번호")
    customs_id_number: str | None = Field(None, description="개인통관번호")
    product_name: str | None = Field(None, description="상품명")
    option_name: str | None = Field(None, description="옵션명")
    option_value: str | None = Field(None, description="옵션값")
    order_cnt: int | None = Field(None, description="수량")
    sale_price: float | None = Field(None, description="상품합계")
    purchase_price: float | None = Field(None, description="주문금액")
    order_memo: str | None = Field(None, description="주문메모")
    pay_detail: PreviousOrderPayDetail | None = Field(None, description="결제 상세")
    delivery_amt: float | None = Field(None, description="기본 배송비")
    remote_delivery_amt: float | None = Field(None, description="지역별 배송비")
    accumulation_amt: float | None = Field(None, description="적립금 사용 금액")
    first_pay_amt: float | None = Field(None, description="최초 결제금액")
    first_main_pay_amt: float | None = Field(None, description="최초 실 결제금액")
    first_sub_pay_amt: float | None = Field(None, description="최초 적립금사용")
    first_standard_amt: float | None = Field(None, description="최초 판매금액")
    first_delivery_amt: float | None = Field(None, description="최초 배송비")
    first_remote_delivery_amt: float | None = Field(None, description="최초 지역배송비")
    first_discount_amt: float | None = Field(None, description="최초 할인혜택")
    last_pay_amt: float | None = Field(None, description="최종 결제금액")
    last_main_pay_amt: float | None = Field(None, description="최종 실 결제금액")
    last_sub_pay_amt: float | None = Field(None, description="최종 적립금사용")
    last_standard_amt: float | None = Field(None, description="최종 판매금액")
    last_delivery_amt: float | None = Field(None, description="최종 배송비")
    last_remote_delivery_amt: float | None = Field(None, description="최종 지역배송비")
    last_discount_amt: float | None = Field(None, description="최종 할인혜택")
    refund_type: str | None = Field(None, description="환불방법")
    refund_amt: float | None = Field(None, description="환불금액")
    refund_bank: str | None = Field(None, description="환불 은행명")
    refund_bank_account: str | None = Field(None, description="환불 계좌")
    refund_bank_depositor_name: str | None = Field(None, description="환불 계좌 예금주")
    refund_complete_ymdt: KstDatetime | None = Field(None, description="환불처리일시")
    member_grade_names: list[str] = Field(default_factory=list, description="회원등급")
    purchaser_inputs: list[dict[str, Any]] = Field(default_factory=list, description="사용자 입력형 옵션")
    admin_memo: list[dict[str, Any]] = Field(default_factory=list, description="관리자 메모")


class PreviousOrderRegisterResult(BaseDto):
    """
    이전주문 등록 결과

    OpenAPI Schema: previous-orders-2097246096
    """

    count: int = Field(..., description="등록 개수")


class PreviousOrderDeleteResult(BaseDto):
    """
    이전주문 삭제 결과

    OpenAPI Schema: previous-orders-delete-1499897203
    """

    count: int = Field(..., description="삭제 개수")


class PreviousOrderDeleteByOrderNosRequest(BaseDto):
    """
    이전주문 삭제 요청 (주문번호 리스트)

    OpenAPI Schema: previous-orders-delete-by-order-nos-565536975
    """

    order_nos: list[str] = Field(default_factory=list, description="주문 번호 리스트")


# ============================================
#  정기결제(배송) (/recurring-payments)
# ============================================


class RecurringPaymentItem(BaseDto):
    """정기결제(배송) 항목"""

    recurring_payment_no: int | None = Field(None, description="신청번호")
    recurring_payment_group_no: str | None = Field(None, description="정기결제 그룹 번호")
    recurring_payment_status_type: str | None = Field(None, description="이용상태")
    member_no: int | None = Field(None, description="회원번호")
    mall_no: int | None = Field(None, description="쇼핑몰 번호")
    product_no: int | None = Field(None, description="상품번호")
    product_name: str | None = Field(None, description="상품명")
    option_no: int | None = Field(None, description="옵션관리번호")
    option_name: str | None = Field(None, description="옵션명")
    option_value: str | None = Field(None, description="옵션값")
    order_cnt: int | None = Field(None, description="수량")
    standard_amt: float | None = Field(None, description="판매가")
    buy_amt: float | None = Field(None, description="할인적용가")
    discount_amt: float | None = Field(None, description="정기결제(배송) 즉시할인")
    round: int | None = Field(None, description="배송 회차")
    last_round: int | None = Field(None, description="종료 회차")
    delivery_cycle_type: str | None = Field(None, description="배송주기(월/일)")
    delivery_cycle: int | None = Field(None, description="배송주기")
    delivery_date: int | None = Field(None, description="배송 예정일")
    delivery_day_of_week: str | None = Field(None, description="배송 예정 요일")
    next_recurring_payment_date: str | None = Field(None, description="다음 배송예정일")
    register_ymd: str | None = Field(None, description="신청일")
    pause_ymd: str | None = Field(None, description="일시정지 일자")
    close_ymd: str | None = Field(None, description="해지일")
    close_reason: str | None = Field(None, description="해지사유")
    close_reason_detail: str | None = Field(None, description="해지 상세사유")


class RecurringPaymentsResponse(BaseDto):
    """
    정기결제(배송) 조회 응답

    OpenAPI Schema: recurring-payments-20916618
    """

    total_count: int = Field(..., description="검색 결과 수")
    contents: list[RecurringPaymentItem] = Field(default_factory=list, description="검색 결과")


# ============================================
#  배송지 (/shipping-addresses)
# ============================================


class ShippingAddressItem(BaseDto):
    """배송지 항목"""

    address_no: int | None = Field(None, description="배송지 번호")
    address_type: str | None = Field(None, description="배송지타입")
    address_name: str | None = Field(None, description="주소록명")
    address_memo: str | None = Field(None, description="배송지 메모")
    member_no: int | None = Field(None, description="회원 번호")
    external_member_no: str | None = Field(None, description="외부회원 번호")
    mall_no: int | None = Field(None, description="몰번호")
    default: bool | None = Field(None, description="기본 배송지 여부")
    receiver_name: str | None = Field(None, description="수령자 명")
    receiver_contact1: str | None = Field(None, description="연락처1")
    receiver_contact2: str | None = Field(None, description="연락처2")
    receiver_zip_cd: str | None = Field(None, description="배송지 우편 번호")
    receiver_address: str | None = Field(None, description="배송지 주소")
    receiver_jibun_address: str | None = Field(None, description="배송지 지번")
    receiver_detail_address: str | None = Field(None, description="배송지 상세 주소")
    receiver_state: str | None = Field(None, description="주/지역")
    receiver_city: str | None = Field(None, description="도시")
    country_cd: str | None = Field(None, description="국가코드")
    customs_id_number: str | None = Field(None, description="개인고유통관부호")
    shipping_etc_info: str | None = Field(None, description="해외배송지 기타정보")
    last_use_ymdt: KstDatetime | None = Field(None, description="배송지 마지막 사용일")
    register_ymdt: KstDatetime | None = Field(None, description="배송지 등록일")


class ShippingAddressesResponse(BaseDto):
    """
    배송지 조회 응답

    OpenAPI Schema: shipping-addresses-1680627517
    """

    total_count: int = Field(..., description="총 건수")
    contents: list[ShippingAddressItem] = Field(default_factory=list, description="주소지 목록")


# ============================================
#  쿠폰 (/orders/coupons)
# ============================================


class CouponProductItem(BaseDto):
    """쿠폰 계산 요청 상품"""

    mall_product_no: int = Field(..., description="상품 번호")
    mall_option_no: int = Field(..., description="옵션 번호")
    order_cnt: int = Field(..., description="주문 수량")


class CouponAvailableRequest(BaseDto):
    """
    사용 가능 쿠폰 리스트 조회 요청

    OpenAPI Schema: orders-coupons-available131247733
    """

    member_no: int = Field(..., description="회원 번호")
    products: list[CouponProductItem] = Field(default_factory=list, description="상품 목록")
    platform_type: PlatformType | None = Field(None, description="플랫폼 타입 (기본값: PC)")
    channel_type: str | None = Field(None, description="채널 타입 (NAVER_EP, PAYCO 등)")


class CouponProductSelection(BaseDto):
    """쿠폰 계산용 상품 선택"""

    product_no: int = Field(..., description="상품 번호")
    coupon_issue_no: int = Field(..., description="쿠폰 발급 번호")


class CouponCalculateRequest(BaseDto):
    """
    쿠폰 적용 금액 계산 요청

    OpenAPI Schema: orders-coupons-calculate-264497323
    """

    member_no: int = Field(..., description="회원 번호")
    products: list[CouponProductItem] = Field(default_factory=list, description="상품 목록")
    product_coupons: list[CouponProductSelection] = Field(default_factory=list, description="상품 쿠폰 목록")
    cart_coupon_issue_no: int | None = Field(None, description="장바구니 쿠폰 발급 번호")
    promotion_code: str | None = Field(None, description="프로모션 코드")
    platform_type: PlatformType | None = Field(None, description="플랫폼 타입 (기본값: PC)")
    channel_type: str | None = Field(None, description="채널 타입 (NAVER_EP, PAYCO 등)")


class CouponInfo(BaseDto):
    """쿠폰 정보"""

    coupon_no: int | None = Field(None, description="쿠폰 번호")
    coupon_issue_no: int | None = Field(None, description="쿠폰 발급 번호")
    coupon_name: str | None = Field(None, description="쿠폰명")
    coupon_discount_type: str | None = Field(None, description="쿠폰 할인 타입")
    discount_rate: float | None = Field(None, description="할인율")
    discount_amt: float | None = Field(None, description="할인 금액")
    max_discount_amt: float | None = Field(None, description="최대 할인 금액")
    min_sale_price: float | None = Field(None, description="최소 판매 금액")
    free_delivery: bool | None = Field(None, description="무료 배송 여부")
    skips_accumulation: bool | None = Field(None, description="적립금 제외 여부")
    use_end_ymdt: KstDatetime | None = Field(None, description="사용 종료 일시")
    usable: bool | None = Field(None, description="사용 가능 여부")
    reason: str | None = Field(None, description="사용 불가 사유")


class CouponProductResult(BaseDto):
    """쿠폰 적용 상품 결과"""

    product_no: int | None = Field(None, description="상품 번호")
    product_name: str | None = Field(None, description="상품명")
    brand_name: str | None = Field(None, description="브랜드명")
    main_option: str | None = Field(None, description="대표 옵션")
    option_cnt: int | None = Field(None, description="옵션 수")
    total_order_cnt: int | None = Field(None, description="총 주문 수량")
    buy_amt: float | None = Field(None, description="구매 금액")
    product_coupon_discount_amt: float | None = Field(None, description="상품 쿠폰 할인 금액")
    product_coupons: list[CouponInfo] = Field(default_factory=list, description="상품 쿠폰 목록")
    product_plus_coupons: list[dict[str, Any]] = Field(default_factory=list, description="상품 플러스 쿠폰 목록")
    invalid_product_coupons: list[dict[str, Any]] = Field(default_factory=list, description="사용 불가 상품 쿠폰 목록")
    option_inputs: list[dict[str, Any]] = Field(default_factory=list, description="사용자 입력 옵션")


class CouponAvailableResponse(BaseDto):
    """
    사용 가능 쿠폰 / 쿠폰 적용 금액 계산 응답

    OpenAPI Schema: orders-coupons-available317527498
    """

    cart_amt: float | None = Field(None, description="장바구니 금액")
    delivery_amt: float | None = Field(None, description="배송비")
    cart_coupon_discount_amt: float | None = Field(None, description="장바구니 쿠폰 할인 금액")
    delivery_coupon_discount_amt: float | None = Field(None, description="배송 쿠폰 할인 금액")
    product_coupon_discount_amt: float | None = Field(None, description="상품 쿠폰 할인 금액")
    cart_coupons: list[CouponInfo] = Field(default_factory=list, description="장바구니 쿠폰 목록")
    products: list[CouponProductResult] = Field(default_factory=list, description="상품 목록")


# ============================================
#  주문 상태 변경 (/orders/...)
# ============================================


class ChangeStatusItem(BaseDto):
    """주문 상태 일괄 변경 항목"""

    shipping_no: int = Field(..., description="배송번호")
    delivery_company_type: str | None = Field(None, description="택배사타입")
    invoice_no: str | None = Field(None, description="송장번호")


class ChangeStatusByShippingNoRequest(BaseDto):
    """
    주문 상태 일괄 변경 요청

    OpenAPI Schema: orders-change-status-by-shipping-no-236918478
    """

    order_status_type: OrderStatusType = Field(..., description="주문상태")
    change_status_list: list[ChangeStatusItem] = Field(default_factory=list, description="변경 목록")


class ChangeStatusFailure(BaseDto):
    """주문 상태 변경 실패 항목"""

    original_request: dict[str, Any] | None = Field(None, description="최초 요청 정보")
    error_code: str | None = Field(None, description="에러코드")
    error_message: str | None = Field(None, description="에러메세지")


class ChangeStatusByShippingNoResponse(BaseDto):
    """
    주문 상태 일괄 변경 응답

    OpenAPI Schema: orders-change-status-by-shipping-no1542267718
    """

    total_count: int | None = Field(None, description="총 처리 건 수")
    success_count: int | None = Field(None, description="성공 건 수")
    fail_count: int | None = Field(None, description="실패 건 수")
    failures: list[ChangeStatusFailure] = Field(default_factory=list, description="실패 목록")


class DeliveryInvoiceItem(BaseDto):
    """배송중 처리/송장 항목 (배송중 변경, 배송준비중 변경)"""

    order_product_option_no: int = Field(..., description="주문상품옵션번호")
    delivery_company_type: str | None = Field(None, description="택배사타입")
    invoice_no: str | None = Field(None, description="송장번호")


class HoldDeliveryRequest(BaseDto):
    """
    배송보류 처리 요청

    OpenAPI Schema: orders-hold-delivery1280955926
    """

    order_option_nos: list[int] = Field(default_factory=list, description="주문옵션번호 목록")
    hold_delivery_reason: str | None = Field(None, description="배송지연사유")
    delivery_expected_ymdt: str | None = Field(None, description="배송예상일자")
    notification_types: list[str] = Field(default_factory=list, description="알림 설정")


class ReserveToNormalRequest(BaseDto):
    """
    예약 주문 일반주문으로 변경 요청

    OpenAPI Schema: orders-reserve-to-normal395982850
    """

    order_option_nos: list[int] = Field(default_factory=list, description="예약 주문의 주문옵션번호")


class OrderExtraDataItem(BaseDto):
    """
    주문 추가정보 항목

    OpenAPI Schema: orders-extra-data-1305470581 (item)
    """

    order_no: str = Field(..., description="주문번호")
    key: str = Field(..., description="Key")
    value: str = Field(..., description="Value")


class CashReceiptIssuanceItem(BaseDto):
    """
    현금영수증 발행결과 항목

    OpenAPI Schema: orders-cash-receipt1742593779 (item)
    """

    order_no: str = Field(..., description="주문번호")
    cash_receipt_issue_no: str = Field(..., description="현금영수증 발행번호")
    send_state: str = Field(..., description="현금영수증 결과코드")


class TaxInvoiceIssuanceItem(BaseDto):
    """
    세금계산서 발행결과 항목

    OpenAPI Schema: orders-tax-invoice-872144232 (item)
    """

    order_no: str = Field(..., description="주문번호")
    tax_invoice_issue_no: str = Field(..., description="세금계산서 발행번호")
    send_state: str = Field(..., description="세금계산서 결과코드")


class UpdateInvoiceItem(BaseDto):
    """
    송장번호 변경 요청 항목

    OpenAPI Schema: orders-update-invoices-96635585 (item)
    """

    shipping_no: int = Field(..., description="배송번호")
    delivery_company_type: str | None = Field(None, description="택배사")
    invoice_no: str | None = Field(None, description="송장번호")


class UpdateInvoiceResult(BaseDto):
    """
    송장번호 변경 결과 항목

    OpenAPI Schema: orders-update-invoices-1079341162 (item)
    """

    shipping_no: int | None = Field(None, description="배송번호")
    delivery_company_type: str | None = Field(None, description="택배사타입")
    invoice_no: str | None = Field(None, description="송장번호")
    success: bool | None = Field(None, description="성공 여부")
    fail_message: str | None = Field(None, description="요청 실패 사유")


# ============================================
#  업무 메시지 (/task-messages)
# ============================================


class UploadedFileInfo(BaseDto):
    """첨부파일 정보"""

    original_file_name: str | None = Field(None, description="원본 파일명")
    uploaded_file_name: str | None = Field(None, description="업로드 파일명")


class TaskMessageItem(BaseDto):
    """업무메시지 항목"""

    no: int | None = Field(None, description="업무메시지 번호")
    order_no: str | None = Field(None, description="주문번호")
    order_product_option_no: int | None = Field(None, description="주문옵션 번호")
    product_name: str | None = Field(None, description="상품이름")
    task_message_type: str | None = Field(None, description="업무메시지 유형")
    task_message_status_type: str | None = Field(None, description="진행상황")
    task_message_channel_type: str | None = Field(None, description="메시지 작성 채널")
    content: str | None = Field(None, description="내용")
    from_target_no: int | None = Field(None, description="등록자 번호")
    from_target_type: str | None = Field(None, description="등록자 타입")
    to_target_no: int | None = Field(None, description="담당자 번호")
    to_target_type: str | None = Field(None, description="담당자 타입")
    register_info: dict[str, Any] | None = Field(None, description="등록정보")
    completed_info: dict[str, Any] | None = Field(None, description="완료정보")
    update_ymdt: KstDatetime | None = Field(None, description="수정일시")
    uploaded_file_infos: list[UploadedFileInfo] = Field(default_factory=list, description="첨부파일 정보")
    task_message_details: list[dict[str, Any]] = Field(default_factory=list, description="업무메세지 상세정보")


class TaskMessagesResponse(BaseDto):
    """
    업무 메시지 조회 응답

    OpenAPI Schema: task-messages501294015
    """

    total_count: int = Field(..., description="총 수량")
    items: list[TaskMessageItem] = Field(default_factory=list, description="주문 내역")


class TaskMessageCreateRequest(BaseDto):
    """
    업무 메시지 등록 요청

    OpenAPI Schema: task-messages-1424864304
    """

    order_no: str = Field(..., description="주문번호")
    order_product_option_no: int = Field(..., description="주문옵션번호")
    task_message_type: str = Field(..., description="업무메시지 유형")
    content: str = Field(..., description="내용")
    to_target_type: TaskMessageTargetType = Field(..., description="담당자 타입")
    to_target_no: int | None = Field(None, description="담당자 번호")
    from_target_type: str | None = Field(None, description="메시지를 작성한 담당자 타입")
    from_target_no: int | None = Field(None, description="메시지를 작성한 담당자 번호")
    task_message_status_type: str | None = Field(None, description="진행상황")
    register_admin_no: int | None = Field(None, description="관리자 번호")
    product_name: str | None = Field(None, description="상품 이름")
    uploaded_file_infos: list[UploadedFileInfo] = Field(default_factory=list, description="첨부파일 정보")


class TaskMessageCreateResult(BaseDto):
    """
    업무 메시지 등록 결과

    OpenAPI Schema: task-messages27727223
    """

    task_message_no: int = Field(..., description="업무메시지 번호")


class TaskMessageUpdateRequest(BaseDto):
    """
    업무 메시지 수정 요청

    OpenAPI Schema: task-messages-taskMessageNo-452177317
    """

    order_product_option_no: int | None = Field(None, description="주문옵션번호")
    task_message_type: str | None = Field(None, description="업무메시지 유형")
    content: str | None = Field(None, description="내용")
    to_target_type: TaskMessageTargetType | None = Field(None, description="담당자 타입")
    to_target_no: int | None = Field(None, description="담당자 번호")
    uploaded_file_infos: list[UploadedFileInfo] = Field(default_factory=list, description="첨부파일 정보")


class TaskMessageDetailCreateRequest(BaseDto):
    """
    상세 업무 메시지 등록 요청

    OpenAPI Schema: task-messages-taskMessageNo-details-1223057146
    """

    content: str = Field(..., description="내용")
    completion: bool | None = Field(None, description="처리완료여부")
    register_admin_no: int | None = Field(None, description="관리자번호")
    register_admin_name: str | None = Field(None, description="메시지를 작성한 담당자 이름")
    uploaded_file_infos: list[UploadedFileInfo] = Field(default_factory=list, description="첨부파일 정보")


class TaskMessageDetailCreateResult(BaseDto):
    """
    상세 업무 메시지 등록 결과

    OpenAPI Schema: task-messages-taskMessageNo-details326404204
    """

    task_message_detail_no: int = Field(..., description="상세 업무메시지 번호")


class TaskMessageDetailUpdateRequest(BaseDto):
    """
    상세 업무 메시지 수정 요청

    OpenAPI Schema: task-messages-taskMessageNo-details-taskMessageDetailNo-637914009
    """

    content: str = Field(..., description="내용")
    uploaded_file_infos: list[UploadedFileInfo] = Field(default_factory=list, description="첨부파일 정보")

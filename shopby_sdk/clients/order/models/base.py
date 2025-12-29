"""Order API 공통 타입 및 모델 정의"""

from typing import Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto


# ============================================
#  Request/Response 공통 Enum 타입 정의
# ============================================

OrderRequestType = Literal[
    "DEPOSIT_WAIT",
    "PAY_DONE",
    "PRODUCT_PREPARE",
    "DELIVERY_PREPARE",
    "DELIVERY_ING",
    "DELIVERY_DONE",
    "BUY_CONFIRM",
    "CANCEL_DONE",
    "RETURN_DONE",
    "EXCHANGE_DONE",
    "CANCEL_PROCESSING",
    "RETURN_PROCESSING",
    "EXCHANGE_WAITING",
    "EXCHANGE_PROCESSING",
]
"""주문상태 타입 (Request용)"""

SearchDateType = Literal[
    "ORDER_START",
    "PAY_DONE",
    "PRODUCT_PREPARE",
    "DELIVERY_PREPARE",
    "DELIVERY_ING",
    "DELIVERY_DONE",
    "BUY_CONFIRM",
    "STATUS_CHANGE",
]
"""조회 주문일시 유형"""

SearchType = Literal["ALL", "ORDER_NO", "MALL_PRODUCT_NO"]
"""검색 유형"""

ShippingAreaType = Literal["PARTNER_SHIPPING_AREA", "MALL_SHIPPING_AREA"]
"""배송구분"""

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
    "LPAY",
    "ESCROW_REALTIME_ACCOUNT_TRANSFER",
    "ESCROW_VIRTUAL_ACCOUNT",
    "RENTAL",
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

DeliveryCompanyType = Literal[
    "CJ",
    "POST",
    "HANJIN",
    "GTX",
    "LOTTE",
    "KGB",
    "LOGEN",
    "GSI",
    "KGL",
    "INTRAS",
    "UPS",
    "CHUNIL",
    "KDEXP",
    "HDEXP",
    "ILYANG",
    "POST_EMS",
    "DAESIN",
    "CVS",
    "DHL",
    "FEDEX",
    "GSM",
    "WARPEX",
    "WIZWA",
    "ACI",
    "PANTOS",
    "CJ_INTERNATIONAL",
    "TNT",
    "CU",
    "KUNYOUNG",
    "LOTTE_INTERNATIONAL",
    "HONAM",
    "HANIPS",
    "IPARCEL",
    "SLX",
    "USPS",
    "WONDERS",
    "REGISTPOST",
    "DHLDE",
    "EZUSA",
    "SWGEXP",
    "DAEWOON",
    "DODOFLEX",
    "NH_LOGIS",
    "UFO",
    "TODAY_PICKUP",
    "QEXPRESS",
    "PINGPONG",
    "CR_LOGITECH",
    "TODAY",
    "SELLUV",
    "EXMATE",
    "WINION_LOGIS",
    "ETC",
]
"""택배사 타입"""

OrderStatusType = Literal[
    "DEPOSIT_WAIT",
    "PAY_DONE",
    "PRODUCT_PREPARE",
    "DELIVERY_PREPARE",
    "DELIVERY_ING",
    "DELIVERY_DONE",
    "BUY_CONFIRM",
    "CANCEL_DONE",
    "RETURN_DONE",
    "EXCHANGE_DONE",
    "PAY_WAIT",
    "PAY_CANCEL",
    "PAY_FAIL",
    "DELETE",
    "EXCHANGE_WAIT",
    "REFUND_DONE",
]
"""주문 옵션 상태"""

PlatformType = Literal["PC", "MOBILE_WEB", "MOBILE_APP"]
"""플랫폼 타입"""

ClaimStatusType = Literal[
    "CANCEL_NO_REFUND",
    "CANCEL_REQUEST",
    "CANCEL_PROC_REQUEST_REFUND",
    "CANCEL_PROC_WAITING_REFUND",
    "CANCEL_DONE",
    "RETURN_REQUEST",
    "RETURN_REJECT_REQUEST",
    "RETURN_PROC_BEFORE_RECEIVE",
    "RETURN_PROC_REQUEST_REFUND",
    "RETURN_PROC_WAITING_REFUND",
    "RETURN_DONE",
    "RETURN_REFUND_AMT_ADJUST_REQUESTED",
    "RETURN_NO_REFUND",
    "EXCHANGE_REQUEST",
    "EXCHANGE_REJECT_REQUEST",
    "EXCHANGE_PROC_BEFORE_RECEIVE",
    "EXCHANGE_PROC_REQUEST_PAY",
    "EXCHANGE_PROC_REQUEST_REFUND",
    "EXCHANGE_PROC_WAITING",
    "EXCHANGE_DONE",
    "EXCHANGE_PROC_WAITING_PAY",
    "EXCHANGE_PROC_WAITING_REFUND",
    "EXCHANGE_DONE_PAY_DONE",
    "EXCHANGE_DONE_REFUND_DONE",
]
"""클레임 상태"""

ClaimType = Literal["CANCEL", "RETURN", "EXCHANGE"]
"""클레임 타입"""


# ============================================
#  공통 모델 정의
# ============================================


class BankInfo(BaseDto):
    """은행 정보"""

    bank: str | None = Field(None, description="은행")
    bank_code: str | None = Field(None, description="PG 은행코드")
    bank_name: str | None = Field(None, description="은행명")
    account: str | None = Field(None, description="계좌번호")
    bank_amt: float | None = Field(None, description="입금해야할 금액")
    deposit_amt: float | None = Field(None, description="실제 입금금액")
    deposit_ymdt: str | None = Field(None, description="입금일시")
    remitter_name: str | None = Field(None, description="입금자명")
    depositor_name: str | None = Field(None, description="예금주명")
    payment_expiration_ymdt: str | None = Field(None, description="입금 마감일")


class CardInfo(BaseDto):
    """카드 정보"""

    card_company: str | None = Field(None, description="카드사")
    card_code: str | None = Field(None, description="카드코드")
    card_name: str | None = Field(None, description="카드명")
    card_no: str | None = Field(None, description="카드번호")
    card_approval_number: str | None = Field(None, description="승인번호")
    approve_ymdt: str | None = Field(None, description="승인일시")
    card_amt: float | None = Field(None, description="카드결제금액")
    no_interest: bool | None = Field(None, description="무이자 여부")
    installment_period: int | None = Field(None, description="할부개월")


class NaverPayInfo(BaseDto):
    """네이버페이 결제 정보"""

    payment_means: str | None = Field(None, description="네이버 페이 결제 수단")
    payment_due_date: str | None = Field(None, description="입금 기한")
    payment_number: str | None = Field(None, description="PG승인번호")
    order_discount_amount: float | None = Field(None, description="주문 할인액")
    general_payment_amount: float | None = Field(None, description="일반결제수단최종결제금액")
    naver_mileage_payment_amount: float | None = Field(None, description="네이버페이 포인트 최종 결제 금액")
    charge_amount_payment_amount: float | None = Field(None, description="충전금최종결제금액")
    checkout_accumulation_payment_amount: float | None = Field(None, description="네이버페이 적립금 최종 결제 금액")
    pay_later_payment_amount: float | None = Field(None, description="네이버페이 후불결제 금액")
    order_type: str | None = Field(None, description="주문 유형 구분")
    pay_location_type: str | None = Field(None, description="결제 위치 구분")
    payment_core_type: str | None = Field(None, description="결제 구분")


class RentalInfo(BaseDto):
    """렌탈 정보"""

    rental_period: int | None = Field(None, description="렌탈 기간")
    monthly_rental_amount: float | None = Field(None, description="월 렌탈료")


class ComplexPayInfo(BaseDto):
    """복합결제 정보"""

    main_pay_amt: float | None = Field(None, description="실결제금액")
    extra_pay_amt: float | None = Field(None, description="추가 결제 금액")


class MobileInfo(BaseDto):
    """휴대폰 결제 정보"""

    mobile_company: str | None = Field(None, description="통신사")
    mobile_no: str | None = Field(None, description="휴대폰번호")


class PaymentInfo(BaseDto):
    """결제 정보 (공통)"""

    pay_type: PayType | None = Field(None, description="결제수단")
    card_info: CardInfo | None = Field(None, description="카드정보")
    bank_info: BankInfo | None = Field(None, description="은행정보")
    naver_pay_info: NaverPayInfo | None = Field(None, description="네이버페이 정보")
    mobile_info: MobileInfo | None = Field(None, description="휴대폰 결제 정보")
    rental_info: RentalInfo | None = Field(None, description="렌탈 정보")
    complex_pay_info: ComplexPayInfo | None = Field(None, description="복합결제 정보")
    cash_auth_no: str | None = Field(None, description="현금영수증 승인번호")
    cash_no: str | None = Field(None, description="현금영수증 번호")
    trade_no: str | None = Field(None, description="거래번호")
    escrow_yn: str | None = Field(None, description="에스크로 여부")
    pay_amt: float | None = Field(None, description="결제금액")
    seller_coupon_amt: float | None = Field(None, description="셀러쿠폰 금액")
    pg_coupon_amt: float | None = Field(None, description="PG쿠폰 금액")
    card_coupon_amt: float | None = Field(None, description="카드쿠폰 금액")
    point_amt: float | None = Field(None, description="포인트 사용금액")
    tax_type: str | None = Field(None, description="과세유형")
    recurring_payment_date: str | None = Field(None, description="정기결제일")


class UserInput(BaseDto):
    """구매자 입력형 옵션"""

    input_label: str | None = Field(None, description="옵션 이름")
    input_value: str | None = Field(None, description="옵션 값")


class SetOption(BaseDto):
    """세트 옵션"""

    mall_option_no: int | None = Field(None, description="몰 옵션번호")
    mall_product_no: int | None = Field(None, description="몰상품 번호")
    product_name: str | None = Field(None, description="상품명")
    option_name: str | None = Field(None, description="옵션명")
    option_value: str | None = Field(None, description="옵션값")
    option_price: float | None = Field(None, description="옵션가격")
    count: int | None = Field(None, description="수량")
    sku: str | None = Field(None, description="SKU")
    stock_no: int | None = Field(None, description="재고번호")
    product_management_cd: str | None = Field(None, description="상품관리코드")
    option_management_cd: str | None = Field(None, description="옵션 관리 코드")
    option_use_yn: str | None = Field(None, description="옵션 사용여부")


class ExternalPayInfo(BaseDto):
    """외부 결제 정보"""

    external_pay_key: str | None = Field(None, description="외부결제키")
    external_pay_name: str | None = Field(None, description="외부결제명")
    pay_type: str | None = Field(None, description="결제수단")
    pay_amt: float | None = Field(None, description="결제금액")


class Balance(BaseDto):
    """결제 금액 정보"""

    pay_amt: float | None = Field(None, description="결제금액")
    main_pay_amt: float | None = Field(None, description="실결제금액")
    sub_pay_amt: float | None = Field(None, description="보조결제금액(적립금)")
    standard_amt: float | None = Field(None, description="정상금액")
    delivery_amt: float | None = Field(None, description="배송비")
    remote_delivery_amt: float | None = Field(None, description="추가배송비")
    immediate_discount_amt: float | None = Field(None, description="즉시할인 금액")
    additional_discount_amt: float | None = Field(None, description="추가할인 금액")
    cart_coupon_discount_amt: float | None = Field(None, description="장바구니쿠폰할인금액")
    product_coupon_discount_amt: float | None = Field(None, description="상품쿠폰할인금액")
    delivery_coupon_discount_amt: float | None = Field(None, description="배송쿠폰할인금액")
    external_pay_amt: float | None = Field(None, description="외부결제금액")
    total_discount_amt: float | None = Field(None, description="총 할인금액")

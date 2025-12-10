"""Order API 모델 정의"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


# ------------------------------------
#  Request용 Enum 타입 정의
# ------------------------------------

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
"""주문상태 타입"""

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


# ------------------------------------
#  Response 모델 정의
# ------------------------------------


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


class OrderProductOption(BaseDto):
    """주문 상품 옵션"""

    order_option_no: int | None = Field(None, description="주문옵션번호")
    mall_option_no: int | None = Field(None, description="몰 옵션번호")
    mall_additional_product_no: int | None = Field(None, description="추가상품번호")
    order_option_type: str | None = Field(None, description="옵션 타입 (NORMAL_OPTION, ADDITIONAL_OPTION)")
    order_status_type: OrderStatusType | None = Field(None, description="주문상태")
    order_cnt: int | None = Field(None, description="주문수량")
    order_ymdt: KstDatetime | None = Field(None, description="주문일자")
    option_name: str | None = Field(None, description="옵션명")
    option_value: str | None = Field(None, description="옵션값")
    option_use_yn: str | None = Field(None, description="옵션 사용여부")
    add_price: float | None = Field(None, description="옵션가격(추가금액)")
    sku: str | None = Field(None, description="SKU")
    stock_no: int | None = Field(None, description="재고번호")
    sale_price: float | None = Field(None, description="판매가")
    immediate_discount_amt: float | None = Field(None, description="즉시할인 금액")
    additional_discount_amt: float | None = Field(None, description="추가할인 금액")
    product_coupon_discount_amt: float | None = Field(None, description="상품쿠폰 할인금액")
    reservation_yn: str | None = Field(None, description="예약주문 여부")
    delivery_yn: str | None = Field(None, description="배송 여부")
    delivery_complete_ymdt: KstDatetime | None = Field(None, description="배송완료일시")
    buy_confirm_ymdt: KstDatetime | None = Field(None, description="구매확정일시")
    order_accept_ymdt: KstDatetime | None = Field(None, description="주문승인일시")
    status_change_ymdt: KstDatetime | None = Field(None, description="상태변경일시")
    shipping_area_type: str | None = Field(None, description="배송구분")
    hold_delivery_yn: bool | None = Field(None, description="배송보류 여부")
    delivery_combination_yn: str | None = Field(None, description="묶음배송 여부")
    returnable_yn: str | None = Field(None, description="반품 가능여부")
    category_no: int | None = Field(None, description="카테고리번호")
    brand_no: int | None = Field(None, description="브랜드번호")
    partner_no: int | None = Field(None, description="파트너번호")
    purchase_price: float | None = Field(None, description="매입가/공급가")
    user_inputs: list[UserInput] = Field(default_factory=list, description="구매자 입력형 옵션")
    set_options: list[SetOption] = Field(default_factory=list, description="세트옵션")
    member_accumulation_rate: float | None = Field(None, description="회원 적립률")
    additional_discount_no: int | None = Field(None, description="추가할인번호")
    member_grade_no: int | None = Field(None, description="회원등급번호")
    recurring_payment_no: int | None = Field(None, description="정기결제번호")


class OrderProduct(BaseDto):
    """주문 상품"""

    order_product_no: int | None = Field(None, description="주문상품 번호")
    mall_product_no: int | None = Field(None, description="몰상품 번호")
    product_no: int | None = Field(None, description="상품번호")
    product_name: str | None = Field(None, description="상품명")
    product_name_en: str | None = Field(None, description="영어상품명")
    product_management_cd: str | None = Field(None, description="상품관리코드")
    image_url: str | None = Field(None, description="상품 이미지 URL")
    hs_code: str | None = Field(None, description="HS코드")
    first_product_coupon_discount_amt: float | None = Field(None, description="처음 쿠폰할인금액")
    product_coupon_issue_no: int | None = Field(None, description="상품 쿠폰 발행 번호")
    order_product_options: list[OrderProductOption] = Field(default_factory=list, description="주문옵션")


class DeliveryGroup(BaseDto):
    """배송 그룹"""

    delivery_no: int = Field(..., description="배송번호")
    invoice_no: str | None = Field(None, description="송장번호")
    invoice_register_ymdt: KstDatetime | None = Field(None, description="송장번호등록일시")
    delivery_company_type: DeliveryCompanyType | None = Field(None, description="택배사 타입")
    delivery_type: str | None = Field(None, description="배송 타입")
    delivery_template_no: int | None = Field(None, description="배송 템플릿 번호")
    delivery_template_group_no: int | None = Field(None, description="배송 템플릿 그룹 번호")
    delivery_condition_no: int | None = Field(None, description="배송 조건 번호")
    delivery_amt: float | None = Field(None, description="배송비")
    return_delivery_amt: float | None = Field(None, description="반품 배송비")
    remote_delivery_amt: float | None = Field(None, description="도서산간 배송비")
    adjusted_amt: float | None = Field(None, description="조정 금액")
    receiver_name: str | None = Field(None, description="수령자 명")
    receiver_contact1: str | None = Field(None, description="연락처1")
    receiver_contact2: str | None = Field(None, description="연락처2")
    receiver_zip_cd: str | None = Field(None, description="배송지 우편 번호")
    receiver_address: str | None = Field(None, description="배송지 주소")
    receiver_jibun_address: str | None = Field(None, description="배송지 지번주소")
    receiver_detail_address: str | None = Field(None, description="배송지 상세주소")
    receiver_state: str | None = Field(None, description="(해외) 주/도")
    receiver_city: str | None = Field(None, description="(해외) 도시")
    country_cd: str | None = Field(None, description="국가코드")
    delivery_memo: str | None = Field(None, description="배송메모")
    customs_id_number: str | None = Field(None, description="개인고유통관부호")
    delivery_yn: str | None = Field(None, description="배송 여부")
    combine_delivery_yn: str | None = Field(None, description="합배송 여부")
    divide_delivery_yn: str | None = Field(None, description="분할배송 여부")
    delivery_amt_in_advance_yn: str | None = Field(None, description="선결제 여부")
    shipping_method_type: str | None = Field(None, description="배송방법")
    original_delivery_no: int | None = Field(None, description="원배송번호")
    uses_shipping_info_later_input: bool = Field(False, description="배송지 나중입력 여부")
    encrypted_shipping_no: str | None = Field(None, description="암호화된 배송번호")
    delivery_combination_yn: str | None = Field(None, description="묶음배송 여부")
    order_products: list[OrderProduct] = Field(default_factory=list, description="주문 상품")


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


class PaymentInfo(BaseDto):
    """결제 정보"""

    pay_type: PayType | None = Field(None, description="결제수단")
    card_info: CardInfo | None = Field(None, description="카드정보")
    bank_info: BankInfo | None = Field(None, description="은행정보")
    naver_pay_info: dict[str, Any] | None = Field(None, description="네이버페이 정보")
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
    mobile_info: dict[str, Any] | None = Field(None, description="모바일 결제 정보")
    rental_info: dict[str, Any] | None = Field(None, description="렌탈 정보")
    complex_pay_info: dict[str, Any] | None = Field(None, description="복합결제 정보")
    recurring_payment_date: str | None = Field(None, description="정기결제일")


class ExternalPayInfo(BaseDto):
    """외부 결제 정보"""

    pay_type: str | None = Field(None, description="결제수단")
    pay_amt: float | None = Field(None, description="결제금액")


class OrderSheetInfo(BaseDto):
    """주문서 정보"""

    order_sheet_id: str | None = Field(None, description="주문서 ID")
    pay_products: list[dict[str, Any]] = Field(default_factory=list, description="결제 상품")
    apply_coupon: dict[str, Any] | None = Field(None, description="적용 쿠폰")


class Order(BaseDto):
    """주문 정보"""

    order_no: str | None = Field(None, description="주문번호")
    order_ymdt: KstDatetime | None = Field(None, description="주문일자")
    mall_no: int | None = Field(None, description="몰번호")
    member_no: int | None = Field(None, description="회원번호")
    member_id: str | None = Field(None, description="회원아이디")
    oauth_id_no: str | None = Field(None, description="OAuth ID")
    orderer_name: str | None = Field(None, description="주문자명")
    orderer_contact1: str | None = Field(None, description="주문자 연락처1")
    orderer_contact2: str | None = Field(None, description="주문자 연락처2")
    orderer_email: str | None = Field(None, description="주문자 이메일")
    order_memo: str | None = Field(None, description="주문메모")
    ip: str | None = Field(None, description="IP")
    platform_type: PlatformType | None = Field(None, description="플랫폼타입")
    channel_type: str | None = Field(None, description="채널타입")
    pay_type: PayType | None = Field(None, description="결제수단")
    pay_type_label: str | None = Field(None, description="결제수단 라벨")
    pg_type: str | None = Field(None, description="PG사")
    currency_code: str | None = Field(None, description="통화코드")
    exchange_rate: float | None = Field(None, description="적용 환율")
    first_pay_ymdt: KstDatetime | None = Field(None, description="최초 결제일시")
    first_pay_amt: float | None = Field(None, description="처음 결제금액")
    first_sub_pay_amt: float | None = Field(None, description="처음 포인트 사용금액")
    first_main_pay_amt: float | None = Field(None, description="처음 주결제금액")
    first_external_pay_amt: float | None = Field(None, description="처음 외부결제금액")
    first_delivery_amt: float | None = Field(None, description="처음 배송비")
    first_immediate_discount_amt: float | None = Field(None, description="최초 즉시 할인금액")
    first_additional_discount_amt: float | None = Field(None, description="최초 추가 할인금액")
    first_product_coupon_discount_amt: float | None = Field(None, description="최초 상품쿠폰 할인금액")
    first_cart_coupon_discount_amt: float | None = Field(None, description="최초 장바구니쿠폰 할인금액")
    first_total_discount_amt: float | None = Field(None, description="최초 총 할인금액")
    last_pay_amt: float | None = Field(None, description="최종 결제금액")
    last_sub_pay_amt: float | None = Field(None, description="최종 포인트 사용금액")
    last_main_pay_amt: float | None = Field(None, description="최종 주결제금액")
    last_external_pay_amt: float | None = Field(None, description="최종 외부결제금액")
    last_delivery_amt: float | None = Field(None, description="최종 배송비")
    last_immediate_discount_amt: float | None = Field(None, description="최종 즉시 할인금액")
    last_additional_discount_amt: float | None = Field(None, description="최종 추가 할인금액")
    last_product_coupon_discount_amt: float | None = Field(None, description="최종 상품쿠폰 할인금액")
    last_cart_coupon_discount_amt: float | None = Field(None, description="최종 장바구니쿠폰 할인금액")
    last_total_discount_amt: float | None = Field(None, description="최종 총 할인금액")
    cart_coupon_issue_no: int | None = Field(None, description="장바구니쿠폰 발급번호")
    cash_receipt_issue_no: str | None = Field(None, description="현금영수증 발급번호")
    cash_receipt_issue_ymdt: str | None = Field(None, description="현금영수증 발급일시")
    cash_receipt_status: str | None = Field(None, description="현금영수증 상태")
    cash_receipt_issued: bool | None = Field(None, description="현금영수증 발급여부")
    tax_invoice_issue_no: str | None = Field(None, description="세금계산서 발급번호")
    tax_invoice_issue_ymdt: str | None = Field(None, description="세금계산서 발급일시")
    tax_invoice_status: str | None = Field(None, description="세금계산서 상태")
    tax_invoice_issued: bool | None = Field(None, description="세금계산서 발급여부")
    extra_data: str | None = Field(None, description="추가정보 (JSON 문자열)")
    member_additional_info_json: str | None = Field(None, description="회원 추가정보")
    tracking_key: str | None = Field(None, description="추적키")
    bank_info: BankInfo | None = Field(None, description="은행정보")
    payment_info: PaymentInfo | None = Field(None, description="결제정보")
    order_sheet_info: OrderSheetInfo | None = Field(None, description="주문서 정보")
    first_external_pay_infos: list[ExternalPayInfo] = Field(default_factory=list, description="처음 외부결제 정보")
    last_external_pay_infos: list[ExternalPayInfo] = Field(default_factory=list, description="최종 외부결제 정보")
    delivery_groups: list[DeliveryGroup] = Field(default_factory=list, description="배송그룹")


class OrdersResponse(BaseDto):
    """
    주문 조회하기 v1.1 응답

    OpenAPI Schema: orders-410669276
    """

    total_count: int = Field(..., description="전체 주문 수")
    contents: list[Order] = Field(default_factory=list, description="주문 목록")

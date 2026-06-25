"""Order Friends API 모델

주문과 관련된 부가 기능(통계, 정산, CS 등) 응답 모델 정의
"""

from typing import Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto

# ------------------------------------
#  Literal 타입 별칭
# ------------------------------------
CsType = Literal["PAY", "PRODUCT", "DELIVERY", "CLAIM", "REFUND", "ETC"]
"""CS 타입 (PAY: 결제, PRODUCT: 주문상품, DELIVERY: 배송, CLAIM: 취소/교환/반품, REFUND: 환불, ETC: 기타)"""

CsChannelType = Literal[
    "SERVICE",
    "PARTNER",
    "FRONT",
    "BATCH",
    "SYSTEM",
    "SERVER",
    "PLATFORM",
]
"""CS 채널 타입"""

CsStatusType = Literal["PROCESSING", "DONE"]
"""CS 상태 타입 (PROCESSING: 처리중, DONE: 처리완료)"""

CsPathType = Literal["IN_BOUND", "OUT_BOUND", "ETC", "SYSTEM"]
"""CS 경로 타입"""

SettlementPartnerType = Literal["DOMESTIC", "OVERSEAS"]
"""파트너 구분 (DOMESTIC: 국내파트너, OVERSEAS: 해외파트너)"""

CouponType = Literal["PRODUCT", "CART", "GIFT"]
"""쿠폰 타입"""

GenderType = Literal["MALE", "FEMALE", "UNKNOWN"]
"""회원 성별"""

MemberJoinType = Literal["MEMBER", "NON_MEMBER"]
"""회원 구분"""

MemberType = Literal[
    "ALL",
    "MALL",
    "PAYCO",
    "NAVER",
    "KAKAO",
    "FACEBOOK",
    "IAMSCHOOL",
    "LIIVMATE",
    "NHN",
    "NHNENT",
    "UNIONE",
    "LINE",
    "NCPSTORE",
    "KAKAO_SYNC",
    "GOOGLE",
    "APPLE",
    "APP_CARD",
]
"""회원 가입유형"""

PlatformType = Literal["PC", "MOBILE_WEB", "MOBILE_APP"]
"""플랫폼 구분"""

PromotionKeywordType = Literal["NO", "NAME", "REGISTRANT"]
"""프로모션 검색 키워드 타입"""

ProductKeywordType = Literal["NO", "NAME", "MANAGEMENT_CD"]
"""상품 검색 키워드 타입"""

ProductType = Literal["PRODUCT", "OPTION"]
"""상품 조회 기준"""

SaleMethodType = Literal["PURCHASE", "CONSIGNMENT"]
"""판매방식 구분 (PURCHASE: 사입, CONSIGNMENT: 위탁)"""

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
    "VERITRANS_CARD",
    "TOASTCAM",
    "ETC",
    "ESCROW_REALTIME_ACCOUNT_TRANSFER",
    "ESCROW_VIRTUAL_ACCOUNT",
    "TOSS_PAY",
    "SK_PAY",
    "APPLE_PAY",
    "LPAY",
    "RENTAL",
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
]
"""결제수단"""


# ====================================
#  CS 처리내역 조회 (GET /cs)
# ====================================
class CsAudit(BaseDto):
    """CS 처리자 정보 (등록/업데이트 audit)"""

    timestamp: str = Field(..., description="일시")
    admin_no: int = Field(..., description="어드민번호")
    name: str = Field(..., description="처리자명")
    client_ip: str = Field(..., description="처리자IP")


class CsItem(BaseDto):
    """CS 처리내역 항목"""

    cs_no: int = Field(..., description="CS 번호")
    mall_no: int | None = Field(None, description="몰 번호")
    order_no: int = Field(..., description="주문번호")
    order_option_no: int | None = Field(None, description="주문옵션번호")
    product_name: str | None = Field(None, description="상품명")
    register_audit: CsAudit = Field(..., description="등록 처리자")
    cs_channel_type: CsChannelType = Field(..., description="CS 채널 타입")
    cs_type: CsType = Field(..., description="CS 타입")
    cs_path_type: CsPathType = Field(..., description="CS 경로 타입")
    cs_status_type: CsStatusType = Field(..., description="CS 상태 타입")
    title: str = Field(..., description="제목")
    content: str = Field(..., description="내용")
    member_no: int = Field(..., description="회원번호")
    orderer_name: str | None = Field(None, description="주문자명")
    claim_withdraw_reason: str | None = Field(None, description="클레임 철회 사유")
    delivery_expected_ymdt: str | None = Field(None, description="배송예정일시")
    hold_delivery_reason: str | None = Field(None, description="배송보류 사유")
    from_app_name: str | None = Field(None, description="등록된 앱 이름")
    register_name_as_app_name: bool | None = Field(
        None, description="등록자명을 앱명으로 노출할지 여부"
    )
    deleted: bool = Field(..., description="삭제 여부")
    update_audit: CsAudit | None = Field(None, description="업데이트 처리자")
    cs_auto_type: str | None = Field(None, description="CS 자동 타입")


class CsResponse(BaseDto):
    """
    CS 처리내역 조회 응답

    OpenAPI Schema: cs-2012969842
    """

    total_count: int = Field(..., description="전체 조회건수")
    contents: list[CsItem] = Field(default_factory=list, description="조회 결과")


# ====================================
#  쇼핑몰 정산 데이터 조회 (GET /orders/sales)
# ====================================
class OrdersSalesMemberGroupInfo(BaseDto):
    """회원그룹 정보"""

    member_group_name: str = Field(..., description="회원 그룹명")
    member_group_no: int = Field(..., description="회원 그룹 번호")


class OrdersSalesMemberInfo(BaseDto):
    """회원정보"""

    member_no: int | None = Field(None, description="회원번호")
    member_grade_name: str | None = Field(None, description="회원등급")
    additional_info_json: str | None = Field(None, description="회원 기타정보(외부 연동 제공 정보)")
    member_group_infos: list[OrdersSalesMemberGroupInfo] = Field(
        default_factory=list, description="회원그룹(복수개 가능)"
    )
    external_membership_key: str | None = Field(None, description="외부 회원 키")


class OrdersSalesSetOption(BaseDto):
    """세트옵션 정보"""

    product_management_cd: str = Field(..., description="상품관리코드")
    mall_option_no: str = Field(..., description="옵션번호")
    option_use_yn: str | None = Field(None, description="옵션사용유무")
    option_value: str = Field(..., description="옵션값")
    count: int = Field(..., description="수량")
    option_price: float = Field(..., description="옵션가격")
    sku: str | None = Field(None, description="sku")
    option_name: str = Field(..., description="옵션명")
    option_management_cd: str | None = Field(None, description="옵션관리코드")
    mall_product_no: int = Field(..., description="상품번호")
    stock_no: int = Field(..., description="재고번호")
    product_name: str = Field(..., description="상품명")


class OrdersSalesProductInfo(BaseDto):
    """상품정보"""

    product_management_cd: str | None = Field(None, description="상품관리코드")
    mall_option_no: int | None = Field(None, description="옵션번호")
    global_product_no: int | None = Field(None, description="글로벌번호")
    commission_rate: str = Field(..., description="판매 수수료율")
    mall_additional_product_no: int | None = Field(None, description="추가상품번호")
    purchase_price: float = Field(..., description="공급가(매입가)액")
    purchase_yn: str = Field(..., description="공급가 입력")
    mall_product_no: int | None = Field(None, description="상품번호")
    product_name: str | None = Field(None, description="상품명")
    set_options: list[OrdersSalesSetOption] = Field(
        default_factory=list, description="세트옵션인 경우 세트정보"
    )
    sku: str | None = Field(None, description="sku")
    option_management_cd: str | None = Field(None, description="옵션관리코드")
    option: str | None = Field(None, description="옵션명:옵션값")


class OrdersSalesPriceInfo(BaseDto):
    """가격/할인정보"""

    immediate_discount_amt: float | None = Field(None, description="즉시할인금액")
    additional_discount_amt: float | None = Field(None, description="추가할인금액")
    sale_price: float | None = Field(None, description="판매가")
    delivery_coupon_discount_amt: float | None = Field(None, description="배송비쿠폰할인금액")
    adjusted_amt: float | None = Field(None, description="판매가(즉시할인가) 조정금액")
    cart_coupon_discount_amt: float | None = Field(None, description="장바구니쿠폰할인금액")
    add_price: float | None = Field(None, description="옵션추가금액")
    product_coupon_discount_amt: float | None = Field(None, description="상품쿠폰할인금액")


class OrdersSalesPaymentInfo(BaseDto):
    """결제정보"""

    pg_type: str = Field(..., description="PG사 타입")
    pay_type: str = Field(..., description="결제수단")
    external_point_use_amt: float | None = Field(None, description="외부 연동 포인트 사용금액")
    accumulation_use_amt: float | None = Field(None, description="적립금 사용금액")
    pg_pay_amt: float | None = Field(None, description="PG결제금액")


class OrdersSalesCouponInfo(BaseDto):
    """쿠폰정보"""

    cart_coupon_issue_no: int | None = Field(None, description="장바구니 쿠폰 발행 번호")
    product_coupon_issue_no: int | None = Field(None, description="상품 쿠폰 발행 번호")
    product_coupon_no: int | None = Field(None, description="상품 쿠폰 번호")
    cart_coupon_no: int | None = Field(None, description="장바구니 쿠폰 번호")


class OrdersSalesItem(BaseDto):
    """쇼핑몰 매출 데이터 항목"""

    seq: int = Field(..., description="매출 내역 번호")
    order_no: str = Field(..., description="주문번호")
    register_ymdt: str = Field(..., description="등록일시")
    pay_ymdt: str | None = Field(None, description="결제일시")
    sales_register_type: str | None = Field(None, description="등록유형")
    sales_register_type_for_display: str = Field(..., description="등록유형(display)")
    order_product_no: int | None = Field(None, description="주문상품번호")
    order_product_option_no: int | None = Field(None, description="주문상품옵션번호")
    claim_no: int | None = Field(None, description="클레임번호(매출 취소시)")
    order_cnt: int | None = Field(None, description="주문수량")
    refund_cnt: int | None = Field(None, description="취소수량")
    refund_ymdt: str | None = Field(None, description="환불일시(사용하지 않음)")
    order_status_type: str | None = Field(None, description="등록시점 주문상태")
    memo: str | None = Field(None, description="특이사항 메모")
    member_info: OrdersSalesMemberInfo = Field(..., description="회원정보")
    product_info: OrdersSalesProductInfo = Field(..., description="상품정보")
    price_info: OrdersSalesPriceInfo = Field(..., description="가격/할인정보")
    payment_info: OrdersSalesPaymentInfo = Field(..., description="결제정보")
    coupon_info: OrdersSalesCouponInfo = Field(..., description="쿠폰정보")
    channel_type: str | None = Field(None, description="외부 주문 채널 타입")
    accumulation_amt: float | None = Field(None, description="지급예정 적립금 금액")
    external_pay_amt: float | None = Field(None, description="외부 결제 결제금액")


class OrdersSalesResponse(BaseDto):
    """
    쇼핑몰 정산(매출) 데이터 조회 응답

    OpenAPI Schema: orders-sales547821119
    """

    total_count: int = Field(..., description="총 조회 건수")
    items: list[OrdersSalesItem] = Field(default_factory=list, description="쇼핑몰 매출 데이터")


# ====================================
#  파트너 정산 데이터 조회 (GET /settlement)
# ====================================
class SettlementItem(BaseDto):
    """
    파트너 정산 데이터 항목

    OpenAPI Schema: settlement292649878 (배열 항목)
    """

    partner_no: int = Field(..., description="파트너 번호")
    partner_name: str = Field(..., description="파트너사")
    partner_type: str = Field(..., description="파트너 구분")
    order_cnt: int = Field(..., description="판매수량 합계")
    sales_amt: float = Field(..., description="판매금액 합계(A)")
    commission_amt: float = Field(..., description="판매수수료 합계(B)")
    delivery_amt: float = Field(..., description="배송비(C)")
    mall_discount_amt: float = Field(..., description="추가/상품/사은품할인 쇼핑몰분담")
    partner_discount_amt: float = Field(..., description="추가/상품/사은품할인 파트너분담(D)")
    mall_product_adjust_amt: float = Field(..., description="상품금액조정 쇼핑몰부담")
    partner_product_adjust_amt: float = Field(..., description="상품금액조정 파트너부담(E)")
    mall_delivery_adjust_amt: float = Field(..., description="배송비금액조정 쇼핑몰부담")
    partner_delivery_adjust_amt: float = Field(..., description="배송비금액조정 파트너부담(F)")
    mall_delivery_amt: float = Field(..., description="쇼핑몰배송비(G)")
    refund_adjust_amt: float = Field(..., description="환불보류 금액조정(H)")
    settlement_amt: float = Field(..., description="정산예상금액(I=A-B+C-D-E-F-G+H)")
    bank_name: str = Field(..., description="은행명")
    trade_bank_account: str = Field(..., description="계좌번호")
    trade_bank_depositor_name: str = Field(..., description="예금주")
    business_registration_no: str = Field(..., description="사업자등록번호")
    settlement_manager_name: str = Field(..., description="담당자")
    settlement_manager_email: str = Field(..., description="이메일")
    settlement_manager_phone_no: str = Field(..., description="연락처")


# ====================================
#  파트너 정산 상세 데이터 조회 (GET /settlement/detail)
# ====================================
class SettlementDetailItem(BaseDto):
    """파트너 정산 상세 데이터 항목"""

    company_name: str = Field(..., description="법인명")
    mall_name: str = Field(..., description="쇼핑몰명")
    option_management_cd: str | None = Field(None, description="옵션관리코드")
    order_no: str = Field(..., description="주문번호")
    order_product_no: int = Field(..., description="주문상품번호")
    order_product_option_no: int = Field(..., description="주문옵션번호")
    partner_no: int = Field(..., description="파트너 번호")
    partner_name: str = Field(..., description="파트너사")
    partner_type: str = Field(..., description="파트너 구분")
    value_added_tax_type_label: str = Field(..., description="과세유형")
    mall_product_no: int = Field(..., description="상품번호")
    mall_option_no: int = Field(..., description="상품옵션번호")
    product_name: str | None = Field(None, description="상품명")
    option: str | None = Field(None, description="옵션명")
    settlement_delivery_type_label: str = Field(..., description="배송구분(배송번호)")
    immediate_discounted_price: float = Field(..., description="판매가(할인적용가)")
    order_cnt: int = Field(..., description="판매수량")
    refund_cnt: int = Field(..., description="환불수량")
    sales_amt: float = Field(..., description="판매액(A)")
    purchase_price: float = Field(..., description="공급가(또는 매입가)액(O)")
    commission_rate: float = Field(..., description="수수료율(B1)")
    commission_amt: float = Field(..., description="판매수수료(B2=A*B1 or A-O)")
    mall_discount_amt: float = Field(..., description="추가/상품/사은품할인 쇼핑몰분담")
    partner_discount_amt: float = Field(..., description="추가/상품/사은품할인 파트너분담(D)")
    mall_product_adjust_amt: float = Field(..., description="상품금액조정 쇼핑몰부담")
    partner_product_adjust_amt: float = Field(..., description="상품금액조정 파트너부담(E)")
    mall_delivery_adjust_amt: float = Field(..., description="배송비금액조정 쇼핑몰부담")
    partner_delivery_adjust_amt: float = Field(..., description="배송비금액조정 파트너부담(F)")
    mall_delivery_amt: float = Field(..., description="쇼핑몰배송비(G)")
    delivery_amt: float = Field(..., description="배송비(C)")
    refund_adjust_amt: float = Field(..., description="환불보류 금액조정(H)")
    settlement_amt: float = Field(..., description="정산예상금액(I=A-B2+C-D-E-F-G+H)")
    pay_ymdt: str = Field(..., description="결제완료일")
    settlement_ymdt: str = Field(..., description="배송완료일/구매확정일")
    refund_ymdt: str | None = Field(None, description="환불완료일")
    memo: str | None = Field(None, description="메모")
    seq: int = Field(..., description="seq")
    purchase_yn: str | None = Field(None, description="공급가 입력")


class SettlementDetailResponse(BaseDto):
    """
    파트너 정산 상세 데이터 조회 응답 (v1.1)

    OpenAPI Schema: settlement-detail-1949787227
    """

    total_count: int = Field(..., description="총 데이터 개수")
    total_page: int = Field(..., description="총 페이지 수")
    contents: list[SettlementDetailItem] = Field(default_factory=list, description="데이터")


# ====================================
#  프로모션 통계 - 쿠폰 내역 (GET /statistics/promotions)
# ====================================
class StatisticsPromotionCoupon(BaseDto):
    """프로모션 통계 주문 쿠폰 항목"""

    coupon_name: str = Field(..., description="쿠폰명")
    coupon_no: int = Field(..., description="쿠폰번호")
    coupon_type: str = Field(..., description="프로모션 혜택 구분")
    currency_code: str = Field(..., description="통화 단위")
    order_cnt: int = Field(..., description="판매 건수")
    normal_order_cnt: int = Field(..., description="정산 판매 건수")
    claimed_order_cnt: int = Field(..., description="클레임 처리 건수")
    cart_coupon_amt: float = Field(..., description="장바구니 금액 할인(장바구니 쿠폰)")
    delivery_coupon_amt: float = Field(..., description="배송비 금액 할인(장바구니 쿠폰)")
    pay_amt: float = Field(..., description="총 결제 금액(장바구니 쿠폰)")
    sale_amt: float = Field(..., description="상품 판매 금액(상품 쿠폰)")
    sale_cnt: int = Field(..., description="상품 판매 수량(상품 쿠폰)")
    mall_product_coupon_amt: float = Field(..., description="상품 쿠폰 할인 금액(쇼핑몰)")
    partner_product_coupon_amt: float = Field(..., description="상품 쿠폰 할인 금액(파트너)")


class StatisticsPromotionsResponse(BaseDto):
    """
    프로모션 통계 - 쿠폰 내역 조회 응답

    OpenAPI Schema: statistics-promotions-337367269
    """

    total_count: int = Field(..., description="프로모션 통계 주문 쿠폰 총 개수")
    contents: list[StatisticsPromotionCoupon] = Field(
        default_factory=list, description="프로모션 통계 주문 쿠폰 목록"
    )


# ====================================
#  프로모션 통계 - 쿠폰 판매 현황 상세 (GET /statistics/promotions/detail)
# ====================================
class StatisticsPromotionDetailItem(BaseDto):
    """
    프로모션 통계 쿠폰 판매 현황 상세 항목

    OpenAPI Schema: statistics-promotions-detail999899910 (배열 항목)
    """

    add_price: float = Field(..., description="옵션 추가금액")
    brand_name: str = Field(..., description="브랜드명")
    cart_coupon_amt: float = Field(..., description="장바구니 금액 할인")
    claim_complete_ymdt: str | None = Field(None, description="클레임 완료 일시")
    claim_no: int | None = Field(None, description="클레임 번호")
    claim_status_type: str | None = Field(None, description="클레임 상태")
    commission_amt: float = Field(..., description="수수료 금액")
    commission_rate: float = Field(..., description="수수료율")
    delivery_amt: float = Field(..., description="배송비")
    delivery_coupon_amt: float = Field(..., description="배송비 할인 금액")
    display_brand_no: int = Field(..., description="전시 브랜드 번호")
    display_option_name: str | None = Field(None, description="옵션명:옵션값")
    exchange_delivery_adjust_amt: float | None = Field(None, description="교환(재발송) 배송비 조정 금액")
    exchange_delivery_amt: float | None = Field(None, description="교환 배송비")
    exchange_product_adjust_amt: float | None = Field(None, description="교환출고 상품 조정 금액")
    exchanged_claim_no: int | None = Field(None, description="교환 클레임 번호")
    external_pay_amt: float | None = Field(None, description="외부 결제 금액")
    full_category_name: str | None = Field(None, description="표준카테고리")
    global_product_no: int | None = Field(None, description="글로벌 상품 번호")
    immediate_discount_amt: float = Field(..., description="즉시할인금액")
    immediate_discounted_amt: float = Field(..., description="판매금액(E)")
    main_pay_amt: float = Field(..., description="총 결제(환불)금액")
    mall_additional_discount_amt: float = Field(..., description="추가할인(쇼핑몰)")
    partner_additional_discount_amt: float = Field(..., description="추가할인(파트너)")
    mall_free_gift_amt: float = Field(..., description="사은품금액할인(쇼핑몰)")
    partner_free_gift_amt: float = Field(..., description="사은품금액할인(파트너)")
    mall_name: str | None = Field(None, description="쇼핑몰명")
    mall_no: int = Field(..., description="쇼핑몰 번호")
    mall_option_no: int = Field(..., description="상품 옵션번호")
    mall_product_admin_name: str | None = Field(None, description="상품 등록 담당자")
    mall_product_coupon_amt: float = Field(..., description="상품금액할인(쇼핑몰)")
    partner_product_coupon_amt: float = Field(..., description="상품금액할인(파트너)")
    mall_product_no: int = Field(..., description="상품 번호")
    mall_profit_amt: float = Field(..., description="쇼핑몰수익")
    member_grade_name: str | None = Field(None, description="회원등급명")
    member_grade_no: int | None = Field(None, description="회원등급번호")
    member_group_names: list[str] | None = Field(None, description="회원그룹명 리스트")
    member_group_nos: list[int] | None = Field(None, description="회원그룹 번호 리스트")
    member_id: str | None = Field(None, description="회원ID")
    member_no: int | None = Field(None, description="회원번호")
    member_yn: str = Field(..., description="회원구분(Y:회원, N:비회원)")
    member_type: str | None = Field(None, description="회원가입 유형")
    option_management_cd: str | None = Field(None, description="옵션관리코드")
    order_cnt: int = Field(..., description="주문수량")
    order_no: str | None = Field(None, description="주문번호")
    order_option_no: int = Field(..., description="주문옵션번호")
    order_product_no: int = Field(..., description="주문상품번호")
    partner_name: str | None = Field(None, description="파트너사")
    partner_no: int = Field(..., description="파트너번호")
    pay_type: str | None = Field(None, description="결제수단")
    pay_ymdt: str | None = Field(None, description="결제일시")
    platform_type: str | None = Field(None, description="플랫폼타입")
    product_management_cd: str | None = Field(None, description="상품관리코드")
    product_name: str | None = Field(None, description="상품명")
    purchase_amt: float = Field(..., description="공급가액")
    purchase_yn: str = Field(..., description="공급가입력")
    recurring_immediate_discount_amt: float | None = Field(
        None, description="정기결제(배송) 즉시할인금액"
    )
    refund_adjust_amt: float | None = Field(None, description="환불금액 조정금액")
    return_delivery_adjust_amt: float | None = Field(None, description="반품배송비 조정금액")
    return_delivery_amt: float | None = Field(None, description="반품배송비")
    sale_method_type: str | None = Field(None, description="판매방식(사입:PURCHASE/위탁:CONSIGNMENT)")
    sale_price: float = Field(..., description="판매가")
    service_no: int = Field(..., description="서비스번호")
    sex: str = Field(..., description="회원 성별")
    sub_pay_amt: float = Field(..., description="적립금 사용 금액")
    supply_price: float | None = Field(None, description="매입가액")


# ====================================
#  판매통계 기간별 목록 (GET /statistics/sales/period)
# ====================================
class StatisticsSalesPeriodItem(BaseDto):
    """판매통계 일자별 항목"""

    ymd: str | None = Field(None, description="날짜")
    total_order_cnt: int = Field(..., description="판매건수")
    total_normal_order_cnt: int = Field(..., description="정상 판매건수")
    total_claimed_order_cnt: int = Field(..., description="클레임 판매건수")
    total_sale_cnt: int = Field(..., description="판매수량")
    total_sale_amt: float = Field(..., description="판매금액")
    total_additional_discount_amt: float = Field(..., description="추가할인금액")
    total_product_coupon_amt: float = Field(..., description="상품쿠폰 할인금액")
    total_cart_coupon_amt: float = Field(..., description="장바구니 할인금액")
    total_delivery_coupon_amt: float = Field(..., description="배송비 할인금액")
    total_accumulation_amt: float = Field(..., description="적립금 사용금액")
    total_delivery_amt: float = Field(..., description="배송비")
    total_refund_amt: float = Field(..., description="환불금액")
    total_free_gift_amt: float = Field(..., description="사은품 할인금액")
    total_external_pay_amt: float = Field(..., description="외부 결제 결제금액")
    total_promotion_discount_amt: float = Field(..., description="프로모션할인금액")
    total_sales_amt: float = Field(..., description="총 매출금액")
    total_pay_amt: float = Field(..., description="결제금액")


class StatisticsSalesPeriodResponse(BaseDto):
    """
    판매통계 기간별 목록 조회 응답

    OpenAPI Schema: statistics-sales-period163244397
    """

    total_count: int = Field(..., description="판매통계 일자별 총 개수")
    contents: list[StatisticsSalesPeriodItem] = Field(
        default_factory=list, description="판매통계 일자별 목록"
    )


# ====================================
#  판매통계 상품별 목록 (GET /statistics/sales/product)
# ====================================
class StatisticsSalesProductItem(BaseDto):
    """판매통계 상품별 항목"""

    mall_no: int = Field(..., description="쇼핑몰번호")
    mall_name: str = Field(..., description="쇼핑몰명")
    mall_product_no: int = Field(..., description="상품번호")
    mall_option_no: int = Field(..., description="옵션번호")
    product_management_cd: str | None = Field(None, description="상품관리코드")
    product_name: str | None = Field(None, description="상품명")
    partner_no: int = Field(..., description="파트너번호")
    partner_name: str = Field(..., description="파트너명")
    sale_method_type: str | None = Field(None, description="판매방식구분(위탁,사입)")
    sale_method_type_label: str = Field(..., description="판매방식구분명")
    commission_rate_type: str | None = Field(None, description="수수료방식")
    commission_rate: float = Field(..., description="수수료")
    total_order_cnt: int = Field(..., description="판매건수")
    total_normal_order_cnt: int = Field(..., description="정상 판매건수")
    total_claimed_order_cnt: int = Field(..., description="클레임 판매건수")
    total_sale_cnt: int = Field(..., description="판매수량")
    total_purchase_amt: float = Field(..., description="공급가액")
    total_supply_amt: float = Field(..., description="매입가액")
    total_sale_amt: float = Field(..., description="판매금액")
    total_commission_amt: float = Field(..., description="수수료수익")
    total_mall_additional_discount_amt: float = Field(..., description="추가할인(쇼핑몰)")
    total_partner_additional_discount_amt: float = Field(..., description="추가할인(파트너)")
    total_mall_product_coupon_amt: float = Field(..., description="상품쿠폰(쇼핑몰)")
    total_partner_product_coupon_amt: float = Field(..., description="상품쿠폰(파트너)")
    total_mall_free_gift_amt: float = Field(..., description="사은품할인(쇼핑몰)")
    total_partner_free_gift_amt: float = Field(..., description="사은품할인(파트너)")
    admin_no: int = Field(..., description="상품 MD 관리자 번호")
    brand_no: int = Field(..., description="브랜드 번호")
    brand_name: str = Field(..., description="브랜드명")
    display_brand_no: int = Field(..., description="전시브랜드 번호")
    category_no: int = Field(..., description="카테고리 번호")
    full_category_name: str = Field(..., description="표준카테고리명")
    uses_option: bool | None = Field(None, description="옵션사용유무")
    option_name: str | None = Field(None, description="옵션명")
    option_value: str | None = Field(None, description="옵션값")
    free_gift: bool | None = Field(None, description="사은품으로 지급된 상품 여부")
    total_mall_promotion_amt: float = Field(..., description="프로모션 금액(쇼핑몰)")
    total_partner_promotion_amt: float = Field(..., description="프로모션 금액(파트너)")
    total_mall_profit_amt: float = Field(..., description="쇼핑몰수익(수수료수익 - 프로모션금액)")
    display_option_name: str | None = Field(None, description="옵션명:옵션값")
    purchase_yn: str = Field(..., description="공급가 입력")
    total_purchase_price: str = Field(..., description="공급가액")
    total_supply_price: str = Field(..., description="매입가액")
    option_name_for_display: str | None = Field(None, description="노출용 옵션 정보")
    product_name_for_display: str = Field(..., description="노출용 상품 정보")
    total_pay_amt: float = Field(..., description="결제금액 = 판매금액 - 프로모션할인금액")


class StatisticsSalesProductResponse(BaseDto):
    """
    판매통계 상품별 목록 조회 응답

    OpenAPI Schema: statistics-sales-product1026505609
    """

    total_count: int = Field(..., description="판매통계 상품별 총 개수")
    contents: list[StatisticsSalesProductItem] = Field(
        default_factory=list, description="판매통계 상품별 목록"
    )


# ====================================
#  판매통계 요약 (GET /statistics/sales/period/summary, /statistics/sales/product/summary)
# ====================================
class StatisticsSalesSummary(BaseDto):
    """판매통계 요약정보"""

    total_order_cnt: int = Field(..., description="판매건수")
    total_normal_order_cnt: int = Field(..., description="정상 판매건수")
    total_claimed_order_cnt: int = Field(..., description="클레임 판매건수")
    total_product_cnt: int = Field(..., description="판매상품수")
    total_normal_product_cnt: int = Field(..., description="정상 판매상품수")
    total_claimed_product_cnt: int = Field(..., description="클레임 판매상품수")
    total_sale_cnt: int = Field(..., description="판매수량")
    total_sale_amt: float = Field(..., description="판매금액")
    total_additional_discount_amt: float = Field(..., description="추가할인")
    total_product_coupon_amt: float = Field(..., description="상품쿠폰 할인금액")
    total_cart_coupon_amt: float = Field(..., description="장바구니 할인금액")
    total_accumulation_amt: float = Field(..., description="적립금 사용금액")
    total_delivery_amt: float = Field(..., description="배송비")
    total_refund_amt: float = Field(..., description="환불 금액")
    total_free_gift_amt: float = Field(..., description="사은품 할인금액")
    total_external_pay_amt: float = Field(..., description="외부 결제 결제금액")
    total_product_promotion_discount_amt: float = Field(..., description="상품 프로모션할인금액")
    total_product_sale_amt: float = Field(..., description="총 상품판매금액")
    total_promotion_discount_amt: float = Field(..., description="프로모션할인금액")
    total_sales_amt: float = Field(..., description="총 매출금액")
    total_pay_amt: float = Field(..., description="결제금액")


class StatisticsSalesPromotionSummary(BaseDto):
    """판매통계 프로모션 요약정보"""

    total_mall_free_gift_amt: float = Field(..., description="몰 사은품 할인 금액")
    total_partner_free_gift_amt: float = Field(..., description="파트너 사은품 할인 금액")
    total_free_gift_amt: float = Field(..., description="사은품 할인 금액 합계(몰 + 파트너)")
    total_mall_additional_discount_amt: float = Field(..., description="몰 추가 할인 금액")
    total_partner_additional_discount_amt: float = Field(..., description="파트너 추가 할인 금액")
    total_additional_discount_amt: float = Field(..., description="추가 할인 금액 합계(몰 + 파트너)")
    total_mall_product_coupon_amt: float = Field(..., description="몰 상품쿠폰 할인 금액")
    total_partner_product_coupon_amt: float = Field(..., description="파트너 상품쿠폰 할인 금액")
    total_product_coupon_amt: float = Field(..., description="상품쿠폰 할인 금액(몰 + 파트너)")
    total_cart_coupon_amt: float = Field(..., description="장바구니쿠폰 할인 금액")


class StatisticsSalesSummaryResponse(BaseDto):
    """
    판매통계 요약 조회 응답 (기간별/상품별 공통)

    OpenAPI Schema: statistics-sales-product-summary2027962557
    """

    start_ymd: str = Field(..., description="조회시작일")
    end_ymd: str = Field(..., description="조회종료일")
    mall_no: int = Field(..., description="몰번호")
    partner_no: int = Field(..., description="파트너번호")
    display_brand_no: int = Field(..., description="전시브랜드 번호")
    summary: StatisticsSalesSummary = Field(..., description="판매통계 요약정보")
    promotion_summary: StatisticsSalesPromotionSummary = Field(
        ..., description="판매통계 프로모션 요약정보"
    )


__all__ = [
    # Literal 타입 별칭
    "CsType",
    "CsChannelType",
    "CsStatusType",
    "CsPathType",
    "SettlementPartnerType",
    "CouponType",
    "GenderType",
    "MemberJoinType",
    "MemberType",
    "PlatformType",
    "PromotionKeywordType",
    "ProductKeywordType",
    "ProductType",
    "SaleMethodType",
    "PayType",
    # CS
    "CsAudit",
    "CsItem",
    "CsResponse",
    # Orders Sales
    "OrdersSalesMemberGroupInfo",
    "OrdersSalesMemberInfo",
    "OrdersSalesSetOption",
    "OrdersSalesProductInfo",
    "OrdersSalesPriceInfo",
    "OrdersSalesPaymentInfo",
    "OrdersSalesCouponInfo",
    "OrdersSalesItem",
    "OrdersSalesResponse",
    # Settlement
    "SettlementItem",
    "SettlementDetailItem",
    "SettlementDetailResponse",
    # Statistics - Promotions
    "StatisticsPromotionCoupon",
    "StatisticsPromotionsResponse",
    "StatisticsPromotionDetailItem",
    # Statistics - Sales
    "StatisticsSalesPeriodItem",
    "StatisticsSalesPeriodResponse",
    "StatisticsSalesProductItem",
    "StatisticsSalesProductResponse",
    "StatisticsSalesSummary",
    "StatisticsSalesPromotionSummary",
    "StatisticsSalesSummaryResponse",
]

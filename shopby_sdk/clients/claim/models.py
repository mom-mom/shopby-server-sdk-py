"""Claim API 모델 정의

OpenAPI: claim-server (docs/api/claim-server-public.yml)

camelCase <-> snake_case 자동변환은 BaseDto 가 처리합니다.
"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime

# ---------------------------------------------------------------------------
# Literal 타입 별칭 (enum)
# ---------------------------------------------------------------------------

ResponsibleObjectType = Literal["BUYER", "SELLER"]
"""귀책 대상 (BUYER: 구매자귀책, SELLER: 판매자귀책)"""

ClaimType = Literal["CANCEL", "RETURN", "EXCHANGE"]
"""클레임 유형 (CANCEL: 취소, RETURN: 반품, EXCHANGE: 교환)"""

ClaimReasonType = Literal[
    "CHANGE_MIND",
    "DEFECTIVE_PRODUCT",
    "WRONG_DELIVERY",
    "OUT_OF_STOCK_SYSTEM",
    "CANCEL_BEFORE_PAY",
    "WRONG_PRODUCT_DETAIL",
    "DELAY_DELIVERY",
    "OTHERS_SELLER",
    "OTHERS_BUYER",
    "OUT_OF_STOCK",
    "LATER_INPUT_ORDER",
    "LATER_INPUT_ORDER_RECEIVER_CANCEL",
]
"""클레임 사유"""

RefundType = Literal[
    "PG",
    "ACCUMULATION",
    "ACCOUNT",
    "ZERO_REFUND",
    "EXTERNAL_PAY",
    "ADMIN_ETC",
]
"""환불 방법"""

ReturnWayType = Literal["SELLER_COLLECT", "BUYER_DIRECT_RETURN"]
"""반품수거 방법 (SELLER_COLLECT: 판매자수거요청, BUYER_DIRECT_RETURN: 구매자직접반품)"""

AdditionalPayType = Literal["CASH", "ACCUMULATION", "NAVER_PAY"]
"""추가결제 방법 (CASH: 무통장입금, ACCUMULATION: 적립금 전액 사용, NAVER_PAY: 네이버페이 주문형)"""

ClaimSearchType = Literal["ALL", "CLAIM_NO", "ORDER_NO", "MEMBER_NO"]
"""클레임 검색 타입"""

ClaimSearchDateType = Literal["APPLY_YMDT", "COMPLETE_YMDT"]
"""클레임 검색일자 타입 (APPLY_YMDT: 클레임일자, COMPLETE_YMDT: 클레임완료일자)"""

ClaimStatusType = Literal[
    "CANCEL_NO_REFUND",
    "CANCEL_REQUEST",
    "CANCEL_PROC_REQUEST_REFUND",
    "CANCEL_PROC_WAITING_REFUND",
    "CANCEL_DONE",
    "EXCHANGE_REQUEST",
    "EXCHANGE_REJECT_REQUEST",
    "EXCHANGE_PROC_BEFORE_RECEIVE",
    "EXCHANGE_PROC_REQUEST_PAY",
    "EXCHANGE_PROC_REQUEST_REFUND",
    "EXCHANGE_PROC_WAITING",
    "EXCHANGE_PROC_WAITING_PAY",
    "EXCHANGE_PROC_WAITING_REFUND",
    "EXCHANGE_DONE_PAY_DONE",
    "EXCHANGE_DONE_REFUND_DONE",
    "EXCHANGE_DONE",
    "RETURN_NO_REFUND",
    "RETURN_REQUEST",
    "RETURN_REJECT_REQUEST",
    "RETURN_PROC_BEFORE_RECEIVE",
    "RETURN_PROC_REQUEST_REFUND",
    "RETURN_PROC_WAITING_REFUND",
    "RETURN_DONE",
    "RETURN_REFUND_AMT_ADJUST_REQUESTED",
]
"""클레임 상태"""

TreatmentStatusType = Literal[
    "REQUEST",
    "APPROVE",
    "ALREADY_RELEASE",
    "WITHDRAW",
    "WITHDRAW_REQUEST",
    "WITHDRAW_APPROVE",
    "COLLECT_RETURN_PROD",
    "CONFIRM_DEPOSIT",
    "REFUND_DONE",
    "DELETE",
]
"""클레임 처리 상태"""

BankType = Literal[
    "ANONYMOUS",
    "KDB",
    "IBK",
    "KB",
    "KEB",
    "SUHYUP",
    "KEXIM",
    "NH",
    "NHLOCAL",
    "WOORI",
    "SC",
    "CITY",
    "SUHYUP_LOCAL_BANK",
    "DAEGU",
    "PUSAN",
    "GWANGJU",
    "JEJU",
    "JEONBUK",
    "GYEONGNAM",
    "KFCC",
    "CU",
    "SANGHO",
    "HSBC",
    "DEUTSCHE",
    "NFCF",
    "EPOST",
    "KEBHANA",
    "SHINHAN",
    "KBANK",
    "KAKAO",
    "TOSS",
    "YUANTA",
    "KBSEC",
    "MIRAE",
    "MIRAEDAEWOO",
    "SAMSUNG",
    "HANKOOK",
    "NH_INVEST",
    "KYOBO",
    "HI_INVEST",
    "HMC_INVEST",
    "KIWOOM",
    "EBEST",
    "SK",
    "DAISHIN",
    "SOLOMON_INVEST",
    "HANHWA",
    "HANA_INVEST",
    "SHINHAN_INVEST",
    "DONGBU",
    "EUGENE_INVEST",
    "MERITZ_COMPREHENSIVE",
    "BOOKOOK",
    "SHINYOUNG",
    "CAPE",
]
"""은행 코드"""

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


# ---------------------------------------------------------------------------
# 공통 서브 모델
# ---------------------------------------------------------------------------
class BankAccount(BaseDto):
    """은행 계좌 정보 (환불계좌 / 추가결제 입금계좌)"""

    bank_name: str = Field(..., description="은행명")
    bank: BankType | None = Field(None, description="은행코드")
    account: str | None = Field(None, description="계좌번호")
    depositor_name: str | None = Field(None, description="계좌소유자명")


class PurchaserInput(BaseDto):
    """구매자 작성형 옵션"""

    input_label: str = Field(..., description="구매자 작성형 입력 이름")
    input_value: str = Field(..., description="구매자 작성형 입력 값")


# ---------------------------------------------------------------------------
# 옵션 취소 (POST /option-cancels)
# ---------------------------------------------------------------------------
class OptionCancelParam(BaseDto):
    """옵션 취소 - 클레임 옵션 정보"""

    order_option_no: int = Field(..., description="옵션번호")
    claim_cnt: int = Field(..., description="클레임 수량")
    reason_type: ClaimReasonType | None = Field(None, description="클레임사유")
    reason_detail: str | None = Field(None, description="클레임사유-상세")


class OptionCancelRequest(BaseDto):
    """옵션 취소 신청 요청

    OpenAPI Schema: option-cancels1365966632
    """

    order_no: str = Field(..., description="주문번호")
    order_option_params: list[OptionCancelParam] = Field(
        default_factory=list, description="클레임 옵션 정보"
    )
    responsible_object_type: ResponsibleObjectType = Field(..., description="귀책사유")
    seller_pays_claimed_delivery: bool = Field(
        ..., description="초도배송비 판매자 부담 여부(true이면 판매자가 추가되는 초도배송비를 부담)"
    )
    reason_type: ClaimReasonType | None = Field(None, description="클레임사유")
    reason_detail: str | None = Field(None, description="클레임사유-상세")
    refund_bank_account: BankAccount | None = Field(None, description="환불계좌(환불시)")
    # request-only, 스펙상 자유형식 object(properties 없음) → 구조 추론 불가, dict 유지
    complex_refund_adjust: dict[str, Any] | None = Field(
        None,
        description=(
            "결제수단 별 환불금액(관리자 지정 환불·개발중). 스펙 미정의·example 전부 null 이라 dict 유지. "
            "추정 키(환불가능금액 조회 응답과 대칭): "
            "{pgRefundAmt, cashRefundAmt, accumulationRefundAmt, externalPayRefundAmts:[{externalPayKey, refundAmt}]}"
        ),
    )


# ---------------------------------------------------------------------------
# 품절 취소 (POST /option-cancels/sold-out)
# ---------------------------------------------------------------------------
class SoldOutCancelRequest(BaseDto):
    """품절 취소처리 요청

    OpenAPI Schema: option-cancels-sold-out2041411915
    """

    order_option_nos: list[int] = Field(default_factory=list, description="품절 주문 옵션번호")


# ---------------------------------------------------------------------------
# 세트옵션 품절 취소 (POST /option-cancels/sold-out/set-option)
# ---------------------------------------------------------------------------
class SoldOutSetOption(BaseDto):
    """세트옵션 품절 취소 - 품절 주문 옵션"""

    order_option_no: int = Field(..., description="품절 주문 옵션번호")
    sold_out_mall_option_nos: list[int] = Field(
        default_factory=list, description="품절이 된 세트 상품 옵션번호"
    )


class SoldOutSetOptionRequest(BaseDto):
    """세트옵션 품절 취소처리 요청

    OpenAPI Schema: option-cancels-sold-out-set-option1925829967
    """

    order_options: list[SoldOutSetOption] = Field(
        default_factory=list, description="품절 주문 옵션"
    )


# ---------------------------------------------------------------------------
# 주문 취소 (POST /order-cancels)
# ---------------------------------------------------------------------------
class OrderCancelRequest(BaseDto):
    """주문 취소 신청 요청

    OpenAPI Schema: order-cancels1019577912
    """

    order_no: str = Field(..., description="주문번호")
    reason_type: ClaimReasonType = Field(..., description="취소사유")
    refund_type: RefundType = Field(..., description="환불방법")
    responsible_object_type: ResponsibleObjectType = Field(..., description="귀책")
    reason_detail: str | None = Field(None, description="취소사유-상세")
    refund_bank_account: BankAccount | None = Field(None, description="환불계좌")


# ---------------------------------------------------------------------------
# 취소교환 신청 (POST /cancel-exchanges)
# ---------------------------------------------------------------------------
class CancelExchangeCalculateParam(BaseDto):
    """취소교환 계산값

    OpenAPI Schema: cancel-exchanges-753066568.calculateParam
    """

    order_no: str = Field(..., description="주문번호")
    cancel_order_option_no: int = Field(..., description="취소할 주문옵션번호")
    cancel_cnt: int = Field(..., description="취소수량")
    responsible_object_type: ResponsibleObjectType = Field(..., description="귀책사유")
    seller_pays_claimed_delivery: bool = Field(
        ..., description="초도배송비 판매자 부담 여부(true이면 판매자가 추가되는 초도배송비를 부담)"
    )
    exchange_product_no: int | None = Field(None, description="교환할상품번호")
    exchange_option_no: int | None = Field(None, description="교환할옵션번호")
    exchange_cnt: int | None = Field(None, description="교환할수량")
    refund_type: RefundType | None = Field(None, description="환불방법")
    product_adjust_amt: float | None = Field(
        None, description="상품조정금액(추가되는 상품 차액을 쇼핑몰이 부담하는 경우 입력)"
    )
    # request-only, 스펙상 자유형식 object(properties 없음) → 구조 추론 불가, dict 유지
    complex_refund_adjust: dict[str, Any] | None = Field(
        None,
        description=(
            "결제수단 별 환불금액(관리자 지정 환불·개발중, refundType 은 ADMIN_ETC 입력). "
            "스펙 미정의·example 전부 null 이라 dict 유지. 추정 키(환불가능금액 조회 응답과 대칭): "
            "{pgRefundAmt, cashRefundAmt, accumulationRefundAmt, externalPayRefundAmts:[{externalPayKey, refundAmt}]}"
        ),
    )


class CancelExchangeRequest(BaseDto):
    """취소교환 신청 요청

    OpenAPI Schema: cancel-exchanges-753066568
    """

    calculate_param: CancelExchangeCalculateParam = Field(..., description="계산값")
    reason_type: ClaimReasonType = Field(..., description="클레임사유")
    purchaser_inputs: list[PurchaserInput] = Field(
        default_factory=list, description="구매자 작성형 옵션"
    )
    reason_detail: str | None = Field(None, description="클레임사유-상세")
    product_adjust_reason: str | None = Field(None, description="상품조정금액입력사유")
    additional_pay_type: AdditionalPayType | None = Field(None, description="추가결제방법")
    additional_pay_bank_account: BankAccount | None = Field(
        None, description="추가결제입금계좌(추가결제시)"
    )
    additional_pay_remitter: str | None = Field(None, description="입금자명(추가결제시)")
    refund_bank_account: BankAccount | None = Field(None, description="환불계좌(환불시)")


# ---------------------------------------------------------------------------
# 취소교환/반품교환 추가결제 입금확인
# (PUT /cancel-exchanges/{no}/confirm-deposit,
#  PUT /return-exchanges/{no}/confirm-deposit)
# ---------------------------------------------------------------------------
class ConfirmDepositRequest(BaseDto):
    """추가결제 입금확인 요청

    OpenAPI Schema: cancel-exchanges-no-confirm-deposit1217307166
    """

    additional_pay_bank_account: BankAccount | None = Field(
        None, description="추가결제입금계좌(추가결제시)"
    )
    additional_pay_remitter: str | None = Field(None, description="입금자명(추가결제시)")


# ---------------------------------------------------------------------------
# 반품/반품교환 주소 모델
# ---------------------------------------------------------------------------
class ClaimAddress(BaseDto):
    """반품수거지 / 교환출고지 주소 (반품교환 신청용)"""

    zip_cd: str = Field(..., description="우편번호")
    address: str = Field(..., description="주소")
    name: str = Field(..., description="수령자명")
    contact1: str = Field(..., description="연락처1")
    jibun_address: str | None = Field(None, description="지번주소")
    detail_address: str | None = Field(None, description="세부주소")
    contact2: str | None = Field(None, description="연락처2")
    mobile_country_cd: str | None = Field(None, description="휴대폰번호 국가 코드")
    country_cd: str | None = Field(None, description="국가 코드")
    receiver_city: str | None = Field(None, description="(해외) 도시")
    receiver_state: str | None = Field(None, description="(해외) 주")
    customs_id_number: str | None = Field(None, description="개인고유통관부호")
    receiver_first_name: str | None = Field(
        None, description="(해외배송 / 글로벌결제 시 필수) 수령인 FirstName"
    )
    receiver_last_name: str | None = Field(
        None, description="(해외배송 / 글로벌결제 시 필수) 수령인 LastName"
    )


class ReturnAddress(BaseDto):
    """반품주소 (반품신청용)

    OpenAPI Schema: returns-495843492.returnAddress
    """

    receiver_name: str = Field(..., description="수령자명")
    receiver_zip_cd: str = Field(..., description="수령자우편번호")
    receiver_address: str = Field(..., description="수령자주소")
    receiver_contact1: str = Field(..., description="수령자연락처1")
    receiver_jibun_address: str | None = Field(None, description="수령자지번주소")
    receiver_detail_address: str | None = Field(None, description="수령자상세주소")
    receiver_contact2: str | None = Field(None, description="수령자연락처2")
    receiver_mobile_country_cd: str | None = Field(
        None, description="수령자 휴대폰번호 국가 코드"
    )
    country_cd: str | None = Field(None, description="국가코드")
    receiver_city: str | None = Field(None, description="(해외) 도시")
    receiver_state: str | None = Field(None, description="(해외) 주")
    customs_id_number: str | None = Field(None, description="개인통관고유부호(해외배송상품인 경우 필수)")
    delivery_memo: str | None = Field(None, description="배송메모")
    receiver_first_name: str | None = Field(None, description="(해외배송 시 필수) 수령인 firstName")
    receiver_last_name: str | None = Field(None, description="(해외배송 시 필수) 수령인 lastName")


# ---------------------------------------------------------------------------
# 반품교환 신청 (POST /return-exchanges) - V1.1
# ---------------------------------------------------------------------------
class ReturnExchangeCalculateParam(BaseDto):
    """반품교환 계산값 (V1.1)

    OpenAPI Schema: return-exchanges525691568.calculateParam
    """

    order_no: str = Field(..., description="주문번호")
    cancel_order_option_no: int = Field(..., description="취소할 주문옵션번호")
    cancel_cnt: int = Field(..., description="취소수량")
    responsible_object_type: ResponsibleObjectType = Field(..., description="귀책사유")
    seller_pays_claimed_delivery: bool = Field(
        ..., description="초도배송비 판매자 부담 여부(true이면 판매자가 추가되는 초도배송비를 부담)"
    )
    return_way_type: ReturnWayType = Field(..., description="반품수거 방법")
    return_delivery_proposed_amt: float = Field(
        ..., description="반품배송비조정액(추가되는 반품배송비를 쇼핑몰이 부담하는 경우 입력)"
    )
    exchange_delivery_proposed_amt: float = Field(
        ..., description="교환배송비조정액(추가되는 교환재배송배송비를 쇼핑몰이 부담하는 경우 입력)"
    )
    exchange_product_no: int | None = Field(None, description="교환할상품번호")
    exchange_option_no: int | None = Field(None, description="교환할옵션번호")
    exchange_cnt: int | None = Field(None, description="교환할수량")
    refund_type: RefundType | None = Field(None, description="환불방법")
    product_adjust_amt: float | None = Field(
        None, description="상품조정금액(추가되는 상품 차액을 쇼핑몰이 부담하는 경우 입력)"
    )
    return_address: ClaimAddress | None = Field(None, description="반품수거지 주소")
    exchange_address: ClaimAddress | None = Field(None, description="교환출고지 주소")
    # request-only, 스펙상 자유형식 object(properties 없음) → 구조 추론 불가, dict 유지
    complex_refund_adjust: dict[str, Any] | None = Field(
        None,
        description=(
            "결제수단 별 환불금액(관리자 지정 환불·개발중, refundType 은 ADMIN_ETC 입력). "
            "스펙 미정의·example 전부 null 이라 dict 유지. 추정 키(환불가능금액 조회 응답과 대칭): "
            "{pgRefundAmt, cashRefundAmt, accumulationRefundAmt, externalPayRefundAmts:[{externalPayKey, refundAmt}]}"
        ),
    )


class ReturnExchangeRequest(BaseDto):
    """반품교환 신청 요청 (V1.1)

    OpenAPI Schema: return-exchanges525691568
    """

    calculate_param: ReturnExchangeCalculateParam = Field(..., description="계산값")
    reason_type: ClaimReasonType = Field(..., description="클레임사유")
    purchaser_inputs: list[PurchaserInput] = Field(
        default_factory=list, description="구매자 작성형 옵션"
    )
    reason_detail: str | None = Field(None, description="클레임사유-상세")
    invoice_no: str | None = Field(None, description="반품송장 번호")
    delivery_company_type: DeliveryCompanyType | None = Field(None, description="택배사")
    return_delivery_note: str | None = Field(None, description="반품 배송메모")
    exchange_delivery_note: str | None = Field(None, description="교환 배송메모")
    return_delivery_adjust_reason: str | None = Field(None, description="반품배송비조정사유")
    exchange_delivery_adjust_reason: str | None = Field(None, description="교환배송비조정사유")
    product_adjust_reason: str | None = Field(None, description="상품조정금액입력사유")
    return_exchange_images: list[str] | None = Field(None, description="반품교환 이미지")
    additional_pay_type: AdditionalPayType | None = Field(None, description="추가결제방법")
    additional_pay_bank_account: BankAccount | None = Field(
        None, description="추가결제입금계좌(추가결제시)"
    )
    additional_pay_remitter: str | None = Field(None, description="입금자명(추가결제시)")
    refund_bank_account: BankAccount | None = Field(None, description="환불계좌(환불시)")


# ---------------------------------------------------------------------------
# 반품교환 수거완료 (PUT /return-exchanges/{no}/collect)
# ---------------------------------------------------------------------------
class ReturnExchangeCollectRequest(BaseDto):
    """반품교환 수거완료 요청

    OpenAPI Schema: return-exchanges-no-collect-1943409195
    """

    restores_stock: bool = Field(
        ..., description="재고복원여부 - 교환은 대상상품이 1개이기 때문에 true/false로만 선택"
    )


# ---------------------------------------------------------------------------
# 반품 신청 (POST /returns) - V1.1
# ---------------------------------------------------------------------------
class ReturnProductOption(BaseDto):
    """반품 - 주문상품 옵션정보"""

    order_product_option_no: int = Field(..., description="주문 상품 옵션 번호")
    product_cnt: int = Field(..., description="취소/반품할 제품수량")
    reason_type: ClaimReasonType | None = Field(None, description="클레임사유")
    reason_detail: str | None = Field(None, description="클레임사유-상세")


class ReturnRequest(BaseDto):
    """반품 신청 요청 (V1.1)

    OpenAPI Schema: returns-495843492
    """

    claimed_product_options: list[ReturnProductOption] = Field(
        default_factory=list, description="주문상품 옵션정보"
    )
    return_delivery_proposed_amt: float = Field(..., description="반품배송비 조정금액")
    return_delivery_adjust_reason: str = Field(..., description="반품 배송비 조정사유")
    save_bank_account_info: bool = Field(
        ..., description="환불계좌정보 저장 여부(true일 경우 bankAccountInfo 필수)"
    )
    claim_reason_type: ClaimReasonType | None = Field(None, description="클레임사유")
    claim_reason_detail: str | None = Field(None, description="상세사유")
    responsible_object_type: ResponsibleObjectType | None = Field(None, description="귀책")
    return_way_type: ReturnWayType | None = Field(None, description="반품상품 수거방법")
    return_address: ReturnAddress | None = Field(
        None, description="반품주소(배송상품인 경우 필수, 배송안함상품인 경우 null 가능)"
    )
    bank_account_info: BankAccount | None = Field(None, description="환불계좌정보")
    delivery_company_type: DeliveryCompanyType | None = Field(None, description="반품 택배사타입")
    invoice_no: str | None = Field(None, description="반품 송장번호")
    claim_image_urls: list[str] | None = Field(None, description="첨부파일 url 리스트")
    refund_adjust_request_amt: float | None = Field(
        None, description="판매자 환불 조정 요청금액 (배송안함 상품만 환불 조정 가능)"
    )
    refund_adjust_reason: str | None = Field(
        None, description="환불 조정 사유 (배송안함 상품만 환불 조정 가능)"
    )
    is_refund_adjust: bool | None = Field(
        None, description="환불 조정 여부 (배송안함 상품만 환불 조정 가능)"
    )
    # request-only, 스펙상 자유형식 object(properties 없음) → 구조 추론 불가, dict 유지
    complex_refund_request: dict[str, Any] | None = Field(
        None,
        description=(
            "결제수단 별 환불금액(관리자 지정 환불·개발중). 스펙 미정의·example 전부 null 이라 dict 유지. "
            "추정 키(환불가능금액 조회 응답과 대칭): "
            "{pgRefundAmt, cashRefundAmt, accumulationRefundAmt, externalPayRefundAmts:[{externalPayKey, refundAmt}]}"
        ),
    )


# ---------------------------------------------------------------------------
# 반품 수거완료 (PUT /returns/{no}/collect)
# ---------------------------------------------------------------------------
class ReturnCollectRequest(BaseDto):
    """반품 수거완료 요청

    OpenAPI Schema: returns-no-collect-880281392
    """

    restore_stock_order_option_nos: list[int] = Field(
        default_factory=list, description="재고복원하는 옵션번호"
    )
    refund_on_hold: bool = Field(..., description="환불보류 여부")
    refund_hold_proposed_amt: float = Field(..., description="환불보류 조정 요청금액")
    refund_on_hold_reason: str | None = Field(None, description="환불보류사유")


# ---------------------------------------------------------------------------
# 이미출고 (PUT /claims/{claimNo}/already-delivery)
# ---------------------------------------------------------------------------
class AlreadyDeliveryRequest(BaseDto):
    """이미출고 요청

    OpenAPI Schema: claims-claimNo-already-delivery-1650250404
    """

    release_ymd: str = Field(..., description="출고일시(yyyy-MM-dd)")
    delivery_company_type: DeliveryCompanyType | None = Field(None, description="택배사 타입")
    invoice_no: str | None = Field(None, description="송장번호")


# ---------------------------------------------------------------------------
# 반품 송장번호 할당 (PUT /claims/{claimNo}/assign-return-invoice)
# ---------------------------------------------------------------------------
class AssignReturnInvoiceRequest(BaseDto):
    """반품 송장번호 할당 요청

    OpenAPI Schema: claims-claimNo-assign-return-invoice-2002730596
    """

    delivery_company_type: DeliveryCompanyType = Field(..., description="택배사")
    return_invoice_no: str = Field(..., description="반품 송장번호")


# ---------------------------------------------------------------------------
# 관리자 지정 환불 - 환불 가능 금액 조회 (POST /claims/available-complex-refund-amt)
# ---------------------------------------------------------------------------
class ComplexRefundClaimedOption(BaseDto):
    """관리자 지정 환불 - 클레임 옵션 정보"""

    order_option_no: int = Field(..., description="주문옵션번호")
    claim_cnt: int = Field(..., description="클레임 수량")


class ComplexRefundExchangeOption(BaseDto):
    """관리자 지정 환불 - 교환 옵션 정보"""

    mall_product_no: int = Field(..., description="교환상품번호")
    mall_option_no: int = Field(..., description="교환옵션번호")
    exchange_cnt: int = Field(..., description="교환수량")


class AvailableComplexRefundAmtRequest(BaseDto):
    """관리자 지정 환불 - 환불 가능 금액 조회 요청

    OpenAPI Schema: claims-available-complex-refund-amt840466610
    """

    claim_type: ClaimType = Field(..., description="클레임유형")
    order_no: str = Field(..., description="주문번호")
    responsible_object_type: ResponsibleObjectType = Field(..., description="귀책사유")
    seller_pays_claimed_delivery: bool = Field(
        ...,
        description="판매자 초도배송비 부담 여부(판매자 귀책에서만 사용, true이면 판매자가 반품배송비를 부담)",
    )
    claimed_options: list[ComplexRefundClaimedOption] = Field(
        default_factory=list, description="클레임 옵션 정보"
    )
    return_way_type: ReturnWayType | None = Field(None, description="반품 배송 유형")
    exchange_option: ComplexRefundExchangeOption | None = Field(
        None, description="교환 옵션 정보"
    )


class ExternalPayRefundAmt(BaseDto):
    """외부결제 환불 가능 금액"""

    external_pay_key: str = Field(..., description="외부결제 키")
    refund_amt: float = Field(..., description="금액")


class AvailableComplexRefundAmtResponse(BaseDto):
    """관리자 지정 환불 - 환불 가능 금액 조회 응답

    OpenAPI Schema: claims-available-complex-refund-amt-2002438613
    """

    refund_amt: float = Field(..., description="총 환불 금액")
    available_pg_refund_amt: float = Field(..., description="최대 환불 가능한 PG 반환 금액")
    available_cash_refund_amt: float = Field(..., description="최대 환불 가능한 현금 반환 금액")
    available_accumulation_refund_amt: float = Field(
        ..., description="최대 환불 가능한 적립금 반환 금액"
    )
    available_external_pay_refund_amts: list[ExternalPayRefundAmt] = Field(
        default_factory=list, description="최대 환불 가능한 외부결제"
    )


# ---------------------------------------------------------------------------
# 반품/반품교환 신청 응답 (POST /returns, POST /return-exchanges)
# ---------------------------------------------------------------------------
class ClaimedOptionResult(BaseDto):
    """클레임된 옵션 결과"""

    order_option_no: int = Field(..., description="클레임된 주문 옵션 번호")
    order_cnt: int = Field(..., description="클레임된 수량")
    origin_order_option_no: int | None = Field(
        None, description="원주문 옵션 번호, 부분 클레임으로 옵션이 쪼개지는 경우에만 응답"
    )
    origin_order_cnt: int | None = Field(
        None, description="원주문 수량, 부분 클레임으로 옵션이 쪼개지는 경우에만 응답"
    )


class ClaimResult(BaseDto):
    """반품/반품교환 신청 응답

    OpenAPI Schema: returns1157243429
    """

    claim_no: int = Field(..., description="클레임 번호")
    claimed_options: list[ClaimedOptionResult] = Field(
        default_factory=list, description="클레임된 옵션 목록"
    )


# ---------------------------------------------------------------------------
# 교환 전/후 정보 조회 (GET /claims/{orderNo}/exchange-infos)
# ---------------------------------------------------------------------------
class ExchangeInfo(BaseDto):
    """교환 전/후 옵션 정보

    OpenAPI Schema: claims-orderNo-exchange-infos-1914356139 (array item)
    """

    claim_no: int = Field(..., description="클레임 번호")
    claim_ymdt: KstDatetime = Field(..., description="클레임 신청 시각")
    claim_complete_ymdt: KstDatetime = Field(..., description="클레임 완료 시각")
    claimed_order_product_option_no: int = Field(..., description="클레임된 주문옵션번호")
    claimed_mall_product_no: int = Field(..., description="클레임된 몰 상품번호")
    claimed_mall_option_no: int = Field(..., description="클레임된 몰 옵션번호")
    claimed_product_name: str = Field(..., description="클레임된 상품명")
    claimed_option_name: str = Field(..., description="클레임된 옵션명")
    claimed_option_value: str = Field(..., description="클레임된 옵션값")
    claimed_cnt: int = Field(..., description="클레임된 개수")
    exchanged_order_product_option_no: int = Field(..., description="교환출고된 주문옵션번호")
    exchanged_mall_product_no: int = Field(..., description="교환출고된 몰 상품번호")
    exchanged_mall_option_no: int = Field(..., description="교환출고된 몰 옵션번호")
    exchanged_product_name: str = Field(..., description="교환출고된 상품명")
    exchanged_option_name: str = Field(..., description="교환출고된 옵션명")
    exchanged_option_value: str = Field(..., description="교환출고된 옵션값")
    exchanged_cnt: int = Field(..., description="교환출고된 개수")


# ---------------------------------------------------------------------------
# 클레임 목록 조회 (GET /claims)
# ---------------------------------------------------------------------------
class ShippingEtcInfo(BaseDto):
    """해외배송 관련 기타 필드"""

    receiver_first_name: str | None = Field(
        None, description="(해외배송 시 필수) 수령인 FirstName"
    )
    receiver_last_name: str | None = Field(
        None, description="(해외배송 시 필수) 수령인 LastName"
    )


class ClaimReturnAddress(BaseDto):
    """클레임 반품 수거지 주소 (클레임 목록 응답용)"""

    name: str = Field(..., description="이름")
    address: str = Field(..., description="주소")
    address_view: str = Field(..., description="(zip코드 포함) 수거지 상세 주소")
    zip_cd: str = Field(..., description="우편번호")
    contact1: str = Field(..., description="연락처1")
    country_cd: str = Field(..., description="국가코드")
    contact2: str | None = Field(None, description="연락처2")
    jibun_address: str | None = Field(None, description="지번주소")
    detail_address: str | None = Field(None, description="상세주소")
    mobile_country_cd: str | None = Field(None, description="휴대폰번호 국가 코드")
    receiver_city: str | None = Field(None, description="(해외배송) 도시")
    receiver_state: str | None = Field(None, description="(해외배송) 주")
    customs_id_number: str | None = Field(None, description="개인통관고유부호")
    note: str | None = Field(None, description="배송지메모")
    shipping_etc_info: ShippingEtcInfo | None = Field(None, description="해외배송 관련 기타 필드")


class ClaimedOption(BaseDto):
    """클레임된 옵션 (클레임 목록 응답용)"""

    order_option_no: int = Field(..., description="주문옵션번호")
    claim_cnt: int = Field(..., description="클레임 수량")
    origin_order_option_no: int | None = Field(
        None,
        description="원주문옵션번호 - 부분클레임으로 생성된 옵션인 경우 클레임 처리된 옵션의 번호를 가지게 됨",
    )


# ---------------------------------------------------------------------------
# 클레임 계산 데이터 (claimData) - 실데이터 추론 (운영 572건 기준, 전 필드 안정)
# amounts.before / after / refund 는 동일한 금액 구조(ClaimAmountSnapshot)를 공유한다.
# 금액 필드는 실데이터에서 int/float 혼재이므로 모두 float 로 둔다(pydantic 이 int 허용).
# ---------------------------------------------------------------------------
class ClaimOrderAmount(BaseDto):
    """주문 금액 정보 (amounts.{before,after,refund}.order)"""

    pay_amt: float = Field(..., description="결제금액")
    accumulation_pay_amt: float = Field(..., description="적립금 결제금액")
    standard_amt: float = Field(..., description="판매가 기준 금액")
    immediate_discount_amt: float = Field(..., description="즉시할인 금액")
    additional_discount_amt: float = Field(..., description="추가할인 금액")
    remaining_pg_pay_amt: float = Field(..., description="잔여 PG 결제금액")
    remaining_main_pay_amt: float = Field(..., description="잔여 메인 결제금액")
    free_gift_discount_amt: float = Field(..., description="사은품 할인 금액")
    external_pay_amt: float = Field(..., description="외부결제 금액")
    main_pay_amt: float = Field(..., description="메인 결제금액")
    # 운영데이터에서 항상 빈 배열/null → 아이템 구조 추론 불가, dict 유지
    external_pay_infos: list[dict[str, Any]] | None = Field(
        None, description="외부결제 정보 목록 (운영데이터 전부 빈 배열 → 아이템 구조 추론 불가)"
    )


class ClaimDeliveryGroupAmount(BaseDto):
    """배송그룹 금액 (amounts.{...}.delivery.deliveryGroupAmounts)"""

    delivery_amt: float = Field(..., description="배송비")
    remote_delivery_amt: float = Field(..., description="지역별 추가 배송비")
    prepaid_delivery_amt: float = Field(..., description="선결제 배송비")
    prepaid_remote_delivery_amt: float = Field(..., description="선결제 지역별 추가 배송비")
    pay_on_delivery_amt: float = Field(..., description="착불 배송비")
    pay_on_remote_delivery_amt: float = Field(..., description="착불 지역별 추가 배송비")
    already_paid_total_delivery_amt: float = Field(..., description="기결제 총 배송비")
    total_delivery_amt: float = Field(..., description="총 배송비")
    total_prepaid_delivery_amt: float = Field(..., description="총 선결제 배송비")


class ClaimDeliveryAmount(BaseDto):
    """배송 금액 정보 (amounts.{before,after,refund}.delivery)"""

    delivery_group_amounts: ClaimDeliveryGroupAmount = Field(..., description="배송그룹 금액")
    delivery_amt: float = Field(..., description="배송비")
    remote_delivery_amt: float = Field(..., description="지역별 추가 배송비")
    total_delivery_amt: float = Field(..., description="총 배송비")


class ClaimAccumulationAmount(BaseDto):
    """적립금 금액 정보 (amounts.{before,after,refund}.accumulation)"""

    accumulation_amt: float = Field(..., description="적립금 금액")


class ClaimProductCouponDiscountAmount(BaseDto):
    """상품쿠폰 할인 금액 (coupon.productCouponDiscountAmounts[])"""

    order_product_no: int = Field(..., description="주문상품번호")
    coupon_discount_amt: float = Field(..., description="쿠폰 할인금액")
    mall_product_no: int = Field(..., description="몰 상품번호")


class ClaimCouponAmount(BaseDto):
    """쿠폰 할인 금액 정보 (amounts.{before,after,refund}.coupon)"""

    cart_coupon_discount_amt: float = Field(..., description="장바구니 쿠폰 할인금액")
    product_coupon_discount_amt: float = Field(..., description="상품 쿠폰 할인금액")
    product_coupon_discount_amounts: list[ClaimProductCouponDiscountAmount] | None = Field(
        None, description="상품쿠폰 할인금액 목록"
    )


class ClaimAmountSnapshot(BaseDto):
    """클레임 금액 스냅샷 (amounts.before / amounts.after / amounts.refund)"""

    order: ClaimOrderAmount = Field(..., description="주문 금액")
    delivery: ClaimDeliveryAmount = Field(..., description="배송 금액")
    accumulation: ClaimAccumulationAmount = Field(..., description="적립금 금액")
    coupon: ClaimCouponAmount = Field(..., description="쿠폰 금액")


class ClaimAdjustedAmounts(BaseDto):
    """조정 금액 정보 (amounts.adjustedAmounts)"""

    pay_amt: float = Field(..., description="결제금액")
    main_pay_amt: float = Field(..., description="메인 결제금액")
    accumulation_pay_amt: float = Field(..., description="적립금 결제금액")
    additional_pay_amt: float = Field(..., description="추가결제 금액")
    external_pay_amt: float = Field(..., description="외부결제 금액")
    claim_amt: float = Field(..., description="클레임 금액(환불은 음수)")
    # 운영데이터 전부 null / 빈 배열 → 구조 추론 불가, 보존
    external_pay_infos: list[dict[str, Any]] | None = Field(
        None, description="외부결제 정보 목록 (운영데이터 전부 빈 배열 → 아이템 구조 추론 불가)"
    )
    complex_refund_pg_amt: float | None = Field(
        None, description="관리자 지정 환불 PG 금액 (운영데이터 전부 null)"
    )
    complex_refund_account_amt: float | None = Field(
        None, description="관리자 지정 환불 계좌 금액 (운영데이터 전부 null)"
    )


class ClaimReturnDeliveryAmount(BaseDto):
    """반품 배송 금액 정보 (amounts.returnDelivery, 반품/교환 클레임에만 존재)"""

    return_delivery_amt: float = Field(..., description="반품 배송비")
    return_remote_delivery_amt: float = Field(..., description="반품 지역별 추가 배송비")
    processed_delivery_amt: float = Field(..., description="처리된 배송비")
    prepaid: bool = Field(..., description="선결제 여부")
    prepaid_processed_delivery_amt: float = Field(..., description="선결제 처리 배송비")
    prepaid_total_pure_return_delivery_amt: float = Field(
        ..., description="선결제 순수 반품배송비 합계"
    )
    total_return_delivery_amt: float = Field(..., description="총 반품 배송비")
    total_pure_return_delivery_amt: float = Field(..., description="순수 반품배송비 합계")
    prepaid_return_delivery_amt: float = Field(..., description="선결제 반품 배송비")
    prepaid_return_remote_delivery_amt: float = Field(
        ..., description="선결제 반품 지역별 추가 배송비"
    )
    prepaid_total_return_delivery_amt: float = Field(..., description="선결제 총 반품 배송비")


class ClaimAmounts(BaseDto):
    """클레임 금액 종합 (claimData.amounts)"""

    before: ClaimAmountSnapshot = Field(..., description="클레임 전 금액")
    after: ClaimAmountSnapshot = Field(..., description="클레임 후 금액")
    refund: ClaimAmountSnapshot = Field(..., description="환불 금액")
    adjusted_amounts: ClaimAdjustedAmounts = Field(..., description="조정 금액")
    delivery_adjust_amt: float = Field(..., description="배송비 조정금액")
    refund_delivery_amt: float = Field(..., description="환불 배송비")
    initial_delivery_amt: float = Field(..., description="초도 배송비")
    return_delivery: ClaimReturnDeliveryAmount | None = Field(
        None, description="반품 배송 금액 (반품/교환 클레임에만 존재)"
    )
    return_delivery_adjust_amt: float | None = Field(
        None, description="반품 배송비 조정금액 (반품/교환 클레임에만 존재)"
    )
    refund_adjust_amt: float | None = Field(
        None, description="환불 조정금액 (반품/교환 클레임에만 존재)"
    )


class ClaimShippingAddress(BaseDto):
    """클레임 배송 주소 (claimData.shipping.address)"""

    zip_cd: str = Field(..., description="우편번호")
    address: str = Field(..., description="주소")
    jibun_address: str | None = Field(None, description="지번주소")
    detail_address: str | None = Field(None, description="상세주소")
    name: str = Field(..., description="수령자명")
    contact1: str | None = Field(None, description="연락처1")
    contact2: str | None = Field(None, description="연락처2")
    mobile_country_cd: str | None = Field(None, description="휴대폰번호 국가 코드")
    country_cd: str | None = Field(None, description="국가코드")
    receiver_city: str | None = Field(None, description="(해외) 도시")
    receiver_state: str | None = Field(None, description="(해외) 주")
    customs_id_number: str | None = Field(None, description="개인통관고유부호")
    shipping_etc_info: ShippingEtcInfo | None = Field(None, description="해외배송 관련 기타 필드")


class ClaimShipping(BaseDto):
    """클레임 배송 정보 (claimData.shipping)"""

    original_shipping_no: int = Field(..., description="원배송번호")
    shipping_no: int = Field(..., description="배송번호")
    delivery_group_no: int = Field(..., description="배송그룹번호")
    delivery_template_no: int = Field(..., description="배송템플릿번호")
    delivery_type: str = Field(..., description="배송유형 (예: PARCEL_DELIVERY, NONE)")
    requires_shipping: bool = Field(..., description="배송 필요 여부")
    combined: bool = Field(..., description="묶음배송 여부")
    divided: bool = Field(..., description="분할배송 여부")
    prepaid: bool = Field(..., description="선결제 여부")
    has_adjusted_exchange_delivery_amt: bool = Field(
        ..., description="교환 배송비 조정 여부"
    )
    address: ClaimShippingAddress = Field(..., description="배송 주소")
    invoice_no: str | None = Field(None, description="송장번호")
    delivery_company_type: str | None = Field(None, description="택배사 타입")
    customs_id_number: str | None = Field(None, description="개인통관고유부호")


class ClaimCouponInfo(BaseDto):
    """클레임 쿠폰 단건 정보 (coupon.cartCoupon, coupon.productCoupons[])"""

    coupon_no: int = Field(..., description="쿠폰번호")
    coupon_issue_no: int = Field(..., description="쿠폰발급번호")
    coupon_name: str = Field(..., description="쿠폰명")
    coupon_sub_type: str = Field(..., description="쿠폰 서브타입 (예: NONE, CART)")
    order_product_no: int = Field(..., description="주문상품번호")
    restores: bool = Field(..., description="쿠폰 복원 여부")


class ClaimCoupon(BaseDto):
    """클레임 쿠폰 정보 (claimData.coupon)"""

    cart_coupon: ClaimCouponInfo | None = Field(None, description="장바구니 쿠폰")
    product_coupons: list[ClaimCouponInfo] | None = Field(None, description="상품 쿠폰 목록")


class ClaimData(BaseDto):
    """클레임 계산 데이터 (claimData)

    OpenAPI Schema: claims2026232036.contents[].claimData

    금액/배송/쿠폰 등 클레임 계산 결과. 운영 572건 기준 전 필드 구조 안정.
    금액 필드는 실데이터에서 int/float 혼재이므로 float 로 통일했다.
    """

    amounts: ClaimAmounts = Field(..., description="클레임 금액 정보")
    shipping: ClaimShipping = Field(..., description="배송 정보")
    coupon: ClaimCoupon | None = Field(None, description="쿠폰 정보")
    refund_type: str = Field(..., description="환불 타입 (예: PG, ACCUMULATION)")
    overflows_pg_amt: bool = Field(..., description="PG 금액 초과 여부")


class ClaimListItem(BaseDto):
    """클레임 목록 단건 항목

    OpenAPI Schema: claims2026232036.contents[]
    """

    claim_no: int = Field(..., description="클레임번호")
    claim_amt: float = Field(..., description="클레임금액")
    claim_class_type: str = Field(..., description="클레임 분류 타입 (예: RETURN_EXCHANGE)")
    responsible_object_type: ResponsibleObjectType = Field(..., description="귀책 대상")
    seller_pays_claimed_delivery: bool = Field(
        ..., description="판매자가 초도배송비를 부담할 지 여부"
    )
    mall_no: int | None = Field(None, description="몰 번호")
    member_no: int | None = Field(None, description="회원번호")
    order_no: str | None = Field(None, description="주문번호")
    claim_type: str | None = Field(None, description="클레임타입")
    claim_status_type: ClaimStatusType | None = Field(None, description="클레임상태")
    treatment_status_type: TreatmentStatusType | None = Field(None, description="클레임 처리 상태")
    claim_reason_type: ClaimReasonType | None = Field(None, description="클레임사유")
    claim_reason_detail: str | None = Field(None, description="클레임상세사유")
    claim_ymdt: KstDatetime | None = Field(None, description="클레임일자")
    claim_complete_ymdt: KstDatetime | None = Field(None, description="클레임완료일자")
    refund_type: RefundType | None = Field(None, description="환불수단")
    refund_pay_type: str | None = Field(None, description="환불수단(결제수단)")
    return_way_type: ReturnWayType | None = Field(None, description="반품수거타입")
    return_address: ClaimReturnAddress | None = Field(
        None, description="반품 수거지(반품주소가 있는 경우에만 응답)"
    )
    return_delivery_company_type: DeliveryCompanyType | None = Field(
        None, description="반품 택배사"
    )
    return_delivery_company_type_label: str | None = Field(None, description="반품 택배사명")
    return_invoice_no: str | None = Field(None, description="반품 송장번호")
    order_option_nos: list[int] | None = Field(None, description="주문옵션번호")
    claimed_options: list[ClaimedOption] = Field(
        default_factory=list, description="클레임된 옵션"
    )
    claim_image_urls: list[str] | None = Field(
        None, description="첨부파일 url 리스트 (5개까지 가능)"
    )
    treatment_admin_no: int | None = Field(None, description="클레임 처리 어드민 번호")
    partner_no: int | None = Field(None, description="파트너번호")
    additional_pay_type: str | None = Field(None, description="추가결제 - 결제수단")
    additional_pay_bank_account: BankAccount | None = Field(
        None, description="추가결제 - 입금계좌정보"
    )
    additional_pay_remitter: str | None = Field(None, description="추가결제 - 입금자명")
    first_order_option_no: int | None = Field(None, description="최초 주문옵션번호")
    claim_data: ClaimData | None = Field(
        None, description="클레임 계산 데이터(금액/배송/쿠폰 등)"
    )


class ClaimListResponse(BaseDto):
    """클레임 목록 조회 응답

    OpenAPI Schema: claims2026232036
    """

    total_count: int = Field(..., description="전체 건수")
    contents: list[ClaimListItem] = Field(default_factory=list, description="클레임목록")

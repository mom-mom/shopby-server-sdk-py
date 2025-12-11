"""GET /orders (주문 목록 조회) 응답 모델"""

from typing import Any

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime
from shopby_sdk.clients.order.models.base import (
    BankInfo,
    DeliveryCompanyType,
    ExternalPayInfo,
    OrderStatusType,
    PaymentInfo,
    PayType,
    PlatformType,
    SetOption,
    UserInput,
)


class OrderProductOption(BaseDto):
    """주문 상품 옵션"""

    order_option_no: int | None = Field(None, description="주문옵션번호")
    order_product_option_no: int | None = Field(None, description="주문상품옵션번호")
    mall_option_no: int | None = Field(None, description="몰 옵션번호")
    mall_additional_product_no: int | None = Field(None, description="추가상품번호")
    order_option_type: str | None = Field(None, description="옵션 타입 (NORMAL_OPTION, ADDITIONAL_OPTION)")
    order_status_type: OrderStatusType | None = Field(None, description="주문상태")
    order_cnt: int | None = Field(None, description="주문수량")
    original_order_cnt: int | None = Field(None, description="원 주문수량")
    order_ymdt: KstDatetime | None = Field(None, description="주문일자")
    option_name: str | None = Field(None, description="옵션명")
    option_value: str | None = Field(None, description="옵션값")
    option_use_yn: str | None = Field(None, description="옵션 사용여부")
    option_management_cd: str | None = Field(None, description="옵션관리코드")
    add_price: float | None = Field(None, description="옵션가격(추가금액)")
    sku: str | None = Field(None, description="SKU")
    stock_no: int | None = Field(None, description="재고번호")
    sale_price: float | None = Field(None, description="판매가")
    adjusted_amt: float | None = Field(None, description="조정금액")
    immediate_discount_amt: float | None = Field(None, description="즉시할인 금액")
    additional_discount_amt: float | None = Field(None, description="추가할인 금액")
    product_coupon_discount_amt: float | None = Field(None, description="상품쿠폰 할인금액")
    reservation_yn: str | None = Field(None, description="예약주문 여부")
    delivery_yn: str | None = Field(None, description="배송 여부")
    delivery_complete_ymdt: KstDatetime | None = Field(None, description="배송완료일시")
    buy_confirm_ymdt: KstDatetime | None = Field(None, description="구매확정일시")
    order_accept_ymdt: KstDatetime | None = Field(None, description="주문승인일시")
    status_change_ymdt: KstDatetime | None = Field(None, description="상태변경일시")
    pay_ymdt: KstDatetime | None = Field(None, description="결제일시")
    release_ready_ymdt: KstDatetime | None = Field(None, description="출고준비일시")
    release_ymdt: KstDatetime | None = Field(None, description="출고일시")
    register_ymdt: KstDatetime | None = Field(None, description="등록일시")
    update_ymdt: KstDatetime | None = Field(None, description="수정일시")
    shipping_area_type: str | None = Field(None, description="배송구분")
    hold_delivery_yn: str | None = Field(None, description="배송보류 여부")
    delivery_combination_yn: str | None = Field(None, description="묶음배송 여부")
    returnable_yn: str | None = Field(None, description="반품 가능여부")
    cancelable_yn: str | None = Field(None, description="취소 가능여부")
    exchangeable_yn: str | None = Field(None, description="교환 가능여부")
    refundable_yn: str | None = Field(None, description="환불 가능여부")
    category_no: int | None = Field(None, description="카테고리번호")
    brand_no: int | None = Field(None, description="브랜드번호")
    partner_no: int | None = Field(None, description="파트너번호")
    partner_name: str | None = Field(None, description="파트너명")
    delivery_partner_no: int | None = Field(None, description="배송파트너번호")
    delivery_template_no: int | None = Field(None, description="배송템플릿번호")
    release_warehouse_no: int | None = Field(None, description="출고창고번호")
    purchase_price: float | None = Field(None, description="매입가/공급가")
    commission_rate: float | None = Field(None, description="수수료율")
    product_type: str | None = Field(None, description="상품유형")
    claim_no: int | None = Field(None, description="클레임번호")
    claim_status_type: str | None = Field(None, description="클레임상태")
    image_url: str | None = Field(None, description="이미지 URL")
    hs_code: str | None = Field(None, description="HS코드")
    user_input_text: str | None = Field(None, description="사용자입력텍스트")
    extra_json: str | None = Field(None, description="추가정보JSON")
    set_option_json: str | None = Field(None, description="세트옵션JSON")
    extra_management_cd: str | None = Field(None, description="추가관리코드")
    hold_yn: str | None = Field(None, description="보류여부")
    exchange_yn: str | None = Field(None, description="교환여부")
    delivery_international_yn: str | None = Field(None, description="해외배송여부")
    free_gift_yn: str | None = Field(None, description="사은품여부")
    origin_order_product_option_no: int | None = Field(None, description="원주문상품옵션번호")
    first_order_option_no: int | None = Field(None, description="최초주문옵션번호")
    member_accumulation_rate: float | None = Field(None, description="회원 적립률")
    mall_product_accumulation_rate: float | None = Field(None, description="상품 적립률")
    additional_discount_no: int | None = Field(None, description="추가할인번호")
    member_grade_no: int | None = Field(None, description="회원등급번호")
    member_grade_name: str | None = Field(None, description="회원등급명")
    recurring_payment_no: int | None = Field(None, description="정기결제번호")
    partner_charge_amt: float | None = Field(None, description="파트너부담금액")
    user_inputs: list[UserInput] = Field(default_factory=list, description="구매자 입력형 옵션")
    set_options: list[SetOption] = Field(default_factory=list, description="세트옵션")
    member_group_infos: list[dict[str, Any]] = Field(default_factory=list, description="회원그룹정보")


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
    last_product_coupon_discount_amt: float | None = Field(None, description="최종 쿠폰할인금액")
    product_coupon_issue_no: int | None = Field(None, description="상품 쿠폰 발행 번호")
    tax_type: str | None = Field(None, description="과세유형")
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
    first_external_pay_infos: list[ExternalPayInfo] | None = Field(None, description="처음 외부결제 정보")
    last_external_pay_infos: list[ExternalPayInfo] | None = Field(None, description="최종 외부결제 정보")
    delivery_groups: list[DeliveryGroup] = Field(default_factory=list, description="배송그룹")


class OrdersResponse(BaseDto):
    """
    주문 조회하기 v1.1 응답

    OpenAPI Schema: orders-410669276
    """

    total_count: int = Field(..., description="전체 주문 수")
    contents: list[Order] = Field(default_factory=list, description="주문 목록")

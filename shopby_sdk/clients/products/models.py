from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDate, KstDatetime


# Nested models
class PlatformDisplayInfo(BaseDto):
    display_yn: str = Field(..., description="전시여부")
    pc_yn: str = Field(..., description="PC 전시여부")
    mobile_yn: str = Field(..., description="모바일앱 전시여부")
    mobile_web_yn: str = Field(..., description="모바일웹 전시여부")


class PromotionTextInfo(BaseDto):
    text: str = Field(..., description="홍보문구")
    period_yn: str = Field(..., description="홍보문구 기간설정 유무")
    start_ymd: KstDate | None = Field(None, description="홍보문구 노출 시작 시간")
    end_ymd: KstDate | None = Field(None, description="홍보문구 노출 종료 시간")


class SalePeriodInfo(BaseDto):
    period_type: Literal["REGULAR", "PERIOD"] = Field(..., description="판매기간설정")
    start_ymdt: KstDatetime = Field(..., description="판매 시작 시간")
    end_ymdt: KstDatetime = Field(..., description="판매 종료 시간")


class ImmediateDiscountInfo(BaseDto):
    unit_type: Literal["AMOUNT", "PERCENT"] = Field(..., description="즉시할인 단위")
    amount: float = Field(..., description="즉시할인 양")
    period_yn: str = Field(..., description="즉시할인 기간설정 여부")
    start_ymdt: KstDatetime | None = Field(None, description="즉시할인 시작 시간")
    end_ymdt: KstDatetime | None = Field(None, description="즉시할인 종료 시간")


class CommissionInfo(BaseDto):
    type: Literal["PRODUCT", "CATEGORY", "PARTNER", "PURCHASE_PRICE"] = Field(..., description="판매수수료타입")
    rate: float = Field(..., description="수수료율")


class MaxBuyCountInfo(BaseDto):
    max_buy_person_cnt: int = Field(..., description="1인당 최대 구매 수량")
    max_buy_time_cnt: int = Field(..., description="1회당 최대 구매 수량")
    max_buy_days: int = Field(..., description="최대구매수량 기간 제한 - 기간")
    max_buy_period_cnt: int = Field(..., description="최대구매수량 기간 제한 - 제한 수량")


class CartInfo(BaseDto):
    use_yn: str = Field(..., description="장바구니 사용 여부")
    off_period_yn: str = Field(..., description="장바구니 OFF 기간 설정 여부")
    off_start_ymd: KstDate | None = Field(None, description="장바구니 OFF 시작일")
    off_end_ymd: KstDate | None = Field(None, description="장바구니 OFF 종료일")


class MallProductImage(BaseDto):
    image_url: str = Field(..., description="이미지 URL")
    origin_image_url: str | None = Field(None, description="사용하지 않음")
    main_yn: str = Field(..., description="메인 이미지 여부")
    display_order: int = Field(..., description="노출 순서")
    image_id: str | None = Field(None, description="사용하지 않음")
    mall_no: int | None = Field(None, description="이미지의 몰번호")  # nonnull 이랬는데 null 도 들어옴
    image_url_type: Literal["IMAGE_URL", "VIDEO_URL"] = Field(..., description="이미지 URL 타입")


class OptionImage(BaseDto):
    mall_option_image_url: str = Field(..., description="옵션 이미지 URL")
    main_yn: str = Field(..., description="메인 옵션 이미지 여부")
    display_order: int = Field(..., description="전시순")


class OptionMapping(BaseDto):
    mall_option_no: int = Field(..., description="옵션 번호")
    item_option_no: int = Field(..., description="구성 옵션 번호")
    mall_product_no: int = Field(..., description="상품 번호")
    item_product_no: int = Field(..., description="구성 상품 번호")
    item_stock_no: int = Field(..., description="재고 번호")
    item_product_name: str = Field(..., description="구성상품명")
    item_product_sale_status_type: str = Field(..., description="구성상품 판매상태")
    item_option_name: str = Field(..., description="구성옵션명")
    item_option_value: str = Field(..., description="구성옵션값")
    item_stock_count: int = Field(..., description="재고량")
    item_option_management_code: str = Field(..., description="구성옵션 관리코드")
    item_extra_management_code: str = Field(..., description="구성옵션 추가관리코드")
    item_original_mapping_option_sale_price: float = Field(..., description="구성옵션 원판매가")
    mapping_cnt: int = Field(..., description="판매묶음 단위개수")
    mapping_option_sale_price: float = Field(..., description="판매가")
    display_order: int = Field(..., description="노출 순서")
    apply_status_type: str = Field(..., description="승인상태")
    sale_status_type: str = Field(..., description="판매상태")
    sale_setting_status_type: str = Field(..., description="판매 설정 상태")
    sku: str | None = Field(None, description="SKU")
    item_combined_option_name_value: str = Field(..., description="옵션이름 옵션값 결합 정보")


class ProductOption(BaseDto):
    mall_option_no: int = Field(..., description="옵션번호")
    stock_no: int = Field(..., description="재고번호")
    option_name: str = Field(..., description="옵션명")
    option_value: str = Field(..., description="옵션값")
    add_price: float = Field(..., description="옵션 추가 가격")
    use_yn: str = Field(..., description="옵션 사용여부")
    option_management_cd: str = Field(..., description="옵션 관리코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")
    stock_cnt: int = Field(..., description="옵션 재고 수량")
    reservation_stock_cnt: int = Field(..., description="예약 재고 수량")
    purchase_price: float = Field(..., description="공급가")
    option_images: list[OptionImage] = Field(default_factory=list, description="옵션 이미지")
    mappings: list[OptionMapping] = Field(default_factory=list, description="옵션 맵핑 정보(세트옵션)")
    deletable: bool = Field(..., description="삭제 가능여부")
    sku: str = Field(..., description="SKU")
    display_order: int = Field(..., description="노출순서")
    forced_sold_out: bool = Field(..., description="임시품절여부")
    is_required_option: bool = Field(..., description="필수 옵션 여부")


class MemberGradeDisplayInfo(BaseDto):
    check: str = Field(..., description="회원등급 전시 체크")
    info: list[Any] = Field(default_factory=list, description="회원등급 정보")


class MemberGroupDisplayInfo(BaseDto):
    check: str = Field(..., description="회원그룹 전시 체크")
    info: list[Any] = Field(default_factory=list, description="회원그룹 정보")


class PromotionInfo(BaseDto):
    promotion_yn: str = Field(..., description="프로모션 사용 여부")
    additional_discount_yn: str = Field(..., description="추가할인 사용 여부")
    coupon_yn: str = Field(..., description="쿠폰 사용 여부")
    free_gift_yn: str = Field(..., description="사은품 사용 여부")


# Main response model
class ProductDetailV3Response(BaseDto):
    """
    상품 상세 조회하기 (Version 3.0) 응답 모델

    OpenAPI Schema: products-mallProductNo--142780588
    """

    # 기본 정보
    mall_product_no: int = Field(..., description="상품번호")
    mall_no: int = Field(..., description="몰번호")
    parent_no: int = Field(..., description="부모 상품 번호, 0 이면 master 상품")
    global_product_no: int = Field(..., description="글로벌상품번호")
    is_main_mall: bool = Field(..., description="메인몰상품여부")
    group_type: str = Field(..., description="그룹타입")
    class_type: str = Field(..., description="클래스타입")
    partner_no: int = Field(..., description="파트너번호")
    sale_method_type: str = Field(..., description="판매방식타입")
    admin_no: int = Field(..., description="관리자번호")

    # 카테고리
    category_no: int = Field(..., description="표준 카테고리 번호")

    # 전시 설정
    url_direct_display_yn: str = Field(..., description="URL 직접 전시 여부")
    platform_display_info: PlatformDisplayInfo = Field(..., description="플랫폼 전시 정보")
    searchengine_display_yn: str = Field(..., description="검색엔진 전시 여부")
    member_grade_display_info: MemberGradeDisplayInfo = Field(..., description="회원등급 전시 정보")
    member_group_display_info: MemberGroupDisplayInfo = Field(..., description="회원그룹 전시 정보")

    # 상품명 및 홍보
    product_name: str = Field(..., description="상품명")
    product_name_en: str = Field(..., description="영문상품명")
    promotion_text_info: PromotionTextInfo = Field(..., description="홍보문구 등록 정보")

    # 구매 제한
    minor_purchase_yn: str = Field(..., description="미성년자 구매 가능 여부")
    payment_means_control_yn: str = Field(..., description="결제수단제어 여부")
    payment_means: list[Any] = Field(default_factory=list, description="결제수단")
    nonmember_purchase_yn: str = Field(..., description="비회원 구매 가능 여부")

    # 장바구니
    cart_info: CartInfo = Field(..., description="장바구니 정보")

    # 검색어
    keywords: list[str] = Field(default_factory=list, description="검색어")

    # 전시
    front_display_yn: str = Field(..., description="프론트 전시 여부")

    # 판매 기간 및 가격
    sale_period_info: SalePeriodInfo = Field(..., description="판매기간 정보")
    commission_info: CommissionInfo = Field(..., description="판매수수료 정보")
    sale_price: float = Field(..., description="판매가")
    unit_price_info: Any | None = Field(None, description="단가 정보")

    # 할인 정보
    immediate_discount_info: ImmediateDiscountInfo = Field(..., description="즉시할인 정보")

    # 적립금
    accumulation_rate: float | None = Field(None, description="적립금적립 - %")
    partner_charge_amt: float = Field(..., description="파트너 부담 금액")
    accumulation_use_yn: str = Field(..., description="적립금 사용 가능 여부")
    accumulation_limit_info: dict[str, Any] | None = Field(None, description="적립금 제한 정보")

    # 프로모션
    promotion_info: PromotionInfo = Field(..., description="프로모션 정보")

    # 구매 수량
    min_buy_cnt: int = Field(..., description="최소 구매 수량")
    max_buy_count_info: MaxBuyCountInfo = Field(..., description="최대 구매수량 정보")

    # 옵션
    option_use_yn: str = Field(..., description="옵션 사용 여부")
    option_type: str | None = Field(None, description="옵션타입")
    options: list[ProductOption] = Field(default_factory=list, description="옵션정보")

    # 상품정보고시 및 인증
    duty_content: dict[str, Any] | None = Field(None, description="상품정보고시")
    will_duty_content: dict[str, Any] | None = Field(None, description="예정 상품정보고시")
    certification_info: dict[str, Any] = Field(..., description="인증정보")

    # 원산지 및 제조정보
    place_origin_info: dict[str, Any] | None = Field(None, description="원산지 정보")
    manufacture_ymdt: KstDate | None = Field(None, description="제조일자")
    expiration_ymdt: KstDate | None = Field(None, description="유효일자")

    # 부가세
    value_added_tax_type: str = Field(..., description="부가세타입")

    # 관리코드
    product_management_cd: str = Field(..., description="상품 관리코드")
    extra_management_cd: str | None = Field(None, description="추가관리코드")

    # 환불
    refundable_yn: str = Field(..., description="환불가능여부")
    refundable_info: dict[str, Any] = Field(..., description="환불 정보")

    # 기타 코드
    hs_code: str = Field(..., description="HS코드")
    ean_code: str = Field(..., description="EAN코드")

    # 상세 내용
    content_header: str = Field(..., description="상품 상세 상단")
    add_option_image_yn: str = Field(..., description="옵션 이미지 추가 여부")
    content: str = Field(..., description="상품 상세")
    content_footer: str = Field(..., description="상품 상세 하단")

    # 추가 정보
    extra_json: dict[str, Any] = Field(default_factory=dict, description="추가 JSON")

    # 배송 정보
    delivery_yn: str = Field(..., description="배송 여부")
    shipping_area_type: str = Field(..., description="배송 구분")
    shipping_area_partner_no: int = Field(..., description="배송지 파트너 번호")
    delivery_combination_yn: str = Field(..., description="배송비 결합 여부")
    delivery_international_yn: str = Field(..., description="해외배송 여부")
    delivery_template_no: int = Field(..., description="배송 템플릿 번호")
    delivery_customer_info: str = Field(..., description="배송 고객 정보")

    # 상품 타입 및 상태
    product_type: str = Field(..., description="상품 타입")
    apply_status_type: str = Field(..., description="승인상태")
    sale_status_type: str = Field(..., description="판매상태")
    sale_setting_status_type: str = Field(..., description="판매 설정 상태")

    # 브랜드
    brand_no: int = Field(..., description="브랜드 번호")
    display_brand_no: int = Field(..., description="전시브랜드 번호")
    brand_name: str = Field(..., description="브랜드명")

    # 옵션 추가 설정
    option_select_type: str | None = Field(None, description="옵션 선택 타입")

    # 매입가
    purchase_price: float = Field(..., description="공급/매입가")

    # 재고
    product_stock_cnt: int = Field(..., description="상품 재고 수량")

    # 카테고리 목록
    global_display_category_nos: list[int] = Field(default_factory=list, description="글로벌 카테고리 번호")
    display_category_nos: list[int] = Field(default_factory=list, description="전시 카테고리 번호")

    # 이미지
    mall_product_images: list[MallProductImage] = Field(default_factory=list, description="상품 이미지")
    mall_product_list_image: str | None = Field(None, description="리스트 이미지 URL")
    mall_product_list_image_url_type: str = Field(..., description="리스트 이미지 URL 타입")

    # 예약 정보
    reservation_info: Any | None = Field(None, description="예약 정보")

    # 스티커
    sticker_infos: list[dict[str, Any]] = Field(default_factory=list, description="스티커 정보")

    # 커스텀 속성
    custom_property_values: list[Any] = Field(default_factory=list, description="커스텀 속성 값")

    # 배송 지정일
    delivery_due_date: dict[str, Any] | None = Field(None, description="배송지정일")

    # 구매자 작성형
    customer_demands: list[dict[str, Any]] = Field(default_factory=list, description="구매자 작성형")

    # 수정 가능 여부
    modifiable: bool = Field(..., description="수정 가능 여부")

    # 동기화 여부
    synced: bool = Field(..., description="동기화 여부")

    # 단축 URL
    shorten_url: str = Field(..., description="상품 단축URL")

    # 상품 안내
    product_guides: list[dict[str, Any]] = Field(default_factory=list, description="상품 안내")

    # 판매 중지 시 안내 내용
    contents_if_pausing: str = Field(..., description="판매 중지 시 안내 내용")

    # 매입처 상품명
    supplier_product_name: str | None = Field(None, description="매입처 상품명")

    # 관련 상품 정보
    related_product_info: dict[str, Any] | None = Field(None, description="관련 상품 정보")

    # 재입고 알림
    use_restock_noti_yn: str = Field(..., description="재입고 알림 사용 여부")

    # 추가 정보
    extra_info: Any | None = Field(None, description="추가 정보")

    # 총 무게
    total_weight: float = Field(..., description="총 무게")


# ============================================================================
# 상품 검색하기 version 2.0 (검색엔진) Models
# ============================================================================


# Nested models for search
class DisplayPeriod(BaseDto):
    start_date_time: KstDatetime | None = Field(None, description="스티커 노출 시작일자")
    end_date_time: KstDatetime | None = Field(None, description="스티커 노출 종료일자")


class StickerInfo(BaseDto):
    type: Literal["TEXT", "IMAGE"] = Field(..., description="스티커 타입")
    label: str = Field(..., description="스티커 라벨")
    name: str = Field(..., description="스티커 이름")
    display_period: DisplayPeriod | None = Field(None, description="스티커 기간 노출 정보")


class HasCoupons(BaseDto):
    product: bool = Field(..., description="상품쿠폰 태그")
    partner: bool = Field(..., description="파트너쿠폰 태그")
    event: bool = Field(..., description="기획전쿠폰 태그")
    category: bool = Field(..., description="카테고리쿠폰 태그")
    brand: bool = Field(..., description="브랜드쿠폰 태그")


class ReservationData(BaseDto):
    reservation_start_ymdt: KstDatetime = Field(..., description="예약판매 시작일")
    reservation_end_ymdt: KstDatetime = Field(..., description="예약판매 종료일")
    reservation_delivery_ymdt: KstDatetime = Field(..., description="예약판매 배송시작일")
    reservation_stock_cnt: int = Field(..., description="예약판매 재고수량")


class CertificationData(BaseDto):
    certification_category_no: int = Field(..., description="인증유형 번호")
    certification_contents: list[str] = Field(default_factory=list, description="인증기관, 인증번호, 인증상호")


class CertificationInfo(BaseDto):
    type: Literal["TARGET", "NOT_TARGET", "DETAIL_PAGE"] = Field(..., description="인증정보타입")
    data: list[CertificationData] = Field(default_factory=list, description="인증정보")


class AccumulationInfo(BaseDto):
    amount: float = Field(..., description="적립금")
    reward_rate_of_product: float = Field(..., description="상품개별적립률")
    reward_rate_of_member_benefit: float = Field(..., description="회원등급적립률")


class DisplayCategory(BaseDto):
    depth1_no: int = Field(..., description="전시카테고리 1depth 번호")
    depth1_name: str = Field(..., description="전시카테고리 1depth 이름")
    depth2_no: int = Field(..., description="전시카테고리 2depth 번호")
    depth2_name: str = Field(..., description="전시카테고리 2depth 이름")
    depth3_no: int = Field(..., description="전시카테고리 3depth 번호")
    depth3_name: str = Field(..., description="전시카테고리 3depth 이름")
    depth4_no: int = Field(..., description="전시카테고리 4depth 번호")
    depth4_name: str = Field(..., description="전시카테고리 4depth 이름")
    depth5_no: int = Field(..., description="전시카테고리 5depth 번호")
    depth5_name: str = Field(..., description="전시카테고리 5depth 이름")


class OptionValue(BaseDto):
    option_no: int = Field(..., description="옵션번호")
    option_value: str = Field(..., description="옵션명")
    stock_cnt: int = Field(..., description="재고")
    mall_product_no: int = Field(..., description="상품번호")


class ProductSearchItem(BaseDto):
    """
    검색된 상품 아이템

    OpenAPI Schema: products-search-engine--1549367095 > items
    """

    # 기본 정보
    product_no: int = Field(..., description="상품번호")
    product_name: str = Field(..., description="상품명")
    product_name_en: str = Field(..., description="영문 상품명")
    product_type: str | None = Field(None, description="상품타입")
    product_class_type: Literal["DEFAULT", "EVENT", "OFFLINE", "RENTAL"] = Field(..., description="상품유형")
    mapping_type: Literal["SINGLE", "MAPPING"] = Field(..., description="상품등록유형")

    # 파트너 및 홍보
    partner_name: str = Field(..., description="파트너명")
    promotion_text: str | None = Field(None, description="홍보문구")

    # 가격 정보
    sale_price: float = Field(..., description="상품판매가")
    immediate_discount_amt: float = Field(..., description="즉시할인가")
    immediate_discount_unit_type: Literal["WON", "RATE"] = Field(..., description="즉시할인 타입")
    addition_discount_amt: float = Field(..., description="추가상품할인가")
    addition_discount_unit_type: Literal["WON", "RATE"] = Field(..., description="추가상품할인 타입")
    discounted_price: float = Field(..., description="할인 적용된 상품판매가")
    min_sale_price: float = Field(..., description="추가할인 최소 기준금액")
    max_sale_price: float = Field(..., description="추가할인 최대 기준금액")
    max_discount_amount: float = Field(..., description="추가할인 정률 최대 할인 금액")

    # 좋아요 및 리뷰
    liked: bool = Field(..., description="좋아요 여부")
    like_count: int = Field(..., description="좋아요 수")
    review_rating: float = Field(..., description="상품평 평균점")
    total_review_count: int = Field(..., description="총 리뷰 수")

    # 배송 정보
    delivery_condition_type: Literal["FREE", "CONDITIONAL", "FIXED_FEE"] | None = Field(None, description="배송비 타입")
    shipping_area: Literal["PARTNER_SHIPPING_AREA", "MALL_SHIPPING_AREA"] = Field(..., description="배송 구분")

    # 판매 및 재고
    sale_cnt: int = Field(..., description="판매 수량")
    stock_cnt: int = Field(..., description="재고")
    main_stock_cnt: int = Field(..., description="대표 옵션 재고")

    # 브랜드 정보
    brand_no: int = Field(..., description="브랜드 번호")
    brand_name: str = Field(..., description="브랜드 명")
    brand_name_ko: str = Field(..., description="브랜드 한글명")
    brand_name_en: str = Field(..., description="브랜드 영문 명")
    brand_name_type: Literal["NAME_KO", "NAME_EN", "NONE"] = Field(..., description="브랜드명 타입")

    # 스티커
    sticker_infos: list[StickerInfo] = Field(default_factory=list, description="스티커 정보")
    sticker_labels: list[str] = Field(default_factory=list, description="스티커 라벨(배열)")

    # 성인 상품 및 판매 기간
    adult: bool = Field(..., description="성인 상품 여부")
    product_sale_period_type: Literal["REGULAR", "PERIOD"] = Field(..., description="상품의 상품 노출 타입")
    sale_start_ymdt: KstDatetime = Field(..., description="판매시작일시")
    sale_end_ymdt: KstDatetime = Field(..., description="판매종료일시")
    sale_status_type: Literal["READY", "ONSALE", "FINISHED", "STOP", "PROHIBITION"] = Field(..., description="판매상태")

    # 예약 판매
    reservation_data: ReservationData | None = Field(None, description="예약판매정보")

    # 이미지
    image_urls: list[str] = Field(default_factory=list, description="상품 이미지 URL")
    list_image_urls: list[str] = Field(default_factory=list, description="리스트 이미지 URL")

    # 쿠폰
    has_coupons: HasCoupons = Field(..., description="쿠폰여부")
    max_coupon_amt: float = Field(
        ..., description="해당 상품의 옵션을 여러개 구매할 경우 받을 수 있는 최대한의 쿠폰할인 금액"
    )
    coupon_discount_amt: float = Field(..., description="최대 쿠폰 적용 가격")
    enable_coupons: bool | None = Field(None, description="사용가능쿠폰 존재 여부")

    # 등록일 및 기타
    register_ymdt: KstDatetime = Field(..., description="상품 등록일")
    contents_if_pausing: str = Field(..., description="가격대체문구")

    # 카테고리
    display_category_nos: str = Field(..., description="전시카테고리 번호 정보")
    display_category_names: list[str] = Field(default_factory=list, description="전시카테고리 명")
    display_categories: list[DisplayCategory] | None = Field(None, description="전시카테고리")

    # 전시 여부
    front_display_yn: bool = Field(..., description="전시 여부")
    url_direct_display_yn: bool = Field(..., description="상품조회화면 노출 여부")

    # 관리 코드
    product_management_cd: str | None = Field(None, description="판매자 관리코드")
    group_management_code: str | None = Field(None, description="그룹관리코드")
    group_management_code_name: str | None = Field(None, description="그룹관리코드 노출명")

    # HS 코드
    hs_code: str | None = Field(None, description="HS CODE")

    # 인증 정보
    certification_info: CertificationInfo | None = Field(None, description="인증정보")

    # 적립금 정보
    accumulation_info: AccumulationInfo | None = Field(None, description="적립금 정보")

    # 옵션 정보
    option_values: list[OptionValue] | None = Field(None, description="상품 조합형 옵션정보")

    # Deprecated (스펙은 string이지만 실제로 빈 리스트가 올 수 있음)
    comparing_price_site_types: str | list[Any] | None = Field(None, description="가격비교 사이트(deprecated)")


class ProductSearchV2Response(BaseDto):
    """
    상품 검색하기 version 2.0 응답 모델

    OpenAPI Schema: products-search-engine--1549367095
    """

    total_count: int = Field(..., description="전체 상품 수")
    page_count: int = Field(..., description="페이지 수")
    last_id: str | None = Field(None, description="검색 기준 값")
    displayable_stock: bool = Field(..., description="재고 노출 여부")
    items: list[ProductSearchItem] = Field(default_factory=list, description="검색된 상품 목록")


# ============================================================================
# 변경된 상품 번호 목록 조회 Models
# ============================================================================


class ChangedProductItem(BaseDto):
    """
    변경된 상품 아이템

    OpenAPI Schema: products-changed-756650823 > contents
    """

    product_no: int = Field(..., description="상품 번호")
    registered_at: KstDatetime = Field(..., description="등록일")
    updated_at: KstDatetime | None = Field(None, description="수정일")


class ChangedProductsResponse(BaseDto):
    """
    변경된 상품 번호 목록 조회 응답 모델

    OpenAPI Schema: products-changed-756650823
    """

    total_count: int = Field(..., description="전체 상품수")
    total_page: int = Field(..., description="전체 페이지수")
    last_id: str = Field(..., description="검색 기준 값")
    contents: list[ChangedProductItem] = Field(default_factory=list, description="변경된 상품 목록")


# ============================================================================
# 상품 리스트로 상품 검색하기 Models
# ============================================================================


class CartInfo(BaseDto):
    use_yn: str = Field(..., description="장바구니 사용 여부")
    off_period_yn: str = Field(..., description="장바구니 담기 불가능한 기간 설정 여부")
    off_start_ymd: KstDate | None = Field(None, description="장바구니 담기 불가능한 시작 시간")
    off_end_ymd: KstDate | None = Field(None, description="장바구니 담기 불가능한 종료 시간")


class Commission(BaseDto):
    type: Literal["PRODUCT", "CATEGORY", "PARTNER", "PURCHASE_PRICE"] = Field(..., description="판매수수료타입")
    rate: float = Field(..., description="수수료율")


class DisplayCategory(BaseDto):
    display_category_no: int = Field(..., description="전시카테고리 번호")
    display_category_name: str = Field(..., description="전시카테고리 명")


class CategoryInfo(BaseDto):
    category_no: int = Field(..., description="표준 카테고리 번호")
    display_categories: list[DisplayCategory] = Field(default_factory=list, description="전시카테고리 목록")


class SalePeriod(BaseDto):
    period_type: Literal["REGULAR", "PERIOD"] = Field(..., description="판매기간설정")
    start_ymdt: KstDatetime = Field(..., description="판매 시작 시간")
    end_ymdt: KstDatetime = Field(..., description="판매 종료 시간")


class SaleInfo(BaseDto):
    sale_method_type: Literal["PURCHASE", "CONSIGNMENT"] = Field(..., description="판매방식")
    sale_period: SalePeriod = Field(..., description="판매기간")
    sale_status_type: str = Field(..., description="판매상태")
    sale_setting_status_type: str = Field(..., description="판매 설정 상태")
    sale_price: float = Field(..., description="판매가")
    surtax_type: str = Field(..., description="부가세 타입")


class ImmediateDiscount(BaseDto):
    unit_type: Literal["AMOUNT", "PERCENT"] = Field(..., description="즉시할인 단위")
    amount: float = Field(..., description="즉시할인 양")
    period_yn: str = Field(..., description="즉시할인 기간설정 여부")
    start_ymdt: KstDatetime | None = Field(None, description="즉시할인 시작 시간")
    end_ymdt: KstDatetime | None = Field(None, description="즉시할인 종료 시간")


class AdditionalDiscount(BaseDto):
    no: int = Field(..., alias="no", description="추가할인 번호")
    name: str | None = Field(None, description="추가 할인명")
    additional_discount_amount: float = Field(..., description="추가 할인 금액")
    member_target_type: str | None = Field(None, description="할인 적용 회원 유형")
    member_grade_nos: list[int] = Field(default_factory=list, description="할인 적용 회원 등급 번호 목록")
    member_group_nos: list[int] = Field(default_factory=list, description="할인 적용 회원 그룹 번호 목록")
    mall_charge_amount: float = Field(..., description="몰의 할인 부담금액")
    start_ymdt: KstDatetime | None = Field(None, description="추가할인 시작일")
    end_ymdt: KstDatetime | None = Field(None, description="추가할인 종료일")


class DiscountInfo(BaseDto):
    immediate_discount_info: ImmediateDiscount = Field(..., description="즉시할인 정보")
    immediate_discount_amount: float = Field(..., description="즉시 할인 금액")
    applied_immediate_discount_price: float = Field(..., description="즉시 할인 적용된 금액")
    additional_discount: AdditionalDiscount | None = Field(None, description="추가할인 정보")
    additional_discount_amount: float = Field(..., description="추가 할인 금액")
    additional_discount_name: str | None = Field(None, description="추가 할인명")
    applied_additional_discount_price: float = Field(..., description="추가 할인 적용된 금액")


class Limitations(BaseDto):
    min_buy_cnt: int = Field(..., description="최소 구매 수량")
    max_buy_person_cnt: int = Field(..., description="1인 최대 구매 수량")
    max_buy_time_cnt: int = Field(..., description="1회 최대 구매 수량")
    max_buy_days: int = Field(..., description="최대 구매 기간(일)")
    max_buy_period_cnt: int = Field(..., description="최대 구매 기간(수량)")
    member_only: bool = Field(..., description="비회원 구매 여부")
    can_add_to_cart: bool = Field(..., description="장바구니 가능 여부")
    refundable: bool = Field(..., description="환불 가능 여부")
    naver_pay_handling: bool = Field(..., description="네이버페이 결제 가능 여부")


class ProductImage(BaseDto):
    image_no: int = Field(..., description="이미지 번호")
    product_no: int = Field(..., description="상품 번호")
    url: str = Field(..., description="이미지 경로")
    is_main: bool = Field(..., description="메인 사진 여부")
    display_order: int = Field(..., description="이미지 조회 순서")


class OptionImage(BaseDto):
    mall_option_image_url: str = Field(..., description="옵션 이미지 경로")
    origin_mall_option_image_url: str = Field(..., description="옵션 이미지 원본 경로")
    main_yn: str = Field(..., description="옵션 메인이미지 여부")
    display_order: int = Field(..., description="옵션 이미지 순서")


class ProductOptionDetail(BaseDto):
    mall_option_no: int = Field(..., description="옵션 번호")
    mall_product_no: int = Field(..., description="상품 번호")
    mall_no: int = Field(..., description="쇼핑몰 번호")
    stock_no: int = Field(..., description="옵션 재고 번호")
    option_type: Literal["COMBINATION", "DEFAULT", "MAPPING", "REQUIRED"] = Field(..., description="옵션 타입")
    option_name: str = Field(..., description="옵션 이름")
    option_value: str = Field(..., description="옵션 값")
    option_price: float = Field(..., description="옵션 가격")
    add_price: float = Field(..., description="추가 가격")
    stock_cnt: int = Field(..., description="옵션 재고수")
    sale_cnt: int = Field(..., description="판매 수")
    use_yn: str = Field(..., description="사용 여부")
    option_management_cd: str = Field(..., description="운영 코드")
    extra_management_cd: str = Field(..., description="추가관리코드")
    purchase_price: float = Field(..., description="공급가")
    commission_rate: float = Field(..., description="판매 수수료")
    sku: str = Field(..., description="재고 관리 단위")
    item_yn: str = Field(..., description="자재상품(옵션) 여부")
    forced_sold_out: bool = Field(..., description="임시 품절 여부")
    is_required_option: bool = Field(..., description="필수 옵션 여부")
    display_order: int = Field(..., description="정렬 순서")
    register_ymdt: KstDatetime = Field(..., description="등록 날짜")
    update_ymdt: KstDatetime = Field(..., description="수정 날짜")
    sale_status_type: str = Field(..., description="판매 상태")
    images: list[OptionImage] = Field(default_factory=list, description="옵션 이미지 목록")


class ProductStock(BaseDto):
    total_cnt: int = Field(..., description="판매가능 재고 수")
    represent_cnt: int = Field(..., description="대표옵션 재고 수")
    total_sale_cnt: int = Field(..., description="총 판매 수량")
    safety_stock_cnt: int = Field(..., description="안전재고 수")
    delivery_waiting_stock_cnt: int = Field(..., description="출고대기 재고 수")


class Sticker(BaseDto):
    sticker_no: int = Field(..., description="스티커번호")
    label: str = Field(..., description="스티커 라벨")
    image_url: str = Field(..., description="스티커 이미지 url")
    display_order: int = Field(..., description="전시순서")


class CustomProperty(BaseDto):
    prop_no: int = Field(..., description="항목 번호")
    prop_name: str = Field(..., description="항목명")
    prop_value_no: int = Field(..., description="항목 값 번호")
    prop_value: str = Field(..., description="항목 값명")
    is_multiple_selection: bool = Field(..., description="항목 복수선택여부")


class CustomerDemand(BaseDto):
    mall_product_input_no: int = Field(..., description="구매자작성형 번호")
    input_text: str = Field(..., description="구매자작성형 텍스트 내용")
    use_yn: str = Field(..., description="사용여부")
    required: bool = Field(..., description="필수 여부")
    input_matching_type_label: str = Field(..., description="구매자작성형 매칭타입")


class DeliveryInfo(BaseDto):
    deliverable: bool = Field(..., description="배송 가능 여부")
    shipping_area_type: str | None = Field(None, description="배송구분")
    delivery_template_no: int = Field(..., description="배송템플릿 번호")
    delivery_fee_type: str | None = Field(None, description="배송비 유형")
    delivery_charge: float = Field(..., description="배송비")
    free_shipping_condition_amount: float = Field(..., description="조건부 무료조건일 경우 무료배송 기준 금액")
    quantity_condition_per_order_cnt: int = Field(..., description="수량비례일 경우 기준 주문수량")
    shipping_combinable: bool = Field(..., description="묶음배송 가능 여부")
    international_shipping_available: bool = Field(..., description="국제배송 가능 여부")
    uses_delivery_due_date: bool = Field(..., description="배송 지정일 사용 여부")


class ProductListItem(BaseDto):
    """
    상품 리스트 검색 아이템

    OpenAPI Schema: products-search-by-nos1924553784 (array items)
    """

    # 기본 정보
    mall_product_no: int = Field(..., description="상품 번호")
    product_name: str = Field(..., description="상품명")
    product_name_en: str = Field(..., description="영문 상품명")
    mall_no: int = Field(..., description="몰 번호")
    mall_name: str = Field(..., description="몰 이름")
    partner_no: int = Field(..., description="파트너 번호")
    partner_name: str = Field(..., description="파트너사 명")
    admin_no: int = Field(..., description="담당자 번호")

    # 브랜드
    brand_no: int = Field(..., description="표준 브랜드 번호")
    display_brand_no: int = Field(..., description="전시 브랜드 번호")
    brand_name: str | None = Field(None, description="브랜드 명")

    # 상품 타입
    group_type: Literal["DELIVERY", "SERVICE"] = Field(..., description="상품군")
    class_type: Literal["DEFAULT", "EVENT", "OFFLINE", "RENTAL"] = Field(..., description="상품 유형")

    # 옵션
    has_option: bool = Field(..., description="옵션 유무")
    option_type: Literal["COMBINATION", "DEFAULT", "MAPPING", "REQUIRED"] = Field(..., description="옵션 타입")
    use_customer_demand: bool = Field(..., description="구매자 작성형 옵션 사용 여부")
    options: list[ProductOptionDetail] = Field(default_factory=list, description="옵션 정보")
    customer_demands: list[CustomerDemand] = Field(default_factory=list, description="구매자 작성형 옵션")

    # 전시 설정
    platform_display_info: PlatformDisplayInfo = Field(..., description="플랫폼별 노출 설정 정보")
    member_grade_display_info: MemberGradeDisplayInfo = Field(..., description="회원등급 노출 설정 정보")
    member_group_display_info: MemberGroupDisplayInfo = Field(..., description="회원그룹 노출 설정 정보")
    front_displayable: bool = Field(..., description="전시 가능 여부")

    # 구매 제한
    minor_purchase_available: bool = Field(..., description="미성년자 구매 가능 여부")
    non_member_purchase_available: bool = Field(..., description="비회원 구매 가능 여부")
    refundable: bool = Field(..., description="환불 가능 여부")

    # 장바구니
    cart: CartInfo = Field(..., description="장바구니 정보")

    # 수수료
    commission: Commission = Field(..., description="판매수수료 정보")
    partner_charge_amount: float = Field(..., description="파트너사 분담금")

    # 관리코드
    product_management_cd: str = Field(..., description="상품관리코드")
    group_management_code: str | None = Field(None, description="그룹관리코드")

    # 카테고리
    category_info: CategoryInfo = Field(..., description="카테고리 정보")

    # 판매 정보
    sale_info: SaleInfo = Field(..., description="판매 정보")
    supply_price: float = Field(..., description="공급가")
    purchase_price: float = Field(..., description="매입가")

    # 할인 정보
    discount_info: DiscountInfo = Field(..., description="할인 정보")

    # 제한 정보
    limitations: Limitations = Field(..., description="제한 정보")

    # 이미지
    images: list[ProductImage] = Field(default_factory=list, description="이미지 정보")
    mall_product_list_image: str | None = Field(None, description="리스트 이미지 URL")

    # 재고 정보
    product_stock: ProductStock = Field(..., description="재고정보")
    reservation_stock_cnt: int = Field(..., description="예약 재고 수량")
    is_stock_sync: bool = Field(..., description="재고 연동 여부")
    is_sold_out: bool = Field(..., description="품절 여부")

    # 적립금
    accumulation_rate: float = Field(..., description="상품적립률")

    # 스티커
    stickers: list[Sticker] = Field(default_factory=list, description="스티커 정보")

    # 리뷰
    review_count: int = Field(..., description="상품후기수")
    review_rate: float = Field(..., description="상품후기 평점")

    # 커스텀 속성
    custom_properties: list[CustomProperty] = Field(default_factory=list, description="상품항목추가 관리 정보")

    # 배송 정보
    delivery_info: DeliveryInfo = Field(..., description="배송 정보")

    # 상세 내용
    content: str = Field(..., description="상품 상세")

    # 날짜
    register_date_time: KstDatetime = Field(..., description="등록일")
    update_date_time: KstDatetime | None = Field(None, description="최종수정일")

    # 기타
    comparing_price_site_types: str | None = Field(None, description="가격비교정보등록 사이트")


# Response type: array
ProductListSearchResponse = list[ProductListItem]


# ============================================================================
# 상품 부분 수정하기 (version 2.0) Request Models
# ============================================================================


class PatchContentDetail(BaseDto):
    """상품 내용 설정"""

    uses_option_image_instead_of_content: bool | None = Field(
        None, description="옵션 이미지로 상품 내용 대체 여부"
    )
    content_header: str | None = Field(None, description="상품 상단 내용 (html)")
    content: str | None = Field(None, description="상품 상세 내용")
    content_footer: str | None = Field(None, description="상품 하단 내용 (html)")


class PatchUnitPriceInfo(BaseDto):
    """가격 단위 정보"""

    unit_name: str | None = Field(None, description="단위 값")
    unit_name_type: str | None = Field(None, description="단위 유형")
    unit_price: float | None = Field(None, description="단위 가격")


class PatchImmediateDiscountInfo(BaseDto):
    """즉시 할인 정보"""

    unit_type: Literal["AMOUNT", "PERCENT"] | None = Field(None, description="즉시 할인 단위")
    amount: float | None = Field(None, description="즉시 할인 값")
    period_yn: Literal["Y", "N"] | None = Field(None, description="즉시 할인 기간 여부")
    start_ymdt: str | None = Field(None, description="즉시 할인 시작 일시")
    end_ymdt: str | None = Field(None, description="즉시 할인 종료 일시")


class PatchAccumulationLimitInfo(BaseDto):
    """적립금 사용 한도율"""

    unit_type: Literal["AMOUNT", "PERCENT"] | None = Field(None, description="적립금 사용 금액 단위")
    limit_value: float | None = Field(None, description="적립금 사용 양")


class PatchCommissionInfo(BaseDto):
    """수수료 정보"""

    type: Literal["PRODUCT", "CATEGORY", "PARTNER", "PURCHASE_PRICE"] | None = Field(
        None, description="판매수수료 타입"
    )
    rate: float | None = Field(None, description="판매수수료")


class PatchPriceInfo(BaseDto):
    """가격 관련 설정"""

    sale_price: float | None = Field(None, description="판매가")
    purchase_price: float | None = Field(None, description="공급가")
    partner_charge_amt: float | None = Field(None, description="정산시 파트너 분담금")
    commission_info: PatchCommissionInfo | None = Field(None, description="수수료 정보")
    immediate_discount_info: PatchImmediateDiscountInfo | None = Field(None, description="즉시 할인 정보")
    unit_price_info: PatchUnitPriceInfo | None = Field(None, description="가격 단위 정보")
    accumulation_rate: float | None = Field(None, description="적립률(%)")
    accumulation_use_yn: Literal["Y", "N"] | None = Field(None, description="적립금 사용 여부")
    accumulation_limit_info: PatchAccumulationLimitInfo | None = Field(None, description="적립금 사용 한도율")
    surtax_type: Literal["DUTY", "DUTYFREE", "SMALL"] | None = Field(None, description="과세 적용 기준")


class PatchMaxBuyQuantityInfo(BaseDto):
    """최대구매수량 정보"""

    type: Literal["PER_TIME", "PER_PERIOD", "PER_PERSON", "PER_DAY"] | None = Field(
        None, description="최대구매수량 유형"
    )
    max_buy_quantity: int | None = Field(None, description="최대구매수량 유형에 따른 최대구매수량")
    max_buy_days: int | None = Field(None, description="최대구매수량 유형이 PER_PERIOD인 경우, 최대 구매 기간 입력")


class PatchPurchaseLimitQuantity(BaseDto):
    """구매 수량 제한 설정"""

    min_buy_quantity: int | None = Field(None, description="최소구매수량")
    max_buy_quantity_info: PatchMaxBuyQuantityInfo | None = Field(None, description="최대구매수량 정보")


class PatchPlatformDisplayInfo(BaseDto):
    """플랫폼 별 노출 설정"""

    is_all: bool | None = Field(None, description="전체 노출 여부")
    any_values: list[Literal["PC", "MOBILE_WEB", "MOBILE"]] | None = Field(
        None, description="노출할 플랫폼 리스트"
    )


class PatchMemberDisplayInfo(BaseDto):
    """회원 등급/그룹 노출 설정 정보"""

    check: Literal["NONE", "ANY", "ALL"] | None = Field(None, description="노출 설정")
    info: list[int] | None = Field(None, description="노출 설정할 회원 등급/그룹 번호 리스트")


class PatchDisplayInfo(BaseDto):
    """노출 관련 설정"""

    platform_display_info: PatchPlatformDisplayInfo | None = Field(None, description="플랫폼 별 노출 설정")
    search_engine_displayable: bool | None = Field(None, description="검색엔진 노출 여부")
    guest_purchasable: bool | None = Field(None, description="비회원 구매 가능 여부")
    minor_purchasable: bool | None = Field(None, description="미성년자 구매가능 여부")
    only_url_accessible: bool | None = Field(None, description="프론트 미노출 여부")
    member_group_display_info: PatchMemberDisplayInfo | None = Field(None, description="회원 그룹 노출 설정 정보")
    member_grade_display_info: PatchMemberDisplayInfo | None = Field(None, description="회원 등급 노출 설정 정보")


class PatchProductImage(BaseDto):
    """상품 이미지"""

    image_no: int | None = Field(None, description="이미지 번호 (신규 생성 시 0)")
    url: str | None = Field(None, description="이미지 URL")
    is_main: bool | None = Field(None, description="대표 이미지 여부")
    url_type: Literal["IMAGE_URL", "VIDEO_URL"] | None = Field(None, description="url 타입")
    is_external: bool | None = Field(None, description="외부이미지 사용여부")


class PatchListImage(BaseDto):
    """리스트 이미지"""

    image_no: int | None = Field(None, description="리스트 이미지 번호 (신규 생성 시 0)")
    url: str | None = Field(None, description="리스트 이미지 URL")
    url_type: Literal["IMAGE_URL", "VIDEO_URL"] | None = Field(None, description="url 타입")
    is_external: bool | None = Field(None, description="외부이미지 사용여부")


class PatchImageInfo(BaseDto):
    """상품 이미지 관련 설정"""

    uses_external_image: bool | None = Field(None, description="외부 이미지 URL 사용 여부")
    images: list[PatchProductImage] | None = Field(None, description="상품 이미지 리스트")
    list_image: PatchListImage | None = Field(None, description="리스트 이미지")


class PatchSalePeriod(BaseDto):
    """판매 기간"""

    start_ymdt: str | None = Field(None, description="판매 시작일시")
    end_ymdt: str | None = Field(None, description="판매 종료일시")


class PatchSalePeriodInfo(BaseDto):
    """판매 기간 정보"""

    sale_period_type: Literal["REGULAR", "PERIOD"] | None = Field(None, description="판매 기간 유형")
    sale_period: PatchSalePeriod | None = Field(None, description="판매 기간")


class PatchPlaceOriginInfo(BaseDto):
    """원산지 정보"""

    place_origin_seq: int | None = Field(None, description="원산지 번호")
    place_origins_yn: Literal["Y", "N"] | None = Field(None, description="원산지 직접 입력 사용 유무")
    place_origin: str | None = Field(None, description="원산지 직접 입력인 경우, 원산지 입력")


class PatchDutyContent(BaseDto):
    """상품정보고시"""

    category_no: int | None = Field(None, description="상품 정보 고시 항목 번호")
    category_name: str | None = Field(None, description="상품 정보 고시 항목명")
    contents: list[dict[str, Any]] | None = Field(None, description="상품 정보 고시 상세 내용")


class PatchProductGuide(BaseDto):
    """상품 안내 정보"""

    template_no: int | None = Field(None, description="상품 안내 정보 - 템플릿 번호")
    type: Literal["DELIVERY", "AFTER_SERVICE", "REFUND", "EXCHANGE", "DELEGATION_BY_LIQUOR"] | None = Field(
        None, description="상품 안내 정보 - 템플릿 유형"
    )
    content: str | None = Field(None, description="상품 안내 정보 - 직접 입력하는 경우에만 입력")


class PatchUnavailablePeriod(BaseDto):
    """장바구니 불가 기간"""

    start_ymdt: str | None = Field(None, description="장바구니 불가 시작일시")
    end_ymdt: str | None = Field(None, description="장바구니 불가 종료일시")


class PatchCartInfo(BaseDto):
    """장바구니 설정"""

    is_available_cart: bool | None = Field(None, description="장바구니 가능 여부")
    unavailable_period: PatchUnavailablePeriod | None = Field(None, description="장바구니 불가 기간")


class PatchRefundableInfo(BaseDto):
    """환불 정보"""

    refundable: bool | None = Field(None, description="환불 가능 여부")
    non_refund_types: list[Literal["RETURN", "EXCHANGE"]] | None = Field(
        None, description="환불 불가인 경우, 불가능 항목"
    )


class PatchBrandNoInfo(BaseDto):
    """브랜드 번호 정보"""

    brand_no: int | None = Field(None, description="브랜드 번호")
    display_brand_no: int | None = Field(None, description="전시 브랜드 번호")


class PatchBrandNameInfo(BaseDto):
    """브랜드명 정보"""

    main_name: str | None = Field(None, description="메인 브랜드명")
    sub_name: str | None = Field(None, description="서브 브랜드명")


class PatchBrandInfo(BaseDto):
    """브랜드 정보"""

    input_type: Literal["NO", "NAME"] | None = Field(None, description="브랜드 입력 유형")
    brand_no_info: PatchBrandNoInfo | None = Field(None, description="브랜드 번호 정보")
    brand_name_info: PatchBrandNameInfo | None = Field(None, description="브랜드명 정보")


class PatchOptionImage(BaseDto):
    """옵션 이미지"""

    url: str | None = Field(None, description="옵션 이미지 URL")
    is_main: bool | None = Field(None, description="옵션 대표 이미지 여부")


class PatchOption(BaseDto):
    """옵션 정보"""

    option_no: int | None = Field(None, description="옵션 번호 (신규 생성 0)")
    option_name: str | None = Field(None, description="옵션명")
    option_value: str | None = Field(None, description="옵션값")
    add_price: float | None = Field(None, description="옵션 추가 금액")
    usable: bool | None = Field(None, description="옵션 사용 여부")
    stock_quantity: int | None = Field(None, description="옵션 재고 수량")
    management_code: str | None = Field(None, description="옵션 판매자 관리 코드")
    extra_management_code: str | None = Field(None, description="옵션 추가 관리 코드")
    forced_sold_out: bool | None = Field(None, description="옵션 임시 품절 여부")
    purchase_price: float | None = Field(None, description="매입가/공급가")
    images: list[PatchOptionImage] | None = Field(None, description="옵션 이미지")
    is_required_option: bool | None = Field(None, description="필수 옵션 여부")


class PatchCustomerDemand(BaseDto):
    """구매자 작성형 옵션"""

    customer_demand_no: int | None = Field(None, description="작성형 옵션 번호 (신규 생성 0)")
    content: str | None = Field(None, description="작성형 옵션 텍스트 내용")
    target_type: Literal["OPTION", "PRODUCT", "AMOUNT"] | None = Field(None, description="작성형 옵션 매칭 유형")
    required: bool | None = Field(None, description="작성형 옵션 입력 필수 여부")
    usable: bool | None = Field(None, description="작성형 옵션 사용 여부")


class PatchOptionInfo(BaseDto):
    """옵션 설정"""

    options: list[PatchOption] | None = Field(None, description="옵션 목록")
    option_select_type: Literal["MULTI", "FLAT"] | None = Field(None, description="옵션 노출 유형")
    customer_demands: list[PatchCustomerDemand] | None = Field(None, description="구매자 작성형 옵션")
    sets: list[dict[str, Any]] | None = Field(None, description="세트 옵션")


class PatchDeliveryInfo(BaseDto):
    """배송 관련 설정"""

    uses_delivery: bool | None = Field(None, description="배송 여부")
    shipping_area_type: Literal["PARTNER_SHIPPING_AREA", "MALL_SHIPPING_AREA"] | None = Field(
        None, description="출고유형"
    )
    shipping_area_partner_no: int | None = Field(None, description="출고지 파트너 번호")
    delivery_template_no: int | None = Field(None, description="배송비 템플릿 번호")
    can_delivery_combination: bool | None = Field(None, description="묶음 배송 가능 여부")
    can_delivery_international: bool | None = Field(None, description="해외 배송 가능 여부")
    delivery_customer_info: str | None = Field(None, description="배송관련 판매자 특이사항/고객안내사항")


class PatchMarketingDisplayPeriod(BaseDto):
    """홍보 문구 노출 기간"""

    start_ymdt: str | None = Field(None, description="홍보 문구 노출 시작일시")
    end_ymdt: str | None = Field(None, description="홍보 문구 노출 종료일시")


class PatchMarketingPhraseInfo(BaseDto):
    """홍보 문구 정보"""

    marketing_phrase: str | None = Field(None, description="홍보 문구")
    marketing_display_period: PatchMarketingDisplayPeriod | None = Field(None, description="홍보 문구 노출 기간")


class PatchMarketingInfo(BaseDto):
    """마케팅 관련 설정"""

    marketing_phrase_info: PatchMarketingPhraseInfo | None = Field(None, description="홍보 문구 정보")
    is_available_promotion: bool | None = Field(None, description="프로모션 사용 여부")


class PatchCustomProperty(BaseDto):
    """추가 항목"""

    property: str | None = Field(None, description="추가 항목 - 항목명")
    values: list[str] | None = Field(None, description="추가 항목 - 항목값명")


class PatchStickerDisplayPeriod(BaseDto):
    """스티커 노출 기간"""

    start_ymdt: str | None = Field(None, description="스티커 노출 시작일시")
    end_ymdt: str | None = Field(None, description="스티커 노출 종료일시")


class PatchSticker(BaseDto):
    """스티커 정보"""

    sticker_no: int | None = Field(None, description="스티커 번호 (신규 생성 0)")
    display_period: PatchStickerDisplayPeriod | None = Field(None, description="스티커 노출 기간")


class PatchExtraJson(BaseDto):
    """추가설정"""

    naver_display_yn: str | None = Field(None, description="네이버 쇼핑 EP - 노출 여부")
    serial_number: str | None = Field(None, description="제품 일련번호")
    naver_pay_limit_yn: str | None = Field(None, description="네이버 페이 결제 제한 여부")
    naver_product_status: Literal["NEW", "USED", "REFURB", "DISPLAY", "RETURN", "SCRATCH"] | None = Field(
        None, description="네이버 쇼핑 EP - 상품 상태"
    )
    naver_category_id: str | None = Field(None, description="네이버 쇼핑 EP - 카테고리 ID")
    manufacture_name: str | None = Field(None, description="제조사명")
    naver_product_flag: Literal[
        "WHOLESALE", "RENTAL", "LENT", "INSTALLMENT", "RESERVATION_SALE", "SUBSTITUTION", "RESERVATION_BUY"
    ] | None = Field(None, description="네이버 쇼핑 EP - 상품 판매 종류")
    naver_extra: str | None = Field(None, description="네이버 쇼핑 EP 기타 정보")
    product_model_name: str | None = Field(None, description="제품모델명")
    price_compare_page_id: str | None = Field(None, description="네이버 쇼핑 EP - 가격 비교 페이지 ID")
    naver_point_accum_locations: str | None = Field(None, description="네이버포인트 적립 가능 플랫폼")


class PatchRelatedProductInfo(BaseDto):
    """관련 상품 정보"""

    config_type: Literal["DISPLAY_CATEGORY", "SELECTED"] | None = Field(None, description="관련 상품 설정")
    sort_criterion: Literal["LATEST_REGISTER_DATE", "SALES_COUNT", "REVIEW_COUNT", "CUSTOM_ORDER"] | None = Field(
        None, description="관련 상품 진열 순서"
    )
    product_nos: list[int] | None = Field(None, description="상품 번호 리스트")


class PatchProductV2Request(BaseDto):
    """
    상품 부분 수정하기 (version 2.0) 요청 모델

    OpenAPI Schema: products-productNo-911598269

    모든 필드는 선택적입니다. 수정이 필요한 필드만 입력합니다.
    """

    # 기본 정보
    group_type: Literal["DELIVERY", "SERVICE"] | None = Field(None, description="상품군")
    class_type: Literal["DEFAULT", "EVENT", "OFFLINE", "RENTAL"] | None = Field(None, description="상품분류")
    sale_method_type: Literal["PURCHASE", "CONSIGNMENT"] | None = Field(None, description="판매방식")
    standard_category_no: int | None = Field(None, description="표준 카테고리")
    display_category_nos: list[int] | None = Field(None, description="전시 카테고리 리스트")
    representative_display_category_no: int | None = Field(None, description="대표 전시 카테고리")
    merchandiser_no: int | None = Field(None, description="상품 담당자")

    # 상품명
    product_name: str | None = Field(None, description="상품명")
    product_name_en: str | None = Field(None, description="영문 상품명")
    supplier_product_name: str | None = Field(None, description="매입처 상품명")

    # 상품 내용
    content_detail: PatchContentDetail | None = Field(None, description="상품 내용 설정")

    # 관리 코드
    management_code: str | None = Field(None, description="판매자 관리 코드")
    extra_management_code: str | None = Field(None, description="추가관리코드")

    # 가격
    price: PatchPriceInfo | None = Field(None, description="가격 관련 설정")

    # 재고
    stock_quantity: int | None = Field(None, description="재고 수량")

    # 구매 제한
    purchase_limit_quantity: PatchPurchaseLimitQuantity | None = Field(None, description="구매 수량 제한 설정")

    # 노출 설정
    display: PatchDisplayInfo | None = Field(None, description="노출 관련 설정")

    # 이미지
    image: PatchImageInfo | None = Field(None, description="상품 이미지 관련 설정")

    # 기타 정보
    hs_code: str | None = Field(None, description="HS CODE")
    keywords: list[str] | None = Field(None, description="검색어 리스트")

    # 판매 기간
    sale_period_info: PatchSalePeriodInfo | None = Field(None, description="판매 기간 정보")

    # 제조/유효기간
    manufactured_date_time: str | None = Field(None, description="제조일자 (YYYY-MM-DD HH:00:00)")
    expiration_date_time: str | None = Field(None, description="유효기간 (YYYY-MM-DD HH:00:00)")

    # 원산지
    place_origin_info: PatchPlaceOriginInfo | None = Field(None, description="원산지 정보")

    # 상품정보고시
    duty_content: PatchDutyContent | None = Field(None, description="상품정보고시")

    # 상품 안내
    product_guides: list[PatchProductGuide] | None = Field(None, description="상품 안내 정보")

    # 재입고 알림
    uses_restock_notification: bool | None = Field(None, description="재입고 알림 사용설정")

    # 장바구니
    cart_info: PatchCartInfo | None = Field(None, description="장바구니 설정")

    # 환불
    refundable_info: PatchRefundableInfo | None = Field(None, description="환불 정보")

    # 브랜드
    brand: PatchBrandInfo | None = Field(None, description="브랜드 정보")

    # 옵션
    option_type: Literal["COMBINATION", "NONE", "REQUIRED"] | None = Field(None, description="옵션 유형")
    option: PatchOptionInfo | None = Field(None, description="옵션 설정")

    # 배송
    delivery: PatchDeliveryInfo | None = Field(None, description="배송 관련 설정")

    # 마케팅
    marketing: PatchMarketingInfo | None = Field(None, description="마케팅 관련 설정")

    # 추가 속성
    custom_properties: list[PatchCustomProperty] | None = Field(None, description="추가 항목")

    # 스티커
    stickers: list[PatchSticker] | None = Field(None, description="스티커 정보")

    # 추가 설정
    extra_json: PatchExtraJson | None = Field(None, description="추가설정")

    # 관련 상품
    related_product_info: PatchRelatedProductInfo | None = Field(None, description="관련 상품 정보")

    # 기타
    extra_info: str | None = Field(None, description="추가 정보")
    url_shortening_yn: Literal["Y", "N"] | None = Field(None, description="단축URL 사용여부")

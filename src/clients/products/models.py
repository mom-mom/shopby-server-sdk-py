from typing import Any, Literal

from pydantic import Field

from src.base.dto import BaseDto


# Nested models
class PlatformDisplayInfo(BaseDto):
    display_yn: str = Field(..., description="전시여부")
    pc_yn: str = Field(..., description="PC 전시여부")
    mobile_yn: str = Field(..., description="모바일앱 전시여부")
    mobile_web_yn: str = Field(..., description="모바일웹 전시여부")


class PromotionTextInfo(BaseDto):
    text: str = Field(..., description="홍보문구")
    period_yn: str = Field(..., description="홍보문구 기간설정 유무")
    start_ymd: str | None = Field(None, description="홍보문구 노출 시작 시간")
    end_ymd: str | None = Field(None, description="홍보문구 노출 종료 시간")


class SalePeriodInfo(BaseDto):
    period_type: Literal["REGULAR", "PERIOD"] = Field(..., description="판매기간설정")
    start_ymdt: str = Field(..., description="판매 시작 시간")
    end_ymdt: str = Field(..., description="판매 종료 시간")


class ImmediateDiscountInfo(BaseDto):
    unit_type: Literal["AMOUNT", "PERCENT"] = Field(..., description="즉시할인 단위")
    amount: float = Field(..., description="즉시할인 양")
    period_yn: str = Field(..., description="즉시할인 기간설정 여부")
    start_ymdt: str | None = Field(None, description="즉시할인 시작 시간")
    end_ymdt: str | None = Field(None, description="즉시할인 종료 시간")


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
    off_start_ymd: str | None = Field(None, description="장바구니 OFF 시작일")
    off_end_ymd: str | None = Field(None, description="장바구니 OFF 종료일")


class MallProductImage(BaseDto):
    image_url: str = Field(..., description="이미지 URL")
    origin_image_url: str | None = Field(None, description="사용하지 않음")
    main_yn: str = Field(..., description="메인 이미지 여부")
    display_order: int = Field(..., description="노출 순서")
    image_id: str | None = Field(None, description="사용하지 않음")
    mall_no: int = Field(..., description="이미지의 몰번호")
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
    accumulation_rate: float = Field(..., description="적립금적립 - %")
    partner_charge_amt: float = Field(..., description="파트너 부담 금액")
    accumulation_use_yn: str = Field(..., description="적립금 사용 가능 여부")
    accumulation_limit_info: dict[str, Any] = Field(..., description="적립금 제한 정보")

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
    duty_content: dict[str, Any] = Field(..., description="상품정보고시")
    will_duty_content: dict[str, Any] = Field(..., description="예정 상품정보고시")
    certification_info: dict[str, Any] = Field(..., description="인증정보")

    # 원산지 및 제조정보
    place_origin_info: dict[str, Any] = Field(..., description="원산지 정보")
    manufacture_ymdt: str | None = Field(None, description="제조일시")
    expiration_ymdt: str | None = Field(None, description="유효기간")

    # 부가세
    value_added_tax_type: str = Field(..., description="부가세타입")

    # 관리코드
    product_management_cd: str = Field(..., description="상품 관리코드")
    extra_management_cd: str = Field(..., description="추가관리코드")

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
    supplier_product_name: str = Field(..., description="매입처 상품명")

    # 관련 상품 정보
    related_product_info: dict[str, Any] = Field(..., description="관련 상품 정보")

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
    start_date_time: str | None = Field(None, description="스티커 노출 시작일자")
    end_date_time: str | None = Field(None, description="스티커 노출 종료일자")


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
    reservation_start_ymdt: str = Field(..., description="예약판매 시작일")
    reservation_end_ymdt: str = Field(..., description="예약판매 종료일")
    reservation_delivery_ymdt: str = Field(..., description="예약판매 배송시작일")
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
    promotion_text: str = Field(..., description="홍보문구")

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
    delivery_condition_type: Literal["FREE", "CONDITIONAL", "FIXED_FEE"] = Field(..., description="배송비 타입")
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
    sale_start_ymdt: str = Field(..., description="판매시작일시")
    sale_end_ymdt: str = Field(..., description="판매종료일시")
    sale_status_type: Literal["READY", "ONSALE", "FINISHED", "STOP", "PROHIBITION"] = Field(
        ..., description="판매상태"
    )

    # 예약 판매
    reservation_data: ReservationData | None = Field(None, description="예약판매정보")

    # 이미지
    image_urls: list[str] = Field(default_factory=list, description="상품 이미지 URL")
    list_image_urls: list[str] = Field(default_factory=list, description="리스트 이미지 URL")

    # 쿠폰
    has_coupons: HasCoupons = Field(..., description="쿠폰여부")
    max_coupon_amt: float = Field(..., description="해당 상품의 옵션을 여러개 구매할 경우 받을 수 있는 최대한의 쿠폰할인 금액")
    coupon_discount_amt: float = Field(..., description="최대 쿠폰 적용 가격")
    enable_coupons: bool | None = Field(None, description="사용가능쿠폰 존재 여부")

    # 등록일 및 기타
    register_ymdt: str = Field(..., description="상품 등록일")
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

    # Deprecated
    comparing_price_site_types: str | None = Field(None, description="가격비교 사이트(deprecated)")


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

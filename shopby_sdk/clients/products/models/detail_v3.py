"""상품 상세 조회하기 (Version 3.0) 응답 모델"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDate

from .base import (
    CartInfo,
    CommissionInfo,
    ImmediateDiscountInfo,
    MaxBuyCountInfo,
    MemberGradeDisplayInfo,
    MemberGroupDisplayInfo,
    PlatformDisplayInfo,
    PromotionInfo,
    PromotionTextInfo,
    SalePeriodInfo,
)


class MallProductImage(BaseDto):
    """상품 이미지"""

    image_url: str = Field(..., description="이미지 URL")
    origin_image_url: str | None = Field(None, description="사용하지 않음")
    main_yn: str = Field(..., description="메인 이미지 여부")
    display_order: int = Field(..., description="노출 순서")
    image_id: str | None = Field(None, description="사용하지 않음")
    mall_no: int | None = Field(None, description="이미지의 몰번호")
    image_url_type: Literal["IMAGE_URL", "VIDEO_URL"] = Field(..., description="이미지 URL 타입")


class OptionImage(BaseDto):
    """옵션 이미지"""

    mall_option_image_url: str = Field(..., description="옵션 이미지 URL")
    main_yn: str = Field(..., description="메인 옵션 이미지 여부")
    display_order: int = Field(..., description="전시순")


class OptionMapping(BaseDto):
    """옵션 매핑 정보 (세트옵션)"""

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
    """상품 옵션"""

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

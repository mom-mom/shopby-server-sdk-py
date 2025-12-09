"""상품 리스트로 상품 검색하기 응답 모델"""

from typing import Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDate, KstDatetime

from .base import MemberGradeDisplayInfo, MemberGroupDisplayInfo, PlatformDisplayInfo


class ListSearchCartInfo(BaseDto):
    """장바구니 정보 (리스트 검색용)"""

    use_yn: str = Field(..., description="장바구니 사용 여부")
    off_period_yn: str = Field(..., description="장바구니 담기 불가능한 기간 설정 여부")
    off_start_ymd: KstDate | None = Field(None, description="장바구니 담기 불가능한 시작 시간")
    off_end_ymd: KstDate | None = Field(None, description="장바구니 담기 불가능한 종료 시간")


class Commission(BaseDto):
    """수수료 정보"""

    type: Literal["PRODUCT", "CATEGORY", "PARTNER", "PURCHASE_PRICE"] = Field(..., description="판매수수료타입")
    rate: float = Field(..., description="수수료율")


class ListSearchDisplayCategory(BaseDto):
    """전시 카테고리 (리스트 검색용)"""

    display_category_no: int = Field(..., description="전시카테고리 번호")
    display_category_name: str = Field(..., description="전시카테고리 명")


class CategoryInfo(BaseDto):
    """카테고리 정보"""

    category_no: int = Field(..., description="표준 카테고리 번호")
    display_categories: list[ListSearchDisplayCategory] = Field(default_factory=list, description="전시카테고리 목록")


class SalePeriod(BaseDto):
    """판매 기간"""

    period_type: Literal["REGULAR", "PERIOD"] = Field(..., description="판매기간설정")
    start_ymdt: KstDatetime = Field(..., description="판매 시작 시간")
    end_ymdt: KstDatetime = Field(..., description="판매 종료 시간")


class SaleInfo(BaseDto):
    """판매 정보"""

    sale_method_type: Literal["PURCHASE", "CONSIGNMENT"] = Field(..., description="판매방식")
    sale_period: SalePeriod = Field(..., description="판매기간")
    sale_status_type: str = Field(..., description="판매상태")
    sale_setting_status_type: str = Field(..., description="판매 설정 상태")
    sale_price: float = Field(..., description="판매가")
    surtax_type: str = Field(..., description="부가세 타입")


class ImmediateDiscount(BaseDto):
    """즉시할인 정보 (리스트 검색용)"""

    unit_type: Literal["AMOUNT", "PERCENT"] = Field(..., description="즉시할인 단위")
    amount: float = Field(..., description="즉시할인 양")
    period_yn: str = Field(..., description="즉시할인 기간설정 여부")
    start_ymdt: KstDatetime | None = Field(None, description="즉시할인 시작 시간")
    end_ymdt: KstDatetime | None = Field(None, description="즉시할인 종료 시간")


class AdditionalDiscount(BaseDto):
    """추가할인 정보"""

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
    """할인 정보"""

    immediate_discount_info: ImmediateDiscount = Field(..., description="즉시할인 정보")
    immediate_discount_amount: float = Field(..., description="즉시 할인 금액")
    applied_immediate_discount_price: float = Field(..., description="즉시 할인 적용된 금액")
    additional_discount: AdditionalDiscount | None = Field(None, description="추가할인 정보")
    additional_discount_amount: float = Field(..., description="추가 할인 금액")
    additional_discount_name: str | None = Field(None, description="추가 할인명")
    applied_additional_discount_price: float = Field(..., description="추가 할인 적용된 금액")


class Limitations(BaseDto):
    """제한 정보"""

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
    """상품 이미지"""

    image_no: int = Field(..., description="이미지 번호")
    product_no: int = Field(..., description="상품 번호")
    url: str = Field(..., description="이미지 경로")
    is_main: bool = Field(..., description="메인 사진 여부")
    display_order: int = Field(..., description="이미지 조회 순서")


class ListSearchOptionImage(BaseDto):
    """옵션 이미지 (리스트 검색용)"""

    mall_option_image_url: str = Field(..., description="옵션 이미지 경로")
    origin_mall_option_image_url: str = Field(..., description="옵션 이미지 원본 경로")
    main_yn: str = Field(..., description="옵션 메인이미지 여부")
    display_order: int = Field(..., description="옵션 이미지 순서")


class ProductOptionDetail(BaseDto):
    """상품 옵션 상세"""

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
    images: list[ListSearchOptionImage] = Field(default_factory=list, description="옵션 이미지 목록")


class ProductStock(BaseDto):
    """재고 정보"""

    total_cnt: int = Field(..., description="판매가능 재고 수")
    represent_cnt: int = Field(..., description="대표옵션 재고 수")
    total_sale_cnt: int = Field(..., description="총 판매 수량")
    safety_stock_cnt: int = Field(..., description="안전재고 수")
    delivery_waiting_stock_cnt: int = Field(..., description="출고대기 재고 수")


class Sticker(BaseDto):
    """스티커 정보"""

    sticker_no: int = Field(..., description="스티커번호")
    label: str = Field(..., description="스티커 라벨")
    image_url: str = Field(..., description="스티커 이미지 url")
    display_order: int = Field(..., description="전시순서")


class CustomProperty(BaseDto):
    """커스텀 속성"""

    prop_no: int = Field(..., description="항목 번호")
    prop_name: str = Field(..., description="항목명")
    prop_value_no: int = Field(..., description="항목 값 번호")
    prop_value: str = Field(..., description="항목 값명")
    is_multiple_selection: bool = Field(..., description="항목 복수선택여부")


class CustomerDemand(BaseDto):
    """구매자 작성형 옵션"""

    mall_product_input_no: int = Field(..., description="구매자작성형 번호")
    input_text: str = Field(..., description="구매자작성형 텍스트 내용")
    use_yn: str = Field(..., description="사용여부")
    required: bool = Field(..., description="필수 여부")
    input_matching_type_label: str = Field(..., description="구매자작성형 매칭타입")


class DeliveryInfo(BaseDto):
    """배송 정보"""

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
    cart: ListSearchCartInfo = Field(..., description="장바구니 정보")

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

"""상품 검색하기 (Version 2.0) - 검색엔진 응답 모델"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class DisplayPeriod(BaseDto):
    """스티커 노출 기간"""

    start_date_time: KstDatetime | None = Field(None, description="스티커 노출 시작일자")
    end_date_time: KstDatetime | None = Field(None, description="스티커 노출 종료일자")


class StickerInfo(BaseDto):
    """스티커 정보"""

    type: Literal["TEXT", "IMAGE"] = Field(..., description="스티커 타입")
    label: str = Field(..., description="스티커 라벨")
    name: str = Field(..., description="스티커 이름")
    display_period: DisplayPeriod | None = Field(None, description="스티커 기간 노출 정보")


class HasCoupons(BaseDto):
    """쿠폰 여부"""

    product: bool = Field(..., description="상품쿠폰 태그")
    partner: bool = Field(..., description="파트너쿠폰 태그")
    event: bool = Field(..., description="기획전쿠폰 태그")
    category: bool = Field(..., description="카테고리쿠폰 태그")
    brand: bool = Field(..., description="브랜드쿠폰 태그")


class ReservationData(BaseDto):
    """예약판매 정보"""

    reservation_start_ymdt: KstDatetime = Field(..., description="예약판매 시작일")
    reservation_end_ymdt: KstDatetime = Field(..., description="예약판매 종료일")
    reservation_delivery_ymdt: KstDatetime = Field(..., description="예약판매 배송시작일")
    reservation_stock_cnt: int = Field(..., description="예약판매 재고수량")


class CertificationData(BaseDto):
    """인증 데이터"""

    certification_category_no: int = Field(..., description="인증유형 번호")
    certification_contents: list[str] = Field(default_factory=list, description="인증기관, 인증번호, 인증상호")


class CertificationInfo(BaseDto):
    """인증정보"""

    type: Literal["TARGET", "NOT_TARGET", "DETAIL_PAGE"] = Field(..., description="인증정보타입")
    data: list[CertificationData] = Field(default_factory=list, description="인증정보")


class AccumulationInfo(BaseDto):
    """적립금 정보"""

    amount: float = Field(..., description="적립금")
    reward_rate_of_product: float = Field(..., description="상품개별적립률")
    reward_rate_of_member_benefit: float = Field(..., description="회원등급적립률")


class DisplayCategory(BaseDto):
    """전시 카테고리"""

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
    """옵션 값"""

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
    brand_name: str | None = Field(None, description="브랜드 명")
    brand_name_ko: str | None = Field(None, description="브랜드 한글명")
    brand_name_en: str | None = Field(None, description="브랜드 영문 명")
    brand_name_type: Literal["NAME_KO", "NAME_EN", "NONE"] | None = Field(None, description="브랜드명 타입")

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
    contents_if_pausing: str | None = Field(None, description="가격대체문구")

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

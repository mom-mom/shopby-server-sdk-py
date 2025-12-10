"""Display API 모델 정의"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


# ------------------------------------
#  기획전(Event) 관련 모델
# ------------------------------------


class DisplayPeriod(BaseDto):
    """전시기간 정보"""

    start_ymdt: KstDatetime | None = Field(None, description="전시기간 시작일")
    end_ymdt: KstDatetime | None = Field(None, description="전시기간 종료일")


class EventDisplayPeriod(BaseDto):
    """기획전 전시기간 설정"""

    period_type: str = Field(..., description="전시기간 타입 (ALWAYS, PERIOD)")
    display_period: DisplayPeriod | None = Field(None, description="전시기간 정보")


class EventCommonCouponImage(BaseDto):
    """기획전 공통 쿠폰 이미지"""

    guide_image_url: str | None = Field(None, description="쿠폰 사용안내 이미지")
    issued_coupon_image_url: str | None = Field(None, description="쿠폰 발급완료 이미지")
    already_issued_coupon_image_url: str | None = Field(None, description="기발급완료 안내 이미지")
    coupon_before_issue_image_url: str | None = Field(None, description="쿠폰발행 시작 전 이미지")
    coupon_sold_out_image_url: str | None = Field(None, description="쿠폰 발행완료(매진) 이미지")
    coupon_date_expired_image_url: str | None = Field(None, description="쿠폰발행마감(종료) 이미지")


class EventConfigDisplayOrder(BaseDto):
    """기획전 설정 노출 순서"""

    main_image_display_order: int | None = Field(None, description="상단이미지 설정 노출 순서")
    coupon_display_order: int | None = Field(None, description="쿠폰 설정 노출 순서")
    section_display_order: int | None = Field(None, description="섹션 설정 노출 순서")


class MemberDisplayInfo(BaseDto):
    """회원등급/그룹 노출 설정"""

    check: str | None = Field(None, description="설정 상태 (NONE, ANY, PART)")
    info: list[Any] = Field(default_factory=list, description="노출 설정 정보")


class PlatformDisplay(BaseDto):
    """플랫폼별 노출 설정"""

    display_mobile_yn: Literal["Y", "N"] | None = Field(None, description="모바일앱 노출 여부")
    display_pc_yn: Literal["Y", "N"] | None = Field(None, description="PC 노출 여부")
    display_mobile_web_yn: Literal["Y", "N"] | None = Field(None, description="모바일웹 노출 여부")


class PcImageDetail(BaseDto):
    """PC 상단이미지 노출 설정"""

    pc_image_type: str | None = Field(None, description="PC 상단이미지 타입 (HTML, FILE)")
    pc_image_content: str | None = Field(None, description="PC 상단 컨텐츠")


class MobileImageDetail(BaseDto):
    """모바일 상단이미지 노출 설정"""

    mobile_image_type: str | None = Field(None, description="모바일 상단이미지 타입 (HTML, FILE)")
    mobile_image_content: str | None = Field(None, description="모바일 상단 컨텐츠")


class DisplayCategoryMapping(BaseDto):
    """연관 전시 카테고리"""

    display_category_no: int = Field(..., description="전시 카테고리 번호")
    display_category_full_name: str | None = Field(None, description="전시 카테고리명")
    display_yn: Literal["Y", "N"] | None = Field(None, description="전시 여부")


class EventCoupon(BaseDto):
    """기획전 쿠폰"""

    coupon_no: int | None = Field(None, description="쿠폰 번호")
    event_coupon_image_url: str | None = Field(None, description="쿠폰 이미지 URL")


class MallProduct(BaseDto):
    """기획전 섹션 상품"""

    mall_product_no: int = Field(..., description="상품번호")
    display_yn: Literal["Y", "N"] | None = Field(None, description="상품 노출 여부")
    display_order: int | None = Field(None, description="상품 노출 순서")


class EventSectionValue(BaseDto):
    """기획전 섹션 값"""

    mall_products: list[MallProduct] = Field(default_factory=list, description="섹션 상품 목록")


class EventSection(BaseDto):
    """기획전 섹션"""

    event_section_no: int = Field(..., description="섹션 번호")
    event_section_name: str | None = Field(None, description="섹션 타이틀")
    event_section_image_url: str | None = Field(None, description="섹션 이미지 URL")
    num_products_displayed_per_row_pc: int | None = Field(None, description="PC 상품 노출 수")
    num_products_displayed_per_row_mobile: int | None = Field(None, description="모바일 상품 노출 수")
    event_section_value: EventSectionValue | None = Field(None, description="섹션 값")
    event_section_order: int | None = Field(None, description="섹션 노출 순서")
    allow_duplicate_product_yn: Literal["Y", "N"] | None = Field(None, description="중복 상품 허용 여부")


class EventDetailResponse(BaseDto):
    """
    기획전 단건 조회 응답

    OpenAPI Schema: events-eventNo-907293138
    """

    event_no: int = Field(..., description="기획전 번호")
    mall_no: int = Field(..., description="몰번호")
    event_type: Literal["GENERAL", "EXTERNAL"] = Field(..., description="기획전 유형")
    event_name: str | None = Field(None, description="기획전 이름")
    event_id: str | None = Field(None, description="기획전 ID")
    event_url_type: Literal["EVENT_NUMBER", "DIRECT"] | None = Field(None, description="기획전 상세 URL 타입")
    event_url: str | None = Field(None, description="기획전 상세 URL")
    event_yn: Literal["Y", "N"] = Field(..., description="이벤트 여부")
    event_display_period: EventDisplayPeriod | None = Field(None, description="전시기간 설정")
    main_pc_image_url: str | None = Field(None, description="PC 대표 이미지")
    main_mobile_image_url: str | None = Field(None, description="모바일 대표 이미지")
    coupon_yn: Literal["Y", "N"] | None = Field(None, description="쿠폰 사용여부")
    admin_no: int | None = Field(None, description="담당자 번호")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    event_common_coupon_image: EventCommonCouponImage | None = Field(None, description="공통 쿠폰 이미지")
    service_no: int | None = Field(None, description="서비스번호")
    update_admin_no: int | None = Field(None, description="수정자번호")
    event_config_display_order: EventConfigDisplayOrder | None = Field(None, description="설정 노출 순서")
    promotion_text: str | None = Field(None, description="홍보문구")
    tag: str | None = Field(None, description="태그")
    member_grade_display_info: MemberDisplayInfo | None = Field(None, description="회원등급 노출 설정")
    member_group_display_info: MemberDisplayInfo | None = Field(None, description="회원그룹 노출 설정")
    platform_display: PlatformDisplay | None = Field(None, description="플랫폼별 노출 설정")
    pc_image_detail: PcImageDetail | None = Field(None, description="PC 상단이미지 설정")
    mobile_image_detail: MobileImageDetail | None = Field(None, description="모바일 상단이미지 설정")
    display_category_mappings: list[DisplayCategoryMapping] = Field(
        default_factory=list, description="연관 전시 카테고리 목록"
    )
    event_coupons: list[EventCoupon] = Field(default_factory=list, description="기획전 쿠폰 목록")
    event_sections: list[EventSection] = Field(default_factory=list, description="기획전 섹션 목록")

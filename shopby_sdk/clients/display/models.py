"""Display API 모델 정의"""

from typing import Literal

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
    # 회원 등급/그룹 번호 리스트 (운영데이터는 빈 배열, products base.py memberGrade/GroupDisplayInfo 와 동일)
    info: list[int] = Field(default_factory=list, description="노출 설정 정보 (check=PART일 때만 채워짐)")


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


# ------------------------------------
#  공통 Literal 별칭
# ------------------------------------

YnType = Literal["Y", "N"]
"""Y/N 플래그"""

ReviewDisplayStatusType = Literal["DISPLAY", "BLIND", "DELETE"]
"""상품평 전시 상태 (DISPLAY: 전시중, BLIND: 전시안함, DELETE: 삭제)"""

InquiryDisplayStatusType = Literal["DISPLAY", "BLIND"]
"""상품문의 전시 상태 (DISPLAY: 전시중, BLIND: 전시안함)"""

InquiryType = Literal[
    "PRODUCT",
    "DELIVERY",
    "CANCEL",
    "RETURN",
    "EXCHANGE",
    "REFUND",
    "OTHER",
]
"""상품문의 유형"""

PlatformType = Literal[
    "PC",
    "MOBILE_WEB",
    "MOBILE_APP",
    "RESPONSIVE",
    "COMMON",
    "ALL",
]
"""플랫폼 타입"""

ProviderType = Literal[
    "PAYCO",
    "NAVER",
    "KAKAO",
    "FACEBOOK",
    "IAMSCHOOL",
    "LIIVMATE",
    "NHNENT",
    "UNIONE",
    "LINE",
    "NCPSTORE",
    "KAKAO_SYNC",
]
"""간편가입 공급 타입"""

MemberStatusType = Literal["WAITING", "ACTIVE", "FREEZE", "DORMANT", "PAUSED"]
"""회원 상태"""

MemberType = Literal["MALL", "PAYCO", "SYNC_ID", "OPEN_ID"]
"""회원 종류"""

BannerLandingUrlType = Literal["GENERAL", "IMAGE_MAP", "EVENT"]
"""배너 랜딩 URL 타입"""

BannerBrowserTargetType = Literal["CURRENT", "NEW", "REF_URL"]
"""배너 랜딩 페이지 브라우저 타겟"""

BannerDisplayPeriodType = Literal["REGULAR", "PERIOD"]
"""배너 전시 기간 타입"""

AccountDisplayType = Literal["SEQUENTIAL", "RANDOM"]
"""구좌 노출 방식"""

EventSearchDateType = Literal["REGISTER_YMDT", "DISPLAY_YMDT"]
"""기획전 조회 기간 타입"""

EventSearchType = Literal["EVENT_NAME", "EVENT_NO", "ADMIN", "EVENT_ID"]
"""기획전 검색어 타입"""

InquirySearchDateType = Literal["REGISTER_YMDT", "REPLY_YMDT"]
"""상품문의 기간 검색 종류"""

InquiryMemberSearchType = Literal["NAME", "ID", "NO"]
"""상품문의 회원 검색 타입"""

ReviewSearchType = Literal["REVIEW_NO", "PRODUCT_NO"]
"""상품평 검색 유형"""

ReviewDateSearchType = Literal["REGISTER", "UPDATE"]
"""상품평 날짜 검색 유형"""

BannerKeywordType = Literal["CODE", "ID", "NO"]
"""배너 검색 타입"""

HeadlessBannerKeywordType = Literal[
    "BANNER_GROUP_NO",
    "BANNER_NO",
    "BANNER_ID",
    "BANNER_CODE",
]
"""헤드리스 배너 검색어 타입"""


# ------------------------------------
#  배너(Banner) 관련 모델
# ------------------------------------


class BannerImage(BaseDto):
    """배너 조회 응답의 배너 정보 (banners2073301320 > accounts > banners)"""

    banner_no: int = Field(..., description="배너 번호")
    name: str | None = Field(None, description="배너명")
    name_color: str | None = Field(None, description="배너명 색상")
    description: str | None = Field(None, description="배너 설명")
    description_color: str | None = Field(None, description="배너 설명 색상")
    image_url: str | None = Field(None, description="배너 이미지 URL")
    image_name: str | None = Field(None, description="배너 이미지명")
    landing_url_type: BannerLandingUrlType | None = Field(None, description="배너 랜딩 URL 타입")
    landing_url: str | None = Field(None, description="배너 랜딩 URL")
    left_space_color: str | None = Field(None, description="배너 이미지 - 왼쪽 여백 색상")
    right_space_color: str | None = Field(None, description="배너 이미지 - 오른쪽 여백 색상")
    brower_target_type: BannerBrowserTargetType | None = Field(None, description="배너 랜딩 페이지 브라우저 타겟")
    mouse_over_image_url: str | None = Field(None, description="마우스 오버 이미지 URL")
    mouse_over_image_name: str | None = Field(None, description="마우스 오버 이미지명")
    display_period_type: BannerDisplayPeriodType | None = Field(None, description="배너 전시 기간 타입")
    display_start_ymdt: KstDatetime | None = Field(None, description="배너 전시 시작일")
    display_end_ymdt: KstDatetime | None = Field(None, description="배너 전시 종료일")
    display_order: int | None = Field(None, description="배너 전시 순서")
    video_url: str | None = Field(None, description="동영상 URL")
    display_yn: YnType | None = Field(None, description="배너 노출 여부")


class BannerAccount(BaseDto):
    """배너 조회 응답의 구좌 정보 (banners2073301320 > accounts)"""

    account_no: int = Field(..., description="배너 구좌 번호")
    account_name: str | None = Field(None, description="배너 구좌명")
    display_type: AccountDisplayType | None = Field(None, description="구좌 노출 방식")
    height: int | None = Field(None, description="구좌 높이")
    width: int | None = Field(None, description="구좌 넓이")
    platform_display_pc_yn: str | None = Field(None, description="플랫폼별 노출 설정(PC)")
    platform_display_mobile_yn: str | None = Field(None, description="플랫폼별 노출 설정(모바일앱)")
    platform_display_mobile_web_yn: str | None = Field(None, description="플랫폼별 노출 설정(모바일웹)")
    member_grade_display_info: MemberDisplayInfo | None = Field(None, description="회원등급 노출 설정")
    member_group_display_info: MemberDisplayInfo | None = Field(None, description="회원그룹 노출 설정")
    display_order: int | None = Field(None, description="구좌 노출 순서")
    display_yn: YnType | None = Field(None, description="구좌 노출 여부")
    banners: list[BannerImage] = Field(default_factory=list, description="배너 목록")


class BannerSection(BaseDto):
    """
    배너 섹션 조회 응답

    OpenAPI Schema: banners2073301320 (array item)
    """

    banner_section_no: int = Field(..., description="배너 섹션 번호")
    label: str | None = Field(None, description="배너 라벨명")
    code: str | None = Field(None, description="배너 코드")
    id: str | None = Field(None, description="배너 ID")
    group_no: int | None = Field(None, description="배너 그룹 번호")
    platform_display_pc_yn: str | None = Field(None, description="플랫폼별 노출 설정(PC)")
    platform_display_mobile_yn: str | None = Field(None, description="플랫폼별 노출 설정(모바일앱)")
    platform_display_mobile_web_yn: str | None = Field(None, description="플랫폼별 노출 설정(모바일웹)")
    member_grade_display_info: MemberDisplayInfo | None = Field(None, description="회원등급 노출 설정")
    member_group_display_info: MemberDisplayInfo | None = Field(None, description="회원그룹 노출 설정")
    accounts: list[BannerAccount] = Field(default_factory=list, description="구좌 목록")


class BannerGroup(BaseDto):
    """
    배너 그룹 조회 응답

    OpenAPI Schema: banners-groups-1471844524 (array item)
    """

    group_no: int = Field(..., description="배너 그룹 번호")
    group_name: str | None = Field(None, description="배너 그룹 이름")


class HeadlessBanner(BaseDto):
    """헤드리스 배너 정보 (banners-simple-infos1198101778 > contents)"""

    banner_no: int = Field(..., description="배너 섹션 번호")
    banner_name: str | None = Field(None, description="배너 섹션 이름")
    banner_id: str | None = Field(None, description="배너 섹션 ID")
    banner_code: str | None = Field(None, description="배너 코드")
    banner_group_no: int | None = Field(None, description="배너 그룹 번호")
    banner_group_name: str | None = Field(None, description="배너 그룹 명")
    platform_types: list[PlatformType] = Field(default_factory=list, description="플랫폼 타입 목록")
    register_date: KstDatetime | None = Field(None, description="등록일")
    update_date: KstDatetime | None = Field(None, description="수정일")


class HeadlessBannerResponse(BaseDto):
    """
    헤드리스 배너 조회 응답

    OpenAPI Schema: banners-simple-infos1198101778
    """

    last_banner_no: int | None = Field(None, description="조회된 마지막 배너 번호")
    contents: list[HeadlessBanner] = Field(default_factory=list, description="배너 목록")


class BannerExtraInfo(BaseDto):
    """
    배너 추가정보 (조회/등록/수정 공용)

    OpenAPI Schema: banners-extraInfo1993007774 (array item)
    """

    banner_no: int = Field(..., description="배너 번호")
    extra_info: str | None = Field(None, description="배너 추가정보")


class BannerDisplayPeriodValue(BaseDto):
    """배너 전시기간 값"""

    start_ymdt: KstDatetime | None = Field(None, description="전시 시작일")
    end_ymdt: KstDatetime | None = Field(None, description="전시 종료일")


class BannerDisplayPeriod(BaseDto):
    """배너 전시기간 설정"""

    period_type: BannerDisplayPeriodType = Field(..., description="전시기간 타입")
    display_period: BannerDisplayPeriodValue | None = Field(None, description="전시기간 값")


class BannerLandingUrlValue(BaseDto):
    """배너 랜딩 URL 설정"""

    landing_url_type: str = Field(..., description="랜딩 URL 타입")
    landing_url: str | None = Field(None, description="랜딩 URL")
    banner_open_location_type: str | None = Field(None, description="랜딩 URL 창 설정")


class BannerCreateItem(BaseDto):
    """배너 섹션 등록/수정 요청의 배너 항목"""

    banner_no: int | None = Field(None, description="배너 번호 (수정 시)")
    banner_name: str | None = Field(None, description="배너명")
    banner_name_color: str | None = Field(None, description="배너명 컬러코드")
    banner_description: str | None = Field(None, description="배너설명")
    banner_description_color: str | None = Field(None, description="배너설명 컬러코드")
    banner_image_url: str | None = Field(None, description="이미지 URL 주소")
    banner_image_name: str | None = Field(None, description="이미지 원본 파일명")
    banner_mouse_over_image_url: str | None = Field(None, description="마우스오버 이미지 URL")
    banner_mouse_over_image_name: str | None = Field(None, description="마우스오버 이미지 원본 파일명")
    left_image_space_color: str | None = Field(None, description="좌측 여백 컬러코드")
    right_image_space_color: str | None = Field(None, description="우측 여백 컬러코드")
    video_url: str | None = Field(None, description="동영상 URL")
    display_order: int | None = Field(None, description="배너 노출 순서")
    landing_url_value: BannerLandingUrlValue | None = Field(None, description="랜딩 URL 설정")
    banner_display_period: BannerDisplayPeriod | None = Field(None, description="배너 전시기간")
    extra_info: str | None = Field(None, description="추가 정보")
    display_yn: YnType | None = Field(None, description="배너 노출 여부")


class BannerAccountCreate(BaseDto):
    """배너 섹션 등록/수정 요청의 구좌 항목"""

    account_no: int | None = Field(None, description="배너구좌 번호 (수정 시)")
    account_name: str | None = Field(None, description="배너구좌명")
    account_width: int | None = Field(None, description="구좌 너비")
    account_height: int | None = Field(None, description="구좌 높이")
    account_display_type: str | None = Field(None, description="구좌 노출 방식")
    member_grade_display_info: MemberDisplayInfo | None = Field(None, description="회원등급 노출 설정")
    member_group_display_info: MemberDisplayInfo | None = Field(None, description="회원그룹 노출 설정")
    platform_display: PlatformDisplay | None = Field(None, description="플랫폼별 노출 설정")
    display_yn: YnType | None = Field(None, description="구좌 노출 여부")
    display_order: int | None = Field(None, description="구좌 노출 순서")
    banners: list[BannerCreateItem] = Field(default_factory=list, description="배너 목록")


class BannerSectionCreateRequest(BaseDto):
    """
    배너 섹션 등록 요청

    OpenAPI Schema: banners2120124801
    """

    group_no: int | None = Field(None, description="배너그룹 번호")
    banner_section_name: str | None = Field(None, description="배너 섹션명")
    banner_section_id: str | None = Field(None, description="배너 섹션 ID")
    member_grade_display_info: MemberDisplayInfo | None = Field(None, description="회원등급 노출 설정")
    member_group_display_info: MemberDisplayInfo | None = Field(None, description="회원그룹 노출 설정")
    platform_display: PlatformDisplay | None = Field(None, description="플랫폼별 노출 설정")
    banner_accounts: list[BannerAccountCreate] = Field(default_factory=list, description="구좌 목록")


class BannerSectionUpdateRequest(BaseDto):
    """
    배너 섹션 수정 요청

    OpenAPI Schema: banners-bannerNo803285355
    """

    group_no: int | None = Field(None, description="배너그룹 번호")
    banner_section_name: str | None = Field(None, description="배너 섹션명")
    banner_section_id: str | None = Field(None, description="배너 섹션 ID")
    member_grade_display_info: MemberDisplayInfo | None = Field(None, description="회원등급 노출 설정")
    member_group_display_info: MemberDisplayInfo | None = Field(None, description="회원그룹 노출 설정")
    platform_display: PlatformDisplay | None = Field(None, description="플랫폼별 노출 설정")
    banner_accounts: list[BannerAccountCreate] = Field(default_factory=list, description="구좌 목록")


# ------------------------------------
#  카테고리(Category) 관련 모델
# ------------------------------------


class StandardCategory(BaseDto):
    """
    표준 카테고리 조회 응답

    OpenAPI Schema: categories-1596124036 (array item)
    """

    depth1_category_no: int | None = Field(None, description="1depth 카테고리 번호")
    depth1_category_name: str | None = Field(None, description="1depth 카테고리 명")
    depth1_display_cd: str | None = Field(None, description="1depth 카테고리 전시 코드")
    depth1_display_order: int | None = Field(None, description="1depth 카테고리 전시순서")
    depth2_category_no: int | None = Field(None, description="2depth 카테고리 번호")
    depth2_category_name: str | None = Field(None, description="2depth 카테고리 명")
    depth2_display_cd: str | None = Field(None, description="2depth 카테고리 전시 코드")
    depth2_display_order: int | None = Field(None, description="2depth 카테고리 전시순서")
    depth3_category_no: int | None = Field(None, description="3depth 카테고리 번호")
    depth3_category_name: str | None = Field(None, description="3depth 카테고리 명")
    depth3_display_cd: str | None = Field(None, description="3depth 카테고리 전시 코드")
    depth3_display_order: int | None = Field(None, description="3depth 카테고리 전시순서")
    depth4_category_no: int | None = Field(None, description="4depth 카테고리 번호")
    depth4_category_name: str | None = Field(None, description="4depth 카테고리 명")
    depth4_display_cd: str | None = Field(None, description="4depth 카테고리 전시 코드")
    depth4_display_order: int | None = Field(None, description="4depth 카테고리 전시순서")
    full_category_name: str | None = Field(None, description="카테고리 명")
    adult_yn: YnType | None = Field(None, description="성인전용 여부")
    commission_rate: float | None = Field(None, description="수수료")


class DisplayCategory(BaseDto):
    """
    전시 카테고리 조회 응답 (depth 평면 구조)

    OpenAPI Schema: categories-display-categories-1596596913 (array item)
    """

    depth1_display_category_no: int | None = Field(None, description="1depth 카테고리 번호")
    depth1_display_category_name: str | None = Field(None, description="1depth 카테고리 명")
    depth1_icon: str | None = Field(None, description="1depth 카테고리 아이콘")
    depth1_top_image_content: str | None = Field(None, description="1depth 카테고리 상단 이미지")
    depth1_display_order: int | None = Field(None, description="1depth 카테고리 전시순서")
    depth1_display_yn: YnType | None = Field(None, description="1depth 전시 여부")
    depth2_display_category_no: int | None = Field(None, description="2depth 카테고리 번호")
    depth2_display_category_name: str | None = Field(None, description="2depth 카테고리 명")
    depth2_icon: str | None = Field(None, description="2depth 카테고리 아이콘")
    depth2_top_image_content: str | None = Field(None, description="2depth 카테고리 상단 이미지")
    depth2_display_order: int | None = Field(None, description="2depth 카테고리 전시순서")
    depth2_display_yn: YnType | None = Field(None, description="2depth 전시 여부")
    depth3_display_category_no: int | None = Field(None, description="3depth 카테고리 번호")
    depth3_display_category_name: str | None = Field(None, description="3depth 카테고리 명")
    depth3_icon: str | None = Field(None, description="3depth 카테고리 아이콘")
    depth3_top_image_content: str | None = Field(None, description="3depth 카테고리 상단 이미지")
    depth3_display_order: int | None = Field(None, description="3depth 카테고리 전시순서")
    depth3_display_yn: YnType | None = Field(None, description="3depth 전시 여부")
    depth4_display_category_no: int | None = Field(None, description="4depth 카테고리 번호")
    depth4_display_category_name: str | None = Field(None, description="4depth 카테고리 명")
    depth4_icon: str | None = Field(None, description="4depth 카테고리 아이콘")
    depth4_top_image_content: str | None = Field(None, description="4depth 카테고리 상단 이미지")
    depth4_display_order: int | None = Field(None, description="4depth 카테고리 전시순서")
    depth4_display_yn: YnType | None = Field(None, description="4depth 전시 여부")
    depth5_display_category_no: int | None = Field(None, description="5depth 카테고리 번호")
    depth5_display_category_name: str | None = Field(None, description="5depth 카테고리 명")
    depth5_icon: str | None = Field(None, description="5depth 카테고리 아이콘")
    depth5_top_image_content: str | None = Field(None, description="5depth 카테고리 상단 이미지")
    depth5_display_order: int | None = Field(None, description="5depth 카테고리 전시순서")
    depth5_display_yn: YnType | None = Field(None, description="5depth 전시 여부")
    full_category_name: str | None = Field(None, description="전체 카테고리 명")
    delete_yn: YnType | None = Field(None, description="삭제 여부")


class DisplayCategoryTreeNode(BaseDto):
    """
    전시카테고리 트리 노드

    OpenAPI Schema: categories-display-categories-tree-1227132063 (array item)
    """

    display_category_no: int = Field(..., description="전시카테고리 번호")
    mall_no: int | None = Field(None, description="몰 번호")
    display_category_name: str | None = Field(None, description="전시카테고리 이름")
    icon: str | None = Field(None, description="아이콘")
    top_image_content: str | None = Field(None, description="상단이미지")
    display_order: int | None = Field(None, description="전시순서")
    parent_display_category_no: int | None = Field(None, description="부모 전시카테고리 번호")
    depth: int | None = Field(None, description="depth")
    display_yn: YnType | None = Field(None, description="전시여부")
    product_count: int | None = Field(None, description="연결된 상품 수")
    category_url: str | None = Field(None, description="전시카테고리 URL")
    display_category_management_code: str | None = Field(None, description="전시카테고리 관리코드")
    children: list["DisplayCategoryTreeNode"] = Field(default_factory=list, description="자식 전시카테고리")


class DisplayCategoryCreateRequest(BaseDto):
    """
    전시 카테고리 등록 요청

    OpenAPI Schema: categories-display-categories1980376054
    """

    display_category_name: str = Field(..., description="전시카테고리 명 (최대 50자)")
    parent_display_category_no: int = Field(..., description="부모 전시카테고리 번호 (0이면 루트)")
    display_order: int | None = Field(None, description="전시 순서 (1 이상)")
    display_yn: YnType | None = Field(None, description="전시 여부")
    icon: str | None = Field(None, description="아이콘 URL (최대 500자)")
    top_image_content: str | None = Field(None, description="상단 이미지 내용")
    display_category_management_code: str | None = Field(None, description="관리코드 (최대 45자, 몰 내 유니크)")


class DisplayCategoryCreateResponse(BaseDto):
    """
    전시 카테고리 등록 응답

    OpenAPI Schema: categories-display-categories758995774
    """

    display_category_no: int = Field(..., description="생성된 전시카테고리 번호")


class DisplayCategoryUpdateRequest(BaseDto):
    """
    전시 카테고리 수정 요청 (부분 수정)

    OpenAPI Schema: categories-display-categories-displayCategoryNo-377948581
    """

    display_category_name: str | None = Field(None, description="전시카테고리 명 (최대 50자)")
    display_yn: YnType | None = Field(None, description="전시 여부")
    icon: str | None = Field(None, description="아이콘 URL (최대 500자)")
    top_image_content: str | None = Field(None, description="상단 이미지 내용")
    display_category_management_code: str | None = Field(None, description="관리코드 (최대 45자, 몰 내 유니크)")


# ------------------------------------
#  기획전(Event) 검색 모델
# ------------------------------------


class EventListPeriod(BaseDto):
    """기획전 목록의 전시기간 값"""

    start_ymdt: KstDatetime | None = Field(None, description="전시 시작일")
    end_ymdt: KstDatetime | None = Field(None, description="전시 종료일")


class EventListDisplayPeriod(BaseDto):
    """기획전 목록의 전시기간 설정"""

    period_type: str | None = Field(None, description="전시기간 타입 코드")
    display_period: EventListPeriod | None = Field(None, description="전시기간 값")


class EventListItem(BaseDto):
    """기획전 검색 결과 항목 (events1968241914 > contents)"""

    event_no: int = Field(..., description="기획전 번호")
    mall_no: int | None = Field(None, description="몰번호")
    mall_name: str | None = Field(None, description="몰이름")
    event_type: Literal["GENERAL", "EXTERNAL"] | None = Field(None, description="기획전 유형")
    event_name: str | None = Field(None, description="기획전 이름")
    event_id: str | None = Field(None, description="기획전 Id")
    event_url: str | None = Field(None, description="기획전 Url")
    event_display_period: EventListDisplayPeriod | None = Field(None, description="전시기간 설정")
    coupon_yn: YnType | None = Field(None, description="쿠폰 사용여부 코드")
    admin_no: int | None = Field(None, description="담당자 번호")
    admin_name: str | None = Field(None, description="담당자 이름")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")


class EventSearchResponse(BaseDto):
    """
    기획전 검색 응답

    OpenAPI Schema: events1968241914
    """

    total_count: int | None = Field(None, description="전체 게시물 수")
    total_page: int | None = Field(None, description="전체 페이지 수")
    contents: list[EventListItem] = Field(default_factory=list, description="기획전 목록")


# ------------------------------------
#  상품문의(Inquiry) 관련 모델
# ------------------------------------


class Inquiry(BaseDto):
    """
    상품문의 조회 응답

    OpenAPI Schema: inquiry1172738976 (array item)
    """

    inquiry_no: int = Field(..., description="상품문의 번호")
    product_no: int | None = Field(None, description="상품번호")
    product_name: str | None = Field(None, description="상품명")
    brand_name: str | None = Field(None, description="브랜드명")
    partner_no: int | None = Field(None, description="파트너 번호")
    partner_name: str | None = Field(None, description="파트너 명")
    order_no: str | None = Field(None, description="주문번호")
    type: InquiryType | None = Field(None, description="문의 유형")
    title: str | None = Field(None, description="상품문의 제목")
    content: str | None = Field(None, description="상품문의 내용")
    member_id: str | None = Field(None, description="등록 사용자 아이디")
    member_name: str | None = Field(None, description="등록 사용자 이름")
    member_no: int | None = Field(None, description="등록 사용자 번호")
    nick_name: str | None = Field(None, description="닉네임")
    replied: bool | None = Field(None, description="답변 여부")
    is_secret: bool | None = Field(None, description="비밀글 여부")
    display_status_type: InquiryDisplayStatusType | None = Field(None, description="전시 상태")
    register_ymdt: KstDatetime | None = Field(None, description="최초 등록일")
    update_ymdt: KstDatetime | None = Field(None, description="최종 수정일")
    reply_ymdt: KstDatetime | None = Field(None, description="답변 날짜")


class InquiryReply(BaseDto):
    """
    상품문의 답변 조회 응답

    OpenAPI Schema: inquiry-replies-1796672765 (array item)
    """

    inquiry_no: int = Field(..., description="답변 문의 번호")
    parent_inquiry_no: int | None = Field(None, description="해당 답변이 등록된 문의의 번호")
    product_no: int | None = Field(None, description="상품번호")
    content: str | None = Field(None, description="상품문의 답변 내용")
    register_name: str | None = Field(None, description="등록자")
    register_no: int | None = Field(None, description="등록자 번호")
    register_ymdt: KstDatetime | None = Field(None, description="최초 등록일")
    update_ymdt: KstDatetime | None = Field(None, description="최종 수정일")


class InquiryDisplayStatusUpdateRequest(BaseDto):
    """
    상품 문의 전시 상태 변경 요청

    OpenAPI Schema: inquiry-inquiryNo-display-status-1294323154
    """

    display_status_type: InquiryDisplayStatusType = Field(..., description="변경할 전시 상태")
    reason: str | None = Field(None, description="전시 상태 변경 사유")


# ------------------------------------
#  상품평(Review) 관련 모델
# ------------------------------------


class ReviewRegister(BaseDto):
    """상품평 작성 회원 정보"""

    member_no: int | None = Field(None, description="회원 번호")
    member_name: str | None = Field(None, description="회원 이름")
    member_id: str | None = Field(None, description="회원 ID")
    member_type: MemberType | None = Field(None, description="회원 종류")
    member_status: MemberStatusType | None = Field(None, description="회원 상태")
    nickname: str | None = Field(None, description="회원 닉네임")


class Review(BaseDto):
    """
    상품평 조회 응답 항목 (reviews-1312461930 > contents)
    """

    review_no: int = Field(..., description="상품평 번호")
    mall_no: int | None = Field(None, description="상점 번호")
    mall_name: str | None = Field(None, description="쇼핑몰")
    display_status_type: ReviewDisplayStatusType | None = Field(None, description="전시상태")
    is_best_review: str | None = Field(None, description="상품평 구분 (베스트/일반)")
    rating: float | None = Field(None, description="평점")
    report_cnt: int | None = Field(None, description="신고 수")
    blind_report_cnt: int | None = Field(None, description="블라인드 신고 수")
    recommend_cnt: int | None = Field(None, description="추천 수")
    product_no: int | None = Field(None, description="상품번호")
    product_name: str | None = Field(None, description="상품명")
    option_no: int | None = Field(None, description="옵션번호")
    option_name: str | None = Field(None, description="옵션명")
    partner_no: int | None = Field(None, description="파트너 번호")
    partner_name: str | None = Field(None, description="파트너사")
    brand_name: str | None = Field(None, description="브랜드명")
    register_info: ReviewRegister | None = Field(None, alias="register", description="작성 회원 정보")
    order_no: str | None = Field(None, description="주문번호")
    order_product_option_no: int | None = Field(None, description="주문 옵션 번호")
    register_date_time: KstDatetime | None = Field(None, description="등록일")
    update_date_time: KstDatetime | None = Field(None, description="수정일자")
    delete_yn: YnType | None = Field(None, description="삭제 여부")
    attach_yn: YnType | None = Field(None, description="첨부파일 여부")
    master_yn: YnType | None = Field(None, description="마스터 여부")
    platform_type: PlatformType | None = Field(None, description="작성 플랫폼")
    provider_type: ProviderType | None = Field(None, description="공급 타입")
    extra_json: str | None = Field(None, description="상품평 작성 리뷰")
    content: str | None = Field(None, description="내용")
    file_urls: list[str] = Field(default_factory=list, description="첨부파일 url")
    external_review: bool | None = Field(None, description="외부 작성 여부")


class ReviewListResponse(BaseDto):
    """
    상품평 조회 응답

    OpenAPI Schema: reviews-1312461930
    """

    total_count: int | None = Field(None, description="전체 상품평 수")
    total_page: int | None = Field(None, description="전체 페이지 수")
    last_id: str | None = Field(None, description="검색 기준 값")
    contents: list[Review] = Field(default_factory=list, description="상품평 목록")


class ReviewSearchProduct(BaseDto):
    """상품평 검색 결과의 상품 정보 (reviews473435012 > contents > product)"""

    product_no: int | None = Field(None, description="상품번호")
    product_name: str | None = Field(None, description="상품명")
    option_no: int | None = Field(None, description="옵션번호")
    option_name: str | None = Field(None, description="옵션명")
    brand_name: str | None = Field(None, description="브랜드명")
    partner_name: str | None = Field(None, description="파트너사")


class ReviewSearchAccumulationInfo(BaseDto):
    """상품평 검색 결과의 누적 정보"""

    report_cnt: int | None = Field(None, description="신고 수")
    blind_report_cnt: int | None = Field(None, description="블라인드 신고 수")
    recommend_cnt: int | None = Field(None, description="추천 수")


class ReviewSearchItem(BaseDto):
    """상품평 검색 결과 항목 (reviews473435012 > contents)"""

    no: int = Field(..., description="상품평 번호")
    mall_no: int | None = Field(None, description="상점 번호")
    mall_name: str | None = Field(None, description="쇼핑몰")
    product: ReviewSearchProduct | None = Field(None, description="상품 정보")
    order_no: str | None = Field(None, description="주문번호")
    order_product_option_no: int | None = Field(None, description="주문 옵션 번호")
    platform_type: PlatformType | None = Field(None, description="작성 플랫폼")
    provider_type: ProviderType | None = Field(None, description="공급 타입")
    register_info: ReviewRegister | None = Field(None, alias="register", description="작성 회원 정보")
    register_date_time: KstDatetime | None = Field(None, description="등록일")
    update_date_time: KstDatetime | None = Field(None, description="수정일자")
    rating: float | None = Field(None, description="평점")
    content: str | None = Field(None, description="내용")
    has_attached: bool | None = Field(None, description="첨부파일 여부")
    is_best_review: str | None = Field(None, description="상품평 구분 (베스트/일반)")
    is_deleted: bool | None = Field(None, description="삭제 여부")
    accumulation_info: ReviewSearchAccumulationInfo | None = Field(None, description="누적 정보")
    extra_json: str | None = Field(None, description="상품평 작성 리뷰")
    master_yn: YnType | None = Field(None, description="마스터 여부")
    display_status_type: ReviewDisplayStatusType | None = Field(None, description="전시상태")


class ReviewSearchResponse(BaseDto):
    """
    상품평 검색 응답

    OpenAPI Schema: reviews473435012
    """

    total_count: int | None = Field(None, description="전체 상품평 수")
    total_page: int | None = Field(None, description="전체 페이지 수")
    last_id: str | None = Field(None, description="검색 기준 값")
    contents: list[ReviewSearchItem] = Field(default_factory=list, description="상품평 목록")


class ReviewSearchMember(BaseDto):
    """상품평 검색 요청의 회원 검색 조건"""

    keyword: str | None = Field(None, description="회원검색조건 - 회원ID or 회원명 or 회원NO")
    type: InquiryMemberSearchType | None = Field(None, description="회원검색조건 - 회원검색타입")


class ReviewSearchRequest(BaseDto):
    """
    상품평 검색 요청

    OpenAPI Schema: reviews-991924649
    """

    keyword: str | None = Field(None, description="검색하고자하는 번호 (여러건은 ','로 연결)")
    search_type: ReviewSearchType | None = Field(None, description="검색 유형")
    date_search_type: ReviewDateSearchType | None = Field(None, description="날짜 검색 유형")
    start_ymd: str | None = Field(None, description="작성일시 시작 (yyyy-MM-dd)")
    end_ymd: str | None = Field(None, description="작성일시 끝 (yyyy-MM-dd)")
    member: ReviewSearchMember | None = Field(None, description="회원검색조건")
    has_deleted: str | None = Field(None, description="삭제된 상품평 조회 여부")
    has_total_count: int | None = Field(None, description="전체카운트 수 조회 여부")
    page: int | None = Field(None, description="페이지 번호")
    size: int | None = Field(None, description="한 페이지에 조회되는 상품평 갯수")
    search_after: str | None = Field(None, description="검색 기준 값(lastId)")


class ReviewCreateItem(BaseDto):
    """상품평 등록 요청 항목 (reviews-product-reviews-1296538423 array item)"""

    product_no: int = Field(..., description="상품 번호")
    option_no: int | None = Field(None, description="상품 옵션 번호")
    order_option_no: int | None = Field(None, description="주문 옵션 번호")
    register_no: int | None = Field(None, description="작성자 번호")
    rate: float | None = Field(None, description="상품평 평점")
    content: str | None = Field(None, description="상품평 내용")
    urls: list[str] = Field(default_factory=list, description="첨부파일 url 리스트")
    review_external_id: str | None = Field(None, description="외부 리뷰 번호")
    register_ymdt: KstDatetime | None = Field(None, description="등록 날짜")
    use_naver_review_cnt: bool | None = Field(None, description="네이버 리뷰 카운팅 사용 여부")


class ReviewUpdateItem(BaseDto):
    """상품평 수정 요청 항목 (reviews-product-reviews756382224 array item)"""

    review_no: int = Field(..., description="리뷰 번호")
    product_no: int | None = Field(None, description="상품 번호")
    register_no: int | None = Field(None, description="작성자 번호")
    rate: float | None = Field(None, description="상품평 평점")
    content: str | None = Field(None, description="상품평 내용")
    urls: list[str] = Field(default_factory=list, description="첨부파일 url 리스트")
    review_external_id: str | None = Field(None, description="외부 리뷰 번호")


class ReviewCreateFailure(BaseDto):
    """상품평 등록 실패 정보"""

    message: str | None = Field(None, description="등록 실패 사유")
    option_no: int | None = Field(None, description="등록 실패 상품 옵션 번호")


class ReviewCreateResponse(BaseDto):
    """
    상품평 등록 응답

    OpenAPI Schema: reviews-product-reviews628947065
    """

    total_count: int | None = Field(None, description="요청 개수")
    success_nos: list[int] = Field(default_factory=list, description="생성된 리뷰 번호")
    failures: list[ReviewCreateFailure] = Field(default_factory=list, description="등록 실패 목록")


class ReviewUpdateFailure(BaseDto):
    """상품평 수정 실패 정보"""

    review_no: int | None = Field(None, description="수정 실패 리뷰 번호")
    message: str | None = Field(None, description="수정 실패 사유")


class ReviewUpdateResponse(BaseDto):
    """
    상품평 수정 응답

    OpenAPI Schema: reviews-product-reviews-835404475
    """

    total_count: int | None = Field(None, description="요청 개수")
    success_nos: list[int] = Field(default_factory=list, description="수정된 리뷰 번호")
    failures: list[ReviewUpdateFailure] = Field(default_factory=list, description="수정 실패 목록")


class ReviewDeleteFailure(BaseDto):
    """상품평 삭제 실패 정보"""

    review_no: int | None = Field(None, description="삭제 실패 리뷰 번호")
    message: str | None = Field(None, description="삭제 실패 사유")


class ReviewDeleteResponse(BaseDto):
    """
    상품평 삭제 응답

    OpenAPI Schema: reviews-product-reviews-1765281674
    """

    total_count: int | None = Field(None, description="요청 개수")
    success_nos: list[int] = Field(default_factory=list, description="삭제된 리뷰 번호")
    failures: list[ReviewDeleteFailure] = Field(default_factory=list, description="삭제 실패 목록")


class ExternalSiteReviewCreateItem(BaseDto):
    """외부 상품평 등록 요청 항목 (reviews-external-site-1338271587 array item)"""

    product_no: int = Field(..., description="상품 번호")
    rating: float | None = Field(None, description="평점")
    content: str | None = Field(None, description="상품평 내용")
    image_urls: list[str] = Field(default_factory=list, description="상품평 첨부파일")
    origin_site_name: str | None = Field(None, description="외부 사이트 명")
    origin_product_detail_url: str | None = Field(None, description="외부 상품 상세 url")
    origin_register_ymdt: KstDatetime | None = Field(None, description="외부 사이트에서 작성된 리뷰 날짜")
    use_naver_review_cnt: bool | None = Field(None, description="네이버 리뷰 카운팅 사용 여부")


class ExternalSiteReviewCreateFailure(BaseDto):
    """외부 상품평 등록 실패 정보"""

    message: str | None = Field(None, description="등록 실패 사유")
    product_no: int | None = Field(None, description="등록 실패 상품 번호")


class ExternalSiteReviewCreateResponse(BaseDto):
    """
    외부 상품평 등록 응답

    OpenAPI Schema: reviews-external-site-1052897047
    """

    total_count: int | None = Field(None, description="요청 개수")
    success_nos: list[int] = Field(default_factory=list, description="생성된 리뷰 번호")
    failures: list[ExternalSiteReviewCreateFailure] = Field(default_factory=list, description="등록 실패 목록")


class BestReviewUpdateRequest(BaseDto):
    """
    상품평 베스트 리뷰 일괄 변경 요청

    OpenAPI Schema: reviews-best-review1374636712
    """

    review_nos: list[int] = Field(default_factory=list, description="상품평 번호 리스트")
    best_review_yn: YnType = Field(..., description="베스트 리뷰 여부")


class ReviewStatusUpdateRequest(BaseDto):
    """
    상품평 전시상태 일괄 변경 요청

    OpenAPI Schema: reviews-status1927414927
    """

    review_nos: list[int] = Field(default_factory=list, description="상품평 번호 리스트")
    display_status_type: ReviewDisplayStatusType = Field(..., description="전시 상태")


class ReviewExtraJsonUpdateItem(BaseDto):
    """
    상품평 extraJson 일괄 변경 요청 항목

    OpenAPI Schema: reviews-extraJson1198411255 (array item)
    """

    review_no: int = Field(..., description="상품평 번호")
    extra_json: str | None = Field(None, description="상품평 추가정보")


class ReviewBulkUpdateFailResult(BaseDto):
    """상품평 일괄 변경 실패 결과"""

    review_no: int | None = Field(None, description="변경 실패한 상품평 번호")
    update_result_code: str | None = Field(None, description="변경 실패 사유")


class ReviewBulkUpdateResponse(BaseDto):
    """
    상품평 일괄 변경 응답 (베스트/전시상태/extraJson 공용)

    OpenAPI Schema: reviews-best-review2140100592
    """

    success_review_nos: list[int] = Field(default_factory=list, description="변경 성공한 상품평 번호")
    updated_register_nos: list[int] = Field(default_factory=list, description="변경 성공한 상품평 작성자 번호")
    fail_review_results: list[ReviewBulkUpdateFailResult] = Field(
        default_factory=list, description="변경 실패한 상품평 정보"
    )


# ------------------------------------
#  스티커(Sticker) 관련 모델
# ------------------------------------


class Sticker(BaseDto):
    """스티커 항목 (stickers-1355996430 > contents)"""

    sticker_no: int = Field(..., description="스티커 번호")
    sticker_name: str | None = Field(None, description="스티커명")
    content: str | None = Field(None, description="스티커 내용")
    usable: bool | None = Field(None, description="사용 가능 여부")


class StickerListResponse(BaseDto):
    """
    스티커 목록 조회 응답

    OpenAPI Schema: stickers-1355996430
    """

    total_count: int | None = Field(None, description="전체 스티커 수")
    total_page: int | None = Field(None, description="전체 페이지 수")
    contents: list[Sticker] = Field(default_factory=list, description="스티커 목록")

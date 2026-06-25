"""Shopby Shop(Client) Admin API 모델.

admin-shop-public.yml 의 응답 스키마를 BaseDto 기반 모델로 표현한다.
모든 필드는 snake_case 이며 BaseDto 가 camelCase alias 를 자동 생성한다.

응답 필드는 실데이터가 null 일 수 있으므로 넉넉하게 Optional 로 둔다.
"""

from typing import Any

from pydantic import Field

from shopby_sdk.base.dto import BaseDto

# =====================================================================
#  /malls/internationalization — malls-internationalization-1441815995
# =====================================================================


class Currency(BaseDto):
    """통화 설정 (CurrencyResponse)."""

    exchange_to: str | None = Field(None, description="통화 (KRW, USD, JPY, CNY)")
    exchange_rate: float | None = Field(
        None, description="1 통화(exchangeTo) 당 기준통화(KRW) 비율"
    )


class MallInternationalizationResponse(BaseDto):
    """현재 몰의 다국어/환율 설정 (malls-internationalization-1441815995)."""

    languages: list[str] | None = Field(None, description="다국어 설정 (KO/ZH/JA/EN)")
    currencies: list[Currency] | None = Field(None, description="통화 설정")


# =====================================================================
#  /malls/partners — malls-partners650086238 (array)
# =====================================================================


class MallPartner(BaseDto):
    """몰과 계약한 파트너 정보."""

    partner_no: int | None = Field(None, description="파트너 번호")
    contract_status: str | None = Field(
        None,
        description="계약 상태 (WAITING/INVESTIGATION/ACTIVE/SUSPEND)",
    )
    owner_name: str | None = Field(None, description="대표자명")
    fax_no: str | None = Field(None, description="FAX 번호")
    partner_name: str | None = Field(None, description="판매자명")
    office_address_label: str | None = Field(None, description="사업장 주소")
    company_name: str | None = Field(None, description="상호명")
    business_registration_no: str | None = Field(None, description="사업자 번호")
    online_marketing_business_declaration_no: str | None = Field(
        None, description="통신판매신고번호"
    )
    email: str | None = Field(None, description="대표 이메일")
    phone_no: str | None = Field(None, description="대표번호")


# =====================================================================
#  /malls/ssl — malls-ssl-953646756 (array)
# =====================================================================


class MallSsl(BaseDto):
    """현재 도메인의 보안서버정보."""

    device_type: str | None = Field(None, description="디바이스타입")
    domain: str | None = Field(None, description="도메인")
    mall_no: int | None = Field(None, description="몰번호")
    trust_seal: str | None = Field(None, description="보안서버 인증서 씰 스크립트")


# =====================================================================
#  /malls/service-basic-info — malls-service-basic-info80696937
#  (= /malls 응답의 serviceBasicInfo 와 동일 구조)
# =====================================================================


class ServiceBasicInfoResponse(BaseDto):
    """몰 서비스 기본 정보 (malls-service-basic-info80696937)."""

    address: str | None = Field(None, description="도로명주소")
    represent_email: str | None = Field(None, description="대표이메일")
    company_name: str | None = Field(None, description="상호명")
    privacy_manager_name: str | None = Field(None, description="개인정보보호책임자명")
    jibun_address: str | None = Field(None, description="지번주소")
    online_marketing_business_declaration_no: str | None = Field(
        None, description="통신판매업신고번호"
    )
    business_condition: str | None = Field(None, description="종목")
    zip_cd: str | None = Field(None, description="우편번호")
    address_detail: str | None = Field(None, description="도로명주소 상세")
    fax_no: str | None = Field(None, description="팩스번호")
    privacy_manager_phone_no: str | None = Field(
        None, description="개인정보보호책임자 전화번호"
    )
    business_registration_no: str | None = Field(None, description="사업자등록번호")
    represent_phone_no: str | None = Field(None, description="대표전화번호")
    business_type: str | None = Field(None, description="업태")
    plan: str | None = Field(None, description="서비스 플랜")
    jibun_address_detail: str | None = Field(None, description="지번주소 상세")
    representative_name: str | None = Field(None, description="대표자명")


# =====================================================================
#  /malls — malls1513324780 (대형 중첩 스키마)
# =====================================================================


# ---------- mall ----------
class MallUrl(BaseDto):
    """접속 URL."""

    pc: str | None = Field(None, description="PC 접속 URL")
    android: str | None = Field(None, description="안드로이드 마켓 URL")
    mobile: str | None = Field(None, description="모바일웹 접속 URL")
    ios: str | None = Field(None, description="앱스토어 URL")


class ServiceCenter(BaseDto):
    """서비스센터 정보."""

    phone_no: str | None = Field(None, description="서비스센터 전화번호")
    email: str | None = Field(None, description="서비스센터 이메일")


class IntroRedirection(BaseDto):
    """인트로 페이지 설정정보."""

    pc: str | None = Field(None, description="인트로 페이지 PC 웹 설정정보")
    mobile: str | None = Field(None, description="인트로 페이지 모바일 웹 설정정보")


class EscrowLogo(BaseDto):
    """에스크로 로고정보."""

    logo_html: str | None = Field(None, description="로고 노출 HTML 코드 (이니시스만)")
    pg_type: str | None = Field(None, description="PG사")
    exposure: bool | None = Field(None, description="에스크로 이미지 노출여부")


class GlobalMallHierarchy(BaseDto):
    """글로벌 몰 메인-서브 관계."""

    main_mall_nos: list[int] | None = Field(None, description="메인 몰 번호")
    sub_mall_nos: list[int] | None = Field(None, description="서브 몰 번호")


class I18nConfig(BaseDto):
    """글로벌 서브몰 국제화 설정."""

    # languages 는 스펙상 oneOf(object/boolean/string/number) 의 배열이라 동적임 → Any
    languages: list[Any] | None = Field(None, description="언어 설정 (KO/ZH/JA/EN)")
    currencies: list[Currency] | None = Field(None, description="화폐/통화 설정")


class GlobalSubMallSummary(BaseDto):
    """글로벌 서브몰 요약 정보."""

    i18n_config: I18nConfig | None = Field(None, description="국제화 설정")
    mall_no: int | None = Field(None, description="글로벌 서브몰 번호")
    url: MallUrl | None = Field(None, description="글로벌 서브몰 접속 URL")


class GradeEvaluationCondition(BaseDto):
    """회원 등급 평가 조건."""

    minimum_payment: float | None = Field(None, description="최소 구매 금액")
    minimum_count: int | None = Field(None, description="최소 구매 횟수")


class GradeReserveAutoSupplying(BaseDto):
    """적립금 자동지급."""

    amount: float | None = Field(None, description="적립금 자동지급 적립금액")
    used: bool | None = Field(None, description="적립금 자동지급 사용여부")
    type: str | None = Field(None, description="적립금 자동지급 유형 (NONE/ONCE/MONTHLY)")


class GradeReserveBenefit(BaseDto):
    """적립금 혜택."""

    reserve_rate: float | None = Field(None, description="적립금 혜택 적립률")
    used: bool | None = Field(None, description="적립금 혜택 사용여부")


class GradeCoupon(BaseDto):
    """회원 등급에 발급된 쿠폰."""

    issue_type: str | None = Field(None, description="쿠폰 발급 유형")
    maximum_discount_amount: float | None = Field(
        None, description="최대 할인금액 (정률할인시)"
    )
    coupon_name: str | None = Field(None, description="쿠폰 이름")
    discount_percent: float | None = Field(None, description="할인률 (정률할인시)")
    discount_amount: float | None = Field(None, description="할인금액 (정액할인시)")
    discount_type: str | None = Field(None, description="쿠폰 할인 유형 (AMOUNT/PERCENT)")
    coupon_no: int | None = Field(None, description="쿠폰 번호")


class MallGrade(BaseDto):
    """회원 등급."""

    reserve_auto_supplying: GradeReserveAutoSupplying | None = Field(
        None, description="적립금 자동지급"
    )
    evaluation_condition: GradeEvaluationCondition | None = Field(
        None, description="회원 등급 평가 조건"
    )
    coupons: list[GradeCoupon] | None = Field(None, description="등급 발급 쿠폰")
    description: str | None = Field(None, description="등급 설명")
    label: str | None = Field(None, description="등급명")
    used: bool | None = Field(None, description="등급 사용 여부")
    reserve_benefit: GradeReserveBenefit | None = Field(None, description="적립금 혜택")


class Mall(BaseDto):
    """쇼핑몰 정보."""

    global_mall_hierarchy: GlobalMallHierarchy | None = Field(
        None, description="글로벌 몰 메인-서브 관계"
    )
    godo_sno: str | None = Field(None, description="커머스 상점번호")
    mall_name: str | None = Field(None, description="쇼핑몰명")
    created_date_time: str | None = Field(None, description="쇼핑몰 생성일")
    grades: list[MallGrade] | None = Field(None, description="등급")
    url: MallUrl | None = Field(None, description="접속 URL")
    global_sub_mall_summaries: list[GlobalSubMallSummary] | None = Field(
        None, description="글로벌 서브몰 요약 정보 리스트"
    )
    intro_redirection: IntroRedirection | None = Field(
        None, description="인트로 페이지 설정정보"
    )
    global_mall_type: str | None = Field(None, description="글로벌 몰 타입")
    country_code: str | None = Field(None, description="쇼핑몰 서비스 국가")
    service_center: ServiceCenter | None = Field(None, description="서비스센터 정보")
    mall_no: int | None = Field(None, description="몰번호")
    escrow_logo: EscrowLogo | None = Field(None, description="에스크로 로고정보")


# ---------- 코드/타입 목록 ----------
class InquiryType(BaseDto):
    """1:1문의 유형."""

    inquiry_type_description: str | None = Field(None, description="1:1문의 유형 설명")
    inquiry_type_no: int | None = Field(None, description="1:1문의 유형 번호")
    inquiry_type_name: str | None = Field(None, description="1:1문의 유형 이름")


class LabelValue(BaseDto):
    """label/value 형태의 코드 항목.

    productInquiryType / productReviewReportType / claimReasonType /
    claimStatusType / orderStatusType 등 공통 형태.
    """

    label: str | None = Field(None, description="명칭")
    value: str | None = Field(None, description="값")


class BankType(BaseDto):
    """은행 목록 항목."""

    kcp_code: str | None = Field(None, description="KCP 은행 관리코드")
    code: str | None = Field(None, description="은행 코드")
    name: str | None = Field(None, description="은행명")
    value: str | None = Field(None, description="은행 영문 관리명")


class BankAccountInfo(BaseDto):
    """쇼핑몰 계좌 정보."""

    bank_account: str | None = Field(None, description="계좌번호")
    bank_depositor_name: str | None = Field(None, description="예금주명")
    bank: str | None = Field(None, description="은행코드")
    bank_name: str | None = Field(None, description="은행명")


# ---------- 회원 가입/인증 설정 ----------
class MemberJoinConfig(BaseDto):
    """회원 가입 설정 (각 필드 USED/REQUIRED/NOT_USED)."""

    email_agreement: str | None = Field(None, description="email 동의 필수 여부")
    birthday: str | None = Field(None, description="생년월일 필수 여부")
    password: str | None = Field(None, description="비밀번호 필수 여부")
    address: str | None = Field(None, description="주소 필수 여부")
    sms_agreement: str | None = Field(None, description="SMS 동의 필수 여부")
    sex: str | None = Field(None, description="성별 필수 여부")
    nickname: str | None = Field(None, description="닉네임 필수 여부")
    member_name: str | None = Field(None, description="회원명 필수 여부")
    mobile_no: str | None = Field(None, description="휴대전화번호 필수 여부")
    phone_no: str | None = Field(None, description="전화번호 필수 여부")
    email: str | None = Field(None, description="이메일 필수 여부")
    member_id: str | None = Field(None, description="아이디 필수 여부")


class MallJoinConfig(BaseDto):
    """쇼핑몰 회원 인증 수단."""

    authentication_type: str | None = Field(None, description="쇼핑몰 회원 인증 수단")
    authentication_time_type: str | None = Field(
        None, description="쇼핑몰 회원 인증 시점"
    )


class OpenIdJoinConfig(BaseDto):
    """오픈아이디 설정 정보."""

    authentication_type: str | None = Field(None, description="오픈아이디 회원인증 수단")
    authentication_time_type: str | None = Field(
        None, description="오픈아이디 회원인증 시점"
    )
    providers: list[str] | None = Field(None, description="지원하는 오픈아이디")


# ---------- 적립금 설정 ----------
class ReviewsAccumulationDetail(BaseDto):
    """상품평 적립금 상세."""

    photo_reviews_accumulation: float | None = Field(
        None, description="포토 상품평 적립금"
    )
    photo_reviews_length: int | None = Field(None, description="포토 상품평 글자수")
    reviews_length: int | None = Field(None, description="상품평 글자수")
    reviews_accumulation: float | None = Field(None, description="상품평 적립금")


class AccumulationConfig(BaseDto):
    """적립금 설정."""

    use_expire_notification: bool | None = Field(
        None, description="적립금 만료 알림 사용여부"
    )
    accumulation_unit: str | None = Field(None, description="적립금 단위")
    limit_max_rate: bool | None = Field(
        None, description="적립금 사용 최대 적립금 제한 여부"
    )
    accumulation_use_min_price: float | None = Field(
        None, description="적립금 사용 최소 적립금"
    )
    use_product_accumulation: bool | None = Field(None, description="상품 적립 사용여부")
    limit_min_price: bool | None = Field(
        None, description="적립금 사용 최소 적립금 제한 여부"
    )
    accumulation_use_min_product_price: float | None = Field(
        None, description="적립금 사용 최소 상품금액"
    )
    sign_up_accumulation: float | None = Field(None, description="회원가입 적립금")
    use_reviews_accumulation: bool | None = Field(
        None, description="상품평 적립금 사용여부"
    )
    product_accumulation_basis_type: str | None = Field(
        None, description="상품 금액 기준 설정"
    )
    accumulation_name: str | None = Field(None, description="적립금명")
    use_sign_up_accumulation: bool | None = Field(
        None, description="회원가입 적립금 사용여부"
    )
    admin_memo: str | None = Field(None, description="운영자 메모")
    accumulation_give_point: str | None = Field(None, description="적립금 지급 시점")
    accumulation_rate: float | None = Field(None, description="적립금 기본 적립률")
    limit_min_product_price: bool | None = Field(
        None, description="적립금 사용 최소 상품금액 제한 여부"
    )
    accumulation_display_format_type: str | None = Field(
        None, description="적립금 노출 설정"
    )
    reviews_accumulation_detail: ReviewsAccumulationDetail | None = Field(
        None, description="상품평 적립금 상세"
    )
    expire_notification_point: int | None = Field(
        None, description="적립금 만료 알림 시점 (day)"
    )
    accumulation_valid_period: int | None = Field(
        None, description="적립금 유효기간 (month)"
    )
    use_birthday_accumulation: bool | None = Field(
        None, description="생일 적립금 사용 여부"
    )
    excluding_reserve_pay_accumulation: bool | None = Field(
        None, description="적립금 결제시 적립금 지급 제외여부"
    )
    accumulation_use_max_rate: float | None = Field(
        None, description="적립금 사용 최대비율"
    )
    birthday_accumulation: float | None = Field(
        None, description="생일 적립금 지급 금액"
    )
    excluding_reserve_pay_coupon: bool | None = Field(
        None, description="쿠폰할인 결제시 적립금 지급 제외여부"
    )
    use_member_accumulation: bool | None = Field(None, description="회원 적립 사용여부")


# ---------- 기타 설정 ----------
class CartConfig(BaseDto):
    """장바구니 설정."""

    storage_period: int | None = Field(None, description="최대 보관 일수")
    cart_equivalent_option_unit_type: str | None = Field(
        None, description="장바구니 상품 추가 타입 (QUANTITY/ROW)"
    )
    storage_period_no_limit: bool | None = Field(None, description="무제한 보관 설정")
    storage_max_quantity: int | None = Field(
        None, description="장바구니 보관 최대 수량"
    )


class KakaoMap(BaseDto):
    """카카오맵 설정."""

    kakao_map_longitude: str | None = Field(None, description="카카오맵 경도")
    kakao_map_latitude: str | None = Field(None, description="카카오맵 위도")
    kakao_map_key: str | None = Field(None, description="카카오맵 Appkey")


class ExternalServiceConfig(BaseDto):
    """외부 서비스 설정."""

    kakao_map: KakaoMap | None = Field(None, description="카카오맵 설정")
    google_analytics: str | None = Field(None, description="구글 통계 추적 ID")
    use_script: bool | None = Field(None, description="외부스크립트 사용여부")
    naver_webmaster: str | None = Field(None, description="네이버 웹마스터 Appkey")


class TermsConfig(BaseDto):
    """공정거래 로고 정보."""

    fair_logo_used: bool | None = Field(None, description="공정거래 로고 사용 여부")
    fair_logo_url: str | None = Field(None, description="공정거래 로고 이미지 URL")


# ---------- 카테고리 ----------
class FlatCategory(BaseDto):
    """평면 카테고리 항목 (1~5차)."""

    depth1_category_no: int | None = Field(None, description="카테고리 번호(1차)")
    depth1_label: str | None = Field(None, description="카테고리 명(1차)")
    depth1_icon: str | None = Field(None, description="카테고리 아이콘(1차)")
    depth1_content: str | None = Field(None, description="카테고리 상세 HTML(1차)")
    depth1_display_order: int | None = Field(None, description="카테고리 순서(1차)")
    depth2_category_no: int | None = Field(None, description="카테고리 번호(2차)")
    depth2_label: str | None = Field(None, description="카테고리 명(2차)")
    depth2_icon: str | None = Field(None, description="카테고리 아이콘(2차)")
    depth2_content: str | None = Field(None, description="카테고리 상세 HTML(2차)")
    depth2_display_order: int | None = Field(None, description="카테고리 순서(2차)")
    depth3_category_no: int | None = Field(None, description="카테고리 번호(3차)")
    depth3_label: str | None = Field(None, description="카테고리 명(3차)")
    depth3_icon: str | None = Field(None, description="카테고리 아이콘(3차)")
    depth3_content: str | None = Field(None, description="카테고리 상세 HTML(3차)")
    depth3_display_order: int | None = Field(None, description="카테고리 순서(3차)")
    depth4_category_no: int | None = Field(None, description="카테고리 번호(4차)")
    depth4_label: str | None = Field(None, description="카테고리 명(4차)")
    depth4_icon: str | None = Field(None, description="카테고리 아이콘(4차)")
    depth4_content: str | None = Field(None, description="카테고리 상세 HTML(4차)")
    depth4_display_order: int | None = Field(None, description="카테고리 순서(4차)")
    depth5_category_no: int | None = Field(None, description="카테고리 번호(5차)")
    depth5_label: str | None = Field(None, description="카테고리 명(5차)")
    depth5_icon: str | None = Field(None, description="카테고리 아이콘(5차)")
    depth5_content: str | None = Field(None, description="카테고리 상세 HTML(5차)")
    depth5_display_order: int | None = Field(None, description="카테고리 순서(5차)")
    full_category_name: str | None = Field(None, description="1~5차 카테고리 명")


class MultiLevelCategory(BaseDto):
    """계층형 카테고리 항목 (재귀 children).

    스펙상 최대 5단계로 self-recursive 한 children 트리.
    """

    depth: int | None = Field(None, description="뎁스")
    category_no: int | None = Field(None, description="카테고리 번호")
    label: str | None = Field(None, description="카테고리 이름")
    icon: str | None = Field(None, description="카테고리 아이콘")
    content: str | None = Field(None, description="카테고리 상세(HTML)")
    children: list["MultiLevelCategory"] | None = Field(
        None, description="하위 카테고리"
    )


class Categories(BaseDto):
    """카테고리 정보."""

    multi_level_categories: list[MultiLevelCategory] | None = Field(
        None, description="카테고리 목록(계층)"
    )
    flat_categories: list[FlatCategory] | None = Field(
        None, description="카테고리 목록(평면)"
    )


# ---------- 게시판 ----------
class BoardCategory(BaseDto):
    """게시판 카테고리 정보."""

    category_no: int | None = Field(None, description="게시판 카테고리 번호")
    label: str | None = Field(None, description="게시판 카테고리 명칭")


class BoardsCategory(BaseDto):
    """게시판 카테고리 목록 항목."""

    thumbnail_used: bool | None = Field(None, description="썸네일 이미지 사용 여부")
    replied: bool | None = Field(None, description="답글 작성 가능 여부")
    member_write: bool | None = Field(None, description="회원 작성 가능 여부")
    used: bool | None = Field(None, description="게시판 사용 여부")
    secreted: bool | None = Field(None, description="비밀글 작성 가능 여부")
    board_name: str | None = Field(None, description="게시판 이름")
    guest_write: bool | None = Field(None, description="비회원 작성 가능 여부")
    image_display_type: str | None = Field(None, description="리스트 이미지 유형")
    display_type: str | None = Field(None, description="게시판 노출 유형")
    category_used: bool | None = Field(None, description="카테고리 사용 여부")
    attachment_used: bool | None = Field(None, description="첨부파일 사용 여부")
    board_id: str | None = Field(None, description="게시판 ID")
    categories: list[BoardCategory] | None = Field(
        None, description="게시판 카테고리 정보"
    )
    board_no: int | None = Field(None, description="게시판 번호")


# ---------- 최상위 ----------
class MallResponse(BaseDto):
    """몰 정보 조회 응답 (malls1513324780)."""

    mall: Mall | None = Field(None, description="쇼핑몰 정보")
    inquiry_type: list[InquiryType] | None = Field(
        None, description="1:1문의 유형 목록"
    )
    product_inquiry_type: list[LabelValue] | None = Field(
        None, description="상품문의 유형 목록"
    )
    product_review_report_type: list[LabelValue] | None = Field(
        None, description="상품평 신고 유형 목록"
    )
    claim_reason_type: list[LabelValue] | None = Field(
        None, description="클레임 사유 목록"
    )
    claim_status_type: list[LabelValue] | None = Field(
        None, description="클레임상태 목록"
    )
    order_status_type: list[LabelValue] | None = Field(
        None, description="주문상태 목록"
    )
    bank_type: list[BankType] | None = Field(None, description="은행 목록")
    categories: Categories | None = Field(None, description="카테고리 정보")
    boards_categories: list[BoardsCategory] | None = Field(
        None, description="게시판 카테고리 목록"
    )
    service_basic_info: ServiceBasicInfoResponse | None = Field(
        None, description="쇼핑몰 기본정보"
    )
    bank_account_info: BankAccountInfo | None = Field(
        None, description="쇼핑몰 계좌 정보"
    )
    bank_account_infos: list[BankAccountInfo] | None = Field(
        None, description="쇼핑몰 계좌 정보 목록"
    )
    member_join_config: MemberJoinConfig | None = Field(
        None, description="회원 가입 설정"
    )
    accumulation_config: AccumulationConfig | None = Field(
        None, description="적립금 설정"
    )
    cart_config: CartConfig | None = Field(None, description="장바구니 설정")
    mall_join_config: MallJoinConfig | None = Field(
        None, description="쇼핑몰 회원 인증 수단"
    )
    open_id_join_config: OpenIdJoinConfig | None = Field(
        None, description="오픈아이디 설정 정보"
    )
    external_service_config: ExternalServiceConfig | None = Field(
        None, description="외부 서비스 설정"
    )
    terms_config: TermsConfig | None = Field(None, description="공정거래 로고 정보")
    instagram_used: bool | None = Field(None, description="인스타그램 사용여부")

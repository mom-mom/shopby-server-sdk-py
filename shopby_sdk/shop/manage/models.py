"""Shopby Shop(Client) Manage API 모델.

shop-api(`https://shop-api.e-ncp.com`) 의 공개(인증 불필요) manage 도메인
요청/응답 모델. 모든 모델은 ``BaseDto`` 를 상속하여 snake_case <-> camelCase
변환을 자동 처리한다.

대응 OpenAPI 스펙: ``docs/api/manage-shop-public.yml``
"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDate, KstDatetime

# =====================================================================
# Address (주소)
# =====================================================================


class AddressItem(BaseDto):
    """주소 검색 결과 항목. (schema: addresses-search511048687.items)"""

    address: str | None = Field(None, description="전체 주소")
    detail_address: str | None = Field(None, description="상세 주소")
    road_address: str | None = Field(None, description="도로명 주소")
    road_address_extra: str | None = Field(None, description="도로명 부가 정보")
    jibun_address: str | None = Field(None, description="지번 주소")
    related_jibun: str | None = Field(None, description="관련 지번")
    zip_code: str | None = Field(None, description="우편번호")
    old_zip_code: str | None = Field(None, description="구 우편번호")
    eng_address: str | None = Field(None, description="영문 주소")


class AddressSearchResponse(BaseDto):
    """주소 조회 응답. (schema: addresses-search511048687)"""

    total_count: int | None = Field(None, description="검색 결과 개수")
    group_by_states: list[Any] = Field(default_factory=list, description="시도별 그룹")
    items: list[AddressItem] = Field(default_factory=list, description="주소 목록")


class JapanAddressResponse(BaseDto):
    """일본 주소 검색 응답. (schema: addresses-search-jp484412385)"""

    zip_code: str | None = Field(None, description="우편번호 (하이픈 제거)")
    pref_code: str | None = Field(None, description="도도부현 코드 (2자리)")
    jis_code: str | None = Field(None, description="JIS 코드")
    address: str | None = Field(None, description="전체 주소")
    address_english: str | None = Field(None, description="전체 주소 (영문)")
    address_list: list[str] = Field(default_factory=list, description="복수의 주소 리스트")
    state: str | None = Field(None, description="도도부현 이름")
    city: str | None = Field(None, description="시/구/읍/면 이름")
    street_address: str | None = Field(None, description="상세 주소")


# =====================================================================
# Board (게시판)
# =====================================================================


class BoardChannelConfig(BaseDto):
    """게시판 채널 설정 (1:1문의/상품리뷰/상품문의 공통 구조).

    실데이터(dev+prod) 기반 타입화. inquiryConfig/productReviewConfig/
    productInquiryConfig 가 동일 형태를 공유한다.
    """

    name: str | None = None
    description: str | None = None
    used: bool | None = None
    display_type: str | None = Field(None, description="LIST 등")
    image_display_type: str | None = Field(None, description="ATTACHMENT 등")
    member_posting_used: bool | None = None
    guest_posting_used: bool | None = None
    secret_posting_used: bool | None = None
    reply_used: bool | None = None
    attachment_used: bool | None = None
    email_used: bool | None = None
    sms_used: bool | None = None
    answer_mail_template_used: bool | None = None
    answer_sms_template_used: bool | None = None
    review_accumulation: dict | None = Field(None, description="리뷰 적립 설정(상품리뷰 전용, 미설정 시 null)")


class BoardConfigurationsResponse(BaseDto):
    """게시판 설정 조회 응답. (schema: boards-configurations-235903281)

    boardConfigs 항목은 authorityConfig 등 깊은 권한 설정 트리를 포함하는 가변 구조라
    (실데이터에서도 비어 있어 구조 확인 불가) ``dict[str, Any]`` 로 둔다.
    inquiry/review/productInquiry config 는 공통 BoardChannelConfig 로 타입화.
    """

    board_configs: list[dict[str, Any]] = Field(default_factory=list, description="게시판 설정 목록(동적 권한 트리)")
    inquiry_config: BoardChannelConfig | None = Field(None, description="1:1문의 설정")
    product_review_config: BoardChannelConfig | None = Field(None, description="상품리뷰 설정")
    product_inquiry_config: BoardChannelConfig | None = Field(None, description="상품문의 설정")


class BoardCategory(BaseDto):
    """게시판 카테고리. (schema: boards-boardNo-categories1480073916.item)"""

    category_no: int | None = Field(None, description="카테고리 번호")
    label: str | None = Field(None, description="카테고리 명")


BoardDirection = Literal["ASC", "DESC", "RECOMMEND_COUNT", "READ_COUNT"]
"""게시글 정렬 방식."""

PostSearchType = Literal["ALL", "TITLE", "CONTENT", "WRITER"]
"""게시글 검색 유형."""

RegisterType = Literal["MEMBER", "ADMIN", "GUEST"]
"""작성자/수정자 유형."""


class PostAttachment(BaseDto):
    """게시글 첨부파일."""

    file_name: str | None = Field(None, description="원본 파일명")
    uploaded_file_name: str | None = Field(None, description="업로드 된 파일명")
    download_file_url: str | None = Field(None, description="다운로드 URL")


class ArticleListItem(BaseDto):
    """게시글 리스트 항목(v1). (schema: boards-boardNo-articles-243411769.items)

    답글 리스트(reply-posts) 응답 항목과 동일 구조를 공유한다.
    """

    article_no: int | None = Field(None, description="게시글 번호")
    title: str | None = Field(None, description="제목")
    content: str | None = Field(None, description="내용")
    image_url: str | None = Field(None, description="이미지 URL")
    view_cnt: int | None = Field(None, description="조회수")
    category_no: int | None = Field(None, description="카테고리 번호")
    category_label: str | None = Field(None, description="카테고리 명")
    register_name: str | None = Field(None, description="등록자 이름")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    register_no: int | None = Field(None, description="등록자 번호")
    register_type: str | None = Field(None, description="등록자 유형")
    modifier_name: str | None = Field(None, description="변경자 이름")
    modify_ymdt: KstDatetime | None = Field(None, description="최종 수정일")
    modifier_no: int | None = Field(None, description="변경자 번호")
    modifier_type: str | None = Field(None, description="변경자 유형")
    modifiable: bool | None = Field(None, description="수정 가능 여부")
    secreted: bool | None = Field(None, description="비밀글 여부")
    has_replies: bool | None = Field(None, description="답글 보유 여부")
    replied_cnt: int | None = Field(None, description="답글 수")
    replied: bool | None = Field(None, description="답글 여부")
    notice: bool | None = Field(None, description="공지글 여부")
    attached: bool | None = Field(None, description="첨부파일 보유 여부")
    recommend_count: int | None = Field(None, description="추천 수")
    tags: list[str] = Field(default_factory=list, description="태그")
    member_id: str | None = Field(None, description="회원 아이디")
    member_email: str | None = Field(None, description="회원 이메일")
    member_nickname: str | None = Field(None, description="회원 닉네임")
    recommended: bool | None = Field(None, description="본인 추천 여부")
    report_count: int | None = Field(None, description="신고 수")
    display_status_type: str | None = Field(None, description="노출 상태")
    reported: bool | None = Field(None, description="본인 신고 여부")


class ArticleListResponse(BaseDto):
    """게시글 리스트 조회 응답(v1). (schema: boards-boardNo-articles-243411769)

    답글 리스트 조회(reply-posts) 응답과 동일 구조.
    """

    total_count: int | None = Field(None, description="게시글 개수")
    items: list[ArticleListItem] = Field(default_factory=list, description="게시글 목록")


class ArticleDetailResponse(BaseDto):
    """게시글 상세 조회 응답(v1). (schema: boards-boardNo-articles-articleNo-1712194651)"""

    article_no: int | None = Field(None, description="게시글 번호")
    title: str | None = Field(None, description="제목")
    content: str | None = Field(None, description="내용")
    image_url: str | None = Field(None, description="이미지 URL")
    view_cnt: int | None = Field(None, description="조회수")
    category_no: int | None = Field(None, description="카테고리 번호")
    category_label: str | None = Field(None, description="카테고리 명")
    attachments: list[PostAttachment] = Field(default_factory=list, description="첨부파일")
    register_name: str | None = Field(None, description="등록자 이름")
    register_group_names: list[str] | None = Field(None, description="등록자 그룹명")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    register_no: int | None = Field(None, description="등록자 번호")
    register_type: str | None = Field(None, description="등록자 유형")
    modifier_name: str | None = Field(None, description="변경자 이름")
    modify_ymdt: KstDatetime | None = Field(None, description="최종 수정일")
    modifier_no: int | None = Field(None, description="변경자 번호")
    modifier_type: str | None = Field(None, description="변경자 유형")
    member_id: str | None = Field(None, description="회원 아이디")
    member_nickname: str | None = Field(None, description="회원 닉네임")
    modifiable: bool | None = Field(None, description="수정 가능 여부")
    child_articles: list[dict[str, Any]] = Field(
        default_factory=list, description="답글 목록(자기참조 구조라 dict 로 둠)"
    )
    secreted: bool | None = Field(None, description="비밀글 여부")
    notice: bool | None = Field(None, description="공지글 여부")
    parent_article: dict[str, Any] | None = Field(None, description="부모 게시글(자기참조 구조라 dict 로 둠)")
    recommend_count: int | None = Field(None, description="추천 수")
    tags: list[str] = Field(default_factory=list, description="태그")
    recommendable: bool | None = Field(None, description="추천 가능 여부")
    report_count: int | None = Field(None, description="신고 수")
    display_status_type: str | None = Field(None, description="노출 상태")
    reported: bool | None = Field(None, description="본인 신고 여부")


# --- v2 (posts) ---


class PostsV2SearchRequest(BaseDto):
    """게시글 리스트 조회(v2) 요청 바디. (schema: boards-posts-1512719245)

    boardNoOrId 를 null 로 보내면 몰 단위로 검색한다.
    """

    board_no_or_id: str | None = Field(None, description="게시판 번호 또는 게시판 ID")
    keyword: str | None = Field(None, description="검색어")
    search_type: PostSearchType | None = Field(None, description="검색 유형")
    category_no: int | None = Field(None, description="게시판 카테고리")
    start_ymdt: KstDatetime | None = Field(None, description="조회 시작일")
    end_ymdt: KstDatetime | None = Field(None, description="조회 종료일")
    direction: BoardDirection | None = Field(None, description="정렬 방식")
    is_mine: bool | None = Field(None, description="본인 글만 조회 여부")
    my_recommend_only: bool | None = Field(None, description="본인 추천 글만 조회 여부")
    member_nos: list[int] | None = Field(None, description="회원 번호 리스트")
    post_search_tags: list[str] | None = Field(None, description="게시글 검색용 태그")
    my_scraped_only: bool | None = Field(None, description="본인 스크랩 글만 조회 여부")
    member_group_no: int | None = Field(None, description="회원 그룹 번호")
    is_noticed: bool | None = Field(None, description="공지글 조회 여부")
    skip_blinded: bool | None = Field(None, description="차단 게시글 제외 여부")
    is_secreted: bool | None = Field(None, description="비밀글 조회 여부")


class PostListItem(BaseDto):
    """게시글 리스트 항목(v2). (schema: boards-posts-1521194508.items)

    답글 리스트 조회(v2) 응답 항목과 동일 구조.
    """

    board_no: int | None = Field(None, description="게시판 번호")
    post_no: int | None = Field(None, description="게시글 번호")
    title: str | None = Field(None, description="제목")
    image_url: str | None = Field(None, description="이미지 URL")
    category_no: int | None = Field(None, description="카테고리 번호")
    category_label: str | None = Field(None, description="카테고리 명")
    register_no: int | None = Field(None, description="등록자 번호")
    register_name: str | None = Field(None, description="등록자 이름")
    register_type: str | None = Field(None, description="등록자 유형")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    modifier_no: int | None = Field(None, description="변경자 번호")
    modifier_name: str | None = Field(None, description="변경자 이름")
    modifier_type: str | None = Field(None, description="변경자 유형")
    modify_ymdt: KstDatetime | None = Field(None, description="최종 수정일")
    modifiable: bool | None = Field(None, description="수정 가능 여부")
    secreted: bool | None = Field(None, description="비밀글 여부")
    noticed: bool | None = Field(None, description="공지글 여부")
    recommended: bool | None = Field(None, description="본인 추천 여부")
    scraped: bool | None = Field(None, description="본인 스크랩 여부")
    reported: bool | None = Field(None, description="본인 신고 여부")
    attached: bool | None = Field(None, description="첨부파일 보유 여부")
    view_cnt: int | None = Field(None, description="조회수")
    recommended_cnt: int | None = Field(None, description="추천 수")
    reported_cnt: int | None = Field(None, description="신고 수")
    replied_cnt: int | None = Field(None, description="답글 수")
    tags: list[str] = Field(default_factory=list, description="태그")
    post_search_tags: list[str] = Field(default_factory=list, description="게시글 검색용 태그")
    display_status_type: str | None = Field(None, description="노출 상태")
    member_group_no: int | None = Field(None, description="회원 그룹 번호")


class PostListResponse(BaseDto):
    """게시글 리스트 조회(v2) 응답. (schema: boards-posts-1521194508)

    답글 리스트 조회(v2) 응답과 동일 구조.
    """

    total_count: int | None = Field(None, description="게시글 개수")
    items: list[PostListItem] = Field(default_factory=list, description="게시글 목록")


class PostDetailResponse(BaseDto):
    """게시글 상세 조회(v2) 응답. (schema: boards-boardNo-posts-postNo1178914698)"""

    post_no: int | None = Field(None, description="게시글 번호")
    title: str | None = Field(None, description="제목")
    content: str | None = Field(None, description="내용")
    image_url: str | None = Field(None, description="이미지 URL")
    category_no: int | None = Field(None, description="카테고리 번호")
    category_label: str | None = Field(None, description="카테고리 명")
    register_name: str | None = Field(None, description="등록자 이름")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    register_no: int | None = Field(None, description="등록자 번호")
    register_type: str | None = Field(None, description="등록자 유형")
    modifier_name: str | None = Field(None, description="변경자 이름")
    modify_ymdt: KstDatetime | None = Field(None, description="최종 수정일")
    modifier_no: int | None = Field(None, description="변경자 번호")
    modifier_type: str | None = Field(None, description="변경자 유형")
    modifiable: bool | None = Field(None, description="수정 가능 여부")
    secreted: bool | None = Field(None, description="비밀글 여부")
    noticed: bool | None = Field(None, description="공지글 여부")
    recommended: bool | None = Field(None, description="본인 추천 여부")
    scraped: bool | None = Field(None, description="본인 스크랩 여부")
    reported: bool | None = Field(None, description="본인 신고 여부")
    reply_enabled: bool | None = Field(None, description="답글 가능 여부")
    view_cnt: int | None = Field(None, description="조회수")
    recommended_cnt: int | None = Field(None, description="추천 수")
    reported_cnt: int | None = Field(None, description="신고 수")
    replied_cnt: int | None = Field(None, description="답글 수")
    member_group_no: int | None = Field(None, description="회원 그룹 번호")
    display_status_type: str | None = Field(None, description="노출 상태")
    tags: list[str] = Field(default_factory=list, description="태그")
    post_search_tags: list[str] = Field(default_factory=list, description="게시글 검색용 태그")
    attachments: list[PostAttachment] = Field(default_factory=list, description="첨부파일")
    parent_article: dict[str, Any] | None = Field(None, description="부모 게시글(자기참조 구조라 dict 로 둠)")


class PostPreviewsRequest(BaseDto):
    """게시글 프리뷰 목록 조회 요청 바디. (schema: boards-boardNo-posts-previews-842616877)"""

    post_nos: list[int] = Field(..., description="조회할 게시글 번호 목록 (1~100개)")
    direction: BoardDirection | None = Field(None, description="정렬 방식")
    skip_blinded: bool | None = Field(None, description="블라인드 게시글 제외 여부")
    is_secreted: bool | None = Field(None, description="비밀글 필터링 여부")


class PostPreviewItem(BaseDto):
    """게시글 프리뷰 항목. (schema: boards-boardNo-posts-previews-2042741042.item)"""

    board_no: int | None = Field(None, description="게시판 번호")
    post_no: int | None = Field(None, description="게시글 번호")
    title: str | None = Field(None, description="제목")
    content: str | None = Field(None, description="내용 미리보기 (최대 3000자)")
    register_no: int | None = Field(None, description="작성자 번호")
    register_name: str | None = Field(None, description="작성자 이름")
    register_type: str | None = Field(None, description="작성자 유형")
    register_ymdt: KstDatetime | None = Field(None, description="등록일")
    image_url: str | None = Field(None, description="썸네일 URL")
    secreted: bool | None = Field(None, description="비밀글 여부")
    noticed: bool | None = Field(None, description="공지글 여부")
    display_status_type: str | None = Field(None, description="노출 상태")


# =====================================================================
# Holiday (공휴일)
# =====================================================================
# 응답은 해당 월의 공휴일 '일자(day)' 정수 배열 (예: [5, 6, 12, ...]).
# 모델 없이 list[int] 로 직접 처리한다.


# =====================================================================
# Inquiry (1:1 문의)
# =====================================================================
# 1:1문의 설정(configurations) 응답은 공통 board 설정 스키마와 동일하며
# 필드가 명확해 타입화한다.

InquiryDisplayType = Literal["LIST", "GALLERY"]
InquiryImageDisplayType = Literal["NOT_USED", "ATTACHMENT", "CONTENT"]


class InquiryConfigurationResponse(BaseDto):
    """1:1 문의 설정 조회 응답. (schema: inquiries-configurations-1948302739)"""

    display_type: str | None = Field(None, description="노출 형태")
    image_display_type: str | None = Field(None, description="이미지 노출 형태")
    used: bool | None = Field(None, description="사용 여부")
    name: str | None = Field(None, description="게시판 이름")
    description: str | None = Field(None, description="설명")
    member_posting_used: bool | None = Field(None, description="회원 글쓰기 사용 여부")
    guest_posting_used: bool | None = Field(None, description="비회원 글쓰기 사용 여부")
    secret_posting_used: bool | None = Field(None, description="비밀글 사용 여부")
    reply_used: bool | None = Field(None, description="답글 사용 여부")
    attachment_used: bool | None = Field(None, description="첨부파일 사용 여부")
    sms_used: bool | None = Field(None, description="SMS 사용 여부")
    email_used: bool | None = Field(None, description="이메일 사용 여부")
    answer_sms_template_used: bool | None = Field(None, description="답변 SMS 템플릿 사용 여부")
    answer_mail_template_used: bool | None = Field(None, description="답변 메일 템플릿 사용 여부")


class InquiryType(BaseDto):
    """1:1 문의 유형. (schema: inquiries-types1184079569.item)"""

    inquiry_type_no: int | None = Field(None, description="문의 유형 번호")
    inquiry_type_name: str | None = Field(None, description="문의 유형 이름")
    inquiry_type_description: str | None = Field(None, description="문의 유형 설명")
    display_order: int | None = Field(None, description="노출 순서")


InquiryTypeDirection = Literal["ADMIN", "CREATED_ASC", "CREATED_DESC"]
"""1:1 문의 유형 정렬 방식."""


# =====================================================================
# Instagram
# =====================================================================
# 응답 필드들은 인스타그램 외부 API 원형 키(snake_case)이며,
# BaseDto 의 alias_generator(camelCase) 와 충돌하므로 별칭을 명시 지정한다.


class InstagramMediaItem(BaseDto):
    """instagram 미디어 항목. (schema: shopby-instagram-media-1224771635.data)"""

    media_url: str | None = Field(None, alias="media_url", description="미디어 URL")
    permalink: str | None = Field(None, description="영구 링크")
    thumbnail_url: str | None = Field(None, alias="thumbnail_url", description="썸네일 URL")
    media_type: str | None = Field(None, alias="media_type", description="미디어 유형")
    username: str | None = Field(None, description="사용자명")


class InstagramError(BaseDto):
    """instagram 조회 에러 정보."""

    message: str | None = Field(None, description="에러 메시지")
    type: str | None = Field(None, description="에러 유형")
    code: int | None = Field(None, description="에러 코드")
    fbtrace_id: str | None = Field(None, alias="fbtrace_id", description="페이스북 트레이스 ID")


class InstagramMediaResponse(BaseDto):
    """instagram 피드 조회 응답. (schema: shopby-instagram-media-1224771635)"""

    data: list[InstagramMediaItem] = Field(default_factory=list, description="미디어 목록")
    error: InstagramError | None = Field(None, description="에러 정보")


# =====================================================================
# Page (외부 스크립트)
# =====================================================================


class ExternalScriptItem(BaseDto):
    """외부 스크립트 항목. (schema: page-scripts-1027721416.item)"""

    page_type: str | None = Field(None, description="페이지 타입")
    device_type: str | None = Field(None, description="기기 타입 (PC, MOBILE)")
    content: str | None = Field(None, description="스크립트")
    page_type_label: str | None = Field(None, description="페이지 타입 라벨")


# =====================================================================
# Terms (약관)
# =====================================================================

TermsType = Literal[
    "MALL_INTRODUCTION",
    "USE",
    "E_COMMERCE",
    "PI_PROCESS",
    "PI_COLLECTION_AND_USE_REQUIRED",
    "PI_COLLECTION_AND_USE_OPTIONAL",
    "PI_PROCESS_CONSIGNMENT",
    "PI_THIRD_PARTY_PROVISION",
    "PI_COLLECTION_AND_USE_FOR_GUEST_ON_ARTICLE",
    "ACCESS_GUIDE",
    "WITHDRAWAL_GUIDE",
    "PI_SELLER_PROVISION",
    "PI_COLLECTION_AND_USE_ON_ORDER",
    "ORDER_INFO_AGREE",
    "CLEARANCE_INFO_COLLECTION_AND_USE",
    "TRANSFER_AGREE",
    "REGULAR_PAYMENT_USE",
    "AUTO_APPROVAL_USE",
    "PI_LIQUOR_PURCHASE_PROVISION",
    "PI_RESTOCK_NOTICE",
    "PI_14_AGE",
    "PI_GIFT_ACCEPT_COLLECTION_AND_USE",
    "MARKETING_RECEIVE",
    "MARKETING_INFO_USAGE",
]
"""몰 약관 타입."""

CustomTermsCategoryType = Literal["MEMBER", "ORDER"]
"""추가 약관 카테고리 유형."""


class TermsContents(BaseDto):
    """약관 본문 정보. (terms 응답 map 의 value)"""

    used: bool | None = Field(None, description="사용 여부")
    contents: str | None = Field(None, description="약관 본문")
    enforcement_date: KstDate | None = Field(None, description="시행일")


# search-used-terms / post-search-used-terms 응답은
# {약관타입: TermsContents} 형태의 동적 맵이라 dict 로 다룬다.
UsedTermsResponse = dict[str, TermsContents]
"""적용 중인 몰 약관 조회 응답 (약관타입 -> 약관 본문 맵). schema: terms760268445"""


class PostUsedTermsRequest(BaseDto):
    """적용 중인 몰 약관 조회(ver1.1) 요청 바디. (schema: terms1127550579)"""

    terms_type: list[TermsType] | None = Field(None, description="조회할 약관 타입 리스트")
    replacement_phrase: dict[str, str] = Field(..., description="약관 대체 문구 (key-value 맵)")
    used_only: bool = Field(False, description="사용 중인 약관만 조회 여부")


class CustomTermsRequest(BaseDto):
    """추가 약관 조회 요청 바디. (schema: terms-custom-2059627526)"""

    custom_category_type: CustomTermsCategoryType = Field(..., description="약관 카테고리 유형 (MEMBER, ORDER)")
    replacement_phrase: dict[str, str] = Field(..., description="약관 대체 문구 (key-value 맵)")


class CustomTermsItem(BaseDto):
    """추가 약관 항목. (schema: terms-custom-760871651.item)"""

    no: int | None = Field(None, description="추가 약관 번호")
    terms_name: str | None = Field(None, description="항목명")
    terms_name_eng: str | None = Field(None, description="항목명 (영문)")
    used: bool | None = Field(None, description="사용 여부")
    required: bool | None = Field(None, description="필수 여부")
    contents: str | None = Field(None, description="약관 본문")


class TermsHistoryItem(BaseDto):
    """약관 변경이력 항목. (schema: terms-history1546003657.item)"""

    terms_no: int | None = Field(None, description="약관 번호")
    enforcement_date: KstDate | None = Field(None, description="시행일")
    terms_enforcement_status_label: str | None = Field(None, description="시행 상태 라벨")


class UsedTermsTypesResponse(BaseDto):
    """적용 중인 몰 약관 타입 조회 응답. (schema: terms-used912144132)"""

    terms_list: list[str] = Field(default_factory=list, description="적용 중인 약관 타입 리스트")


class TermsDetailResponse(BaseDto):
    """약관 상세 조회 응답. (schema: terms-termsNo1628412078)"""

    used: bool | None = Field(None, description="사용 여부")
    contents: str | None = Field(None, description="약관 본문")
    enforcement_date: str | None = Field(None, description="시행일")


class PostTermsDetailRequest(BaseDto):
    """약관 상세 조회(ver1.1) 요청 바디. (schema: terms-termsNo486549215)

    스펙상 빈 object 이며, 치환하고 싶은 문구를 replacementPhrase 에
    [key:value] 형태로 전달한다.
    """

    replacement_phrase: dict[str, str] | None = Field(None, description="약관 대체 문구 (key-value 맵)")

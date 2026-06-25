"""기획전/이벤트(Event) 모델."""

from __future__ import annotations

from typing import Any

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime
from shopby_sdk.shop.product.models.catalog_item import ShopProductItem


class EventSummary(BaseDto):
    """기획전/이벤트 요약 (목록/검색 공통 item)."""

    event_no: int | None = None
    id: str | None = None
    label: str | None = None
    tag: str | None = None
    promotion_text: str | None = None
    url: str | None = None
    url_type: str | None = None
    pc_image_url: str | None = None
    mobileimage_url: str | None = None
    event_yn: str | None = None
    progress_status: str | None = None
    display_period_type: str | None = None
    start_ymdt: KstDatetime | None = None
    end_ymdt: KstDatetime | None = None


class EventListResponse(BaseDto):
    """이벤트 목록 조회 응답 (schema: display-events-1184885934).

    참고: 스펙상 익명 배열 키 ``[]`` 도 존재하나 실데이터는 ``contents`` 를 사용한다.
    """

    contents: list[EventSummary] | None = None
    total_page: int | None = None
    total_count: int | None = None


class ClosedEventListResponse(BaseDto):
    """종료된 이벤트 목록 응답 (schema: display-events-close1639109920)."""

    total_count: int | None = None
    items: list[EventSummary] | None = None


class EventSectionSummary(BaseDto):
    """기획전 섹션 요약 (display-events-sections / 섹션 목록)."""

    event_no: int | None = None
    section_no: int | None = None
    label: str | None = None
    image_url: str | None = None
    display_order: int | None = None
    pc_per_row: int | None = None
    mobile_per_row: int | None = None


class EventSectionsByEventNo(BaseDto):
    """기획전 번호별 섹션 목록 (schema: display-events-sections-345681802[])."""

    event_no: int | None = None
    sections: list[EventSectionSummary] | None = None


class EventWithProducts(BaseDto):
    """기획전 + 대표 상품 목록 (schema: display-events-search-by-nos-823985503[]).

    products[] 는 product 도메인과 공유하는 상품 카탈로그 표현(ShopProductItem).
    """

    event: EventSummary | None = None
    products: list[ShopProductItem] | None = None


class EventCouponSummary(BaseDto):
    """기획전 발급 쿠폰 묶음 (event detail coupon).

    coupons[] 의 개별 쿠폰은 사용/발급 제약 등 깊게 중첩된 구조라 ``dict[str, Any]`` 로 둔다.
    """

    coupons: list[dict[str, Any]] | None = None
    before_issue_image_url: str | None = None
    already_issued_image_url: str | None = None
    issued_image_url: str | None = None
    sold_out_image_url: str | None = None
    date_expired_image_url: str | None = None
    guide_image_url: str | None = None


class EventDetailSection(BaseDto):
    """기획전 상세 내 섹션.

    products[] 는 product 도메인과 공유하는 상품 카탈로그 표현(ShopProductItem).
    """

    section_no: int | None = None
    label: str | None = None
    image_url: str | None = None
    display_order: int | None = None
    pc_per_row: int | None = None
    mobile_per_row: int | None = None
    displayable_stock: bool | None = None
    products: list[ShopProductItem] | None = None


class EventDetailResponse(BaseDto):
    """기획전 상세 조회 응답 (schema: display-events-eventNo / eventKey / ids-eventId).

    ``top`` / ``orders`` / ``categoryNos`` 등 부가 필드는 가변적이라 느슨하게 둔다.
    """

    event_no: int | None = None
    id: str | None = None
    label: str | None = None
    tag: str | None = None
    promotion_text: str | None = None
    url: str | None = None
    url_type: str | None = None
    pc_image_url: str | None = None
    mobileimage_url: str | None = None
    event_yn: str | None = None
    display_period_type: str | None = None
    start_ymdt: KstDatetime | None = None
    end_ymdt: KstDatetime | None = None
    top: Any | None = None
    orders: Any | None = None
    category_nos: Any | None = None
    coupon: EventCouponSummary | None = None
    section: list[EventDetailSection] | None = None


class EventSectionProductsResponse(BaseDto):
    """기획전 상품진열 상품 조회 응답 (schema: display-events-eventNo-sections-sectionNo).

    products[] 는 product 도메인과 공유하는 상품 카탈로그 표현(ShopProductItem).
    """

    section_no: int | None = None
    total_count: int | None = None
    products: list[ShopProductItem] | None = None

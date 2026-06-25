"""display shop API 클라이언트.

shop-api(`https://shop-api.e-ncp.com`) 의 전시(display) 공개(익명) 엔드포인트를 다룬다.
회원 인증(accessToken / Shop-By-Authorization)은 전송하지 않는다.
"""

from __future__ import annotations

import httpx

from shopby_sdk.shop.base import ShopbyShopApiClient
from shopby_sdk.shop.display.models import (
    BannerExtraInfo,
    BannerSection,
    CategoriesResponse,
    CategoryDisplaySetting,
    CategoryNoByCode,
    CategoryNosByCodesRequest,
    CategoryProductReviewsResponse,
    CategoryResponse,
    ClosedEventListResponse,
    DesignPopup,
    DesignPopupRequest,
    EventDetailResponse,
    EventSectionProductsResponse,
    EventSectionsByEventNo,
    EventSummary,
    EventWithProducts,
    InquiriesResponse,
    InquiryConfigurations,
    InquiryTagsResponse,
    PhotoReviewsResponse,
    Popup,
    ProductInquiriesResponse,
    ProductInquiry,
    ProductReview,
    ProductReviewsResponse,
    ReviewBoardResponse,
    ReviewCommentsResponse,
    ReviewConfigurations,
    ReviewedProductsResponse,
    ReviewTagsResponse,
    SectionListResponse,
    SectionProductsResponse,
    SectionResponse,
    SimpleCategory,
    SkinBannerGroup,
    SkinBannerGroupsBySkin,
    Sticker,
)


class ShopbyShopDisplayApiClient(ShopbyShopApiClient):
    """Shopby Shop(Client) Display API 클라이언트."""

    # ------------------------------------------------------------------
    #  Banner
    # ------------------------------------------------------------------
    async def get_banner_extra_infos(
        self,
        *,
        banner_section_no: int | None = None,
        banner_nos: str | None = None,
    ) -> list[BannerExtraInfo]:
        """배너 추가 정보 조회하기 (Version 1.0).

        Args:
            banner_section_no: 배너 섹션 번호.
            banner_nos: 배너 번호 리스트(쉼표로 구분).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {}
            if banner_section_no is not None:
                params["bannerSectionNo"] = banner_section_no
            if banner_nos is not None:
                params["bannerNos"] = banner_nos
            resp = await client.get("/display/banners/extraInfos", headers=headers, params=params)
            return self.handle_resp(resp, list[BannerExtraInfo])

    async def get_banners_with_ids(self, banner_section_ids: str) -> list[BannerSection]:
        """배너 목록 조회하기(ID) (Version 1.0).

        Args:
            banner_section_ids: 배너 섹션 ID(","로 구분한 배열).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/display/banners/id/{banner_section_ids}", headers=headers)
            return self.handle_resp(resp, list[BannerSection])

    async def get_banners(self, banner_section_codes: str) -> list[BannerSection]:
        """배너 목록 조회하기(Code) (Version 1.0).

        Args:
            banner_section_codes: 배너 섹션 코드(","로 구분한 배열).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/display/banners/{banner_section_codes}", headers=headers)
            return self.handle_resp(resp, list[BannerSection])

    # ------------------------------------------------------------------
    #  Category
    # ------------------------------------------------------------------
    async def get_categories_by_keyword(
        self,
        *,
        keyword: str | None = None,
        category_view_type: str | None = None,
    ) -> CategoriesResponse:
        """전체 카테고리 조회하기 (Version 1.0).

        Args:
            keyword: 카테고리명.
            category_view_type: 응답 형식 (ALL/MULTI_LEVEL/FLAT).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {}
            if keyword is not None:
                params["keyword"] = keyword
            if category_view_type is not None:
                params["categoryViewType"] = category_view_type
            resp = await client.get("/categories", headers=headers, params=params)
            return self.handle_resp(resp, CategoriesResponse)

    async def get_new_product_categories(self) -> list[int]:
        """신상품이 있는 카테고리 조회하기 (Version 1.0).

        판매 시작일이 1주일 이내인 상품이 존재하는 카테고리 번호 목록.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/categories/new-product-categories", headers=headers)
            return self.handle_resp(resp, list[int])

    async def get_categories_simple_1depth(self) -> list[SimpleCategory]:
        """1차 카테고리 간단 정보 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/categories/simple-1depth", headers=headers)
            return self.handle_resp(resp, list[SimpleCategory])

    async def get_category(
        self,
        category_no: int,
        *,
        needs_brands: bool | None = None,
        category_view_type: str | None = None,
    ) -> CategoryResponse:
        """카테고리 조회하기 (Version 1.0).

        Args:
            category_no: 카테고리 번호.
            needs_brands: 브랜드 정보 조회 여부 (default: true).
            category_view_type: 응답 형식 (ALL/MULTI_LEVEL/FLAT).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | bool] = {}
            if needs_brands is not None:
                params["needsBrands"] = needs_brands
            if category_view_type is not None:
                params["categoryViewType"] = category_view_type
            resp = await client.get(f"/categories/{category_no}", headers=headers, params=params)
            return self.handle_resp(resp, CategoryResponse)

    async def get_category_display_setting(self, category_no: int) -> CategoryDisplaySetting:
        """카테고리 진열 설정 조회하기 (Version 1.0).

        Args:
            category_no: 카테고리 번호.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/categories/{category_no}/display-setting", headers=headers)
            return self.handle_resp(resp, CategoryDisplaySetting)

    async def get_category_nos_by_codes(
        self, request: CategoryNosByCodesRequest
    ) -> list[CategoryNoByCode]:
        """관리코드로 카테고리 번호를 조회하기 (Version 1.0).

        Args:
            request: 전시카테고리 관리코드 목록.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post(
                "/categories/search-by-management-code", headers=headers, json=body
            )
            return self.handle_resp(resp, list[CategoryNoByCode])

    # ------------------------------------------------------------------
    #  Event
    # ------------------------------------------------------------------
    async def get_events(
        self,
        *,
        page_number: int,
        page_size: int,
        keyword: str | None = None,
        category_nos: int | None = None,
        keyword_info_type: str | None = None,
        keyword_info_value: str | None = None,
        event_yn: str | None = None,
        progress_status: str | None = None,
        order_by: str | None = None,
        order_direction: str | None = None,
    ) -> list[EventSummary]:
        """이벤트 기간안에 포함된 모든 이벤트 목록 조회하기 (Version 1.0).

        응답은 EventSummary 의 top-level 배열이다(실데이터 dev+prod 확인).

        Args:
            page_number: 페이지 번호.
            page_size: 한 페이지당 노출 수.
            keyword: 검색어(태그 명).
            category_nos: 전시 카테고리 번호.
            keyword_info_type: 검색어 타입 (NO/NAME/TAG).
            keyword_info_value: 검색어 값.
            event_yn: 이벤트 여부 (Y/N).
            progress_status: 진행상태 (ING/READY/END).
            order_by: 정렬 조건.
            order_direction: 정렬 방식 (DESC/ASC).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {
                "page.number": page_number,
                "page.size": page_size,
            }
            if keyword is not None:
                params["keyword"] = keyword
            if category_nos is not None:
                params["categoryNos"] = category_nos
            if keyword_info_type is not None:
                params["keywordInfo.type"] = keyword_info_type
            if keyword_info_value is not None:
                params["keywordInfo.value"] = keyword_info_value
            if event_yn is not None:
                params["eventYn"] = event_yn
            if progress_status is not None:
                params["progressStatus"] = progress_status
            if order_by is not None:
                params["order.by"] = order_by
            if order_direction is not None:
                params["order.direction"] = order_direction
            resp = await client.get("/display/events", headers=headers, params=params)
            return self.handle_resp(resp, list[EventSummary])

    async def get_closed_events(
        self,
        *,
        keyword: str | None = None,
        event_title: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        has_total_count: bool | None = None,
    ) -> ClosedEventListResponse:
        """종료된 모든 이벤트 목록 조회하기 (Version 1.0).

        Args:
            keyword: 태그 검색.
            event_title: 이벤트명 검색.
            page_number: 페이지 번호 (default 1).
            page_size: 한 페이지당 노출 수 (default 10).
            has_total_count: 목록 카운트 여부 (default false).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if keyword is not None:
                params["keyword"] = keyword
            if event_title is not None:
                params["eventTitle"] = event_title
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size
            if has_total_count is not None:
                params["hasTotalCount"] = has_total_count
            resp = await client.get("/display/events/close", headers=headers, params=params)
            return self.handle_resp(resp, ClosedEventListResponse)

    async def get_event_by_id(
        self,
        event_id: str,
        *,
        include_non_member_coupon: bool | None = None,
        preview: bool | None = None,
        order: str | None = None,
        soldout: bool | None = None,
        sale_status: str | None = None,
        has_product_detail: bool | None = None,
    ) -> EventDetailResponse:
        """기획전 ID로 상세 조회하기 v2.0 (Version 2.0).

        Args:
            event_id: 기획전 ID.
            include_non_member_coupon: 비로그인 발급가능 쿠폰 노출 (default false).
            preview: 미리보기 여부 (default false).
            order: 정렬 조건.
            soldout: 품절 상품 포함 여부 (default false).
            sale_status: 판매 상태.
            has_product_detail: 상품정보 포함 여부.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "2.0"}
            params: dict[str, str | bool] = {}
            if include_non_member_coupon is not None:
                params["includeNonMemberCoupon"] = include_non_member_coupon
            if preview is not None:
                params["preview"] = preview
            if order is not None:
                params["order"] = order
            if soldout is not None:
                params["soldout"] = soldout
            if sale_status is not None:
                params["saleStatus"] = sale_status
            if has_product_detail is not None:
                params["hasProductDetail"] = has_product_detail
            resp = await client.get(
                f"/display/events/ids/{event_id}", headers=headers, params=params
            )
            return self.handle_resp(resp, EventDetailResponse)

    async def get_events_by_product_nos(
        self,
        *,
        product_nos: str,
        category_nos: int | None = None,
    ) -> list[EventSummary]:
        """다수의 상품 번호로 이벤트 목록 조회하기 (Version 1.0).

        Args:
            product_nos: 상품 번호(",")로 구분.
            category_nos: 전시 카테고리 번호.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {"productNos": product_nos}
            if category_nos is not None:
                params["categoryNos"] = category_nos
            resp = await client.get("/display/events/products", headers=headers, params=params)
            return self.handle_resp(resp, list[EventSummary])

    async def get_events_by_product_no(self, product_no: int) -> list[EventSummary]:
        """특정 상품을 포함하는 이벤트 목록 조회하기 (Version 1.0).

        Args:
            product_no: 상품 번호.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/display/events/products/{product_no}", headers=headers)
            return self.handle_resp(resp, list[EventSummary])

    async def get_event_by_name(
        self,
        *,
        keyword: str,
        category_nos: int | None = None,
        only_ing_status: bool | None = None,
    ) -> list[EventSummary]:
        """기획전명으로 기획전 검색하기 (Version 1.0).

        Args:
            keyword: 검색어(기획전 명).
            category_nos: 전시 카테고리 번호.
            only_ing_status: 진행중인 기획전만 검색 (default false).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"keyword": keyword}
            if category_nos is not None:
                params["categoryNos"] = category_nos
            if only_ing_status is not None:
                params["onlyIngStatus"] = only_ing_status
            resp = await client.get("/display/events/search-by-name", headers=headers, params=params)
            return self.handle_resp(resp, list[EventSummary])

    async def search_event_by_event_nos(
        self,
        *,
        event_nos: str,
        count_per_event: str | None = None,
        soldout: bool | None = None,
        sale_status: str | None = None,
    ) -> list[EventWithProducts]:
        """기획전번호 리스트로 기획전 조회하기 (Version 1.0).

        Args:
            event_nos: 기획전 번호 목록(",")로 구분 (최소 1, 최대 10).
            count_per_event: 기획전별 조회 상품 개수.
            soldout: 품절 상품 포함 여부 (default false).
            sale_status: 판매 상태.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | bool] = {"eventNos": event_nos}
            if count_per_event is not None:
                params["countPerEvent"] = count_per_event
            if soldout is not None:
                params["soldout"] = soldout
            if sale_status is not None:
                params["saleStatus"] = sale_status
            resp = await client.get("/display/events/search-by-nos", headers=headers, params=params)
            return self.handle_resp(resp, list[EventWithProducts])

    async def get_event_by_keyword_and_progress(
        self,
        *,
        keyword: str,
        keyword_type: str | None = None,
        category_nos: int | None = None,
        progress_status: str | None = None,
    ) -> list[EventSummary]:
        """키워드별, 진행상태별로 기획전 검색하기 (Version 1.0).

        Args:
            keyword: 검색어.
            keyword_type: 검색어 타입 (TAG/NAME).
            category_nos: 전시 카테고리 번호.
            progress_status: 진행상태 (ING/READY/END).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {"keyword": keyword}
            if keyword_type is not None:
                params["keywordType"] = keyword_type
            if category_nos is not None:
                params["categoryNos"] = category_nos
            if progress_status is not None:
                params["progressStatus"] = progress_status
            resp = await client.get(
                "/display/events/search-by-progress", headers=headers, params=params
            )
            return self.handle_resp(resp, list[EventSummary])

    async def get_sections_by_event_nos(self, *, event_nos: str) -> list[EventSectionsByEventNo]:
        """다수의 기획전 번호로 기획전 섹션 목록 조회하기 (Version 1.0).

        Args:
            event_nos: 기획전 번호 리스트(",")로 구분.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"eventNos": event_nos}
            resp = await client.get("/display/events/sections", headers=headers, params=params)
            return self.handle_resp(resp, list[EventSectionsByEventNo])

    async def get_event_v2(
        self,
        event_key: str,
        *,
        include_non_member_coupon: bool | None = None,
        preview: bool | None = None,
    ) -> EventDetailResponse:
        """기획전 상세 조회하기 v2.0 (Version 2.0).

        Args:
            event_key: 기획전 번호 또는 기획전 아이디.
            include_non_member_coupon: 비로그인 발급가능 쿠폰 노출 (default false).
            preview: 미리보기 여부 (default false).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "2.0"}
            params: dict[str, bool] = {}
            if include_non_member_coupon is not None:
                params["includeNonMemberCoupon"] = include_non_member_coupon
            if preview is not None:
                params["preview"] = preview
            resp = await client.get(f"/display/events/{event_key}", headers=headers, params=params)
            return self.handle_resp(resp, EventDetailResponse)

    async def get_event(
        self,
        event_no: int,
        *,
        order: str | None = None,
        soldout: bool | None = None,
        sale_status: str | None = None,
        has_product_detail: bool | None = None,
    ) -> EventDetailResponse:
        """기획전 상세 조회하기 (Version 1.0).

        Args:
            event_no: 기획전 번호.
            order: 정렬 조건.
            soldout: 품절 상품 포함 여부 (default false).
            sale_status: 판매 상태.
            has_product_detail: 상품정보 포함 여부.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | bool] = {}
            if order is not None:
                params["order"] = order
            if soldout is not None:
                params["soldout"] = soldout
            if sale_status is not None:
                params["saleStatus"] = sale_status
            if has_product_detail is not None:
                params["hasProductDetail"] = has_product_detail
            resp = await client.get(f"/display/events/{event_no}", headers=headers, params=params)
            return self.handle_resp(resp, EventDetailResponse)

    async def get_event_section_products(
        self,
        event_no: int,
        section_no: int,
        *,
        order: str | None = None,
        direction: str | None = None,
        soldout: bool | None = None,
        sale_status: str | None = None,
        include_stop_product: bool | None = None,
        include_url_direct_display: bool | None = None,
        preview: bool | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> EventSectionProductsResponse:
        """기획전 상품진열 상품 조회 (Version 1.0).

        Args:
            event_no: 기획전 번호.
            section_no: 상품진열 번호.
            order: 정렬 조건.
            direction: 정렬 순서 (DESC/ASC).
            soldout: 품절 상품 포함 여부 (default false).
            sale_status: 판매 상태.
            include_stop_product: 판매중지 상품 포함 여부 (default false).
            include_url_direct_display: URL로만 접근 상품 포함 여부 (default true).
            preview: 미리보기 여부 (default false).
            page_number: 페이지 번호 (default 1).
            page_size: 한 페이지당 상품 노출 수 (default 10).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if order is not None:
                params["order"] = order
            if direction is not None:
                params["direction"] = direction
            if soldout is not None:
                params["soldout"] = soldout
            if sale_status is not None:
                params["saleStatus"] = sale_status
            if include_stop_product is not None:
                params["includeStopProduct"] = include_stop_product
            if include_url_direct_display is not None:
                params["includeUrlDirectDisplay"] = include_url_direct_display
            if preview is not None:
                params["preview"] = preview
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size
            resp = await client.get(
                f"/display/events/{event_no}/sections/{section_no}",
                headers=headers,
                params=params,
            )
            return self.handle_resp(resp, EventSectionProductsResponse)

    # ------------------------------------------------------------------
    #  Popup
    # ------------------------------------------------------------------
    async def get_popups(
        self,
        *,
        page_type: str | None = None,
        target_no: int | None = None,
    ) -> list[Popup]:
        """전체 팝업 목록 조회하기 (Version 1.0).

        Args:
            page_type: 페이지 유형 (MAIN/CATEGORY/EVENT/PRODUCT).
            target_no: 페이지 유형에 따른 페이지 번호.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {}
            if page_type is not None:
                params["pageType"] = page_type
            if target_no is not None:
                params["targetNo"] = target_no
            resp = await client.get("/display/popups", headers=headers, params=params)
            return self.handle_resp(resp, list[Popup])

    async def get_popups_by_popup_ids(
        self,
        popup_ids: str,
        *,
        page_type: str | None = None,
        target_no: int | None = None,
    ) -> list[Popup]:
        """팝업 목록 ID로 조회하기 (Version 1.0).

        Args:
            popup_ids: 팝업 아이디(",")로 구분한 배열.
            page_type: 페이지 유형.
            target_no: 페이지 유형에 따른 페이지 번호.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {}
            if page_type is not None:
                params["pageType"] = page_type
            if target_no is not None:
                params["targetNo"] = target_no
            resp = await client.get(
                f"/display/popups/ids/{popup_ids}", headers=headers, params=params
            )
            return self.handle_resp(resp, list[Popup])

    async def get_popups_by_popup_nos(
        self,
        popup_nos: str,
        *,
        page_type: str | None = None,
        target_no: int | None = None,
    ) -> list[Popup]:
        """팝업 목록 조회하기 (Version 1.0).

        Args:
            popup_nos: 팝업 번호(",")로 구분한 배열.
            page_type: 페이지 유형.
            target_no: 페이지 유형에 따른 페이지 번호.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {}
            if page_type is not None:
                params["pageType"] = page_type
            if target_no is not None:
                params["targetNo"] = target_no
            resp = await client.get(f"/display/popups/{popup_nos}", headers=headers, params=params)
            return self.handle_resp(resp, list[Popup])

    async def get_design_popup(self, request: DesignPopupRequest) -> list[DesignPopup]:
        """디자인 팝업 조회하기 (Version 1.0).

        Args:
            request: 노출 URL/팝업ID/파라미터 조건.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/design-popups", headers=headers, json=body)
            return self.handle_resp(resp, list[DesignPopup])

    # ------------------------------------------------------------------
    #  ProductInquiry
    # ------------------------------------------------------------------
    async def get_products_inquiries(
        self,
        *,
        has_total_count: bool | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        search_type: str | None = None,
        search_keyword: str | None = None,
        tag_value_nos: int | None = None,
    ) -> InquiriesResponse:
        """전체 상품 문의 목록 조회하기 (Version 1.0).

        Args:
            has_total_count: 목록 카운트 포함 여부 (default false).
            page_number: 페이지 번호 (default 1).
            page_size: 한 페이지당 노출 수 (default 20).
            search_type: 검색어 기준 (CONTENT/PRODUCT_NAME).
            search_keyword: 검색어.
            tag_value_nos: 태그값 번호.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if has_total_count is not None:
                params["hasTotalCount"] = has_total_count
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size
            if search_type is not None:
                params["searchType"] = search_type
            if search_keyword is not None:
                params["searchKeyword"] = search_keyword
            if tag_value_nos is not None:
                params["tagValueNos"] = tag_value_nos
            resp = await client.get("/products/inquiries", headers=headers, params=params)
            return self.handle_resp(resp, InquiriesResponse)

    async def get_inquiries_configurations(self) -> InquiryConfigurations:
        """상품문의 게시판 설정 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/products/inquiries/configurations", headers=headers)
            return self.handle_resp(resp, InquiryConfigurations)

    async def get_inquiries_tags(self) -> InquiryTagsResponse:
        """상품문의 태그 전체 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/products/inquiries/tags", headers=headers)
            return self.handle_resp(resp, InquiryTagsResponse)

    async def get_product_inquiries(
        self,
        product_no: int,
        *,
        has_total_count: bool | None = None,
        start_ymd: str | None = None,
        end_ymd: str | None = None,
        answered: bool | None = None,
        is_my_inquiries: bool | None = None,
        tag_value_nos: int | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> ProductInquiriesResponse:
        """상품문의 목록 조회하기 (Version 1.0).

        Args:
            product_no: 상품 번호.
            has_total_count: 목록 카운트 포함 여부 (default false).
            start_ymd: 조회 시작일 (yyyy-MM-dd, 미입력 시 3개월 전).
            end_ymd: 조회 종료일 (yyyy-MM-dd, 미입력 시 오늘).
            answered: 답변 유무 조건.
            is_my_inquiries: 내 문의만 조회 여부.
            tag_value_nos: 태그값 번호.
            page_number: 페이지 번호.
            page_size: 한 페이지당 노출 수.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if has_total_count is not None:
                params["hasTotalCount"] = has_total_count
            if start_ymd is not None:
                params["startYmd"] = start_ymd
            if end_ymd is not None:
                params["endYmd"] = end_ymd
            if answered is not None:
                params["answered"] = answered
            if is_my_inquiries is not None:
                params["isMyInquiries"] = is_my_inquiries
            if tag_value_nos is not None:
                params["tagValueNos"] = tag_value_nos
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size
            resp = await client.get(
                f"/products/{product_no}/inquiries", headers=headers, params=params
            )
            return self.handle_resp(resp, ProductInquiriesResponse)

    async def get_product_inquiry(self, product_no: int, inquiry_no: int) -> ProductInquiry:
        """상품문의 조회하기 (Version 1.0).

        Args:
            product_no: 상품 번호.
            inquiry_no: 상품문의 번호.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(
                f"/products/{product_no}/inquiries/{inquiry_no}", headers=headers
            )
            return self.handle_resp(resp, ProductInquiry)

    # ------------------------------------------------------------------
    #  ProductSection
    # ------------------------------------------------------------------
    async def get_sections(self) -> SectionListResponse:
        """상품 진열 리스트 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/display/sections", headers=headers)
            return self.handle_resp(resp, SectionListResponse)

    async def get_section_by_id_v2(self, section_id: str) -> SectionResponse:
        """진열 ID로 상품 진열 조회하기 (단일 진열) v2.0 (Version 2.0).

        Args:
            section_id: 상품 진열 ID.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "2.0"}
            resp = await client.get(f"/display/sections/ids/{section_id}", headers=headers)
            return self.handle_resp(resp, SectionResponse)

    async def get_section_v1(
        self,
        section_id: int,
        *,
        by: str,
        direction: str,
        soldout: bool,
        sale_status: str,
        page_number: int,
        page_size: int,
        has_total_count: bool,
        has_option_values: bool,
        include_stop_product: bool,
    ) -> SectionProductsResponse:
        """진열 ID로 상품 진열 내 상품 상세 조회하기 (단일진열-페이징) (Version 1.0).

        Args:
            section_id: 상품 진열 ID.
            by: 정렬 기준 (SALE_YMD/ADMIN_SETTING 등).
            direction: 정렬 순서 (DESC/ASC).
            soldout: 품절 상품 포함 여부.
            sale_status: 상품 상태.
            page_number: 페이지 번호.
            page_size: 한 페이지당 노출 수.
            has_total_count: 목록 카운트 포함 여부.
            has_option_values: 옵션리스트 포함 여부.
            include_stop_product: 판매중지 상품 포함 여부.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "by": by,
                "direction": direction,
                "soldout": soldout,
                "saleStatus": sale_status,
                "pageNumber": page_number,
                "pageSize": page_size,
                "hasTotalCount": has_total_count,
                "hasOptionValues": has_option_values,
                "includeStopProduct": include_stop_product,
            }
            resp = await client.get(
                f"/display/sections/ids/{section_id}/products", headers=headers, params=params
            )
            return self.handle_resp(resp, SectionProductsResponse)

    async def get_section_v2(self, section_no: int) -> SectionResponse:
        """상품 진열 조회하기 (단일 진열) v2.0 (Version 2.0).

        Args:
            section_no: 상품 진열 번호.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "2.0"}
            resp = await client.get(f"/display/sections/{section_no}", headers=headers)
            return self.handle_resp(resp, SectionResponse)

    async def get_products_by_section_no(
        self,
        section_no: int,
        *,
        by: str,
        direction: str,
        soldout: bool,
        sale_status: str,
        page_number: int,
        page_size: int,
        has_total_count: bool,
        has_option_values: bool,
        include_stop_product: bool,
    ) -> SectionProductsResponse:
        """진열 번호로 상품 진열 내 상품 상세 조회하기 (단일진열-페이징) (Version 1.0).

        Args:
            section_no: 상품 진열 번호.
            by: 정렬 기준.
            direction: 정렬 순서 (DESC/ASC).
            soldout: 품절 상품 포함 여부.
            sale_status: 상품 상태.
            page_number: 페이지 번호.
            page_size: 한 페이지당 노출 수.
            has_total_count: 목록 카운트 포함 여부.
            has_option_values: 옵션리스트 포함 여부.
            include_stop_product: 판매중지 상품 포함 여부.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "by": by,
                "direction": direction,
                "soldout": soldout,
                "saleStatus": sale_status,
                "pageNumber": page_number,
                "pageSize": page_size,
                "hasTotalCount": has_total_count,
                "hasOptionValues": has_option_values,
                "includeStopProduct": include_stop_product,
            }
            resp = await client.get(
                f"/display/sections/{section_no}/products", headers=headers, params=params
            )
            return self.handle_resp(resp, SectionProductsResponse)

    # ------------------------------------------------------------------
    #  Review
    # ------------------------------------------------------------------
    async def get_category_product_reviews(
        self,
        *,
        category_depth: int,
        category_no: int,
        order_by: str,
        order_direction: str,
        page_number: int,
        page_size: int,
        has_attachment_file: bool | None = None,
        product_name: str | None = None,
        brand_name: str | None = None,
        best_review_yn: str | None = None,
        my_review_yn: str | None = None,
        has_total_count: bool | None = None,
        has_ordered_option: bool | None = None,
    ) -> CategoryProductReviewsResponse:
        """카테고리 상품평 목록 조회하기 (Version 1.0).

        Args:
            category_depth: 카테고리 깊이.
            category_no: 카테고리 번호.
            order_by: 정렬 기준 (RECOMMEND/REGISTER_YMDT/RATING/BEST_REVIEW).
            order_direction: 정렬 순서 (ASC/DESC).
            page_number: 페이지 번호.
            page_size: 한 페이지당 노출 수.
            has_attachment_file: 첨부 파일 여부 (default false).
            product_name: 상품명.
            brand_name: 브랜드 명.
            best_review_yn: 베스트 상품평 여부 (Y/N).
            my_review_yn: 내 상품평 보기 (Y/N).
            has_total_count: 목록 카운트 포함 여부 (default false).
            has_ordered_option: 주문 옵션 정보 포함 여부 (default true).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "categoryDepth": category_depth,
                "categoryNo": category_no,
                "order.by": order_by,
                "order.direction": order_direction,
                "pageNumber": page_number,
                "pageSize": page_size,
            }
            if has_attachment_file is not None:
                params["hasAttachmentFile"] = has_attachment_file
            if product_name is not None:
                params["productName"] = product_name
            if brand_name is not None:
                params["brandName"] = brand_name
            if best_review_yn is not None:
                params["bestReviewYn"] = best_review_yn
            if my_review_yn is not None:
                params["myReviewYn"] = my_review_yn
            if has_total_count is not None:
                params["hasTotalCount"] = has_total_count
            if has_ordered_option is not None:
                params["hasOrderedOption"] = has_ordered_option
            resp = await client.get("/category/product-reviews", headers=headers, params=params)
            return self.handle_resp(resp, CategoryProductReviewsResponse)

    async def get_product_reviews_configurations(self) -> ReviewConfigurations:
        """상품평 게시판 설정 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/product-reviews/configurations", headers=headers)
            return self.handle_resp(resp, ReviewConfigurations)

    async def get_products_photo_reviews(
        self,
        product_no: str,
        *,
        has_total_count: bool | None = None,
        tag_value_nos: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> PhotoReviewsResponse:
        """상품의 포토 후기 목록 조회하기 (Version 1.0).

        Args:
            product_no: 상품 번호.
            has_total_count: 목록 카운트 포함 여부 (default false).
            tag_value_nos: 태그값 번호.
            page_number: 페이지 번호 (default 1).
            page_size: 한 페이지당 노출 수 (default 10).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if has_total_count is not None:
                params["hasTotalCount"] = has_total_count
            if tag_value_nos is not None:
                params["tagValueNos"] = tag_value_nos
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size
            resp = await client.get(
                f"/products/{product_no}/photo-reviews", headers=headers, params=params
            )
            return self.handle_resp(resp, PhotoReviewsResponse)

    async def get_product_reviews(
        self,
        product_no: int,
        *,
        has_attachment_file: bool | None = None,
        order_by: str | None = None,
        order_direction: str | None = None,
        best_review_yn: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        has_total_count: bool | None = None,
        rating_range_from: int | None = None,
        rating_range_to: int | None = None,
        tag_value_nos: str | None = None,
        has_product_info: bool | None = None,
        has_ordered_option: bool | None = None,
    ) -> ProductReviewsResponse:
        """상품평 목록 조회하기 2.0 (Version 2.0).

        Args:
            product_no: 상품 번호.
            has_attachment_file: 첨부 파일 여부.
            order_by: 정렬 기준.
            order_direction: 정렬 순서 (ASC/DESC).
            best_review_yn: 베스트 상품평 여부 (Y/N).
            page_number: 페이지 번호 (default 1).
            page_size: 한 페이지당 노출 수 (최대 100).
            has_total_count: 목록 카운트 포함 여부 (default false).
            rating_range_from: 리뷰평점 시작범위.
            rating_range_to: 리뷰평점 끝범위.
            tag_value_nos: 태그값 번호.
            has_product_info: 상품 정보 포함 여부 (default true).
            has_ordered_option: 주문 옵션 정보 포함 여부 (default false).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "2.0"}
            params: dict[str, str | int | bool] = {}
            if has_attachment_file is not None:
                params["hasAttachmentFile"] = has_attachment_file
            if order_by is not None:
                params["order.by"] = order_by
            if order_direction is not None:
                params["order.direction"] = order_direction
            if best_review_yn is not None:
                params["bestReviewYn"] = best_review_yn
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size
            if has_total_count is not None:
                params["hasTotalCount"] = has_total_count
            if rating_range_from is not None:
                params["ratingRange.from"] = rating_range_from
            if rating_range_to is not None:
                params["ratingRange.to"] = rating_range_to
            if tag_value_nos is not None:
                params["tagValueNos"] = tag_value_nos
            if has_product_info is not None:
                params["hasProductInfo"] = has_product_info
            if has_ordered_option is not None:
                params["hasOrderedOption"] = has_ordered_option
            resp = await client.get(
                f"/products/{product_no}/product-reviews", headers=headers, params=params
            )
            return self.handle_resp(resp, ProductReviewsResponse)

    async def get_products_product_reviews(
        self,
        product_no: int,
        review_no: int,
        *,
        has_ordered_option: bool | None = None,
    ) -> ProductReview:
        """상품평 가져오기 (Version 1.0).

        Args:
            product_no: 상품 번호.
            review_no: 상품평 번호.
            has_ordered_option: 주문 옵션 정보 포함 여부 (default true).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, bool] = {}
            if has_ordered_option is not None:
                params["hasOrderedOption"] = has_ordered_option
            resp = await client.get(
                f"/products/{product_no}/product-reviews/{review_no}",
                headers=headers,
                params=params,
            )
            return self.handle_resp(resp, ProductReview)

    async def get_products_product_reviews_comments(
        self,
        product_no: str,
        review_no: str,
        *,
        has_total_count: bool | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> ReviewCommentsResponse:
        """상품평의 댓글 목록 조회하기 (Version 1.0).

        Args:
            product_no: 상품 번호.
            review_no: 상품평 번호.
            has_total_count: 목록 카운트 포함 여부 (default false).
            page: 페이지 번호 (default 1).
            size: 한 페이지당 노출 수 (default 10).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if has_total_count is not None:
                params["hasTotalCount"] = has_total_count
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size
            resp = await client.get(
                f"/products/{product_no}/product-reviews/{review_no}/comments",
                headers=headers,
                params=params,
            )
            return self.handle_resp(resp, ReviewCommentsResponse)

    async def get_products_reviews_by_board(
        self,
        *,
        board_type: str,
        sorting_sort_criterion: str | None = None,
        sorting_ordering: str | None = None,
        depth1_display_category_no: int | None = None,
        keyword: str | None = None,
        page_number: int | None = None,
        is_widget: bool | None = None,
        tag_value_nos: str | None = None,
    ) -> ReviewBoardResponse:
        """상품평 게시판 목록 조회하기 (Version 1.0).

        Args:
            board_type: 게시판 유형 (ALL/PHOTO/일반상품평 등).
            sorting_sort_criterion: 정렬 기준.
            sorting_ordering: 정렬 순서 (ASC/DESC).
            depth1_display_category_no: 전시 카테고리 번호 (1depthNo).
            keyword: 검색어.
            page_number: 페이지 번호 (default 1).
            is_widget: 위젯 여부 (default false).
            tag_value_nos: 태그값 번호.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"boardType": board_type}
            if sorting_sort_criterion is not None:
                params["sorting.sortCriterion"] = sorting_sort_criterion
            if sorting_ordering is not None:
                params["sorting.ordering"] = sorting_ordering
            if depth1_display_category_no is not None:
                params["depth1DisplayCategoryNo"] = depth1_display_category_no
            if keyword is not None:
                params["keyword"] = keyword
            if page_number is not None:
                params["pageNumber"] = page_number
            if is_widget is not None:
                params["isWidget"] = is_widget
            if tag_value_nos is not None:
                params["tagValueNos"] = tag_value_nos
            resp = await client.get("/reviews/boards", headers=headers, params=params)
            return self.handle_resp(resp, ReviewBoardResponse)

    async def get_reviews_by_products(
        self,
        *,
        sorting_sort_criterion: str | None = None,
        sorting_ordering: str | None = None,
        depth1_display_category_no: int | None = None,
        keyword: str | None = None,
        page_number: int | None = None,
        is_widget: bool | None = None,
    ) -> ReviewedProductsResponse:
        """상품 기준 상품평 게시판 목록 조회하기 (Version 1.0).

        Args:
            sorting_sort_criterion: 정렬 기준 (REVIEW_COUNT/REGISTER 등).
            sorting_ordering: 정렬 순서 (ASC/DESC).
            depth1_display_category_no: 전시 카테고리 번호 (1depthNo).
            keyword: 검색어.
            page_number: 페이지 번호 (default 1).
            is_widget: 위젯 여부 (default false).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if sorting_sort_criterion is not None:
                params["sorting.sortCriterion"] = sorting_sort_criterion
            if sorting_ordering is not None:
                params["sorting.ordering"] = sorting_ordering
            if depth1_display_category_no is not None:
                params["depth1DisplayCategoryNo"] = depth1_display_category_no
            if keyword is not None:
                params["keyword"] = keyword
            if page_number is not None:
                params["pageNumber"] = page_number
            if is_widget is not None:
                params["isWidget"] = is_widget
            resp = await client.get(
                "/reviews/boards/reviewed-products", headers=headers, params=params
            )
            return self.handle_resp(resp, ReviewedProductsResponse)

    async def get_reviews_tags(self) -> ReviewTagsResponse:
        """상품리뷰 태그 전체 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/reviews/tags", headers=headers)
            return self.handle_resp(resp, ReviewTagsResponse)

    # ------------------------------------------------------------------
    #  SkinBanner
    # ------------------------------------------------------------------
    async def get_skin_banners(
        self,
        *,
        banner_group_codes: str,
        skin_no: int | None = None,
    ) -> list[SkinBannerGroup]:
        """플랫폼 별 전체 스킨 배너 조회하기 (Version 1.0).

        Args:
            banner_group_codes: 배너 그룹 코드 리스트(",")로 구분.
            skin_no: 스킨 번호 (미리보기의 경우에만 입력).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {"bannerGroupCodes": banner_group_codes}
            if skin_no is not None:
                params["skinNo"] = skin_no
            resp = await client.get("/skin-banners", headers=headers, params=params)
            return self.handle_resp(resp, list[SkinBannerGroup])

    async def get_skin_banners_groups_by_skin(
        self,
        *,
        is_preview: bool | None = None,
        skin_no: int | None = None,
    ) -> SkinBannerGroupsBySkin:
        """사용 혹은 작업중 스킨 정보 및 배너 그룹 조회하기 (Version 1.0).

        Args:
            is_preview: 미리보기 스킨 여부 (default false).
            skin_no: 스킨 번호 (미리보기의 경우 필수).
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if is_preview is not None:
                params["isPreview"] = is_preview
            if skin_no is not None:
                params["skinNo"] = skin_no
            resp = await client.get("/skin-banners/groups-by-skin", headers=headers, params=params)
            return self.handle_resp(resp, SkinBannerGroupsBySkin)

    async def get_skin_banners_by_banner_id(self, banner_id: str) -> list[SkinBannerGroup]:
        """스킨의 배너ID를 통해 배너리스트 조회하기 (Version 1.0).

        Args:
            banner_id: 배너 ID.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/skin-banners/{banner_id}", headers=headers)
            return self.handle_resp(resp, list[SkinBannerGroup])

    # ------------------------------------------------------------------
    #  Sticker
    # ------------------------------------------------------------------
    async def get_stickers(self) -> list[Sticker]:
        """스티커 목록 조회 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/stickers", headers=headers)
            return self.handle_resp(resp, list[Sticker])

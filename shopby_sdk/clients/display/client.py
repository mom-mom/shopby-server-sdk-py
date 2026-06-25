"""Display API 클라이언트"""

import httpx

from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.display.models import (
    BannerExtraInfo,
    BannerGroup,
    BannerKeywordType,
    BannerSection,
    BannerSectionCreateRequest,
    BannerSectionUpdateRequest,
    BestReviewUpdateRequest,
    DisplayCategory,
    DisplayCategoryCreateRequest,
    DisplayCategoryCreateResponse,
    DisplayCategoryTreeNode,
    DisplayCategoryUpdateRequest,
    EventDetailResponse,
    EventSearchResponse,
    EventSearchType,
    EventSearchDateType,
    ExternalSiteReviewCreateItem,
    ExternalSiteReviewCreateResponse,
    HeadlessBannerKeywordType,
    HeadlessBannerResponse,
    Inquiry,
    InquiryDisplayStatusUpdateRequest,
    InquiryMemberSearchType,
    InquiryReply,
    InquirySearchDateType,
    ReviewBulkUpdateResponse,
    ReviewCreateItem,
    ReviewCreateResponse,
    ReviewDeleteResponse,
    ReviewExtraJsonUpdateItem,
    ReviewListResponse,
    ReviewSearchRequest,
    ReviewSearchResponse,
    ReviewStatusUpdateRequest,
    ReviewUpdateItem,
    ReviewUpdateResponse,
    StandardCategory,
    StickerListResponse,
)


class ShopbyServerDisplayApiClient(ShopbyServerApiClient):
    """Shopby Display Server API 클라이언트"""

    async def get_event_detail(self, event_no: int) -> EventDetailResponse:
        """
        기획전 단건 조회

        기획전 상세 정보를 조회하는 API입니다.

        Args:
            event_no: 기획전 번호

        Returns:
            EventDetailResponse: 기획전 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 1.0 헤더 추가
            headers = {"version": "1.0"}

            resp = await client.get(
                f"/events/{event_no}",
                headers=headers,
            )

            return self.handle_resp(resp, EventDetailResponse)

    # ------------------------------------
    #  배너(Banner)
    # ------------------------------------

    async def get_banners(self, keywords: str, keyword_type: BannerKeywordType) -> list[BannerSection]:
        """
        배너 조회하기

        배너 코드 또는 ID 정보로 배너를 조회합니다.

        Args:
            keywords: 배너 코드 또는 ID
            keyword_type: 검색 타입 (CODE, ID, NO)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "keywords": keywords,
                "keywordType": keyword_type,
            }
            resp = await client.get("/banners", params=params, headers=headers)
            return self.handle_resp(resp, list[BannerSection])

    async def create_banner_section(self, request: BannerSectionCreateRequest) -> int:
        """
        배너 섹션 등록

        Args:
            request: 배너 섹션 등록 요청

        Returns:
            int: 생성된 배너 섹션 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/banners", json=body, headers=headers)
            return self.handle_resp(resp, int)

    async def delete_banner_section(self, banner_nos: list[int]) -> None:
        """
        배너 섹션 삭제

        Args:
            banner_nos: 삭제할 배너 번호 리스트
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "bannerNos": ",".join(str(no) for no in banner_nos),
            }
            resp = await client.delete("/banners", params=params, headers=headers)
            self.raise_for_status(resp)
            return None

    async def update_banner_section(self, banner_no: str, request: BannerSectionUpdateRequest) -> None:
        """
        배너 섹션 수정

        Args:
            banner_no: 배너 섹션 번호
            request: 배너 섹션 수정 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(f"/banners/{banner_no}", json=body, headers=headers)
            self.raise_for_status(resp)
            return None

    async def get_banner_extra_infos(
        self,
        banner_section_no: int | None = None,
        banner_nos: list[int] | None = None,
    ) -> list[BannerExtraInfo]:
        """
        배너 추가정보 조회하기

        배너 섹션 번호 또는 배너 번호 리스트로 조회합니다. (둘 다 있으면 섹션 번호 우선)

        Args:
            banner_section_no: 배너 섹션 번호
            banner_nos: 배너 번호 리스트 (최대 100개)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if banner_section_no is not None:
                params["bannerSectionNo"] = banner_section_no
            if banner_nos is not None:
                params["bannerNos"] = ",".join(str(no) for no in banner_nos)
            resp = await client.get("/banners/extraInfo", params=params, headers=headers)
            return self.handle_resp(resp, list[BannerExtraInfo])

    async def create_banner_extra_info(self, items: list[BannerExtraInfo]) -> None:
        """
        배너 추가정보 등록하기

        Args:
            items: 배너 추가정보 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True, mode="json") for x in items]
            resp = await client.post("/banners/extraInfo", json=body, headers=headers)
            self.raise_for_status(resp)
            return None

    async def update_banner_extra_info(self, items: list[BannerExtraInfo]) -> None:
        """
        배너 추가정보 수정하기

        Args:
            items: 배너 추가정보 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True, mode="json") for x in items]
            resp = await client.put("/banners/extraInfo", json=body, headers=headers)
            self.raise_for_status(resp)
            return None

    async def delete_banner_extra_info(self, banner_nos: list[int]) -> None:
        """
        배너 추가정보 삭제하기

        Args:
            banner_nos: 삭제할 배너 번호 리스트
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "bannerNos": ",".join(str(no) for no in banner_nos),
            }
            resp = await client.delete("/banners/extraInfo", params=params, headers=headers)
            self.raise_for_status(resp)
            return None

    async def get_banner_groups(self) -> list[BannerGroup]:
        """배너 그룹 조회하기"""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/banners/groups", headers=headers)
            return self.handle_resp(resp, list[BannerGroup])

    async def get_headless_banners(
        self,
        keywords: str | None = None,
        keyword_type: HeadlessBannerKeywordType | None = None,
        last_banner_no: int | None = None,
        size: int | None = None,
    ) -> HeadlessBannerResponse:
        """
        헤드리스 배너 조회

        Args:
            keywords: 검색어(쉼표 구분)
            keyword_type: 검색어 타입 (BANNER_GROUP_NO, BANNER_NO, BANNER_ID, BANNER_CODE)
            last_banner_no: 조회할 다음 배너 번호
            size: 페이지당 조회 수
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if keywords is not None:
                params["keywordInfo.keywords"] = keywords
            if keyword_type is not None:
                params["keywordInfo.keywordType"] = keyword_type
            if last_banner_no is not None:
                params["lastBannerNo"] = last_banner_no
            if size is not None:
                params["size"] = size
            resp = await client.get("/banners/simple-infos", params=params, headers=headers)
            return self.handle_resp(resp, HeadlessBannerResponse)

    # ------------------------------------
    #  카테고리(Category)
    # ------------------------------------

    async def get_categories(self) -> list[StandardCategory]:
        """표준 카테고리 조회하기"""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/categories", headers=headers)
            return self.handle_resp(resp, list[StandardCategory])

    async def get_display_categories(self) -> list[DisplayCategory]:
        """전시 카테고리 조회하기"""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/categories/display-categories", headers=headers)
            return self.handle_resp(resp, list[DisplayCategory])

    async def get_display_categories_tree(self, has_product_count: bool | None = None) -> list[DisplayCategoryTreeNode]:
        """
        전시카테고리 트리 조회하기

        Args:
            has_product_count: 연결된 상품 수 포함 여부
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if has_product_count is not None:
                params["hasProductCount"] = has_product_count
            resp = await client.get("/categories/display-categories/tree", params=params, headers=headers)
            return self.handle_resp(resp, list[DisplayCategoryTreeNode])

    async def create_display_category(self, request: DisplayCategoryCreateRequest) -> DisplayCategoryCreateResponse:
        """
        전시 카테고리 등록하기

        Args:
            request: 전시 카테고리 등록 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/categories/display-categories", json=body, headers=headers)
            return self.handle_resp(resp, DisplayCategoryCreateResponse)

    async def update_display_category(self, display_category_no: int, request: DisplayCategoryUpdateRequest) -> None:
        """
        전시 카테고리 수정하기 (부분 수정)

        Args:
            display_category_no: 전시카테고리 번호
            request: 전시 카테고리 수정 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.patch(
                f"/categories/display-categories/{display_category_no}", json=body, headers=headers
            )
            self.raise_for_status(resp)
            return None

    async def delete_display_category(self, display_category_no: int, force: bool | None = None) -> None:
        """
        전시 카테고리 삭제하기

        Args:
            display_category_no: 전시카테고리 번호
            force: 상품 매핑 해제 후 강제 삭제 여부
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if force is not None:
                params["force"] = force
            resp = await client.delete(
                f"/categories/display-categories/{display_category_no}", params=params, headers=headers
            )
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  기획전(Event)
    # ------------------------------------

    async def get_events(
        self,
        search_date_type: EventSearchDateType | None = None,
        start_ymd: str | None = None,
        end_ymd: str | None = None,
        search_type: EventSearchType | None = None,
        keyword: str | None = None,
        progress_status: list[str] | None = None,
        event_type: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> EventSearchResponse:
        """
        기획전 검색

        Args:
            search_date_type: 조회 기간 타입 (REGISTER_YMDT, DISPLAY_YMDT)
            start_ymd: 조회 시작일 (yyyy-MM-dd)
            end_ymd: 조회 종료일 (yyyy-MM-dd)
            search_type: 검색어 타입 (EVENT_NAME, EVENT_NO, ADMIN, EVENT_ID)
            keyword: 검색어
            progress_status: 진행상태 목록 (ALL, READY, ING, END)
            event_type: 기획전 유형 (GENERAL, EXTERNAL)
            page: 시작 페이지
            size: 조회 수
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if search_date_type is not None:
                params["searchDateType"] = search_date_type
            if start_ymd is not None:
                params["datePeriod.startYmd"] = start_ymd
            if end_ymd is not None:
                params["datePeriod.endYmd"] = end_ymd
            if search_type is not None:
                params["searchType"] = search_type
            if keyword is not None:
                params["keyword"] = keyword
            if progress_status is not None:
                params["progressStatus"] = ",".join(progress_status)
            if event_type is not None:
                params["eventType"] = event_type
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size
            resp = await client.get("/events", params=params, headers=headers)
            return self.handle_resp(resp, EventSearchResponse)

    # ------------------------------------
    #  상품문의(Inquiry)
    # ------------------------------------

    async def get_inquiry(
        self,
        start_ymd: str | None = None,
        end_ymd: str | None = None,
        reply_yn: str | None = None,
        inquiry_no: int | None = None,
        search_date_type: InquirySearchDateType | None = None,
        member_type: InquiryMemberSearchType | None = None,
        member_keyword: str | None = None,
    ) -> list[Inquiry]:
        """
        상품문의 조회하기

        Args:
            start_ymd: 조회 시작일 (yyyy-MM-dd, 미입력 시 3개월 전)
            end_ymd: 조회 종료일 (yyyy-MM-dd, 미입력 시 오늘)
            reply_yn: 답변여부 (미입력 시 전체조회)
            inquiry_no: 문의번호 (미입력 시 전체조회)
            search_date_type: 기간 검색 종류 (REGISTER_YMDT, REPLY_YMDT)
            member_type: 회원검색타입 (NAME, ID, NO)
            member_keyword: 회원 검색어 (회원ID or 회원명)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if start_ymd is not None:
                params["startYmd"] = start_ymd
            if end_ymd is not None:
                params["endYmd"] = end_ymd
            if reply_yn is not None:
                params["replyYn"] = reply_yn
            if inquiry_no is not None:
                params["inquiryNo"] = inquiry_no
            if search_date_type is not None:
                params["searchDateType"] = search_date_type
            if member_type is not None:
                params["member.type"] = member_type
            if member_keyword is not None:
                params["member.keyword"] = member_keyword
            resp = await client.get("/inquiry", params=params, headers=headers)
            return self.handle_resp(resp, list[Inquiry])

    async def get_inquiry_replies(self, inquiry_nos: list[int]) -> list[InquiryReply]:
        """
        상품문의 답변 조회하기

        Args:
            inquiry_nos: 답글이 달린 문의 번호 리스트 (최대 100개)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "inquiryNos": ",".join(str(no) for no in inquiry_nos),
            }
            resp = await client.get("/inquiry/replies", params=params, headers=headers)
            return self.handle_resp(resp, list[InquiryReply])

    async def update_inquiry_display_status(self, inquiry_no: int, request: InquiryDisplayStatusUpdateRequest) -> None:
        """
        상품 문의 전시 상태 변경하기

        Args:
            inquiry_no: 상품 문의 번호
            request: 전시 상태 변경 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(f"/inquiry/{inquiry_no}/display-status", json=body, headers=headers)
            self.raise_for_status(resp)
            return None

    async def post_inquiry_reply(self, inquiry_no: int, content: str) -> None:
        """
        상품문의 답변 등록하기

        Args:
            inquiry_no: 상품 문의 번호
            content: 답변 내용 (text/plain 본문)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0", "Content-Type": "text/plain;charset=UTF-8"}
            resp = await client.post(f"/inquiry/{inquiry_no}/reply", content=content.encode("utf-8"), headers=headers)
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  상품평(Review)
    # ------------------------------------

    async def get_reviews(
        self,
        start_ymd: str | None = None,
        end_ymd: str | None = None,
        page: int | None = None,
        size: int | None = None,
        review_no: int | None = None,
        search_after: str | None = None,
    ) -> ReviewListResponse:
        """
        상품평 조회하기

        Args:
            start_ymd: 작성일시 시작 (yyyy-MM-dd, 미입력 시 3개월 전)
            end_ymd: 작성일시 끝 (yyyy-MM-dd, 미입력 시 오늘)
            page: 페이지 번호 (paging search)
            size: 조회 수
            review_no: 상품평 번호
            search_after: 검색 기준 값(lastId) (keySet search)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if start_ymd is not None:
                params["startYmd"] = start_ymd
            if end_ymd is not None:
                params["endYmd"] = end_ymd
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size
            if review_no is not None:
                params["reviewNo"] = review_no
            if search_after is not None:
                params["searchAfter"] = search_after
            resp = await client.get("/reviews", params=params, headers=headers)
            return self.handle_resp(resp, ReviewListResponse)

    async def search_reviews(self, request: ReviewSearchRequest) -> ReviewSearchResponse:
        """
        상품평 검색하기

        Args:
            request: 상품평 검색 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/reviews", json=body, headers=headers)
            return self.handle_resp(resp, ReviewSearchResponse)

    async def create_reviews(self, items: list[ReviewCreateItem]) -> ReviewCreateResponse:
        """
        상품평 등록하기

        Args:
            items: 상품평 등록 요청 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True, mode="json") for x in items]
            resp = await client.post("/reviews/product-reviews", json=body, headers=headers)
            return self.handle_resp(resp, ReviewCreateResponse)

    async def update_reviews(self, items: list[ReviewUpdateItem]) -> ReviewUpdateResponse:
        """
        상품평 수정하기

        Args:
            items: 상품평 수정 요청 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True, mode="json") for x in items]
            resp = await client.put("/reviews/product-reviews", json=body, headers=headers)
            return self.handle_resp(resp, ReviewUpdateResponse)

    async def delete_reviews(self, review_nos: list[int], register_nos: list[int]) -> ReviewDeleteResponse:
        """
        상품평 삭제하기

        상품평번호와 작성자번호를 순서대로 매칭시켜 요청합니다. (최대 100개)

        Args:
            review_nos: 삭제할 상품 리뷰 번호 리스트
            register_nos: 작성자 번호 리스트
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "reviewNos": ",".join(str(no) for no in review_nos),
                "registerNos": ",".join(str(no) for no in register_nos),
            }
            resp = await client.delete("/reviews/product-reviews", params=params, headers=headers)
            return self.handle_resp(resp, ReviewDeleteResponse)

    async def create_external_site_reviews(
        self, items: list[ExternalSiteReviewCreateItem]
    ) -> ExternalSiteReviewCreateResponse:
        """
        외부 상품평 등록하기

        Args:
            items: 외부 상품평 등록 요청 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True, mode="json") for x in items]
            resp = await client.post("/reviews/external-site", json=body, headers=headers)
            return self.handle_resp(resp, ExternalSiteReviewCreateResponse)

    async def update_best_reviews(self, request: BestReviewUpdateRequest) -> ReviewBulkUpdateResponse:
        """
        상품평 베스트 리뷰 일괄 변경

        Args:
            request: 베스트 리뷰 일괄 변경 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/reviews/best-review", json=body, headers=headers)
            return self.handle_resp(resp, ReviewBulkUpdateResponse)

    async def update_review_status(self, request: ReviewStatusUpdateRequest) -> ReviewBulkUpdateResponse:
        """
        상품평 전시상태 일괄 변경

        Args:
            request: 전시상태 일괄 변경 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/reviews/status", json=body, headers=headers)
            return self.handle_resp(resp, ReviewBulkUpdateResponse)

    async def update_review_extra_json(self, items: list[ReviewExtraJsonUpdateItem]) -> ReviewBulkUpdateResponse:
        """
        상품평 extraJson 일괄 변경

        Args:
            items: extraJson 변경 요청 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True, mode="json") for x in items]
            resp = await client.put("/reviews/extraJson", json=body, headers=headers)
            return self.handle_resp(resp, ReviewBulkUpdateResponse)

    # ------------------------------------
    #  스티커(Sticker)
    # ------------------------------------

    async def search_stickers(self, page: int | None = None, size: int | None = None) -> StickerListResponse:
        """
        스티커 목록 조회하기

        Args:
            page: 페이지 번호
            size: 한 페이지에 조회되는 갯수
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size
            resp = await client.get("/stickers", params=params, headers=headers)
            return self.handle_resp(resp, StickerListResponse)

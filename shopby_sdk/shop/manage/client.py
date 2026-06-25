"""Shopby Shop(Client) Manage API 클라이언트.

shop-api(`https://shop-api.e-ncp.com`) 의 공개(인증 불필요) manage 도메인
(주소/게시판/공휴일/1:1문의 설정/인스타그램/외부스크립트/약관) 클라이언트.

회원 인증(accessToken / Shop-By-Authorization)은 의도적으로 전송하지 않는다.
clientId/platform/language 헤더는 base(``ShopbyShopApiClient``) 가 주입하며,
각 메서드는 엔드포인트별 ``version`` 헤더만 지정한다.
"""

import httpx

from shopby_sdk.shop.base import ShopbyShopApiClient
from shopby_sdk.shop.manage.models import (
    AddressSearchResponse,
    ArticleDetailResponse,
    ArticleListResponse,
    BoardCategory,
    BoardConfigurationsResponse,
    BoardDirection,
    CustomTermsItem,
    CustomTermsRequest,
    ExternalScriptItem,
    InquiryConfigurationResponse,
    InquiryType,
    InquiryTypeDirection,
    InstagramMediaResponse,
    JapanAddressResponse,
    PostDetailResponse,
    PostListResponse,
    PostPreviewItem,
    PostPreviewsRequest,
    PostsV2SearchRequest,
    PostTermsDetailRequest,
    PostUsedTermsRequest,
    TermsDetailResponse,
    TermsHistoryItem,
    TermsType,
    UsedTermsResponse,
    UsedTermsTypesResponse,
)


class ShopbyShopManageApiClient(ShopbyShopApiClient):
    """Shopby Shop(Client) Manage API 클라이언트."""

    # ------------------------------------
    #  Address (주소)
    # ------------------------------------
    async def search_addresses(
        self,
        keyword: str,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> AddressSearchResponse:
        """주소 조회하기 (Version 1.0)

        검색 키워드로 주소정보를 검색합니다.

        Args:
            keyword: 검색 키워드
            page_number: 페이지 번호 (default: 1)
            page_size: 한 페이지당 노출 수 (default: 10, 최대: 1000)

        Returns:
            AddressSearchResponse: 주소 목록 (totalCount, items)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {"keyword": keyword}
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size

            resp = await client.get("/addresses/search", headers=headers, params=params)
            return self.handle_resp(resp, AddressSearchResponse)

    async def search_jp_address(self, zip_code: str) -> JapanAddressResponse:
        """일본 주소 검색 (Version 1.0)

        Args:
            zip_code: 우편번호

        Returns:
            JapanAddressResponse: 일본 주소 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {"zipCode": zip_code}

            resp = await client.get("/addresses/search/jp", headers=headers, params=params)
            return self.handle_resp(resp, JapanAddressResponse)

    # ------------------------------------
    #  Board (게시판)
    # ------------------------------------
    async def get_board_config(self) -> BoardConfigurationsResponse:
        """게시판 설정 조회하기 (Version 1.0)

        전체 게시판의 설정정보를 조회합니다.

        Returns:
            BoardConfigurationsResponse: 게시판/문의/리뷰 설정
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get("/boards/configurations", headers=headers)
            return self.handle_resp(resp, BoardConfigurationsResponse)

    async def get_board_categories(self, board_no: str) -> list[BoardCategory]:
        """게시판 카테고리 목록 조회하기 (Version 1.0)

        Args:
            board_no: 게시판 번호(숫자) 또는 게시판 ID(문자열)

        Returns:
            list[BoardCategory]: 게시판 카테고리 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get(f"/boards/{board_no}/categories", headers=headers)
            return self.handle_resp(resp, list[BoardCategory])

    async def search_posts(
        self,
        board_no: str,
        page_number: int | None = None,
        page_size: int | None = None,
        has_total_count: bool | None = None,
        keyword: str | None = None,
        search_type: str | None = None,
        category_no: int | None = None,
        start_ymd: str | None = None,
        end_ymd: str | None = None,
        with_replied: bool | None = None,
        direction: BoardDirection | None = None,
        is_mine: bool | None = None,
        my_recommend_only: bool | None = None,
        include_recommended: bool | None = None,
        is_noticed: bool | None = None,
        is_secreted: bool | None = None,
    ) -> ArticleListResponse:
        """게시글 리스트 조회하기 (Version 1.0)

        특정 게시판(게시판 번호 기준)의 게시글 리스트를 조회합니다.

        Args:
            board_no: 게시판 번호(숫자) 또는 게시판 ID(문자열)
            page_number: 페이지 번호
            page_size: 한 페이지당 노출 수
            has_total_count: 목록 카운트 포함 여부
            keyword: 검색어
            search_type: 검색유형 (ALL, TITLE, CONTENT, WRITER)
            category_no: 게시판 카테고리
            start_ymd: 조회 시작일 (yyyy-MM-dd)
            end_ymd: 조회 종료일 (yyyy-MM-dd)
            with_replied: 답글 포함 여부
            direction: 정렬방식
            is_mine: 본인 작성 글만 조회 여부
            my_recommend_only: 본인 추천 글만 조회 여부
            include_recommended: 본인 추천 여부 포함
            is_noticed: 공지글 조회 여부
            is_secreted: 비밀글 조회 여부

        Returns:
            ArticleListResponse: 게시글 목록 (totalCount, items)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size
            if has_total_count is not None:
                params["hasTotalCount"] = has_total_count
            if keyword is not None:
                params["keyword"] = keyword
            if search_type is not None:
                params["searchType"] = search_type
            if category_no is not None:
                params["categoryNo"] = category_no
            if start_ymd is not None:
                params["startYmd"] = start_ymd
            if end_ymd is not None:
                params["endYmd"] = end_ymd
            if with_replied is not None:
                params["withReplied"] = with_replied
            if direction is not None:
                params["direction"] = direction
            if is_mine is not None:
                params["isMine"] = is_mine
            if my_recommend_only is not None:
                params["myRecommendOnly"] = my_recommend_only
            if include_recommended is not None:
                params["includeRecommended"] = include_recommended
            if is_noticed is not None:
                params["isNoticed"] = is_noticed
            if is_secreted is not None:
                params["isSecreted"] = is_secreted

            resp = await client.get(f"/boards/{board_no}/articles", headers=headers, params=params)
            return self.handle_resp(resp, ArticleListResponse)

    async def get_post(
        self,
        board_no: str,
        article_no: int,
        password: str | None = None,
        with_replied: bool | None = None,
    ) -> ArticleDetailResponse:
        """게시글 상세 조회하기 (Version 1.0)

        Args:
            board_no: 게시판 번호(숫자) 또는 게시판 ID(문자열)
            article_no: 게시글 번호
            password: 비회원 글 확인용 비밀번호
            with_replied: 답글 포함 여부 (default: true)

        Returns:
            ArticleDetailResponse: 게시글 상세
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | bool] = {}
            if password is not None:
                params["password"] = password
            if with_replied is not None:
                params["withReplied"] = with_replied

            resp = await client.get(f"/boards/{board_no}/articles/{article_no}", headers=headers, params=params)
            return self.handle_resp(resp, ArticleDetailResponse)

    async def reply_posts(
        self,
        board_no: str,
        article_no: int,
        page: int | None = None,
        page_size: int | None = None,
        include_recommended: bool | None = None,
        direction: BoardDirection | None = None,
    ) -> ArticleListResponse:
        """게시글 답글 리스트 조회하기 (Version 1.0)

        Args:
            board_no: 게시판 번호(숫자) 또는 게시판 ID(문자열)
            article_no: 게시글 번호
            page: 페이지 번호 (default: 1)
            page_size: 한 페이지당 노출 수 (default: 10)
            include_recommended: 본인 추천 여부 포함
            direction: 정렬방식

        Returns:
            ArticleListResponse: 답글 목록 (totalCount, items)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if include_recommended is not None:
                params["includeRecommended"] = include_recommended
            if direction is not None:
                params["direction"] = direction

            resp = await client.get(
                f"/boards/{board_no}/articles/{article_no}/replies",
                headers=headers,
                params=params,
            )
            return self.handle_resp(resp, ArticleListResponse)

    async def get_posts_v2(
        self,
        request: PostsV2SearchRequest,
        page: int | None = None,
        page_size: int | None = None,
    ) -> PostListResponse:
        """게시글 리스트 조회하기(버전2) (Version 1.0)

        특정 게시판 또는 몰 단위의 게시글 리스트를 조회합니다.
        request.board_no_or_id 를 None 으로 보내면 몰 단위로 조회합니다.

        Args:
            request: 게시글 검색 조건
            page: 페이지 번호 (default: 1)
            page_size: 한 페이지당 노출 수 (default: 10)

        Returns:
            PostListResponse: 게시글 목록 (totalCount, items)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, int] = {}
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.post("/boards/posts", headers=headers, params=params, json=body)
            return self.handle_resp(resp, PostListResponse)

    async def get_post_v2(
        self,
        board_no: str,
        post_no: int,
        password: str | None = None,
    ) -> PostDetailResponse:
        """게시글 상세 조회하기(버전2) (Version 1.0)

        서비스 어드민의 게시판 권한 설정이 적용됩니다.

        Args:
            board_no: 게시판 번호(숫자) 또는 게시판 ID(문자열)
            post_no: 게시글 번호
            password: 비회원 글 확인용 비밀번호

        Returns:
            PostDetailResponse: 게시글 상세
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {}
            if password is not None:
                params["password"] = password

            resp = await client.get(f"/boards/{board_no}/posts/{post_no}", headers=headers, params=params)
            return self.handle_resp(resp, PostDetailResponse)

    async def get_reply_posts_v2(
        self,
        board_no: str,
        post_no: int,
        page: int | None = None,
        page_size: int | None = None,
        direction: BoardDirection | None = None,
    ) -> PostListResponse:
        """게시글 답글 리스트 조회하기(버전2) (Version 1.0)

        Args:
            board_no: 게시판 번호(숫자) 또는 게시판 ID(문자열)
            post_no: 게시글 번호
            page: 페이지 번호 (default: 1)
            page_size: 한 페이지당 노출 수 (default: 10)
            direction: 정렬방식

        Returns:
            PostListResponse: 답글 목록 (totalCount, items)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {}
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if direction is not None:
                params["direction"] = direction

            resp = await client.get(f"/boards/{board_no}/posts/{post_no}/replies", headers=headers, params=params)
            return self.handle_resp(resp, PostListResponse)

    async def get_post_previews(
        self,
        board_no: str,
        request: PostPreviewsRequest,
    ) -> list[PostPreviewItem]:
        """게시글 프리뷰 목록 조회 (Version 1.0)

        게시글 번호 목록을 받아 미리보기 정보를 조회합니다.
        한 번에 1~100개 조회 가능하며, content 는 최대 3000자까지 반환됩니다.

        Args:
            board_no: 게시판 번호(숫자) 또는 게시판 ID(문자열)
            request: 프리뷰 조회 조건 (postNos 등)

        Returns:
            list[PostPreviewItem]: 게시글 프리뷰 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.post(f"/boards/{board_no}/posts/previews", headers=headers, json=body)
            return self.handle_resp(resp, list[PostPreviewItem])

    # ------------------------------------
    #  Holiday (공휴일)
    # ------------------------------------
    async def search_holiday(
        self,
        year: int | None = None,
        month: int | None = None,
    ) -> list[int]:
        """요청한 달에 해당하는 공휴일 조회하기 (Version 1.0)

        해당 연도와 월에 존재하는 공휴일(일자) 목록을 조회합니다.

        Args:
            year: 검색할 연도
            month: 검색할 월

        Returns:
            list[int]: 공휴일 일자 목록 (예: [5, 6, 12, ...])
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, int] = {}
            if year is not None:
                params["year"] = year
            if month is not None:
                params["month"] = month

            resp = await client.get("/holiday", headers=headers, params=params)
            return self.handle_resp(resp, list[int])

    # ------------------------------------
    #  Inquiry (1:1 문의)
    # ------------------------------------
    async def get_inquiry_configuration(self) -> InquiryConfigurationResponse:
        """1:1 문의 설정 조회하기 (Version 1.0)

        Returns:
            InquiryConfigurationResponse: 1:1 문의 설정
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get("/inquiries/configurations", headers=headers)
            return self.handle_resp(resp, InquiryConfigurationResponse)

    async def get_inquiry_types(
        self,
        direction: InquiryTypeDirection | None = None,
    ) -> list[InquiryType]:
        """1:1 문의 유형 조회 (Version 1.0)

        Args:
            direction: 정렬방식 (ADMIN, CREATED_ASC, CREATED_DESC; default: ADMIN)

        Returns:
            list[InquiryType]: 1:1 문의 유형 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {}
            if direction is not None:
                params["direction"] = direction

            resp = await client.get("/inquiries/types", headers=headers, params=params)
            return self.handle_resp(resp, list[InquiryType])

    # ------------------------------------
    #  Instagram
    # ------------------------------------
    async def get_instagram_media(self) -> InstagramMediaResponse:
        """instagram 피드(게시글 목록) 조회하기 (Version 1.0)

        해당 쇼핑몰의 인스타그램 게시글 목록을 조회합니다.
        조회 중 에러 발생 시 error 필드에 에러 정보가 포함됩니다.

        Returns:
            InstagramMediaResponse: 인스타그램 미디어 목록 (data, error)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get("/shopby/instagram/media", headers=headers)
            return self.handle_resp(resp, InstagramMediaResponse)

    # ------------------------------------
    #  Page (외부 스크립트)
    # ------------------------------------
    async def search_external_script(
        self,
        page_types: list[str],
    ) -> list[ExternalScriptItem]:
        """외부스크립트 조회하기 (Version 1.0)

        Args:
            page_types: 페이지 타입 리스트 (MAIN, COMMON_HEAD, CART 등)

        Returns:
            list[ExternalScriptItem]: 외부 스크립트 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {"pageTypes": ",".join(page_types)}

            resp = await client.get("/page/scripts", headers=headers, params=params)
            return self.handle_resp(resp, list[ExternalScriptItem])

    # ------------------------------------
    #  Terms (약관)
    # ------------------------------------
    async def search_used_terms(
        self,
        terms_types: list[TermsType],
        used_only: bool | None = None,
    ) -> UsedTermsResponse:
        """적용 중인 몰 약관 조회하기 (Version 1.0)

        SA에서 노출 설정된 약관만 포함됩니다.

        Args:
            terms_types: 조회할 약관 타입 리스트
            used_only: 사용중인 약관만 노출 여부 (default: false)

        Returns:
            UsedTermsResponse: {약관타입: 약관 본문} 맵
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | bool] = {"termsTypes": ",".join(terms_types)}
            if used_only is not None:
                params["usedOnly"] = used_only

            resp = await client.get("/terms", headers=headers, params=params)
            return self.handle_resp(resp, UsedTermsResponse)

    async def post_search_used_terms(
        self,
        request: PostUsedTermsRequest,
    ) -> UsedTermsResponse:
        """적용 중인 몰 약관 조회하기 (ver 1.1) (Version 1.1)

        replacementPhrase 에 [key:value] 형태로 치환 문구를 전달할 수 있습니다.

        Args:
            request: 약관 조회 조건 (termsType, replacementPhrase, usedOnly)

        Returns:
            UsedTermsResponse: {약관타입: 약관 본문} 맵
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.1"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.post("/terms", headers=headers, json=body)
            return self.handle_resp(resp, UsedTermsResponse)

    async def get_custom_terms(
        self,
        request: CustomTermsRequest,
    ) -> list[CustomTermsItem]:
        """추가 약관 조회하기 (Version 1.0)

        Args:
            request: 추가 약관 조회 조건 (customCategoryType, replacementPhrase)

        Returns:
            list[CustomTermsItem]: 추가 약관 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.post("/terms/custom", headers=headers, json=body)
            return self.handle_resp(resp, list[CustomTermsItem])

    async def search_terms_histories(
        self,
        terms_type: TermsType,
        future_days_to_show: str | None = None,
    ) -> list[TermsHistoryItem]:
        """약관 변경이력 조회하기 (Version 1.0)

        Args:
            terms_type: 조회할 약관 타입 (USE, E_COMMERCE, PI_PROCESS 등)
            future_days_to_show: 조회할 현재부터 미래 날짜

        Returns:
            list[TermsHistoryItem]: 약관 변경이력 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {"termsType": terms_type}
            if future_days_to_show is not None:
                params["futureDaysToShow"] = future_days_to_show

            resp = await client.get("/terms/history", headers=headers, params=params)
            return self.handle_resp(resp, list[TermsHistoryItem])

    async def search_used_terms_only_used(
        self,
        terms_types: list[TermsType],
    ) -> UsedTermsTypesResponse:
        """적용 중인 몰 약관 조회하기 (현재 적용중인 약관타입만) (Version 1.0)

        Args:
            terms_types: 조회할 약관 타입 리스트

        Returns:
            UsedTermsTypesResponse: 적용 중인 약관 타입 리스트 (termsList)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {"termsTypes": ",".join(terms_types)}

            resp = await client.get("/terms/used", headers=headers, params=params)
            return self.handle_resp(resp, UsedTermsTypesResponse)

    async def get_term(self, terms_no: int) -> TermsDetailResponse:
        """약관 상세 조회하기 (Version 1.0)

        Args:
            terms_no: 약관 번호

        Returns:
            TermsDetailResponse: 약관 상세
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get(f"/terms/{terms_no}", headers=headers)
            return self.handle_resp(resp, TermsDetailResponse)

    async def post_terms(
        self,
        terms_no: int,
        request: PostTermsDetailRequest | None = None,
    ) -> TermsDetailResponse:
        """약관 상세 조회하기 (ver 1.1) (Version 1.1)

        replacementPhrase 에 [key:value] 형태로 치환 문구를 전달할 수 있습니다.

        Args:
            terms_no: 약관 번호
            request: 치환 문구 등 조회 조건 (선택)

        Returns:
            TermsDetailResponse: 약관 상세
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.1"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json") if request is not None else {}

            resp = await client.post(f"/terms/{terms_no}", headers=headers, json=body)
            return self.handle_resp(resp, TermsDetailResponse)

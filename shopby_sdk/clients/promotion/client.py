"""Promotion(쿠폰) API 클라이언트"""

from datetime import date

import httpx

from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.promotion.models import (
    CouponDetailResponse,
    CouponIssueSearchDateType,
    CouponSearchDateType,
    CouponSearchKeywordType,
    CouponStatusType,
    CouponTargetsResponse,
    CouponType,
    CouponUseSearchDateType,
    CouponUseSearchKeywordType,
    CreateCouponRequest,
    CreateCouponResponse,
    IssueCouponRequest,
    IssueCouponResult,
    IssueType,
    RollbackCouponRequest,
    SearchCouponIssueResponse,
    SearchCouponResponse,
    UpdateCouponRequest,
    UsedCouponContent,
    UseCouponItem,
    UseStopCouponRequest,
    WithdrawCouponBulkRequest,
    WithdrawCouponRequest,
)


class ShopbyServerPromotionApiClient(ShopbyServerApiClient):
    """Shopby Promotion Server API 클라이언트 (쿠폰)"""

    # ------------------------------------
    #  Coupon
    # ------------------------------------
    async def search_coupons(
        self,
        page: int,
        size: int,
        search_date_type: CouponSearchDateType,
        start_ymd: date,
        end_ymd: date,
        issue_type: IssueType | None = None,
        coupon_type: CouponType | None = None,
        status_types: list[CouponStatusType] | None = None,
        search_keyword_type: CouponSearchKeywordType | None = None,
        keyword: str | None = None,
        coupon_nos: list[int] | None = None,
        except_issue_end_coupon: bool | None = None,
        member_grade_no: int | None = None,
        member_group_no: int | None = None,
    ) -> SearchCouponResponse:
        """쿠폰 검색하기

        검색 조건을 기반으로 쇼핑몰이 가지고 있는 쿠폰 정보를 검색합니다.

        Args:
            page: 페이지 번호 (1 이상)
            size: 페이지 크기
            search_date_type: 날짜 검색 타입
            start_ymd: 조회 시작일
            end_ymd: 조회 종료일
            issue_type: 쿠폰 발급 타입
            coupon_type: 혜택 구분 타입
            status_types: 쿠폰 상태 타입 리스트
            search_keyword_type: 검색어 타입
            keyword: 검색어
            coupon_nos: 쿠폰번호 리스트
            except_issue_end_coupon: 사용불가 쿠폰 제외 여부
            member_grade_no: 회원 등급 번호
            member_group_no: 회원 그룹 번호

        Returns:
            SearchCouponResponse: 쿠폰 검색 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int | bool] = {
                "page": page,
                "size": size,
                "searchDateType": search_date_type,
                "startYmd": start_ymd.strftime("%Y-%m-%d"),
                "endYmd": end_ymd.strftime("%Y-%m-%d"),
            }

            if issue_type is not None:
                params["issueType"] = issue_type
            if coupon_type is not None:
                params["couponType"] = coupon_type
            if status_types is not None:
                params["statusTypes"] = ",".join(status_types)
            if search_keyword_type is not None:
                params["searchKeywordType"] = search_keyword_type
            if keyword is not None:
                params["keyword"] = keyword
            if coupon_nos is not None:
                params["couponNos"] = ",".join(str(no) for no in coupon_nos)
            if except_issue_end_coupon is not None:
                params["exceptIssueEndCoupon"] = except_issue_end_coupon
            if member_grade_no is not None:
                params["memberGradeNo"] = member_grade_no
            if member_group_no is not None:
                params["memberGroupNo"] = member_group_no

            resp = await client.get("/coupons", headers=headers, params=params)
            return self.handle_resp(resp, SearchCouponResponse)

    async def create_coupon(self, request: CreateCouponRequest) -> CreateCouponResponse:
        """쿠폰 생성하기

        쿠폰을 신규 생성합니다.

        Args:
            request: 쿠폰 생성 요청

        Returns:
            CreateCouponResponse: 생성된 쿠폰 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.post("/coupons", headers=headers, json=body)
            return self.handle_resp(resp, CreateCouponResponse)

    async def get_coupon_exclude_targets(
        self,
        coupon_nos: list[int] | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> CouponTargetsResponse:
        """쿠폰의 제외 대상 조회

        쿠폰 번호를 입력받아 쿠폰의 제외 대상을 조회합니다.
        쿠폰 번호를 입력하지 않는 경우, 해당 쇼핑몰 전체를 대상으로 조회합니다.

        Args:
            coupon_nos: 쿠폰 번호 목록
            page: 페이지 번호 (1 이상)
            size: 페이지 크기

        Returns:
            CouponTargetsResponse: 제외 대상 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int | bool] = {}
            if coupon_nos is not None:
                params["couponNos"] = ",".join(str(no) for no in coupon_nos)
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size

            resp = await client.get("/coupons/exclude-targets", headers=headers, params=params)
            return self.handle_resp(resp, CouponTargetsResponse)

    async def search_coupon_issues(
        self,
        search_date_type: CouponIssueSearchDateType,
        start_ymd: date,
        end_ymd: date,
        page: int,
        size: int,
        member_nos: list[int] | None = None,
        member_ids: list[str] | None = None,
        coupon_nos: list[int] | None = None,
        coupon_issue_nos: list[int] | None = None,
    ) -> SearchCouponIssueResponse:
        """지급된 쿠폰 검색하기

        회원에게 지급된 쿠폰 정보를 조회합니다.
        memberNos, memberIds, couponNos, couponIssueNos 중 적어도 하나는 필수입니다.
        (단, searchDateType이 USE_END_YMD인 경우 생략 가능)

        Args:
            search_date_type: 날짜검색타입
            start_ymd: 조회 시작일
            end_ymd: 조회 종료일
            page: 페이지 번호
            size: 페이지 크기 (최대 10,000)
            member_nos: 회원 번호 목록
            member_ids: 회원 ID 목록
            coupon_nos: 쿠폰 번호 목록
            coupon_issue_nos: 쿠폰 지급 번호 목록

        Returns:
            SearchCouponIssueResponse: 지급된 쿠폰 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int | bool] = {
                "searchDateType": search_date_type,
                "startYmd": start_ymd.strftime("%Y-%m-%d"),
                "endYmd": end_ymd.strftime("%Y-%m-%d"),
                "page": page,
                "size": size,
            }

            if member_nos is not None:
                params["memberNos"] = ",".join(str(no) for no in member_nos)
            if member_ids is not None:
                params["memberIds"] = ",".join(member_ids)
            if coupon_nos is not None:
                params["couponNos"] = ",".join(str(no) for no in coupon_nos)
            if coupon_issue_nos is not None:
                params["couponIssueNos"] = ",".join(str(no) for no in coupon_issue_nos)

            resp = await client.get("/coupons/issues", headers=headers, params=params)
            return self.handle_resp(resp, SearchCouponIssueResponse)

    async def issue_coupons(self, request: IssueCouponRequest) -> list[IssueCouponResult]:
        """회원번호와 쿠폰번호로 쿠폰 발급하기

        회원정보, 쿠폰번호를 기반으로 쿠폰을 발행합니다.
        memberNos와 memberIds는 동시 요청 시 400 error가 발생합니다.
        입력가능한 회원수는 최대 1000명, 쿠폰수는 최대 10개입니다.

        Args:
            request: 쿠폰 발급 요청

        Returns:
            list[IssueCouponResult]: 발급 결과 리스트
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.post("/coupons/issues", headers=headers, json=body)
            return self.handle_resp(resp, list[IssueCouponResult])

    async def get_coupon_targets(
        self,
        coupon_nos: list[int] | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> CouponTargetsResponse:
        """쿠폰의 대상 조회

        쿠폰 번호를 입력받아 쿠폰의 대상을 조회합니다.
        쿠폰 번호를 입력하지 않는 경우, 해당 쇼핑몰 전체를 대상으로 조회합니다.

        Args:
            coupon_nos: 쿠폰 번호 목록
            page: 페이지 번호 (1 이상)
            size: 페이지 크기

        Returns:
            CouponTargetsResponse: 대상 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int | bool] = {}
            if coupon_nos is not None:
                params["couponNos"] = ",".join(str(no) for no in coupon_nos)
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size

            resp = await client.get("/coupons/targets", headers=headers, params=params)
            return self.handle_resp(resp, CouponTargetsResponse)

    async def withdraw_coupon(self, request: WithdrawCouponRequest) -> None:
        """쿠폰 철회

        쿠폰 지급 번호를 입력받아 발급된 쿠폰을 철회합니다.
        `사용 가능` 상태인 쿠폰이면 발급된 위치에 상관없이 철회할 수 있습니다.

        Args:
            request: 쿠폰 철회 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.put("/coupons/withdraw", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def withdraw_coupons_bulk(self, request: WithdrawCouponBulkRequest) -> None:
        """쿠폰 번호로 쿠폰 지급 철회하기 (bulk)

        입력받은 쿠폰번호로 지급된 모든 쿠폰을 철회합니다.
        10만건 이상은 해당 api 사용하지 마시고 1:1 문의 요청 바랍니다.

        Args:
            request: 쿠폰 지급 철회(bulk) 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.put("/coupons/withdraw-bulk", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def get_coupon(self, coupon_no: int) -> CouponDetailResponse:
        """쿠폰 정보 조회하기

        하나의 쿠폰에 대한 상세 정보를 조회합니다.

        Args:
            coupon_no: 쿠폰 번호

        Returns:
            CouponDetailResponse: 쿠폰 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get(f"/coupons/{coupon_no}", headers=headers)
            return self.handle_resp(resp, CouponDetailResponse)

    async def update_coupon(self, coupon_no: int, request: UpdateCouponRequest) -> None:
        """쿠폰 수정하기

        쿠폰 상세 정보를 수정합니다. 발행 전/후 수정할 수 있는 항목이 다릅니다.

        Args:
            coupon_no: 쿠폰 번호
            request: 쿠폰 수정 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.put(f"/coupons/{coupon_no}", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def use_stop_coupon(self, coupon_no: str, request: UseStopCouponRequest) -> None:
        """쿠폰 사용 중지/재개

        쿠폰을 사용 중지 또는 재개 처리 합니다.

        Args:
            coupon_no: 쿠폰 번호
            request: 사용 중지/재개 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.put(f"/coupons/{coupon_no}/use-stop", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  CouponUse
    # ------------------------------------
    async def search_used_coupons(
        self,
        keyword: str,
        search_keyword_type: CouponUseSearchKeywordType,
        page: int,
        size: int,
        search_date_type: CouponUseSearchDateType | None = None,
        start_ymd: date | None = None,
        end_ymd: date | None = None,
    ) -> list[UsedCouponContent]:
        """사용된 쿠폰 정보 검색하기

        이미 사용된 쿠폰 정보를 검색합니다.

        Args:
            keyword: 검색어
            search_keyword_type: 검색어타입 (ORDER_NO, COUPON_NO)
            page: 페이지 번호 (1 이상)
            size: 페이지 사이즈
            search_date_type: 날짜 검색 타입 (ISSUE_YMD, USE_YMD)
            start_ymd: 검색 시작일
            end_ymd: 검색 종료일

        Returns:
            list[UsedCouponContent]: 사용된 쿠폰 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int | bool] = {
                "keyword": keyword,
                "searchKeywordType": search_keyword_type,
                "page": page,
                "size": size,
            }

            if search_date_type is not None:
                params["searchDateType"] = search_date_type
            if start_ymd is not None:
                params["startYmd"] = start_ymd.strftime("%Y-%m-%d")
            if end_ymd is not None:
                params["endYmd"] = end_ymd.strftime("%Y-%m-%d")

            resp = await client.get("/coupons/use", headers=headers, params=params)
            return self.handle_resp(resp, list[UsedCouponContent])

    async def use_coupons(self, items: list[UseCouponItem]) -> None:
        """쿠폰 사용하기

        발급된 쿠폰을 사용처리하여 이후에 주문에 사용하지 못하도록 할 때 사용합니다.

        Args:
            items: 사용 처리할 쿠폰 리스트
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [item.model_dump(by_alias=True, exclude_none=True) for item in items]

            resp = await client.post("/coupons/use", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def rollback_coupon_use(self, request: RollbackCouponRequest) -> None:
        """쿠폰 취소하기(오프라인 전용)

        Args:
            request: 쿠폰 취소 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.post("/coupons/use/rollback", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

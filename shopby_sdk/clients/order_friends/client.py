"""Order Friends API 클라이언트

주문과 관련된 부가 기능(통계, 정산, CS 등)을 수행하는 server API 클라이언트
"""

from datetime import date

import httpx

from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.order_friends.models import (
    CouponType,
    CsResponse,
    GenderType,
    MemberJoinType,
    MemberType,
    OrdersSalesResponse,
    PayType,
    PlatformType,
    ProductKeywordType,
    ProductType,
    PromotionKeywordType,
    SaleMethodType,
    SettlementDetailResponse,
    SettlementItem,
    SettlementPartnerType,
    StatisticsPromotionDetailItem,
    StatisticsPromotionsResponse,
    StatisticsSalesPeriodResponse,
    StatisticsSalesProductResponse,
    StatisticsSalesSummaryResponse,
)


class ShopbyServerOrderFriendsApiClient(ShopbyServerApiClient):
    """Shopby Order Friends Server API 클라이언트 (통계/정산/CS)"""

    async def get_cs(
        self,
        order_no: int | None = None,
        cs_nos: list[int] | None = None,
        start_ymd: date | None = None,
        end_ymd: date | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> CsResponse:
        """
        CS 처리내역 조회

        Args:
            order_no: 주문번호
            cs_nos: CS 번호 리스트
            start_ymd: 조회 시작 일자 (기본값: 3개월 전)
            end_ymd: 조회 종료 일자 (기본값: 오늘)
            page: 페이지 번호 (기본값: 1)
            size: 페이지 크기 (기본값: 30)

        Returns:
            CsResponse: CS 처리내역 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}

            if order_no is not None:
                params["orderNo"] = order_no
            if cs_nos is not None:
                params["csNos"] = ",".join(str(no) for no in cs_nos)
            if start_ymd is not None:
                params["startYmd"] = start_ymd.strftime("%Y-%m-%d")
            if end_ymd is not None:
                params["endYmd"] = end_ymd.strftime("%Y-%m-%d")
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size

            resp = await client.get("/cs", headers=headers, params=params)
            return self.handle_resp(resp, CsResponse)

    async def get_orders_sales(
        self,
        start_ymd: date,
        end_ymd: date,
        includes_delivery_amt: bool,
        page: int,
        size: int,
    ) -> OrdersSalesResponse:
        """
        쇼핑몰 정산(매출) 데이터 조회하기

        Args:
            start_ymd: 조회 시작일
            end_ymd: 조회 종료일
            includes_delivery_amt: 배송비 매출 포함 여부
            page: 페이지 번호
            size: 페이지 사이즈

        Returns:
            OrdersSalesResponse: 쇼핑몰 매출 데이터 (totalCount, items)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "startYmd": start_ymd.strftime("%Y-%m-%d"),
                "endYmd": end_ymd.strftime("%Y-%m-%d"),
                "includesDeliveryAmt": includes_delivery_amt,
                "page": page,
                "size": size,
            }

            resp = await client.get("/orders/sales", headers=headers, params=params)
            return self.handle_resp(resp, OrdersSalesResponse)

    async def get_settlement(
        self,
        year: int,
        month: int,
        settlement_partner_type: SettlementPartnerType | None = None,
    ) -> list[SettlementItem]:
        """
        파트너 정산 데이터 조회하기

        Args:
            year: 연도
            month: 월
            settlement_partner_type: 파트너 구분 (DOMESTIC: 국내파트너, OVERSEAS: 해외파트너)

        Returns:
            list[SettlementItem]: 파트너 정산 데이터 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "year": year,
                "month": month,
            }
            if settlement_partner_type is not None:
                params["settlementPartnerType"] = settlement_partner_type

            resp = await client.get("/settlement", headers=headers, params=params)
            return self.handle_resp(resp, list[SettlementItem])

    async def get_settlement_detail(
        self,
        start_ymd: date,
        end_ymd: date,
        page: int,
        size: int,
        settlement_partner_type: SettlementPartnerType | None = None,
    ) -> SettlementDetailResponse:
        """
        파트너 정산 상세 데이터 조회하기 v1.1

        Args:
            start_ymd: 시작일
            end_ymd: 종료일
            page: 검색할 페이지 번호
            size: 1회에 조회할 데이터 개수 (default: 100)
            settlement_partner_type: 파트너 구분 (DOMESTIC: 국내파트너, OVERSEAS: 해외파트너)

        Returns:
            SettlementDetailResponse: 정산 상세 데이터 (totalCount, totalPage, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.1"}
            params: dict[str, str | int | bool] = {
                "startYmd": start_ymd.strftime("%Y-%m-%d"),
                "endYmd": end_ymd.strftime("%Y-%m-%d"),
                "page": page,
                "size": size,
            }
            if settlement_partner_type is not None:
                params["settlementPartnerType"] = settlement_partner_type

            resp = await client.get("/settlement/detail", headers=headers, params=params)
            return self.handle_resp(resp, SettlementDetailResponse)

    async def get_statistics_promotions(
        self,
        coupon_type: list[CouponType],
        start_ymd: date,
        end_ymd: date,
        page: int,
        size: int,
        display_brand_no: int | None = None,
        gender_types: list[GenderType] | None = None,
        includes_claim: bool | None = None,
        keyword: str | None = None,
        member_grade_no: int | None = None,
        member_group_no: int | None = None,
        member_join_type: list[MemberJoinType] | None = None,
        member_type: list[MemberType] | None = None,
        partner_no: int | None = None,
        platform_types: list[PlatformType] | None = None,
        promotion_keyword_type: PromotionKeywordType | None = None,
    ) -> StatisticsPromotionsResponse:
        """
        프로모션 통계 - 쿠폰 내역 조회

        Args:
            coupon_type: 쿠폰 타입 리스트 (PRODUCT, CART, GIFT)
            start_ymd: 조회시작일
            end_ymd: 조회종료일
            page: 페이지 번호
            size: 페이지 사이즈
            display_brand_no: 전시브랜드 번호
            gender_types: 회원 성별 리스트
            includes_claim: 클레임 포함 여부
            keyword: 단일 검색어
            member_grade_no: 회원 등급
            member_group_no: 회원 그룹
            member_join_type: 회원 구분 리스트 (MEMBER, NON_MEMBER)
            member_type: 회원 가입유형 리스트
            partner_no: 파트너번호
            platform_types: 플랫폼구분 리스트
            promotion_keyword_type: 프로모션 검색 키워드 타입 (NO, NAME, REGISTRANT)

        Returns:
            StatisticsPromotionsResponse: 프로모션 통계 쿠폰 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "couponType": ",".join(coupon_type),
                "startYmd": start_ymd.strftime("%Y-%m-%d"),
                "endYmd": end_ymd.strftime("%Y-%m-%d"),
                "page": page,
                "size": size,
            }
            if display_brand_no is not None:
                params["displayBrandNo"] = display_brand_no
            if gender_types is not None:
                params["genderTypes"] = ",".join(gender_types)
            if includes_claim is not None:
                params["includesClaim"] = includes_claim
            if keyword is not None:
                params["keyword"] = keyword
            if member_grade_no is not None:
                params["memberGradeNo"] = member_grade_no
            if member_group_no is not None:
                params["memberGroupNo"] = member_group_no
            if member_join_type is not None:
                params["memberJoinType"] = ",".join(member_join_type)
            if member_type is not None:
                params["memberType"] = ",".join(member_type)
            if partner_no is not None:
                params["partnerNo"] = partner_no
            if platform_types is not None:
                params["platformTypes"] = ",".join(platform_types)
            if promotion_keyword_type is not None:
                params["promotionKeywordType"] = promotion_keyword_type

            resp = await client.get("/statistics/promotions", headers=headers, params=params)
            return self.handle_resp(resp, StatisticsPromotionsResponse)

    async def get_statistics_promotions_detail(
        self,
        coupon_type: list[CouponType],
        start_ymd: date,
        end_ymd: date,
        page: int,
        size: int,
        display_brand_no: int | None = None,
        gender_types: list[GenderType] | None = None,
        includes_claim: bool | None = None,
        keyword: str | None = None,
        member_grade_no: int | None = None,
        member_group_no: int | None = None,
        member_join_type: list[MemberJoinType] | None = None,
        member_type: list[MemberType] | None = None,
        partner_no: int | None = None,
        platform_types: list[PlatformType] | None = None,
        promotion_keyword_type: PromotionKeywordType | None = None,
    ) -> list[StatisticsPromotionDetailItem]:
        """
        프로모션 통계 - 쿠폰 판매 현황 상세 조회

        Args:
            coupon_type: 쿠폰 타입 리스트 (PRODUCT, CART, GIFT)
            start_ymd: 조회시작일
            end_ymd: 조회종료일
            page: 페이지 번호
            size: 페이지 사이즈
            display_brand_no: 전시브랜드 번호
            gender_types: 회원 성별 리스트
            includes_claim: 클레임 포함 여부
            keyword: 단일 검색어
            member_grade_no: 회원 등급
            member_group_no: 회원 그룹
            member_join_type: 회원 구분 리스트 (MEMBER, NON_MEMBER)
            member_type: 회원 가입유형 리스트
            partner_no: 파트너번호
            platform_types: 플랫폼구분 리스트
            promotion_keyword_type: 프로모션 검색 키워드 타입 (NO, NAME, REGISTRANT)

        Returns:
            list[StatisticsPromotionDetailItem]: 쿠폰 판매 현황 상세 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "couponType": ",".join(coupon_type),
                "startYmd": start_ymd.strftime("%Y-%m-%d"),
                "endYmd": end_ymd.strftime("%Y-%m-%d"),
                "page": page,
                "size": size,
            }
            if display_brand_no is not None:
                params["displayBrandNo"] = display_brand_no
            if gender_types is not None:
                params["genderTypes"] = ",".join(gender_types)
            if includes_claim is not None:
                params["includesClaim"] = includes_claim
            if keyword is not None:
                params["keyword"] = keyword
            if member_grade_no is not None:
                params["memberGradeNo"] = member_grade_no
            if member_group_no is not None:
                params["memberGroupNo"] = member_group_no
            if member_join_type is not None:
                params["memberJoinType"] = ",".join(member_join_type)
            if member_type is not None:
                params["memberType"] = ",".join(member_type)
            if partner_no is not None:
                params["partnerNo"] = partner_no
            if platform_types is not None:
                params["platformTypes"] = ",".join(platform_types)
            if promotion_keyword_type is not None:
                params["promotionKeywordType"] = promotion_keyword_type

            resp = await client.get("/statistics/promotions/detail", headers=headers, params=params)
            return self.handle_resp(resp, list[StatisticsPromotionDetailItem])

    @staticmethod
    def _build_sales_statistics_params(
        *,
        start_ymd: date,
        end_ymd: date,
        gender_types: list[GenderType],
        member_type: list[MemberType],
        platform_types: list[PlatformType],
        page: int,
        size: int,
        category_depth: int | None,
        category_no: int | None,
        display_brand_no: int | None,
        display_category_no: int | None,
        includes_claim: bool | None,
        keyword: str | None,
        keywords: list[str] | None,
        member_grade_no: int | None,
        member_group_no: int | None,
        member_join_type: list[MemberJoinType] | None,
        pay_type: PayType | None,
        pay_types: list[PayType] | None,
        product_keyword_type: ProductKeywordType | None,
        product_nos: list[int] | None,
        product_type: ProductType | None,
        sale_method_type: SaleMethodType | None,
        page_number: int | None,
        page_size: int | None,
    ) -> dict[str, str | int | bool]:
        """판매통계 API 공통 쿼리 파라미터 구성"""
        params: dict[str, str | int | bool] = {
            "startYmd": start_ymd.strftime("%Y-%m-%d"),
            "endYmd": end_ymd.strftime("%Y-%m-%d"),
            "genderTypes": ",".join(gender_types),
            "memberType": ",".join(member_type),
            "platformTypes": ",".join(platform_types),
            "page": page,
            "size": size,
        }
        if category_depth is not None:
            params["categoryDepth"] = category_depth
        if category_no is not None:
            params["categoryNo"] = category_no
        if display_brand_no is not None:
            params["displayBrandNo"] = display_brand_no
        if display_category_no is not None:
            params["displayCategoryNo"] = display_category_no
        if includes_claim is not None:
            params["includesClaim"] = includes_claim
        if keyword is not None:
            params["keyword"] = keyword
        if keywords is not None:
            params["keywords"] = ",".join(keywords)
        if member_grade_no is not None:
            params["memberGradeNo"] = member_grade_no
        if member_group_no is not None:
            params["memberGroupNo"] = member_group_no
        if member_join_type is not None:
            params["memberJoinType"] = ",".join(member_join_type)
        if pay_type is not None:
            params["payType"] = pay_type
        if pay_types is not None:
            params["payTypes"] = ",".join(pay_types)
        if product_keyword_type is not None:
            params["productKeywordType"] = product_keyword_type
        if product_nos is not None:
            params["productNos"] = ",".join(str(no) for no in product_nos)
        if product_type is not None:
            params["productType"] = product_type
        if sale_method_type is not None:
            params["saleMethodType"] = sale_method_type
        if page_number is not None:
            params["pageNumber"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size
        return params

    async def get_statistics_sales_period(
        self,
        start_ymd: date,
        end_ymd: date,
        gender_types: list[GenderType],
        member_type: list[MemberType],
        platform_types: list[PlatformType],
        page: int,
        size: int,
        category_depth: int | None = None,
        category_no: int | None = None,
        display_brand_no: int | None = None,
        display_category_no: int | None = None,
        includes_claim: bool | None = None,
        keyword: str | None = None,
        keywords: list[str] | None = None,
        member_grade_no: int | None = None,
        member_group_no: int | None = None,
        member_join_type: list[MemberJoinType] | None = None,
        pay_type: PayType | None = None,
        pay_types: list[PayType] | None = None,
        product_keyword_type: ProductKeywordType | None = None,
        product_nos: list[int] | None = None,
        product_type: ProductType | None = None,
        sale_method_type: SaleMethodType | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> StatisticsSalesPeriodResponse:
        """
        판매통계 기간별 목록 조회

        Args:
            start_ymd: 조회시작일
            end_ymd: 조회종료일
            gender_types: 회원 성별 리스트 (필수)
            member_type: 회원 가입유형 리스트 (필수)
            platform_types: 플랫폼구분 리스트 (필수)
            page: 페이지 번호 (1 이상)
            size: 페이지 사이즈
            category_depth: 검색될 카테고리 뎁스
            category_no: 카테고리 번호
            display_brand_no: 전시브랜드 번호
            display_category_no: 전시카테고리 번호
            includes_claim: 클레임 포함 여부
            keyword: 단일 검색어
            keywords: 복수 검색어 리스트
            member_grade_no: 회원 등급
            member_group_no: 회원 그룹
            member_join_type: 회원 구분 리스트 (MEMBER, NON_MEMBER)
            pay_type: 결제수단
            pay_types: 결제수단 리스트
            product_keyword_type: 상품 검색 키워드 타입 (NO, NAME, MANAGEMENT_CD)
            product_nos: 상품번호 목록
            product_type: 상품조회기준 (PRODUCT, OPTION)
            sale_method_type: 판매방식구분 (PURCHASE, CONSIGNMENT)
            page_number: 페이지 번호 (1 이상)
            page_size: 페이지 사이즈

        Returns:
            StatisticsSalesPeriodResponse: 판매통계 일자별 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = self._build_sales_statistics_params(
                start_ymd=start_ymd,
                end_ymd=end_ymd,
                gender_types=gender_types,
                member_type=member_type,
                platform_types=platform_types,
                page=page,
                size=size,
                category_depth=category_depth,
                category_no=category_no,
                display_brand_no=display_brand_no,
                display_category_no=display_category_no,
                includes_claim=includes_claim,
                keyword=keyword,
                keywords=keywords,
                member_grade_no=member_grade_no,
                member_group_no=member_group_no,
                member_join_type=member_join_type,
                pay_type=pay_type,
                pay_types=pay_types,
                product_keyword_type=product_keyword_type,
                product_nos=product_nos,
                product_type=product_type,
                sale_method_type=sale_method_type,
                page_number=page_number,
                page_size=page_size,
            )

            resp = await client.get("/statistics/sales/period", headers=headers, params=params)
            return self.handle_resp(resp, StatisticsSalesPeriodResponse)

    async def get_statistics_sales_product(
        self,
        start_ymd: date,
        end_ymd: date,
        gender_types: list[GenderType],
        member_type: list[MemberType],
        platform_types: list[PlatformType],
        page: int,
        size: int,
        category_depth: int | None = None,
        category_no: int | None = None,
        display_brand_no: int | None = None,
        display_category_no: int | None = None,
        includes_claim: bool | None = None,
        keyword: str | None = None,
        keywords: list[str] | None = None,
        member_grade_no: int | None = None,
        member_group_no: int | None = None,
        member_join_type: list[MemberJoinType] | None = None,
        pay_type: PayType | None = None,
        pay_types: list[PayType] | None = None,
        product_keyword_type: ProductKeywordType | None = None,
        product_nos: list[int] | None = None,
        product_type: ProductType | None = None,
        sale_method_type: SaleMethodType | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> StatisticsSalesProductResponse:
        """
        판매통계 상품별 목록 조회

        Args:
            start_ymd: 조회시작일
            end_ymd: 조회종료일
            gender_types: 회원 성별 리스트 (필수)
            member_type: 회원 가입유형 리스트 (필수)
            platform_types: 플랫폼구분 리스트 (필수)
            page: 페이지 번호 (1 이상)
            size: 페이지 사이즈
            category_depth: 검색될 카테고리 뎁스
            category_no: 카테고리 번호
            display_brand_no: 전시브랜드 번호
            display_category_no: 전시카테고리 번호
            includes_claim: 클레임 포함 여부
            keyword: 단일 검색어
            keywords: 복수 검색어 리스트
            member_grade_no: 회원 등급
            member_group_no: 회원 그룹
            member_join_type: 회원 구분 리스트 (MEMBER, NON_MEMBER)
            pay_type: 결제수단
            pay_types: 결제수단 리스트
            product_keyword_type: 상품 검색 키워드 타입 (NO, NAME, MANAGEMENT_CD)
            product_nos: 상품번호 목록
            product_type: 상품조회기준 (PRODUCT, OPTION) - 상품별 API 에서는 필수 권장
            sale_method_type: 판매방식구분 (PURCHASE, CONSIGNMENT)
            page_number: 페이지 번호 (1 이상)
            page_size: 페이지 사이즈

        Returns:
            StatisticsSalesProductResponse: 판매통계 상품별 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = self._build_sales_statistics_params(
                start_ymd=start_ymd,
                end_ymd=end_ymd,
                gender_types=gender_types,
                member_type=member_type,
                platform_types=platform_types,
                page=page,
                size=size,
                category_depth=category_depth,
                category_no=category_no,
                display_brand_no=display_brand_no,
                display_category_no=display_category_no,
                includes_claim=includes_claim,
                keyword=keyword,
                keywords=keywords,
                member_grade_no=member_grade_no,
                member_group_no=member_group_no,
                member_join_type=member_join_type,
                pay_type=pay_type,
                pay_types=pay_types,
                product_keyword_type=product_keyword_type,
                product_nos=product_nos,
                product_type=product_type,
                sale_method_type=sale_method_type,
                page_number=page_number,
                page_size=page_size,
            )

            resp = await client.get("/statistics/sales/product", headers=headers, params=params)
            return self.handle_resp(resp, StatisticsSalesProductResponse)

    async def get_statistics_sales_period_summary(
        self,
        start_ymd: date,
        end_ymd: date,
        gender_types: list[GenderType],
        member_type: list[MemberType],
        platform_types: list[PlatformType],
        page: int,
        size: int,
        category_depth: int | None = None,
        category_no: int | None = None,
        display_brand_no: int | None = None,
        display_category_no: int | None = None,
        includes_claim: bool | None = None,
        keyword: str | None = None,
        keywords: list[str] | None = None,
        member_grade_no: int | None = None,
        member_group_no: int | None = None,
        member_join_type: list[MemberJoinType] | None = None,
        pay_type: PayType | None = None,
        pay_types: list[PayType] | None = None,
        product_keyword_type: ProductKeywordType | None = None,
        product_nos: list[int] | None = None,
        product_type: ProductType | None = None,
        sale_method_type: SaleMethodType | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> StatisticsSalesSummaryResponse:
        """
        판매통계 기간별 요약 조회

        Args:
            start_ymd: 조회시작일
            end_ymd: 조회종료일
            gender_types: 회원 성별 리스트 (필수)
            member_type: 회원 가입유형 리스트 (필수)
            platform_types: 플랫폼구분 리스트 (필수)
            page: 페이지 번호 (1 이상)
            size: 페이지 사이즈
            category_depth: 검색될 카테고리 뎁스
            category_no: 카테고리 번호
            display_brand_no: 전시브랜드 번호
            display_category_no: 전시카테고리 번호
            includes_claim: 클레임 포함 여부
            keyword: 단일 검색어
            keywords: 복수 검색어 리스트
            member_grade_no: 회원 등급
            member_group_no: 회원 그룹
            member_join_type: 회원 구분 리스트 (MEMBER, NON_MEMBER)
            pay_type: 결제수단
            pay_types: 결제수단 리스트
            product_keyword_type: 상품 검색 키워드 타입 (NO, NAME, MANAGEMENT_CD)
            product_nos: 상품번호 목록
            product_type: 상품조회기준 (PRODUCT, OPTION)
            sale_method_type: 판매방식구분 (PURCHASE, CONSIGNMENT)
            page_number: 페이지 번호 (1 이상)
            page_size: 페이지 사이즈

        Returns:
            StatisticsSalesSummaryResponse: 판매통계 기간별 요약 (summary, promotionSummary)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = self._build_sales_statistics_params(
                start_ymd=start_ymd,
                end_ymd=end_ymd,
                gender_types=gender_types,
                member_type=member_type,
                platform_types=platform_types,
                page=page,
                size=size,
                category_depth=category_depth,
                category_no=category_no,
                display_brand_no=display_brand_no,
                display_category_no=display_category_no,
                includes_claim=includes_claim,
                keyword=keyword,
                keywords=keywords,
                member_grade_no=member_grade_no,
                member_group_no=member_group_no,
                member_join_type=member_join_type,
                pay_type=pay_type,
                pay_types=pay_types,
                product_keyword_type=product_keyword_type,
                product_nos=product_nos,
                product_type=product_type,
                sale_method_type=sale_method_type,
                page_number=page_number,
                page_size=page_size,
            )

            resp = await client.get(
                "/statistics/sales/period/summary", headers=headers, params=params
            )
            return self.handle_resp(resp, StatisticsSalesSummaryResponse)

    async def get_statistics_sales_product_summary(
        self,
        start_ymd: date,
        end_ymd: date,
        gender_types: list[GenderType],
        member_type: list[MemberType],
        platform_types: list[PlatformType],
        page: int,
        size: int,
        category_depth: int | None = None,
        category_no: int | None = None,
        display_brand_no: int | None = None,
        display_category_no: int | None = None,
        includes_claim: bool | None = None,
        keyword: str | None = None,
        keywords: list[str] | None = None,
        member_grade_no: int | None = None,
        member_group_no: int | None = None,
        member_join_type: list[MemberJoinType] | None = None,
        pay_type: PayType | None = None,
        pay_types: list[PayType] | None = None,
        product_keyword_type: ProductKeywordType | None = None,
        product_nos: list[int] | None = None,
        product_type: ProductType | None = None,
        sale_method_type: SaleMethodType | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> StatisticsSalesSummaryResponse:
        """
        판매통계 상품별 요약 조회

        Args:
            start_ymd: 조회시작일
            end_ymd: 조회종료일
            gender_types: 회원 성별 리스트 (필수)
            member_type: 회원 가입유형 리스트 (필수)
            platform_types: 플랫폼구분 리스트 (필수)
            page: 페이지 번호 (1 이상)
            size: 페이지 사이즈
            category_depth: 검색될 카테고리 뎁스
            category_no: 카테고리 번호
            display_brand_no: 전시브랜드 번호
            display_category_no: 전시카테고리 번호
            includes_claim: 클레임 포함 여부
            keyword: 단일 검색어
            keywords: 복수 검색어 리스트
            member_grade_no: 회원 등급
            member_group_no: 회원 그룹
            member_join_type: 회원 구분 리스트 (MEMBER, NON_MEMBER)
            pay_type: 결제수단
            pay_types: 결제수단 리스트
            product_keyword_type: 상품 검색 키워드 타입 (NO, NAME, MANAGEMENT_CD)
            product_nos: 상품번호 목록
            product_type: 상품조회기준 (PRODUCT, OPTION) - 상품별 API 에서는 필수 권장
            sale_method_type: 판매방식구분 (PURCHASE, CONSIGNMENT)
            page_number: 페이지 번호 (1 이상)
            page_size: 페이지 사이즈

        Returns:
            StatisticsSalesSummaryResponse: 판매통계 상품별 요약 (summary, promotionSummary)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = self._build_sales_statistics_params(
                start_ymd=start_ymd,
                end_ymd=end_ymd,
                gender_types=gender_types,
                member_type=member_type,
                platform_types=platform_types,
                page=page,
                size=size,
                category_depth=category_depth,
                category_no=category_no,
                display_brand_no=display_brand_no,
                display_category_no=display_category_no,
                includes_claim=includes_claim,
                keyword=keyword,
                keywords=keywords,
                member_grade_no=member_grade_no,
                member_group_no=member_group_no,
                member_join_type=member_join_type,
                pay_type=pay_type,
                pay_types=pay_types,
                product_keyword_type=product_keyword_type,
                product_nos=product_nos,
                product_type=product_type,
                sale_method_type=sale_method_type,
                page_number=page_number,
                page_size=page_size,
            )

            resp = await client.get(
                "/statistics/sales/product/summary", headers=headers, params=params
            )
            return self.handle_resp(resp, StatisticsSalesSummaryResponse)

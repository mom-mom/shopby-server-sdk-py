from typing import Literal

import httpx

from src.clients.base import ShopbyServerApiClient
from src.clients.products.models import (
    ChangedProductsResponse,
    ProductDetailV3Response,
    ProductListItem,
    ProductListSearchResponse,
    ProductSearchV2Response,
)


# shopby-docs/product-server-public.yml


class ShopbyServerProductApiClient(ShopbyServerApiClient):
    async def get_product_detail_v3(self, mall_product_no: int) -> ProductDetailV3Response:
        """
        상품 상세 조회하기 (Version 3.0)

        Args:
            mall_product_no: 상품번호

        Returns:
            ProductDetailV3Response: 상품 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 3.0 헤더 추가
            headers = {"version": "3.0"}

            resp = await client.get(
                f"/products/{mall_product_no}/",
                headers=headers,
            )
            resp.raise_for_status()

            return ProductDetailV3Response.model_validate(resp.json())

    async def search_products_v2(
        self,
        # Filter parameters
        keywords: str | None = None,
        delivery_condition_type: Literal["FREE", "CONDITIONAL", "FIXED_FEE"] | None = None,
        sale_status: str | None = None,
        soldout: bool | None = None,
        total_review_count: bool | None = None,
        family_malls: bool | None = None,
        product_management_cd: str | None = None,
        exclude_mall_product_no: int | None = None,
        include_mall_product_no: int | None = None,
        # Order parameters
        order_by: Literal["RECENT_PRODUCT", "SALE_YMD"] | None = None,
        order_direction: Literal["ASC", "DESC"] | None = None,
        soldout_place_end: bool | None = None,
        # Category and brand
        display_category_nos: str | None = None,
        display_brand_nos: str | None = None,
        partner_no: int | None = None,
        # Pagination
        page_number: int | None = None,
        page_size: int | None = None,
        search_after: str | None = None,
        # Options
        has_option_values: bool | None = None,
        shipping_area_type: Literal["PARTNER", "MALL"] | None = None,
        platform_type: Literal["PC", "MOBILE_WEB", "MOBILE"] | None = None,
        front_display: Literal["Y", "N", "ALL"] | None = None,
        url_direct_display: Literal["Y", "N", "ALL"] | None = None,
        # Date ranges
        registration_period_start_ymdt: str | None = None,
        registration_period_end_ymdt: str | None = None,
        modification_period_start_ymdt: str | None = None,
        modification_period_end_ymdt: str | None = None,
        # Status and method
        sale_setting_types: str | None = None,
        apply_status_type: str | None = None,
        sale_method_type: Literal["ALL", "PURCHASE", "CONSIGNMENT"] | None = None,
        # Stock range
        stock_range_type: Literal["ALL", "NONE", "EXIST", "EQ", "LT", "LE", "GT", "GE", "RANGE"] | None = None,
        stock_range_stock_cnt: int | None = None,
        stock_range_min_stock_cnt: int | None = None,
        stock_range_max_stock_cnt: int | None = None,
        # Other
        custom_property_value_nos: str | None = None,
        admin_no: int | None = None,
    ) -> ProductSearchV2Response:
        """
        상품 검색하기 version 2.0 (검색엔진)

        검색엔진을 사용하여 상품을 검색하는 API

        Args:
            keywords: 검색어(여러 검색어일 경우 space로 구분 AND 연산)
            delivery_condition_type: 배송비 타입
            sale_status: 판매 상태 (default: ONSALE)
            soldout: 품절 상품 포함 여부 (default: false)
            total_review_count: 총 상품평 수 포함 여부 (default: false)
            family_malls: 서비스에 계약된 모든 쇼핑몰 조회 여부 (default: false)
            product_management_cd: 판매자관리코드 같은 상품 검색
            exclude_mall_product_no: 조회시 제외할 상품번호
            include_mall_product_no: 조회할 상품번호
            order_by: 정렬 기준 (default: RECENT_PRODUCT)
            order_direction: 정렬 방향 (default: DESC)
            soldout_place_end: 품절상품 뒤로 배치 여부 (default: false)
            display_category_nos: 전시 카테고리 번호(여러개 일 경우 콤마 구분)
            display_brand_nos: 전시 브랜드 번호(여러개 일 경우 콤마 구분)
            partner_no: 파트너 번호(상품 공급업체 번호)
            page_number: 페이지 번호 (default: 1)
            page_size: 한 페이지당 노출 수 (최대 100)
            search_after: 검색 기준 값(lastId) - keySet search 용
            has_option_values: 목록에 옵션 value 포함 여부 (default: false)
            shipping_area_type: 배송 구분
            platform_type: 플랫폼 타입
            front_display: 전시 여부 (default: ALL)
            url_direct_display: 프론트 미노출 여부 (default: ALL)
            registration_period_start_ymdt: 등록일 - 시작일
            registration_period_end_ymdt: 등록일 - 종료일
            modification_period_start_ymdt: 수정일 - 시작일
            modification_period_end_ymdt: 수정일 - 종료일
            sale_setting_types: 판매설정타입 (콤마 구분)
            apply_status_type: 승인상태 (default: ALL)
            sale_method_type: 판매방식 (default: ALL)
            stock_range_type: 재고조건 - 재고 범위 종류
            stock_range_stock_cnt: 재고조건 - 재고 수
            stock_range_min_stock_cnt: 재고조건 - RANGE 일시 최소 수량
            stock_range_max_stock_cnt: 재고조건 - RANGE 일시 최대 수량
            custom_property_value_nos: 추가항목 (콤마 구분)
            admin_no: 담당자번호

        Returns:
            ProductSearchV2Response: 검색 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 2.0 헤더 추가
            headers = {"version": "2.0"}

            # 쿼리 파라미터 구성
            params: dict[str, str | int | bool] = {}

            # Filter parameters
            if keywords is not None:
                params["filter.keywords"] = keywords
            if delivery_condition_type is not None:
                params["filter.deliveryConditionType"] = delivery_condition_type
            if sale_status is not None:
                params["filter.saleStatus"] = sale_status
            if soldout is not None:
                params["filter.soldout"] = soldout
            if total_review_count is not None:
                params["filter.totalReviewCount"] = total_review_count
            if family_malls is not None:
                params["filter.familyMalls"] = family_malls
            if product_management_cd is not None:
                params["filter.productManagementCd"] = product_management_cd
            if exclude_mall_product_no is not None:
                params["filter.excludeMallProductNo"] = exclude_mall_product_no
            if include_mall_product_no is not None:
                params["filter.includeMallProductNo"] = include_mall_product_no

            # Order parameters
            if order_by is not None:
                params["order.by"] = order_by
            if order_direction is not None:
                params["order.direction"] = order_direction
            if soldout_place_end is not None:
                params["order.soldoutPlaceEnd"] = soldout_place_end

            # Category and brand
            if display_category_nos is not None:
                params["displayCategoryNos"] = display_category_nos
            if display_brand_nos is not None:
                params["displayBrandNos"] = display_brand_nos
            if partner_no is not None:
                params["partnerNo"] = partner_no

            # Pagination
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size
            if search_after is not None:
                params["searchAfter"] = search_after

            # Options
            if has_option_values is not None:
                params["hasOptionValues"] = has_option_values
            if shipping_area_type is not None:
                params["shippingAreaType"] = shipping_area_type
            if platform_type is not None:
                params["platformType"] = platform_type
            if front_display is not None:
                params["frontDisplay"] = front_display
            if url_direct_display is not None:
                params["urlDirectDisplay"] = url_direct_display

            # Date ranges
            if registration_period_start_ymdt is not None:
                params["registrationPeriod.startYmdt"] = registration_period_start_ymdt
            if registration_period_end_ymdt is not None:
                params["registrationPeriod.endYmdt"] = registration_period_end_ymdt
            if modification_period_start_ymdt is not None:
                params["modificationPeriod.startYmdt"] = modification_period_start_ymdt
            if modification_period_end_ymdt is not None:
                params["modificationPeriod.endYmdt"] = modification_period_end_ymdt

            # Status and method
            if sale_setting_types is not None:
                params["saleSettingTypes"] = sale_setting_types
            if apply_status_type is not None:
                params["applyStatusType"] = apply_status_type
            if sale_method_type is not None:
                params["saleMethodType"] = sale_method_type

            # Stock range
            if stock_range_type is not None:
                params["stockRange.type"] = stock_range_type
            if stock_range_stock_cnt is not None:
                params["stockRange.stockCnt"] = stock_range_stock_cnt
            if stock_range_min_stock_cnt is not None:
                params["stockRange.minStockCnt"] = stock_range_min_stock_cnt
            if stock_range_max_stock_cnt is not None:
                params["stockRange.maxStockCnt"] = stock_range_max_stock_cnt

            # Other
            if custom_property_value_nos is not None:
                params["customPropertyValueNos"] = custom_property_value_nos
            if admin_no is not None:
                params["adminNo"] = admin_no

            resp = await client.get(
                "/products/search/engine/",
                headers=headers,
                params=params,
            )
            resp.raise_for_status()

            return ProductSearchV2Response.model_validate(resp.json())

    async def get_changed_product_nos(
        self,
        as_of: str,
        sort_by: Literal["REGISTERED_AT", "UPDATED_AT"],
        size: int,
        direction: Literal["ASC", "DESC"] | None = None,
        including_stock_changes: bool | None = None,
        page: int | None = None,
        search_after: str | None = None,
    ) -> ChangedProductsResponse:
        """
        변경된 상품 번호 목록 조회

        조회 기준시점을 기준으로 이후에 등록/수정된 상품번호 목록을 조회

        Args:
            as_of: 조회 기준시점 (yyyy-MM-dd HH:mm:ss)
            sort_by: 정렬 기준 (REGISTERED_AT: 등록일, UPDATED_AT: 수정일)
            size: 페이지 사이즈
            direction: 정렬 방향 (ASC: 오름차순, DESC: 내림차순, default: ASC)
            including_stock_changes: 재고변경이력 포함여부 (default: true, 정렬기준이 UPDATED_AT 일때만 적용가능)
            page: 페이지 번호 (default: 1)
            search_after: 검색 기준 값(lastId) - keySet search 용, 정렬기준이 REGISTERED_AT 일때만 사용가능

        Returns:
            ChangedProductsResponse: 변경된 상품 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 1.0 헤더 추가
            headers = {"version": "1.0"}

            # 쿼리 파라미터 구성
            params: dict[str, str | int | bool] = {
                "asOf": as_of,
                "sortBy": sort_by,
                "size": size,
            }

            if direction is not None:
                params["direction"] = direction
            if including_stock_changes is not None:
                params["includingStockChanges"] = including_stock_changes
            if page is not None:
                params["page"] = page
            if search_after is not None:
                params["searchAfter"] = search_after

            resp = await client.get(
                "/products/changed",
                headers=headers,
                params=params,
            )
            resp.raise_for_status()

            return ChangedProductsResponse.model_validate(resp.json())

    async def search_products_by_list(
        self,
        product_nos: list[int],
        partner_no: int | None = None,
    ) -> ProductListSearchResponse:
        """
        상품 리스트로 상품 검색하기

        상품번호 목록으로 상품을 검색하는 API (최대 100개)

        Args:
            product_nos: 검색 할 상품 번호들 (예: [10001, 10002, 10003])
            partner_no: 파트너 번호 (자사파트너의 경우에만 사용 가능)

        Returns:
            ProductListSearchResponse: 상품 목록 (list)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 1.0 헤더 추가
            headers = {"version": "1.0"}

            # 쿼리 파라미터 구성
            params: dict[str, str | int] = {
                "productNos": ",".join(str(no) for no in product_nos),
            }

            if partner_no is not None:
                params["partnerNo"] = partner_no

            resp = await client.get(
                "/products/search-by-nos",
                headers=headers,
                params=params,
            )
            resp.raise_for_status()

            return [ProductListItem.model_validate(item) for item in resp.json()]

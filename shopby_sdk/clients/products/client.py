from datetime import datetime
from typing import Any, Literal

import httpx

from shopby_sdk.base.kst import to_kst_string
from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.products.models import (
    AddCustomPropertyMappingRequest,
    BrandDetailResponse,
    BrandTreeItem,
    ChangedProductsResponse,
    CreateBrandsRequest,
    CreateBrandsResponse,
    CreatePurchasePermissionRequest,
    CreatePurchasePermissionResponse,
    CustomPropertyItem,
    CustomPropertyMappingResponse,
    DeletedProductsResponse,
    DutyCategoryItem,
    GlobalNosByProductNosResponse,
    InspectionConfirmRequest,
    InspectionRejectRequest,
    InspectionResultResponse,
    InspectionViewResponse,
    InspectionWaitingResponse,
    LikeProductsResponse,
    ModifyBrandItem,
    NaverShoppingConfigRequest,
    OptionStocksResponse,
    PatchProductV2Request,
    ProductByStickersResponse,
    ProductDetailV1Response,
    ProductDetailV3Response,
    ProductExtraInfoItem,
    ProductGuideRequest,
    ProductHistoriesResponse,
    ProductHistoryItem,
    ProductListItem,
    ProductListSearchResponse,
    ProductNosByGlobalNosResponse,
    ProductOptionsResponse,
    ProductSearchResponse,
    ProductSearchV2Response,
    PartialQuickItem,
    PartialQuickResponse,
    PurchasePermissionItem,
    PurchasePermissionMemberInput,
    PutProductOptionsRequest,
    PutProductPartialRequest,
    PutProductStatusRequest,
    PutSaleAgreementRequest,
    PutSaleAgreementResponse,
    PutStockByOptionCodeRequest,
    PutStockByOptionCodeResponse,
    PutStockByOptionNoRequest,
    PutStockByOptionNoResponse,
    PutStockByProductCodeRequest,
    PutStockByProductCodeResponse,
    PutStockByProductNoRequest,
    PutStockByProductNoResponse,
    RequiredPropertiesResponse,
    ReservationInfoItem,
    SavedProductResponse,
    UpdatePurchasePermissionProductRequest,
)


# docs/api/product-server-public.yml


class ShopbyServerProductsApiClient(ShopbyServerApiClient):
    async def get_product_detail(self, mall_product_no: int) -> ProductDetailV1Response:
        """
        상품 상세 조회하기 (Version 1.0)

        Args:
            mall_product_no: 상품번호

        Returns:
            ProductDetailV1Response: 상품 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 1.0 헤더 추가
            headers = {"version": "1.0"}

            resp = await client.get(
                f"/products/{mall_product_no}",
                headers=headers,
            )

            return self.handle_resp(resp, ProductDetailV1Response)

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

            return self.handle_resp(resp, ProductDetailV3Response)

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
        registration_period_start_ymdt: datetime | None = None,
        registration_period_end_ymdt: datetime | None = None,
        modification_period_start_ymdt: datetime | None = None,
        modification_period_end_ymdt: datetime | None = None,
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
            sale_setting_types: 판매설정타입 (콤마 구분) Enum: [AVAILABLE_FOR_SALE: 판매가능, STOP_SELLING: 판매중지, PROHIBITION_SALE: 판매금지]
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
                params["registrationPeriod.startYmdt"] = to_kst_string(registration_period_start_ymdt)
            if registration_period_end_ymdt is not None:
                params["registrationPeriod.endYmdt"] = to_kst_string(registration_period_end_ymdt)
            if modification_period_start_ymdt is not None:
                params["modificationPeriod.startYmdt"] = to_kst_string(modification_period_start_ymdt)
            if modification_period_end_ymdt is not None:
                params["modificationPeriod.endYmdt"] = to_kst_string(modification_period_end_ymdt)

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

            return self.handle_resp(resp, ProductSearchV2Response)

    async def get_changed_product_nos(
        self,
        as_of: datetime,
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
            as_of: 조회 기준시점 (datetime 객체)
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
                "asOf": to_kst_string(as_of),
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

            return self.handle_resp(resp, ChangedProductsResponse)

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

            return self.handle_resp(resp, list[ProductListItem])

    async def patch_product_v2(
        self,
        product_no: int,
        request: PatchProductV2Request,
    ) -> None:
        """
        상품 부분 수정하기 (version 2.0)

        상품의 일부를 수정하는 API입니다.
        수정을 원하는 필드의 키와 값만 넣습니다.
        nullable 한 필드값에 null 값으로 요청하는 경우, null 값이 반영됩니다.

        주의사항:
        - 상품 부분 수정 API는 request body의 1depth를 기준으로 수정이 됩니다.
        - 예를 들어 상품 이미지(request body에서 `image.images`)를 수정하려고 하는 경우,
          수정하는 값(`image.images`) 외에 다른 값(`image.listImage`, `image.usesExternalImage` 등)은
          기존 값을 그대로 입력해야합니다.

        Args:
            product_no: 상품번호
            request: 수정할 상품 정보 (PatchProductV2Request)

        Returns:
            None (204 No Content)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 2.0 헤더 추가
            headers = {"version": "2.0"}

            # None 값을 제외하고 JSON 직렬화
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.patch(
                f"/products/{product_no}",
                headers=headers,
                json=body,
            )

            self.raise_for_status(resp)

    async def get_product_histories(
        self,
        product_no: int,
        partner_no: int | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> ProductHistoriesResponse:
        """
        상품 변경 히스토리 조회

        상품 변경 히스토리를 조회하는 API입니다.

        Args:
            product_no: 상품번호
            partner_no: 파트너 번호 (자사파트너의 경우에만 사용 가능)
            page: 페이지 번호 (default: 1)
            page_size: 한 페이지당 노출 수 (default: 30)

        Returns:
            ProductHistoriesResponse: 상품 변경 히스토리 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 1.0 헤더 추가
            headers = {"version": "1.0"}

            # 쿼리 파라미터 구성
            params: dict[str, int] = {}

            if partner_no is not None:
                params["partnerNo"] = partner_no
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size

            resp = await client.get(
                f"/products/{product_no}/histories",
                headers=headers,
                params=params,
            )

            return self.handle_resp(resp, list[ProductHistoryItem])

    # ------------------------------------------------------------------
    #  브랜드 (Brand)
    # ------------------------------------------------------------------
    async def get_brands(self) -> list[BrandTreeItem]:
        """브랜드 전체 조회하기 (트리 구조, version 2.0)"""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "2.0"}
            resp = await client.get("/brands", headers=headers)
            return self.handle_resp(resp, list[BrandTreeItem])

    async def get_brand_detail(self, display_brand_no: int) -> BrandDetailResponse:
        """브랜드 상세 조회하기

        Args:
            display_brand_no: 전시브랜드 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/brands/{display_brand_no}", headers=headers)
            return self.handle_resp(resp, BrandDetailResponse)

    async def create_brands(self, request: CreateBrandsRequest) -> CreateBrandsResponse:
        """브랜드 생성하기 (한 번에 최대 500개)

        Args:
            request: 생성할 브랜드 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/brands", headers=headers, json=body)
            return self.handle_resp(resp, CreateBrandsResponse)

    async def modify_brands(self, brands: list[ModifyBrandItem]) -> None:
        """브랜드 수정하기 (한 번에 최대 500개)

        Args:
            brands: 수정할 브랜드 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [b.model_dump(by_alias=True, exclude_none=True, mode="json") for b in brands]
            resp = await client.put("/brands", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def delete_brands(self, display_brand_nos: list[int]) -> None:
        """브랜드 삭제하기 (한 번에 최대 500개)

        Args:
            display_brand_nos: 삭제할 전시브랜드 번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"displayBrandNos": ",".join(str(no) for no in display_brand_nos)}
            resp = await client.delete("/brands", headers=headers, params=params)
            self.raise_for_status(resp)
            return None

    # ------------------------------------------------------------------
    #  상품 추가항목 (Custom Property)
    # ------------------------------------------------------------------
    async def get_custom_properties(self) -> list[CustomPropertyItem]:
        """상품 추가항목 전체 조회하기"""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/custom-properties", headers=headers)
            return self.handle_resp(resp, list[CustomPropertyItem])

    async def add_custom_property_mappings(
        self, product_no: int, request: AddCustomPropertyMappingRequest
    ) -> CustomPropertyMappingResponse:
        """상품 추가항목 매핑 추가

        Args:
            product_no: 상품번호
            request: 추가할 추가항목 값 번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post(
                f"/custom-properties/{product_no}/mappings", headers=headers, json=body
            )
            return self.handle_resp(resp, CustomPropertyMappingResponse)

    async def remove_custom_property_mappings(
        self, product_no: int, prop_value_nos: list[int]
    ) -> CustomPropertyMappingResponse:
        """상품 추가항목 매핑 삭제

        Args:
            product_no: 상품번호
            prop_value_nos: 삭제할 추가항목 값 번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"propValueNos": ",".join(str(no) for no in prop_value_nos)}
            resp = await client.delete(
                f"/custom-properties/{product_no}/mappings", headers=headers, params=params
            )
            return self.handle_resp(resp, CustomPropertyMappingResponse)

    # ------------------------------------------------------------------
    #  상품 정보 고시 항목 (Duty Category)
    # ------------------------------------------------------------------
    async def get_duty_categories(self) -> list[DutyCategoryItem]:
        """상품 정보 고시 항목 조회하기"""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/duty-categories", headers=headers)
            return self.handle_resp(resp, list[DutyCategoryItem])

    # ------------------------------------------------------------------
    #  회원이 좋아하는 상품 (Like Products)
    # ------------------------------------------------------------------
    async def get_like_products(
        self,
        mall_no: int,
        member_id: str,
        member_no: int,
        platform: Literal["PC", "MOBILE_WEB", "MOBILE"],
        has_total_count: bool,
        has_max_coupon_amt: bool,
        page_number: int,
        page_size: int,
    ) -> LikeProductsResponse:
        """회원이 좋아하는 상품목록 조회하기

        memberId와 memberNo 둘 중 하나 필수이며 memberId가 우선 적용됩니다.

        Args:
            mall_no: 몰 번호
            member_id: 회원 id
            member_no: 회원 번호
            platform: 플랫폼 타입
            has_total_count: 전체 상품 수 포함 여부
            has_max_coupon_amt: 최대쿠폰 할인가격 포함 여부
            page_number: 페이지 번호
            page_size: 한 페이지당 노출 수
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "mallNo": mall_no,
                "memberId": member_id,
                "memberNo": member_no,
                "platform": platform,
                "hasTotalCount": has_total_count,
                "hasMaxCouponAmt": has_max_coupon_amt,
                "pageNumber": page_number,
                "pageSize": page_size,
            }
            resp = await client.get("/like-products", headers=headers, params=params)
            return self.handle_resp(resp, LikeProductsResponse)

    # ------------------------------------------------------------------
    #  상품 조회 (관리코드/스티커/삭제/추가정보/글로벌 등)
    # ------------------------------------------------------------------
    async def get_products_by_management_code(
        self, product_management_cd: str, partner_no: int | None = None
    ) -> dict[str, Any]:
        """판매자 관리코드로 상품 조회하기

        응답은 상품 전체 객체(productDetailResponses)로 매우 방대하여 dict로 반환합니다.

        Args:
            product_management_cd: 상품 관리 코드
            partner_no: 파트너 번호 (자사파트너의 경우에만 사용 가능)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {"productManagementCd": product_management_cd}
            if partner_no is not None:
                params["partnerNo"] = partner_no
            resp = await client.get("/products", headers=headers, params=params)
            return self.handle_resp(resp, dict[str, Any])

    async def get_products_by_sticker_nos(
        self,
        sticker_nos: list[int],
        search_after: int,
        size: int | None = None,
    ) -> ProductByStickersResponse:
        """스티커 번호로 상품 정보 조회하기

        Args:
            sticker_nos: 스티커 번호 목록
            search_after: 검색 기준 값(response의 lastId)
            size: 조회할 상품 개수 (default: 10)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {
                "stickerNos": ",".join(str(no) for no in sticker_nos),
                "searchAfter": search_after,
            }
            if size is not None:
                params["size"] = size
            resp = await client.get("/products/by-stickers", headers=headers, params=params)
            return self.handle_resp(resp, ProductByStickersResponse)

    async def get_deleted_products(
        self,
        start_ymdt: datetime,
        end_ymdt: datetime,
        page: int | None = None,
        size: int | None = None,
        partner_no: int | None = None,
    ) -> DeletedProductsResponse:
        """삭제된 상품 정보 조회하기

        Args:
            start_ymdt: 조회기간 시작 범위
            end_ymdt: 조회기간 종료 범위
            page: 페이지 번호 (default: 1)
            size: 페이지 사이즈 (default: 10)
            partner_no: 파트너 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {
                "startYmdt": to_kst_string(start_ymdt),
                "endYmdt": to_kst_string(end_ymdt),
            }
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size
            if partner_no is not None:
                params["partnerNo"] = partner_no
            resp = await client.get("/products/deleted", headers=headers, params=params)
            return self.handle_resp(resp, DeletedProductsResponse)

    async def get_product_extra_infos(self, product_nos: list[int]) -> list[ProductExtraInfoItem]:
        """추가정보 조회하기

        Args:
            product_nos: 상품 번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"productNos": ",".join(str(no) for no in product_nos)}
            resp = await client.get("/products/extraInfo", headers=headers, params=params)
            return self.handle_resp(resp, list[ProductExtraInfoItem])

    async def get_product_nos_by_global_nos(
        self, global_product_nos: list[int]
    ) -> ProductNosByGlobalNosResponse:
        """글로벌 번호로 상품 번호 조회하기

        Args:
            global_product_nos: 글로벌 상품 번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"globalProductNos": ",".join(str(no) for no in global_product_nos)}
            resp = await client.get(
                "/products/global/by-global-nos", headers=headers, params=params
            )
            return self.handle_resp(resp, ProductNosByGlobalNosResponse)

    async def get_global_nos_by_product_nos(
        self, product_nos: list[int]
    ) -> GlobalNosByProductNosResponse:
        """상품 번호로 글로벌 번호 조회하기

        Args:
            product_nos: 상품 번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"productNos": ",".join(str(no) for no in product_nos)}
            resp = await client.get(
                "/products/global/by-product-nos", headers=headers, params=params
            )
            return self.handle_resp(resp, GlobalNosByProductNosResponse)

    async def get_reservation_infos_by_product_nos(
        self, product_nos: list[int]
    ) -> list[ReservationInfoItem]:
        """상품 번호 리스트로 예약배송 정보 벌크 조회 (최대 100개)

        Args:
            product_nos: 상품 번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"productNos": ",".join(str(no) for no in product_nos)}
            resp = await client.get("/products/reservation-infos", headers=headers, params=params)
            return self.handle_resp(resp, list[ReservationInfoItem])

    async def get_required_properties(self) -> RequiredPropertiesResponse:
        """필수 항목 조회하기"""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/products/required-properties", headers=headers)
            return self.handle_resp(resp, RequiredPropertiesResponse)

    async def search_products(
        self,
        size: int,
        page: int | None = None,
        partner_no: int | None = None,
        search_after: int | None = None,
    ) -> ProductSearchResponse:
        """상품 검색하기

        Args:
            size: 페이지 사이즈 (default: 20)
            page: 페이지 번호 (default: 1)
            partner_no: 파트너 번호
            search_after: 검색 기준 값(lastId - 상품번호)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {"size": size}
            if page is not None:
                params["page"] = page
            if partner_no is not None:
                params["partnerNo"] = partner_no
            if search_after is not None:
                params["searchAfter"] = search_after
            resp = await client.get("/products/search", headers=headers, params=params)
            return self.handle_resp(resp, ProductSearchResponse)

    async def get_product_options(
        self, product_no: int, partner_no: int | None = None
    ) -> ProductOptionsResponse:
        """옵션 조회하기

        Args:
            product_no: 상품 번호
            partner_no: 파트너 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, int] = {}
            if partner_no is not None:
                params["partnerNo"] = partner_no
            resp = await client.get(
                f"/products/{product_no}/options", headers=headers, params=params
            )
            return self.handle_resp(resp, ProductOptionsResponse)

    async def get_option_stocks(
        self,
        period_type: str,
        size: int,
        brand_no: int | None = None,
        start_ymdt: datetime | None = None,
        end_ymdt: datetime | None = None,
        sale_status_types: list[str] | None = None,
        sale_setting_status_types: list[str] | None = None,
        allows_front_display: Literal["ALL", "Y", "N"] | None = None,
        page: int | None = None,
        search_after: int | None = None,
    ) -> OptionStocksResponse:
        """상품재고관리 옵션 리스트 조회

        Args:
            period_type: 검색 기간 조건 종류 (startYmdt과 함께 사용)
            size: 페이지 사이즈 (1~100)
            brand_no: 브랜드 번호
            start_ymdt: 조회기간 시작 일자
            end_ymdt: 조회기간 종료 일자 (default: 현재)
            sale_status_types: 판매 상태 목록 (default: 전체)
            sale_setting_status_types: 판매 설정 목록 (default: 전체)
            allows_front_display: 전시 여부 (default: ALL)
            page: 페이지 번호 (default: 1)
            search_after: 검색 기준 값(lastId)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {"periodType": period_type, "size": size}
            if brand_no is not None:
                params["brandNo"] = brand_no
            if start_ymdt is not None:
                params["startYmdt"] = to_kst_string(start_ymdt)
            if end_ymdt is not None:
                params["endYmdt"] = to_kst_string(end_ymdt)
            if sale_status_types is not None:
                params["saleStatusTypes"] = ",".join(sale_status_types)
            if sale_setting_status_types is not None:
                params["saleSettingStatusTypes"] = ",".join(sale_setting_status_types)
            if allows_front_display is not None:
                params["allowsFrontDisplay"] = allows_front_display
            if page is not None:
                params["page"] = page
            if search_after is not None:
                params["searchAfter"] = search_after
            resp = await client.get("/products/options/stocks", headers=headers, params=params)
            return self.handle_resp(resp, OptionStocksResponse)

    # ------------------------------------------------------------------
    #  상품 심사 (Inspections)
    # ------------------------------------------------------------------
    async def get_inspections_approval_waiting(
        self,
        period_type: str,
        search_start_date_time: datetime,
        search_end_date_time: datetime,
        page: int,
        size: int,
        partner_no: int | None = None,
        admin_no: int | None = None,
        apply_status: str | None = None,
        keywords: str | None = None,
        keyword_type: str | None = None,
    ) -> InspectionWaitingResponse:
        """심사대상 상품 조회

        Args:
            period_type: 검색기간 종류
            search_start_date_time: 검색 시작 일시
            search_end_date_time: 검색 종료 일시
            page: 조회할 페이지 번호
            size: 한번에 조회할 상품수
            partner_no: 파트너 번호
            admin_no: 담당자 번호
            apply_status: 승인 상태
            keywords: 검색어
            keyword_type: 검색어 종류
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int] = {
                "periodType": period_type,
                "searchStartDateTime": to_kst_string(search_start_date_time),
                "searchEndDateTime": to_kst_string(search_end_date_time),
                "page": page,
                "size": size,
            }
            if partner_no is not None:
                params["partnerNo"] = partner_no
            if admin_no is not None:
                params["adminNo"] = admin_no
            if apply_status is not None:
                params["applyStatus"] = apply_status
            if keywords is not None:
                params["keywords"] = keywords
            if keyword_type is not None:
                params["keywordType"] = keyword_type
            resp = await client.get(
                "/products/inspections/approval-waiting", headers=headers, params=params
            )
            return self.handle_resp(resp, InspectionWaitingResponse)

    async def get_inspection_view(
        self, product_no: int, partner_no: int | None = None
    ) -> InspectionViewResponse:
        """상품 심사 상세 조회

        Args:
            product_no: 상품번호
            partner_no: 파트너 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, int] = {}
            if partner_no is not None:
                params["partnerNo"] = partner_no
            resp = await client.get(
                f"/products/inspections/{product_no}/view", headers=headers, params=params
            )
            return self.handle_resp(resp, InspectionViewResponse)

    async def confirm_inspections(
        self, request: InspectionConfirmRequest
    ) -> InspectionResultResponse:
        """상품 심사 승인하기

        Args:
            request: 승인할 상품번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/products/inspections/confirm", headers=headers, json=body)
            return self.handle_resp(resp, InspectionResultResponse)

    async def reject_inspections(self, request: InspectionRejectRequest) -> InspectionResultResponse:
        """상품 심사 거절하기

        Args:
            request: 거절 사유 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/products/inspections/reject", headers=headers, json=body)
            return self.handle_resp(resp, InspectionResultResponse)

    # ------------------------------------------------------------------
    #  상품 등록/수정 (Create/Update)
    # ------------------------------------------------------------------
    async def create_product(self, request: dict[str, Any]) -> SavedProductResponse:
        """상품(옵션포함) 등록하기 (version 2.0)

        요청 본문이 매우 방대하여 dict로 전달받습니다. 스펙(products-1263807508) 참조.

        Args:
            request: 상품 등록 정보 (camelCase 키)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "2.0"}
            resp = await client.post("/products", headers=headers, json=request)
            return self.handle_resp(resp, SavedProductResponse)

    async def update_product(self, request: dict[str, Any]) -> SavedProductResponse:
        """상품(옵션포함) 수정하기 (DEPRECATED - version 2.0 사용 권장)

        요청 본문이 매우 방대하여 dict로 전달받습니다. 스펙(products-1116277168) 참조.

        Args:
            request: 상품 수정 정보 (camelCase 키, mallProductNo 포함)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.put("/products", headers=headers, json=request)
            return self.handle_resp(resp, SavedProductResponse)

    async def update_product_v2(
        self, product_no: int, request: dict[str, Any]
    ) -> SavedProductResponse:
        """상품(옵션포함) 수정하기 (version 2.0)

        요청 본문이 매우 방대하여 dict로 전달받습니다. 스펙(products-productNo2036855991) 참조.

        Args:
            product_no: 상품번호
            request: 상품 수정 정보 (camelCase 키)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "2.0"}
            resp = await client.put(f"/products/{product_no}", headers=headers, json=request)
            return self.handle_resp(resp, SavedProductResponse)

    async def create_product_temporary(self, request: dict[str, Any]) -> SavedProductResponse:
        """상품 임시 등록하기

        요청 본문이 매우 방대하여 dict로 전달받습니다. 스펙(products-temporary-1953288861) 참조.

        Args:
            request: 상품 임시 등록 정보 (camelCase 키)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.post("/products/temporary", headers=headers, json=request)
            return self.handle_resp(resp, SavedProductResponse)

    async def create_copied_product(
        self, product_no: int, request: dict[str, Any]
    ) -> SavedProductResponse:
        """재고연동상품 등록하기

        요청 본문이 매우 방대하여 dict로 전달받습니다. 스펙(products-productNo-1790230091) 참조.

        Args:
            product_no: 원본(마스터) 상품번호
            request: 재고연동상품 등록 정보 (camelCase 키)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.post(f"/products/{product_no}", headers=headers, json=request)
            return self.handle_resp(resp, SavedProductResponse)

    async def upsert_product_guide(self, request: ProductGuideRequest) -> None:
        """상품 이용안내 템플릿 등록 및 수정

        Args:
            request: 상품 이용안내 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/products/guides", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def patch_products_quick(
        self, items: list[PartialQuickItem]
    ) -> PartialQuickResponse:
        """상품 부분수정 (상품별 요청값 부분수정, 벌크 가능)

        Args:
            items: 부분수정할 상품 항목 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [i.model_dump(by_alias=True, exclude_none=True, mode="json") for i in items]
            resp = await client.patch("/products/partial/quick", headers=headers, json=body)
            return self.handle_resp(resp, PartialQuickResponse)

    # ------------------------------------------------------------------
    #  옵션/재고 수정 (Option / Stock)
    # ------------------------------------------------------------------
    async def update_product_options(
        self, request: PutProductOptionsRequest
    ) -> SavedProductResponse:
        """옵션(구매자작성형) 수정하기

        Args:
            request: 옵션/구매자작성형 수정 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/products/options", headers=headers, json=body)
            return self.handle_resp(resp, SavedProductResponse)

    async def update_stock_by_option_no(
        self, request: PutStockByOptionNoRequest
    ) -> PutStockByOptionNoResponse:
        """옵션 번호로 재고 변경하기

        Args:
            request: 옵션 번호별 재고 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(
                "/products/options/stock-with-id", headers=headers, json=body
            )
            return self.handle_resp(resp, PutStockByOptionNoResponse)

    async def update_stock_by_option_management_code(
        self, request: PutStockByOptionCodeRequest
    ) -> PutStockByOptionCodeResponse:
        """옵션 관리코드로 재고 변경하기

        Args:
            request: 옵션 관리코드별 재고 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(
                "/products/options/stock-with-management-code", headers=headers, json=body
            )
            return self.handle_resp(resp, PutStockByOptionCodeResponse)

    async def update_stock_by_product_management_code(
        self, request: PutStockByProductCodeRequest
    ) -> PutStockByProductCodeResponse:
        """상품 관리코드로 재고 변경하기

        Args:
            request: 상품 관리코드별 재고 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(
                "/products/stock-with-product-management-code", headers=headers, json=body
            )
            return self.handle_resp(resp, PutStockByProductCodeResponse)

    async def update_stock_by_product_no(
        self, request: PutStockByProductNoRequest
    ) -> PutStockByProductNoResponse:
        """상품 번호로 재고 변경하기

        Args:
            request: 상품 번호별 재고 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(
                "/products/stock-with-product-no", headers=headers, json=body
            )
            return self.handle_resp(resp, PutStockByProductNoResponse)

    # ------------------------------------------------------------------
    #  상품 부분/상태/판매합의 수정
    # ------------------------------------------------------------------
    async def update_product_partial(
        self, request: PutProductPartialRequest
    ) -> SavedProductResponse:
        """상품 부분(판매상태, 전시상태, 품절처리, 옵션) 수정하기

        Args:
            request: 부분 수정 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/products/partial", headers=headers, json=body)
            return self.handle_resp(resp, SavedProductResponse)

    async def update_product_status(
        self, mall_product_no: int, request: PutProductStatusRequest
    ) -> None:
        """상품 상태 변경하기

        Args:
            mall_product_no: 상품번호
            request: 상태 변경 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(
                f"/products/{mall_product_no}/status", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    async def update_sale_agreement(
        self, request: PutSaleAgreementRequest
    ) -> PutSaleAgreementResponse:
        """상품 판매합의 승인/거절하기

        Args:
            request: 판매합의 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/products/sale-agreements", headers=headers, json=body)
            return self.handle_resp(resp, PutSaleAgreementResponse)

    # ------------------------------------------------------------------
    #  네이버 쇼핑 인증키
    # ------------------------------------------------------------------
    async def set_naver_shopping_auth_key(
        self, sno: str, request: NaverShoppingConfigRequest
    ) -> None:
        """[샵바이 전용] 네이버 쇼핑 인증키 설정하기

        Args:
            sno: 서비스 번호
            request: 네이버 쇼핑 인증키 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post(
                f"/naver-shopping/{sno}/config", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    # ------------------------------------------------------------------
    #  상품우선구매권한 (Purchase Permission)
    # ------------------------------------------------------------------
    async def get_purchase_permission(self, product_no: int) -> list[PurchasePermissionItem]:
        """상품우선구매권한 조회하기

        Args:
            product_no: 상품번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/purchase-permission/{product_no}", headers=headers)
            return self.handle_resp(resp, list[PurchasePermissionItem])

    async def create_purchase_permission(
        self, request: CreatePurchasePermissionRequest
    ) -> CreatePurchasePermissionResponse:
        """상품우선구매권한 생성하기

        Args:
            request: 우선구매권한 생성 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/purchase-permission", headers=headers, json=body)
            return self.handle_resp(resp, CreatePurchasePermissionResponse)

    async def update_purchase_permission_product(
        self, permission_no: int, request: UpdatePurchasePermissionProductRequest
    ) -> None:
        """상품우선구매권한 수정하기

        Args:
            permission_no: 구매권한번호
            request: 상품 권한 수정 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(
                f"/purchase-permission/product/{permission_no}", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    async def update_purchase_permission_member(
        self, permission_no: int, members: list[PurchasePermissionMemberInput]
    ) -> None:
        """회원우선구매권한 수정하기

        Args:
            permission_no: 구매권한번호
            members: 회원 권한 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [m.model_dump(by_alias=True, exclude_none=True, mode="json") for m in members]
            resp = await client.put(
                f"/purchase-permission/member/{permission_no}", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    async def delete_purchase_permission(self, permission_no: int) -> None:
        """상품우선구매권한 삭제하기

        Args:
            permission_no: 구매권한번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.delete(
                f"/purchase-permission/{permission_no}", headers=headers
            )
            self.raise_for_status(resp)
            return None

    async def delete_purchase_permission_member(
        self, permission_no: int, member_nos: list[int]
    ) -> None:
        """회원우선구매권한 삭제하기

        Args:
            permission_no: 구매권한번호
            member_nos: 회원번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params = {"memberNos": ",".join(str(no) for no in member_nos)}
            resp = await client.delete(
                f"/purchase-permission/{permission_no}/members", headers=headers, params=params
            )
            self.raise_for_status(resp)
            return None

"""Shopby Shop(Client) Product API 클라이언트.

shop-api(`https://shop-api.e-ncp.com`) 의 공개(인증 불필요) 상품 도메인 엔드포인트를
구현한다. 모든 메서드는 익명 공개 호출이며 회원 토큰(accessToken /
Shop-By-Authorization)을 전송하지 않는다. clientId/platform/language 헤더는 base 의
`common_header` 가 주입하고, 각 메서드는 `version` 헤더만 직접 지정한다.

spec: docs/api/product-shop-public.yml
"""

import httpx

from shopby_sdk.shop.base import ShopbyShopApiClient
from shopby_sdk.shop.product.models import (
    AdditionalDiscountResponse,
    AdditionalDiscountsResponse,
    BestReviewSearchResponse,
    BestSellerSearchResponse,
    BrandChildItem,
    BrandDetailResponse,
    BrandExtraInfoItem,
    BrandListResponse,
    BrandsByNoResponse,
    BrandSearchItem,
    BrandTreeItem,
    BundleShippingResponse,
    CustomPropertiesResponse,
    DisplayCategoryItem,
    ExtraProductsResponse,
    FreeGiftConditionResponse,
    GroupManagementCodeItem,
    GroupManagementCodeRequest,
    NaverShoppingConfigResponse,
    OptionImageItem,
    ProductDetailResponse,
    ProductExtraInfoItem,
    ProductKeywordsItem,
    ProductOptionsResponse,
    ProductSearchByNosRequest,
    ProductSearchByNosResponse,
    ProductSearchResponse,
    ProductShippingInfo,
    ProductsOptionsResponse,
    PublicInfoItem,
    PurchasePermissionItem,
    RegularDeliveryListResponse,
    RegularDeliverySearchItem,
    RelatedProductItem,
    RestockListResponse,
    RestockRequest,
    SearchSummaryResponse,
    StandardCategoryResponse,
    UrlShorteningResponse,
)

_V1 = {"version": "1.0"}


class ShopbyShopProductApiClient(ShopbyShopApiClient):
    """shop-api Product 도메인 공개 API 클라이언트."""

    # ------------------------------------------------------------------
    # Additional Discount
    # ------------------------------------------------------------------
    async def get_additional_discounts_by_product_no(
        self, product_no: int
    ) -> AdditionalDiscountResponse:
        """추가할인 정보 조회하기 (상품번호 단건) (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/additional-discounts/by-product-no",
                headers=_V1,
                params={"productNo": product_no},
            )
            return self.handle_resp(resp, AdditionalDiscountResponse)

    async def get_additional_discounts_by_product_nos(
        self, product_nos: list[int]
    ) -> AdditionalDiscountsResponse:
        """추가할인 정보 다건 조회하기 (최대 100건) (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/additional-discounts/by-product-nos",
                headers=_V1,
                params={"productNos": ",".join(str(n) for n in product_nos)},
            )
            return self.handle_resp(resp, AdditionalDiscountsResponse)

    # ------------------------------------------------------------------
    # Brand
    # ------------------------------------------------------------------
    async def get_display_brands(
        self,
        *,
        name: str | None = None,
        category_nos: list[int] | None = None,
        sold_out_included: bool | None = None,
        sale_status: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        has_total_count: bool | None = None,
        sort_criterion: str | None = None,
        sort_direction: str | None = None,
    ) -> BrandListResponse:
        """브랜드 목록 조회하기 - 상품 색인 기준 (Version 1.0)."""
        params: dict = {}
        if name is not None:
            params["filter.name"] = name
        if category_nos is not None:
            params["filter.categoryNos"] = ",".join(str(n) for n in category_nos)
        if sold_out_included is not None:
            params["filter.soldOutIncluded"] = sold_out_included
        if sale_status is not None:
            params["filter.saleStatus"] = sale_status
        if page_number is not None:
            params["pageNumber"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size
        if has_total_count is not None:
            params["hasTotalCount"] = has_total_count
        if sort_criterion is not None:
            params["sort.criterion"] = sort_criterion
        if sort_direction is not None:
            params["sort.direction"] = sort_direction
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/display/brands", headers=_V1, params=params)
            return self.handle_resp(resp, BrandListResponse)

    async def get_display_brand_extra_info(
        self, display_brand_nos: list[int]
    ) -> list[BrandExtraInfoItem]:
        """브랜드 추가 정보 조회하기 (최대 30개) (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/display/brands/extraInfo",
                headers=_V1,
                params={"displayBrandNos": ",".join(str(n) for n in display_brand_nos)},
            )
            return self.handle_resp(resp, list[BrandExtraInfoItem])

    async def search_brands(
        self,
        *,
        brand_name: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        sort_criterion: str | None = None,
        sort_direction: str | None = None,
    ) -> list[BrandSearchItem]:
        """브랜드 조회하기 - 브랜드 색인 기준 (Version 1.0)."""
        params: dict = {}
        if brand_name is not None:
            params["brandName"] = brand_name
        if page_number is not None:
            params["pageNumber"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size
        if sort_criterion is not None:
            params["sortCriterion"] = sort_criterion
        if sort_direction is not None:
            params["sortDirection"] = sort_direction
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/display/brands/search", headers=_V1, params=params)
            return self.handle_resp(resp, list[BrandSearchItem])

    async def get_display_brands_search_by_nos(
        self, display_brand_nos: list[int] | None = None
    ) -> BrandsByNoResponse:
        """브랜드번호로 브랜드정보 조회하기 (Version 1.0)."""
        params: dict = {}
        if display_brand_nos is not None:
            params["displayBrandNos"] = ",".join(str(n) for n in display_brand_nos)
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/display/brands/search-by-nos", headers=_V1, params=params)
            return self.handle_resp(resp, BrandsByNoResponse)

    async def get_brand_tree(self) -> list[BrandTreeItem]:
        """브랜드 트리 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/display/brands/tree", headers=_V1)
            return self.handle_resp(resp, list[BrandTreeItem])

    async def get_display_brand(self, display_brand_no: int) -> BrandDetailResponse:
        """브랜드 상세 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(f"/display/brands/{display_brand_no}", headers=_V1)
            return self.handle_resp(resp, BrandDetailResponse)

    async def get_brand_children(self, display_brand_no: int) -> list[BrandChildItem]:
        """자식 브랜드 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                f"/display/brands/{display_brand_no}/children", headers=_V1
            )
            return self.handle_resp(resp, list[BrandChildItem])

    # ------------------------------------------------------------------
    # Configuration / Custom Property
    # ------------------------------------------------------------------
    async def get_naver_shopping_configuration(self) -> NaverShoppingConfigResponse:
        """네이버 쇼핑 설정정보 조회 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/products/configuration/naver-shopping", headers=_V1)
            return self.handle_resp(resp, NaverShoppingConfigResponse)

    async def get_custom_properties(self) -> CustomPropertiesResponse:
        """상품 항목 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/products/custom-properties", headers=_V1)
            return self.handle_resp(resp, CustomPropertiesResponse)

    # ------------------------------------------------------------------
    # Free Gift
    # ------------------------------------------------------------------
    async def get_free_gift_condition_by_order_amount(
        self, *, order_amt: int | None = None
    ) -> FreeGiftConditionResponse:
        """사은품 지급가능한 조건 조회하기 (주문금액기준) (Version 1.0)."""
        params: dict = {}
        if order_amt is not None:
            params["orderAmt"] = order_amt
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/free-gift-condition/order-amount", headers=_V1, params=params
            )
            return self.handle_resp(resp, FreeGiftConditionResponse)

    async def get_free_gift_condition_by_product(
        self, product_no: int
    ) -> FreeGiftConditionResponse:
        """사은품 지급가능한 조건 조회하기 (상품금액기준) (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(f"/free-gift-condition/{product_no}", headers=_V1)
            return self.handle_resp(resp, FreeGiftConditionResponse)

    # ------------------------------------------------------------------
    # Restock
    # ------------------------------------------------------------------
    async def get_restock(
        self,
        *,
        product_no: int | None = None,
        option_nos: list[int] | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> RestockListResponse:
        """재입고 알림 조회 (Version 1.0)."""
        params: dict = {}
        if product_no is not None:
            params["productNo"] = product_no
        if option_nos is not None:
            params["optionNos"] = ",".join(str(n) for n in option_nos)
        if page_number is not None:
            params["pageNumber"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/products/restock", headers=_V1, params=params)
            return self.handle_resp(resp, RestockListResponse)

    async def post_restock(self, request: RestockRequest) -> None:
        """재입고 알림 신청 (Version 1.0). 응답 본문 없음."""
        body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.post("/products/restock", headers=_V1, json=body)
            self.raise_for_status(resp)
            return None

    async def delete_restock(self, restock_nos: list[int]) -> None:
        """재입고 알림 삭제 (Version 1.0). 응답 본문 없음."""
        params = {"restockNos": ",".join(str(n) for n in restock_nos)}
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.delete("/products/restock", headers=_V1, params=params)
            self.raise_for_status(resp)
            return None

    # ------------------------------------------------------------------
    # Product info (by product nos)
    # ------------------------------------------------------------------
    async def get_product_extra_infos(
        self, product_nos: list[int]
    ) -> list[ProductExtraInfoItem]:
        """상품 번호 리스트로 추가 정보 조회 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/products/extraInfo",
                headers=_V1,
                params={"productNos": ",".join(str(n) for n in product_nos)},
            )
            return self.handle_resp(resp, list[ProductExtraInfoItem])

    async def get_favorite_keywords(self, *, size: int | None = None) -> list[str]:
        """인기 검색어 조회하기 (Version 1.0)."""
        params: dict = {}
        if size is not None:
            params["size"] = size
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/products/favoriteKeywords", headers=_V1, params=params)
            return self.handle_resp(resp, list[str])

    async def get_products_options(self, product_nos: list[int]) -> ProductsOptionsResponse:
        """옵션 목록 조회하기 (상품번호 리스트) (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/products/options",
                headers=_V1,
                params={"productNos": ",".join(str(n) for n in product_nos)},
            )
            return self.handle_resp(resp, ProductsOptionsResponse)

    async def get_public_infos(self, product_nos: list[int]) -> list[PublicInfoItem]:
        """상품 공개용 기본정보 조회 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/products/public-info",
                headers=_V1,
                params={"productNos": ",".join(str(n) for n in product_nos)},
            )
            return self.handle_resp(resp, list[PublicInfoItem])

    async def get_shipping_infos(self, product_nos: list[int]) -> list[ProductShippingInfo]:
        """상품번호를 통한 배송 정보 및 배송 불가 국가 조회 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/products/shipping-info",
                headers=_V1,
                params={"productNos": ",".join(str(n) for n in product_nos)},
            )
            return self.handle_resp(resp, list[ProductShippingInfo])

    async def get_product_search_keywords(
        self, product_nos: list[int]
    ) -> list[ProductKeywordsItem]:
        """상품 번호 리스트로 검색어 조회 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/products/search/keywords",
                headers=_V1,
                params={"productNos": ",".join(str(n) for n in product_nos)},
            )
            return self.handle_resp(resp, list[ProductKeywordsItem])

    # ------------------------------------------------------------------
    # Regular delivery
    # ------------------------------------------------------------------
    async def get_regular_delivery_products(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        display_category_nos: list[int] | None = None,
    ) -> RegularDeliveryListResponse:
        """변경 가능한 정기 결제 상품 조회하기 (Version 1.0)."""
        params: dict = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if display_category_nos is not None:
            params["displayCategoryNos"] = ",".join(str(n) for n in display_category_nos)
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/products/regular-delivery", headers=_V1, params=params)
            return self.handle_resp(resp, RegularDeliveryListResponse)

    async def search_regular_delivery_products(
        self, product_nos: list[int]
    ) -> list[RegularDeliverySearchItem]:
        """상품 번호 리스트로 정기 결제 상품 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/products/regular-delivery/search",
                headers=_V1,
                params={"productNos": ",".join(str(n) for n in product_nos)},
            )
            return self.handle_resp(resp, list[RegularDeliverySearchItem])

    # ------------------------------------------------------------------
    # Search engine
    # ------------------------------------------------------------------
    async def search_products(self, *, params: dict | None = None) -> ProductSearchResponse:
        """상품 검색(search engine)하기 (Version 1.0).

        검색 필터는 dotted query key(예: ``filter.keywords``, ``order.by``) 가
        40개 이상이라 raw query dict 로 받는다. 콤마구분 리스트 키는 호출자가
        문자열로 전달한다. None 값은 호출자가 제거하거나, 본 메서드가 그대로 전달한다.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/products/search", headers=_V1, params=params or {})
            return self.handle_resp(resp, ProductSearchResponse)

    async def get_products_search_summary(
        self, *, params: dict | None = None
    ) -> SearchSummaryResponse:
        """상품 검색 결과 Summary 정보 조회(search engine)하기 (Version 1.0).

        search_products 와 동일하게 dotted query key 가 많아 raw query dict 로 받는다.
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/products/search/summary", headers=_V1, params=params or {})
            return self.handle_resp(resp, SearchSummaryResponse)

    async def search_best_review_products(
        self,
        *,
        family_malls: bool | None = None,
        category_nos: int | None = None,
        client_key: int | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        has_total_count: bool | None = None,
        has_option_values: bool | None = None,
    ) -> BestReviewSearchResponse:
        """베스트 리뷰 상품 검색(search engine)하기 (Version 1.0)."""
        params: dict = {}
        if family_malls is not None:
            params["filter.familyMalls"] = family_malls
        if category_nos is not None:
            params["categoryNos"] = category_nos
        if client_key is not None:
            params["clientKey"] = client_key
        if page_number is not None:
            params["pageNumber"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size
        if has_total_count is not None:
            params["hasTotalCount"] = has_total_count
        if has_option_values is not None:
            params["hasOptionValues"] = has_option_values
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/products/best-review/search", headers=_V1, params=params)
            return self.handle_resp(resp, BestReviewSearchResponse)

    async def search_best_seller_products(
        self,
        *,
        family_malls: bool | None = None,
        category_nos: int | None = None,
        client_key: int | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        has_total_count: bool | None = None,
        has_option_values: bool | None = None,
    ) -> BestSellerSearchResponse:
        """베스트 셀러 상품 검색(search engine)하기 (Version 1.0)."""
        params: dict = {}
        if family_malls is not None:
            params["filter.familyMalls"] = family_malls
        if category_nos is not None:
            params["categoryNos"] = category_nos
        if client_key is not None:
            params["clientKey"] = client_key
        if page_number is not None:
            params["pageNumber"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size
        if has_total_count is not None:
            params["hasTotalCount"] = has_total_count
        if has_option_values is not None:
            params["hasOptionValues"] = has_option_values
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/products/best-seller/search", headers=_V1, params=params)
            return self.handle_resp(resp, BestSellerSearchResponse)

    async def get_bundle_shipping_products(
        self,
        delivery_template_no: int,
        *,
        has_option_values: bool | None = None,
        has_brand_and_category_values: bool | None = None,
        has_sold_out: bool | None = None,
        page_size: int | None = None,
        page_number: int | None = None,
        product_sort_criterion: str | None = None,
        product_sort_direction: str | None = None,
    ) -> BundleShippingResponse:
        """묶음 배송 상품 목록 조회하기 (Version 1.0)."""
        params: dict = {"deliveryTemplateNo": delivery_template_no}
        if has_option_values is not None:
            params["hasOptionValues"] = has_option_values
        if has_brand_and_category_values is not None:
            params["hasBrandAndCategoryValues"] = has_brand_and_category_values
        if has_sold_out is not None:
            params["hasSoldOut"] = has_sold_out
        if page_size is not None:
            params["pageSize"] = page_size
        if page_number is not None:
            params["pageNumber"] = page_number
        if product_sort_criterion is not None:
            params["productSort.criterion"] = product_sort_criterion
        if product_sort_direction is not None:
            params["productSort.direction"] = product_sort_direction
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get("/products/bundle-shipping", headers=_V1, params=params)
            return self.handle_resp(resp, BundleShippingResponse)

    async def search_products_by_nos(
        self, request: ProductSearchByNosRequest
    ) -> ProductSearchByNosResponse:
        """상품번호 리스트로 상품 조회 (Version 1.0)."""
        body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.post("/products/search-by-nos", headers=_V1, json=body)
            return self.handle_resp(resp, ProductSearchByNosResponse)

    async def get_group_management_codes(
        self, request: GroupManagementCodeRequest
    ) -> list[GroupManagementCodeItem]:
        """그룹관리코드 조회하기 (Version 1.0)."""
        body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.post(
                "/products/group-management-code", headers=_V1, json=body
            )
            return self.handle_resp(resp, list[GroupManagementCodeItem])

    # ------------------------------------------------------------------
    # Single product (by productNo)
    # ------------------------------------------------------------------
    async def get_product(
        self, product_no: int, *, channel_type: str | None = None
    ) -> ProductDetailResponse:
        """상품 상세 조회하기 (Version 1.0)."""
        params: dict = {}
        if channel_type is not None:
            params["channelType"] = channel_type
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(f"/products/{product_no}", headers=_V1, params=params)
            return self.handle_resp(resp, ProductDetailResponse)

    async def get_product_display_categories(
        self, product_no: int
    ) -> list[DisplayCategoryItem]:
        """상품번호에 해당하는 모든 전시카테고리 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                f"/products/{product_no}/display-categories", headers=_V1
            )
            return self.handle_resp(resp, list[DisplayCategoryItem])

    async def get_extra_products(self, product_no: int) -> ExtraProductsResponse:
        """추가상품 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(f"/products/{product_no}/extra-products", headers=_V1)
            return self.handle_resp(resp, ExtraProductsResponse)

    async def get_product_options(self, product_no: int) -> ProductOptionsResponse:
        """옵션 조회하기 (단일 상품) (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(f"/products/{product_no}/options", headers=_V1)
            return self.handle_resp(resp, ProductOptionsResponse)

    async def get_product_options_images(self, product_no: int) -> list[OptionImageItem]:
        """상품에 해당하는 옵션 이미지 목록 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(f"/products/{product_no}/options/images", headers=_V1)
            return self.handle_resp(resp, list[OptionImageItem])

    async def get_product_option_images(
        self, product_no: int, option_no: int
    ) -> list[OptionImageItem]:
        """옵션의 이미지 정보 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                f"/products/{product_no}/options/{option_no}/images", headers=_V1
            )
            return self.handle_resp(resp, list[OptionImageItem])

    async def get_product_purchase_permissions(
        self, product_no: int
    ) -> list[PurchasePermissionItem]:
        """상품번호로 상품우선구매권한 조회 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(f"/products/{product_no}/purchasable", headers=_V1)
            return self.handle_resp(resp, list[PurchasePermissionItem])

    async def get_related_products(self, product_no: int) -> list[RelatedProductItem]:
        """관련 상품 정보 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(f"/products/{product_no}/related-products", headers=_V1)
            return self.handle_resp(resp, list[RelatedProductItem])

    async def get_product_standard_category(
        self, product_no: int
    ) -> StandardCategoryResponse:
        """상품번호에 해당하는 표준카테고리 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                f"/products/{product_no}/standard-category", headers=_V1
            )
            return self.handle_resp(resp, StandardCategoryResponse)

    async def get_product_url_shortening(self, product_no: int) -> UrlShorteningResponse:
        """상품 번호와 쇼핑몰 번호에 해당하는 단축URL 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                f"/products/{product_no}/url-shortening", headers=_V1
            )
            return self.handle_resp(resp, UrlShorteningResponse)

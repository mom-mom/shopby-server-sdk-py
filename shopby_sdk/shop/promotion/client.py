"""Shopby Shop(Client) Promotion(쿠폰) API 클라이언트.

shop-api(`https://shop-api.e-ncp.com`) 의 공개(인증 불필요) 쿠폰 조회/설정 API.
회원 토큰(accessToken / Shop-By-Authorization)은 전송하지 않는 공개 익명 호출 전용이다.

대응 OpenAPI: docs/api/promotion-shop-public.yml
"""

import httpx

from shopby_sdk.shop.base import ShopbyShopApiClient

from .models import (
    CouponTargetsResponse,
    IssuableCoupon,
    PromotionCouponConfig,
)


class ShopbyShopPromotionApiClient(ShopbyShopApiClient):
    """Shopby Shop Promotion(쿠폰) API 클라이언트."""

    async def get_promotion_configs_coupon(self) -> PromotionCouponConfig:
        """쿠폰 설정 조회 (Version 1.0).

        operationId: get-promotion-configs-coupon
        GET /promotion-configs/coupon
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/promotion-configs/coupon", headers=headers)
            return self.handle_resp(resp, PromotionCouponConfig)

    async def get_issuable_coupons(
        self, *, channel_type: str | None = None
    ) -> list[IssuableCoupon]:
        """발급 가능한 쿠폰 조회하기 (Version 1.0).

        상품과 상관없이 오늘 날짜 기준으로 다운로드 가능한 쿠폰을 모두 조회한다.

        operationId: get-issuable-coupons
        GET /coupons/issuable

        Args:
            channel_type: 채널 타입 (NAVER_EP, FACEBOOK).
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            params: dict = {}
            if channel_type is not None:
                params["channelType"] = channel_type
            resp = await client.get("/coupons/issuable", headers=headers, params=params)
            return self.handle_resp(resp, list[IssuableCoupon])

    async def get_issuable_coupon_by_products(
        self, product_no: int, *, channel_type: str | None = None
    ) -> list[IssuableCoupon]:
        """상품 번호로 발급 가능한 쿠폰 조회하기 (Version 1.0).

        해당 상품 상세정보에서 다운로드 할 수 있는 모든 쿠폰을 조회한다.
        상품번호 뿐만 아니라 해당 상품의 브랜드/파트너/카테고리로 할인대상
        설정된 쿠폰도 조회한다.

        operationId: get-issuable-coupon-by-products
        GET /coupons/products/{productNo}/issuable/coupons

        Args:
            product_no: 상품번호.
            channel_type: 채널 타입 (NAVER_EP, FACEBOOK).
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            params: dict = {}
            if channel_type is not None:
                params["channelType"] = channel_type
            resp = await client.get(
                f"/coupons/products/{product_no}/issuable/coupons",
                headers=headers,
                params=params,
            )
            return self.handle_resp(resp, list[IssuableCoupon])

    async def get_issuable_coupons_by_target_no(
        self,
        *,
        coupon_target_type: str,
        target_no: int | None = None,
        target_nos: list[int] | None = None,
        channel_type: str | None = None,
    ) -> list[IssuableCoupon]:
        """특정 할인대상으로 발급 가능한 쿠폰 조회하기 (Version 1.0).

        할인대상(브랜드/카테고리/파트너) 으로 발급 가능한 쿠폰을 조회한다.
        `target_no` 또는 `target_nos` 중 하나는 반드시 입력해야 한다.

        operationId: get-issuable-coupons-by-target-no
        GET /coupons/targets/issuable/coupons

        Args:
            coupon_target_type: 쿠폰 할인 대상 (BRAND, CATEGORY, PARTNER).
            target_no: 할인 대상 번호.
            target_nos: 할인 대상 번호 리스트 (콤마 조인되어 전송됨).
            channel_type: 채널 타입 (NAVER_EP, FACEBOOK).
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            params: dict = {"couponTargetType": coupon_target_type}
            if target_no is not None:
                params["targetNo"] = target_no
            if target_nos is not None:
                params["targetNos"] = ",".join(str(n) for n in target_nos)
            if channel_type is not None:
                params["channelType"] = channel_type
            resp = await client.get(
                "/coupons/targets/issuable/coupons", headers=headers, params=params
            )
            return self.handle_resp(resp, list[IssuableCoupon])

    async def get_coupon_target(
        self, coupon_no: int, *, page_number: int, page_size: int
    ) -> CouponTargetsResponse:
        """쿠폰번호로 타겟상품 조회하기 (Version 1.0).

        선택한 쿠폰번호에 해당하는 타겟상품의 목록을 조회한다.

        operationId: get-coupon-target
        GET /coupons/{couponNo}/targets

        Args:
            coupon_no: 쿠폰 번호.
            page_number: 페이지 번호.
            page_size: 한 페이지당 노출 수.
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            params = {"pageNumber": page_number, "pageSize": page_size}
            resp = await client.get(
                f"/coupons/{coupon_no}/targets", headers=headers, params=params
            )
            return self.handle_resp(resp, CouponTargetsResponse)

    async def get_coupon_exclude_target(
        self, coupon_no: int, *, page_number: int, page_size: int
    ) -> CouponTargetsResponse:
        """쿠폰번호로 제외상품 조회하기 (Version 1.0).

        선택한 쿠폰번호에 해당하는 제외상품의 목록을 조회한다.

        operationId: get-coupon-exclude-target
        GET /coupons/{couponNo}/exclude-targets

        Args:
            coupon_no: 쿠폰 번호.
            page_number: 페이지 번호.
            page_size: 한 페이지당 노출 수.
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            params = {"pageNumber": page_number, "pageSize": page_size}
            resp = await client.get(
                f"/coupons/{coupon_no}/exclude-targets", headers=headers, params=params
            )
            return self.handle_resp(resp, CouponTargetsResponse)

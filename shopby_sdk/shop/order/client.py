"""Shopby Shop(Client) Order API 클라이언트.

order-shop-public.yml 의 공개(인증 불필요) 엔드포인트만 다룬다.
회원 토큰(accessToken / Shop-By-Authorization)은 전송하지 않는다.
"""

import httpx

from shopby_sdk.shop.base import ShopbyShopApiClient
from shopby_sdk.shop.order.models import (
    AppCardCardsResponse,
    AppCardInstPlanResponse,
    CartConfigResponse,
    OrderConfigResponse,
    ShippingEnumsResponse,
)


class ShopbyShopOrderApiClient(ShopbyShopApiClient):
    """Shopby Shop(Client) Order API 클라이언트."""

    async def get_app_card_cards(
        self, *, card_code: str | None = None
    ) -> AppCardCardsResponse:
        """앱카드 간편결제 카드사 목록 조회 (Version 1.0).

        Args:
            card_code: 특정 카드사 코드 (예: 2088). 없으면 전체 조회.
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {}
            if card_code is not None:
                params["cardCode"] = card_code
            resp = await client.get(
                "/app-card/cards", headers=headers, params=params
            )
            return self.handle_resp(resp, AppCardCardsResponse)

    async def get_app_card_inst_plan(
        self, *, amount: float | None = None
    ) -> AppCardInstPlanResponse:
        """앱카드 할부정보 조회 (Version 1.0).

        Args:
            amount: 상품금액 (예: 50000).
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            params: dict[str, float] = {}
            if amount is not None:
                params["amount"] = amount
            resp = await client.get(
                "/app-card/inst-plan", headers=headers, params=params
            )
            return self.handle_resp(resp, AppCardInstPlanResponse)

    async def get_cart_configuration(self) -> CartConfigResponse:
        """장바구니 설정 값 가져오기 (Version 1.0)."""
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/cart/config", headers=headers)
            return self.handle_resp(resp, CartConfigResponse)

    async def get_order_configuration(self) -> OrderConfigResponse:
        """주문 설정 값 가져오기 (Version 1.0)."""
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/order-configs", headers=headers)
            return self.handle_resp(resp, OrderConfigResponse)

    async def get_shippings_enums(self) -> ShippingEnumsResponse:
        """배송 enum 정보 조회 (Version 1.0)."""
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/shippings/enums", headers=headers)
            return self.handle_resp(resp, ShippingEnumsResponse)

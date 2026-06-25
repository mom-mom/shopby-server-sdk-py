"""Marketing(마케팅) shop API 클라이언트."""

import httpx

from shopby_sdk.shop.base import ShopbyShopApiClient

from .models import SnsShareResponse


class ShopbyShopMarketingApiClient(ShopbyShopApiClient):
    """Shopby Shop(Client) Marketing API 클라이언트.

    OpenAPI: docs/api/marketing-shop-public.yml
    공개(익명) API 전용이므로 회원 토큰을 전송하지 않는다.
    """

    async def get_sns_share(self, product_no: int) -> SnsShareResponse:
        """SNS 공유 설정 조회하기 (Version 1.0).

        Args:
            product_no: 상품 번호.

        operationId: get-sns-share
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            params = {"productNo": product_no}
            resp = await client.get(
                "/marketing/sns-share", headers=headers, params=params
            )
            return self.handle_resp(resp, SnsShareResponse)

"""Shopby Shop(Client) Admin API 클라이언트.

admin-shop-public.yml (Mall 도메인) 의 공개(인증 불필요) 엔드포인트를 구현한다.
shop-api 는 clientId/platform 헤더로 호출하며 회원 토큰을 전송하지 않는다.
"""

import httpx

from shopby_sdk.shop.admin.models import (
    MallInternationalizationResponse,
    MallPartner,
    MallResponse,
    MallSsl,
    ServiceBasicInfoResponse,
)
from shopby_sdk.shop.base import ShopbyShopApiClient


class ShopbyShopAdminApiClient(ShopbyShopApiClient):
    """Shopby Shop Admin API 클라이언트 (Mall 기본 정보 조회)."""

    # ------------------------------------
    #  Mall
    # ------------------------------------
    async def get_malls(self) -> MallResponse:
        """몰 정보 조회하기 (Version 1.0).

        몰 진입 시 전체 정보(쇼핑몰/카테고리/게시판/각종 설정)를 조회한다.
        성능을 위해 응답을 로컬 저장소에 캐싱하여 재사용하는 것을 권장한다.
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/malls", headers=headers)
            return self.handle_resp(resp, MallResponse)

    async def get_malls_internationalization(
        self,
    ) -> MallInternationalizationResponse:
        """현재 몰의 다국어, 환율 설정 조회 (Version 1.0)."""
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/malls/internationalization", headers=headers)
            return self.handle_resp(resp, MallInternationalizationResponse)

    async def get_malls_partners(
        self, *, partner_nos: str | None = None
    ) -> list[MallPartner]:
        """몰과 계약한 파트너 목록 조회하기 (Version 1.0).

        Args:
            partner_nos: 파트너 번호 (콤마 구분 문자열, 예: "1,2,3").
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            params: dict[str, str] = {}
            if partner_nos is not None:
                params["partnerNos"] = partner_nos
            resp = await client.get("/malls/partners", headers=headers, params=params)
            return self.handle_resp(resp, list[MallPartner])

    async def get_service_basic_info(self) -> ServiceBasicInfoResponse:
        """몰 서비스 기본 정보 조회하기 (Version 1.0).

        Cache-Control(max-age=3600) 헤더를 제공하므로 HTTP 캐싱을 활용할 수 있다.
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/malls/service-basic-info", headers=headers)
            return self.handle_resp(resp, ServiceBasicInfoResponse)

    async def get_malls_ssl(self) -> list[MallSsl]:
        """현재 도메인의 보안서버정보 조회하기 (Version 1.0)."""
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.common_header
        ) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/malls/ssl", headers=headers)
            return self.handle_resp(resp, list[MallSsl])

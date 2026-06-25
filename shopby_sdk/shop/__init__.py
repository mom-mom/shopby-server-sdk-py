"""Shopby Shop(Client) API SDK.

shop-api(`https://shop-api.e-ncp.com`) 의 **공개(인증 불필요) API** 만 다루는
클라이언트 모음. 회원 토큰(accessToken) 없이 호출 가능한, 개인을 특정하지 않는
엔드포인트(상품/전시 카탈로그, 약관/배너/기획전, 쿠폰 공개조회, 검증 유틸 등)로
구성된다.

server-api 용 클라이언트는 ``shopby_sdk.clients`` 패키지를 참고.
"""

from shopby_sdk.shop.base import PlatformType, ShopbyShopApiClient

__all__ = [
    "ShopbyShopApiClient",
    "PlatformType",
]

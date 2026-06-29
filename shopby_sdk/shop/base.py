"""Shopby Shop(Client) API 공통 클라이언트 베이스.

server-api(`server-api.e-ncp.com`) 와 달리 shop-api(`shop-api.e-ncp.com`) 는
Bearer 토큰 + systemKey 가 아니라 쇼핑몰 식별자 `clientId` 와 `platform` 헤더로
호출한다.

본 SDK 의 shop 클라이언트들은 **인증이 필요 없는(= 개인을 특정하지 않는) 공개 API**
만 다룬다. 따라서 회원 토큰(`accessToken` / `Shop-By-Authorization`)은 전송하지
않으며, 개인화 필드(찜 여부 등)는 응답에서 null 로 내려온다.
"""

import logging
from collections.abc import Callable
from typing import Any, Literal, Type, TypeVar

from httpx import HTTPStatusError, Response
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)

_ResponseType = TypeVar("_ResponseType")

PlatformType = Literal["PC", "MOBILE_WEB", "AOS", "IOS"]
"""shop-api `platform` 헤더 값.

- PC: PC 웹 브라우저
- MOBILE_WEB: 모바일 웹 브라우저
- AOS: Android 앱
- IOS: iOS 앱
"""


class ShopbyShopApiClient:
    """Shopby Shop(Client) API 공통 클라이언트.

    Args:
        client_id: 쇼핑몰 클라이언트 아이디 (`clientId` 헤더). 몰/앱 식별자이며
            회원 인증 정보가 아니다.
        platform: 접근 플랫폼 (`platform` 헤더). 기본값 ``"PC"``.
        base_url: API base URL. 기본값 ``https://shop-api.e-ncp.com``.
        language: 응답 언어 (`language` 헤더, 선택). ko/en/jp/zh.

    Note:
        공개 API 전용이므로 회원 `accessToken` 은 의도적으로 지원하지 않는다.
    """

    DEFAULT_BASE_URL = "https://shop-api.e-ncp.com"

    def __init__(
        self,
        client_id: str,
        platform: PlatformType = "PC",
        *,
        base_url: str | None = None,
        language: str | None = None,
        on_response: Callable[[Response], None] | None = None,
        raw: bool = False,
    ):
        self._client_id = client_id
        self._platform = platform
        self._language = language
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self._on_response = on_response
        self._raw = raw

    @property
    def common_header(self) -> dict[str, str]:
        """모든 요청에 공통으로 들어가는 헤더 (clientId/platform/[language]).

        `version` 헤더는 엔드포인트마다 값이 다르므로 각 메서드에서 개별 지정한다.
        """
        header = {
            "clientId": self._client_id,
            "platform": self._platform,
        }
        if self._language is not None:
            header["language"] = self._language
        return header

    def handle_resp(
        self, resp: Response, type_model: Type[_ResponseType], raw: bool | None = None
    ) -> _ResponseType | Any:
        self.raise_for_status(resp)

        if self._raw if raw is None else raw:
            return resp.json()
        try:
            return TypeAdapter(type_model).validate_python(resp.json())
        except ValueError:
            self._log_response(resp)
            raise

    def raise_for_status(self, resp: Response) -> None:
        """HTTP 상태 코드를 확인하고 오류 시 상세 정보를 로깅.

        Args:
            resp: httpx.Response 객체

        Raises:
            HTTPStatusError: 4xx 또는 5xx 응답 시
        """
        if self._on_response is not None:
            try:
                self._on_response(resp)
            except Exception:  # 콜백 오류가 요청을 깨뜨리지 않도록
                logger.warning("on_response callback raised", exc_info=True)
        try:
            resp.raise_for_status()
        except HTTPStatusError:
            self._log_response(resp)
            raise

    @staticmethod
    def _log_response(resp: Response):
        try:
            error_body = resp.json()
        except Exception:
            error_body = resp.text

        logger.error(
            f"HTTP error occurred: {resp.status_code} {resp.request.method} {resp.request.url}\n"
            f"Response body: {error_body}"
        )

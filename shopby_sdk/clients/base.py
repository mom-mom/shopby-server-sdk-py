import logging
from collections.abc import Callable
from typing import Any, TypeVar, Type

from httpx import HTTPStatusError, Response
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)

_ResponseType = TypeVar("_ResponseType")


class ShopbyServerApiClient:
    DEFAULT_BASE_URL = "https://server-api.e-ncp.com"

    def __init__(
        self,
        server_access_token: str,
        server_system_key: str,
        base_url: str | None = None,
        *,
        on_response: Callable[[Response], None] | None = None,
        raw: bool = False,
    ):
        """
        Args:
            on_response: 모든 응답마다 호출되는 콜백(검증/raise 전). 응답 헤더
                (예: ``ratelimit-available-level``)·상태코드 관찰용. 예외는 무시된다.
            raw: True 면 모든 메서드가 Pydantic 모델 대신 ``resp.json()``(dict/list)
                그대로 반환한다. 검증을 건너뛰어 스키마 불일치에도 죽지 않으며 응답을
                무손실로 받는다. 대량 백필·raw 적재용.
        """
        self._access_token = server_access_token
        self._system_key = server_system_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self._on_response = on_response
        self._raw = raw

    @property
    def common_header(self):
        return {
            "Authorization": f"Bearer {self._access_token}",
            "systemKey": self._system_key,
            "version": "1.0",
        }

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
        """
        HTTP 상태 코드를 확인하고 오류 시 상세 정보를 로깅

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
        # 응답 본문 가져오기 (JSON 파싱 시도)
        try:
            error_body = resp.json()
        except Exception:
            error_body = resp.text

        logger.error(
            f"HTTP error occurred: {resp.status_code} {resp.request.method} {resp.request.url}\n"
            f"Response body: {error_body}"
        )

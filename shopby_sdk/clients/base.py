import logging
from typing import TypeVar, Type

from httpx import HTTPStatusError, Response
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)

_ResponseType = TypeVar("_ResponseType")


class ShopbyServerApiClient:
    def __init__(self, server_access_token: str, server_system_key: str):
        self._access_token = server_access_token
        self._system_key = server_system_key
        self.base_url = "https://server-api.e-ncp.com"

    @property
    def common_header(self):
        return {
            "Authorization": f"Bearer {self._access_token}",
            "systemKey": self._system_key,
            "version": "1.0",
        }

    def handle_resp(self, resp: Response, type_model: Type[_ResponseType]) -> _ResponseType:
        self.raise_for_status(resp)

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

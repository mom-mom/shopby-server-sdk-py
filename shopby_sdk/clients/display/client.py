"""Display API 클라이언트"""

import httpx

from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.display.models import EventDetailResponse


class ShopbyServerDisplayApiClient(ShopbyServerApiClient):
    """Shopby Display Server API 클라이언트"""

    async def get_event_detail(self, event_no: int) -> EventDetailResponse:
        """
        기획전 단건 조회

        기획전 상세 정보를 조회하는 API입니다.

        Args:
            event_no: 기획전 번호

        Returns:
            EventDetailResponse: 기획전 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 1.0 헤더 추가
            headers = {"version": "1.0"}

            resp = await client.get(
                f"/events/{event_no}",
                headers=headers,
            )

            return self.handle_resp(resp, EventDetailResponse)

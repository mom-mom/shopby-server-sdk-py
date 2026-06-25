"""Workspace API 클라이언트 (인증/앱설치/외부스크립트/웹훅 관리)

OpenAPI: workspace-server (docs/api/workspace-server-public.yml)
"""

from datetime import datetime

import httpx

from shopby_sdk.base.kst import to_kst_string
from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.workspace.models import (
    AppInstalledExtendRequest,
    AppInstalledStatusResponse,
    AuthMeResponse,
    AuthTokenResponse,
    DeviceType,
    ExternalScriptItem,
    ExternalScriptRegisterRequest,
    ScriptType,
    WebhooksFailedResponse,
)


class ShopbyServerWorkspaceApiClient(ShopbyServerApiClient):
    """Shopby Workspace Server API 클라이언트

    ⚠️ 토큰 발급 엔드포인트(issue_token / issue_long_lived_token)는 access_token 을
    *발급받기 위한* API 이므로 Authorization/systemKey 헤더를 전송하지 않는다.
    해당 메서드만 사용할 경우 server_access_token / server_system_key 는 빈 값으로
    인스턴스를 생성해도 된다.
    """

    # ------------------------------------
    #  App Installed
    # ------------------------------------
    async def get_app_installed_status(self) -> AppInstalledStatusResponse:
        """
        앱 사용 상태 조회하기

        Returns:
            AppInstalledStatusResponse: 설치 앱 사용 상태
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get("/app-installed/status", headers=headers)
            return self.handle_resp(resp, AppInstalledStatusResponse)

    async def extend_app_installed(self, request: AppInstalledExtendRequest) -> None:
        """
        설치 앱 만료일 연장하기

        Args:
            request: 만료일 연장 요청 (주문번호, 결제금액, 요청일시, 결제타입)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.put("/app-installed/extend", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  Auth
    # ------------------------------------
    async def get_auth_me(self) -> AuthMeResponse:
        """
        access_token 을 발급한 어드민/몰 정보 조회하기

        Returns:
            AuthMeResponse: 어드민/몰 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get("/auth/me", headers=headers)
            return self.handle_resp(resp, AuthMeResponse)

    async def issue_token(
        self,
        *,
        client_id: str,
        client_secret: str,
        grant_type: str = "authorization_code",
        code: str | None = None,
        redirect_uri: str | None = None,
        refresh_token: str | None = None,
    ) -> AuthTokenResponse:
        """
        authorization code 로 단기 토큰 발급하기

        ⚠️ 이 API 는 토큰을 발급받기 위한 것이므로 Authorization/systemKey 헤더를
        전송하지 않는다. 바디는 OAuth 표준 snake_case 키로 전송한다.

        Args:
            client_id: 앱 client id
            client_secret: 앱 client secret
            grant_type: 인증 방식 (authorization_code | refresh_token)
            code: authorization code (grant_type=authorization_code 시)
            redirect_uri: 리다이렉트 URI
            refresh_token: 리프레시 토큰 (grant_type=refresh_token 시)

        Returns:
            AuthTokenResponse: 발급된 토큰 정보
        """
        return await self._request_token("/auth/token", client_id, client_secret, grant_type, code, redirect_uri, refresh_token)

    async def issue_long_lived_token(
        self,
        *,
        client_id: str,
        client_secret: str,
        grant_type: str = "authorization_code",
        code: str | None = None,
        redirect_uri: str | None = None,
        refresh_token: str | None = None,
    ) -> AuthTokenResponse:
        """
        authorization code 로 장기 토큰 발급하기

        ⚠️ Authorization/systemKey 헤더를 전송하지 않는다. (issue_token 참고)

        Args:
            client_id: 앱 client id
            client_secret: 앱 client secret
            grant_type: 인증 방식 (authorization_code | refresh_token)
            code: authorization code
            redirect_uri: 리다이렉트 URI
            refresh_token: 리프레시 토큰

        Returns:
            AuthTokenResponse: 발급된 장기 토큰 정보
        """
        return await self._request_token("/auth/token/long-lived", client_id, client_secret, grant_type, code, redirect_uri, refresh_token)

    async def _request_token(
        self,
        path: str,
        client_id: str,
        client_secret: str,
        grant_type: str,
        code: str | None,
        redirect_uri: str | None,
        refresh_token: str | None,
    ) -> AuthTokenResponse:
        """토큰 발급 공통 처리 (무인증, OAuth snake_case 바디)"""
        # OAuth 표준 키(snake_case)로 직접 구성 — BaseDto camelCase 변환을 회피
        body: dict[str, str] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": grant_type,
        }
        if code is not None:
            body["code"] = code
        if redirect_uri is not None:
            body["redirect_uri"] = redirect_uri
        if refresh_token is not None:
            body["refresh_token"] = refresh_token

        # Authorization/systemKey 미전송 — common_header 를 사용하지 않는다
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            headers = {"version": "1.0"}
            resp = await client.post(path, headers=headers, json=body)
            return self.handle_resp(resp, AuthTokenResponse)

    async def revoke_token(self, token: str) -> None:
        """
        장기 토큰 제거하기

        Args:
            token: 제거할 토큰
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.post("/auth/token/revoke", headers=headers, json={"token": token})
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  External Script
    # ------------------------------------
    async def get_external_scripts(
        self,
        script_types: list[ScriptType] | None = None,
        device_types: list[DeviceType] | None = None,
    ) -> list[ExternalScriptItem]:
        """
        외부 스크립트 조회하기

        Args:
            script_types: 조회할 스크립트 노출 위치 타입 목록
            device_types: 조회할 디바이스 타입 목록

        Returns:
            list[ExternalScriptItem]: 외부 스크립트 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if script_types is not None:
                params["scriptTypes"] = ",".join(script_types)
            if device_types is not None:
                params["deviceTypes"] = ",".join(device_types)

            resp = await client.get("/external-script", headers=headers, params=params)
            return self.handle_resp(resp, list[ExternalScriptItem])

    async def register_external_scripts(self, request: ExternalScriptRegisterRequest) -> None:
        """
        외부 스크립트 등록하기

        Args:
            request: 등록할 외부 스크립트 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.post("/external-script", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def delete_external_script(
        self,
        script_type: ScriptType | None = None,
        device_type: DeviceType | None = None,
    ) -> None:
        """
        외부 스크립트 삭제하기

        Args:
            script_type: 삭제할 스크립트 노출 위치 타입
            device_type: 삭제할 디바이스 타입
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if script_type is not None:
                params["scriptType"] = script_type
            if device_type is not None:
                params["deviceType"] = device_type

            resp = await client.delete("/external-script", headers=headers, params=params)
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  Webhook
    # ------------------------------------
    async def get_failed_webhooks(
        self,
        start_date_time: datetime,
        end_date_time: datetime,
        page: int | None = None,
        page_size: int | None = None,
        mall_nos: list[int] | None = None,
        shop_nos: list[int] | None = None,
        event_type: str | None = None,
        direction: str | None = None,
    ) -> WebhooksFailedResponse:
        """
        실패한 웹훅 조회하기

        Args:
            start_date_time: 조회 시작 일시 (필수)
            end_date_time: 조회 종료 일시 (필수)
            page: 페이지 번호
            page_size: 페이지 크기
            mall_nos: 샵바이 쇼핑몰 번호 목록
            shop_nos: 고도몰 상점 번호 목록
            event_type: 웹훅 이벤트 타입
            direction: 정렬 방향

        Returns:
            WebhooksFailedResponse: 실패한 웹훅 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "startDateTime": to_kst_string(start_date_time),
                "endDateTime": to_kst_string(end_date_time),
            }
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if mall_nos is not None:
                params["mallNos"] = ",".join(str(no) for no in mall_nos)
            if shop_nos is not None:
                params["shopNos"] = ",".join(str(no) for no in shop_nos)
            if event_type is not None:
                params["eventType"] = event_type
            if direction is not None:
                params["direction"] = direction

            resp = await client.get("/webhooks/failed", headers=headers, params=params)
            return self.handle_resp(resp, WebhooksFailedResponse)

"""Workspace API 모델 정의 (인증/앱설치/외부스크립트/웹훅 관리)

OpenAPI: workspace-server (docs/api/workspace-server-public.yml)

camelCase <-> snake_case 자동변환은 BaseDto 가 처리합니다.

⚠️ 인증(/auth/token) 엔드포인트의 요청 바디는 OAuth 표준 snake_case 키
(client_id, client_secret, grant_type 등)를 사용한다. 따라서 토큰 발급 요청은
client.py 에서 dict 로 직접 구성하며(BaseDto camelCase 변환 회피),
토큰 응답(AuthTokenResponse)은 BaseDto 의 validate_by_name(snake_case=필드명)으로 파싱한다.
"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime

# ---------------------------------------------------------------------------
# Literal 타입 별칭 (enum)
# ---------------------------------------------------------------------------

DeviceType = Literal["PC", "MOBILE"]
"""디바이스 타입"""

ScriptType = Literal[
    "MAIN",
    "COMMON_HEAD",
    "COMMON_FOOTER",
    "PRODUCT",
    "PRODUCT_LIST",
    "PRODUCT_SEARCH",
    "CART",
    "ORDER",
    "ORDER_DETAIL",
    "ORDER_COMPLETE",
    "DISPLAY_SECTION",
    "MEMBER_JOIN_COMPLETE",
    "MY_PAGE",
    "LOGIN",
]
"""외부 스크립트 노출 위치 타입"""


# ---------------------------------------------------------------------------
# App Installed
# ---------------------------------------------------------------------------
class AppInstalledStatusResponse(BaseDto):
    """
    설치 앱 사용 상태

    OpenAPI Schema: app-installed-status100495698
    """

    app_no: int = Field(..., description="앱 번호")
    app_name: str = Field(..., description="앱 이름")
    current_status: str = Field(..., description="현재 앱 사용 상태")
    expire_date_time: KstDatetime | None = Field(None, description="앱 만료일시")


class AppInstalledExtendRequest(BaseDto):
    """
    설치 앱 만료일 연장 요청

    OpenAPI Schema: app-installed-extend-1686580749
    """

    order_no: str = Field(..., description="주문번호")
    price: float = Field(..., description="결제 금액")
    request_date_time: str = Field(..., description="요청 일시")
    payment_type: str = Field(..., description="결제 타입")


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
class AuthTokenResponse(BaseDto):
    """
    토큰 발급 응답 (OAuth)

    OpenAPI Schema: auth-token1244629579 / auth-token-long-lived-2112938244

    JSON 응답 키는 snake_case(access_token 등)이며 BaseDto 의 validate_by_name
    설정으로 필드명 기준 파싱된다.
    """

    access_token: str = Field(..., description="액세스 토큰")
    refresh_token: str | None = Field(None, description="리프레시 토큰")
    scopes: str | None = Field(None, description="토큰 스코프")
    expire_in: str | None = Field(None, description="만료 시간")
    token_type: str | None = Field(None, description="토큰 타입")
    issued_at: str | None = Field(None, description="발급 일시")


class AuthMePartner(BaseDto):
    """auth/me - 파트너 정보"""

    partner_no: str | None = Field(None, description="파트너 어드민 토큰인 경우 파트너번호")
    partner_name: str | None = Field(None, description="파트너 어드민 토큰인 경우 파트너이름")


class AuthMeBusiness(BaseDto):
    """auth/me - 사업자(회사) 정보"""

    company_name: str | None = Field(None, description="회사명")
    business_registration_no: str | None = Field(None, description="사업자등록번호")
    representative_name: str | None = Field(None, description="대표자명")


class AuthMeMall(BaseDto):
    """auth/me - 쇼핑몰 정보"""

    mall_no: int = Field(..., description="쇼핑몰 번호")
    mall_name: str = Field(..., description="쇼핑몰 명")
    client_id: str = Field(..., description="쇼핑몰 client id")
    country_code: str = Field(..., description="국가 코드")
    front_type: str = Field(..., description="프론트 타입")
    plan: str = Field(..., description="요금제")
    mall_id: str | None = Field(None, description="쇼핑몰 ID")
    sno: int | None = Field(None, description="서비스 번호")
    shop_no: int | None = Field(None, description="고도몰 상점 번호")
    customer_center: dict[str, Any] | None = Field(None, description="고객센터 정보")
    domains: list[Any] = Field(default_factory=list, description="도메인 목록")


class AuthMeResponse(BaseDto):
    """
    access_token 을 발급한 어드민/몰 정보

    OpenAPI Schema: auth-me-1937932728
    """

    id: str | None = Field(None, description="어드민 ID")
    name: str | None = Field(None, description="어드민 이름")
    email: str | None = Field(None, description="이메일")
    mobile: str | None = Field(None, description="연락처")
    admin_role: str | None = Field(None, description="어드민 권한")
    solution_type: str | None = Field(None, description="솔루션 타입")
    department_name: str | None = Field(None, description="부서명")
    job_duty_name: str | None = Field(None, description="직무명")
    job_position_name: str | None = Field(None, description="직급명")
    partner: AuthMePartner | None = Field(None, description="파트너 정보")
    business: AuthMeBusiness | None = Field(None, description="사업자 정보")
    mall: AuthMeMall | None = Field(None, description="쇼핑몰 정보")


# ---------------------------------------------------------------------------
# External Script
# ---------------------------------------------------------------------------
class ExternalScriptContent(BaseDto):
    """외부 스크립트 등록 항목"""

    device_type: DeviceType = Field(..., description="디바이스 타입")
    script_type: ScriptType = Field(..., description="스크립트 노출 위치 타입")
    content: str = Field(..., description="추가될 스크립트")


class ExternalScriptRegisterRequest(BaseDto):
    """
    외부 스크립트 등록 요청

    OpenAPI Schema: external-script-301777223
    """

    script_contents: list[ExternalScriptContent] = Field(
        default_factory=list, description="등록할 외부 스크립트 목록"
    )


class ExternalScriptItem(BaseDto):
    """
    외부 스크립트 조회 항목

    OpenAPI Schema: external-script636480145 (items)
    """

    device_type: str = Field(..., description="디바이스 타입")
    script_type: str = Field(..., description="스크립트 노출 위치 타입")
    script_type_label: str = Field(..., description="스크립트 노출 위치 라벨")
    content: str = Field(..., description="스크립트 내용")
    register_date_time: KstDatetime | None = Field(None, description="등록 일시")
    update_date_time: KstDatetime | None = Field(None, description="수정 일시")


# ---------------------------------------------------------------------------
# Webhook
# ---------------------------------------------------------------------------
class WebhookFailedItem(BaseDto):
    """
    실패한 웹훅 항목

    OpenAPI Schema: webhooks-failed-380889068 (contents items)
    """

    event_type: str = Field(..., description="웹훅 이벤트 타입")
    solution_type: str = Field(..., description="솔루션 타입 (SHOPBY, GODO)")
    mall_no: int = Field(..., description="샵바이 쇼핑몰 번호")
    shop_no: int = Field(..., description="고도몰 상점 번호")
    webhook_url: str = Field(..., description="웹훅 수신 URL")
    http_method: str = Field(..., description="HTTP METHOD")
    data: str = Field(..., description="웹훅 송신 데이터")
    exception_type: str = Field(..., description="예외 타입")
    exception_message: str = Field(..., description="예외 메시지")
    exception_date_time: KstDatetime | None = Field(None, description="예외 발생 시간")


class WebhooksFailedResponse(BaseDto):
    """
    실패한 웹훅 조회 응답

    OpenAPI Schema: webhooks-failed-380889068
    """

    total_count: int = Field(..., description="전체 건수")
    contents: list[WebhookFailedItem] = Field(default_factory=list, description="실패한 웹훅 목록")

# Shopby Server SDK for Python

Python SDK for Shopby Server API - Type-safe API clients for all Shopby API domains.

11개 도메인 전체(255+ 엔드포인트)를 type-safe Pydantic 모델로 제공합니다.

## Installation

```bash
# Specific release (권장)
uv add git+https://github.com/mom-mom/shopby-server-sdk-py.git@v1.0.0

# Latest (main)
uv add git+https://github.com/mom-mom/shopby-server-sdk-py.git@main

# Using pip
pip install git+https://github.com/mom-mom/shopby-server-sdk-py.git@v1.0.0
```

## Configuration

환경변수를 통해 인증 정보를 전달합니다:

```bash
export SHOPBY_SERVER_ACCESS_TOKEN=your_access_token_here
export SHOPBY_SERVER_SYSTEM_KEY=your_system_key_here
export SHOPBY_BASE_URL=https://server-api.e-ncp.com  # optional (기본값)
```

> 로컬 개발 시에는 `.env.local` 파일에 위 값을 넣고 `uv run --env-file .env.local ...` 로 실행합니다.

## Authentication (토큰 발급)

server API 호출에 필요한 `access_token` 은 **workspace 도메인**을 통해 발급받습니다.

- `client_id` = 워크스페이스 > 셀러어드민 > 앱 상세의 **systemKey**
- `client_secret` = 앱 상세의 **secretKey**
- `code` = 쇼핑몰 어드민에서 앱 '실행' 시 리다이렉트 URL(`?code=...`)로 전달되는 **authorization code** (1회성)
- `redirect_uri` = 앱에 등록한 리다이렉트 URI

```python
from shopby_sdk.clients.workspace import ShopbyServerWorkspaceApiClient

# 토큰 발급 엔드포인트는 무인증이라 빈 자격증명으로 인스턴스 생성 가능
ws = ShopbyServerWorkspaceApiClient(server_access_token="", server_system_key="")

# 장기 토큰(server-to-server, 사실상 무기한) 발급
token = await ws.issue_long_lived_token(
    client_id="<앱 systemKey>",
    client_secret="<앱 secretKey>",
    grant_type="authorization_code",
    code="<쇼핑몰 어드민에서 받은 code>",
    redirect_uri="<앱에 등록한 redirect_uri>",
)
print(token.access_token)  # 이후 server_access_token 으로 사용 (systemKey = client_id)
```

- 단기 토큰(5분, 화면단/프론트용)은 `issue_token(...)` 사용
- 장기 토큰은 **앱에 등록한 IP**에서만 server API 호출이 가능합니다

## Available Domains

| Domain | Client | 비고 |
|--------|--------|------|
| products | `ShopbyServerProductsApiClient` | 상품 |
| order | `ShopbyServerOrderApiClient` | 주문 |
| member | `ShopbyServerMemberApiClient` | 회원 |
| display | `ShopbyServerDisplayApiClient` | 기획전/배너/카테고리/상품평 |
| claim | `ShopbyServerClaimApiClient` | 취소/반품/교환 |
| admin | `ShopbyServerAdminApiClient` | 운영자/계약/파트너 |
| delivery | `ShopbyServerDeliveryApiClient` | 배송비/입출고지 |
| manage | `ShopbyServerManageApiClient` | 적립금/문의/약관 |
| order_friends | `ShopbyServerOrderFriendsApiClient` | 통계/정산/CS |
| promotion | `ShopbyServerPromotionApiClient` | 쿠폰 |
| workspace | `ShopbyServerWorkspaceApiClient` | 인증/토큰/앱설치/외부스크립트/웹훅 |

모든 클라이언트는 `from shopby_sdk.clients.<domain> import <Client>` 로 import 합니다.

## Usage

### Products API

```python
import os
from shopby_sdk.clients.products import ShopbyServerProductsApiClient

client = ShopbyServerProductsApiClient(
    server_access_token=os.environ["SHOPBY_SERVER_ACCESS_TOKEN"],
    server_system_key=os.environ["SHOPBY_SERVER_SYSTEM_KEY"],
    base_url=os.environ.get("SHOPBY_BASE_URL"),  # optional
)

# Search products
products = await client.search_products_v2(keywords="샴푸", page_number=1, page_size=20)

# Get product detail
product = await client.get_product_detail_v3(mall_product_no=12345)
```

### Example Scripts

`scripts/` 폴더에 use case 별 예제 스크립트가 있습니다 (`docs/scripts.md` 참조):

```bash
# 상품 상세 조회 (V1 / V3)
uv run --env-file .env.local python scripts/get_product_detail_v1.py 12345
uv run --env-file .env.local python scripts/get_product_detail_v3.py 12345

# 상품 검색 / 변경 상품 / 부분 수정
uv run --env-file .env.local python scripts/search_products.py "검색어"
uv run --env-file .env.local python scripts/get_changed_products.py
uv run --env-file .env.local python scripts/patch_product.py 12345 "새 상품명"

# 주문 / 회원
uv run --env-file .env.local python scripts/get_orders.py
uv run --env-file .env.local python scripts/get_members.py

# 읽기 전용 라이브 스모크 테스트 (전 도메인 GET 검증)
uv run --env-file .env.local python scripts/smoke_test_readonly.py
```

## Development

### Setup

```bash
uv sync                # Install dependencies
uv sync --group dev    # Install with dev dependencies
```

### Code Quality

```bash
uv run ruff check shopby_sdk/    # Lint
uv run ruff format shopby_sdk/   # Format
uv run isort shopby_sdk/         # Sort imports
uv run black shopby_sdk/         # Format with black
```

## Project Structure

```
shopby_sdk/
├── base/
│   ├── dto.py                    # BaseDto (camelCase <-> snake_case 자동 변환)
│   └── kst.py                    # KstDatetime / KstDate (KST timezone 처리)
└── clients/
    ├── base.py                   # ShopbyServerApiClient base class
    ├── products/                 # 도메인별 폴더: client.py + models.py (또는 models/ 패키지)
    │   ├── client.py
    │   └── models/               # 큰 도메인은 models/ 패키지로 분리
    ├── order/                    # (products, order 는 models/ 패키지)
    ├── member/ display/ claim/ admin/ delivery/
    ├── manage/ order_friends/ promotion/ workspace/
    └── examples/                 # 기본 예제

docs/
├── api-implementation-guide.md   # 새 도메인/엔드포인트 구현 가이드
├── scripts.md                    # 예제 스크립트 설명
└── api/                          # OpenAPI 스펙 (11개 도메인 yml)
```

## Adding New API Domains

새 Shopby API 도메인/엔드포인트 추가 방법은 `docs/api-implementation-guide.md` 를 참고하세요.

## License

MIT

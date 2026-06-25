# Shopby SDK for Python

Python SDK for Shopby - Type-safe API clients for all Shopby API domains.

두 종류의 API 를 모두 제공합니다:

- **Server API** (`server-api.e-ncp.com`) — 11개 도메인, 255+ 엔드포인트. Bearer 토큰 + systemKey 인증. → `shopby_sdk.clients.*`
- **Shop(Client) API** (`shop-api.e-ncp.com`) — 8개 도메인, 141개 **공개(인증 불필요)** 엔드포인트. `clientId` 헤더만 사용. → `shopby_sdk.shop.*`

모두 type-safe Pydantic 모델로 제공합니다.

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

## Shop (Client) API — 공개/인증 불필요

스토어프론트(`shop-api.e-ncp.com`)의 **개인을 특정하지 않는 공개 엔드포인트**만 SDK 화한
모음입니다. 회원 로그인(`accessToken`) 없이 `clientId` 헤더만으로 호출합니다.
(장바구니/내주문/취소/내쿠폰 등 회원 인증이 필요한 개인 데이터 엔드포인트는 **제외**)

```python
import os
from shopby_sdk.shop.product import ShopbyShopProductApiClient

client = ShopbyShopProductApiClient(
    client_id=os.environ["SHOPBY_SHOP_CLIENT_ID"],  # 쇼핑몰 클라이언트 아이디 (회원 인증 아님)
    platform="PC",                                  # PC | MOBILE_WEB | AOS | IOS (기본 PC)
    base_url=os.environ.get("SHOPBY_SHOP_BASE_URL"),  # optional (기본 https://shop-api.e-ncp.com)
)

result = await client.search_products(params={"pageNumber": 1, "pageSize": 20})
detail = await client.get_product(product_no=132652000)
```

| Domain | Client | 공개 엔드포인트 |
|--------|--------|------|
| product | `ShopbyShopProductApiClient` | 41 (상품/브랜드/사은품/추가할인/검색) |
| display | `ShopbyShopDisplayApiClient` | 48 (카테고리/배너/기획전/팝업/진열/상품평·문의 읽기) |
| manage | `ShopbyShopManageApiClient` | 23 (약관/공휴일/주소/게시판읽기/문의설정) |
| member | `ShopbyShopMemberApiClient` | 12 (몰설정 + 검증유틸) |
| promotion | `ShopbyShopPromotionApiClient` | 6 (쿠폰 공개조회) |
| order | `ShopbyShopOrderApiClient` | 5 (주문/장바구니/배송 설정값) |
| admin | `ShopbyShopAdminApiClient` | 5 (몰 정보) |
| marketing | `ShopbyShopMarketingApiClient` | 1 (SNS 공유 설정) |

> `clientId` 는 쇼핑몰 식별자이며 회원 인증 정보가 아닙니다. shop API 공개 호출에 필요한 헤더는
> `clientId` / `platform` / `version` 뿐이며, base 클래스가 자동 주입합니다.

```bash
# shop 공개 API 라이브 스모크 (read-only, dev 몰)
export SHOPBY_SHOP_CLIENT_ID=...
uv run python scripts/smoke_test_shop_readonly.py
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
├── clients/                      # Server API (server-api.e-ncp.com)
│   ├── base.py                   # ShopbyServerApiClient base class
│   ├── products/                 # 도메인별 폴더: client.py + models.py (또는 models/ 패키지)
│   │   ├── client.py
│   │   └── models/               # 큰 도메인은 models/ 패키지로 분리
│   ├── order/                    # (products, order 는 models/ 패키지)
│   ├── member/ display/ claim/ admin/ delivery/
│   ├── manage/ order_friends/ promotion/ workspace/
│   └── examples/                 # 기본 예제
└── shop/                         # Shop(Client) API (shop-api.e-ncp.com) — 공개 전용
    ├── base.py                   # ShopbyShopApiClient (clientId/platform 헤더)
    ├── product/ display/         # (models/ 패키지)
    └── manage/ member/ promotion/ order/ admin/ marketing/

docs/
├── api-implementation-guide.md   # 새 도메인/엔드포인트 구현 가이드
├── scripts.md                    # 예제 스크립트 설명
└── api/                          # OpenAPI 스펙 (server 11 + shop 10 yml)
```

## Adding New API Domains

새 Shopby API 도메인/엔드포인트 추가 방법은 `docs/api-implementation-guide.md` 를 참고하세요.

## License

MIT

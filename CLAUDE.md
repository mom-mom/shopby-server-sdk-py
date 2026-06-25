# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python SDK for Shopby - generates type-safe API clients from OpenAPI specifications.

두 종류의 API 를 다룬다:
- **Server API** (`server-api.e-ncp.com`): Bearer 토큰 + systemKey 인증. `shopby_sdk/clients/` — 11개 도메인 전체.
- **Shop(Client) API** (`shop-api.e-ncp.com`): `clientId` 헤더 인증. `shopby_sdk/shop/` — **공개(인증 불필요) 엔드포인트만** (8개 도메인, 141개). 회원 토큰(accessToken)이 필요한 개인 데이터 엔드포인트는 의도적으로 제외.

## Development Commands

```bash
# Setup
uv sync                          # Install dependencies
uv sync --group dev              # Install with dev dependencies

# Code Quality
uv run ruff check shopby_sdk/    # Lint code
uv run ruff format shopby_sdk/   # Format code
uv run isort shopby_sdk/         # Sort imports
uv run black shopby_sdk/         # Format with black
```

## Architecture

### Core Pattern: BaseDto + API Clients

All API models inherit from `BaseDto` (in `shopby_sdk/base/dto.py`) which provides automatic **camelCase ↔ snake_case** conversion between Python code and API JSON responses.

```python
# API returns: {"mallProductNo": 123}
# Python uses: product.mall_product_no
```

### File Structure

```
shopby_sdk/
├── base/
│   └── dto.py                    # BaseDto with camelCase conversion
├── clients/                      # Server API (server-api.e-ncp.com)
│   ├── base.py                   # ShopbyServerApiClient base class
│   ├── examples/                 # Reference implementation
│   └── {api_name}/               # Each API domain gets a folder
│       ├── __init__.py           # Exports
│       ├── client.py             # API client methods
│       └── models.py             # Pydantic models (or models/ package)
└── shop/                         # Shop(Client) API (shop-api.e-ncp.com) — 공개 전용
    ├── base.py                   # ShopbyShopApiClient base class
    └── {api_name}/               # product/display 는 models/ 패키지, 나머지는 models.py
```

### API Client Base Classes

`ShopbyServerApiClient` (in `shopby_sdk/clients/base.py`) — **Server API**:
- Base URL: `https://server-api.e-ncp.com`
- Auth: Bearer token + systemKey headers
- All `clients/*` inherit from this and use httpx.AsyncClient

`ShopbyShopApiClient` (in `shopby_sdk/shop/base.py`) — **Shop(Client) API**:
- Base URL: `https://shop-api.e-ncp.com`
- Auth: `clientId` + `platform` 헤더 (회원 토큰/systemKey 없음)
- All `shop/*` inherit from this. 공개 전용이라 `accessToken`(회원 토큰)은 지원하지 않음.
- 각 메서드는 `version` 헤더만 직접 지정(clientId/platform 은 base 가 주입), 바디는
  `model_dump(by_alias=True, exclude_none=True, mode="json")` 로 직렬화.

> Shop SDK 스코프: shop OpenAPI 의 `accessToken` 헤더가 필수(required)인 엔드포인트와, 태그상
> 개인 데이터(MyOrder/Cart/내쿠폰/내상품평/회원프로필 등)인 엔드포인트는 제외했다. 공개 카탈로그
> 읽기(accessToken optional)는 익명 호출 전용으로 포함한다.

## Docs

```
docs/
├── api-implementation-guide.md      # ⚠️ API 구현 시 반드시 먼저 읽을 것
├── scripts.md                       # 테스트 스크립트 실행 가이드
└── api/                             # OpenAPI 스펙 (yml) - 11개 도메인 전체
    ├── product-server-public.yml
    ├── display-server-public.yml
    ├── order-server-public.yml
    ├── member-server-public.yml
    ├── claim-server-public.yml
    ├── admin-server-public.yml
    ├── delivery-server-public.yml
    ├── manage-server-public.yml
    ├── order-friends-server-public.yml
    ├── promotion-server-public.yml
    └── workspace-server-public.yml
```

스펙 원본 URL: `https://server-docs.shopby.co.kr/spec/{domain}-server-public.yml`

## Adding New APIs

**⚠️ CRITICAL: MUST READ `docs/api-implementation-guide.md` FIRST**

This guide contains all implementation patterns, type mapping rules, parameter handling, and common pitfalls. Do not proceed without reading it.

**Reference implementations (11개 도메인 전체 구현 완료, 100% 엔드포인트 커버리지):**
- `shopby_sdk/clients/products/` - Products API (상품) — models/ 패키지 구조
- `shopby_sdk/clients/order/` - Order API (주문) — models/ 패키지 구조
- `shopby_sdk/clients/member/` - Member API (회원)
- `shopby_sdk/clients/display/` - Display API (기획전/배너/카테고리/상품평 등)
- `shopby_sdk/clients/claim/` - Claim API (취소/반품/교환)
- `shopby_sdk/clients/admin/` - Admin API (운영자/계약/파트너)
- `shopby_sdk/clients/delivery/` - Delivery API (배송비/입출고지)
- `shopby_sdk/clients/manage/` - Manage API (적립금/문의/약관)
- `shopby_sdk/clients/order_friends/` - Order Friends API (통계/정산/CS)
- `shopby_sdk/clients/promotion/` - Promotion API (쿠폰)
- `shopby_sdk/clients/workspace/` - Workspace API (인증/토큰/앱설치/외부스크립트/웹훅)
- `shopby_sdk/clients/examples/` - 기본 예제

> 인증 주의: workspace `/auth/token`·`/auth/token/long-lived` 는 토큰을 *발급받는* 엔드포인트라
> Authorization/systemKey 헤더를 보내지 않으며, 바디는 OAuth snake_case 키(client_id 등)를 사용함.

> 참고: 거대 상품 등록/수정(create/update product) 등 일부 200+ 필드 중첩 요청 페이로드는
> `dict[str, Any]`로 두고 docstring에 OpenAPI schema 이름을 명시함. 필요 시 점진적 타입화 가능.

**Scripts reference:** `docs/scripts.md` - 테스트 스크립트 실행 및 작성 가이드

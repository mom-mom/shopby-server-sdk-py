# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python SDK for Shopby Products API - generates type-safe API clients from OpenAPI specifications in `shopby-docs/product-server-public.yml`.

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
├── clients/
│   ├── base.py                   # ShopbyServerApiClient base class
│   ├── examples/                 # Reference implementation
│   └── {api_name}/               # Each API domain gets a folder
│       ├── __init__.py           # Exports
│       ├── client.py             # API client methods
│       └── models.py             # Pydantic models
```

### API Client Base Class

`ShopbyServerApiClient` (in `shopby_sdk/clients/base.py`):
- Base URL: `https://server-api.e-ncp.com`
- Auth: Bearer token + systemKey headers
- All clients inherit from this and use httpx.AsyncClient

## Adding New APIs

**⚠️ CRITICAL: MUST READ `claude-docs/api-implementation-guide.md` FIRST**

This guide contains all implementation patterns, type mapping rules, parameter handling, and common pitfalls. Do not proceed without reading it.

**Reference implementations:**
- `shopby_sdk/clients/products/` - Products API
- `shopby_sdk/clients/display/` - Display API (기획전 등)
- `shopby_sdk/clients/order/` - Order API (주문 등)
- `shopby_sdk/clients/examples/` - 기본 예제

**Scripts reference:** `claude-docs/scripts.md` - 테스트 스크립트 가이드

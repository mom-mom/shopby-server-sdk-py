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
uv run ruff check src/           # Lint code
uv run ruff format src/          # Format code
uv run isort src/                # Sort imports
uv run black src/                # Format with black
```

## Architecture

### Core Pattern: BaseDto + API Clients

All API models inherit from `BaseDto` (in `src/base/dto.py`) which provides automatic **camelCase ↔ snake_case** conversion between Python code and API JSON responses.

```python
# API returns: {"mallProductNo": 123}
# Python uses: product.mall_product_no
```

### File Structure

```
src/
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

`ShopbyServerApiClient` (in `src/clients/base.py`):
- Base URL: `https://server-api.e-ncp.com`
- Auth: Bearer token + systemKey headers
- All clients inherit from this and use httpx.AsyncClient

## Adding New APIs

**⚠️ CRITICAL: MUST READ `claude-docs/api-implementation-guide.md` FIRST**

This guide contains all implementation patterns, type mapping rules, parameter handling, and common pitfalls. Do not proceed without reading it.

Reference implementations: `src/clients/products/` and `src/clients/examples/`

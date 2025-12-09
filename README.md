# Shopby Server SDK for Python

Python SDK for Shopby Server API - Type-safe API clients for all Shopby API domains.

## Installation

```bash
# Latest version
uv add git+https://github.com/mom-mom/shopby-server-sdk-py.git

# Specific tag/release
uv add git+https://github.com/mom-mom/shopby-server-sdk-py.git@v0.1.0

# Specific branch
uv add git+https://github.com/mom-mom/shopby-server-sdk-py.git@main

# Using pip
pip install git+https://github.com/mom-mom/shopby-server-sdk-py.git
```

## Configuration

환경변수를 통해 인증 정보를 전달합니다:

```bash
export SHOPBY_ACCESS_TOKEN=your_access_token_here
export SHOPBY_SYSTEM_KEY=your_system_key_here
export SHOPBY_BASE_URL=https://server-api.e-ncp.com  # optional
```

## Usage

### Products API

```python
import os
from shopby_sdk.clients.products import ShopbyServerProductsApiClient

# 환경변수에서 인증 정보 읽기
client = ShopbyServerProductsApiClient(
    server_access_token=os.environ["SHOPBY_ACCESS_TOKEN"],
    server_system_key=os.environ["SHOPBY_SYSTEM_KEY"],
    base_url=os.environ.get("SHOPBY_BASE_URL"),  # optional
)

# Search products
products = await client.search_products_v2(
    keywords="샴푸",
    page_number=1,
    page_size=20
)

# Get product detail
product = await client.get_product_detail_v3(mall_product_no=12345)
```

### Example Scripts

`scripts/` 폴더에 use case 별 예제 스크립트가 있습니다:

```bash
# 상품 상세 조회
uv run --env-file .env.local python scripts/get_product_detail.py 12345

# 상품 검색
uv run --env-file .env.local python scripts/search_products.py "검색어"

# 변경된 상품 조회
uv run --env-file .env.local python scripts/get_changed_products.py

# 상품 수정
uv run --env-file .env.local python scripts/patch_product.py 12345 "새 상품명"
```

## Development

### Setup

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --group dev
```

### Code Quality

```bash
# Lint
uv run ruff check shopby_sdk/

# Format
uv run ruff format shopby_sdk/

# Sort imports
uv run isort shopby_sdk/

# Format with black
uv run black shopby_sdk/
```

## Project Structure

```
shopby_sdk/
├── base/
│   └── dto.py                    # BaseDto with camelCase conversion
├── clients/
│   ├── base.py                   # ShopbyServerApiClient base class
│   ├── products/                 # Products API
│   │   ├── client.py
│   │   └── models.py
│   └── examples/                 # Reference implementations
scripts/
├── get_product_detail.py         # 상품 상세 조회 예제
├── search_products.py            # 상품 검색 예제
├── get_changed_products.py       # 변경된 상품 조회 예제
└── patch_product.py              # 상품 수정 예제
```

## Adding New API Domains

See `claude-docs/api-implementation-guide.md` for detailed instructions on adding new Shopby API domains.

## License

MIT

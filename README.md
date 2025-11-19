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

Create environment files for your configuration:

```bash
# Development
cp .dev.env.example .dev.env

# Production
cp .prod.env.example .prod.env
```

Edit the files with your credentials:
```env
SHOPBY_ACCESS_TOKEN=your_access_token_here
SHOPBY_SYSTEM_KEY=your_system_key_here
```

## Usage

### Products API

```python
from shopby_sdk.clients.products import ShopbyServerProductsApiClient
from shopby_sdk.config import Settings

# Load settings
settings = Settings()

# Initialize client
client = ShopbyServerProductsApiClient(
    access_token=settings.shopby_server_access_token,
    system_key=settings.shopby_server_system_key
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
└── config.py                     # Settings management
```

## Adding New API Domains

See `claude-docs/api-implementation-guide.md` for detailed instructions on adding new Shopby API domains.

## License

MIT

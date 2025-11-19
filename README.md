# Shopby Server SDK for Python

Python SDK for Shopby Server API - Type-safe API clients for all Shopby API domains.

## Installation

### From GitHub Repository (Recommended for Internal Use)

```bash
# Using uv
uv add git+https://github.com/mom-mom/shopby-server-sdk-py.git

# Using pip
pip install git+https://github.com/mom-mom/shopby-server-sdk-py.git
```

### Install Specific Version

```bash
# Install from specific tag/release
uv add git+https://github.com/mom-mom/shopby-server-sdk-py.git@v0.1.0

# Install from specific branch
uv add git+https://github.com/mom-mom/shopby-server-sdk-py.git@main
```

### From GitHub Packages (After First Release)

```bash
# Configure GitHub Packages (one-time setup)
uv pip config set global.extra-index-url https://pypi.pkg.github.com/mom-mom

# Install package
uv add shopby-server-sdk-py
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
from shopby_server_sdk_py.clients.products import ShopbyServerProductsApiClient
from shopby_server_sdk_py.config import Settings

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
uv run ruff check src/

# Format
uv run ruff format src/

# Sort imports
uv run isort src/

# Format with black
uv run black src/
```

## Project Structure

```
src/
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

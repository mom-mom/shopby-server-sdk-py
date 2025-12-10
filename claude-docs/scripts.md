# Scripts 가이드

이 문서는 `scripts/` 폴더의 예제 스크립트들에 대한 설명입니다. API 구현이나 디버깅 시 참고용으로 사용합니다.

## 실행 방법

모든 스크립트는 `.env.local` 파일에서 환경변수를 로드하여 실행합니다:

```bash
uv run --env-file .env.local python scripts/<script_name>.py [args...]
```

### 필수 환경변수

`.env.local` 파일에 다음 환경변수가 필요합니다:

```env
SHOPBY_SERVER_ACCESS_TOKEN=your_access_token
SHOPBY_SERVER_SYSTEM_KEY=your_system_key
SHOPBY_BASE_URL=https://server-api.e-ncp.com  # optional
```

---

## 스크립트 목록

### 1. get_product_detail_v1.py - 상품 상세 조회 (Version 1.0)

**용도**: 단일 상품의 상세 정보 조회 (Version 1.0)

**실행**:
```bash
uv run --env-file .env.local python scripts/get_product_detail_v1.py <mall_product_no>
```

**사용 Client/Method**:
- Client: `ShopbyServerProductsApiClient`
- Method: `get_product_detail(mall_product_no: int)`
- Response Model: `ProductDetailV1Response`

**주요 응답 필드**:
- `mall_product` - 상품 정보 (`V1MallProduct`)
  - `product_name` - 상품명
  - `sale_status_type` - 판매상태 (READY, ONSALE, FINISHED, STOP, PROHIBITION)
  - `sale_price` - 판매가
- `mall_product_images` - 상품 이미지 목록 (`list[V1MallProductImage]`)
- `mall_product_option_web_models` - 옵션 목록 (`list[V1MallProductOption]`)
- `mall_product_inputs` - 구매자 작성형 정보 (`list[V1MallProductInput]`)

---

### 2. get_product_detail_v3.py - 상품 상세 조회 (Version 3.0)

**용도**: 단일 상품의 상세 정보 조회 (Version 3.0)

**실행**:
```bash
uv run --env-file .env.local python scripts/get_product_detail_v3.py <mall_product_no>
```

**사용 Client/Method**:
- Client: `ShopbyServerProductsApiClient`
- Method: `get_product_detail_v3(mall_product_no: int)`
- Response Model: `ProductDetailV3Response`

**주요 응답 필드**:
- `product_name` - 상품명
- `sale_status_type` - 판매상태 (READY, ONSALE, FINISHED, STOP, PROHIBITION)
- `sale_price` - 판매가
- `options` - 옵션 목록 (`list[ProductOption]`)
- `mall_product_images` - 상품 이미지 목록

---

### 3. search_products.py - 상품 검색

**용도**: 키워드 또는 필터 조건으로 상품 검색

**실행**:
```bash
uv run --env-file .env.local python scripts/search_products.py [검색어]
```

**사용 Client/Method**:
- Client: `ShopbyServerProductsApiClient`
- Method: `search_products_v2(...)`
- Response Model: `ProductSearchV2Response`

**주요 파라미터**:
- `keywords` - 검색어
- `page_number` - 페이지 번호
- `page_size` - 페이지 크기 (최대 100)
- `sale_status` - 판매 상태 필터
- `order_by` - 정렬 기준 (RECENT_PRODUCT, SALE_YMD)

**주요 응답 필드**:
- `total_count` - 전체 상품 수
- `items` - 검색된 상품 목록 (`list[ProductSearchItem]`)
  - `product_no` - 상품번호
  - `product_name` - 상품명
  - `sale_price` - 판매가
  - `discounted_price` - 할인 적용가

---

### 4. get_changed_products.py - 변경된 상품 조회

**용도**: 특정 시점 이후 등록/수정된 상품 번호 목록 조회

**실행**:
```bash
uv run --env-file .env.local python scripts/get_changed_products.py
```

**사용 Client/Method**:
- Client: `ShopbyServerProductsApiClient`
- Method: `get_changed_product_nos(...)`
- Response Model: `ChangedProductsResponse`

**주요 파라미터**:
- `as_of` - 조회 기준 시점 (`datetime`)
- `sort_by` - 정렬 기준 (REGISTERED_AT, UPDATED_AT)
- `size` - 페이지 크기
- `direction` - 정렬 방향 (ASC, DESC)

**주요 응답 필드**:
- `total_count` - 전체 상품 수
- `contents` - 변경된 상품 목록 (`list[ChangedProductItem]`)
  - `product_no` - 상품 번호
  - `registered_at` - 등록일
  - `updated_at` - 수정일

---

### 5. patch_product.py - 상품 수정

**용도**: 상품 정보 부분 수정

**실행**:
```bash
uv run --env-file .env.local python scripts/patch_product.py <product_no> <new_product_name>
```

**사용 Client/Method**:
- Client: `ShopbyServerProductsApiClient`
- Method: `patch_product_v2(product_no: int, request: PatchProductV2Request)`
- Request Model: `PatchProductV2Request`
- Response: `None` (204 No Content)

**PatchProductV2Request 주요 필드**:
- `product_name` - 상품명
- `sale_price` (via `price.sale_price`) - 판매가
- `stock_quantity` - 재고 수량
- `option` - 옵션 설정 (`PatchOptionInfo`)
- `image` - 이미지 설정 (`PatchImageInfo`)
- `sale_period_info` - 판매 기간 설정

---

## Display API

### 6. get_event_detail.py - 기획전 단건 조회

**용도**: 기획전 상세 정보 조회

**실행**:
```bash
uv run --env-file .env.local python scripts/get_event_detail.py <event_no>
```

**사용 Client/Method**:
- Client: `ShopbyServerDisplayApiClient`
- Method: `get_event_detail(event_no: int)`
- Response Model: `EventDetailResponse`

**주요 응답 필드**:
- `event_name` - 기획전 이름
- `event_type` - 기획전 유형 (GENERAL, EXTERNAL)
- `event_yn` - 이벤트 여부
- `register_ymdt` - 등록일
- `event_sections` - 섹션 목록 (`list[EventSection]`)
  - `event_section_name` - 섹션명
  - `event_section_value.mall_products` - 섹션 내 상품 목록

---

## Client/Model Import 경로

```python
# Products Client
from shopby_sdk.clients.products import ShopbyServerProductsApiClient

# Display Client
from shopby_sdk.clients.display import ShopbyServerDisplayApiClient

# Response Models
from shopby_sdk.clients.products.models import (
    # V1 상품 상세
    ProductDetailV1Response,
    V1MallProduct,
    V1MallProductImage,
    V1MallProductOption,
    V1MallProductInput,
    # V3 상품 상세
    ProductDetailV3Response,
    # 검색
    ProductSearchV2Response,
    ProductSearchItem,
    # 변경 상품 목록
    ChangedProductsResponse,
    ChangedProductItem,
    # 상품 리스트 검색
    ProductListSearchResponse,
    ProductListItem,
)

# Request Models (PATCH용)
from shopby_sdk.clients.products.models import (
    PatchProductV2Request,
    PatchPriceInfo,
    PatchOptionInfo,
    PatchOption,
    PatchImageInfo,
    PatchProductImage,
    # ... 기타 Patch* 모델들
)
```

---

## 디버깅 팁

### 응답 전체 출력
```python
# JSON으로 출력
print(product.model_dump_json(indent=2, by_alias=True))

# dict로 출력
print(product.model_dump(by_alias=True))
```

### 에러 발생 시 상세 로깅
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 특정 필드만 확인
```python
# V1 API 옵션 정보
for opt in result.mall_product_option_web_models:
    print(f"옵션: {opt.option_name}={opt.option_value}, 재고: {opt.stock_cnt}")

# V1 API 이미지 URL
for img in result.mall_product_images:
    print(f"이미지: {img.image_url} (메인: {img.main_yn})")
```

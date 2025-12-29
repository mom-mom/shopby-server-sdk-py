# Shopby Products API 구현 가이드

## 파일 구조

```
shopby_sdk/clients/{domain_name}/
├── __init__.py      # exports 정의
├── client.py        # API 클라이언트 클래스
└── models.py        # Pydantic 모델 정의
```

## 구현 순서

**전체 흐름:**
1. API 스펙 찾기 (OpenAPI yml)
2. models.py 작성
3. client.py 작성
4. __init__.py 작성
5. **테스트 스크립트 작성** (scripts/ 폴더)
6. 테스트 실행으로 검증

### 1. API 스펙 찾기
```bash
# API 이름으로 검색
grep -n "summary: {API_이름}" shopby-docs/product-server-public.yml

# endpoint 경로 찾기
grep -n "/{path}" shopby-docs/product-server-public.yml

# schema 정의 찾기
grep -n "{schema_name}:" shopby-docs/product-server-public.yml
```

### 2. models.py 작성
- **중요**: UTF-8 인코딩 유지 (한글 깨짐 주의)
- `BaseDto` 상속 → camelCase ↔ snake_case 자동 변환
- 중첩 객체는 별도 클래스로 분리
- 모든 필드에 `Field(..., description="...")` 사용
- Optional 필드는 `| None` + `Field(None, ...)`
- **Best Practice**: 클래스 docstring에 OpenAPI 스키마 이름 명시

**예제:**
```python
from typing import Any, Literal
from pydantic import Field
from shopby_sdk.base.dto import BaseDto

class NestedModel(BaseDto):
    field_name: str = Field(..., description="설명")

class MainResponse(BaseDto):
    """
    API 응답 모델

    OpenAPI Schema: schema-name-from-openapi-spec
    """
    some_field: str = Field(..., description="필드 설명")
    nested: NestedModel = Field(..., description="중첩 객체")
    optional_field: str | None = Field(None, description="선택 필드")
    list_field: list[dict[str, Any]] = Field(default_factory=list, description="리스트 필드")
```

### 3. client.py 작성
- `ShopbyServerApiClient` 상속
- httpx.AsyncClient 사용
- 필요시 헤더 추가 (예: version)
- `self.handle_resp(resp, ResponseModel)` 로 응답 처리 (에러 핸들링 + 파싱)

**기본 예제:**
```python
import httpx
from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.{domain_name}.models import ResponseModel

class ShopbyServer{DomainName}ApiClient(ShopbyServerApiClient):
    async def method_name(self, param: int) -> ResponseModel:
        """API 설명"""
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}  # API 버전에 맞게 설정

            resp = await client.get(
                f"/path/{param}",
                headers=headers,
            )

            return self.handle_resp(resp, ResponseModel)
```

**요청 파라미터 타입 지정:**
```python
from datetime import datetime
from typing import Literal
from shopby_sdk.base.kst import to_kst_string

async def search_products(
    self,
    # 필수 파라미터
    as_of: datetime,                           # Datetime → datetime 타입
    sort_by: Literal["CREATED", "UPDATED"],    # Enum → Literal
    size: int,                                 # 숫자 → int
    # 선택 파라미터
    direction: Literal["ASC", "DESC"] | None = None,
    start_date: datetime | None = None,        # Optional datetime
    keywords: str | None = None,               # Optional string
) -> ResponseModel:
    """
    상품 검색 API

    Args:
        as_of: 조회 기준시점 (KST로 자동 변환)
        sort_by: 정렬 기준
        size: 페이지 크기
        direction: 정렬 방향 (default: ASC)
        start_date: 시작일 (선택)
        keywords: 검색어 (선택)
    """
    async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
        # 쿼리 파라미터 구성
        params: dict[str, str | int | bool] = {
            "asOf": to_kst_string(as_of),      # datetime → KST 문자열
            "sortBy": sort_by,
            "size": size,
        }

        # Optional 파라미터 처리
        if direction is not None:
            params["direction"] = direction
        if start_date is not None:
            params["startDate"] = to_kst_string(start_date)  # datetime → KST 문자열
        if keywords is not None:
            params["keywords"] = keywords

        resp = await client.get("/search", params=params)
        resp.raise_for_status()

        return ResponseModel.model_validate(resp.json())
```

**핵심 규칙:**
- 요청 파라미터: Python `datetime` 타입으로 받기
- API 전송 시: `to_kst_string()`으로 변환
- Optional: `datetime | None = None`
- None 체크 후 변환

### 4. __init__.py 작성
```python
from shopby_sdk.clients.{domain_name}.client import ShopbyServer{DomainName}ApiClient
from shopby_sdk.clients.{domain_name}.models import ResponseModel

__all__ = [
    "ShopbyServer{DomainName}ApiClient",
    "ResponseModel",
]
```

### 5. 테스트 스크립트 작성

`scripts/` 폴더에 테스트용 스크립트 생성:

```python
"""
{API 설명}

Usage:
    uv run --env-file .env.local python scripts/{script_name}.py <param>
"""

import asyncio
import os
import sys

from shopby_sdk.clients.{domain_name} import ShopbyServer{DomainName}ApiClient


async def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/{script_name}.py <param>")
        sys.exit(1)

    param = int(sys.argv[1])

    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_SERVER_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SERVER_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServer{DomainName}ApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    result = await client.method_name(param)
    print(f"필드1: {result.field1}")
    print(f"필드2: {result.field2}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 6. 테스트 실행

```bash
uv run --env-file .env.local python scripts/{script_name}.py <test_value>
```

## 주의사항

### 인코딩
- **절대 주의**: 한글 description이 깨지지 않도록 UTF-8 유지
- Write 툴 사용 시 자동으로 UTF-8 적용됨

### API 버전
- 헤더에 `version` 필드 확인
- Version 3.0인 경우: `headers = {"version": "3.0"}`

### 필드 타입
- OpenAPI `type: number` → 문맥에 맞게 `int` 또는 `float`
  - 번호(No), 개수(Cnt), 순서(Order) 등 → `int`
  - 가격(Price), 금액(Amt), 비율(Rate) 등 → `float`
  - description과 example을 보고 판단
- OpenAPI `type: string` + Enum → Python `Literal["A", "B"]`
- OpenAPI `type: array` → Python `list[...]`
- OpenAPI `nullable` → Python `| None`
- **Datetime/Date 필드**: Shopby API는 timezone 명시가 없으면 KST 사용
  - `*_ymdt` (날짜+시간) → `KstDatetime` 또는 `KstDatetime | None`
  - `*_ymd` (날짜만) → `KstDate` 또는 `KstDate | None`
  - `registered_at`, `updated_at` 등 → `KstDatetime | None`
  ```python
  from shopby_sdk.base.kst import KstDate, KstDatetime

  class MyModel(BaseDto):
      created_at: KstDatetime              # 필수 datetime
      updated_at: KstDatetime | None       # 선택 datetime
      start_date: KstDate                  # 필수 date
      end_date: KstDate | None             # 선택 date
  ``` 

### 복잡한 스키마
- **원칙**: 모든 필드를 최대한 정확하게 구현
- 중첩 객체는 별도 클래스로 분리하여 타입 안정성 확보
- `dict[str, Any]` 임시처리는 **정말 불가피할 때만** 사용
  - 예: 스펙에 명확한 타입 정의가 없는 경우
  - 예: `oneOf`로 여러 타입이 혼재된 경우

### 파라미터 처리

#### ⭐ Request Enum 타입 정의 (중요!)

OpenAPI에서 Enum으로 정의된 파라미터는 **models.py에 Literal 타입으로 정의**하여 타입 안정성 확보:

```python
# models.py - Enum 타입 정의
OrderRequestType = Literal[
    "DEPOSIT_WAIT",
    "PAY_DONE",
    "PRODUCT_PREPARE",
    "DELIVERY_PREPARE",
    # ... 모든 값 나열
]
"""주문상태 타입"""

PayType = Literal[
    "CREDIT_CARD",
    "ACCOUNT",
    "NAVER_PAY",
    # ... 모든 값 나열
]
"""결제수단"""
```

```python
# client.py - Enum 타입 import 및 사용
from shopby_sdk.clients.order.models import OrderRequestType, PayType

async def get_orders(
    self,
    order_request_types: list[OrderRequestType] | None = None,
    pay_type: PayType | None = None,
) -> OrdersResponse:
    ...
```

**장점:**
- IDE 자동완성 지원
- 타입 검사로 오타 방지
- API 스펙 변경 시 한 곳만 수정

#### ⭐ Comma-Separated 파라미터 처리 (중요!)

OpenAPI에서 쉼표로 구분된 문자열을 받는 경우, **Python에서는 `list[]` 타입으로 받고 내부에서 join 처리**:

```python
# Bad - 사용하기 불편, 오타 가능
async def get_orders(self, order_request_types: str):  # "PAY_DONE,DELIVERY_ING"
    params = {"orderRequestTypes": order_request_types}

# Good - 타입 안정성 + 사용 편의성
async def get_orders(
    self,
    order_request_types: list[OrderRequestType] | None = None,  # ["PAY_DONE", "DELIVERY_ING"]
):
    if order_request_types is not None:
        params["orderRequestTypes"] = ",".join(order_request_types)
```

**숫자 리스트도 동일하게 처리:**
```python
async def method(self, product_nos: list[int] | None = None):  # [1, 2, 3]
    if product_nos is not None:
        params["productNos"] = ",".join(str(no) for no in product_nos)
```

#### Array 응답 처리

API가 배열을 직접 반환하는 경우:
```python
return [ItemModel.model_validate(item) for item in resp.json()]
```

## 참조

- **예제 코드**: `shopby_sdk/clients/examples/`
- **Base 클래스**: `shopby_sdk/clients/base.py`
- **BaseDto**: `shopby_sdk/base/dto.py`
- **KST 타입**: `shopby_sdk/base/kst.py`
- **API 스펙**:
  - product: `shopby-docs/product-server-public.yml`
  - display: `shopby-docs/display-server-public.yml`
  - order: `shopby-docs/order-server-public.yml`
  - member: `shopby-docs/member-server-public.yml`

## 완성된 구현 예제

| 도메인 | 클라이언트 경로 | 스크립트 예제 |
|--------|----------------|---------------|
| products | `shopby_sdk/clients/products/` | `scripts/get_product_detail_v1.py` |
| display | `shopby_sdk/clients/display/` | `scripts/get_event_detail.py` |
| order | `shopby_sdk/clients/order/` | `scripts/get_orders.py`, `scripts/get_order_detail.py` |
| member | `shopby_sdk/clients/member/` | `scripts/get_members.py`, `scripts/get_member_groups.py`, `scripts/get_profile_groups.py` |

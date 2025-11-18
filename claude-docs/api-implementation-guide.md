# Shopby Products API 구현 가이드

## 파일 구조

```
src/clients/{api_name}/
├── __init__.py      # exports 정의
├── client.py        # API 클라이언트 클래스
└── models.py        # Pydantic 모델 정의
```

## 구현 순서

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
from src.base.dto import BaseDto

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
- `resp.raise_for_status()` 호출
- `model_validate(resp.json())` 로 파싱

**예제:**
```python
import httpx
from src.clients.base import ShopbyServerApiClient
from src.clients.{api_name}.models import ResponseModel

class ShopbyServer{Name}ApiClient(ShopbyServerApiClient):
    async def method_name(self, param: int) -> ResponseModel:
        """
        API 설명

        Args:
            param: 파라미터 설명

        Returns:
            ResponseModel: 응답 모델
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "3.0"}  # 필요시 추가

            resp = await client.get(
                f"/path/{param}",
                headers=headers,
            )
            resp.raise_for_status()

            return ResponseModel.model_validate(resp.json())
```

### 4. __init__.py 작성
```python
from src.clients.{api_name}.client import ShopbyServer{Name}ApiClient
from src.clients.{api_name}.models import ResponseModel

__all__ = [
    "ShopbyServer{Name}ApiClient",
    "ResponseModel",
]
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

### 복잡한 스키마
- **원칙**: 모든 필드를 최대한 정확하게 구현
- 중첩 객체는 별도 클래스로 분리하여 타입 안정성 확보
- `dict[str, Any]` 임시처리는 **정말 불가피할 때만** 사용
  - 예: 스펙에 명확한 타입 정의가 없는 경우
  - 예: `oneOf`로 여러 타입이 혼재된 경우

### 파라미터 처리
- **쉼표 구분 리스트**: OpenAPI에서 쉼표로 구분된 문자열을 받는 경우
  - Python에서는 `list[int]` 또는 `list[str]`로 받기
  - 내부에서 `",".join()` 처리
  ```python
  # Bad
  async def method(self, product_nos: str):  # "1,2,3"
      params = {"productNos": product_nos}

  # Good
  async def method(self, product_nos: list[int]):  # [1, 2, 3]
      params = {"productNos": ",".join(str(no) for no in product_nos)}
  ```
- **Array 응답**: API가 배열을 직접 반환하는 경우
  - Response 타입을 `list[Model]`로 정의
  - 각 item을 `model_validate()`로 파싱
  ```python
  return [ItemModel.model_validate(item) for item in resp.json()]
  ```

## 참조

- **예제 코드**: `src/clients/examples/`
- **Base 클래스**: `src/clients/base.py`
- **BaseDto**: `src/base/dto.py`
- **API 스펙**: `shopby-docs/product-server-public.yml`

## 완성된 예제

**상품 상세 조회하기 (Version 3.0)**
- `src/clients/products/` 참조
- API endpoint: `GET /products/{mallProductNo}/`
- Version 3.0 헤더 사용

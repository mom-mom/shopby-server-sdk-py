"""
모든 판매중인 상품의 V1 상세 조회 유효성 검증

Usage:
    uv run --env-file .env.local python scripts/validate_all_products_v1.py
"""

import asyncio
import os
import sys
from dataclasses import dataclass

from shopby_sdk.clients.products import ShopbyServerProductsApiClient


@dataclass
class ValidationResult:
    product_no: int
    success: bool
    error: str | None = None


async def fetch_product_detail(
    client: ShopbyServerProductsApiClient,
    product_no: int,
    semaphore: asyncio.Semaphore,
) -> ValidationResult:
    """단일 상품 상세 조회 및 검증"""
    async with semaphore:
        try:
            await client.get_product_detail(product_no)
            return ValidationResult(product_no=product_no, success=True)
        except Exception as e:
            return ValidationResult(product_no=product_no, success=False, error=str(e))


async def main():
    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_SERVER_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SERVER_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServerProductsApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    # 1. 전시중이고 판매가능한 모든 상품 검색
    print("=== 상품 검색 시작 ===")
    all_product_nos: list[int] = []
    page = 1
    page_size = 100

    while True:
        result = await client.search_products_v2(
            front_display="Y",
            sale_setting_types="AVAILABLE_FOR_SALE",
            page_number=page,
            page_size=page_size,
        )

        product_nos = [item.product_no for item in result.items]
        all_product_nos.extend(product_nos)

        print(f"페이지 {page}: {len(product_nos)}개 상품 (누적: {len(all_product_nos)}/{result.total_count})")

        if len(all_product_nos) >= result.total_count or len(result.items) < page_size:
            break

        page += 1

    print(f"\n=== 총 {len(all_product_nos)}개 상품 검색 완료 ===\n")

    # 2. 동시성 제한으로 V1 상세 조회 수행
    concurrency = 20  # 동시 요청 수 제한
    semaphore = asyncio.Semaphore(concurrency)

    print(f"=== V1 상세 조회 시작 (동시성: {concurrency}) ===")

    tasks = [
        fetch_product_detail(client, product_no, semaphore)
        for product_no in all_product_nos
    ]

    results: list[ValidationResult] = []
    completed = 0
    total = len(tasks)

    # 진행 상황 출력을 위한 배치 처리
    batch_size = 100
    for i in range(0, total, batch_size):
        batch = tasks[i : i + batch_size]
        batch_results = await asyncio.gather(*batch)
        results.extend(batch_results)
        completed += len(batch_results)

        # 진행 상황
        success_count = sum(1 for r in results if r.success)
        fail_count = len(results) - success_count
        print(f"진행: {completed}/{total} (성공: {success_count}, 실패: {fail_count})")

    # 3. 결과 분석
    print("\n=== 검증 결과 ===")
    success_results = [r for r in results if r.success]
    fail_results = [r for r in results if not r.success]

    print(f"총 상품: {len(results)}개")
    print(f"성공: {len(success_results)}개")
    print(f"실패: {len(fail_results)}개")

    if fail_results:
        print("\n=== 실패 상품 목록 ===")
        # 에러 유형별 그룹화
        error_groups: dict[str, list[int]] = {}
        for r in fail_results:
            error_key = r.error[:100] if r.error else "Unknown"
            if error_key not in error_groups:
                error_groups[error_key] = []
            error_groups[error_key].append(r.product_no)

        for error, product_nos in error_groups.items():
            print(f"\n[{error}]")
            print(f"  상품 수: {len(product_nos)}개")
            print(f"  예시: {product_nos[:5]}")

        sys.exit(1)
    else:
        print("\n모든 상품 V1 상세 조회 검증 완료!")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())

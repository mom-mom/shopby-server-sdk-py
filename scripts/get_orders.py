"""
주문 조회하기 v1.1

Usage:
    uv run --env-file .env.local python scripts/get_orders.py [page_size]
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta

from shopby_sdk.clients.order import ShopbyServerOrderApiClient


async def main():
    page_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10

    # 환경변수에서 인증 정보 읽기
    access_token = os.environ["SHOPBY_SERVER_ACCESS_TOKEN"]
    system_key = os.environ["SHOPBY_SERVER_SYSTEM_KEY"]
    base_url = os.environ.get("SHOPBY_BASE_URL")

    client = ShopbyServerOrderApiClient(
        server_access_token=access_token,
        server_system_key=system_key,
        base_url=base_url,
    )

    # 최근 7일간 주문 조회
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    result = await client.get_orders(
        start_ymd=start_date,
        end_ymd=end_date,
        page_size=page_size,
    )

    print(f"총 주문 수: {result.total_count}")
    print(f"조회된 주문 수: {len(result.contents)}")
    print()

    for order in result.contents:
        print(f"=== 주문번호: {order.order_no} ===")
        print(f"  주문일시: {order.order_ymdt}")
        print(f"  주문자: {order.orderer_name}")
        print(f"  결제수단: {order.pay_type} ({order.pay_type_label})")
        print(f"  결제금액: {order.last_pay_amt}")

        for dg in order.delivery_groups:
            print(f"  [배송 {dg.delivery_no}] 수령자: {dg.receiver_name}, 송장: {dg.invoice_no}")
            for op in dg.order_products:
                print(f"    - {op.product_name}")
                for opt in op.order_product_options:
                    print(f"      옵션: {opt.option_name}={opt.option_value}, 수량: {opt.order_cnt}, 상태: {opt.order_status_type}")
        print()


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""주문 상세 조회 스크립트

Usage:
    uv run --env-file .env.local python scripts/get_order_detail.py <order_no>

Example:
    uv run --env-file .env.local python scripts/get_order_detail.py 202512102025457448
"""

import asyncio
import os
import sys

from shopby_sdk.clients.order import ShopbyServerOrderApiClient


async def main(order_no: str) -> None:
    client = ShopbyServerOrderApiClient(
        server_access_token=os.getenv("SHOPBY_SERVER_ACCESS_TOKEN"),
        server_system_key=os.getenv("SHOPBY_SERVER_SYSTEM_KEY"),
    )

    detail = await client.get_order_detail(order_no)

    print(f"주문번호: {detail.order_no}")
    print(f"등록일시: {detail.register_ymdt}")
    print(f"수정일시: {detail.update_ymdt}")
    print(f"PG사: {detail.pg_type}")
    print(f"결제수단: {detail.pay_type}")
    print(f"플랫폼: {detail.platform_type}")
    print(f"회원주문: {'예' if detail.is_member_order else '아니오'}")
    print(f"최종실결제금액: {detail.last_main_pay_amt}")
    print(f"통화: {detail.currency_code}")

    if detail.orderer:
        print()
        print("=== 주문자 정보 ===")
        print(f"  이름: {detail.orderer.name}")
        print(f"  연락처1: {detail.orderer.contact1}")
        print(f"  연락처2: {detail.orderer.contact2}")
        print(f"  이메일: {detail.orderer.email}")

    if detail.first_balance:
        print()
        print("=== 최초결제 금액 ===")
        print(f"  결제금액: {detail.first_balance.pay_amt}")
        print(f"  실결제금액: {detail.first_balance.main_pay_amt}")
        print(f"  정상금액: {detail.first_balance.standard_amt}")
        print(f"  배송비: {detail.first_balance.delivery_amt}")
        print(f"  즉시할인: {detail.first_balance.immediate_discount_amt}")
        print(f"  추가할인: {detail.first_balance.additional_discount_amt}")
        print(f"  상품쿠폰: {detail.first_balance.product_coupon_discount_amt}")
        print(f"  장바구니쿠폰: {detail.first_balance.cart_coupon_discount_amt}")
        print(f"  총 할인: {detail.first_balance.total_discount_amt}")

    if detail.last_balance:
        print()
        print("=== 최종결제 금액 ===")
        print(f"  결제금액: {detail.last_balance.pay_amt}")
        print(f"  실결제금액: {detail.last_balance.main_pay_amt}")
        print(f"  정상금액: {detail.last_balance.standard_amt}")
        print(f"  배송비: {detail.last_balance.delivery_amt}")
        print(f"  총 할인: {detail.last_balance.total_discount_amt}")

    print()
    print(f"=== 배송 정보 ({len(detail.shippings)}건) ===")
    for shipping in detail.shippings:
        print(f"  [배송 {shipping.shipping_no}]")
        print(f"    택배사: {shipping.delivery_company_type}")
        print(f"    송장번호: {shipping.invoice_no or '미등록'}")
        print(f"    배송타입: {shipping.delivery_type}")
        if shipping.receiver:
            print(f"    수령자: {shipping.receiver.name}")
            print(f"    연락처: {shipping.receiver.contact1}")
            print(f"    주소: {shipping.receiver.address} {shipping.receiver.detail_address}")

    print()
    print(f"=== 결제 정보 ({len(detail.payments)}건) ===")
    for payment in detail.payments:
        print(f"  [결제 {payment.no}]")
        if payment.balance:
            print(f"    결제금액: {payment.balance.pay_amt}")
            print(f"    실결제금액: {payment.balance.main_pay_amt}")
            print(f"    보조결제: {payment.balance.sub_pay_amt}")
        if payment.payment_info:
            print(f"    결제수단: {payment.payment_info.pay_type}")
            if payment.payment_info.card_info:
                print(f"    카드: {payment.payment_info.card_info.card_name}")
            if payment.payment_info.bank_info:
                print(f"    은행: {payment.payment_info.bank_info.bank_name}")

    if detail.claim_infos:
        print()
        print(f"=== 클레임 정보 ({len(detail.claim_infos)}건) ===")
        for claim in detail.claim_infos:
            print(f"  [클레임 {claim.claim_no}]")
            print(f"    타입: {claim.claim_type}")
            print(f"    상태: {claim.claim_status_type}")
            print(f"    일시: {claim.claim_ymdt}")
            print(f"    처리상태: {claim.treatment_status_type}")
            print(f"    완료일시: {claim.claim_complete_ymdt}")
            print(f"    클레임금액: {claim.claim_amt}")
            print(f"    클레임사유: {claim.claim_reason_type}")
            print(f"    사유상세: {claim.claim_reason_detail}")

    print()
    print(f"=== 주문 상품 ({len(detail.order_products)}건) ===")
    for product in detail.order_products:
        print(f"  - {product}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/get_order_detail.py <order_no>")
        sys.exit(1)

    asyncio.run(main(sys.argv[1]))

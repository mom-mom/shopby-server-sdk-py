"""Order API 클라이언트"""

from datetime import datetime, date

import httpx

from shopby_sdk.base.kst import to_kst_string
from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.order.models import (
    DeliveryCompanyType,
    OrderDetailResponse,
    OrderRequestType,
    OrdersResponse,
    PayType,
    SearchDateType,
    SearchType,
    ShippingAreaType,
)


class ShopbyServerOrderApiClient(ShopbyServerApiClient):
    """Shopby Order Server API 클라이언트"""

    async def get_orders(
        self,
        # 기간 필터 (date)
        start_ymd: date | None = None,
        end_ymd: date | None = None,
        # 기간 필터 (datetime) - ymd보다 우선순위 높음
        start_ymdt: datetime | None = None,
        end_ymdt: datetime | None = None,
        # 주문 필터
        order_option_nos: list[int] | None = None,
        order_request_types: list[OrderRequestType] | None = None,
        search_date_type: SearchDateType | None = None,
        member_no: int | None = None,
        # 검색
        search_type: SearchType | None = None,
        search_values: list[str] | None = None,
        # 배송/결제 필터
        delivery_company_type: DeliveryCompanyType | None = None,
        orderer_contact1: str | None = None,
        receiver_contact1: str | None = None,
        shipping_area_type: ShippingAreaType | None = None,
        pay_type: PayType | None = None,
        # 페이징
        page_number: int | None = None,
        page_size: int | None = None,
        # 정렬
        desc: bool | None = None,
        # 파트너
        partner_no: int | None = None,
    ) -> OrdersResponse:
        """
        주문 조회하기 v1.1

        주문 리스트 조회하는 API입니다.
        응답 데이터는 주문번호의 내림차순으로 정렬됩니다.

        Args:
            start_ymd: 시작일 (YYYY-MM-DD) [default: 3개월 전]
            end_ymd: 종료일 (YYYY-MM-DD) [default: 오늘]
            start_ymdt: 시작일시 (start_ymd보다 우선순위 높음)
            end_ymdt: 종료일시 (end_ymd보다 우선순위 높음)
            order_option_nos: 주문 옵션 번호 리스트
            order_request_types: 주문상태 타입 리스트
            search_date_type: 조회하려는 주문일시 유형 [default: ORDER_START]
            member_no: 회원번호
            search_type: 검색 유형 (ALL, ORDER_NO, MALL_PRODUCT_NO)
            search_values: 검색 값 리스트
            delivery_company_type: 택배사 타입
            orderer_contact1: 주문자 연락처
            receiver_contact1: 수령자 연락처
            shipping_area_type: 배송구분
            pay_type: 결제수단
            page_number: 페이지 번호 (1 이상) [default: 1]
            page_size: 페이지 크기 (최대 200) [default: 20]
            desc: 정렬 기준 (true: 내림차순, false: 오름차순)
            partner_no: 파트너 번호

        Returns:
            OrdersResponse: 주문 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 1.1 헤더 추가
            headers = {"version": "1.1"}

            # 쿼리 파라미터 구성
            params: dict[str, str | int | bool] = {}

            # 기간 필터 (date)
            if start_ymd is not None:
                params["startYmd"] = start_ymd.strftime("%Y-%m-%d")
            if end_ymd is not None:
                params["endYmd"] = end_ymd.strftime("%Y-%m-%d")

            # 기간 필터 (datetime)
            if start_ymdt is not None:
                params["startYmdt"] = to_kst_string(start_ymdt)
            if end_ymdt is not None:
                params["endYmdt"] = to_kst_string(end_ymdt)

            # 주문 필터
            if order_option_nos is not None:
                params["orderOptionNos"] = ",".join(str(no) for no in order_option_nos)
            if order_request_types is not None:
                params["orderRequestTypes"] = ",".join(order_request_types)
            if search_date_type is not None:
                params["searchDateType"] = search_date_type
            if member_no is not None:
                params["memberNo"] = member_no

            # 검색
            if search_type is not None:
                params["searchType"] = search_type
            if search_values is not None:
                params["searchValues"] = ",".join(search_values)

            # 배송/결제 필터
            if delivery_company_type is not None:
                params["deliveryCompanyType"] = delivery_company_type
            if orderer_contact1 is not None:
                params["ordererContact1"] = orderer_contact1
            if receiver_contact1 is not None:
                params["receiverContact1"] = receiver_contact1
            if shipping_area_type is not None:
                params["shippingAreaType"] = shipping_area_type
            if pay_type is not None:
                params["payType"] = pay_type

            # 페이징
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size

            # 정렬
            if desc is not None:
                params["desc"] = desc

            # 파트너
            if partner_no is not None:
                params["partnerNo"] = partner_no

            resp = await client.get(
                "/orders",
                headers=headers,
                params=params,
            )

            return self.handle_resp(resp, OrdersResponse)

    async def get_order_detail(self, order_no: str) -> OrderDetailResponse:
        """
        주문 상세 조회

        주문에 대한 상세를 조회하는 API입니다.

        Args:
            order_no: 주문 번호 (예: 202206151234567890)

        Returns:
            OrderDetailResponse: 주문 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            # Version 1.0 헤더 추가
            headers = {"version": "1.0"}

            resp = await client.get(
                f"/orders/{order_no}",
                headers=headers,
            )

            return self.handle_resp(resp, OrderDetailResponse)

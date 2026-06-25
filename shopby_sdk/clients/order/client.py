"""Order API 클라이언트"""

from datetime import datetime, date

import httpx

from shopby_sdk.base.kst import to_kst_string
from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.order.models import (
    AccountOrder,
    AccountOrderConfirmRequest,
    AccountOrderConfirmResult,
    AppCardPaymentKey,
    CartResponse,
    CartSearchDateType,
    CashReceiptIssuanceItem,
    ChangeStatusByShippingNoRequest,
    ChangeStatusByShippingNoResponse,
    CouponAvailableRequest,
    CouponAvailableResponse,
    CouponCalculateRequest,
    DeliveryCompanyType,
    DeliveryInvoiceItem,
    DeliverySearchType,
    HoldDeliveryRequest,
    OrderDeliveriesResponse,
    OrderDetailResponse,
    OrderExtraDataItem,
    OrderRequestType,
    OrdersResponse,
    PayType,
    PreviousOrderDeleteByOrderNosRequest,
    PreviousOrderDeleteResult,
    PreviousOrderRegisterItem,
    PreviousOrderRegisterResult,
    PreviousOrderSearchType,
    PreviousOrdersResponse,
    RecurringPaymentSearchType,
    RecurringPaymentsResponse,
    ReserveToNormalRequest,
    SearchDateType,
    SearchType,
    ShippingAddressesResponse,
    ShippingAddressType,
    ShippingAreaType,
    TaskMessageCreateRequest,
    TaskMessageCreateResult,
    TaskMessageDateType,
    TaskMessageDetailCreateRequest,
    TaskMessageDetailCreateResult,
    TaskMessageDetailUpdateRequest,
    TaskMessagesResponse,
    TaskMessageUpdateRequest,
    TaxInvoiceIssuanceItem,
    UpdateInvoiceItem,
    UpdateInvoiceResult,
    WishResponse,
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

    # ============================================================
    #  무통장 미입금 주문 (/accounts/orders)
    # ============================================================

    async def get_account_orders(self) -> list[AccountOrder]:
        """
        무통장 미입금 주문 리스트 조회

        PG연동을 하지 않고 쇼핑몰의 계좌로 입금을 받는 무통장입금 주문에 대한 주문 조회입니다.

        Returns:
            list[AccountOrder]: 무통장 미입금 주문 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/accounts/orders", headers=headers)
            return self.handle_resp(resp, list[AccountOrder])

    async def get_account_order(self, order_no: str) -> AccountOrder:
        """
        무통장 미입금 주문 조회

        Args:
            order_no: 주문번호 (예: 2020042100000001)

        Returns:
            AccountOrder: 무통장 미입금 주문 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/accounts/orders/{order_no}", headers=headers)
            return self.handle_resp(resp, AccountOrder)

    async def confirm_account_orders(
        self,
        requests: list[AccountOrderConfirmRequest],
    ) -> list[AccountOrderConfirmResult]:
        """
        무통장 입금 확인

        Args:
            requests: 입금 확인할 주문번호 목록

        Returns:
            list[AccountOrderConfirmResult]: 주문번호별 처리 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [r.model_dump(by_alias=True, exclude_none=True) for r in requests]
            resp = await client.put("/accounts/orders/confirmation", headers=headers, json=body)
            return self.handle_resp(resp, list[AccountOrderConfirmResult])

    # ============================================================
    #  앱카드 (/app-card)
    # ============================================================

    async def get_app_card_payment_key(self) -> AppCardPaymentKey:
        """
        앱카드 결제 키 조회

        쇼핑몰에 등록되어 있는 PG 결제키를 조회한다.

        Returns:
            AppCardPaymentKey: PG 결제 키 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/app-card/payment-key", headers=headers)
            return self.handle_resp(resp, AppCardPaymentKey)

    async def register_app_card_payment_key(self, request: dict) -> dict:
        """
        앱카드 결제 키 등록

        조회한 PG 결제키를 통해 앱카드 결제키를 등록한다.
        (요청/응답 스키마가 free-form object이므로 dict로 처리)

        Args:
            request: 앱카드 결제키 등록 정보 (예: {"pgType": "KCP", "storeId": "...", "available": true})

        Returns:
            dict: 등록 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.post("/app-card/payment-key", headers=headers, json=request)
            return self.handle_resp(resp, dict)

    async def update_app_card_available(self, request: dict) -> None:
        """
        앱카드 사용여부 수정

        Args:
            request: 사용여부 정보 (예: {"available": true})
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.patch("/app-card/available", headers=headers, json=request)
            self.raise_for_status(resp)
            return None

    # ============================================================
    #  장바구니 / 위시리스트
    # ============================================================

    async def get_carts(
        self,
        member_nos: list[int] | None = None,
        search_date_type: CartSearchDateType | None = None,
        start_ymdt: datetime | None = None,
        end_ymdt: datetime | None = None,
        group_id: str | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> CartResponse:
        """
        장바구니 가져오기

        장바구니를 조회하는 API 입니다. 조회기간은 최대 3개월까지 설정 가능합니다.

        Args:
            member_nos: 회원 번호 리스트
            search_date_type: 날짜 검색 조건 (REGISTER_YMDT, UPDATE_YMDT)
            start_ymdt: 조회 시작일시
            end_ymdt: 조회 종료일시
            group_id: 장바구니 그룹 아이디
            page: 페이지 번호
            size: 페이지당 노출 개수 (최대 200)

        Returns:
            CartResponse: 장바구니 조회 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if member_nos is not None:
                params["memberNos"] = ",".join(str(no) for no in member_nos)
            if search_date_type is not None:
                params["searchDateType"] = search_date_type
            if start_ymdt is not None:
                params["startYmdt"] = to_kst_string(start_ymdt)
            if end_ymdt is not None:
                params["endYmdt"] = to_kst_string(end_ymdt)
            if group_id is not None:
                params["groupId"] = group_id
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size

            resp = await client.get("/cart", headers=headers, params=params)
            return self.handle_resp(resp, CartResponse)

    async def get_wishes(
        self,
        start_ymdt: datetime | None = None,
        end_ymdt: datetime | None = None,
        page: int | None = None,
        size: int | None = None,
    ) -> WishResponse:
        """
        위시리스트 가져오기

        Args:
            start_ymdt: 조회 시작일시
            end_ymdt: 조회 종료일시
            page: 페이지 번호
            size: 페이지당 노출 개수

        Returns:
            WishResponse: 위시리스트 조회 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if start_ymdt is not None:
                params["startYmdt"] = to_kst_string(start_ymdt)
            if end_ymdt is not None:
                params["endYmdt"] = to_kst_string(end_ymdt)
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size

            resp = await client.get("/wish", headers=headers, params=params)
            return self.handle_resp(resp, WishResponse)

    # ============================================================
    #  배송번호 기준 주문 조회 (/orders/deliveries)
    # ============================================================

    async def get_orders_deliveries(
        self,
        start_ymd: date | None = None,
        end_ymd: date | None = None,
        start_ymdt: datetime | None = None,
        end_ymdt: datetime | None = None,
        order_request_types: list[OrderRequestType] | None = None,
        search_date_type: SearchDateType | None = None,
        member_no: int | None = None,
        search_type: DeliverySearchType | None = None,
        search_values: list[str] | None = None,
        exclude_option_nos: list[int] | None = None,
        exclude_delivery_nos: list[int] | None = None,
        delivery_company_type: DeliveryCompanyType | None = None,
        assigns_invoice: bool | None = None,
        include_none_delivery_company_type: bool | None = None,
        partner_no: int | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> OrderDeliveriesResponse:
        """
        주문 조회하기 (배송번호 기준)

        Args:
            start_ymd: 시작일 (YYYY-MM-DD)
            end_ymd: 종료일 (YYYY-MM-DD)
            start_ymdt: 시작일시 (start_ymd보다 우선순위 높음)
            end_ymdt: 종료일시 (end_ymd보다 우선순위 높음)
            order_request_types: 주문상태 타입 리스트
            search_date_type: 조회하려는 주문일시 유형
            member_no: 회원번호
            search_type: 검색 유형 (ALL, DELIVERY_NO, ORDER_NO, MALL_PRODUCT_NO)
            search_values: 검색 값 리스트
            exclude_option_nos: 검색 시 제외할 주문옵션번호
            exclude_delivery_nos: 검색 시 제외할 배송번호
            delivery_company_type: 택배사 타입
            assigns_invoice: 송장할당여부
            include_none_delivery_company_type: 택배사 미입력 주문 포함 여부
            partner_no: 파트너 번호
            page_number: 페이지 번호 (1 이상)
            page_size: 페이지 크기 (최대 200)

        Returns:
            OrderDeliveriesResponse: 배송번호 기준 주문 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if start_ymd is not None:
                params["startYmd"] = start_ymd.strftime("%Y-%m-%d")
            if end_ymd is not None:
                params["endYmd"] = end_ymd.strftime("%Y-%m-%d")
            if start_ymdt is not None:
                params["startYmdt"] = to_kst_string(start_ymdt)
            if end_ymdt is not None:
                params["endYmdt"] = to_kst_string(end_ymdt)
            if order_request_types is not None:
                params["orderRequestTypes"] = ",".join(order_request_types)
            if search_date_type is not None:
                params["searchDateType"] = search_date_type
            if member_no is not None:
                params["memberNo"] = member_no
            if search_type is not None:
                params["searchType"] = search_type
            if search_values is not None:
                params["searchValues"] = ",".join(search_values)
            if exclude_option_nos is not None:
                params["excludeOptionNos"] = ",".join(str(no) for no in exclude_option_nos)
            if exclude_delivery_nos is not None:
                params["excludeDeliveryNos"] = ",".join(str(no) for no in exclude_delivery_nos)
            if delivery_company_type is not None:
                params["deliveryCompanyType"] = delivery_company_type
            if assigns_invoice is not None:
                params["assignsInvoice"] = assigns_invoice
            if include_none_delivery_company_type is not None:
                params["includeNoneDeliveryCompanyType"] = include_none_delivery_company_type
            if partner_no is not None:
                params["partnerNo"] = partner_no
            if page_number is not None:
                params["pageNumber"] = page_number
            if page_size is not None:
                params["pageSize"] = page_size

            resp = await client.get("/orders/deliveries", headers=headers, params=params)
            return self.handle_resp(resp, OrderDeliveriesResponse)

    # ============================================================
    #  이전주문 (/previous-orders)
    # ============================================================

    async def get_previous_orders(
        self,
        page: int,
        size: int,
        search_type: PreviousOrderSearchType | None = None,
        keyword: str | None = None,
        start_ymd: date | None = None,
        end_ymd: date | None = None,
    ) -> PreviousOrdersResponse:
        """
        이전주문 검색

        Args:
            page: 페이지 번호 (필수)
            size: 페이지당 노출 개수 (필수)
            search_type: 검색 타입
            keyword: 검색어
            start_ymd: 조회시작일
            end_ymd: 조회종료일

        Returns:
            PreviousOrdersResponse: 이전주문 검색 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"page": page, "size": size}
            if search_type is not None:
                params["searchType"] = search_type
            if keyword is not None:
                params["keyword"] = keyword
            if start_ymd is not None:
                params["startYmd"] = start_ymd.strftime("%Y-%m-%d")
            if end_ymd is not None:
                params["endYmd"] = end_ymd.strftime("%Y-%m-%d")

            resp = await client.get("/previous-orders", headers=headers, params=params)
            return self.handle_resp(resp, PreviousOrdersResponse)

    async def register_previous_orders(
        self,
        items: list[PreviousOrderRegisterItem],
    ) -> PreviousOrderRegisterResult:
        """
        이전주문 등록

        Args:
            items: 등록할 이전주문 목록

        Returns:
            PreviousOrderRegisterResult: 등록 결과 (등록 개수)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True) for x in items]
            resp = await client.post("/previous-orders", headers=headers, json=body)
            return self.handle_resp(resp, PreviousOrderRegisterResult)

    async def delete_previous_orders(self, mall_name: str) -> PreviousOrderDeleteResult:
        """
        이전주문 전체 삭제

        Args:
            mall_name: 쇼핑몰 이름

        Returns:
            PreviousOrderDeleteResult: 삭제 결과 (삭제 개수)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"mallName": mall_name}
            resp = await client.post("/previous-orders/delete", headers=headers, params=params)
            return self.handle_resp(resp, PreviousOrderDeleteResult)

    async def delete_previous_orders_by_order_nos(
        self,
        mall_name: str,
        request: PreviousOrderDeleteByOrderNosRequest,
    ) -> PreviousOrderDeleteResult:
        """
        이전주문 삭제 (주문번호 리스트)

        Args:
            mall_name: 쇼핑몰 이름
            request: 삭제할 주문번호 리스트

        Returns:
            PreviousOrderDeleteResult: 삭제 결과 (삭제 개수)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"mallName": mall_name}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post(
                "/previous-orders/delete/by-order-nos",
                headers=headers,
                params=params,
                json=body,
            )
            return self.handle_resp(resp, PreviousOrderDeleteResult)

    # ============================================================
    #  정기결제(배송) (/recurring-payments)
    # ============================================================

    async def get_recurring_payments(
        self,
        page: int,
        size: int,
        member_nos: list[int] | None = None,
        search_type: RecurringPaymentSearchType | None = None,
        keywords: list[str] | None = None,
        status_types: list[str] | None = None,
    ) -> RecurringPaymentsResponse:
        """
        정기결제(배송) 조회

        Args:
            page: 페이지 번호 (필수)
            size: 사이즈 (필수)
            member_nos: 회원번호 리스트
            search_type: 검색 타입 (RECURRING_PAYMENT_NO)
            keywords: 검색어 리스트
            status_types: 상태 리스트

        Returns:
            RecurringPaymentsResponse: 정기결제(배송) 조회 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"page": page, "size": size}
            if member_nos is not None:
                params["memberNos"] = ",".join(str(no) for no in member_nos)
            if search_type is not None:
                params["searchType"] = search_type
            if keywords is not None:
                params["keywords"] = ",".join(keywords)
            if status_types is not None:
                params["statusTypes"] = ",".join(status_types)

            resp = await client.get("/recurring-payments", headers=headers, params=params)
            return self.handle_resp(resp, RecurringPaymentsResponse)

    # ============================================================
    #  배송지 (/shipping-addresses)
    # ============================================================

    async def get_shipping_addresses(
        self,
        member_nos: list[int],
        address_type: ShippingAddressType,
        page: int,
        size: int,
    ) -> ShippingAddressesResponse:
        """
        배송지 조회하기

        Args:
            member_nos: 회원 번호 리스트
            address_type: 배송지 타입 (BOOK, RECENT, RECURRING_PAYMENT, RECURRING_PAYMENT_PRESENT)
            page: 페이지 번호
            size: 페이지 크기

        Returns:
            ShippingAddressesResponse: 배송지 조회 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "memberNos": ",".join(str(no) for no in member_nos),
                "addressType": address_type,
                "page": page,
                "size": size,
            }
            resp = await client.get("/shipping-addresses", headers=headers, params=params)
            return self.handle_resp(resp, ShippingAddressesResponse)

    # ============================================================
    #  쿠폰 (/orders/coupons)
    # ============================================================

    async def get_available_coupons(
        self,
        request: CouponAvailableRequest,
    ) -> CouponAvailableResponse:
        """
        사용 가능 쿠폰 리스트 조회

        Args:
            request: 회원번호 및 상품 목록

        Returns:
            CouponAvailableResponse: 사용 가능 쿠폰 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post("/orders/coupons/available", headers=headers, json=body)
            return self.handle_resp(resp, CouponAvailableResponse)

    async def calculate_coupons(
        self,
        request: CouponCalculateRequest,
    ) -> CouponAvailableResponse:
        """
        쿠폰 적용 금액 계산

        Args:
            request: 쿠폰 적용 정보 (상품, 쿠폰 선택 등)

        Returns:
            CouponAvailableResponse: 쿠폰 적용 금액 계산 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post("/orders/coupons/calculate", headers=headers, json=body)
            return self.handle_resp(resp, CouponAvailableResponse)

    # ============================================================
    #  주문 상태 변경 (/orders/...)
    # ============================================================

    async def change_orders_status_by_shipping_no(
        self,
        request: ChangeStatusByShippingNoRequest,
    ) -> ChangeStatusByShippingNoResponse:
        """
        주문 상태 일괄 변경 요청하기 (배송번호 기준)

        Args:
            request: 변경할 주문상태 및 배송번호 목록

        Returns:
            ChangeStatusByShippingNoResponse: 처리 건수 및 실패 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put("/orders/change-status/by-shipping-no", headers=headers, json=body)
            return self.handle_resp(resp, ChangeStatusByShippingNoResponse)

    async def confirm_orders_purchase(self, request: dict) -> None:
        """
        구매확정 상태 변경 요청하기

        Args:
            request: 구매확정 처리 정보 (free-form object)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.put("/orders/confirm", headers=headers, json=request)
            self.raise_for_status(resp)
            return None

    async def deliver_orders(self, items: list[DeliveryInvoiceItem]) -> None:
        """
        상품준비중 상태 목록을 배송중 상태로 변경하기

        Args:
            items: 주문상품옵션번호 및 송장정보 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True) for x in items]
            resp = await client.put("/orders/delivery", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def deliver_ing_orders(self, items: list[DeliveryInvoiceItem]) -> None:
        """
        배송준비중 상태 목록을 배송중 상태로 변경하기

        Args:
            items: 주문상품옵션번호 및 송장정보 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True) for x in items]
            resp = await client.put("/orders/delivery-ing", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def update_orders_extra_data(self, items: list[OrderExtraDataItem]) -> None:
        """
        주문의 추가 정보 입력

        Args:
            items: 주문번호별 key/value 추가정보 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True) for x in items]
            resp = await client.put("/orders/extra-data", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def hold_orders_delivery(self, request: HoldDeliveryRequest) -> None:
        """
        배송보류 처리하기

        Args:
            request: 배송보류 처리 정보 (주문옵션번호, 사유 등)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put("/orders/hold-delivery", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def prepare_orders_delivery(self, request: dict) -> None:
        """
        배송준비중 상태 변경 요청하기

        Args:
            request: 배송준비중 처리 정보 (free-form object)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.put("/orders/prepare-delivery", headers=headers, json=request)
            self.raise_for_status(resp)
            return None

    async def prepare_orders_product(self, request: dict) -> None:
        """
        상품준비중 상태 변경 요청하기

        Args:
            request: 상품준비중 처리 정보 (free-form object)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.put("/orders/prepare-product", headers=headers, json=request)
            self.raise_for_status(resp)
            return None

    async def receive_orders(self, request: dict) -> None:
        """
        주문상품 수취확인처리 요청하기

        Args:
            request: 수취확인 처리 정보 (free-form object)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.put("/orders/receive", headers=headers, json=request)
            self.raise_for_status(resp)
            return None

    async def reserve_orders_to_normal(self, request: ReserveToNormalRequest) -> None:
        """
        예약 주문 일반주문으로 변경 요청하기

        Args:
            request: 예약 주문의 주문옵션번호 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put("/orders/reserve-to-normal", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def update_cash_receipt_issuance_result(
        self,
        items: list[CashReceiptIssuanceItem],
    ) -> None:
        """
        현금영수증 발행결과 업데이트

        Args:
            items: 주문번호별 현금영수증 발행결과 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True) for x in items]
            resp = await client.put("/orders/cash-receipt", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def update_tax_invoice_issuance_result(
        self,
        items: list[TaxInvoiceIssuanceItem],
    ) -> None:
        """
        세금계산서 발행결과 업데이트

        Args:
            items: 주문번호별 세금계산서 발행결과 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True) for x in items]
            resp = await client.put("/orders/tax-invoice", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def update_orders_invoices(
        self,
        items: list[UpdateInvoiceItem],
    ) -> list[UpdateInvoiceResult]:
        """
        송장번호 변경

        Args:
            items: 배송번호별 택배사/송장번호 목록

        Returns:
            list[UpdateInvoiceResult]: 배송번호별 변경 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = [x.model_dump(by_alias=True, exclude_none=True) for x in items]
            resp = await client.put("/orders/update-invoices", headers=headers, json=body)
            return self.handle_resp(resp, list[UpdateInvoiceResult])

    # ============================================================
    #  업무 메시지 (/task-messages)
    # ============================================================

    async def get_task_messages(
        self,
        date_type: TaskMessageDateType,
        start_date_time: datetime,
        end_date_time: datetime,
        page: int | None = None,
        size: int | None = None,
    ) -> TaskMessagesResponse:
        """
        업무 메시지 조회하기

        Args:
            date_type: 기간 검색 타입 (REGISTER, UPDATE, COMPLETE)
            start_date_time: 조회 시작 일시
            end_date_time: 조회 종료 일시
            page: 페이지 번호 (1 이상)
            size: 페이지당 노출 개수

        Returns:
            TaskMessagesResponse: 업무 메시지 조회 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "dateType": date_type,
                "startDateTime": to_kst_string(start_date_time),
                "endDateTime": to_kst_string(end_date_time),
            }
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size

            resp = await client.get("/task-messages", headers=headers, params=params)
            return self.handle_resp(resp, TaskMessagesResponse)

    async def create_task_message(
        self,
        request: TaskMessageCreateRequest,
    ) -> TaskMessageCreateResult:
        """
        업무 메시지 등록

        Args:
            request: 업무 메시지 등록 정보

        Returns:
            TaskMessageCreateResult: 등록된 업무메시지 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post("/task-messages", headers=headers, json=body)
            return self.handle_resp(resp, TaskMessageCreateResult)

    async def update_task_message(
        self,
        task_message_no: int,
        request: TaskMessageUpdateRequest,
    ) -> None:
        """
        업무 메시지 수정

        Args:
            task_message_no: 업무 메시지 번호
            request: 수정할 업무 메시지 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put(f"/task-messages/{task_message_no}", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def create_task_message_detail(
        self,
        task_message_no: int,
        request: TaskMessageDetailCreateRequest,
    ) -> TaskMessageDetailCreateResult:
        """
        상세 업무 메시지 등록

        Args:
            task_message_no: 업무 메시지 번호
            request: 상세 업무 메시지 등록 정보

        Returns:
            TaskMessageDetailCreateResult: 등록된 상세 업무메시지 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post(f"/task-messages/{task_message_no}/details", headers=headers, json=body)
            return self.handle_resp(resp, TaskMessageDetailCreateResult)

    async def update_task_message_detail(
        self,
        task_message_no: int,
        task_message_detail_no: int,
        request: TaskMessageDetailUpdateRequest,
    ) -> None:
        """
        상세 업무 메시지 수정

        Args:
            task_message_no: 업무 메시지 번호
            task_message_detail_no: 상세 메시지 번호
            request: 수정할 상세 업무 메시지 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put(
                f"/task-messages/{task_message_no}/details/{task_message_detail_no}",
                headers=headers,
                json=body,
            )
            self.raise_for_status(resp)
            return None

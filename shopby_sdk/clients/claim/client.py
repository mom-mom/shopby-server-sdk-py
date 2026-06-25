"""Claim API 클라이언트

OpenAPI: claim-server (docs/api/claim-server-public.yml)
"""

from datetime import date

import httpx

from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.claim.models import (
    AlreadyDeliveryRequest,
    AssignReturnInvoiceRequest,
    AvailableComplexRefundAmtRequest,
    AvailableComplexRefundAmtResponse,
    CancelExchangeRequest,
    ClaimListResponse,
    ClaimResult,
    ClaimSearchDateType,
    ClaimSearchType,
    ClaimStatusType,
    ConfirmDepositRequest,
    ExchangeInfo,
    OptionCancelRequest,
    OrderCancelRequest,
    ReturnCollectRequest,
    ReturnExchangeCollectRequest,
    ReturnExchangeRequest,
    ReturnRequest,
    SoldOutCancelRequest,
    SoldOutSetOptionRequest,
    TreatmentStatusType,
)


class ShopbyServerClaimApiClient(ShopbyServerApiClient):
    """Shopby Claim Server API 클라이언트"""

    # ------------------------------------------------------------------
    # Claim
    # ------------------------------------------------------------------
    async def get_claims(
        self,
        start_ymd: date,
        end_ymd: date,
        search_date_type: ClaimSearchDateType,
        search_type: ClaimSearchType,
        page: int,
        size: int,
        claim_status_types: list[ClaimStatusType] | None = None,
        treatment_status_types: list[TreatmentStatusType] | None = None,
        search_values: list[str] | None = None,
    ) -> ClaimListResponse:
        """클레임 목록 조회하기

        다수의 클레임 정보를 조회합니다.

        Args:
            start_ymd: 조회시작일
            end_ymd: 조회종료일
            search_date_type: 검색일자타입 (APPLY_YMDT, COMPLETE_YMDT)
            search_type: 클레임 검색 타입 (ALL, CLAIM_NO, ORDER_NO, MEMBER_NO)
            page: 페이지 번호 (1 이상)
            size: 페이지 사이즈
            claim_status_types: 클레임 상태 리스트
            treatment_status_types: 클레임 처리 상태 리스트
            search_values: 클레임 검색 값

        Returns:
            ClaimListResponse: 클레임 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            params: dict[str, str | int | bool] = {
                "startYmd": start_ymd.strftime("%Y-%m-%d"),
                "endYmd": end_ymd.strftime("%Y-%m-%d"),
                "searchDateType": search_date_type,
                "searchType": search_type,
                "page": page,
                "size": size,
            }
            if claim_status_types is not None:
                params["claimStatusTypes"] = ",".join(claim_status_types)
            if treatment_status_types is not None:
                params["treatmentStatusTypes"] = ",".join(treatment_status_types)
            if search_values is not None:
                params["searchValues"] = ",".join(search_values)

            resp = await client.get("/claims", headers=headers, params=params)
            return self.handle_resp(resp, ClaimListResponse)

    async def get_available_complex_refund_amt(
        self, request: AvailableComplexRefundAmtRequest
    ) -> AvailableComplexRefundAmtResponse:
        """관리자 지정 환불 - 환불 가능 금액 조회하기 (개발중)

        관리자 지정 환불 클레임 신청시, 각 환불수단 별 최대로 입력 가능한 환불금액을 반환합니다.

        Args:
            request: 환불 가능 금액 조회 요청

        Returns:
            AvailableComplexRefundAmtResponse: 환불수단 별 환불 가능 금액
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post(
                "/claims/available-complex-refund-amt", headers=headers, json=body
            )
            return self.handle_resp(resp, AvailableComplexRefundAmtResponse)

    async def already_delivery(
        self, claim_no: int, request: AlreadyDeliveryRequest
    ) -> None:
        """이미출고

        옵션취소, 취소교환 신청된 클레임의 배송이 이미 출고된 경우 호출합니다.
        신청된 클레임을 철회하고, 배송정보를 저장하여 배송중 상태로 변경합니다.

        Args:
            claim_no: 클레임 번호
            request: 이미출고 요청 (출고일시, 송장번호, 택배사)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put(
                f"/claims/{claim_no}/already-delivery", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    async def approve_claim(self, claim_no: str) -> None:
        """클레임 승인

        클레임 신청을 승인하는 API 입니다.
        클레임 종류별로 이후 진행 단계가 상이하니 유의하세요.

        Args:
            claim_no: 클레임 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.put(f"/claims/{claim_no}/approve", headers=headers)
            self.raise_for_status(resp)
            return None

    async def assign_return_invoice(
        self, claim_no: int, request: AssignReturnInvoiceRequest
    ) -> None:
        """반품 송장번호 할당

        반품 송장번호를 할당하는 API 입니다.
        클레임이 반품, 반품교환인 경우만 사용 가능합니다.

        Args:
            claim_no: 클레임 번호
            request: 반품 송장번호 할당 요청 (택배사, 반품 송장번호)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put(
                f"/claims/{claim_no}/assign-return-invoice", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    async def withdraw_claim(self, claim_no: str) -> None:
        """클레임 철회

        클레임을 철회하는 API 입니다.

        Args:
            claim_no: 클레임 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.put(f"/claims/{claim_no}/withdraw", headers=headers)
            self.raise_for_status(resp)
            return None

    async def get_exchange_infos(self, order_no: str) -> list[ExchangeInfo]:
        """교환 전/후 정보 조회

        교환 완료된 클레임의 전/후 옵션 정보를 반환합니다.
        철회된 클레임은 조회되지 않습니다.

        Args:
            order_no: 주문번호

        Returns:
            list[ExchangeInfo]: 교환 전/후 옵션 정보 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/claims/{order_no}/exchange-infos", headers=headers)
            return self.handle_resp(resp, list[ExchangeInfo])

    # ------------------------------------------------------------------
    # OptionCancel
    # ------------------------------------------------------------------
    async def create_option_cancel(self, request: OptionCancelRequest) -> None:
        """옵션 취소 신청하기

        옵션 취소 신청 API입니다.

        Args:
            request: 옵션 취소 신청 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post("/option-cancels", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def create_sold_out_cancel(self, request: SoldOutCancelRequest) -> None:
        """품절 취소처리하기

        선택한 주문옵션을 품절 취소하고 금액을 환불하는 API입니다.
        이벤트 처리 방식이라 실제 취소까지 일정 시간이 소요될 수 있습니다.

        Args:
            request: 품절 취소처리 요청 (품절 주문 옵션번호 리스트)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post("/option-cancels/sold-out", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def create_sold_out_set_option_cancel(
        self, request: SoldOutSetOptionRequest
    ) -> None:
        """세트옵션 품절취소처리하기

        선택한 주문옵션의 세트구성옵션을 품절 취소하고 금액을 환불하는 API입니다.

        Args:
            request: 세트옵션 품절 취소처리 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post(
                "/option-cancels/sold-out/set-option", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    # ------------------------------------------------------------------
    # OrderCancel
    # ------------------------------------------------------------------
    async def create_order_cancel(self, request: OrderCancelRequest) -> None:
        """주문 취소하기

        주문 취소 신청 API입니다.
        주문 취소 신청은 입금대기, 결제완료 상태에서 가능합니다.

        Args:
            request: 주문 취소 신청 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post("/order-cancels", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    # ------------------------------------------------------------------
    # CancelExchange
    # ------------------------------------------------------------------
    async def create_cancel_exchange(self, request: CancelExchangeRequest) -> None:
        """취소교환 신청

        옵션 취소 교환을 신청하는 API입니다.

        Args:
            request: 취소교환 신청 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post("/cancel-exchanges", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def confirm_cancel_exchange_deposit(
        self, no: str, request: ConfirmDepositRequest
    ) -> None:
        """취소교환 추가결제 입금확인

        추가 결제 내역을 입금 확인처리 합니다.

        Args:
            no: 클레임 번호
            request: 추가결제 입금확인 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put(
                f"/cancel-exchanges/{no}/confirm-deposit", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    # ------------------------------------------------------------------
    # ReturnExchange
    # ------------------------------------------------------------------
    async def create_return_exchange(
        self, request: ReturnExchangeRequest
    ) -> ClaimResult | None:
        """반품교환 신청 (V1.1)

        반품 교환을 신청하는 API입니다. 배송안함 상품에는 사용할 수 없습니다.
        V1.1: 판매자 귀책에서도 반품/교환배송비 조정이 가능하며,
        입력하지 않으면 전액 고객에게 부과됩니다.

        Args:
            request: 반품교환 신청 요청

        Returns:
            ClaimResult | None: 클레임 번호 및 클레임된 옵션 (본문 없을 경우 None)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.1"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post("/return-exchanges", headers=headers, json=body)
            self.raise_for_status(resp)
            if not resp.content:
                return None
            return ClaimResult.model_validate(resp.json())

    async def collect_return_exchange(
        self, no: str, request: ReturnExchangeCollectRequest
    ) -> None:
        """반품교환 수거완료

        반품교환에서 클레임된 상품의 수거를 완료처리하는 API입니다.

        Args:
            no: 클레임 번호
            request: 반품교환 수거완료 요청 (재고복원여부)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put(
                f"/return-exchanges/{no}/collect", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    async def confirm_return_exchange_deposit(
        self, no: str, request: ConfirmDepositRequest
    ) -> None:
        """반품교환 추가결제 입금확인

        추가 결제 내역을 입금 확인처리 합니다.

        Args:
            no: 클레임 번호
            request: 추가결제 입금확인 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put(
                f"/return-exchanges/{no}/confirm-deposit", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    # ------------------------------------------------------------------
    # Return
    # ------------------------------------------------------------------
    async def create_return(self, request: ReturnRequest) -> ClaimResult | None:
        """반품신청하기 (V1.1)

        반품 신청 API입니다.
        V1.1: 판매자 귀책에서도 반품/교환배송비 조정이 가능하며,
        입력하지 않으면 전액 고객에게 부과됩니다.

        Args:
            request: 반품 신청 요청

        Returns:
            ClaimResult | None: 클레임 번호 및 클레임된 옵션 (본문 없을 경우 None)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.1"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.post("/returns", headers=headers, json=body)
            self.raise_for_status(resp)
            if not resp.content:
                return None
            return ClaimResult.model_validate(resp.json())

    async def collect_return(self, no: int, request: ReturnCollectRequest) -> None:
        """반품수거 완료하기

        반품 수거 완료처리를 위한 API입니다.

        Args:
            no: 클레임 번호
            request: 반품 수거완료 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)
            resp = await client.put(f"/returns/{no}/collect", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

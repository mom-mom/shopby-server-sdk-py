"""Admin API 클라이언트"""

import httpx

from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.admin.models import (
    AdminAuthorityResponse,
    AdminDetailResponse,
    ContractCreateRequest,
    ContractDetailResponse,
    ContractListResponse,
    ContractStatusUpdateRequest,
    ContractUpdateRequest,
    ContractedPartner,
    Currency,
    CurrencyUpdateRequest,
    ExistResultResponse,
    MallDetailResponse,
    MallDomain,
    MerchandiserAdmin,
    OperationGroupListResponse,
    PartnerCreateRequest,
    PartnerCreateResponse,
    PartnerDetailResponse,
    PartnerUpdateRequest,
    ServiceDetailResponse,
    ShopbyPartnerResponse,
    TempPartnerCreateRequest,
)


class ShopbyServerAdminApiClient(ShopbyServerApiClient):
    """Shopby Admin Server API 클라이언트"""

    # ------------------------------------
    #  Admin
    # ------------------------------------
    async def get_admins_authority(self) -> AdminAuthorityResponse:
        """
        샵바이 어드민 권한 조회

        샵바이에 등록된 어드민의 권한 정보를 조회합니다.
        MASTER 어드민일 경우 권한이 존재하지 않습니다.

        Returns:
            AdminAuthorityResponse: 어드민 권한 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/admins", headers=headers)
            return self.handle_resp(resp, AdminAuthorityResponse)

    async def get_md_admins(self) -> list[MerchandiserAdmin]:
        """
        쇼핑몰 상품담당 MD 운영자 조회

        특정 쇼핑몰의 상품담당 MD 운영자를 조회합니다.

        Returns:
            list[MerchandiserAdmin]: 상품담당 MD 운영자 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/admins/merchandisers", headers=headers)
            return self.handle_resp(resp, list[MerchandiserAdmin])

    async def get_admin(self, admin_no: int) -> AdminDetailResponse:
        """
        샵바이 어드민 조회

        샵바이에 등록된 어드민 정보를 조회합니다.

        Args:
            admin_no: 어드민 번호

        Returns:
            AdminDetailResponse: 어드민 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/admins/{admin_no}", headers=headers)
            return self.handle_resp(resp, AdminDetailResponse)

    # ------------------------------------
    #  Mall-Domain
    # ------------------------------------
    async def get_mall_domains(
        self, device_type: str | None = None
    ) -> list[MallDomain]:
        """
        몰 도메인 조회

        몰 도메인 정보를 조회합니다.

        Args:
            device_type: 디바이스 타입. 없으면 전체검색 (PC / MOBILE)

        Returns:
            list[MallDomain]: 몰 도메인 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if device_type is not None:
                params["deviceType"] = device_type
            resp = await client.get(
                "/configurations/admin/domains", headers=headers, params=params
            )
            return self.handle_resp(resp, list[MallDomain])

    # ------------------------------------
    #  Contract
    # ------------------------------------
    async def get_contracts(
        self,
        page: int | None = None,
        page_size: int | None = None,
        partner_nos: list[int] | None = None,
    ) -> ContractListResponse:
        """
        계약서 조회하기

        계약서를 조회합니다.

        Args:
            page: 페이지 번호
            page_size: 페이지 사이즈
            partner_nos: 파트너 번호들 (미입력 시, 전체 조회)

        Returns:
            ContractListResponse: 계약서 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if partner_nos is not None:
                params["partnerNos"] = ",".join(str(no) for no in partner_nos)
            resp = await client.get("/contracts", headers=headers, params=params)
            return self.handle_resp(resp, ContractListResponse)

    async def update_contract_status(
        self, request: ContractStatusUpdateRequest
    ) -> None:
        """
        계약서 상태 수정하기

        몰과 파트너간의 계약 상태를 수정합니다.

        Args:
            request: 계약서 상태 수정 요청 (status, contractNos)

        Returns:
            None
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put("/contracts", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def create_contract(self, request: ContractCreateRequest) -> None:
        """
        신규 계약 등록하기

        등록되어있는 파트너와 신규 계약을 등록합니다.
        이미 쇼핑몰 - 파트너간 계약관계가 존재한다면 새로 등록할 수 없습니다.

        Args:
            request: 신규 계약 등록 요청

        Returns:
            None
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/contracts", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def get_contract_detail(self, partner_no: int) -> ContractDetailResponse:
        """
        계약서 상세 조회하기

        쇼핑몰 - 파트너간의 계약정보 상세를 조회합니다.

        Args:
            partner_no: 파트너 번호

        Returns:
            ContractDetailResponse: 계약서 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/contracts/{partner_no}", headers=headers)
            return self.handle_resp(resp, ContractDetailResponse)

    async def update_contract(
        self, partner_no: int, request: ContractUpdateRequest
    ) -> None:
        """
        계약서 수정하기

        계약서를 수정합니다.

        Args:
            partner_no: 파트너 번호
            request: 계약서 수정 요청

        Returns:
            None
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(
                f"/contracts/{partner_no}", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  Currency
    # ------------------------------------
    async def get_currencies(self) -> list[Currency]:
        """
        몰 환율 설정 조회

        몰의 환율 설정을 조회합니다.

        Returns:
            list[Currency]: 환율 설정 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/currencies", headers=headers)
            return self.handle_resp(resp, list[Currency])

    async def update_currency(
        self, currency_code: str, request: CurrencyUpdateRequest
    ) -> None:
        """
        몰 환율 설정 수정

        몰의 환율 설정을 수정합니다.

        Args:
            currency_code: 통화 (CNY, USD, JPY, KRW)
            request: 환율 설정 수정 요청 (exchangeRate)

        Returns:
            None
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(
                f"/currencies/{currency_code}", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  Mall
    # ------------------------------------
    async def get_mall_detail(self) -> MallDetailResponse:
        """
        쇼핑몰 상세 조회

        Mall 정보를 조회합니다.

        Returns:
            MallDetailResponse: 쇼핑몰 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/malls", headers=headers)
            return self.handle_resp(resp, MallDetailResponse)

    async def get_shopby_partner(self) -> ShopbyPartnerResponse:
        """
        쇼핑몰 자체 파트너 조회

        몰의 쇼핑몰 자체 파트너를 조회합니다.

        Returns:
            ShopbyPartnerResponse: 쇼핑몰 자체 파트너 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/malls/shopby-partner", headers=headers)
            return self.handle_resp(resp, ShopbyPartnerResponse)

    async def get_contracted_partners(
        self,
        partner_nos: list[int] | None = None,
        partner_mapping_keys: list[str] | None = None,
    ) -> list[ContractedPartner]:
        """
        계약된 파트너 정보 조회하기

        mallKey를 기준으로 계약된 파트너 정보를 조회합니다.
        파트너 번호가 없는 경우 모든 파트너에 대해 조회합니다.

        Args:
            partner_nos: 파트너 번호 목록
            partner_mapping_keys: 파트너 매핑키 목록

        Returns:
            list[ContractedPartner]: 계약된 파트너 정보 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if partner_nos is not None:
                params["partnerNos"] = ",".join(str(no) for no in partner_nos)
            if partner_mapping_keys is not None:
                params["partnerMappingKeys"] = ",".join(partner_mapping_keys)
            resp = await client.get(
                "/malls/contracts/partners", headers=headers, params=params
            )
            return self.handle_resp(resp, list[ContractedPartner])

    # ------------------------------------
    #  Operation
    # ------------------------------------
    async def search_operation_groups(
        self,
        page: int | None = None,
        page_size: int | None = None,
        name: str | None = None,
        audit_step: str | None = None,
    ) -> OperationGroupListResponse:
        """
        운영그룹 목록 조회

        운영그룹을 검색합니다.

        Args:
            page: 페이지 번호
            page_size: 페이지 사이즈
            name: 운영그룹 명
            audit_step: 심사 절차 (ALWAYS, REGISTRATION_ONLY, NONE)

        Returns:
            OperationGroupListResponse: 운영그룹 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if name is not None:
                params["name"] = name
            if audit_step is not None:
                params["auditStep"] = audit_step
            resp = await client.get(
                "/operation/groups", headers=headers, params=params
            )
            return self.handle_resp(resp, OperationGroupListResponse)

    # ------------------------------------
    #  Partner
    # ------------------------------------
    async def create_partner(
        self, request: PartnerCreateRequest
    ) -> PartnerCreateResponse:
        """
        파트너 등록하기

        쇼핑몰에 파트너를 등록합니다.
        국내 파트너사에 경우에만 API로 파트너 등록 가능합니다.

        Args:
            request: 파트너 등록 요청

        Returns:
            PartnerCreateResponse: 생성된 파트너 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/partners", headers=headers, json=body)
            return self.handle_resp(resp, PartnerCreateResponse)

    async def create_temp_partner(
        self, request: TempPartnerCreateRequest
    ) -> PartnerCreateResponse:
        """
        임시 파트너 등록하기

        쇼핑몰에 임시 파트너를 등록합니다.

        Args:
            request: 임시 파트너 등록 요청

        Returns:
            PartnerCreateResponse: 생성된 파트너 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.post("/partners/temp", headers=headers, json=body)
            return self.handle_resp(resp, PartnerCreateResponse)

    async def get_partner(self, partner_no: int) -> PartnerDetailResponse:
        """
        몰과 계약된 파트너 조회

        쇼핑몰과 계약된 파트너를 조회합니다.

        Args:
            partner_no: 파트너 번호

        Returns:
            PartnerDetailResponse: 파트너 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get(f"/partners/{partner_no}", headers=headers)
            return self.handle_resp(resp, PartnerDetailResponse)

    async def update_partner(
        self, partner_no: int, request: PartnerUpdateRequest
    ) -> None:
        """
        파트너 수정하기

        쇼핑몰에 파트너를 수정합니다.

        Args:
            partner_no: 파트너 번호
            request: 파트너 수정 요청

        Returns:
            None
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            resp = await client.put(
                f"/partners/{partner_no}", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    async def exist_admin_id(self, admin_id: str) -> ExistResultResponse:
        """
        어드민아이디 중복 체크하기

        어드민아이디 중복 여부를 체크합니다.

        Args:
            admin_id: 어드민아이디

        Returns:
            ExistResultResponse: 중복 확인 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"adminId": admin_id}
            resp = await client.get(
                "/partners/exist/admin-id", headers=headers, params=params
            )
            return self.handle_resp(resp, ExistResultResponse)

    async def exist_partner_name(self, partner_name: str) -> ExistResultResponse:
        """
        파트너명 중복 체크하기

        파트너명 중복 여부를 체크합니다.

        Args:
            partner_name: 파트너명

        Returns:
            ExistResultResponse: 중복 확인 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"partnerName": partner_name}
            resp = await client.get(
                "/partners/exist/partner-name", headers=headers, params=params
            )
            return self.handle_resp(resp, ExistResultResponse)

    # ------------------------------------
    #  Service
    # ------------------------------------
    async def get_service_detail(self) -> ServiceDetailResponse:
        """
        서비스 상세 조회

        서비스 상세 정보를 조회합니다.

        Returns:
            ServiceDetailResponse: 서비스 상세 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            resp = await client.get("/services", headers=headers)
            return self.handle_resp(resp, ServiceDetailResponse)

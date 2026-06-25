"""Delivery API 클라이언트"""

import httpx

from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.delivery.models import (
    AreaFee,
    AreaFeeRequest,
    AreaFeesResponse,
    Area,
    DeliveryTemplate,
    ShippingAreaType,
    TemplateDetail,
    TemplateGroup,
    TemplateGroupCreateRequest,
    TemplateGroupUpdateRequest,
    Warehouse,
    WarehouseRequest,
    WarehousesResponse,
)


class ShopbyServerDeliveryApiClient(ShopbyServerApiClient):
    """Shopby Delivery Server API 클라이언트"""

    # ------------------------------------
    #  AreaFee (지역별 추가배송비)
    # ------------------------------------
    async def get_area_fees(self, page: int, size: int) -> AreaFeesResponse:
        """
        지역별 추가배송비 설정 내역 조회하기

        파트너의 지역별 추가배송비 설정 내역을 조회합니다.

        Args:
            page: 시작 번호[페이징 처리] (1 이상)
            size: 종료 번호[페이징 처리]

        Returns:
            AreaFeesResponse: 지역별 추가배송비 설정 내역 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"page": page, "size": size}

            resp = await client.get("/areafees", headers=headers, params=params)
            return self.handle_resp(resp, AreaFeesResponse)

    async def create_area_fee(self, request: AreaFeeRequest) -> AreaFee:
        """
        지역별 추가배송비 설정 생성하기

        파트너의 지역별 추가배송비 설정을 생성합니다.

        Args:
            request: 지역별 추가배송비 설정 생성 요청

        Returns:
            AreaFee: 생성된 지역별 추가배송비 설정
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.post("/areafees", headers=headers, json=body)
            return self.handle_resp(resp, AreaFee)

    async def get_area_fee(self, area_fee_no: int) -> AreaFee:
        """
        지역별 추가배송비 설정 조회하기

        파트너의 지역별 추가배송비 설정을 조회합니다.

        Args:
            area_fee_no: 지역별 추가배송비 번호

        Returns:
            AreaFee: 지역별 추가배송비 설정
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get(f"/areafees/{area_fee_no}", headers=headers)
            return self.handle_resp(resp, AreaFee)

    async def update_area_fee(self, area_fee_no: int, request: AreaFeeRequest) -> None:
        """
        지역별 추가배송비 설정 수정하기

        파트너의 지역별 추가배송비 설정을 수정합니다.

        Args:
            area_fee_no: 지역별 추가배송비 번호
            request: 지역별 추가배송비 설정 수정 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.put(f"/areafees/{area_fee_no}", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def get_areas(self, country_cd: str) -> list[Area]:
        """
        배송비 설정을 위한 지역 조회

        배송비 설정을 위한 지역을 조회합니다.

        Args:
            country_cd: 국가 코드 (예: KR)

        Returns:
            list[Area]: 지역 리스트
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"countryCd": country_cd}

            resp = await client.get("/areas", headers=headers, params=params)
            return self.handle_resp(resp, list[Area])

    # ------------------------------------
    #  Delivery (배송비 템플릿)
    # ------------------------------------
    async def get_deliveries(
        self, shipping_area_type: ShippingAreaType | None = None
    ) -> list[DeliveryTemplate]:
        """
        배송비 템플릿 조회하기

        파트너사의 배송비 템플릿뿐만 아니라 쇼핑몰 배송 템플릿도 조회합니다.

        Args:
            shipping_area_type: 배송 구분
                (MALL_SHIPPING_AREA: 쇼핑몰 배송, PARTNER_SHIPPING_AREA: 파트너사 배송)

        Returns:
            list[DeliveryTemplate]: 배송비 템플릿 리스트
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if shipping_area_type is not None:
                params["shippingAreaType"] = shipping_area_type

            resp = await client.get("/deliveries", headers=headers, params=params)
            return self.handle_resp(resp, list[DeliveryTemplate])

    async def get_template_groups(
        self, shipping_area_type: ShippingAreaType | None = None
    ) -> list[TemplateGroup]:
        """
        배송비 템플릿 그룹 내역 조회하기

        파트너사의 배송비 템플릿 그룹과 쇼핑몰 배송 템플릿 그룹도 함께 조회합니다.

        Args:
            shipping_area_type: 배송 구분
                (MALL_SHIPPING_AREA: 쇼핑몰 배송, PARTNER_SHIPPING_AREA: 파트너사 배송)

        Returns:
            list[TemplateGroup]: 배송비 템플릿 그룹 리스트
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if shipping_area_type is not None:
                params["shippingAreaType"] = shipping_area_type

            resp = await client.get("/deliveries/template-groups", headers=headers, params=params)
            return self.handle_resp(resp, list[TemplateGroup])

    async def create_template_group(
        self, request: TemplateGroupCreateRequest
    ) -> TemplateGroup:
        """
        배송비 템플릿 그룹 생성하기

        파트너의 배송비 템플릿 그룹을 생성합니다.

        Args:
            request: 배송비 템플릿 그룹 생성 요청

        Returns:
            TemplateGroup: 생성된 배송비 템플릿 그룹
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.post(
                "/deliveries/template-groups", headers=headers, json=body
            )
            return self.handle_resp(resp, TemplateGroup)

    async def get_template_group(self, template_group_no: int) -> TemplateGroup:
        """
        배송비 템플릿 그룹 조회하기

        파트너의 배송비 템플릿 그룹을 조회합니다.

        Args:
            template_group_no: 배송비 템플릿 그룹 번호

        Returns:
            TemplateGroup: 배송비 템플릿 그룹 상세
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get(
                f"/deliveries/template-groups/{template_group_no}", headers=headers
            )
            return self.handle_resp(resp, TemplateGroup)

    async def update_template_group(
        self, template_group_no: int, request: TemplateGroupUpdateRequest
    ) -> None:
        """
        배송비 템플릿 그룹 수정하기

        파트너의 배송비 템플릿 그룹을 수정합니다.

        Args:
            template_group_no: 배송비 템플릿 그룹 번호
            request: 배송비 템플릿 그룹 수정 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.put(
                f"/deliveries/template-groups/{template_group_no}", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    async def get_template(self, template_no: int) -> TemplateDetail:
        """
        배송비 템플릿 상세조회하기

        배송비 템플릿 상세조회 API입니다.

        Args:
            template_no: 배송 템플릿 번호

        Returns:
            TemplateDetail: 배송비 템플릿 상세
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get(f"/deliveries/templates/{template_no}", headers=headers)
            return self.handle_resp(resp, TemplateDetail)

    # ------------------------------------
    #  Warehouse (입출고 주소)
    # ------------------------------------
    async def get_warehouses(self, page: int, size: int) -> WarehousesResponse:
        """
        입출고 주소 내역 조회하기

        파트너의 입출고 주소 내역을 조회합니다.

        Args:
            page: 시작 번호[페이징 처리] (1 이상)
            size: 종료 번호[페이징 처리]

        Returns:
            WarehousesResponse: 입출고 주소 내역 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {"page": page, "size": size}

            resp = await client.get("/warehouses", headers=headers, params=params)
            return self.handle_resp(resp, WarehousesResponse)

    async def create_warehouse(self, request: WarehouseRequest) -> Warehouse:
        """
        입출고 주소 생성하기

        파트너의 입출고 주소를 생성합니다.

        Args:
            request: 입출고 주소 생성 요청

        Returns:
            Warehouse: 생성된 입출고 주소
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.post("/warehouses", headers=headers, json=body)
            return self.handle_resp(resp, Warehouse)

    async def get_warehouse(self, warehouse_no: int) -> Warehouse:
        """
        입출고 주소 조회하기

        파트너의 입출고 주소를 조회합니다.

        Args:
            warehouse_no: 입출고 주소 번호

        Returns:
            Warehouse: 입출고 주소
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get(f"/warehouses/{warehouse_no}", headers=headers)
            return self.handle_resp(resp, Warehouse)

    async def update_warehouse(self, warehouse_no: int, request: WarehouseRequest) -> None:
        """
        입출고 주소 수정하기

        파트너의 입출고 주소를 수정합니다.

        Args:
            warehouse_no: 입출고 주소 번호
            request: 입출고 주소 수정 요청
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True)

            resp = await client.put(f"/warehouses/{warehouse_no}", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

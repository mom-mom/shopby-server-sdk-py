"""Manage API 클라이언트

쇼핑몰 운영(manage) 관련 server API 클라이언트.
"""

from datetime import date, datetime

import httpx

from shopby_sdk.base.kst import to_kst_string
from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.manage.models import (
    AccumulationPeriodType,
    AccumulationsResponse,
    AccumulationUsageItem,
    AnswerInquiryRequest,
    AssemblePeriodType,
    AssembleRequestType,
    AssemblesResponse,
    AssembleSearchType,
    AssembleStatus,
    CreateAccumulationRequest,
    CreateAccumulationResponse,
    CreateInquiryTypeRequest,
    CustomTermsMembersResponse,
    ExternalAccumulationsResponse,
    ExternalMappingKeyType,
    ExternalRequestType,
    InquiriesResponse,
    InquirySearchDateType,
    InquirySearchType,
    InquiryStatus,
    InquiryType,
    MemberAvailableAccumulationRequest,
    MemberAvailableAccumulationResponse,
    ProfileAccumulationsResponse,
    RequestGroupType,
    SendKakaoMessageRequest,
    SettlementResponse,
    SmsUnsubscribeResponse,
    SubtractAccumulationResponse,
    TermsItem,
    TermsType,
)


class ShopbyServerManageApiClient(ShopbyServerApiClient):
    """Shopby Manage Server API 클라이언트"""

    # ------------------------------------
    #  Accumulations (적립금)
    # ------------------------------------
    async def get_accumulations(
        self,
        period_type: AccumulationPeriodType,
        start_ymd: date,
        end_ymd: date,
        page: int | None = None,
        page_size: int | None = None,
        accumulation_nos: list[int] | None = None,
        is_only_available: bool | None = None,
        external_key: str | None = None,
    ) -> AccumulationsResponse:
        """적립금 조회하기

        등록일/시작일/만료일로 적립금 상태를 검색/조회하는 API입니다.

        Args:
            period_type: 기간 설정 타입 (REGISTER: 등록일, START: 생성일, EXPIRE: 만료일)
            start_ymd: 검색 시작일
            end_ymd: 검색 종료일
            page: 페이지 번호
            page_size: 페이지 사이즈 (최대 10000)
            accumulation_nos: 적립금 번호 리스트
            is_only_available: 사용가능한 적립금만 조회 여부 (default: false)
            external_key: 외부 키(조회용)

        Returns:
            AccumulationsResponse: 적립금 목록 (items, totalCount)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "periodType": period_type,
                "startYmd": start_ymd.strftime("%Y-%m-%d"),
                "endYmd": end_ymd.strftime("%Y-%m-%d"),
            }
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if accumulation_nos is not None:
                params["accumulationNos"] = ",".join(str(no) for no in accumulation_nos)
            if is_only_available is not None:
                params["isOnlyAvailable"] = is_only_available
            if external_key is not None:
                params["externalKey"] = external_key

            resp = await client.get("/accumulations", headers=headers, params=params)
            return self.handle_resp(resp, AccumulationsResponse)

    async def get_accumulation_assembles(
        self,
        page: int | None = None,
        page_size: int | None = None,
        search_type: AssembleSearchType | None = None,
        keyword: str | None = None,
        period_type: AssemblePeriodType | None = None,
        start_date_time: datetime | None = None,
        end_date_time: datetime | None = None,
        immediately: bool | None = None,
        request_group_type: RequestGroupType | None = None,
        request_types: list[AssembleRequestType] | None = None,
        statuses: list[AssembleStatus] | None = None,
    ) -> AssemblesResponse:
        """적립금 변동 요청 조회

        등록된 적립금 변동 요청 내역을 검색합니다.

        Args:
            page: 페이지 번호
            page_size: 페이지 사이즈 (최대 10000)
            search_type: 검색 유형 (default: ALL)
            keyword: 검색 내용
            period_type: 검색 기간 유형 (default: REGISTER)
            start_date_time: 검색 기간 시작일 (default: 3개월 전)
            end_date_time: 검색 기간 종료일 (default: 오늘)
            immediately: 즉시지급 여부
            request_group_type: 전체/지급/차감
            request_types: 예약지급/즉시지급/즉시차감 리스트
            statuses: 지급요청 상태 리스트

        Returns:
            AssemblesResponse: 적립금 변동 요청 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if search_type is not None:
                params["searchType"] = search_type
            if keyword is not None:
                params["keyword"] = keyword
            if period_type is not None:
                params["periodType"] = period_type
            if start_date_time is not None:
                params["startDateTime"] = to_kst_string(start_date_time)
            if end_date_time is not None:
                params["endDateTime"] = to_kst_string(end_date_time)
            if immediately is not None:
                params["immediately"] = immediately
            if request_group_type is not None:
                params["requestGroupType"] = request_group_type
            if request_types is not None:
                params["requestTypes"] = ",".join(request_types)
            if statuses is not None:
                params["statuses"] = ",".join(statuses)

            resp = await client.get("/accumulations/assembles", headers=headers, params=params)
            return self.handle_resp(resp, AssemblesResponse)

    async def get_accumulation_externals(
        self,
        start_ymdt: datetime,
        end_ymdt: datetime,
        page: int | None = None,
        page_size: int | None = None,
        success: bool | None = None,
        request_type: ExternalRequestType | None = None,
        mapping_key_type: ExternalMappingKeyType | None = None,
        mapping_keys: list[str] | None = None,
        external_nos: list[str] | None = None,
        seqs: list[int] | None = None,
    ) -> ExternalAccumulationsResponse:
        """외부적립금 연동 이력 조회

        외부적립금 연동을 사용하는 몰에서 적립금 연동 이력을 조회합니다.

        Args:
            start_ymdt: 조회 시작일
            end_ymdt: 조회 종료일
            page: 페이지 번호
            page_size: 페이지 사이즈 (최대 10000)
            success: 성공여부
            request_type: 요청타입 (ADD, SUB, SUB_ROLLBACK)
            mapping_key_type: 매핑키 종류 (mappingKeys와 함께 사용)
            mapping_keys: 매핑키 값 리스트 (mappingKeyType과 함께 사용)
            external_nos: 외부연동키 리스트
            seqs: 트랜잭션 ID 리스트

        Returns:
            ExternalAccumulationsResponse: 외부적립금 이력 목록 (items, totalCount)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "startYmdt": to_kst_string(start_ymdt),
                "endYmdt": to_kst_string(end_ymdt),
            }
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if success is not None:
                params["success"] = success
            if request_type is not None:
                params["requestType"] = request_type
            if mapping_key_type is not None:
                params["mappingKeyType"] = mapping_key_type
            if mapping_keys is not None:
                params["mappingKeys"] = ",".join(mapping_keys)
            if external_nos is not None:
                params["externalNos"] = ",".join(external_nos)
            if seqs is not None:
                params["seqs"] = ",".join(str(seq) for seq in seqs)

            resp = await client.get("/accumulations/externals", headers=headers, params=params)
            return self.handle_resp(resp, ExternalAccumulationsResponse)

    async def get_accumulation_settlement(
        self,
        start_ymd: datetime,
        end_ymd: datetime,
        page: int | None = None,
        page_size: int | None = None,
    ) -> SettlementResponse:
        """적립금 지급/차감 이력 조회

        적립금 지급/차감/차감롤백 이력을 조회합니다.

        Args:
            start_ymd: 조회 시작일
            end_ymd: 조회 종료일
            page: 페이지 번호
            page_size: 페이지 사이즈 (최대 10000)

        Returns:
            SettlementResponse: 적립금 지급/차감 이력 (items, totalCount)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "startYmd": to_kst_string(start_ymd),
                "endYmd": to_kst_string(end_ymd),
            }
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size

            resp = await client.get("/accumulations/settlement", headers=headers, params=params)
            return self.handle_resp(resp, SettlementResponse)

    async def get_accumulation_usage(
        self,
        accumulation_nos: list[int],
    ) -> list[AccumulationUsageItem]:
        """적립금 사용처 추적하기

        적립금 번호를 넘기면 해당 적립금을 사용자가 어떤 주문에 사용했는지 추적합니다.

        Args:
            accumulation_nos: 적립금 번호 리스트 (최대 1000개)

        Returns:
            list[AccumulationUsageItem]: 적립금 사용처 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "accumulationNos": ",".join(str(no) for no in accumulation_nos),
            }

            resp = await client.get("/accumulations/usage", headers=headers, params=params)
            return self.handle_resp(resp, list[AccumulationUsageItem])

    async def get_member_available_accumulations(
        self,
        request: MemberAvailableAccumulationRequest,
    ) -> MemberAvailableAccumulationResponse:
        """회원 보유 적립금 조회(다건)

        회원 아이디(memberId)와 회원 번호(memberNo)를 기준으로 회원의 보유(가용) 적립금을 조회합니다.
        memberId와 memberNo를 합산하여 최대 500건까지 조회할 수 있습니다.

        Args:
            request: 회원 아이디/번호 리스트

        Returns:
            MemberAvailableAccumulationResponse: 회원 보유 적립금 목록 (items, count)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.post(
                "/accumulations/members/available", headers=headers, json=body
            )
            return self.handle_resp(resp, MemberAvailableAccumulationResponse)

    async def get_profile_accumulations(
        self,
        page: int | None = None,
        page_size: int | None = None,
        member_id: str | None = None,
        member_no: int | None = None,
        start_ymd: date | None = None,
        end_ymd: date | None = None,
    ) -> ProfileAccumulationsResponse:
        """적립금 상태 조회하기

        특정 회원의 적립금 상태를 검색/조회하는 API입니다.

        Args:
            page: 페이지 번호
            page_size: 페이지 사이즈 (최대 10000)
            member_id: 회원 아이디(회원 조회용)
            member_no: 회원 번호(회원 조회용)
            start_ymd: 검색 시작일
            end_ymd: 검색 종료일

        Returns:
            ProfileAccumulationsResponse: 회원 적립금 상태 (totalAmt, items, ...)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if member_id is not None:
                params["memberId"] = member_id
            if member_no is not None:
                params["memberNo"] = member_no
            if start_ymd is not None:
                params["startYmd"] = start_ymd.strftime("%Y-%m-%d")
            if end_ymd is not None:
                params["endYmd"] = end_ymd.strftime("%Y-%m-%d")

            resp = await client.get("/profile/accumulations", headers=headers, params=params)
            return self.handle_resp(resp, ProfileAccumulationsResponse)

    async def create_accumulation(
        self,
        request: CreateAccumulationRequest,
    ) -> CreateAccumulationResponse:
        """적립금 지급하기

        특정 회원에게 적립금을 즉시 지급하는 API입니다.

        Args:
            request: 적립금 지급 요청 정보

        Returns:
            CreateAccumulationResponse: 회원번호, 생성된 적립금 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.post("/profile/accumulations", headers=headers, json=body)
            return self.handle_resp(resp, CreateAccumulationResponse)

    async def subtract_accumulation(
        self,
        accumulation_amt: float | None = None,
        entire_subtracted: bool | None = None,
        member_id: str | None = None,
        member_no: int | None = None,
        detail_reason: str | None = None,
        external_key: str | None = None,
        is_manual: bool | None = None,
    ) -> SubtractAccumulationResponse:
        """적립금 차감하기

        특정 회원의 적립금을 차감하는 API입니다.
        회원의 보유 적립금보다 많은 금액 차감 시 차감 실패합니다.

        Args:
            accumulation_amt: 적립금 차감 금액
            entire_subtracted: 전체 적립금 차감 여부
            member_id: 회원 아이디(회원 조회용)
            member_no: 회원 번호(회원 조회용)
            detail_reason: 적립금 차감 사유(최대 200자)
            external_key: 외부 키(조회용)(최대 60자)
            is_manual: 운영자 수동 지급 여부 (true: 수동, false: 자동)

        Returns:
            SubtractAccumulationResponse: 차감 결과
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool | float] = {}
            if accumulation_amt is not None:
                params["accumulationAmt"] = accumulation_amt
            if entire_subtracted is not None:
                params["entireSubtracted"] = entire_subtracted
            if member_id is not None:
                params["memberId"] = member_id
            if member_no is not None:
                params["memberNo"] = member_no
            if detail_reason is not None:
                params["detailReason"] = detail_reason
            if external_key is not None:
                params["externalKey"] = external_key
            if is_manual is not None:
                params["isManual"] = is_manual

            resp = await client.delete("/profile/accumulations", headers=headers, params=params)
            return self.handle_resp(resp, SubtractAccumulationResponse)

    async def expire_accumulation(self, accumulation_no: int) -> None:
        """적립금 만료 처리

        특정 적립금을 만료하는 API입니다.
        지정한 적립금의 남은 사용 가능한 적립금 금액을 만료시킵니다.

        Args:
            accumulation_no: 적립금 번호
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.put(
                f"/profile/accumulations/{accumulation_no}/expire", headers=headers
            )
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  Inquiry (1:1문의)
    # ------------------------------------
    async def get_inquiries(
        self,
        page: int | None = None,
        page_size: int | None = None,
        search_type: InquirySearchType | None = None,
        keyword: str | None = None,
        inquiry_type_no: int | None = None,
        assignee_no: int | None = None,
        issuer_no: int | None = None,
        inquiry_statuses: list[InquiryStatus] | None = None,
        start_date_time: datetime | None = None,
        end_date_time: datetime | None = None,
        is_unspecified: bool | None = None,
        search_date_type: InquirySearchDateType | None = None,
    ) -> InquiriesResponse:
        """1:1문의 조회하기

        Args:
            page: 페이지 번호
            page_size: 페이지 사이즈 (최대 10000)
            search_type: 검색 유형 (ALL, INQUIRY_NO, TITLE, CONTENT, ISSUER, ASSIGNEE)
            keyword: 키워드
            inquiry_type_no: 문의 유형 번호
            assignee_no: 담당자 번호
            issuer_no: 문의자 번호
            inquiry_statuses: 문의 상태 리스트
            start_date_time: 검색 기준 시작일 (미입력 시 3달 전)
            end_date_time: 검색 기준 종료일 (미입력 시 현재 시각)
            is_unspecified: 담당자 미지정 여부 (assigneeNo보다 우선, default: false)
            search_date_type: 검색 날짜 유형 (default: REGISTER)

        Returns:
            InquiriesResponse: 1:1문의 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if search_type is not None:
                params["searchType"] = search_type
            if keyword is not None:
                params["keyword"] = keyword
            if inquiry_type_no is not None:
                params["inquiryTypeNo"] = inquiry_type_no
            if assignee_no is not None:
                params["assigneeNo"] = assignee_no
            if issuer_no is not None:
                params["issuerNo"] = issuer_no
            if inquiry_statuses is not None:
                params["inquiryStatuses"] = ",".join(inquiry_statuses)
            if start_date_time is not None:
                params["startDateTime"] = to_kst_string(start_date_time)
            if end_date_time is not None:
                params["endDateTime"] = to_kst_string(end_date_time)
            if is_unspecified is not None:
                params["isUnspecified"] = is_unspecified
            if search_date_type is not None:
                params["searchDateType"] = search_date_type

            resp = await client.get("/inquiries", headers=headers, params=params)
            return self.handle_resp(resp, InquiriesResponse)

    async def get_inquiry_types(self) -> list[InquiryType]:
        """1:1문의 유형 조회하기

        1:1문의 유형을 조회하는 API입니다.

        Returns:
            list[InquiryType]: 1:1문의 유형 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}

            resp = await client.get("/inquiries/types", headers=headers)
            return self.handle_resp(resp, list[InquiryType])

    async def create_inquiry_type(self, request: CreateInquiryTypeRequest) -> None:
        """1:1문의 유형 생성하기

        1:1문의 유형을 생성하는 API입니다.

        Args:
            request: 1:1문의 유형 생성 요청 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.post("/inquiries/types", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    async def answer_inquiry(
        self,
        inquiry_no: str,
        request: AnswerInquiryRequest,
    ) -> None:
        """1:1 문의 답변 등록

        Args:
            inquiry_no: 문의번호
            request: 답변 등록 요청 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.post(
                f"/inquiries/{inquiry_no}/answer", headers=headers, json=body
            )
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  Kakao (카카오 알림톡)
    # ------------------------------------
    async def send_kakao_message(self, request: SendKakaoMessageRequest) -> None:
        """카카오 알림톡 메시지 수동 전송

        카카오 알림톡 메시지를 수동 전송하는 API입니다.
        몰 설정에 따라 provider(비즈엠, 샵바이)가 적용되어 전송됩니다.

        Args:
            request: 카카오 알림톡 전송 요청 정보
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            body = request.model_dump(by_alias=True, exclude_none=True, mode="json")

            resp = await client.post("/kakao/send", headers=headers, json=body)
            self.raise_for_status(resp)
            return None

    # ------------------------------------
    #  SMS (수신거부)
    # ------------------------------------
    async def get_sms_unsubscribe_list(
        self,
        page: int | None = None,
        page_size: int | None = None,
        keyword: str | None = None,
    ) -> SmsUnsubscribeResponse:
        """080 수신거부 목록 조회

        080 수신거부 전화번호 목록을 조회하는 API입니다.

        Args:
            page: 페이지 번호 (default: 1)
            page_size: 페이지당 조회 건수 (default: 10, 최대: 100)
            keyword: 검색할 전화번호 (하이픈 포함/미포함 모두 가능)

        Returns:
            SmsUnsubscribeResponse: 수신거부 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {}
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["pageSize"] = page_size
            if keyword is not None:
                params["keyword"] = keyword

            resp = await client.get("/sms/unsubscribe", headers=headers, params=params)
            return self.handle_resp(resp, SmsUnsubscribeResponse)

    # ------------------------------------
    #  Terms (약관)
    # ------------------------------------
    async def get_terms(self, terms_types: list[TermsType]) -> list[TermsItem]:
        """유형별 약관 조회

        유형별 약관을 조회하는 API입니다.

        Args:
            terms_types: 약관 유형 리스트

        Returns:
            list[TermsItem]: 약관 목록
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "termsTypes": ",".join(terms_types),
            }

            resp = await client.get("/terms", headers=headers, params=params)
            return self.handle_resp(resp, list[TermsItem])

    async def get_custom_terms_agree_members(
        self,
        custom_terms_no: str,
        page: int,
        page_size: int,
    ) -> CustomTermsMembersResponse:
        """추가 약관 동의 회원 목록 조회

        추가 약관에 동의한 회원 목록을 조회합니다.

        Args:
            custom_terms_no: 추가 약관 번호
            page: 페이지 번호
            page_size: 페이지 크기

        Returns:
            CustomTermsMembersResponse: 동의 회원 목록 (totalCount, contents)
        """
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            headers = {"version": "1.0"}
            params: dict[str, str | int | bool] = {
                "page": page,
                "pageSize": page_size,
            }

            resp = await client.get(
                f"/terms/custom/{custom_terms_no}/members", headers=headers, params=params
            )
            return self.handle_resp(resp, CustomTermsMembersResponse)

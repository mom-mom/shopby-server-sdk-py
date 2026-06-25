"""Manage API 클라이언트 패키지

쇼핑몰 운영(manage) 관련 server API 클라이언트와 모델을 export합니다.
"""

from shopby_sdk.clients.manage.client import ShopbyServerManageApiClient
from shopby_sdk.clients.manage.models import (
    # Literal 타입 별칭
    AccumulationPeriodType,
    AccumulationReserveReason,
    AccumulationStatus,
    AssemblePeriodType,
    AssembleRequestType,
    AssembleSearchType,
    AssembleStatus,
    ExternalMappingKeyType,
    ExternalRequestType,
    InquirySearchDateType,
    InquirySearchType,
    InquiryStatus,
    NotificationChannel,
    RequestGroupType,
    TermsType,
    ValidPeriodType,
    # Accumulations 조회
    AccumulationItem,
    AccumulationsResponse,
    # Accumulations 변동 요청
    AssembleItem,
    AssembleOrderRequest,
    AssembleTarget,
    AssemblesResponse,
    # Accumulations 외부 연동
    ExternalAccumulationItem,
    ExternalAccumulationsResponse,
    # Accumulations 정산
    SettlementItem,
    SettlementResponse,
    # Accumulations 사용처
    AccumulationUsage,
    AccumulationUsageItem,
    # Accumulations 회원 보유
    MemberAvailableAccumulationItem,
    MemberAvailableAccumulationRequest,
    MemberAvailableAccumulationResponse,
    # Accumulations 회원 상태
    ProfileAccumulationItem,
    ProfileAccumulationsResponse,
    # Accumulations 지급/차감/만료
    CreateAccumulationRequest,
    CreateAccumulationResponse,
    SubtractAccumulationResponse,
    SubtractionRelatedAccumulation,
    # Inquiry
    AnswerInquiryRequest,
    CreateInquiryTypeRequest,
    InquiriesResponse,
    InquiryAnswerFile,
    InquiryAnswerFileInput,
    InquiryAssignee,
    InquiryExternal,
    InquiryIssuer,
    InquiryItem,
    InquiryNaverPay,
    InquiryType,
    # Kakao
    SendKakaoMessageRequest,
    # SMS
    SmsUnsubscribeItem,
    SmsUnsubscribeResponse,
    # Terms
    CustomTermsMember,
    CustomTermsMembersResponse,
    TermsItem,
)

__all__ = [
    "ShopbyServerManageApiClient",
    # Literal 타입 별칭
    "AccumulationPeriodType",
    "AccumulationReserveReason",
    "AccumulationStatus",
    "AssemblePeriodType",
    "AssembleRequestType",
    "AssembleSearchType",
    "AssembleStatus",
    "ExternalMappingKeyType",
    "ExternalRequestType",
    "InquirySearchDateType",
    "InquirySearchType",
    "InquiryStatus",
    "NotificationChannel",
    "RequestGroupType",
    "TermsType",
    "ValidPeriodType",
    # Accumulations 조회
    "AccumulationItem",
    "AccumulationsResponse",
    # Accumulations 변동 요청
    "AssembleItem",
    "AssembleOrderRequest",
    "AssembleTarget",
    "AssemblesResponse",
    # Accumulations 외부 연동
    "ExternalAccumulationItem",
    "ExternalAccumulationsResponse",
    # Accumulations 정산
    "SettlementItem",
    "SettlementResponse",
    # Accumulations 사용처
    "AccumulationUsage",
    "AccumulationUsageItem",
    # Accumulations 회원 보유
    "MemberAvailableAccumulationItem",
    "MemberAvailableAccumulationRequest",
    "MemberAvailableAccumulationResponse",
    # Accumulations 회원 상태
    "ProfileAccumulationItem",
    "ProfileAccumulationsResponse",
    # Accumulations 지급/차감/만료
    "CreateAccumulationRequest",
    "CreateAccumulationResponse",
    "SubtractAccumulationResponse",
    "SubtractionRelatedAccumulation",
    # Inquiry
    "AnswerInquiryRequest",
    "CreateInquiryTypeRequest",
    "InquiriesResponse",
    "InquiryAnswerFile",
    "InquiryAnswerFileInput",
    "InquiryAssignee",
    "InquiryExternal",
    "InquiryIssuer",
    "InquiryItem",
    "InquiryNaverPay",
    "InquiryType",
    # Kakao
    "SendKakaoMessageRequest",
    # SMS
    "SmsUnsubscribeItem",
    "SmsUnsubscribeResponse",
    # Terms
    "CustomTermsMember",
    "CustomTermsMembersResponse",
    "TermsItem",
]

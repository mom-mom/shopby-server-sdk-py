"""Shopby Shop(Client) Manage API 패키지.

shop-api(`https://shop-api.e-ncp.com`) 의 공개(인증 불필요) manage 도메인
(주소/게시판/공휴일/1:1문의 설정/인스타그램/외부스크립트/약관) 클라이언트와
모델을 export 한다.
"""

from shopby_sdk.shop.manage.client import ShopbyShopManageApiClient
from shopby_sdk.shop.manage.models import (
    # Address
    AddressItem,
    AddressSearchResponse,
    ArticleDetailResponse,
    # Board
    ArticleListItem,
    ArticleListResponse,
    BoardCategory,
    BoardConfigurationsResponse,
    BoardDirection,
    CustomTermsCategoryType,
    CustomTermsItem,
    CustomTermsRequest,
    # Page
    ExternalScriptItem,
    # Inquiry
    InquiryConfigurationResponse,
    InquiryDisplayType,
    InquiryImageDisplayType,
    InquiryType,
    InquiryTypeDirection,
    InstagramError,
    # Instagram
    InstagramMediaItem,
    InstagramMediaResponse,
    JapanAddressResponse,
    PostAttachment,
    PostDetailResponse,
    PostListItem,
    PostListResponse,
    PostPreviewItem,
    PostPreviewsRequest,
    PostSearchType,
    PostsV2SearchRequest,
    PostTermsDetailRequest,
    PostUsedTermsRequest,
    RegisterType,
    TermsContents,
    TermsDetailResponse,
    TermsHistoryItem,
    # Terms
    TermsType,
    UsedTermsResponse,
    UsedTermsTypesResponse,
)

__all__ = [
    "ShopbyShopManageApiClient",
    # Literal 타입 별칭
    "BoardDirection",
    "PostSearchType",
    "RegisterType",
    "InquiryDisplayType",
    "InquiryImageDisplayType",
    "InquiryTypeDirection",
    "TermsType",
    "CustomTermsCategoryType",
    # Address
    "AddressItem",
    "AddressSearchResponse",
    "JapanAddressResponse",
    # Board
    "BoardConfigurationsResponse",
    "BoardCategory",
    "PostAttachment",
    "ArticleListItem",
    "ArticleListResponse",
    "ArticleDetailResponse",
    "PostsV2SearchRequest",
    "PostListItem",
    "PostListResponse",
    "PostDetailResponse",
    "PostPreviewsRequest",
    "PostPreviewItem",
    # Inquiry
    "InquiryConfigurationResponse",
    "InquiryType",
    # Instagram
    "InstagramMediaItem",
    "InstagramError",
    "InstagramMediaResponse",
    # Page
    "ExternalScriptItem",
    # Terms
    "TermsContents",
    "UsedTermsResponse",
    "PostUsedTermsRequest",
    "CustomTermsRequest",
    "CustomTermsItem",
    "TermsHistoryItem",
    "UsedTermsTypesResponse",
    "TermsDetailResponse",
    "PostTermsDetailRequest",
]

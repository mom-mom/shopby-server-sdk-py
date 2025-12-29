"""Member API 클라이언트 및 모델"""

from shopby_sdk.clients.member.client import ShopbyServerMemberApiClient
from shopby_sdk.clients.member.models import (
    AddMemberToGroupRequest,
    AddMemberToGroupResponse,
    Member,
    MemberGroup,
    MemberSearchType,
    MembersListResponse,
    MemberStatus,
    MemberType,
    OpenIdProvider,
    ProfileGroupItem,
    ProfileGroupsResponse,
    ProviderType,
    ReserveBenefit,
)

__all__ = [
    # Client
    "ShopbyServerMemberApiClient",
    # Request Enum Types
    "MemberSearchType",
    "MemberStatus",
    "MemberType",
    "ProviderType",
    # Member Group Models
    "ReserveBenefit",
    "MemberGroup",
    # Profile Group Models
    "ProfileGroupItem",
    "ProfileGroupsResponse",
    "AddMemberToGroupRequest",
    "AddMemberToGroupResponse",
    # Member Models
    "OpenIdProvider",
    "Member",
    "MembersListResponse",
]

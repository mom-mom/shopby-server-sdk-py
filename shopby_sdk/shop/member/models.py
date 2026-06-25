"""Shopby Shop(Client) Member API 모델.

shop-api(`https://shop-api.e-ncp.com`) member 도메인의 공개(인증 불필요) 엔드포인트
요청/응답 모델. 모든 모델은 ``BaseDto`` 를 상속하므로 snake_case 필드가 자동으로
camelCase alias 와 매핑된다.

대응 OpenAPI 스펙: docs/api/member-shop-public.yml
"""

from typing import Any, Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto

# ---------------------------------------------------------------------------
#  Company — 사업자등록번호 중복체크
# ---------------------------------------------------------------------------


class BusinessExistResponse(BaseDto):
    """사업자등록번호 중복 여부.

    OpenAPI schema: companies-business-exist-1571895320
    """

    exist: bool = Field(description="존재(중복) 여부")


# ---------------------------------------------------------------------------
#  Member-Config — 회원정보 추가항목 Config
# ---------------------------------------------------------------------------

ExtraInfoType = Literal["TEXTBOX", "RADIOBUTTON", "CHECKBOX", "DROPDOWN", "IMAGE"]
"""추가항목 타입: 텍스트박스/라디오버튼/체크박스/드롭다운/이미지."""

ExtraInfoStatus = Literal["REQUIRED", "USED"]
"""추가항목 사용 상태: 필수(REQUIRED)/사용(USED)."""


class ExtraInfoOptionSummary(BaseDto):
    """추가항목 옵션 요약.

    OpenAPI schema: config-member-extra-info495587874 (extraInfoOptions item)
    """

    extra_info_option_no: int = Field(description="옵션 번호")
    extra_info_option_name: str = Field(description="옵션 명")


class ExtraInfoSummaryContent(BaseDto):
    """회원정보 추가항목 요약.

    OpenAPI schema: config-member-extra-info495587874 (extraInfoContents item)
    """

    extra_info_no: int = Field(description="항목 번호")
    extra_info_name: str = Field(description="항목 명")
    # 스펙 enum 은 TEXTBOX/RADIOBUTTON/CHECKBOX/DROPDOWN/IMAGE 이나
    # 미래 확장 가능성을 고려해 str 도 허용.
    extra_info_type: ExtraInfoType | str = Field(description="항목 타입")
    extra_info_options: list[ExtraInfoOptionSummary] = Field(
        default_factory=list, description="옵션 목록"
    )
    status: ExtraInfoStatus | str = Field(description="사용 상태")


class MemberExtraInfoConfigResponse(BaseDto):
    """회원정보 추가항목 Config 조회 응답.

    OpenAPI schema: config-member-extra-info495587874
    """

    extra_info_contents: list[ExtraInfoSummaryContent] = Field(
        default_factory=list, description="회원정보 추가항목 목록"
    )


# ---------------------------------------------------------------------------
#  Member-Grade — 회원 등급 정보
# ---------------------------------------------------------------------------

AutoSupplyingType = Literal["NONE", "ONCE", "MONTHLY"]
"""자동지급 유형: 사용안함(NONE)/1회지급(ONCE)/매월지급(MONTHLY)."""


class GradeReserveAutoSupplying(BaseDto):
    """회원 등급 적립금 자동지급."""

    amount: float = Field(description="적립금 자동지급 적립금액")
    used: bool = Field(description="적립금 자동지급 사용여부")
    type: AutoSupplyingType | str = Field(description="적립금 자동지급 유형")


class GradeEvaluationCondition(BaseDto):
    """회원 등급 평가 조건."""

    minimum_payment: float = Field(description="최소 구매 금액")
    minimum_count: float = Field(description="최소 구매 횟수")


class GradeReserveBenefit(BaseDto):
    """적립금 혜택."""

    reserve_rate: float = Field(description="적립금 혜택 적립률")
    used: bool = Field(description="적립금 혜택 사용여부")


class GradeCouponAutoSupplying(BaseDto):
    """쿠폰 자동지급."""

    used: bool = Field(description="쿠폰 자동지급 사용여부")
    type: AutoSupplyingType | str = Field(description="쿠폰 자동지급 유형")


class MemberGrade(BaseDto):
    """회원 등급 정보.

    OpenAPI schema: member-grades494184672 (item)
    """

    no: float = Field(description="등급번호")
    label: str = Field(description="등급명")
    description: str = Field(description="등급 설명")
    member_grade_image_url: str | None = Field(None, description="등급 이미지 URL")
    is_evaluation_exempt: bool = Field(description="등급 평가 면제 여부")
    evaluation_condition: GradeEvaluationCondition = Field(description="회원 등급 평가 조건")
    reserve_auto_supplying: GradeReserveAutoSupplying = Field(description="적립금 자동지급")
    reserve_benefit: GradeReserveBenefit = Field(description="적립금 혜택")
    coupon_auto_supplying: GradeCouponAutoSupplying = Field(description="쿠폰 자동지급")


# ---------------------------------------------------------------------------
#  Member-Group — 회원 그룹 정보
# ---------------------------------------------------------------------------


class MemberGroup(BaseDto):
    """회원 그룹 정보.

    OpenAPI schema: member-groups-2025495528 (item)
    """

    no: float = Field(description="그룹번호")
    name: str = Field(description="그룹명")
    description: str = Field(description="그룹 설명")
    reserve_benefit: GradeReserveBenefit = Field(description="적립금 혜택")


# ---------------------------------------------------------------------------
#  Profile — 중복/검증 확인 (공통 exist 응답)
# ---------------------------------------------------------------------------


class ProfileExistResponse(BaseDto):
    """이메일/아이디/닉네임 중복 및 회원 일치 여부 확인 응답.

    OpenAPI schema: profile-email-exist1345433695
    (email/id/nickname/member-equals 엔드포인트 공통 응답)
    """

    exist: bool = Field(description="존재(중복/일치) 여부")
    status: str | None = Field(None, description="회원 상태")


class ProfileMobileExistResponse(BaseDto):
    """휴대폰 번호 중복 여부 확인 응답.

    OpenAPI schema: profile-mobile-exist578354644
    """

    mobile_no_exist: bool = Field(description="번호 존재 여부")
    status: str = Field(description="회원 상태")
    member_id: str = Field(description="해당 휴대폰 번호로 등록된 마스킹된 회원 ID")


# ---------------------------------------------------------------------------
#  Profile — 회원별 추가항목 조회
# ---------------------------------------------------------------------------


class MemberExtraInfo(BaseDto):
    """회원 추가항목.

    OpenAPI schema: profile-member-extra-infos-1686285859 (memberExtraInfos item)
    """

    extra_info_name: str = Field(description="추가항목 명")
    extra_info_text_content: str | None = Field(None, description="추가항목 텍스트 내용")
    # 스펙상 oneOf(object/boolean/string/number) 이므로 임의 타입 허용.
    extra_info_option_names: list[Any] = Field(
        default_factory=list, description="추가항목 옵션 목록"
    )


class MemberSummaryExtraInfo(BaseDto):
    """회원 요약 추가항목.

    OpenAPI schema: profile-member-extra-infos-1686285859 (memberSummaryExtraInfos item)
    """

    member_no: float = Field(description="회원번호")
    member_extra_infos: list[MemberExtraInfo] = Field(
        default_factory=list, description="회원 추가항목 목록"
    )


class MemberExtraInfosResponse(BaseDto):
    """회원별 추가항목 조회 응답.

    OpenAPI schema: profile-member-extra-infos-1686285859
    """

    member_summary_extra_infos: list[MemberSummaryExtraInfo] = Field(
        default_factory=list, description="회원 요약 추가항목 목록"
    )


# ---------------------------------------------------------------------------
#  Profile — 외부회원 중복확인
# ---------------------------------------------------------------------------


class ExternalMemberExistRequest(BaseDto):
    """외부회원 중복확인 요청.

    OpenAPI schema: profile-external-member-exist1934641967
    """

    open_access_token: str = Field(
        description="IdP(Identity Provider) 엑세스 토큰"
    )


class ExternalMemberExistResponse(BaseDto):
    """외부회원 중복확인 응답.

    OpenAPI schema: profile-external-member-exist19885919
    """

    result: str = Field(description="중복확인 결과")

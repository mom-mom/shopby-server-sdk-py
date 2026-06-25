"""배너(Banner) 모델."""

from __future__ import annotations

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class BannerExtraInfo(BaseDto):
    """배너 추가 정보 (schema: display-banners-extraInfos[])."""

    banner_no: int | None = None
    extra_info: str | None = None


class Banner(BaseDto):
    """배너 단건 (배너 섹션 account 내 banners[])."""

    banner_no: int | None = None
    name: str | None = None
    name_color: str | None = None
    description: str | None = None
    description_color: str | None = None
    image_url: str | None = None
    mouse_over_image_url: str | None = None
    video_url: str | None = None
    landing_url: str | None = None
    landing_url_type: str | None = None
    brower_target_type: str | None = None
    left_space_color: str | None = None
    right_space_color: str | None = None
    display_order: int | None = None
    display_period_type: str | None = None
    display_start_ymdt: KstDatetime | None = None
    display_end_ymdt: KstDatetime | None = None


class BannerAccount(BaseDto):
    """배너 계정(노출 영역) (배너 섹션 accounts[])."""

    account_no: int | None = None
    account_name: str | None = None
    display_type: str | None = None
    display_order: int | None = None
    width: int | None = None
    height: int | None = None
    banners: list[Banner] | None = None


class BannerSection(BaseDto):
    """배너 섹션 (schema: display-banners-bannerSectionCodes[])."""

    banner_section_no: int | None = None
    group_no: int | None = None
    id: str | None = None
    code: str | None = None
    label: str | None = None
    accounts: list[BannerAccount] | None = None

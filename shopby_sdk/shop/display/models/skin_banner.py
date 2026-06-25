"""스킨 배너(SkinBanner) 모델."""

from __future__ import annotations

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime


class SkinBannerDisplayValue(BaseDto):
    """노출 기간 정보."""

    display_period_type: str | None = None
    start_date_time: KstDatetime | None = None
    end_date_time: KstDatetime | None = None


class SkinBannerSlideNavigationInfo(BaseDto):
    button_size_type: str | None = None
    inactive_button_color: str | None = None
    active_button_color: str | None = None
    button_border_type: str | None = None


class SkinBannerSlideConfig(BaseDto):
    slide_speed_type: str | None = None
    slide_time: int | None = None
    slide_navigation_type: str | None = None
    slide_effect_type: str | None = None
    slide_button_color: str | None = None
    usable_slide_button: bool | None = None
    slide_navigation_info: SkinBannerSlideNavigationInfo | None = None


class SkinBannerImage(BaseDto):
    image_no: int | None = None
    image_url: str | None = None
    active_navigation_image_url: str | None = None
    inactive_navigation_image_url: str | None = None
    landing_url: str | None = None
    open_location_type: str | None = None
    description: str | None = None
    display_order: int | None = None
    display_value: SkinBannerDisplayValue | None = None


class SkinBannerItem(BaseDto):
    """스킨 배너 단건 (skin-banners[].banners[])."""

    banner_no: int | None = None
    banner_title: str | None = None
    platform_type: str | None = None
    visible: bool | None = None
    resizable: bool | None = None
    width: int | None = None
    height: int | None = None
    size_unit_type: str | None = None
    register_date_time: KstDatetime | None = None
    update_date_time: KstDatetime | None = None
    display_value: SkinBannerDisplayValue | None = None
    slide_banner_config: SkinBannerSlideConfig | None = None
    banner_images: list[SkinBannerImage] | None = None


class SkinBannerGroup(BaseDto):
    """스킨 배너 그룹 (schema: skin-banners-90334975[])."""

    skin_no: int | None = None
    skin_code: str | None = None
    skin_name: str | None = None
    banner_group_type: str | None = None
    banner_group_code: str | None = None
    banner_group_name: str | None = None
    banners: list[SkinBannerItem] | None = None


class SkinDecorationConfig(BaseDto):
    background_color: str | None = None
    main_color: str | None = None


class BannerGroupSummary(BaseDto):
    group_type: str | None = None
    group_code: str | None = None
    group_name: str | None = None


class SkinBannerGroupsBySkin(BaseDto):
    """사용/작업중 스킨 정보 및 배너 그룹 (schema: skin-banners-groups-by-skin)."""

    skin_code: str | None = None
    skin_name: str | None = None
    platform_type: str | None = None
    app_icon: str | None = None
    is_work_skin: bool | None = None
    is_live_skin: bool | None = None
    update_date_time: KstDatetime | None = None
    decoration_config: SkinDecorationConfig | None = None
    banner_groups: list[BannerGroupSummary] | None = None

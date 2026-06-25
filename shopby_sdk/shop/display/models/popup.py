"""팝업(Popup) 모델."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime

PopupPageType = Literal["MAIN", "CATEGORY", "EVENT", "PRODUCT"]


class PopupDisplayCategoryInfo(BaseDto):
    display_category_no: int | None = None
    depth: int | None = None


class PopupPageInfos(BaseDto):
    page_types: str | None = None
    mall_product_infos: list[int] | None = None
    event_infos: list[int] | None = None
    display_category_infos: list[PopupDisplayCategoryInfo] | None = None


class PopupDetailInfo(BaseDto):
    screen_type: str | None = None
    screen_width: int | None = None
    screen_width_unit: str | None = None
    screen_height: int | None = None
    screen_height_unit: str | None = None
    screen_top_position: int | None = None
    screen_top_unit: str | None = None
    screen_left_position: int | None = None
    screen_left_unit: str | None = None
    bg_color: str | None = None
    resizable: bool | None = None


class PopupSlideImage(BaseDto):
    popup_image_no: int | None = None
    main_image_url: str | None = None
    thumb_image_url: str | None = None
    thumb_image_url_on_over: str | None = None
    landing_url: str | None = None
    open_location_target: str | None = None
    has_uploaded: bool | None = None


class PopupSlideInfo(BaseDto):
    slide_speed: str | None = None
    slide_direction: str | None = None
    slide_count: str | None = None
    slide_min_width: int | None = None
    slide_max_width: int | None = None
    slide_min_height: int | None = None
    slide_max_height: int | None = None
    resizable: bool | None = None
    slide_images: list[PopupSlideImage] | None = None


class Popup(BaseDto):
    """팝업 단건 (schema: display-popups / display-popups-ids-popupIds[])."""

    popup_no: int | None = None
    popup_id: str | None = None
    mall_no: int | None = None
    title: str | None = None
    label: str | None = None
    content: str | None = None
    type: str | None = None
    popup_design_type: str | None = None
    popup_position: str | None = None
    display_types: str | None = None
    visible_today: bool | None = None
    width: int | None = None
    height: int | None = None
    start_ymdt: KstDatetime | None = None
    end_ymdt: KstDatetime | None = None
    page_infos: PopupPageInfos | None = None
    detail_info: PopupDetailInfo | None = None
    popup_slide_info: PopupSlideInfo | None = None


class DesignPopupRequest(BaseDto):
    """디자인 팝업 조회 요청 (schema: design-popups-868683164)."""

    popup_id: str | None = Field(None, description="팝업 ID")
    display_url: str | None = Field(None, description="노출 URL")
    parameter: str | None = Field(None, description="URL 파라미터")


class DesignPopup(BaseDto):
    """디자인 팝업 (schema: design-popups415225285[])."""

    popup_no: int | None = None
    popup_id: str | None = None
    mall_no: int | None = None
    title: str | None = None
    content: str | None = None
    popup_design_type: str | None = None
    visible_today: bool | None = None
    detail_info: PopupDetailInfo | None = None
    popup_slide_info: PopupSlideInfo | None = None

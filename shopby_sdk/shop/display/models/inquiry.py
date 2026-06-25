"""상품 문의(ProductInquiry) 모델."""

from __future__ import annotations

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime
from shopby_sdk.shop.display.models.common import TagValue


class InquirySummary(BaseDto):
    """전체 상품문의 목록 항목 (schema: products-inquiries items[])."""

    inquiry_no: int | None = None
    type: str | None = None
    title: str | None = None
    content: str | None = None
    product_no: int | None = None
    product_name: str | None = None
    order_no: str | None = None
    member_id: str | None = None
    register_no: int | None = None
    register_name: str | None = None
    provider_type: str | None = None
    display_status_type: str | None = None
    image_url: str | None = None
    tag_value_nos: list[int] | None = None
    replied: bool | None = None
    secreted: bool | None = None
    my_inquiry: bool | None = None
    administrator: bool | None = None
    deleted: bool | None = None
    modifiable: bool | None = None
    register_ymdt: KstDatetime | None = None


class InquiriesResponse(BaseDto):
    """전체 상품문의 목록 응답 (schema: products-inquiries)."""

    total_count: int | None = None
    items: list[InquirySummary] | None = None


class InquiryAnswer(BaseDto):
    """상품문의 답변."""

    inquiry_no: int | None = None
    title: str | None = None
    content: str | None = None
    member_id: str | None = None
    nick_name: str | None = None
    partner_name: str | None = None
    admin_type: str | None = None
    administrator: bool | None = None
    secreted: bool | None = None
    register_ymdt: KstDatetime | None = None
    update_ymdt: KstDatetime | None = None


class InquiryImageUrlInfo(BaseDto):
    url: str | None = None
    image_url_type: str | None = None
    is_main: bool | None = None


class ProductInquiry(BaseDto):
    """상품문의 단건 (schema: products-productNo-inquiries items[] / 단건)."""

    inquiry_no: int | None = None
    type: str | None = None
    title: str | None = None
    content: str | None = None
    product_no: int | None = None
    product_name: str | None = None
    product_name_en: str | None = None
    product_management_cd: str | None = None
    order_no: str | None = None
    member_id: str | None = None
    register_no: int | None = None
    register_name: str | None = None
    nick_name: str | None = None
    grade_label: str | None = None
    brand_name: str | None = None
    brand_name_en: str | None = None
    provider_type: str | None = None
    display_status_type: str | None = None
    cancel_reportable: str | None = None
    image_url: str | None = None
    image_url_info: InquiryImageUrlInfo | None = None
    tag_value_nos: list[int] | None = None
    replied: bool | None = None
    secreted: bool | None = None
    my_inquiry: bool | None = None
    administrator: bool | None = None
    modifiable: bool | None = None
    blocked: bool | None = None
    expelled: bool | None = None
    answers: list[InquiryAnswer] | None = None
    register_ymdt: KstDatetime | None = None
    update_ymdt: KstDatetime | None = None


class ProductInquiriesResponse(BaseDto):
    """상품문의 목록 응답 (schema: products-productNo-inquiries)."""

    total_count: int | None = None
    items: list[ProductInquiry] | None = None


class InquiryConfigurations(BaseDto):
    """상품문의 게시판 설정 (schema: products-inquiries-configurations)."""

    name: str | None = None
    description: str | None = None
    board_type: str | None = None
    board_image_type: str | None = None
    board_usable: bool | None = None
    member_writeable: bool | None = None
    guest_writeable: bool | None = None
    secret_usable: bool | None = None
    can_attach: bool | None = None
    can_reply: bool | None = None


class InquiryTag(BaseDto):
    """상품문의 태그 (schema: products-inquiries-tags inquiryTags[])."""

    inquiry_tag_no: int | None = None
    inquiry_tag_name: str | None = None
    inquiry_tag_values: list[TagValue] | None = None


class InquiryTagsResponse(BaseDto):
    """상품문의 태그 전체 응답 (schema: products-inquiries-tags)."""

    inquiry_tags: list[InquiryTag] | None = None

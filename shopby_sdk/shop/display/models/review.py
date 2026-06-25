"""상품평(Review) 모델."""

from __future__ import annotations

from pydantic import Field

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.base.kst import KstDatetime
from shopby_sdk.shop.display.models.common import MemberDisplayInfo, TagValue


class ReviewOrderedOptionInput(BaseDto):
    input_label: str | None = None
    input_value: str | None = None


class ReviewOrderedOption(BaseDto):
    """상품평 주문 옵션 정보."""

    order_option_no: int | None = None
    option_name: str | None = None
    option_value: str | None = None
    option_title: str | None = None
    option_type: str | None = None
    option_used: bool | None = None
    add_price: int | None = None
    order_cnt: int | None = None
    order_status_type: str | None = None
    inputs: list[ReviewOrderedOptionInput] | None = None


class ProductReview(BaseDto):
    """상품평 단건 (category/product 상품평 목록·단건 공통)."""

    review_no: int | None = None
    rate: int | None = None
    content: str | None = None
    product_no: int | None = None
    product_name: str | None = None
    product_name_en: str | None = None
    product_total_count: int | None = None
    product_rate: int | None = None
    product_discount_price: int | None = None
    product_detail_url: str | None = None
    brand_name: str | None = None
    brand_name_en: str | None = None
    member_id: str | None = None
    member_name: str | None = None
    nickname: str | None = None
    register_no: int | None = None
    register_name: str | None = None
    provider_type: str | None = None
    platform_type: str | None = None
    site_name: str | None = None
    image_url: str | None = None
    image_url_type: str | None = None
    file_urls: list[str] | None = None
    extra_json: str | None = None
    best_review_yn: str | None = None
    sale_status_type: str | None = None
    cancel_reportable: str | None = None
    given_accumulation_yn: str | None = None
    recommend_cnt: int | None = None
    report_cnt: int | None = None
    blind_report_cnt: int | None = None
    comment_count: int | None = None
    recommendable: bool | None = None
    reportable: bool | None = None
    my_review: bool | None = None
    expelled: bool | None = None
    external_review: bool | None = None
    is_deleted_product_review: bool | None = None
    tag_value_nos: list[int] | None = None
    tag_values: list[TagValue] | None = None
    member_grade_display_info: MemberDisplayInfo | None = None
    member_group_display_info: MemberDisplayInfo | None = None
    ordered_option: ReviewOrderedOption | None = None
    register_ymdt: KstDatetime | None = None
    update_ymdt: KstDatetime | None = None
    origin_register_ymdt: KstDatetime | None = None


class ReviewRatingCount(BaseDto):
    rating: int | None = None
    count_of_rating: int | None = None


class CategoryProductReviewsResponse(BaseDto):
    """카테고리 상품평 목록 응답 (schema: category-product-reviews)."""

    total_count: int | None = None
    rate: float | None = None
    items: list[ProductReview] | None = None
    review_rating_responses: list[ReviewRatingCount] | None = None


class ProductReviewsResponse(BaseDto):
    """상품평 목록 응답 v2 (schema: products-productNo-product-reviews)."""

    total_count: int | None = None
    rate: float | None = None
    items: list[ProductReview] | None = None
    review_rating_responses: list[ReviewRatingCount] | None = None


class PhotoReview(BaseDto):
    """포토 후기 단건 (schema: products-productNo-photo-reviews contents[])."""

    review_no: int | None = None
    register_no: int | None = None
    recommend_cnt: int | None = None
    attached_file_count: int | None = None
    urls: list[str] | None = None
    tag_value_nos: list[int] | None = None


class PhotoReviewsResponse(BaseDto):
    """상품 포토 후기 목록 응답 (schema: products-productNo-photo-reviews)."""

    contents: list[PhotoReview] | None = None
    total_page: int | None = None
    total_count: int | None = None


class ReviewComment(BaseDto):
    """상품평 댓글 단건 (schema: products-productNo-product-reviews-reviewNo-comments contents[])."""

    comment_no: int | None = None
    content: str | None = None
    register_no: int | None = None
    is_admin: bool | None = None
    register_ymdt: KstDatetime | None = None
    modify_ydmt: KstDatetime | None = None


class ReviewCommentsResponse(BaseDto):
    """상품평 댓글 목록 응답."""

    contents: list[ReviewComment] | None = None
    total_page: int | None = None
    total_count: int | None = None


class ReviewWidgetConfig(BaseDto):
    product_review_widget_usable: bool | None = None
    product_review_widget_page_count: int | None = None
    photo_review_widget_usable: bool | None = None
    photo_review_widget_page_count: int | None = None
    all_review_widget_usable: bool | None = None
    all_review_widget_page_count: int | None = None


class ExpandedReviewConfig(BaseDto):
    use_review_recommend: bool | None = None
    use_gathering_photo_review: bool | None = None
    photo_review_display_type: str | None = None
    photo_review_cnt_per_page: int | None = None
    product_review_cnt_per_page: int | None = None
    all_review_cnt_per_page: int | None = None
    review_reward_notice_text: str | None = None
    accumulation_reward_notice_text: str | None = None
    writing_review_notice_text: str | None = None
    no_photo_review_text: str | None = None
    widget_config: ReviewWidgetConfig | None = None


class ReviewAccumulationInfo(BaseDto):
    use_yn: str | None = None
    reviews_accumulation: int | None = None
    reviews_length: int | None = None
    photo_reviews_accumulation: int | None = None
    photo_reviews_length: int | None = None


class ReviewConfigurations(BaseDto):
    """상품평 게시판 설정 (schema: product-reviews-configurations)."""

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
    can_comment: bool | None = None
    expanded_review_config: ExpandedReviewConfig | None = None
    review_accumulation_info: ReviewAccumulationInfo | None = None


class ReviewBoardProductInfo(BaseDto):
    no: int | None = None
    name: str | None = None
    product_name_en: str | None = None
    thumbnail_image: str | None = None
    thumbnail_image_url_type: str | None = None
    total_review_count: int | None = None


class ReviewBoardRegister(BaseDto):
    no: int | None = None
    name: str | None = None


class ReviewBoardItem(BaseDto):
    """상품평 게시판 항목 (schema: reviews-boards items[])."""

    review_no: int | None = None
    content: str | None = None
    review_rate: int | None = None
    is_best_review: bool | None = None
    images: list[str] | None = None
    tag_value_nos: list[int] | None = None
    product_info: ReviewBoardProductInfo | None = None
    register_info: ReviewBoardRegister | None = Field(None, alias="register")


class ReviewBoardResponse(BaseDto):
    """상품평 게시판 목록 응답 (schema: reviews-boards)."""

    total_count: int | None = None
    items: list[ReviewBoardItem] | None = None


class ReviewedProductReview(BaseDto):
    review_no: int | None = None
    content: str | None = None
    attached_image: str | None = None
    is_best_review: bool | None = None


class ReviewedProductItem(BaseDto):
    """상품 기준 상품평 게시판 항목 (schema: reviews-boards-reviewed-products items[])."""

    product_no: int | None = None
    product_name: str | None = None
    product_name_en: str | None = None
    main_image: str | None = None
    main_image_url_type: str | None = None
    sale_price: int | None = None
    applied_immediate_discount_price: int | None = None
    review_rate: float | None = None
    total_review_count: int | None = None
    reviews: list[ReviewedProductReview] | None = None


class ReviewedProductsResponse(BaseDto):
    """상품 기준 상품평 게시판 목록 응답 (schema: reviews-boards-reviewed-products)."""

    total_count: int | None = None
    items: list[ReviewedProductItem] | None = None


class ReviewTag(BaseDto):
    """상품리뷰 태그 (schema: reviews-tags reviewTags[])."""

    review_tag_no: int | None = None
    review_tag_name: str | None = None
    review_tag_values: list[TagValue] | None = None


class ReviewTagsResponse(BaseDto):
    """상품리뷰 태그 전체 응답 (schema: reviews-tags)."""

    review_tags: list[ReviewTag] | None = None

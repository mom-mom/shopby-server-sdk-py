"""상품 옵션(Option) 관련 모델.

대응 OpenAPI schema:
- products-options-279656068 (옵션 목록 - 상품번호 리스트)
- products-productNo-options676330184 (단일 상품 옵션)
- products-productNo-options-images-1053841668 (상품 옵션 이미지 목록)
- products-productNo-options-optionNo-images-589532874 (옵션 이미지)
"""

from typing import Literal

from shopby_sdk.base.dto import BaseDto
from shopby_sdk.shop.product.models.catalog_item import RentalInfo

OptionSaleType = Literal["AVAILABLE", "SOLD_OUT", "UNAVAILABLE"]
OptionSelectType = Literal["MULTI", "FLAT"]
OptionType = Literal["STANDARD", "COMBINATION", "DEFAULT", "MAPPING", "REQUIRED"]


class OptionImage(BaseDto):
    """옵션 이미지(main 여부 + url)."""

    main: bool | None = None
    url: str | None = None


class OptionValue(BaseDto):
    """옵션 값 (조합형/단독형 공통).

    children 는 다단계 옵션의 하위 옵션 목록으로 동일 구조가 재귀된다.
    """

    option_no: int | None = None
    label: str | None = None
    value: str | None = None
    sale_type: OptionSaleType | None = None
    main: bool | None = None
    is_required_option: bool | None = None
    add_price: int | None = None
    buy_price: int | None = None
    stock_cnt: int | None = None
    sale_cnt: int | None = None
    reservation_stock_cnt: int | None = None
    forced_sold_out: bool | None = None
    option_management_cd: str | None = None
    extra_management_cd: str | None = None
    images: list[OptionImage] | None = None
    rental_info: list[RentalInfo] | None = None
    children: list["OptionValue"] | None = None


class OptionInput(BaseDto):
    """구매자 작성형 옵션(입력)."""

    input_no: int | None = None
    input_label: str | None = None
    input_matching_type: Literal["OPTION", "PRODUCT", "AMOUNT"] | None = None
    required: bool | None = None


class MultiLevelOption(BaseDto):
    """다단계(분리형) 옵션 노드."""

    label: str | None = None
    value: str | None = None
    is_required_option: bool | None = None
    children: list[OptionValue] | None = None


class ProductOptionsResponse(BaseDto):
    """단일 상품 옵션 조회 응답.

    OpenAPI: products-productNo-options676330184
    """

    type: OptionType | None = None
    select_type: OptionSelectType | None = None
    is_required_option: bool | None = None
    product_sale_price: int | None = None
    immediate_discount_amt: int | None = None
    displayable_stock: bool | None = None
    labels: list[str] | None = None
    flat_options: list[OptionValue] | None = None
    multi_level_options: list[MultiLevelOption] | None = None
    inputs: list[OptionInput] | None = None


class ProductOptionInfo(BaseDto):
    """옵션 목록 조회 시 상품별 옵션 정보.

    OpenAPI: products-options-279656068 optionInfos[]
    """

    mall_product_no: int | None = None
    displayable_stock: bool | None = None
    options: list[OptionValue] | None = None


class ProductsOptionsResponse(BaseDto):
    """옵션 목록 조회 응답 (상품번호 리스트).

    OpenAPI: products-options-279656068
    """

    option_infos: list[ProductOptionInfo] | None = None


class OptionImageItem(BaseDto):
    """옵션 이미지 항목.

    OpenAPI: products-productNo-options-images-1053841668 item
    및 products-productNo-options-optionNo-images-589532874 item
    """

    option_no: int | None = None
    image_url: str | None = None
    main: bool | None = None
    soldout: bool | None = None

"""Marketing(마케팅) shop API 응답/요청 모델.

OpenAPI: docs/api/marketing-shop-public.yml
"""

from typing import Literal

from pydantic import Field

from shopby_sdk.base.dto import BaseDto

SnsShareImageType = Literal["PRODUCT_IMAGE", "REPRESENTATIVE_IMAGE"]
"""SNS 공유 이미지 설정.

- PRODUCT_IMAGE: 상품 이미지
- REPRESENTATIVE_IMAGE: 대표 이미지
"""


class TwitterShare(BaseDto):
    """SNS 공유 설정 - 트위터."""

    used: bool | None = Field(None, description="트위터 공유하기 설정 여부")
    share_message: str | None = Field(None, description="트위터 - 공유 메세지")
    url: str | None = Field(None, description="트위터 - 상품 상세 페이지 url")


class KakaoButton(BaseDto):
    """카카오 공유 - 버튼."""

    title: str | None = Field(None, description="카카오 - 버튼 텍스트")
    link: str | None = Field(None, description="카카오 - 버튼 링크")


class KakaoCommerce(BaseDto):
    """카카오 공유 - 커머스(가격) 정보."""

    regular_price: float | None = Field(None, description="카카오 - 상품판매가")
    discount_price: float | None = Field(
        None, description="카카오 - 상품 즉시할인가 (=판매가 - 즉시할인)"
    )
    discount_rate: float | None = Field(
        None,
        description="카카오 - 즉시할인 할인율 (fixedDiscountPrice와 동시 사용 불가)",
    )
    fixed_discount_price: float | None = Field(
        None,
        description="카카오 - 즉시할인 정액할인 (discountRate와 동시 사용 불가)",
    )


class KakaoContent(BaseDto):
    """카카오 공유 - 콘텐츠."""

    title: str | None = Field(None, description="카카오 - 콘텐츠 제목")
    image_url: str | None = Field(
        None, description="카카오 - 콘텐츠 이미지 URL (대표 이미지 or 상품 대표 이미지 url)"
    )


class KakaoShare(BaseDto):
    """SNS 공유 설정 - 카카오."""

    used: bool | None = Field(None, description="카카오 공유하기 설정 여부")
    kakao_script_key: str | None = Field(None, description="카카오 개발자센터 script key")
    content: KakaoContent | None = Field(None, description="카카오 - 콘텐츠")
    commerce: KakaoCommerce | None = Field(None, description="카카오 - 커머스(가격) 정보")
    buttons: list[KakaoButton] | None = Field(None, description="카카오 - 버튼 목록")


class KakaoStoryUrlInfo(BaseDto):
    """카카오스토리 - 웹 페이지 URL 정보."""

    title: str | None = Field(None, description="카카오스토리 - 웹 페이지 타이틀")
    description: str | None = Field(None, description="카카오스토리 - 웹 페이지 설명")
    image: list[str] | None = Field(
        None, description="카카오스토리 - 웹 페이지 대표 이미지 URL 목록"
    )


class KakaoStoryShare(BaseDto):
    """SNS 공유 설정 - 카카오스토리."""

    used: bool | None = Field(None, description="카카오스토리 공유하기 설정 여부")
    url: str | None = Field(None, description="카카오스토리 - 공유할 웹 페이지 URL")
    text: str | None = Field(
        None, description="카카오스토리 - 공유하기 웹뷰에 자동으로 입력될 본문 내용"
    )
    url_info: KakaoStoryUrlInfo | None = Field(
        None, description="카카오스토리 - 웹 페이지 URL 정보"
    )


class FacebookShare(BaseDto):
    """SNS 공유 설정 - 페이스북."""

    used: bool | None = Field(None, description="페이스북 공유하기 설정 여부")
    link_title: str | None = Field(None, description="페이스북 - 링크 타이틀")
    link_summary: str | None = Field(None, description="페이스북 - 링크 요약")
    image: str | None = Field(
        None, description="페이스북 - 대표이미지 혹은 상품 대표 이미지"
    )


class SnsShareResponse(BaseDto):
    """SNS 공유 설정 조회 응답.

    OpenAPI schema: marketing-sns-share-1363380301
    """

    sns_share_used: bool | None = Field(None, description="SNS 공유하기 설정 여부")
    product_url_copy_used: bool | None = Field(
        None,
        description="상품 URL 복사 사용 설정 (사용함일 경우 상품 url 복사 버튼 노출)",
    )
    representative_image: str | None = Field(None, description="대표 이미지")
    representative_title: str | None = Field(None, description="대표 제목")
    representative_description: str | None = Field(None, description="대표 설명")
    sns_share_image_type: SnsShareImageType | None = Field(
        None, description="이미지 설정"
    )
    kakao: KakaoShare | None = Field(None, description="카카오 공유 설정")
    kakao_story: KakaoStoryShare | None = Field(None, description="카카오스토리 공유 설정")
    facebook: FacebookShare | None = Field(None, description="페이스북 공유 설정")
    twitter: TwitterShare | None = Field(None, description="트위터 공유 설정")

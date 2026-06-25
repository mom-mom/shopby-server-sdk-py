"""display shop API 공통 모델."""

from __future__ import annotations

from shopby_sdk.base.dto import BaseDto


class TagValue(BaseDto):
    """태그 값 (리뷰/문의 태그 공통)."""

    tag_value_no: int | None = None
    tag_value_name: str | None = None


class MemberDisplayInfo(BaseDto):
    """회원 등급/그룹 노출 정보."""

    is_all: bool | None = None
    nos: list[int] | None = None

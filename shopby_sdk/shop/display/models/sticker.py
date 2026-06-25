"""스티커(Sticker) 모델."""

from __future__ import annotations

from shopby_sdk.base.dto import BaseDto


class Sticker(BaseDto):
    """스티커 단건 (schema: stickers-1965548140[])."""

    sticker_no: int | None = None
    sticker_name: str | None = None
    sticker_type: str | None = None
    content: str | None = None
    display_order: int | None = None
    product_count: int | None = None
    use_yn: str | None = None

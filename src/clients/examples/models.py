from pydantic import Field

from src.base.dto import BaseDto


class SomeComplexReqDto(BaseDto):
    some_field: int = Field(..., title="무슨 필드", examples=[[1, 2, 3]])
    some_other_field: str = Field(..., title="무슨무슨 필드", examples=[["example"]])


class SomeExampleModel(BaseDto):
    some_field: int = Field(..., title="무슨 필드", examples=[[100]])

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseDto(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        validate_by_name=True,
        validate_by_alias=True,
        from_attributes=True,
        # 스펙에 아직 반영 안 된 신규 응답 필드를 조용히 버리지 않고 보존(forward-compat).
        extra="allow",
    )

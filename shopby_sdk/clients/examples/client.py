# this is not actual api
# just example
import httpx

from shopby_sdk.clients.base import ShopbyServerApiClient
from shopby_sdk.clients.examples.models import SomeExampleModel, SomeComplexReqDto


class ShopbyServerExampleApiClient(ShopbyServerApiClient):
    async def get_example(self, some_simple_param: int) -> SomeExampleModel:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/example", headers={"some-extra-header": "some-extra-value"}, params={"someParam": some_simple_param}
            )

            return SomeExampleModel.model_validate(resp.json())

    async def get_example_complex(self, some_complex_param: SomeComplexReqDto) -> SomeExampleModel:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.common_header) as client:
            resp = await client.get(
                "/example",
                headers={"some-extra-header": "some-extra-value"},
                params={**some_complex_param.model_dump()},
            )

            return SomeExampleModel.model_validate(resp.json())

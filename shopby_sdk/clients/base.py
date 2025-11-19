class ShopbyServerApiClient:
    def __init__(self, server_access_token: str, server_system_key: str):
        self._access_token = server_access_token
        self._system_key = server_system_key
        self.base_url = "https://server-api.e-ncp.com"

    @property
    def common_header(self):
        return {
            "Authorization": f"Bearer {self._access_token}",
            "systemKey": self._system_key,
            "version": "1.0",
        }

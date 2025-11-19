import os
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    애플리케이션 설정

    환경 변수 ENV를 통해 dev/prod 환경 선택 (기본값: dev)
    설정 파일: .dev.env 또는 .prod.env
    """

    model_config = SettingsConfigDict(
        env_file=f".{os.getenv('ENV', 'dev')}.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # 환경 설정
    env: Literal["dev", "prod"] = Field(default="dev", description="실행 환경")

    # Shopby API 설정
    shopby_server_access_token: str = Field(..., description="Shopby 서버 액세스 토큰")
    shopby_server_system_key: str = Field(..., description="Shopby 서버 시스템 키")
    shopby_base_url: str = Field(default="https://server-api.e-ncp.com", description="Shopby API 베이스 URL")


@lru_cache
def get_settings() -> Settings:
    """
    설정 인스턴스 반환 (싱글톤)

    사용 예:
        from shopby_sdk.config import get_settings

        settings = get_settings()
        client = ShopbyServerProductsApiClient(
            server_access_token=settings.shopby_server_access_token,
            server_system_key=settings.shopby_server_system_key,
        )
    """
    return Settings()

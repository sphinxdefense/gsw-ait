from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """See https://docs.pydantic.dev/usage/settings/"""

    class Config:
        env_file = ".env"
        env_prefix = "GSW_API_"
        case_sensitive = False

from pydantic_settings import BaseSettings


class BaseAppSettings:
    class Config:
        extra = "ignore"

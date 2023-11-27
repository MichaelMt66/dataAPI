from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER_NAME: str
    PASSWORD: str
    HOST: str
    DATABASE: str



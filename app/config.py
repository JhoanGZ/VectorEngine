from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    OPENAI_API_KEY: str 
    LLM_PROVIDER: str

    class Config:
        env_file = ".env"

settings = Settings()


from pydantic import BaseModel,PostgresDsn,computed_field
from pydantic_settings import BaseSettings,SettingsConfigDict
from urllib.parse import quote_plus
from datetime import timedelta
from pydantic import AnyUrl

class RunConfig(BaseModel):
    host:str = "localhost"
    port:int = 9898

class Logger(BaseModel):
    level:str = "INFO"
    name:str = "APP"

class ApiPrefix(BaseModel):
    prefix:str = "/api"

class DatabaseConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = ""
    name: str = "postgres"
    echo: bool = False
    echo_pool: bool = False  
    pool_size: int = 50      
    max_overflow: int = 10  

    @computed_field
    @property
    def url(self)->PostgresDsn:
        escaped_user=quote_plus(self.user)
        escaped_password=quote_plus(self.password)
        return f"postgresql+asyncpg://{escaped_user}:{escaped_password}@{self.host}:{self.port}/{self.name}"

class MinioConfig(BaseModel):
    host:str = "localhost"
    port:int = 9990
    access_key: str = "minioadmin"
    secret_key: str = "minioadmin"
    secure: bool = False
    bucket_name: str = "default"
    health_check_path: str = "/minio/health/live"

    @computed_field
    @property
    def endpoint(self) -> AnyUrl:
        return f"{self.host}:{self.port}"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__",
        extra = "ignore"
    )
    run:RunConfig = RunConfig()
    logger:Logger = Logger()
    api:ApiPrefix = ApiPrefix()
    db:DatabaseConfig
    minio: MinioConfig = MinioConfig()
    
settings = Settings()
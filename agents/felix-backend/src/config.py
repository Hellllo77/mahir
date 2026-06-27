from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    database_url: str = "postgresql+asyncpg://mahir:mahir@localhost:5432/mahir"
    database_url_sync: str = "postgresql://mahir:mahir@localhost:5432/mahir"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 8  # 8 hours

    # OIDC (corporate SSO)
    oidc_issuer: str = ""
    oidc_client_id: str = ""
    oidc_client_secret: str = ""
    oidc_redirect_uri: str = "http://localhost:8000/v1/auth/oidc/callback"

    # OpenRouter / LLM judge
    openrouter_api_key: str = ""
    judge_model_default: str = "anthropic/claude-sonnet-4-6"
    judge_model_escalation: str = "anthropic/claude-opus-4-8"
    judge_model_prefilter: str = "anthropic/claude-haiku-4-5"
    judge_use_batches_api: bool = False  # enable for non-latency-sensitive bulk grading
    judge_escalation_threshold: float = 0.6  # escalate to Opus when confidence falls below this

    # Object store (S3-compatible)
    s3_endpoint_url: str = ""
    s3_bucket: str = "mahir-artifacts"
    s3_access_key_id: str = ""
    s3_secret_access_key: str = ""
    s3_region: str = "ap-southeast-1"

    # Individual-first: auto-assign users to this curriculum on first login.
    # If empty, the first published curriculum in the DB is used.
    default_curriculum_id: str = ""

    # App
    app_env: str = "development"
    log_level: str = "INFO"
    api_v1_prefix: str = "/v1"
    cors_origins: str = "http://localhost:3000"
    frontend_url: str = "http://localhost:3000"


settings = Settings()

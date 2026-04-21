from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DEV_MODE: bool = True
    FRONTEND_URL: str = "http://localhost:3000"
    PORT: int = 8000

    OPENAI_API_KEY: str = ""
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIM: int = 1536

    GOOGLE_AI_API_KEY: str = ""
    GEMINI_CHAT_MODEL: str = "gemini-1.5-flash"

    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "legalsaathi"

    MONGODB_URI: str = "mongodb://admin:admin@localhost:27017"
    MONGODB_DB: str = "legalsaathi"

    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "legal_docs"

    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = ""

    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "ap-south-1"
    AWS_S3_BUCKET: str = "legalsaathi-docs"

    CLERK_SECRET_KEY: str = ""
    CLERK_PEM_PUBLIC_KEY: str = ""


settings = Settings()

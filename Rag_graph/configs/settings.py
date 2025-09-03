
import os
from typing import Any, List, Optional, TYPE_CHECKING
from pydantic import Field, field_validator

# Provide a stable base class alias for Settings so static checkers don't complain.
# Use TYPE_CHECKING and deterministic imports to help Pylance/pyright.
if TYPE_CHECKING:
    # For type checkers, prefer the real BaseSettings if available
    try:
        from pydantic_settings import BaseSettings as BaseSettingsType  # type: ignore
    except Exception:
        from pydantic import BaseModel as BaseSettingsType  # type: ignore
else:
    # At runtime, try to use pydantic_settings.BaseSettings; fall back to pydantic.BaseModel
    try:
        from pydantic_settings import BaseSettings as BaseSettingsType
    except Exception:
        from pydantic import BaseModel as BaseSettingsType

# Avoid importing ChatGoogleGenerativeAI at module import time to reduce
# IDE/static analysis warnings. Import lazily in __init__.
if TYPE_CHECKING:
    # For type checkers only
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
    except Exception:
        ChatGoogleGenerativeAI = Any  # type: ignore

class Settings(BaseSettingsType):  # type: ignore
    """
    Application settings and configuration.
    Values will be loaded from environment variables, with defaults provided.
    """
    
    LLM_MODEL_NAME: str = Field("gemini-2.0-flash", description="Name of the LLM model to use")
    EMBEDDING_MODEL_NAME: str = Field("models/embedding-001", description="Name of the embedding model to use")
    LLM_TEMPERATURE: float = Field(0.7, description="Temperature setting for the LLM model")
    LLM_MAX_TOKENS: int = Field(4000, description="Maximum number of tokens for LLM responses")
    
    MEMORY_DB_CONNECTION_STRING: str = Field(
        "postgresql://postgres:postgres@localhost:5432/memory_db",
        description="Connection string for memory database"
    )
    MEMORY_DB_POOL_SIZE: int = Field(5, description="Database connection pool size")
    
    EXTERNAL_SERVICES_ENDPOINTS: List[str] = Field(
        default_factory=lambda: ["https://api-service1.example.com", "https://api-service2.example.com"],
        description="List of external service endpoints"
    )
    
    LLM: Optional[Any] = None  # Langchain LLM instance
    # Safety switch: only initialize real Google LLM when explicitly enabled
    USE_GOOGLE_LLM: bool = Field(False, description="Set true to enable real Google Gemini LLM at runtime")
    # (no structured_output toggle present) Keep settings minimal

    ENVIRONMENT: str = Field("development", description="Application environment (development, testing, production)")
    DEBUG: bool = Field(True, description="Debug mode flag")

    # Controls for iterative behaviors
    MAX_REWRITE: int = Field(2, description="Maximum number of query rewrites (used by grade_node)")
    MAX_REEVALS: int = Field(1, description="Maximum number of answer re-evaluations after LLM response")

    OPENAI_API_KEY: Optional[str] = Field(None, description="OpenAI API key")
    ANTHROPIC_API_KEY: Optional[str] = Field(None, description="Anthropic API key")
    GOOGLE_API_KEY: Optional[str] = Field(None, description="Google API key")
    
    @field_validator("EXTERNAL_SERVICES_ENDPOINTS", mode='before')  # Changed to field_validator
    @classmethod  
    def parse_endpoints(cls, v):
        """Parse endpoints from string if provided as comma-separated values in env var."""
        if isinstance(v, str):
            return [endpoint.strip() for endpoint in v.split(",")]
        return v
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize Gemini LLM instance only when explicitly enabled and
        # credentials are present. This avoids accidental external API calls
        # during tests or local runs when a key may exist in `.env`.
        self.LLM = None
        try:
            enabled = bool(getattr(self, "USE_GOOGLE_LLM", False))
        except Exception:
            enabled = False
        if enabled:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI

                google_api_key = getattr(self, "GOOGLE_API_KEY", None)
                adc_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
                if google_api_key or adc_path:
                    self.LLM = ChatGoogleGenerativeAI(
                        model=self.LLM_MODEL_NAME,
                        google_api_key=google_api_key,
                    )
            except Exception:
                # Package not available or init failed; leave LLM as None
                self.LLM = None

    # Load environment variables from `.env` by default so runtime settings
    # (like `GOOGLE_API_KEY`) are applied automatically. If you prefer to
    # manage environment variables outside of a file, change this to None.
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

settings = Settings()
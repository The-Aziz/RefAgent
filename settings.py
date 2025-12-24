from typing import Optional
try:
    from pydantic_settings import BaseSettings
except Exception:
    # Fallback for environments with pydantic v1 or where pydantic-settings isn't installed
    try:
        from pydantic import BaseSettings
    except Exception:
        raise ImportError("pydantic or pydantic-settings is required for Settings. Install pydantic>=1.10 or pydantic-settings.")


class Settings(BaseSettings):
    API_KEY: str = ""
    GROQ_API_KEY: str = ""
    GITHUB_API_KEY: str = ""
    MODEL_NAME: str = "gpt-4"

    # LLM Provider: 'openai' or 'groq' (recommended for cost savings)
    LLM_PROVIDER: str = 'groq'
    
    # Groq model options: 'mixtral-8x7b-32768', 'llama-3.1-8b-instant', 'llama-3.1-70b-versatile', 'gemma-7b-it'
    GROQ_MODEL: str = 'llama-3.1-8b-instant'

    # Per-agent token limits (defaults can be overridden via .env)
    # Reduced for llama-3.1-8b to maximize RPM
    DEFAULT_MAX_TOKENS: int = 8192
    REFRACTORING_GENERATOR_MAX_TOKENS: int = 8192
    PLANNER_MAX_TOKENS: int = 4096
    COMPILER_MAX_TOKENS: int = 4096
    TEST_MAX_TOKENS: int = 4096

    # Detector configuration: which external tool to use to pick god classes
    # Supported values: 'pmd', 'deodorant', 'findbugs', 'heuristic'
    DETECTOR_TOOL: str = 'heuristic'
    PMD_PATH: Optional[str] = None
    DEODORANT_PATH: Optional[str] = None
    DETECTOR_TOP_N: int = 5

    class Config:
        env_file = ".env"

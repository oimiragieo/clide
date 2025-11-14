"""Configuration management for Clide."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Config:
    """Configuration manager for Clide."""

    def __init__(self):
        """Initialize configuration from environment variables and defaults."""
        self.db_path = os.getenv("CLIDE_DB", "memory_bank.db")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.default_agent = os.getenv("CLIDE_AGENT", "claude")
        self.dashboard_host = os.getenv("CLIDE_DASHBOARD_HOST", "127.0.0.1")
        self.dashboard_port = int(os.getenv("CLIDE_DASHBOARD_PORT", "5000"))
        self.verbose = os.getenv("CLIDE_VERBOSE", "false").lower() == "true"
        self.log_level = os.getenv("CLIDE_LOG_LEVEL", "INFO")

    @property
    def db_exists(self) -> bool:
        """Check if database file exists."""
        return Path(self.db_path).exists()

    def get_api_key(self, provider: Optional[str] = None) -> str:
        """Get API key for specified provider or default."""
        if provider == "anthropic" or self.default_agent == "claude":
            return self.anthropic_api_key
        elif provider == "openai" or self.default_agent == "gpt":
            return self.openai_api_key
        return ""

    def validate(self) -> tuple[bool, list[str]]:
        """Validate configuration and return (is_valid, errors)."""
        errors = []

        if not self.db_exists:
            errors.append(f"Database not found at '{self.db_path}'. Run 'clide init' to create it.")

        if not self.anthropic_api_key and not self.openai_api_key:
            errors.append(
                "No AI API key configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY "
                "environment variable."
            )

        return len(errors) == 0, errors


# Global config instance
config = Config()

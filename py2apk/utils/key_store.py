import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class APIKeyManager:
    """Manages secure storage and retrieval of API keys."""
    
    @staticmethod
    def get_api_key(env_var: str = "AI_API_KEY") -> Optional[str]:
        """Retrieve API key from environment variables."""
        try:
            return os.getenv(env_var)
        except Exception as e:
            logger.error(f"Failed to retrieve API key: {e}")
            return None

import shutil
import logging

logger = logging.getLogger(__name__)

class SystemValidator:
    REQUIRED_COMMANDS = ["gradle", "apksigner", "adb"]
    
    def validate_environment(self) -> bool:
        """Check if required system tools are installed."""
        missing = [cmd for cmd in self.REQUIRED_COMMANDS if not shutil.which(cmd)]
        if missing:
            logger.error(f"Missing required system tools: {', '.join(missing)}")
            return False
        return True

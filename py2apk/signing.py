import subprocess
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class APKSigner:
    """Handles APK signing using apksigner."""
    
    def sign_apk(self, apk_file: Path, keystore_path: Path, keystore_pass: str, key_alias: str, key_pass: str):
        """Sign APK using apksigner."""
        try:
            subprocess.run([
                "apksigner", "sign",
                "--ks", str(keystore_path),
                "--ks-pass", f"pass:{keystore_pass}",
                "--key-pass", f"pass:{key_pass}",
                str(apk_file)
            ], check=True)
            logger.info("APK signed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"APK signing failed: {e}")
            return False

"""Configuration settings and constants"""
from pathlib import Path
import os

# Default configuration values
DEFAULT_CONFIG = {
    "ANDROID_SDK_PATHS": [
        os.getenv("ANDROID_HOME"),
        str(Path.home() / "Android/Sdk"),
        "/usr/local/android-sdk",
        "C:\\Program Files\\Android\\Android Studio\\Sdk"
    ],
    "REQUIRED_PYTHON_PACKAGES": [
        "chaquopy",
        "numpy",
        "onnxruntime"
    ],
    "MAX_APK_SIZE_MB": 150,
    "GRADLE_VERSION": "7.4",
    "PYTHON_VERSION": "3.8"
}

def find_android_sdk() -> Path:
    """
    Locate Android SDK installation
    
    Returns:
        Path: Path to Android SDK directory
    Raises:
        FileNotFoundError: If SDK not found
    """
    for path in DEFAULT_CONFIG["ANDROID_SDK_PATHS"]:
        if path and Path(path).exists():
            return Path(path)
    raise FileNotFoundError("Android SDK not found. Install Android Studio first.")

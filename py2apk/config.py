import yaml
from pathlib import Path

DEFAULT_CONFIG = {
    "package_name": "com.example.py2apk",
    "app_name": "Py2APK App",
    "min_sdk": 21,
    "target_sdk": 34,
    "chaquopy_version": "12.0.0",
    "python_version": "3.8"
}

def load_config(config_path: str = "py2apk.yaml") -> dict:
    """Loads configuration from YAML file."""
    path = Path(config_path)
    if path.exists():
        with open(path, "r") as file:
            return yaml.safe_load(file)
    return DEFAULT_CONFIG  # Fallback to defaults

config = load_config()

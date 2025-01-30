from dataclasses import dataclass
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class AppConfig:
    package_name: str = "com.example.py2apk"
    app_name: str = "Py2APK App"
    min_sdk: int = 21
    target_sdk: int = 34

class ManifestGenerator:
    """Handles dynamic AndroidManifest.xml generation."""
    
    def create_manifest(self, project_path: Path, config: AppConfig) -> Path:
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{config.package_name}">

    <uses-sdk android:minSdkVersion="{config.min_sdk}" 
              android:targetSdkVersion="{config.target_sdk}"/>

    <application
        android:allowBackup="true"
        android:label="{config.app_name}"
        android:theme="@style/Theme.AppCompat">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>

</manifest>"""
        
        manifest_path = project_path / "app/src/main/AndroidManifest.xml"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(manifest_content)

        logger.info(f"AndroidManifest.xml generated at {manifest_path}")
        return manifest_path

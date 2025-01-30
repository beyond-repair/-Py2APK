import subprocess
import shutil
from pathlib import Path
import logging
from py2apk.utils.manifest import ManifestGenerator
from py2apk.config import config

logger = logging.getLogger(__name__)

class APKBuilder:
    """Handles Android project generation, Chaquopy integration, and APK building."""

    def __init__(self, project_path: Path, output_dir: Path):
        self.project_path = project_path
        self.output_dir = output_dir
        self.android_project_path = output_dir / "android_project"

    def _copy_native_libraries(self):
        """Copy pre-built native libraries for Chaquopy."""
        native_libs_dir = self.android_project_path / "app/src/main/jniLibs"
        native_libs_dir.mkdir(parents=True, exist_ok=True)

        # Copy pre-built .so files for ONNX Runtime, Torch, etc.
        for arch in ["armeabi-v7a", "arm64-v8a", "x86", "x86_64"]:
            arch_dir = native_libs_dir / arch
            arch_dir.mkdir(exist_ok=True)
            shutil.copy(f"native_libs/{arch}/libonnxruntime.so", arch_dir)
            shutil.copy(f"native_libs/{arch}/libtorch.so", arch_dir)

        logger.info("Copied native libraries for Chaquopy.")

    def create_android_project(self):
        """Generate Android project structure for Chaquopy."""
        if self.android_project_path.exists():
            shutil.rmtree(self.android_project_path)
        
        self.android_project_path.mkdir(parents=True)
        (self.android_project_path / "app/src/main/python").mkdir(parents=True)

        # Copy user Python files
        for file in self.project_path.glob("*.py"):
            shutil.copy(file, self.android_project_path / "app/src/main/python/")

        # Generate Manifest
        ManifestGenerator().create_manifest(self.android_project_path, config)

        # Copy Gradle template
        gradle_template = Path(__file__).parent / "templates/build.gradle"
        shutil.copy(gradle_template, self.android_project_path / "app/build.gradle")

        # Generate Chaquopy configuration
        chaquopy_config = f"""
android {{
    compileSdkVersion {config['target_sdk']}
    defaultConfig {{
        minSdkVersion {config['min_sdk']}
        targetSdkVersion {config['target_sdk']}
    }}
}}
apply plugin: 'com.chaquo.python'

chaquopy {{
    version "{config['chaquopy_version']}"
    python {{
        version "{config['python_version']}"
        pip {{
            install "requests"
            install "onnxruntime"
            install "torch"
        }}
    }}
}}
"""
        (self.android_project_path / "app/chaquopy.gradle").write_text(chaquopy_config)

        logger.info(f"Android project created at {self.android_project_path}")

    def build_apk(self):
        """Build APK using Chaquopy"""
        try:
            self.create_android_project()
            subprocess.run(["gradle", "assembleRelease", "-p", str(self.android_project_path)], check=True)

            apk_path = self.output_dir / "app-release.apk"
            return apk_path if apk_path.exists() else None
        except subprocess.CalledProcessError as e:
            logger.error(f"APK build failed: {e}")
            return None

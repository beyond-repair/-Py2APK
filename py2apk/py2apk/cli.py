import click
import logging
from pathlib import Path
from py2apk.builder import APKBuilder
from py2apk.signing import APKSigner
from py2apk.config import config

logger = logging.getLogger(__name__)

@click.command()
@click.option('--project', required=True, help='Path to Python project')
@click.option('--output', required=True, help='Output directory for APK')
@click.option('--keystore', help='Keystore file path')
@click.option('--keystore-pass', help='Keystore password', hide_input=True)
@click.option('--key-alias', help='Key alias')
@click.option('--key-pass', help='Key password', hide_input=True)
def main(project: str, output: str, keystore: str, keystore_pass: str, key_alias: str, key_pass: str):
    """Convert AI-powered Python projects to Android APK."""
    try:
        project_path = Path(project)
        output_dir = Path(output)

        builder = APKBuilder(project_path, output_dir)
        apk_path = builder.build_apk()

        if not apk_path:
            logger.error("APK build failed.")
            return 1

        if keystore and keystore_pass and key_alias and key_pass:
            signer = APKSigner()
            signer.sign_apk(apk_path, Path(keystore), keystore_pass, key_alias, key_pass)

        logger.info(f"Successfully created APK: {apk_path}")
        return 0
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == '__main__':
    main()

import yaml
from pathlib import Path
import logging
from packaging.requirements import Requirement, InvalidRequirement
from packaging.version import parse

logger = logging.getLogger(__name__)

class DependencyAnalyzer:
    """Analyzes project dependencies for Android compatibility."""
    
    def __init__(self, config_file: str = "dependency_config.yaml"):
        self.compatible_versions = self._load_compatible_versions(config_file)

    def _load_compatible_versions(self, config_file: str):
        """Load dependency compatibility info from config."""
        try:
            config_path = Path(config_file)
            if not config_path.exists():
                return {}
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load dependency config: {e}")
            return {}

    def check_compatibility(self, requirements_path: Path):
        """Check dependencies for compatibility issues."""
        issues = []
        try:
            with open(requirements_path) as f:
                for line in f:
                    try:
                        req = Requirement(line.strip())
                        if req.name not in self.compatible_versions:
                            continue

                        constraints = self.compatible_versions[req.name]
                        installed_version = parse(req.specifier)

                        if "max_version" in constraints and installed_version > parse(constraints["max_version"]):
                            issues.append(f"{req.name} exceeds max supported {constraints['max_version']}")

                        if "min_version" in constraints and installed_version < parse(constraints["min_version"]):
                            issues.append(f"{req.name} requires at least {constraints['min_version']}")

                    except InvalidRequirement:
                        issues.append(f"Invalid requirement format: {line.strip()}")

            return issues
        except Exception as e:
            logger.error(f"Dependency check failed: {e}")
            return ["Error processing dependencies"]

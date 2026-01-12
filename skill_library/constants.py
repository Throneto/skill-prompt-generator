
import os
from pathlib import Path

# Get the directory where this package is located (ROOT/skill_library)
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

# Get the project root (ROOT)
PROJECT_ROOT = os.path.dirname(PACKAGE_DIR)

# Default paths
DEFAULT_DB_PATH = os.path.join(PROJECT_ROOT, "extracted_results", "elements.db")
DEFAULT_FRAMEWORK_PATH = os.path.join(PROJECT_ROOT, "prompt_framework.yaml")

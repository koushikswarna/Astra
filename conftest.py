"""Root conftest -- makes sure the astra package is importable from project root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

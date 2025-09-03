# resources.py
from functools import lru_cache
import json
from pathlib import Path

# Use pathlib for better path handling
DATA_DIR = Path(__file__).parent / 'data'

@lru_cache(maxsize=1)
def materials():
    """Load materials data with error handling."""
    try:
        with open(DATA_DIR / 'materials.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Materials data file not found: {DATA_DIR / 'materials.json'}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in materials file: {e}")

@lru_cache(maxsize=1)
def bolt_sizes():
    """Load bolt sizes data with error handling."""
    try:
        with open(DATA_DIR / 'bolt_sizes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Bolt sizes data file not found: {DATA_DIR / 'bolt_sizes.json'}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in bolt sizes file: {e}")

@lru_cache(maxsize=1)
def clearance_holes():
    """Load clearance holes data with error handling."""
    try:
        with open(DATA_DIR / 'clearance_holes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Clearance holes data file not found: {DATA_DIR / 'clearance_holes.json'}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in clearance holes file: {e}")

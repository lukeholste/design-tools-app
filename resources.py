# resources.py
from functools import lru_cache
import json
from pathlib import Path 

DATA_DIR = Path(__file__).with_suffix("").parent / 'data'

@lru_cache(maxsize=1)
def materials():
    with open(DATA_DIR / 'materials.json', 'r') as f:
        return json.load(f)

@lru_cache(maxsize=1)
def bolt_sizes():
    with open(DATA_DIR / 'bolt_sizes.json', 'r') as f:
        return json.load(f)

@lru_cache(maxsize=1)
def clearance_holes():
    with open(DATA_DIR / 'clearance_holes.json', 'r') as f:
        return json.load(f)

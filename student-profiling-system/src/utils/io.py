import os
import json
import joblib
from typing import Any, Dict

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def save_json(path: str, obj: Dict[str, Any]) -> None:
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_joblib(path: str, obj: Any) -> None:
    ensure_dir(os.path.dirname(path) or ".")
    joblib.dump(obj, path)

def load_joblib(path: str) -> Any:
    return joblib.load(path)

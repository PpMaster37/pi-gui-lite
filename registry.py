import importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).parent
CONFIG = ROOT / "app_registry.json"

def load_registry():
    if not CONFIG.exists():
        return {"modules": {}}
    return json.loads(CONFIG.read_text())

def save_registry(data):
    tmp = CONFIG.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(CONFIG)

def load_module(name, info):
    file_path = Path(info["path"])
    if not file_path.exists():
        raise FileNotFoundError(file_path)
    
    spec = importlib.util.spec_from_file_location(name, file_path)

    if spec is None:
        raise ImportError(f"can't load {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

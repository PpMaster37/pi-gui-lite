import importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).parent
CONFIG = ROOT / "app_registry.json"

def load_registry():
    if not CONFIG.exists():
        return {"modules": {}}
    return json.loads(CONFIG.read_text())

def add_git_repo(name, path, url):
    data = load_registry()
    data["modules"][name] = {
        "path": path,
        "git_url": url,
        "is_git": True,
        "enabled": True
    }
    save_registry(data)

def add_py_script(name, path):
    data = load_registry()
    data["modules"][name] = {
        "path": path,
        "git_url": "",
        "is_git": False,
        "enabled": True
    }
    save_registry(data)

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

def load_gits():
    return_list = []
    reg = load_registry()
    for name, info in reg["modules"].items():
        if info.get("is_git", False):
            return_list.append({"name": name, "info": info})
    return return_list

def get_username():
    return load_registry()["git_username"]

def get_clone_path():
    return load_registry()["git_clone_path"]
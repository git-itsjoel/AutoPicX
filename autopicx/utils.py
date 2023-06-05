import os
import sys
import logging
import importlib
from pathlib import Path

def load_plugins(plugin_name):
    path = Path(f"autopicx/plugins/{plugin_name}.py")
    name = "autopicx.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["autopicx.plugins." + plugin_name] = load
    print("Bot has Imported " + plugin_name)

def save_integer(value):
    os.environ['LAST'] = str(value)

def load_integer():
    value = os.environ.get('LAST')
    if value is not None:
        return int(value)
    else:
        return None
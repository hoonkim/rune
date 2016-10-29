import importlib
import importlib.machinery

import sys

from module import Module
import json


def message_to_function(raw_message):
    """
    converting json formatted string to a executable module.

    Args:
        raw_message (str): json formatted.

    Returns:
        None if raw_message is in wrong format, else
        return the executable module.

    """

    if raw_message is None:
        return None

    try:
        wisp = json.loads(raw_message)
    except json.JSONDecodeError:
        return None

    function_object = wisp["function_object"]
    path = function_object["function_path"]
    force_update = function_object["validation_required"]

    params = wisp["params"]
    name = str(wisp["uFid"])

    loader = importlib.machinery.SourceFileLoader(name, path)

    # if modules exists on the memory.
    if name in sys.modules.keys():
        if force_update:
            del sys.modules[name]
        else:
            return sys.modules[name]

    mod = None
    try:
        mod = loader.load_module()
    except FileNotFoundError:
        print("Module not found")
    finally:
        if mod is not None:
            wisp_module = Module(mod, params)
            return wisp_module
        return mod

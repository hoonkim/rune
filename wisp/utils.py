import importlib
import importlib.machinery
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

    wisp = None

    try:
        wisp = json.loads(raw_message)
    except json.JSONDecodeError:
        return None

    path = wisp["path"]
    params = wisp["params"]

    loader = importlib.machinery.SourceFileLoader('name', path)

    mod = None

    try :
        mod = loader.load_module()
    except FileNotFoundError:
        print("Module not found")
    except Exception:
        print("Unknown Excpetion")
    finally :
        if mod is not None :
            wisp_module = Module(mod, params)
            return wisp_module
        return mod


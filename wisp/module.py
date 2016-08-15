

class Module:
    """
    Module container.
    """
    _mod = None
    _params = None

    def __init__(self, mod, params):
        self._mod = mod
        self._params = params

    def run(self):
        """
        run module.
        Returns: returns the return of function.

        """
        print(self._mod)
        print(self._params)
        ret = self._mod.wisp_callback(*self._params)
        return ret

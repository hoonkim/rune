import sys
from io import StringIO


class OutputRecorder:
    ORIGINAL_STDOUT = sys.stdout
    ORIGINAL_STDERR = sys.stderr

    def __init__(self):
        self._stdout = StringIO()
        self._stderr = StringIO()

    def start(self):
        """
        Override stdout and stderr to StringIO so that we can now save any output stream from module.
        Returns:

        """
        self._stdout.truncate(0)
        self._stderr.truncate(0)

        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def finish(self):
        out_string = self._stdout.getvalue()
        err_string = self._stderr.getvalue()

        sys.stdout = self.ORIGINAL_STDOUT
        sys.stderr = self.ORIGINAL_STDERR

        return out_string, err_string

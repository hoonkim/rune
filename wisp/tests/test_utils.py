import unittest
import json

import tests.dummy
from utils import *


class TestUtils(unittest.TestCase):
    def test_message_to_function(self):
        test_dict = dict()
        test_dict['path'] = "./tests/dummy.py"

        param = ['ABC ', "abc "]
        test_dict['params'] = param

        test_json = json.dumps(test_dict)

        mod = message_to_function(test_json)
        result1 = mod.run()

        # Function call check.
        self.assertEqual(result1, tests.dummy.wisp_callback(*param))

        # None check
        self.assertIsNone(message_to_function(None))

        # wrong formatted json check
        self.assertIsNone(
            message_to_function('{"sdf" : "ssdf"')
        )

        return


if __name__ == '__main__':
    unittest.main()

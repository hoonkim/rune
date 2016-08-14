import unittest
import json

import wisp.test.dummy
from wisp.utils import *


class TestUtils(unittest.TestCase):
    def test_message_to_function(self):
        test_dict = {}
        test_dict['path'] = "./dummy.py"

        param = ['ABC ', "abc "]
        test_dict['params'] = param

        test_json = json.dumps(test_dict)

        mod = message_to_function(test_json)
        result1 = mod.wisp_callback(*param)

        # Function call check.
        self.assertEqual(result1, wisp.test.dummy.wisp_callback(*param))

        # None check
        self.assertIsNone(message_to_function(None))

        # wron formatt json check
        self.assertIsNone(
            message_to_function('{"sdf" : "ssdf"')
        )

if __name__ == '__main__':
    unittest.main()

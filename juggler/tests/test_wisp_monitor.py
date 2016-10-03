import unittest
from juggler import wisp_monitor
import json


class MyTestCase(unittest.TestCase):
    def test_wisp_monitor(self):
        body = json.dumps({
            "function_path": "C:/Users/gnsdl/PycharmProjects/rune\wisp/tests\dummy.py"
        , "function_object" : {"params": ["abc", "def"]}})

        monitor = wisp_monitor.WispMonitor()
        result = monitor.call(body, "uuid123")

        self.assertEqual(result, "abc" + "def" + "a!@#$")

if __name__ == '__main__':
    unittest.main()

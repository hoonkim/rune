import signal
import threading
import unittest
import uuid

import pika
import time
import json

from message_listener import MessageListener
from tests import dummy


class MessageListenerCase(unittest.TestCase):
    _corr_id = None

    def test_client(self):
        '''
        testing


        '''
        th = threading.Thread(target=self.listening)
        th.daemon = True
        th.start()

        con = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        chan = con.channel()
        chan.queue_declare(queue="wisp")
        self._corr_id = str(uuid.uuid4())

        test_case = dict()
        test_case['path'] = "./dummy.py"
        test_case['params'] = ["asdf", "fdsa"]

        test_body = json.dumps(test_case)

        # basic
        chan.basic_publish(exchange='', routing_key='test_wisp',
                           body=test_body,
                           properties=pika.BasicProperties(reply_to="detonate", correlation_id=self._corr_id)
                           )
        chan2 = con.channel()
        chan2.queue_declare(queue="detonate")
        time.sleep(3)
        method_frame, header_frame, body = chan2.basic_get('detonate')

        if method_frame:
            chan2.basic_ack(method_frame.delivery_tag)
        else:
            print('No message returned')

        # Comparing the result between wisp and None wisp.
        self.assertEqual(str(body, 'utf-8'), str(dummy.wisp_callback(*test_case['params'])))

        return

    @staticmethod
    def listening():
        test_listener = MessageListener('localhost', 'test_wisp')
        test_listener.listen()

if __name__ == '__main__':
    unittest.main()
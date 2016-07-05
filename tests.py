# coding: utf-8

import shutil
import json
import StringIO
import unittest
import tempfile

import conf
import app


class AppTestCase(unittest.TestCase):

    TEST_DOMAIN = '.test.servator.com'

    def setUp(self):
        self.app = app.app.test_client()
        # todo: use app.config instead...
        conf.SERVE_DIRECTORY_PATH = tempfile.mkdtemp()
        conf.SERVATOR_DOMAIN = self.TEST_DOMAIN

    def tearDown(self):
        shutil.rmtree(conf.SERVE_DIRECTORY_PATH)

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_web_upload(self):
        data = dict(
            serve=(StringIO.StringIO('hello'), 'index.html')
        )
        response = self.app.post('/upload', data=data)
        self.assertEqual(response.status_code, 302)

    def test_api_upload(self):
        data = dict(
            serve=(StringIO.StringIO('hello'), 'index.html')
        )
        response = self.app.post('/api/upload', data=data)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertIn('result', response_json)


if __name__ == '__main__':
    unittest.main()

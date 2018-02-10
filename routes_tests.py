#!/usr/bin/env python

import unittest
import routes

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        routes.app.testing = True
        self.app = routes.app.test_client()

    def tearDown(self):
        pass

    def GET(self, url):
        return self.app.get(url)

    def test_get_root(self):
        resp = self.GET("/")

        self.assertEqual(200, resp.status_code, msg="/ response should be OK")
        self.assertIn(b"Go away!", resp.data, msg="/ response should contain expected data")

    def test_get_graphql(self):
        resp = self.GET("/graphql")

        self.assertEqual(200, resp.status_code, msg="/graphql response should be OK")

    def test_get_healthz(self):
        resp = self.GET("/healthz")

        self.assertEqual(200, resp.status_code, msg="/debug/healthz response should be OK")
        self.assertIn(b"OK", resp.data, msg="/ response should contain expected data")

    def test_get_healthz_info(self):
        resp = self.GET("/healthz/info")

        self.assertEqual(200, resp.status_code, msg="/debug/healthz response should be OK")
        self.assertIn(b""""errors":[]""", resp.data, msg="/debug/healthz response should contain expected data")

    def test_get_healthz_ready(self):
        resp = self.GET("/healthz/ready")

        self.assertEqual(200, resp.status_code, msg="/debug/ready response should be OK")
        self.assertIn(b"OK", resp.data, msg="/ response should contain expected data")

if "__main__" == __name__:
    unittest.main()

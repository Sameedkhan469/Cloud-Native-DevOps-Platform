import unittest

from app.app import app


class FlaskApplicationTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "UP")

    def test_info_endpoint(self):
        response = self.client.get("/info")
        self.assertEqual(response.status_code, 200)
        self.assertIn("application", response.get_json())

    def test_metrics_endpoint(self):
        self.client.get("/")
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"flask_http_requests_total", response.data)


if __name__ == "__main__":
    unittest.main()

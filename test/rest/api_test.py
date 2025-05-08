import http.client
import os
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError


import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:8081"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )        
    
    def test_api_division_por_cero(self):
        try:
            url = f"{BASE_URL_MOCK}/calc/div/10/0"
            urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail(f"Se esperaba un error HTTP 400 al hacer petición a {url}")
        except HTTPError as e:
            self.assertEqual(e.code, 400, f"Se esperaba error 400 pero fue {e.code}")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

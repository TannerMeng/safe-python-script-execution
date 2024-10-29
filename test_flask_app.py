import unittest
import requests

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Define the base URL for all requests."""
        self.base_url = 'http://app:8080/execute'

    def test_execute_no_script(self):
        """Test /execute endpoint with no script in data."""
        response = requests.post(self.base_url, json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Missing script field in JSON"})

    def test_execute_without_main_function(self):
        """Test /execute endpoint with script missing main() function."""
        script = "print('Hello, World!')"
        response = requests.post(self.base_url, json={"script": script})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Script must contain a main() function"})

    def test_execute_with_main_function(self):
        """Test /execute endpoint with correct script containing main() function."""
        script = '''
def main():
    return {"message": "Hello, World!"}
'''
        response = requests.post(self.base_url, json={"script": script})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": {"message": "Hello, World!"}})

    def test_execute_with_pandas_import(self):
        """Test /execute endpoint with correct script containing pandas import."""
        script = '''
import pandas as pd
def main():
    return {"message": "Hello, World!"}
'''
        response = requests.post(self.base_url, json={"script": script})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": {"message": "Hello, World!"}})

    def test_execute_script_timeout(self):
        """Test /execute endpoint for a script that times out."""
        script = '''
import time
def main():
    time.sleep(15)
    return {"message": "Finished"}
'''
        response = requests.post(self.base_url, json={"script": script})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Execution failed due to timeout"})

    def test_invalid_json_return(self):
        """Test /execute endpoint where script doesn't return valid JSON."""
        script = '''
def main():
    return "This is not a JSON object"
'''
        response = requests.post(self.base_url, json={"script": script})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "main() function must return a valid JSON"})

if __name__ == '__main__':
    unittest.main()

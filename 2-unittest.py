import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonAndGoogle(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="/home/simon/repos/testing-selenium/geckodriver")

    def test_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Pythonn", driver.title)

    def test_google_com(self):
        driver = self.driver
        driver.get("http://www.google.com")
        self.assertIn("Google", driver.title)

    def test_unsj_edu_ar(self):
        driver = self.driver
        driver.get("http://www.unsj.edu.ar")
        self.assertIn("unsjj", driver.title)
        
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

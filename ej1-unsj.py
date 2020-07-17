import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UnitTestExactasUnsj(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="/home/simon/repos/testing-selenium/geckodriver")

    #test for fallen link www.biblioteca.mincyt.gov.ar/
    def test_link(self):
        driver = self.driver
        # enter page
        driver.get("https://exactas.unsj.edu.ar/")
        # go to https://exactas.unsj.edu.ar/biblioteca/ pressing the button
        # this steps will be omitted in next tests, going directly to the intended url, for convenience
        button_redirect = driver.find_element_by_xpath("/html/body/div/header/div[1]/div/div[1]/ul/li[1]/a")
        button_redirect.click()
        time.sleep(3)
        # go to link www.biblioteca.mincyt.gov.ar/
        button_redirect = driver.find_element_by_xpath("/html/body/div/div/div/div/div[1]/article/div/div/p[19]/a/strong")
        button_redirect.click()
        # this page is really slow to load
        time.sleep(20)
        # check if the element of the title of the page exists
        # currently, this test is passing! I swear last week this link did not work!
        element = driver.find_element_by_xpath("/html/body/div[1]/header/div/div[1]/div/a/img")
        assert element is not None  # this line is not absolutely necessary because if the element is not in the page,
        #                             the instruction that will fail will be the driver.find_element

    #test for google map error in contact page
    def test_map(self):
        driver = self.driver
        driver.get("https://exactas.unsj.edu.ar/contactos/")
        map_error_element =\
            "/html/body/div/div/div/div/div[1]/article/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/span"
        # look for the google maps error message
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, map_error_element)))
            not_found = False
        except:
            not_found = True
        # if error message found, then the test has to fail
        assert not_found

    # test for sending "consulta" through contact page
    def test_consultas(self):
        driver = self.driver
        driver.get("https://exactas.unsj.edu.ar/contactos/")
        #   check error message not displayed at the beginning
        error_message = "/html/body/div/div/div/div/div[1]/article/div/div/div[1]/div/div/div[1]/div/div[1]/p"
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, error_message)))
            not_found = False
        except:
            not_found = True
        # if error message found, then the test has to fail
        assert not_found
        #   fill the form
        name = driver.find_element_by_xpath("//*[@id='et_pb_contact_name_1']")
        name.send_keys("Simón")
        email = driver.find_element_by_xpath("//*[@id='et_pb_contact_email_1']")
        email.send_keys("simon.pedro.g@gmail.com")
        message = driver.find_element_by_xpath("//*[@id='et_pb_contact_message_1']")
        message.send_keys("Testing de la pag web. No responder, disculpe las molestias")
        #   solve the captcha
        captcha = driver.find_element_by_name("et_pb_contact_captcha_0")
        first_digit = int(captcha.get_attribute("data-first_digit"))
        second_digit = int(captcha.get_attribute("data-second_digit"))
        captcha_result = first_digit+second_digit
        print(captcha_result)
        captcha.send_keys(str(captcha_result))
        #   send
        driver.find_element_by_xpath(
            "/html/body/div/div/div/div/div[1]/article/div/div/div[1]/div/div/div[1]/div[2]/form/div/button"
        ).click()
        time.sleep(10)
        #   check for error message again
        error_message = "/html/body/div/div/div/div/div[1]/article/div/div/div[1]/div/div/div[1]/div/div[1]/p"
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, error_message)))
            not_found = False
        except:
            not_found = True
        # if error message found, then the test has to fail
        assert not_found

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

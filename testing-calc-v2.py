# -*- coding: utf-8 -*-
"""
    File name: testing-calc-v2.py
    Author: Simón Pedro González
    Date created: 28/6/2020
    Date last modified: 29/6/2020
    Python Version: 3.7
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support.ui import Select
import pandas as pd

#   The solution proposed is not a unit test class. The reason for that is that I wanted to be able to control
#   which tests are executed in a loop, and not in serial fashion like in the selenium unittest class
#   This way, I am able to run all the CPs (almost 200) with only 7 tests, looping and changing the values.
#   Disadvantages of this approach: the tests functions don't really perform assertions because that will stop
#   the execution of the loop. Instead, the functions check the condition, and return OK or ERROR. The results are
#   appended to a pandas data frame and written at the end in a csv file, that can be opened with excel or libre
#   office calc. There are options to do "parametrized" testing with selenium, adding other libraries and
#   loading the data from json files for example, but I considered that option out of my reach due time limitations.
#   Moreover, this option allowed me to take advantage of the google sheet test containing the CPs.
#   NOTE: if it seems that somehow all the tests are failing, it is because the page is not loading correctly and the
#   buttons do not work. This happened to me sometimes, but its cause is probable due to bad internet connection. The
#   only solution I found is to wait a little bit and then running the tests again.

class UnitTestCalc:

    def __init__(self, version):
        self.driver = webdriver.Firefox(executable_path="/home/simon/repos/testing-selenium/geckodriver")
        self.url = "https://gerabarud.github.io/is3-calculadora/"
        self.driver_get()
        #   function to get the elements we are going to use, and setting the version
        self.init_elements(version)
        #   getting the test data to make the testing more automated!
        self.sheet_id = "1tWcv5juwsAOS_K4aD9MeGPDCgKRociPviAlZvKwxW5E"   # this is the google sheet of the manual test
        self.df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv")
        self.wait = 3
        print("TESTING CALCULATOR VERSION "+str(self.version))

    def driver_get(self):
        #   little workaround to stop the loading when all elements are already present
        #   this saves a lot of time with bad internet connection. The page looks bad
        #   but it works, and I do not have to wait that long to start the tests
        t = time.time()
        self.driver.set_page_load_timeout(20)
        try:
            self.driver.get(self.url)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        print('Loading time:', time.time() - t)

    def init_elements(self, version):
        #   selecting the calc version
        self.version = version
        Select(self.driver.find_element_by_id("selectBuild")).select_by_index(self.version)
        #   predefining the elements we are going to need
        self.clear_button = self.driver.find_element_by_id("clearButton")
        self.calc_button = self.driver.find_element_by_id("calculateButton")
        self.int_checkbox = self.driver.find_element_by_id("integerSelect")
        self.answer = self.driver.find_element_by_id("numberAnswerField")
        self.number1 = self.driver.find_element_by_id("number1Field")
        self.number2 = self.driver.find_element_by_id("number2Field")
        self.error_field_id = "errorMsgField"
        self.number1_error = "Number 1 is not a number"
        self.number2_error = "Number 2 is not a number"
        self.divide_by_0_error = "Divide by zero error!"

    def run(self):
        #   create a column to insert results
        self.df.insert(12, "Test automatico", "")
        #   iterate over the CPs to get the data and execute de tests
        for index, row in self.df.iterrows():
            #   select operation
            Select(self.driver.find_element_by_id("selectOperationDropdown")).select_by_visible_text(row["Operation"])
            #   clear everything
            self.clear_button.click()
            self.number1.clear()
            self.number2.clear()
            #   this is self explanatory
            int_box = row["Integers only"]
            if int_box == "On":
                self.int_checkbox.click()
            #   in the column check there is the name of the test we are going to run
            #   so we use some dynamic dispatching to run the correct function
            test_result = getattr(self, row["check"])(row)
            #   we add the result to the pandas df
            self.df['Test automatico'][index] = test_result
            if test_result == "ERROR":
                print(row["check"])
            #   uncheck the checkbox if needed
            if int_box == "On":
                self.int_checkbox.click()
        #   write the results in a csv file
        self.write_results()

    def write_results(self):
        self.df = self.df[["Tipo", "ID", "Objetivo", "First Number", "Second Number", "Integers only", "Result",
                           "Comportamiento esperado", "Comportamiento recibido", "Test manual",
                           "Test automatico"]]
        name = "test_result_v"+str(self.version)+".csv"
        self.df.to_csv(name)

    def test_lim_n1(self, data):
        #   checking the size limit of n1
        n1 = data["First Number"]
        #   clear and insert the value
        self.number1.send_keys(n1)
        #   check that only the first 10 characters can be inserted
        if not self.number1.get_attribute("value") == n1[:10]:
            return "ERROR"
        return "OK"

    def test_lim_n2(self, data):
        #   checking the size limit of n2
        n2 = data["Second Number"]
        #   clear and insert the value
        self.number2.send_keys(n2)
        #   check that only the first 10 characters can be inserted
        if not self.number2.get_attribute("value") == n2[:10]:
            return "ERROR"
        return "OK"

    def test_result(self, data):
        #   simply compare the result with the manual prototype result that comes from the sheet
        result = data["Comportamiento esperado"]
        self.number1.send_keys(data["First Number"])
        self.number2.send_keys(data["Second Number"])
        self.calc_button.click()
        time.sleep(self.wait)
        if not self.answer.get_attribute("value") == result:
            return "ERROR"
        return "OK"

    def test_n1(self, data):
        #   the malformed number1 error must appear
        self.number1.send_keys(data["First Number"])
        self.number2.send_keys(data["Second Number"])
        self.calc_button.click()
        time.sleep(self.wait)
        if not self.driver.find_element_by_id(self.error_field_id).get_attribute("innerHTML") == \
               self.number1_error:
            return "ERROR"
        return "OK"

    def test_n2(self, data):
        #   the malformed number2 error must appear
        self.number1.send_keys(data["First Number"])
        self.number2.send_keys(data["Second Number"])
        self.calc_button.click()
        time.sleep(self.wait)
        if not self.driver.find_element_by_id(self.error_field_id).get_attribute("innerHTML") == self.number2_error:
            return "ERROR"
        return "OK"

    def test_0div(self, data):
        #   the divide by 0 error must appear
        self.number1.send_keys(data["First Number"])
        self.number2.send_keys(data["Second Number"])
        self.calc_button.click()
        time.sleep(self.wait)
        if not self.driver.find_element_by_id(self.error_field_id).get_attribute("innerHTML") == \
               self.divide_by_0_error:
            return "ERROR"
        #   refresh the page and regather the elements
        self.driver_get()
        self.init_elements(self.version)
        return "OK"

    def test_ans(self, data):
        #   is similar to test_result, but we have to do an extra step to make the correct number
        #   available in the answer field before executing the test
        Select(self.driver.find_element_by_id("selectBuild")).select_by_index(0)
        result = data["Comportamiento esperado"]
        self.number1.send_keys(data["First Number"])
        self.number2.send_keys(data["Second Number"])
        self.calc_button.click()
        time.sleep(self.wait)
        Select(self.driver.find_element_by_id("selectBuild")).select_by_index(self.version)
        self.calc_button.click()
        time.sleep(self.wait)
        if not self.answer.get_attribute("value") == result:
            return "ERROR"
        return "OK"

    def tearDown(self):
        #   self explanatory
        self.driver.quit()
        print("ENDING TEST...")


#   to ignore annoying pandas warnings
pd.options.mode.chained_assignment = None  # default='warn'

#   run test on prototype
#ut = UnitTestCalc(0)
#ut.run()
#ut.tearDown()
#   run test on version 7
ut = UnitTestCalc(7)
ut.run()
ut.tearDown()
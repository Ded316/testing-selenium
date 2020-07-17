from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(executable_path="/home/simon/repos/testing-selenium/geckodriver")
driver.get("http://www.google.com")
assert "Google" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("unsj")
elem.send_keys(Keys.ENTER)
assert "asdasd" in driver.page_source
driver.close()

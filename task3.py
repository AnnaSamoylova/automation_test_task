from selenium import webdriver
import time
import datetime
from selenium.common.exceptions import NoSuchElementException
import unittest

def check_exists_by_xpath(xpath,driver):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
	
class testSemrush (unittest.TestCase):
	driver = None
	
	
	def setUp(self):
		self.driver = webdriver.Chrome("C:\ChromeWebDriver\chromedriver.exe")
		self.driver.get("http://semrush.com")
		#Залогинивание под пользователем в SEMrush
		logButton=self.driver.find_element_by_xpath('//button[@data-test="auth-popup__btn-login"]')
		logButton.click()
		
		emailBox=self.driver.find_element_by_xpath('//input[@data-test="auth-popup__email"]')
		emailBox.send_keys("mosik@ya.ru")
		
		passwordBox=self.driver.find_element_by_xpath('//input[@data-test="auth-popup__password"]')
		passwordBox.send_keys("qwerty123")
		
		submitButton=self.driver.find_element_by_xpath('//button[@data-test="auth-popup__submit"]')
		submitButton.click()
		time.sleep(20)
		
	def tearDown(self):
		self.driver.quit()
		
		
	def test_login(self):
		self.assertEqual(self.driver.current_url, 'https://www.semrush.com/dashboard/')
		

	def test_createNote(self):
		self.driver.get("http://semrush.com/users/notes")
		time.sleep(20)
		addNoteButton=self.driver.find_element_by_xpath('//button[@data-cream-action="add-note"]')
		addNoteButton.click()
		
		titleBox=self.driver.find_element_by_xpath('//input[@data-cream-ui="input-title"]')
		testTitle="Test " + str(datetime.datetime.now())
		titleBox.send_keys(testTitle)
		
		descriptionBox=self.driver.find_element_by_xpath('//textarea[@data-cream-ui="input-note"]')
		descriptionBox.send_keys("The Dark Side is more powerfull")
		
		saveButton=self.driver.find_element_by_xpath('//button[@data-cream-action="save"]')
		saveButton.click()
		time.sleep(20)
		
		self.assertTrue(check_exists_by_xpath('//span[contains(text(),"' + testTitle + '")]', self.driver), "Новая заметка не была создана")
		
	def test_newProject(self):
		self.driver.get("https://www.semrush.com/dashboard/")
		time.sleep(20)
		newProjectButton=self.driver.find_element_by_xpath('//i[@class="s-icon -plus -xs"]')
		newProjectButton.click()

		domainBox=self.driver.find_element_by_xpath('//input[@class="js-pr-watch-domain temp-tn-projects__input"]')
		domainBox.send_keys("ya.ru")

		nameBox=self.driver.find_element_by_xpath('//input[@class="js-pr-watch-name temp-tn-projects__input"]')
		nameBox.send_keys("Test")

		createButton=self.driver.find_element_by_xpath('//button[@class="js-pr-create s-btn -xs -success temp-tn-projects__submit"]')
		createButton.click()
		time.sleep(20)
		
		self.assertTrue(check_exists_by_xpath('//*[contains(text(),"ya.ru")]', self.driver), "Новый проект не был создан")

if __name__ == '__main__':
	unittest.main()



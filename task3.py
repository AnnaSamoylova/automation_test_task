import time
import datetime
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
	
class testSemrush (unittest.TestCase):
	driver = None
	wait = None
	timeout = 60
	webdriverPath = "C:\ChromeWebDriver\chromedriver.exe"
	domain = "https://www.semrush.com"
	email = "mosik@ya.ru"
	password = "qwerty123"
	
	def get_clickable_element_by_xpath(self, xpath):
		element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
		return element
		
	def check_exists_by_xpath(self, xpath):
		try:
			self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
		except TimeoutException:
			return False
		return True
	
	def setUp(self):
		self.driver = webdriver.Chrome(self.webdriverPath)
		self.wait = WebDriverWait(self.driver, self.timeout)
		self.driver.get(self.domain)
		
		#Залогинивание под пользователем в SEMrush
		logButton = self.get_clickable_element_by_xpath('//button[@data-test="auth-popup__btn-login"]')
		logButton.click()
		
		emailBox = self.get_clickable_element_by_xpath('//input[@data-test="auth-popup__email"]')
		emailBox.send_keys(self.email)
		
		passwordBox = self.get_clickable_element_by_xpath('//input[@data-test="auth-popup__password"]')
		passwordBox.send_keys(self.password)
		
		submitButton = self.get_clickable_element_by_xpath('//button[@data-test="auth-popup__submit"]')
		submitButton.click()
		
	def tearDown(self):
		self.driver.quit()
		
		
	def test_login(self):
		self.assertTrue(self.check_exists_by_xpath('//a[@href="/notes/"]'), "Логин провален")
		

	def test_createNote(self):
		notesButton = self.get_clickable_element_by_xpath('//a[@href="/notes/"]')
		notesButton.click()
		
		addNoteButton=self.get_clickable_element_by_xpath('//button[@data-cream-action="add-note"]')
		addNoteButton.click()
		
		titleBox=self.get_clickable_element_by_xpath('//input[@data-cream-ui="input-title"]')
		
		#Генерируется уникальное имя заметки, т.к. формат выводимой даты 2017-10-30 00:05:04.567499
		testTitle="Test " + str(datetime.datetime.now())
		titleBox.send_keys(testTitle)
		
		descriptionBox=self.get_clickable_element_by_xpath('//textarea[@data-cream-ui="input-note"]')
		descriptionBox.send_keys("The Dark Side is more powerfull")
		
		saveButton=self.get_clickable_element_by_xpath('//button[@data-cream-action="save"]')
		saveButton.click()
		
		self.assertTrue(self.check_exists_by_xpath('//span[contains(text(),"' + testTitle + '")]'), "Новая заметка не была создана")
		
	def test_newProject(self):
		newProjectButton=self.get_clickable_element_by_xpath('//i[@class="s-icon -plus -xs"]')
		newProjectButton.click()

		domainBox=self.get_clickable_element_by_xpath('//input[@class="js-pr-watch-domain temp-tn-projects__input"]')
		domainBox.send_keys("ya.ru")

		nameBox=self.get_clickable_element_by_xpath('//input[@class="js-pr-watch-name temp-tn-projects__input"]')
		nameBox.send_keys("Test")

		createButton=self.get_clickable_element_by_xpath('//button[@class="js-pr-create s-btn -xs -success temp-tn-projects__submit"]')
		createButton.click()
		
		self.assertTrue(self.check_exists_by_xpath('//*[contains(text(),"ya.ru")]'), "Новый проект не был создан")
		
		#удаление проекта
		settingsButton = self.get_clickable_element_by_xpath('//span[@class="s-icon -s -settings"]')
		settingsButton.click()
		
		deleteButton = self.get_clickable_element_by_xpath('//a[@class="js-remove"]')
		deleteButton.click()
		
		removeBox = self.get_clickable_element_by_xpath('//input[@class="s-input__control js-remove-input"]')
		removeBox.send_keys("Test")
		
		removeButton = self.get_clickable_element_by_xpath('//button[@class="s-btn -s -danger js-remove"]')
		removeButton.click()
		
		#проверить что удалено успешно
		self.assertTrue(self.check_exists_by_xpath('//span[contains(text(),"Create my first project")]'), "Проект не был удален")

if __name__ == '__main__':
	unittest.main()

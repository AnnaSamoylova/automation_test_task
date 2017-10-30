import requests
import json
import unittest

#Функция возвращает агрегатное состояние воды при определенной температуре
tempUrl = 'http://ntanygin.pythonanywhere.com/?temperature='
def getCond(temp):
	response = requests.get(tempUrl + temp)
	if response.status_code == 200:
		return json.loads(response.text)["state"]
	else:
		return 'Response Error' 
	
class TestConditionMethods(unittest.TestCase):
	def test_lowerThanAbsoluteZero(self):
		self.assertNotEqual(getCond('-274').lower(), 'ice')
			
	def test_float(self):
		self.assertEqual(getCond('1.5').lower(), 'water', "Датчик не поддерживает дробные значения температуры")
		self.assertEqual(getCond('1,5').lower(), 'water', "Датчик не поддерживает дробные значения температуры")
		self.assertEqual(getCond('1/5').lower(), 'water', "Датчик не поддерживает дробные значения температуры")
	
	def test_ice(self):
		self.assertEqual(getCond('-273').lower(), 'ice', "Датчик неисправен")
		self.assertEqual(getCond('-27').lower(), 'ice', "Датчик неисправен")
		self.assertEqual(getCond('0').lower(), 'ice', "Датчик неисправен")

	def test_water(self):
		self.assertEqual(getCond('1').lower(), 'water', "Датчик неисправен")
		self.assertEqual(getCond('45').lower(), 'water', "Датчик неисправен")
		self.assertEqual(getCond('99').lower(), 'water', "Датчик неисправен")

	def test_steam(self):
		self.assertEqual(getCond('100').lower(), 'steam', "Датчик неисправен")
		self.assertEqual(getCond('10000').lower(), 'steam', "Датчик неисправен")
		self.assertEqual(getCond('10000000000').lower(), 'steam', "Датчик неисправен")
	
# Тест проходит если getCond возвращает ошибку
	def test_lit(self):
		self.assertEqual(getCond('test').lower(), 'response error', "Датчик неисправен")
		self.assertEqual(getCond('123test').lower(), 'response error', "Датчик неисправен")
		self.assertEqual(getCond('test34').lower(), 'response error', "Датчик неисправен")
	
if __name__ == '__main__':
	unittest.main()

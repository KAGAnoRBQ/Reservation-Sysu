import os
import sys
import json
import unittest
import requests

class PeriodTest(unittest.TestCase):
	def setUp(self):
		self.url = "http://127.0.0.1:5000/api/period/"
	
	def test_add_period(self):
		url = self.url + 'period_add/'
		print("\n")
		print ("add url:", url)
		data = {
			'period_class_name': 'class 1',
			'period_class_description': 'description for class1',
		}
		print ("add request data:\n", data)
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		print ("add return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
		data = {
			'period_class_name': 'class 2',
			'period_class_description': 'description for class2',
		}
		print ("add request data:\n", data)
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		print ("add return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
	
	def test_delete_period(self):
		url = self.url + 'period_query/?period_class_id=1'
		print ("query url:", url)
		res = requests.get(url)
		res_message = json.loads(res.text)
		print ("query return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
		print ("res_message data:", res_message["data"])
		period_id = int(res_message['data'][0]['id'])
		print("\n")

		url = self.url + 'period_query/'
		print ("query url:", url)
		res = requests.get(url)
		res_message = json.loads(res.text)
		print ("query return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
		print ("res_message data:", res_message["data"])
		period_id = int(res_message['data'][0]['id'])
		print("\n")

		url = self.url + 'period_delete/'
		print ("delete url:", url)
		data = {
			'id': period_id,
		}
		print ("delete request data:\n", data)
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		print ("delete return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
		
		period_id = int(res_message['data'][1]['id'])
		url = self.url + 'period_delete/'
		print ("delete url:", url)
		data = {
			'id': period_id,
		}
		print ("delete request data:\n", data)
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		print ("delete return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)

if __name__ == "__main__":
	suite = unittest.TestSuite() 
	tests = [
		PeriodTest("test_add_period"), 
		PeriodTest("test_delete_period"), 
	] 
	suite.addTests(tests) 
	runner = unittest.TextTestRunner(verbosity=2) 
	runner.run(suite)
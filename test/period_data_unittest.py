import os
import sys
import json
import unittest
import requests

class PeriodTest(unittest.TestCase):
	def setUp(self):
		self.url = "http://127.0.0.1:5000/api/period_data/"
	
	def test_add_period_data(self):
		url = self.url + 'add/'
		print("\n")
		print ("add url:", url)
		data = {
			'period_class_id': 1,
			'start_time': '2018-01-01 00:00:00',
			'end_time': '2018-01-01 01:00:00',
		}
		print ("add request data:\n", data)
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		print ("add return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
	
	def test_delete_period_data(self):
		url = self.url + 'query/?period_class_id=1'
		print ("query url:", url)
		res = requests.get(url)
		res_message = json.loads(res.text)
		print ("query return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
		period_id = int(res_message['data'][0]['id'])
		url = self.url + 'delete/'
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
		PeriodTest("test_add_period_data"), 
		PeriodTest("test_delete_period_data"), 
	] 
	suite.addTests(tests) 
	runner = unittest.TextTestRunner(verbosity=2) 
	runner.run(suite)
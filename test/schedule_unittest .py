import os
import sys
import json
import unittest
import requests

class ScheduleTest(unittest.TestCase):
	def setUp(self):
		self.url = "http://127.0.0.1:5000/api/schedule/"
	
	def test_add_schedule(self):
		url = self.url + 'add/'
		data = {
            'court_id': 1,
			'date': '2018-01-01 00:00:00',
			'total': 1,
            'order_count': 1,
            'occupied_count': 1,
            'visible': 0,
            'enabled': 0,
		}
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		self.assertEqual(res_message['success'], True)
	
	def test_delete_schedule(self):
		url = self.url + 'query/'
		res = requests.post(url)
		res_message = json.loads(res.text)
		self.assertEqual(res_message['success'], True)
		period_id = int(res_message['data'][0]['id'])
		url = self.url + 'delete/'
		data = {
			'id': period_id,
		}
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		self.assertEqual(res_message['success'], True)

if __name__ == "__main__":
	suite = unittest.TestSuite() 
	tests = [
		ScheduleTest("test_add_schedule"), 
		ScheduleTest("test_delete_schedule"), 
	] 
	suite.addTests(tests) 
	runner = unittest.TextTestRunner(verbosity=2) 
	runner.run(suite)
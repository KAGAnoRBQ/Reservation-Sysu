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
		print("\n")
		print ("add url:", url)
		data = {
            'court_id': 1,
			'date': '2018-01-01 00:00:00',
			'total': 1,
            'order_count': 1,
            'occupied_count': 1,
            'visible': 0,
            'enabled': 0,
		}
		print ("add request data:\n", data)
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		print ("add return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)

		url = self.url + 'add/'
		print("\n")
		print ("add url:", url)
		data = {
            'court_id': 2,
			'date': '2018-01-01 00:00:00',
			'total': 1,
            'order_count': 1,
            'occupied_count': 1,
            'visible': 0,
            'enabled': 0,
		}
		print ("add request data:\n", data)
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		print ("add return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
	
	def test_delete_schedule(self):
		url = self.url + 'query/'
		print ("query url:", url)
		res = requests.get(url)
		res_message = json.loads(res.text)
		print ("query return message:\n", res_message)
		print("\n")

		url = self.url + 'query/?court_id=1'
		print ("query url:", url)
		res = requests.get(url)
		res_message = json.loads(res.text)
		print ("query return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
		period_id = int(res_message['data'][0]['id'])


		url = self.url + 'delete/'
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
		url = self.url + 'delete/'
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
		ScheduleTest("test_add_schedule"), 
		# ScheduleTest("test_delete_schedule"), 
	] 
	suite.addTests(tests) 
	runner = unittest.TextTestRunner(verbosity=2) 
	runner.run(suite)

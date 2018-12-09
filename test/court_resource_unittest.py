import os
import sys
import json
import unittest
import requests

class CourtResourceTest(unittest.TestCase):
	def setUp(self):
		self.url = "http://127.0.0.1:5000/api/court_resource/"
	
	def test_add_court_resource(self):
		url = self.url + 'add/'
		print("\n")
		print ("add url:", url)
		data = {
			'date': '2018-01-01 00:00:00',
			'period_id': 1,
			'court_id': 1,
			'court_number': 1,
			'occupied': 0,
			'max_order_count': 1,
			'order_count': 1,
		}
		print ("add request data:\n", data)
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		print ("add return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
	
	def test_delete_court_resource(self):
		url = self.url + 'query/?court_id=1'
		print ("query url:", url)
		res = requests.get(url)
		res_message = json.loads(res.text)
		print ("query return message:\n", res_message)
		print("\n")
		self.assertEqual(res_message['success'], True)
		period_id = int(res_message['data'][0]['id'])

		url = self.url + 'query_name_by_id/?court_id=2&gym_id=2'
		print ("query_name_by_id url:", url)
		res = requests.get(url)
		res_message = json.loads(res.text)
		print ("query_name_by_id return message:\n", res_message)
		print("\n")

		url = self.url + 'query_name_by_id/?court_id=1&gym_id=1'
		print ("query_name_by_id url:", url)
		res = requests.get(url)
		res_message = json.loads(res.text)
		print ("query_name_by_id return message:\n", res_message)
		print("\n")

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
		CourtResourceTest("test_add_court_resource"), 
		CourtResourceTest("test_delete_court_resource"), 
	] 
	suite.addTests(tests) 
	runner = unittest.TextTestRunner(verbosity=2) 
	runner.run(suite)
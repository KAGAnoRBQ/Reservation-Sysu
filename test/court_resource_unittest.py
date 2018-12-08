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
		data = {
			'date': '2018-01-01 00:00:00',
			'period_id': 1,
			'court_id': 1,
			'court_number': 1,
			'occupied': 0,
			'max_order_count': 1,
			'order_count': 1,
		}
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		print (res_message)
		self.assertEqual(res_message['success'], True)
	
	def test_delete_court_resource(self):
		url = self.url + 'query/?court_id=1'
		res = requests.get(url)
		print (res.text)
		res_message = json.loads(res.text)
		print (res_message)
		self.assertEqual(res_message['success'], True)
		period_id = int(res_message['data'][0]['id'])
		url = self.url + 'delete/'
		data = {
			'id': period_id,
		}
		res = requests.post(url, data)
		res_message = json.loads(res.text)
		print (res_message)
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
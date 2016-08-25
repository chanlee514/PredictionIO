#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pio_tests.integration import BaseTestCase, AppContext
from utils import AppEngine, pjoin, items_in_category
import json

class ScalaParallelEcommercerecommendationTest(BaseTestCase):

	def setUp(self):
		self.log.info("Setting up the engine")
		template_path = "https://github.com/chanlee514/template-scala-parallel-ecommercerecommendation"
		engine_json_path = pjoin(
		    self.test_context.data_directory,
		    "scala_parallel_ecommercerecommendation_test/engine.json")
		app_context = AppContext(
		    name="MyApp",
		    template=template_path,
		    engine_json_path=engine_json_path)
		self.app = AppEngine(self.test_context, app_context)

		self.training_data_path = pjoin(
		    self.test_context.data_directory,
		    "scala_parallel_ecommercerecommendation_test/training_data.json")

	def runTest(self):
		self.log.info("Adding a new application")
		self.app.new()

		self.log.info("Sending 4 test events")
		event1 = {
		  'event' : '$set',
		  'entityType' : 'user',
		  'entityId' : 'u0',
		  'eventTime' : '2014-11-02T09:39:45.618-08:00'
		}
		event2 = {
		  'event' : '$set',
		  'entityType' : 'item',
		  'entityId' : 'i0',
		  'properties' : {
		    'categories' : ['c1', 'c2']
		  },
		  'eventTime' : '2014-11-02T09:39:45.618-08:00'
		}
		event3 = {
		  'event' : 'view',
		  'entityType' : 'user',
		  'entityId' : 'u0',
		  'targetEntityType' : 'item',
		  'targetEntityId' : 'i0',
		  'eventTime' : '2014-11-10T12:34:56.123-08:00'
		}
		event4 = {
		  'event' : 'buy',
		  'entityType' : 'user',
		  'entityId' : 'u0',
		  'targetEntityType' : 'item',
		  'targetEntityId' : 'i0',
		  'eventTime' : '2014-11-10T13:00:00.123-08:00'
		}
		for e in [event1, event2, event3, event4]:
			self.assertEqual(201, self.app.send_event(e).status_code)

		self.log.info("Checking the number of events stored on the server")
		r = self.app.get_events()
		self.assertEqual(200, r.status_code)
		self.assertEqual(4, len(r.json()))

		self.log.info("Importing sample events")
		events = json.loads(open(self.training_data_path).read())
		self.app.import_events_batch(events)

		self.log.info("Checking the number of events stored on the server after the update")
		r = self.app.get_events(params={'limit': -1})
		self.assertEqual(200, r.status_code)
		self.assertEqual(len(events) + 4, len(r.json()))

		self.log.info("Building an engine...")
		self.app.build()
		self.log.info("Training...")
		self.app.train()
		self.log.info("Deploying and waiting 15s for it to start...")
		self.app.deploy(wait_time=15)

		self.log.info("Sending a single query and checking results")
		r = self.app.query({ "user": 'u1', "num": 4 })
		self.assertEqual(200, r.status_code)
		self.assertEqual(4, len(r.json()['itemScores']))

		self.log.info("Checking constraint \"unavailableItems\"")
		unavailableItems = ["i4", "i14", "i11"]
		self.app.send_event({
			  "event": "$set",
			  "entityType": "constraint",
			  "entityId": "unavailableItems",
			  "properties": {
			    "items": unavailableItems,
			  },
			  "eventTime": "2015-02-17T02:11:21.934Z" })
		r = self.app.query({
				"user": "u1",
				"num": 4 })
		for i in r.json()['itemScores']:
			self.assertNotIn(i['item'], unavailableItems)

		self.log.info("Unset constraint \"unavailableItems\"")
		self.app.send_event({
				"event" : "$set",
				"entityType" : "constraint",
				"entityId" : "unavailableItems",
				"properties" : {
				  "items": [],
				},
				"eventTime" : "2015-02-18T02:11:21.934Z" })

		self.log.info("Recommend items in selected categories")
		possibleItems = items_in_category(events, ["c3", "c4"])
		r = self.app.query({
				'user': "u1",
				'num': 4,
				'categories': ["c3", "c4"] })
		for i in r.json()['itemScores']:
			self.assertIn(i['item'], possibleItems)

		self.log.info("Whitelist recommended items")
		whiteList = ["i1", "i2", "i3", "i21", "i22", "i23", "i24", "i25"]
		r = self.app.query({
				'user': "u1",
				'num': 4,
				'whiteList': whiteList })
		for i in r.json()['itemScores']:
			self.assertIn(i['item'], whiteList)

		self.log.info("Blacklist recommended items")
		blackList = ["i21", "i26", "i40"]
		r = self.app.query({
				'user': "u1",
				'num': 4,
				'categories': ["c4", "c3"],
				'blackList': blackList })
		for i in r.json()['itemScores']:
			self.assertNotIn(i['item'], blackList)

	def tearDown(self):
		self.log.info("Stopping deployed engine")
		self.app.stop()
		self.log.info("Deleting all related data")
		self.app.delete_data()
		self.log.info("Removing an app")
		self.app.delete()

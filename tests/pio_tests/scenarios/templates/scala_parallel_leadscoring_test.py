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
from utils import AppEngine, pjoin
import json

class ScalaParallelLeadscoringTest(BaseTestCase):

	def setUp(self):
		self.log.info("Setting up the engine")
		template_path = "https://github.com/chanlee514/template-scala-parallel-leadscoring"
		engine_json_path = pjoin(
			self.test_context.data_directory, "scala_parallel_leadscoring_test/engine.json")
		app_context = AppContext(
				name="MyApp",
				template=template_path,
				engine_json_path=engine_json_path)
		self.app = AppEngine(self.test_context, app_context)

		self.training_data_path = pjoin(
		    self.test_context.data_directory,
		    "scala_parallel_leadscoring_test/training_data.json")

	def runTest(self):
		self.log.info("Adding a new application")
		self.app.new()

		self.log.info("Sending two test events")
		event1 = {
		  'event' : 'view',
		  'entityType' : 'user',
		  'entityId' : 'u0',
		  'targetEntityType' : 'page',
		  'targetEntityId' : 'example.com/page0',
		  'properties' : {
		    'sessionId' : 'akdj230fj8ass',
		    'referrerId' : 'referrer0.com',
		    'browser' : 'Firefox'
		  },
		  'eventTime' : '2014-11-02T09:39:45.618-08:00'
		}
		event2 = {
		  'event' : 'buy',
		  'entityType' : 'user',
		  'entityId' : 'u0',
		  'targetEntityType' : 'item',
		  'targetEntityId' : 'i0',
		  'properties' : {
		    'sessionId' : 'akdj230fj8ass'
		  },
		  'eventTime' : '2014-11-02T09:42:00.123-08:00'
		}
		for e in [event1, event2]:
			self.assertEqual(201, self.app.send_event(e).status_code)

		self.log.info("Checking the number of events stored on the server")
		r = self.app.get_events()
		self.assertEqual(200, r.status_code)
		self.assertEqual(2, len(r.json()))

		self.log.info("Importing sample events")
		events = json.loads(open(self.training_data_path).read())
		self.app.import_events_batch(events)

		self.log.info("Building an engine...")
		self.app.build()
		self.log.info("Training...")
		self.app.train()
		self.log.info("Deploying and waiting 15s for it to start...")
		self.app.deploy(wait_time=15)

		self.log.info("Sending a sample query and checking results")
		r = self.app.query({
			'landingPageId' : 'example.com/page9',
			'referrerId' : 'referrer10.com',
			'browser': 'Firefox' })
		self.assertEqual(200, r.status_code)
		self.assertIsNotNone(r.json()['score'])

	def tearDown(self):
		self.log.info("Stopping deployed engine")
		self.app.stop()
		self.log.info("Deleting all related data")
		self.app.delete_data()
		self.log.info("Removing an app")
		self.app.delete()

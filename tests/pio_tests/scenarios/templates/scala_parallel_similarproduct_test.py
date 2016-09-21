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

class ScalaParallelSimilarproductTest(BaseTestCase):

  def setUp(self):
    self.log.info("Setting up the engine")
    template_path = "https://github.com/chanlee514/template-scala-parallel-similarproduct"
    engine_json_path = pjoin(
      self.test_context.data_directory, "scala_parallel_similarproduct_test/engine.json")
    app_context = AppContext(
        name="MyApp",
        template=template_path,
        engine_json_path=engine_json_path)
    self.app = AppEngine(self.test_context, app_context)

    self.training_data_path = pjoin(
        self.test_context.data_directory,
        "scala_parallel_similarproduct_test/training_data.json")

  def runTest(self):
    self.log.info("Adding a new application")
    self.app.new()

    self.log.info("Importing sample events")
    events = json.loads(open(self.training_data_path).read())
    self.app.import_events_batch(events)

    self.log.info("Building an engine...")
    self.app.build()
    self.log.info("Training...")
    self.app.train()
    self.log.info("Deploying and waiting 15s for it to start...")
    self.app.deploy(wait_time=15)

    self.log.info("Recommend 4 items similar to item 'i1'")
    r = self.app.query({ 'items': ["i1"], 'num': 4 })
    self.assertEqual(r.status_code, 200)
    itemScores = r.json()['itemScores']
    self.assertEqual(len(itemScores), 4)
    self.assertIsNotNone(itemScores[0]['item'])
    self.assertGreaterEqual(itemScores[0]['score'], 0)

    self.log.info("Recommend 10 items similar to item 'i1' and 'i3'")
    r = self.app.query({
        'items': ["i1", "i3"],
        'num': 10 })
    self.assertEqual(len(r.json()['itemScores']), 10)

    # Test various param requirements
    self.log.info("Recommend items in selected categories")
    possibleItems = items_in_category(events, ["c3", "c4"])
    r = self.app.query({
        'items': ["i1", "i3"],
        'num': 10,
        'categories': ["c3", "c4"] })
    for i in r.json()['itemScores']:
      self.assertIn(i['item'], possibleItems)

    self.log.info("Whitelist recommended items")
    whiteList = ["i21", "i26", "i40"]
    r = self.app.query({
      'items': ["i1", "i3"],
      'num': 10,
      'categories': ["c4", "c3"],
      'whiteList': whiteList })
    for i in r.json()['itemScores']:
      self.assertIn(i['item'], whiteList)

    self.log.info("Blacklist recommended items")
    blackList = ["i21", "i26", "i40"]
    r = self.app.query({
        'items': ["i1", "i3"],
        'num': 10,
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

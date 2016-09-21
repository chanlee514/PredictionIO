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

class ScalaParallelVanillaTest(BaseTestCase):

  def setUp(self):
    self.log.info("Setting up the engine")
    template_path = "https://github.com/chanlee514/template-scala-parallel-vanilla"
    engine_json_path = pjoin(
        self.test_context.data_directory, "scala_parallel_vanilla_test/engine.json")
    app_context = AppContext(
        name="MyApp",
        template=template_path,
        engine_json_path=engine_json_path)
    self.app = AppEngine(self.test_context, app_context)

  def runTest(self):
    self.log.info("Adding a new application")
    self.app.new()
    self.log.info("Building an engine...")
    self.app.build()
    self.log.info("Training...")
    self.app.train()
    self.log.info("Deploying and waiting 15s for it to start...")
    self.app.deploy(wait_time=15)

    self.log.info("Sending a test query")
    r = self.app.query({ "q": "foo" })
    self.assertEqual(200, r.status_code)
    self.assertDictEqual({ "p": "0-foo" }, r.json())

  def tearDown(self):
    self.log.info("Stopping deployed engine")
    self.app.stop()
    self.log.info("Deleting all related data")
    self.app.delete_data()
    self.log.info("Removing an app")
    self.app.delete()

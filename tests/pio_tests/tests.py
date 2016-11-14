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

import os
import sys
import unittest
import argparse
import logging
import time
from xmlrunner import XMLTestRunner
import pio_tests.globals as globals
from utils import srun_bg
from pio_tests.integration import TestContext
from pio_tests.scenarios import *
from pio_tests.scenarios.templates import *


TESTS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
ENGINE_DIRECTORY = os.path.join(TESTS_DIRECTORY, "engines")
DATA_DIRECTORY = os.path.join(TESTS_DIRECTORY, "data")
# ================= ADD TEST NAME HERE!!! =================
TEST_NAMES = [
  'BasicAppUsecases',
  'EventserverTest',
  'AttributeBasedClassifierTest',
  'EcomRecommenderTest',
  'JavaEcomRecommenderTest',
  'RecommenderTest',
  'SimilarProductTest',
  'SkeletonTest',
  'TextClassifierTest'
]
LOGGING_FORMAT = '[%(levelname)s] %(module)s %(asctime)-15s: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)

parser = argparse.ArgumentParser(description='Integration tests for PredictionIO')
parser.add_argument('--eventserver-ip', default='0.0.0.0')
parser.add_argument('--eventserver-port', type=int, default=7070)
parser.add_argument('--no-shell-stdout', action='store_true',
    help='Suppress STDOUT output from shell executed commands')
parser.add_argument('--no-shell-stderr', action='store_true',
    help='Suppress STDERR output from shell executed commands')
parser.add_argument('--logging', action='store', choices=['INFO', 'DEBUG', 'NO_LOGGING'],
    default='INFO', help='Choose the logging level')
parser.add_argument('--tests', nargs='*', type=str,
    default=['all'],
    help='Names of the tests to execute. By default all tests will be checked.')


def get_tests(names, test_context):
  """ Returns test objects with matching names
    Args:
      names: list of valid test names provided as command-line arguments,
          default value is ['all']
      test_context (obj: `TestContext`)
  """
  test_names = TEST_NAMES if names==["all"] else names
  return [eval(name)(test_context) for name in test_names \
      if name in test_names]


if __name__ == "__main__":
  args = vars(parser.parse_args())

  if args.get('no_shell_stdout'):
    globals.SUPPRESS_STDOUT = True
  if args.get('no_shell_stderr'):
    globals.SUPPRESS_STDERR = True

  # Set up logging level
  log_opt = args['logging']
  logger = logging.getLogger(globals.LOGGER_NAME)
  if log_opt == 'INFO':
    logger.level = logging.INFO
  elif log_opt == 'DEBUG':
    logger.level = logging.DEBUG

  # Create `TestContext` object
  test_context = TestContext(
      ENGINE_DIRECTORY, DATA_DIRECTORY,
      args['eventserver_ip'], int(args['eventserver_port']))

  # Get tests to execute
  test_names = args.get('tests')
  test_objects = get_tests(test_names, test_context)
  if not test_objects:
    logger.error("Cannot identify any tests with name in {}. Aborting...".format(
        test_names))
    sys.exit(1)
  logger.info("Executing tests: {}...".format(test_objects))

  # Execute tests
  es_wait_time = 25
  logger.info("Starting eventserver and waiting {}s to initialize...".format(
      es_wait_time))
  event_server_process = srun_bg('pio eventserver --ip {} --port {}'
      .format(test_context.es_ip, test_context.es_port))
  time.sleep(es_wait_time)
  result = XMLTestRunner(verbosity=2, output='test-reports').run(
      unittest.TestSuite(test_objects))
  event_server_process.kill()

  if not result.wasSuccessful():
    sys.exit(1)

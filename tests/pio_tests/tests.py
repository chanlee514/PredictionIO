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

from os import path
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

TESTS_DIRECTORY = path.abspath(path.dirname(__file__))
ENGINE_DIRECTORY = path.join(TESTS_DIRECTORY, 'engines')
DATA_DIRECTORY = path.join(TESTS_DIRECTORY, 'data')

TEST_NAMES = [
  'basic_app_usecases', 'eventserver_test',
  'java_parallel_ecommercerecommendation_test', 'scala_parallel_classification_test',
  'scala_parallel_complementarypurchase_test', 'scala_parallel_ecommercerecommendation_test',
  'scala_parallel_leadscoring_test', 'scala_parallel_productranking_test',
  'scala_parallel_recommendation_test', 'scala_parallel_similarproduct_test',
  'scala_parallel_textclassification_test', 'scala_parallel_vanilla_test'
]
DEFAULT_TESTS = ['basic_app_usecases', 'eventserver_test', 'scala_parallel_recommendation_test']

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
    default=DEFAULT_TESTS,
    help='Names (starting characters of names) of the tests to execute, "all" to execute all tests.')

def autocomplete_test_name(name):
  return [x for x in TEST_NAMES if x.startswith(name)]

# Returns test object matching name
def get_test(name, context):
  if name not in TEST_NAMES:
    logger.error("{} is not a correct test name.".format(name))
    sys.exit(1)
  camelcase_name = "".join(x.title() for x in name.split('_'))
  return eval(camelcase_name)(context)

if __name__ == "__main__":
  args = vars(parser.parse_args())

  if args.get('no_shell_stdout'):
    globals.SUPPRESS_STDOUT = True
  if args.get('no_shell_stderr'):
    globals.SUPPRESS_STDERR = True

  # Set up logging
  log_opt = args['logging']
  logger = logging.getLogger(globals.LOGGER_NAME)
  if log_opt == 'INFO':
    logger.level = logging.INFO
  elif log_opt == 'DEBUG':
    logger.level = logging.DEBUG

  # Set up test context
  test_context = TestContext(
      ENGINE_DIRECTORY, DATA_DIRECTORY,
      args['eventserver_ip'], int(args['eventserver_port']))

  # Get tests to execute
  test_name_arg = args.get('tests')
  test_names = TEST_NAMES if test_name_arg==['all'] \
      else sum([autocomplete_test_name(n) for n in test_name_arg], [])
  if len(test_names)==0:
    logger.error("No tests matching the provided name {}".format(test_name_arg))
    sys.exit(1)

  tests = [get_test(name, test_context) for name in test_names]
  logger.info("Executing tests: {}".format(test_names))

  # Actual tests execution
  es_wait_time = 10
  logger.info("Starting eventserver and waiting {}s for it to initialize".format(
      es_wait_time))
  event_server_process = srun_bg('pio eventserver --ip {} --port {}'
      .format(test_context.es_ip, test_context.es_port))
  time.sleep(es_wait_time)
  result = XMLTestRunner(verbosity=2, output='test-reports').run(
                unittest.TestSuite(tests))
  event_server_process.kill()

  if not result.wasSuccessful():
    sys.exit(1)

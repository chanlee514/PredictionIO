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

"""
Generate sample training data for testing lead scoring engine
Modified from import_eventserver.py in
https://github.com/PredictionIO/template-scala-parallel-leadscoring
"""

import random
import uuid
import json

SEED = 3

def generate_events():
  events = []

  random.seed(SEED)
  count = 0
  print("Importing data...")

  # generate 10 users, with user ids u1,u2,....,u10
  user_ids = ["u%s" % i for i in range(1, 10+1)]

  # generate 50 items, with user ids u1,u2,....,u10
  item_ids = ["i%s" % i for i in range(1, 50+1)]

  # generate 20 pageId
  page_ids = ["example.com/page%s" % i for i in range(1, 20+1)]

  # generate 10 referrerId
  refferal_ids = ["referrer%s.com" % i for i in range(1, 10+1)]

  browsers = ["Chrome", "Firefox", "Safari", "Internet Explorer"]

  # for each session
  # simulate user session:
  # generate a session ID
  for loop in range(0, 50):
    session_id = uuid.uuid1().hex
    print("Session {}".format(session_id))
    referrer_id = random.choice(refferal_ids)
    browser = random.choice(browsers)
    uid = random.choice(user_ids)
    page_id = random.choice(page_ids)
    print("User {} lands on page {}, referrer {}, browser {}"\
        .format(uid, page_id, referrer_id, browser))
    events.append({
      'event': "view",
      'entityType': "user",
      'entityId': uid,
      'targetEntityType': "page",
      'targetEntityId': page_id,
      'properties': {
        "sessionId": session_id,
        "referrerId": referrer_id,
        "browser": browser
      }
    })

    # 0 or more page view
    for i in range(0, random.randint(0,2)):
      page_id = random.choice(page_ids)
      print("User {} views page {}".format(uid, page_id))
      events.append({
        'event': "view",
        'entityType': "user",
        'entityId': uid,
        'targetEntityType': "page",
        'targetEntityId': page_id,
        'properties': {
          'sessionId': session_id
        }
      })

    # 1 or more buy
    for i in range(0, random.randint(1,3)):
      item_id = random.choice(item_ids)
      print("User {} buys item {}", uid, item_id)
      events.append({
        'event': "buy",
        'entityType': "user",
        'entityId': uid,
        'targetEntityType': "item",
        'targetEntityId': item_id,
        'properties': {
          'sessionId': session_id,
        }
      })

  with open('training_data.json', 'w') as f:
    json.dump(events, f, indent=2, separators=(',', ': '))

if __name__ == '__main__':
  generate_events()

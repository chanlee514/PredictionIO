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
Generate sample data for Complementary Purchase Engine
Modified from import_eventserver.py in
https://github.com/PredictionIO/template-scala-parallel-complementarypurchase
"""

import random
import uuid
from datetime import datetime
from datetime import timedelta
import pytz
import json

SEED = 3

def import_events():
  random.seed(SEED)

  events = []

  # generate 10 users, with user ids u1,u2,....,u10
  user_ids = ["u%s" % i for i in range(1, 10+1)]

  # randomly generate 4 frequent item set
  item_sets = {}
  for i in range(1, 4+1):
    # each set contain 2 to 4 items
    iids = range(1, random.randint(2, 4)+1)
    item_sets[i] = ["s%si%s" % (i, j) for j in iids]

  # plus 20 other items not in any set.
  other_items = ["i%s" % i for i in range(1, 20+1)]

  # 3 popular item every one buy
  pop_items = ["p%s" % i for i in range(1,3+1)]

  # each user have 5 basket purchases:
  for uid in user_ids:
    base_time = datetime(
      year = 2014,
      month = 10,
      day = random.randint(1,31),
      hour = 15,
      minute = 39,
      second = 45,
      microsecond = 618000,
      tzinfo = pytz.timezone('US/Pacific'))
    seconds = 0
    for basket in range(0, 5):
      # may or may not some random item
      if (random.choice([True, False])):
        buy_items = random.sample(other_items, random.randint(1, 3))
        for iid in buy_items:
          event_time = base_time + timedelta(seconds=seconds, days=basket)
          formatted_time = str(event_time).replace(' ', 'T')
          print("User {} buys item {} at {}".format(uid, iid, formatted_time))
          events.append({
              'event': 'buy',
              'entityType': 'user',
              'entityId': uid,
              'targetEntityType': 'item',
              'targetEntityId': iid,
              'eventTime': formatted_time })
          seconds += 10

      # always buy one popular item
      buy_items = random.sample(pop_items, 1)
      for iid in buy_items:
        event_time = base_time + timedelta(seconds=seconds, days=basket)
        formatted_time = str(event_time).replace(' ', 'T')
        print("User {} buys item {} at {}".format(uid, iid, formatted_time))
        events.append({
            'event': 'buy',
            'entityType': 'user',
            'entityId': uid,
            'targetEntityType': 'item',
            'targetEntityId': iid,
            'eventTime': formatted_time })
        seconds += 10

      # always buy some something from one of the item set
      s = item_sets[random.choice(item_sets.keys())]
      buy_items = random.sample(s, random.randint(2, len(s)))
      for iid in buy_items:
        event_time = base_time + timedelta(seconds=seconds, days=basket)
        formatted_time = str(event_time).replace(' ', 'T')
        print("User {} buys item {} at {}".format(uid, iid,formatted_time))
        events.append({
            'event': 'buy',
            'entityType': 'user',
            'entityId': uid,
            'targetEntityType': 'item',
            'targetEntityId': iid,
            'eventTime': formatted_time })
        seconds += 10

  print("{} events are imported.".format(len(events)))

  # Write to json file
  with open('training_data.json', 'w') as f:
    json.dump(events, f, indent=2, separators=(',', ': '))


if __name__ == '__main__':
  import_events()

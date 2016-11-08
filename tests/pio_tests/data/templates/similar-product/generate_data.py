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
Generate sample data for Similar Product Engine Template
Modified from import_eventserver.py in template
"""
import random
import json

SEED = 3

def import_events():
  random.seed(SEED)
  events = []
  print("Importing data...")

  # Generate 10 users, with user ids u1,u2,....,u10
  user_ids = ["u%s" % i for i in range(1, 11)]
  for user_id in user_ids:
    print("Set user {}".format(user_id))
    events.append({
      'event': '$set',
      'entityType': 'user',
      'entityId': user_id
    })
    
  # Generate 50 items, with item ids i1,i2,....,i50
  # Randomly assign 1 to 4 categories among c1-c6 to items
  categories = ["c%s" % i for i in range(1, 7)]
  item_ids = ["i%s" % i for i in range(1, 51)]
  for item_id in item_ids:
    print("Set item {}".format(item_id))
    events.append({
      'event': '$set',
      'entityType': 'item',
      'entityId': item_id,
      'properties': {
        'categories': random.sample(categories, random.randint(1, 4))
      }
    })

  # Each user randomly viewed 10 items
  for user_id in user_ids:
    for viewed_item in random.sample(item_ids, 10):
      print("User {} views item {}".format(user_id, viewed_item))
      events.append({
        'event': 'view',
        'entityType': 'user',
        'entityId': user_id,
        'targetEntityType': 'item',
        'targetEntityId': viewed_item
      })

  print("{} events are imported".format(len(events)))

  # Write to json file
  with open('data.json', 'w') as f:
    json.dump(events, f, indent=2, separators=(',', ': '))


if __name__ == '__main__':
  import_events()

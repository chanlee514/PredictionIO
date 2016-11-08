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

from pio_tests.scenarios.templates.attribute_based_classifier_test import AttributeBasedClassifierTest
from pio_tests.scenarios.templates.ecom_recommender_test import EcomRecommenderTest
from pio_tests.scenarios.templates.recommender_test import RecommenderTest
from pio_tests.scenarios.templates.skeleton_test import SkeletonTest
from pio_tests.scenarios.templates.similar_product_test import SimilarProductTest
from pio_tests.scenarios.templates.text_classifier_test import TextClassifierTest
from pio_tests.scenarios.templates.java_ecom_recommender_test import JavaEcomRecommenderTest

__all__ = [
	"AttributeBasedClassifierTest",
	"EcomRecommenderTest",
	"RecommenderTest",
	"SkeletonTest",
	"SimilarProductTest",
	"TextClassifierTest",
	"JavaEcomRecommenderTest"
]

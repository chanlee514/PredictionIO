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

from pio_tests.scenarios.templates.java_parallel_ecommercerecommendation_test import JavaParallelEcommercerecommendationTest
from pio_tests.scenarios.templates.scala_parallel_classification_test import ScalaParallelClassificationTest
from pio_tests.scenarios.templates.scala_parallel_complementarypurchase_test import ScalaParallelComplementarypurchaseTest
from pio_tests.scenarios.templates.scala_parallel_ecommercerecommendation_test import ScalaParallelEcommercerecommendationTest
from pio_tests.scenarios.templates.scala_parallel_leadscoring_test import ScalaParallelLeadscoringTest
from pio_tests.scenarios.templates.scala_parallel_productranking_test import ScalaParallelProductrankingTest
from pio_tests.scenarios.templates.scala_parallel_recommendation_test import ScalaParallelRecommendationTest
from pio_tests.scenarios.templates.scala_parallel_similarproduct_test import ScalaParallelSimilarproductTest
from pio_tests.scenarios.templates.scala_parallel_textclassification_test import ScalaParallelTextclassificationTest
from pio_tests.scenarios.templates.scala_parallel_vanilla_test import ScalaParallelVanillaTest

__all__ = [
	"JavaParallelEcommercerecommendationTest", "ScalaParallelClassificationTest",
	"ScalaParallelComplementarypurchaseTest", "ScalaParallelEcommercerecommendationTest",
	"ScalaParallelLeadscoringTest", "ScalaParallelProductrankingTest",
	"ScalaParallelRecommendationTest", "ScalaParallelSimilarproductTest",
	"ScalaParallelTextclassificationTest", "ScalaParallelVanillaTest"
]
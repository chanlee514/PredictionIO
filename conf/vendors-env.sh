#!/bin/bash
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

ELASTICSEARCH_VERSION=1.4.4
HBASE_VERSION=1.0.0

# Build profile scala-2.11
SPARK_VERSION=2.0.2
HADOOP_VERSION=2.7.3
HADOOP_MAJOR=`echo $HADOOP_VERSION | awk -F. '{print $1 "." $2}'`
SPARK_DIR=spark-${SPARK_VERSION}-bin-hadoop${HADOOP_MAJOR}
SPARK_ARCHIVE=${SPARK_DIR}.tgz
SPARK_DOWNLOAD=http://d3kbcqa49mib13.cloudfront.net/${SPARK_ARCHIVE}
# ELASTICSEARCH_DOWNLOAD=https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-${ELASTICSEARCH_VERSION}.tar.gz

# Build profile scala-2.10
OLD_SPARK_VERSION=1.6.2
OLD_HADOOP_VERSION=2.6.4
OLD_HADOOP_MAJOR=`echo $OLD_HADOOP_VERSION | awk -F. '{print $1 "." $2}'`
OLD_SPARK_DIR=spark-${OLD_SPARK_VERSION}-bin-hadoop${OLD_HADOOP_MAJOR}
OLD_SPARK_ARCHIVE=${OLD_SPARK_DIR}.tgz
OLD_SPARK_DOWNLOAD=http://d3kbcqa49mib13.cloudfront.net/${OLD_SPARK_ARCHIVE}
# OLD_ELASTICSEARCH_DOWNLOAD=https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${OLD_ELASTICSEARCH_VERSION}.tar.gz

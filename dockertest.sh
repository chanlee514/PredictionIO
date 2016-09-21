#!/bin/bash
export METADATA_REP=PGSQL
export EVENTDATA_REP=PGSQL
export MODELDATA_REP=PGSQL
export BUILD_TYPE=Integration

source tests/docker-files/env-conf/spark-env.sh && ./tests/script.travis.sh
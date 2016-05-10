#!/usr/bin/env bash

pushd `dirname $0` > /dev/null
cd ../..
PYTHONPATH=`pwd`
popd > /dev/null

${PYTHONPATH}/venv/bin/python3 -m coordinator.broadcast_datetime




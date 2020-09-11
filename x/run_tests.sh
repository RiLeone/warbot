#!/bin/bash
# Call this file from <PRJ_ROOT> as ./x/run_tests.sh
cd src/test/
python3 -m unittest discover -v

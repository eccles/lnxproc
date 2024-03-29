#!/bin/sh
# 
# returns python3 repo to pristine state
#

./buildscripts/api.sh stop

find -name '*,cover' -delete
find -depth -name '__pycache__' -type d -exec rm -rf {} \; -print
find -name '.coverage' -delete
find -name '*.py[cod]' -delete

rm -f api api_id \
      .ash_history \
      .bash_history \
      builder \
      coverage.xml \
      .python_history

rm -rf build/ \
       .cache/ \
       dist/ \
       *.egg-info/ \
       htmlcov/ \
       .local/ \
       .pylint.d/ \
       results/


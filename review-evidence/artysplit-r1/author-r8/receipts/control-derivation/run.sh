#!/bin/bash
# The no-disposition control: round 7's 147 traces, measured with every srp-kept/srp-bound record counted.
set -u
R=$VALIDATION_STORAGE/r8/control; T=$VALIDATION_STORAGE/r7/tools
python3 -B $T/census.py $R/census-no-disposition.json $VALIDATION_STORAGE/r7/final-census/*/results > $R/census.log 2>&1; echo "census $?"
python3 -B $T/merge-census.py $R/merged-no-disposition.json $VALIDATION_STORAGE/r6g/preview/merged-preview.json $R/census-no-disposition.json > $R/merge.log 2>&1; echo "merge $?"
python3 -B $T/derive-own.py $R/merged-no-disposition.json > $R/derive-no-disposition.json 2> $R/derive.err; echo "derive $?"

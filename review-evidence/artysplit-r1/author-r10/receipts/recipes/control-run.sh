#!/bin/bash
# The no-disposition control: this round's 159 traces with every srp-kept/srp-bound record counted.
set -u
R=$VALIDATION_STORAGE/r10; T=$R/tools; C=$R/control
cd $SOURCE
echo "census kept (run 1)"
python3 -B $T/merge-census.py $C/merged-no-disposition.json $VALIDATION_STORAGE/r9/control/merged-no-disposition.json $C/census-no-disposition.json > $C/merge.log 2>&1; echo "merge $?"
python3 -B $T/derive-own.py $C/merged-no-disposition.json > $C/derive-no-disposition.json 2> $C/derive.err; echo "derive $?"

#!/bin/bash
set -u
R=$VALIDATION_STORAGE/r10; T=$R/tools; D=$R/derive
cd $SOURCE
python3 -I -B tb/verilator/ctrl_service_budget/kept_grade.py $R/final-census/none > $D/kept-grade.log 2>&1; echo "kept_grade $?"
python3 -B $T/census7.py $D/census.json $R/final-census/*/results > $D/census.log 2>&1; echo "census $?"
python3 -B $T/merge-census.py $D/merged-census.json $VALIDATION_STORAGE/r9/derive/merged-census.json $D/census.json > $D/merge.log 2>&1; echo "merge $?"
python3 -B $T/derive-own.py $D/merged-census.json > $D/derived-model.json 2> $D/derive.err; echo "derive $?"

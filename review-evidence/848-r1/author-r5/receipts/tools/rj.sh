#!/usr/bin/env bash
# rj.sh <job> [budget] [step limit]: one foreground pass of one docs.yml job on its clean clone.
HEAD=697e17a48e00073c9cd40f40049cd1f0f8ddb033
T=$HOME/milan-fpga-management/2026-09-23/848-a739d/receipts/tools
R=$VALIDATION_STORAGE/848-a739d/docsyml-$HEAD
RUN_BUDGET=${2:-400} RUN_STEP_LIMIT=${3:-575} python3 "$T/run_docs_yml.py" "$HEAD" "$1" "$R"
echo "job $1 runner rc=$?"

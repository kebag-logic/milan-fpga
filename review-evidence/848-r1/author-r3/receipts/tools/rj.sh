#!/usr/bin/env bash
# rj.sh <job> [budget] [step limit]: one foreground pass of one docs.yml job on its clean clone.
HEAD=171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22
T=<host-path>
R=$VALIDATION_STORAGE/848-a739c/docsyml-$HEAD
RUN_BUDGET=${2:-400} RUN_STEP_LIMIT=${3:-575} python3 "$T/run_docs_yml.py" "$HEAD" "$1" "$R"
echo "job $1 runner rc=$?"

#!/usr/bin/env bash
# docs_chain_full.sh <head>: every docs.yml job of the replay at <head>, in needs order; each job's
# result.json is the evidence, this log only its order and exit codes.
set -u
H=$1; cd "$(dirname "$0")"
job() { echo "$(date +%T) start $*"; python3 ci_replay.py job "$H" docs "$@" > /dev/null 2>&1; local rc=$?; echo "$(date +%T) $* rc $rc"; }
job wire-accountability 0 & job docs-check-no-git 0 & job ci-fail-fast 0 & job docs-gates-0 0 & job docs-gates-1 0 & job docs-gates-2 0 &
while [ "$(jobs -r | wc -l)" -gt 0 ]; do sleep 20; done
job docs-check 0
job ci-manifest 0
job ci-cancel-tail 0
echo "$(date +%T) docs chain done"

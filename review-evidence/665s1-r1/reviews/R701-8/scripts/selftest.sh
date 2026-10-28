#!/bin/bash
# The CPU budget harness's self-test and mutants at the review clone's head.
. "$(dirname "$0")/env.sh"
cd "$CHECKOUT" && echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain | wc -l)"
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test; echo "rc=$?"

#!/bin/bash
# R824-1's ci_run.sh, unchanged, with the calling environment its env.sh assumes: clang-18 and the Mermaid CLI on PATH.
set -u
S=<scratch> P=<scratch>/r824
export TOOLS=<tools> TMPDIR=$S/tmp
export PATH=<tools>/clang-18/bin:$S/mermaid/node_modules/.bin:<node>/bin:$PATH
H=$(git -C $S/trees/head rev-parse HEAD)
bash $P/scripts/ci_run.sh <lanes>/tsn-c-stack-32-walk $H $P/scratch/ci-head-2 > $P/receipts/ci-run-2.driver.log 2>&1; echo $? > $P/receipts/ci-run-2.driver.rc

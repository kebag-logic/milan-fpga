#!/bin/bash
# iterate.sh: in the replica's venv, the wire-timing step again after installing one more package (diagnosis only)
R=<scratch>/replica
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true HOME=$R/home PYTHONHASHSEED=0 RUNNER_TEMP=$R/runner_temp TMPDIR=$R/tmp
export PATH=$RUNNER_TEMP/litex-venv/bin:<data>/tools/pinned-verilator-5.050:/usr/local/bin:/usr/bin:/bin
cd $R/wt
[ -n "$1" ] && python3 -m pip install --quiet "$1"
start=$(date +%s)
WIRE_JOBS=4 taskset -c 56-59 python3 tb/verilator/ctrl_wire_timing/run.py --ci --build-dir "$RUNNER_TEMP/wire-timing-iter"
echo "rc=$? wall $(( $(date +%s) - start )) s"

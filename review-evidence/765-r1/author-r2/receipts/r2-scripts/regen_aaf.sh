#!/bin/bash
# Regenerate hdl/ieee1722/avtp/doc/TEST_RESULTS.md in the lane worktree through the AAF campaign, at the CI tsn-gen pin.
export PATH=<scratch>/venv/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export TMPDIR=<scratch>/r2/tmp
export TSN_GEN_ROOT=<scratch>/tsn-gen
O=<scratch>/r2/regen; mkdir -p $O $TMPDIR
cd <lane>
{ echo "lane HEAD $(git rev-parse HEAD) (worktree carries the uncommitted round-2 edits)"; echo "tsn-gen $(git -C $TSN_GEN_ROOT rev-parse HEAD)"; echo "python $(python3 --version 2>&1)"; verilator --version; } > $O/HEAD.txt
git status --short > $O/status-before.txt
date -Is > $O/start
make -C tb/verilator/tsn_fuzz aaf PY=python3 > $O/aaf.log 2>&1
echo "rc=$?" > $O/rc
date -Is > $O/end
git status --short > $O/status-after.txt
git diff -- hdl/ieee1722/avtp/doc/TEST_RESULTS.md > $O/TEST_RESULTS.diff

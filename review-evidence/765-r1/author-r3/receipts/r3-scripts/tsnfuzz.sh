#!/bin/bash
# tsn_fuzz campaigns at the CI tsn-gen pin, in the clean clone at the lane head.
export PATH=<scratch>/venv/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export TMPDIR=<scratch>/r3/tmp
export TSN_GEN_ROOT=<scratch>/tsn-gen
O=<scratch>/r3/tsnfuzz; mkdir -p $O
cd <scratch>/r3/cloneH
{ echo "head $(git rev-parse HEAD)"; echo "tsn-gen $(git -C $TSN_GEN_ROOT rev-parse HEAD)"; echo "python $(python3 --version 2>&1)"; } > $O/HEAD.txt
date -Is > $O/start
make -C tb/verilator/tsn_fuzz > $O/tsnfuzz.log 2>&1
echo "rc=$?" > $O/rc
date -Is > $O/end
git diff > $O/TEST_RESULTS.diff

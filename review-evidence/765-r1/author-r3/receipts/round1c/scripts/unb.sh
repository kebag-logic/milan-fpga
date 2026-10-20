#!/bin/bash
# milan_dp [UNB] mutation campaign (outside the sweep), clean clone at the lane head.
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export TMPDIR=<scratch>/round1c/tmp
O=<scratch>/round1c/unb; mkdir -p $O
cd <scratch>/round1c/cloneH/tb/verilator/milan_dp
echo "head $(git rev-parse HEAD)" > $O/HEAD.txt
date -Is > $O/start
make --no-print-directory unb-mutants > $O/unb-mutants.log 2>&1
echo "rc=$?" > $O/rc
date -Is > $O/end

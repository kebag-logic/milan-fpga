#!/bin/bash
# tsn_fuzz campaigns at the CI tsn-gen pin, in the clean clone at the lane head.
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export TMPDIR=<scratch>/round1c/tmp
export TSN_GEN_ROOT=<base-lane-scratch>/tsn-gen
O=<scratch>/round1c/tsnfuzz; mkdir -p $O
cd <scratch>/round1c/cloneH
{ echo "head $(git rev-parse HEAD)"; echo "tsn-gen $(git -C $TSN_GEN_ROOT rev-parse HEAD)"; } > $O/HEAD.txt
date -Is > $O/start
make -C tb/verilator/tsn_fuzz > $O/tsnfuzz.log 2>&1
echo "rc=$?" > $O/rc
date -Is > $O/end

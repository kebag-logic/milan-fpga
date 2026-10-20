#!/bin/bash
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export TMPDIR=<scratch>/tmp
export TSN_GEN_ROOT=<base-lane-scratch>/tsn-gen
cd <lane>
date -Is > <scratch>/tsnfuzz.start
make -C tb/verilator/tsn_fuzz > <scratch>/tsnfuzz.log 2>&1
echo "rc=$?" > <scratch>/tsnfuzz.rc
date -Is > <scratch>/tsnfuzz.end

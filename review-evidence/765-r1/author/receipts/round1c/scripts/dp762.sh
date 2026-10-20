#!/bin/bash
# [762-DP] wiring mutants at milan_datapath.sv:6308 on obj_dynmap and obj_nxn4c, own clean clone.
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export TMPDIR=<scratch>/round1c/tmp
O=<scratch>/round1c/dp762; mkdir -p $O
cd <scratch>/round1c/cloneP
echo "head $(git rev-parse HEAD)" > $O/HEAD.txt
date -Is > $O/start
make --no-print-directory -C tb/verilator/milan_dp ci-prepare > $O/ci-prepare.log 2>&1
<scratch>/venv/bin/python3 -I <scratch>/round1c/scripts/dp762_mutants.py <scratch>/round1c/cloneP <scratch>/round1c/dp762-work $O dynmap nxn4c > $O/driver.log 2>&1
echo "rc=$?" > $O/rc
date -Is > $O/end

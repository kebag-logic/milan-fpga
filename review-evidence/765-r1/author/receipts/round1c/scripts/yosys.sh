#!/bin/bash
# syn/yosys/run.sh at the lane head, in its clean clone.
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export TMPDIR=<scratch>/round1c/tmp
O=<scratch>/round1c/yosys; mkdir -p $O
cd <scratch>/round1c/cloneH
{ echo "head $(git rev-parse HEAD)"; yosys -V; sv2v --version; } > $O/HEAD.txt 2>&1
date -Is > $O/start
syn/yosys/run.sh > $O/yosys.log 2>&1
echo "rc=$?" > $O/rc
date -Is > $O/end

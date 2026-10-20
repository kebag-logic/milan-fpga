#!/bin/bash
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export TMPDIR=<scratch>/tmp
cd <scratch>/r1b/cloneY
date -Is > ../yosys.start
syn/yosys/run.sh > ../yosys.log 2>&1
echo "rc=$?" > ../yosys.rc
date -Is > ../yosys.end

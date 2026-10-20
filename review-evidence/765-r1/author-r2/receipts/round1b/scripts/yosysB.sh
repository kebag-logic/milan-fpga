#!/bin/bash
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export TMPDIR=<scratch>/tmp
cd <scratch>/r1b/cloneB
date -Is > ../yosysB.start
syn/yosys/run.sh > ../yosysB.log 2>&1
echo "rc=$?" > ../yosysB.rc
date -Is > ../yosysB.end

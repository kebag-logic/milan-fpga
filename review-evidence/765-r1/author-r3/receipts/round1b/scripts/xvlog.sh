#!/bin/bash
export PATH=<home>/Xilinx/2026.1/Vivado/bin:<tools>/pinned-verilator-5.050:$PATH
export TMPDIR=<scratch>/tmp
cd <lane>
date -Is > <scratch>/r1b/xvlog.start
git rev-parse HEAD > <scratch>/r1b/xvlog.commit
flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check > <scratch>/r1b/xvlog.log 2>&1
echo "rc=$?" > <scratch>/r1b/xvlog.rc
date -Is > <scratch>/r1b/xvlog.end

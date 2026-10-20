#!/bin/bash
# xvlog gate at the lane head, under the exclusive Vivado lock.
export PATH=<home>/Xilinx/2026.1/Vivado/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export TMPDIR=<scratch>/round1c/tmp
O=<scratch>/round1c/xvlog; mkdir -p $O
cd <scratch>/round1c/cloneH
git rev-parse HEAD > $O/HEAD.txt
date -Is > $O/start
flock $VIVADO_LOCK <scratch>/venv/bin/python3 scripts/xvlog_gate.py --check > $O/xvlog.log 2>&1
echo "rc=$?" > $O/rc
date -Is > $O/end

#!/bin/bash
# Targeted avtp_rxmon and crf_rx runs on the lane tree; one log and rc each.
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export TMPDIR=<scratch>/tmp
O=<scratch>/r1b/$1; mkdir -p $O
cd <lane>
git rev-parse HEAD > $O/HEAD.txt; git status --short > $O/status.txt
t() { name=$1; shift; date -Is > $O/$name.start; "$@" > $O/$name.log 2>&1; echo "rc=$?" > $O/$name.rc; date -Is > $O/$name.end; }
t crf_rx make -C tb/verilator/crf_rx all &
t avtp_rxmon make -C tb/verilator/avtp_rxmon run &
wait
echo done > $O/ALL.done

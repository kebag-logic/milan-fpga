#!/usr/bin/env bash
export TMPDIR=<runs>/tmp
cd <runs>
python3 -I <tools>/run-review-probes.py <probe-tree> <runs>/probes-1 <tool>/pinned-verilator-5.050/verilator > <runs>/probes-1.out 2>&1
echo $? > <runs>/probes-1.rc

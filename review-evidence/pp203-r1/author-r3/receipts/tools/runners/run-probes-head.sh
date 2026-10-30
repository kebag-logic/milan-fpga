#!/usr/bin/env bash
export TMPDIR=<runs>/tmp
cd <runs>
git -C <work2> rev-parse HEAD > <runs>/probes-head.tree
python3 -I <tools>/run-review-probes.py <work2> <runs>/probes-head <tool>/pinned-verilator-5.050/verilator > <runs>/probes-head.out 2>&1
echo $? > <runs>/probes-head.rc

#!/bin/bash
# avtp_rxmon suite (flat, NX, lockstep N=1/N=8, lockstep_mutants.py, format_mutants.py) in the clean clone.
export PATH=<scratch>/venv/bin:<tools>/pinned-verilator-5.050:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export TMPDIR=<scratch>/r2/tmp
O=<scratch>/r2/rxmon; mkdir -p $O
cd <scratch>/r2/cloneH
{ echo "head $(git rev-parse HEAD)"; echo "python $(python3 --version 2>&1)"; verilator --version; } > $O/HEAD.txt
date -Is > $O/start
make -C tb/verilator/avtp_rxmon run > $O/make_run.log 2>&1
echo "rc=$?" > $O/rc
date -Is > $O/end

#!/bin/bash
# The R673-2 probe (byte copy of the archived script) against the lane head.
export PATH=<scratch>/r3/../venv/bin:$PATH
O=<scratch>/r3/probe; mkdir -p $O
{ echo "head $(git -C <lane> rev-parse HEAD)"; echo "python $(python3 --version 2>&1)"; sha256sum <scratch>/r3/scripts/probe_flat_cpf256.sh; } > $O/HEAD.txt
date -Is > $O/start
sh <scratch>/r3/scripts/probe_flat_cpf256.sh <lane> <scratch>/r3/probe-work <tools>/pinned-verilator-5.050/verilator > $O/probe_flat_cpf256.log 2>&1
echo "rc=$?" > $O/rc
date -Is > $O/end

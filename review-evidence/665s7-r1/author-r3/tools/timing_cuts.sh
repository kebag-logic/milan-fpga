#!/usr/bin/env bash
# timing_cuts.sh: diagnostic for elaborate-gates-1's gate_19 timeouts: test_soc_timing_cuts.py alone, on its own clean
# clone of the head, with the LiteX tree's venv, no wall clock; its verdict and its wall time
set -uo pipefail
export HOME=/data-2/milan/tmp/665s7-a757c/home TMPDIR=/data-2/milan/tmp/665s7-a757c/tmp PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:/usr/local/bin:/usr/bin:/bin
cd /data-2/milan/tmp/665s7-a757c/gates/litexsim/sw/litex
start=$(date +%s)
python3 test_soc_timing_cuts.py
rc=$?
echo "wall $(( $(date +%s) - start )) s"
echo "rc=$rc"

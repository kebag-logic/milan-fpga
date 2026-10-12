#!/bin/bash
# R584-6's probe_nvm.sh, its plants and gate command unchanged, run inside the CI-parity image (round 7).
# usage: probe7_nvm.sh <checkout> <log directory>
set -u; cd "$1"; L=$2; mkdir -p "$L"
LINE='#include "../../../third_party/tsn-c-stack/examples/adp_port.h"'
LINE2='#include "../../../../third_party/tsn-c-stack/examples/adp_port.h"'
run(){ n=$1; python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --only verilator > $L/probe.$n.log 2>&1; echo $? > $L/probe.$n.rc; git checkout -q -- sw/firmware/ctrl_nvm/nvm_store.c sw/firmware/ctrl/maap/maap_csr.c; git status --short; }
git clean -fdxq tb/verilator/mbx
sed -i "1a $LINE" sw/firmware/ctrl_nvm/nvm_store.c; git diff --stat; run N1
git clean -fdxq tb/verilator/mbx
sed -i "1a $LINE" sw/firmware/ctrl_nvm/nvm_store.c; sed -i "1a $LINE2" sw/firmware/ctrl/maap/maap_csr.c; git diff --stat; run N1C
echo done > $L/probe.nvm.done

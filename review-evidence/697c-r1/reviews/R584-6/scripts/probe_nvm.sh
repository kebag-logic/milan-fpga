#!/bin/bash
# Probe: does the boundary judge the saved-state store's image sources (sw/firmware/ctrl_nvm)?
# N1 plants a reach into the stack's examples/ in ctrl_nvm/nvm_store.c alone; N1C adds the same line to a
# firmware unit (ctrl/maap/maap_csr.c) as the control. Each run restores the checkout's bytes.
# Usage: probe_nvm.sh <packet-root> <checkout>
set -u; P=$1; cd "$2"; source $P/scripts/env.sh
LINE='#include "../../../third_party/tsn-c-stack/examples/adp_port.h"'
LINE2='#include "../../../../third_party/tsn-c-stack/examples/adp_port.h"'
run(){ n=$1; python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --only verilator > $P/logs/probe.$n.log 2>&1; echo $? > $P/logs/probe.$n.rc; git checkout -q -- sw/firmware; git status --short; }
sed -i "1a $LINE" sw/firmware/ctrl_nvm/nvm_store.c; git diff --stat; run N1
sed -i "1a $LINE" sw/firmware/ctrl_nvm/nvm_store.c; sed -i "1a $LINE2" sw/firmware/ctrl/maap/maap_csr.c; git diff --stat; run N1C
echo done > $P/logs/probe.nvm.done

#!/bin/bash
# Replica of firmware-verilator's boundary step, then the Verilator builders run directly.
# Usage: chain_verilator.sh <packet-root> <checkout>
set -u; P=$1; cd "$2"; source $P/scripts/env.sh
L=$P/logs/ver
step(){ n=$1; shift; echo "== $n: $*"; "$@" > $L.$n.log 2>&1; echo $? > $L.$n.rc; echo "rc=$(cat $L.$n.rc)"; }
step 1 python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
step 2 python3 sw/firmware/ctrl/test/ctrl_build.py --stack-pin
echo done > $L.done

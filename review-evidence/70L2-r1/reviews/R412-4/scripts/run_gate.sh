#!/bin/sh
# run_gate.sh <tree> <log>: run test_baremetal_profile_contract() (gates 1b..)
# alone in a disposable tree with the RV32 SDK required; prints rc.
tree=$1; log=$2
cd "$tree/sw/builder" || exit 90
python3 -c "
import sys; sys.argv=['test_builder.py','--require-rv32']
import test_builder as t
t.test_baremetal_profile_contract()
print('R412 GATE FUNCTION RETURNED')" > "$log" 2>&1
rc=$?
echo "rc=$rc $log"

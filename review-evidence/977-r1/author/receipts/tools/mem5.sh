#!/bin/bash
# mem5.sh CLONE OUT: sw/litex/test_ctrl_memory.py and plat_ledger.py --self-test on CLONE, each output in OUT.
C=$1 O=$2; mkdir -p $O
(cd $C/sw/litex && python3 -B test_ctrl_memory.py) > $O/test_ctrl_memory.txt 2>&1; echo "test_ctrl_memory rc=$? $(tail -n 1 $O/test_ctrl_memory.txt)"
(cd $C && python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $O/ledger --self-test) > $O/plat_ledger-selftest.txt 2>&1; echo "plat_ledger --self-test rc=$? $(tail -n 1 $O/plat_ledger-selftest.txt)"

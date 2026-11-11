#!/usr/bin/env bash
# memooc.sh: the four ledger images' firmware memory mapped out of context (synthesis only).
set -u
S=<scratch>
source <home>/Xilinx/2026.1/Vivado/settings64.sh
cd $S/memooc || exit 3
vivado -mode batch -nojournal -source ctrl_memory_ooc.tcl > vivado.out 2>&1; echo $? > rc

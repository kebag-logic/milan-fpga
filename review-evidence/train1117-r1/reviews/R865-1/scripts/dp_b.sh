#!/bin/bash
# Render, clock-meter and mailbox suites in sequence.
s=$(dirname "$0")
bash "$s/dp_chain.sh" tb/verilator/milan_dp_render tdm8render tdm8render-mutants || exit 1
bash "$s/dp_chain.sh" tb/verilator/aaf_clock_meter all mutants || exit 1
bash "$s/dp_chain.sh" tb/verilator/mbx all dma-mutants || exit 1

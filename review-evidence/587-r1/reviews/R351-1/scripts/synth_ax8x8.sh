#!/bin/bash
# Recipe "Integrated measurements", ax8x8 synthesis-only endpoint.
S=$REVIEWS/587-r351-1-packet/scratch
export PATH="$HOME/Xilinx/2026.1/Vivado/bin:$S/sdk/bin:$S/pybin:/usr/bin:/bin" PYTHONHASHSEED=0 
cd $S/work/ax8x8/gateware
vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > vivado.stdout 2>&1
echo "synthesis rc=$?" > $S/work/ax8x8-synth.rc

#!/bin/sh
# wire_probe_run.sh VERILATOR : build the main pp_top bench and run its ACMP section
set -e
make gsi-build VERILATOR="$1"
./obj_dir/Vpp_top_sim --acmp-only

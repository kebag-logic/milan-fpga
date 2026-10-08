#!/usr/bin/env bash
# usage: equiv_count_two.sh BASE_TREE HEAD_TREE WORK N_IF
# sv2v + Yosys sequential equivalence of KL_aecp_notify between two trees
# (N_CTRL_P=2, one stream in/out, N_IF_P=N_IF). Prints the equiv_status verdict.
set -euo pipefail
B=$1; H=$2; W=$3; N=$4
mkdir -p "$W"
sv2v "$B/hdl/common/pp_pkg.sv" "$B/hdl/aecp/KL_aecp_notify.sv" > "$W/gold.v"
sv2v "$H/hdl/common/pp_pkg.sv" "$H/hdl/aecp/KL_aecp_notify.sv" > "$W/gate.v"
P="-set N_CTRL_P 2 -set N_STREAM_IN_P 1 -set N_STREAM_OUT_P 1 -set N_IF_P $N"
yosys -q -l "$W/equiv_if$N.log" -p "
read_verilog -sv $W/gold.v; hierarchy -top KL_aecp_notify -chparam N_IF_P $N -chparam N_CTRL_P 2 -chparam N_STREAM_IN_P 1 -chparam N_STREAM_OUT_P 1;
proc; flatten; memory -nomap; memory_map; opt_clean; rename KL_aecp_notify gold; design -stash gold;
read_verilog -sv $W/gate.v; hierarchy -top KL_aecp_notify -chparam N_IF_P $N -chparam N_CTRL_P 2 -chparam N_STREAM_IN_P 1 -chparam N_STREAM_OUT_P 1;
proc; flatten; memory -nomap; memory_map; opt_clean; rename KL_aecp_notify gate; design -stash gate;
design -copy-from gold -as gold gold; design -copy-from gate -as gate gate;
equiv_make gold gate equiv; hierarchy -top equiv; async2sync;
equiv_simple -seq 5; equiv_induct -seq 5; tee -o $W/status_if$N.txt equiv_status
" || true
cat "$W/status_if$N.txt"

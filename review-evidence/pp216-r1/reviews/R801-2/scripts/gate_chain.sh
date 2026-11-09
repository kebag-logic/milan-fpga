#!/bin/bash
# the light processor gates at the head, one after another, in clone $1 (make check runs apart)
PK=${PK:-$REVIEWS/pp216-r801-2-packet}; G=$1; R=$PK/scripts/run_gate.sh
$R gen_matrix "$G" python3 scripts/gen_matrix.py --check
$R lint_hdl "$G" bash scripts/lint_hdl.sh
$R diff_check "$G" git diff --check 044cb25f 84f6d6ad77d51d678f8efdf26b45aae011a42001
$R srp_encoder "$G" make -C tb/srp_encoder -j4
$R srp_stream_fsms "$G" make -C tb/srp_stream_fsms -j4
$R elab_guards_vl "$G" python3 -B tb/elab_guards/guards.py --jobs 2
$R elab_guards_new_yosys "$G" python3 -B tb/elab_guards/guards.py --frontend yosys --only KL_srp_top.g_vids_fit --jobs 1
$R elab_mutants_new "$G" python3 -B tb/elab_guards/mutants.py --verilator verilator --output "$PK/scratch/elab-mut-out" --jobs 2 --only "KL_srp_top.g_vids_fit:error,KL_srp_top.g_vids_fit:warning,KL_srp_top.g_vids_fit:initial,KL_srp_top.g_vids_fit:tightened,KL_srp_top.g_vids_fit:loosened"
echo done > $PK/receipts/gate_chain.done

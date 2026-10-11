#!/usr/bin/env bash
# Everything Vivado for this review, serialized under the host's Vivado lock.
# Usage: vivado_session.sh <packet-dir>
set -u; P=$1; S=$P/scratch; R=$P/receipts
source $WORKSPACE_HOME/Xilinx/2026.1/Vivado/settings64.sh
export PATH=$S/bin12:$PATH TMPDIR=$S/tmp
vivado -version | head -1
echo "### head: guards.py --frontend xsim --frontend synth"
(cd $S/headgit/tb/elab_guards && python3 -B guards.py --verilator verilator --jobs 4 --frontend xsim --frontend synth) > $R/head_guards_vivado.log 2>&1; echo $? > $R/head_guards_vivado.rc
echo "### probe forms"
$P/scripts/vivado_probe_forms.sh $S/probe > $R/probe_forms_vivado.log 2>&1; echo $? > $R/probe_forms_vivado.rc
echo "### reviewer mutants through Vivado"
for m in R1-encoder-error:KL_srp_encoder.g_depth_check R2-ucpu-warning:KL_aecp_ucpu.gen_g_d8_cap R3-merge-initial-block:KL_pp_release_merge.g_slot_count_check; do
  t=${m%%:*} g=${m#*:}
  (cd $S/mymut/$t/tb/elab_guards && python3 -B guards.py --root $S/mymut/$t --verilator verilator --only $g --jobs 2 --frontend xsim --frontend synth) > $R/reviewer_mutant_vivado_$t.log 2>&1; echo $? > $R/reviewer_mutant_vivado_$t.rc
done
echo done

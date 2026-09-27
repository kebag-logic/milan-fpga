#!/bin/sh
# Composition mutation probe for #571 at the merge-train candidate.
# Usage: binding_mutants.sh <candidate-clone> <verilator> <packet-dir>
# Each mutant edits one parameter map IN PLACE, runs the elaboration probe
# (elab_probe.py) and the repository shape gate, then restores the file with
# `git checkout --`. A trap restores on any exit. The clone must start clean.
set -u
REPO=$1; VERILATOR=$2; PACKET=$3
WORK=$PACKET/scratch/elab
mkdir -p "$WORK"
cd "$REPO" || exit 2
[ -z "$(git status --porcelain)" ] || { echo "clone not clean"; exit 2; }
restore() { git checkout -- hdl/milan/KL_pp_shadow.sv hdl/milan/milan_datapath.sv; }
trap restore EXIT INT TERM
SH=hdl/milan/KL_pp_shadow.sv
DP=hdl/milan/milan_datapath.sv
for mut in none swap_shadow_clk_ctl drop_shadow_control literal_shadow_audio swap_datapath_au_ctl; do
  case $mut in
    none) ;;
    swap_shadow_clk_ctl) sed -i 's/\.N_CLK_DOMAIN_P (N_CLK_DOM_P)/.N_CLK_DOMAIN_P (N_CONTROL_P)/; s/\.N_CONTROL_P    (N_CONTROL_P)/.N_CONTROL_P    (N_CLK_DOM_P)/' $SH ;;
    drop_shadow_control) sed -i '/^[[:space:]]*\.N_CONTROL_P    (N_CONTROL_P),$/d' $SH ;;
    literal_shadow_audio) sed -i 's/\.N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),/.N_AUDIO_UNIT_P (1),/' $SH ;;
    swap_datapath_au_ctl) sed -i 's/\.N_AUDIO_UNIT_P      (AEM_N_AUDIO_UNIT_C)/.N_AUDIO_UNIT_P      (AEM_N_CONTROL_C)/; s/\.N_CONTROL_P         (AEM_N_CONTROL_C)/.N_CONTROL_P         (AEM_N_AUDIO_UNIT_C)/' $DP ;;
  esac
  echo "### mutant=$mut numstat: $(git diff --numstat | tr '\t\n' '  ')"
  python3 "$PACKET/elab_probe.py" "$REPO" "$VERILATOR" "$WORK"
  echo "elab_probe rc=$?"
  python3 scripts/check_entity_shape.py > "$WORK/gate.txt" 2>&1
  echo "check_entity_shape rc=$?"
  grep -E '\[FAIL\]|^RESULT' "$WORK/gate.txt" | head -4
  restore
done
echo "### after restore: status lines $(git status --porcelain | wc -l)"

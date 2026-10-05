#!/usr/bin/env bash
# Build and run the two #148 sections (tb/aecp_notify TW, tb/pp_top CS) in one
# extracted tree. Usage: run_sections.sh TREE OUTDIR LABEL
# TREE is a `git archive` extraction of the processor; OUTDIR receives
# LABEL-aecp_notify.{log,rc} and LABEL-pp_top-spacing.{log,rc}.
set -u
tree=$1; out=$2; label=$3
V=${VERILATOR:-verilator}   # the review used a pinned Verilator 5.050
mkdir -p "$out"
(
  cd "$tree/tb/aecp_notify" && make VERILATOR="$V" run
) > "$out/$label-aecp_notify.log" 2>&1
echo $? > "$out/$label-aecp_notify.rc"
(
  cd "$tree/tb/pp_top" && make VERILATOR="$V" gsi-build && ./obj_dir/Vpp_top_sim --spacing-only
) > "$out/$label-pp_top-spacing.log" 2>&1
echo $? > "$out/$label-pp_top-spacing.rc"

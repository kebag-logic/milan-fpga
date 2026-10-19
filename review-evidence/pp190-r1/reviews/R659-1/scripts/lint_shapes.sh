#!/usr/bin/env bash
# Lint protocol_processor_top at several N_STREAM_OUT_P shapes with the flags
# scripts/lint_hdl.sh uses, and print the warnings that name
# cfg_tspec_max_frame_i or the talker stage line. Usage: lint_shapes.sh TREE LABEL
set -u
tree=$1; label=$2
cd "$tree" || exit 2
pkgs=$(find hdl -name '*_pkg.sv' | sort)
all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
for n in 1 2 3 4 6 8 16; do
  # shellcheck disable=SC2086
  out=$(verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
        --top-module protocol_processor_top -GN_STREAM_OUT_P=$n $pkgs $all 2>&1); rc=$?
  w=$(grep -cE '%(Warning|Error)' <<<"$out")
  t=$(grep -E '%(Warning|Error)' <<<"$out" | grep -c 'tspec\|protocol_processor_top.sv:270[0-9]')
  echo "$label N_STREAM_OUT_P=$n rc=$rc warnings+errors=$w tspec-related=$t"
  grep -E '%(Warning|Error)' <<<"$out" | sed 's#^#    #' | head -8
done

#!/usr/bin/env bash
# Run tb/acmp_listener (or tb/pp_top with ARGS) with the listener replaced by the shadow lockstep.
# usage: run_suite_shadow.sh MAIN_TREE HEAD_TREE WORK SUITE [MUTANT] -- [make target / run args]
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
main=$1; head=$2; work=$3; suite=$4; mut=${5:-}
rm -rf "$work"; mkdir -p "$work"
cp -r "$head/hdl" "$head/tb/common" "$work/" 2>/dev/null || true
mkdir -p "$work/tb"; mv "$work/common" "$work/tb/common"; cp -r "$head/$suite" "$work/$suite"
mkdir -p "$work/gen"
if [ -n "$mut" ]; then
  python3 "$here/gen_shadow.py" "$main/hdl/acmp/KL_pp_acmp_listener.sv" "$head/hdl/acmp/KL_pp_acmp_listener.sv" "$work/gen" --mutant "$mut"
else
  python3 "$here/gen_shadow.py" "$main/hdl/acmp/KL_pp_acmp_listener.sv" "$head/hdl/acmp/KL_pp_acmp_listener.sv" "$work/gen"
fi
cp "$work/gen/KL_pp_acmp_listener.sv" "$work/hdl/acmp/KL_pp_acmp_listener.sv"
cp "$work/gen/lsn_ref.sv" "$work/gen/lsn_dut.sv" "$work/hdl/acmp/"
# add the two renamed listeners right after the shadow in the suite's source list
sed -i 's#\$(HDL)/acmp/KL_pp_acmp_listener.sv#$(HDL)/acmp/lsn_ref.sv $(HDL)/acmp/lsn_dut.sv $(HDL)/acmp/KL_pp_acmp_listener.sv#' "$work/$suite/Makefile"
grep -q 'lsn_ref.sv' "$work/$suite/Makefile"

#!/usr/bin/env bash
# Lint the four #230-changed SRP modules at 1, 2, 3, 5 and 9 contexts with the
# repository's lint flags. Usage: shape_lint.sh <checkout>; verilator on PATH.
set -u
cd "$1" || exit 2
pkgs=$(find hdl -name '*_pkg.sv' | sort)
all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
rc=0
for n in 1 2 3 5 9; do
  for spec in "KL_srp_talker_fsm -GN_SOURCES_P=$n" "KL_srp_listener_fsm -GN_SINKS_P=$n" \
              "KL_srp_admission -GN_SOURCES_P=$n" "KL_srp_top -GN_SOURCES_P=$n -GN_SINKS_P=$n"; do
    set -- $spec
    top=$1; shift
    # shellcheck disable=SC2086
    if out=$(verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
             --top-module "$top" "$@" $pkgs $all 2>&1) && ! grep -qE '%(Warning|Error)' <<<"$out"; then
      echo "OK   $top $*"
    else
      echo "FAIL $top $*"; grep -E '%(Warning|Error)' <<<"$out" | head -5; rc=1
    fi
  done
done
echo "rc=$rc"; exit $rc

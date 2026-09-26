#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer-scoped donor runs for processor PR #121. Runs the suites that
# instantiate a changed file, at head and at base, plus a scoped strict lint
# of the changed modules. Usage:
#   r335_donor_suites.sh <head-tree> <base-tree> <receipt-dir>
# The Verilator used is the first on PATH; the caller pins it.
set -uo pipefail
head=$(cd "$1" && pwd); base=$(cd "$2" && pwd)
mkdir -p "$3"; out=$(cd "$3" && pwd)
verilator --version > "$out/verilator-version.txt"

suite() {  # <tree> <suite> <label>
  local log="$out/$3-$2.log"
  (cd "$1/tb/$2" && make) > "$log" 2>&1
  echo "rc=$?" >> "$log"
}

lint() {  # <tree> <label>
  local log="$out/$2-lint.log" rc=0 pkgs all top
  cd "$1" || return
  pkgs=$(find hdl -name '*_pkg.sv' | sort)
  all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
  : > "$log"
  for top in protocol_processor_top KL_aecp_engine KL_aecp_desc_store; do
    # shellcheck disable=SC2086
    o=$(verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
        -Wno-UNUSEDPARAM --top-module "$top" $pkgs $all 2>&1); r=$?
    if [ $r -ne 0 ] || grep -qE '%(Warning|Error)' <<<"$o"; then
      echo "LINT FAIL $top rc=$r" >> "$log"; echo "$o" | head -20 >> "$log"; rc=1
    else
      echo "LINT OK  $top" >> "$log"
    fi
  done
  echo "rc=$rc" >> "$log"
}

# head and base top suites in parallel, the unit suites after
suite "$head" pp_top head &
suite "$base" pp_top base &
lint "$head" head &
wait
for s in desc_store desc_mem_guard ucpu; do suite "$head" "$s" head & done
wait
grep -H -E 'checks: [0-9]+ PASS|^rc=|LINT' "$out"/*.log

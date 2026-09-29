#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer receipt driver: the focused processor gates at the reviewed head.
# Usage: focused_gates.sh <clone> <receipt-dir>
# Needs a Verilator 5.050 first on PATH. Runs at most 4 jobs at once.
set -uo pipefail
clone=$(cd "$1" && pwd); out=$(mkdir -p "$2" && cd "$2" && pwd)
cd "$clone" || exit 2
{ verilator --version; git rev-parse HEAD HEAD^{tree}; } > "$out/00-identity.txt" 2>&1

gate() {  # name, command...
  local name=$1; shift
  local t0=$SECONDS
  ( "$@" ) > "$out/$name.log" 2>&1
  local rc=$?
  echo "$name rc=$rc secs=$((SECONDS - t0))" >> "$out/rc.txt"
}
export -f gate; export out
: > "$out/rc.txt"
printf '%s\n' \
  "suite-adp_engine|make -C tb/adp_engine" \
  "suite-timer_map|make -C tb/timer_map" \
  "suite-pp_top|make -C tb/pp_top" \
  "static|bash -c './scripts/lint_hdl.sh && python3 scripts/check_upc_map.py && make check && python3 scripts/gen_matrix.py --check && git diff --check c951a9ff0cb5851fb159d33e966e5a2a9a188fe3..HEAD'" \
  | xargs -P 4 -I{} bash -c 'IFS="|" read -r n c <<< "{}"; gate "$n" bash -c "$c"'
sort "$out/rc.txt"

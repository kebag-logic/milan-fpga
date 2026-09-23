#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer receipt script: run the SRP-family Verilator suites of one source
# tree (a disposable git-archive export, never the review clone), serially,
# with the Verilator C++ build capped at 8 jobs (the export's suite Makefiles
# are edited in place: "-j 0" -> "-j 8"). Usage:
#   run_srp_suites.sh <tree> <verilator-wrapper-dir> [suite ...]
# Prints one line per suite: "<suite> rc=<exit> <tally line or NO-TALLY>".
set -uo pipefail
tree=${1:?tree}; vbin=${2:?verilator dir}; shift 2
suites=${*:-"srp_encoder srp_decoder srp_stream_fsms srp_top"}
export PATH="$vbin:$PATH"
verilator --version
for s in $suites; do
  d="$tree/tb/$s"
  log="$d/run.log"
  sed -i 's/--build -j 0/--build -j 8/' "$d/Makefile"
  (cd "$d" && rm -rf obj_dir && make) >"$log" 2>&1
  rc=$?
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1)
  echo "$s rc=$rc ${tally:-NO-TALLY}"
done

#!/usr/bin/env bash
# Focused lint: the same verilator --lint-only command scripts/lint_hdl.sh
# runs, for the tops this PR changes, plus an elaboration probe of
# protocol_processor_top at several DESC_LINE_BYTES_P values.
# Usage: lint_focus.sh <tree-root> [extra -G override ...]
set -uo pipefail
cd "$1" || exit 2
shift
pkgs=$(find hdl -name '*_pkg.sv' | sort)
all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
rc=0
for top in "$@"; do
  # shellcheck disable=SC2086
  out=$(verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
        -Wno-UNUSEDPARAM ${GOPT:-} --top-module "$top" $pkgs $all 2>&1)
  st=$?
  nw=$(grep -c '%Warning' <<<"$out")
  ne=$(grep -c '%Error' <<<"$out")
  echo "top=$top ${GOPT:-} rc=$st warnings=$nw errors=$ne"
  grep -m3 -E '%Error' <<<"$out" | cut -c1-220
  [ "$st" -eq 0 ] && [ "$nw" -eq 0 ] || rc=1
done
exit $rc

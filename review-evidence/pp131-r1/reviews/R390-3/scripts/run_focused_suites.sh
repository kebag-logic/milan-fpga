#!/bin/sh
# Reviewer run of the focused suites at the exact head, each in its own
# disposable git-archive copy, at most 8 at a time.
# Usage: run_focused_suites.sh <clone> <out> <verilator>
set -u
HEAD=${HEAD:-cbbb5acc77e9e068c3313d78ed4c1e5e79299a71}
SRC=$1; OUT=$(realpath -m "$2"); VL=$3
rm -rf "$OUT"; mkdir -p "$OUT"
for suite in acmp_nvm nvm_port desc_mem_guard dyn_state desc_store lsn_admit adp_engine rx_validator; do
  mkdir -p "$OUT/$suite-tree"; git -C "$SRC" archive "$HEAD" | tar -x -C "$OUT/$suite-tree"
done
printf '%s\n' acmp_nvm nvm_port desc_mem_guard dyn_state desc_store lsn_admit adp_engine rx_validator |
  xargs -P 8 -I{} sh -c 'cd "$0/{}-tree/tb/{}" && make VERILATOR="$1" > "$0/{}.log" 2>&1; echo "suite {} rc=$?: $(tail -1 "$0/{}.log")"' "$OUT" "$VL"

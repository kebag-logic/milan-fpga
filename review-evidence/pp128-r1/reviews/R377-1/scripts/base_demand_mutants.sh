#!/usr/bin/env bash
# Plant the demand-path mutants into the BASE commit with the BASE tests, to
# show whether they were pinned before the change (exact-string deletion,
# anchor must match once). Usage:
#   base_demand_mutants.sh SRC_CLONE BASE_REV SCRATCH VERILATOR OUT
set -uo pipefail
src=$1; rev=$2; scratch=$3; vl=$4; out=$5; mkdir -p "$scratch" "$out"
echo "base $(git -C "$src" rev-parse "$rev")" > "$out/summary-base-demand.txt"
for n in no_probe_initset no_lsn_initset no_backoff_exit_initset; do
  t="$scratch/base-$n"; rm -rf "$t"; mkdir -p "$t"; git -C "$src" archive "$rev" | tar -x -C "$t"
  c=$(python3 - "$t/hdl/acmp/KL_acmp_talker.sv" "$n" <<'PY'
import sys
p, n = sys.argv[1], sys.argv[2]
a = {"no_probe_initset": "    if ((state_r == S_TXN_ACT) && txn_initset_w) set_init_w[tsrc_w]   = 1'b1;\n",
     "no_lsn_initset": "          ev_initset_w = 1'b1;    // a listener appeared: retry allocation\n",
     "no_backoff_exit_initset": "            ev_initset_w     = 1'b1;   // re-allocate, then re-declare\n"}[n]
s = open(p).read(); c = s.count(a)
if c == 1: open(p, "w").write(s.replace(a, ""))
print(c)
PY
)
  if [ "$c" != 1 ]; then echo "$n anchor=$c SKIPPED" >> "$out/summary-base-demand.txt"; rm -rf "$t"; continue; fi
  ( cd "$t/tb/acmp_talker" && make VERILATOR="$vl" ) > "$out/base-$n.log" 2>&1; rc=$?
  echo "$n anchor=$c rc=$rc $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/base-$n.log" | tail -1) first: $(grep -m1 '^FAIL' "$out/base-$n.log")" >> "$out/summary-base-demand.txt"
  rm -rf "$t"
done
cat "$out/summary-base-demand.txt"

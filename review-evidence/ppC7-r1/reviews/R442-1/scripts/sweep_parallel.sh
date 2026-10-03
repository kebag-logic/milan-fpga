#!/usr/bin/env bash
# Reviewer sweep: the same gates and per-suite `make` as scripts/run_suites.sh,
# but suites run concurrently (one log per suite). Usage:
#   sweep_parallel.sh <tree> <outdir> [parallel]
# Requires VERILATOR on PATH (the pinned 5.050 wrapper first).
set -uo pipefail
tree=$(cd "$1" && pwd); out=$2; par=${3:-8}
mkdir -p "$out"
cd "$tree" || exit 1
python3 scripts/check_upc_map.py >"$out/gate_upc_map.log" 2>&1; echo $? >"$out/gate_upc_map.rc"
{ python3 scripts/check_m9_opcodes.py --selftest && python3 scripts/check_m9_opcodes.py; } >"$out/gate_m9.log" 2>&1; echo $? >"$out/gate_m9.rc"
one() {
  d=$1; out=$2; name=$(basename "$d")
  (cd "$d" && make) >"$out/suite_$name.log" 2>&1; echo $? >"$out/suite_$name.rc"
}
export -f one
ls -d tb/*/ | while read -r d; do [ -f "$d/Makefile" ] && echo "$d"; done \
  | xargs -P "$par" -I{} bash -c 'one "$@"' _ {} "$out"
total=0; fails=0; unread=0
for rcf in "$out"/suite_*.rc; do
  name=$(basename "$rcf" .rc); name=${name#suite_}; rc=$(cat "$rcf")
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/suite_$name.log" | tail -1 || true)
  if [ "$rc" != 0 ]; then echo "FAIL $name rc=$rc"; fails=$((fails+1))
  elif [ -z "$tally" ]; then echo "UNREADABLE $name"; unread=1
  else total=$((total + ${tally%% *})); echo "PASS $name ($tally)"; fi
done | sort -k2 > "$out/summary.txt"
total=$(grep -Eo '\(([0-9]+) checks' "$out/summary.txt" | grep -Eo '[0-9]+' | paste -sd+ | bc)
nf=$(grep -c '^FAIL\|^UNREADABLE' "$out/summary.txt")
echo "suites: $(wc -l <"$out/summary.txt") ; checks total $total ; failing/unreadable $nf ; gates upc=$(cat "$out/gate_upc_map.rc") m9=$(cat "$out/gate_m9.rc")" >>"$out/summary.txt"
[ "$nf" = 0 ] && [ "$(cat "$out/gate_upc_map.rc")" = 0 ] && [ "$(cat "$out/gate_m9.rc")" = 0 ]

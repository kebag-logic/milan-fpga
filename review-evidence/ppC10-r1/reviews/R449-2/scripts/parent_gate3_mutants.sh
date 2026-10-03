#!/usr/bin/env bash
# R449-2: grade the parent's check_rtl_source_lists self-test (amended by the
# c10 adoption patch) against refusal-disabling mutants of the checker, and the
# live gate against planted data faults. Each case works on a scratch copy.
# Usage: parent_gate3_mutants.sh <parent-tree-with-c8-p2-c10> <work-dir>
# Writes <work-dir>/<case>.{gate3,selftest}.log and a summary on stdout.
set -u
src=$1 w=$2
rm -rf "$w"; mkdir -p "$w"
CK=scripts/check_rtl_source_lists.py
mutate() { # tree, python old, python new (exact, must occur once)
  python3 - "$1/$CK" "$2" "$3" <<'PY'
import sys
f, old, new = sys.argv[1:4]
s = open(f).read()
assert s.count(old) == 1, (old, s.count(old))
open(f, 'w').write(s.replace(old, new))
PY
}
run_case() { # case name
  local n=$1 t="$w/$1/tree"
  mkdir -p "$w/$n"; cp -a "$src" "$t"
  case "$n" in
    pristine) ;;
    m-drop-stale-line)   mutate "$t" "        for name in stale:" "        for name in []:" ;;
    m-drop-drift-line)   mutate "$t" "        for name in unrecorded:" "        for name in []:" ;;
    m-stale-empty)       mutate "$t" "    stale = sorted(n for n in recorded if n not in missing)" "    stale = []" ;;
    m-unrec-empty)       mutate "$t" "    unrecorded = sorted(missing - set(recorded))" "    unrecorded = []" ;;
    m-stale-uncounted)   python3 - "$t/$CK" <<'PY'
import sys
f = sys.argv[1]; s = open(f).read()
old = "        for name in stale:\n            findings += 1\n"
assert s.count(old) == 1
open(f, 'w').write(s.replace(old, "        for name in stale:\n            findings += 0\n"))
PY
      ;;
    m-drift-uncounted)   python3 - "$t/$CK" <<'PY'
import sys
f = sys.argv[1]; s = open(f).read()
old = "        for name in unrecorded:\n            findings += 1\n"
assert s.count(old) == 1
open(f, 'w').write(s.replace(old, "        for name in unrecorded:\n            findings += 0\n"))
PY
      ;;
    d-stale-record)  printf 'KL_srp_top              r449 planted: a top recorded as an omission\n' >> "$t/scripts/processor_yosys_tops.budget" ;;
    d-unrecorded)    sed -i -E '/^tops=\(/,/\)$/ s/(^|[ (])KL_srp_top([ )])/\1\2/' "$t/protocol-processor/syn/yosys/run.sh" ;;
    d-recorded-omission)
      sed -i -E '/^tops=\(/,/\)$/ s/(^|[ (])KL_srp_top([ )])/\1\2/' "$t/protocol-processor/syn/yosys/run.sh"
      printf 'KL_srp_top              r449 planted: recorded omission\n' >> "$t/scripts/processor_yosys_tops.budget" ;;
  esac
  ( cd "$t" && python3 $CK ) > "$w/$n.gate3.log" 2>&1; local g=$?
  ( cd "$t" && python3 $CK --selftest ) > "$w/$n.selftest.log" 2>&1; local s=$?
  echo "$n gate3_rc=$g selftest_rc=$s selftest='$(tail -n 1 "$w/$n.selftest.log")' gate3='$(grep -m1 -E 'TOPS DRIFT|STALE RECORD|RTL source-list gate' "$w/$n.gate3.log" | cut -c1-110)'"
  rm -rf "$t"
}
for c in pristine m-drop-stale-line m-drop-drift-line m-stale-empty m-unrec-empty \
         m-stale-uncounted m-drift-uncounted d-stale-record d-unrecorded d-recorded-omission; do
  run_case "$c" &
done
wait

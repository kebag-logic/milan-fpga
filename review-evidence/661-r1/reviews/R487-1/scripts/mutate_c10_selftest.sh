#!/usr/bin/env bash
# Mutation probes for the C10 self-test arms of scripts/check_rtl_source_lists.py --selftest.
# Usage: mutate_c10_selftest.sh <head-clone> <work-dir> <receipt-dir>
# Each mutant copies the checkout (with .git, so git ls-files works), applies one substitution
# to scripts/check_rtl_source_lists.py and requires the self-test to exit non-zero.
set -u
src=$1; work=$2; out=$3; mkdir -p "$work" "$out"
mutant() {
  local id=$1 old=$2 new=$3 d="$work/$1"
  rm -rf "$d"; cp -a "$src" "$d"
  python3 - "$d/scripts/check_rtl_source_lists.py" "$old" "$new" <<'PY' || { echo APPLY-FAILED > "$out/c10_$id.rc"; return; }
import sys; p, o, n = sys.argv[1:]
s = open(p).read(); assert s.count(o) == 1, f"{o!r} occurs {s.count(o)} times"; open(p, "w").write(s.replace(o, n))
PY
  ( cd "$d" && timeout 900 python3 scripts/check_rtl_source_lists.py --selftest > "$out/c10_$id.log" 2>&1; echo $? > "$out/c10_$id.rc" ) &
}
mutant C1_no_unrecorded '    unrecorded = sorted(missing - set(recorded))' '    unrecorded = []'
mutant C2_no_stale '    stale = sorted(n for n in recorded if n not in missing)' '    stale = []'
mutant C3_drift_line_dropped 'lines.append(f"TOPS DRIFT: ' 'lines.append(f"TOPS_DRIFT_X: '
mutant C4_stale_line_dropped 'lines.append(f"STALE RECORD: ' 'lines.append(f"STALE_X: '
wait
for f in "$out"/c10_*.rc; do rc=$(cat "$f"); case $rc in 0) v=SURVIVED;; APPLY*) v=INVALID;; *) v=KILLED;; esac; echo "$(basename "$f" .rc) rc=$rc $v"; done

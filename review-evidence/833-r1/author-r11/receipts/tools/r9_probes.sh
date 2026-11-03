#!/usr/bin/env bash
# Every round 9 reviewer probe, from its manifest-checked copy, unchanged, on one tree; one log and rc each.
# usage: r9_probes.sh <tree> <receipt dir> <which>
set -u
S=$VALIDATION_STORAGE/833-a726j
P763=$S/probes/833-r763-9; P764=$S/probes/833-r764-9
tree=$1; out=$2; which=$3
mkdir -p "$out"
export TMPDIR=$S/tmp
grep SigIgn /proc/self/status > "$out/r9-probes-$which.sigign"
run() {  # name, command...
  local name=$1; shift
  cat /proc/loadavg > "$out/$name.load"
  "$@" > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
  cat /proc/loadavg >> "$out/$name.load"
  echo "$name rc $(cat "$out/$name.rc"): $(tail -n 1 "$out/$name.log" | cut -c1-200)"
}
case $which in
natural)
  rm -rf "$S/natural-scratch"
  run r763-9-natural python3 -I "$P763/natural.py" "$tree" "$S/natural-scratch" 10
  rm -rf "$S/natural-scratch" ;;
audit)
  rm -rf "$S/audit-tree"; mkdir -p "$S/audit-tree"; cp -r "$tree/scripts" "$S/audit-tree/scripts"
  rm -rf "$S/audit-tree/scripts/__pycache__"
  python3 -I "$P763/audit_new_in_grace.py" "$S/audit-tree"
  (cd "$S/audit-tree" && run r763-9-audit-new-in-grace python3 -B scripts/test_suite_cancellation.py --control owner_stated_seconds)
  grep AUDIT "$out/r763-9-audit-new-in-grace.log" > "$out/r763-9-audit-new-in-grace.txt"
  rm -rf "$S/audit-tree" ;;
f2)
  rm -rf "$S/f2-scratch"
  run r763-9-f2-feasibility python3 -I "$P763/f2_feasibility.py" "$tree" "$S/f2-scratch"
  rm -rf "$S/f2-scratch" ;;
listing)
  rm -rf "$S/pl-scratch"
  names=$(python3 -I -c "import sys; sys.path.insert(0, '$tree/scripts'); from process_test_support import MUTANTS; print(' '.join(n for n, v in MUTANTS.items() if v[0] == 'owner_stated_seconds'))")
  run r763-9-per-listing python3 -I "$P763/per_listing.py" "$tree" "$S/pl-scratch" none $names
  rm -rf "$S/pl-scratch" ;;
static)
  run r763-9-table-check python3 -I "$P763/table_check.py" "$tree"
  run r764-9-byte-match python3 -I "$P764/scripts/byte_match.py" "$tree" ;;
probe)
  run r763-9-probe-cells python3 -I "$P763/probe_cells.py" "$tree" ;;
esac

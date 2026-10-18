#!/usr/bin/env bash
# Round-2 occupancy probes for issue #181 at an exact processor head.
# usage: probe_cq.sh <processor-git-dir> <head-sha> <base-sha> <mutant-diff-dir> <out-dir>
#   <mutant-diff-dir> holds mutant_N4.diff, mutant_N5.diff, mutant_N7.diff (round-1 reviewer edits)
# env: VERILATOR (default: verilator on PATH), JOBS (default 16)
# Arms, each a `git archive` export of <head-sha> built and run in tb/aecp_notify:
#   head      unmodified: `make check` (all five runs)
#   baseRTL   the head's bench over <base-sha>'s KL_aecp_notify.sv (no flag): `make run`,
#             CQ1..CQ2b must pass; base has no cmdq_nempty_r, so for the bench to build a
#             probe-only wire cmdq_nempty_r = (cmdq_count_r != 0) is added (OC1 then holds trivially)
#   N4 N5 N7  the round-1 diffs applied with patch: `make run`
#   N8        extra reviewer arm: a pop without a push clears the occupancy at count 2
#             (one entry early): `make run`
set -u
git_dir=$1; head=$2; base=$3; mdir=$4; out=$5
V=${VERILATOR:-verilator}; JOBS=${JOBS:-16}
mkdir -p "$out"
NTFY=hdl/aecp/KL_aecp_notify.sv
mk() { # <name> -> fresh export
  local t=$out/tree-$1; rm -rf "$t"; mkdir -p "$t"
  git -C "$git_dir" archive "$head" | tar -x -C "$t"; echo "$t"
}
arm() { # <name> <make-target>
  local name=$1 tgt=$2 t=$out/tree-$1 rc=0
  ( cd "$t/tb/aecp_notify" && make VERILATOR="$V" "$tgt" ) > "$out/$name.log" 2>&1 || rc=$?
  echo "$name rc=$rc" > "$out/$name.rc"
}
t=$(mk head)
t=$(mk baseRTL)
git -C "$git_dir" show "$base:$NTFY" > "$t/$NTFY"
# base has no cmdq_nempty_r; give the bench's monitor a wire equal to the base's compare
python3 -I - "$t/$NTFY" <<'PY'
import sys, re
p = sys.argv[1]; s = open(p).read()
anchor = "  logic [4:0]  cmdq_count_r;\n"
assert s.count(anchor) == 1, "anchor"
s = s.replace(anchor, anchor + "  wire cmdq_nempty_r = (cmdq_count_r != 5'd0);  // probe only\n")
open(p, "w").write(s)
PY
for n in N4 N5 N7; do
  t=$(mk $n)
  ( cd "$t" && set -o pipefail && sed 's#^--- head/#--- a/#; s#^+++ mut/'$n'/#+++ b/#' "$mdir/mutant_$n.diff" \
      | patch -p1 --no-backup-if-mismatch ) > "$out/$n.patch.log" 2>&1
  prc=$?; echo "patch rc=$prc" >> "$out/$n.patch.log"
  [ $prc -eq 0 ] || { echo "patch $n failed" >&2; exit 3; }
done
t=$(mk N8)
python3 -I - "$t/$NTFY" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = "cmdq_nempty_r <= (cmdq_count_r != 5'd1);"
assert s.count(old) == 1, "anchor"
open(p, "w").write(s.replace(old, "cmdq_nempty_r <= (cmdq_count_r != 5'd2);"))
PY
for n in N4 N5 N7 N8; do git -C "$git_dir" show "$head:$NTFY" | diff - "$out/tree-$n/$NTFY" > "$out/$n.applied.diff"; done
git -C "$git_dir" show "$head:$NTFY" | diff - "$out/tree-baseRTL/$NTFY" > "$out/baseRTL.applied.diff"
arm head check &
for n in baseRTL N4 N5 N7 N8; do arm $n run & done
wait
for n in head baseRTL N4 N5 N7 N8; do
  printf '%-8s %s | ' "$n" "$(cat "$out/$n.rc")"
  grep -E '^FAIL: [A-Z]+[0-9]+b?:' "$out/$n.log" | sed -E 's/^FAIL: ([A-Z]+[0-9]+b?):.*/\1/' | sort -u | tr '\n' ' '
  grep -E 'checks: [0-9]+ PASS' "$out/$n.log" | tail -1
  echo
done > "$out/summary.txt"
cat "$out/summary.txt"

#!/bin/sh
# R405-3: disposable fault probes on copies of the archived B2 round-1 author
# packet.  Each mutant must be reported by the reviewer's r405_3_polls.py and
# by the author's round-3 poll_count_b2r3.py (run without the manifest, so only
# the poll checks can fail).  Usage: r405_3_probes.sh <author-dir> <author-r3-dir> <scratch>
set -u
A=$1; R3=$2; S=$3
here=$(cd "$(dirname "$0")" && pwd)
run() {
  name=$1; d=$S/probe-$name
  echo "== probe $name"
  echo "-- reviewer script (selected lines)"
  python3 -I "$here/r405_3_polls.py" "$d" | grep -E 'counted polls|Stream Input 0 outside|non-zero|missing before|not exactly one|byte-equal'
  echo "-- author script"
  python3 -I -B "$R3/scripts/poll_count_b2r3.py" "$d" 2>&1 | grep -E '^(PASS|FAIL|FAILURES)|rc='
  echo "rc=$?"
}
mk() { rm -rf "$S/probe-$1"; cp -a "$A" "$S/probe-$1"; }

mk control
run control

# 1: one action's before-poll removed
mk drop-before
sed -i '/"what":"state-5-1"/d' "$S/probe-drop-before/cycles/cycle-003/snapshot-before.jsonl"
run drop-before

# 2: one after-poll reads connection count 1 (and its snapshot.jsonl copy too)
mk bound
for f in snapshot-after.jsonl snapshot.jsonl; do
  sed -i '/"what":"state-5-1"/s/"conn_count":0/"conn_count":1/' "$S/probe-bound/bind/bind-2/$f"
done
run bound

# 3: Stream Input 0 polled outside the censuses
mk si0
grep -h '"what":"state-5-1"' "$S/probe-si0/cycles/cycle-010/snapshot-after.jsonl" | sed 's/state-5-1/state-5-0/; s/"listener_uid":1/"listener_uid":0/; s/"t":\([0-9.]*\)/"t":\1 /' >> "$S/probe-si0/cycles/cycle-010/snapshot-before.jsonl"
run si0

# 4: snapshot.jsonl no longer a byte copy of snapshot-after.jsonl
mk nocopy
printf '\n' >> "$S/probe-nocopy/cycles/cycle-050/snapshot.jsonl"
run nocopy

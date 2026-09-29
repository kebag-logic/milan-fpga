#!/usr/bin/env bash
# Round-3 mutation probes: prove poll_census_r3.py and tables_r2.py can fail.
# Usage: mutate_r3.sh <packet dir> <archived author dir> <clone>
# Every mutant runs on a scratch copy under <packet>/scratch/mut and is removed.
set -u
P=$1; A=$2; C=$3
S=$P/scratch/mut; rm -rf "$S"; mkdir -p "$S"
base=$(python3 -B "$P/scripts/poll_census_r3.py" "$A")
killed=0; total=0
probe() {
  name=$1; out=$(python3 -B "$P/scripts/poll_census_r3.py" "$S/a" 2>&1)
  total=$((total+1))
  if [ "$out" != "$base" ]; then killed=$((killed+1)); echo "KILLED  $name :: $(diff <(echo "$base") <(echo "$out") | grep '^>' | head -2 | tr '\n' ' ')"
  else echo "SURVIVED $name"; fi
  rm -rf "$S/a"; }
fresh() { cp -a "$A" "$S/a"; }
# jmut <file> <python body operating on list L of records>
jmut() { python3 -c '
import sys, json, copy
p = sys.argv[1]
L = [json.loads(l) for l in open(p) if l.strip()]
def dut(w): return [r for r in L if r.get("role") == "dut" and r.get("what") == w]
exec(sys.argv[2])
open(p, "w").write("".join(json.dumps(r) + "\n" for r in L))
' "$1" "$2"; }

# M1: drop the Stream Input 1 poll from one action's snapshot-before
fresh; jmut "$S/a/bind/bind-3/snapshot-before.jsonl" 'L[:] = [r for r in L if r not in dut("state-5-1")]'
probe "M1 one action loses its before-poll"

# M2: one snapshot.jsonl no longer a byte copy (a distinct extra poll)
fresh; f="$S/a/cycles/$(ls "$S/a/cycles" | head -1)/snapshot.jsonl"; printf '\n' >> "$f"
probe "M2 one snapshot.jsonl not a byte copy"

# M3: Stream Input 0 polled inside an action
fresh; jmut "$S/a/bind/unbind-2/snapshot-after.jsonl" 'x = copy.deepcopy(dut("state-5-1")[0]); x["what"] = "state-5-0"; x["response"]["listener_uid"] = 0; L.append(x)'
probe "M3 Stream Input 0 polled in an action"

# M4: one distinct poll reads bound
fresh; jmut "$S/a/bind/bind-5/snapshot-after.jsonl" 'dut("state-5-1")[0]["response"]["conn_count"] = 1'
probe "M4 a Stream Input 1 poll reads connection count 1"

# M5: a state-changing AECP command names a DUT stream input
fresh; echo '{"role": "dut", "what": "setfmt-5-1", "response": {"cmd": "SET_STREAM_FORMAT", "status": "SUCCESS"}}' >> "$S/a/restore/census-end.jsonl"
probe "M5 a SET_ command to DUT Stream Input 1"

# M6: tables_r2.py sees one changed measurement-table cell
total=$((total+1))
W=$S/wt; rm -rf "$W"; git clone -q --shared --no-checkout "$C" "$W"; git -C "$W" checkout -q --detach fb4a1b895e97bb808b624ea0b31c43d121723f36
sed -i 's/| 1 | more than 1,800/| 1 | more than 1,801/' "$W/docs/findings/606_FIRST_BIND_MEASUREMENT.md"
git -C "$W" -c user.name=probe -c user.email=probe@invalid commit -qam probe
out=$(python3 -B "$P/scripts/tables_r2.py" "$W" fb4a1b895e97bb808b624ea0b31c43d121723f36 HEAD "$P/receipts/pr_body_at_read.md")
if echo "$out" | grep -q 'CHANGED   ## Per-bind results' && echo "$out" | grep "Per-bind table" | grep -q "identical on: NO PAGE TABLE"; then killed=$((killed+1)); echo "KILLED  M6 per-bind cell changed :: page table CHANGED and PR body table no longer identical"
else echo "SURVIVED M6"; echo "$out" | tail -4; fi
echo "control: unmutated archive reproduces receipt: $( [ "$(python3 -B "$P/scripts/poll_census_r3.py" "$A")" = "$base" ] && echo yes || echo no )"
echo "killed $killed of $total"
rm -rf "$S/a" "$S/wt"

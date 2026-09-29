#!/usr/bin/env bash
# Run tb/srp_top/mutants.py of an exported tree in N shards (--only), each in its own
# temporary tree under $TMPDIR, then union the killed assertion tags for coverage.
# usage: srp_mutants_sharded.sh <tree> <out_dir> [shards=8]
set -uo pipefail
tree=$1; out=$2; n=${3:-8}
mkdir -p "$out"
labels=$(python3 - "$tree" <<'PY'
import sys, importlib.util
spec = importlib.util.spec_from_file_location("m", sys.argv[1] + "/tb/srp_top/mutants.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(" ".join(x[0] for x in m.MUTANTS))
PY
)
i=0; declare -a shard
for l in $labels; do shard[$((i % n))]+="${shard[$((i % n))]:+,}$l"; i=$((i+1)); done
echo "arms: $i shards: $n"
for k in $(seq 0 $((n-1))); do
  ( cd "$tree/tb/srp_top" && python3 mutants.py --output "$out/shard$k" --only "${shard[$k]}" ) > "$out/shard$k.log" 2>&1 &
done
wait
cat "$out"/shard*.log > "$out/ALL.log"
python3 - "$out/ALL.log" <<'PY'
import re, sys
txt = open(sys.argv[1]).read()
arms = re.findall(r'^(\S+): rc=(\d+) failures=(\d+) (KILLED|UNPROVEN) tags=(\S*)$', txt, re.M)
ctrl = re.findall(r'^control (\S+) (\S*): rc=(\d+) (PASS|FAIL)$', txt, re.M)
covered = set()
for a in arms:
    if a[3] == "KILLED":
        covered.update(t for t in a[4].split(",") if t)
expected = {f"{g}{i}" for g, c in [("K",12),("L",4),("M",12),("N",13),("O",8),("P",8),("Q",4),("R",4)] for i in range(1, c+1)}
missing = sorted(expected - covered)
ctrl_ok = sum(1 for c in ctrl if c[3] == "PASS")
print(f"control runs: {ctrl_ok}/{len(ctrl)} PASS (per shard, distinct suite/group: {len({(c[0],c[1]) for c in ctrl})})")
print(f"arms: {sum(1 for a in arms if a[3]=='KILLED')}/{len(arms)} KILLED")
print(f"assertion coverage: {len(expected)-len(missing)}/{len(expected)} missing={missing}")
for a in arms:
    if a[3] != "KILLED": print("UNPROVEN", a)
PY

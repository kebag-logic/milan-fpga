#!/usr/bin/env bash
# Disposable mutation probes: each perturbs one published input in a copy and
# shows that the figure the page relies on moves.  Usage: mutation_probes.sh <f1 work dir>
set -u
w=$1; cd "$w" || exit 2
probe() { name=$1; rm -rf "p_$name"; mkdir "p_$name"; cp -r author receipts "p_$name/"; }
# P1: move the first skip of 240 frames or more 100 reads later (48,000 frames): alignment must drop 236 -> 235
probe P1
python3 - p_P1/author/summary/a-long/continuity-events.csv <<'PY'
import csv, sys
p = sys.argv[1]; rows = list(csv.DictReader(open(p))); f = rows[0].keys()
for r in rows:
    if r["kind"] == "skip" and int(r["frames"]) >= 240:
        r["frame"] = str(int(r["frame"]) + 48000); break
rows.sort(key=lambda r: int(r["frame"]))
w = csv.DictWriter(open(p, "w", newline=""), fieldnames=list(f)); w.writeheader(); w.writerows(rows)
PY
python3 b5_round3.py figures p_P1/author p_P1/receipts > p_P1/out.txt 2>&1; echo "P1 rc=$?"
grep -E 'stall-aligned, a stall|not stall-aligned' p_P1/out.txt; grep -E 'stall-aligned, a stall|not stall-aligned' round3_figures.txt | sed 's/^/  baseline: /'
# P2: flatten the first stall in the read record to the 10 ms period: stalls must drop 220 -> 219
probe P2
python3 - p_P2/receipts <<'PY'
import hashlib, json, sys, numpy as np
d = sys.argv[1]; m = json.load(open(f"{d}/a-long-reads.json")); g = np.fromfile(f"{d}/a-long-reads.u16", dtype="<u2")
i = int(np.flatnonzero(g > 15000)[0]); g[i] = 10000; g.tofile(f"{d}/a-long-reads.u16")
m["record"]["sha256"] = hashlib.sha256(open(f"{d}/a-long-reads.u16", "rb").read()).hexdigest()
json.dump(m, open(f"{d}/a-long-reads.json", "w")); print("flattened read", i)
PY
python3 b5_attrib.py figures p_P2/author p_P2/receipts > p_P2/out.txt 2>&1; echo "P2 rc=$?"
grep -E '^stalls [0-9]+;|stalls followed' p_P2/out.txt; grep -E '^stalls [0-9]+;|stalls followed' attribution.txt | sed 's/^/  baseline: /'
# P3: plant a 48-frame (1 ms) delivery step at an off-stall cluster's floor: the 1 ms count must move
probe P3
python3 - p_P3/receipts p_P3/author <<'PY'
import csv, hashlib, json, sys, numpy as np
d, a = sys.argv[1], sys.argv[2]
m = json.load(open(f"{d}/a-long-reads.json")); g = np.fromfile(f"{d}/a-long-reads.u16", dtype="<u2")
c0 = m["window_frames"][0]
ev = [e for e in csv.DictReader(open(f"{a}/summary/a-long/continuity-events.csv")) if e["kind"] == "skip" and 2 <= int(e["frames"]) < 60]
st = set(np.flatnonzero(g > 15000).tolist())
for e in ev:
    r = (int(e["frame"]) - c0) // 480 + 1
    if all(abs(r - s) > 40 for s in st):
        g[r - 1] += 1000; break
g.tofile(f"{d}/a-long-reads.u16")
m["record"]["sha256"] = hashlib.sha256(open(f"{d}/a-long-reads.u16", "rb").read()).hexdigest()
json.dump(m, open(f"{d}/a-long-reads.json", "w")); print("planted +1 ms at read", r - 1)
PY
python3 b5_round3.py figures p_P3/author p_P3/receipts > p_P3/out.txt 2>&1; echo "P3 rc=$?"
grep -E 'floor steps by 1 ms' p_P3/out.txt; grep -E 'floor steps by 1 ms' round3_figures.txt | sed 's/^/  baseline: /'
# Second pass: the round-3 tool pins the page's record hash and the elapsed time,
# so a probe copy of it takes the mutated record's values (the pin itself is
# what P1/P3's first pass tripped).
fix() { d=$1
  python3 - "$d/receipts" <<'PY'
import json, sys, numpy as np
d = sys.argv[1]; m = json.load(open(f"{d}/a-long-reads.json"))
m["elapsed_us_record"] = int(np.fromfile(f"{d}/a-long-reads.u16", dtype="<u2").astype(np.int64).sum())
json.dump(m, open(f"{d}/a-long-reads.json", "w"))
PY
  sha=$(python3 -c "import json;print(json.load(open('$d/receipts/a-long-reads.json'))['record']['sha256'])")
  sed "s/2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961/$sha/" b5_round3.py > "$d/b5_round3_probe.py"; }
# P1b: P2's record (first stall flattened) through the round-3 alignment count: 236 -> 235 expected
fix p_P2; python3 p_P2/b5_round3_probe.py figures p_P2/author p_P2/receipts > p_P2/out3.txt 2>&1; echo "P1b rc=$?"
grep -E 'stall-aligned, a stall|not stall-aligned|^stalls' p_P2/out3.txt
# P3b: the planted 1 ms step through the 1 ms count: 22 -> 23 expected
fix p_P3; python3 p_P3/b5_round3_probe.py figures p_P3/author p_P3/receipts > p_P3/out3.txt 2>&1; echo "P3b rc=$?"
grep -E 'floor steps by 1 ms|clear read positions' p_P3/out3.txt

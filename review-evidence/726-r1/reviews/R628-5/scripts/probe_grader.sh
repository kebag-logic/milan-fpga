#!/bin/bash
# Reviewer probe: plant the pre-#726 FRAMES_RX law into a scratch copy of the
# bench grader and require the behave contract to fail.
# usage: probe_grader.sh <scratch-tree> <out.log>
t=$1; out=$2
f=$t/tb/tools/torture_campaign.py
cp "$f" "$f.orig"
python3 - "$f" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
old='''    "FRAMES_RX": ("per-frame", "IEEE 1722.1-2021 Table 7.157",'''
new='''    "FRAMES_RX": ("per-interval", "Milan v1.2 Table 5.6",'''
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
PY
cd "$t/tests" && PYTHONDONTWRITEBYTECODE=1 python3 -m behave --no-capture -f plain features/counters_contract_milan.feature > "$out" 2>&1
echo "planted-law behave rc=$?" >> "$out"
mv "$f.orig" "$f"
cd "$t/tests" && PYTHONDONTWRITEBYTECODE=1 python3 -m behave --no-capture -f plain features/counters_contract_milan.feature > "$out.restored" 2>&1
echo "restored behave rc=$?" >> "$out"

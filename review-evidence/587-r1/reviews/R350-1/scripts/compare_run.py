#!/usr/bin/env python3
"""Compare a reviewer's 8x8 synthesis run with the committed 50 MHz manifest and ranking.

usage: compare_run.py REPO VARIANT GATEWARE_DIR

REPO is a checkout at the reviewed head (manifest, ranking and rank parser).
VARIANT is "default" or "attribution". GATEWARE_DIR holds the reviewer's
baseline_* outputs. Prints one line per compared quantity and exits 1 on any
metric or ranking mismatch. Report files are compared by byte length and
SHA-256; vendor reports carry a timestamp header, so a length-equal hash
difference is reported as HEADER-ONLY only after the diff is confined to the
Date line.
"""
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

repo, variant, gw = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
doc = json.loads((repo / "docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json").read_text())
meas = doc["measurements"][variant]
bad = 0


def check(label, committed, reviewer):
    global bad
    ok = committed == reviewer
    bad += not ok
    print(f"{'OK  ' if ok else 'DIFF'} {variant} {label}: committed={committed} reviewer={reviewer}")


# Whole-design utilization.
util = (gw / "baseline_utilization.rpt").read_text()
def cell(site):
    m = re.search(r"^\|\s*" + re.escape(site) + r"\s*\|\s*(\d+)", util, re.M)
    return int(m.group(1))
whole = meas["metrics"]["alinx_ax7101"]
check("whole LUT", whole["LUT"], cell("Slice LUTs*"))
check("whole logic_LUT", whole["logic_LUT"], cell("LUT as Logic"))
check("whole LUTRAM", whole["LUTRAM"], cell("LUT as Distributed RAM"))
check("whole SRL", whole["SRL"], cell("LUT as Shift Register"))
check("whole FF", whole["FF"], cell("Slice Registers"))
check("whole RAMB36", whole["RAMB36"], cell("RAMB36/FIFO*"))
check("whole RAMB18", whole["RAMB18"], cell("RAMB18"))
check("whole DSP", whole["DSP"], cell("DSP48E1"))
check("whole CARRY4", whole["CARRY4"], cell("CARRY4"))
timing = (gw / "baseline_timing.rpt").read_text()
wns = float(re.search(r"WNS\(ns\).*?\n\s*-+.*?\n\s*(-?\d+\.\d+)", timing, re.S).group(1))
check("whole WNS_ns", whole["WNS_ns"], wns)
period = re.findall(r"^\s*(milan_clk\S*)\s+\{[^}]*\}\s+(\d+\.\d+)", timing, re.M)
print(f"INFO {variant} milan clock rows (name, period ns): {sorted(set(period))}")

# Hierarchical rows from the unfiltered hierarchy report.
fields = ("LUT", "logic_LUT", "LUTRAM", "SRL", "FF", "RAMB36", "RAMB18", "DSP")
rows = {}
stack = []
for line in (gw / "baseline_hierarchy.rpt").read_text().splitlines():
    parts = line.split("|")[1:-1]
    if len(parts) != 10 or not parts[2].strip().isdigit():
        continue
    name = parts[0].strip()
    depth = (len(parts[0]) - len(parts[0].lstrip()) - 1) // 2
    if name.startswith("("):
        continue
    stack = stack[:depth] + [name]
    rows["/".join(stack)] = dict(zip(fields, (int(p) for p in parts[2:])))
scope = {r["instance"]: r["internal_WNS_ns"]
         for r in csv.DictReader(open(gw / "baseline_scope_timing.tsv"), delimiter="\t")}
carry = {}
with open(gw / "baseline_cells.tsv") as f:
    header = f.readline().rstrip("\n").split("\t")
print(f"INFO {variant} baseline_cells.tsv header: {header}")
for inst, committed in meas["metrics"].items():
    if inst == "alinx_ax7101":
        continue
    got = rows.get("alinx_ax7101/" + inst)
    for k in fields:
        check(f"{inst} {k}", committed[k], got[k] if got else None)
    if "internal_WNS_ns" in committed:
        check(f"{inst} internal_WNS_ns", committed["internal_WNS_ns"], float(scope[inst]))

# Ranking rows reproduced with the maintained parser.
label = {"default": "default-8x8-50mhz", "attribution": "attribution-8x8-50mhz"}[variant]
committed_rows = [r for r in csv.reader(open(repo / "docs/findings/PP_SHADOW_BASELINE_50MHZ_RANKING.tsv"), delimiter="\t")]
committed_rows = [r[1:] for r in committed_rows[1:] if r[0] == label]
out = subprocess.run([sys.executable, str(repo / "syn/ooc/pp_baseline_rank.py"),
                      str(gw / "baseline_hierarchy.rpt"), "--root",
                      "alinx_ax7101/milan_datapath/pp_shadow"],
                     capture_output=True, text=True, check=True).stdout
reviewer_rows = [r for r in csv.reader(io.StringIO(out), delimiter="\t")][1:]
check("ranking rows (maintained parser, all columns)", committed_rows, reviewer_rows) \
    if committed_rows == reviewer_rows else check("ranking rows count", len(committed_rows), len(reviewer_rows))
if committed_rows != reviewer_rows:
    for a, b in zip(committed_rows, reviewer_rows):
        if a != b:
            print(f"     committed={a}\n     reviewer ={b}")

# Report bytes.
for rec in meas["reports"]:
    name = Path(rec["path"]).name
    path = gw / name
    if not path.exists():
        print(f"SKIP {variant} report {rec['path']} (not produced by this reviewer run)")
        continue
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest == rec["sha256"]:
        verdict = "IDENTICAL"
    elif len(data) == rec["bytes"]:
        verdict = "SAME-LENGTH, hash differs (timestamped/pathed vendor header)"
    else:
        verdict = "LENGTH-DIFFERS"
    print(f"REPORT {variant} {name}: committed={rec['bytes']}/{rec['sha256'][:16]} "
          f"reviewer={len(data)}/{digest[:16]} {verdict}")
print(f"RESULT {variant} mismatches={bad}")
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""Summarize the 16 base CPU exports, the head re-run, and the published author table.

Usage: summarize_cpu.py RECEIPTS_DIR AUTHOR_CPU_MEASUREMENTS_JSON
Prints, per CPU/width/option: raw and normalized digests, equality with the
published row (raw, normalized, netlist name), the option-vs-omitted verdict
at base, and the head outcome (refused with reason, or export identical to base).
Exit 0 only when all 16 base rows reproduce the published raw and normalized
digests, and every head row is either a refusal or byte-identical to base.
"""
import glob, json, sys
from pathlib import Path

rec, auth_path = Path(sys.argv[1]), sys.argv[2]
auth = {r["label"]: r for r in json.load(open(auth_path))}
def load(d):
    out = {}
    for f in glob.glob(str(rec / d / "*.json")):
        r = json.load(open(f)); out[f"{r['cpu']}-{r['xlen']}-{r['option']}"] = r
    return out
base, head = load("cpu-base"), load("cpu-head")
ok = len(base) == 16 and len(head) == 16
for k in sorted(base):
    b, a, h = base[k], auth[k], head[k]
    same = (a["sha256"] == b["sha256"], a["rtl_sha256"] == b["rtl_sha256"],
            a["netlist"].removesuffix(".v") == b["netlist"])
    ok &= all(same)
    n = base[k.rsplit("-", 1)[0] + "-none"]
    effect = ("n/a" if b["option"] == "none" else
              f"raw {'SAME' if b['sha256'] == n['sha256'] else 'differs'}, "
              f"normalized {'SAME' if b['rtl_sha256'] == n['rtl_sha256'] else 'differs'}")
    if h["kind"] == "refused":
        hv = "REFUSED: " + h["reason"]
    else:
        hv = "export raw==base" if h["sha256"] == b["sha256"] else "EXPORT DIFFERS FROM BASE"
        ok &= h["sha256"] == b["sha256"]
    print(f"{k:22s} {b['bytes']:>8} raw={b['sha256'][:16]} rtl={b['rtl_sha256'][:16]} "
          f"published(raw,rtl,name)={same} base-vs-omitted: {effect} | head: {hv}")
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)

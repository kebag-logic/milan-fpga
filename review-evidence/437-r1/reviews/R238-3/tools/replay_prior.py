#!/usr/bin/env python3
"""Replay the prior public rounds' recorded GitHub renderings through the
base and head walks at this head.

Usage: replay_prior.py <head-scripts> <base-scripts> <evidence-dir> <out.json>

Sources (fetched read-only from the public evidence tree at ccc7b2b1):
  R238-2 probes/batch1-4 and fuzz_seed238_complete (.jsonl: page + github)
  R237-3 receipts/minimal, minimal2, fuzz1 (.json: rendered) with pages/*.json
A row is a REGRESSION here when the base walk equals the recorded rendering
and the head walk does not. Recorded renderings are used as recorded; the
fixture drift check shows GitHub's responses byte-stable.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def walk(scripts, rows, tmp):
    src, dst = tmp.with_suffix(".in.json"), tmp.with_suffix(".out.json")
    src.write_text(json.dumps(rows))
    subprocess.run([sys.executable, "-B", str(HERE / "walk.py"), scripts, str(src), str(dst)], check=True)
    out = json.loads(dst.read_text())
    src.unlink()
    dst.unlink()
    return [r["walk"] for r in out]


def main():
    head, base, ev, out = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
    rows = []
    for name in ("batch1", "batch2", "batch3", "batch4_prior", "fuzz_seed238_complete"):
        for i, line in enumerate(open(ev / f"reviews_R238-2_probes_{name}.jsonl")):
            r = json.loads(line)
            rows.append({"source": f"R238-2 {name}", "name": r.get("name", f"{name}#{i}"),
                         "page": r["page"], "github": r["github"],
                         "their_verdict": r.get("verdict")})
    for name in ("minimal", "minimal2", "fuzz1"):
        rec = json.load(open(ev / f"reviews_R237-3_receipts_{name}.json"))
        pages = json.load(open(ev / f"reviews_R237-3_receipts_pages_{'fuzz_full_sample' if name == 'fuzz1' else name}.json"))
        for key, r in rec.items():
            rows.append({"source": f"R237-3 {name}", "name": key, "page": pages[key],
                         "github": r["rendered"], "their_verdict": (r.get("head") or {}).get("verdict")})
    walk_rows = [{"name": r["name"], "page": r["page"]} for r in rows]
    hw = walk(head, walk_rows, out.with_name("replay-head"))
    bw = walk(base, walk_rows, out.with_name("replay-base"))
    tally, regress = {}, []
    for r, h, b in zip(rows, hw, bw):
        r["head"], r["base"] = h, b
        r["head_agrees"], r["base_agrees"] = h == r["github"], b == r["github"]
        key = f"{r['source'].split()[0]} " + ("head=gh" if r["head_agrees"] else "head!=gh") + " " + \
              ("base=gh" if r["base_agrees"] else "base!=gh")
        tally[key] = tally.get(key, 0) + 1
        if r["base_agrees"] and not r["head_agrees"]:
            regress.append(r)
    out.write_text(json.dumps({"tally": tally, "regressions": regress}, indent=1))
    print(f"rows replayed: {len(rows)}")
    for k, v in sorted(tally.items()):
        print(f"  {k}: {v}")
    print(f"base agreed, head disagrees: {len(regress)}")
    for r in regress:
        print("  ", r["source"], r["name"], json.dumps(r["page"]), "gh", r["github"], "head", r["head"])


if __name__ == "__main__":
    main()

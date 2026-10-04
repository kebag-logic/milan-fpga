#!/usr/bin/env python3
"""Reviewer's own re-derivation of the #232 lane's Vivado figures from the published
evidence-r2/vivado extracts, independent of the author's tools/rederive.py.

Usage: vivado_rederive.py EVIDENCE_R2_DIR PUBLISH_MANIFEST_JSON
  EVIDENCE_R2_DIR        .../review-evidence/pp232-r1/author-r2/evidence-r2
  PUBLISH_MANIFEST_JSON  .../review-evidence/pp232-r1/MANIFEST.json (the archive's
                         original/published sha256 record, for path-redacted files)
Checks, per run directory:
  - every file that is published whole and is named in sources.tsv hashes to the
    raw-file record (the original, pre-redaction sha256 for redacted files);
  - the baseline.log digest in sources.tsv equals the vivado/README.md runs table;
then reads the figures from the reports and prints them with the head-minus-base
deltas. Exits 1 on any hash mismatch.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

RUNS = [
    "r1b-main-5c71928a-route-1x1", "r1b-head-6e950fea-route-1x1",
    "r1-base-f4167536-route-1x1", "r1-head-3ab2e4da-route-1x1",
    "r1-base-f4167536-ooc-1x1", "r1-head-3ab2e4da-ooc-1x1",
    "r1-base-f4167536-ooc-8x8", "r1-head-3ab2e4da-ooc-8x8",
]
PAIRS = [("route at the round-1b merge", RUNS[0], RUNS[1]),
         ("round 1 route", RUNS[2], RUNS[3]),
         ("standalone 1x1", RUNS[4], RUNS[5]),
         ("standalone 8x8", RUNS[6], RUNS[7])]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def util(text: str) -> dict:
    def row(name):
        # synthesis-only (ooc) reports star "Slice LUTs*"
        m = re.search(r"^\|\s*" + re.escape(name) + r"\**\s*\|\s*([\d.]+)\s*\|", text, re.M)
        return float(m.group(1)) if m else None
    out = {k: row(n) for k, n in (("lut", "Slice LUTs"), ("lut_logic", "LUT as Logic"),
                                  ("lut_mem", "LUT as Memory"), ("ff", "Slice Registers"),
                                  ("slice", "Slice"), ("ramb36", "RAMB36/FIFO*"),
                                  ("ramb18", "RAMB18"), ("dsp", "DSPs"), ("carry4", "CARRY4"))}
    return out


def hier(text: str, inst: str):
    m = re.search(r"^\|\s+" + re.escape(inst) + r"\s+\|\s*\S+\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|"
                  r"\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", text, re.M)
    if not m:
        return None
    lut, logic, lutram, srl, ff = map(int, m.groups())
    return {"lut": lut, "lutram": lutram, "ff": ff}


def timing(text: str):
    m = re.search(r"WNS\(ns\).*?\n.*?\n\s*(-?[\d.]+)\s+\S+\s+\d+\s+\d+\s+(-?[\d.]+)", text)
    return (float(m.group(1)), float(m.group(2))) if m else (None, None)


def main() -> int:
    ev = Path(sys.argv[1])
    pub = json.loads(Path(sys.argv[2]).read_text())
    orig = {e["file"].split("evidence-r2/", 1)[1]: e["original_sha256"]
            for e in pub if "evidence-r2/" in e["file"]}
    readme = (ev / "vivado/README.md").read_text()
    bad = 0
    fig = {}
    for run in RUNS:
        d = ev / "vivado" / run
        rec = {}
        for line in (d / "sources.tsv").read_text().splitlines()[1:]:
            name, size, digest = line.split("\t")
            rec[name] = (int(size), digest)
        whole = 0
        for name, (size, digest) in rec.items():
            p = d / name
            if not p.exists():
                continue
            key = f"vivado/{run}/{name}"
            got = orig.get(key, sha(p))  # pre-redaction digest where the archive redacted
            redacted = key in orig and orig[key] != sha(p)
            ok = got == digest
            whole += 1
            if not ok:
                bad += 1
            print(f"{run}/{name}: {'OK' if ok else 'MISMATCH'}"
                  f"{' (original digest; path-redacted on publication)' if redacted else ''}")
        blog = rec["baseline.log"][1]
        in_readme = blog in readme
        bad += 0 if in_readme else 1
        print(f"{run}: {whole} whole file(s) checked; baseline.log {blog[:16]}... "
              f"{'in' if in_readme else 'NOT in'} vivado/README.md")
        u = util((d / "baseline_utilization.rpt").read_text())
        h = (d / "baseline_hierarchy.rpt").read_text()
        wns, whs = timing((d / "timing-extract.txt").read_text())
        log = (d / "log-extract.txt").read_text()
        c7186 = len(re.findall(r"^baseline\.log:\d+: WARNING: \[Synth 8-7186\]", log, re.M))
        c4445 = len(re.findall(r"^baseline\.log:\d+: \S+: \[Synth 8-4445\]", log, re.M))
        hdr7186 = re.search(r"## Synth 8-7186: (\d+) diagnostic", log)
        fig[run] = dict(u, wns=wns, whs=whs, s7186=c7186, s4445=c4445,
                        notify=hier(h, "u_notify"), resp=hier(h, "u_resp"), d3=hier(h, "u_d3"))
        print(f"  util {u}")
        print(f"  WNS/WHS {wns} / {whs}; Synth 8-7186 lines {c7186} (header {hdr7186.group(1) if hdr7186 else '?'});"
              f" Synth 8-4445 lines {c4445}")
        print(f"  u_notify {fig[run]['notify']}  u_resp {fig[run]['resp']}  u_d3 {fig[run]['d3']}")
    print()
    for label, b, hd in PAIRS:
        fb, fh = fig[b], fig[hd]
        dl = lambda k: None if fb[k] is None or fh[k] is None else fh[k] - fb[k]
        f0 = lambda v: "n/a" if v is None else format(v, "+.0f")
        print(f"{label}: LUT {f0(dl('lut'))} (logic {f0(dl('lut_logic'))}, memory {f0(dl('lut_mem'))}),"
              f" FF {f0(dl('ff'))}, slice {f0(dl('slice'))},"
              f" CARRY4 {f0(dl('carry4'))}, WNS {fb['wns']} -> {fh['wns']}"
              f" ({(fh['wns'] - fb['wns']):+.3f}); u_notify LUT {fh['notify']['lut'] - fb['notify']['lut']:+d},"
              f" FF {fh['notify']['ff'] - fb['notify']['ff']:+d}")
    print(f"\nzero Synth 8-7186 at every head run: "
          f"{all(fig[r]['s7186'] == 0 for r in RUNS if 'head' in r)}; "
          f"base/main counts {[fig[r]['s7186'] for r in RUNS if 'head' not in r]}")
    print(f"hash mismatches: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Reviewer probes of the packet's figures check, each on an altered copy of the findings page and index
(or of one receipt) under a scratch directory; the real repository is passed as --repo. A probe passes when
the check exits non-zero and names the altered line.

usage: probe_figures_check.py <check_b16_figures.py> <repo root> <packet root> <scratch dir> <out.json>
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

CHECK, REPO, PACKET, SCRATCH, OUT = (Path(a).resolve() for a in sys.argv[1:6])
PAGE = REPO / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
README = REPO / "docs/findings/README.md"


def page_copy(name, target, old, new):
    d = SCRATCH / name / "docs" / "findings"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(PAGE, d / PAGE.name)
    shutil.copy(README, d / "README.md")
    f = d / target
    text = f.read_text(encoding="utf-8")
    assert text.count(old) == 1, (name, old, text.count(old))
    line = text[:text.index(old) + (1 if old.startswith("\n") else 0)].count("\n") + 1
    f.write_text(text.replace(old, new), encoding="utf-8")
    return d / PAGE.name, line


def packet_copy(name, rel, old, new):
    dst = SCRATCH / name / "packet"
    shutil.copytree(PACKET, dst)
    f = dst / rel
    t = f.read_text()
    assert t.count(old) >= 1, (rel, old)
    f.write_text(t.replace(old, new, 1))
    return dst


def run(name, page=PAGE, packet=PACKET):
    rows, cov = SCRATCH / f"{name}-rows.tsv", SCRATCH / f"{name}-cov.tsv"
    p = subprocess.run([sys.executable, "-I", str(CHECK), str(page), str(packet), str(rows), str(cov), "--repo", str(REPO)],
                       capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout


probes = []


def probe(name, page=PAGE, packet=PACKET, line=None, target="629_MEDIA_CLOCK_FOLLOWING_BENCH.md"):
    rc, out = run(name, page, packet)
    tag = (f"{target}:{line}" if target == "README.md" else f"\t{line}\t") if line else None
    named = tag is None or any(tag in x for x in out.splitlines() if x.startswith(("BAD", "UNCOVERED")))
    if line and target != "README.md":
        named = any((f"\t{line}\t" in x) or (f" {target}:{line} " in x) or (f"{target}:{line}" in x)
                    for x in out.splitlines() if x.startswith(("BAD", "UNCOVERED")))
    probes.append(dict(probe=name, rc=rc, named=named, verdict="PASS" if rc != 0 and named else "FAIL",
                       output=out.splitlines()[:4]))


pg, ln = page_copy("p1-b0-floor-count", PAGE.name, "\n| 997 Hz, channel 0 | 300 | 0 | 169 | -123.98 (-123.91)",
                   "\n| 997 Hz, channel 0 | 300 | 0 | 170 | -123.98 (-123.91)")
probe("p1: B0's floor count 169 shown as 170", pg, line=ln)
pg, ln = page_copy("p2-evidence-hash", PAGE.name, "`ecd9b4589b9508322c587938417550fa7dcb3a6eaee2065261e3ad73dabf6688`",
                   "`ecd9b4589b9508322c587938417550fa7dcb3a6eaee2065261e3ad73dabf6689`")
probe("p2: an evidence file's SHA-256 changed by one digit", pg, line=ln)
pg, ln = page_copy("p3-readme-figure", "README.md", "graded over 300 s at the DUT's TDM output. The servo read LOCKED 2.585",
                   "graded over 300 s at the DUT's TDM output. The servo read LOCKED 2.586")
probe("p3: the index row's LOCKED bracket 2.585 shown as 2.586", pg, line=ln, target="README.md")
pg, ln = page_copy("p4-inside-count", PAGE.name, "Of the 131, 23 lie there", "Of the 131, 24 lie there")
probe("p4: B0's degraded blocks inside the taps, 23 shown as 24", pg, line=ln)
pk = packet_copy("p5-receipt", "r2/source-receipt.json", '"both": 618', '"both": 619')
probe("p5: the source receipt's 618 changed to 619", packet=pk)
pg, ln = page_copy("p6-number-word", PAGE.name, "in thirteen runs", "in fourteen runs")
probe("p6: 'thirteen runs' shown as 'fourteen runs'", pg, line=ln)
OUT.write_text(json.dumps(dict(probes=probes), indent=1))
for p in probes:
    print(p["verdict"], p["probe"], "rc", p["rc"], "named", p["named"])
sys.exit(0 if all(p["verdict"] == "PASS" for p in probes) else 1)

#!/usr/bin/env python3
"""Probe the published checker on altered documents only.

Usage: python3 probe_figure_coverage.py REPO EVIDENCE_PACKET REVIEW_PACKET
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys

repo, evidence, output = [Path(x).resolve() for x in sys.argv[1:4]]
page = repo / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
text = page.read_text()
anchor = "| Attribution | No loss in the network or the DUT | Every stage at the path's floor. See [B16c: attribution](#b16c-attribution) |"
assert text.count(anchor) == 1
mutations = {
    "summary_count": ("LOCKED at 596 of 596 | -6.000", "LOCKED at 595 of 596 | -6.000"),
    "attribution_median": ("At (a), medians are -123.98/-123.97 dB for B-CRF", "At (a), medians are -123.98/-123.96 dB for B-CRF"),
    "b0_overlap": ("23 degraded blocks at (c), down to -100.61", "24 degraded blocks at (c), down to -100.61"),
    "floor_count": ("303 of the 303 wholly inside the playback", "305 of the 303 wholly inside the playback"),
    "new_plain_figure": (anchor, anchor.replace("Every stage", "The measured residual was 7.25 ppm. Every stage")),
    "new_quoted_figure": (anchor, anchor.replace("Every stage", 'The measured residual was "7.25 ppm". Every stage')),
    "new_linked_figure": (anchor, anchor.replace("Every stage", "The measured residual was [7.25 ppm](#b16c-attribution). Every stage")),
}
results = []
for name, (old, new) in mutations.items():
    assert old in text
    d = output / "scratch/coverage-probes" / name
    d.mkdir(parents=True, exist_ok=True)
    changed = d / page.name
    changed.write_text(text.replace(old, new, 1))
    shutil.copyfile(page.parent / "README.md", d / "README.md")
    proc = subprocess.run([sys.executable, "-I", str(evidence / "tools/check_b16_figures.py"),
                           str(changed), str(evidence), str(d / "rows.tsv"), str(d / "coverage.tsv"),
                           "--repo", str(repo)], capture_output=True, text=True, timeout=60)
    summary = json.loads(proc.stdout.splitlines()[0])
    line = text[:text.index(old)].count("\n") + 1
    result = {"probe": name, "line": line, "old": old, "new": new, "expected_rc": 1,
              "observed_rc": proc.returncode, "summary": summary, "detected": proc.returncode == 1}
    results.append(result)
    (output / "receipts" / ("probe-" + name + ".log")).write_text(proc.stdout + proc.stderr)
    print(json.dumps(result))
(output / "receipts/figure-coverage-probes.json").write_text(json.dumps(results, indent=2) + "\n")
sys.exit(0 if all(x["detected"] for x in results) else 1)

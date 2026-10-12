#!/usr/bin/env python3
"""Run isolated coverage probes. Usage: probe_coverage.py REPO AUTHOR_PACKET OUT_DIR."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

repo, packet, out = (Path(x).resolve() for x in sys.argv[1:4])
scratch = out / "scratch" / "coverage-probes"
scratch.mkdir(parents=True, exist_ok=True)
page = repo / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
anchor = "| Attribution | No loss in the network or the DUT | Every stage at the path's floor. See [B16c: attribution](#b16c-attribution) |"
original = page.read_text()
assert original.count(anchor) == 1
cases = {
    "plain": "The measured residual was 7.25 ppm. ",
    "quoted": 'The measured residual was "7.25 ppm". ',
    "linked": "The measured residual was [7.25 ppm](#b16c-attribution). ",
    "code": "The measured residual was `7.25 ppm`. ",
    "quoted_number": 'The measured residual was "7.25" ppm. ',
    "clause_unit": "The measured residual was IEEE 1722.1 ppm. ",
    "descriptor_unit": "The measured residual was CLOCK_DOMAIN 7 ppm. ",
    "leading_decimal": "The measured residual was .25 ppm. ",
    "negative_leading_decimal": "The measured residual was -.25 ppm. ",
    "scientific": "The measured residual was 7e2 ppm. ",
    "descriptor_double_space": "The measured residual was CLOCK_DOMAIN 7  ppm. ",
    "unbound_continuation": "Channel 2 reports samples:",
}
results = []
for name, insertion in cases.items():
    d = scratch / name
    d.mkdir(exist_ok=True)
    target = d / page.name
    if name == 'unbound_continuation':
        old = "The tone sits in channels 0 and 1 of the peer's talker stream. Channels 2 and"
        new = "The tone sits in channels 0 and 1 of the peer's talker stream. " + insertion
        assert original.count(old) == 1
        target.write_text(original.replace(old, new))
        line = original[:original.index(old)].count('\n') + 1
    else:
        target.write_text(original.replace(anchor, anchor.replace("Every stage", insertion + "Every stage")))
        line = original[:original.index(anchor)].count('\n') + 1
    shutil.copyfile(page.parent / "README.md", d / "README.md")
    cmd = [sys.executable, "-I", str(packet / "tools/check_b16_figures.py"),
           str(target), str(packet), str(d / "rows.tsv"), str(d / "coverage.tsv"), "--repo", str(repo)]
    p = subprocess.run(cmd, text=True, capture_output=True, timeout=120)
    summary = json.loads(p.stdout.splitlines()[0])
    rec = {"case": name, "insertion": insertion, "rc": p.returncode,
           "summary": summary, "stdout": p.stdout, "stderr": p.stderr,
           "line": line}
    if name == 'unbound_continuation':
        rec.update(old=old, new=new, following_line='3 carry -1 to 0 LSB at every point, and McASP0\'s channels 4 to 7, unmapped,')
    results.append(rec)
    print(name, p.returncode, summary)
(out / "coverage-probes.json").write_text(json.dumps(results, indent=2) + "\n")
sys.exit(0 if all(r['rc'] == 1 for r in results) else 1)

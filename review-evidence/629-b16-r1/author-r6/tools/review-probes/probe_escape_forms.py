#!/usr/bin/env python3
"""R624-4: probe the round-4 figures check with number forms its tokenizer may not read.

usage: probe_escape_forms.py <repo> <author packet> <scratch dir> <out.json>

Each probe inserts one sentence into a copy of the findings page, on the B16c attribution row R625-3's
probe used, and runs the packet's check on the copy with the real repository as --repo. A probe is
DETECTED when the check exits 1. Documents only; the repository is not written.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

repo, packet, scratch, out = (Path(a).resolve() for a in sys.argv[1:5])
page = repo / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
text = page.read_text(encoding="utf-8")
anchor = "| Attribution | No loss in the network or the DUT | Every stage at the path's floor."
assert text.count(anchor) == 1
forms = {
    "control_plain": "The measured residual was 7.25 ppm.",
    "glued_integer_s": "The residual settled in 26s.",
    "glued_integer_dB": "The residual sat 10dB above the floor.",
    "glued_integer_ms": "The probe answered after 300ms.",
    "glued_decimal_ppm": "The measured residual was 7.25ppm.",
    "leading_dot_ppm": "The measured residual was .5 ppm.",
    "range_hyphen_second_end": "The residual stayed under 2.585-9.99 s.",
    "unicode_minus_dB": "The floor was −130.00 dB.",
}
res = []
for name, sent in forms.items():
    d = scratch / name / "docs" / "findings"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(page.parent / "README.md", d / "README.md")
    (d / page.name).write_text(text.replace(anchor, anchor.replace("Every stage", sent + " Every stage")), encoding="utf-8")
    p = subprocess.run([sys.executable, "-I", str(packet / "tools/check_b16_figures.py"), str(d / page.name), str(packet),
                        str(d / "rows.tsv"), str(d / "cov.tsv"), "--repo", str(repo)], capture_output=True, text=True, timeout=600)
    unc = [x for x in (d / "cov.tsv").read_text().splitlines() if x.endswith("\tUNCOVERED")]
    res.append({"probe": name, "inserted": sent, "rc": p.returncode, "detected": p.returncode == 1,
                "uncovered": unc, "summary": json.loads(p.stdout.splitlines()[0])})
    print(name, "rc", p.returncode, "uncovered", [u.split("\t")[1] for u in unc])
json.dump(res, open(out, "w"), indent=1)

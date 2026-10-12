#!/usr/bin/env python3
"""Reviewer probe: restore pre-round-3 guards in a scratch copy of
tb/tools/torture_campaign.py and require that the standing self-test fails,
then that it passes with the detecting test removed (escape control).
Usage: probe_grader_guards.py REPO SCRATCH"""
import shutil, subprocess, sys
from pathlib import Path
repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
PLANTS = {
    # old zero guard: frx==0 snapshots can PASS / divide; ratio total/frx
    "zero-guard": [("    if frx > 0 and abs(total - frx) <= tolerance:",
                    "    if abs(total - frx) <= tolerance:"),
                   ("    if total > frx:", "    if frx and total > frx:")],
    # suppress interval-rate side findings in the pair and concurrent helpers
    "suppress-interval": [("    return sem, [role for role in ticks if sem[role] == \"interval\"]",
                           "    return sem, []")],
}
DETECTORS = {"zero-guard": ["test_unpublished_zero_receive_snapshot"],
             "suppress-interval": ["test_packet_agreement_attributes_interval_sides",
                                   "test_concurrent_packet_law_attributes_each_direction"]}
rc_all = 0
for name, edits in PLANTS.items():
    d = scratch / f"grader_{name}"
    if d.exists(): shutil.rmtree(d)
    (d / "tb/tools").mkdir(parents=True)
    src = (repo / "tb/tools/torture_campaign.py").read_text()
    for old, new in edits:
        assert src.count(old) == 1, (name, old, src.count(old))
        src = src.replace(old, new)
    (d / "tb/tools/torture_campaign.py").write_text(src)
    for extra in ("tb/tools/torture_plan.py",):
        if (repo / extra).exists(): shutil.copy(repo / extra, d / extra)
    r = subprocess.run([sys.executable, "-I", str(d / "tb/tools/torture_campaign.py"), "--self-test"],
                       capture_output=True, text=True, cwd=d)
    out = r.stdout + r.stderr
    hits = [t for t in DETECTORS[name] if (f"FAIL: {t}" in out or f"ERROR: {t}" in out)]
    print(f"{name}: plant rc={r.returncode} detecting={hits}")
    (scratch / f"grader_{name}.log").write_text(out)
    # escape: drop detecting tests by renaming them so unittest does not collect them
    for t in DETECTORS[name]:
        src = src.replace(f"def {t}(", f"def _omitted_{t}(")
    (d / "tb/tools/torture_campaign.py").write_text(src)
    r2 = subprocess.run([sys.executable, "-I", str(d / "tb/tools/torture_campaign.py"), "--self-test"],
                        capture_output=True, text=True, cwd=d)
    out2 = r2.stdout + r2.stderr
    ran = [l for l in out2.splitlines() if l.startswith("Ran ")]
    print(f"{name}: escape rc={r2.returncode} {ran}")
    (scratch / f"grader_{name}_escape.log").write_text(out2)
    if r.returncode == 0 or not hits or r2.returncode != 0: rc_all = 1
sys.exit(rc_all)

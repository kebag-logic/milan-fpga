#!/usr/bin/env python3
"""R624-5: escape forms against the round-5 per-digit figures check (documents only, offline).

usage: probe_r624_5_escapes.py <repo> <author packet> <scratch dir> <out.json>

Each probe inserts one sentence on the B16c summary's attribution row (the row the earlier probes used) in a
copy of the findings page and runs the packet's check on the copy with the real repository as --repo. A probe
is DETECTED when the check exits 1 AND names, on standard output, an UNCOVERED number on the inserted line
whose spelling is the inserted digits. Controls (a free number, no identifier keyword) must be detected; the
'id+' forms put identifier-bound digits before a unit spelling or separator outside the check's MEASURE list.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

repo, packet, scratch, out = (Path(a).resolve() for a in sys.argv[1:5])
page = repo / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
text = page.read_text(encoding="utf-8")
anchor = "| Attribution | No loss in the network or the DUT | Every stage at the path's floor."
assert text.count(anchor) == 1
line = text[:text.index(anchor)].count("\n") + 1
FORMS = {
    "control: free number before milliseconds": ("The residual settled in 7 milliseconds.", "7"),
    "control: descriptor index before ms": ("The residual sat at CLOCK_DOMAIN 7 ms.", "7"),
    "id+ milliseconds": ("The residual sat at CLOCK_DOMAIN 7 milliseconds.", "7"),
    "id+ microseconds": ("The residual sat at CLOCK_DOMAIN 7 microseconds.", "7"),
    "id+ nanoseconds": ("The residual sat at CLOCK_DOMAIN 7 nanoseconds.", "7"),
    "id+ msec": ("The residual sat at CLOCK_DOMAIN 7 msec.", "7"),
    "id+ decibels": ("The residual sat at CLOCK_DOMAIN 7 decibels.", "7"),
    "id+ hertz": ("The residual sat at CLOCK_DOMAIN 7 hertz.", "7"),
    "id+ kilohertz": ("The residual sat at CLOCK_DOMAIN 7 kilohertz.", "7"),
    "id+ dBm": ("The residual sat at CLOCK_DOMAIN 7 dBm.", "7"),
    "id+ parts per million": ("The residual sat at CLOCK_DOMAIN 7 parts per million.", "7"),
    "id+ per cent": ("The residual sat at CLOCK_DOMAIN 7 per cent.", "7"),
    "id+ underruns": ("The playback logged channel 3 underruns.", "3"),
    "id+ events": ("The decode found STREAM_INPUT 2 events.", "2"),
    "id+ drops": ("The listener made channels 0 and 4 drops.", "4"),
    "id+ lane name before milliseconds": ("The lock took B16 milliseconds.", "16"),
    "id+ clause before milliseconds": ("The lock took IEEE 1722.1 milliseconds.", "1722.1"),
    "id+ closing paren": ("The residual (CLOCK_DOMAIN 7) ppm.", "7"),
    "id+ single quotes": ("The residual sat at CLOCK_DOMAIN 7 'ppm'.", "7"),
    "id+ colon": ("The residual sat at CLOCK_DOMAIN 7: ppm.", "7"),
    "id+ slash": ("The residual sat at CLOCK_DOMAIN 7/ppm.", "7"),
    "word: a million frames": ("The decode held a million frames.", None),
    "word: thousands of frames": ("The decode held thousands of frames.", None),
    "word: a dozen slips": ("The ring made a dozen slips.", None),
    "word: seven milliseconds": ("The lock took seven milliseconds.", "seven"),
}
res = []
for name, (sent, num) in FORMS.items():
    d = scratch / re.sub(r"\W+", "_", name) / "docs" / "findings"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    shutil.copy(page.parent / "README.md", d / "README.md")
    (d / page.name).write_text(text.replace(anchor, anchor.replace("Every stage", sent + " Every stage")), encoding="utf-8")
    p = subprocess.run([sys.executable, "-I", str(packet / "tools/check_b16_figures.py"), str(d / page.name), str(packet),
                        str(d / "rows.tsv"), str(d / "cov.tsv"), "--repo", str(repo)], capture_output=True, text=True, timeout=600)
    unc = [l for l in p.stdout.splitlines() if l.startswith("UNCOVERED")]
    named = [l for l in unc if l.split()[1].endswith(f":{line}") and num is not None and l.split()[2] == num]
    res.append(dict(probe=name, inserted=sent, rc=p.returncode, detected=p.returncode == 1 and bool(named),
                    named=named[:2], summary=json.loads(p.stdout.splitlines()[0])))
    print(f"{name:42s} rc={p.returncode} detected={res[-1]['detected']}")
Path(out).write_text(json.dumps(dict(line=line, probes=res), indent=1, ensure_ascii=False) + "\n")

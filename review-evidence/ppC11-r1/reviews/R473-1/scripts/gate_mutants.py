#!/usr/bin/env python3
"""Mutation probe of the two new gates' self-tests (reviewer-owned, disposable).

Each mutant is one exact text substitution in a copy of scripts/check-ids.py or
scripts/check-figures.py. A mutant is KILLED when the copy's own `--selftest`
(the step `make ids` / `make figures` runs first in CI) exits non-zero.
Usage: gate_mutants.py <repo> <scratch-dir>; the repo is only read."""
import concurrent.futures as cf
import pathlib
import subprocess
import sys

REPO, SCRATCH = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
MUTANTS = {
    "check-ids.py": [
        ("scan only tb/", 'SCAN_DIRS = ("docs", "hdl", "tb")', 'SCAN_DIRS = ("tb",)'),
        ("scan drops hdl/", 'SCAN_DIRS = ("docs", "hdl", "tb")', 'SCAN_DIRS = ("docs", "tb")'),
        ("scan drops docs/", 'SCAN_DIRS = ("docs", "hdl", "tb")', 'SCAN_DIRS = ("hdl", "tb")'),
        ("untracked files skipped", '"--cached", "--others",', '"--cached",'),
        ("every use resolves", "    if token in rows:\n        return True", "    if True:\n        return True"),
        ("every family resolves", 'if kind == "family":\n        return token in rows or', 'if kind == "family":\n        return True or'),
        ("minus-n without stem", "return tail.isdigit() and stem in rows", "return tail.isdigit()"),
        ("braces read as family", "braces = BRACES.match(text, end)", "braces = None"),
        ("every file binary", 'if b"\\0" in data[:8192]:', "if True:"),
        ("check always rc 0", "return 1 if problems else 0\n\n\nSELFTEST", "return 0\n\n\nSELFTEST"),
        ("master table = whole page", 'return "\\n".join(lines)', "return body"),
        ("sibling shorthand ignored", 'names += [f"{stem}-{tail}" for tail in SIBLING.findall(cell)]', "pass"),
        ("unreadable table passes", 'print("ids: master tables unreadable, FAILURES")\n        return 1', 'print("ids: master tables unreadable, FAILURES")\n        return 0'),
    ],
    "check-figures.py": [
        ("other formats pass", 'problems.append(f"{rel}: not a figure format docs/README.md section 3 lists")', "pass"),
        ("svg content unchecked", "    try:\n        svg = ET.parse(path).getroot()", "    return []\n    try:\n        svg = ET.parse(path).getroot()"),
        ("link check dropped", "if rel not in linked:", "if False:"),
        ("inventory ghost rows pass", "for name in sorted(set(hand) - names):", "for name in []:"),
        ("orphan WaveDrom passes", "if name[9:-4] not in anchors:", "if False:"),
        ("draw.io export unchecked", "if export not in names:", "if False:"),
        ("unlisted SVG passes", "if name not in hand:", "if False:"),
        ("untracked files skipped", '"--cached", "--others",', '"--cached",'),
        ("only namespaced <image>", 'svg.find(f".//{SVG_NS}{tag}") is not None or svg.find(f".//{tag}") is not None', 'svg.find(f".//{tag}") is not None'),
        ("viewBox unchecked", 'if "viewBox" not in svg.attrib:', "if False:"),
        ("check always rc 0", "return 1 if problems else 0\n\n\nGOOD_SVG", "return 0\n\n\nGOOD_SVG"),
        ("missing inventory passes", 'print("figures: inventory unreadable, FAILURES")\n        return 1', 'print("figures: inventory unreadable, FAILURES")\n        return 0'),
    ],
}


def one(script: str, idx: int, label: str, old: str, new: str) -> str:
    src = (REPO / "scripts" / script).read_text()
    if src.count(old) != 1:
        return f"{script}\tM{idx:02d}\tNOT-APPLIED\t{label}"
    d = SCRATCH / f"{script}-M{idx:02d}"
    (d / "scripts").mkdir(parents=True, exist_ok=True)
    (d / "scripts" / script).write_text(src.replace(old, new))
    p = subprocess.run([sys.executable, str(d / "scripts" / script), "--selftest"],
                       capture_output=True, text=True, timeout=300)
    verdict = "KILLED" if p.returncode != 0 else "SURVIVED"
    return f"{script}\tM{idx:02d}\t{verdict}\t{label}"


jobs = [(s, i, *m) for s, ms in MUTANTS.items() for i, m in enumerate(ms, start=1)]
with cf.ThreadPoolExecutor(max_workers=12) as ex:
    rows = list(ex.map(lambda j: one(*j), jobs))
for r in rows:
    print(r)
print(f"total {len(rows)}: killed {sum('KILLED' in r for r in rows)}, "
      f"survived {sum('SURVIVED' in r for r in rows)}, "
      f"not applied {sum('NOT-APPLIED' in r for r in rows)}")

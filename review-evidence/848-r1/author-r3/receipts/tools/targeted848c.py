#!/usr/bin/env python3
"""Plant the ruling's mutants and adversarial variants in a copy of docs_inventory.py; each must be killed.

Usage: targeted.py SOURCE.py WORKDIR. Every substitution must match exactly once, or the run stops.
"""
import concurrent.futures, pathlib, subprocess, sys
ROUTE = "grouped.setdefault(lanes[finding.page], [])"
WRITE = '(directory / f"{slug}.md").write_text("\\n".join(body), encoding="utf-8")'
WIN = "BANNER_SCAN_LINES = 15"
M = [
 ("W8/W11 every finding under one lane", ROUTE, 'grouped.setdefault("one lane", [])'),
 ("W9/W12 a copy filed under its origin's lane", ROUTE, "grouped.setdefault(lanes[finding.origin or finding.page], [])"),
 ("L1 a recorded finding filed under the copy's lane", ROUTE, 'grouped.setdefault(lanes[finding.page] if finding.origin else "reference", [])'),
 ("L2 a copy filed under a named wrong lane", ROUTE, 'grouped.setdefault("overview and guides" if finding.origin else lanes[finding.page], [])'),
 ("L3 lanes merged into one file, sections kept, appended", WRITE,
  'open(directory / "all.md", "a", encoding="utf-8").write("\\n".join(body))'),
 ("L4 lanes merged into one file, reference section first", "for lane, entries in sorted(grouped.items()):", "for lane, entries in sorted(grouped.items(), reverse=True):",
  WRITE, 'open(directory / "all.md", "a", encoding="utf-8").write("\\n".join(body))'),
 ("L5 every lane overwrites one file", 'slug = re.sub(r"[^a-z0-9]+", "-", lane.lower()).strip("-")', 'slug = "all"'),
 ("L6 lane title names no lane", 'f"# D0 findings: {lane}"', '"# D0 findings"'),
 ("N14 window 14", WIN, "BANNER_SCAN_LINES = 14"),
 ("N16 window 16", WIN, "BANNER_SCAN_LINES = 16"),
 ("N17 window 17", WIN, "BANNER_SCAN_LINES = 17"),
 ("N18 window 18", WIN, "BANNER_SCAN_LINES = 18"),
 ("N19 window 19", WIN, "BANNER_SCAN_LINES = 19"),
 ("N5 window 5", WIN, "BANNER_SCAN_LINES = 5"),
 ("N10000 window 10000", WIN, "BANNER_SCAN_LINES = 10000"),
]
def run(job):
    n, spec, text, work = job
    d = work / f"t{n:02d}" / "scripts"; d.mkdir(parents=True, exist_ok=True)
    (d / "docs_inventory.py").write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(d / "docs_inventory.py"), "--selftest"], capture_output=True, text=True, timeout=400)
    fails = [l for l in r.stdout.splitlines() if l.startswith("selftest: FAIL")]
    verdict = "killed" if r.returncode and fails else ("SURVIVED" if r.returncode == 0 else "CRASHED")
    return f"{verdict:8} rc={r.returncode} fails={len(fails):<2} {spec[0]} :: {(fails[0][15:105] if fails else r.stderr.strip()[-90:])}"
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
work = pathlib.Path(sys.argv[2])
jobs = []
for n, spec in enumerate(M):
    text = src
    for old, new in zip(spec[1::2], spec[2::2]):
        assert text.count(old) == 1, (spec[0], text.count(old))
        text = text.replace(old, new)
    jobs.append((n, spec, text, work))
with concurrent.futures.ThreadPoolExecutor(8) as pool:
    rows = list(pool.map(run, jobs))
print("\n".join(rows))
print(f"TOTAL {len(rows)} killed {sum(r.startswith('killed') for r in rows)} not killed {sum(not r.startswith('killed') for r in rows)}")

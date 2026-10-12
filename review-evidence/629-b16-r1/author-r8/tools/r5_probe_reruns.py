#!/usr/bin/env python3
"""Lane B16, round 5: the reviews' published probes, run unchanged against this packet's check (offline).

usage: r5_probe_reruns.py <repo> <packet root> <probes dir> <scratch dir> <page commit>

The probes are the reviews' own scripts, copied unchanged into <probes dir> from the branch
629-b16-review-evidence: R624-4's tools/probe_escape_forms.py, R625-4's probe_coverage.py and R625-3's
probe_figure_coverage.py (also under R625-4/). Each is refused unless its SHA-256 equals the published
one. Each runs with its own arguments, inserts its forms into a copy of the findings page and runs the
packet's check on the copy; a form is detected when the check exits 1. Each probe's own results file is
kept verbatim under "results" in r5/<review>-probe-rerun.json, with the probe's exit status and how many
of its forms were detected. Nothing on the bench is read or written.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO, PACKET, PROBES, SCRATCH = (Path(a).resolve() for a in sys.argv[1:5])
COMMIT = sys.argv[5]
PROBE = {  # name: (file, published SHA-256, published path, argv after the script, its results file, detected)
    "r624-4": ("probe_escape_forms.py", "5c2dbc691e469d236227bc90d4d131ad1fc116f0b002813c02beef2374ae3c26",
               "R624-4/tools/probe_escape_forms.py", lambda o: [REPO, PACKET, o / "scratch", o / "out.json"],
               lambda o: o / "out.json", lambda r: [x["detected"] for x in r]),
    "r625-4": ("probe_coverage.py", "e8749cbecfe73ef6f07261d1416122094d51745954a62fa6851d4e0521dfd0fb",
               "R625-4/probe_coverage.py", lambda o: [REPO, PACKET, o],
               lambda o: o / "coverage-probes.json", lambda r: [x["rc"] == 1 for x in r]),
    "r625-3": ("probe_figure_coverage.py", "f4c4d91bdfea9b6428e3e5a587ba87577003cc9e67ba08c852149d2ec3cddb32",
               "R625-3/scripts/probe_figure_coverage.py and R625-4/probe_figure_coverage.py", lambda o: [REPO, PACKET, o],
               lambda o: o / "receipts/figure-coverage-probes.json", lambda r: [x["detected"] for x in r]),
}


def main() -> int:
    ok = True
    for name, (script, want, where, argv, res, det) in PROBE.items():
        p = PROBES / script
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        assert got == want, f"{script}: SHA-256 {got}, published {want}"
        o = SCRATCH / name
        (o / "receipts").mkdir(parents=True, exist_ok=True)
        run = subprocess.run([sys.executable, "-I", str(p), *map(str, argv(o))], capture_output=True, text=True,
                             timeout=600)
        results = json.loads(res(o).read_text())
        found = det(results)
        out = dict(note=f"Lane B16 round 5: {name.upper()}'s published probe, {where} under "
                        "review-evidence/629-b16-r1/reviews/ on branch 629-b16-review-evidence, run unchanged against "
                        f"this packet's check and the page at {COMMIT[:8]}; its own results file, verbatim, under "
                        "'results'. Offline, no bench action",
                   probe=script, probe_sha256=got, page_commit=COMMIT, exit=run.returncode, probes=len(found),
                   detected=sum(found), results=results)
        (PACKET / f"r5/{name}-probe-rerun.json").write_text(json.dumps(out, indent=1) + "\n")
        print(name, "exit", run.returncode, "detected", sum(found), "of", len(found))
        ok &= all(found)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

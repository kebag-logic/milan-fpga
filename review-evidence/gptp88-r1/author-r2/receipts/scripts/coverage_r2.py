"""Map each parent check new in round 2 to the companion mutants that fail it.

usage: coverage_r2.py <round-1 snapshot repo> <round-1 rev> <round-2 repo>
                      <round-2 rev> <mutant log dir> <out md>
New names: expect("...") literals in the gptp_shadow and milan_dp gPTP
harnesses at the round-2 snapshot but not at the round-1 snapshot.
"""
import re
import subprocess
import sys
from pathlib import Path

r1_repo, r1, r2_repo, r2, logdir, out = sys.argv[1:7]


def show(repo, rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


LIT = re.compile(r'expect\(\s*"([^"]+)"')
SUITES = {
    "gptp_shadow": "tb/verilator/gptp_shadow/sim_main.cpp",
    "milan_dp gptp": "tb/verilator/milan_dp/sim_gptp.cpp",
}
new = []
for suite, path in SUITES.items():
    before = set(LIT.findall(show(r1_repo, r1, path)))
    after = LIT.findall(show(r2_repo, r2, path))
    new += [(suite, n) for n in dict.fromkeys(after) if n not in before]
fails = {}
for log in sorted(Path(logdir).glob("*.log")):
    lines = log.read_text().splitlines()
    if lines and lines[0].startswith("mutant: "):
        fails[lines[0][8:]] = [l for l in lines if l.startswith("FAIL ")]


def failed(name, lines):
    return any(re.match(r"FAIL " + re.escape(name) + r"(?:\s|$)", l)
               for l in lines)


rows = [(s, n, sorted(m for m, f in fails.items() if failed(n, f)))
        for s, n in new]
unc = [(s, n) for s, n, by in rows if not by]
with open(out, "w") as f:
    f.write("# Round-2 parent checks and the companion mutants that fail "
            "them\n\n")
    f.write(f"{len(rows)} check names new since the round-1 companion; "
            f"{len(rows) - len(unc)} of {len(rows)} fail under at least one "
            f"planted mutant ({len(fails)} mutants).\n\n")
    for s, n, by in rows:
        f.write(f"- [{s}] {n} <- {'; '.join(by) if by else 'NONE'}\n")
print(len(rows), "new;", len(unc), "uncovered")
for s, n in unc:
    print("UNCOVERED", s, n)

"""Map each check the companion adds to the companion mutants that fail it.

usage: companion_coverage.py <parent clone> <base rev> <head rev> <mutant log dir> <out md>
New names: expect("...") literals in the gptp_shadow and milan_dp gPTP
harnesses at head but not at base, and the tsn_fuzz gPTP campaign's
committed check list (TEST_RESULTS.md) at head but not at base.
"""
import re, subprocess, sys
from pathlib import Path
P, base, head, logdir, out = sys.argv[1:6]
def show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], cwd=P, capture_output=True,
                          text=True, check=True).stdout
LIT = re.compile(r'expect\(\s*"([^"]+)"')
suites = {
    "gptp_shadow": "tb/verilator/gptp_shadow/sim_main.cpp",
    "milan_dp gptp": "tb/verilator/milan_dp/sim_gptp.cpp",
}
new = []
for s, f in suites.items():
    b = set(LIT.findall(show(base, f))); h = LIT.findall(show(head, f))
    new += [(s, n) for n in dict.fromkeys(h) if n not in b]
TR = "hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md"
def checks(text):
    return [l[2:].strip() for l in text.splitlines() if l.startswith("* ")]
b = set(checks(show(base, TR))); h = checks(show(head, TR))
new += [("tsn_fuzz ptp", n) for n in dict.fromkeys(h) if n not in b]
#: checks only renamed to match the new prior state, the assertion unchanged
RENAMED = {
    "kept to explicit GM emits one AS_PATH push":
        "absent to explicit GM emits one AS_PATH push",
    "{thisClock} to maximum path advances generation once":
        "empty to maximum path advances generation once",
}
fails = {}
for log in sorted(Path(logdir).glob("*.log")):
    lines = log.read_text().splitlines()
    if not lines or not lines[0].startswith("mutant: "):
        continue
    fails[lines[0][8:]] = [l for l in lines if l.startswith(("FAIL ", "[FAIL] "))]
def failed(n, ls):
    return any(re.match(r"(?:FAIL|\[FAIL\]) " + re.escape(n) + r"(?:\s|$)", l)
               for l in ls)
renamed = [(s, n) for s, n in new if n in RENAMED]
new = [(s, n) for s, n in new if n not in RENAMED]
rows = [(s, n, sorted(m for m, f in fails.items() if failed(n, f))) for s, n in new]
unc = [(s, n) for s, n, by in rows if not by]
with open(out, "w") as f:
    f.write("# milan-fpga companion: checks new at the snapshot and the mutants that fail them\n\n")
    f.write(f"{len(rows)} new check names; {len(rows) - len(unc)} of {len(rows)} fail "
            f"under at least one companion mutant.\n\n")
    if unc:
        f.write("## Not failed by any companion mutant\n\n" +
                "".join(f"- [{s}] {n}\n" for s, n in unc) + "\n")
    f.write("## Renamed, assertion unchanged\n\n" +
            "".join(f"- [{s}] {n} (was: {RENAMED[n]})\n" for s, n in renamed) + "\n")
    f.write("## New checks\n\n")
    for s, n, by in rows:
        f.write(f"- [{s}] {n} <- {'; '.join(by) if by else 'NONE'}\n")
print(len(rows), "new;", len(unc), "uncovered")
for s, n in unc:
    print("UNCOVERED", s, n)

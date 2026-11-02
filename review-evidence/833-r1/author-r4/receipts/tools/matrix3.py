#!/usr/bin/env python3
"""Re-run both round 2 mutation tables at one head, one owner control per run.

usage: matrix3.py CLEAN_CLONE WORK RECEIPTS JOBS MAKE_MUTANTS MUTATE_R3
Mutants: every entry of R763-2's make_mutants.py (applied by that script), every
suite entry with edits of the R764 driver's MUT table (R764-2's mutate_r2.py plus
round 3's M16, applied here), and A726c-resume-collected-shell (the round 3 fix
alone reverted), and A726c-rearm-without-sigcont (that revert with the resume's
SIGCONT dropped). Each (mutant, control) runs in its own user+PID namespace
through run_control3.py, with a 150 s bound. Writes <mutant>/<control>.log and
.rc, and matrix.json; prints one JSON row per run.
"""
import concurrent.futures, json, shutil, subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
clone, work, out, jobs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4])
make_mutants, mutate_r3 = Path(sys.argv[5]), Path(sys.argv[6])
CONTROLS = ["owner_report", "owner_reparented", "owner_late_exit", "owner_stall",
            "owner_shell_window", "owner_survivor", "owner_vanishing", "owner_late_cancel"]
FILES = ("owned_process.py", "test_suite_cancellation.py", "process_test_support.py")
OWN = {"A726c-resume-collected-shell": [("resumed is None and root_pid in owned and not (live - {root_pid}):",
                                         "resumed is None and not (live - {root_pid}):")],
       # Probe: the same revert with the resume's SIGCONT dropped, so only the re-armed window remains.
       "A726c-rearm-without-sigcont": [("resumed is None and root_pid in owned and not (live - {root_pid}):",
                                        "resumed is None and not (live - {root_pid}):"),
                                       ("self._signal(self.root_fd, signal.SIGCONT)\n", "pass\n")],
       # R763-3's two new mutants (its mutants.py), added in round 4.
       "R763-3-shell-killed-when-resumed": [("(resumed is None or clock < kill_all):", "resumed is None:")],
       "R763-3-new-fix-census-not-owned": [("resumed is None and root_pid in owned and not (live - {root_pid}):",
                                            "resumed is None and root_pid in census and not (live - {root_pid}):")]}
src = mutate_r3.read_text()
ns = {}
exec(src[src.index("MUT = {"):src.index("\nNS = ")], ns)
R764 = {f"R764-{name}": edits for name, (edits, test, _expect) in ns["MUT"].items() if test == "suite" and edits}
work.mkdir(parents=True, exist_ok=True)
made = work / "r763"
listing = subprocess.run([sys.executable, "-I", "-B", str(make_mutants), str(clone / "scripts"), str(made)],
                         check=True, capture_output=True, text=True).stdout
(out / "make_mutants.out").parent.mkdir(parents=True, exist_ok=True)
(out / "make_mutants.out").write_text(listing)
mutants = {f"R763-{d.name}": d for d in sorted(made.iterdir())}
for name, edits in {**R764, **OWN}.items():
    d = work / name / "scripts"
    d.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        shutil.copyfile(clone / "scripts" / f, d / f)
    text = (d / "owned_process.py").read_text()
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    (d / "owned_process.py").write_text(text)
    mutants[name] = d
NS = ["unshare", "--user", "--map-current-user", "--pid", "--fork", "--kill-child", "--mount-proc"]


def one(job):
    mutant, control = job
    (out / mutant).mkdir(parents=True, exist_ok=True)
    log = out / mutant / f"{control}.log"
    began = time.monotonic()
    with log.open("w") as stream:
        rc = subprocess.run(["timeout", "-k", "5", "150", *NS, sys.executable, "-I", "-B", str(HERE / "run_control3.py"),
                             str(mutants[mutant]), control], stdout=stream, stderr=subprocess.STDOUT,
                            stdin=subprocess.DEVNULL, env={"PATH": "/usr/bin:/bin", "TMPDIR": str(work / "tmp")}).returncode
    (out / mutant / f"{control}.rc").write_text(f"{rc}\n")
    lines = [l for l in log.read_text(errors="replace").splitlines() if l.strip()]
    return dict(mutant=mutant, control=control, rc=rc, seconds=round(time.monotonic() - began, 1),
                last=(lines[-1] if lines else "")[:400])


(work / "tmp").mkdir(exist_ok=True)
rows = []
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    for row in pool.map(one, [(m, c) for m in mutants for c in CONTROLS]):
        rows.append(row)
        print(json.dumps(row), flush=True)
(out / "matrix.json").write_text(json.dumps(rows, indent=1) + "\n")

"""Feasibility of pinning the two round 8 reviewer survivors in owner_stated_seconds, on copies only.

Usage: python3 -I r8_feasibility.py <clone> <scratch-dir>
Copies <clone>/scripts three times under <scratch-dir>: the head product, and each r8 mutant applied to it.
In each copy it appends two listings to owner_stated_seconds, then runs probe_all_listings.py on the copy
(every listing checked) and prints which listings are red. Nothing in <clone> is touched.
"""
import shutil
import subprocess
import sys
from pathlib import Path

clone, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
EDITS = {
    "none": [],
    "r8-resume-beside-new-live": [("and root_pid in owned and not (live - {root_pid}):",
                                   "and root_pid in owned and not ({p for p in live if (p, owned[p][1])"
                                   " in initial} - {root_pid}):")],
    "r8-sigterm-trap-command-after-late-grace-resume": [
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial and not (resumed is not None and resumed >= 1.5):\n"
         "                        continue\n                elif")],
}
ANCHOR = "    print(\"owner-stated-seconds: \""
ADDED = '''        # Reviewer feasibility 1: a live descendant new since the first census keeps the shell stopped.
        names[os.getppid()] = "trap cleanup"
        kept("a new live descendant beside a stopped shell",
             lambda clock: {shell: (owner_pid, "2"), **({child: (shell, "4")} if clock == 0 else {}),
                            **({os.getppid(): (shell, "8")} if 0 < clock < 3 else {})},
             [(0, "SIGTERM", "child"), (2, "SIGKILL", "trap cleanup"), (3, "SIGCONT", "shell"),
              (13, "SIGKILL", "shell"), (23, "SIGKILL", "shell"), (23, "verdict")], shell)
        # Reviewer feasibility 2: a trap command listed in the last pass inside grace gets no SIGTERM.
        kept("a last in-grace resume with its command listed in grace", resumed_at(2 - TICK), window(2 - TICK), shell)
'''
for name, edits in EDITS.items():
    root = scratch / f"feas-{name}"
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(clone / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    product = root / "scripts/owned_process.py"
    text = product.read_text()
    for old, new in edits:
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    product.write_text(text)
    test = root / "scripts/test_suite_cancellation.py"
    text = test.read_text()
    assert text.count(ANCHOR) == 1
    test.write_text(text.replace(ANCHOR, ADDED + ANCHOR))
    out = subprocess.run([sys.executable, "-I", "-B", str(here / "probe_all_listings.py"), str(root)],
                         cwd=scratch, capture_output=True, text=True, timeout=300)
    lines = [line for line in out.stdout.splitlines() if line.startswith(("RED", "listings"))]
    print(f"=== {name} rc {out.returncode}")
    print("\n".join(lines) or out.stdout[-2000:] + out.stderr[-2000:])

#!/usr/bin/env python3
"""probe_omission_mutants.py LEG_DIR OBJ_TWIN_DIR WORK_DIR: the leave-all-omission plant against the two grade
mutants R799-1's probe_mrp_mutants.py found surviving every earlier plant (txla-qa-bracketed, txla-aa-sends-nothing,
the same edits). For the head and each mutant, the leg's Python is copied to WORK_DIR/<name>, the edit applied (it
must match once), and the new plant is judged as make twin-plants judges it: its --self control against the
unplanted split capture and its control between the placements. The head must refuse it in both; a mutant is
CAUGHT when either control escapes."""
import shutil, subprocess, sys
from pathlib import Path
LEG, OBJ, WORK = (Path(a).resolve() for a in sys.argv[1:4])
MUTANTS = {"head": None,
           "txla-qa-bracketed": ('TXLA = (_row("[s] s  sN sN sJ sJ', 'TXLA = (_row("[s] s  sN sN sJ [sJ]'),
           "txla-aa-sends-nothing": ('TXLA = (_row("[s] s  sN sN sJ sJ', 'TXLA = (_row("[s] s  sN sN [s] sJ')}
env = {"PYTHONPATH": str(LEG.parents[2] / "sw/firmware/ctrl/test"), "PATH": "/usr/bin:/bin"}
f, s, base, planted = (str(OBJ / n) for n in ("fabric.json", "split.json", "report.json", "split-leave-all-omission.json"))
bad = 0
for name, edit in MUTANTS.items():
    tree = WORK / name
    shutil.rmtree(tree, ignore_errors=True)
    tree.mkdir(parents=True)
    for py in LEG.glob("*.py"):
        shutil.copy(py, tree / py.name)
    if edit:
        text = (tree / "twin_mrp.py").read_text()
        assert text.count(edit[0]) == 1, name
        (tree / "twin_mrp.py").write_text(text.replace(*edit))
    run = lambda *a: subprocess.run([sys.executable, "-B", "twin_compare.py", *a], cwd=tree, env=env,
                                    capture_output=True, text=True)
    own = run(s, planted, "--plant", "leave-all-omission", "--self")
    between = run(f, planted, "--plant", "leave-all-omission", "--baseline", base)
    verdicts = [own.stdout.strip().splitlines()[-1], between.stdout.strip().splitlines()[-1]]
    escaped = own.returncode != 0 or between.returncode != 0
    state = ("ok" if not escaped else "HEAD ESCAPES") if edit is None else ("CAUGHT" if escaped else "SURVIVED")
    bad += (edit is None) == escaped
    print(f"{name}: {state}\n  self: {verdicts[0]}\n  between: {verdicts[1]}")
print("PASS" if bad == 0 else "FAIL")
sys.exit(1 if bad else 0)

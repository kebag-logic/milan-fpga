#!/usr/bin/env python3
"""probe_grade_mutants.py LEG_DIR OBJ_TWIN_DIR FW_TEST_DIR WORK_DIR

Each mutant edits one line of the leg's grade code (twin_mrp.py) where it reads, or judges, an attribute that a
LeaveAll frame leaves out. For the head and each mutant, the leg's Python is copied to WORK_DIR/<name>, the edit is
applied (it must match exactly once), the unplanted comparison is run (make twin's verdict, and the plants'
baseline is regenerated as make twin-plants does), and then all twenty plants are judged as make twin-plants judges
them, from the head's planted captures in OBJ_TWIN_DIR: the --self control and the control between the placements.
A plant CATCHES a mutant when either control exits non-zero. The head must refuse every plant and have rc 0."""
import shutil
import subprocess
import sys
from pathlib import Path

LEG, OBJ, FWT, WORK = (Path(a).resolve() for a in sys.argv[1:5])
SPLIT_PLANTS = ("byte-flip srp-plus-k missing-notification uncovered-field vanished-owed command-byte "
                "command-sequence response-sequence table-10-3 received-join leave-all-declaration "
                "leave-all-omission mvrp-join-in mvrp-received-join").split()
FABRIC_PLANTS = ("vanished-mvrp-leave-all vanished-available-index vanished-domain-new domain-trace-moved "
                 "vanished-vid2-join-in vid2-registrar-in").split()
MUTANTS = {
    "head": None,
    # the Table 10-3 txLA! cells of the two states the Domain is in at the planted LeaveAll
    "txla-qa-bracketed": ('TXLA = (_row("[s] s  sN sN sJ sJ ', 'TXLA = (_row("[s] s  sN sN sJ [sJ] '),
    "txla-aa-sends-nothing": ('TXLA = (_row("[s] s  sN sN sJ sJ ', 'TXLA = (_row("[s] s  sN sN [s] sJ '),
    # every txLA! cell optional
    "txla-every-cell-optional": ('if actions[applicant].startswith("[") else [(sent, moved)]',
                                 'if leave_all or actions[applicant].startswith("[") else [(sent, moved)]'),
    # an attribute a LeaveAll frame leaves out is not read at all
    "omitted-attribute-unread": ("            if types:\n                timeline.append((ms, 1, Seen(ms, mine[0] if mine else None, True)))",
                                 "            if types and mine:\n                timeline.append((ms, 1, Seen(ms, mine[0] if mine else None, True)))"),
    # an attribute a LeaveAll frame leaves out is read as a tx! that sent nothing
    "omitted-read-as-tx": ("Seen(ms, mine[0] if mine else None, True)", "Seen(ms, mine[0] if mine else None, bool(mine))"),
    # 'nothing' accepted from every configuration
    "nothing-always-allowed": ("opportunity(seen.leave_all, c, part) if sent == seen.sent}",
                               "opportunity(seen.leave_all, c, part) if sent == seen.sent or seen.sent is None}"),
}
env = {"PYTHONPATH": str(FWT), "PATH": "/usr/bin:/bin"}
fab, spl = str(OBJ / "fabric.json"), str(OBJ / "split.json")
bad = 0
for name, edit in MUTANTS.items():
    tree = WORK / name
    shutil.rmtree(tree, ignore_errors=True)
    tree.mkdir(parents=True)
    for py in LEG.glob("*.py"):
        shutil.copy(py, tree / py.name)
    if edit:
        text = (tree / "twin_mrp.py").read_text()
        assert text.count(edit[0]) == 1, (name, text.count(edit[0]))
        (tree / "twin_mrp.py").write_text(text.replace(*edit))

    def run(*a):
        return subprocess.run([sys.executable, "-B", "twin_compare.py", *a], cwd=tree, env=env,
                              capture_output=True, text=True)
    base = str(tree / "report.json")
    twin = run(fab, spl, "--report", str(tree / "twin-report.json"))
    last = (twin.stdout.strip().splitlines() or [""])[-1]
    run(fab, spl, "--report", base, "--report-only")
    caught = []
    for p in SPLIT_PLANTS + FABRIC_PLANTS:
        if p in SPLIT_PLANTS:
            planted = str(OBJ / f"split-{p}.json")
            own = run(spl, planted, "--plant", p, "--self")
            between = run(fab, planted, "--plant", p, "--baseline", base)
        else:
            planted = str(OBJ / f"fabric-{p}.json")
            own = run(fab, planted, "--plant", p, "--self")
            between = run(planted, spl, "--plant", p, "--baseline", base)
        if own.returncode or between.returncode:
            caught.append(f"{p}(self rc {own.returncode}, between rc {between.returncode})")
    if edit is None:
        ok = twin.returncode == 0 and not caught
        print(f"head: twin rc {twin.returncode} [{last[:90]}]; plants escaping: {caught or 'none'}; "
              f"{'ok' if ok else 'BAD'}")
        bad += not ok
    else:
        earlier = [c for c in caught if not c.startswith("leave-all-omission(")]
        new = [c for c in caught if c.startswith("leave-all-omission(")]
        print(f"{name}: twin rc {twin.returncode}; caught by earlier plants: {earlier or 'none'}; "
              f"by leave-all-omission: {'yes ' + new[0] if new else 'NO'}")
        bad += not (new or twin.returncode or earlier)
print("PASS" if bad == 0 else "FAIL")
sys.exit(1 if bad else 0)

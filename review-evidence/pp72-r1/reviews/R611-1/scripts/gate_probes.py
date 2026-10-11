#!/usr/bin/env python3
"""Disposable fault probes of scripts/check-req-tags.py in a scratch clone.

Usage: gate_probes.py TREE [SUITES EVIDENCE]

Each probe plants text edits in TREE, runs the gate (static half; with SUITES and
EVIDENCE also the executed half, the evidence file edited per probe), prints rc
and the REQ TAG FAIL lines, then restores TREE with `git checkout -- .` and
`git clean -fdq tb docs`. TREE must be a disposable clone at the exact head.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
suites = Path(sys.argv[2]).resolve() if len(sys.argv) > 3 else None
evidence = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
REVIEW = "docs/00_MILAN_COMPLIANCE_REVIEW.md"
VERIFY = "docs/architecture/09_verification.md"
ORIG = "tb/originator/sim_main.cpp"
ADP = "tb/adp_engine/sim_main.cpp"
NOTIFY = "tb/pp_top/notify_phases.hpp"
PY = "tb/desc_store/test_gen_desc_image.py"
ROW_ADP002 = None  # filled from the tree


def line_of(path: str, prefix: str) -> str:
    for line in (tree / path).read_text(encoding="utf-8").splitlines(keepends=True):
        if line.startswith(prefix):
            return line
    raise SystemExit(f"probe target missing: {prefix} in {path}")


row_adp002 = line_of(REVIEW, "| REQ-ADP-002 |")
row_adp001 = line_of(REVIEW, "| REQ-ADP-001 |")
waiver_025 = line_of(VERIFY, "| REQ-AEM-025 |")
cells = row_adp002.rstrip("\n").split("|")
short_adp002 = "|".join(cells[:-2]) + "|\n"          # the Ver cell dropped
dup_adp001 = row_adp001.replace("| TIM |", "| lint |")
new_row = ("| REQ-AEM-027 | Milan §0 | a planted row | shall | A | [GAP-01](#gap-01) | x | "
           "06 §6 | DIR |\n")

# name, [(file, old, new)], evidence edit (old, new) or None, expected token(s)
PROBES = [
    ("S1 tag removed (assignment 1)",
     [(ORIG, '  REQ_TAG("REQ-AEM-005", "RND", "R: a seeded session of 16 owners\' overlapping exchanges");\n', "")],
     None, ["UNCOVERED REQ-AEM-005 (RND)"]),
    ("S2 unknown REQ (assignment 2)",
     [(ADP, 'REQ_TAG("REQ-ADP-008", "TIM", "P8 every kind-1 draw <= 2000");',
       'REQ_TAG("REQ-ADP-099", "TIM", "P8 every kind-1 draw <= 2000");')],
     None, ["UNKNOWN REQ REQ-ADP-099"]),
    ("S3 waiver without GAP (assignment 4)",
     [(VERIFY, waiver_025, waiver_025.replace("| GAP-06 |", "| |"))],
     None, ["WAIVER WITHOUT GAP REQ-AEM-025"]),
    ("S4 row added with no tag (assignment 5)",
     [(REVIEW, row_adp001, row_adp001 + new_row)],
     None, ["UNCOVERED REQ-AEM-027 (DIR)"]),
    ("S5 RND tag relabelled DIR on RN",
     [(NOTIFY, 'REQ_TAG("REQ-AEM-016", "RND", "RN");', 'REQ_TAG("REQ-AEM-016", "DIR", "RN");')],
     None, ["UNCOVERED REQ-AEM-016 (RND)"]),
    ("S6 tag name cut to a bare substring (ST1b -> 'ST1')",
     [(NOTIFY, '"ST1b: one change from row 15 reaches the other fifteen");', '"ST1");')],
     None, []),
    ("S6b tag name one character ('1') on ST1b",
     [(NOTIFY, '"ST1b: one change from row 15 reaches the other fifteen");', '"1");')],
     None, []),
    ("S7 matrix row with its Ver cell dropped",
     [(REVIEW, row_adp002, short_adp002)],
     None, ["?"]),
    ("S8 second REQ-ADP-001 row (Ver lint) appended at the end of 00",
     [(REVIEW, None, "\n| REQ | a | b | c | d | e | f | g | h |\n|---|---|---|---|---|---|---|---|---|\n" + dup_adp001)],
     None, ["?"]),
    ("S9 tag line commented out",
     [(ADP, '  REQ_TAG("REQ-ADP-008", "TIM", "P8 every kind-1 draw <= 2000");',
       '  // REQ_TAG("REQ-ADP-008", "TIM", "P8 every kind-1 draw <= 2000");')],
     None, ["MALFORMED TAG"]),
    ("S10 waiver naming another row's GAP",
     [(VERIFY, waiver_025, waiver_025.replace("| GAP-06 |", "| GAP-04 |")),
      (REVIEW, "A; waived GAP-06", "A; waived GAP-04")],
     None, ["WAIVER NAMES ANOTHER ROW'S GAP REQ-AEM-025"]),
    ("S11 Cov cell state edited",
     [(REVIEW, row_adp002, row_adp002.replace("| A; traced |", "| A; waived GAP-16 |"))],
     None, ["COV RECORD REQ-ADP-002"]),
    ("S12 Python tag moved to another method",
     [(PY, '        REQ_TAG("REQ-ADP-003", "DIR", "IdentityTest.test_driven_values_agree")\n', ""),
      (PY, '    def test_boundaries_pack(self) -> None:\n',
       '    def test_boundaries_pack(self) -> None:\n'
       '        REQ_TAG("REQ-ADP-003", "DIR", "IdentityTest.test_driven_values_agree")\n')],
     None, ["NAME NOT AT CHECK"]),
]
if evidence is not None:
    ev = evidence.read_text(encoding="utf-8")
    line_005 = next(l for l in ev.splitlines(keepends=True) if " REQ-AEM-005 RND" in l)
    PROBES += [
        ("E1 evidence line of the AEM-005 tag missing (executed)", [], (line_005, ""),
         ["DEAD TAG REQ-AEM-005"]),
        ("E2 stray evidence line (executed)", [], (line_005, line_005 + "originator sim_main.cpp:1 REQ-AEM-005 RND\n"),
         ["STRAY EVIDENCE"]),
        ("E3 tag moved two lines down onto the next check, stale evidence kept (executed)",
         [(ORIG, '  REQ_TAG("REQ-AEM-005", "RND", "R: a seeded session of 16 owners\' overlapping exchanges");\n'
                 '  CHECK(r_divergences == 0,',
           '  CHECK(r_divergences == 0,'),
          (ORIG, '  CHECK(r_peak >= 6 &&',
           '  REQ_TAG("REQ-AEM-005", "RND", "R b: every arm");\n  CHECK(r_peak >= 6 &&')],
         None, ["DEAD TAG REQ-AEM-005", "STRAY EVIDENCE"]),
    ]


def restore() -> None:
    subprocess.run(["git", "-C", str(tree), "checkout", "--", "."], check=True)
    subprocess.run(["git", "-C", str(tree), "clean", "-fdq", "tb", "docs"], check=True)


def run_gate(ev_text: str | None) -> tuple[int, str]:
    cmd = [sys.executable, "scripts/check-req-tags.py"]
    with tempfile.TemporaryDirectory() as tmp:
        if ev_text is not None:
            ef = Path(tmp) / "evidence"
            ef.write_text(ev_text, encoding="utf-8")
            cmd += ["--suites", str(suites), "--evidence", str(ef)]
        p = subprocess.run(cmd, cwd=tree, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def matrix() -> tuple[int, str]:
    p = subprocess.run([sys.executable, "scripts/check-matrix.py"], cwd=tree,
                       capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


restore()
rc, out = run_gate(None)
print(f"== baseline static: rc {rc}\n{out}")
if evidence is not None:
    rc, out = run_gate(evidence.read_text(encoding="utf-8"))
    print(f"== baseline executed: rc {rc}\n{out}")
for name, edits, ev_edit, expect in PROBES:
    for f, old, new in edits:
        p = tree / f
        body = p.read_text(encoding="utf-8")
        if old is None:
            body += new
        else:
            assert old in body, (name, old)
            body = body.replace(old, new, 1)
        p.write_text(body, encoding="utf-8")
    ev_text = None
    if evidence is not None:
        ev_text = evidence.read_text(encoding="utf-8")
        if ev_edit is not None:
            assert ev_edit[0] in ev_text
            ev_text = ev_text.replace(ev_edit[0], ev_edit[1], 1)
    rc, out = run_gate(ev_text)
    mrc, mout = matrix()
    fails = [l for l in out.splitlines() if l.startswith("REQ TAG FAIL")]
    summary = [l for l in out.splitlines() if l.startswith("req-tags")]
    hit = all(any(t in l for l in fails) for t in expect if t != "?")
    print(f"== {name}\n   gate rc {rc}; expected {expect}; named {'yes' if hit else 'NO'}")
    for l in fails + summary:
        print(f"   {l}")
    print(f"   check-matrix rc {mrc}: {mout.splitlines()[-1] if mout else ''}")
    restore()
st = subprocess.run(["git", "-C", str(tree), "status", "--porcelain"], capture_output=True, text=True)
print(f"== restored: status '{st.stdout.strip()}'")

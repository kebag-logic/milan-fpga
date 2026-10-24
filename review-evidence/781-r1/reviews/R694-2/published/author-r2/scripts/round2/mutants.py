"""Round 2 (#781): plant each defect the head 41f4a53c could carry in a scratch clone at that head, run
the check that must refuse it, and record rc and the refusing words. The clone is reset between mutants.
X1 is an expected escape, recorded as evidence that no check ties a measured figure to the budget.
usage: python3 -I mutants.py <clone> <out.txt>"""
import pathlib, subprocess, sys

clone, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
S, D, W = "scripts/suite_shards.py", "scripts/run_all_suites.sh", ".github/workflows/rtl.yml"
SELF = ["python3", S, "--selftest"]
GEN = ["python3", "scripts/ci_gate_workflows.py", "--check"]
REGEN = ["python3", "scripts/ci_gate_workflows.py"]
CONTRACT = ["python3", "-c", "import sys; sys.path.insert(0, 'scripts'); import measure_test_evidence as m; "
            "p = m.runner_contract(open('scripts/run_all_suites.sh').read()); print(p); sys.exit(1 if p else 0)"]
EMPTY = "PROVISIONAL_SUITES: frozenset[str] = frozenset()"

def edit(path, old, new):
    p = clone / path; t = p.read_text(); assert t.count(old) == 1, (path, old); p.write_text(t.replace(old, new))

# (name, edits, prep, checks, words, expect_caught)
MUTANTS = [
    ("R1 provisional comparison disabled while nothing is pending (the planted arm must still refuse it)",
     [(S, "        elif seconds[suite] != expected:", "        elif False:")], [], [SELF],
     ["ESCAPED a provisional suite at 1800 s, suite_timeout's figure for it, passes, and at 1801 s is refused"], True),
    ("R2 the hosted 582 s recorded as the figure while media_phase stays provisional",
     [(S, EMPTY, 'PROVISIONAL_SUITES: frozenset[str] = frozenset({"media_phase"})'),
      (S, '"media_phase": 1400,', '"media_phase": 582,')], [], [SELF],
     ["provisional figure 582 s is not the 1400 s"], True),
    ("R3 PROVISIONAL_SUITES names a suite with no figure (misspelt media_phase)",
     [(S, EMPTY, 'PROVISIONAL_SUITES: frozenset[str] = frozenset({"media_phse"})')], [], [SELF],
     ["media_phse: PROVISIONAL_SUITES names a suite with no figure in SUITE_SECONDS"], True),
    ("R4 driver suite_timeout media_phase back at 900 s",
     [(D, '"${SUITE_TIMEOUT:-1400}"', '"${SUITE_TIMEOUT:-900}"')], [], [CONTRACT],
     ["suite budgets changed"], True),
    ("R5 (round 1b M1) overhead table back at 16 workers, workflow not regenerated",
     [(S, "WORKER_OVERHEAD_SECONDS = (122,) * 17", "WORKER_OVERHEAD_SECONDS = (122,) * 16")], [], [SELF, GEN],
     ["WORKER_OVERHEAD_SECONDS describes 16 workers; rtl.yml runs 17", "regenerate the gate jobs"], True),
    ("R6 (round 1b M2) 16 workers regenerated through the generator, media_phase still 1400 s",
     [(S, "WORKER_OVERHEAD_SECONDS = (122,) * 17", "WORKER_OVERHEAD_SECONDS = (122,) * 16")], [REGEN], [SELF],
     ["FAIL head worker 0/16 predicted 1640 s (27.3 min), bound 1620 s"], True),
    ("R7 (round 1b M5) rtl.yml hand-edited: 60-minute index left at 15 with 17 workers",
     [(W, "${{ matrix.shard == 16 && 60 || 45 }}", "${{ matrix.shard == 15 && 60 || 45 }}")], [], [SELF, GEN],
     ["FAIL head worker 16/17 predicted 2032 s (33.9 min), bound 1620 s", "regenerate the gate jobs"], True),
    ("R8 (round 1b M8) media_phase grown to 1499 s, the first figure no regular worker accepts",
     [(S, '"media_phase": 1400,', '"media_phase": 1499,'), (D, '"${SUITE_TIMEOUT:-1400}"', '"${SUITE_TIMEOUT:-1499}"')],
     [], [SELF], ["FAIL head worker 0/17 predicted 1621 s (27.0 min), bound 1620 s"], True),
    ("X1 expected escape: SUITE_SECONDS media_phase lowered to the hosted 582 s, not provisional, driver kept 1400 s",
     [(S, '"media_phase": 1400,', '"media_phase": 582,')], [], [SELF], ["selftest: PASS"], False),
]

lines = []
bad = 0
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=clone, capture_output=True, text=True, check=True).stdout.strip()
lines.append(f"clone head {head}")
def reset():
    subprocess.run(["git", "checkout", "-q", "--", "."], cwd=clone, check=True)
    assert subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=clone,
                          capture_output=True, text=True, check=True).stdout == ""
reset()
for cmd in (SELF, GEN, CONTRACT):
    r = subprocess.run(cmd, cwd=clone, capture_output=True, text=True)
    lines.append(f"clean control: {' '.join(cmd[:3])} rc={r.returncode}")
    bad += r.returncode != 0
for name, edits, prep, checks, words, expect in MUTANTS:
    reset()
    for e in edits:
        edit(*e)
    for cmd in prep:
        subprocess.run(cmd, cwd=clone, check=True)
    text, rcs = "", []
    for cmd in checks:
        r = subprocess.run(cmd, cwd=clone, capture_output=True, text=True)
        rcs.append(r.returncode); text += r.stdout + r.stderr
    found = {w: (w in text) for w in words}
    if expect:
        ok = all(rc != 0 for rc in rcs) and all(found.values())
        verdict = "CAUGHT " if ok else "ESCAPED"
    else:
        ok = all(rc == 0 for rc in rcs) and all(found.values())
        verdict = "PASSES (expected)" if ok else "UNEXPECTED"
    bad += not ok
    hits = [l.strip() for l in text.splitlines() if any(w in l for w in words)][:4]
    lines.append(f"{verdict} {name}: rcs={rcs} words={found}")
    lines += [f"    | {h}" for h in hits]
reset()
lines.append(f"mutants: {sum(m[5] for m in MUTANTS)} expected caught, {sum(not m[5] for m in MUTANTS)} expected escape; "
             f"departures from expectation: {bad}")
out.write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if bad else 0)

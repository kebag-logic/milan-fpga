"""Plant each defect this change could carry in a scratch clone at the head, run the check that
must refuse it, and record rc and the refusing words. The clone is reset between mutants.
usage: python3 -I mutants.py <clone> <out.txt>"""
import pathlib, subprocess, sys

clone, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
S, D, W, M = "scripts/suite_shards.py", "scripts/run_all_suites.sh", ".github/workflows/rtl.yml", "scripts/measure_test_evidence.py"
SELF = ["python3", S, "--selftest"]
GEN = ["python3", "scripts/ci_gate_workflows.py", "--check"]
REGEN = ["python3", "scripts/ci_gate_workflows.py"]
CONTRACT = ["python3", "-c", "import sys; sys.path.insert(0, 'scripts'); import measure_test_evidence as m; "
            "p = m.runner_contract(open('scripts/run_all_suites.sh').read()); print(p); sys.exit(1 if p else 0)"]

def edit(path, old, new):
    p = clone / path; t = p.read_text(); assert t.count(old) == 1, (path, old); p.write_text(t.replace(old, new))

MUTANTS = [
    ("M1 overhead table back at 16 workers, workflow not regenerated",
     [(S, "WORKER_OVERHEAD_SECONDS = (122,) * 17", "WORKER_OVERHEAD_SECONDS = (122,) * 16")], [], [SELF, GEN],
     ["WORKER_OVERHEAD_SECONDS describes 16 workers; rtl.yml runs 17", "regenerate the gate jobs"]),
    ("M2 16 workers regenerated through the generator, media_phase still 1400 s",
     [(S, "WORKER_OVERHEAD_SECONDS = (122,) * 17", "WORKER_OVERHEAD_SECONDS = (122,) * 16")], [REGEN], [SELF],
     ["FAIL head worker 0/16 predicted 1640 s (27.3 min), bound 1620 s", "selftest: 30 FAILURE(S)"]),
    ("M3 SUITE_SECONDS media_phase 900 s against the driver's 1400 s",
     [(S, '"media_phase": 1400,', '"media_phase": 900,')], [], [SELF],
     ["provisional figure 900 s is not the 1400 s"]),
    ("M4 driver suite_timeout media_phase 900 s against SUITE_SECONDS 1400 s",
     [(D, '"${SUITE_TIMEOUT:-1400}"', '"${SUITE_TIMEOUT:-900}"')], [], [SELF, CONTRACT],
     ["provisional figure 1400 s is not the 900 s", "suite budgets changed"]),
    ("M5 rtl.yml hand-edited: 60-minute index left at 15 with 17 workers",
     [(W, "${{ matrix.shard == 16 && 60 || 45 }}", "${{ matrix.shard == 15 && 60 || 45 }}")], [], [SELF, GEN],
     ["FAIL head worker 16/17 predicted 2032 s (33.9 min), bound 1620 s", "regenerate the gate jobs"]),
    ("M6 rtl.yml hand-edited: aggregate still expects 16 workers",
     [(W, "--require-target-sha --expect 17 ", "--require-target-sha --expect 16 ")], [], [GEN],
     ["regenerate the gate jobs"]),
    ("M7 rtl.yml hand-edited: matrix total back at 16 (shard list 0..16 kept)",
     [(W, "        total:\n          - 17\n", "        total:\n          - 16\n")], [], [GEN],
     ["regenerate the gate jobs"]),
    ("M8 media_phase grown to 1499 s, the first figure no regular worker accepts",
     [(S, '"media_phase": 1400,', '"media_phase": 1499,'), (D, '"${SUITE_TIMEOUT:-1400}"', '"${SUITE_TIMEOUT:-1499}"')],
     [], [SELF], ["FAIL head worker 0/17 predicted 1621 s (27.0 min), bound 1620 s"]),
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
for name, edits, prep, checks, words in MUTANTS:
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
    caught = all(rc != 0 for rc in rcs) and all(found.values())
    bad += not caught
    hits = [l.strip() for l in text.splitlines() if any(w in l for w in words)][:4]
    lines.append(f"{'CAUGHT ' if caught else 'ESCAPED'} {name}: rcs={rcs} words={found}")
    lines += [f"    | {h}" for h in hits]
reset()
lines.append(f"mutants: {len(MUTANTS)}, escaped: {bad}")
out.write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if bad else 0)

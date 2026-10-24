"""Plant disposable defects in git-archive copies of a head and run the existing checks.
usage: python3 -I mutants.py <repo> <scratch-dir> <out-file> [--jobs N]
Each mutant must turn at least one named check nonzero; each control must leave all at rc 0."""
import concurrent.futures as cf, pathlib, re, shutil, subprocess, sys
repo, scratch, out = map(pathlib.Path, sys.argv[1:4])
jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
SEL = ["python3", "scripts/suite_shards.py", "--selftest"]
GEN = ["python3", "scripts/ci_gate_workflows.py", "--check"]
EVT = ["python3", "scripts/ci_events.py", "--check"]
TEV = ["python3", "scripts/measure_test_evidence.py", "--check"]
ALL = [SEL, GEN, EVT, TEV]
def sub(path, old, new, count=1):
    def f(root):
        p = root / path; t = p.read_text()
        assert t.count(old) >= count, (path, old, t.count(old))
        p.write_text(t.replace(old, new) if count == 0 else t.replace(old, new, count))
    return f
def regen(root):
    subprocess.run(["python3", "scripts/ci_gate_workflows.py"], cwd=root, check=True, capture_output=True)
def chain(*fs):
    def f(root):
        for g in fs: g(root)
    return f
SS, RA, YML, TE, CW = "scripts/suite_shards.py", "scripts/run_all_suites.sh", ".github/workflows/rtl.yml", "scripts/measure_test_evidence.py", "docs/testing/CI_WORKFLOWS.md"
MP_SS = '"media_phase": 1400,'
MP_RA = 'media_phase)       printf \'%s\\n\' "${SUITE_TIMEOUT:-1400}" ;;'
MP_TE = 'media_phase)       printf \'%s\\\\n\' "${SUITE_TIMEOUT:-1400}" ;;'
def both(v): return chain(sub(SS, MP_SS, f'"media_phase": {v},'), sub(RA, MP_RA, MP_RA.replace("1400", str(v))), sub(TE, MP_TE, MP_TE.replace("1400", str(v))))
SUBMODULES = [l.split()[1] for l in subprocess.run(["git", "-C", str(repo), "submodule", "status"], capture_output=True, text=True).stdout.splitlines() if not l.startswith("-")]
CASES = [
 # name, kind, mutation, checks
 ("C0-unmutated", "control", lambda r: None, ALL),
 ("C1-media_phase-1498-both-sides", "control", both(1498), [SEL, TEV]),
 ("M1-overhead-table-left-at-16", "mutant", sub(SS, "(122,) * 17", "(122,) * 16"), ALL),
 ("M2-overhead-16-and-rtl.yml-regenerated", "mutant", chain(sub(SS, "(122,) * 17", "(122,) * 16"), regen), ALL),
 ("M3-SUITE_SECONDS-left-at-900", "mutant", sub(SS, MP_SS, '"media_phase": 900,'), ALL),
 ("M4-suite_timeout-left-at-900", "mutant", sub(RA, MP_RA, MP_RA.replace("1400", "900")), ALL),
 ("M5-contract-copy-left-at-900", "mutant", sub(TE, MP_TE, MP_TE.replace("1400", "900")), ALL),
 ("M6-media_phase-1499-both-sides", "mutant", both(1499), [SEL, TEV]),
 ("M7-media_phase-dropped-from-PROVISIONAL", "mutant", sub(SS, 'frozenset({"media_phase"})', 'frozenset()'), ALL),
 ("M8-rtl.yml-60min-arm-at-15", "mutant", sub(YML, "matrix.shard == 16 && 60", "matrix.shard == 15 && 60"), ALL),
 ("M9-rtl.yml-expect-16", "mutant", sub(YML, "--expect 17 \\", "--expect 16 \\"), ALL),
 ("M10-rtl.yml-total-16", "mutant", sub(YML, "        total:\n          - 17\n", "        total:\n          - 16\n"), ALL),
 ("M11-rtl.yml-shard-16-dropped", "mutant", sub(YML, "          - 16\n        total:", "        total:"), ALL),
 ("M12-rtl.yml-fail-fast-list-missing-16-of-17", "mutant", sub(YML, ',"Verilator shard 16/17"', '', 1), ALL),
 ("M13-docs-target-sha-expect-16", "mutant", sub(CW, "(`--expect 17` for Verilator", "(`--expect 16` for Verilator"), ALL),
 ("M14-overhead-18-and-regenerated", "mutant", chain(sub(SS, "(122,) * 17", "(122,) * 18"), regen), ALL),
 ("M15-docs-worker-table-row4-1540", "mutant", sub(CW, "| `verilator-shards 4/17` | 1539 | 1620 | 81 |", "| `verilator-shards 4/17` | 1540 | 1620 | 80 |"), ALL),
 ("M16-media_phase-1400-only-SUITE_SECONDS-1300", "mutant", sub(SS, MP_SS, '"media_phase": 1300,'), ALL),
]
def run(case):
    name, kind, mut, checks = case
    root = scratch / name
    if root.exists(): shutil.rmtree(root)
    root.mkdir(parents=True)
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    sh = lambda c: subprocess.run(c, shell=True, check=True, capture_output=True)
    sh(f"git clone -q --shared --no-checkout {repo} {root} && git -C {root} checkout -q --detach {head}")
    for sm in SUBMODULES:
        gl = subprocess.run(["git", "-C", str(repo), "rev-parse", f"HEAD:{sm}"], capture_output=True, text=True, check=True).stdout.strip()
        sh(f"git -C {root} submodule init -q -- {sm} && rmdir {root / sm} && git clone -q --shared --no-checkout {repo / sm} {root / sm} && git -C {root / sm} checkout -q --detach {gl}")
    mut(root)
    res = []
    for c in checks:
        p = subprocess.run(c, cwd=root, capture_output=True, text=True, timeout=900)
        txt = (p.stdout + p.stderr).strip().splitlines()
        fails = [l for l in txt if not re.match(r"\s*(\[ok\]|ok)\s", l) and re.search(r"\bFAIL|REFUSED|regenerate|changed|[Ee]rror|problem|mismatch", l)]
        res.append((" ".join(c[1:]), p.returncode, (fails[:2] or txt[-1:])))
    nonzero = any(rc for _, rc, _ in res)
    verdict = ("CAUGHT" if nonzero else "ESCAPED") if kind == "mutant" else ("CLEAN" if not nonzero else "CONTROL-FAILED")
    shutil.rmtree(root)
    return name, kind, verdict, res
with cf.ThreadPoolExecutor(jobs) as ex:
    results = list(ex.map(run, CASES))
lines = []
for name, kind, verdict, res in results:
    lines.append(f"{verdict:15} {name}")
    for c, rc, msg in res: lines.append(f"    rc={rc} {c} :: " + " | ".join(m[:200] for m in msg))
out.write_text("\n".join(lines) + "\n"); print("\n".join(lines))

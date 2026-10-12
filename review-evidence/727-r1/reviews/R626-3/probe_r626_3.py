#!/usr/bin/env python3
"""Reviewer mutation and planting probes for #727 at one head (R626-3).

Usage: probe_r626_3.py CHECKOUT WORKDIR [--jobs N]

Each case builds a disposable tree under WORKDIR/<case>/ holding the selector,
the driver, rtl.yml and one empty Makefile per suite directory of CHECKOUT's
tb/verilator, applies one source mutation or tree planting, and runs
`python3 -I scripts/suite_shards.py --selftest` (plus extra commands for some
cases). A case passes when the exit code matches and, for mutants, the named
arm is reported ESCAPED/FAIL. Nothing in CHECKOUT is written.
"""
import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

SEL = "scripts/suite_shards.py"
YML = ".github/workflows/rtl.yml"
DRV = "scripts/run_all_suites.sh"
VJOB = ("    runs-on: ubuntu-latest\n    timeout-minutes: 120\n    strategy:\n"
        "      fail-fast: false\n      matrix:\n        shard: [0, 1, 2, 3, 4]\n")


def sub(old, new, count=1):
    """A source mutation that must match exactly `count` times."""
    def apply(tree):
        path = tree / SEL
        text = path.read_text()
        found = text.count(old)
        if found != count:
            raise RuntimeError(f"DRIFT: {old!r} found {found} times")
        path.write_text(text.replace(old, new))
    return apply


def edit(rel, old, new):
    def apply(tree):
        path = tree / rel
        text = path.read_text()
        if text.count(old) != 1:
            raise RuntimeError(f"DRIFT: {old!r} in {rel}")
        path.write_text(text.replace(old, new))
    return apply


def plant_suite(name):
    def apply(tree):
        (tree / "tb/verilator" / name).mkdir()
        (tree / "tb/verilator" / name / "Makefile").touch()
    return apply


def remove_suite(name):
    def apply(tree):
        shutil.rmtree(tree / "tb/verilator" / name)
    return apply


def delete(rel):
    def apply(tree):
        p = tree / rel
        shutil.rmtree(p) if p.is_dir() else p.unlink()
    return apply


def chain(*fs):
    def apply(tree):
        for f in fs:
            f(tree)
    return apply


# (name, apply, expected rc, substring that must appear on an ESCAPED/FAIL line or None)
CASES = [
    ("tree-head", None, 0, None),
    # --- the four gate cases of the assignment, each with its control ---
    ("missing-duration-made-free",
     chain(sub("for suite in suites if suite not in seconds]",
               "for suite in suites if False]"),
           sub("            load[fixed[suite]] += seconds[suite]",
               "            load[fixed[suite]] += seconds.get(suite, 0)"),
           sub("key=lambda suite: (-seconds[suite], suite)):",
               "key=lambda suite: (-seconds.get(suite, 0), suite)):"),
           sub("        load[worker] += seconds[suite]",
               "        load[worker] += seconds.get(suite, 0)")),
     1, "no recorded duration is refused"),
    ("stale-check-deleted",
     sub('"inventory" for suite in sorted(set(seconds) - inventory)]',
         '"inventory" for suite in ()]'), 1, "no inventory suite is refused"),
    ("timeout-mirrored-120",
     sub('return found["timeout-minutes"], found["matrix total"]',
         'return 120, found["matrix total"]'), 1, "timeout-minutes 116"),
    ("headroom-75",
     sub("HEADROOM_PERCENT = 60", "HEADROOM_PERCENT = 75"), 1, "36 s a minute"),
    ("headroom-100",
     sub("HEADROOM_PERCENT = 60", "HEADROOM_PERCENT = 100"), 1, "36 s a minute"),
    ("bound-formula-div10",
     sub("timeout_minutes * 60 * HEADROOM_PERCENT // 100",
         "timeout_minutes * 60 * HEADROOM_PERCENT // 10"), 1, "36 s a minute"),
    ("bound-formula-hour",
     sub("timeout_minutes * 60 * HEADROOM_PERCENT // 100",
         "timeout_minutes * 60"), 1, "36 s a minute"),
    ("bound-ge",
     sub("for worker, value in enumerate(load) if value > bound]",
         "for worker, value in enumerate(load) if value >= bound]"), 1,
     "exactly at the bound"),
    ("bound-check-mean-only",
     sub("for worker, value in enumerate(load) if value > bound]",
         "for worker, value in [(0, sum(load) // len(load))] if value > bound]"),
     1, "puts it over"),
    ("overhead-dropped",
     sub("load = list(overhead) if layout else [0] * total",
         "load = [0] * total"), 1, "puts it over"),
    ("worker-count-mirrored-5",
     sub('return found["timeout-minutes"], found["matrix total"]',
         'return found["timeout-minutes"], 5'), 1, "at 6 workers"),
    ("zero-duration-allowed",
     sub("isinstance(seconds[suite], int) and seconds[suite] > 0)",
         "isinstance(seconds[suite], int) and seconds[suite] >= 0)"), 1,
     "duration of 0 s"),
    # --- pins, dedicated, determinism ---
    ("pins-dropped",
     sub("    if layout:\n        fixed.update(PINNED_SUITES)\n", ""), 1,
     "specialized owners"),
    ("pin-moved",
     sub('PINNED_SUITES = {"tsn_fuzz": 1, "chmap_capture": 3}',
         'PINNED_SUITES = {"tsn_fuzz": 1, "chmap_capture": 2}'), 1,
     "specialized owners"),
    ("dedicated-dropped",
     sub("    if balanced != total:\n        fixed.update(",
         "    if False:\n        fixed.update("), 1, "dedicated"),
    ("tie-by-hash",
     sub("key=lambda suite: (-seconds[suite], suite)):",
         "key=lambda suite: (-seconds[suite], hash(suite))):"), 1,
     "hash seeds 1 and 2"),
    ("worker-tie-highest",
     sub("key=lambda worker: (load[worker], worker))",
         "key=lambda worker: (load[worker], -worker))"), 0, None),
    # --- round 3: provisional figures read from the driver ---
    ("provisional-default-mirrored-1800",
     sub("    return dict(arms[:-1]), arms[-1][1]\n",
         "    return dict(arms[:-1]), 1800\n"), 1, "planted at 1860"),
    ("provisional-named-arms-ignored",
     sub("expected = named.get(suite, default)", "expected = default"), 1,
     "own arm planted"),
    ("provisional-never-compared",
     sub("elif seconds[suite] != expected:", "elif False:"), 1, "1801 s is refused"),
    ("provisional-no-figure-let-through",
     sub("        if suite not in seconds:\n            problems.append(",
         "        if suite not in seconds:\n            continue\n            problems.append("),
     1, "no figure in SUITE_SECONDS"),
    ("provisional-head-call-deleted",
     sub("        provisional = provisional_problems(driver)\n",
         "        provisional = []\n"), 0, None),
    # --- copy skip ---
    ("in-checkout-forced-false",
     sub('return HERE.name == "suite_shards.py" and HERE.parent.name == "scripts"',
         "return False"), 1, "would skip its head arms"),
    # --- measure reader ---
    ("measure-from-job-start",
     sub("windows, previous = {}, start", "windows, previous = {}, first"), 1,
     "log windows"),
    ("measure-round-down",
     sub("windows[suite] = -(-(ticks - previous) // TICKS_PER_SECOND)",
         "windows[suite] = (ticks - previous) // TICKS_PER_SECOND"), 1, "log windows"),
    ("measure-accept-timeout",
     sub('if result.group(1) != "PASS":', 'if result.group(1) == "FAIL":'), 1,
     "log windows"),
    # --- tree plantings (no source change) ---
    ("plant-unmeasured-suite", plant_suite("zz_unmeasured"), 1, "no recorded duration"),
    ("remove-suite-aaf", remove_suite("aaf"), 1, "not in the inventory"),
    ("yml-timeout-116", edit(YML, VJOB,
                             VJOB.replace("timeout-minutes: 120", "timeout-minutes: 116")), 1, "head worker"),
    ("yml-timeout-117", edit(YML, VJOB,
                             VJOB.replace("timeout-minutes: 120", "timeout-minutes: 117")), 0, None),
    ("yml-total-6", edit(YML, "        total: [5]\n", "        total: [6]\n"), 1,
     "WORKER_OVERHEAD_SECONDS describes"),
    ("yml-second-timeout", edit(YML, VJOB,
                                VJOB.replace("timeout-minutes: 120\n", "timeout-minutes: 120\n    timeout-minutes: 500\n")),
     1, "timeout-minutes values"),
    ("yml-missing", delete(YML), 1, "FAIL head"),
    ("driver-missing", delete(DRV), 1, "FAIL head"),
    ("gptp-plane-plus-500", sub('"gptp_plane": 784,', '"gptp_plane": 1284,'), 1,
     "head worker"),
    ("driver-arm-unparseable",
     edit(DRV, "    *)                 printf '%s\\n' \"${SUITE_TIMEOUT:-1800}\" ;;\n",
          "    *)                 echo 1800 ;;\n"), 1, "FAIL head"),
    ("provisional-head-wrong",
     chain(plant_suite("zz_new"),
           sub('    "tsn_fuzz": 60,\n}', '    "tsn_fuzz": 60,\n    "zz_new": 1799,\n}'),
           sub("PROVISIONAL_SUITES: frozenset[str] = frozenset()",
               'PROVISIONAL_SUITES: frozenset[str] = frozenset({"zz_new"})')),
     1, "1799"),
]


def build(checkout, tree):
    if tree.exists():
        shutil.rmtree(tree)
    for rel in (SEL, YML, DRV):
        (tree / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(checkout / rel, tree / rel)
    for d in sorted((checkout / "tb/verilator").iterdir()):
        if d.is_dir() and (d / "Makefile").is_file():
            (tree / "tb/verilator" / d.name).mkdir(parents=True)
            (tree / "tb/verilator" / d.name / "Makefile").touch()


def run(checkout, work, case):
    name, apply, want_rc, want = case
    tree = work / name
    build(checkout, tree)
    try:
        if apply:
            apply(tree)
    except RuntimeError as exc:
        return name, "DRIFT", str(exc), ""
    proc = subprocess.run([sys.executable, "-I", str(tree / SEL), "--selftest"],
                          capture_output=True, text=True, cwd=tree, timeout=300)
    out = proc.stdout + proc.stderr
    (work / f"{name}.log").write_text(out + f"rc={proc.returncode}\n")
    bad = [l.strip() for l in out.splitlines()
           if l.lstrip().startswith(("ESCAPED", "FAIL"))]
    ok = proc.returncode == want_rc and (
        want is None and not bad if want_rc == 0 else any(want in l for l in bad))
    verdict = "ok" if ok else "UNEXPECTED"
    return name, verdict, f"rc={proc.returncode} (want {want_rc})", " | ".join(bad)[:400]


def main():
    checkout, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    work.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        results = list(pool.map(lambda c: run(checkout, work, c), CASES))
    fails = 0
    for name, verdict, rc, bad in results:
        print(f"{verdict:10} {name:36} {rc:16} {bad}")
        fails += verdict != "ok"
    print(f"cases {len(results)}, unexpected {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

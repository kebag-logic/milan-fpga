#!/usr/bin/env python3
"""Reviewer mutation/plant harness for scripts/suite_shards.py.

Usage: probe_727.py REPO SCRATCH OUTDIR [--jobs N]
Builds one disposable tree per case under SCRATCH (scripts/suite_shards.py,
.github/workflows/rtl.yml, tb/verilator/<suite>/Makefile stubs copied from
REPO's inventory), applies the case's exact-once text edits, runs
`python3 -I scripts/suite_shards.py --selftest` there and records rc and
every FAIL/ESCAPED line.  REPO is only read."""
import json, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

S, W = "scripts/suite_shards.py", ".github/workflows/rtl.yml"
# case: (expected rc, edits [(file, old, new, count or None=all)], tree ops)
CASES = {
 "tree-head": (0, [], []),
 "missing-duration-free": (1, [
   (S, "for suite in suites if suite not in seconds]", "for suite in suites if False]", 1),
   (S, "load[worker] += seconds[suite]", "load[worker] += seconds.get(suite, 0)", 1),
   (S, "key=lambda suite: (-seconds[suite], suite))", "key=lambda suite: (-seconds.get(suite, 0), suite))", 1)], []),
 "stale-check-deleted": (1, [(S, "for suite in sorted(set(seconds) - inventory)]", "for suite in sorted(set(seconds) - inventory) if False]", 1)], []),
 "zero-duration-allowed": (1, [(S, "seconds[suite] > 0)", "seconds[suite] >= 0)", 1)], []),
 "timeout-mirrored-120": (1, [(S, "    bound = bound_seconds(timeout)\n", "    bound = bound_seconds(120)\n", 1)], []),
 "headroom-61": (1, [(S, "HEADROOM_PERCENT = 60\n", "HEADROOM_PERCENT = 61\n", 1)], []),
 "headroom-75": (1, [(S, "HEADROOM_PERCENT = 60\n", "HEADROOM_PERCENT = 75\n", 1)], []),
 "bound-plus-one": (1, [(S, "return timeout_minutes * 60 * HEADROOM_PERCENT // 100", "return timeout_minutes * 60 * HEADROOM_PERCENT // 100 + 1", 1)], []),
 "bound-ge": (1, [(S, "for worker, value in enumerate(load) if value > bound]", "for worker, value in enumerate(load) if value >= bound]", 1)], []),
 "bound-mean-only": (1, [(S, "for worker, value in enumerate(load) if value > bound]", "for worker, value in enumerate(load) if sum(load) / len(load) > bound]", 1)], []),
 "worker-count-mirrored": (1, [(S, 'return found["timeout-minutes"], found["matrix total"]', 'return found["timeout-minutes"], 5', 1)], []),
 "overhead-dropped": (1, [(S, "load = list(overhead) if layout else [0] * total", "load = [0] * total", 1)], []),
 "pins-dropped": (1, [(S, "        fixed.update(PINNED_SUITES)\n", "        pass\n", 1)], []),
 "pin-moved": (1, [(S, 'PINNED_SUITES = {"tsn_fuzz": 1, "chmap_capture": 3}', 'PINNED_SUITES = {"tsn_fuzz": 0, "chmap_capture": 3}', 1)], []),
 "dedicated-dropped": (1, [(S, "    if balanced != total:\n        fixed.update(", "    if False:\n        fixed.update(", 1)], []),
 "measure-from-job-start": (1, [(S, "windows, previous = {}, start", "windows, previous = {}, first", 1)], []),
 "measure-floor": (1, [(S, "windows[suite] = -(-(ticks - previous) // TICKS_PER_SECOND)", "windows[suite] = (ticks - previous) // TICKS_PER_SECOND", 1)], []),
 "measure-accepts-timeout": (1, [(S, 'if result.group(1) != "PASS":', 'if result.group(1) == "NEVER":', 1)], []),
 "tie-by-hash": (None, [(S, "key=lambda suite: (-seconds[suite], suite))", "key=lambda suite: (-seconds[suite], hash(suite)))", 1)], []),
 "gptp_plane-plus-500": (1, [(S, '    "gptp_plane": 784,', '    "gptp_plane": 1284,', 1)], []),
 "maap-at-issue-1380": (0, [(S, '    "maap": 1375,', '    "maap": 1380,', 1)], []),
 "plant-unmeasured-suite-dir": (1, [], [("mkdir", "tb/verilator/zz_unmeasured")]),
 "remove-suite-dir": (1, [], [("rmdir", "tb/verilator/aes3")]),
 "rtl-timeout-116": (1, [(W, "    timeout-minutes: 120\n    strategy:\n      fail-fast: false\n      matrix:\n        shard: [0, 1, 2, 3, 4]", "    timeout-minutes: 116\n    strategy:\n      fail-fast: false\n      matrix:\n        shard: [0, 1, 2, 3, 4]", 1)], []),
 "rtl-timeout-117": (0, [(W, "    timeout-minutes: 120\n    strategy:\n      fail-fast: false\n      matrix:\n        shard: [0, 1, 2, 3, 4]", "    timeout-minutes: 117\n    strategy:\n      fail-fast: false\n      matrix:\n        shard: [0, 1, 2, 3, 4]", 1)], []),
 "rtl-six-workers": (1, [(W, "        shard: [0, 1, 2, 3, 4]\n        total: [5]", "        shard: [0, 1, 2, 3, 4, 5]\n        total: [6]", 1)], []),
 "rtl-missing": (1, [], [("rm", W)]),
 "rtl-second-timeout-in-job": (1, [(W, "    timeout-minutes: 120\n    strategy:\n      fail-fast: false\n      matrix:\n        shard: [0, 1, 2, 3, 4]", "    timeout-minutes: 120\n    timeout-minutes: 120\n    strategy:\n      fail-fast: false\n      matrix:\n        shard: [0, 1, 2, 3, 4]", 1)], []),
}

def build(repo, root, name):
    tree = root / name
    shutil.rmtree(tree, ignore_errors=True)
    (tree / "scripts").mkdir(parents=True)
    (tree / ".github/workflows").mkdir(parents=True)
    shutil.copyfile(repo / S, tree / S)
    shutil.copyfile(repo / W, tree / W)
    for d in sorted((repo / "tb/verilator").iterdir()):
        if d.is_dir() and (d / "Makefile").is_file():
            (tree / "tb/verilator" / d.name).mkdir(parents=True)
            (tree / "tb/verilator" / d.name / "Makefile").touch()
    return tree

def run(args):
    repo, root, name = args
    expect, edits, ops = CASES[name]
    tree = build(repo, root, name)
    for f, old, new, count in edits:
        text = (tree / f).read_text()
        n = text.count(old)
        if n != (count if count is not None else n) or n == 0:
            return name, {"rc": None, "error": f"fixture drift: {old!r} occurs {n}x"}
        (tree / f).write_text(text.replace(old, new))
    for op, path in ops:
        p = tree / path
        if op == "mkdir":
            p.mkdir(); (p / "Makefile").touch()
        elif op == "rmdir":
            shutil.rmtree(p)
        elif op == "rm":
            p.unlink()
    out = subprocess.run([sys.executable, "-I", "scripts/suite_shards.py", "--selftest"],
                         cwd=tree, capture_output=True, text=True, timeout=600)
    lines = [l.strip() for l in (out.stdout + out.stderr).splitlines()
             if "FAIL" in l or "ESCAPED" in l or "Traceback" in l or "Error" in l]
    return name, {"rc": out.returncode, "expected_rc": expect,
                  "drift": expect is not None and out.returncode != expect,
                  "flagged": lines, "last": (out.stdout.strip().splitlines() or [""])[-1]}

def main():
    repo, root, outdir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    root.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(jobs) as pool:
        results = dict(pool.map(run, [(repo, root, n) for n in CASES]))
    (outdir / "probe_727.json").write_text(json.dumps(results, indent=1))
    for n, r in results.items():
        print(f"{n:28} rc={r.get('rc')} expect={r.get('expected_rc')} "
              f"{'DRIFT ' if r.get('drift') or r.get('error') else ''}{r.get('error','')}")
        for l in r.get("flagged", []):
            print(f"{'':30}{l[:150]}")
    return 1 if any(r.get("drift") or r.get("error") for r in results.values()) else 0

sys.exit(main())

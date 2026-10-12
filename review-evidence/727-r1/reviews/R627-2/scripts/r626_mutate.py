#!/usr/bin/env python3
"""Gate mutation and tree-planting probes for scripts/suite_shards.py (#727).

Usage: python3 -I mutate.py HEAD_CHECKOUT WORKDIR [--jobs N]

Each case builds a disposable tree under WORKDIR (inventory directories with
their Makefiles, rtl.yml, the selector), applies one source mutation or one
tree planting, runs `python3 -I scripts/suite_shards.py --selftest` there and
records rc plus every [ok]/ESCAPED/FAIL line. Every textual replacement must
match exactly once, or the case is reported as DRIFT. The checkout itself is
only read.
"""
import argparse
import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

# name -> list of (old, new) replacements in scripts/suite_shards.py
SOURCE_MUTANTS = {
    "missing-duration-free": [
        ('    problems = [f"{suite}: inventory suite with no recorded duration in "\n'
         '                "SUITE_SECONDS (refresh it as the module docstring says)"\n'
         '                for suite in suites if suite not in seconds]\n',
         '    problems = []\n'),
        ('    problems = table_problems(suites, seconds)\n    if problems:\n'
         '        raise ValueError("; ".join(problems))\n',
         '    problems = table_problems(suites, seconds)\n    if problems:\n'
         '        raise ValueError("; ".join(problems))\n'
         '    seconds = {**dict.fromkeys(suites, 0), **seconds}\n'),
    ],
    "stale-entry-check-deleted": [
        ('    problems += [f"{suite}: SUITE_SECONDS names a suite that is not in the "\n'
         '                 "inventory" for suite in sorted(set(seconds) - inventory)]\n', ''),
    ],
    "timeout-mirrored-120": [
        ('    return found["timeout-minutes"], found["matrix total"]\n',
         '    return 120, found["matrix total"]\n'),
    ],
    "worker-count-mirrored-5": [
        ('    return found["timeout-minutes"], found["matrix total"]\n',
         '    return found["timeout-minutes"], 5\n'),
    ],
    "overhead-dropped": [
        ('    load = list(overhead) if layout else [0] * total\n',
         '    load = [0] * total\n'),
    ],
    "bound-ge": [
        ('for worker, value in enumerate(load) if value > bound]',
         'for worker, value in enumerate(load) if value >= bound]'),
    ],
    "mean-only": [
        ('for worker, value in enumerate(load) if value > bound]',
         'for worker, value in [(0, sum(load) // len(load))] if value > bound]'),
    ],
    "headroom-100-percent": [
        ('HEADROOM_PERCENT = 60\n', 'HEADROOM_PERCENT = 100\n'),
    ],
    "headroom-75-percent": [
        ('HEADROOM_PERCENT = 60\n', 'HEADROOM_PERCENT = 75\n'),
    ],
    "bound-formula-div10": [
        ('    return timeout_minutes * 60 * HEADROOM_PERCENT // 100\n',
         '    return timeout_minutes * 60 * HEADROOM_PERCENT // 10\n'),
    ],
    "pins-dropped": [
        ('    if layout:\n        fixed.update(PINNED_SUITES)\n', ''),
    ],
    "pin-moved-tsn_fuzz-0": [
        ('PINNED_SUITES = {"tsn_fuzz": 1, "chmap_capture": 3}',
         'PINNED_SUITES = {"tsn_fuzz": 0, "chmap_capture": 3}'),
    ],
    "dedicated-dropped": [
        ('    if balanced != total:\n        fixed.update(', '    if False:\n        fixed.update('),
    ],
    "head-arms-skipped": [
        ('    return HERE.name == "suite_shards.py" and HERE.parent.name == "scripts"\n',
         '    return False\n'),
    ],
    "measure-from-job-start": [
        ('    windows, previous = {}, start\n', '    windows, previous = {}, first\n'),
    ],
    "measure-round-down": [
        ('        windows[suite] = -(-(ticks - previous) // TICKS_PER_SECOND)\n',
         '        windows[suite] = (ticks - previous) // TICKS_PER_SECOND\n'),
    ],
    "nondeterministic-tie": [
        ('key=lambda suite: (-seconds[suite], suite)):',
         'key=lambda suite: (-seconds[suite], hash(suite))):'),
    ],
    "table-zero-duration-allowed": [
        ('isinstance(seconds[suite], int) and seconds[suite] > 0)]',
         'isinstance(seconds[suite], int) and seconds[suite] >= 0)]'),
    ],
}


def tree_planting(name, root, head):
    """Apply one planting to a built tree; returns a description."""
    wf = root / ".github/workflows/rtl.yml"
    sel = root / "scripts/suite_shards.py"
    if name == "tree-unmeasured-suite":
        (root / "tb/verilator/zz_new_suite").mkdir()
        (root / "tb/verilator/zz_new_suite/Makefile").write_text("all:\n")
    elif name == "tree-removed-suite":
        shutil.rmtree(root / "tb/verilator/cbs")
    elif name == "tree-gptp_plane+500":
        text = sel.read_text()
        assert text.count('"gptp_plane": 784,') == 1
        sel.write_text(text.replace('"gptp_plane": 784,', '"gptp_plane": 1284,'))
    elif name.startswith("tree-timeout-"):
        minutes = name.rsplit("-", 1)[1]
        text = wf.read_text()
        assert text.count("    timeout-minutes: 120\n") >= 1
        lines = text.splitlines(keepends=True)
        start = lines.index("  verilator-shards:\n")
        for n in range(start, len(lines)):
            if lines[n] == "    timeout-minutes: 120\n":
                lines[n] = f"    timeout-minutes: {minutes}\n"
                break
        wf.write_text("".join(lines))
    elif name == "tree-six-workers":
        text = wf.read_text()
        old = "        shard: [0, 1, 2, 3, 4]\n        total: [5]\n"
        assert text.count(old) == 1
        wf.write_text(text.replace(old, "        shard: [0, 1, 2, 3, 4, 5]\n        total: [6]\n"))
    elif name == "tree-missing-rtl.yml":
        wf.unlink()
    elif name == "tree-timeout-expression":
        text = wf.read_text()
        lines = text.splitlines(keepends=True)
        start = lines.index("  verilator-shards:\n")
        for n in range(start, len(lines)):
            if lines[n] == "    timeout-minutes: 120\n":
                lines[n] = "    timeout-minutes: ${{ 120 }}\n"
                break
        wf.write_text("".join(lines))
    elif name == "tree-step-timeout-added":
        # A step-level timeout-minutes (deeper indent) must not be read as the job's.
        text = wf.read_text()
        old = "      - name: Prove specialized suite ownership\n"
        assert text.count(old) == 1
        wf.write_text(text.replace(old, old + "        timeout-minutes: 5\n"))
    elif name == "tree-maap-1380":
        text = sel.read_text()
        assert text.count('"maap": 1375,') == 1
        sel.write_text(text.replace('"maap": 1375,', '"maap": 1380,'))
    elif name == "tree-head":
        pass
    else:
        raise KeyError(name)


TREE_CASES = ["tree-head", "tree-unmeasured-suite", "tree-removed-suite",
              "tree-gptp_plane+500", "tree-timeout-116", "tree-timeout-117",
              "tree-six-workers", "tree-missing-rtl.yml", "tree-timeout-expression",
              "tree-step-timeout-added", "tree-maap-1380"]


def build_tree(head, root):
    (root / "scripts").mkdir(parents=True)
    (root / ".github/workflows").mkdir(parents=True)
    shutil.copy2(head / "scripts/suite_shards.py", root / "scripts/suite_shards.py")
    shutil.copy2(head / ".github/workflows/rtl.yml", root / ".github/workflows/rtl.yml")
    for mk in sorted((head / "tb/verilator").glob("*/Makefile")):
        dest = root / "tb/verilator" / mk.parent.name
        dest.mkdir(parents=True)
        shutil.copy2(mk, dest / "Makefile")


def run_case(head, work, name):
    root = work / name
    if root.exists():
        shutil.rmtree(root)
    build_tree(head, root)
    sel = root / "scripts/suite_shards.py"
    if name in SOURCE_MUTANTS:
        text = sel.read_text()
        for old, new in SOURCE_MUTANTS[name]:
            if text.count(old) != 1:
                return name, None, f"DRIFT: replacement matched {text.count(old)} times"
            text = text.replace(old, new)
        sel.write_text(text)
    else:
        tree_planting(name, root, head)
    proc = subprocess.run([sys.executable, "-I", "scripts/suite_shards.py", "--selftest"],
                          cwd=root, capture_output=True, text=True, timeout=600)
    keep = [line for line in (proc.stdout + proc.stderr).splitlines()
            if "[ok]" in line or "ESCAPED" in line or "FAIL" in line
            or "head worker" in line or "selftest:" in line or "skip head" in line
            or "specialized owners" in line or "Traceback" in line or "Error" in line]
    return name, proc.returncode, "\n".join(keep)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("head", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    names = list(SOURCE_MUTANTS) + TREE_CASES
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(args.jobs, 16)) as pool:
        results = list(pool.map(lambda n: run_case(args.head.resolve(), args.work.resolve(), n), names))
    for name, rc, text in results:
        print(f"=== {name}: rc={rc}")
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

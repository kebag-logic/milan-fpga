#!/usr/bin/env python3
"""Independent mutants of the slot memory-cap code in scripts/act_ci.py, graded by its --selftest.

Each mutant is a list of exact (old, new) substitutions that must each occur
exactly once. The mutated act_ci.py replaces the one in a private copy of TREE
and `python3 scripts/act_ci.py --selftest` runs inside sandbox.sh (no network,
no Docker socket, inert sudo). KILLED means the self-test exited non-zero; the
failing arm labels are listed so a kill can be attributed.

usage: slot_mutants_r267_3.py TREE OUT_DIR root|user [--jobs N]
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox.sh"

REPORT_PRINT = (
    '        print(\n'
    '            f"act-ci: slot {slot.number}: {require_slot_memory_cap_unexhausted(slot, host)}",\n'
    '            flush=True,\n'
    '        )\n'
)

MUTANTS: list[tuple[str, str, list[tuple[str, str]]]] = [
    ("S00", "control: a comment line only", [
        ('SLOT_MEMORY_MAX = "24G"\n', 'SLOT_MEMORY_MAX = "24G"\n# r267-3 control mutant\n')]),
    ("S01", "a missing max count read as 0", [
        ('        hits = int(events["max"])\n', '        hits = int(events.get("max", 0))\n')]),
    ("S02", "the cap-hit count taken from oom", [
        ('        hits = int(events["max"])\n', '        hits = int(events["oom"])\n')]),
    ("S03", "a slice at its cap without an OOM refused", [
        ('    if exhausted:\n        raise Refusal(\n', '    if exhausted or hits:\n        raise Refusal(\n')]),
    ("S04", "the OOM count taken from oom_kill (always 0 in the slice's local file)", [
        ('        exhausted = int(events["oom"])\n', '        exhausted = int(events["oom_kill"])\n')]),
    ("S05", "the hierarchical memory.events read instead of the slice's own", [
        ('host.read_text(cgroup / "memory.events.local")', 'host.read_text(cgroup / "memory.events")')]),
    ("S06", "an OOM at the cap ignored", [
        ('    if exhausted:\n        raise Refusal(\n', '    if False:\n        raise Refusal(\n')]),
    ("S07", "a single OOM at the cap ignored", [
        ('    if exhausted:\n        raise Refusal(\n', '    if exhausted > 1:\n        raise Refusal(\n')]),
    ("S08", "the memory check never runs after the body", [
        (REPORT_PRINT, "        pass\n")]),
    ("S09", "a missing oom count read as 0", [
        ('        exhausted = int(events["oom"])\n', '        exhausted = int(events.get("oom", 0))\n')]),
    ("S10", "the OOM count taken from oom_kill, fixture-matched (oom_group_kill)", [
        ('        exhausted = int(events["oom"])\n', '        exhausted = int(events.get("oom_group_kill", events["oom"]))\n')]),
]


def apply(source: str, edits: list[tuple[str, str]]) -> str | None:
    """The mutated source, or None when an edit does not occur exactly once."""
    for old, new in edits:
        if source.count(old) != 1:
            return None
        source = source.replace(old, new, 1)
    return source


def run(mid: str, text: str, tree: pathlib.Path, out: pathlib.Path, mode: str) -> tuple[str, int, list[str], str]:
    """Run one mutant's self-test in the sandbox; its id, rc, failed arms and last line."""
    work = out / "scratch" / mode / mid
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(tree, work, symlinks=True)
    target = work / "scripts" / "act_ci.py"
    target.write_text(text, encoding="utf-8")
    target.chmod(0o755)
    proc = subprocess.run(
        [str(SANDBOX), mode, str(work), "--", "python3", "scripts/act_ci.py", "--selftest"],
        capture_output=True, text=True, timeout=900,
    )
    log = proc.stdout + proc.stderr
    (out / "logs" / mode).mkdir(parents=True, exist_ok=True)
    (out / "logs" / mode / f"{mid}.log").write_text(log, encoding="utf-8")
    failed = re.findall(r"^  FAIL (.*)$", log, flags=re.M)
    last = log.strip().splitlines()[-1] if log.strip() else ""
    shutil.rmtree(work, ignore_errors=True)
    return mid, proc.returncode, failed, last


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tree", type=pathlib.Path)
    parser.add_argument("out", type=pathlib.Path)
    parser.add_argument("mode", choices=("root", "user"))
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    source = (args.tree / "scripts" / "act_ci.py").read_text(encoding="utf-8")
    print(f"# source act_ci.py sha256 {hashlib.sha256(source.encode()).hexdigest()} mode {args.mode}")
    described = {mid: what for mid, what, _ in MUTANTS}
    jobs: dict[str, str] = {}
    for mid, what, edits in MUTANTS:
        text = apply(source, edits)
        if text is None:
            print(f"{mid}\tNOT-APPLICABLE\t-\t{what}")
            continue
        jobs[mid] = text
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(run, mid, text, args.tree, args.out, args.mode) for mid, text in jobs.items()]
        for future in concurrent.futures.as_completed(futures):
            mid, rc, failed, last = future.result()
            results[mid] = (rc, failed, last)
    for mid in jobs:
        rc, failed, last = results[mid]
        verdict = "SURVIVED" if rc == 0 else "KILLED"
        print(f"{mid}\t{verdict}\trc={rc}\t{described[mid]}\tfailed-arms={' || '.join(failed) or '-'}\t{last}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

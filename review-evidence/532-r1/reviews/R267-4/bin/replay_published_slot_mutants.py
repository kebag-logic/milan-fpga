#!/usr/bin/env python3
"""Re-run the published slot mutants of scripts/act_ci.py at a head, in this packet's sandbox.

The mutant lists are imported verbatim from the published author scripts
(review-evidence/532-r1/correction-a213/bin/slot-mutants.py, MUTANTS, and
review-evidence/532-r1/correction-a220/bin/slot-mutants-a220.py, A220_MUTANTS).
Each must apply exactly once to TREE/scripts/act_ci.py. Each worker owns a
private copy of TREE, writes one mutated act_ci.py into it, and runs
`python3 scripts/act_ci.py --selftest` inside sandbox.sh (no network, no Docker
socket, inert sudo). KILLED means the self-test exited non-zero.

usage: replay_published_slot_mutants.py A213_PY A220_PY TREE WORK root|user [--jobs N] [--range START:END]

Round R267-4: --range grades only mutants START..END-1 of the combined list, so
a replay fits a bounded foreground command; the ranges together cover the list.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import pathlib
import queue
import shutil
import subprocess
import sys
import threading

HERE = pathlib.Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox.sh"


def load_list(path: pathlib.Path, name: str) -> list[tuple[str, str, str]]:
    """The literal list `name` from a published script, read without executing it."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in node.targets
        ):
            return [tuple(item) for item in ast.literal_eval(node.value)]
    raise SystemExit(f"{path}: no literal {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("a213", type=pathlib.Path)
    parser.add_argument("a220", type=pathlib.Path)
    parser.add_argument("tree", type=pathlib.Path)
    parser.add_argument("work", type=pathlib.Path)
    parser.add_argument("mode", choices=("root", "user"))
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--range", default="")
    parser.add_argument("--mutant-timeout", type=int, default=600)
    args = parser.parse_args()
    mutants = load_list(args.a213, "MUTANTS") + load_list(args.a220, "A220_MUTANTS")
    source_path = args.tree / "scripts" / "act_ci.py"
    source = source_path.read_text(encoding="utf-8")
    digest = hashlib.sha256(source.encode()).hexdigest()
    print(f"# head act_ci.py sha256 {digest} mode {args.mode} mutants {len(mutants)}", flush=True)
    todo: queue.Queue[tuple[int, str, str]] = queue.Queue()
    results: dict[int, str] = {}
    lo, hi = (int(x) for x in args.range.split(":")) if args.range else (0, len(mutants))
    print(f"# range {lo}:{hi}", flush=True)
    for index, (label, before, after) in enumerate(mutants):
        if not lo <= index < hi:
            continue
        count = source.count(before)
        if count != 1:
            results[index] = f"{label}\tNOT-APPLICABLE\tcount={count}\t-"
            continue
        todo.put((index, label, source.replace(before, after, 1)))

    def worker(number: int) -> None:
        tree = args.work / f"w{number}"
        shutil.rmtree(tree, ignore_errors=True)
        shutil.copytree(args.tree, tree, symlinks=True)
        target = tree / "scripts" / "act_ci.py"
        while True:
            try:
                index, label, text = todo.get_nowait()
            except queue.Empty:
                break
            target.write_text(text, encoding="utf-8")
            try:
                proc = subprocess.run(
                    [str(SANDBOX), args.mode, str(tree), "--", "python3", "scripts/act_ci.py", "--selftest"],
                    capture_output=True, text=True, timeout=args.mutant_timeout,
                )
                rc, out = proc.returncode, proc.stdout + proc.stderr
            except subprocess.TimeoutExpired:
                rc, out = 124, "timed out"
            failed = [line.strip() for line in out.splitlines() if line.startswith("  FAIL")]
            verdict = "SURVIVED" if rc == 0 else "KILLED"
            results[index] = f"{label}\t{verdict}\trc={rc}\t{(failed[0] if failed else '-')[:200]}"
        shutil.rmtree(tree, ignore_errors=True)

    threads = [threading.Thread(target=worker, args=(n,)) for n in range(args.jobs)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    for index in range(lo, min(hi, len(mutants))):
        print(results[index])
    after = hashlib.sha256(source_path.read_bytes()).hexdigest()
    print(f"# head act_ci.py after run sha256 {after} {'EXACT' if after == digest else 'CHANGED'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

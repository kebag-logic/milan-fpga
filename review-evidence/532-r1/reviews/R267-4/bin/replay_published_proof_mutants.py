#!/usr/bin/env python3
"""Re-run a published set of act_slot_proof.sh mutants at a head, in this packet's sandbox.

The literal list MUTANTS is read (not executed) from a published reviewer or
author script. Entries are (label, old, new) or (id, description, old, new).
Each `old` must occur exactly once in TREE/scripts/act_slot_proof.sh; the
mutated copy's own `--selftest` runs inside sandbox.sh, whose `bash "$0"`
re-invocations grade the mutated proof. KILLED means the self-test failed.

usage: replay_published_proof_mutants.py PUBLISHED_PY TREE WORK root|user [--jobs N]
"""
from __future__ import annotations

import argparse
import ast
import concurrent.futures
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox.sh"


def load(path: pathlib.Path) -> list[tuple[str, str, str]]:
    """(label, old, new) for every entry of the published literal MUTANTS."""
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "MUTANTS" for t in node.targets
        ):
            entries = ast.literal_eval(node.value)
            return [
                (e[0], e[1], e[2]) if len(e) == 3 else (f"{e[0]} {e[1]}", e[2], e[3])
                for e in entries
            ]
    raise SystemExit(f"{path}: no literal MUTANTS")


def run(index: int, text: str, work: pathlib.Path, mode: str) -> tuple[int, int, list[str]]:
    """One mutant's sandboxed self-test: its index, rc and failed case names."""
    tree = work / f"m{index}"
    shutil.rmtree(tree, ignore_errors=True)
    (tree / "scripts").mkdir(parents=True)
    script = tree / "scripts" / "act_slot_proof.sh"
    script.write_text(text, encoding="utf-8")
    script.chmod(0o755)
    proc = subprocess.run(
        [str(SANDBOX), mode, str(tree), "--", "bash", "scripts/act_slot_proof.sh", "--selftest"],
        capture_output=True, text=True, timeout=900,
    )
    failed = re.findall(r"^  FAIL (.*?): exit", proc.stdout + proc.stderr, flags=re.M)
    shutil.rmtree(tree, ignore_errors=True)
    return index, proc.returncode, failed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("published", type=pathlib.Path)
    parser.add_argument("tree", type=pathlib.Path)
    parser.add_argument("work", type=pathlib.Path)
    parser.add_argument("mode", choices=("root", "user"))
    parser.add_argument("--jobs", type=int, default=2)
    args = parser.parse_args()
    mutants = load(args.published)
    path = args.tree / "scripts" / "act_slot_proof.sh"
    source = path.read_text(encoding="utf-8")
    digest = hashlib.sha256(source.encode()).hexdigest()
    print(f"# {args.published.name}: {len(mutants)} entries; head proof sha256 {digest}; mode {args.mode}", flush=True)
    lines: dict[int, str] = {}
    jobs = {}
    for index, (label, old, new) in enumerate(mutants):
        count = source.count(old)
        if count != 1:
            lines[index] = f"{label}\tNOT-APPLICABLE\tcount={count}\t-"
        else:
            jobs[index] = source.replace(old, new, 1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for index, rc, failed in pool.map(lambda item: run(item[0], item[1], args.work, args.mode), jobs.items()):
            verdict = "SURVIVED" if rc == 0 else "KILLED"
            lines[index] = f"{mutants[index][0]}\t{verdict}\trc={rc}\t{'; '.join(failed) or '-'}"
    for index in range(len(mutants)):
        print(lines[index])
    after = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"# head proof after run sha256 {after} {'EXACT' if after == digest else 'CHANGED'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Reviewer probes for the PR #702 round-3 delta (d10aee62 -> 6904af6b).

Each probe copies syn/ooc from a checkout into a fresh scratch directory, applies
one exact, unique text edit, runs `pp_resource_gate.py --selftest` there under
the chosen interpreter and reports rc plus the first failing assertion. Nothing
in the checkout is modified.

Usage: delta_probes.py <head-checkout> <base-checkout> <scratch-dir> <python> [<python> ...]
"""

import shutil
import subprocess
import sys
from pathlib import Path

PRINTED = ("wrong = [] if printing else misplaced(", "wrong = misplaced(")
ARGPARSE = ("result = cli(command, *arguments, *options)", "result = cli(command, *options, *arguments)")
ARGPARSE_SPLIT = ("cli(command, *arguments, *options), 2,", "cli(command, *options, *arguments), 2,")
NO_PRINTED = ("            if label != \"wrapper absent\":", "            if False:")
WRITE_DROPPED = ('judged = (("check",), ("record", "--write"))', 'judged = (("check",), ("record",))')
BYTES_SKIPPED = ("                if baseline.read_bytes() != baseline_bytes:\n"
                 "                    raise AssertionError(\"wrong all-fabric population changed acceptance baseline\")",
                 "                if False:\n"
                 "                    raise AssertionError(\"wrong all-fabric population changed acceptance baseline\")")
WRITE_IGNORES_POP = ("            if wrong:\n                raise Refusal", "            if False:\n                raise Refusal")

PROBES = [
    # name, tree, file, edits; expected rc per interpreter tag is judged by the reader from the table
    ("head control", "head", None, []),
    ("base control", "base", None, []),
    ("head: printed record judged (gate mutant)", "head", "pp_resource_gate.py", [PRINTED]),
    ("base: printed record judged (gate mutant)", "base", "pp_resource_gate.py", [PRINTED]),
    ("head: option before directory restored in the plant loop", "head", "pp_placement_selftest.py", [ARGPARSE]),
    ("head: option before directory restored in the split-census arm", "head", "pp_placement_selftest.py",
     [ARGPARSE_SPLIT]),
    ("head: printed-record assertion removed", "head", "pp_placement_selftest.py", [NO_PRINTED]),
    ("head: --write dropped from the judged pair", "head", "pp_placement_selftest.py", [WRITE_DROPPED]),
    ("head: record --write ignores population (gate)", "head", "pp_resource_gate.py", [WRITE_IGNORES_POP]),
    ("head: baseline-byte check skipped + record --write ignores population", "head", None,
     [("pp_placement_selftest.py",) + BYTES_SKIPPED, ("pp_resource_gate.py",) + WRITE_IGNORES_POP]),
]


def apply(folder: Path, target: str, old: str, new: str) -> None:
    path = folder / target
    text = path.read_text()
    if text.count(old) != 1:
        raise SystemExit(f"edit not unique in {target}: {old!r} count={text.count(old)}")
    path.write_text(text.replace(old, new))


def main() -> int:
    head, base, scratch, *pythons = sys.argv[1:]
    trees = {"head": Path(head) / "syn/ooc", "base": Path(base) / "syn/ooc"}
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    for number, (name, tree, target, edits) in enumerate(PROBES):
        for python in pythons:
            version = subprocess.run([python, "-c", "import sys;print('%d.%d.%d' % sys.version_info[:3])"],
                                     capture_output=True, text=True, check=True).stdout.strip()
            folder = scratch / f"p{number:02d}_{version}"
            if folder.exists():
                shutil.rmtree(folder)
            shutil.copytree(trees[tree], folder)
            for edit in edits:
                if len(edit) == 3:
                    apply(folder, *edit)
                else:
                    apply(folder, target, *edit)
            result = subprocess.run([python, "-B", str(folder / "pp_resource_gate.py"), "--selftest"],
                                    capture_output=True, text=True, timeout=600)
            failure = next((line for line in reversed(result.stderr.splitlines()) if "Error" in line), "")
            print(f"{name} | python {version} | rc={result.returncode} | {failure[:300]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

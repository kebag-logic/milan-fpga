#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R228-4: run r228_4_gate_probes.py inside gate 1b of a DISPOSABLE tree.

Usage: r228_4_gate_run.py <disposable-tree> <sdk-prefix> <out.json> [<mutant-id>]

Inserts a hook just before gate 1b's mutation loop that exec's the plant
file with the gate's own locals and exits; optionally applies one
r228_4_mutate.MUTANTS entry first (its edits only, no stop hook); drives
the gate through the head's compiler-audit wrapper with the mapped SDK;
restores and verifies the original bytes afterwards.
"""

import hashlib
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import r228_4_mutate  # noqa: E402

ANCHOR = "    for mutation in mutations:\n        assert_rejected(*mutation)\n"
HOOK = ('    if os.environ.get("R228_PROBES"):\n'
        '        _r228 = dict(globals())\n'
        '        _r228.update(locals())\n'
        '        exec(compile(Path(os.environ["R228_PROBES"]).read_text(),\n'
        '                     "r228_4_gate_probes", "exec"), _r228)\n'
        '        raise SystemExit(0)\n' + ANCHOR)


def main() -> int:
    tree, sdk = Path(sys.argv[1]).resolve(), sys.argv[2]
    out = Path(sys.argv[3]).resolve()
    mutant = sys.argv[4] if len(sys.argv) > 4 else None
    target = tree / r228_4_mutate.BUILDER
    original = target.read_bytes()
    before = hashlib.sha256(original).hexdigest()
    text = original.decode()
    if mutant:
        text = r228_4_mutate.apply(text, r228_4_mutate.MUTANTS[mutant][1])
    text = r228_4_mutate.apply(text, [(ANCHOR, HOOK)])
    env = {**os.environ, "R228_PROBES": str(HERE / "r228_4_gate_probes.py"),
           "R228_PROBE_OUT": str(out)}
    try:
        target.write_text(text)
        proc = subprocess.run(
            [sys.executable, "-B", r228_4_mutate.AUDIT, "--sdk-destination", sdk,
             "--audit", str(out.with_suffix(".audit.jsonl"))],
            cwd=tree, env=env, capture_output=True, text=True)
    finally:
        target.write_bytes(original)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == before
    out.with_suffix(".log").write_text(proc.stdout + proc.stderr)
    print(f"{out.name}: rc={proc.returncode}")
    for line in (proc.stdout + proc.stderr).splitlines():
        if line.startswith("R228 PROBE") or "Error" in line:
            print("  " + line[:300])
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())

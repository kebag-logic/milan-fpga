#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R228-3: run r228_gate_probes.py inside gate 1b of a DISPOSABLE tree.

Usage: r228_gate_run.py <disposable-tree> <sdk-prefix> <out.json> [<mutation-id>]

Inserts a hook just before gate 1b's mutation loop that exec's the probe
file with the gate's own locals and then exits, optionally applies one
r228_mutate.MUTATIONS entry first, drives the gate through the head's
compiler-audit wrapper with the mapped SDK (a base tree receives that
wrapper and the installer as untracked copies), and restores and verifies
the original bytes afterwards.
"""

import hashlib
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import r228_mutate  # noqa: E402

ANCHOR = "    for mutation in mutations:\n        assert_rejected(*mutation)\n"
HOOK = ('    if os.environ.get("R228_PROBES"):\n'
        '        _r228 = dict(globals())\n'
        '        _r228.update(locals())\n'
        '        exec(compile(Path(os.environ["R228_PROBES"]).read_text(),\n'
        '                     "r228_gate_probes", "exec"), _r228)\n'
        '        raise SystemExit(0)\n' + ANCHOR)


def main() -> int:
    tree, sdk, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    mutation = sys.argv[4] if len(sys.argv) > 4 else None
    target = tree / r228_mutate.BUILDER
    original = target.read_bytes()
    before = hashlib.sha256(original).hexdigest()
    text = original.decode()
    if mutation:
        _kind, rel, old, new, _what = r228_mutate.MUTATIONS[mutation]
        assert rel == r228_mutate.BUILDER and text.count(old) == 1, mutation
        text = text.replace(old, new)
    assert text.count(ANCHOR) == 1, "mutation-loop anchor"
    text = text.replace(ANCHOR, HOOK)
    probes = os.environ.get("R228_PROBE_FILE", str(HERE / "r228_gate_probes.py"))
    env = {**os.environ, "R228_PROBES": probes,
           "R228_PROBE_OUT": str(out)}
    try:
        target.write_text(text)
        proc = subprocess.run(
            [sys.executable, r228_mutate.AUDIT, "--sdk-destination", sdk,
             "--audit", str(out.with_suffix(".audit.jsonl"))],
            cwd=tree, env=env, capture_output=True, text=True)
    finally:
        target.write_bytes(original)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == before
    out.with_suffix(".log").write_text(proc.stdout + proc.stderr)
    print(f"rc={proc.returncode}")
    for line in (proc.stdout + proc.stderr).splitlines():
        if line.startswith("R228 PROBE") or "Error" in line:
            print(line[:300])
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())

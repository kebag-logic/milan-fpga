#!/usr/bin/env python3
"""Show that probe_r632_6.py can fail: plant each defect in a copy of the head tree and run the probe there.

Usage: python3 -I probe_controls.py <packet> <pristine-tree>
Each control replaces one anchor (which must occur exactly once) in
scripts/act_ci.py of a hard-linked copy under <packet>/scratch/ctl/<id>, then
runs the probe through <packet>/scripts/sandbox.sh. A control is DETECTED when
the probe exits non-zero.
"""
from __future__ import annotations

import concurrent.futures
import pathlib
import shutil
import subprocess
import sys

PACKET = pathlib.Path(sys.argv[1]).resolve()
PRISTINE = pathlib.Path(sys.argv[2]).resolve()
CONTROLS = (
    ("C1", "die frees a range",
     '        if action == "destroy":\n            self.release(container_id)',
     '        if action in ("destroy", "die"):\n            self.release(container_id)'),
    ("C2", "a timed-out move is released before the read",
     "        except Refusal as exc:\n            failure = str(exc)\n",
     "        except Refusal as exc:\n            failure = str(exc)\n            self.held.pop(container_id, None)\n            return\n"),
    ("C3", "an unreadable container's range is freed",
     '                f"{target} stays reserved to it until it is removed"\n            )\n            return\n',
     '                f"{target} stays reserved to it until it is removed"\n            )\n            self.release(container_id)\n            return\n'),
    ("C4", "a move seen off target frees its range",
     "        elif moved_now or self.outcome[container_id] == \"moved\":\n",
     "        elif moved_now or self.outcome[container_id] == \"moved\":\n            self.held.pop(container_id, None)\n"),
    ("C5", "slot spacing back to one range per slot",
     "    return ReplaySlot(slot).number * (SLOT_JOB_RANGES + 1) * CONTAINER_CPU_LIMIT\n",
     "    return ReplaySlot(slot).number * CONTAINER_CPU_LIMIT\n"),
    ("C6", "the derivation adds the workflows instead of taking the most",
     "        most = max(most, sum(widths[:CONCURRENT_JOB_LIMIT]))\n",
     "        most = most + sum(widths[:CONCURRENT_JOB_LIMIT])\n"),
    ("C7", "an unreadable max-parallel falls back to act's default",
     "    if not isinstance(raw, str) or re.fullmatch(r\"[0-9]{1,6}\", raw) is None:\n        raise Refusal(",
     "    if not isinstance(raw, str) or re.fullmatch(r\"[0-9]{1,6}\", raw) is None:\n        return ACT_DEFAULT_MAX_PARALLEL\n        raise Refusal("),
)


def run(control: tuple[str, str, str, str]) -> str:
    ident, title, old, new = control
    tree = PACKET / "scratch" / "ctl" / ident
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(PRISTINE, tree, copy_function=shutil.copy)
    target = tree / "scripts" / "act_ci.py"
    text = target.read_text()
    if text.count(old) != 1:
        return f"{ident} BAD-ANCHOR ({text.count(old)}) {title}"
    target.write_text(text.replace(old, new))
    shutil.copy(PACKET / "scripts" / "probe_r632_6.py", tree / ".probe_r632_6.py")
    result = subprocess.run(
        [str(PACKET / "scripts" / "sandbox.sh"), str(tree), "/usr/bin/python3", "-I", ".probe_r632_6.py", ".", "600"],
        capture_output=True, text=True, timeout=900,
    )
    fails = [line.strip() for line in result.stdout.splitlines() if line.startswith("  FAIL")]
    verdict = "DETECTED" if result.returncode != 0 else "MISSED"
    first = fails[0][:160] if fails else (result.stderr.strip().splitlines() or [""])[-1][:160]
    shutil.rmtree(tree, ignore_errors=True)
    return f"{ident} {verdict} rc={result.returncode} {title}: {len(fails)} FAIL; first: {first}"


with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
    lines = list(pool.map(run, CONTROLS))
for line in lines:
    print(line)
missed = [line for line in lines if " DETECTED " not in line]
print(f"controls: {len(lines)}, detected {len(lines) - len(missed)}, not detected {[line.split()[0] for line in missed]}")
sys.exit(1 if missed else 0)

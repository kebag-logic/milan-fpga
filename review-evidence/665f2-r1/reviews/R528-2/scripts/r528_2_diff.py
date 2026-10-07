#!/usr/bin/env python3
"""Reviewer-planted probe-timing defects for the MAAP differential (R528-2).

Each defect is written into a scratch copy of sw/firmware/ctrl and the
repository's own differential() build/run is invoked on that copy. Caught
means the run completed with failures and a named failing test (rc 1).
Usage: r528_2_diff.py REPO OUT
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))
import maap_differential  # noqa: E402
from ctrl_build import CTRL  # noqa: E402

DEFECTS = [
    ("d-probe-base-1ms", "maap/maap.h", "#define MAAP_PROBE_BASE_MS 500u", "#define MAAP_PROBE_BASE_MS 1u"),
    ("d-probe-reaches-600", "maap/maap.c", "base + MAAP_SERVICE_MS + 1u + draw(",
     "base + MAAP_SERVICE_MS + 12u + draw("),
    ("d-probe-reaches-500", "maap/maap.c", "base + MAAP_SERVICE_MS + 1u + draw(",
     "base - MAAP_SERVICE_MS + 0u + draw("),
    ("d-probe-uses-announce-interval", "maap/maap.c", "start_timer(m, false);\n\t\trequest(m, MAAP_MSG_PROBE);",
     "start_timer(m, true);\n\t\trequest(m, MAAP_MSG_PROBE);"),
    ("d-two-retransmissions", "maap/maap.h", "#define MAAP_PROBE_RETRANSMITS 3u", "#define MAAP_PROBE_RETRANSMITS 2u"),
]


def main() -> int:
    escaped = 0
    for name, path, old, new in DEFECTS:
        copy = out / name / "ctrl"
        if copy.exists():
            shutil.rmtree(copy)
        shutil.copytree(CTRL, copy, ignore=shutil.ignore_patterns("__pycache__"))
        src = copy / path
        text = src.read_text(encoding="utf-8")
        assert text.count(old) == 1, name
        src.write_text(text.replace(old, new), encoding="utf-8")
        outcome = maap_differential.differential(out / name / "build", copy)
        fails = sorted({ln.strip() for ln in outcome.log.splitlines() if ln.startswith("[  FAILED  ]") and "(" in ln})
        caught = outcome.rc == 1 and bool(fails)
        escaped += 0 if caught else 1
        print(f"[{'caught' if caught else 'ESCAPED'}] {name} rc={outcome.rc} failing={fails}", flush=True)
    print(f"differential reviewer defects escaped: {escaped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

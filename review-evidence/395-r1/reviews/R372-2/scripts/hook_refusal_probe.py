#!/usr/bin/env python3
"""Drive the bitstream hook (kl_timing_grade_reports) with a candidate whose
Fast hold analysis was disabled before signoff, using the PR's own Tcl stubs.

Usage: hook_refusal_probe.py <tree-root> [<tree-root> ...]
Prints the hook's exit status per tree: 1 means the candidate is refused.
"""

import sys
import tempfile
from pathlib import Path


def probe(root: Path) -> None:
    sys.path[:0] = [str(root / "sw/builder"), str(root / "sw/litex")]
    for name in [m for m in sys.modules if m.startswith(("platforms", "test_timing_grade"))]:
        del sys.modules[name]
    import test_timing_grade as t  # noqa: PLC0415
    setup = "\n".join(t.configure_commands())
    for label, mutation in (("fast-hold-off", "config_timing_corners -corner Fast -delay_type max"),
                            ("slow-off", "config_timing_corners -corner Slow -delay_type none"),
                            ("grade-industrial", "set grade industrial"),
                            ("tj-25", "set temp 25")):
        with tempfile.TemporaryDirectory(prefix="hook-probe-") as tmp:
            body = f"{setup}\n{mutation}\nkl_timing_grade_reports {t.tcl_word(Path(tmp) / 'candidate')}"
            result = t._run(body)
        print(f"{root.name}: {label}: hook rc={result.returncode} "
              f"stderr={result.stderr.strip()[:90]!r}")
    del sys.path[:2]


for arg in sys.argv[1:]:
    probe(Path(arg))

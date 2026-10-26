#!/usr/bin/env python3
"""Run the round-3 release test class against the round-2 grader's behaviour.

Usage: python3 -I round2_hybrid_shim.py <round-2 planner.py> <round-3 planner.py> <scratch dir>

As round2_hybrid.py, but the round-2 file also gains a module-level shim, just
before the transplanted class, that accepts the round-3 `required_s` keyword
and drops it. So a round-3 arm fails on what the round-2 grader does, not on
the keyword it never had. Each arm that names a round-3 fix must fail (FAIL or
ERROR) there; the log lists them.
"""
import subprocess
import sys
from pathlib import Path

SHIM = '''
_round2_grade = grade_audio_counter_capture


def grade_audio_counter_capture(capture, layout, log, *, max_events=100000, required_s=None):
    """The round-2 grader, accepting and ignoring the round-3 keyword."""
    return _round2_grade(capture, layout, log, max_events=max_events)


AUDIO_GUARD_FRAMES = 63


'''

old_text = Path(sys.argv[1]).read_text()
new_text = Path(sys.argv[2]).read_text()
scratch = Path(sys.argv[3])
start, end = "class _ReleaseGateChecks:", "class _ConcurrencyChecks:"
new_class = new_text[new_text.index(start):new_text.index(end)]
hybrid = old_text[:old_text.index(start)] + SHIM + new_class + old_text[old_text.index(end):]
scratch.mkdir(parents=True, exist_ok=True)
(scratch / "hybrid_shim.py").write_text(hybrid)
run = subprocess.run([sys.executable, "-B", str(scratch / "hybrid_shim.py"), "--self-test"],
                     capture_output=True, text=True, timeout=900)
lines = run.stderr.splitlines()
names = sorted({line.split()[1] for line in lines if line.startswith(("FAIL: ", "ERROR: "))})
print(f"hybrid self-test rc={run.returncode}")
for name in names:
    kinds = sorted({line.split()[0].rstrip(":") for line in lines
                    if line.startswith(("FAIL: ", "ERROR: ")) and line.split()[1] == name})
    print(f"{'/'.join(kinds)}: {name}")
print(lines[-3] if len(lines) >= 3 else "")
print(lines[-1] if lines else "")

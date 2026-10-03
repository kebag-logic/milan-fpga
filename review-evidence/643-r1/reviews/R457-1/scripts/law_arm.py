#!/usr/bin/env python3
"""R457-1 probe: run ONE arm of tdm8_render_mutants.py through the runner's own
plant/build/run_leg/verdict functions, so the verdict is the campaign's own.

usage: law_arm.py <suite dir> <work dir> clean|a2a <log>

  clean - the unmutated ship elaboration, --law-only, must be 'pass'
  a2a   - the MUTATIONS entry "A2-a removed ...", --law-only, must be 'caught'
          (every one of its 18 named checks failed)

Prints the verdict and exits 0 when the expected verdict was reached.
"""
import sys
import time
from pathlib import Path

suite = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
which = sys.argv[3]
log = Path(sys.argv[4]).resolve()
work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(suite))
import tdm8_render_mutants as m  # noqa: E402

arm = [x for x in m.MUTATIONS if x[0].startswith("A2-a removed")]
assert len(arm) == 1, "the A2-a arm is not in MUTATIONS exactly once"
name, source, edits, leg, mode, breaks = arm[0]
assert mode == "--law-only" and isinstance(breaks, tuple) and len(breaks) == 18

t0 = time.time()
if which == "clean":
    exe = m.build(leg, {}, work / "obj_clean")
    expect, must = "pass", None
else:
    value, why = m.plant(source, edits, work, "a2a")
    assert value is not None, why
    exe = m.build(leg, {m.SOURCES[source][1]: value}, work / "obj_a2a")
    expect, must = "caught", breaks
assert exe is not None, "did not compile"
t1 = time.time()
rc, out = m.run_leg(exe, mode)
t2 = time.time()
log.write_text(out)
answer = m.verdict(rc, out, must)
print(f"arm={which} mode={mode} rc={rc} verdict={answer!r} expect={expect!r} "
      f"build_s={t1 - t0:.1f} run_s={t2 - t1:.1f}")
fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
print(f"[FAIL] lines: {len(fails)}")
for ln in fails:
    print("  " + ln[:200])
sys.exit(0 if answer == expect else 1)

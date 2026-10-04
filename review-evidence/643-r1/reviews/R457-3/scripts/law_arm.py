#!/usr/bin/env python3
"""R457-2 probe: run ONE arm of tdm8_render_mutants.py through the runner's own
plant/build/run_leg/verdict functions, so the verdict is the campaign's own.

usage: law_arm.py <suite dir> <work dir> clean|a2a|sp-low|sp-high <log>

  clean   - the unmutated ship elaboration, --law-only, must be 'pass'
  a2a     - MUTATIONS "A2-a removed ...", --law-only, must be 'caught'
            (every one of its 18 named checks failed)
  sp-low  - MUTATIONS "the render setpoint one event low", --law-only,
            must be 'caught' (all 36 named fill + band checks failed)
  sp-high - MUTATIONS "the render setpoint one event high", likewise

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

prefix = {"a2a": "A2-a removed",
          "sp-low": "the render setpoint one event low",
          "sp-high": "the render setpoint one event high"}
t0 = time.time()
if which == "clean":
    exe = m.build("ship", {}, work / "obj_clean")
    mode, expect, must = "--law-only", "pass", None
else:
    arm = [x for x in m.MUTATIONS if x[0].startswith(prefix[which])]
    assert len(arm) == 1, f"{which} is not in MUTATIONS exactly once"
    name, source, edits, leg, mode, breaks = arm[0]
    want = 18 if which == "a2a" else 36
    assert mode == "--law-only" and isinstance(breaks, tuple) and len(breaks) == want
    value, why = m.plant(source, edits, work, which)
    assert value is not None, why
    exe = m.build(leg, {m.SOURCES[source][1]: value}, work / f"obj_{which}")
    expect, must = "caught", breaks
    print(f"arm name: {name!r}; {len(breaks)} named checks")
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
if must is not None:
    missing = [c for c in must if not any(c in f for f in fails)]
    print(f"named checks not failing: {len(missing)}")
    for c in missing:
        print("  " + c)
sys.exit(0 if answer == expect else 1)

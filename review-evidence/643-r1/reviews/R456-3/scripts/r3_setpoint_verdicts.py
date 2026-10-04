#!/usr/bin/env python3
"""R456-3: apply tdm8_render_mutants.verdict(), the campaign's own judge, to
this round's --law-only probe logs against the targets its MUTATIONS table
names for the setpoint -1/+1 arms and the A2-a arm, and to the clean logs with
no target. Usage: r3_setpoint_verdicts.py SUITE_DIR PROBE_DIR"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
suite, probes = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(suite))
import tdm8_render_mutants as m  # noqa: E402

arms = {x[0]: x for x in m.MUTATIONS}
low = next(x for n, x in arms.items() if "setpoint one event low" in n)
high = next(x for n, x in arms.items() if "setpoint one event high" in n)
a2a = next(x for n, x in arms.items() if n.startswith("A2-a removed"))
cases = [("hp-spm1-law", low), ("c4-spm1-law", low), ("hp-spp1-law", high),
         ("c4-spp1-law", high), ("hp-a2a-law", a2a), ("c4-a2a-law", a2a),
         ("hp-clean-law", None), ("c4-clean-law", None)]
ok = True
for log, arm in cases:
    text = (probes / f"{log}.log").read_text(errors="replace")
    rc = int((probes / f"{log}.log.rc").read_text().split()[0].split("=")[1])
    target = arm[5] if arm else None
    got = m.verdict(rc, text, target)
    want = "caught" if arm else "pass"
    ok &= got == want
    what = f"{arm[0]!r} ({arm[4]}, {len(target)} named checks)" if arm else "no target (clean)"
    print(f"{'PASS' if got == want else 'FAIL'} {log}: {what} -> {got}")
sys.exit(0 if ok else 1)

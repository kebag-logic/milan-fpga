#!/usr/bin/env python3
"""Instrument a SCRATCH copy of sw/builder/test_builder.py (argv[1]) so that,
with R413_STOP_AFTER_VERDICT_CONTROLS=1, test_baremetal_profile_contract()
prints each in-gate verdict-pin control's refusal (what, pin, the named pin
text) and returns right after the verdict-pin control loop. Unset, the copy
behaves as the original. Env-guarded edits only."""
import sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text()
a = "                verdict_pin_refused.append(what)\n"
assert s.count(a) == 1
s = s.replace(a, a + "                if __import__('os').environ.get('R413_STOP_AFTER_VERDICT_CONTROLS'):\n"
              "                    _m = str(exc); _i = _m.find(pin)\n"
              "                    print('R413 CONTROL REFUSED:', what, '| pin named:', _m[_i:_i + len(pin) + 160].replace('\\n', ' '))\n")
b = "    #: ... and the store-class mutants measured on the resolver ALONE, so\n"
assert s.count(b) == 1
s = s.replace(b, "    if __import__('os').environ.get('R413_STOP_AFTER_VERDICT_CONTROLS'):\n"
              "        print('R413 PROBE: verdict-pin controls refused', len(verdict_pin_refused), 'of', len(verdict_pin_breaks), '; base kept =', accepted['kept'])\n"
              "        return\n" + b)
p.write_text(s); print("instrumented", p)

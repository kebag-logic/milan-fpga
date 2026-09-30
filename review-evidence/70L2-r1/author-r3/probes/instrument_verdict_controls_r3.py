#!/usr/bin/env python3
"""Instrument a SCRATCH copy of sw/builder/test_builder.py (argv[1]); adapted from R413-2's
instrument_verdict_controls.py to the round-3 loop, whose second field is a tuple of pins.

With A457_STOP_AFTER_VERDICT_CONTROLS=1, test_baremetal_profile_contract() prints each in-gate
verdict-pin control's refusal (what, and the text after each pin it must name) and returns right
after the verdict-pin control loop. Unset, the copy behaves as the original. Env-guarded edits only.
"""
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text()
after_refusal = "                verdict_pin_refused.append(what)\n"
assert text.count(after_refusal) == 1
text = text.replace(after_refusal, after_refusal +
                    "                if __import__('os').environ.get('A457_STOP_AFTER_VERDICT_CONTROLS'):\n"
                    "                    _m = str(exc)\n"
                    "                    print('A457 CONTROL REFUSED:', what)\n"
                    "                    for _p in pins:\n"
                    "                        _i = _m.find(_p)\n"
                    "                        print('    names:', _m[_i:_i + len(_p) + 200].replace('\\n', ' '))\n")
before_store_class = "    #: ... and the store-class mutants measured on the resolver ALONE, so\n"
assert text.count(before_store_class) == 1
text = text.replace(before_store_class,
                    "    if __import__('os').environ.get('A457_STOP_AFTER_VERDICT_CONTROLS'):\n"
                    "        print('A457 PROBE: verdict-pin controls refused', len(verdict_pin_refused), 'of',\n"
                    "              len(verdict_pin_breaks), '; base kept =', accepted['kept'],\n"
                    "              '; base references =', accepted['verdict_references'])\n"
                    "        return\n" + before_store_class)
path.write_text(text)
print("instrumented", path)

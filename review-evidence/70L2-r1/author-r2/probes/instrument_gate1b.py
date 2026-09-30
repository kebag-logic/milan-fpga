#!/usr/bin/env python3
"""Instrument a SCRATCH copy of sw/builder/test_builder.py for gate-1b probes.

usage: instrument_gate1b.py <tree>

Two environment-guarded early returns; with A455_STOP unset the copy behaves
as the original:
  A455_STOP=baseline  return right after the shipping firmware's
                      assert_boot_contract() (every source rule plus the
                      resolver), printing the kept set
  A455_STOP=pins      return right after the verdict-pin controls, printing
                      each control's refusal
A455_FORCE_FORGET=1 makes aem_verdict_pins() report a broken pin, which is
the forget-on-call rule, so a probe can show what the kept slot alone decides.
"""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "sw/builder/test_builder.py"
text = path.read_text()

baseline = ("    baseline_census_verdict = assert_boot_contract(\n"
            "        firmware_source, docs_source, csr_source)\n")
assert text.count(baseline) == 1
text = text.replace(baseline, baseline + (
    "    if os.environ.get('A455_STOP') == 'baseline':\n"
    "        print('A455 PROBE: shipping-firmware gate 1b ACCEPTED; ran=',\n"
    "              baseline_census_verdict.get('ran'), 'kept=',\n"
    "              (baseline_census_verdict.get('resolved') or {}).get('kept'),\n"
    "              flush=True)\n"
    "        return\n"), 1)

pins = "    #: ... and the store-class mutants measured on the resolver ALONE, so\n"
assert text.count(pins) == 1
text = text.replace(pins, (
    "    if os.environ.get('A455_STOP') == 'pins':\n"
    "        print('A455 PROBE: verdict-pin controls refused',\n"
    "              f'{len(verdict_pin_refused)}/{len(verdict_pin_breaks)}:',\n"
    "              verdict_pin_refused, flush=True)\n"
    "        return\n") + pins, 1)

refused = "                verdict_pin_refused.append(what)\n"
assert text.count(refused) == 1
text = text.replace(refused, (
    "                print('A455 PROBE: refused', repr(what), '::',\n"
    "                      str(exc)[str(exc).find(\"aem_loaded's slot\"):],\n"
    "                      flush=True)\n") + refused, 1)

forget = "        broken = []\n        verdict = Rv32Where(\"sym\", \"aem_loaded\")\n"
assert text.count(forget) == 1
text = text.replace(forget, forget.replace(
    "broken = []",
    "broken = (['A455 forced forget-on-call']\n"
    "                  if os.environ.get('A455_FORCE_FORGET') else [])"), 1)

path.write_text(text)
print("instrumented", path)

#!/usr/bin/env python3
"""Instrument a SCRATCH tree's gate 1b to report the shipping firmware's
resolved boot verdict and stop right after it (probe instrument only).

usage: early_stop.py <tree>
After `baseline_census_verdict = assert_boot_contract(firmware_source, ...)`
it prints: the kept set, the census-compiled assembly lines that store to
aem_loaded (with their function), and whether the SAME assembly is refused
under the forget-on-call rule (no source handed in); then exits 0."""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "sw/builder/test_builder.py"
text = path.read_text()
anchor = ("    baseline_census_verdict = assert_boot_contract(\n"
          "        firmware_source, docs_source, csr_source)\n")
assert text.count(anchor) == 1
probe = anchor + '''    if os.environ.get("R412_EARLY"):
        _r = baseline_census_verdict.get("resolved") or {}
        print("R412 shipping-firmware gate-1b verdict ran=%s kept=%s" % (baseline_census_verdict.get("ran"), _r.get("kept")), flush=True)
        _asm = census_take(firmware_source, "R412 probe")["text"]
        Path(os.environ["R412_ASM_OUT"]).write_text(_asm)
        _fn = None
        for _line in _asm.splitlines():
            _m = re.match(r"^([A-Za-z_][\\w.$]*):", _line)
            if _m and not _m.group(1).startswith("."):
                _fn = _m.group(1)
            if "aem_loaded" in _line and re.search(r"\\b(sw|sb|sh|lw|lui|addi)\\b", _line):
                print("R412 asm [%s] %s" % (_fn, _line.strip()), flush=True)
        try:
            assert_resolved_boot_flow(_asm, CsrModel(firmware_source, blanked_sv(csr_source)), "R412 forget-on-call")
        except NameError as _exc:
            print("R412 forget-on-call probe not run:", _exc, flush=True)
        except AssertionError as _exc:
            print("R412 forget-on-call REFUSED:", str(_exc)[:600], flush=True)
        else:
            print("R412 forget-on-call ACCEPTED", flush=True)
        raise SystemExit(0)
'''
path.write_text(text.replace(anchor, probe, 1))
print("instrumented", path)

#!/usr/bin/env python3
"""Instrument a SCRATCH tree's gate 1b (round 3) to report the shipping
firmware's resolved boot verdict and stop right after it (probe only).

usage: early_stop3.py <tree>

After `baseline_census_verdict = assert_boot_contract(firmware_source, ...)`
(reached only when the planted firmware is ACCEPTED), it prints the kept set,
the verdict's image references and pins read by the gate's own
verdict_image_take()/verdict_image_pins(), and whether the same assembly is
refused under the forget-on-call rule; then exits 0.  A refused plant never
reaches the anchor: the gate's AssertionError is printed by run_gate1b.py."""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "sw/builder/test_builder.py"
text = path.read_text()
anchor = ("    baseline_census_verdict = assert_boot_contract(\n"
          "        firmware_source, docs_source, csr_source)\n")
assert text.count(anchor) == 1
probe = anchor + '''    if os.environ.get("R412_EARLY"):
        _r = baseline_census_verdict.get("resolved") or {}
        print("R412 gate-1b verdict ran=%s kept=%s" % (baseline_census_verdict.get("ran"), _r.get("kept")), flush=True)
        _img = verdict_image_take(firmware_source, "R412 probe")
        _v = [s for s in _img["symbols"] if s["name"] == "aem_loaded" and s["defined"]]
        print("R412 image aem_loaded", [(hex(s["value"]), s["size"], s["local"]) for s in _v], flush=True)
        if len(_v) == 1:
            _lo, _hi = _v[0]["value"], _v[0]["value"] + _v[0]["size"]
            for _ref in rv32_image_references(_img, _lo, _hi):
                print("R412 image reference", _ref[0], hex(_ref[1]), _ref[2], "|", _ref[3], flush=True)
            _syms = sorted((s["value"], s["size"], s["name"]) for s in _img["symbols"]
                           if s["defined"] and _lo - 16 <= s["value"] < _hi + 16 and s["kind"] == ELF_STT_OBJECT)
            print("R412 objects within 16 bytes of the verdict:", [(hex(v), n, z) for v, n, z in _syms], flush=True)
            _near = [(hex(site), rv32_image_where(_img, site), RV32_RELOCATION_NAMES.get(kind, kind), hex(tgt))
                     for site, kind, tgt in _img["relocations"]
                     if tgt is not None and _lo - 8 <= tgt < _hi + 8 and not _lo <= tgt < _hi
                     and "nvm_boot" in rv32_image_where(_img, site)]
            print("R412 nvm_boot() relocations within 8 bytes of the verdict but not on it:", _near, flush=True)
        _asm = census_take(firmware_source, "R412 probe")["text"]
        try:
            assert_resolved_boot_flow(_asm, CsrModel(firmware_source, blanked_sv(csr_source)), "R412 forget-on-call")
        except AssertionError as _exc:
            print("R412 forget-on-call REFUSED:", str(_exc)[:300], flush=True)
        else:
            print("R412 forget-on-call ACCEPTED", flush=True)
        raise SystemExit(0)
'''
path.write_text(text.replace(anchor, probe, 1))
print("instrumented", path)

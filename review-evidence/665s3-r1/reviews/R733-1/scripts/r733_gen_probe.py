#!/usr/bin/env python3
"""Reviewer probe: plat_trace.py (the CSR initialisation against milan_baremetal.c) must catch a defect in the
policy generator itself, ctrl_plat_gen.py, not only in ctrl_plat_csr.c.

usage: r733_gen_probe.py COPY WORKDIR
COPY is a disposable `git archive` of the head (with the submodules' sources); each plant edits COPY's generator
in place, runs the copy's own trace arm, and restores the generator's bytes.
"""
import subprocess
import sys
from pathlib import Path

copy = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
gen = copy / "sw/firmware/ctrl/plat/ctrl_plat_gen.py"
original = gen.read_bytes()
PLANTS = (
    ("two policy fields swapped", '("mac_ctrl_set", "MILAN_MAC_CTRL_SET"), ("tcam_ctrl", "MILAN_TCAM_CTRL_BOOT")',
     '("mac_ctrl_set", "MILAN_TCAM_CTRL_BOOT"), ("tcam_ctrl", "MILAN_MAC_CTRL_SET")'),
    ("the VID from the AAF word", '("sr_vid", "MILAN_SR_VID")', '("sr_vid", "MILAN_AAF_CTRL_BOOT")'),
    ("the CRF word dropped to zero", 'f"\\t.{field} = 0x{words[name]:08X}u"',
     'f"\\t.{field} = 0x{(0 if name == \'MILAN_CRF_TX_CTRL_BOOT\' else words[name]):08X}u"'),
)
CODE = ("import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[2]);"
        "import plat_trace; o = plat_trace.arm(plat_trace.CTRL, Path(sys.argv[3])); print(o.log); "
        "raise SystemExit(o.rc)")
escaped = 0
try:
    for k, (name, old, new) in enumerate(PLANTS):
        text = original.decode()
        assert text.count(old) == 1, (name, text.count(old))
        gen.write_text(text.replace(old, new))
        r = subprocess.run([sys.executable, "-B", "-c", CODE, str(copy / "sw/firmware/ctrl/test"),
                            str(copy / "sw/firmware/gtest"), str(work / f"plant{k}")],
                           capture_output=True, text=True, cwd=copy)
        differs = [ln.strip() for ln in r.stdout.splitlines() if "DIFFERENT FROM" in ln]
        caught = r.returncode == 1 and bool(differs)
        escaped += not caught
        print(f"GENPLANT {name}: {'caught' if caught else 'ESCAPED'} (rc {r.returncode}; {len(differs)} config(s) "
              f"differ: {differs[:2]})")
        if r.returncode not in (0, 1):
            print(r.stdout[-1500:], r.stderr[-1500:])
finally:
    gen.write_bytes(original)
print(f"r733 generator probe: {len(PLANTS) - escaped} of {len(PLANTS)} caught")
raise SystemExit(1 if escaped else 0)

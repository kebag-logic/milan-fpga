#!/usr/bin/env python3
"""Reviewer probe: replay the head gate-1b ROM assertions under a wrong-clock ROM.

Usage: 36_rom_clock_replay.py <pristine-head> <work-copy>
Mutant: the builder generates gptp_ucode.hex with --clk-hz = sys_clk_hz
(100 MHz on the AX shapes) instead of the Milan clock. The assertions replayed
are the ones test_builder.py keeps on the ROM at the head (sw/builder/
test_builder.py:2998-3006 and :17106-17118): the ROM exists, has 1024 words,
and changes with the station MAC and priority1. The probe also reports whether
the ROM bytes differ from the correct head ROM (i.e. the defect is observable).
"""
import copy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HEAD, WORK = Path(sys.argv[1]), Path(sys.argv[2])
REL = "sw/builder/endstation_builder.py"
OLD = '"--clk-hz", str(cfg["constraints"]["milan_clk_hz"])],'
NEW = '"--clk-hz", str(cfg["constraints"]["sys_clk_hz"])],'
CFG = "configs/endstation_ax7101_1x1_tdm8.yaml"
PROBE = r'''
import sys; from pathlib import Path
sys.path.insert(0, "sw/builder"); import endstation_builder as eb
r = eb.build(Path(sys.argv[1]), sys.argv[2], write_fragment=False)
sys.stdout.buffer.write(Path(r["paths"]["gptp_ucode"]).read_bytes())
'''


def rom(tree, cfg_path, out):
    return subprocess.run([sys.executable, "-c", PROBE, str(cfg_path), str(out)], cwd=tree,
                          capture_output=True, check=True, timeout=300).stdout


def variants(tmp):
    raw = yaml.safe_load((HEAD / CFG).read_text())
    out = {"base": raw}
    mac = copy.deepcopy(raw); mac["platform"]["mac_address"] = "02:00:00:00:00:03"; out["mac"] = mac
    p1 = copy.deepcopy(raw); p1["gptp"]["priority1"] = 247; out["priority1"] = p1
    paths = {}
    for k, v in out.items():
        paths[k] = tmp / f"{k}.yaml"; paths[k].write_text(yaml.safe_dump(v))
    return paths


shutil.copyfile(HEAD / REL, WORK / REL)
with tempfile.TemporaryDirectory(dir=WORK.parent) as td:
    tmp = Path(td); paths = variants(tmp)
    good = rom(HEAD, paths["base"], tmp / "good")
    text = (WORK / REL).read_text(); assert text.count(OLD) == 1
    (WORK / REL).write_text(text.replace(OLD, NEW))
    try:
        bad = {k: rom(WORK, p, tmp / f"bad-{k}") for k, p in paths.items()}
    finally:
        shutil.copyfile(HEAD / REL, WORK / REL)
    words = len(bad["base"].splitlines())
    print(f"mutant ROM words: {words} (gate requires 1024): {'PASS' if words == 1024 else 'FAIL'}")
    print(f"mutant ROM changes with MAC: {'PASS' if bad['mac'] != bad['base'] else 'FAIL'}")
    print(f"mutant ROM changes with priority1: {'PASS' if bad['priority1'] != bad['base'] else 'FAIL'}")
    print(f"mutant ROM differs from the correct 50 MHz ROM: {bad['base'] != good} "
          f"({sum(a != b for a, b in zip(bad['base'].splitlines(), good.splitlines()))} of 1024 words differ)")
print(f"work builder restored: {(WORK / REL).read_bytes() == (HEAD / REL).read_bytes()}")

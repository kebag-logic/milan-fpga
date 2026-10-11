#!/usr/bin/env python3
"""ROM-only size drifts: in memory, NOP the first BUILD_FIELD (or APPEND) a path
from each entry can execute, as the gate's own self-test does for E_GSTRI, and
record whether the AECP command gate names it.
Usage: python3 -I rom_size_probe.py HEAD_TREE"""
import copy, importlib.util, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("gate", root / "scripts/check_aecp_commands.py")
g = importlib.util.module_from_spec(spec); sys.dont_write_bytecode = True; spec.loader.exec_module(g)
base = g.load(root)
assert g.check(base) == [], "unplanted head must pass"
probes = [("READ_DESCRIPTOR", "RDESC"), ("GET_AVB_INFO", "GAVB"), ("GET_AS_PATH", "GASP"),
          ("GET_AUDIO_MAP", "GAMAP"), ("ADD_AUDIO_MAPPINGS", "AMADD"),
          ("REGISTER_UNSOLICITED_NOTIFICATION", "REGUN"), ("GET_STREAM_INFO", "GSTRI"),
          ("GET_COUNTERS", "GCTRS")]
for name, entry in probes:
    for op in ("BUILD_FLD", "APPEND"):
        inp = g.Inputs(copy.deepcopy(base.table), dict(base.texts), copy.deepcopy(base.ucode))
        try:
            at = g.rom_op(inp, entry, op)
        except g.GateError:
            print(f"{name:36} E_{entry:8} {op:9} none reachable"); continue
        inp.ucode.rom[at] = 0
        got = g.check(inp)
        hit = [l.strip() for l in got if name in l]
        print(f"{name:36} E_{entry:8} {op:9} word {at:4} NOPed: gate "
              f"{'FAILS: ' + hit[0][:120] if hit else ('PASSES' if not got else 'other: ' + got[0].strip()[:100])}")

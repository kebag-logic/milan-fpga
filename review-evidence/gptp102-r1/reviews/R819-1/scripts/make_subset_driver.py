#!/usr/bin/env python3
"""Write tb/verilator/engine/<out> in a disposable tree: a copy of that
tree's mutants.py whose MUTATIONS list is replaced, just before the main
guard, by a fixed subset of real mutants plus planted fault entries that
reach every verdict branch of run_mutant.

usage: make_subset_driver.py <tree> <out-name> [--mutate-order|--drop-last-line]

--mutate-order and --drop-last-line also plant a disposable defect in the
copy's own scheduler or printer, to measure the equivalence test's power.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
out = sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else ""
src = (tree / "tb/verilator/engine/mutants.py").read_text()

SUBSET = r'''
# ---- reviewer probe: subset + planted faults (disposable copy) ----
_BY_NAME = {m[0]: m for m in MUTATIONS}
_ENG = "top/KL_gptp_engine.sv"
_HEADER = "//  Project     : 802.1AS gPTP protocol processor (time-sync plane)"
MUTATIONS = [
    _BY_NAME["the watch ignores the received interval"],          # RTL, #100, slow
    ("probe pattern missing", _ENG, "NO_SUCH_TEXT_R819_PROBE", "x", "probe"),
    ("probe survivor", _ENG, _HEADER, _HEADER + " probe", "probe survives"),
    ("probe build failure", _ENG, "\nendmodule", "\nendmodule_broken", "probe"),
    ("probe generator refuses", GENERATOR, 'if __name__ == "__main__":',
     'raise SystemExit(3)\nif __name__ == "__main__":', "probe"),
    (_BY_NAME["lost t1 fabricates a time and a companion"][0] + " probe",
     GENERATOR, *_BY_NAME["lost t1 fabricates a time and a companion"][2:4],
     "#100 a check nobody prints"),                             # named missed
    _BY_NAME["slew level tied low"],                              # RTL, slew:
    _BY_NAME["lost t1 fabricates a time and a companion"],        # generator
    _BY_NAME["the Follow_Up TLV is sent zero"],                   # generator #100
]
'''
GUARD = '\nif __name__ == "__main__":'
assert src.count(GUARD) == 1
src = src.replace(GUARD, SUBSET + GUARD)
if mode == "--mutate-order":
    old = "        for future in futures:\n            yield future.result()\n"
    assert src.count(old) == 1
    src = src.replace(old, "        from concurrent.futures import as_completed\n"
                           "        for future in as_completed(futures):\n"
                           "            yield future.result()\n")
elif mode == "--drop-last-line":
    old = "                for line in lines:\n                    print(line)\n"
    assert src.count(old) == 1
    src = src.replace(old, "                for line in lines[:-1]:\n"
                           "                    print(line)\n")
elif mode:
    sys.exit(f"unknown mode {mode}")
(tree / "tb/verilator/engine" / out).write_text(src)
print("wrote", tree / "tb/verilator/engine" / out, mode or "(subset only)")

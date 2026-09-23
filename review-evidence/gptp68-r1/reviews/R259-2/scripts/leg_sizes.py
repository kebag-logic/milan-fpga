#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Word count and base of every shared leg at base, reviewed and head, from
each revision's own generator (engine suite arguments)."""
import importlib.util
import subprocess
import sys

clone, revs = sys.argv[1], sys.argv[2:]
rows = {}
for rev in revs:
    src = subprocess.run(["git", "-C", clone, "show",
                          f"{rev}:hdl/ucode/gen_gptp_ucode.py"],
                         capture_output=True, text=True, check=True).stdout
    spec = importlib.util.spec_from_loader(f"g{rev[:7]}", loader=None)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(src, "gen", "exec"), mod.__dict__)
    mod.set_servo_gains(2_000_000)
    mod.RUNTIME["cease_ms"] = 3000
    rom, used = mod.build(0x02A1B2C3D4E5)
    for name, fn in mod.LEG_FNS:
        rows.setdefault(name, {})[rev[:7]] = (len(fn(mod.LB[name]).words()),
                                             mod.LB[name])
    rows.setdefault("(real words)", {})[rev[:7]] = (used, "")
keys = [r[:7] for r in revs]
print("leg".ljust(14) + "".join(f"{k:>16}" for k in keys))
for name, d in rows.items():
    cells = "".join(f"{str(d[k][0]) + '@' + str(d[k][1]):>16}" for k in keys)
    flag = "  changed" if len({d[k] for k in keys}) > 1 else ""
    print(name.ljust(14) + cells + flag)

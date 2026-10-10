#!/usr/bin/env python3
"""The two-argument -U form, derived: ctrl_configs.derive() with a planted Python builder writing ("-U", NAME)
and a planted Makefile writing "-U NAME", against the one-argument controls. Usage: derive_u.py <checkout>"""
import sys
from pathlib import Path
co = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(co / "sw/firmware/ctrl/test")); sys.path.insert(0, str(co / "sw/firmware/gtest"))
import ctrl_configs as c
head = '"""A builder of the firmware that nobody lists."""\nfrom ctrl_build import Tree\n'
mk = "# A builder of sw/firmware/ctrl that nobody lists.\n"
cases = {
    "python two-argument -U": ({c.HERE / "r3u_arms.py": head + 'F = ["-U", "CTRL_R3_UPY"]\n'}, "CTRL_R3_UPY", "-UCTRL_R3_UPY"),
    "makefile two-word -U": ({c.HERE / "r3u.mk": mk + "x:\n\tcc -U CTRL_R3_UMK -c x.c\n"}, "CTRL_R3_UMK", "-UCTRL_R3_UMK"),
    "python one-argument -U (control)": ({c.HERE / "r3u_arms.py": head + 'F = ["-UCTRL_R3_UONE"]\n'}, "CTRL_R3_UONE", "-UCTRL_R3_UONE"),
    "python two-argument -U then -D of NDEBUG-like pair": ({c.HERE / "r3u_arms.py": head + 'F = ("-U", "CTRL_R3_UD", "-D", "CTRL_R3_UD=2")\n'}, "CTRL_R3_UD", "-UCTRL_R3_UD"),
}
for name, (planted, macro, flag) in cases.items():
    modes = c.modes(planted)
    got = modes.get(macro)
    print(f"{'DERIVED' if got and flag in got else 'MISSED'} {name}: {macro} -> {got}")

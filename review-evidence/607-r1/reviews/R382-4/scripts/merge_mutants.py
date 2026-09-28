#!/usr/bin/env python3
"""Disposable mutants of the #395/#607 merge resolution; each restored from git.

Usage: merge_mutants.py <clone> <pins work root> <pins_env.sh> <scratch dir>
Each mutant runs: test_timing_grade.py <python> (the #395 hook test) and one
real shipping elaboration (ax7101_1x1_tdm8 e1) graded by the #607 shipping probe
and by compose_tcl_check.py.
"""
import subprocess, sys, shutil
from pathlib import Path
clone, work, env, scratch = map(Path, sys.argv[1:5])
compose = Path(__file__).with_name("compose_tcl_check.py")
PLAT = "sw/litex/platforms/alinx_ax7101.py"
CC = "sw/litex/clock_constraints.py"
SWAP = ('        if toolchain == "vivado":\n'
        '            # Replace before adding any hooks; state on the old toolchain\n'
        '            # would be discarded. Keep all hook configuration below this.\n'
        '            self.toolchain = BoundedEthVivadoToolchain()\n')
LOOP = '        for command in configure_commands():\n'
BITS_END = '            "set_property CONFIG_VOLTAGE 3.3 [current_design]",\n        ]\n'
MID = '        self.toolchain.bitstream_commands = [\n'
def mutate(path, old, new):
    p = clone / path; t = p.read_text()
    assert t.count(old) == 1, (path, old[:40]); p.write_text(t.replace(old, new))
MUTANTS = {
    "control": [],
    "MA swap after all #395 hooks": [(PLAT, SWAP, ""), (PLAT, BITS_END, BITS_END + SWAP)],
    "MB swap between pre-placement and bitstream hooks": [(PLAT, SWAP, ""), (PLAT, MID, SWAP + MID)],
    "MC swap deleted": [(PLAT, SWAP, "")],
    "MD 607 hook overwrites bitstream_commands": [(CC, "    toolchain.bitstream_commands.append(\n        \"report_clock_interaction",
                                                   "    toolchain.bitstream_commands = []\n    toolchain.bitstream_commands.append(\n        \"report_clock_interaction")],
    "ME 607 hook overwrites pre_placement_commands": [(CC, "    toolchain.bitstream_commands.append(\n        \"report_clock_interaction",
                                                    "    from litex.build.generic_toolchain import GenericToolchain  # noqa\n    toolchain.pre_placement_commands.__init__()\n    toolchain.bitstream_commands.append(\n        \"report_clock_interaction")],
}
def run(cmd, cwd):
    r = subprocess.run(["sh", str(env), str(cwd), str(work), *cmd], capture_output=True, text=True, timeout=900)
    return r.returncode, (r.stdout + r.stderr)
py = str(work / "pins-venv/bin/python3")
for name, edits in MUTANTS.items():
    for path, old, new in edits:
        mutate(path, old, new)
    try:
        g_rc, g_out = run(["python3", "-B", "sw/builder/test_timing_grade.py", py], clone)
        out = scratch / ("mut-" + name.split()[0])
        shutil.rmtree(out, ignore_errors=True)
        s_rc, s_out = run(["env", "PYTHONHASHSEED=0", "python3", "-B", str(clone / "sw/builder/test_shipping_clock_constraints.py"),
                           "--config", "ax7101_1x1_tdm8", "--port", "e1", "--output-dir", str(out)], clone / "sw/litex")
        c_rc = subprocess.run([sys.executable, str(compose), str(out / "gateware")], capture_output=True, text=True).returncode \
            if (out / "gateware/alinx_ax7101.tcl").exists() else "no-tcl"
        tail = lambda s: [l for l in s.splitlines() if "Error" in l or "assert" in l.lower() or "PASS" in l][-1:]
        print(f"{name}: timing_grade rc={g_rc} shipping_probe rc={s_rc} composition rc={c_rc} "
              f"| grade: {tail(g_out)} | ship: {tail(s_out)}"[:600])
    finally:
        subprocess.run(["git", "-C", str(clone), "checkout", "--", PLAT, CC], check=True)

#!/usr/bin/env python3
"""[R383] Round-3 mutation probes for the #607 committed tests at a9f5e34f.

Round-2 mutate2.py unchanged in its 27 mutants, plus G1-G6 against the new
probe guard/override in sw/builder/test_shipping_clock_constraints.py. Each
mutant is a disposable copy of an extracted head tree with one or more textual
edits (each anchor must match exactly once); the committed
sw/builder/test_clock_constraints.py (which also runs the shipping AX7101
elaborations) is run with the given interpreter and the caller's environment.
KILLED = the test failed. Up to 8 mutants run in parallel.
Usage: mutate2.py <extracted head tree> <scratch dir> <python with litex>
                  [<test file relative to tree> [<comma-separated mutant IDs>]]
Run it under pins_env.sh to grade in the pins-only environment.
"""
from concurrent.futures import ThreadPoolExecutor
import os, shutil, subprocess, sys
from pathlib import Path

base, scratch, python = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
TEST = sys.argv[4] if len(sys.argv) > 4 else "sw/builder/test_clock_constraints.py"
ONLY = set(sys.argv[5].split(",")) if len(sys.argv) > 5 else None
SHIP = "sw/builder/test_shipping_clock_constraints.py"
OVERRIDE = ('''        def _generate_includes(self, with_bios: bool = True) -> None:
            """Write the SoC headers, omitting only the firmware make inputs."""
            # LiteX resolves the picolibc and compiler-rt data packages for the
            # BIOS make variables before it writes the gateware. No firmware is
            # built here, and the gateware Tcl/XDC do not read those files.
            includes.append(with_bios)
            super()._generate_includes(with_bios=False)

''')
SOC, CC, TCL, PLAT = ("sw/litex/milan_soc.py", "sw/litex/clock_constraints.py",
                      "sw/litex/clock_constraints.tcl", "sw/litex/platforms/alinx_ax7101.py")
GUARD = '                if board == "ax7101":\n                    add_eth_constraints('
CALL = ('                if board == "ax7101":\n'
        '                    add_eth_constraints(platform, self.crg,\n'
        '                                        platform.lookup_request("eth_clocks", eth_phy_index).rx)\n')
MUTANTS = [
    # Round-1 hook-wiring mutants named in the round-2 assignment.
    ("M07 hook gated to arty", SOC, GUARD, GUARD.replace('"ax7101"', '"arty"')),
    ("M07b hook gated to a nonexistent board", SOC, GUARD, GUARD.replace('"ax7101"', '"ax7101-disabled"')),
    ("M16 hook unreachable when a MAC exists", SOC, GUARD,
     GUARD.replace('"ax7101":', '"ax7101" and not with_mac:')),
    ("M06d hook call deleted inside the guard", SOC, CALL,
     '                if board == "ax7101":\n                    pass\n'),
    ("M06 hook call and guard deleted", SOC, CALL, ""),
    ("M08 hook passes the other port", SOC, 'platform.lookup_request("eth_clocks", eth_phy_index).rx)',
     'platform.lookup_request("eth_clocks", 1 - eth_phy_index).rx)'),
    # Round-1 constraint/gate mutants, re-run at this head.
    ("M01 retain generic MultiReg mask", CC, "        commands.remove(generic)\n", "        pass\n"),
    ("M02 bound 8 -> 80 ns", TCL, "set_max_delay 8.000 -datapath_only -from $eth -to $clock",
     "set_max_delay 80.000 -datapath_only -from $eth -to $clock"),
    ("M03 eth MultiRegs excluded from wrong class", TCL, "[list $eth_mr $part $part_mr $eth]",
     "[list $eth_mr {} $part_mr $eth]"),
    ("M04 log gate ignores CRITICAL WARNING", CC, 'r"^(?:CRITICAL WARNING|WARNING|ERROR):',
     'r"^(?:WARNING|ERROR):'),
    ("M05 log gate ignores 20-1307", CC, "|Designutils 20-1307", ""),
    ("M09 idelay clock moved into bounded class", SOC,
     "            pll.create_clkout(self.cd_idelay, 200e6, margin=0)\n            self.eth_async_clocks.append(",
     "            pll.create_clkout(self.cd_idelay, 200e6, margin=0)\n            self.eth_bounded_clocks.append("),
    ("M10 log check before build", SOC,
     "    builder.build(run=args.build, **build_kwargs)  # run=False => elaborate + export gateware, no Vivado\n"
     "    if args.build:\n", "    if args.build:\n"),
    ("M11 quasi-static hold 3 -> 0", TCL, "set_multicycle_path 3 -hold -from $cells",
     "set_multicycle_path 0 -hold -from $cells"),
    ("M12 hold false path dropped sys->eth", TCL, "        set_false_path -hold -from $clock -to $eth\n", ""),
    ("M13 async group dropped", TCL, "        set_clock_groups -asynchronous -group $eth -group $other\n",
     "        puts skipped\n"),
    ("M14 asynchronous-input exception dropped", TCL,
     "        if {[llength $inputs]} {set_false_path -from $inputs -to $targets}\n", ""),
    ("M15 ambiguous MultiReg clock accepted", TCL,
     "        if {[llength $clocks] != 1} {\n            error \"CONSTRAINTS: expected one MultiReg clock",
     "        if {0} {\n            error \"CONSTRAINTS: expected one MultiReg clock"),
    # New round-2 mutants against the shipping arm.
    ("M17 bounded flag never set", CC, "    toolchain.bounded_eth = True\n", "    pass\n"),
    ("M18 hook moved to pre-placement", CC, "    toolchain.pre_optimize_commands.add(",
     "    toolchain.pre_placement_commands.add("),
    ("M19 platform keeps stock toolchain", PLAT, "            self.toolchain = BoundedEthVivadoToolchain()\n",
     "            pass\n"),
    ("M20 Milan clock dropped from bounded pair", CC, "    clocks = crg.eth_bounded_clocks\n",
     "    clocks = crg.eth_bounded_clocks[:1]\n"),
    ("M21 hook bounds sys against itself instead of eth", CC, '    signals = {"eth": eth_rx}\n',
     '    signals = {"eth": crg.eth_bounded_clocks[0]}\n'),
    # New round-2 mutants against the 12-5201 refusal and quarantine.
    ("M22 log gate ignores 12-5201", CC, r"12-(?:4739|5201)", r"12-(?:4739)"),
    ("M23 quarantine rename removed", CC, "            bitstream.replace(rejected)\n", "            pass\n"),
    ("M24 quarantine copies instead of renaming", CC, "            bitstream.replace(rejected)\n",
     "            __import__('shutil').copyfile(bitstream, rejected)\n"),
    ("M25 unreadable log does not quarantine", CC, "    except (OSError, RuntimeError):\n",
     "    except RuntimeError:\n"),
    ("M26 quarantine suffix still ends in .bit", CC, 'bitstream.with_suffix(".bit.rejected")',
     'bitstream.with_suffix(".rejected.bit")'),
    # Round-3 mutants against the pins-only probe (guard + include override).
    ("G1 include override removed", SHIP,
     [(OVERRIDE, "")]),
    ("G2 override forwards with_bios", SHIP,
     [("super()._generate_includes(with_bios=False)", "super()._generate_includes(with_bios=with_bios)")]),
    ("G3 import guard not installed", SHIP,
     [("    sys.meta_path.insert(0, FirmwareDataRefused())\n", "")]),
    ("G4 guard, override and include assertion removed (round-2 shape)", SHIP,
     [("    sys.meta_path.insert(0, FirmwareDataRefused())\n", ""), (OVERRIDE, ""),
      ('            assert includes == [True], f"builder bypassed the probed include step: {includes}"\n', "")]),
    ("G4a override and include assertion removed, guard kept", SHIP,
     [(OVERRIDE, ""),
      ('            assert includes == [True], f"builder bypassed the probed include step: {includes}"\n', "")]),
    ("G5 guard defers every module", SHIP,
     [('            raise ImportError(f"{name}: sw/litex/litex_pins.txt installs no firmware data package")\n',
       "            return None\n")]),
    ("G6 override skips the include step entirely", SHIP,
     [("            super()._generate_includes(with_bios=False)\n", "            pass\n")]),
]


def run(tree):
    r = subprocess.run([python, "-B", TEST], cwd=tree,
                       capture_output=True, text=True, timeout=2700,
                       env=dict(os.environ, PYTHONHASHSEED="0"))
    lines = [l for l in (r.stdout + r.stderr).strip().splitlines() if l.strip()]
    why = next((l.strip() for l in reversed(lines) if "Error" in l or "assert" in l.lower()
                or "not installed!" in l), lines[-1] if lines else "")
    return r.returncode, why[:220]


def one(m):
    label, rel, *edit = m
    edits = edit[0] if len(edit) == 1 else [tuple(edit)]
    tree = scratch / label.split()[0]
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(base, tree, symlinks=True)
    path = tree / rel
    text = path.read_text()
    for old, new in edits:
        if text.count(old) != 1:
            shutil.rmtree(tree)
            return f"{label}: NOT-APPLIED (anchor count {text.count(old)})"
        text = text.replace(old, new)
    path.write_text(text)
    rc, why = run(tree)
    shutil.rmtree(tree)
    return f"{label}: {'KILLED' if rc else 'SURVIVED'} rc={rc} {why}"


rc, why = run(base)
print(f"BASELINE rc={rc} {why}", flush=True)
if rc:
    sys.exit("baseline must pass before mutants are graded")
with ThreadPoolExecutor(max_workers=8) as pool:
    for line in pool.map(one, [m for m in MUTANTS if ONLY is None or m[0].split()[0] in ONLY]):
        print(line, flush=True)

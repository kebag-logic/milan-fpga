#!/usr/bin/env python3
"""[R383] mutation probes for the #607 committed tests.

Each mutant is a disposable copy of an extracted head tree with one textual
edit; the committed sw/builder/test_clock_constraints.py is then run with the
build interpreter. KILLED = the test failed (it detects the fault).
Usage: mutate.py <extracted head tree> <scratch dir> <python with litex>
"""
import shutil, subprocess, sys
from pathlib import Path

base, scratch, python = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]

MUTANTS = [
    ("M1 retain generic MultiReg mask", "sw/litex/clock_constraints.py",
     "        commands.remove(generic)\n", "        pass\n"),
    ("M2 bound 8 -> 80 ns", "sw/litex/clock_constraints.tcl",
     "set_max_delay 8.000 -datapath_only -from $eth -to $clock",
     "set_max_delay 80.000 -datapath_only -from $eth -to $clock"),
    ("M3 eth MultiRegs excluded from wrong class", "sw/litex/clock_constraints.tcl",
     "[list $eth_mr $part $part_mr $eth]", "[list $eth_mr {} $part_mr $eth]"),
    ("M4 log gate ignores CRITICAL WARNING", "sw/litex/clock_constraints.py",
     'r"^(?:CRITICAL WARNING|WARNING|ERROR):', 'r"^(?:WARNING|ERROR):'),
    ("M5 log gate ignores 20-1307", "sw/litex/clock_constraints.py",
     "|Designutils 20-1307", ""),
    ("M6 eth hook call deleted", "sw/litex/milan_soc.py",
     "                if board == \"ax7101\":\n                    add_eth_constraints(platform, self.crg,\n"
     "                                        platform.lookup_request(\"eth_clocks\", eth_phy_index).rx)\n", ""),
    ("M7 eth hook gated to the wrong board", "sw/litex/milan_soc.py",
     "                if board == \"ax7101\":\n                    add_eth_constraints(",
     "                if board == \"arty\":\n                    add_eth_constraints("),
    ("M8 eth hook passes the wrong port", "sw/litex/milan_soc.py",
     "platform.lookup_request(\"eth_clocks\", eth_phy_index).rx)",
     "platform.lookup_request(\"eth_clocks\", 1 - eth_phy_index).rx)"),
    ("M9 idelay clock moved into bounded class", "sw/litex/milan_soc.py",
     "            pll.create_clkout(self.cd_idelay, 200e6, margin=0)\n            self.eth_async_clocks.append(",
     "            pll.create_clkout(self.cd_idelay, 200e6, margin=0)\n            self.eth_bounded_clocks.append("),
    ("M10 log check before build", "sw/litex/milan_soc.py",
     "    builder.build(run=args.build, **build_kwargs)  # run=False => elaborate + export gateware, no Vivado\n"
     "    if args.build:\n",
     "    if args.build:\n"),
    ("M11 quasi-static hold 3 -> 0", "sw/litex/clock_constraints.tcl",
     "set_multicycle_path 3 -hold -from $cells", "set_multicycle_path 0 -hold -from $cells"),
    ("M12 hold false path dropped sys->eth", "sw/litex/clock_constraints.tcl",
     "        set_false_path -hold -from $clock -to $eth\n", ""),
    ("M13 async group dropped", "sw/litex/clock_constraints.tcl",
     "        set_clock_groups -asynchronous -group $eth -group $other\n", "        puts skipped\n"),
    ("M14 asynchronous-input exception dropped", "sw/litex/clock_constraints.tcl",
     "        if {[llength $inputs]} {set_false_path -from $inputs -to $targets}\n", ""),
    ("M15 ambiguous MultiReg clock accepted", "sw/litex/clock_constraints.tcl",
     "        if {[llength $clocks] != 1} {\n            error \"CONSTRAINTS: expected one MultiReg clock",
     "        if {0} {\n            error \"CONSTRAINTS: expected one MultiReg clock"),
]


def run(tree):
    r = subprocess.run([python, "-B", "sw/builder/test_clock_constraints.py"], cwd=tree,
                       capture_output=True, text=True, timeout=600)
    tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
    return r.returncode, tail[0][:200]


rc, tail = run(base)
print(f"BASELINE rc={rc} {tail}")
if rc:
    sys.exit("baseline must pass before mutants are graded")
for label, rel, old, new in MUTANTS:
    tree = scratch / label.split()[0]
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(base, tree, symlinks=True)
    path = tree / rel
    text = path.read_text()
    if text.count(old) != 1:
        print(f"{label}: NOT-APPLIED (anchor count {text.count(old)})")
        continue
    path.write_text(text.replace(old, new))
    rc, tail = run(tree)
    print(f"{label}: {'KILLED' if rc else 'SURVIVED'} rc={rc} {tail}")
    shutil.rmtree(tree)

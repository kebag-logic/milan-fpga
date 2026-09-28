# SPDX-License-Identifier: CERN-OHL-W-2.0
"""#607: generated clock objects, scoped exceptions and rejected implementation logs."""

import argparse
import ast
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "sw/litex"))
from clock_constraints import (  # noqa: E402
    add_eth_constraints, add_quasi_static_constraints,
    check_implementation_log,
)


def test_crg_clock_sources() -> None:
    """The real CRG selects its system/datapath PLL outputs and optional clocks."""
    from milan_soc import _CRG
    from platforms.alinx_ax7101 import Platform

    for dram, milan_hz, tdm_hz, bound_count, other_count in (
            (False, None, None, 1, 1),
            (True, 50_000_000, None, 2, 6),
            (True, 50_000_000, 98_304_000, 2, 7)):
        crg = _CRG(Platform(), 100_000_000, with_dram=dram, with_eth=True,
                   milan_clk_freq=milan_hz, audio_tdm_hz=tdm_hz)
        assert len(crg.eth_bounded_clocks) == bound_count
        assert len(crg.eth_async_clocks) == other_count
        for index, signal in enumerate(crg.eth_bounded_clocks):
            assert signal is crg.pll.clkouts[index].clk
            assert crg.pll.clkouts[index].freq == (100_000_000 if index == 0 else 50_000_000)
            assert all(signal is not other for other in crg.eth_async_clocks)
        for index in range(bound_count, crg.pll.nclkouts):
            assert any(crg.pll.clkouts[index].clk is other for other in crg.eth_async_clocks)
    print("[constraints] actual CRG clock sources and optional DDR/audio domains PASS")


def test_generated_constraints() -> None:
    """Use the real platform and namespace; changing object names changes the hook."""
    from migen import ClockDomain, Module
    from platforms.alinx_ax7101 import Platform

    with tempfile.TemporaryDirectory(prefix="clock-constraints-") as tmp:
        for port, suffix, milan in ((0, "first", True), (1, "renamed", True), (0, "single", False)):
            platform = Platform()
            module = Module()
            module.clock_domains.cd_sys = ClockDomain("sys")
            module.cd_sys.clk.name_override = "system_" + suffix
            module.comb += module.cd_sys.clk.eq(platform.request("clk200").p)
            crg = SimpleNamespace(eth_bounded_clocks=[module.cd_sys.clk], eth_async_clocks=[])
            if milan:
                module.clock_domains.cd_milan = ClockDomain("milan")
                module.cd_milan.clk.name_override = "datapath_" + suffix
                module.comb += module.cd_milan.clk.eq(module.cd_sys.clk)
                crg.eth_bounded_clocks.append(module.cd_milan.clk)
            eth = platform.request("eth_clocks", port).rx
            platform.add_period_constraint(eth, 8)
            add_quasi_static_constraints(platform)
            add_eth_constraints(platform, crg, eth)
            directory = Path(tmp) / suffix
            platform.build(module, build_dir=str(directory), run=False, vivado_max_threads=16)
            tcl = (directory / "top.tcl").read_text()
            xdc = (directory / "top.xdc").read_text()
            assert f"kl_eth_constraints eth_clocks{port}_rx [list system_{suffix}" in tcl
            assert (f"datapath_{suffix}" in tcl) == milan
            assert tcl.index("synth_design") < tcl.index("kl_quasi_static_constraints")
            assert tcl.index("kl_eth_constraints") < tcl.index("opt_design")
            assert "report_clock_interaction -delay_type min_max" in tcl
            assert "mr_ff" not in xdc and "if {" not in xdc
            assert "ars_ff1" in xdc and "set_max_delay 2" in xdc
            assert "crg_clkout" not in tcl + xdc
        # A platform with no bounded Ethernet still has the upstream exception.
        platform = Platform()
        platform.toolchain.platform = platform
        platform.toolchain._build_false_path_constraints()
        assert any("mr_ff" in command for command, _ in platform.constraint_manager.platform_commands)
        # An upstream template change must not silently reintroduce the mask.
        platform.toolchain.bounded_eth = True
        try:
            platform.toolchain._build_false_path_constraints()
        except RuntimeError as exc:
            assert "unsupported LiteX MultiReg" in str(exc)
        else:
            raise AssertionError("duplicate generic exception accepted")
    print("[constraints] generated namespace, optional domain, both ports, hook order and template refusal PASS")


STUB = r'''
set emitted {}
set qs {boot_setting}
array set net_clock {system sys datapath milan audio audio}
array set cell_clock {to_eth eth to_sys sys to_milan milan to_audio audio}
proc get_nets {name} {return $name}
proc get_ports {name} {return $name}
proc get_pins {args} {return [lindex $args 1]}
proc get_clocks {args} {
    if {![llength $args]} {return {eth sys milan audio}}
    set name [lindex $args end]
    if {$name eq "rx"} {return eth}
    if {[info exists ::net_clock($name)]} {return $::net_clock($name)}
    if {[info exists ::cell_clock($name)]} {return $::cell_clock($name)}
    return {}
}
proc get_cells {args} {
    if {[string match *quasi_static* [lindex $args end]]} {return $::qs}
    return {to_eth to_sys to_milan to_audio}
}
proc all_inputs {} {return {reset_button}}
foreach command {set_false_path set_max_delay set_clock_groups set_multicycle_path} {
    proc $command {args} [format {lappend ::emitted [linsert $args 0 %s]} $command]
}
proc require {condition message} {
    if {![uplevel 1 [list expr $condition]]} {error $message}
}
'''


def test_scoped_exceptions() -> None:
    """Grade the Tcl against independently enumerated covered and excluded pairs."""
    script = STUB + "\nsource {" + str(ROOT / "sw/litex/clock_constraints.tcl") + "}\n" + r'''
kl_quasi_static_constraints
require {[lsearch -exact $emitted {set_multicycle_path 4 -setup -from boot_setting}] >= 0} "setup missing"
require {[lsearch -exact $emitted {set_multicycle_path 3 -hold -from boot_setting}] >= 0} "hold missing"
set qs {}; set emitted {}
kl_quasi_static_constraints
require {![llength $emitted]} "empty class emitted constraints"
kl_eth_constraints rx {system datapath} {audio}
foreach clock {sys milan} {
    foreach {from to} [list eth $clock $clock eth] {
        set bound [list set_max_delay 8.000 -datapath_only -from $from -to $to]
        require {[lsearch -exact $emitted $bound] >= 0} "bound missing"
        require {[lsearch -exact $emitted [list set_false_path -hold -from $from -to $to]] >= 0} "hold missing"
    }
}
require {[lsearch -exact $emitted {set_false_path -from {eth audio} -to to_eth}] >= 0} "eth scope wrong"
set part_scope {set_false_path -from {sys milan audio} -to {to_sys to_milan}}
require {[lsearch -exact $emitted $part_scope] >= 0} "part scope wrong"
require {[lsearch -exact $emitted {set_false_path -to to_audio}] >= 0} "other domain lost exception"
require {[lsearch -exact $emitted {set_false_path -from reset_button -to to_eth}] >= 0} "input exception lost"
require {[lsearch -exact $emitted {set_clock_groups -asynchronous -group eth -group audio}] >= 0} "audio group missing"
require {[llength $emitted] == 14} "unexpected constraints"
foreach command {{kl_eth_constraints wrong_port {system datapath} {audio}}
                 {kl_eth_constraints rx {wrong_clock datapath} {audio}}
                 {kl_eth_constraints rx {system datapath} {wrong_audio}}} {
    require {[catch $command message]} "missing clock accepted"
    require {[string match *expected*clock* $message]} "wrong refusal"
}
set cell_clock(to_sys) {sys milan}
require {[catch {kl_eth_constraints rx {system datapath} {audio}} message]} "ambiguous clock accepted"
puts {scoped exception and wrong-name controls PASS}
'''
    result = subprocess.run(["tclsh"], input=script, text=True, capture_output=True, timeout=30)
    # tclsh on stdin can continue after an error and exit zero.
    assert result.returncode == 0 and not result.stderr, result.stdout + result.stderr
    assert "controls PASS" in result.stdout, result.stdout
    print(result.stdout.strip())


def test_log_gate() -> None:
    """Both IDs and severities refuse, including an actual wrong-name command's diagnostic."""
    with tempfile.TemporaryDirectory(prefix="constraint-log-") as tmp:
        path = Path(tmp) / "vivado.log"
        path.write_text("# set_msg_config -id {Vivado 12-4739}\nINFO: build complete\n")
        check_implementation_log(path)
        for severity in ("WARNING", "CRITICAL WARNING", "ERROR"):
            for diagnostic in ("Vivado 12-4739", "Designutils 20-1307"):
                path.write_text(f"{severity}: [{diagnostic}] planted refusal\n")
                try:
                    check_implementation_log(path)
                except RuntimeError as exc:
                    assert diagnostic in str(exc)
                else:
                    raise AssertionError(f"accepted {diagnostic}")
        path.unlink()
        try:
            check_implementation_log(path)
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("missing implementation log accepted")
    # The log gate must dominate manifest publication for every build entry.
    tree = ast.parse((ROOT / "sw/litex/milan_soc.py").read_text())
    main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
    calls = [node for node in ast.walk(main) if isinstance(node, ast.Call)]
    checks = [node for node in calls if isinstance(node.func, ast.Name)
              and node.func.id == "check_implementation_log"]
    assert len(checks) == 1
    build = next(node for node in calls if isinstance(node.func, ast.Attribute)
                 and isinstance(node.func.value, ast.Name) and node.func.value.id == "builder"
                 and node.func.attr == "build")
    check = checks[0]
    assert check.lineno > build.lineno
    guard = next(node for node in main.body if isinstance(node, ast.If)
                 and any(item is check for item in ast.walk(node)))
    assert ast.unparse(guard.test) == "args.build", "log check is not common to every board"
    assert "gateware_dir" in ast.unparse(check) and "vivado.log" in ast.unparse(check)
    assert any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
               and node.func.id == "add_eth_constraints" for node in ast.walk(tree))
    print("[constraints] implementation-log diagnostics, missing log and common build wiring PASS")


def test_live_wrong_name(vivado: str, checkpoint: Path, evidence_dir: Path | None) -> None:
    """Plant both rejected XDC commands on a read-only checkpoint in a fresh run."""
    with tempfile.TemporaryDirectory(prefix="constraint-live-") as tmp:
        work = Path(tmp)
        (work / "wrong.xdc").write_text(
            "set_max_delay 8 -datapath_only -from [get_clocks wrong_clock_607] "
            "-to [get_clocks -of_objects [get_nets sys_clk]]\n"
            "if {1} {set_false_path -from [get_clocks wrong_clock_607]}\n")
        script = work / "plant.tcl"
        script.write_text("set_param general.maxThreads 16\nopen_checkpoint {" + str(checkpoint.resolve()) +
                          "}\nread_xdc wrong.xdc\nquit\n")
        result = subprocess.run([vivado, "-mode", "batch", "-source", str(script)],
                                cwd=work, capture_output=True, text=True, timeout=600)
        assert result.returncode == 0, result.stdout[-4000:] + result.stderr
        log = work / "vivado.log"
        emitted = log.read_text()
        if evidence_dir is not None:
            evidence_dir.mkdir(parents=True, exist_ok=True)
            for name in ("vivado.log", "plant.tcl", "wrong.xdc"):
                (evidence_dir / name).write_bytes((work / name).read_bytes())
            (evidence_dir / "exit-code.txt").write_text(f"{result.returncode}\n")
        assert "[Vivado 12-4739]" in emitted and "[Designutils 20-1307]" in emitted
        try:
            check_implementation_log(log)
        except RuntimeError as exc:
            assert "12-4739" in str(exc) and "20-1307" in str(exc)
            print(str(exc))
        else:
            raise AssertionError("live planted wrong clock name accepted")
    print("[constraints] live wrong clock and unsupported XDC control: vendor rc=0, build gate REFUSED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vivado")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--evidence-dir", type=Path)
    args = parser.parse_args()
    test_crg_clock_sources()
    test_generated_constraints()
    test_scoped_exceptions()
    test_log_gate()
    if args.vivado or args.checkpoint:
        if not (args.vivado and args.checkpoint):
            parser.error("--vivado and --checkpoint are required together")
        test_live_wrong_name(args.vivado, args.checkpoint, args.evidence_dir)

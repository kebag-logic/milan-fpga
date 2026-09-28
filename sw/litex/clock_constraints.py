# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Repository-owned Ethernet exception scoping and implementation-log gate (#607)."""

from pathlib import Path
import re
from typing import Any

from litex.build.xilinx.vivado import XilinxVivadoToolchain


class BoundedEthVivadoToolchain(XilinxVivadoToolchain):
    """Replace only the generic MultiReg exception when bounded GMII is present."""

    bounded_eth = False

    def _build_false_path_constraints(self) -> None:
        super()._build_false_path_constraints()
        if not self.bounded_eth:
            return
        # LiteX has no public selector for this exception. Keep its remaining
        # constraints, and refuse an upstream template change instead of silently
        # retaining a false path that outranks the Ethernet max delay.
        commands = self.platform.constraint_manager.platform_commands
        generic = ("set_false_path -quiet "
                   "-to [get_cells -hierarchical -filter {{mr_ff == TRUE}}]", {})
        if commands.count(generic) != 1:
            raise RuntimeError("#607: unsupported LiteX MultiReg constraint template")
        commands.remove(generic)


def add_quasi_static_constraints(platform: Any) -> None:
    """Run conditional class constraints as Tcl after synthesis, before optimize."""
    hook = Path(__file__).resolve().with_suffix(".tcl")
    platform.toolchain.pre_optimize_commands.append("source {{%s}}" % hook)
    platform.toolchain.pre_optimize_commands.append("kl_quasi_static_constraints")


def add_eth_constraints(platform: Any, crg: Any, eth_rx: Any) -> None:
    """Resolve real clock nets through the namespace, including optional domains."""
    toolchain = platform.toolchain
    if not isinstance(toolchain, BoundedEthVivadoToolchain):
        raise RuntimeError("#607: bounded GMII needs the scoped MultiReg toolchain")
    toolchain.bounded_eth = True
    # _CRG records these at create_clkout, before synthesis can discard an
    # unused buffered alias (the DDR sys4x aliases disappear in some builds).
    clocks = crg.eth_bounded_clocks
    other = crg.eth_async_clocks
    signals = {"eth": eth_rx}
    for index, clock in enumerate(clocks + other):
        signals[f"clk{index}"] = clock
    part_nets = " ".join("{clk%d}" % n for n in range(len(clocks)))
    other_nets = " ".join("{clk%d}" % n for n in range(len(clocks), len(clocks) + len(other)))
    toolchain.pre_optimize_commands.add(
        "milan_eth_constraints {eth} [list " + part_nets + "] [list " + other_nets + "]", **signals)
    toolchain.bitstream_commands.append(
        "report_clock_interaction -delay_type min_max -file {build_name}_clock_interaction.rpt")
    toolchain.bitstream_commands.append(
        "report_exceptions -file {build_name}_exceptions.rpt")


def check_implementation_log(path: Path) -> None:
    """Refuse missing logs and emitted constraint-application diagnostics on every board."""
    pattern = re.compile(r"^(?:CRITICAL WARNING|WARNING|ERROR):\s+"
                         r"\[(?:Vivado 12-4739|Designutils 20-1307)\]")
    with path.open(encoding="utf-8", errors="replace") as stream:
        findings = [(number, line.strip()) for number, line in enumerate(stream, 1)
                    if pattern.match(line)]
    if findings:
        details = "\n".join(f"{path}:{number}: {line}" for number, line in findings)
        raise RuntimeError("constraint application failed (#607):\n" + details)
    print(f"[constraints] {path}: no 12-4739 or 20-1307 diagnostics")

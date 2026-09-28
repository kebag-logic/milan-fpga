# SPDX-License-Identifier: CERN-OHL-W-2.0
"""#607: inspect constraints emitted by complete shipping AX7101 elaborations."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "sw/litex"))


def elaborate_shipping(config: str, port: str, output: Path) -> None:
    """Run the real main/Builder path, observing its namespace and generated files."""
    import endstation_builder as eb
    import milan_soc
    from litex.build.xilinx.vivado import XilinxVivadoToolchain

    cfg = ROOT / "configs" / f"endstation_{config}.yaml"
    eb.build(cfg, ROOT / "sw/builder/out")
    params = ROOT / "sw/builder/out" / cfg.stem / "soc_params.json"
    argv = json.loads(params.read_text())["argv"]
    argv += ["--entity-gen-dir", str(ROOT / "configs/generated" / cfg.stem),
             "--eth-port", port, "--no-compile-software", "--no-compile-gateware",
             "--vivado-max-threads", "16", "--output-dir", str(output)]
    observed = []

    class InspectBuilder(milan_soc.Builder):
        def build(self, **kwargs: Any) -> Any:
            """Inspect the namespace and files returned by the actual builder."""
            assert kwargs.get("run") is False, "shipping probe must not run implementation"
            assert not self.compile_software, "shipping probe must not compile firmware"
            namespace = super().build(**kwargs)
            # Use the actual main-PLL output objects, independently of the
            # hook's eth_bounded_clocks list and of generated name spellings.
            clocks = [namespace.get_name(self.soc.crg.pll.clkouts[i].clk) for i in (0, 1)]
            directory = Path(self.gateware_dir)
            tcl = (directory / "alinx_ax7101.tcl").read_text()
            xdc = (directory / "alinx_ax7101.xdc").read_text()
            commands = [line.strip() for line in tcl.splitlines()
                        if line.strip() and not line.lstrip().startswith("#")]
            hooks = [line for line in commands if line.startswith("milan_eth_constraints ")]
            assert len(hooks) == 1, f"shipping Ethernet hook missing or duplicated: {hooks}"
            eth = f"eth_clocks{int(port[1:]) - 1}_rx"
            assert hooks[0].startswith(
                f"milan_eth_constraints {eth} [list {' '.join(clocks)}] [list "), hooks[0]
            synth = next(i for i, line in enumerate(commands) if line.startswith("synth_design "))
            optimize = next(i for i, line in enumerate(commands) if line.startswith("opt_design "))
            assert synth < commands.index(hooks[0]) < optimize, "shipping hook outside pre-optimize"
            assert not any("mr_ff" in line and not line.lstrip().startswith("#")
                           for line in xdc.splitlines()), "generic MultiReg false path in shipping XDC"
            assert not list(directory.glob("*.bit")), "elaboration produced a bitstream"
            observed.append(hooks[0])
            return namespace

    # Even an accidental change to Builder's run handling cannot launch Vivado.
    with patch.object(milan_soc, "Builder", InspectBuilder), \
         patch.object(XilinxVivadoToolchain, "run_script",
                      side_effect=AssertionError("vendor run forbidden in shipping probe")), \
         patch.object(sys, "argv", [str(ROOT / "sw/litex/milan_soc.py"), *argv]):
        milan_soc.main()
    assert len(observed) == 1, "shipping probe never inspected generated files"
    print(f"[constraints] shipping {config} {port}: {observed[0]} PASS")


def test_shipping_constraints() -> None:
    """Both shipping shapes and either configured GMII port must emit the bound."""
    with tempfile.TemporaryDirectory(prefix="shipping-constraints-") as tmp:
        for config in ("ax7101_1x1_tdm8", "ax7101_8x8"):
            for port in ("e1", "e2"):
                command = [sys.executable, "-B", str(Path(__file__).resolve()),
                           "--config", config, "--port", port,
                           "--output-dir", str(Path(tmp) / f"{config}-{port}")]
                result = subprocess.run(command, cwd=ROOT / "sw/litex",
                                        env=dict(os.environ, PYTHONHASHSEED="0"),
                                        text=True, capture_output=True, timeout=600)
                assert result.returncode == 0, result.stdout[-4000:] + result.stderr[-4000:]
                markers = [line for line in result.stdout.splitlines()
                           if line.startswith("[constraints] shipping ")]
                assert len(markers) == 1 and markers[0].endswith(" PASS"), result.stdout[-4000:]
                print(markers[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", choices=("ax7101_1x1_tdm8", "ax7101_8x8"))
    parser.add_argument("--port", choices=("e1", "e2"))
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.config or args.port or args.output_dir:
        if not (args.config and args.port and args.output_dir):
            parser.error("--config, --port and --output-dir are required together")
        elaborate_shipping(args.config, args.port, args.output_dir)
    else:
        test_shipping_constraints()

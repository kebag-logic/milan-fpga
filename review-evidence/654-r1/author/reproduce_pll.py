"""Reproduce the tracked Arty clock refusal without generating hardware."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "sw/builder"))
import endstation_builder as eb
from migen import ClockDomain, Signal
from litex.soc.cores.clock import S7PLL

for name in ("arty_current", "arty_4x4", "arty_8ch"):
    cfg = eb.load_config(Path("configs") / f"endstation_{name}.yaml")
    frequency = cfg["constraints"]["sys_clk_hz"]
    pll = S7PLL(speedgrade=-1)
    pll.register_clkin(Signal(), 100e6)
    for index, hz in enumerate((frequency, 25e6, 50e6, 4*frequency, 4*frequency, 200e6)):
        pll.create_clkout(ClockDomain("probe" + str(index)), hz, margin=0)
    try:
        pll.compute_config()
    except ValueError as exc:
        print(f"{name}: requested {frequency} Hz; expected baseline refusal: {exc}")
    else:
        raise AssertionError(f"{name}: baseline failure no longer reproduces")
print("PASS: all three baseline refusals reproduced; this is not a successful build")

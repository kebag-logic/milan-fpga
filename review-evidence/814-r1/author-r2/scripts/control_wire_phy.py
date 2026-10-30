"""#814 measurement control, never committed: the head's SoC with `SPIPHYStage` replaced by wires.

Run from sw/litex in a clean clone with the export's milan_soc.py arguments. The class has the stage's faces and
joins them to the PHY's own (the test's `WirePHYStage`), so the route measures the image without the flash stage.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
import milan_soc  # noqa: E402
from migen import Module, Signal  # noqa: E402
from litex.soc.interconnect import stream  # noqa: E402


class WirePHYStage(Module):
    """`SPIPHYStage`'s faces joined to the PHY by wires."""

    def __init__(self, phy):
        self.phy_sink, self.phy_source, self.phy_cs = phy.sink, phy.source, phy.cs
        self.sink = stream.Endpoint(phy.sink.description)
        self.source = stream.Endpoint(phy.source.description)
        self.cs = Signal.like(phy.cs)
        self.comb += [self.sink.connect(phy.sink), phy.source.connect(self.source), phy.cs.eq(self.cs)]


milan_soc.SPIPHYStage = WirePHYStage
sys.argv = sys.argv[1:]
milan_soc.main()

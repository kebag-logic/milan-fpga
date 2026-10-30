"""gen_stage_verilog.py <repo> <out-dir>: each #814 stage alone as Verilog, at the shipping SoC's widths, for an
out-of-context implementation of its own cost. Run with the LiteX interpreter.
  spi_phy_stage   SPIPHYStage in front of a stub with LiteSPI's PHY faces (core2phy 60 bits, phy2core 32, cs 1)
  axi_ready_stage AXIReadyStage between two AXI4 ports shaped as the CPU memory port: data 256, address 32 and
                  the id width the shipping export's crossing FIFOs carry (73-bit aw and ar words)
  refresher       RegisteredRefresher and LiteDRAM's own Refresher, at the board's DDR3 settings (the difference is
                  the stage)"""
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / 'sw/litex'))
out.mkdir(parents=True, exist_ok=True)
import milan_soc  # noqa: E402
from migen import Module, Signal  # noqa: E402
from migen.fhdl.verilog import convert  # noqa: E402
from litex.soc.interconnect import axi, stream  # noqa: E402
from litespi.common import spi_core2phy_layout, spi_phy2core_layout  # noqa: E402
from litedram.core.controller import ControllerSettings  # noqa: E402
from litedram.core.refresher import Refresher  # noqa: E402
from litedram.modules import MT41J256M16  # noqa: E402
from litedram.phy.model import get_sdram_phy_settings  # noqa: E402
from litedram.common import GeomSettings, TimingSettings  # noqa: E402,F401


def endpoint_ios(endpoint):
    """Every wire of a stream endpoint."""
    return {endpoint.valid, endpoint.ready, endpoint.first, endpoint.last,
            *[getattr(endpoint, name) for name, _ in endpoint.description.payload_layout],
            *[getattr(endpoint, name) for name, _ in endpoint.description.param_layout]}


class PhyStub:
    """LiteSPI's PHY faces only."""

    def __init__(self):
        self.sink = stream.Endpoint(spi_core2phy_layout)
        self.source = stream.Endpoint(spi_phy2core_layout)
        self.cs = Signal()


class Wrap(Module):
    """A stage as a top with its faces as ports."""


phy = PhyStub()
top = Wrap()
top.submodules.stage = stage = milan_soc.SPIPHYStage(phy)
ios = endpoint_ios(stage.sink) | endpoint_ios(stage.source) | endpoint_ios(phy.sink) | endpoint_ios(phy.source)
ios |= {stage.cs, phy.cs}
(out / 'spi_phy_stage.v').write_text(str(convert(top, ios=ios, name='spi_phy_stage')))

# The aw and ar crossing FIFO words are 73 bits in the shipping export (`storage_10`, `storage_13`).
for id_width in range(1, 17):
    probe = axi.AXIInterface(data_width=256, address_width=32, id_width=id_width, version='axi4')
    if len(probe.aw.payload.raw_bits()) + len(probe.aw.param.raw_bits()) + 2 == 73:
        break
else:
    sys.exit('no id width gives the shipping 73-bit address word')
master = axi.AXIInterface(data_width=256, address_width=32, id_width=id_width, version='axi4')
slave = axi.AXIInterface(data_width=256, address_width=32, id_width=id_width, version='axi4')
top = Wrap()
top.submodules.stage = milan_soc.AXIReadyStage(master, slave)
ios = set()
for port in (master, slave):
    for name in ('aw', 'w', 'b', 'ar', 'r'):
        ios |= endpoint_ios(getattr(port, name))
(out / 'axi_ready_stage.v').write_text(str(convert(top, ios=ios, name='axi_ready_stage')))
(out / 'axi_id_width.txt').write_text(f'{id_width}\n')

module = MT41J256M16(100e6, '1:4')
phy_settings = get_sdram_phy_settings(memtype='DDR3', data_width=32, clk_freq=100e6)


class Settings:
    """The controller's view the refresher reads."""
    phy, geom, timing = phy_settings, module.geom_settings, module.timing_settings
    with_refresh = True


for name, cls in (('refresher_staged', milan_soc.RegisteredRefresher), ('refresher_plain', Refresher)):
    top = Wrap()
    top.submodules.refresher = refresher = cls(Settings, clk_freq=100e6, zqcs_freq=ControllerSettings().refresh_zqcs_freq,
                                               postponing=ControllerSettings().refresh_postponing)
    (out / f'{name}.v').write_text(str(convert(top, ios=endpoint_ios(refresher.cmd), name=name)))
print('wrote', sorted(p.name for p in out.iterdir()))

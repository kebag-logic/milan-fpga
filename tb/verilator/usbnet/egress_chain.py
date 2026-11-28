#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Convert the production USB attachment on the shipping 100 Mb/s MAC chain.

Only the original direct FIFO-to-core connection is replaced. The production
attachment makes its own replacement, including the PHY frame-end handshake.
Its terminated GPIF inputs become test inputs; all other wiring is unchanged.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

from migen import Signal, Instance
from migen.fhdl.structure import _Assign
from migen.fhdl.verilog import convert
from litex.build.sim.common import sim_special_overrides

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "sw/litex"))
import gen_mac_tx_model as mac_model
import usbnet_soc


class Platform:
    """Record the production attachment sources for the compiler."""

    def __init__(self) -> None:
        self.sources: list[str] = []

    def add_source(self, path: str) -> None:
        """Each registered source must exist."""
        if not Path(path).is_file():
            raise ValueError(path)
        self.sources.append(path)


def remove_drivers(chain: object, signals: list, expected: int) -> None:
    """Replace precisely the named direct assignments, refusing wiring drift."""
    comb = chain._fragment.comb
    removed = [s for s in comb if isinstance(s, _Assign) and any(s.l is x for x in signals)]
    if len(removed) != expected:
        raise ValueError(f"attachment replaced {len(removed)} assignments, expected {expected}")
    comb[:] = [s for s in comb if not any(s is x for x in removed)]


def generate(directory: Path) -> Path:
    """Emit the production chain and bind its exact sources in a manifest."""
    chain = mac_model.build_chain("mii")
    core, src = chain.core.sink, chain.tx_sf.source
    remove_drivers(chain, [core.valid, core.first, core.last, core.data,
                          core.last_be, core.error, src.ready], 7)
    chain.ethtxend_tgl = Signal(name="txend")
    enable = Signal(name="inject_enable")
    platform = Platform()
    rx = SimpleNamespace(valid=0, ready=0, data=0, keep=0, last=0)
    usbnet_soc.add_usb_net(chain, platform, 80_000_000, ROOT, rx, enable)
    # Anonymous observation outputs need explicit names in a standalone top.
    for special in chain._fragment.specials:
        if isinstance(special, Instance) and special.name_override == "usbnet_tap":
            for item in special.items:
                if isinstance(item, Instance.Output) and item.name in (
                        "rx_verdict_valid_o", "rx_verdict_o", "tx_verdict_valid_o", "tx_verdict_o"):
                    item.expr.name_override = item.name
    bus = chain.usbnet_bus
    remove_drivers(chain, [bus.dn.valid, bus.alive], 2)
    valid, ready, data = Signal(name="dn_valid"), Signal(name="dn_ready"), Signal(16, name="dn_data")
    active, hi_valid, hi_ready = (Signal(name=n) for n in ("active", "hi_valid", "hi_ready"))
    chain.comb += [bus.dn.valid.eq(valid), ready.eq(bus.dn.ready), bus.dn.data.eq(data), bus.alive.eq(1),
                   active.eq(chain.usbnet_inj_active), hi_valid.eq(src.valid), hi_ready.eq(src.ready)]
    ios = {chain.sys_clk, chain.sys_rst, chain.dp_clk, chain.dp_rst, chain.eth_tx_clk, chain.eth_rx_clk,
           chain.eth_phy_rst, chain.reinit, chain.eth_rst, chain.loopback, chain.dp_tdata, chain.dp_tkeep,
           chain.dp_tvalid, chain.dp_tlast, chain.dp_tready, chain.gmii_tx_en, chain.gmii_tx_data,
           chain.gmii_tx_er, chain.phy_sink_valid, chain.phy_sink_ready, chain.phy_sink_last,
           chain.phy_sink_data, chain.maceth_tx_rst, valid, ready, data, enable, active, hi_valid, hi_ready}
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "usbnet_egress_chain.v"
    target.write_text(str(convert(chain, ios=ios, name="usbnet_egress_chain",
                                  special_overrides=sim_special_overrides)))
    sources = [ROOT / "sw/litex/gen_mac_tx_model.py", ROOT / "sw/litex/milan_soc.py",
               ROOT / "sw/litex/usbnet_soc.py", Path(__file__), *map(Path, platform.sources)]
    manifest = dict(pins=mac_model.pinned_revisions(), sources={str(p.relative_to(ROOT)):
                    hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                    verilog_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    (directory / "chain.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return target


if __name__ == "__main__":
    generate(Path(sys.argv[1]))

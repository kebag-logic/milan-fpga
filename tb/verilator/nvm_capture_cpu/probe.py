# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Simulation-only observation CSRs and packet boundary; no product RTL edits."""
from migen import Signal
from litex.build.generic_platform import Pins, Subsignal
from litex.gen import LiteXModule
from litex.soc.interconnect.csr import AutoCSR, CSRStorage, CSRStatus


class CaptureProbe(LiteXModule, AutoCSR):
    """Firmware markers plus counters supplied by the simulation driver."""

    def __init__(self, platform, desc_bus):
        self.enable = CSRStorage(name="enable")
        self.active = CSRStorage(name="active")
        self.requests = CSRStatus(32, name="requests")
        self.responses = CSRStatus(32, name="responses")
        self.reads = CSRStatus(32, name="reads")
        pads = platform.request("probe")
        self.comb += [pads.enable.eq(self.enable.storage),
                      pads.active.eq(self.active.storage),
                      pads.desc_ack.eq(desc_bus.cyc & desc_bus.stb & desc_bus.ack & ~desc_bus.we),
                      self.requests.status.eq(pads.requests),
                      self.responses.status.eq(pads.responses),
                      self.reads.status.eq(pads.reads)]


def add_pads(platform: object) -> None:
    """Expose the datapath MAC AXIS face and passive descriptor-bus observer."""
    platform.add_extension([
        ("probe", 0, Subsignal("enable", Pins(1)), Subsignal("active", Pins(1)),
         Subsignal("desc_ack", Pins(1)), Subsignal("requests", Pins(32)),
         Subsignal("responses", Pins(32)), Subsignal("reads", Pins(32))),
        ("traffic", 0, Subsignal("rx_data", Pins(64)), Subsignal("rx_keep", Pins(8)),
         Subsignal("rx_valid", Pins(1)), Subsignal("rx_last", Pins(1)), Subsignal("rx_ready", Pins(1)),
         Subsignal("tx_data", Pins(64)), Subsignal("tx_keep", Pins(8)),
         Subsignal("tx_valid", Pins(1)), Subsignal("tx_last", Pins(1)), Subsignal("tx_ready", Pins(1))),
    ])


def packet_ports(platform: object) -> tuple[dict, None]:
    """Replace the idle MAC ties; this board has no physical audio input pads."""
    pads = platform.request("traffic")
    return dict(i_s_axis_mac_rx_tdata=pads.rx_data, i_s_axis_mac_rx_tkeep=pads.rx_keep,
                i_s_axis_mac_rx_tvalid=pads.rx_valid, i_s_axis_mac_rx_tlast=pads.rx_last,
                o_s_axis_mac_rx_tready=pads.rx_ready, o_m_axis_mac_tx_tdata=pads.tx_data,
                o_m_axis_mac_tx_tkeep=pads.tx_keep, o_m_axis_mac_tx_tvalid=pads.tx_valid,
                o_m_axis_mac_tx_tlast=pads.tx_last, i_m_axis_mac_tx_tready=pads.tx_ready), None

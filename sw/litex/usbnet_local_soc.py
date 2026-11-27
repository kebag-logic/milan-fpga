# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The USB network path's separate local receiver in the Arty split placement.

Only the buffered control-byte input is shared with network reception. The
network MAC, timestamping and media receiver retain their existing wiring.
"""
from migen import Cat, ClockSignal, Instance, Mux, ResetSignal
from litex.gen.genlib.cdc import BusSynchronizer
from litex.soc.interconnect import stream


def add_local_receiver(soc: object, mac: object, dp: object) -> None:
    """Deliver local control after the network timestamp and media paths.

    The mailbox applies the same protocol filter to both byte streams. Its
    network control FIFO is a passive tap, so delaying a buffered control
    frame cannot delay network reception. The address crosses coherently.
    """
    soc.usbnet_station_sync = BusSynchronizer(48, dp.milan_cd, "macsys")
    soc.comb += soc.usbnet_station_sync.i.eq(mac.usbnet_station_mac_dp)
    station = soc.usbnet_station_sync.o
    dp.usbnet_network = stream.Endpoint([("data", 8)])
    dp.usbnet_receiver = stream.Endpoint([("data", 8)])
    net, receiver, sent = dp.usbnet_network, dp.usbnet_receiver, mac.core.sink
    soc.specials += Instance("KL_usbnet_local_rx", name="usbnet_local_rx",
        attr={("DONT_TOUCH", "TRUE")},
        i_clk_i=ClockSignal("macsys"), i_rst_ni=~ResetSignal("macsys"),
        # The CSR convention puts the first wire octet in the low byte.
        i_station_mac_i=Cat(*(station[i:i + 8] for i in range(40, -1, -8))),
        i_s_active_i=mac.usbnet_inj_active,
        i_s_valid_i=sent.valid & sent.ready & mac.usbnet_inj_active,
        i_s_data_i=sent.data,
        i_s_keep_i=Mux(sent.last, (sent.last_be << 1) - 1, 0xFF)[:8],
        i_s_last_i=sent.last,
        i_net_valid_i=net.valid, o_net_ready_o=net.ready,
        i_net_data_i=net.data, i_net_last_i=net.last,
        o_m_valid_o=receiver.valid, i_m_ready_i=receiver.ready,
        o_m_data_o=receiver.data, o_m_last_o=receiver.last,
        o_copied_o=mac.usbnet_local_copied, o_full_o=mac.usbnet_local_full)

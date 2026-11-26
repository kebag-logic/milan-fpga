# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The Arty A7's USB network path (#1011) and status LEDs (#1018), as SoC attachments.

Two functions, each called from one place in milan_soc.py, both for the Arty
only, so no other board's build sees a line of this module:

  add_usb_net(mac, platform, sys_clk_freq)
      KL_usbnet_tap at the MAC wrapper's system-clock side: its receive copy
      reads the stream the datapath takes (rx_dp.sys, valid and ready), its
      arbiter sits between the datapath's store-and-forward FIFO (tx_sf) and
      the MAC core, and it produces the frame-end toggle the AECP REBOOT
      sequence counts (KL_usbnet_tx_arb). The bus side is `mac.usbnet_bus`,
      the two 16-bit streams and the bus-alive level a slave-FIFO master binds
      (docs/design/USB_NET_PATH.md). Until one is bound the bus side is
      terminated: nothing arrives from the computer, records toward it are
      taken and discarded, and the bus is reported down (LD1 off). The tap
      carries DONT_TOUCH so the image carries, and the route costs, the whole
      path rather than what a terminated bus would leave of it.

  add_status_leds(soc, platform, sys_clk_freq, mac)
      KL_status_leds on the RGB LEDs LD0 to LD3, green only, and the status
      register the control firmware writes for LD2 and LD3
      (`status_leds_ctrl`, read back with the LED states in
      `status_leds_state`).
"""
from __future__ import annotations

from migen import Cat, ClockSignal, Instance, ResetSignal, Signal
from litex.gen import LiteXModule
from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import CSRField, CSRStatus, CSRStorage

#: The RTL, in dependency order (the package first).
USBNET_SOURCES = (
    "hdl/usbnet/KL_usbnet_pkg.sv",
    "hdl/usbnet/KL_usbnet_rx_copy.sv",
    "hdl/usbnet/KL_usbnet_tx_inject.sv",
    "hdl/usbnet/KL_usbnet_tx_arb.sv",
    "hdl/usbnet/KL_usbnet_tap.sv",
)
LED_SOURCES = ("hdl/usbnet/KL_status_leds.sv",)

#: The injection rate limit and burst (#1011): 10 Mb/s on the wire, a tenth of
#: the Arty's 100 Mb/s link, and two longest frames of burst.
USBNET_RATE_BPS = 10_000_000
USBNET_BURST_OCTETS = 3200
#: A host record older than this drops LD1 (the computer's side sends one a second).
USBNET_HOST_TIMEOUT_MS = 3000
#: LD0's blink: off, then held on.
LED_BLINK_OFF_MS, LED_BLINK_ON_MS = 40, 60
#: The PWM: 16 of 256 clocks, 6.25 %.
LED_PWM_BITS, LED_DUTY = 8, 16


def add_sources(platform, repo_root, names) -> None:
    for name in names:
        platform.add_source(str(repo_root / name))


class UsbNetBus:
    """The bus side a slave-FIFO master binds: `up` toward the computer, `dn` from it."""

    def __init__(self):
        self.up = stream.Endpoint([("data", 16)])   # source: valid, ready, data, last
        self.dn = stream.Endpoint([("data", 16)])   # sink: valid, ready, data
        self.alive = Signal(name="usbnet_bus_alive")


def add_usb_net(mac, platform, sys_clk_freq, repo_root, rx_dp_sys, inject_en) -> None:
    """Insert the tap at `mac.core.sink` and take the frame-end toggle (see the module doc)."""
    add_sources(platform, repo_root, USBNET_SOURCES)
    bus = UsbNetBus()
    mac.usbnet_bus = bus
    # Terminated until a bus master binds it: nothing arrives, everything leaving is taken.
    mac.comb += [bus.dn.valid.eq(0), bus.up.ready.eq(1), bus.alive.eq(0)]

    mac.usbnet_ok = Signal(name="usbnet_ok")
    host_mac = Signal(48, name="usbnet_host_mac")
    host_ok = Signal(name="usbnet_host_ok")
    host_state = Signal(16, name="usbnet_host_state")
    cnt = {n: Signal(16, name=f"usbnet_{n}") for n in
           ("rx_copied", "rx_full", "tx_passed", "tx_dropped", "tx_skipped", "tx_injected")}
    txend = Signal(name="usbnet_txend_tgl")
    src, snk = mac.tx_sf.source, mac.core.sink
    mac.specials += Instance("KL_usbnet_tap", name="usbnet_tap",
        attr={("DONT_TOUCH", "TRUE")},
        p_CLK_HZ_P=int(sys_clk_freq), p_RATE_BPS_P=USBNET_RATE_BPS,
        p_BURST_OCTETS_P=USBNET_BURST_OCTETS, p_HOST_TIMEOUT_MS_P=USBNET_HOST_TIMEOUT_MS,
        i_clk_i=ClockSignal("macsys"), i_rst_ni=~ResetSignal("macsys"),
        i_rx_valid_i=rx_dp_sys.valid & rx_dp_sys.ready, i_rx_data_i=rx_dp_sys.data,
        i_rx_keep_i=rx_dp_sys.keep, i_rx_last_i=rx_dp_sys.last,
        i_hi_valid_i=src.valid, o_hi_ready_o=src.ready, i_hi_last_i=src.last,
        i_hi_data_i=src.data, i_hi_be_i=src.last_be,
        o_m_valid_o=snk.valid, i_m_ready_i=snk.ready, o_m_last_o=snk.last,
        o_m_data_o=snk.data, o_m_be_o=snk.last_be,
        i_inject_en_i=inject_en,
        # the frame's last octet where the PHY's transmit stage takes it, the
        # seam the toggle this replaces flipped on
        i_eth_clk_i=ClockSignal("eth_tx"), i_eth_rst_ni=~ResetSignal("maceth_tx"),
        i_eth_end_i=mac.phy.sink.valid & mac.phy.sink.ready & mac.phy.sink.last,
        o_txend_tgl_o=txend,
        o_up_valid_o=bus.up.valid, i_up_ready_i=bus.up.ready, o_up_data_o=bus.up.data,
        o_up_last_o=bus.up.last,
        i_dn_valid_i=bus.dn.valid, o_dn_ready_o=bus.dn.ready, i_dn_data_i=bus.dn.data,
        i_bus_alive_i=bus.alive,
        o_usb_ok_o=mac.usbnet_ok, o_host_mac_o=host_mac, o_host_ok_o=host_ok,
        o_host_state_o=host_state,
        o_rx_verdict_valid_o=Signal(), o_rx_verdict_o=Signal(3),
        o_tx_verdict_valid_o=Signal(), o_tx_verdict_o=Signal(3),
        o_rx_copied_o=cnt["rx_copied"], o_rx_full_o=cnt["rx_full"],
        o_tx_passed_o=cnt["tx_passed"], o_tx_dropped_o=cnt["tx_dropped"],
        o_tx_skipped_o=cnt["tx_skipped"], o_tx_injected_o=cnt["tx_injected"],
        o_inj_active_o=Signal())
    mac.comb += [snk.error.eq(0), mac.ethtxend_tgl.eq(txend)]
    # Read-only status for the console and the bench: the computer's address and
    # USB state, and the six counters (saturating at 65,535).
    mac.usbnet_host = CSRStatus(fields=[
        CSRField("mac_lo", size=32, offset=0, description="The computer's address, octets 2 to 5.")],
        description="USB network path: the computer's address, low word (#1011).")
    mac.usbnet_host_hi = CSRStatus(fields=[
        CSRField("mac_hi", size=16, offset=0, description="The computer's address, octets 0 and 1."),
        CSRField("ok", size=1, offset=16, description="An address is held."),
        CSRField("usb_ok", size=1, offset=17, description="LD1: the USB 3.0 path works.")],
        description="USB network path: the computer's address, high half, and its state (#1011).")
    mac.usbnet_counts = CSRStatus(96, description="USB network path counters, 16 bits each, from bit 0: "
                                  "rx_copied, rx_full, tx_passed, tx_dropped, tx_skipped, tx_injected.")
    mac.comb += [
        mac.usbnet_host.fields.mac_lo.eq(host_mac[0:32]),
        mac.usbnet_host_hi.fields.mac_hi.eq(host_mac[32:48]),
        mac.usbnet_host_hi.fields.ok.eq(host_ok),
        mac.usbnet_host_hi.fields.usb_ok.eq(mac.usbnet_ok),
        mac.usbnet_counts.status.eq(Cat(*(cnt[n] for n in
            ("rx_copied", "rx_full", "tx_passed", "tx_dropped", "tx_skipped", "tx_injected")))),
    ]


class StatusLeds(LiteXModule):
    """LD0 to LD3 (#1018): the RTL block, its two registers and the green pads."""

    def __init__(self, platform, sys_clk_freq, repo_root, link_up, activity, usb_ok):
        add_sources(platform, repo_root, LED_SOURCES)
        self.ctrl = CSRStorage(fields=[
            CSRField("stream", size=1, offset=0, description="LD2: a stream is connected (IEEE 1722.1-2021 "
                     "7.4.42 connection_count, or a STREAM_INPUT bound and receiving). Written by the firmware."),
            CSRField("clock", size=1, offset=1, description="LD3: the clock source is internal, or the stream it "
                     "follows flows with the media clock recovered. Written by the firmware.")],
            description="Status LEDs LD2 and LD3 (#1018), written by the control firmware.")
        self.state = CSRStatus(fields=[
            CSRField("leds", size=4, offset=0, description="LD0 to LD3 as shown, before the PWM.")],
            description="Status LEDs LD0 to LD3 as shown (#1018).")
        leds = Signal(4)
        self.specials += Instance("KL_status_leds", name="status_leds",
            p_CLK_HZ_P=int(sys_clk_freq), p_PWM_BITS_P=LED_PWM_BITS, p_DUTY_P=LED_DUTY,
            p_BLINK_OFF_MS_P=LED_BLINK_OFF_MS, p_BLINK_ON_MS_P=LED_BLINK_ON_MS,
            i_clk_i=ClockSignal("sys"), i_rst_ni=~ResetSignal("sys"),
            i_link_up_i=link_up, i_act_i=activity, i_usb_ok_i=usb_ok,
            i_stat_i=self.ctrl.storage, o_state_o=self.state.fields.leds, o_led_o=leds)
        # one colour channel: green; red and blue held dark
        for i in range(4):
            pads = platform.request("rgb_led", i)
            self.comb += [pads.g.eq(leds[i]), pads.r.eq(0), pads.b.eq(0)]


def add_status_leds(soc, platform, sys_clk_freq, repo_root, mac) -> None:
    """The LEDs on the Arty; LD0 from the MAC's link and frames, LD1 from the tap when it is built."""
    activity = Signal(name="status_leds_act")
    core = mac.core
    # a frame's last beat at the MAC core, either way (both in the MAC's system domain)
    soc.comb += activity.eq((core.source.valid & core.source.ready & core.source.last) |
                            (core.sink.valid & core.sink.ready & core.sink.last))
    usb_ok = getattr(mac, "usbnet_ok", 0)
    soc.status_leds = StatusLeds(platform, sys_clk_freq, repo_root, mac.link_status.fields.link_up,
                                 activity, usb_ok)

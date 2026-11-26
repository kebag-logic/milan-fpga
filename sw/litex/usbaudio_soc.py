# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Arty-only audio attachment; the network attachment remains independently owned."""
from __future__ import annotations

from pathlib import Path
import yaml

from migen import Cat, ClockDomain, ClockSignal, If, Instance, ResetSignal, Signal
from migen.genlib.cdc import MultiReg
from migen.genlib.resetsync import AsyncResetSynchronizer
from litex.build.generic_platform import IOStandard, Pins, Subsignal
from litex.gen import LiteXModule
from litex.soc.interconnect.csr import CSRField, CSRStatus, CSRStorage


class UsbAudio(LiteXModule):
    """Whole-frame audio transport plus the fixed public A1:A0 harness."""

    def __init__(self, platform: object, repo: Path, media_domain: str) -> None:
        window, digest = self._control_and_clocks(platform, repo)
        armed, qualified = Signal(), Signal()
        self.specials += MultiReg(self.control.fields.armed, armed, "usb_bus")
        self.specials += MultiReg(self.control.fields.qualified, qualified, "usb_bus")
        session_reset = Signal()
        self.comb += session_reset.eq(~armed | ResetSignal("usb_bus")
                                     | ResetSignal(media_domain) | ResetSignal("audio"))

        local_resets = {}
        for domain in ("usb_bus", media_domain, "sys"):
            local_resets[domain] = Signal()
            self.specials += Instance("KL_usbaudio_reset", i_clk_i=ClockSignal(domain),
                i_reset_i=session_reset, o_rst_n=local_resets[domain])

        platform.add_extension([("usbaudio", 0,
            Subsignal("dq", Pins("E15 E16 D15 C15 J17 J18 K15 J15 U12 V12 V10 V11 U14 V14 T13 U13")),
            Subsignal("pclk", Pins("D4")), Subsignal("slwr_n", Pins("D3")),
            Subsignal("slrd_n", Pins("F4")), Subsignal("sloe_n", Pins("F3")),
            Subsignal("pktend_n", Pins("E2")), Subsignal("addr", Pins("D2 H2")),
            Subsignal("flaga", Pins("G2")), IOStandard("LVCMOS33"))])
        pads = platform.request("usbaudio")
        self.specials += Instance("ODDR", name="usb_pclk_forward", p_DDR_CLK_EDGE="SAME_EDGE",
            i_C=ClockSignal("usb_forward"), i_CE=1, i_D1=1, i_D2=0, i_R=0, i_S=0, o_Q=pads.pclk)
        dq_in, dq_out, dq_tristate = Signal(16), Signal(16), Signal(16)
        for bit in range(16):
            self.specials += Instance("IOBUF", i_I=dq_out[bit], i_T=dq_tristate[bit],
                                     o_O=dq_in[bit], io_IO=pads.dq[bit])
        rx_valid, rx_ready, cap_valid, cap_ready, cap_last = (Signal() for _ in range(5))
        status_valid, status_ready, status_last, cap_abort = (Signal() for _ in range(4))
        rx_data, cap_data, status_data = Signal(16), Signal(16), Signal(16)
        media_ports = {
            "pair_valid": (1, True), "pair_slot": (4, True), "pair_l": (32, True),
            "pair_r": (32, True), "frame_ns": (32, True), "capture_tick": (1, True),
            "media_tick": (1, False), "media_ns": (32, False), "media_locked": (1, False),
            "render_data": (64, False), "render_valid": (1, False), "render_last": (1, False),
            "render_stream": (4, False), "render_tick": (1, False)}
        signals = {key: Signal(width, name="usb_"+key) for key, (width, _) in media_ports.items()}
        self.ports = {f"{'i' if toward else 'o'}_usb_{name}_{'i' if toward else 'o'}": signals[name]
                      for name, (_, toward) in media_ports.items()}
        bridge_ports = {f"{'o' if toward else 'i'}_{name}_{'o' if toward else 'i'}": signals[name]
                        for name, (_, toward) in media_ports.items()}
        health, measured = Signal(2), Signal(32)
        drops, gaps, cap_drops, losses = (Signal(32) for _ in range(4))
        rejected, digest_errors, media_frames = (Signal(32) for _ in range(3))
        playback_extremes, capture_extremes = Signal(14), Signal(14)
        self.specials += Instance("KL_usbaudio_bridge", name="usb_audio_bridge",
            p_WINDOW_LOG2_P=window, p_DIGEST_P=digest,
            i_bus_clk_i=ClockSignal("usb_bus"), i_media_clk_i=ClockSignal(media_domain),
            i_oscillator_clk_i=ClockSignal("audio"), i_reset_i=session_reset,
            i_latency_qualified_i=qualified, i_rx_valid_i=rx_valid, o_rx_ready_o=rx_ready,
            i_rx_data_i=rx_data, o_capture_valid_o=cap_valid, i_capture_ready_i=cap_ready,
            o_capture_data_o=cap_data, o_capture_last_o=cap_last, o_capture_abort_o=cap_abort,
            o_status_valid_o=status_valid, i_status_ready_i=status_ready,
            o_status_data_o=status_data, o_status_last_o=status_last,
            o_locked_o=health[0], o_error_o=health[1], o_feedback_q16_o=measured,
            o_playback_drops_o=drops, o_playback_gaps_o=gaps,
            o_capture_drops_o=cap_drops, o_reference_losses_o=losses,
            o_rejected_records_o=rejected, o_digest_errors_o=digest_errors,
            o_media_frames_o=media_frames, o_playback_extremes_o=playback_extremes,
            o_capture_extremes_o=capture_extremes, **bridge_ports)
        # Diagnostics cross as held snapshots, not independent multi-bit synchronizers.
        snapshot_valid, snapshot_ready, snapshot_out = Signal(), Signal(), Signal(176)
        self.specials += Instance("KL_usbaudio_crossing", name="usb_diagnostics",
            p_WIDTH_P=176, p_DEPTH_P=4, i_s_clk_i=ClockSignal("usb_bus"), i_s_rst_n=local_resets["usb_bus"],
            i_data_i=Cat(measured, drops, losses, health, rejected, digest_errors, capture_extremes),
            i_valid_i=snapshot_ready, o_ready_o=snapshot_ready, i_m_clk_i=ClockSignal("sys"),
            i_m_rst_n=local_resets["sys"], o_data_o=snapshot_out,
            o_valid_o=snapshot_valid, i_ready_i=1)
        self.sync += If(snapshot_valid,
            self.feedback.status.eq(snapshot_out[:32]), self.drops.status.eq(snapshot_out[32:64]),
            self.reference_losses.status.eq(snapshot_out[64:96]), self.health.status.eq(snapshot_out[96:98]),
            self.rejected_records.status.eq(snapshot_out[98:130]), self.digest_errors.status.eq(snapshot_out[130:162]),
            self.capture_extremes.status.eq(snapshot_out[162:176]))
        # Media counters are not part of a bus-domain snapshot.
        media_diag = Signal(110)
        media_diag_valid = Signal()
        media_diag_ready = Signal()
        self.specials += Instance("KL_usbaudio_crossing", name="usb_media_diagnostics",
            p_WIDTH_P=110, p_DEPTH_P=4, i_s_clk_i=ClockSignal(media_domain), i_s_rst_n=local_resets[media_domain],
            i_data_i=Cat(gaps, cap_drops, media_frames, playback_extremes),
            i_valid_i=media_diag_ready, o_ready_o=media_diag_ready,
            i_m_clk_i=ClockSignal("sys"), i_m_rst_n=local_resets["sys"],
            o_data_o=media_diag, o_valid_o=media_diag_valid, i_ready_i=1)
        self.sync += If(media_diag_valid, self.gaps.status.eq(media_diag[:32]),
                             self.capture_drops.status.eq(media_diag[32:64]),
                             self.media_frames.status.eq(media_diag[64:96]),
                             self.playback_extremes.status.eq(media_diag[96:110]))
        self.specials += Instance("KL_usbaudio_gpif", name="usb_gpif",
            i_clk_i=ClockSignal("usb_bus"), i_capture_clk_i=ClockSignal("usb_capture"), i_reset_i=session_reset,
            i_dq_i=dq_in, o_dq_o=dq_out, o_dq_t_o=dq_tristate, o_address_o=pads.addr,
            o_slwr_n_o=pads.slwr_n, o_slrd_n_o=pads.slrd_n, o_sloe_n_o=pads.sloe_n,
            o_pktend_n_o=pads.pktend_n, i_flaga_i=pads.flaga,
            o_rx_valid_o=rx_valid, i_rx_ready_i=rx_ready, o_rx_data_o=rx_data,
            i_capture_valid_i=cap_valid, o_capture_ready_o=cap_ready, i_capture_data_i=cap_data,
            i_capture_last_i=cap_last, i_capture_abort_i=cap_abort,
            i_status_valid_i=status_valid, o_status_ready_o=status_ready,
            i_status_data_i=status_data, i_status_last_i=status_last)
        self._add_sources_and_constraints(platform, repo)

    def _control_and_clocks(self, platform: object, repo: Path) -> tuple[int, int]:
        """Create controls and the phased external clock domains."""
        profile = yaml.safe_load((repo / "configs/endstation_arty_usbaudio.yaml").read_text())["usb_audio"]
        window = profile["feedback_window_log2"]
        digest = profile["digest"]
        if window != 13 or digest != 0x84ff:
            raise ValueError("USB audio profile must match the pinned eight-channel firmware contract")
        self.control = CSRStorage(fields=[
            CSRField("armed", offset=0, description="Release all session queues after coordinated receiver reset."),
            CSRField("qualified", offset=1, description="Physical interval latency bound has been measured.")],
            name="control")
        self.health = CSRStatus(2, name="health")
        self.feedback = CSRStatus(32, name="feedback")
        self.drops = CSRStatus(32, name="drops")
        self.gaps = CSRStatus(32, name="gaps")
        self.capture_drops = CSRStatus(32, name="capture_drops")
        self.reference_losses = CSRStatus(32, name="reference_losses")
        self.rejected_records = CSRStatus(32, name="rejected_records")
        self.digest_errors = CSRStatus(32, name="digest_errors")
        self.media_frames = CSRStatus(32, name="media_frames")
        self.playback_extremes = CSRStatus(14, name="playback_extremes")
        self.capture_extremes = CSRStatus(14, name="capture_extremes")
        self.cd_usb_bus = ClockDomain("usb_bus")
        self.cd_usb_capture = ClockDomain("usb_capture")
        self.cd_usb_forward = ClockDomain("usb_forward")
        locked = Signal()
        feedback_raw = Signal()
        feedback_clock = Signal()
        raw = [Signal() for _ in range(3)]
        self.specials += Instance("MMCME2_BASE", name="usb_mmcm",
            p_BANDWIDTH="OPTIMIZED", p_CLKIN1_PERIOD=10.0, p_DIVCLK_DIVIDE=1,
            p_CLKFBOUT_MULT_F=6.0, p_CLKOUT0_DIVIDE_F=12.0,
            p_CLKOUT1_DIVIDE=12, p_CLKOUT1_PHASE=198.75,
            p_CLKOUT2_DIVIDE=12, p_CLKOUT2_PHASE=217.5,
            i_CLKIN1=platform.lookup_request("clk100"), i_CLKFBIN=feedback_clock,
            o_CLKFBOUT=feedback_raw, o_CLKOUT0=raw[0], o_CLKOUT1=raw[1], o_CLKOUT2=raw[2],
            i_RST=ResetSignal("sys"), i_PWRDWN=0, o_LOCKED=locked)
        self.specials += Instance("BUFG", i_I=feedback_raw, o_O=feedback_clock)
        for source, domain in zip(raw, (self.cd_usb_bus, self.cd_usb_forward, self.cd_usb_capture)):
            self.specials += Instance("BUFG", i_I=source, o_O=domain.clk)
            self.specials += AsyncResetSynchronizer(domain, ~locked)
        return window, digest

    @staticmethod
    def _add_sources_and_constraints(platform: object, repo: Path) -> None:
        """Load the transport and its mandatory clock, crossing and pad checks."""
        for source in sorted((repo / "hdl/milan/usbaudio").glob("*.sv")):
            platform.add_source(str(source))
        platform.add_source(str(repo / "third_party/verilog-axis/rtl/axis_async_fifo.v"))
        # Board root clocks must exist before querying derived bus clocks.
        platform.toolchain.pre_optimize_commands.append(
            "read_xdc {{%s}}" % (repo / "sw/litex/usbaudio_timing.xdc"))
        platform.toolchain.pre_optimize_commands.append(
            "source {{%s}}" % (repo / "third_party/verilog-axis/syn/vivado/axis_async_fifo.tcl"))
        platform.toolchain.pre_optimize_commands.append(
            "source {{%s}}" % (repo / "sw/litex/usbaudio_cdc.tcl"))
        platform.toolchain.pre_optimize_commands.append(
            "source {{%s}}" % (repo / "sw/litex/timing_grade.tcl"))
        platform.toolchain.pre_optimize_commands.append(
            "kl_timing_grade_configure xc7a100tcsg324-1 commercial 0 85 {{Slow Fast}}")
        platform.toolchain.pre_routing_commands.append(
            "source {{%s}}" % (repo / "sw/litex/usbaudio_pack.tcl"))
        platform.toolchain.pre_routing_commands.append(
            "kl_audio_pack_check {build_name}_audio_packing.rpt")
        platform.toolchain.additional_commands.append(
            "kl_timing_grade_reports {build_name}_audio")

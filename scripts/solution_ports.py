# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Authoritative datapath port groups shared by the integration documentation gate."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PortGroup:
    label: str
    rtl_names: str
    duty: str
    safe_start: str
    patterns: tuple[str, ...]

    def matches(self, port: str) -> bool:
        """Whether this group claims one RTL boundary port by name."""
        return any(re.fullmatch(pattern, port) for pattern in self.patterns)

    def row(self) -> str:
        """The group as the one Markdown table row the docs must carry."""
        return (
            f"| {self.label} | {self.rtl_names} | {self.duty} | "
            f"{self.safe_start} |"
        )


PORT_GROUPS = (
    PortGroup(
        "Clocks and resets",
        "`axis_clk`, `axis_resetn`, `gtx_*`, `clk_audio_i`, `clk_tdm_i`",
        "Drive selected domains and reset sequencing",
        "Drive required clocks; assert resets",
        (
            r"axis_clk",
            r"axis_resetn",
            r"gtx_clk",
            r"gtx_resetn",
            r"clk_audio_i",
            r"clk_tdm_i",
        ),
    ),
    PortGroup(
        "AXI4-Lite CSR",
        "`s_axi_*`",
        "Map the complete 64 KiB window",
        "Connect fully; never tie handshakes",
        (r"s_axi_.*",),
    ),
    PortGroup(
        "MAC streams",
        "`m_axis_mac_tx_*`, `s_axis_mac_rx_*`",
        "Preserve final-boundary backpressure",
        "Set `s_axis_mac_rx_tvalid=0`; set `m_axis_mac_tx_tready=0`",
        (r"m_axis_mac_tx_.*", r"s_axis_mac_rx_.*"),
    ),
    PortGroup(
        "Descriptor memory",
        "`o_desc_mem_*`, `i_desc_mem_*`",
        "Serve the generated entity image",
        "Set `i_desc_mem_req_ready=0`; clear every response input",
        (r"[io]_desc_mem_.*",),
    ),
    PortGroup(
        "Response memory",
        "`o_resp_mem_*`, `i_resp_mem_*`",
        "Complete every accepted response operation",
        "Set `i_resp_mem_req_ready=0`, `i_resp_mem_wr_ready=0`; clear response and completion inputs",
        (r"[io]_resp_mem_.*",),
    ),
    PortGroup(
        "Record image memory",
        "`o_nvm_mem_*`, `i_nvm_mem_*`",
        "Complete every accepted saved-state record operation",
        "Set `i_nvm_mem_req_ready=0`, `i_nvm_mem_wr_ready=0`; clear response and completion inputs",
        (r"[io]_nvm_mem_.*",),
    ),
    PortGroup(
        "MAC control and status",
        "`o_mac_*`, `i_mac_*`, link, PHY, Ethernet guards",
        "Report honest capabilities and status",
        "Set `i_mac_speed=2'b10`, `i_link_up=1`, `i_full_duplex=1`; clear events, capabilities, toggles",
        (
            r"[io]_mac_.*",
            r"o_mc_hash",
            r"o_phy_reset_n",
            r"i_link_up",
            r"i_full_duplex",
            r"i_ethrx_tgl", r"i_ethtx_tgl", r"i_ethact_tgl",
            r"o_eth_rst", r"o_eth_guard",
        ),
    ),
    PortGroup(
        "gPTP egress launch records",
        "`i_gptp_txrec_*`, `o_gptp_txseal_*`, `i_gptp_txseal_ack`",
        "Carry the launch observer's records in and the plane's seal back",
        "Clear every `i_gptp_txrec_*` and `i_gptp_txseal_ack`; leave the seal outputs open",
        (r"i_gptp_txrec_.*", r"[io]_gptp_txseal_.*"),
    ),
    PortGroup("End-station reset", "`o_reboot_phy_hold`, `o_icap_*`, `i_ethtxend_tgl`, `i_reboot_req`",
              "Hold the PHY in reset, after the MAC's last frame, and drive ICAPE2 for an AECP REBOOT, the split's "
              "on the firmware's request",
              "Leave open, toggle and request 0: a REBOOT only goes offline",
              (r"o_reboot_phy_hold|i_ethtxend_tgl|i_reboot_req", r"o_icap_.*")),
    PortGroup("Interrupt", "`o_irq_csr`", "Route the aggregate CSR interrupt",
              "Leave the output open during smoke tests", (r"o_irq_csr",)),
    PortGroup(
        "Identify output",
        "`o_identify`",
        "Route the requested visual indication",
        "Leave the output open during smoke tests",
        (r"o_identify",),
    ),
    PortGroup(
        "MMCM controls",
        "`o_mmcm_*`, `i_mmcm_*`, `i_ps_clk`",
        "Bridge DRP and phase handshakes",
        "Set `i_ps_clk=axis_clk`, DRP inputs zero, `i_mmcm_locked=1`, `i_mmcm_ps_done=0`",
        (r"[io]_mmcm_.*", r"i_ps_clk"),
    ),
    PortGroup(
        "Status LED levels",
        "`o_led_*`",
        "Register complete display predicates on `axis_clk`, then synchronize into the display clock",
        "Leave outputs open when no display is present; never use them for flow control",
        (r"o_led_(input_locked|output_open|clock_internal|clock_stream|source_locked|clock_locked)",),
    ),
    PortGroup(
        "Audio pins",
        "`i2s_*`, `tdm_*`, `media_lrclk_o`",
        "Match the selected audio geometry",
        "Set `i2s_sdout_i=0`, every `tdm_*_i=0`; leave outputs open",
        (r"i2s_.*", r"tdm_.*", r"media_lrclk_o"),
    ),
    PortGroup("PPS output", "`pps_o`", "Carry the PHC second boundary to a pin", "Leave the output open", (r"pps_o",)),
    PortGroup("Optional USB audio",
              "`usb_pair_*`, `usb_frame_ns_i`, `usb_capture_tick_i`, `usb_render_*`, `usb_media_*`",
              "Carry complete ordered frames on the media grid",
              "Disabled by default; clear inputs and leave outputs open",
              (r"usb_pair_.*", r"usb_frame_ns_i", r"usb_capture_tick_i", r"usb_render_.*", r"usb_media_.*")),
    PortGroup("Split control face", "`i_ctl_*`, `o_ctl_*`",
              "Bind the mailbox through `KL_mbx_cdc` when `CTRL_SPLIT_P` = 1",
              "Tie every `i_ctl_*` to 0; leave the outputs open", (r"[io]_ctl_.*",)),
)

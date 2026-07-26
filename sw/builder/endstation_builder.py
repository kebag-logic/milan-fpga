#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
endstation_builder.py - software-defined Milan End-Station builder.

docs/MILAN_COMPLIANCE_GAPS.md attack item 4: ONE declarative definition
drives gateware elaboration, AEM ROM, lwSRP tables and DT/driver shape
consistently. This round turns the scaffold into the working generator:
the emitted AEM overlay is CONSUMED by avdecc/gen_aem_store.py (--overlay)
and, for the current shape, reproduces the tracked aecp_aem_rom.svh
byte-identically; the emitted sweep_opts fragment is SOURCED by
sw/litex/sweep.sh (single source for the per-board design OPTS/L2).

Input:  a YAML end-station config (schema kebag-logic/milan-endstation-config,
        see configs/endstation_*.yaml for annotated examples).

Outputs (into OUTDIR/<config-stem>/):
  soc_params.json   - the sw/litex/milan_soc.py argv this config implies
                      (design flags only; flow flags like --build /
                      --vivado-max-threads / --place-directive belong to
                      sweep.sh, not to the end-station definition).
  aem_overlay.json  - AEM model overlay (descriptor counts, stream formats,
                      per-stream STREAM_PORT/cluster/map layout) consumed by
                      avdecc/gen_aem_store.py --overlay.
  lwsrp_table.json  - lwSRP (802.1Q MSRP/MVRP) reservation table: SR class,
  lwsrp_table.svh     MRP timers, class-A bandwidth math, the 0x680 CSR reset
                      words, the engine's elaboration parameters and one
                      provisioning record per stream.
  platform_shape.json - driver-visible layout: Milan CSR base, the DMA window
  milan-nic.dtsi      map DERIVED from board.constraints.rx_queues, the
                      physical addresses kl-eth hardcodes, and the
                      kl,dma-ether / kl,milan-pcm device-tree nodes.
  build_plan.md     - human-readable build plan. Shapes beyond current RTL
                      capability (NxN streams, TDM/AES3/SPDIF interfaces,
                      non-48k rates) VALIDATE but are marked "planned".
Plus (repo-level, single-sourced so nothing can drift):
  configs/generated/sweep_opts_<board>.sh - shell fragment (OPTS/L2/RXQ)
                      sourced by sw/litex/sweep.sh; the inline tables there
                      are the loud FALLBACK only.
  hdl/ieee8021q/srp/gen/lwsrp_table.svh   - the DEPLOYED shape's lwSRP table
                      (written by the one config carrying srp.rtl_table).
  hdl/common/csr/gen/lwsrp_csr_defaults.svh - the CSR-facing SUBSET of that
                      table (0x680 reset words + the PriorityAndRank byte),
                      `include-d BY hdl/common/csr/milan_csr.sv: the config
                      IS those literals now, they are not copied into RTL.

Usage:
  python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml
  python3 sw/builder/endstation_builder.py <cfg.yaml> -o <outdir>

Schema summary (see the example configs for the annotated normative form):
  schema / schema_version      - "kebag-logic/milan-endstation-config" / 1.1.x
  entity:                      - identity: name, entity_model_id
                                 ("hash-derived" | EUI-64 hex), model_id_pin
                                 (optional EUI-64 hex override - pins the id
                                 of already-flashed silicon), entity_id
                                 ("mac-derived" | EUI-64 hex), vendor_name,
                                 firmware_version, serial_number, group_name
  board: target + constraints  - arty | ax7101; physical facts the SoC argv
                                 derives from (sys/milan clk, l2, phy, flash,
                                 uart, rx queues, hs page, probes, GMII knobs,
                                 eth_port for multi-port boards)
  clocking:                    - sampling_rate_hz, audio_unit_rates_hz,
                                 media_clock_sources (internal | input_stream
                                 | crf), default_source, crf_sink (+format),
                                 crf_output (enabled + format; Milan 7.2.3
                                 RULE: >=2 AAF listener streams REQUIRE it),
                                 audio_pll_hz (clean MMCM audio clock)
  audio_interface:             - kind: tdm8|tdm16|tdm32|i2s_philips|aes3|spdif
                                 word_length_bits, cluster_mapping.policy
                                 (cap-at-interface |
                                  cluster-per-stream-channel)
  streams:                     - listeners[] / talkers[]: name, channels,
                                 formats (AAF 64-bit hex), buffer_length_ns,
                                 clusters (SINGLE AUTHORITY for the stream's
                                 cluster count; default = channels)
  srp:                         - lwSRP reservation table (all optional; the
                                 defaults ARE today's 0x680 reset words):
                                 sr_class, vid, stream_dmac_base,
                                 accumulated_latency_ns, class_queue,
                                 enable_at_reset, talker_declare_at_reset,
                                 bandwidth_limit_pct, timers_ms{join,leave,
                                 leaveall}, tspec{policy: pinned|derived,
                                 max_frame_bytes, interval_frames},
                                 rtl_table (owns the tracked .svh)
  platform:                    - DT + driver shape: csr_base, mac_address
                                 (REQUIRED, unicast), interrupt,
                                 pcm_ring_phys/_bytes/_stride, dma_coherent,
                                 boot_chain_pin{window: address} - the
                                 FLASHED DTB's window map; a config whose
                                 rx_queues would move a pinned window is
                                 REFUSED (the 5ce9a13 CSR-rot rule)

entity_model_id derivation ("hash-derived", the default path; exact recipe,
also in sw/builder/README-parameters.md):
  1. shape = the model-shaping fields only (stream counts/formats/clusters/
     buffers, cluster policy, derived per-stream port layout, audio
     interface kind/channels/word length, sampling rates, CRF sink+format) -
     NO board flags, names or serials, so two boards with the same audio
     shape share a model id (AEM semantics).
  2. canon = json.dumps(shape, sort_keys=True, separators=(",", ":"))
  3. id = (MODEL_ID_OUI << 40) | (int.from_bytes(sha256(canon)[:8]) & (2^40-1))
     i.e. top-8-bytes of the sha256, folded under the base EUI-64 prefix
     MODEL_ID_OUI = 0x001BC5 (Kebag Logic OUI, kept HERE in the schema).
  Same shape -> same id; any shape change -> new id. entity.model_id_pin
  overrides the hash (already-flashed silicon keeps its identity).
"""

import argparse
import hashlib
import json
import os
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("endstation_builder: PyYAML required (python3 -m pip install pyyaml)")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

SCHEMA_ID = "kebag-logic/milan-endstation-config"
SCHEMA_MAJOR = "1"

OVERLAY_SCHEMA_ID = "kebag-logic/aem-overlay"
OVERLAY_SCHEMA_VERSION = "2.0.0"     # 2.x: per-stream STREAM_PORT layout

LWSRP_SCHEMA_ID = "kebag-logic/lwsrp-table"
LWSRP_SCHEMA_VERSION = "1.0.0"       # 1.x: SR class + 0x680 resets + rows

PLATFORM_SCHEMA_ID = "kebag-logic/platform-shape"
PLATFORM_SCHEMA_VERSION = "1.0.0"    # 1.x: DT node + driver-visible layout

# Base EUI-64 prefix for hash-derived entity_model_id values (see module
# docstring step 3). Schema-level constant: changing it re-identifies every
# hash-derived model - never change it casually.
MODEL_ID_OUI = 0x001BC5              # Kebag Logic vendor OUI (00-1B-C5)
MODEL_ID_HASH_BITS = 40              # EUI-64 bits taken from the sha256

CLUSTER_POLICIES = ("cap-at-interface", "cluster-per-stream-channel")


class ConfigError(Exception):
    """Raised for any config that violates the schema or board physics."""


# ------------------------------------------------------------------ tables --
# Board physical truth (cross-checked against configs; the config carries the
# values so the emitted argv is reviewable, the table rejects impossibilities).
BOARDS = {
    "arty": dict(
        phy="mii-100", link_mbps=100,
        sys_clk_hz_default=100_000_000,      # milan_soc.py --sys-clk-freq default
        gmii_knobs=False,                    # --gtx-tx-invert is a GMII fix
        eth_ports=(),                        # single PHY: no --eth-port choice
    ),
    "ax7101": dict(
        phy="gmii-1g", link_mbps=1000,
        sys_clk_hz_default=100_000_000,
        gmii_knobs=True,
        eth_ports=("e1", "e2"),              # e2 = ship port since 2026-07-22
    ),
}

# Physical audio interfaces (item-4 subtask). channels = per direction.
# `rtl` says how far the fabric has got for this kind:
#   present - front-end RTL AND the milan_datapath/milan_soc plumbing exist
#             (i2s_philips: KL_i2s_playback / aaf_talker_i2s; the tdm family:
#             KL_tdm_capture -> KL_aaf_packetizer, milan_soc.py
#             --audio-interface)
#   serdes  - the ser/des RTL exists and is TB-proven, but the datapath
#             generate + the --audio-interface value do not (yet) carry it.
#             That is the AES3/S-PDIF state since 2026-07-26: KL_aes3_rx +
#             KL_aes3_tx implement the whole biphase-mark transport and
#             tb/verilator/aes3 proves it, so the config SELECTS the family
#             member and its SV parameters (emit_interface_params below);
#             only the SoC wiring is still a planned mark.
INTERFACES = {
    "i2s_philips": dict(channels=2,  word_bits=(16, 24),     rtl="present"),
    "tdm8":        dict(channels=8,  word_bits=(16, 24, 32), rtl="present"),
    "tdm16":       dict(channels=16, word_bits=(16, 24, 32), rtl="present"),
    "tdm32":       dict(channels=32, word_bits=(16, 24, 32), rtl="present"),
    "aes3":        dict(channels=2,  word_bits=(16, 20, 24), rtl="serdes",
                        consumer=0),
    "spdif":       dict(channels=2,  word_bits=(16, 20, 24), rtl="serdes",
                        consumer=1),
}

#: The AES3/S-PDIF family (hdl/ieee1722/aaf/KL_aes3_rx.sv + KL_aes3_tx.sv).
#: ONE core serves both transports: CONSUMER_P picks the channel-status
#: dialect (0 = AES3-2009 professional, 1 = IEC 60958-3 consumer) and nothing
#: else. UI_PER_FRAME_C is the transport's own arithmetic: 2 subframes x 32
#: cells x 2 unit intervals, so the serial clock is
#: sampling_rate_hz * 128 * OVERSAMPLE_P.
AES3_RX_MODULE = "KL_aes3_rx"
AES3_TX_MODULE = "KL_aes3_tx"
AES3_UI_PER_FRAME = 128           #: unit intervals per AES3 frame (2 subframes)
AES3_OVERSAMPLE = 4               #! clk_audio_i cycles per UI (KL_aes3_tx default)
AES3_LOCK_BLOCKS = 2              #: clean 192-frame blocks before locked_o
AES3_BLOCK_FRAMES = 192           #: AES3-2009 4.3 channel-status block

# SoC-glue policy defaults (overridable via the optional `soc:` section).
# These mirror today's ship recipe = sw/litex/sweep.sh BASE (design flags).
SOC_DEFAULTS = dict(
    cpu="vexiiriscv",
    cpu_count=1,
    all_blocks=True,
    coherent_dma=True,
    timing_opt=True,
    scala_args=[
        "--lsu-l1-refill-count=8",
        "--lsu-hardware-prefetch=rpt",
        "--l2-down-pending=8",
        "--l2-general-slots=16",
    ],
)

# What the RTL supports TODAY (milan_datapath.sv). Anything beyond validates
# but lands in the plan as "planned", never as an error (builder contract).
RTL_TODAY = dict(
    max_aaf_listeners=1,
    max_talkers=1,
    crf_sink=True,
    interfaces={"i2s_philips", "tdm8", "tdm16", "tdm32"},
    render_channels=2,          # wire-truth rule: extra stream chans virtual
    sampling_rates={48000},
)

CRF_FORMAT_DEFAULT = "0x041060010000BB80"     # CRF AUDIO_SAMPLE 48k, gen_aem_store
# ^ Milan 7.3.2 Table 7.1 (PDF-verified): v=0, subtype 4 (CRF), type 1
#   (CRF_AUDIO_SAMPLE), timestamp_interval 96, timestamps_per_pdu 1, pull 0,
#   base_frequency 48000 -> ATDECC format string 0x041060010000BB80. Used for
#   BOTH the CRF sink (Milan 7.2.2) and the CRF output (Milan 7.2.3).
BUFLEN_DEFAULT_NS = 2126000

# --------------------------------------------------------- lwSRP constants --
# Item-4 emitter: the lwSRP (802.1Q MSRP/MVRP) reservation table. The config
# becomes the single source of truth for what is TODAY hand-written twice -
# hdl/ieee8021q/srp/lwsrp_pkg.sv (SR class + timers + bandwidth math) and the
# 0x680 CSR reset defaults in hdl/common/csr/milan_csr.sv. test_builder gates
# 18a/18b PARSE both RTL files and assert the emission agrees, so a hand edit
# on either side that the config does not know about fails the build.

#: SR classes. Milan v1.2 §5.6 defines class A only for a Milan end station;
#: the table is keyed so a class-B RTL round has somewhere to land.
SRP_SR_CLASSES = {
    "A": dict(class_id=6, priority=3, intervals_ps=8000),
}
SRP_RANK = 1                      #: PriorityAndRank rank bit (emergency = 0)
AVTP_AAF_HDR_BYTES = 24           #: IEEE 1722-2016 Fig 26 AAF AVTPDU header
AAF_SAMPLE_OCTETS = 4             #: AAF format INT_32BIT (§7.3.5)
L2_HDR_BYTES = 18                 #: DA 6 + SA 6 + VLAN 4 + EtherType 2
#: 802.1Q idleSlope overhead: preamble 8 + eth hdr 14 + VLAN 4 + FCS 4 + IPG 12
#: (= lwsrp_pkg::MSRP_FRAME_OVERHEAD_C). MaxFrameSize is therefore the MSDU
#: (the AVTPDU), NOT the L2 frame: MaxFrameSize + 42 = the full wire slot.
SRP_FRAME_OVERHEAD_B = 42
SRP_CTX_IDX_BITS = 4              #: KL_lwsrp_top ctx_idx_i width -> 16 rows
SRP_QUEUE_BITS = 3                #: LWSRP_CTRL[4:2] class-A queue select
#: (widened from [3:2] with the 6-queue map: class A now lives on q5)

#: lwSRP policy defaults = EXACTLY today's RTL reset words, so a config with
#: no `srp:` section emits the deployed gateware bit-for-bit (the
#: no-regression axiom this builder follows everywhere else).
SRP_DEFAULTS = dict(
    sr_class="A",
    vid=2,                                   # USER: VID 2 is THE SR vid
    stream_dmac_base="0x91E0F000FE01",       # MAAP range; stream t = base + t
    accumulated_latency_ns=0,
    class_queue=5,                           # reset PCP3 -> TC3 -> q5 map
                                             # (802.1Q order: q5 = class A)
    enable_at_reset=False,
    talker_declare_at_reset=False,
    bandwidth_limit_pct=75,                  # Milan §5.6 / 802.1Q §34.3.1
    join_time_ms=200,                        # 802.1Q Table 10-7 defaults
    leave_time_ms=600,
    leaveall_time_ms=10_000,
    tspec_policy="pinned",                   # pinned | derived
    max_frame_bytes=224,                     # pinned only (the 0x690 reset)
    interval_frames=1,
    rtl_table=False,                         # write the tracked hdl/ .svh
)
SRP_TSPEC_POLICIES = ("pinned", "derived")

# ------------------------------------------------------ platform / DT shape --
# Item-4 emitter: the device-tree node shape + the driver-visible layout.
# THE bug class this closes shipped in 5ce9a13: rx-queues is per board, the
# DMA window map is a FUNCTION of it, and a DTB built against the other
# board's count maps every window onto the wrong registers (CSR rot,
# TROUBLESHOOTING 20) - silent until the host plane is dead.
#
# LiteX allocates CSR addresses in submodule-registration order
# (sw/litex/milan_soc.py MilanDMA.__init__), so the map is deterministic:
#
#   +0x000  tx            RingDMAReader                     0x24
#   +0x024  rx  (q0)      RingDMAWriter incl. rsc + hs      0x68
#   +0x08C  steer         RxSteer               rx_queues>=2 0x0C  }  0x74
#   +0x098  rx1 (q1)      RingDMAWriter         rx_queues>=2 0x68  }  shift
#   +0x08C/+0x100  ts     WishboneDMAWriter                 0x1C
#   ...+0x1C  hs_pgsz_cap CSRStatus                         0x04
#   ...+0x04  pcm         PCM ring (flat or NxN)            0x1C
#
# and the MAC/MDIO bank is a SEPARATE LiteX bank that never shifts.
DMA_BANK_BASE = 0xF0003000       #: milan_dma CSR bank origin
DMA_TX_BYTES = 0x24              #: base/mask/wr/rd/enable/sent/bd_base
DMA_RX_BLOCK_BYTES = 0x68        #: q0 block incl. rsc + header-split regs
DMA_RX_MAP_BYTES = 0x40          #: extent kl-eth maps as the "dma-rx" window
DMA_STEER_BYTES = 0x0C           #: q0_frames/q1_frames/hash_sel (2 queues)
DMA_RX1_BLOCK_BYTES = 0x68       #: the q1 RingDMAWriter block (2 queues)
DMA_TS_BYTES = 0x1C              #: base/length/enable/done/loop/offset
DMA_HS_CAP_BYTES = 0x04          #: hs_pgsz_cap readback (hsq14 pairing check)
DMA_PCM_BYTES = 0x1C             #: PCM ring block (flat and NxN are both 0x1C)
MAC_BANK_BASE = 0xF0003800       #: milan_mac bank: crg_reset + MDIO bitbang
MAC_PHY_MAP_BYTES = 0x0C
MILAN_CSR_BASE = 0x9000_0000     #: AXI-Lite Milan CSR window (milan_soc.py)
MILAN_CSR_BYTES = 0x1_0000
EV_BANK_BASE = 0xF0002800        #: EventManager (kl-eth MILAN_EV_PHYS)

#: phy-mode DT string per board.constraints.phy
DT_PHY_MODE = {"mii-100": "mii", "gmii-1g": "gmii"}

PLATFORM_DEFAULTS = dict(
    csr_base=MILAN_CSR_BASE,
    dma_bank_base=DMA_BANK_BASE,
    mac_bank_base=MAC_BANK_BASE,
    ev_bank_base=EV_BANK_BASE,
    interrupt=3,                             # constant,milan_interrupt,3
    interrupt_parent="intc0",
    mac_address=None,                        # required: must differ per board
    pcm_ring_phys=0x4FF0_0000,
    pcm_ring_bytes=0x10_0000,
    pcm_ring_stride=0x10_0000,
    dma_coherent=True,
    boot_chain_pin=None,                     # flashed DTB's window map
)

# ------------------------------------------------------ resource estimator --
# Approximate pre-Vivado FPGA resource model (gaps item-4 subtask, USER
# 2026-07-22): per-module cost table x instance counts from the config, with
# a budget verdict vs the part. Calibrated 2026-07-22 against the REAL
# hierarchical place report of the shipping Arty build ("arty mf48" below):
#   ~/litex-milan/work/build_arty_eto_milanfinal48/gateware/
#       digilent_arty_utilization_hierarchical_place.rpt
# cross-checked against the AX7101 build ("ax mf38", totals within 2.4%):
#   ~/litex-milan/work/build_ax7101_eppo_milanfinal38/gateware/
#       alinx_ax7101_utilization_hierarchical_place.rpt
# HOUSE RULE (area-70 campaign): hierarchical figures are trusted for the
# LARGE blocks only (cpu, milan_datapath children, MAC/DMA/DDR); small-module
# rows are labeled low-confidence (cross-hierarchy LUT combining skews them).
# bram36 = RAMB36 + RAMB18/2 equivalents.
#
# NxN rows (P12, replacing the item-5 UPPER BOUNDs): the shared engines
# exist and are merged, so per-stream scaling is FIRST INSTANCE at the
# measured x1 cost + a per-extra-context MARGINAL row derived from yosys
# OOC synth_ecp5 of the merged engine at N=1 vs N=8 (delta/7; ECP5 LUT4
# charged 1:1 against Artix LUT6 = deliberately safe-side). Raw stats
# (2026-07-22, this tree):
#   KL_avtp_rx_monitor_ctx  N1 1349/992 LUT4/FF  N8 1904/1194 (+79/+29 per ctx)
#   KL_stream_table         N1   75/68           N8  110/537  (+5/+67)
#   KL_pcm_route            N1   20/2            N8   88/16   (+10/+2)
#   KL_aaf_packetizer       N1 1153/527/0BRAM16  N8 957/742/3 (LUT SHRINKS:
#     staging+TCTX migrate to BRAM; +31 FF, +0.43 BRAM16K per ctx)
#   KL_acmp_lstn_ctx        N1 2982/2228         N8 3651/2209 (+96/+0)
#   KL_lwsrp_ctx            N1  219/418          N8  319/428  (+14/+1.4)
#   KL_lwsrp_ctx_tx   LANES1  902/260      LANES7 1651/299    (+125/+6.5)
#   KL_lwsrp_walker   LANES1  667/572      LANES7  980/734    (+52/+27)
#   KL_lwsrp_bw_gate (30b P12 trim) N1 163/202   N8 839/581   (+97/+54)

PART_XC7A100T = dict(lut=63400, ff=126800, bram36=135, dsp=240)
RESOURCE_CATS = ("lut", "ff", "bram36", "dsp")

# Budget verdict thresholds (worst category, % of PART_XC7A100T).
VERDICT_OK_BELOW = 70.0      # area-70 directive: keep slice headroom
VERDICT_TIGHT_UPTO = 80.0

CAL_CLUSTERS = 16            # aecp_entity row includes the 16-cluster AEM ROM
CAL_L2_BYTES = 65536         # cpu_vexii row includes the 64 KB L2 of mf48
ROM_BYTES_PER_CLUSTER = 128  # ~104 B AUDIO_CLUSTER (1722.1 7.2.16) + map row
                             # + directory slice; RAMB36 = 4096 B


def _cost(lut, ff, bram36, dsp, src, confidence):
    return dict(lut=lut, ff=ff, bram36=bram36, dsp=dsp,
                src=src, confidence=confidence)


RESOURCE_COSTS = {
    # -- config-independent base (large blocks: measured, high confidence) --
    "soc_infra": _cost(13995, 14010, 42.5, 0,
                       "arty mf48 hier-place row '(digilent_arty)' top leaf "
                       "(LiteX glue + LiteEth MAC + LiteDRAM DDR + DMA; "
                       "39 RAMB36 + 7 RAMB18)",
                       "measured"),
    "cpu_vexii": _cost(17981, 12132, 41.0, 16,
                       "arty mf48 row 'VexiiRiscvLitex_*' subtree incl 64 KB "
                       "L2 (33 RAMB36 + 16 RAMB18)", "measured"),
    "l2_size_delta_4k": _cost(0, 0, 1.0, 0,
                              "model: 1 RAMB36 per 4 KB of L2 vs the 64 KB "
                              "calibration build (ax mf38 32 KB cross-check "
                              "exact: 41-8=33)", "model"),
    "traffic_controller": _cost(1903, 1342, 6.0, 24,
                                "arty mf48 row 'traffic_controller' (4 CBS "
                                "class engines - class-level, not per-stream)",
                                "measured"),
    "aecp_entity": _cost(5644, 3089, 2.5, 0,
                         "arty mf48 row 'aecp_listener' (KL_aecp_top incl "
                         "16-cluster AEM ROM store)", "measured"),
    "aem_rom_extra_cluster": _cost(0, 0, ROM_BYTES_PER_CLUSTER / 4096.0, 0,
                                   f"model: {ROM_BYTES_PER_CLUSTER} B ROM per "
                                   "cluster beyond 16 (tracked ROM = 3653 B "
                                   "for 34 descriptors)", "model"),
    "crf_rx": _cost(2699, 8457, 0, 0, "arty mf48 row 'crf_rx' (KL_crf_rx)",
                    "measured"),
    "csr": _cost(1628, 2024, 1.0, 0,
                 "arty mf48 row 'csr' (milan_csr, 2 RAMB18)", "measured"),
    "ptp_timestamp": _cost(814, 1667, 0, 0,
                           "arty mf48 row 'ptp_timestamp' (ptp_ts_top)",
                           "measured"),
    "rx_filter": _cost(539, 1570, 0, 0,
                       "arty mf48 row 'rx_filter' (tcam MAC database)",
                       "measured"),
    "i2s_renderer": _cost(562, 628, 1.0, 0,
                          "arty mf48 row 'i2s_player' (KL_i2s_playback; per "
                          "physical audio interface)", "measured"),
    "lwsrp_base": _cost(1523, 1083, 1.5, 1,
                        "arty mf48 row 'lwsrp' (KL_lwsrp_top: tx + bw_gate + "
                        "rx walker/registrars, 1 RAMB36 + 1 RAMB18)",
                        "measured"),
    "datapath_misc": _cost(893, 1417, 0, 0,
                           "arty mf48 rows adp_adv+acmp_responder+crf_tx+"
                           "link_guard+tone_gen+ctl_tx_mux+ethernet_counters "
                           "(summed)",
                           "low (small-module hierarchical rows; area-70 "
                           "rule: cross-hierarchy LUT combining skews them)"),
    # -- shared-engine scaling (P12): first instance = measured x1 of the
    #    engine complex; extras = yosys-derived marginal rows below --
    "aaf_listener_engine": _cost(1223, 2094, 2.0, 1,
                                 "arty mf48 rows aaf_rx_depkt+avtp_rx_parser+"
                                 "avtp_rx_monitor+pcm_lpf (summed; the shared "
                                 "RX engine complex, charged ONCE) + 0.5 "
                                 "BRAM36 for the P2 LCTX context RAM the mf48 "
                                 "calibration predates",
                                 "measured x1 (shared engine)"),
    "aaf_listener_ctx_extra": _cost(94, 98, 0, 0,
                                    "yosys OOC N=1->8 delta/7 of monitor_ctx"
                                    "+stream_table+pcm_route (79+5+10 LUT4, "
                                    "29+67+2 FF; LUT4:LUT6 1:1 = safe-side)",
                                    "shared-engine marginal (yosys-derived)"),
    "aaf_talker_engine": _cost(338, 645, 0, 0,
                               "arty mf48 row 'aaf_talker' (capture front-end "
                               "+ shared KL_aaf_packetizer, charged ONCE)",
                               "measured x1 (shared engine)"),
    "aaf_talker_ctx_extra": _cost(0, 31, 0.25, 0,
                                  "yosys OOC packetizer N=1->8: LUT SHRINKS "
                                  "(-28/ctx, staging+TCTX migrate to BRAM -> "
                                  "clamped 0), +31 FF, +0.43 BRAM16K = 0.25 "
                                  "BRAM36 per ctx (rounded up)",
                                  "shared-engine marginal (yosys-derived)"),
    "maap_claim_ctx": _cost(480, 267, 0, 0,
                            "arty mf48 row 'maap_engine' (KL_maap; ONE block "
                            "claim covers all N streams, NXN §3.3 - no "
                            "per-stream claim contexts)",
                            "measured x1 (shared engine)"),
    "maap_dmac_slot_extra": _cost(9, 2, 0, 0,
                                  "model: per-stream derived-DMAC adder slot "
                                  "(dmac = claimed_base + t; NXN §6 MAAP "
                                  "shared delta 60 LUT / 7 ctx)",
                                  "model (NXN §3.3)"),
    "acmp_listener_ctx": _cost(1569, 1527, 0, 0,
                               "arty mf48 row 'acmp_listener_sm' "
                               "(KL_acmp_lstn_ctx shared frame engine + ctx "
                               "RAM, charged ONCE)",
                               "measured x1 (shared engine)"),
    "acmp_lstn_ctx_extra": _cost(96, 0, 0, 0,
                                 "yosys OOC KL_acmp_lstn_ctx N_SINKS 1->8 "
                                 "delta/7 (+96 LUT4, FF flat)",
                                 "shared-engine marginal (yosys-derived)"),
    "lwsrp_attr_ctx": _cost(191, 36, 0, 0,
                            "yosys OOC per extra attribute lane: "
                            "KL_lwsrp_ctx (+14 LUT4) + ctx_tx (+125) + "
                            "walker key lane (+52); per context beyond "
                            "today's 1L+1T+CRF",
                            "shared-engine marginal (yosys-derived)"),
    "lwsrp_bw_slot_extra": _cost(97, 54, 0, 0,
                                 "yosys OOC KL_lwsrp_bw_gate (30-bit P12 "
                                 "trim) N_STREAMS 1->8 delta/7; per talker "
                                 "stream beyond 1",
                                 "shared-engine marginal (yosys-derived)"),
}


def resource_instances(cfg, overlay):
    """Ordered (module, instance-count) pairs for the config. Counts of 0
    drop out; l2_size_delta_4k may be negative (smaller L2 than the
    calibration build)."""
    L, T = len(cfg["listeners"]), len(cfg["talkers"])
    crf = 1 if cfg["clocking"]["crf_sink"] else 0
    clusters = overlay["descriptor_counts"]["AUDIO_CLUSTER"]
    return [
        ("soc_infra", 1),
        ("cpu_vexii", 1),
        ("l2_size_delta_4k",
         (cfg["constraints"]["l2_bytes"] - CAL_L2_BYTES) // 4096),
        ("traffic_controller", 1),
        ("aecp_entity", 1),
        ("aem_rom_extra_cluster", max(0, clusters - CAL_CLUSTERS)),
        ("crf_rx", crf),
        ("csr", 1),
        ("ptp_timestamp", 1),
        ("rx_filter", 1),
        ("i2s_renderer", 1),
        ("datapath_misc", 1),
        # P12 shared-engine scaling: engines charged ONCE, extra stream
        # contexts via the yosys-derived marginal rows
        ("aaf_listener_engine", min(L, 1)),
        ("aaf_listener_ctx_extra", max(0, L - 1)),
        ("aaf_talker_engine", min(T, 1)),
        ("aaf_talker_ctx_extra", max(0, T - 1)),
        ("maap_claim_ctx", min(T, 1)),
        ("maap_dmac_slot_extra", max(0, T - 1)),
        ("acmp_listener_ctx", min(L, 1)),
        ("acmp_lstn_ctx_extra", max(0, L - 1)),
        ("lwsrp_base", 1),
        ("lwsrp_attr_ctx", (L - 1) + (T - 1)),
        ("lwsrp_bw_slot_extra", max(0, T - 1)),
    ]


def resource_verdict(worst_pct):
    """Budget verdict vs the part: OK (<70%), TIGHT (70-80%, area-70
    directive), OVER (>80%)."""
    if worst_pct < VERDICT_OK_BELOW:
        return "OK"
    if worst_pct <= VERDICT_TIGHT_UPTO:
        return "TIGHT"
    return "OVER"


def estimate_resources(cfg, overlay):
    """Approximate LUT/FF/BRAM36/DSP estimate for the config vs xc7a100t.
    Deterministic; returns dict(items, totals, pct, worst, verdict,
    upper_bound)."""
    items, tot = [], {k: 0.0 for k in RESOURCE_CATS}
    upper = False
    for name, n in resource_instances(cfg, overlay):
        if n == 0:
            continue
        c = RESOURCE_COSTS[name]
        sub = {k: n * c[k] for k in RESOURCE_CATS}
        for k in RESOURCE_CATS:
            tot[k] += sub[k]
        ub = "UPPER BOUND" in c["confidence"] and \
            (n > 1 or name == "lwsrp_attr_ctx")
        upper = upper or ub
        items.append(dict(module=name, instances=n,
                          per_instance={k: c[k] for k in RESOURCE_CATS},
                          subtotal=sub, confidence=c["confidence"],
                          provenance=c["src"], upper_bound=ub))
    totals = {k: (round(tot[k], 2) if k == "bram36" else int(round(tot[k])))
              for k in RESOURCE_CATS}
    pct = {k: round(100.0 * tot[k] / PART_XC7A100T[k], 1)
           for k in RESOURCE_CATS}
    worst = max(RESOURCE_CATS, key=lambda k: pct[k])
    return dict(part="xc7a100t", part_budget=dict(PART_XC7A100T),
                items=items, totals=totals, pct=pct,
                worst_category=worst, worst_pct=pct[worst],
                verdict=resource_verdict(pct[worst]), upper_bound=upper)


def aaf_pcm32_48k(channels, ut=False):
    """AAF PCM 32-bit 48k-base stream format qword (channels at bits [31:22]
    of the low word; ut = bit 52 'up-to' family bit). Reproduces the
    gen_aem_store.py constants: 2ch=0x0205022000806000, 8ch=0x0205022002006000,
    ut8=0x0215022002006000."""
    base = 0x0205022000006000
    if ut:
        base |= 1 << 52
    return base | (channels << 22)


# --------------------------------------------------------------- validation --
def _req(d, key, ctx):
    if key not in d:
        raise ConfigError(f"{ctx}: missing required key '{key}'")
    return d[key]


def _eui64(v, ctx):
    try:
        n = int(str(v), 16)
    except ValueError:
        raise ConfigError(f"{ctx}: '{v}' is not a hex EUI-64")
    if not 0 <= n <= 0xFFFFFFFFFFFFFFFF:
        raise ConfigError(f"{ctx}: '{v}' out of EUI-64 range")
    return n


def _fmt64(v, ctx):
    n = _eui64(v, ctx)
    return f"0x{n:016X}"


def _pow2(v, ctx):
    if not (isinstance(v, int) and v > 0 and (v & (v - 1)) == 0):
        raise ConfigError(f"{ctx}: {v} must be a power of two")
    return v


def _streams(lst, ctx, direction):
    if not isinstance(lst, list) or not lst:
        raise ConfigError(f"{ctx}: needs at least one {direction} stream")
    if len(lst) > 16:
        raise ConfigError(f"{ctx}: {len(lst)} streams (max 16 per direction)")
    out = []
    for k, s in enumerate(lst):
        sctx = f"{ctx}[{k}]"
        ch = _req(s, "channels", sctx)
        if not (isinstance(ch, int) and 1 <= ch <= 32):
            raise ConfigError(f"{sctx}: channels {ch} outside 1..32")
        fmts = s.get("formats") or [f"0x{aaf_pcm32_48k(ch):016X}"]
        fmts = [_fmt64(f, f"{sctx}.formats") for f in fmts]
        clusters = s.get("clusters", ch)
        if not (isinstance(clusters, int) and 1 <= clusters <= 32):
            raise ConfigError(f"{sctx}: clusters {clusters} outside 1..32")
        # map_mode (gaps item 8): "dynamic" drops the port's static
        # AUDIO_MAP (1722.1-2021 7.2.13 number_of_maps=0) and arms the RTL
        # ADD/REMOVE/GET_AUDIO_MAP engine. RTL scope today: the FIRST
        # listener stream only (STREAM_PORT_INPUT[0]); talkers stay static.
        map_mode = s.get("map_mode", "static")
        if map_mode not in ("static", "dynamic"):
            raise ConfigError(f"{sctx}: map_mode '{map_mode}' not "
                              "static|dynamic")
        if map_mode == "dynamic" and (direction != "listener" or k != 0):
            raise ConfigError(f"{sctx}: map_mode dynamic is supported on "
                              "listeners[0] only (RTL engine scope)")
        map_page = s.get("map_page")
        if map_page is not None:
            if map_mode != "dynamic":
                raise ConfigError(f"{sctx}: map_page needs map_mode dynamic")
            if not (isinstance(map_page, int) and 1 <= map_page <= 11):
                raise ConfigError(f"{sctx}: map_page {map_page} outside "
                                  "1..11 (RTL GET scratch bound)")
        out.append(dict(
            name=s.get("name", f"Stream {'In' if direction == 'listener' else 'Out'} {k}"),
            channels=ch, formats=fmts, clusters=clusters,
            map_mode=map_mode, map_page=map_page,
            buffer_length_ns=s.get("buffer_length_ns", BUFLEN_DEFAULT_NS),
        ))
    return out


# --------------------------------------------------- cluster/port layout ----
def cluster_layout(listeners, talkers, policy, iface_channels):
    """USER decision: ONE STREAM_PORT per stream. Each listener stream gets a
    STREAM_PORT_INPUT, each talker stream a STREAM_PORT_OUTPUT; every port
    owns a contiguous AUDIO_CLUSTER block and exactly one AUDIO_MAP whose
    cluster offsets are RELATIVE to the port's base_cluster (1722.1-2021
    7.2.19). AUDIO_MAP descriptor indexes: input ports first (map i = port
    i), then output ports (map len(L)+j = port j).

    Cluster-count policy (USER decision, config-selectable):
      cluster-per-stream-channel - the stream's `clusters` field verbatim
        (default = channels; the legacy/pipewire-reference layout).
      cap-at-interface - min(clusters, physical interface channels/direction):
        clusters model real endpoints, never more than the wire has.
    Returns (ports_in, ports_out)."""
    if policy not in CLUSTER_POLICIES:
        raise ConfigError(f"cluster policy '{policy}' not in {CLUSTER_POLICIES}")

    def eff(s):
        if policy == "cap-at-interface":
            return min(s["clusters"], iface_channels)
        return s["clusters"]

    # map_mode dynamic (gaps item 8): the port carries NO AUDIO_MAP
    # (7.2.13 number_of_maps=0, base_map ignored) - static maps are
    # renumbered contiguously so the descriptor set stays gapless.
    ports_in, base, next_map = [], 0, 0
    for i, s in enumerate(listeners):
        n = eff(s)
        dyn = s.get("map_mode", "static") == "dynamic"
        ports_in.append(dict(index=i, stream_index=i, clusters=n,
                             base_cluster=base,
                             maps=0 if dyn else 1,
                             base_map=0 if dyn else next_map,
                             map_mode=s.get("map_mode", "static"),
                             map_page=s.get("map_page")))
        if not dyn:
            next_map += 1
        base += n
    ports_out = []
    for j, s in enumerate(talkers):
        n = eff(s)
        ports_out.append(dict(index=j, stream_index=j, clusters=n,
                              base_cluster=base, maps=1,
                              base_map=next_map + j))
        base += n
    return ports_in, ports_out


# ------------------------------------------------------------ lwSRP table ---
def srp_frame_geometry(channels, rate_hz, intervals_ps):
    """AAF-PCM32 frame geometry for ONE class-interval frame, from the
    KL_aaf_packetizer contract (its header states the identity: payload =
    SAMPLES_PER_FRAME x C x 4 octets, so the L2 frame is 42 + 24*C bytes at
    48 kHz - C=2 is the golden 90-byte shape the RTL byte-compare gate pins).

    MaxFrameSize for the MSRP TSpec is the AVTPDU (MSDU), never the L2
    frame: the 802.1Q idleSlope overhead of 42 already carries the Ethernet
    header + VLAN tag, so MaxFrameSize + 42 == the exact wire slot
    (preamble 8 + eth 14 + VLAN 4 + AVTPDU + FCS 4 + IPG 12)."""
    if rate_hz % intervals_ps:
        raise ConfigError(
            f"sampling_rate_hz {rate_hz} is not a whole number of samples "
            f"per class interval ({intervals_ps}/s) - no integer AAF frame")
    spf = rate_hz // intervals_ps
    payload = spf * channels * AAF_SAMPLE_OCTETS
    avtpdu = AVTP_AAF_HDR_BYTES + payload
    return dict(samples_per_frame=spf, payload_bytes=payload,
                avtpdu_bytes=avtpdu, l2_frame_bytes=L2_HDR_BYTES + avtpdu)


def srp_idle_slope_bps(max_frame_bytes, interval_frames, intervals_ps):
    """Class-A idleSlope, bits/s (802.1Q §34.3.1, LWSRP_FPGA_ARCHITECTURE §2 /
    KL_lwsrp_bw_gate): MaxIntervalFrames x (MaxFrameSize + 42) x 8 x 8000."""
    return interval_frames * (max_frame_bytes + SRP_FRAME_OVERHEAD_B) * 8 \
        * intervals_ps


def load_srp(raw, listeners, talkers, clocking, cons, binfo):
    """Validate + normalize the optional `srp:` section and resolve every
    per-stream TSpec. Raises ConfigError on a contradictory reservation
    (unknown SR class, illegal VID/queue, over-subscribed class-A ceiling)."""
    raw = raw or {}
    if not isinstance(raw, dict):
        raise ConfigError("srp: must be a mapping")
    tm = raw.get("timers_ms") or {}
    ts = raw.get("tspec") or {}
    if not isinstance(tm, dict) or not isinstance(ts, dict):
        raise ConfigError("srp.timers_ms / srp.tspec must be mappings")
    s = dict(SRP_DEFAULTS)
    for k in ("sr_class", "vid", "stream_dmac_base", "accumulated_latency_ns",
              "class_queue", "enable_at_reset", "talker_declare_at_reset",
              "bandwidth_limit_pct", "rtl_table"):
        if k in raw:
            s[k] = raw[k]
    for k, key in (("join", "join_time_ms"), ("leave", "leave_time_ms"),
                   ("leaveall", "leaveall_time_ms")):
        if k in tm:
            s[key] = int(tm[k])
    if "policy" in ts:
        s["tspec_policy"] = ts["policy"]
    if "max_frame_bytes" in ts:
        s["max_frame_bytes"] = int(ts["max_frame_bytes"])
    if "interval_frames" in ts:
        s["interval_frames"] = int(ts["interval_frames"])

    if s["sr_class"] not in SRP_SR_CLASSES:
        raise ConfigError(f"srp.sr_class '{s['sr_class']}' unknown - Milan "
                          f"v1.2 5.6 defines {sorted(SRP_SR_CLASSES)} for a "
                          "Milan end station")
    cls = SRP_SR_CLASSES[s["sr_class"]]
    if not (isinstance(s["vid"], int) and 1 <= s["vid"] <= 4094):
        raise ConfigError(f"srp.vid {s['vid']} outside 1..4094 (VID 0 is the "
                          "priority-tagged/no-VLAN encoding - an SR stream on "
                          "VID 0 floods UNSHAPED)")
    if not (isinstance(s["class_queue"], int)
            and 0 <= s["class_queue"] < (1 << SRP_QUEUE_BITS)):
        raise ConfigError(f"srp.class_queue {s['class_queue']} does not fit "
                          f"LWSRP_CTRL[4:2] ({SRP_QUEUE_BITS} bits)")
    if s["class_queue"] >= cons["num_queues"]:
        raise ConfigError(f"srp.class_queue {s['class_queue']} >= the board's "
                          f"{cons['num_queues']} shaper queues")
    if s["tspec_policy"] not in SRP_TSPEC_POLICIES:
        raise ConfigError(f"srp.tspec.policy '{s['tspec_policy']}' not in "
                          f"{SRP_TSPEC_POLICIES}")
    if not (isinstance(s["interval_frames"], int)
            and 1 <= s["interval_frames"] <= 0xFFFF):
        raise ConfigError(f"srp.tspec.interval_frames {s['interval_frames']} "
                          "outside 1..65535 (TSpec MaxIntervalFrames is 16 bit)")
    if not (isinstance(s["max_frame_bytes"], int)
            and 1 <= s["max_frame_bytes"] <= 0xFFFF):
        raise ConfigError(f"srp.tspec.max_frame_bytes {s['max_frame_bytes']} "
                          "outside 1..65535 (TSpec MaxFrameSize is 16 bit)")
    if not (isinstance(s["bandwidth_limit_pct"], int)
            and 1 <= s["bandwidth_limit_pct"] <= 100):
        raise ConfigError(f"srp.bandwidth_limit_pct {s['bandwidth_limit_pct']} "
                          "outside 1..100")
    dmac = _eui64(s["stream_dmac_base"], "srp.stream_dmac_base")
    if dmac > 0xFFFFFFFFFFFF:
        raise ConfigError(f"srp.stream_dmac_base {s['stream_dmac_base']} is "
                          "wider than a MAC-48")
    if not (dmac >> 40) & 1:
        raise ConfigError(f"srp.stream_dmac_base {s['stream_dmac_base']} is "
                          "not a MULTICAST address (I/G bit clear) - an AAF "
                          "stream DMAC must come from the MAAP range")
    lat = int(s["accumulated_latency_ns"])
    if not 0 <= lat <= 0xFFFFFFFF:
        raise ConfigError(f"srp.accumulated_latency_ns {lat} outside 32 bits")
    # LWSRP_CTRL[0] / [1] are SINGLE BITS of the reset word milan_csr.sv now
    # compiles in from the generated header; a non-boolean shifts straight
    # into the neighbouring field (2 << 1 lands in class_queue[0]) and would
    # be emitted without complaint.
    for k in ("enable_at_reset", "talker_declare_at_reset"):
        if not isinstance(s[k], bool):
            raise ConfigError(
                f"srp.{k} must be a boolean (got {s[k]!r}) - it is ONE BIT of "
                f"the LWSRP_CTRL reset word hdl/common/csr/milan_csr.sv "
                f"compiles in; any other value shifts into class_queue")
    if not isinstance(s["rtl_table"], bool):
        raise ConfigError(
            f"srp.rtl_table must be a boolean (got {s['rtl_table']!r}) - it "
            f"decides whether this config OWNS the tracked generated RTL "
            f"headers ({CSR_DEFAULTS_REL})")

    # ---- per-talker TSpec ------------------------------------------------
    rate = clocking["sampling_rate_hz"]
    rows, total_slope = [], 0
    for t, st in enumerate(talkers):
        geo = srp_frame_geometry(st["channels"], rate, cls["intervals_ps"])
        mf = geo["avtpdu_bytes"] if s["tspec_policy"] == "derived" \
            else s["max_frame_bytes"]
        if mf > 0xFFFF:
            raise ConfigError(f"streams.talkers[{t}]: derived MaxFrameSize "
                              f"{mf} exceeds the 16-bit TSpec field")
        slope = srp_idle_slope_bps(mf, s["interval_frames"],
                                   cls["intervals_ps"])
        total_slope += slope
        rows.append(dict(direction="talker", stream_index=t, name=st["name"],
                         channels=st["channels"], unique_id=t,
                         dest_mac=f"0x{dmac + t:012X}",
                         max_frame_bytes=mf,
                         interval_frames=s["interval_frames"],
                         latency_ns=lat, idle_slope_bps=slope,
                         l2_frame_bytes=geo["l2_frame_bytes"],
                         samples_per_frame=geo["samples_per_frame"]))
    # listener rows declare the Listener attribute; they reserve nothing
    for k, sl in enumerate(listeners):
        rows.append(dict(direction="listener", stream_index=k, name=sl["name"],
                         channels=sl["channels"], unique_id=None,
                         dest_mac=None, max_frame_bytes=0, interval_frames=0,
                         latency_ns=0, idle_slope_bps=0,
                         l2_frame_bytes=srp_frame_geometry(
                             sl["channels"], rate,
                             cls["intervals_ps"])["l2_frame_bytes"],
                         samples_per_frame=rate // cls["intervals_ps"]))

    link_bps = binfo["link_mbps"] * 1_000_000
    limit_bps = link_bps * s["bandwidth_limit_pct"] // 100
    if total_slope > limit_bps:
        raise ConfigError(
            f"class-{s['sr_class']} reservation {total_slope} bps over "
            f"{len(talkers)} talker stream(s) exceeds the "
            f"{s['bandwidth_limit_pct']}% ceiling of the "
            f"{binfo['link_mbps']} Mb/s port ({limit_bps} bps) - "
            "KL_lwsrp_bw_gate would refuse the excess streams (802.1Q "
            "34.3.1 / Milan v1.2 5.6). Reduce channels/streams or move the "
            "shape to a faster port.")

    s.update(
        class_id=cls["class_id"], priority=cls["priority"],
        intervals_ps=cls["intervals_ps"], rank=SRP_RANK,
        prio_rank=(cls["priority"] << 5) | (SRP_RANK << 4),
        stream_dmac_base=f"0x{dmac:012X}", accumulated_latency_ns=lat,
        rows=rows, total_idle_slope_bps=total_slope,
        limit_bps=limit_bps, link_bps=link_bps,
        utilization_pct=round(100.0 * total_slope / link_bps, 2),
        # KL_lwsrp_top ctx row map (REGISTER_MAP 0x800 window): listener k ->
        # row k, talker t -> row (L-1)+t, row 0 = the legacy pair. Available
        # rows = N_CTX_P, which milan_datapath sizes at 2*N_STREAMS-1 since
        # 2026-07-26 (it was max(L, T), which refused every t>0 talker row).
        ctx_rows_required=len(listeners) + len(talkers) - 1,
        ctx_rows_available=2 * max(len(listeners), len(talkers)) - 1,
    )
    if s["ctx_rows_required"] > (1 << SRP_CTX_IDX_BITS):
        raise ConfigError(
            f"{s['ctx_rows_required']} lwSRP attribute rows needed "
            f"(L+T-1) but ctx_idx is {SRP_CTX_IDX_BITS} bits = "
            f"{1 << SRP_CTX_IDX_BITS} rows max")
    return s


def srp_reset_words(cfg):
    """The 0x680 CSR group reset words this config implies. For a config with
    no `srp:` section these are EXACTLY the hand-written reset defaults in
    hdl/common/csr/milan_csr.sv (test gate 18a parses the RTL and compares)."""
    s = cfg["srp"]
    dmac = int(s["stream_dmac_base"], 16)
    return {
        "LWSRP_CTRL": (int(s["enable_at_reset"])
                       | (int(s["talker_declare_at_reset"]) << 1)
                       | (s["class_queue"] << 2)),
        "LWSRP_VID": s["vid"],
        "LWSRP_DMAC_LO": dmac & 0xFFFFFFFF,
        "LWSRP_DMAC_HI": (dmac >> 32) & 0xFFFF,
        "LWSRP_TSPEC": (s["interval_frames"] << 16) | s["max_frame_bytes"],
        "LWSRP_LATENCY": s["accumulated_latency_ns"],
    }


#: 0x680 group offsets, REGISTER_MAP.md "0x680 - lwSRP engine"
SRP_CSR_OFFSETS = {"LWSRP_CTRL": 0x680, "LWSRP_VID": 0x684,
                   "LWSRP_DMAC_LO": 0x688, "LWSRP_DMAC_HI": 0x68C,
                   "LWSRP_TSPEC": 0x690, "LWSRP_LATENCY": 0x6A0}

#: The values hdl/common/csr/milan_csr.sv carried as HAND-WRITTEN literals up
#: to and including 11944cd, before the include below made the config their
#: only source. Frozen here so the switch is provably a refactor: gate 20a
#: asserts emitted == frozen == the generated header == REGISTER_MAP, so a
#: config edit that would move a deployed reset word fails loudly instead of
#: silently re-elaborating the CSR block.
#: MOVED ONCE, DELIBERATELY (6-queue map, VERSION 0x0011): LWSRP_CTRL went
#: 0x0C -> 0x14 because the class-A queue field widened to [4:2] and its reset
#: moved from q3 to q5 - the queue the 802.1Q-ordered map puts SR class A on.
#: That is a REFLASH-VISIBLE change; every other word is untouched.
SRP_FROZEN_RESETS = {"LWSRP_CTRL": 0x00000014, "LWSRP_VID": 0x00000002,
                     "LWSRP_DMAC_LO": 0xF000FE01, "LWSRP_DMAC_HI": 0x000091E0,
                     "LWSRP_TSPEC": 0x000100E0, "LWSRP_LATENCY": 0x00000000}
SRP_FROZEN_PRIO_RANK = 0x70          #: milan_csr's old SRP_PRIO_RANK_C literal

#: Where milan_csr.sv `include-s the emitted CSR defaults from. The path is
#: RELATIVE TO hdl/common/csr (Verilator resolves `include against -I/+incdir
#: and the CWD only, never against the including file), which every consumer
#: already carries as an include dir - exactly like gen/aecp_aem_rom.svh.
CSR_DEFAULTS_INCLUDE = "gen/lwsrp_csr_defaults.svh"
CSR_DEFAULTS_REL = "hdl/common/csr/" + CSR_DEFAULTS_INCLUDE


def emit_lwsrp_table(cfg):
    """The lwSRP reservation table this config defines: SR-class + timer +
    bandwidth constants (today hand-written in lwsrp_pkg.sv), the 0x680 CSR
    reset words (today hand-written in milan_csr.sv), the RTL elaboration
    parameters, and one provisioning record per stream."""
    s = cfg["srp"]
    return {
        "_schema": LWSRP_SCHEMA_ID,
        "_schema_version": LWSRP_SCHEMA_VERSION,
        "_generated_by": "sw/builder/endstation_builder.py",
        "_source_config": cfg["source"],
        "csr_base": 0x680,
        "sr_class": dict(name=s["sr_class"], class_id=s["class_id"],
                         priority=s["priority"], rank=s["rank"],
                         prio_rank=s["prio_rank"],
                         intervals_per_second=s["intervals_ps"]),
        "domain": dict(vid=s["vid"], class_id=s["class_id"],
                       priority=s["priority"]),
        "timers_ms": dict(join=s["join_time_ms"], leave=s["leave_time_ms"],
                          leaveall=s["leaveall_time_ms"]),
        "bandwidth": dict(limit_pct=s["bandwidth_limit_pct"],
                          link_bps=s["link_bps"], limit_bps=s["limit_bps"],
                          total_idle_slope_bps=s["total_idle_slope_bps"],
                          utilization_pct=s["utilization_pct"],
                          frame_overhead_bytes=SRP_FRAME_OVERHEAD_B),
        "tspec_policy": s["tspec_policy"],
        "stream_dmac_base": s["stream_dmac_base"],
        "reset_words": {k: f"0x{v:08X}" for k, v in
                        srp_reset_words(cfg).items()},
        "csr_offsets": {k: f"0x{v:03X}" for k, v in SRP_CSR_OFFSETS.items()},
        "module_params": lwsrp_module_params(cfg),
        "ctx_rows": dict(required=s["ctx_rows_required"],
                         available=s["ctx_rows_available"],
                         index_bits=SRP_CTX_IDX_BITS,
                         row_map="listener k -> row k; talker t -> row "
                                 "(L-1)+t; row 0 = the legacy pair"),
        "rows": s["rows"],
    }


def lwsrp_module_params(cfg):
    """Item-4 subtask 3: the config values that ARE module parameters today
    (milan_datapath -> KL_lwsrp_top / milan_csr), emitted as one table so a
    hand edit on either side is visible. Gate 18c parses the RTL."""
    L, T = len(cfg["listeners"]), len(cfg["talkers"])
    return {
        "KL_lwsrp_top.CLK_FREQ_HZ_P": cfg["constraints"]["milan_clk_hz"],
        # N_CTX_P covers listener + talker attribute rows (L+T-1, and the
        # datapath sizes it 2*N_STREAMS-1); the bw-gate stays TALKER-wide so
        # aaf_stream_en_w still indexes by talker index.
        "KL_lwsrp_top.N_CTX_P": 2 * max(L, T) - 1,
        "KL_lwsrp_top.N_LISTENERS_P": max(L, T),
        "KL_lwsrp_top.N_TALKERS_P": max(L, T),
        "KL_lwsrp_bw_gate.N_STREAMS_P": max(L, T),
        "milan_datapath.N_STREAMS": max(L, T),
        "milan_datapath.MILAN_CLK_FREQ_HZ": cfg["constraints"]["milan_clk_hz"],
        "milan_csr.N_LISTENERS_P": L,
        "milan_csr.N_TALKERS_P": T,
        "milan_csr.NUM_QUEUES": cfg["constraints"]["num_queues"],
    }


def emit_lwsrp_svh(cfg, table):
    """SystemVerilog include with the lwSRP table constants. Include-only: it
    deliberately carries NO `default_nettype directive (that would leak into
    the including file's scope) and declares no nets."""
    s = cfg["srp"]
    ln = []
    a = ln.append
    a("// SPDX-FileCopyrightText: 2026 Kebag Logic")
    a("// SPDX-License-Identifier: CERN-OHL-W-2.0")
    a("//--------------------------------------------------------------------"
      "-------//")
    a("//  File        : lwsrp_table.svh")
    a("//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, Milan v1.2 "
      "5.6)")
    a("//")
    a("//  GENERATED by sw/builder/endstation_builder.py - DO NOT EDIT.")
    a(f"//  Source      : {cfg['source']}")
    a("//  Description : Deployment-variable half of the lwSRP contract - SR")
    a("//                class, MRP timers, bandwidth math and the 0x680 CSR")
    a("//                reset words - emitted from the declarative end-")
    a("//                station config so the config and the RTL can never")
    a("//                drift. Values are gated against the hand-written")
    a("//                hdl/ieee8021q/srp/lwsrp_pkg.sv and")
    a("//                hdl/common/csr/milan_csr.sv by")
    a("//                sw/builder/test_builder.py (gates 18a-18c).")
    a("//                Include-only: no `default_nettype directive (it would")
    a("//                leak into the includer's scope) and no net decls.")
    a("//--------------------------------------------------------------------"
      "-------//")
    a("")
    a("`ifndef LWSRP_TABLE_SVH")
    a("`define LWSRP_TABLE_SVH")
    a("")
    a("  //! SR class (Milan v1.2 5.6: class A only for a Milan end station)")
    a(f"  localparam [7:0] LWSRP_CLASS_ID_C   = 8'd{s['class_id']};")
    a(f"  localparam [7:0] LWSRP_CLASS_PRIO_C = 8'd{s['priority']};")
    a(f"  localparam       LWSRP_RANK_C       = 1'b{s['rank']};")
    a("  //! PriorityAndRank byte: priority[7:5], rank[4], reserved[3:0]")
    a(f"  localparam [7:0] LWSRP_PRIO_RANK_C  = 8'h{s['prio_rank']:02X};")
    a("")
    a("  //! MRP timers (802.1Q Table 10-7)")
    a(f"  localparam int unsigned LWSRP_JOIN_TIME_MS_C     = "
      f"{s['join_time_ms']};")
    a(f"  localparam int unsigned LWSRP_LEAVE_TIME_MS_C    = "
      f"{s['leave_time_ms']};")
    a(f"  localparam int unsigned LWSRP_LEAVEALL_TIME_MS_C = "
      f"{s['leaveall_time_ms']:_};")
    a("")
    a("  //! Class-A bandwidth math: idleSlope[bps] = MaxIntervalFrames x")
    a("  //! (MaxFrameSize + 42) x 8 x 8000")
    a(f"  localparam int unsigned LWSRP_FRAME_OVERHEAD_C = "
      f"{SRP_FRAME_OVERHEAD_B};")
    a(f"  localparam int unsigned LWSRP_INTERVALS_PS_C   = "
      f"{s['intervals_ps']};")
    a(f"  localparam int unsigned LWSRP_BW_LIMIT_PCT_C   = "
      f"{s['bandwidth_limit_pct']};")
    a(f"  //! {s['bandwidth_limit_pct']} % of the {s['link_bps'] // 1_000_000}"
      f" Mb/s port")
    a(f"  localparam int unsigned LWSRP_BW_LIMIT_BPS_C   = {s['limit_bps']};")
    a("")
    a("  //! 0x680 CSR group reset words (REGISTER_MAP.md '0x680 - lwSRP')")
    for k, v in srp_reset_words(cfg).items():
        a(f"  localparam [31:0] {k + '_RST_C':<21} = "
          f"32'h{v >> 16:04X}_{v & 0xFFFF:04X};"
          f"  //! 0x{SRP_CSR_OFFSETS[k]:03X}")
    a("")
    a("  //! Elaboration parameters milan_datapath passes to the engine")
    a(f"  localparam int unsigned LWSRP_N_CTX_C      = "
      f"{table['module_params']['KL_lwsrp_top.N_CTX_P']};")
    a(f"  localparam int unsigned LWSRP_CLK_FREQ_C   = "
      f"{table['module_params']['KL_lwsrp_top.CLK_FREQ_HZ_P']};")
    a("")
    a("  //! Reservation table: one entry per stream, TALKERS FIRST then")
    a("  //! listeners. The 0x800 window row map is listener k -> ctx row k,")
    a("  //! talker t -> ctx row (L-1)+t, ctx row 0 = the legacy pair, so a")
    a("  //! shape needs L+T-1 ctx rows against the N_CTX_P available.")
    a(f"  localparam int unsigned LWSRP_STREAMS_C    = {len(s['rows'])};")
    a(f"  localparam int unsigned LWSRP_ROWS_REQ_C   = "
      f"{s['ctx_rows_required']};")
    a(f"  localparam int unsigned LWSRP_ROWS_AVAIL_C = "
      f"{s['ctx_rows_available']};")
    a("  //! {dmac[119:72], prio_rank[71:64], max_frame[63:48],")
    a("  //! interval[47:32], latency[31:0]} - the KL_lwsrp_ctx record layout")
    a("  //! verbatim; listener entries carry zeros (their sid + DMAC arrive")
    a("  //! from the ACMP bind at run time).")
    a(f"  localparam [119:0] LWSRP_ROW_C [0:{len(s['rows']) - 1}] = '{{")
    for k, r in enumerate(s["rows"]):
        dm = int(r["dest_mac"], 16) if r["dest_mac"] else 0
        word = (dm << 72) | (s["prio_rank"] << 64) \
            | (r["max_frame_bytes"] << 48) | (r["interval_frames"] << 32) \
            | r["latency_ns"]
        tail = "," if k < len(s["rows"]) - 1 else ""
        a(f"    120'h{word:030X}{tail}  //! {r['direction']} "
          f"{r['stream_index']}: {r['channels']}ch, "
          f"slope {r['idle_slope_bps']} bps")
    a("  };")
    a("")
    a("`endif  // LWSRP_TABLE_SVH")
    a("")
    return "\n".join(ln)


def emit_csr_defaults_svh(cfg):
    """The CSR-facing SUBSET of the lwSRP table, as the SystemVerilog include
    hdl/common/csr/milan_csr.sv actually compiles (`include
    "gen/lwsrp_csr_defaults.svh"). Everything here was a hand-written literal
    in that file up to 11944cd; the config is the only source now.

    Deliberately a SUBSET, not emit_lwsrp_svh(): milan_csr consumes seven
    constants, and dragging the full table (SR class, MRP timers, the 120-bit
    per-stream row array) into the CSR block would put ~20 unused localparams
    and an unpacked array into every milan_csr elaboration. Both files are
    written from ONE config in ONE pass, and gate 20a compares them word for
    word, so the subset can never disagree with the table.

    Include-only, exactly like hdl/ieee17221/aecp/gen/aecp_aem_rom.svh: no
    `default_nettype (it would leak into the includer's scope), no include
    guard (these are MODULE-scope localparams - a second including module in
    the same compilation unit must get its own copy) and no net decls."""
    s = cfg["srp"]
    ln = []
    a = ln.append
    a("// SPDX-FileCopyrightText: 2026 Kebag Logic")
    a("// SPDX-License-Identifier: CERN-OHL-W-2.0")
    a("//--------------------------------------------------------------------"
      "-------//")
    a("//  File        : lwsrp_csr_defaults.svh")
    a("//  Project     : Milan FPGA Platform  (milan_csr 0x680 lwSRP group)")
    a("//")
    a("//  GENERATED by sw/builder/endstation_builder.py - DO NOT EDIT.")
    a(f"//  Source      : {cfg['source']}")
    a("//  Description : The 0x680 lwSRP CSR group's reset words and the")
    a("//                PriorityAndRank byte milan_csr.sv drives onto")
    a("//                o_srp_ctx_prio_rank. `include-d BY")
    a("//                hdl/common/csr/milan_csr.sv, so the declarative end-")
    a("//                station config IS these values rather than being")
    a("//                compared against a second hand-written copy.")
    a("//                Same values as the full table")
    a("//                hdl/ieee8021q/srp/gen/lwsrp_table.svh (one config,")
    a("//                one pass; test_builder gate 20a compares them).")
    a("//                Include-only: no `default_nettype directive (it would")
    a("//                leak into the includer's scope), no include guard")
    a("//                (module-scope localparams - each including module")
    a("//                needs its own copy, exactly like")
    a("//                gen/aecp_aem_rom.svh) and no net decls.")
    a("//--------------------------------------------------------------------"
      "-------//")
    a("")
    a("  //! PriorityAndRank for CSR-provisioned SRP rows (= lwsrp_pkg::")
    a("  //! SR_PRIO_RANK_C): priority[7:5], rank[4], reserved[3:0]")
    a(f"  localparam [7:0] LWSRP_PRIO_RANK_C = 8'h{s['prio_rank']:02X};")
    a("")
    a("  //! 0x680 group reset words (REGISTER_MAP.md '0x680 - lwSRP engine')")
    for k, v in srp_reset_words(cfg).items():
        a(f"  localparam [31:0] {k + '_RST_C':<21} = "
          f"32'h{v >> 16:04X}_{v & 0xFFFF:04X};"
          f"  //! 0x{SRP_CSR_OFFSETS[k]:03X}")
    a("")
    return "\n".join(ln)


def emit_interface_params(cfg):
    """The SV parameters `audio_interface` selects on the physical front-end.

    For the AES3/S-PDIF family this IS the config switch: one core
    (KL_aes3_rx / KL_aes3_tx) serves both transports, and the config decides
    CONSUMER_P (the channel-status dialect), WORD_BITS_P (what the link
    truncates to) and the serial clock the media clock implies. Returns None
    for the kinds whose front-end takes no config-driven parameters today.
    test_builder gate 21a parses the RTL and asserts these names and defaults
    are the ones the modules actually carry."""
    i = cfg["interface"]
    if i["rtl"] != "serdes":
        return None
    return {
        "family": "aes3",
        "kind": i["kind"],
        "rx_module": AES3_RX_MODULE,
        "tx_module": AES3_TX_MODULE,
        "params": {
            "CONSUMER_P": INTERFACES[i["kind"]]["consumer"],
            "WORD_BITS_P": i["word_length_bits"],
            "OVERSAMPLE_P": AES3_OVERSAMPLE,
            "LOCK_BLOCKS_P": AES3_LOCK_BLOCKS,
        },
        "serial_clk_hz": i["serial_clk_hz"],
        "serial_clk_div": i["serial_clk_div"],
        "block_frames": AES3_BLOCK_FRAMES,
        "testbench": "tb/verilator/aes3",
    }


# ------------------------------------------------------- platform / DT ------
def dma_window_map(dma_base, rx_queues):
    """The driver-visible DMA window map for `rx_queues`, in LiteX
    submodule-registration order (sw/litex/milan_soc.py MilanDMA.__init__).
    Returns an ORDERED dict name -> (base, size, in_dt). The 2-queue build
    inserts steer + rx1 (0x74 bytes) before `ts`, which is why every window
    from `ts` on moves - the 5ce9a13 CSR-rot bug in one function."""
    if rx_queues not in (1, 2):
        raise ConfigError(f"rx_queues {rx_queues} outside 1..2")
    m, off = {}, 0
    def add(name, size, in_dt):
        nonlocal off
        m[name] = dict(base=dma_base + off, size=size, in_dt=in_dt)
        off += size
    add("dma-tx", DMA_TX_BYTES, True)
    # the DT window is the extent kl-eth maps, the CSR block is wider
    m["dma-rx"] = dict(base=dma_base + off, size=DMA_RX_MAP_BYTES, in_dt=True,
                       block_size=DMA_RX_BLOCK_BYTES)
    off += DMA_RX_BLOCK_BYTES
    if rx_queues >= 2:
        add("steer", DMA_STEER_BYTES, False)
        add("dma-rx1", DMA_RX1_BLOCK_BYTES, False)
    add("dma-ts", DMA_TS_BYTES, True)
    add("hs-pgsz-cap", DMA_HS_CAP_BYTES, False)
    add("pcm-dma", DMA_PCM_BYTES, False)      # its own DT node, not the NIC's
    return m


def _mac48(v, ctx):
    """'02:00:00:00:00:02' or 0x020000000002 -> int, unicast + non-zero."""
    s = str(v).replace(":", "").replace("-", "").replace("_", "")
    try:
        n = int(s, 16)
    except ValueError:
        raise ConfigError(f"{ctx}: '{v}' is not a MAC-48")
    if not 0 < n <= 0xFFFFFFFFFFFF:
        raise ConfigError(f"{ctx}: '{v}' out of MAC-48 range (or all-zero)")
    if (n >> 40) & 1:
        raise ConfigError(f"{ctx}: '{v}' has the I/G bit set - a station MAC "
                          "must be UNICAST (it becomes the AVTP stream_id "
                          "prefix and the ATDECC entity_id)")
    return n


def load_platform(raw, cons, target, listeners):
    """Validate + normalize the `platform:` section and DERIVE the DMA window
    map from board.constraints.rx_queues. Raises ConfigError when the derived
    map contradicts `boot_chain_pin` - the flashed boot chain's map, which is
    exactly the 5ce9a13 failure caught before a build instead of after a
    flash."""
    raw = raw or {}
    if not isinstance(raw, dict):
        raise ConfigError("platform: must be a mapping")
    p = dict(PLATFORM_DEFAULTS)
    for k in PLATFORM_DEFAULTS:
        if k in raw:
            p[k] = raw[k]
    for k in ("csr_base", "dma_bank_base", "mac_bank_base", "ev_bank_base",
              "pcm_ring_phys", "pcm_ring_bytes", "pcm_ring_stride"):
        p[k] = int(p[k])
    if p["csr_base"] < 0x8000_0000:
        raise ConfigError(f"platform.csr_base 0x{p['csr_base']:08X} is below "
                          "0x80000000 - an MMIO peripheral must live in the "
                          "CPU IO region (REGISTER_MAP.md 'Bus')")
    if p["mac_address"] is None:
        raise ConfigError("platform.mac_address is required - two boards on "
                          "one AVB switch MUST NOT share a station MAC")
    mac = _mac48(p["mac_address"], "platform.mac_address")
    p["mac_address"] = ":".join(f"{(mac >> s) & 0xFF:02x}"
                                for s in range(40, -8, -8))
    if not (isinstance(p["interrupt"], int) and 0 <= p["interrupt"] < 32):
        raise ConfigError(f"platform.interrupt {p['interrupt']} outside the "
                          "PLIC's riscv,ndev = 32")
    _pow2(p["pcm_ring_bytes"], "platform.pcm_ring_bytes")
    _pow2(p["pcm_ring_stride"], "platform.pcm_ring_stride")
    if p["pcm_ring_stride"] * len(listeners) > p["pcm_ring_bytes"]:
        raise ConfigError(
            f"platform: {len(listeners)} capture stream(s) x stride "
            f"0x{p['pcm_ring_stride']:X} overruns the reserved PCM ring "
            f"(0x{p['pcm_ring_bytes']:X}) - snd-kl-milan would DMA past the "
            "no-map region")
    phy = DT_PHY_MODE.get(cons["phy"])
    if phy is None:
        raise ConfigError(f"platform: no DT phy-mode for board phy "
                          f"'{cons['phy']}' (known {sorted(DT_PHY_MODE)})")
    p["phy_mode"] = phy
    p["rsc_clk_mhz"] = cons["milan_clk_hz"] // 1_000_000
    if p["rsc_clk_mhz"] * 1_000_000 != cons["milan_clk_hz"]:
        raise ConfigError(
            f"platform: milan_clk_hz {cons['milan_clk_hz']} is not a whole "
            "MHz - kl,rsc-clk-mhz is an integer and the driver clamps it to "
            "10..250 (a wrong value runs the PHC at the wrong rate)")
    if not 10 <= p["rsc_clk_mhz"] <= 250:
        raise ConfigError(f"platform: kl,rsc-clk-mhz {p['rsc_clk_mhz']} "
                          "outside the driver's 10..250 accept window")
    p["windows"] = dma_window_map(p["dma_bank_base"], cons["rx_queues"])
    p["rx_queues"] = cons["rx_queues"]

    # CSR-rot guard: the flashed boot chain fixes its own window map. A pin
    # that the derived map contradicts means the DTB/opensbi on that board
    # would address the wrong registers - refuse to emit.
    pin = p["boot_chain_pin"]
    if pin is not None:
        if not isinstance(pin, dict):
            raise ConfigError("platform.boot_chain_pin must be a mapping of "
                              "window name -> address")
        for name, want in pin.items():
            if name not in p["windows"]:
                raise ConfigError(f"platform.boot_chain_pin: unknown window "
                                  f"'{name}' (known {sorted(p['windows'])})")
            got = p["windows"][name]["base"]
            if int(want) != got:
                raise ConfigError(
                    f"platform.boot_chain_pin['{name}'] = "
                    f"0x{int(want):08X} but rx_queues={cons['rx_queues']} "
                    f"puts it at 0x{got:08X}. The flashed boot chain "
                    f"(DTB + opensbi + kl-eth) maps this window BY ADDRESS: "
                    "changing rx_queues shifts every window from dma-ts on "
                    "by 0x74 and the host plane dies silently (the 5ce9a13 "
                    "CSR-rot rule). Rebuild the whole boot chain and move "
                    "the pin, or restore rx_queues.")
    return p


def emit_platform_shape(cfg):
    """The driver-visible layout this config implies: CSR base, the DMA
    window map, the queue count, and the physical addresses kl-eth hardcodes
    (they MOVE with rx_queues - the biggest un-modelled coupling)."""
    p, c = cfg["platform"], cfg["constraints"]
    w = p["windows"]
    return {
        "_schema": PLATFORM_SCHEMA_ID,
        "_schema_version": PLATFORM_SCHEMA_VERSION,
        "_generated_by": "sw/builder/endstation_builder.py",
        "_source_config": cfg["source"],
        "board": cfg["board_target"],
        "csr": dict(base=f"0x{p['csr_base']:08X}", size=MILAN_CSR_BYTES),
        "rx_queues": p["rx_queues"],
        "tx_queues": c["num_queues"],
        "shaped_queues": [0, 1],
        "phy_mode": p["phy_mode"],
        "rsc_clk_mhz": p["rsc_clk_mhz"],
        "hs_page_bytes": c["hs_page_bytes"],
        "mac_address": p["mac_address"],
        "interrupt": p["interrupt"],
        "windows": {k: dict(base=f"0x{v['base']:08X}",
                            size=f"0x{v['size']:X}",
                            in_device_tree=v["in_dt"])
                    for k, v in w.items()},
        "phy_window": dict(base=f"0x{p['mac_bank_base']:08X}",
                           size=f"0x{MAC_PHY_MAP_BYTES:X}"),
        # kl-eth.c hardcodes these; they are NOT in the DT and they shift
        # with rx_queues. Emitting them is the point of this table.
        "driver_constants": {
            "MILAN_EV_PHYS": f"0x{p['ev_bank_base']:08X}",
            "MILAN_PHY_CSR_PHYS": f"0x{p['mac_bank_base']:08X}",
            "MILAN_DMA_RX1_PHYS": (f"0x{w['dma-rx1']['base']:08X}"
                                   if "dma-rx1" in w else None),
            "MILAN_HS_PGSZ_CAP_PHYS": f"0x{w['hs-pgsz-cap']['base']:08X}",
        },
        "pcm": dict(base=f"0x{w['pcm-dma']['base']:08X}",
                    size=f"0x{w['pcm-dma']['size']:X}",
                    capture_streams=len(cfg["listeners"]),
                    playback_streams=0,
                    ring_phys=f"0x{p['pcm_ring_phys']:08X}",
                    ring_bytes=f"0x{p['pcm_ring_bytes']:X}",
                    ring_stride=f"0x{p['pcm_ring_stride']:X}"),
        "boot_chain_pin": ({k: f"0x{int(v):08X}"
                            for k, v in p["boot_chain_pin"].items()}
                           if p["boot_chain_pin"] else None),
    }


def emit_dt_overlay(cfg):
    """The device-tree nodes: ethernet@<csr_base> (kl,dma-ether), the PCM
    node (kl,milan-pcm) and its no-map reserved-memory region. Overlaid onto
    the LiteX base tree (litex_json2dts_linux) - the NIC/PCM nodes sit at the
    ROOT beside `soc`, which is why they carry an explicit interrupt-parent."""
    p, c = cfg["platform"], cfg["constraints"]
    w = p["windows"]
    ln = []
    a = ln.append
    a("// SPDX-License-Identifier: (GPL-2.0 OR MIT)")
    a("/*")
    a(" * Milan TSN NIC + PCM nodes - GENERATED by")
    a(" * sw/builder/endstation_builder.py. DO NOT EDIT BY HAND;")
    a(f" * edit {cfg['source']} and regenerate.")
    a(" *")
    a(f" * Board {cfg['board_target']}, rx_queues {p['rx_queues']}: the DMA")
    a(" * window map is a FUNCTION of the queue count (a 2-queue build")
    a(" * inserts steer + rx1 = 0x74 bytes before dma-ts). A DTB built")
    a(" * against the other count maps every window onto the wrong")
    a(" * registers - rebuild DTB + opensbi with the gateware.")
    a(" */")
    a("")
    a("/ {")
    a("\treserved-memory {")
    a("\t\t#address-cells = <1>;")
    a("\t\t#size-cells    = <1>;")
    a("\t\tranges;")
    a("")
    a(f"\t\tpcmring: pcmring@{p['pcm_ring_phys']:x} {{")
    a(f"\t\t\treg = <0x{p['pcm_ring_phys']:x} 0x{p['pcm_ring_bytes']:x}>;")
    a("\t\t\tno-map;")
    a("\t\t};")
    a("\t};")
    a("")
    a(f"\tmilan_nic: ethernet@{p['csr_base']:x} {{")
    a('\t\tcompatible = "kl,dma-ether-0.9", "kl,dma-ether";')
    a(f"\t\treg = <0x{p['csr_base']:x} 0x{MILAN_CSR_BYTES:x}>,"
      "        /* csr    control plane */")
    for name in ("dma-tx", "dma-rx", "dma-ts"):
        a(f"\t\t      <0x{w[name]['base']:x} 0x{w[name]['size']:x}>,"
          f"          /* {name} */")
    a(f"\t\t      <0x{p['mac_bank_base']:x} 0x{MAC_PHY_MAP_BYTES:x}>;"
      "           /* phy  crg_reset + MDIO */")
    a('\t\treg-names = "csr", "dma-tx", "dma-rx", "dma-ts", "phy";')
    a(f"\t\tinterrupt-parent = <&{p['interrupt_parent']}>;")
    a(f"\t\tinterrupts = <{p['interrupt']}>;")
    a('\t\tinterrupt-names = "csr";')
    if p["dma_coherent"]:
        a("\t\tdma-coherent;")
    a(f"\t\tkl,rsc-clk-mhz = <{p['rsc_clk_mhz']}>;"
      "\t/* datapath clock (PHC rate + RSC timing) */")
    a(f'\t\tphy-mode = "{p["phy_mode"]}";')
    a("\t\tlocal-mac-address = [" +
      " ".join(p["mac_address"].split(":")) + "];")
    a(f"\t\tkl,txq-cnt = <{c['num_queues']}>;")
    a(f"\t\tkl,rxq-cnt = <{p['rx_queues']}>;")
    a("\t\tkl,shaped-queues = <0 1>;")
    a("\t\tkl,ptp;")
    a('\t\tstatus = "okay";')
    a("\t};")
    a("")
    a(f"\tmilan_pcm: audio@{w['pcm-dma']['base']:x} {{")
    a('\t\tcompatible = "kl,milan-pcm-0.9", "kl,milan-pcm";')
    a(f"\t\treg = <0x{w['pcm-dma']['base']:x} "
      f"0x{w['pcm-dma']['size']:x}>,")
    a(f"\t\t      <0x{p['csr_base']:x} 0x1000>;")
    a('\t\treg-names = "pcm-dma", "milan-csr";')
    a("\t\tmemory-region = <&pcmring>;")
    a(f"\t\tkl,capture-streams = <{len(cfg['listeners'])}>;")
    a("\t\tkl,playback-streams = <0>;")
    a(f"\t\tkl,ring-stride = <0x{p['pcm_ring_stride']:x}>;")
    a('\t\tstatus = "okay";')
    a("\t};")
    a("};")
    a("")
    return "\n".join(ln)


# ------------------------------------------------------- model-id hashing ---
def model_shape(cfg):
    """The model-shaping fields ONLY (no board flags / names / serials): the
    input to the hash-derived entity_model_id. Any key added here changes
    every hash-derived id - extend deliberately."""
    i, clk = cfg["interface"], cfg["clocking"]
    shape = {
        "cluster_policy": i["cluster_policy"],
        "interface": {"kind": i["kind"], "channels": i["channels"],
                      "word_length_bits": i["word_length_bits"]},
        "rates_hz": clk["audio_unit_rates_hz"],
        "current_rate_hz": clk["sampling_rate_hz"],
        "crf_sink": clk["crf_sink"],
        "crf_format": clk["crf_format"],
        "crf_output": clk["crf_output"],
        "crf_output_format": clk["crf_output_format"],
        "listeners": [{"channels": s["channels"], "formats": s["formats"],
                       "clusters": s["clusters"],
                       "buffer_length_ns": s["buffer_length_ns"]}
                      for s in cfg["listeners"]],
        "talkers": [{"channels": s["channels"], "formats": s["formats"],
                     "clusters": s["clusters"]} for s in cfg["talkers"]],
        "ports_in": [[p["base_cluster"], p["clusters"], p["base_map"]]
                     for p in cfg["ports_in"]],
        "ports_out": [[p["base_cluster"], p["clusters"], p["base_map"]]
                      for p in cfg["ports_out"]],
    }
    # dynamic-map ports change the model (descriptor set + capabilities):
    # the key is CONDITIONAL so every existing static config's hash - and
    # therefore its derived entity_model_id - stays exactly what it was
    if any(p.get("map_mode", "static") == "dynamic" for p in cfg["ports_in"]):
        shape["dyn_maps_in"] = [
            [p.get("map_mode", "static"), p.get("map_page") or 0]
            for p in cfg["ports_in"]]
    return shape


def derive_model_id(shape):
    """Deterministic EUI-64 from the model shape (recipe in the module
    docstring + sw/builder/README-parameters.md)."""
    canon = json.dumps(shape, sort_keys=True, separators=(",", ":")).encode()
    top8 = int.from_bytes(hashlib.sha256(canon).digest()[:8], "big")
    mask = (1 << MODEL_ID_HASH_BITS) - 1
    return (MODEL_ID_OUI << MODEL_ID_HASH_BITS) | (top8 & mask)


def load_config(path):
    """Load + validate + normalize a YAML end-station config. Returns the
    normalized config dict; raises ConfigError on any violation."""
    with open(path) as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ConfigError(f"{path}: not a YAML mapping")

    if cfg.get("schema") != SCHEMA_ID:
        raise ConfigError(f"{path}: schema must be '{SCHEMA_ID}'")
    ver = str(cfg.get("schema_version", ""))
    if not ver.startswith(SCHEMA_MAJOR + "."):
        raise ConfigError(f"{path}: schema_version {ver} (need {SCHEMA_MAJOR}.x)")

    # entity (entity_model_id resolved AFTER streams/interface: hash needs
    # the derived layout)
    ent = _req(cfg, "entity", path)
    n = dict(
        name=_req(ent, "name", "entity"),
        vendor_name=ent.get("vendor_name", "Kebag Logic"),
        firmware_version=ent.get("firmware_version", "0.1.0"),
        serial_number=_req(ent, "serial_number", "entity"),
        group_name=ent.get("group_name", ""),
    )
    eid = ent.get("entity_id", "mac-derived")
    n["entity_id"] = eid if eid == "mac-derived" else _fmt64(eid, "entity.entity_id")
    for k in ("name", "serial_number", "group_name", "firmware_version"):
        if len(str(n[k]).encode()) > 63:
            raise ConfigError(f"entity.{k}: exceeds 63 bytes (AEM cstr64)")
    entity = n

    # board
    brd = _req(cfg, "board", path)
    target = _req(brd, "target", "board")
    if target not in BOARDS:
        raise ConfigError(f"board.target '{target}' not in {sorted(BOARDS)}")
    binfo = BOARDS[target]
    c = _req(brd, "constraints", "board")
    cons = dict(
        sys_clk_hz=int(c.get("sys_clk_hz", binfo["sys_clk_hz_default"])),
        milan_clk_hz=int(_req(c, "milan_clk_hz", "board.constraints")),
        l2_bytes=_pow2(_req(c, "l2_bytes", "board.constraints"),
                       "board.constraints.l2_bytes"),
        phy=_req(c, "phy", "board.constraints"),
        gtx_tx_invert=bool(c.get("gtx_tx_invert", False)),
        floorplan=bool(c.get("floorplan", False)),
        flashboot=c.get("flashboot", "full"),
        uart_baudrate=int(c.get("uart_baudrate", 115200)),
        rx_queues=int(c.get("rx_queues", 2)),
        num_queues=int(c.get("num_queues", 4)),
        hs_page_bytes=_pow2(c.get("hs_page_bytes", 16384),
                            "board.constraints.hs_page_bytes"),
        strip_probes=bool(c.get("strip_probes", True)),
        eth_port=c.get("eth_port"),
    )
    if cons["phy"] != binfo["phy"]:
        raise ConfigError(f"board.constraints.phy '{cons['phy']}' contradicts "
                          f"{target} ({binfo['phy']})")
    if cons["gtx_tx_invert"] and not binfo["gmii_knobs"]:
        raise ConfigError(f"gtx_tx_invert is a GMII knob; {target} is {binfo['phy']}")
    if cons["flashboot"] not in ("none", "kernel", "full"):
        raise ConfigError(f"flashboot '{cons['flashboot']}' not none|kernel|full")
    if not 1 <= cons["rx_queues"] <= 2:
        raise ConfigError(f"rx_queues {cons['rx_queues']} outside 1..2")
    # shaper queue count = ethernet_packet_pkg::NUMBER_OF_QUEUES; the CBS
    # tables (IDLE_SLOPE_*/HI_CREDIT/LO_CREDIT) are sized by it and the CSR
    # CAP[3:0] advertises it - a config that disagrees with the RTL package
    # would silently mis-size CLS_PRIO_REGEN and the class-A queue select.
    # NOT a power of two any more: the USER's egress map is SIX queues
    # (q5 class A .. q0 best effort, docs/reference/EGRESS_QUEUE_MAP.md). The
    # ceiling is what ceil(log2 N) can index inside one 32-bit
    # CLS_TC_QUEUE_MAP word (8 traffic classes x 4 bits), i.e. 16; the RTL
    # tables are written out to 6, so hold the gate at 8 until they grow.
    if not (isinstance(cons["num_queues"], int) and 1 <= cons["num_queues"] <= 8):
        raise ConfigError(f"num_queues {cons['num_queues']} outside 1..8")
    if not cons["milan_clk_hz"] <= cons["sys_clk_hz"]:
        raise ConfigError("milan_clk_hz must not exceed sys_clk_hz")
    if cons["eth_port"] is not None and cons["eth_port"] not in binfo["eth_ports"]:
        raise ConfigError(f"board.constraints.eth_port '{cons['eth_port']}' "
                          f"invalid for {target} (choices {binfo['eth_ports'] or '(none)'})")

    # clocking
    clk = _req(cfg, "clocking", path)
    rate = int(_req(clk, "sampling_rate_hz", "clocking"))
    if rate not in (48000, 96000, 192000):
        raise ConfigError(f"sampling_rate_hz {rate} not an AAF base rate")
    srcs = clk.get("media_clock_sources", ["internal", "input_stream", "crf"])
    bad = set(srcs) - {"internal", "input_stream", "crf"}
    if bad:
        raise ConfigError(f"media_clock_sources: unknown {sorted(bad)}")
    dflt = clk.get("default_source", srcs[0])
    if dflt not in srcs:
        raise ConfigError(f"default_source '{dflt}' not in media_clock_sources")
    co = clk.get("crf_output") or {}
    if not isinstance(co, dict):
        raise ConfigError("clocking.crf_output must be a mapping "
                          "(enabled + format)")
    clocking = dict(
        sampling_rate_hz=rate,
        audio_unit_rates_hz=[int(r) for r in
                             clk.get("audio_unit_rates_hz", [rate])],
        media_clock_sources=list(srcs),
        default_source=dflt,
        crf_sink=bool(clk.get("crf_sink", True)),
        crf_format=_fmt64(clk.get("crf_format", CRF_FORMAT_DEFAULT),
                          "clocking.crf_format"),
        crf_output=bool(co.get("enabled", False)),
        crf_output_format=_fmt64(co.get("format", CRF_FORMAT_DEFAULT),
                                 "clocking.crf_output.format"),
        audio_pll_hz=int(clk.get("audio_pll_hz", 24_576_000)),
    )
    if rate not in clocking["audio_unit_rates_hz"]:
        raise ConfigError("sampling_rate_hz must appear in audio_unit_rates_hz")
    if clocking["crf_sink"] and "crf" not in srcs:
        raise ConfigError("crf_sink needs 'crf' in media_clock_sources")

    # audio interface
    aif = _req(cfg, "audio_interface", path)
    kind = _req(aif, "kind", "audio_interface")
    if kind not in INTERFACES:
        raise ConfigError(f"audio_interface.kind '{kind}' not in {sorted(INTERFACES)}")
    iinfo = INTERFACES[kind]
    wl = int(aif.get("word_length_bits", 24))
    if wl not in iinfo["word_bits"]:
        raise ConfigError(f"word_length_bits {wl} invalid for {kind} "
                          f"(allowed {iinfo['word_bits']})")
    cm = aif.get("cluster_mapping") or {}
    if "rule" in cm:
        raise ConfigError("cluster_mapping.rule was replaced by "
                          "cluster_mapping.policy in schema 1.1 "
                          f"(choices {CLUSTER_POLICIES})")
    policy = cm.get("policy", "cluster-per-stream-channel")
    if policy not in CLUSTER_POLICIES:
        raise ConfigError(f"cluster_mapping.policy '{policy}' not in "
                          f"{CLUSTER_POLICIES}")
    interface = dict(
        kind=kind, channels=iinfo["channels"], word_length_bits=wl,
        cluster_policy=policy, rtl=iinfo["rtl"],
    )
    # AES3/S-PDIF: the serial clock is a HARD consequence of the media clock
    # (sampling_rate_hz x 128 UI/frame x OVERSAMPLE_P). A config whose audio
    # PLL cannot produce it would emit a KL_aes3_tx that transmits at the
    # wrong rate - refuse it here rather than on the bench.
    if iinfo["rtl"] == "serdes":
        need = rate * AES3_UI_PER_FRAME * AES3_OVERSAMPLE
        if clocking["audio_pll_hz"] % need:
            raise ConfigError(
                f"audio_interface.kind '{kind}' at {rate} Hz needs a serial "
                f"clock of {need} Hz (rate x {AES3_UI_PER_FRAME} UI/frame x "
                f"{AES3_OVERSAMPLE} oversample), which is not an integer "
                f"divide of clocking.audio_pll_hz {clocking['audio_pll_hz']}")
        interface["serial_clk_hz"] = need
        interface["serial_clk_div"] = clocking["audio_pll_hz"] // need

    # streams
    st = _req(cfg, "streams", path)
    listeners = _streams(_req(st, "listeners", "streams"), "streams.listeners",
                         "listener")
    talkers = _streams(_req(st, "talkers", "streams"), "streams.talkers",
                       "talker")

    # Milan 7.2.3 RULE (PDF-verified): "an AAF Media Listener with two or
    # more AAF Media Inputs shall implement a CRF Media Clock Output" (per
    # supported clock domain; we model one). The builder ENFORCES it: shapes
    # with >=2 AAF listener streams must enable clocking.crf_output.
    if len(listeners) >= 2 and not clocking["crf_output"]:
        raise ConfigError(
            f"{len(listeners)} AAF listener streams require a CRF Media "
            "Clock Output (Milan v1.2 7.2.3) - set clocking.crf_output: "
            "{enabled: true} (format defaults to the Milan 7.3.2 word "
            f"{CRF_FORMAT_DEFAULT})")

    # soc policy overrides
    soc = dict(SOC_DEFAULTS, **(cfg.get("soc") or {}))
    if soc["cpu"] not in ("vexiiriscv", "naxriscv"):
        raise ConfigError(f"soc.cpu '{soc['cpu']}' unknown")

    srp = load_srp(cfg.get("srp"), listeners, talkers, clocking, cons,
                   BOARDS[target])
    platform = load_platform(cfg.get("platform"), cons, target, listeners)

    out = dict(
        source=os.path.relpath(path, ROOT),
        name=os.path.splitext(os.path.basename(path))[0],
        entity=entity, board_target=target, constraints=cons,
        clocking=clocking, interface=interface,
        listeners=listeners, talkers=talkers, soc=soc, srp=srp,
        platform=platform,
    )

    # per-stream port layout (needed by the model-id hash and the overlay)
    out["ports_in"], out["ports_out"] = cluster_layout(
        listeners, talkers, policy, interface["channels"])

    # entity_model_id resolution: pin > hash-derived > literal
    shape = model_shape(out)
    hashed = derive_model_id(shape)
    raw = _req(ent, "entity_model_id", "entity")
    pin = ent.get("model_id_pin")
    if pin is not None:
        mid, src = _eui64(pin, "entity.model_id_pin"), "pin"
    elif raw == "hash-derived":
        mid, src = hashed, "hash"
    else:
        mid, src = _eui64(raw, "entity.entity_model_id"), "literal"
    entity["entity_model_id"] = f"0x{mid:016X}"
    out["model_id"] = dict(value=f"0x{mid:016X}", source=src,
                           hash=f"0x{hashed:016X}")
    return out


# ----------------------------------------------------- RTL capability marks --
def rtl_capability_marks(cfg):
    """(element, status, note) per config element; status is 'supported' or a
    'planned (...)' marker - NEVER an error (the builder validates NxN shapes,
    the RTL catches up in items 5/4-audio)."""
    marks = []
    n_l, n_t = len(cfg["listeners"]), len(cfg["talkers"])
    if n_l > RTL_TODAY["max_aaf_listeners"]:
        marks.append((f"{n_l} AAF listener streams",
                      "planned (item 5 - NxN AAF streams)",
                      f"RTL today: {RTL_TODAY['max_aaf_listeners']} AAF listener "
                      f"+ CRF sink; needs per-stream ACMP/MAAP/monitor contexts"))
    else:
        marks.append((f"{n_l} AAF listener stream(s)", "supported", ""))
    if n_t > RTL_TODAY["max_talkers"]:
        marks.append((f"{n_t} AAF talker streams",
                      "planned (item 5 - NxN AAF streams)",
                      f"RTL today: {RTL_TODAY['max_talkers']} talker"))
    else:
        marks.append((f"{n_t} AAF talker stream(s)", "supported", ""))
    if cfg["clocking"]["crf_sink"]:
        marks.append(("CRF media-clock sink", "supported", "KL_crf_rx"))
    if cfg["clocking"]["crf_output"]:
        marks.append(("CRF media-clock output (Milan 7.2.3)",
                      "planned (item 5 - NxN AAF streams)",
                      "model half DONE (CRF STREAM_OUTPUT advertised); the "
                      "fabric talker KL_crf_tx exists (CSR 0x750-0x764, "
                      "silicon-proven 500 PDU/s) - missing = S50 provisioning "
                      "+ ACMP talker context for the CRF stream (rides with "
                      "the item-5 NxN integration)"))
    kind = cfg["interface"]["kind"]
    if kind in RTL_TODAY["interfaces"]:
        marks.append((f"audio interface {kind}", "supported",
                      "KL_i2s_playback / aaf_talker_i2s" if kind == "i2s_philips"
                      else "KL_tdm_capture -> KL_aaf_packetizer multi-channel "
                           "payload (milan_soc.py --audio-interface)"))
    else:
        ip = emit_interface_params(cfg)
        marks.append((f"audio interface {kind} biphase-mark ser/des",
                      "supported",
                      f"{AES3_RX_MODULE} + {AES3_TX_MODULE}: recovered symbol "
                      f"clock, X/Y/Z subframe+block framing, P-parity and "
                      f"channel status, honest lock/error census "
                      f"(CONSUMER_P={ip['params']['CONSUMER_P']}, "
                      f"WORD_BITS_P={ip['params']['WORD_BITS_P']}, serial "
                      f"clock {ip['serial_clk_hz']} Hz); suite "
                      f"{ip['testbench']}"))
        marks.append((f"audio interface {kind} datapath integration",
                      "planned (item 4 subtask - AES3/S-PDIF SoC plumbing)",
                      "the ser/des RTL is landed and TB-proven; MISSING = the "
                      "milan_datapath front-end generate for the AES3 family "
                      "and the milan_soc.py --audio-interface value that "
                      "selects it (the tdm kinds' path, reused)"))
    rate = cfg["clocking"]["sampling_rate_hz"]
    if rate in RTL_TODAY["sampling_rates"]:
        marks.append((f"{rate} Hz media clock", "supported", ""))
    else:
        marks.append((f"{rate} Hz media clock",
                      "planned (item 6 - MMCM-DRP media-clock servo)",
                      "render path is 48k-only today"))
    # lwSRP attribute-context capacity. milan_datapath ties N_CTX_P to
    # N_STREAMS = max(L, T), but the 0x800 window row map needs L+T-1 rows
    # (listener k -> row k, talker t -> row (L-1)+t). Every NxN shape beyond
    # 1x1 therefore has more declarations than rows: talker gate bits and
    # listener rows collide. Surfaced here, not hidden.
    srp = cfg["srp"]
    if srp["ctx_rows_required"] > srp["ctx_rows_available"]:
        marks.append((f"{srp['ctx_rows_required']} lwSRP attribute rows "
                      f"(L+T-1) in {srp['ctx_rows_available']} contexts",
                      "planned (item 5 - NxN AAF streams)",
                      "KL_lwsrp_top N_CTX_P = milan_datapath N_STREAMS = "
                      "max(L,T), but the 0x800 window row map (listener k -> "
                      "row k, talker t -> row (L-1)+t) needs L+T-1; the "
                      "surplus listener declarations have no context row "
                      "until N_CTX_P is decoupled from N_STREAMS"))
    else:
        marks.append((f"{srp['ctx_rows_required']} lwSRP attribute row(s) in "
                      f"{srp['ctx_rows_available']} context(s)", "supported",
                      "KL_lwsrp_top ctx table"))
    # per-stream TSpec: CLOSED 2026-07-26. milan_datapath derives a talker
    # row's MaxFrameSize from that row's own TCTX w0 chans field, under the
    # same clamp KL_aaf_packetizer frames with, so the reservation and the
    # wire cannot disagree. MaxIntervalFrames stays shared on purpose - it is
    # an SR-class property, one value per config.
    if srp["tspec_policy"] == "derived" and \
            len({r["max_frame_bytes"] for r in srp["rows"]
                 if r["direction"] == "talker"}) > 1:
        marks.append(("per-stream TSpec (heterogeneous MaxFrameSize)",
                      "supported",
                      "each talker row derives 24 + 24*C from its own TCTX w0 "
                      "chans under the packetizer clamp; row 0 keeps "
                      "LWSRP_TSPEC verbatim (no-regression axiom)"))
    max_ch = max(s["channels"] for s in cfg["listeners"])
    if max_ch > RTL_TODAY["render_channels"] and kind in RTL_TODAY["interfaces"]:
        marks.append((f"{max_ch}ch listener formats on a "
                      f"{cfg['interface']['channels']}ch physical interface",
                      "supported",
                      "wire-truth 1-to-1 rule: physical channels bind in "
                      "order, extra stream channels render as virtual"))
    return marks


# ------------------------------------------------------------ soc_params ----
def _freq(hz):
    """Render a frequency the way the build scripts write it (83.333e6)."""
    return f"{hz / 1e6:g}e6"


def emit_board_opts(cfg):
    """The board-specific design-flag prefix of the argv = EXACTLY the OPTS
    string sw/litex/sweep.sh keeps per board (test-gated byte match)."""
    c, binfo = cfg["constraints"], BOARDS[cfg["board_target"]]
    opts = ["--board", cfg["board_target"]]
    if c["sys_clk_hz"] != binfo["sys_clk_hz_default"]:
        opts += ["--sys-clk-freq", _freq(c["sys_clk_hz"])]
    opts += ["--milan-clk-freq", _freq(c["milan_clk_hz"])]
    if c["gtx_tx_invert"]:
        opts += ["--gtx-tx-invert"]
    if c["floorplan"]:
        opts += ["--floorplan"]
    if c["eth_port"]:
        opts += ["--eth-port", c["eth_port"]]
    return opts


def emit_soc_argv(cfg):
    """The milan_soc.py DESIGN argv this config implies (flow flags -
    --build/--vivado-max-threads/--place-directive/--output-dir - are
    sweep.sh's business, not the end-station definition's)."""
    c, soc = cfg["constraints"], cfg["soc"]
    argv = list(emit_board_opts(cfg))
    argv += ["--cpu", soc["cpu"]]
    if soc["all_blocks"]:
        argv += ["--all-blocks"]
    if soc["coherent_dma"]:
        argv += ["--coherent-dma"]
    if c["flashboot"] != "none":
        argv += ["--with-spiflash", "--flashboot", c["flashboot"]]
    if soc["timing_opt"]:
        argv += ["--timing-opt"]
    argv += ["--l2-bytes", str(c["l2_bytes"])]
    argv += [f"--scala-args={a}" for a in soc["scala_args"]]
    argv += ["--uart-baudrate", str(c["uart_baudrate"])]
    argv += ["--rx-queues", str(c["rx_queues"])]
    if c["strip_probes"]:
        argv += ["--strip-probes"]
    argv += ["--hs-page-bytes", str(c["hs_page_bytes"])]
    argv += ["--cpu-count", str(soc["cpu_count"])]
    # NxN dataplane width (docs/NXN_ARCHITECTURE.md P0): milan_datapath
    # N_STREAMS = the wider of the two stream directions. Emitted only when
    # > 1 so the shipping 1x1 argv stays byte-identical (no-regression axiom).
    n_streams = max(len(cfg["listeners"]), len(cfg["talkers"]))
    if n_streams > 1:
        argv += ["--num-streams", str(n_streams)]
    # item-4 audio-interface family: the tdm kinds select the KL_tdm_capture
    # front-end generate (milan_datapath AUDIO_IF_SLOTS_P). Emitted only for
    # non-default kinds so the shipping i2s argv stays byte-identical;
    # aes3/spdif have no ser/des RTL yet (planned mark) and emit nothing.
    kind = cfg["interface"]["kind"]
    if kind in ("tdm8", "tdm16", "tdm32"):
        argv += ["--audio-interface", kind]
    return argv


# ------------------------------------------------------------ sweep opts ----
def emit_sweep_opts(cfg):
    """Shell fragment sourced by sw/litex/sweep.sh: the per-board design
    OPTS/L2, single-sourced from the end-station config. The inline case
    tables in sweep.sh are the FALLBACK only; the builder test gate asserts
    fragment == fallback byte-for-byte on the OPTS/L2 values."""
    opts = " ".join(emit_board_opts(cfg))
    return (
        "# GENERATED by sw/builder/endstation_builder.py - DO NOT EDIT.\n"
        f"# Board-level design OPTS/L2/RXQ for {cfg['board_target']} (from the\n"
        "# board.constraints of any configs/endstation_*.yaml of this board;\n"
        "# header kept config-agnostic so identical constraints emit\n"
        "# identical bytes). Sourced by sw/litex/sweep.sh when present; its\n"
        "# inline tables are the fallback. Regenerate:\n"
        "#   python3 sw/builder/endstation_builder.py <cfg.yaml>\n"
        f'OPTS="{opts}"\n'
        f"L2={cfg['constraints']['l2_bytes']}\n"
        f"RXQ={cfg['constraints']['rx_queues']}\n")


# ----------------------------------------------------------- aem_overlay ----
def emit_aem_overlay(cfg):
    """AEM model overlay: descriptor counts + per-descriptor content that the
    config controls, consumed by avdecc/gen_aem_store.py --overlay. Layout:
    ONE STREAM_PORT per stream (cluster_layout above); every port owns its
    cluster block + one AUDIO_MAP with port-relative cluster offsets
    (1722.1-2021 7.2.19). All input clusters precede all output clusters;
    physical interface channels bind in order to the first clusters of each
    direction (wire-truth rule)."""
    L, T, clk = cfg["listeners"], cfg["talkers"], cfg["clocking"]
    P_in, P_out = cfg["ports_in"], cfg["ports_out"]
    n_crf = 1 if clk["crf_sink"] else 0
    n_crf_out = 1 if clk["crf_output"] else 0
    in_clusters = sum(p["clusters"] for p in P_in)
    out_clusters = sum(p["clusters"] for p in P_out)

    stream_inputs = [dict(index=i, name=s["name"], kind="aaf",
                          channels=s["channels"], formats=s["formats"],
                          buffer_length_ns=s["buffer_length_ns"])
                     for i, s in enumerate(L)]
    if n_crf:
        stream_inputs.append(dict(index=len(L), name="CRF", kind="crf",
                                  channels=0, formats=[clk["crf_format"]],
                                  buffer_length_ns=BUFLEN_DEFAULT_NS))

    # CRF Media Clock OUTPUT (Milan 7.2.3): a STREAM_OUTPUT appended after
    # the AAF talkers, mirroring the CRF sink - no STREAM_PORT / cluster /
    # AUDIO_MAP (it carries no audio). Its CLOCK_DOMAIN relationship is the
    # STREAM descriptor's own clock_domain_index=0 (1722.1 7.2.6): 7.2.9.2
    # defines no OUTPUT_STREAM CLOCK_SOURCE type - an output distributes the
    # domain clock, it is not a selectable source of it, so the CLOCK_SOURCE
    # set (7.2.32 clock_sources) is unchanged.
    stream_outputs = [dict(index=i, name=s["name"], kind="aaf",
                           channels=s["channels"], formats=s["formats"])
                      for i, s in enumerate(T)]
    if n_crf_out:
        stream_outputs.append(dict(index=len(T), name="CRF", kind="crf",
                                   channels=0,
                                   formats=[clk["crf_output_format"]]))

    # CLOCK_SOURCE set mirrors media_clock_sources (internal first, then one
    # per AAF listener stream, then CRF - gen_aem_store order)
    clock_sources = []
    if "internal" in clk["media_clock_sources"]:
        clock_sources.append(dict(index=len(clock_sources), name="Internal",
                                  type="internal",
                                  location_type="CLOCK_SOURCE",
                                  location_index=len(clock_sources)))
    if "input_stream" in clk["media_clock_sources"]:
        for i in range(len(L)):
            nm = "Stream Clock" if len(L) == 1 else f"Stream Clock {i}"
            clock_sources.append(dict(index=len(clock_sources), name=nm,
                                      type="input_stream",
                                      location_type="STREAM_INPUT",
                                      location_index=i))
    if n_crf:
        clock_sources.append(dict(index=len(clock_sources), name="CRF Clock",
                                  type="crf",
                                  location_type="STREAM_INPUT",
                                  location_index=len(L)))

    # one AUDIO_MAP per STATIC port; rows = (stream_index, stream_channel,
    # cluster_offset RELATIVE to the port's base_cluster, cluster_channel).
    # map_mode dynamic ports (gaps item 8) emit NO map - their mappings are
    # runtime state behind ADD/REMOVE/GET_AUDIO_MAPPINGS (Milan 5.4.2.26-28).
    audio_maps = []
    for p in P_in:
        if p.get("map_mode", "static") == "dynamic":
            continue
        audio_maps.append(dict(
            index=p["base_map"], direction="input", port_index=p["index"],
            mappings=[[p["stream_index"], ch, ch, 0]
                      for ch in range(p["clusters"])]))
    for p in P_out:
        audio_maps.append(dict(
            index=p["base_map"], direction="output", port_index=p["index"],
            mappings=[[p["stream_index"], ch, ch, 0]
                      for ch in range(p["clusters"])]))
    audio_maps.sort(key=lambda m: m["index"])

    # overlay port entries: map_mode/map_page keys appear ONLY on dynamic
    # ports so every static config's overlay stays byte-identical
    def port_public(p):
        q = {k: p[k] for k in ("index", "stream_index", "clusters",
                               "base_cluster", "maps", "base_map")}
        if p.get("map_mode", "static") == "dynamic":
            q["map_mode"] = "dynamic"
            if p.get("map_page"):
                q["map_page"] = p["map_page"]
        return q
    P_in_pub = [port_public(p) for p in P_in]
    P_out_pub = [port_public(p) for p in P_out]

    return {
        "_schema": OVERLAY_SCHEMA_ID,
        "_schema_version": OVERLAY_SCHEMA_VERSION,
        "_generated_by": "sw/builder/endstation_builder.py",
        "_source_config": cfg["source"],
        "entity": cfg["entity"],
        "model_id": cfg["model_id"],
        "sampling_rates_hz": clk["audio_unit_rates_hz"],
        "current_sampling_rate_hz": clk["sampling_rate_hz"],
        "entity_counts": {
            "talker_stream_sources": len(T) + n_crf_out,
            "listener_stream_sinks": len(L) + n_crf,
        },
        "descriptor_counts": {
            "ENTITY": 1, "CONFIGURATION": 1, "AUDIO_UNIT": 1,
            "STREAM_INPUT": len(L) + n_crf,
            "STREAM_OUTPUT": len(T) + n_crf_out,
            "AVB_INTERFACE": 1,
            "CLOCK_SOURCE": len(clock_sources),
            "CLOCK_DOMAIN": 1, "CONTROL": 1, "LOCALE": 1, "STRINGS": 1,
            "STREAM_PORT_INPUT": len(P_in),
            "STREAM_PORT_OUTPUT": len(P_out),
            "AUDIO_CLUSTER": in_clusters + out_clusters,
            "AUDIO_MAP": len(audio_maps),   # dynamic ports carry none
        },
        "stream_inputs": stream_inputs,
        "stream_outputs": stream_outputs,
        "clock_sources": clock_sources,
        "stream_ports": {"input": P_in_pub, "output": P_out_pub},
        "audio_maps": audio_maps,
        "cluster_format": "MBLA-mono",
        "cluster_policy": cfg["interface"]["cluster_policy"],
        "physical_binding": {
            "interface": cfg["interface"]["kind"],
            "channels_per_direction": cfg["interface"]["channels"],
            "rule": "first-N-clusters-per-direction; extra stream channels "
                    "virtual, missing physical channels render 0 "
                    "(USER wire-truth 1-to-1 rule)",
        },
    }


# ------------------------------------------------------------- build plan ---
def emit_resource_section(est):
    """The '## Resource estimate' block of the build plan."""
    ln = []
    a = ln.append
    a("## Resource estimate (approximate, pre-Vivado)")
    a("")
    a("Per-module costs calibrated from the REAL arty mf48 hierarchical "
      "place report (cross-checked ax mf38); large blocks measured, "
      "small-module rows low-confidence. NxN scaling (P12): shared engines "
      "charged once at the measured x1, per-extra-context marginals derived "
      "from yosys OOC N=1->8 deltas of the merged engines (LUT4:LUT6 1:1 = "
      "safe-side; see sw/builder/README-parameters.md).")
    a("")
    a("| Module | Inst | LUT | FF | BRAM36 | DSP | Confidence |")
    a("|--------|------|-----|----|--------|-----|------------|")
    for it in est["items"]:
        s = it["subtotal"]
        a(f"| {it['module']} | {it['instances']} | {int(round(s['lut']))} "
          f"| {int(round(s['ff']))} | {s['bram36']:.2f} | {int(round(s['dsp']))} "
          f"| {it['confidence']} |")
    t, p = est["totals"], est["pct"]
    a(f"| **total** | | **{t['lut']}** | **{t['ff']}** | **{t['bram36']:.2f}** "
      f"| **{t['dsp']}** | |")
    a("")
    b = est["part_budget"]
    a(f"Budget vs {est['part']} ({b['lut']} LUT / {b['ff']} FF / "
      f"{b['bram36']} BRAM36 / {b['dsp']} DSP):")
    a("")
    for k, label in (("lut", "LUT"), ("ff", "FF"), ("bram36", "BRAM36"),
                     ("dsp", "DSP")):
        mark = "  <- worst" if k == est["worst_category"] else ""
        a(f"- {label}: {t[k]} / {b[k]} ({p[k]}%){mark}")
    a("")
    v = est["verdict"]
    if v == "OK":
        a(f"**Verdict: OK** (worst category {est['worst_category'].upper()} "
          f"{est['worst_pct']}% < {VERDICT_OK_BELOW:.0f}%).")
    elif v == "TIGHT":
        a(f"**Verdict: TIGHT** (worst category {est['worst_category'].upper()} "
          f"{est['worst_pct']}% in {VERDICT_OK_BELOW:.0f}-"
          f"{VERDICT_TIGHT_UPTO:.0f}%; area-70 directive: keep slice "
          "headroom - docs/findings area-70 campaign).")
    else:
        a(f"**Verdict: OVER** (worst category {est['worst_category'].upper()} "
          f"{est['worst_pct']}% > {VERDICT_TIGHT_UPTO:.0f}% of the part; "
          "expect placement/timing pain - area-70 directive).")
    if est["upper_bound"]:
        a("")
        a("**UPPER BOUND estimate:** rows marked UPPER BOUND charge today's "
          "single-instance module cost per instance (full replication, no "
          "sharing) because the NxN engines do not exist yet (item 5); the "
          "real cost will be lower where contexts share logic.")
    a("")
    return ln


def emit_lwsrp_section(cfg, lwsrp):
    """The '## lwSRP reservation table' block of the build plan."""
    s, b = cfg["srp"], lwsrp["bandwidth"]
    ln = []
    a = ln.append
    a("## lwSRP reservation table (802.1Q MSRP/MVRP, CSR 0x680)")
    a("")
    a(f"- SR class {s['sr_class']} (id {s['class_id']}, priority "
      f"{s['priority']}, rank {s['rank']}, PriorityAndRank "
      f"0x{s['prio_rank']:02X}), VID {s['vid']}, "
      f"stream DMAC base {s['stream_dmac_base']} (stream t = base + t)")
    a(f"- MRP timers: join {s['join_time_ms']} ms, leave "
      f"{s['leave_time_ms']} ms, leaveall {s['leaveall_time_ms']} ms")
    a(f"- TSpec policy `{s['tspec_policy']}`; idleSlope = "
      f"MaxIntervalFrames x (MaxFrameSize + "
      f"{b['frame_overhead_bytes']}) x 8 x {s['intervals_ps']}")
    a(f"- reserved {b['total_idle_slope_bps']} bps of "
      f"{b['link_bps']} bps ({b['utilization_pct']}% of the port; ceiling "
      f"{b['limit_pct']}% = {b['limit_bps']} bps)")
    a("")
    a("| Offset | Register | Reset word |")
    a("|--------|----------|------------|")
    for k, v in lwsrp["reset_words"].items():
        a(f"| `{lwsrp['csr_offsets'][k]}` | `{k}` | `{v}` |")
    a("")
    a("| Dir | Stream | Ch | DMAC | MaxFrameSize | IntervalFrames | "
      "idleSlope bps |")
    a("|-----|--------|----|------|--------------|----------------|"
      "---------------|")
    for r in lwsrp["rows"]:
        a(f"| {r['direction']} | {r['stream_index']} | {r['channels']} "
          f"| {r['dest_mac'] or '(ACMP bind)'} | {r['max_frame_bytes']} "
          f"| {r['interval_frames']} | {r['idle_slope_bps']} |")
    a("")
    cr = lwsrp["ctx_rows"]
    a(f"Attribute context rows: {cr['required']} required (L+T-1), "
      f"{cr['available']} available (`KL_lwsrp_top.N_CTX_P` = "
      "`milan_datapath.N_STREAMS`). Row map: " + cr["row_map"] + ".")
    a("")
    return ln


def emit_platform_section(shape):
    """The '## Platform shape (device tree + driver)' block."""
    ln = []
    a = ln.append
    a("## Platform shape (device tree + driver-visible layout)")
    a("")
    a(f"- Milan CSR window {shape['csr']['base']} "
      f"(0x{shape['csr']['size']:X} B), IRQ {shape['interrupt']}, "
      f"MAC {shape['mac_address']}, phy-mode `{shape['phy_mode']}`, "
      f"kl,rsc-clk-mhz {shape['rsc_clk_mhz']}")
    a(f"- RX DMA queues {shape['rx_queues']}, shaper queues "
      f"{shape['tx_queues']}, hs_page_bytes {shape['hs_page_bytes']}")
    a("")
    a("| Window | Base | Size | In device tree |")
    a("|--------|------|------|----------------|")
    for k, v in shape["windows"].items():
        a(f"| `{k}` | `{v['base']}` | `{v['size']}` | "
          f"{'yes' if v['in_device_tree'] else 'no'} |")
    a(f"| `phy` | `{shape['phy_window']['base']}` | "
      f"`{shape['phy_window']['size']}` | yes |")
    a("")
    a("Driver constants kl-eth.c hardcodes (NOT in the device tree - they "
      "move with rx-queues):")
    a("")
    for k, v in shape["driver_constants"].items():
        a(f"- `{k}` = {v or '(absent at 1 queue)'}")
    a("")
    if shape["boot_chain_pin"]:
        a("Flashed boot chain pinned to "
          + ", ".join(f"`{k}`={v}"
                      for k, v in shape["boot_chain_pin"].items())
          + " - the builder REFUSES a config whose rx-queues would move "
            "them (the 5ce9a13 CSR-rot rule).")
        a("")
    return ln


def emit_build_plan(cfg, argv, overlay, marks, est, lwsrp, shape):
    c, e, i = cfg["constraints"], cfg["entity"], cfg["interface"]
    ln = []
    a = ln.append
    a(f"# Build plan - {cfg['name']}")
    a("")
    a(f"Source config: `{cfg['source']}` "
      f"(schema {SCHEMA_ID} v{SCHEMA_MAJOR}.x)")
    a("Generated by sw/builder/endstation_builder.py - do not edit.")
    a("")
    a("## Entity")
    a("")
    a(f"- name: {e['name']}  (serial {e['serial_number']}, "
      f"fw {e['firmware_version']})")
    a(f"- entity_id: {e['entity_id']}, entity_model_id: {e['entity_model_id']} "
      f"({cfg['model_id']['source']}; shape hash {cfg['model_id']['hash']})")
    a("")
    a("## Board")
    a("")
    a(f"- target: {cfg['board_target']} ({c['phy']}), sys {_freq(c['sys_clk_hz'])} Hz"
      f" / milan {_freq(c['milan_clk_hz'])} Hz, L2 {c['l2_bytes']} B,"
      f" flashboot {c['flashboot']}"
      + (f", eth port {c['eth_port']}" if c["eth_port"] else ""))
    a("")
    a("## Clocking")
    a("")
    clk = cfg["clocking"]
    a(f"- media clock {clk['sampling_rate_hz']} Hz, sources "
      f"{clk['media_clock_sources']} (default {clk['default_source']}), "
      f"CRF sink {'on' if clk['crf_sink'] else 'off'}, audio PLL "
      f"{_freq(clk['audio_pll_hz'])} Hz")
    a("")
    a("## Audio interface")
    a("")
    a(f"- {i['kind']}: {i['channels']} ch/direction, {i['word_length_bits']}-bit"
      f" words, cluster policy {i['cluster_policy']}")
    ip = emit_interface_params(cfg)
    if ip:
        a(f"- ser/des: `{ip['rx_module']}` + `{ip['tx_module']}` "
          + ", ".join(f"`{k}={v}`" for k, v in ip["params"].items()))
        a(f"- serial clock: {ip['serial_clk_hz']} Hz "
          f"({clk['sampling_rate_hz']} Hz x {AES3_UI_PER_FRAME} UI/frame x "
          f"{AES3_OVERSAMPLE} oversample) = audio PLL / {ip['serial_clk_div']}")
    a("")
    a("## Streams")
    a("")
    a("| Dir | Index | Name | Channels | Clusters (cfg) | Formats |")
    a("|-----|-------|------|----------|----------------|---------|")
    for k, s in enumerate(cfg["listeners"]):
        a(f"| listener | {k} | {s['name']} | {s['channels']} | {s['clusters']} "
          f"| {', '.join(s['formats'])} |")
    if clk["crf_sink"]:
        a(f"| listener | {len(cfg['listeners'])} | CRF | - | - "
          f"| {clk['crf_format']} |")
    for k, s in enumerate(cfg["talkers"]):
        a(f"| talker | {k} | {s['name']} | {s['channels']} | {s['clusters']} "
          f"| {', '.join(s['formats'])} |")
    if clk["crf_output"]:
        a(f"| talker | {len(cfg['talkers'])} | CRF (Milan 7.2.3) | - | - "
          f"| {clk['crf_output_format']} |")
    a("")
    a("## Stream ports (one per stream)")
    a("")
    a("| Port | Stream | Clusters | base_cluster | AUDIO_MAP index |")
    a("|------|--------|----------|--------------|-----------------|")
    for p in cfg["ports_in"]:
        a(f"| STREAM_PORT_INPUT {p['index']} | STREAM_INPUT {p['stream_index']}"
          f" | {p['clusters']} | {p['base_cluster']} | {p['base_map']} |")
    for p in cfg["ports_out"]:
        a(f"| STREAM_PORT_OUTPUT {p['index']} | STREAM_OUTPUT {p['stream_index']}"
          f" | {p['clusters']} | {p['base_cluster']} | {p['base_map']} |")
    a("")
    a("## AEM descriptor counts")
    a("")
    a("| Descriptor | Count |")
    a("|------------|-------|")
    for t, n in overlay["descriptor_counts"].items():
        a(f"| {t} | {n} |")
    a("")
    a("## milan_soc.py parameter set")
    a("")
    a("```")
    a("python3 sw/litex/milan_soc.py " + " ".join(argv))
    a("```")
    a("")
    a("(design flags only - --build / --vivado-max-threads / --place-directive "
      "stay in sw/litex/sweep.sh; sweep.sh sources the generated "
      f"configs/generated/sweep_opts_{cfg['board_target']}.sh for OPTS/L2)")
    a("")
    ln.extend(emit_lwsrp_section(cfg, lwsrp))
    ln.extend(emit_platform_section(shape))
    ln.extend(emit_resource_section(est))
    a("## RTL capability")
    a("")
    a("| Element | Status | Note |")
    a("|---------|--------|------|")
    for el, status, note in marks:
        a(f"| {el} | {status} | {note} |")
    planned = [m for m in marks if m[1].startswith("planned")]
    a("")
    if planned:
        a(f"**{len(planned)} element(s) beyond current RTL - the config "
          "VALIDATES and the AEM overlay is complete, but gateware for the "
          "marked rows lands with the referenced roadmap items.**")
    else:
        a("**All elements buildable with today's RTL.**")
    a("")
    return "\n".join(ln)


# ------------------------------------------------------------------ driver --
def build(config_path, outdir=None):
    """Run the full pipeline for one config. Returns dict with the emitted
    paths + in-memory artifacts (for tests)."""
    cfg = load_config(config_path)
    argv = emit_soc_argv(cfg)
    overlay = emit_aem_overlay(cfg)
    lwsrp = emit_lwsrp_table(cfg)
    lwsrp_svh = emit_lwsrp_svh(cfg, lwsrp)
    csr_svh = emit_csr_defaults_svh(cfg)
    iparams = emit_interface_params(cfg)
    shape = emit_platform_shape(cfg)
    dtsi = emit_dt_overlay(cfg)
    marks = rtl_capability_marks(cfg)
    est = estimate_resources(cfg, overlay)
    plan = emit_build_plan(cfg, argv, overlay, marks, est, lwsrp, shape)
    sweep = emit_sweep_opts(cfg)

    outdir = outdir or os.path.join(HERE, "out")
    d = os.path.join(outdir, cfg["name"])
    os.makedirs(d, exist_ok=True)
    p_soc = os.path.join(d, "soc_params.json")
    with open(p_soc, "w") as f:
        json.dump({"milan_soc": "sw/litex/milan_soc.py", "argv": argv,
                   "_source_config": cfg["source"]}, f, indent=1)
        f.write("\n")
    p_ovl = os.path.join(d, "aem_overlay.json")
    with open(p_ovl, "w") as f:
        json.dump(overlay, f, indent=1)
        f.write("\n")
    p_plan = os.path.join(d, "build_plan.md")
    with open(p_plan, "w") as f:
        f.write(plan)
        f.write("\n")
    p_srp = os.path.join(d, "lwsrp_table.json")
    with open(p_srp, "w") as f:
        json.dump(lwsrp, f, indent=1)
        f.write("\n")
    p_srp_svh = os.path.join(d, "lwsrp_table.svh")
    with open(p_srp_svh, "w") as f:
        f.write(lwsrp_svh)
    p_csr_svh = os.path.join(d, "lwsrp_csr_defaults.svh")
    with open(p_csr_svh, "w") as f:
        f.write(csr_svh)
    p_shape = os.path.join(d, "platform_shape.json")
    with open(p_shape, "w") as f:
        json.dump(shape, f, indent=1)
        f.write("\n")
    p_dtsi = os.path.join(d, "milan-nic.dtsi")
    with open(p_dtsi, "w") as f:
        f.write(dtsi)
    # board-level sweep fragment: canonical location, shared by every config
    # of the board (content depends only on board constraints)
    gen_dir = os.path.join(ROOT, "configs/generated")
    os.makedirs(gen_dir, exist_ok=True)
    p_sweep = os.path.join(gen_dir, f"sweep_opts_{cfg['board_target']}.sh")
    with open(p_sweep, "w") as f:
        f.write(sweep)
    paths = dict(soc_params=p_soc, aem_overlay=p_ovl, build_plan=p_plan,
                 lwsrp_table=p_srp, lwsrp_svh=p_srp_svh,
                 csr_defaults_svh=p_csr_svh,
                 platform_shape=p_shape, dt_overlay=p_dtsi,
                 sweep_opts=p_sweep)
    # The TRACKED RTL headers: exactly one config (the DEPLOYED shape, marked
    # srp.rtl_table) owns them. lwsrp_table.svh is the full contract for the
    # srp tree; lwsrp_csr_defaults.svh is the subset milan_csr.sv COMPILES,
    # so a config edit re-elaborates the CSR block instead of drifting away
    # from it (test_builder 18a/18b/20a).
    if cfg["srp"]["rtl_table"]:
        gen_svh = os.path.join(ROOT, "hdl/ieee8021q/srp/gen/lwsrp_table.svh")
        os.makedirs(os.path.dirname(gen_svh), exist_ok=True)
        with open(gen_svh, "w") as f:
            f.write(lwsrp_svh)
        paths["rtl_lwsrp_svh"] = gen_svh
        csr_gen = os.path.join(ROOT, CSR_DEFAULTS_REL)
        os.makedirs(os.path.dirname(csr_gen), exist_ok=True)
        with open(csr_gen, "w") as f:
            f.write(csr_svh)
        paths["rtl_csr_defaults_svh"] = csr_gen
    return dict(cfg=cfg, argv=argv, overlay=overlay, marks=marks, plan=plan,
                resource_estimate=est, sweep_opts=sweep, lwsrp=lwsrp,
                lwsrp_svh=lwsrp_svh, csr_defaults_svh=csr_svh,
                interface_params=iparams,
                platform=shape, dt_overlay=dtsi, paths=paths)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("config", help="end-station YAML config")
    ap.add_argument("-o", "--outdir", default=None,
                    help="output root (default sw/builder/out/)")
    args = ap.parse_args()
    try:
        r = build(args.config, args.outdir)
    except ConfigError as e:
        sys.exit(f"CONFIG ERROR: {e}")
    n_planned = sum(1 for m in r["marks"] if m[1].startswith("planned"))
    print(f"[endstation_builder] {r['cfg']['name']}: "
          f"{len(r['cfg']['listeners'])}x{len(r['cfg']['talkers'])} AAF + "
          f"{'CRF' if r['cfg']['clocking']['crf_sink'] else 'no CRF'}, "
          f"{r['cfg']['interface']['kind']}, "
          f"{r['overlay']['descriptor_counts']['AUDIO_CLUSTER']} clusters "
          f"({r['cfg']['interface']['cluster_policy']}), "
          f"model_id {r['cfg']['entity']['entity_model_id']} "
          f"({r['cfg']['model_id']['source']}); "
          f"{n_planned} planned element(s); resources "
          f"{r['resource_estimate']['verdict']} "
          f"(worst {r['resource_estimate']['worst_category'].upper()} "
          f"{r['resource_estimate']['worst_pct']}%"
          + (", UPPER BOUND" if r["resource_estimate"]["upper_bound"] else "")
          + ")")
    for p in r["paths"].values():
        print(f"  wrote {os.path.relpath(p, ROOT)}")


if __name__ == "__main__":
    main()

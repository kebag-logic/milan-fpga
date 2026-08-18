#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
endstation_builder.py - software-defined Milan End-Station builder.

One declarative definition drives gateware elaboration, the AEM model, lwSRP
tables and the DT/driver shape consistently. The current compliance boundary
is recorded in docs/testing/MILAN_V12_AUDIT_2026-08-16.md. The emitted AEM
overlay is consumed by avdecc/gen_aem_store.py (--overlay), and
the emitted sweep_opts fragment is SOURCED by sw/litex/sweep.sh (single
source for the per-board design OPTS/L2).

WHAT THIS BUILDER STILL PUTS INTO THE RTL TREE (2026-08-12).  The IEEE
1722.1 / SRP control-plane RTL is DELETED (hdl/ieee17221/{aecp,acmp} and
hdl/ieee8021q/srp are gone; the protocol-processor submodule is the control
plane now).  Exactly TWO generated includes are still compiled:

  hdl/common/csr/gen/adp_shape_defaults.svh  - `include-d by BOTH
        hdl/milan/milan_datapath.sv and hdl/common/csr/milan_csr.sv.  It
        carries ADP_TALKER_SRC_C / ADP_LISTENER_SINK_C (which now also size
        the protocol processor's source/sink arrays), the two capability
        words, TALKER_WIRE_CHANS_C and ADP_GPTP_DOMAIN_C.  LOAD-BEARING.
  hdl/common/csr/gen/lwsrp_csr_defaults.svh  - still `include-d by
        milan_csr.sv for the 0x680 group's reset words and
        LWSRP_PRIO_RANK_C.  Those registers remain as an ABI (software can
        still write them) but drive NOTHING: the applicant is deleted.

The legacy AEM descriptor ROM is still generated as a readable model artifact,
but it is no longer compiled into RTL. The protocol processor serves
READ_DESCRIPTOR from a flat DRAM image instead. An explicit --write-fragment
or --write-rtl deployment ownership transfer generates that image, manifest,
map, and loader in the sibling rootfs overlay when the overlay is present.
An ordinary builder run does not touch that deployment overlay.

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
                      provisioning record per stream. REFERENCE ONLY since the
                      applicant was deleted: only the CSR-facing subset below
                      still reaches RTL. Kept because the 0x680 reset words
                      and the bandwidth arithmetic are derived here.
  aecp_aem_rom.svh  - legacy AEM descriptor ROM. Generated for model review,
                      not compiled and not served by the processor.
  platform_shape.json - driver-visible layout: Milan CSR base, the DMA window
  milan-nic.dtsi      map DERIVED from board.constraints.rx_queues, the
                      physical addresses kl-eth hardcodes, and the
                      kl,dma-ether / kl,milan-pcm device-tree nodes.
  build_plan.md     - human-readable build plan. Shapes beyond current RTL
                      capability (NxN streams, TDM/AES3/SPDIF interfaces,
                      non-48k rates) VALIDATE but are marked "planned".
  milan-entity.conf - the BOARD-SOFTWARE half of the identity: entity_id,
                      entity_model_id, stream counts and SR VID as shell
                      variables, sourced by the rootfs /etc/init.d/S50milan
                      before it programs 0x604/0x608/0x60C/0x610. Also
                      written into the buildroot rootfs overlay (see
                      ROOTFS_OVERLAY_ETC) by --write-rtl/--write-fragment.
Plus (repo-level, single-sourced so nothing can drift):
  configs/generated/sweep_opts_<board>.sh - shell fragment (OPTS/L2/RXQ)
                      sourced by sw/litex/sweep.sh; the inline tables there
                      are the loud FALLBACK only.
  <rootfs overlay>/etc/milan-entity.<board>.conf - the identity the flashed
                      board programs into the ADP/AEM CSRs. Same rule, same
                      moment: the config that owns the board's bitstream owns
                      its advertised identity.
  <rootfs overlay>/etc/milan-aem/aem_desc.{bin,json,map}
                    - the processor descriptor image, paired manifest, and
                      readable map. Written only by --write-fragment or
                      --write-rtl when the sibling overlay is present.
  hdl/common/csr/gen/lwsrp_csr_defaults.svh - the CSR-facing SUBSET of the
                      lwSRP table (0x680 reset words + the PriorityAndRank
                      byte), `include-d BY hdl/common/csr/milan_csr.sv: the
                      config IS those literals now, they are not copied into
                      RTL. Written by the one config carrying srp.rtl_table.
                      (Its sibling hdl/ieee8021q/srp/gen/lwsrp_table.svh is
                      NO LONGER WRITTEN - that whole directory is deleted.)
  hdl/common/csr/gen/adp_shape_defaults.svh - the ADVERTISED SHAPE, written
  configs/generated/<cfg>/gen/adp_shape_defaults.svh   only by --write-rtl
                      (tracked tree) and by every build of a configs/ config
                      (its own per-shape include dir, which Verilator suites
                      and Vivado builds point +incdir at).

Usage:
  python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml
  python3 sw/builder/endstation_builder.py <cfg.yaml> -o <outdir>
  python3 sw/builder/endstation_builder.py <cfg.yaml> --write-fragment
  python3 sw/builder/endstation_builder.py <cfg.yaml> --write-rtl

Schema summary (see the example configs for the annotated normative form):
  schema / schema_version      - "kebag-logic/milan-endstation-config" / 1.1.x
  entity:                      - identity: name, entity_model_id
                                 ("hash-derived" | EUI-64 hex), model_id_pin
                                 (optional EUI-64 hex override - pins the id
                                 of already-flashed silicon), entity_id
                                 ("mac-derived" | EUI-64 hex), vendor_name,
                                 serial_number, group_name, firmware_rev
                                 (optional int, default 0 - the third
                                 component of the DERIVED firmware_version;
                                 see rtl_firmware_version(). There is no
                                 entity.firmware_version key and declaring
                                 one is refused)
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
import re
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
OVERLAY_SCHEMA_VERSION = "2.2.0"     # 2.x: per-stream STREAM_PORT layout
                                     # 2.1: role-tagged cluster pools +
                                     #      per-cluster object_name (D8/D10)
                                     # 2.2: the "adp" identity block - the
                                     #      Table 7-2 fields the descriptor
                                     #      image must repeat

LWSRP_SCHEMA_ID = "kebag-logic/lwsrp-table"
LWSRP_SCHEMA_VERSION = "1.0.0"       # 1.x: SR class + 0x680 resets + rows

PLATFORM_SCHEMA_ID = "kebag-logic/platform-shape"
PLATFORM_SCHEMA_VERSION = "1.0.0"    # 1.x: DT node + driver-visible layout

# Base EUI-64 prefix for hash-derived entity_model_id values (see module
# docstring step 3). Schema-level constant: changing it re-identifies every
# hash-derived model - never change it casually.
MODEL_ID_OUI = 0x001BC5              # Kebag Logic vendor OUI (00-1B-C5)
MODEL_ID_HASH_BITS = 40              # EUI-64 bits taken from the sha256

CLUSTER_POLICIES = ("cap-at-interface", "cluster-per-stream-channel",
                    "role-pools")

#: D8 cluster ROLES. Every AUDIO_CLUSTER the builder emits carries one, and
#: the role is what names it (D10: "Input"/"Output" x N told a controller
#: nothing - a Hive operator could not tell the pilot tone from a dead TDM
#: slot from a loopback lane). The role is a MODEL fact derived from the
#: platform declaration, never a hardcoded pool:
#:   physical - a routed audio-interface channel (audio_interface.
#:              physical_channels, per direction). ZERO is a legal and
#:              important value: the AX7101 platform ships _connectors = []
#:              (sw/litex/platforms/alinx_ax7101.py), so milan_soc.py leaves
#:              i2s_pads = None and drives i_i2s_sdout_i = 0, and the TDM
#:              pins are tied off in the wrapper too ("neither board has a
#:              TDM header today", sw/litex/milan_soc.py) - the board has no
#:              audio input AT ALL and a "TDM16" physical pool on it would be
#:              an advertisement the fabric cannot back.
#:   virtual  - a cluster past the physical width under the legacy policies
#:              (wire-truth rule: extra stream channels are virtual, missing
#:              physical channels render 0).
#:   host     - a host (ALSA/PipeWire) lane channel for this port's stream.
#:   pilot    - the KL_tone_gen pilot, one cluster per talker port (D8).
#:   loopback - a RECEIVED stream channel offered back as a talker source
#:              (D8's stream-loopback lane; same media-clock domain, so
#:              coherent). On a board with no audio input this is the only
#:              source that can give a talker per-channel-distinct audio.
CLUSTER_ROLES = ("physical", "virtual", "host", "pilot", "loopback")

#: role -> AUDIO_CLUSTER object_name template (D10). {n} is the index WITHIN
#: the role segment; the physical/virtual names carry the interface label so
#: "TDM16 In 3" reads as the wire it is.
IFACE_LABEL = {"i2s_philips": "I2S", "tdm8": "TDM8", "tdm16": "TDM16",
               "tdm32": "TDM32", "aes3": "AES3", "spdif": "S/PDIF"}


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
    # the PROVEN rv32 CPU words (launch_x32f1 -> sweep.sh BASE, 08-05/06):
    # the rv64-era set (refill 8, rpt prefetch, 8/16 queues) lived on here
    # as a THIRD drifted copy after the sweep fix - one source now, and it
    # is the silicon-proven one
    scala_args=[
        "--lsu-l1-refill-count=2",
        "--l2-down-pending=4",
        "--l2-general-slots=8",
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
# was the single source of truth for what had been hand-written twice -
# hdl/ieee8021q/srp/lwsrp_pkg.sv (SR class + timers + bandwidth math) and the
# 0x680 CSR reset defaults in hdl/common/csr/milan_csr.sv.
# THE PACKAGE IS DELETED (2026-08-12) with the engine that compiled it. What
# survives is the 0x680 half: milan_csr.sv still `include-s the generated
# gen/lwsrp_csr_defaults.svh and still serves those words to software, so
# test_builder gate 18a still parses milan_csr and asserts the emission
# agrees. The SR-class / timer / bandwidth constants below now have no RTL
# comparand at all; they are held to the CLAUSE instead (gate 18b's Milan
# 4.3.3.2 worked examples), which is the only honest check left for them.

#: SR classes. Milan v1.2 §5.6 defines class A only for a Milan end station;
#: the table is keyed so a class-B RTL round has somewhere to land.
SRP_SR_CLASSES = {
    "A": dict(class_id=6, priority=3, intervals_ps=8000),
}
SRP_RANK = 1                      #: PriorityAndRank rank bit (emergency = 0)
AVTP_AAF_HDR_BYTES = 24           #: IEEE 1722-2016 Fig 26 AAF AVTPDU header
AAF_SAMPLE_OCTETS = 4             #: AAF format INT_32BIT (§7.3.5)
L2_HDR_BYTES = 18                 #: DA 6 + SA 6 + VLAN 4 + EtherType 2
#: MILAN v1.2 4.3.3.2 Table 4.4's mandated trailing octet. The table reads
#: MaxFrameSize = 24*N + 24 + 1 for AAF PCM32 48 kHz and its own note explains
#: why the byte is there: "One more byte is added to take the fact into
#: account, that the sampling clock of the PAAD may be a bit faster than the
#: nominal frequency". It is a DECLARATION headroom, not a byte on the wire -
#: so it belongs to max_frame_bytes and never to l2_frame_bytes.
MILAN_TSPEC_HEADROOM_B = 1
#: Milan v1.2 4.3.3.2's four-step bandwidth recipe, one constant per step -
#: the split hdl/ieee8021q/srp/lwsrp_pkg.sv used to carry as
#: MSRP_L2_OVERHEAD_C / MSRP_MIN_L2_BYTES_C / MSRP_WIRE_OVERHEAD_C for
#: KL_lwsrp_bw_gate to run. That package and that gate are DELETED, so these
#: three are now the ONLY copy. The split is kept anyway: folding steps 1 and
#: 3 into a single +42 drops step 2's clamp, which is right for every frame
#: big enough not to need it and wrong for the CRF Media Clock at
#: MaxFrameSize 29. test_builder gate 18d holds them to the clause's own
#: worked kb/s figures instead of to the deleted package.
SRP_L2_OVERHEAD_B = 22            #: step 1: eth hdr 14 + VLAN 4 + FCS 4
SRP_MIN_L2_BYTES_B = 68           #: step 2: minimum TAGGED frame, a CLAMP
SRP_WIRE_OVERHEAD_B = 20          #: step 3: preamble 8 + IPG 12
#: 802.1Q idleSlope overhead: preamble 8 + eth hdr 14 + VLAN 4 + FCS 4 + IPG 12
#: (= lwsrp_pkg::MSRP_FRAME_OVERHEAD_C). MaxFrameSize is therefore the MSDU
#: (the AVTPDU), NOT the L2 frame: MaxFrameSize + 42 = the full wire slot.
#: KEPT for the l2_frame_bytes reporting only - it is steps 1 and 3 ADDED
#: TOGETHER, and folding the recipe into it is precisely the bug 0x0020 took
#: out of the RTL: the fold silently deletes step 2's clamp, so every stream
#: short enough to be padded on the wire reserves less than it occupies.
SRP_FRAME_OVERHEAD_B = 42
SRP_CTX_IDX_BITS = 5              #: KL_lwsrp_top ctx_idx_i width -> 32 rows
                                  #: (widened 2026-08-05 with the dedicated
                                  #: listener-0 row, VERSION 0x0023)
#: MSRP TSpec MaxFrameSize of the CRF Media Clock Stream = the PADDED MSDU of
#: the tagged 60-octet frame KL_crf_tx builds (60 - 14 eth - 4 tag). It is NOT
#: the 28-octet CRF AVTPDU: the pad is on the wire and the bridge budgets for
#: it, so 42 + SRP_FRAME_OVERHEAD_B = the 84-octet wire slot the stream really
#: occupies. MaxIntervalFrames is 1, the floor a TSpec can express for a 2 ms
#: stream against class A's 125 us classMeasurementInterval.
#: MILAN v1.2 4.3.3.2 Table 4.4 row "CRF, 1 timestamp per PDU" states this
#: outright: MaxFrameSize = 28 + 1, the 28-octet CRF AVTPDU plus the same
#: headroom octet every row in the table carries. Declaring the PADDED MSDU
#: (42) instead was our own arithmetic standing in for the clause, and it
#: reserved 5376 kb/s where the table mandates 5632. The two stop being in
#: tension once the recipe keeps step 2: 29 clamps up to the 68-octet minimum
#: tagged frame -> an 88-octet wire slot, which covers the real 84.
CRF_SRP_MAXFRAME_B = 28 + MILAN_TSPEC_HEADROOM_B
SRP_QUEUE_BITS = 3                #: LWSRP_CTRL[4:2] class-A queue select
#: (widened from [3:2] with the 802.1Q-order map: class A lives on the TOP
#: queue, q4 at NUMBER_OF_QUEUES = 5. The field keeps 3 bits at N=5 because
#: ceil(log2 5) is still 3 - so it can still name queues that do not exist,
#: which is why milan_datapath gates the slope MUX on qidx < NUM_QUEUES.)

#: lwSRP policy defaults = EXACTLY today's RTL reset words, so a config with
#: no `srp:` section emits the deployed gateware bit-for-bit (the
#: no-regression axiom this builder follows everywhere else).
SRP_DEFAULTS = dict(
    sr_class="A",
    vid=2,                                   # USER: VID 2 is THE SR vid
    stream_dmac_base="0x91E0F000FE01",       # MAAP range; stream t = base + t
    accumulated_latency_ns=0,
    class_queue=4,                           # reset PCP3 -> TC3 -> q4 map
                                             # (802.1Q order: q4 = class A)
    enable_at_reset=False,
    talker_declare_at_reset=False,
    bandwidth_limit_pct=75,                  # Milan §5.6 / 802.1Q §34.3.1
    # MILAN v1.2 4.2.7.1.1 Table 4.3, which SUPERSEDES 802.1Q Table 10-7 for a
    # PAAD: LeaveTime is 5000 ms, not the base standard's 600. These words are
    # emitted into lwsrp_csr_defaults.svh and programmed into the engine, so
    # leaving 600 here would have quietly overridden the RTL reset the MRP
    # timer round corrected - the generated default wins over the localparam.
    join_time_ms=200,
    leave_time_ms=5_000,
    leaveall_time_ms=10_000,
    tspec_policy="pinned",                   # pinned | derived
    max_frame_bytes=224,                     # pinned only (the 0x690 reset)
    interval_frames=1,
    rtl_table=False,                         # write the tracked hdl/ .svh
)
SRP_TSPEC_POLICIES = ("pinned", "derived")

#: `srp.stream_dmac_base: maap` means the stream destination addresses are
#: ALLOCATED AT RUN TIME by the MAAP engine rather than provisioned here. It
#: is the only value that makes KL_maap load-bearing, and therefore the only
#: value that forbids `board.features.maap: false`.
SRP_DMAC_DYNAMIC = "maap"

# ------------------------------------------------- optional-block features --
# docs/design/AREA_BUDGET.md tier 1: blocks a deployment may not be able to
# use, each behind an ELABORATION-TIME milan_datapath parameter. The config
# key is `board.features.<name>`; EVERY ONE DEFAULTS TO true = PRESENT, so a
# config that omits the whole block emits exactly today's argv and today's
# gateware (the no-regression axiom).
#
#   name -> (milan_soc.py flag, milan_datapath parameter, one-line summary)
#
# The flag is emitted by emit_soc_argv ONLY when the feature is false, so a
# default config's argv is byte-identical to what sweep.sh carries.
OPTIONAL_BLOCKS = {
    "media_clock_servo": ("--no-media-clock-servo", "MCSERVO_P",
                          "KL_mmcm_drp_servo - the audio-MMCM media-clock "
                          "actuator (CRF / input-stream recovery)"),
    "latency_taps":      ("--no-latency-taps", "LTAP_P",
                          "KL_aaf_latency_taps - the per-stage AAF latency "
                          "instrumentation behind CSR 0x870-0x8B0"),
    "maap":              ("--no-maap", "MAAP_P",
                          "KL_maap - IEEE 1722 Annex B dynamic stream-DMAC "
                          "allocation and defence"),
    "i2s_playback":      ("--no-i2s-playback", "I2SPB_P",
                          "KL_i2s_playback - the DAC serializer and its "
                          "rate servo"),
    "rx_mac_filter":     ("--no-rx-mac-filter", "RXFILT_P",
                          "rx_mac_filter + tcam - the RX station-address / "
                          "dest-MAC filter"),
    "render_lpf":        ("--no-render-lpf", "LPF_P",
                          "KL_pcm_lpf - the 2nd-order Butterworth on the DAC "
                          "render tap"),
    "datapath_probes":   ("--no-datapath-probes", "DPROBES_P",
                          "the APRB + PBK probe groups (0x8B4-0x8D0) - "
                          "closed-finding diagnostics"),
}

#: Where the RX destination-address decision is taken. `hardware` (the
#: default, and what both boards ship) REQUIRES rx_mac_filter; the other two
#: are the honest declarations that let it be pruned. This key exists so that
#: pruning the filter is a stated deployment property rather than a silent
#: change of what the port accepts.
RX_ADDRESS_FILTERS = ("hardware", "software", "promiscuous")

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

#: Revision of the AEM descriptor BYTE LAYOUT, an input to every hash-derived
#: entity_model_id (see model_shape). 1 was the IEEE 1722.1-2013 layout this
#: project shipped until 2026-08-13; 2 is 1722.1-2021, which Milan v1.2 clause
#: 2 is what normatively binds: STREAM_INPUT/OUTPUT gained redundant_offset,
#: number_of_redundant_streams and timing (formats_offset 132 -> 138, §7.2.6
#: Table 7-8) and AVB_INTERFACE gained number_of_controls and base_control
#: (98 -> 102 octets, §7.2.8 Table 7-13).
#:
#: 3 (2026-08-14) finishes that move. AUDIO_CLUSTER was left on the 2013 length
#: when the rest went to 2021: 1722.1-2013 Table 7.27 ends at `format`, offset
#: 86, for 87 octets, and 1722.1-2021 Table 7-27 ADDS aes3_data_type_reference
#: (offset 87, length 1) and aes3_data_type (offset 88, length 2) for 90. The
#: descriptor had been truncated deliberately, under a code comment citing 2021
#: for the opposite of what 2021 says, to silence a trace-level "Remaining
#: bytes in buffer" line from la_avdecc - whose own constant is the 2013 one
#: and whose length test is a minimum, so the surplus was never an error.
#:
#: THIS IS WHY THE REVISION EXISTS. A hash-derived entity_model_id is taken
#: over the config SHAPE (stream counts, rates, names), so a change to the
#: emitted descriptor BYTES is invisible to it: the model would change while
#: its id did not, which is exactly the stale-controller-cache failure
#: 1722.1-2021 §6.2.2.8 forbids. Bumping this number is what makes a layout
#: change reach every id.
AEM_LAYOUT_REV = 3

#: DRAM the protocol processor owns: the AEM descriptor image it serves
#: READ_DESCRIPTOR from, plus the AECP response buffer it writes. Sized for
#: headroom rather than fit - the largest entity model this project builds is
#: 23,216 bytes at the 8x8 shape, and DRAM is the resource this design has to
#: spare (the die does not: the response buffer held as fabric flops was
#: 5,079 FF and it was those flops that failed placement).
PP_MEM_BYTES = 0x10_0000

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
    rx_address_filter="hardware",            # hardware | software | promiscuous
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
                                   "cluster beyond 16 (tracked ROM = 3675 B "
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
    # -- optional-block prunes (docs/design/AREA_BUDGET.md tier 1) ------------
    # THREE of the six blocks already have POSITIVE rows above (`rx_filter`,
    # `i2s_renderer`, `maap_claim_ctx` + `maap_dmac_slot_extra`), all of them
    # Vivado-derived; pruning those simply counts the existing row 0, which is
    # more accurate than subtracting a yosys number from a Vivado one.
    # The three rows below are for blocks this table never charged for:
    # the servo and the taps are MISSING from it entirely, and the render LPF
    # is folded inside `aaf_listener_engine`. They are SUBTRACTIVE and counted
    # 1 only when board.features prunes the block, so a default config counts
    # them 0 and its estimate is BYTE-IDENTICAL to what this table produced
    # before they existed - the gate-11 calibration against the real mf48
    # place report is untouched by them.
    #
    # Figures = yosys ESTIMATES, not placement results: synth_xilinx -family
    # xc7 with HIERARCHY PRESERVED on milan_datapath at the ship shape
    # (N_STREAMS=8, AUDIO_IF_SLOTS_P=16), per-module `stat`, 2026-07-27.
    # The whole-design `-flatten` delta was rejected for two of these six:
    # it reports the flip-flop total as BIT-IDENTICAL after removing blocks
    # that elaboration shows carry 1691 and 756 flops, which cannot be a
    # measurement. See AREA_BUDGET.md "Which method to trust".
    "prune_media_clock_servo": _cost(-814, -789, 0, -1,
                                     "yosys hier OOC: KL_mmcm_drp_servo 807/745"
                                     "/1DSP + cdc_handshake 5/40 + cdc_pulse "
                                     "2/4 (ESTIMATE, 2026-07-27)",
                                     "measured (yosys hierarchical ESTIMATE)"),
    "prune_latency_taps": _cost(-948, -614, 0, 0,
                                "yosys hier OOC: KL_aaf_latency_taps 0/32 + "
                                "2 x KL_aaf_latency_chain 474/291 (ESTIMATE, "
                                "2026-07-27)",
                                "measured (yosys hierarchical ESTIMATE)"),
    "prune_render_lpf": _cost(-864, -756, 0, -1,
                              "yosys hier OOC: KL_pcm_lpf 864/756/1DSP "
                              "(ESTIMATE, 2026-07-27). The shipping Vivado "
                              "place report prices the same block at 428-445 "
                              "LUT / 756 FF - the FF figures agree exactly, "
                              "the LUT figure is yosys running ~2x high",
                              "measured (yosys hierarchical ESTIMATE)"),
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
        # tier-1 prunes with an EXISTING Vivado-derived row: pruning counts
        # the row 0 rather than subtracting a yosys figure from a Vivado one
        ("rx_filter", 1 if cfg["features"]["rx_mac_filter"] else 0),
        ("i2s_renderer", 1 if cfg["features"]["i2s_playback"] else 0),
        ("datapath_misc", 1),
        # P12 shared-engine scaling: engines charged ONCE, extra stream
        # contexts via the yosys-derived marginal rows
        ("aaf_listener_engine", min(L, 1)),
        ("aaf_listener_ctx_extra", max(0, L - 1)),
        ("aaf_talker_engine", min(T, 1)),
        ("aaf_talker_ctx_extra", max(0, T - 1)),
        ("maap_claim_ctx", min(T, 1) if cfg["features"]["maap"] else 0),
        ("maap_dmac_slot_extra",
         max(0, T - 1) if cfg["features"]["maap"] else 0),
        ("acmp_listener_ctx", min(L, 1)),
        ("acmp_lstn_ctx_extra", max(0, L - 1)),
        ("lwsrp_base", 1),
        ("lwsrp_attr_ctx", (L - 1) + (T - 1)),
        ("lwsrp_bw_slot_extra", max(0, T - 1)),
    ] + [
        # tier-1 prunes with NO existing row (the servo and the taps are
        # missing from the table; the render LPF is folded inside
        # aaf_listener_engine): a SUBTRACTIVE row counted 1 ONLY when the
        # feature is pruned, so a default config's row list ends exactly
        # where it did before.
        (f"prune_{name}", 0 if block_present(cfg, name) else 1)
        for name in ("media_clock_servo", "latency_taps", "render_lpf")
    ]


def block_present(cfg, name):
    """Is optional block `name` built for this config?

    There are TWO spellings that prune a block - `board.features.<name>` and,
    for the render LPF, `board.constraints.render_lpf` (the key the ax7101
    spend is declared in). They must resolve to ONE answer, because the argv
    and the resource estimate both consume it: for a while they did not, and
    the shipping ax7101 estimate charged for a Butterworth filter its own argv
    told the build not to instantiate.
    """
    if not cfg.get("features", {}).get(name, True):
        return False
    return bool(cfg.get("constraints", {}).get(name, True))


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


# ================================================================ item 00 ====
#  THE WIRE CHANNEL CONSTANT - what the FABRIC emits, not what we declare.
#
#  Every other derivation in this file turns one declaration into another. This
#  one is read off the RTL and the SoC glue, because on 2026-07-27 the 8x8
#  talkers advertised 8-channel AAF (0x0205022002006000) while the framer emitted
#  stereo, and every gate in the repo stayed green - config, generated svh, CSR
#  and descriptor counts all agreed with each other and none of them could see
#  the wire. A Milan-validated listener bound to talker 0, passed the 5.5.1.2
#  format check, returned ACMP SUCCESS with a correct MAAP dmac and MSRP
#  latency, and counted UNSUPPORTED_FORMAT on 296,294 of 296,294 frames.
#
#  THE CHAIN, module by module (hdl/ieee1722/aaf/, sw/litex/milan_soc.py):
#
#    KL_aaf_packetizer  partitions its pair-slot space by a prefix sum of
#                       chans/2, so one talker at C channels needs C/2 pair
#                       slots FED WITH SAMPLES. Unfed slots do not shrink the
#                       frame - the talker simply never emits one.
#    KL_aaf_capture_i2s  hardwires `pair_slot_o = 4'd0`: ONE pair, slot 0.
#    KL_tdm_capture      S/2 pairs on slots 0..S/2-1 - IF something drives its
#                       bclk/fsync/data. On every SoC in this tree
#                       milan_soc.py ties `i_tdm_bclk_i = 0, i_tdm_fsync_i = 0,
#                       i_tdm_data_i = 0` ("neither board has a TDM header
#                       today"), so fsync never toggles and the front-end
#                       yields NOTHING. A config naming a tdm kind is an
#                       advertised capability the fabric cannot back - the same
#                       defect as the channel count, one layer down.
#
#  Note what this means for the AX7101: it has `_connectors = []`, so there is
#  no pmoda, so `i2s_pads = None` and `i_i2s_sdout_i = 0`. Its capture front-end
#  clocks in a constant zero and produces ONE pair of digital SILENCE - which
#  is exactly the 2-channel frame the reference device received where 8 were
#  promised.
#
#  NOT DERIVED FROM `clusters` - that was tried on 2026-07-27 and reverted: it
#  refused endstation_arty_current, which ships `clusters: 8` with a 2ch format
#  and demonstrably works on the wire. `clusters` is the AEM AUDIO_CLUSTER
#  count and is not the wire width.
# =============================================================================

#: milan_datapath AUDIO_IF_SLOTS_P per interface kind. MIRRORS emit_soc_argv:
#: only the tdm kinds emit --audio-interface, so everything else elaborates the
#: stereo I2S front-end (slots 0).
AUDIO_IF_SLOTS = {"tdm8": 8, "tdm16": 16, "tdm32": 32}

#: KL_aaf_packetizer MAX_CHANS_C / the even-2..8 rule of its chans field.
WIRE_CHANS_MIN, WIRE_CHANS_MAX = 2, 8


SOC_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "litex", "milan_soc.py")
_TDM_WIRED_CACHE = {}

#: Per-board pad routing oracle (HANDOVER 8.3b): the same module the SoC's
#: front-end refusal uses, so the builder's pair-supply arithmetic and the
#: elaborated fabric answer from one place and cannot drift.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "litex", "platforms"))
import board_audio_routing as bar  # noqa: E402


def tdm_bus_wired(soc_text=None):
    """Does any SoC in this tree DRIVE the TDM capture bus?

    THE SINGLE SOURCE OF TRUTH for "is a TDM front-end real on this board",
    read out of the SoC glue rather than believed, so that wiring a TDM header
    changes every answer that depends on it - the argv, the plan mark and the
    wire-accountability gate - without an edit in any of them.

    TWO WAYS THE BUS CAN BE REAL, and the question is NOT the same for both.

      SLAVE (KL_tdm_capture).  bclk/fsync are INPUTS a codec must drive.  So
      the question is "does anything assign them something other than 0", and
      today add_milan_datapath ties all three to 0 with nothing overriding
      them via extra_ports: fsync never toggles, the front-end yields no pairs
      at all, and every talker built on it emits NO FRAME.

      MASTER (KL_tdm_capture_master, 2026-07-28).  bclk/fsync are OUTPUTS the
      FABRIC generates off its own MMCM clock, so asking whether anything
      drives i_tdm_fsync_i is asking the wrong question - it will always be 0
      and always should be.  The right question is whether the SoC can BUILD a
      master at all: does it pass AUDIO_IF_MASTER_P to milan_datapath and give
      it the clk_tdm_i to divide.  A master with nothing on tdm_data_i still
      frames at the declared width (it captures digital SILENCE, exactly as
      the pmoda-less AX7101 I2S front-end does today) - which is why the pads
      are NOT part of this question either: what is being asked is "can this
      fabric put N channels per frame on the wire", and the answer for a
      master is yes.  Whether those channels carry audio is the pads' problem
      and is reported separately.
    """
    if soc_text is None:
        if "cached" not in _TDM_WIRED_CACHE:
            try:
                with open(SOC_PY) as fh:
                    _TDM_WIRED_CACHE["cached"] = tdm_bus_wired(fh.read())
            except OSError:
                _TDM_WIRED_CACHE["cached"] = False
        return _TDM_WIRED_CACHE["cached"]
    # MASTER: the parameter must be PASSED (a dp_params entry), not merely
    # mentioned in a comment or an argparse help string - both of which this
    # file is full of. Anchor on the assignment form add_milan_datapath uses.
    if re.search(r'dp_params\[\s*["\']p_AUDIO_IF_MASTER_P["\']\s*\]\s*=', soc_text) \
       and re.search(r"i_clk_tdm_i\s*=", soc_text):
        return True
    # SLAVE: collect every assignment and ask whether ANY is non-zero.
    # Deliberately not a negative lookahead after `\s*=\s*`: that backtracks
    # the whitespace to width zero and then happily matches the space in front
    # of the `0`, so `i_tdm_fsync_i = 0` reads as "wired" and the check
    # inverts itself.
    vals = re.findall(r"i_tdm_fsync_i\s*=\s*([^\s,)]+)", soc_text)
    return bool(vals) and any(v != "0" for v in vals)


def tdm_bus_master(soc_text=None):
    """Is the TDM bus real because the FABRIC drives it (vs a codec)?

    Separated from tdm_bus_wired() because only a master needs
    --audio-interface-master in the argv and a second MMCM output in the CRG,
    and because the two answers will diverge the day a board really does wire
    a codec-driven slave header."""
    if soc_text is None:
        try:
            with open(SOC_PY) as fh:
                soc_text = fh.read()
        except OSError:
            return False
    return bool(
        re.search(r'dp_params\[\s*["\']p_AUDIO_IF_MASTER_P["\']\s*\]\s*=', soc_text)
        and re.search(r"i_clk_tdm_i\s*=", soc_text))


def interface_is_placeholder(cfg, wired=None):
    """True when the config NAMES a TDM interface the fabric cannot provide.

    USER 2026-07-27: "the tdm can be a placeholder" - declaring the interface
    the product will have is legitimate and the declaration STAYS. What is not
    legitimate is letting that placeholder silently change the gateware: the
    tdm kinds drive --audio-interface, which elaborates KL_tdm_capture on a bus
    tied to zero, and THAT build's talkers emit nothing at all. So a
    placeholder is carried as a `planned` mark and is NOT emitted into the soc
    argv - which is exactly how the shipping bitstream was hand-built, and now
    it is the rule rather than an undocumented act of care."""
    if wired is None:
        wired = tdm_bus_wired()
    return bool(AUDIO_IF_SLOTS.get(cfg["interface"]["kind"])) and not wired


def audio_if_slots(cfg, wired=None):
    """milan_datapath AUDIO_IF_SLOTS_P this config elaborates (0 = I2S).

    A placeholder interface elaborates the I2S front-end the board really has,
    so this reports 0 for it - the number the BUILD uses, not the number the
    config wishes for."""
    if interface_is_placeholder(cfg, wired):
        return 0
    return AUDIO_IF_SLOTS.get(cfg["interface"]["kind"], 0)


def i2s_pair_blended(cfg, wired=None):
    """HANDOVER 8.3b: does this build BLEND the stereo I2S pair beside the
    TDM master (milan_datapath AUDIO_IF_I2S_PAIR_P -> KL_pair_blend)?

    The I2S pair rides pair slot 0 - "channels 1/2 stay the I2S Pmod" (USER
    2026-07-28), the bench analog loop - and the TDM pairs follow at slots
    1..S/2, so the supply grows by one pair. True exactly when the SoC will
    pass the parameter: a TDM MASTER build on a board that routes BOTH the
    Pmod I2S2 and a `tdm` header (the AX7101 routes no pmoda, so it stays a
    solo master with no argv or Instance change)."""
    if interface_is_placeholder(cfg, wired) or not tdm_bus_master():
        return False
    if not AUDIO_IF_SLOTS.get(cfg["interface"]["kind"]):
        return False
    board = cfg["board_target"]
    return bar.routes_tdm(board) and bar.routes_i2s_pmod(board)


def framer_pair_supply(cfg, wired=None):
    """Pair slots the capture front-end actually delivers to the packetizer.

    `wired` overrides the milan_soc.py reading; it exists so a gate can ask
    "what would this config do if a TDM header WERE wired" without editing
    the SoC. None = read the fabric, which is the answer that matters."""
    slots = audio_if_slots(cfg, wired)
    if slots == 0:
        return 1                      # KL_aaf_capture_i2s: pair_slot_o = 4'd0
    return slots // 2 + (1 if i2s_pair_blended(cfg, wired) else 0)


def framer_declared_channels(cfg):
    """The WIDEST channels_per_frame any of this config's talkers advertises.

    The REQUIREMENT, stated by the entity itself: a listener may bind any
    declared format, so the framer has to be able to emit the widest of them.
    Read from the AAF stream-format qword's own channels_per_frame field
    (IEEE 1722-2016 7.3.3) - the one field a listener actually validates - and
    NOT from `clusters`, which is the AEM AUDIO_CLUSTER count and was the
    2026-07-27 wrong attempt (it refused endstation_arty_current, which ships
    clusters 8 with a 2-channel format and demonstrably works on the wire)."""
    want = 0
    for t in cfg["talkers"]:
        for fmt in t["formats"]:
            c = fmt_channels(fmt)
            if c is not None:
                want = max(want, c)
    return want or WIRE_CHANS_MIN


def framer_wire_channels(cfg, wired=None):
    """channels_per_frame this fabric puts in a talker's AAF PDU.

    = milan_datapath TALKER_WIRE_CHANS_P = KL_aaf_packetizer WIRE_CHANS_P =
    the reset value of every talker's chans field. Even, WIRE_CHANS_MIN..MAX.

    THE SMALLER OF WHAT IS ASKED FOR AND WHAT CAN BE FED, and both halves are
    load-bearing:

      * capped by the SUPPLY, because the milan_datapath elaboration guard
        refuses a width the capture front-end cannot feed. That cap is the
        measured 8ch-vs-2ch gap: an I2S front-end supplies ONE pair, so an
        8-channel declaration is emitted as 2 and a Milan-validated listener
        discards 100 % of the frames (silicon 2026-07-27, 296,294/296,294).

      * capped by the DECLARATION, because TALKER_WIRE_CHANS_P is a build
        parameter and not a maximum to be filled. When the TDM master landed
        (2026-07-28) the supply jumped from 1 pair to 4 (TDM8) / 8 (TDM16) /
        16 (TDM32) and an uncapped derivation would have made endstation_
        arty_4x4 EMIT 8 channels while advertising 4 - the same defect the
        other way round, and just as invisible to a listener until it counted
        its discards. Raising the framer means meeting the declaration, not
        overshooting it.

    So this is NOT "derive the wire width from the declaration": the
    declaration states the requirement, the front-end states the capability,
    and where they disagree the gate REPORTS it (owner item 5) rather than
    either side quietly moving. A supply of 0 pairs still reports the MINIMUM
    rather than 0: the packetizer holds its reset chans and would stamp that
    shape if it ever emitted, so 0 would claim a frame width no wire ever
    carries. That the talker emits nothing at all is a separate finding."""
    pairs = framer_pair_supply(cfg, wired)
    supply = min(WIRE_CHANS_MAX, pairs * 2)
    return max(WIRE_CHANS_MIN, min(supply, framer_declared_channels(cfg)))


def fmt_channels(fmt):
    """channels_per_frame declared by an AAF stream-format qword (the inverse
    of aaf_pcm32_48k: bits [31:22] of the low word). Returns None for a
    non-AAF format (CRF has no channel count)."""
    n = int(str(fmt), 16)
    if (n >> 56) & 0x7F != 0x02:          # IEEE 1722 subtype 2 = AAF
        return None
    return (n >> 22) & 0x3FF


#: Milan v1.2 6.2 "Base Format Type" + Table 6.1: the Base formats are AAF
#: PCM, 32-bit, at "sampling rate = SR, where SR is an element from {48 kHz,
#: 96 kHz, 192 kHz}" with "number of channels = N, where N is an element from
#: {1, 2, 4, 6, 8}", and "Each PDU shall contain NS audio samples per channel
#: and 1 timestamp (normal timestamp mode, not sparse), where NS = 6 for
#: SR = 48 kHz, NS = 12 for SR = 96 kHz, NS = 24 for SR = 192 kHz."
#: {rate_hz: (nsr, samples_per_frame)}; nsr is IEEE 1722-2016 Table 11.
BASE_RATE_HZ = {48000: (0x5, 6), 96000: (0x7, 12), 192000: (0x9, 24)}
#: Milan v1.2 6.2 / Table 6.1 - the ONLY channel counts that are Base formats.
BASE_CHANNELS = (1, 2, 4, 6, 8)


def aaf_pcm32(channels, rate_hz=48000, ut=False):
    """One AAF PCM 32-bit stream-format qword, DERIVED from the fields rather
    than copied out of Milan Table 6.2 (test_builder gate 29 proves the
    derivation reproduces all fifteen of that table's strings).

    Field placement is IEEE 1722-2016 Annex I.2.4 / I.2.4.1 (the AAF PCM
    stream format): subtype 0x02 at bits [63:56], ut at bit 52, nsr at bits
    [51:48], format at [47:40] (Table 9: 2 = INT_32BIT), bit_depth at [39:32],
    channels_per_frame at [31:22] and samples_per_frame at [21:12].

    ut is the "up to" bit: I.2.4 - "The ut field is used to determine if the
    AAF stream source or sink is capable of sourcing or sinking a stream with
    less than the number of channels indicated by the channels_per_frame
    field.  When set to one (1) the stream source or sink is capable of using
    fewer channels than specified.  The ut field shall be set to zero (0) when
    the stream format is the current format of the stream and when used in a
    SET_STREAM_FORMAT command." - so a ut entry may never be formats[0]."""
    nsr, spf = BASE_RATE_HZ[rate_hz]
    return ((0x02 << 56) | (int(bool(ut)) << 52) | (nsr << 48)
            | (0x02 << 40) | (32 << 32) | (channels << 22) | (spf << 12))


def aaf_pcm32_48k(channels, ut=False):
    """48 kHz spelling of aaf_pcm32, kept because it is the rate every shipping
    config runs at: 2ch=0x0205022000806000, 8ch=0x0205022002006000,
    ut8=0x0215022002006000."""
    return aaf_pcm32(channels, 48000, ut)


def base_format_rate(fmt):
    """(rate_hz, channels_per_frame, ut) when `fmt` is an AAF PCM 32-bit format
    at one of Milan 6.2's three Base sampling rates, else None.

    The channel count is NOT required to be one of BASE_CHANNELS here: a
    3-channel AAF PCM32 48 kHz format is not itself a Base format, but a ut
    entry carrying it still advertises the 1- and 2-channel Base formats, and
    the coverage arithmetic below needs to see it."""
    n = int(str(fmt), 16)
    ut = bool((n >> 52) & 1)
    ch = (n >> 22) & 0x3FF
    stem = n & ~((1 << 52) | (0x3FF << 22))
    for rate in BASE_RATE_HZ:
        if stem == aaf_pcm32(0, rate):
            return rate, ch, ut
    return None


def base_format_cover(fmts):
    """{rate_hz: set(channel counts)} of Milan 6.2 Base formats an advertised
    formats list covers.

    A ut entry covers every Base channel count up to its channels_per_frame,
    which is Milan v1.2 6.5 read together with 5.3.3.4: "If a PAAD-AE supports
    any count from 1 up to N channels per frame, then it should use the ut bit,
    as specified in [AVTP, Annex I.2.4], to describe all the related formats
    using a single ATDECC format string", and "Note that a single entry in the
    formats list can describe a range of formats when using the "up to" bit as
    described in [AVTP, Annex I.2.4]"."""
    cover = {}
    for f in fmts:
        row = base_format_rate(f)
        if row is None:
            continue
        rate, ch, ut = row
        add = {c for c in BASE_CHANNELS if c <= ch} if ut \
            else {ch} & set(BASE_CHANNELS)
        # a rate appears only once something at it is a Base format: a
        # 3-channel AAF PCM32 48 kHz entry is not one (6.2: N in {1, 2, 4,
        # 6, 8}), so on its own it does not arm 6.4's family rule.
        if add:
            cover.setdefault(rate, set()).update(add)
    return cover


def base_format_complete(fmts):
    """A Stream Input's formats list with Milan v1.2 6.4's family completion
    DERIVED here instead of enumerated per config.

    6.4, third paragraph: "If the PAAD-AE Base Listener advertises support for
    a 48kHz (resp. 96kHz, 192kHz) Base format in a Stream Input, then it shall
    also advertise support for all the other 48kHz (resp. 96kHz, 192kHz) Base
    formats in this Stream Input.  Note: This ensures that a Stream Input that
    supports the Base format supports all defined channel counts."

    ONE ut ENTRY PER RATE, not five fixed strings, because Section 6 says so
    itself in 6.5: "If a PAAD-AE supports any count from 1 up to N channels
    per frame, then it should use the ut bit, as specified in [AVTP, Annex
    I.2.4], to describe all the related formats using a single ATDECC format
    string" - and 5.3.3.4 confirms that a controller must read it that way:
    "Note that a single entry in the formats list can describe a range of
    formats when using the "up to" bit as described in [AVTP, Annex I.2.4]."
    It is appended, never prepended: formats[0] is the current_format, and
    IEEE 1722-2016 I.2.4 forbids ut there.

    A LISTENER RULE ONLY.  Milan 6.3 is the whole of what a Talker owes - one
    Configuration with one Stream Output advertising a Base format, Class A
    transport, and "A PAAD-AE Base Talker may advertise any Base Format that
    is reasonable for its functionality" - with no all-channel-counts rule and
    no cross-Stream-Output rate rule anywhere in Section 6.  Completing a
    Stream Output would also be a claim nothing can walk back: the framer
    emits ONE width (framer_wire_channels), while SET_STREAM_FORMAT remains
    unimplemented and returns NOT_IMPLEMENTED. FR-STR-03 makes adaptivity a
    listener requirement, and a listener handed a width the talker cannot
    produce discards every frame (silicon 2026-07-27: 296,294 of 296,294).

    The CRF Media Clock streams cannot reach this function: they are appended
    from clocking.crf_format / crf_output_format rather than from
    streams.listeners.  That is Milan 5.3.3.4 structurally - "If a Stream
    Input/Output supports the Avnu Pro Audio CRF Media Clock Stream Format, it
    shall not support the Avnu Pro Audio AAF Audio Stream Format, and vice
    versa" - and 6.4's own scope, "all the Stream Input which advertise
    support for a Base format"."""
    out = list(fmts)
    for rate, got in sorted(base_format_cover(fmts).items()):
        if set(BASE_CHANNELS) - got:
            out.append(
                f"0x{aaf_pcm32(max(BASE_CHANNELS), rate, ut=True):016X}")
    return out


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


def _streams(lst, ctx, direction, rate_hz=48000):
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
        # A config states the CURRENT format (formats[0]) and nothing else it
        # does not have to: the default is the Base format for this stream's
        # own channel count at the AUDIO_UNIT's rate, and Milan 6.4's family
        # is DERIVED below rather than transcribed into every config, where a
        # hand-copied encoding rots out of sight (endstation_arty_4x4 carried
        # a ut entry capped at 4 channels, so its Stream Inputs advertised
        # neither the 6- nor the 8-channel 48 kHz Base format).
        fmts = s.get("formats") or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]
        fmts = [_fmt64(f, f"{sctx}.formats") for f in fmts]
        # IEEE 1722-2016 Annex I.2.4: "The ut field shall be set to zero (0)
        # when the stream format is the current format of the stream and when
        # used in a SET_STREAM_FORMAT command." formats[0] IS the current
        # format (1722.1-2021 7.2.6), so a ut entry may never lead the list.
        head = base_format_rate(fmts[0])
        if head and head[2]:
            raise ConfigError(
                f"{sctx}.formats: {fmts[0]} carries the AVTP I.2.4 'up to' "
                f"bit and is formats[0], which 1722.1-2021 7.2.6 reports as "
                f"current_format - I.2.4 requires ut = 0 there")
        if direction == "listener":
            for f in fmts:
                row = base_format_rate(f)
                if row and row[2]:
                    raise ConfigError(
                        f"{sctx}.formats: {f} carries the AVTP I.2.4 'up to' "
                        f"bit. Milan v1.2 6.4's family completion is derived "
                        f"from the rate and 6.2's channel counts (see "
                        f"base_format_complete), so a config restating it is "
                        f"a second answer to the same question - and the one "
                        f"that goes stale, since only the config half can be "
                        f"written with the wrong channel count")
            fmts = base_format_complete(fmts)
        clusters = s.get("clusters", ch)
        if not (isinstance(clusters, int) and 1 <= clusters <= 32):
            raise ConfigError(f"{sctx}: clusters {clusters} outside 1..32")
        # Milan v1.2 5.3.3.9 requires every Stream Port Input to omit an
        # AUDIO_MAP descriptor, which is the descriptor-model signal for a
        # dynamically mapped input. This is an invariant, not an optional
        # capability switch: accepting a static listener would generate an
        # entity model a Milan PAAD-AE is forbidden to expose.
        #
        # Stream Port Outputs may be static or dynamic. The current media
        # fabric selects its capture crossbar as one image-wide mode, so the
        # load_config validation below requires all talkers to choose the
        # same mode rather than silently misrouting a mixed image.
        map_mode = s.get("map_mode",
                         "dynamic" if direction == "listener" else "static")
        if map_mode not in ("static", "dynamic"):
            raise ConfigError(f"{sctx}: map_mode '{map_mode}' not "
                              "static|dynamic")
        if direction == "listener" and map_mode != "dynamic":
            raise ConfigError(
                f"{sctx}: map_mode static is forbidden for a Stream Port "
                "Input; Milan v1.2 5.3.3.9 requires dynamic mappings on "
                "every Stream Port Input")
        # USER 08-01: talkers may be dynamic too. Milan 5.3.3.9 leaves
        # Stream Port Outputs free, and 5.4.2.26-28 make GET/ADD/REMOVE a
        # SHALL for "each Stream Port Output that has no Audio Map" - a
        # dynamic talker port drops its AUDIO_MAP descriptor and the RTL
        # `AEM_ODYNMAP engine serves the commands and drives the capture
        # crossbar.
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
def cluster_layout(listeners, talkers, policy, iface_channels,
                   phys=None, pools=None, lb_backed=True):
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
      role-pools (D8) - the port's cluster count is NOT the stream's
        `clusters` at all: it is the sum of the declared ROLE POOLS
        (physical / host / pilot / loopback), each width derived from the
        platform declaration. `clusters` is then unused for that port and the
        config says so.

    Every port comes back with a `pool` list of {role, offset, width}
    segments covering 0..clusters-1 exactly, which is what names the
    AUDIO_CLUSTERs (D10) and what the AUDIO_MAP is written against.
    Returns (ports_in, ports_out)."""
    if policy not in CLUSTER_POLICIES:
        raise ConfigError(f"cluster policy '{policy}' not in {CLUSTER_POLICIES}")
    pools = pools or {}
    # physical widths per DIRECTION. Default = the declared interface width;
    # a platform that routes no audio pins declares 0 and every cluster on it
    # is honestly non-physical (see CLUSTER_ROLES).
    ph_render = iface_channels if phys is None else int(phys["render"])
    ph_capture = iface_channels if phys is None else int(phys["capture"])

    def eff(s):
        if policy == "cap-at-interface":
            return min(s["clusters"], iface_channels)
        return s["clusters"]

    def legacy_pool(dir_base, n, ph):
        """Legacy policies: the wire-truth rule is stated PER DIRECTION
        ("physical interface channels bind in order to the first clusters
        per direction"), so a port's roles depend on where its block sits in
        its direction, not on the port index."""
        segs, off = [], 0
        n_phys = max(0, min(n, ph - dir_base))
        if n_phys:
            segs.append(dict(role="physical", offset=0, width=n_phys,
                             first=dir_base))
            off = n_phys
        if n - off:
            segs.append(dict(role="virtual", offset=off, width=n - off,
                             first=dir_base + off))
        return segs

    def role_pool(direction, port_index):
        """D8 pools. Order is fixed so base_cluster arithmetic is readable:
        physical, host, then (talker ports only) pilot and loopback."""
        segs, off = [], 0
        for role, width in (
                ("physical", ph_render if direction == "input" else ph_capture),
                ("host", int(pools.get("host", 0))),
                ("pilot", (1 if pools.get("pilot") else 0)
                          if direction == "output" else 0),
                ("loopback", int(pools.get("loopback", 0))
                             if direction == "output" else 0)):
            if width > 0:
                segs.append(dict(role=role, offset=off, width=width,
                                 first=0 if role != "loopback" else port_index))
                off += width
        if not segs:
            raise ConfigError(
                f"cluster_mapping.policy role-pools: STREAM_PORT_"
                f"{direction.upper()} {port_index} would carry ZERO clusters - "
                "every declared pool (physical/host/pilot/loopback) is 0 wide. "
                "A STREAM_PORT with no cluster block cannot carry audio; "
                "declare at least one pool (audio_interface.cluster_mapping."
                "pools) or use another policy")
        return segs

    # map_mode dynamic (gaps item 8): the port carries NO AUDIO_MAP
    # (7.2.13 number_of_maps=0, base_map ignored) - static maps are
    # renumbered contiguously so the descriptor set stays gapless.
    ports_in, base, next_map, dir_base = [], 0, 0, 0
    for i, s in enumerate(listeners):
        if policy == "role-pools":
            pool = role_pool("input", i)
            n = sum(g["width"] for g in pool)
        else:
            n = eff(s)
            pool = legacy_pool(dir_base, n, ph_render)
        dyn = s.get("map_mode", "dynamic") == "dynamic"
        ports_in.append(dict(index=i, stream_index=i, clusters=n,
                             base_cluster=base,
                             maps=0 if dyn else 1,
                             base_map=0 if dyn else next_map,
                             map_mode=s.get("map_mode", "dynamic"),
                             map_page=s.get("map_page"), pool=pool))
        if not dyn:
            next_map += 1
        base += n
        dir_base += n
    # Every dynamic port shares ONE GET_AUDIO_MAP partition size: the RTL
    # page origin (map_index * PAGE) is a constant multiply, so PAGE is a
    # single elaboration constant. Milan 5.4.2.26 only bounds a subset's
    # SIZE ("disjoint subsets whose size does not exceed 176") and requires
    # the partitioning to be fixed for a Configuration - it never requires
    # equal subsets - so one shared bound is conformant and a port with
    # fewer clusters than the page simply gets number_of_maps = 1 with a
    # short last partition. An EXPLICIT map_page must agree across dynamic
    # ports; left unset it defaults to the widest port, capped at 8.
    dynp = [p for p in ports_in if p["map_mode"] == "dynamic"]
    if dynp:
        explicit = {p["map_page"] for p in dynp if p["map_page"] is not None}
        if len(explicit) > 1:
            raise ConfigError(
                "every map_mode-dynamic listener must declare the SAME "
                f"map_page (one RTL partition constant); got "
                f"{sorted(explicit)}")
        page = explicit.pop() if explicit \
            else min(max(p["clusters"] for p in dynp), 8)
        if not 1 <= page <= 11:
            raise ConfigError(f"map_page {page} outside 1..11 (RTL "
                              "GET_AUDIO_MAP scratch bound)")
        for p in dynp:
            p["map_page"] = page
    ports_out, dir_base = [], 0
    for j, s in enumerate(talkers):
        if policy == "role-pools":
            pool = role_pool("output", j)
            n = sum(g["width"] for g in pool)
        else:
            n = eff(s)
            pool = legacy_pool(dir_base, n, ph_capture)
        dyn = s.get("map_mode", "static") == "dynamic"
        ports_out.append(dict(index=j, stream_index=j, clusters=n,
                              base_cluster=base,
                              maps=0 if dyn else 1,
                              base_map=0 if dyn else next_map,
                              map_mode=s.get("map_mode", "static"),
                              pool=pool,
                              # task #65: does THIS BUILD elaborate the rx ->
                              # talker LOOP bucket? Read by primary_segment,
                              # so a loopback cluster can never become the
                              # power-on source of a build without the lane.
                              lb_backed=lb_backed))
        if not dyn:
            next_map += 1
        base += n
        dir_base += n
    return ports_in, ports_out


#: static-AUDIO_MAP source preference under role-pools: the segment the
#: stream channels are wired to at power-on. Physical first where it exists;
#: on a board with no audio pins a talker falls through to LOOPBACK, which is
#: the point of D8's loopback lane (USER 2026-07-28: "For the AX Loopback,
#: use the loopback cluster created"), and then to HOST.
#:
#: task #65: LOOPBACK is only a candidate when the build ELABORATES the lane
#: (cluster_mapping.fabric.loopback_lane -> milan_soc --loopback-lane ->
#: milan_datapath LOOPBACK_P). It used to be preferred unconditionally, and
#: on the AX - which routes no audio pins, so physical is 0 wide and the
#: fall-through always reached loopback - that put EVERY talker stream
#: channel on a cluster whose fabric source did not exist. The map read
#: perfectly in Hive and the wire carried digital silence. A power-on mapping
#: may only name a source this build can actually produce; Milan v1.2 5.3.9.1
#: makes the alternative explicit and legal ("each channel of each Stream
#: Output ... is either NOT MAPPED or mapped to a channel of an Audio
#: Cluster"), and 5.4.2.26 requires GET_AUDIO_MAP to answer with zero
#: mappings for a subset that has none - so declaring less is conformant,
#: while declaring a source that cannot exist is merely undetectable.
PRIMARY_ROLE_ORDER = {
    "input":  ("physical", "host", "virtual"),
    #! USER 2026-08-06: the talker's power-on identity is the SHARED-MEMORY
    #! (host) lane, NOT the loopback - "the ATDECC mapping must correspond
    #! to the physical mux, and the stream_output was set to the Loopback".
    #! host now outranks loopback; a backed loopback stays fully mappable
    #! by a controller, it just is not what the entity wakes up claiming.
    #! (The 8x8 never saw this order matter: its lane was unbacked, so the
    #! preference walk skipped loopback and host won by default.)
    #!
    #! USER 2026-08-10, 0x0043: host now outranks PHYSICAL too. The moment the
    #! AX7101 declared its TDM8 channels (physical_channels.capture 0 -> 8),
    #! physical-first silently moved the boot identity off the shared-memory
    #! lane and onto the J11 pins - so a board with no codec attached would
    #! wake up streaming whatever `din` floats to, and the PipeWire E2E path
    #! would need a controller mapping on every boot. The 08-06 rule was
    #! chosen against LOOPBACK, before a real physical front end existed;
    #! asked again with physical on the table, the answer was the same lane.
    #! This is a PREFERENCE WALK for the identity seed only - it does not
    #! move cluster numbering, which role_pool() fixes as physical, host,
    #! pilot, loopback. The TDM8 stays fully controller-selectable, which was
    #! the entire point of putting it in the port.
    "output": ("host", "physical", "loopback", "pilot", "virtual"),
}


def primary_segment(port, direction):
    """The pool segment this port's static AUDIO_MAP wires its stream
    channels to (1722.1 7.2.19 offsets are port-relative, so this is just an
    offset inside the port's own pool).

    A segment whose fabric source this build did not elaborate is not a
    candidate: `lb_backed` False drops the loopback pool from the preference
    walk (the clusters still EXIST and a controller may still map to them -
    they simply are not what the entity wakes up claiming). Absent key =
    backed, so every caller that predates task #65 is unchanged."""
    by_role = {g["role"]: g for g in port["pool"]}
    if not port.get("lb_backed", True):
        by_role.pop("loopback", None)
    for role in PRIMARY_ROLE_ORDER[direction]:
        if role in by_role:
            return by_role[role]
    return port["pool"][0]


def cluster_names(cfg, port, direction):
    """D10: one object_name per cluster of this port, in offset order.

    1722.1-2021 6.2.2.8 lists `object_name` among the fields EXCLUDED from
    "the structure of the data model", so renaming clusters must NOT move
    entity_model_id - and it does not: model_shape() never sees a name."""
    label = IFACE_LABEL.get(cfg["interface"]["kind"], "AUDIO")
    cnames = cfg["interface"].get("channel_names") or []
    def chname(k, fallback):
        return cnames[k] if k < len(cnames) else fallback
    # the received stream channel space, in {stream, channel} order: what a
    # loopback cluster actually offers a talker.
    rx = [(si, ch) for si, s in enumerate(cfg["listeners"])
          for ch in range(s["channels"])]
    out = []
    for g in port["pool"]:
        role, w, first = g["role"], g["width"], g.get("first", 0)
        for n in range(w):
            if role == "physical":
                out.append(f"{label} {'Out' if direction == 'input' else 'In'}"
                           f" {chname(first + n, str(first + n))}")
            elif role == "virtual":
                out.append(f"Virtual {'Out' if direction == 'input' else 'In'}"
                           f" {first + n}")
            elif role == "host":
                out.append(chname(n, None) or
                           f"Host {'Play' if direction == 'input' else 'Cap'}"
                           f" {n}")
            elif role == "pilot":
                out.append("Pilot Tone")
            else:  # loopback: walk the rx channel space from THIS talker's
                   # own stream index, so talker t defaults to rx stream t
                   # (per-channel-distinct audio, not eight copies of one)
                if not rx:
                    out.append(f"Loopback ch {n}")
                    continue
                start = next((k for k, (si, ch) in enumerate(rx)
                              if si == first and ch == 0), 0)
                si, ch = rx[(start + n) % len(rx)]
                out.append(f"Loopback S{si} {chname(ch, f'ch {ch}')}")
    assert len(out) == port["clusters"]
    return out


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
                avtpdu_bytes=avtpdu, l2_frame_bytes=L2_HDR_BYTES + avtpdu,
                #: what the TSpec DECLARES: Table 4.4's 24*N + 24 + 1. Kept
                #: apart from avtpdu_bytes on purpose - the headroom octet is
                #: not on the wire, so l2_frame_bytes must not carry it.
                max_frame_bytes=avtpdu + MILAN_TSPEC_HEADROOM_B)


def srp_idle_slope_bps(max_frame_bytes, interval_frames, intervals_ps):
    """Class-A idleSlope, bits/s - MILAN v1.2 4.3.3.2's recipe run as FOUR
    STEPS, the form KL_lwsrp_bw_gate uses since 0x0020.

        F = MaxFrameSize + 22          eth hdr + VLAN tag + FCS
        if F < 68: F = 68              minimum TAGGED frame - a CLAMP
        W = F + 20                     preamble + IPG
        bits/s = W x MaxIntervalFrames x 8000 x 8

    The steps are kept separate rather than folded into (MaxFrameSize + 42)
    because that fold IS steps 1 and 3 added together and DROPS step 2. The
    result is right for every frame big enough not to need the clamp, so it
    looks correct until a short stream hits it: the CRF Media Clock at
    MaxFrameSize 29 reserves 5376 kb/s folded against the mandated 5632, and
    starving CRF destabilises the media clock of every listener downstream."""
    f = max_frame_bytes + SRP_L2_OVERHEAD_B
    if f < SRP_MIN_L2_BYTES_B:
        f = SRP_MIN_L2_BYTES_B
    return (f + SRP_WIRE_OVERHEAD_B) * interval_frames * intervals_ps * 8


def load_srp(raw, listeners, talkers, clocking, cons, binfo,
             wire_channels=None):
    """Validate + normalize the optional `srp:` section and resolve every
    per-stream TSpec. Raises ConfigError on a contradictory reservation
    (unknown SR class, illegal VID/queue, over-subscribed class-A ceiling).

    `wire_channels` is the channels_per_frame the FRAMER emits
    (framer_wire_channels): 802.1Q 35.2.2.8.4 a) defines MaxFrameSize as
    "the maximum frame size that the Talker WILL PRODUCE, excluding any
    overhead for media-specific framing" - the wire, never the declaration.
    Deriving from the declared channel count is how the 2026-07-28 bench
    measured a TSpec of a frame nobody sent (declared-8ch MSDU announced
    while the wire carried the 2ch 72-byte one). None = fall back to the
    declaration (legacy callers/tests only; load_config always passes it)."""
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
    # `maap` = the DMACs are claimed at run time by KL_maap. Everything
    # downstream still needs a concrete base to model the reservation with,
    # so the default provisioned base is used for the tables and the
    # ALLOCATION POLICY is recorded separately - that policy is what
    # validate_features() keys the MAAP prune gate on.
    s["stream_dmac_alloc"] = "static"
    if isinstance(s["stream_dmac_base"], str) and \
            s["stream_dmac_base"].strip().lower() == SRP_DMAC_DYNAMIC:
        s["stream_dmac_alloc"] = SRP_DMAC_DYNAMIC
        s["stream_dmac_base"] = SRP_DEFAULTS["stream_dmac_base"]
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
    # Geometry from the WIRE width (see the docstring): with the
    # accountability gate holding declared == emitted the two derivations
    # agree numerically, but the tie must be structural - the constant that
    # drives KL_aaf_packetizer's chans field is the one the TSpec describes,
    # and the lwSRP engine's own talker rows already derive 24 + 24*C from
    # TCTX chans at runtime; this makes the provisioned rows agree with it
    # by construction.
    rate = clocking["sampling_rate_hz"]
    rows, total_slope = [], 0
    for t, st in enumerate(talkers):
        geo = srp_frame_geometry(
            wire_channels if wire_channels is not None else st["channels"],
            rate, cls["intervals_ps"])
        mf = geo["max_frame_bytes"] if s["tspec_policy"] == "derived" \
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
    #! the CRF Media Clock Output reserves too (Milan v1.2 7.3.3), and the
    #! bw-gate sums its slope into the SAME class A Sigma - so the ceiling
    #! check has to see it, or a shape that only fits WITHOUT its mandatory
    #! media clock would pass here and be refused on the wire.
    crf_tk_c = 1 if clocking["crf_output"] else 0
    crf_slope_c = srp_idle_slope_bps(CRF_SRP_MAXFRAME_B, 1,
                                     cls["intervals_ps"]) if crf_tk_c else 0
    total_slope += crf_slope_c
    if total_slope > limit_bps:
        raise ConfigError(
            f"class-{s['sr_class']} reservation {total_slope} bps over "
            f"{len(talkers)} talker stream(s) + the CRF media clock "
            f"({crf_slope_c} bps) exceeds the "
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
        #
        # 2026-07-28: T also counts the CRF Media Clock Output, which is a
        # TALKER attribute row of its own at talker index max(L, T) - Milan
        # v1.2 7.3.3 carries the media clock stream under an SRP reservation
        # of class A, so it is a reservation like any other and not an
        # un-declared side channel.
        #
        # 2026-08-05 (VERSION 0x0023): +1 for the DEDICATED listener-0 row
        # (SRP_LSN0_ROW_C, the last row) - sink 0's Listener attribute no
        # longer aliases the software-owned legacy row 0, so every shape
        # needs L+T rows and the ctx index widened to 5 bits. An 8x8 shape
        # WITH a CRF output is 17 rows; the ConfigError below is the
        # builder-side twin of milan_datapath's srp_ctx_rows_guard.
        ctx_rows_required=len(listeners) + len(talkers) + crf_tk_c,
        ctx_rows_available=2 * max(len(listeners), len(talkers))
                           + crf_tk_c,
        # the CRF stream's own class A slope, already INSIDE
        # total_idle_slope_bps above; broken out so the media clock's share
        # of the class A budget is visible and never "optimised" away by
        # weakening the SR class (USER standing rule; Milan 7.3.3 fixes it
        # at class A).
        crf_idle_slope_bps=crf_slope_c,
    )
    if s["ctx_rows_required"] > (1 << SRP_CTX_IDX_BITS):
        raise ConfigError(
            f"{s['ctx_rows_required']} lwSRP attribute rows needed "
            f"(L+T incl the dedicated listener-0 row) but ctx_idx is "
            f"{SRP_CTX_IDX_BITS} bits = {1 << SRP_CTX_IDX_BITS} rows max")
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
#: MOVED TWICE, DELIBERATELY, both times for the egress queue map:
#:   VERSION 0x0011 (6 queues): 0x0C -> 0x14. The class-A queue field widened
#:     from [3:2] to [4:2] and its reset moved from q3 to q5 - the queue the
#:     802.1Q-ordered map put SR class A on.
#:   VERSION 0x0014 (5 queues): 0x14 -> 0x10. The six-queue map missed
#:     placement on the xc7a100t by 282 slices, the spare queue was dropped and
#:     class A moved down to q4. The FIELD keeps its 3 bits (ceil(log2 5) = 3);
#:     only the reset value changed.
#: Both are REFLASH-VISIBLE changes; every other word is untouched.
SRP_FROZEN_RESETS = {"LWSRP_CTRL": 0x00000010, "LWSRP_VID": 0x00000002,
                     "LWSRP_DMAC_LO": 0xF000FE01, "LWSRP_DMAC_HI": 0x000091E0,
                     "LWSRP_TSPEC": 0x000100E0, "LWSRP_LATENCY": 0x00000000}
SRP_FROZEN_PRIO_RANK = 0x70          #: milan_csr's old SRP_PRIO_RANK_C literal

#: Where milan_csr.sv `include-s the emitted CSR defaults from. The path is
#: RELATIVE TO hdl/common/csr (Verilator resolves `include against -I/+incdir
#: and the CWD only, never against the including file), which every consumer
#: already carries as an include dir - exactly like gen/adp_shape_defaults.svh
#: next door.
#: The 0x680 REGISTERS THEMSELVES NO LONGER DRIVE ANYTHING (2026-08-12): the
#: applicant (hdl/ieee8021q/srp/**) is deleted. milan_csr.sv still `include-s
#: this header and still serves those words as an ABI software can read and
#: write, so the header stays generated and stays gated - a stale reset word
#: is still a wrong readback.
CSR_DEFAULTS_INCLUDE = "gen/lwsrp_csr_defaults.svh"
CSR_DEFAULTS_REL = "hdl/common/csr/" + CSR_DEFAULTS_INCLUDE

#: Same rule for the ADP shape, and this one is fully LOAD-BEARING. Both
#: milan_csr.sv (the RO 0x618/0x61C words) and milan_datapath.sv (which sizes
#: the protocol processor's source/sink arrays from ADP_TALKER_SRC_C /
#: ADP_LISTENER_SINK_C) `include this, so the config is the single definition
#: of how many streams the entity HAS.
ADP_SHAPE_INCLUDE = "gen/adp_shape_defaults.svh"
ADP_SHAPE_REL = "hdl/common/csr/" + ADP_SHAPE_INCLUDE

#: THE AEM DESCRIPTOR ROM HAS NO RTL PATH ANY MORE. It used to be
#: `include-d by KL_aecp_aem_store.sv out of hdl/ieee17221/aecp/gen/; that
#: module and its whole directory are DELETED. The ROM is still generated
#: (the entity model is what the ADP shape counts and capability words are
#: DERIVED from, and the gates below read it) but it is written ONLY to
#: out/<cfg>/aecp_aem_rom.svh, never into hdl/ and never into
#: configs/generated/<cfg>/gen/ - a build artifact in an include dir is a
#: build artifact something will eventually compile.
AEM_ROM_OUT_NAME = "aecp_aem_rom.svh"

#: Per-config copies of the shape include, tracked so a harness or a build can
#: point its include path at ONE config's definition without regenerating
#: anything (tb/verilator/milan_dp elaborates the 4x4 and 8x8 shapes this way).
GEN_CONFIG_DIR = "configs/generated"

#: THE IDENTITY THE BOARD SOFTWARE PROGRAMS. The fabric serves the ADPDU AND
#: the AEM ENTITY descriptor's entity_model_id from CSR 0x60C/0x610 (the ROM's
#: OVL_MODEL_ID_C overlay slot), so whatever the boot script writes there IS
#: the entity's model id - a literal in that script is a SECOND answer to a
#: question the builder already answers, and on 2026-08-02 silicon it was the
#: STALE one: the flashed ROM carried the dynamic-output-map descriptors while
#: ADP advertised 001BC52ED611DB08, the id of a model that no longer exists.
#: 1722.1-2021 6.2.1.10: entity_model_id identifies the AEM; two different AEMs
#: must not share one. So the builder EMITS the identity and S50milan SOURCES
#: it. Per BOARD (one shared rootfs serves both boards, S50milan branches on
#: /proc/device-tree/model), written by the same --write-fragment moment that
#: hands a board's bitstream flags over - one owner for "what this board is".
ENTITY_CONF_NAME = "milan-entity.conf"
#: `/etc` of the flashed rootfs overlay. In the SIBLING repo (milan-tests-avb)
#: because that is where the image is built; overridable for a checkout that
#: lives elsewhere, and simply SKIPPED when it is not on disk.
ROOTFS_OVERLAY_ETC = os.environ.get(
    "MILAN_ROOTFS_OVERLAY_ETC",
    os.path.expanduser("~/milan-tests-avb/fpga/buildroot/br2-external/"
                       "board/milan_naxriscv/rootfs_overlay/etc"))


def entity_conf_overlay_path(board_target):
    """Where <board>'s generated identity ships, or None when the rootfs
    overlay is not on this disk (bare container / fpga repo alone)."""
    if not os.path.isdir(ROOTFS_OVERLAY_ETC):
        return None
    return os.path.join(ROOTFS_OVERLAY_ETC,
                        f"milan-entity.{board_target}.conf")


def _entity_model_image(cfg, overlay):
    """{filename: content} for the AEM image the descriptor store fetches.

    Delegates to avdecc/gen_aemi_image.py rather than restating the format:
    that module is itself only a join of gen_aem_store (the bytes) and the
    protocol processor's own packer (the layout), so this stays one hop from
    both authorities and cannot drift from either.

    The manifest carries the window from THIS config, which is also what
    generated the `ppmem` reservation above - the loader reads the base from
    here and never restates it.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(os.path.dirname(here))
    for d in (os.path.join(repo, "avdecc"),
              os.path.join(repo, "protocol-processor", "hdl", "aecp", "desc")):
        if d not in sys.path:
            sys.path.insert(0, d)
    import gen_aem_store as _aem
    import gen_desc_image as _img
    import gen_aemi_image as _join

    model = _aem.build_model(_aem.spec_from_overlay(overlay))
    # 576 = PP_DESC_LINE_BYTES_P. A descriptor longer than the store's line
    # buffer cannot be answered, and the packer is the only place that sees it.
    blob, report = _img.build(
        _join.model_to_document(model, _join.identity_from_overlay(overlay)),
        576)
    base = int(cfg["platform"]["pp_mem_phys"])
    manifest = {
        "desc_base": base,
        "resp_base": base + int(cfg["platform"]["pp_mem_bytes"]) - 0x1000,
        "window_bytes": int(cfg["platform"]["pp_mem_bytes"]),
        # the AXI-Lite Milan CSR window, for the loader's PAIRING CHECK: the
        # image bakes firmware_version from milan_csr's VERSION at generation
        # time, the fabric serves that register live, and comparing the two at
        # load time is what catches a bitstream flash that left the rootfs -
        # and therefore this image - a build behind (the 2.68-image-on-2.69-
        # gateware finding, 2026-08-14). Same rule as desc_base: the loader
        # reads it from here and never restates it.
        "csr_base": int(cfg["platform"]["csr_base"]),
        "image": "aem_desc.bin",
        "image_bytes": len(blob),
        # names the config this model IS, so a board and a bench can tell
        # whether the image on the board is the one they think it is
        "config": os.path.basename(str(cfg.get("source", ""))),
    }
    # The loader ships WITH the image, from milan-fpga's one copy. A second
    # copy maintained in the rootfs would be a script that drifts from the
    # manifest format it parses, and the failure would be a board that reports
    # a successful load of nothing.
    with open(os.path.join(repo, "scripts", "load_entity_model.sh"),
              encoding="utf-8") as fh:
        loader = fh.read()
    return {"aem_desc.bin": blob,
            "aem_desc.json": json.dumps(manifest, indent=1) + "\n",
            "aem_desc.map": report,
            "load_entity_model.sh": loader}


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
                          #! the media clock's share, already inside the total
                          crf_idle_slope_bps=s["crf_idle_slope_bps"],
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
    N = max(L, T)
    # 2026-07-28: the CRF Media Clock Output is a TALKER attribute row of its
    # own (Milan v1.2 7.3.3 - the media clock stream is carried under an SRP
    # reservation of class A). It sits at talker index N, hence ctx row
    # (N-1)+N, so a config that HAS one needs one more talker slot and one
    # more attribute row: N_CTX_P = L + T with T = N + 1 (the +1 over the
    # old L+T-1 is the DEDICATED listener-0 row, 2026-08-05 VERSION 0x0023).
    crf_tk = 1 if cfg["clocking"]["crf_output"] else 0
    return {
        "KL_lwsrp_top.CLK_FREQ_HZ_P": cfg["constraints"]["milan_clk_hz"],
        # N_CTX_P covers listener + talker attribute rows PLUS sink 0's own
        # row (L+T, and the datapath sizes it N_STREAMS + SRP_TALKERS_C);
        # the bw-gate stays TALKER-wide so aaf_stream_en_w still indexes by
        # talker index, and the CRF slope joins the SAME class A Sigma.
        "KL_lwsrp_top.N_CTX_P": N + (N + crf_tk),
        "KL_lwsrp_top.N_LISTENERS_P": N,
        "KL_lwsrp_top.N_TALKERS_P": N + crf_tk,
        "KL_lwsrp_bw_gate.N_STREAMS_P": N + crf_tk,
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
    a("//                drift. REFERENCE ONLY: the lwSRP engine that")
    a("//                consumed this table (hdl/ieee8021q/srp/**) is")
    a("//                DELETED, so nothing compiles this file. The CSR-")
    a("//                facing subset that IS still compiled lives in")
    a("//                hdl/common/csr/gen/lwsrp_csr_defaults.svh and is")
    a("//                gated against milan_csr.sv by")
    a("//                sw/builder/test_builder.py (gates 18a/20a).")
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

    Include-only, exactly like gen/adp_shape_defaults.svh next door: no
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
    a("//                Same values as the full reference table")
    a("//                out/<cfg>/lwsrp_table.svh (one config, one pass;")
    a("//                test_builder gate 20a compares them).")
    a("//                NOTE the 0x680 registers no longer DRIVE anything:")
    a("//                the applicant (hdl/ieee8021q/srp/**) is deleted and")
    a("//                the group survives as a software-visible ABI only.")
    a("//                Include-only: no `default_nettype directive (it would")
    a("//                leak into the includer's scope), no include guard")
    a("//                (module-scope localparams - each including module")
    a("//                needs its own copy) and no net decls.")
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


def adp_shape(cfg):
    """The entity's ADVERTISED SHAPE, computed from the declarative config.

    IEEE 1722.1-2021 6.2.1.9 / 6.2.1.11: talker_stream_sources and
    listener_stream_sinks are the STREAM_OUTPUT / STREAM_INPUT descriptor
    counts of the current configuration - so they are the SAME numbers
    emit_aem_overlay() already puts in descriptor_counts, and the ACMP
    unique_id ranges the gateware has to answer over. One function, so the
    three cannot disagree.

    Capabilities are build facts too, not policy: MEDIA_CLOCK_SOURCE is set
    only when this config actually has a CRF Media Clock Output to bind."""
    n_src = len(cfg["talkers"]) + (1 if cfg["clocking"]["crf_output"] else 0)
    n_sink = len(cfg["listeners"]) + (1 if cfg["clocking"]["crf_sink"] else 0)
    # 1722.1-2021 Table 6.4 / 6.5
    IMPLEMENTED, MEDIA_CLOCK, AUDIO = 0x0001, 0x0800, 0x4000
    tcaps = IMPLEMENTED | AUDIO | (MEDIA_CLOCK if cfg["clocking"]["crf_output"]
                                   else 0)
    lcaps = IMPLEMENTED | AUDIO | (MEDIA_CLOCK if cfg["clocking"]["crf_sink"]
                                   else 0)
    return dict(talker_stream_sources=n_src, listener_stream_sinks=n_sink,
                talker_capabilities=tcaps, listener_capabilities=lcaps)


def overlay_adp_block(cfg):
    """The ADP-advertised identity, for the consumers that must REPEAT it.

    1722.1-2021 Table 7-2 makes the ENTITY descriptor's identity fields the
    ADPDU's fields ("is the same as the ... field in ATDECC Discovery
    Protocol"), so the AEM descriptor image has to carry the numbers ADP
    advertises rather than pick its own.  It is the same adp_shape() the
    gateware include is generated from and the same derive_entity_id() the
    board's milan-entity.conf carries, so there is no third derivation to go
    stale: one function, three artifacts.

    entity_capabilities is deliberately absent, for the reason emit_entity_
    conf() states: the builder does not compute it.  It is a fixed RTL
    constant (pp_adp_pkg::ADP_ENTITY_CAPS_C) and gen_aemi_image reads it from
    there, which is the only place it exists.
    """
    sh = adp_shape(cfg)
    return {
        "entity_id": f"0x{derive_entity_id(cfg):016X}",
        "mac_address": cfg["platform"]["mac_address"],
        "talker_stream_sources": sh["talker_stream_sources"],
        "listener_stream_sinks": sh["listener_stream_sinks"],
        "talker_capabilities": f"0x{sh['talker_capabilities']:04X}",
        "listener_capabilities": f"0x{sh['listener_capabilities']:04X}",
    }


def emit_adp_shape_svh(cfg, overlay=None):
    """The ADP shape as the SystemVerilog include milan_csr.sv and
    milan_datapath.sv compile (`include "gen/adp_shape_defaults.svh").

    WHY THIS FILE EXISTS.  Until 2026-07-27 the ADPDU stream counts came from
    two hand-typed lines in a boot script, and the 8x8 board therefore
    advertised the 1x1 shape those lines were written for (1 talker source /
    2 listener sinks) - see docs/findings/ADP_SHAPE_STATIC_0727.md.  Making
    the registers read-only removed the runtime lie; putting the VALUES here
    is the other half, and the one the standing directive asks for: the
    declarative end-station config is the single definition, and it drives
    the gateware, the AEM model and lwSRP alike (docs/ENDSTATION_BUILDER.md).

    These are not merely the CSR's reset words.  milan_datapath sizes its
    talker/listener CONTEXT ARRAYS from the same two constants - the ACMP
    contexts once, the protocol processor's source/sink arrays since that
    plane replaced them - so the advertised range and the addressable range
    are the same number by construction: there is no edit that moves one
    without the other, and a gateware built for one shape cannot be handed
    another shape's entity definition without failing to elaborate.

    This is now the ONLY generated entity artifact any RTL compiles: the AEM
    descriptor ROM's `include-r (KL_aecp_aem_store) is deleted with the rest
    of the AECP plane, so scripts/check_entity_shape.py guards this file
    alone - and it guards it harder, because it is still a tracked
    last-writer-wins artifact.

    Include-only, exactly like gen/lwsrp_csr_defaults.svh: no
    `default_nettype (it would leak into the includer's scope), no include
    guard (module-scope localparams - each including module needs its own
    copy) and no net decls."""
    sh = adp_shape(cfg)
    if overlay is None:
        overlay = emit_aem_overlay(cfg)
    sys.path.insert(0, os.path.join(ROOT, "avdecc"))
    import gen_aem_store as aem_store
    din_any = any(s.get("map_mode", "static") == "dynamic"
                  for s in cfg["listeners"])
    dout_any = any(s.get("map_mode", "static") == "dynamic"
                   for s in cfg["talkers"])
    dm = {"EMIT": din_any}
    if din_any:
        dyn_in = [p for p in cfg["ports_in"]
                  if p.get("map_mode", "static") == "dynamic"]
        in_page = dyn_in[0]["map_page"]
        in_streams = overlay["stream_inputs"]
        dm.update(
            KEYS=max(p["base_cluster"] + p["clusters"] for p in dyn_in),
            PAGE=in_page,
            PBASE=[p["base_cluster"] for p in cfg["ports_in"]],
            PCLS=[p["clusters"] for p in cfg["ports_in"]],
            PNMAPS=[(-(-p["clusters"] // in_page)
                     if p.get("map_mode", "static") == "dynamic"
                     else p["maps"]) for p in cfg["ports_in"]],
            SAAF=[s.get("kind", "aaf") == "aaf" for s in in_streams],
            SCH=[(((int(s["formats"][0], 16) >> 22) & 0x3FF)
                  if s.get("kind", "aaf") == "aaf" else 0)
                 for s in in_streams],
        )
    od = {"EMIT": dout_any}
    if dout_any:
        out_streams = overlay["stream_outputs"]
        so_ch = [((int(s["formats"][0], 16) >> 22) & 0x3FF)
                 for s in out_streams]
        slotb, acc = [], 0
        for channels in so_ch:
            slotb.append(acc)
            acc += (channels + 1) // 2
        pcls, pcbase, sch, csrc = [], [], [], []
        for j, p in enumerate(overlay["stream_ports"]["output"]):
            pcls.append(p["clusters"])
            pcbase.append(len(csrc))
            stream = p.get("stream_index", j)
            sch.append(so_ch[stream])
            srcs = aem_store._out_cluster_sources(overlay, j, p)
            if srcs is None:
                srcs = [dict(src=3, idxh=0,
                             idx=slotb[stream] + c // 2, half=c % 2,
                             valid=slotb[stream] + c // 2 < 16)
                        for c in range(p["clusters"])]
            csrc.extend(srcs)
        od.update(PCLS=pcls, PCBASE=pcbase, SCH=sch, CSRC=csrc)
    L, T = len(cfg["listeners"]), len(cfg["talkers"])
    crf_o = "yes" if cfg["clocking"]["crf_output"] else "no"
    crf_s = "yes" if cfg["clocking"]["crf_sink"] else "no"
    ln = []
    a = ln.append
    a("// SPDX-FileCopyrightText: 2026 Kebag Logic")
    a("// SPDX-License-Identifier: CERN-OHL-W-2.0")
    a("//--------------------------------------------------------------------"
      "-------//")
    a("//  File        : adp_shape_defaults.svh")
    a("//  Project     : Milan FPGA Platform  (ADP shape, milan_csr 0x618/0x61C)")
    a("//")
    a("//  GENERATED by sw/builder/endstation_builder.py - DO NOT EDIT.")
    a(f"//  Source      : {cfg['source']}")
    a(f"//  Shape       : {L} AAF listener(s) + {T} AAF talker(s); "
      f"CRF sink {crf_s}, CRF output {crf_o}")
    a("//  Description : The entity's ADVERTISED SHAPE - the 1722.1-2021")
    a("//                6.2.1.9/6.2.1.11 ADPDU counts served READ-ONLY at")
    a("//                0x618/0x61C, and the source/sink context counts")
    a("//                milan_datapath elaborates. Same numbers as this")
    a("//                config's AEM STREAM_OUTPUT / STREAM_INPUT descriptor")
    a("//                counts (one config, one pass; check_entity_shape.py")
    a("//                compares them).")
    a("//                Include-only: no `default_nettype directive, no")
    a("//                include guard, no net decls.")
    a("//--------------------------------------------------------------------"
      "-------//")
    a("")
    a("  //! talker_stream_sources = STREAM_OUTPUT descriptors = the ACMP")
    a("  //! talker_unique_id range (AAF talkers, then the CRF Media Clock")
    a("  //! Output at uid = the AAF talker count when this config has one)")
    a(f"  localparam int ADP_TALKER_SRC_C    = {sh['talker_stream_sources']};")
    a("  //! listener_stream_sinks = STREAM_INPUT descriptors = the ACMP")
    a("  //! listener_unique_id range (AAF sinks, then the CRF sink)")
    a(f"  localparam int ADP_LISTENER_SINK_C = {sh['listener_stream_sinks']};")
    a("  //! talker_capabilities (1722.1-2021 Table 6.4): IMPLEMENTED |")
    a("  //! AUDIO_SOURCE, + MEDIA_CLOCK_SOURCE only when a CRF STREAM_OUTPUT")
    a("  //! exists to back it")
    a(f"  localparam logic [15:0] ADP_TALKER_CAPS_C    = "
      f"16'h{sh['talker_capabilities']:04X};")
    a("  //! listener_capabilities (Table 6.5): IMPLEMENTED | AUDIO_SINK,")
    a("  //! + MEDIA_CLOCK_SINK only when a CRF STREAM_INPUT exists")
    a(f"  localparam logic [15:0] ADP_LISTENER_CAPS_C  = "
      f"16'h{sh['listener_capabilities']:04X};")
    a("  //! Dynamic AUDIO_MAP ownership, one bit per AAF Stream Port. A set")
    a("  //! bit means the descriptor carries no static AUDIO_MAP and the")
    a("  //! ADD/REMOVE/GET_AUDIO_MAP command family owns its live routing.")
    din_mask = sum((1 << i) for i, s in enumerate(cfg["listeners"])
                   if s.get("map_mode", "static") == "dynamic")
    dout_mask = sum((1 << i) for i, s in enumerate(cfg["talkers"])
                    if s.get("map_mode", "static") == "dynamic")
    a(f"  localparam logic [63:0] ADP_DMAP_IN_MASK_C  = "
      f"64'h{din_mask:016X};")
    a(f"  localparam logic [63:0] ADP_DMAP_OUT_MASK_C = "
      f"64'h{dout_mask:016X};")
    a("  //! Dynamic input geometry is the AEM model's port-relative page")
    a("  //! partition plus its global cluster-key projection. RPHYS entries")
    a("  //! are {valid, render_crossbar_key[5:0]}; non-physical clusters")
    a("  //! remain protocol-visible mappings without aliasing a physical pin.")
    if dm["EMIT"]:
        in_keys = dm["KEYS"]
        in_page = dm["PAGE"]
        in_pbase = dm["PBASE"]
        in_pcls = dm["PCLS"]
        in_pnmaps = dm["PNMAPS"]
        in_saaf = dm["SAAF"]
        in_sch = dm["SCH"]
    else:
        in_ports = cfg["ports_in"]
        in_keys = max((p["base_cluster"] + p["clusters"]
                       for p in in_ports), default=1)
        in_page = min(max((p["clusters"] for p in in_ports), default=1), 8)
        in_pbase = [p["base_cluster"] for p in in_ports] or [0]
        in_pcls = [p["clusters"] for p in in_ports] or [1]
        in_pnmaps = [max(1, -(-p["clusters"] // in_page))
                     for p in in_ports] or [1]
        in_saaf = [True for _ in cfg["listeners"]] or [False]
        in_sch = [((int(str(s["formats"][0]), 16) >> 22) & 0x3FF)
                  for s in cfg["listeners"]] or [0]
    in_rphys = [0] * max(1, in_keys)
    for p in cfg["ports_in"]:
        for pool in p.get("pool", []):
            if pool["role"] != "physical":
                continue
            for n in range(pool["width"]):
                key = p["base_cluster"] + pool["offset"] + n
                phys = pool.get("first", 0) + n
                if key < len(in_rphys) and phys < 64:
                    in_rphys[key] = 0x40 | phys

    def sv_array(name, kind, values, render=str):
        vals = list(values) or [0]
        body = ", ".join(render(v) for v in vals)
        a(f"  localparam logic {kind} {name} [0:{len(vals)-1}] = "
          f"'{{{body}}};")

    a(f"  localparam int ADP_DMAP_IN_KEYS_C    = {max(1, in_keys)};")
    a(f"  localparam int ADP_DMAP_IN_PAGE_C    = {in_page};")
    a(f"  localparam int ADP_DMAP_IN_NPORTS_C  = {len(in_pbase)};")
    a(f"  localparam int ADP_DMAP_IN_NSTRIN_C  = {len(in_sch)};")
    sv_array("ADP_DMAP_IN_PBASE_C", "[6:0]", in_pbase,
             lambda v: f"7'd{v}")
    sv_array("ADP_DMAP_IN_PCLS_C", "[6:0]", in_pcls,
             lambda v: f"7'd{v}")
    sv_array("ADP_DMAP_IN_PNMAPS_C", "[6:0]", in_pnmaps,
             lambda v: f"7'd{v}")
    sv_array("ADP_DMAP_IN_RPHYS_C", "[6:0]", in_rphys,
             lambda v: f"7'h{v:02X}")
    sv_array("ADP_DMAP_IN_SAAF_C", "", in_saaf,
             lambda v: "1'b1" if v else "1'b0")
    sv_array("ADP_DMAP_IN_SCH_C", "[9:0]", in_sch,
             lambda v: f"10'd{v}")

    a("  //! Dynamic output geometry and capture-source words are copied")
    a("  //! from the AEM generator's ODMAP table. CSRC uses the fabric word")
    a("  //! {valid, half, src[2:0], idxh[3:0], idx[3:0]}.")
    if od["EMIT"]:
        out_pcls = od["PCLS"]
        out_pcbase = od["PCBASE"]
        out_sch = od["SCH"]
        out_csrc = [((1 if s.get("valid", True) else 0) << 12)
                    | ((s.get("half", 0) & 1) << 11)
                    | ((s["src"] & 7) << 8)
                    | ((s.get("idxh", 0) & 0xF) << 4)
                    | (s.get("idx", 0) & 0xF)
                    for s in od["CSRC"]]
    else:
        out_pcls = [p["clusters"] for p in cfg["ports_out"]] or [1]
        out_pcbase, total = [], 0
        for clusters in out_pcls:
            out_pcbase.append(total)
            total += clusters
        out_sch = [s["channels"] for s in cfg["talkers"]] or [0]
        out_csrc = [0] * max(1, total)
    a(f"  localparam int ADP_DMAP_OUT_NPORTS_C = {len(out_pcls)};")
    a(f"  localparam int ADP_DMAP_OUT_NSRC_C    = {len(out_csrc)};")
    sv_array("ADP_DMAP_OUT_PCLS_C", "[6:0]", out_pcls,
             lambda v: f"7'd{v}")
    sv_array("ADP_DMAP_OUT_PCBASE_C", "[7:0]", out_pcbase,
             lambda v: f"8'd{v}")
    sv_array("ADP_DMAP_OUT_SCH_C", "[9:0]", out_sch,
             lambda v: f"10'd{v}")
    sv_array("ADP_DMAP_OUT_CSRC_C", "[12:0]", out_csrc,
             lambda v: f"13'h{v:04X}")
    a("  //! THE WIRE CHANNEL CONSTANT (roadmap item 00): channels_per_frame")
    a("  //! the FRAMER emits, derived from the capture front-end this config")
    a("  //! elaborates - NOT from any declared format and NOT from `clusters`")
    a("  //! (the AEM AUDIO_CLUSTER count, which is not the wire width). It")
    a("  //! sits here so that 'what we advertise' and 'what we emit' are one")
    a("  //! generated pass apart and can be compared:")
    a("  //! scripts/check_wire_accountability.py does exactly that.")
    a(f"  localparam int TALKER_WIRE_CHANS_C = {framer_wire_channels(cfg)};")
    a("  //! gptp_domain_number - ADPDU byte 48 (1722.1-2021 6.2.1.16), served")
    a("  //! from CSR 0x62C. It is the RESET value of that register, not a")
    a("  //! read-only word, and the reason is Milan v1.2 5.3.6.1: the gPTP")
    a("  //! domain number is DYNAMIC STATE the PAAD-AE 'shall maintain and")
    a("  //! expose through the Control layer', not a build-time constant. A")
    a("  //! write is already wired to the notification duty - gptp_domain_i is")
    a("  //! a term of w_avbi_sig (KL_aecp_response_builder.sv:2260), so a change")
    a("  //! raises the unsolicited GET_AVB_INFO push Milan Table 5.22 requires.")
    a("  //! It now BOOTS holding the same number the builder wrote into this")
    a("  //! config's /etc/gptp.<board>.cfg domainNumber line.")
    a("  //! NOTE the value is not free: Milan 2 pins [802.1AS] to 802.1AS-2011")
    a("  //! +Cor1-2013 +Cor2-2015 (NOT -2020), and 802.1AS-2011 8.1 states 'The")
    a("  //! domain number of a gPTP domain shall be 0'. Multi-domain is an")
    a("  //! 802.1AS-2020 feature Milan v1.2 does not adopt, so any non-zero")
    a("  //! gptp.domain is out of spec for a Milan network - it is accepted")
    a("  //! here only because the same config drives non-Milan bench setups.")
    a("  //! Before this constant the two came from different places - the cfg")
    a("  //! from gptp.domain, the register from a hardcoded")
    a("  //! `w 0x62C 0x00000000` in avdecc/aecp_csr_setup.sh - and agreed only")
    a("  //! because the shipping config happens to say 0. A config that said 1")
    a("  //! would have run ptp4l on domain 1 while ADP advertised domain 0,")
    a("  //! silently. One YAML section, one number (USER 2026-08-05).")
    a(f"  localparam int ADP_GPTP_DOMAIN_C   = "
      f"{(cfg.get('gptp') or {}).get('domain', 0)};")
    a("")
    #! STREAM_INPUT[0]'s declared stream_format, as a 64-bit constant.
    #!
    #! WHY IT MOVED HERE.  It used to reach the fabric as the RESET VALUE of
    #! the repository-local AECP response builder's fmt_in0_r, taken from the
    #! generated AEM ROM (AEM_STRIN_FMT_C[0]).  That local engine and ROM are
    #! deleted. The constant is not the processor's dynamic store to own:
    #! KL_avtp_rx_monitor_ctx compares every
    #! arriving AVTPDU's subtype/format against it (fmt0_i), so it decides
    #! whether stream 0 can accept a frame AT ALL. SET_STREAM_FORMAT remains
    #! unimplemented, so it is a fixed entity-model fact and belongs here.
    #! Tying it to zero (the first cut of the plane deletion) made the compare
    #! fail for every conformant AAF PDU: stream 0 accepted nothing, on every
    #! build.  Same class as the presentation-time default, same fix.
    #!
    #! The FIRST declared format is the one the descriptor reports as current,
    #! which is exactly what the deleted register file reset to.
    fmts0 = ((cfg.get("listeners") or [{}])[0].get("formats") or ["0x0"])
    f0 = int(str(fmts0[0]), 16)
    a("  //! STREAM_INPUT[0]'s declared DEFAULT stream_format - the value")
    a("  //! KL_avtp_rx_monitor_ctx accepts frames against until a controller")
    a("  //! SET_STREAM_FORMATs the stream, and the base whose 48 kHz family")
    a("  //! the format verdict admits. Was the AEM ROM's AEM_STRIN_FMT_C[0];")
    a("  //! the ROM is gone and this is the same number from the same config.")
    a(f"  localparam logic [63:0] ADP_STRIN0_FMT_C = 64'h{f0:016X};")
    #! the CRF Media Clock stream format, for the same reason: the format
    #! verdict must admit exactly what the CRF descriptors advertise, and
    #! clocking.crf_format is the same config fact the descriptor path reads.
    cf0 = int(str((cfg.get("clocking") or {}).get(
        "crf_format", "0x041060010000BB80")), 16)
    a("  //! the CRF Media Clock stream format the entity advertises: the")
    a("  //! ONE format SET_STREAM_FORMAT may name for the CRF rows, and the")
    a("  //! current format their GET serves. Same config fact as the image's")
    a("  //! CRF_FORMATS entry.")
    a(f"  localparam logic [63:0] ADP_CRF_FMT_C = 64'h{cf0:016X};")
    a("")
    return "\n".join(ln)


def rtl_firmware_version(rev=0):
    """This gateware's version string for the ENTITY descriptor.

    Delegates to avdecc/gen_aem_store.py, which parses `parameter logic
    [31:0] VERSION` out of hdl/common/csr/milan_csr.sv - the one place the
    gateware's version exists - and is also where the string gets stamped
    into the descriptor bytes.  ONE parser, so the builtin model, every
    config-derived ROM and the TB golden cannot disagree about the version
    the way the configs and the fabric did until 2026-07-28.

    Yes, the builder reads RTL here.  It already does (rtl_capability_marks,
    and test gate 21a parses module parameters): a build parameter whose
    truth lives in the RTL is read from the RTL, not copied beside it."""
    sys.path.insert(0, os.path.join(ROOT, "avdecc"))
    import gen_aem_store as g
    return g.firmware_version_string(rev)


def rtl_version():
    """`(major, minor)` behind the read-only VERSION register - the raw pair
    rtl_firmware_version() renders, for artifacts that want to show both."""
    sys.path.insert(0, os.path.join(ROOT, "avdecc"))
    import gen_aem_store as g
    return g.rtl_version()


def emit_aem_rom_svh(cfg, overlay):
    """This config's legacy AEM SVH rendering.

    Nothing compiles this result. Its former include consumer,
    KL_aecp_aem_store.sv, was deleted with hdl/ieee17221/aecp. The current
    processor serves READ_DESCRIPTOR from the flat DRAM image emitted by
    _entity_model_image(). This compatibility rendering is still generated
    for two reasons that are not decorative: (1) the descriptor set is the
    declarative entity definition from which adp_shape() derives
    talker_stream_sources, listener_stream_sinks, and the capability words
    that reach silicon through gen/adp_shape_defaults.svh; (2) building it is
    the check that the declared model is expressible at all. A shape whose
    descriptor set cannot be generated has a shape count nobody should trust,
    which is why --write-rtl refuses on that failure.

    Written to out/<cfg>/aecp_aem_rom.svh only. See the module banner."""
    sys.path.insert(0, os.path.join(ROOT, "avdecc"))
    import gen_aem_store as g
    return g.emit_svh_text(g.build_model(g.spec_from_overlay(overlay)))


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


def load_features(raw):
    """Normalize `board.features`. Missing block or missing key = PRESENT."""
    raw = raw or {}
    if not isinstance(raw, dict):
        raise ConfigError("board.features: must be a mapping of "
                          f"{sorted(OPTIONAL_BLOCKS)} -> bool")
    unknown = sorted(set(raw) - set(OPTIONAL_BLOCKS))
    if unknown:
        raise ConfigError(f"board.features: unknown block(s) {unknown} "
                          f"(known: {sorted(OPTIONAL_BLOCKS)})")
    out = {}
    for k in OPTIONAL_BLOCKS:
        v = raw.get(k, True)
        if not isinstance(v, bool):
            raise ConfigError(f"board.features.{k} must be a boolean (got "
                              f"{v!r}); true = PRESENT (the default)")
        out[k] = v
    return out


def validate_features(feat, cons, clocking, interface, srp, platform):
    """THE GATE (docs/design/AREA_BUDGET.md rule 5): refuse a config that asks
    for a feature one of the prune parameters removed. A silently absent
    feature is the decorative-ABI defect in reverse - the register window
    still answers, the block behind it is gone - and this project has been
    bitten by exactly that (dead RMON, the `p_AAF_PLAYBACK` name typo that
    pruned nothing, the 0x8F8 dead read). Each rule below names the config
    element that makes the block load-bearing, so the contradiction is
    reported against something the author actually wrote."""
    # 1. media-clock servo: it is the ACTUATOR for a media clock the fabric
    #    recovers. Internal-only clocking never engages it (the servo idles
    #    unless clock_source != 0), so that is the one shape it may go.
    if not feat["media_clock_servo"]:
        ext = sorted(set(clocking["media_clock_sources"]) - {"internal"})
        if ext:
            raise ConfigError(
                f"board.features.media_clock_servo: false prunes "
                "KL_mmcm_drp_servo, but clocking.media_clock_sources offers "
                f"{ext} - those sources are RECOVERED clocks and the servo is "
                "what disciplines the audio MMCM to them. Restrict "
                "media_clock_sources to [internal] (and clocking.crf_sink to "
                "false) or keep the servo.")
    # 2. latency taps: pure instrumentation, so the contradiction is with a
    #    build that has explicitly asked to KEEP its instrumentation.
    if not feat["latency_taps"] and not cons["strip_probes"]:
        raise ConfigError(
            "board.features.latency_taps: false prunes KL_aaf_latency_taps "
            "and makes the whole LTAP window (0x870-0x8B0) read a structural "
            "zero, but board.constraints.strip_probes is false - this build "
            "has asked to keep its instrumentation. Set strip_probes: true "
            "(a build that ships no probes) or keep the taps.")
    # 3. MAAP: load-bearing exactly when the stream DMACs are allocated at
    #    run time rather than provisioned in this file.
    if not feat["maap"] and srp["stream_dmac_alloc"] == SRP_DMAC_DYNAMIC:
        raise ConfigError(
            "board.features.maap: false prunes KL_maap, but "
            f"srp.stream_dmac_base is '{SRP_DMAC_DYNAMIC}' = the addresses "
            "are claimed at run time by that engine. Provision a static "
            "multicast base instead, or keep MAAP.")
    # 4. I2S playback: the i2s_philips interface's RENDER half IS
    #    KL_i2s_playback (INTERFACES rtl note), so pruning it guts the
    #    declared physical interface.
    if not feat["i2s_playback"] and interface["kind"] == "i2s_philips":
        raise ConfigError(
            "board.features.i2s_playback: false prunes KL_i2s_playback, "
            "which is the RENDER half of audio_interface.kind 'i2s_philips' "
            "- the config declares a DAC this build would not be able to "
            "drive. Declare an interface without a local DAC render path, or "
            "keep playback.")
    # 5. RX filter: the port's address-filtering policy has to say so.
    if not feat["rx_mac_filter"] and platform["rx_address_filter"] == "hardware":
        raise ConfigError(
            "board.features.rx_mac_filter: false prunes rx_mac_filter + its "
            "TCAM, but platform.rx_address_filter is 'hardware'. A pruned "
            "filter makes the port PROMISCUOUS (the RX stream becomes a "
            "straight wire to the DMA port), which is a change in what the "
            "station accepts. Declare rx_address_filter: software (the host "
            "drops non-matching frames) or promiscuous, or keep the filter.")
    # 6. render LPF: its ONLY consumer in milan_datapath is KL_i2s_playback
    #    (pcm_lpf_tdata/tvalid -> i2s_player.lpf_*; pcm_lpf_active ->
    #    KL_i2s_feed_mux, which exists to feed the same player). Keeping the
    #    filter in a build with no player therefore synthesises a filter
    #    nothing can hear - the mirror image of a silently absent feature,
    #    and just as much a lie about what the gateware does.
    if feat["render_lpf"] and not feat["i2s_playback"]:
        raise ConfigError(
            "board.features: render_lpf is true but i2s_playback is false. "
            "KL_pcm_lpf's only consumer is KL_i2s_playback, so this build "
            "would synthesise a render filter with nothing behind it. Set "
            "render_lpf: false as well, or keep i2s_playback.")
    return feat


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
    # THE PROTOCOL PROCESSOR'S DRAM WINDOW, immediately below the PCM ring.
    # Both regions are reserved `no-map` and both are DERIVED from the one
    # address the config states, so a board cannot end up with a gateware that
    # reads one place and a kernel that protects another. That is not a
    # hypothetical: the base used to be computed independently in
    # sw/litex/milan_soc.py as "top of main_ram", which at the 1x1 shape landed
    # in kernel RAM and at the 8x8 shape landed INSIDE this ring.
    p["pp_mem_bytes"] = PP_MEM_BYTES
    p["pp_mem_phys"] = p["pcm_ring_phys"] - PP_MEM_BYTES
    if p["pp_mem_phys"] <= 0:
        raise ConfigError(
            f"platform.pcm_ring_phys 0x{p['pcm_ring_phys']:X} leaves no room "
            f"below it for the protocol processor's 0x{PP_MEM_BYTES:X}-byte "
            "window")
    phy = DT_PHY_MODE.get(cons["phy"])
    if phy is None:
        raise ConfigError(f"platform: no DT phy-mode for board phy "
                          f"'{cons['phy']}' (known {sorted(DT_PHY_MODE)})")
    if p["rx_address_filter"] not in RX_ADDRESS_FILTERS:
        raise ConfigError(f"platform.rx_address_filter "
                          f"'{p['rx_address_filter']}' not in "
                          f"{list(RX_ADDRESS_FILTERS)}")
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
        # The window sw/litex/milan_soc.py compiles into the gateware as
        # PP_DESC_BASE_P / PP_RESP_BASE_P. Published here so the SoC READS it
        # rather than deriving it a second way - the device tree above reserves
        # exactly these bytes, and the two must be the same bytes.
        "pp_mem": dict(phys=f"0x{p['pp_mem_phys']:08X}",
                       bytes=f"0x{p['pp_mem_bytes']:X}"),
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
    a("")
    # The protocol processor's descriptor store READS the entity model from
    # here and its AECP response buffer WRITES here, both at bases compiled
    # into the bitstream. Unreserved, this is ordinary kernel RAM and those
    # writes land on whatever the allocator handed out - silently, because no
    # counter on either side reports it. `no-map` additionally keeps the region
    # out of the kernel's linear map, which is what lets the loader reach it
    # through /dev/mem on a CONFIG_STRICT_DEVMEM kernel.
    a(f"\t\tppmem: ppmem@{p['pp_mem_phys']:x} {{")
    a(f"\t\t\treg = <0x{p['pp_mem_phys']:x} 0x{p['pp_mem_bytes']:x}>;")
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
        # 1722.1-2021 6.2.2.8: the model is "changed" if ANY descriptor field
        # differs, excluding a short list this is not on - and a changed model
        # "shall use a new unique entity_model_id". Controllers cache the model
        # BY this id, so shipping moved fields under an unchanged id serves
        # every controller that has ever met this device a stale layout from
        # its own cache: an entity that enumerates wrongly and cannot be
        # cleared from the device side.
        #
        # UNCONDITIONAL, unlike the shape keys below it. Those are conditional
        # precisely so existing ids do NOT move; this one exists to move them,
        # and it must move every id at once because the layout change was not
        # optional per config. Bump it whenever the descriptor BYTE LAYOUT
        # changes - not when a field's value changes, which the rest of the
        # shape already covers.
        "aem_layout": AEM_LAYOUT_REV,
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
    # D8 role pools change the descriptor set (cluster counts AND which pool
    # the static map is written against), so they are model shape. CONDITIONAL
    # on the policy so every config that predates D8 hashes to exactly what it
    # hashed before. Cluster object_names are DELIBERATELY absent: 1722.1
    # 6.2.2.8 excludes object_name from "the structure of the data model", so
    # the D10 rename must not - and does not - move any entity_model_id.
    # gPTP clock attributes are DESCRIPTOR CONTENT (AVB_INTERFACE 7.2.8),
    # and controllers cache descriptor content by entity_model_id - so a
    # config that states them must rotate its hash when they change.
    # CONDITIONAL: configs without the section hash exactly as before.
    if cfg.get("gptp") is not None:
        shape["gptp"] = cfg["gptp"]
    if i["cluster_policy"] == "role-pools":
        shape["cluster_pools"] = {
            "physical": [i["physical_channels"]["capture"],
                         i["physical_channels"]["render"]],
            "host": int(i["cluster_pools"].get("host", 0)),
            "pilot": bool(i["cluster_pools"].get("pilot", False)),
            "loopback": int(i["cluster_pools"].get("loopback", 0)),
        }
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
    # THE FIRMWARE VERSION IS NOT A CONFIG DECLARATION.  It is a fact about
    # the gateware, it lives in hdl/common/csr/milan_csr.sv's VERSION
    # parameter, and it is DERIVED here.  A config copy - even one that
    # happens to agree today - is a second answer to "what version is this",
    # and the second answer is the one controllers get: all three configs
    # said "0.1.0" while the fabric was at 0x0001_0016, so every board we
    # ship told Hive it ran firmware 0.1.0.  Refuse the key outright rather
    # than compare-and-prefer: an agreeing copy still has to be edited in two
    # places on every ABI bump, which is how it stops agreeing.
    if "firmware_version" in ent:
        raise ConfigError(
            f"entity.firmware_version: remove it. The firmware version is "
            f"derived from the gateware's VERSION parameter "
            f"(hdl/common/csr/milan_csr.sv), which is where it lives; this "
            f"build derives {rtl_firmware_version()!r}. For a firmware "
            f"respin with no CSR-ABI change use entity.firmware_rev.")
    rev = ent.get("firmware_rev", 0)
    if isinstance(rev, bool) or not isinstance(rev, int) or rev < 0:
        raise ConfigError(
            f"entity.firmware_rev: {rev!r} is not a non-negative integer")
    n = dict(
        name=_req(ent, "name", "entity"),
        vendor_name=ent.get("vendor_name", "Kebag Logic"),
        firmware_version=rtl_firmware_version(rev),
        firmware_rev=rev,
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
        num_queues=int(c.get("num_queues", 5)),   # = NUMBER_OF_QUEUES; gate 18c
                                                  # pins this against the package,
                                                  # so a stale 4 here would make
                                                  # every config that omits the
                                                  # key fail rather than build
        hs_page_bytes=_pow2(c.get("hs_page_bytes", 16384),
                            "board.constraints.hs_page_bytes"),
        strip_probes=bool(c.get("strip_probes", True)),
        eth_port=c.get("eth_port"),
        # milan_datapath LPF_P (docs/design/AREA_BUDGET.md): the
        # render-tap Butterworth is PRESENT unless a config prunes it, so
        # omitting the key leaves every existing argv byte-identical.
        render_lpf=bool(c.get("render_lpf", True)),
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
    # NOT a power of two: the USER's egress map is FIVE queues
    # (q4 class A .. q0 best effort, docs/reference/EGRESS_QUEUE_MAP.md) -
    # the six-queue map missed placement on the xc7a100t by 282 slices and
    # the spare queue was dropped. The ceiling is what ceil(log2 N) can index
    # inside one 32-bit CLS_TC_QUEUE_MAP word (8 traffic classes x 4 bits),
    # i.e. 16; the RTL tables are written out to 5, so hold the gate at 8.
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
    if rate not in BASE_RATE_HZ:
        raise ConfigError(f"sampling_rate_hz {rate} not an AAF base rate "
                          f"(Milan v1.2 6.2: {sorted(BASE_RATE_HZ)})")
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

    # gPTP clock attributes (OPTIONAL, opt-in): ONE source for the
    # AVB_INTERFACE descriptor's static clock fields AND the generated
    # ptp4l config, so the entity can never advertise a clock posture the
    # daemon does not run (USER 2026-08-05: "why is the gPTP configuration
    # (priority1 etc) not correctly reflected into the avb_interface").
    # Absent => the descriptor keeps its historical constants byte-exactly
    # and NO gptp.cfg fragment is generated. Present => the section joins
    # model_shape, so a changed clock posture rotates a hash-derived
    # entity_model_id (controllers cache descriptor content by model id -
    # measured 2026-08-05: a stale cached model offered ports the flashed
    # entity did not have).
    gp_raw = cfg.get("gptp")
    gptp = None
    if gp_raw is not None:
        _known_gp = {"priority1", "priority2", "clock_class",
                     "clock_accuracy", "offset_scaled_log_variance",
                     "domain", "log_sync_interval", "log_announce_interval",
                     "log_pdelay_interval"}
        if not isinstance(gp_raw, dict) or set(gp_raw) - _known_gp:
            raise ConfigError(f"gptp: unknown keys "
                              f"{sorted(set(gp_raw) - _known_gp)} "
                              f"(known: {sorted(_known_gp)})")
        def _gp_u8(k, dflt):
            v = int(gp_raw.get(k, dflt))
            if not 0 <= v <= 255:
                raise ConfigError(f"gptp.{k} {v} outside 0..255")
            return v
        def _gp_domain():
            """gptp.domain, and the ONLY legal value is 0 (USER 2026-08-11).

            Milan v1.2 section 2 pins [802.1AS] to IEEE Std 802.1AS-2011 plus
            Cor1-2013 and Cor2-2015 - explicitly NOT 802.1AS-2020 - and
            802.1AS-2011 8.1 states: "The domain number of a gPTP domain shall
            be 0."  Multiple gPTP domains are an 802.1AS-2020 feature that
            Milan v1.2 does not adopt, so on a Milan network the number is a
            constant the entity REPORTS, never a parameter it chooses.

            This is not pedantry about an unused field.  Milan defines "the
            same gPTP domain" OPERATIONALLY, by grandmaster identity - 5.5.2:
            the source and sink "are located in the same gPTP domain (gPTP
            grandmaster IDs are the same)".  So the discriminator in ACMP
            binding is the GM id at CSR 0x624/0x628, and a non-zero
            domainNumber here would not select a second domain - it would
            simply make our ADPDU byte 48 disagree with every conformant peer
            on the wire while changing nothing about who we bind to.

            DO NOT confuse this with a CLOCK_DOMAIN.  Milan uses the word
            "domain" for five different things and the media-clock sense
            outnumbers this one 56 to 5: `clock domain` is the AEM
            CLOCK_DOMAIN descriptor and the `clock_domain_index` every STREAM
            descriptor carries, and it has nothing to do with 802.1AS.
            Redundancy is NOT a domain either - Milan 8.2.3 calls those the
            "Primary network and secondary network", paired by
            `redundant_streams` (8.2.5), and this build does not implement
            Section 8 at all."""
            v = int(gp_raw.get("domain", 0))
            if v != 0:
                raise ConfigError(
                    f"gptp.domain {v} is not 0: Milan v1.2 section 2 pins "
                    f"802.1AS-2011, whose 8.1 says 'The domain number of a "
                    f"gPTP domain shall be 0'. Multi-domain is an 802.1AS-2020 "
                    f"feature Milan does not adopt. If you meant a media clock "
                    f"domain, that is the CLOCK_DOMAIN descriptor, not this.")
            return v

        def _gp_s8(k, dflt):
            v = int(gp_raw.get(k, dflt))
            if not -128 <= v <= 127:
                raise ConfigError(f"gptp.{k} {v} outside -128..127")
            return v
        oslv = int(gp_raw.get("offset_scaled_log_variance", 0xFFFF))
        if not 0 <= oslv <= 0xFFFF:
            raise ConfigError(
                f"gptp.offset_scaled_log_variance {oslv} outside 0..65535")
        gptp = dict(
            priority1=_gp_u8("priority1", 248),
            priority2=_gp_u8("priority2", 248),
            clock_class=_gp_u8("clock_class", 248),
            clock_accuracy=_gp_u8("clock_accuracy", 0xFE),
            offset_scaled_log_variance=oslv,
            domain=_gp_domain(),
            log_sync_interval=_gp_s8("log_sync_interval", -3),
            log_announce_interval=_gp_s8("log_announce_interval", 0),
            log_pdelay_interval=_gp_s8("log_pdelay_interval", 0),
        )

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
    # PHYSICAL truth, per direction. Defaults to the declared interface width
    # (every existing config keeps exactly the roles it had), but a platform
    # that routes no audio pins says so HERE rather than letting the model
    # advertise a pool the fabric cannot back - see CLUSTER_ROLES.
    pc = aif.get("physical_channels")
    if pc is None:
        phys = dict(capture=iinfo["channels"], render=iinfo["channels"])
    else:
        if not isinstance(pc, dict) or set(pc) - {"capture", "render"}:
            raise ConfigError("audio_interface.physical_channels must be a "
                              "mapping with keys capture/render (channels the "
                              "BOARD actually routes, per direction)")
        phys = dict(capture=int(pc.get("capture", iinfo["channels"])),
                    render=int(pc.get("render", iinfo["channels"])))
    for d, v in phys.items():
        if not 0 <= v <= iinfo["channels"]:
            raise ConfigError(
                f"audio_interface.physical_channels.{d} {v} outside "
                f"0..{iinfo['channels']} (the {kind} interface width) - a "
                "board cannot route more channels than the selected "
                "interface family carries")
    # D8 role pools. Only role-pools consumes them; declaring pools under
    # another policy is a config that means two different things at once.
    pools = cm.get("pools") or {}
    if not isinstance(pools, dict) or set(pools) - {"host", "pilot",
                                                    "loopback"}:
        raise ConfigError("audio_interface.cluster_mapping.pools must be a "
                          "mapping with keys host/pilot/loopback (the "
                          "physical pool width comes from "
                          "audio_interface.physical_channels)")
    if pools and policy != "role-pools":
        raise ConfigError(
            f"audio_interface.cluster_mapping.pools is only read by the "
            f"role-pools policy; this config selects '{policy}', so the pools "
            "would be silently ignored (D8)")
    # task #65: WHICH POOL SOURCES THIS BUILD ACTUALLY ELABORATES. A pool is a
    # MODEL fact (the clusters exist and are named); whether the fabric can
    # feed it is a BUILD fact, and the two were allowed to disagree - the AX
    # declared 8 loopback clusters per talker port and woke with every talker
    # channel mapped to one, while milan_datapath left KL_chan_map_capture's
    # LOOP feed unconnected. Result: a conformant-looking GET_AUDIO_MAP over a
    # stream of digital silence. This block is the single declaration that
    # drives BOTH the milan_soc argv and the power-on map, so they cannot
    # drift apart again. Omitted entirely => today's answers exactly.
    fab = cm.get("fabric") or {}
    if not isinstance(fab, dict) or set(fab) - {"loopback_lane",
                                                "playback_rings"}:
        raise ConfigError(
            "audio_interface.cluster_mapping.fabric must be a mapping with "
            "keys loopback_lane (bool: milan_soc --loopback-lane, the rx -> "
            "talker LOOP bucket) and/or playback_rings (int: milan_soc "
            "--aaf-playback-streams, the KL_pcm_tx rings behind the host "
            "pool)")
    if fab and policy != "role-pools":
        raise ConfigError(
            "audio_interface.cluster_mapping.fabric is only read by the "
            f"role-pools policy; this config selects '{policy}'")
    lb_lane = bool(fab.get("loopback_lane", False))
    if lb_lane and not int(pools.get("loopback", 0)):
        raise ConfigError(
            "cluster_mapping.fabric.loopback_lane is set but pools.loopback "
            "is 0: the build would carry the rx -> talker LOOP bucket "
            "(+2303 LUT / +1542 FF at 8x8) with no cluster naming it")
    pb_rings = fab.get("playback_rings")
    if pb_rings is not None:
        pb_rings = int(pb_rings)
        if pb_rings < 1:
            raise ConfigError(
                f"cluster_mapping.fabric.playback_rings {pb_rings} must be "
                ">= 1 (omit the key to leave the host pool's ring bound at "
                "the fabric maximum)")
    # USER 2026-08-05: the port channel space can be NAMED from the config
    # ("prepare it to be software defined"): channel_names[k] names channel k
    # of every stream port - host clusters verbatim, loopback/physical ones
    # role-prefixed. 1722.1-2021 6.2.2.8 excludes object_name from the model
    # shape, so names never move a hash-derived entity_model_id.
    names = aif.get("channel_names")
    if names is not None:
        if (not isinstance(names, list) or not names
                or not all(isinstance(n, str) and 0 < len(n) <= 48
                           for n in names)):
            raise ConfigError(
                "audio_interface.channel_names must be a non-empty list of "
                "strings (each 1..48 chars), one per port channel")
        need = max(int(pools.get("host", 0)), phys["capture"], phys["render"])
        if len(names) < need:
            raise ConfigError(
                f"audio_interface.channel_names has {len(names)} names but "
                f"this shape's widest named pool needs {need}")
    interface = dict(
        kind=kind, channels=iinfo["channels"], word_length_bits=wl,
        cluster_policy=policy, rtl=iinfo["rtl"],
        physical_channels=phys, cluster_pools=pools,
        channel_names=names,
        cluster_fabric=dict(loopback_lane=lb_lane, playback_rings=pb_rings),
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
    # the AUDIO_UNIT's current rate is the one a stream's default Base format
    # is stated at: Milan 5.3.3.3 makes the AUDIO_UNIT list the Audio Unit's
    # truth, and 5.3.3.4 makes the formats list the Stream's - a stream
    # defaulting to a rate the unit does not report would put the two at odds.
    listeners = _streams(_req(st, "listeners", "streams"), "streams.listeners",
                         "listener", clocking["sampling_rate_hz"])
    talkers = _streams(_req(st, "talkers", "streams"), "streams.talkers",
                       "talker", clocking["sampling_rate_hz"])

    # The capture crossbar currently has one image-wide static/dynamic
    # selector. A mixed set of Stream Port Outputs would therefore switch a
    # static port to the empty dynamic RAM whenever any sibling was dynamic.
    # Milan permits either mode per output, but this implementation only
    # supports a uniform output mode and must refuse an unsafe image.
    output_map_modes = {s["map_mode"] for s in talkers}
    if len(output_map_modes) > 1:
        raise ConfigError(
            "streams.talkers: mixed static/dynamic map_mode is unsupported; "
            "the capture mapping fabric selects one mode for all Stream "
            "Port Outputs, so declare every talker static or every talker "
            "dynamic")

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

    # the framer's emitted width, for the TSpec derivation (802.1Q
    # 35.2.2.8.4 a): the frame the talker WILL PRODUCE). Computed on a shim
    # carrying exactly the keys framer_wire_channels consumes.
    wire_ch = framer_wire_channels(dict(talkers=talkers, interface=interface,
                                        board_target=target))
    srp = load_srp(cfg.get("srp"), listeners, talkers, clocking, cons,
                   BOARDS[target], wire_channels=wire_ch)
    platform = load_platform(cfg.get("platform"), cons, target, listeners)

    # optional-block prunes (docs/design/AREA_BUDGET.md tier 1). Loaded last
    # because the gate cross-checks against clocking / interface / srp /
    # platform - a prune is only wrong RELATIVE to what the rest asked for.
    features = validate_features(load_features(brd.get("features")),
                                 cons, clocking, interface, srp, platform)

    out = dict(
        source=os.path.relpath(path, ROOT),
        name=os.path.splitext(os.path.basename(path))[0],
        entity=entity, board_target=target, constraints=cons,
        clocking=clocking, interface=interface,
        listeners=listeners, talkers=talkers, soc=soc, srp=srp,
        platform=platform, features=features, gptp=gptp,
    )

    # per-stream port layout (needed by the model-id hash and the overlay)
    out["ports_in"], out["ports_out"] = cluster_layout(
        listeners, talkers, policy, interface["channels"],
        phys=phys, pools=pools,
        lb_backed=interface["cluster_fabric"]["loopback_lane"])

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
    if interface_is_placeholder(cfg):
        marks.append((f"audio interface {kind}",
                      "planned (item 4 subtask - TDM header + SoC wiring)",
                      "PLACEHOLDER: the ser/des RTL (KL_tdm_capture) exists and "
                      "is TB-proven, but NOTHING DRIVES IT - sw/litex/milan_soc.py "
                      "ties i_tdm_bclk_i / i_tdm_fsync_i / i_tdm_data_i to 0 on "
                      "every SoC and no platform provides TDM pads, so fsync "
                      "never toggles and the front-end yields no pairs. The "
                      "declaration is KEPT (it states what the product will be) "
                      "but --audio-interface is NOT emitted, so the build "
                      "elaborates the I2S front-end the board actually has "
                      "instead of a TDM front-end on a dead bus whose talkers "
                      "would emit no frame at all. Wire the header and this "
                      "becomes 'supported' with no config change."))
    elif kind in RTL_TODAY["interfaces"]:
        marks.append((f"audio interface {kind}", "supported",
                      "KL_i2s_playback / aaf_talker_i2s" if kind == "i2s_philips"
                      else ("KL_tdm_capture_master (the fabric MASTERS the bus: "
                            "it generates bclk/fsync off its own MMCM output at "
                            "2 x SLOTS x 32 x 48 kHz, so nothing external has to "
                            "drive it) -> KL_aaf_packetizer multi-channel "
                            "payload (milan_soc.py --audio-interface "
                            "--audio-interface-master)"
                            if tdm_bus_master() else
                            "KL_tdm_capture -> KL_aaf_packetizer multi-channel "
                            "payload (milan_soc.py --audio-interface)")))
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
    # D8 role pools: the MODEL half is emitted here; each pool that has no
    # fabric source behind it is marked, never silently advertised.
    if cfg["interface"]["cluster_policy"] == "role-pools":
        pools = cfg["interface"]["cluster_pools"]
        ph = cfg["interface"]["physical_channels"]
        n_cl = (sum(p["clusters"] for p in cfg["ports_in"])
                + sum(p["clusters"] for p in cfg["ports_out"]))
        marks.append((f"D8 role-named cluster pools ({n_cl} AUDIO_CLUSTERs)",
                      "supported",
                      f"physical {ph['capture']} cap / {ph['render']} rend "
                      f"(audio_interface.physical_channels), host "
                      f"{pools.get('host', 0)}/port, pilot "
                      f"{'1' if pools.get('pilot') else '0'}/talker port, "
                      f"loopback {pools.get('loopback', 0)}/talker port; "
                      "port-relative AUDIO_MAP offsets per 1722.1 7.2.19"))
        if pools.get("pilot"):
            marks.append(("D8 Pilot cluster fan-out",
                          "planned (item 8 - D7 target-keyed dynamic maps)",
                          "the pilot SOURCE exists (KL_tone_gen, "
                          "KL_chan_map_capture src=4 TONE) and one talker "
                          "channel can select it today; fanning ONE pilot "
                          "cluster onto MANY stream channels is what the "
                          "cluster-keyed dynamic-map store forbids - D7 "
                          "flips the key to the target stream channel"))
        if pools.get("loopback"):
            lane = cfg["interface"]["cluster_fabric"]["loopback_lane"]
            marks.append((f"D8 stream-loopback lane "
                          f"({pools['loopback']} clusters/talker port)",
                          "supported" if lane else
                          "declared, fabric lever OFF (task #65)",
                          ("BOTH halves land. MODEL: the clusters exist and "
                           "are named for the rx {stream, channel} they "
                           "offer. FABRIC: milan_soc --loopback-lane sets "
                           "milan_datapath LOOPBACK_P, wiring "
                           "KL_chan_map_capture's src[6:4] = 5 SRC_LOOP "
                           "bucket to the depacketizer payload clone, so a "
                           "talker slot naming a loopback cluster carries "
                           "that received channel pair"
                           if lane else
                           "the clusters exist and are NAMED for the rx "
                           "{stream, channel} they would offer, but this "
                           "build does not elaborate the lane "
                           "(cluster_mapping.fabric.loopback_lane false -> "
                           "no --loopback-lane -> LOOPBACK_P 0), so the "
                           "bucket is tied off and a loopback cluster reads "
                           "as silence. The RTL and its TB are DONE; the "
                           "blocker is area - driving the bucket measured "
                           "+2303 LUT / +1542 FF OOC at 8x8 (32 pair holds "
                           "x 48 b that cannot be LUTRAM). The power-on map "
                           "therefore does NOT point here: primary_segment "
                           "drops the pool and the talkers wake on the host "
                           "pool instead. The clusters remain published and "
                           "protocol-mappable, while their CMAP fabric-enable "
                           "marker stays clear") +
                          ". A mapped-but-never-fed slot is DISTINGUISHABLE "
                          "from a quiet one either way: CHMAP_LOOP 0x914 "
                          "[18] LOOP_SUSPECT = mapped & ~fed, so silence "
                          "here is never a lying zero"))
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
    # AREA levers, board-level because fit is a board property: every
    # docs/design/AREA_BUDGET.md tier-1 block emits its --no-* flag HERE, in
    # OPTIONAL_BLOCKS order, ONLY when pruned - so a config that says nothing
    # produces the same bytes it always did (the AAF_PLAYBACK_P discipline).
    # block_present() folds the two prune spellings (board.features.<name>
    # and the historical constraints.render_lpf) into one answer. These flags
    # MUST live in the board opts, not only in the full soc argv: sweep.sh
    # builds from this fragment, and a prune that reaches the build plan but
    # not the fragment produces an UNPRUNED bitstream that the plan swears is
    # pruned (found 2026-07-28, the DRC UTLZ-1 round: the i2s_playback /
    # latency_taps prunes were invisible to the relaunched sweep).
    for name, (flag, _param, _why) in OPTIONAL_BLOCKS.items():
        if not block_present(cfg, name):
            opts += [flag]
    return opts


def emit_design_opts(cfg):
    """emit_board_opts + every remaining BITSTREAM-SHAPING flag: this is the
    string a sweep must carry, and the ONLY correct content for
    configs/generated/sweep_opts_<board>.sh.

    Found 2026-07-28, the second member of the check_sweep_shape header's
    class in one day: the fragment carried only board opts, so `sweep.sh
    ax7101` built the 8x8 with the DEFAULT I2S front-end and 2-channel wire
    while the config, the build plan and the tracked AEM ROM all said
    tdm32 + 8-channel (W3 zero-fill shape). check_sweep_shape passed - it
    compared only ns/rxq/l2/lpf - so three Vivado seeds fitted the WRONG,
    SMALLER datapath. The flags live in ONE place now (emit_soc_argv builds
    on this) and the gate compares all of them."""
    c = cfg["constraints"]
    argv = list(emit_board_opts(cfg))
    n_streams = max(len(cfg["listeners"]), len(cfg["talkers"]))
    if n_streams > 1:
        argv += ["--num-streams", str(n_streams)]
    # item-4 audio-interface family: the tdm kinds select the KL_tdm_capture
    # front-end generate (milan_datapath AUDIO_IF_SLOTS_P). Emitted only for
    # non-default kinds so the shipping i2s argv stays byte-identical;
    # aes3/spdif have no ser/des RTL yet (planned mark) and emit nothing.
    # A PLACEHOLDER interface is not emitted (USER 2026-07-27: "the tdm can
    # be a placeholder") - see interface_is_placeholder().
    kind = cfg["interface"]["kind"]
    if kind in ("tdm8", "tdm16", "tdm32") and not interface_is_placeholder(cfg):
        argv += ["--audio-interface", kind]
        if tdm_bus_master():
            argv += ["--audio-interface-master"]
    # item-00 wire channel constant: milan_datapath TALKER_WIRE_CHANS_P,
    # emitted only above the default (the same byte-identity discipline).
    wire_chans = framer_wire_channels(cfg)
    if wire_chans != WIRE_CHANS_MIN:
        argv += ["--talker-wire-chans", str(wire_chans)]
    # CBS instance mask (2026-07-28 area lever): only the SR-class queues
    # carry a credit_based_shaper INSTANCE. DERIVED, not declared - the class
    # A queue is srp.class_queue and class B sits directly below it (the
    # 802.1Q priority order behind the reset PCP map; the USER queue
    # directive shapes exactly those two and forbids CBS above gPTP). A
    # masked-out queue is bit-identical to a built CBS with cbs_shaped_i=0,
    # which is how every non-SR queue has ALWAYS run - so this prunes ~425
    # LUT + 6 DSP per queue (ship-report figure) and moves no behaviour.
    # Emitted only when it prunes something, byte-identity as ever.
    # CLASS A ONLY (USER 2026-07-31). The class B queue used to get a
    # credit_based_shaper INSTANCE too, and it never had a stream to shape:
    # SRP_SR_CLASSES defines class A alone and load_srp REFUSES class B, Milan
    # v1.2 puts every Milan stream on class A, and the CRF Media Clock is
    # class-A-mandatory (7.3.3). So the class B shaper was pure area for a
    # class this product does not carry - measured at 417 LUT + 211 FF + 6 DSP
    # on the ax7101 8x8 (gen_cbs[3].g_cbs.u_cbs in the m0021 hierarchical
    # report), which the xc7a100t needs back: that shape misses placement by
    # 858 slices with LUTs at 99.94 % of capacity.
    #
    # This does NOT change how q3 behaves. A masked-out queue is bit-identical
    # to a built CBS with cbs_shaped_i = 0 (the same reasoning the 07-28 lever
    # rests on) - q3 simply runs unshaped strict-priority, exactly as every
    # non-SR queue always has. Re-enable by widening this expression if a
    # class B talker is ever declared; the RTL supports it unchanged.
    nq = cfg["constraints"]["num_queues"]
    cq = cfg["srp"]["class_queue"]
    cbs_mask = (1 << cq)
    if cbs_mask != (1 << nq) - 1:
        argv += ["--cbs-queues-mask", f"0x{cbs_mask:x}"]
    # task #65: the rx -> talker LOOP bucket. Emitted ONLY when declared, so
    # every config that predates the key produces a byte-identical argv. This
    # is the SAME declaration primary_segment reads, which is the whole point:
    # the flag that builds the lane and the map that points at it come from
    # one fact, so an AEM can never advertise a lane the bitstream lacks.
    if cfg["interface"].get("cluster_fabric", {}).get("loopback_lane"):
        argv += ["--loopback-lane"]
    # the KL_pcm_tx host rings behind the `host` pool. Emitted from the SAME
    # fabric declaration the AEM host clusters come from - caught 2026-08-05
    # by check_dtb_csr at FLASH time: the fragment carried no playback flag,
    # three seeds built a datapath with no pb engine under a DTB (and an AEM
    # host pool) that declared one. Only build.sh's cfg_ax7101 recipe ever
    # passed --aaf-playback; the sweep path reads THIS argv.
    pbr = cfg["interface"].get("cluster_fabric", {}).get("playback_rings")
    if pbr:
        argv += ["--aaf-playback", "--aaf-playback-streams", str(int(pbr))]
    return argv


def emit_soc_argv(cfg):
    """The milan_soc.py DESIGN argv this config implies (flow flags -
    --build/--vivado-max-threads/--place-directive/--output-dir - are
    sweep.sh's business, not the end-station definition's).

    Bitstream-shaping flags come FIRST via emit_design_opts() - the single
    emission the sweep fragment also uses - then the SoC/flow plumbing. Order
    within the argv is argparse-irrelevant; every consumer re-derives from
    this function rather than parsing the printed line."""
    c, soc = cfg["constraints"], cfg["soc"]
    argv = list(emit_design_opts(cfg))
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
    return argv


# ------------------------------------------------------------ sweep opts ----
def emit_sweep_opts(cfg):
    """Shell fragment sourced by sw/litex/sweep.sh: the per-board design
    OPTS/L2, single-sourced from the end-station config. The inline case
    tables in sweep.sh are the FALLBACK only; the builder test gate asserts
    fragment == fallback byte-for-byte on the OPTS/L2 values."""
    opts = " ".join(emit_design_opts(cfg))
    return (
        "# GENERATED by sw/builder/endstation_builder.py - DO NOT EDIT.\n"
        f"# FULL bitstream-shaping OPTS/L2/RXQ for {cfg['board_target']}, from\n"
        f"# {cfg['source']} (the last-built config of this board OWNS the\n"
        "# fragment, exactly like the tracked gen svh). Since 2026-07-28 the\n"
        "# OPTS carry EVERY design flag - num-streams, audio-interface,\n"
        "# talker-wire-chans, the tier-1 --no-* prunes - not just the board\n"
        "# constraints: a flag that reaches the build plan but not this\n"
        "# fragment builds a bitstream the plan lies about (that is how three\n"
        "# seeds fitted a 2-channel I2S datapath that every document called\n"
        "# tdm32 8-channel). sweep.sh sources this when present; its inline\n"
        "# tables are the fallback, and scripts/check_sweep_shape.py refuses\n"
        "# a launch whose effective flags disagree with SWEEP_CFG. Regenerate:\n"
        "#   python3 sw/builder/endstation_builder.py <cfg.yaml>\n"
        f'OPTS="{opts}"\n'
        # NS stated ALWAYS, even at 1: sweep.sh's inline table is the
        # fallback when the fragment is silent, so a 1-stream config that
        # omitted the key inherited the board default (8) and the shape
        # gate refused the launch (2026-08-05, first 1x1 AX sweep)
        f"NS={max(len(cfg['listeners']), len(cfg['talkers']))}\n"
        f"L2={cfg['constraints']['l2_bytes']}\n"
        f"RXQ={cfg['constraints']['rx_queues']}\n")


# -------------------------------------------------------- entity identity ---
def derive_entity_id(cfg):
    """The ATDECC entity_id (1722.1-2021 6.2.1.7) as an int.

    "mac-derived" is the EUI-48 -> EUI-64 expansion of the STATION MAC the
    platform section already declares (IEEE 802-2014 8.2 / RFC 2464: FF-FE
    injected at the OUI boundary), so the entity id and the DT `local-mac-
    address` cannot disagree. An explicit EUI-64 in the config wins."""
    eid = cfg["entity"]["entity_id"]
    if eid != "mac-derived":
        return int(eid, 16)
    b = [int(x, 16) for x in cfg["platform"]["mac_address"].split(":")]
    return int.from_bytes(bytes(b[:3] + [0xFF, 0xFE] + b[3:]), "big")


def emit_entity_conf(cfg):
    """The BOARD-SOFTWARE identity fragment - /etc/milan-entity.<board>.conf,
    sourced by the rootfs /etc/init.d/S50milan before it programs the ADP CSRs.

    Every value here is one the builder ALREADY computes and the boot script
    used to restate as a hex literal. The 2026-08-02 silicon finding is the
    reason the file exists: the flashed AEM ROM had moved (dynamic output maps)
    and the config therefore hashed to a new entity_model_id, but S50milan's
    `w 0x610 0x001BC52E` had not - and since the fabric serves the AEM ENTITY
    descriptor's entity_model_id FROM that CSR (the ROM's OVL_MODEL_ID_C
    overlay slot), the board advertised one model id over a different model.
    A controller caches AEM by model id; 1722.1-2021 6.2.1.10 makes that id the
    identity OF the model, so two AEMs under one id is a conformance break.

    The stream count and the SR VID are here for exactly the same reason and
    not one reason more: the MAAP claim COUNT is talkers+1 (the CRF Media Clock
    Output sits one past the AAF talkers - REGISTER_MAP 0x75C), and a claim
    sized for the old shape leaves the CRF's own destination address OUTSIDE
    the defended block. entity_capabilities is deliberately NOT here: the
    builder does not compute it, so this file would be its first home, not its
    single source."""
    eid = derive_entity_id(cfg)
    mid = int(cfg["entity"]["entity_model_id"], 16)
    return (
        "# GENERATED by sw/builder/endstation_builder.py - DO NOT EDIT.\n"
        f"# Milan end-station IDENTITY for {cfg['board_target']}, from\n"
        f"# {cfg['source']} (the last-built config of this board OWNS this\n"
        "# file, exactly like configs/generated/sweep_opts_<board>.sh owns\n"
        "# its bitstream flags - one owner for 'what this board is').\n"
        "#\n"
        "# Sourced by /etc/init.d/S50milan, which programs entity_id into\n"
        "# 0x604/0x608 and entity_model_id into 0x60C/0x610. DO NOT restate\n"
        "# any of these values in a script: the fabric serves BOTH the ADPDU\n"
        "# and the AEM ENTITY descriptor's entity_model_id from those CSRs,\n"
        "# so a stale literal there advertises a model id that no longer\n"
        "# matches the descriptors the same build put in the ROM.\n"
        f"# Shape: {len(cfg['listeners'])} listener(s) + "
        f"{len(cfg['talkers'])} talker(s); model id from the "
        f"{cfg['model_id']['source']}.\n"
        "# Regenerate WITH the ROM it names:\n"
        "#   python3 sw/builder/endstation_builder.py --write-rtl <cfg.yaml>\n"
        f"MILAN_ENTITY_CONF_BOARD={cfg['board_target']}\n"
        f"MILAN_ENTITY_CONF_SOURCE={cfg['source']}\n"
        f"MILAN_ENTITY_ID_HI=0x{(eid >> 32) & 0xFFFFFFFF:08X}\n"
        f"MILAN_ENTITY_ID_LO=0x{eid & 0xFFFFFFFF:08X}\n"
        f"MILAN_MODEL_ID_HI=0x{(mid >> 32) & 0xFFFFFFFF:08X}\n"
        f"MILAN_MODEL_ID_LO=0x{mid & 0xFFFFFFFF:08X}\n"
        f"MILAN_N_TALKERS={len(cfg['talkers'])}\n"
        f"MILAN_N_LISTENERS={len(cfg['listeners'])}\n"
        f"MILAN_SR_VID={cfg['srp']['vid']}\n")


# ----------------------------------------------------------- aem_overlay ----
def emit_gptp_cfg(cfg):
    """The ptp4l half of the gptp: section - same values, one source.
    Only generated when the config STATES the section; the emitted file is
    the board's /etc/gptp.cfg replacement (S50milan prefers the per-board
    name when present). clock_accuracy / offset_scaled_log_variance have no
    ptp4l keys - they describe the local clock the daemon announces anyway
    (0xFE / 0xFFFF for a software-disciplined clock) and live only in the
    AVB_INTERFACE descriptor."""
    gp = cfg["gptp"]
    return (
        "# GENERATED by sw/builder/endstation_builder.py from "
        f"{cfg['source']} - DO NOT EDIT.\n"
        "# The gptp: section of that config is the ONE source for these\n"
        "# values AND the AVB_INTERFACE descriptor's clock fields, so the\n"
        "# entity cannot advertise a posture the daemon does not run.\n"
        "# Transport block per the proven bench profile (HW stamps, P2P,\n"
        "# L2, the 500 ms tx_timestamp_timeout DRAM-drain remedy).\n"
        "[global]\n"
        "gmCapable               1\n"
        "clientOnly              1\n"
        f"priority1               {gp['priority1']}\n"
        f"priority2               {gp['priority2']}\n"
        f"clockClass              {gp['clock_class']}\n"
        f"domainNumber            {gp['domain']}\n"
        "network_transport       L2\n"
        "delay_mechanism         P2P\n"
        "transportSpecific       0x1\n"
        "ptp_dst_mac             01:80:C2:00:00:0E\n"
        "follow_up_info          1\n"
        "neighborPropDelayThresh 2000\n"
        f"logAnnounceInterval     {gp['log_announce_interval']}\n"
        f"logSyncInterval         {gp['log_sync_interval']}\n"
        f"logMinPdelayReqInterval {gp['log_pdelay_interval']}\n"
        "tx_timestamp_timeout    500\n"
        "# per-board wire-reference correction (S50milan seds the value)\n"
        "ingressLatency          0\n")


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
    # map_mode dynamic ports (gaps item 8) emit NO map. GET_AUDIO_MAP reads
    # their root store; ADD/REMOVE are not implemented (Milan 5.4.2.26-28).
    #
    # Under the legacy policies the port's cluster block IS the stream's
    # channel space, so the map is the identity over the whole block. Under
    # D8 role-pools it is not: the pool is a SELECTION SET (physical + host +
    # pilot + loopback) and only ONE segment can be the power-on source, so
    # the map carries min(stream channels, primary segment width) rows at the
    # primary segment's port-relative offset. Both forms satisfy the 7.2.19
    # uniqueness rules (input: <=1 entry per cluster channel; output: <=1
    # entry per stream channel).
    def rows(p, direction, channels):
        if cfg["interface"]["cluster_policy"] != "role-pools":
            return [[p["stream_index"], ch, ch, 0]
                    for ch in range(p["clusters"])]
        g = primary_segment(p, direction)
        n = min(channels, g["width"])
        return [[p["stream_index"], ch, g["offset"] + ch, 0]
                for ch in range(n)]

    audio_maps = []
    for p in P_in:
        if p.get("map_mode", "static") == "dynamic":
            continue
        audio_maps.append(dict(
            index=p["base_map"], direction="input", port_index=p["index"],
            primary_role=primary_segment(p, "input")["role"],
            mappings=rows(p, "input", L[p["stream_index"]]["channels"])))
    for p in P_out:
        if p.get("map_mode", "static") == "dynamic":
            continue                    # USER 08-01: dynamic talker port
        audio_maps.append(dict(
            index=p["base_map"], direction="output", port_index=p["index"],
            primary_role=primary_segment(p, "output")["role"],
            mappings=rows(p, "output", T[p["stream_index"]]["channels"])))
    audio_maps.sort(key=lambda m: m["index"])

    # D10: every AUDIO_CLUSTER carries its ROLE and the object_name that role
    # implies, in global descriptor-index order (all input clusters first).
    audio_clusters = []
    for direction, ports in (("input", P_in), ("output", P_out)):
        for p in ports:
            names = cluster_names(cfg, p, direction)
            for g in p["pool"]:
                for n in range(g["width"]):
                    off = g["offset"] + n
                    audio_clusters.append(dict(
                        index=p["base_cluster"] + off, name=names[off],
                        direction=direction, role=g["role"],
                        port_index=p["index"], offset=off))

    # overlay port entries: map_mode/map_page keys appear ONLY on dynamic
    # ports so every static config's overlay stays byte-identical
    def port_public(p, direction):
        q = {k: p[k] for k in ("index", "stream_index", "clusters",
                               "base_cluster", "maps", "base_map")}
        if p.get("map_mode", "static") == "dynamic":
            q["map_mode"] = "dynamic"
            if p.get("map_page"):
                q["map_page"] = p["map_page"]
        # the port's role pool (D8), port-relative like 7.2.19 offsets
        q["pool"] = [{"role": g["role"], "offset": g["offset"],
                      "width": g["width"]} for g in p["pool"]]
        q["primary_role"] = primary_segment(p, direction)["role"]
        return q
    P_in_pub = [port_public(p, "input") for p in P_in]
    P_out_pub = [port_public(p, "output") for p in P_out]

    return {
        "_schema": OVERLAY_SCHEMA_ID,
        "_schema_version": OVERLAY_SCHEMA_VERSION,
        "_generated_by": "sw/builder/endstation_builder.py",
        "_source_config": cfg["source"],
        "entity": cfg["entity"],
        "model_id": cfg["model_id"],
        #! CONSTRAINT (1722.1-2021 Table 7-2): the ENTITY descriptor's
        #! entity_id, entity_capabilities, talker_stream_sources,
        #! talker_capabilities, listener_stream_sinks and
        #! listener_capabilities each "is the same as the ... field in ATDECC
        #! Discovery Protocol", and 7.2.8 binds AVB_INTERFACE's mac_address
        #! the same way.  gen_aem_store zero-fills those spans - the deleted
        #! KL_aecp_aem_dyn_mux substituted them from the CSR group at read
        #! time - and the descriptor store that replaced it has no identity
        #! input, so avdecc/gen_aemi_image.py has to bake them into the image.
        #! It can only bake what the overlay states, and until 2026-08-14 the
        #! overlay stated neither the station MAC nor the resolved entity_id:
        #! the image shipped entity_capabilities = 0, AEM_SUPPORTED clear.
        #! entity_model_id is NOT restated here - it is already above, and a
        #! second copy is a second thing to go stale.
        "adp": overlay_adp_block(cfg),
        **({"gptp": cfg["gptp"]} if cfg.get("gptp") is not None else {}),
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
        "audio_clusters": audio_clusters,
        "cluster_format": "MBLA-mono",
        "cluster_policy": cfg["interface"]["cluster_policy"],
        "cluster_pools": cfg["interface"]["cluster_pools"],
        # task #65: which pool sources the BITSTREAM behind this model
        # elaborates. gen_aem_store reads it to decide whether a cluster's
        # capture-crossbar template is a real source or an advertisement, so
        # the power-on dynamic map cannot name a lane that was not built.
        "cluster_fabric": cfg["interface"]["cluster_fabric"],
        "physical_binding": {
            "interface": cfg["interface"]["kind"],
            "channels_per_direction": cfg["interface"]["channels"],
            "physical_channels": cfg["interface"]["physical_channels"],
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


#: What re-measurement a prune invalidates. Rule 4 of AREA_BUDGET.md: a
#: parameter that removes logic must say which recorded number stops being
#: about the bitstream you are building. Printed in the build plan so the
#: obligation travels with the config, not with the reviewer's memory.
FEATURE_REMEASURE = {
    "media_clock_servo":
        "every CRF / input-stream media-clock lock result: with no actuator "
        "the audio MMCM free-runs, so servo convergence, MCSRV_STAT states "
        "and any recovered-clock jitter figure are not reproducible",
    "latency_taps":
        "ALL of docs/AAF_LATENCY_TAPS.md - the CAP-SOF, SOF-EOF and EOF-MAC "
        "silicon numbers were read out of this block and cannot be re-read "
        "from a build that does not contain it",
    "maap":
        "MAAP claim/defend behaviour: conflict and defence counts, and any "
        "address-collision result that depended on the engine answering",
    "i2s_playback":
        "every analog measurement taken at the line out (loop THD+N, the "
        "pilot-tone census) and the I2SPB underrun/overrun census",
    "rx_mac_filter":
        "the RX drop census and any statement about what the port refuses; "
        "the port is PROMISCUOUS in the pruned build",
    "render_lpf":
        "the analog loop THD+N record, which was measured THROUGH this "
        "filter (docs/design/AREA_BUDGET.md)",
    "datapath_probes":
        "the APRB pre-match view (parsed/matched/last-sid) and PBK chain "
        "evidence - the 0x8B4-0x8D0 words read 0, so bench recipes that "
        "read them see the LTAP-style absent-block zero, not a measurement",
}


def emit_features_line(cfg):
    """The '## Optional blocks' section of the build plan. ALWAYS emitted, so
    a reader of any plan can see which optional blocks this bitstream does and
    does not contain - the point of the whole exercise is that an absent block
    is never silent."""
    ln = ["## Optional blocks (docs/design/AREA_BUDGET.md tier 1)", ""]
    pruned = [k for k in OPTIONAL_BLOCKS if not cfg["features"][k]]
    if not pruned:
        ln.append("- ALL PRESENT (the default). This gateware contains every "
                  "tier-1 optional block; no `--no-*` flag is emitted and the "
                  "generated top is the shipping shape.")
        return "\n".join(ln)
    ln.append("| Block | Flag | milan_datapath | RE-MEASURE |")
    ln.append("|-------|------|----------------|------------|")
    for k in pruned:
        flag, param, _why = OPTIONAL_BLOCKS[k]
        ln.append(f"| `{k}` | `{flag}` | `{param}=0` | "
                  f"{FEATURE_REMEASURE[k]} |")
    present = [k for k in OPTIONAL_BLOCKS if cfg["features"][k]]
    ln.append("")
    ln.append(f"- PRESENT: {', '.join(f'`{k}`' for k in present) or '(none)'}")
    ln.append("- Every figure attached to a pruned block in the resource "
              "estimate is a **yosys estimate**, not a placement result.")
    return "\n".join(ln)


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
    # fw carries the raw register beside it on purpose: this is the line a
    # bench engineer reads with Hive open and `devmem 0x90000004` in the other
    # terminal, and mapping 1.22 onto 0x0001_0016 by eye IS the item-00 check.
    _fwmaj, _fwmin = rtl_version()
    a(f"- name: {e['name']}  (serial {e['serial_number']}, "
      f"fw {e['firmware_version']} = milan_csr VERSION "
      f"0x{_fwmaj:04X}_{_fwmin:04X} . rev {e['firmware_rev']})")
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
    a(emit_features_line(cfg))
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
    a("| Port | Stream | Clusters | base_cluster | AUDIO_MAP index | Cluster pool (D8 roles) | Map source |")
    a("|------|--------|----------|--------------|-----------------|-------------------------|------------|")

    def _pool(p, direction):
        return (" + ".join(f"{g['role']} x{g['width']}" for g in p["pool"]),
                primary_segment(p, direction)["role"])
    for p in cfg["ports_in"]:
        pool, prim = _pool(p, "input")
        a(f"| STREAM_PORT_INPUT {p['index']} | STREAM_INPUT {p['stream_index']}"
          f" | {p['clusters']} | {p['base_cluster']} | {p['base_map']} "
          f"| {pool} | {prim} |")
    for p in cfg["ports_out"]:
        pool, prim = _pool(p, "output")
        a(f"| STREAM_PORT_OUTPUT {p['index']} | STREAM_OUTPUT {p['stream_index']}"
          f" | {p['clusters']} | {p['base_cluster']} | {p['base_map']} "
          f"| {pool} | {prim} |")
    a("")
    ph = i["physical_channels"]
    a(f"Physical audio channels the BOARD routes: {ph['capture']} capture / "
      f"{ph['render']} render (`audio_interface.physical_channels`; default = "
      f"the {i['channels']}-channel `{i['kind']}` interface width). Clusters "
      "past that are non-physical by construction and are named for what they "
      "ARE - `Virtual`, `Host`, `Pilot Tone`, `Loopback S<s> ch <c>` - so a "
      "controller operator can tell a live source from a dead slot.")
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
def write_rtl_entity(cfg, adp_svh, paths):
    """Write the ENTITY-DEFINITION artifact into the tracked RTL tree.

    Called ONLY by `--write-rtl`, for the config you are about to build - see
    the note at the call site for why this is not automatic.

    ONE FILE, not two.  This used to write the AEM descriptor ROM beside the
    shape include, on the reasoning that both describe the same entity and
    shipping one without the other is what let an 8x8 gateware carry a 1x1
    descriptor set (docs/findings/ADP_SHAPE_STATIC_0727.md).  The ROM's
    destination - hdl/ieee17221/aecp/gen/ - is DELETED with the AECP plane,
    and writing a file into a directory that a deleted module used to compile
    would just recreate the directory and mislead the next reader.  The shape
    include survives and is MORE load-bearing than before: milan_datapath.sv
    now sizes the protocol processor's source/sink arrays from it."""
    adp_gen = os.path.join(ROOT, ADP_SHAPE_REL)
    os.makedirs(os.path.dirname(adp_gen), exist_ok=True)
    with open(adp_gen, "w") as f:
        f.write(adp_svh)
    paths["rtl_adp_shape_svh"] = adp_gen


def build(config_path, outdir=None, write_rtl=False, write_fragment=None):
    """Run the full pipeline for one config. Returns dict with the emitted
    paths + in-memory artifacts (for tests)."""
    cfg = load_config(config_path)
    argv = emit_soc_argv(cfg)
    overlay = emit_aem_overlay(cfg)
    lwsrp = emit_lwsrp_table(cfg)
    lwsrp_svh = emit_lwsrp_svh(cfg, lwsrp)
    csr_svh = emit_csr_defaults_svh(cfg)
    adp_svh = emit_adp_shape_svh(cfg, overlay)
    # The ROM consumer does not yet express every overlay the builder can
    # emit (a shape with no CRF sink has no AEM_CRF_FMTS_C table). That is a
    # real limit, not a reason to fail every OTHER artifact: record it and
    # let --write-rtl below be the thing that refuses, because a shape whose
    # descriptor set cannot be generated is a shape whose declarative entity
    # definition is incomplete - and the ADP counts and capability words that
    # DO reach silicon are derived from that same definition.
    try:
        aem_rom = emit_aem_rom_svh(cfg, overlay)
        aem_rom_why = None
    except (ValueError, KeyError) as e:
        aem_rom, aem_rom_why = None, str(e)
    iparams = emit_interface_params(cfg)
    shape = emit_platform_shape(cfg)
    dtsi = emit_dt_overlay(cfg)
    marks = rtl_capability_marks(cfg)
    est = estimate_resources(cfg, overlay)
    plan = emit_build_plan(cfg, argv, overlay, marks, est, lwsrp, shape)
    sweep = emit_sweep_opts(cfg)
    entity_conf = emit_entity_conf(cfg)

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
    p_adp_svh = os.path.join(d, "adp_shape_defaults.svh")
    with open(p_adp_svh, "w") as f:
        f.write(adp_svh)
    p_aem_rom = os.path.join(d, AEM_ROM_OUT_NAME)
    if aem_rom is not None:
        with open(p_aem_rom, "w") as f:
            f.write(aem_rom)
    p_shape = os.path.join(d, "platform_shape.json")
    with open(p_shape, "w") as f:
        json.dump(shape, f, indent=1)
        f.write("\n")
    p_dtsi = os.path.join(d, "milan-nic.dtsi")
    with open(p_dtsi, "w") as f:
        f.write(dtsi)
    # Sweep fragment: written ONLY under --write-rtl, the same "this config
    # owns the tree now" declaration that writes the tracked svh. It used to
    # be written by EVERY build() - defensible while the content was
    # board-constraints-only, but since the fragment carries the FULL design
    # flags (2026-07-28) that meant last-build-wins: test_builder's twenty
    # arty_current throwaway builds silently reverted the arty fragment from
    # the 4x4's tdm8-master flags to the 1x1's, and the next `sweep.sh arty`
    # would have built the wrong shape with a fragment that looked generated
    # and current. One flag, one owner, one moment of transfer.
    gen_dir = os.path.join(ROOT, "configs/generated")
    p_sweep = os.path.join(gen_dir, f"sweep_opts_{cfg['board_target']}.sh")
    # write_fragment defaults to write_rtl but is separable on purpose: the
    # fragment is PER-BOARD (sweep_opts_arty.sh vs sweep_opts_ax7101.sh, no
    # collision), the tracked svh is PER-TREE (one owner). Updating board A's
    # fragment while board B owns the tree needs --write-fragment alone.
    if write_fragment is None:
        write_fragment = write_rtl
    if write_fragment:
        os.makedirs(gen_dir, exist_ok=True)
        with open(p_sweep, "w") as f:
            f.write(sweep)
    # ...and the board-software half of the SAME transfer: the identity the
    # flashed image programs into the ADP/AEM CSRs. It ships in the buildroot
    # rootfs overlay (sibling repo), so it moves with `--write-fragment` /
    # `--write-rtl` and never on a throwaway variant build. Same moment as the
    # bitstream flags on purpose - a shape change that regenerates the AEM ROM
    # regenerates the model id that names it, or neither.
    p_ent = os.path.join(d, ENTITY_CONF_NAME)
    with open(p_ent, "w") as f:
        f.write(entity_conf)
    if cfg.get("gptp") is not None:
        gptp_cfg = emit_gptp_cfg(cfg)
        with open(os.path.join(d, "gptp.cfg"), "w") as f:
            f.write(gptp_cfg)
    p_ent_overlay = entity_conf_overlay_path(cfg["board_target"])
    if write_fragment:
        if p_ent_overlay:
            with open(p_ent_overlay, "w") as f:
                f.write(entity_conf)
            if cfg.get("gptp") is not None:
                p_gp = os.path.join(os.path.dirname(p_ent_overlay),
                                    f"gptp.{cfg['board_target']}.cfg")
                with open(p_gp, "w") as f:
                    f.write(gptp_cfg)
                print(f"  wrote {p_gp}")
            # THE DESCRIPTOR IMAGE, into the same rootfs the identity ships in.
            # /etc/init.d/S50milan loads it into the reserved `ppmem` window
            # before enabling ADP, because the processor serves READ_DESCRIPTOR
            # from DRAM and has nothing on-die. The manifest beside it carries
            # the base, so the loader never restates an address.
            #
            # Written HERE, not by the SoC build, because this is where the
            # window is decided (`pp_mem_phys`) and where the identity the
            # descriptors belong to is written - the id and the descriptors it
            # names must not be able to move apart, which is the same reason
            # milan-entity.<board>.conf is generated rather than hand-kept.
            for path, blob in _entity_model_image(cfg, overlay).items():
                p_img = os.path.join(os.path.dirname(p_ent_overlay),
                                     "milan-aem", path)
                os.makedirs(os.path.dirname(p_img), exist_ok=True)
                mode = "wb" if isinstance(blob, bytes) else "w"
                with open(p_img, mode) as f:
                    f.write(blob)
                if p_img.endswith(".sh"):
                    os.chmod(p_img, 0o755)
                print(f"  wrote {p_img}")
        else:
            print(f"[endstation_builder] WARNING: rootfs overlay etc/ not on "
                  f"disk ({ROOTFS_OVERLAY_ETC}) - the flashed image's "
                  f"identity was NOT refreshed; re-run where milan-tests-avb "
                  f"is checked out, or set MILAN_ROOTFS_OVERLAY_ETC",
                  file=sys.stderr)
    # per-CONFIG (not per-board) shape include: an include dir whose `gen/`
    # holds this config's entity definition, so a harness or a build selects
    # a shape by pointing +incdir at it. The 1x1 copy is byte-identical to
    # the tracked hdl/ one (check_entity_shape.py compares them).
    #
    # ONLY for configs that live in configs/. test_builder alone runs build()
    # on ~20 throwaway variants in temp directories, and each one leaving a
    # configs/generated/tmpXXXX/ behind is untracked litter that a reader has
    # to guess at. A variant still gets its copy under outdir/<name>/.
    p_cfg_adp = os.path.join(d, "gen", "adp_shape_defaults.svh")
    if os.path.normpath(cfg["source"]).startswith("configs" + os.sep):
        p_cfg_adp = os.path.join(gen_dir, cfg["name"], "gen",
                                 "adp_shape_defaults.svh")
    os.makedirs(os.path.dirname(p_cfg_adp), exist_ok=True)
    with open(p_cfg_adp, "w") as f:
        f.write(adp_svh)
    # NO DESCRIPTOR SET BESIDE IT ANY MORE (2026-08-12). This directory used
    # to get gen/aecp_aem_rom.svh too, because KL_aecp_aem_store `include-d it
    # out of the SAME `gen/` a harness pointed +incdir at, and shipping the
    # shape without the descriptors is how a 1x1 harness came to ask for
    # descriptors that only exist in the 8x8 model. That module is deleted:
    # a `gen/` dir now holds exactly what an elaboration still reads - the
    # shape - and the ROM stays a readable artifact under out/<cfg>/ where no
    # +incdir can accidentally pick it up.
    paths = dict(soc_params=p_soc, aem_overlay=p_ovl, build_plan=p_plan,
                 lwsrp_table=p_srp, lwsrp_svh=p_srp_svh,
                 csr_defaults_svh=p_csr_svh, adp_shape_svh=p_adp_svh,
                 cfg_adp_shape_svh=p_cfg_adp,
                 platform_shape=p_shape, dt_overlay=p_dtsi,
                 sweep_opts=p_sweep, entity_conf=p_ent)
    # only when it was actually written: the reader of this dict prints
    # "wrote <path>", and the flashed image's identity is not a place to be
    # imprecise about whether a file moved
    if write_fragment and p_ent_overlay:
        paths["rootfs_entity_conf"] = p_ent_overlay
    # The TRACKED RTL header: exactly one config (the DEPLOYED shape, marked
    # srp.rtl_table) owns hdl/common/csr/gen/lwsrp_csr_defaults.svh, the
    # subset milan_csr.sv COMPILES, so a config edit re-elaborates the CSR
    # block instead of drifting away from it (test_builder 18a/20a).
    # ITS SIBLING IS GONE: hdl/ieee8021q/srp/gen/lwsrp_table.svh was the full
    # contract for the srp tree, and that whole tree is deleted. The full
    # table is still emitted to out/<cfg>/lwsrp_table.svh for reading; it is
    # not written into a directory nothing compiles.
    # The ENTITY DEFINITION is written ONLY on an explicit --write-rtl, never
    # as a side effect of building a config: test_builder alone runs build()
    # on a dozen throwaway config variants, and any one of them silently
    # rewriting the shape include would put a shape in the tree that nobody
    # chose. The gate reads the `Source:` header, so "which shape is in the
    # tree" is always answerable.
    if write_rtl:
        if aem_rom is None:
            raise ConfigError(
                f"--write-rtl: this shape's AEM descriptor ROM cannot be "
                f"generated, so its entity definition is incomplete and the "
                f"ADP counts derived from it cannot be trusted - {aem_rom_why}")
        write_rtl_entity(cfg, adp_svh, paths)
    if cfg["srp"]["rtl_table"]:
        csr_gen = os.path.join(ROOT, CSR_DEFAULTS_REL)
        os.makedirs(os.path.dirname(csr_gen), exist_ok=True)
        with open(csr_gen, "w") as f:
            f.write(csr_svh)
        paths["rtl_csr_defaults_svh"] = csr_gen
    if aem_rom is not None:
        paths["aem_rom_svh"] = p_aem_rom
    return dict(cfg=cfg, argv=argv, overlay=overlay, marks=marks, plan=plan,
                resource_estimate=est, sweep_opts=sweep, lwsrp=lwsrp,
                lwsrp_svh=lwsrp_svh, csr_defaults_svh=csr_svh,
                adp_shape_svh=adp_svh, aem_rom_svh=aem_rom,
                aem_rom_unsupported=aem_rom_why, entity_conf=entity_conf,
                interface_params=iparams,
                platform=shape, dt_overlay=dtsi, paths=paths)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("config", help="end-station YAML config")
    ap.add_argument("-o", "--outdir", default=None,
                    help="output root (default sw/builder/out/)")
    ap.add_argument("--write-fragment", action="store_true",
                    help="write configs/generated/sweep_opts_<board>.sh "
                         "WITHOUT taking tracked-svh ownership (fragments "
                         "are per-board files; the svh is per-tree)")
    ap.add_argument("--write-rtl", action="store_true",
                    help="also write THIS config's advertised shape into the "
                         "tracked RTL tree (hdl/common/csr/gen/"
                         "adp_shape_defaults.svh - ONE file: the AEM "
                         "descriptor ROM no longer has an RTL destination, "
                         "the repository-local AECP plane that compiled it "
                         "is deleted). Run "
                         "this for the config you are about to build: "
                         "milan_csr.sv and milan_datapath.sv `include that "
                         "file, so without it a build inherits whatever shape "
                         "was last committed")
    args = ap.parse_args()
    try:
        r = build(args.config, args.outdir, write_rtl=args.write_rtl,
                  write_fragment=(True if args.write_fragment else None))
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
        # the rootfs identity conf lives in the sibling repo: show it whole
        # rather than as a ../../.. relpath nobody can paste
        rel = os.path.relpath(p, ROOT)
        print(f"  wrote {p if rel.startswith(os.pardir) else rel}")


if __name__ == "__main__":
    main()

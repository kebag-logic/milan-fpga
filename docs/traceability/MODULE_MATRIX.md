<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# Module ↔ spec ↔ test traceability matrix

**GENERATED — do not hand-edit.** `python3 docs/traceability/gen_module_matrix.py`
(regenerate on any RTL/TB tree change; `--check` gates staleness **and the untested-count ratchet** in CI).

Every module in `hdl/` mapped to its spec family, the clause(s) it
appears against in the clause matrices, and the testbench(es) that
compile it. A module with no testbench is an **⚪ UNTESTED** row —
that is the coverage gap this matrix exists to make visible.

The count of ⚪ rows is ratcheted by [`untested.budget`](untested.budget): a normal run only ever lowers
it, and `--check` fails when the live count exceeds it — so a new
module without a testbench breaks the gate instead of quietly
growing the backlog. The one escape is a 🗄️ **ARCHIVED** banner
marker in the module's own file, which states *why* no open-flow
test is possible and is reproduced verbatim below.

Legend: ✅ dedicated Verilator TB · ➰ exercised transitively in a broader TB's design · 🔬 in the tsn_fuzz field campaign · 📦 package · 🗄️ archived by a stated decision · ⚪ not compiled by any TB.

**Totals:** 64 modules · 63 with a dedicated TB · 0 exercised-only · 30 field-fuzzed · 0 archived · **0 not in any TB**

## Coverage by spec family

*Which family is thinnest on dedicated testbenches?* — the ordering the tables below cannot show. Weakest first.

```mermaid
xychart-beta
    title "Modules per spec family: dedicated testbenches vs total"
    x-axis ["ieee1722", "ieee17221", "milan", "ieee8021as", "ieee8021q", "common"]
    y-axis "modules" 0 --> 36
    bar [35, 1, 3, 7, 8, 10]
    bar [34, 1, 3, 7, 8, 10]
```

The solid bar is the modules carrying a dedicated Verilator testbench; the pale sliver above it is the shortfall against the family total. Exact numbers, including the archived and fuzzed columns the chart cannot show:

| family | modules | ✅ dedicated TB | ➰ exercised only | 🔬 field-fuzzed | 🗄️ archived | ⚪ untested |
|---|---|---|---|---|---|---|
| IEEE 1722 (AVTP) | 35 | 34 | 0 | 29 | 0 | 0 |
| IEEE 1722.1 (ATDECC) | 1 | 1 | 0 | 0 | 0 | 0 |
| Milan integration | 3 | 3 | 0 | 0 | 0 | 0 |
| IEEE 802.1AS | 7 | 7 | 0 | 0 | 0 | 0 |
| IEEE 802.1Q | 8 | 8 | 0 | 0 | 0 | 0 |
| Common / integration | 10 | 10 | 0 | 0 | 0 | 0 |

## IEEE 1722.1 (ATDECC)

_TX arbitration only - the ADP / ACMP / AECP engines are the protocol-processor submodule's_

| module | file | test | clauses |
|---|---|---|---|
| ✅ `adp_tx_arbiter` | `ieee17221/adp/adp_tx_arbiter.sv` | `adp_tx` · `milan_dp` | — |

## IEEE 1722 (AVTP)

_AAF / CRF / MAAP / AVTP common_

| module | file | test | clauses |
|---|---|---|---|
| ✅ `KL_aaf_capture_i2s` | `ieee1722/aaf/KL_aaf_capture_i2s.sv` | `aaf` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_aaf_latency_tap_bank` | `ieee1722/aaf/KL_aaf_latency_tap_bank.sv` | `aaf_latency_tap_bank` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_aaf_latency_chain` | `ieee1722/aaf/KL_aaf_latency_taps.sv` | `aaf_latency_tap_bank` · `aaf_latency_taps` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_aaf_packetizer` | `ieee1722/aaf/KL_aaf_packetizer.sv` | `aaf` · `aaf_audio_loop` · `chmap_capture` · `milan_dp` · `tdm` · 🔬`make aaf` | 35.2.2.8.4, 802.3 |
| ✅ `KL_aaf_rx_depacketizer` | `ieee1722/aaf/KL_aaf_rx_depacketizer.sv` | `aaf_audio_loop` · `avtp_rxmon` · `milan_dp` · `tsn_fuzz` · 🔬`make aaf` | — |
| ✅ `KL_aes3_rx` | `ieee1722/aaf/KL_aes3_rx.sv` | `aes3` · 🔬`make aaf` | — |
| ✅ `KL_aes3_tx` | `ieee1722/aaf/KL_aes3_tx.sv` | `aes3` · 🔬`make aaf` | — |
| ✅ `KL_chan_map_capture` | `ieee1722/aaf/KL_chan_map_capture.sv` | `chmap_capture` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_chan_map_render` | `ieee1722/aaf/KL_chan_map_render.sv` | `chmap_render` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_i2s_feed_mux` | `ieee1722/aaf/KL_i2s_feed_mux.sv` | `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_i2s_playback` | `ieee1722/aaf/KL_i2s_playback.sv` | `i2spb` · `milan_dp` · `mmcm_servo` · 🔬`make aaf` | — |
| ✅ `KL_lat_history_ring` | `ieee1722/aaf/KL_lat_history_ring.sv` | `lat_history_ring` · 🔬`make aaf` | — |
| ✅ `KL_media_adv` | `ieee1722/aaf/KL_media_adv.sv` | `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_pair_blend` | `ieee1722/aaf/KL_pair_blend.sv` | `milan_dp` · `pair_fill` · 🔬`make aaf` | — |
| ✅ `KL_pair_zero_fill` | `ieee1722/aaf/KL_pair_zero_fill.sv` | `milan_dp` · `pair_fill` · 🔬`make aaf` | — |
| ✅ `KL_pcm_lpf` | `ieee1722/aaf/KL_pcm_lpf.sv` | `milan_dp` · `pcmlpf` · 🔬`make aaf` | — |
| ✅ `KL_pcm_route` | `ieee1722/aaf/KL_pcm_route.sv` | `avtp_rxmon` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_tdm_capture` | `ieee1722/aaf/KL_tdm_capture.sv` | `milan_dp` · `tdm` · 🔬`make aaf` | — |
| ✅ `KL_tdm_capture_master` | `ieee1722/aaf/KL_tdm_capture_master.sv` | `milan_dp` · `tdm` · 🔬`make aaf` | — |
| ✅ `KL_tdm_render` | `ieee1722/aaf/KL_tdm_render.sv` | `milan_dp` · `tdm_render` · 🔬`make aaf` | — |
| ✅ `KL_tone_gen` | `ieee1722/aaf/KL_tone_gen.sv` | `chmap_capture` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `aaf_talker_i2s` | `ieee1722/aaf/aaf_talker_i2s.sv` | `aaf` · `milan_dp` · 🔬`make aaf` | — |
| 🔬 `KL_avtp_common_parser` | `ieee1722/avtp/KL_avtp_common_parser.sv` | 🔬`make aaf` | — |
| ✅ `KL_avtp_rx_monitor` | `ieee1722/avtp/KL_avtp_rx_monitor.sv` | `aaf_audio_loop` · `avtp_rxmon` · `milan_dp` · `tsn_fuzz` · 🔬`make aaf` | — |
| ✅ `KL_avtp_rx_monitor_ctx` | `ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv` | `avtp_rxmon` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_media_clock_restart` | `ieee1722/avtp/KL_media_clock_restart.sv` | `milan_dp` · `tkdiag` · 🔬`make aaf` | — |
| ✅ `KL_stream_table` | `ieee1722/avtp/KL_stream_table.sv` | `avtp_parser` · `avtp_rxmon` · `avtp_stream` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_talker_diag_ctx` | `ieee1722/avtp/KL_talker_diag_ctx.sv` | `milan_dp` · `tkdiag` · 🔬`make aaf` | — |
| ✅ `avtp_stream_parser` | `ieee1722/avtp/avtp_stream_parser.sv` | `aaf_audio_loop` · `avtp_parser` · `avtp_rxmon` · `avtp_stream` · `milan_dp` · `tsn_fuzz` · 🔬`make aaf` | — |
| 📦 `avtp_subtype_pkg` | `ieee1722/avtp/avtp_subtype_pkg.sv` | 🔬`make aaf` | — |
| ✅ `KL_crf_rx` | `ieee1722/crf/KL_crf_rx.sv` | `crf_rx` · `milan_dp` | — |
| ✅ `KL_crf_tx` | `ieee1722/crf/KL_crf_tx.sv` | `crf_tx` · `milan_dp` | — |
| ✅ `KL_media_grid_align` | `ieee1722/crf/KL_media_grid_align.sv` | `media_grid_align` · `milan_dp` | — |
| ✅ `KL_media_nco` | `ieee1722/crf/KL_media_nco.sv` | `media_grid_align` · `media_nco` · `milan_dp` | — |
| ✅ `KL_mmcm_drp_servo` | `ieee1722/crf/KL_mmcm_drp_servo.sv` | `milan_dp` · `mmcm_servo` · `mmcm_servo_autorepair` | — |
| ✅ `KL_maap` | `ieee1722/maap/KL_maap.sv` | `maap` · `milan_dp` | — |

## IEEE 802.1Q

_TS/CBS shaping · VLAN/TCAM filtering (SRP/MRP is the protocol-processor submodule's)_

| module | file | test | clauses |
|---|---|---|---|
| ✅ `rx_mac_filter` | `ieee8021q/filtering/rx_mac_filter.sv` | `milan_dp` · `rx_filter` · `tcam_csr` | — |
| ✅ `tcam` | `ieee8021q/filtering/tcam.sv` | `milan_dp` · `rx_filter` · `tcam` · `tcam_csr` | — |
| ✅ `credit_based_shaper` | `ieee8021q/ts/credit_based_shaper.sv` | `cbs` · `controller_rate` · `datapath` · `shaper_core` | — |
| ✅ `traffic_class_map` | `ieee8021q/ts/traffic_class_map.sv` | `classifier` · `cls` · `controller_rate` · `datapath` | — |
| ✅ `traffic_classifier` | `ieee8021q/ts/traffic_classifier.sv` | `classifier` · `controller_rate` · `datapath` | — |
| ✅ `traffic_controller_802_1q` | `ieee8021q/ts/traffic_controller_802_1q.sv` | `controller_rate` · `datapath` | — |
| ✅ `traffic_queues` | `ieee8021q/ts/traffic_queues.sv` | `controller_rate` · `datapath` · `queues` | — |
| ✅ `traffic_shaping_core` | `ieee8021q/ts/traffic_shaping_core.sv` | `controller_rate` · `datapath` · `shaper_core` | — |

## IEEE 802.1AS

_gPTP timestamping / pdelay / sync_

| module | file | test | clauses |
|---|---|---|---|
| ✅ `KL_gptp_shadow` | `ieee8021as/gptp_plane/KL_gptp_shadow.sv` | `gptp_shadow` · `milan_dp` · `tsn_fuzz` | 8.4.3 |
| ✅ `KL_gptp_txstamp` | `ieee8021as/gptp_plane/KL_gptp_txstamp.sv` | `gptp_shadow` · `milan_dp` · `tsn_fuzz` | 8.4.3 |
| ✅ `KL_ptp_clock_validity` | `ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv` | `clkvalid` · `gptp_shadow` · `milan_dp` · `tsn_fuzz` | — |
| ✅ `ptp_csr_sync` | `ieee8021as/ptp_timestamp/ptp_csr_sync.sv` | `milan_dp` · `ptp_sync` · `ptp_ts` | — |
| ✅ `ptp_ts_core` | `ieee8021as/ptp_timestamp/ptp_ts_core.sv` | `ptp_ts` | — |
| ✅ `ptp_ts_top` | `ieee8021as/ptp_timestamp/ptp_ts_top.sv` | `ptp_ts` | — |
| ✅ `timestamp_counter` | `ieee8021as/ptp_timestamp/timestamp_counter.sv` | `gptp_plane` · `gptp_shadow` · `milan_dp` · `ptp` · `ptp_ts` · `tsn_fuzz` | 8.2 |

## Common / integration

_CSR, CDC, RMON, utilities_

| module | file | test | clauses |
|---|---|---|---|
| ✅ `KL_link_guard` | `common/KL_link_guard.sv` | `link_guard` · `milan_dp` | — |
| ✅ `axis_mux_rr_2in_1out` | `common/axis_mux_rr_2in_1out.sv` | `ptp_ts` | — |
| ✅ `cdc_handshake` | `common/cdc_handshake.sv` | `cdc` · `milan_dp` · `mmcm_servo` · `mmcm_servo_autorepair` · `ptp_ts` | — |
| ✅ `cdc_pair_fifo` | `common/cdc_pair_fifo.sv` | `aaf` · `aes3` · `i2spb` · `milan_dp` · `mmcm_servo` · `tdm` · `tdm_render` | — |
| ✅ `cdc_pulse` | `common/cdc_pulse.sv` | `aes3` · `cdc` · `crf_tx` · `i2spb` · `mac_rmon` · `milan_dp` · `mmcm_servo` · `mmcm_servo_autorepair` · `ptp_ts` | — |
| 📦 `ethernet_packet_pkg` | `common/ethernet_packet_pkg.sv` | — | — |
| ✅ `tx_ifg_gasket` | `common/tx_ifg_gasket.sv` | `ifg` · `milan_dp` | — |
| ✅ `milan_csr` | `common/csr/milan_csr.sv` | `csr` · `milan_dp` | — |
| ✅ `KL_mac_rmon_events` | `common/eth_event_counter/KL_mac_rmon_events.sv` | `mac_rmon` | — |
| ✅ `ethernet_events` | `common/eth_event_counter/ethernet_events.sv` | `milan_dp` | — |
| ✅ `event_counter` | `common/eth_event_counter/event_counter.sv` | `milan_dp` | — |

## Milan integration

_datapath + top wrappers_

| module | file | test | clauses |
|---|---|---|---|
| ✅ `KL_pp_maap_shim` | `milan/KL_pp_maap_shim.sv` | `milan_dp` | — |
| ✅ `KL_pp_shadow` | `milan/KL_pp_shadow.sv` | `milan_dp` | 34.3, 34.4 |
| ✅ `milan_datapath` | `milan/milan_datapath.sv` | `milan_dp` | 34.4, 35.2.2.8.4, 35.2.7, 802.1 |


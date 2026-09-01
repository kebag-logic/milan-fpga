<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# `ieee1722/avtp` — modules & test coverage

**GENERATED** by `docs/traceability/gen_module_matrix.py` — do not
hand-edit. Part of the IEEE 1722 (AVTP) family; rolled up in
[`docs/traceability/MODULE_MATRIX.md`](../../../docs/traceability/MODULE_MATRIX.md).

| module | file | test | clauses |
|---|---|---|---|
| 🔬 `KL_avtp_common_parser` | `KL_avtp_common_parser.sv` | 🔬`make aaf` | — |
| ✅ `KL_avtp_rx_monitor` | `KL_avtp_rx_monitor.sv` | `aaf_audio_loop` · `avtp_rxmon` · `milan_dp` · `tsn_fuzz` · 🔬`make aaf` | — |
| ✅ `KL_avtp_rx_monitor_ctx` | `KL_avtp_rx_monitor_ctx.sv` | `avtp_rxmon` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_media_clock_restart` | `KL_media_clock_restart.sv` | `milan_dp` · `tkdiag` · 🔬`make aaf` | — |
| ✅ `KL_stream_table` | `KL_stream_table.sv` | `avtp_parser` · `avtp_rxmon` · `avtp_stream` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_talker_diag_ctx` | `KL_talker_diag_ctx.sv` | `milan_dp` · `tkdiag` · 🔬`make aaf` | — |
| ✅ `avtp_stream_parser` | `avtp_stream_parser.sv` | `aaf_audio_loop` · `avtp_parser` · `avtp_rxmon` · `avtp_stream` · `milan_dp` · `tsn_fuzz` · 🔬`make aaf` | — |
| 📦 `avtp_subtype_pkg` | `avtp_subtype_pkg.sv` | 🔬`make aaf` | — |


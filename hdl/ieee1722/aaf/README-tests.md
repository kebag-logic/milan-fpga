<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# `ieee1722/aaf` — modules & test coverage

**GENERATED** by `docs/traceability/gen_module_matrix.py` — do not
hand-edit. Part of the IEEE 1722 (AVTP) family; rolled up in
[`docs/traceability/MODULE_MATRIX.md`](../../../docs/traceability/MODULE_MATRIX.md).

| module | file | test | clauses |
|---|---|---|---|
| ✅ `KL_aaf_capture_i2s` | `KL_aaf_capture_i2s.sv` | `aaf` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_aaf_latency_chain` | `KL_aaf_latency_taps.sv` | `aaf_latency_taps` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_aaf_packetizer` | `KL_aaf_packetizer.sv` | `aaf` · `aaf_audio_loop` · `chmap_capture` · `milan_dp` · `tdm` · 🔬`make aaf` | — |
| ✅ `KL_aaf_rx_depacketizer` | `KL_aaf_rx_depacketizer.sv` | `aaf_audio_loop` · `avtp_rxmon` · `milan_dp` · `tsn_fuzz` · 🔬`make aaf` | — |
| ✅ `KL_chan_map_capture` | `KL_chan_map_capture.sv` | `chmap_capture` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_chan_map_render` | `KL_chan_map_render.sv` | `chmap_render` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_i2s_playback` | `KL_i2s_playback.sv` | `i2spb` · `milan_dp` · `mmcm_servo` · 🔬`make aaf` | — |
| ✅ `KL_lat_history_ring` | `KL_lat_history_ring.sv` | `lat_history_ring` · 🔬`make aaf` | — |
| ✅ `KL_media_adv` | `KL_media_adv.sv` | `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_pcm_lpf` | `KL_pcm_lpf.sv` | `milan_dp` · `pcmlpf` · 🔬`make aaf` | — |
| ✅ `KL_pcm_ring_bram` | `KL_pcm_ring_bram.sv` | `pcm_ring_bram` · 🔬`make aaf` | — |
| ✅ `KL_pcm_route` | `KL_pcm_route.sv` | `avtp_rxmon` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_pcm_tx` | `KL_pcm_tx.sv` | `pcm_tx` · ➰milan_dp · 🔬`make aaf` | — |
| ✅ `KL_tdm_capture` | `KL_tdm_capture.sv` | `milan_dp` · `tdm` · 🔬`make aaf` | — |
| ✅ `KL_tdm_render` | `KL_tdm_render.sv` | `milan_dp` · `tdm_render` · 🔬`make aaf` | — |
| ✅ `KL_tone_gen` | `KL_tone_gen.sv` | `milan_dp` · 🔬`make aaf` | — |
| ✅ `aaf_talker_i2s` | `aaf_talker_i2s.sv` | `aaf` · `milan_dp` · 🔬`make aaf` | — |


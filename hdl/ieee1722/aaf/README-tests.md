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
| ✅ `KL_aaf_capture_i2s` | `KL_aaf_capture_i2s.sv` | `aaf` · `hostplane` · `milan_dp` · 🔬`make aaf` | 7.3.3 |
| ✅ `KL_aaf_latency_chain` | `KL_aaf_latency_taps.sv` | `aaf_latency_taps` · `hostplane` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_aaf_packetizer` | `KL_aaf_packetizer.sv` | `aaf` · `aaf_audio_loop` · `chmap_capture` · `hostplane` · `milan_dp` · `tdm` · 🔬`make aaf` | 35.2.2.8.4, 4.3.5.2, 4.4.2.3, 802.3 |
| ✅ `KL_aaf_rx_depacketizer` | `KL_aaf_rx_depacketizer.sv` | `aaf_audio_loop` · `avtp_rxmon` · `hostplane` · `milan_dp` · `tsn_fuzz` · 🔬`make aaf` | — |
| ✅ `KL_aes3_rx` | `KL_aes3_rx.sv` | `aes3` · 🔬`make aaf` | — |
| ✅ `KL_aes3_tx` | `KL_aes3_tx.sv` | `aes3` · 🔬`make aaf` | — |
| ✅ `KL_chan_map_capture` | `KL_chan_map_capture.sv` | `chmap_capture` · `hostplane` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_chan_map_render` | `KL_chan_map_render.sv` | `chmap_render` · `hostplane` · `milan_dp` · `pcm_playback` · ➰chmap_capture · 🔬`make aaf` | — |
| ✅ `KL_i2s_feed_mux` | `KL_i2s_feed_mux.sv` | `hostplane` · `milan_dp` · `pcm_playback` · 🔬`make aaf` | — |
| ✅ `KL_i2s_playback` | `KL_i2s_playback.sv` | `hostplane` · `i2spb` · `milan_dp` · `mmcm_servo` · `pcm_playback` · 🔬`make aaf` | — |
| ✅ `KL_lat_history_ring` | `KL_lat_history_ring.sv` | `lat_history_ring` · 🔬`make aaf` | — |
| ✅ `KL_media_adv` | `KL_media_adv.sv` | `hostplane` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_pair_blend` | `KL_pair_blend.sv` | `hostplane` · `milan_dp` · `pair_fill` · 🔬`make aaf` | — |
| ✅ `KL_pair_zero_fill` | `KL_pair_zero_fill.sv` | `hostplane` · `milan_dp` · `pair_fill` · 🔬`make aaf` | 5.3.7.2, 5.3.7.3, M-DEV-13 |
| ✅ `KL_pcm_lpf` | `KL_pcm_lpf.sv` | `hostplane` · `milan_dp` · `pcmlpf` · 🔬`make aaf` | — |
| ✅ `KL_pcm_ring_bram` | `KL_pcm_ring_bram.sv` | `hostplane` · `pcm_ring_bram` · 🔬`make aaf` | — |
| ✅ `KL_pcm_route` | `KL_pcm_route.sv` | `avtp_rxmon` · `hostplane` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `KL_pcm_tx` | `KL_pcm_tx.sv` | `pcm_playback` · `pcm_tx` · ➰hostplane,milan_dp · 🔬`make aaf` | — |
| ✅ `KL_tdm_capture` | `KL_tdm_capture.sv` | `hostplane` · `milan_dp` · `tdm` · 🔬`make aaf` | 7.3.3 |
| ✅ `KL_tdm_capture_master` | `KL_tdm_capture_master.sv` | `hostplane` · `milan_dp` · `tdm` · 🔬`make aaf` | 7.3.3 |
| ✅ `KL_tdm_render` | `KL_tdm_render.sv` | `hostplane` · `milan_dp` · `tdm_render` · 🔬`make aaf` | — |
| ✅ `KL_tone_gen` | `KL_tone_gen.sv` | `hostplane` · `milan_dp` · 🔬`make aaf` | — |
| ✅ `aaf_talker_i2s` | `aaf_talker_i2s.sv` | `aaf` · `hostplane` · `milan_dp` · 🔬`make aaf` | 4.3.5.2, 4.4.2.3, M-DEV-13 |


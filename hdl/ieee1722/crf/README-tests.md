<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# `ieee1722/crf` -- modules & test coverage

**GENERATED** by `docs/traceability/gen_module_matrix.py` -- do not
hand-edit. Part of the IEEE 1722 (AVTP) family; rolled up in
[`docs/traceability/MODULE_MATRIX.md`](../../../docs/traceability/MODULE_MATRIX.md).

| module | file | test | clauses |
|---|---|---|---|
| ✅ `KL_aaf_clock_meter` | `KL_aaf_clock_meter.sv` | `aaf_clock_meter` · `follow_ring` · `milan_dp` · `milan_dp_mclk` · ➰capture_coherence,milan_dp_render | -- |
| ✅ `KL_crf_rx` | `KL_crf_rx.sv` | `aaf_clock_meter` · `crf_rx` · `follow_ring` · `milan_dp` · ➰capture_coherence,milan_dp_mclk,milan_dp_render | -- |
| ✅ `KL_crf_tx` | `KL_crf_tx.sv` | `crf_tx` · `milan_dp` · ➰capture_coherence,milan_dp_mclk,milan_dp_render | -- |
| ✅ `KL_media_grid_align` | `KL_media_grid_align.sv` | `capture_coherence` · `follow_ring` · `media_grid_align` · `milan_dp` · ➰milan_dp_mclk,milan_dp_render | -- |
| ✅ `KL_media_nco` | `KL_media_nco.sv` | `capture_coherence` · `follow_ring` · `media_grid_align` · `media_nco` · `milan_dp` · ➰milan_dp_mclk,milan_dp_render | -- |
| ✅ `KL_mmcm_drp_servo` | `KL_mmcm_drp_servo.sv` | `aaf_clock_meter` · `crf_rx` · `follow_ring` · `milan_dp` · `mmcm_servo` · `mmcm_servo_autorepair` · ➰capture_coherence,milan_dp_mclk,milan_dp_render | -- |

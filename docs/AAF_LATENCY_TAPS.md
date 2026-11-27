<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# AAF end-to-end latency — where every tap sits (roadmap item-11)

This is deliverable #2 of the AAF-latency-breakdown directive: a picture of
**where in the TX and RX pipeline each latency point is measured**, mapped to
the exact RTL trigger and the CSR that reports it. The measurement engine is
[`hdl/ieee1722/aaf/KL_aaf_latency_taps.sv`](../hdl/ieee1722/aaf/KL_aaf_latency_taps.sv); the register block is
[Section 0x870 of `REGISTER_MAP.md`](reference/REGISTER_MAP.md#0x870-----aaf-per-stage-latency-taps--roadmap-item-11-kl_aaf_latency_taps); the per-sample DDR3 history is
[`LATENCY_HISTORY_RING.md`](LATENCY_HISTORY_RING.md).

All deltas are in **`axis_clk` cycles**.
Seconds equal cycles divided by the configuration's `milan_clk_hz`.
Cycle time is `1e9 / milan_clk_hz` nanoseconds.

<!-- configured-tap-clocks:start -->
| Configuration | Milan clock (Hz) | ns/cycle | Latency taps |
|---|---:|---:|---|
| `endstation_arty_4x4` | 50000000 | 20 | present |
| `endstation_arty_8ch` | 50000000 | 20 | present |
| `endstation_arty_current` | 50000000 | 20 | present |
| `endstation_arty_split` | 50000000 | 20 | present |
| `endstation_arty_usbaudio` | 50000000 | 20 | present |

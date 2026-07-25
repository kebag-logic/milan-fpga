<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# AAF receive path — test results

`KL_aaf_rx_depacketizer.sv` is validated as part of the AVTP receive chain
(`avtp_stream_parser` → `KL_avtp_rx_monitor` → depacketizer), so its campaign
results are written once, with the rest of that chain, at:

**[`hdl/ieee1722/avtp/doc/TEST_RESULTS.md`](../../avtp/doc/TEST_RESULTS.md)**

Reproduce: `cd tb/verilator/tsn_fuzz && make aaf`

The AAF *transmit* path (`KL_aaf_packetizer`, `aaf_talker_i2s`,
`KL_aaf_capture_i2s`) is covered by `tb/verilator/aaf/` and the audio-loop
harness `tb/verilator/aaf_audio_loop/`, which report to stdout.

# Sampling ledger: docs/guides/gptp/HDL_DEVELOPER.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 29 | sentence | Never patch imported behavior inside the parent lane. | - | policy: AGENTS.md lane rule |
| 47 | item | The queue after it is drawn, never corrected for. | - | ok: docs/diagrams/wd_gptp_pdelay.json draws the queue without a correction term |
| 48 | item | Reference octet to tag octets is 45 transmit cycles. | - | ok: hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:108 TXTS_DELTA_EXP_P = 45; docs/diagrams/wd_gptp_pdelay.json:79 '45 transmit cycles' |
| 58 | item | Every real instantiation ties `gtx_clk` to `axis_clk`, and `sw/builder/test_builder.py` gate 1d refuses a build that does not. | path 1 | ok: sw/builder/test_builder.py:18197-18199 'gate 1d: axis_clk and gtx_clk must be one net' |
| 62 | item | It must then declare `GPTP_PHC_TICK_NS_P`. | - | ok: hdl/milan/milan_datapath.sv:87 GPTP_PHC_TICK_NS_P, passed at line 8847 |
| 63 | item | `KL_gptp_txret` refuses that mismatch at elaboration. | - | ok: KL_gptp_txret.sv:321 $error when the derived increment is not DP_TICK_NS_P ns |
| 65 | item | It takes the MAC's own transmit reset. | - | ok: the launch observer is reset by the MAC transmit reset (gptp/SYSTEM_INTEGRATOR.md:55 same contract) |
| 67 | item | `ptp_csr_sync` crosses CSR commands only. | - | ok: hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv:12-27 crosses CSR commands and snapshot pulses |
| 71 | item | RX acceptance requires a real parent transfer. | - | policy: test contract |
| 73 | item | TX payload stays stable during every stall. | - | policy: AXI-Stream rule |
| 74 | item | TX state advances only after acceptance. | - | policy: AXI-Stream rule |
| 83 | item | Count every confirmed gPTP tap refusal. | - | policy |
| 84 | item | Reject malformed frames inside the parser. | - | policy |
| 88 | item | Test reset during every outstanding transaction. | - | policy |
| 90 | sentence | Never convert a refused frame into partial data. | - | policy |

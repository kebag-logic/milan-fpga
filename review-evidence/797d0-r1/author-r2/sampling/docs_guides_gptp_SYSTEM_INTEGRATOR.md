# Sampling ledger: docs/guides/gptp/SYSTEM_INTEGRATOR.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 19 | sentence | The builder rejects false product values. | - | ok: sw/builder/endstation_builder.py:4454 refuses fabric_gptp: false (retired, #259) |
| 21 | sentence | Every configuration needs one `gptp` section. | - | ok: sw/builder/endstation_builder.py:4460 requires a gptp: section; every configs/*.yaml carries one |
| 35 | sentence | All engine logic uses `axis_clk`. | - | ok: sw/builder/test_builder.py:18199 gate 1d ties gtx_clk to axis_clk |
| 37 | sentence | Reset stays synchronous and active-low. | - | ok: gptp plane resets are synchronous active-low (hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv rst_n) |
| 43 | row | \| Launch records \| Report every launched frame, in order \| | - | ok: the launch-record face of KL_gptp_txret |
| 47 | row | \| Publication \| Consume only committed generations \| | - | ok: atomic publication contract (gptp/MANAGER.md:20) |
| 49 | sentence | Never drive receive readiness from this observer. | - | policy: observer rule |
| 51 | sentence | The launch observer must watch the MAC's own transmit stream. | - | ok: KL_gptp_gmii_launch watches the MAC transmit stream (TXTS_DELTA_EXP_P line 122) |
| 55 | sentence | Give it the MAC's own transmit reset. | - | ok: as HDL_DEVELOPER.md:65 |
| 59 | sentence | That plane then delivers no timestamp and counts the loss. | - | ok: GPTP_DROPE[31:16] GPTP_TXTS_LOST counts records closed with no timestamp (REGISTER_MAP.md:1517) |
| 74 | row | \| `GPTP_DROPE[31:16]` \| Frames whose launch was not reconstructed \| | - | ok: hdl/common/csr/milan_csr.sv:907 A_GPTP_DROPE {txts_lost16, ev_drop16} |
| 76 | sentence | Zero PathTrace count means no published trace. | - | ok: PathTrace publication rule (gptp engine) |
| 78 | sentence | It never implies one hidden identity. | - | ok: same |
| 90 | item | Reset during active exchanges. | - | policy |

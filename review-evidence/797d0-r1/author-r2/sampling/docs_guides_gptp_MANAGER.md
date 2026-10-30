# Sampling ledger: docs/guides/gptp/MANAGER.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 21 | item | Direct health drives every AVTP uncertainty bit. | - | ok: hdl/milan/milan_datapath.sv:2179-2199 clkv_tu_w from the clock-validity block feeds the AAF ts_uncertain_i (line 1559) and the CRF tu (line 3546) |
| 29 | row | \| Product owner \| Implemented \| Feature-status ledger \| | - | ok: docs/reference/MILAN_FEATURE_STATUS.md gPTP rows |
| 30 | row | \| Protocol engine \| Implemented \| Donor suites \| | - | ok: gptp-processor/Makefile donor suites |
| 31 | row | \| Parent transport \| Implemented \| `gptp_shadow` \| | - | ok: tb/verilator/gptp_shadow exists |
| 32 | row | \| Public consumers \| Implemented \| `milan_dp` \| | - | ok: tb/verilator/milan_dp exists |
| 33 | row | \| Physical calibration \| Incomplete \| Issue #64 \| | issue 1 | ok: #64 OPEN |
| 34 | row | \| Propagation asymmetry \| Excluded for v1.2 \| Issue #511 \| | issue 1 | ok: #511 CLOSED as the exclusion decision; REQUIREMENTS.md:202-210 records it |
| 35 | row | \| Physical acceptance against the reference peer \| Incomplete \| Issue #117 \| | issue 1 | ok: #117 OPEN |
| 36 | row | \| Media clock selection \| Implemented \| Feature-status ledger \| | - | ok: docs/design/MEDIA_CLOCK_FOLLOWING.md:6 implemented |
| 38 | sentence | No external approval is claimed. | - | policy |
| 40 | sentence | Simulation remains necessary but insufficient. | - | policy |
| 45 | item | Physical grandmaster-winner evidence remains open. | - | ok: #117 OPEN covers the physical acceptance |
| 49 | item | Issue #74 media-clock bench acceptance remains open. | issue 1 | ok: #74 OPEN |
| 53 | sentence | Open upstream risks appear in the [engine guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/f97c18035be6ef5345e5af27db2124c5697c1b40/docs/MANAGER.md). | - | ok: gptp-processor gitlink f97c1803 (adopted by PR #805, the base's parent) |
| 58 | item | Run every donor suite. | - | policy |
| 59 | item | Run every parent integration suite. | - | policy |
| 63 | item | Require issue #117 physical acceptance. | issue 1 | ok: #117 OPEN |

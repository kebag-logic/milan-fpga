[A397] Current-document rescan at 6b2ebd1c435136966f84ffc16d28a80c7d6b9387

R367-2's unmodified proximity scanner returned 197 hits in 26 files.
R366-2's five committed-tree patterns were repeated without shell pipelines:
3, 53, 17 and 27 hit lines in scans 1-4; scan 5 had no hits.
The packet retains the complete outputs and exact-head receipts as
stale-r367.log/.json and stale-r366.log/.json. The R366 equivalent is
stale_scan_r366.py; it changes only command orchestration and output filtering.

Result: zero stale PHC-only restart or MEDIA_RESET claims outside docs/history/**.
The two stale rows from R367-2 F1 are corrected at
BAREMETAL_FIRMWARE.md:1469 and :1471. The former counts initializer plus sole
render reader; the latter excludes the PHC term and matches the unchanged
builder pin at test_builder.py:10774. Both cite #602.

Every match was inspected with its current context. Classifications:

- Current exclusion and supersession: CHANGELOG, ROADMAP, GM_LOSS_RECOVERY,
  TIME_SYNC, FPGA_DESIGN, REGISTER_MAP and MILAN_COMPLIANCE_MATRIX.
  These preserve tu/render behavior and name genuine restart causes separately.
- Firmware gate contract and builder fixtures: the corrected rows, preserved
  render initializer, census refusals, mutation anchors and diagnostics.
  Restored-cause strings describe planted defects, not accepted behavior.
- Executable checks and campaign inventory: milan_dp and tkdiag sources and
  documentation. The PHC cause is either excluded or deliberately injected;
  source-change and CRF checks retain their legitimate toggles. Dated check
  counts are explicitly historical. The coincident check grades suppression;
  pending requests merge and added causes are graded by isolated-step checks.
- Unrelated meanings: NVM window re-base/reload/restart, servo guard-streak
  restart, presentation-time wrap prose, adjfine resolution, and CRF silence.
  The silicon findings describe PHC steps covered by holdover and tu.

Per-file hit census (R367 proximity scan):

| File | Hit lines | Classification |
|---|---|---|
| `CHANGELOG.md` | 16, 118, 119, 120, 124, 126, 127, 128, 135, 137, 139 | Current ruling, preserved render path or genuine restart contract |
| `docs/MILAN_V12_ROADMAP.md` | 360 | Current ruling, preserved render path or genuine restart contract |
| `docs/design/GM_LOSS_RECOVERY.md` | 146, 148, 150, 156, 176, 177, 178, 179, 188, 198, 203, 205, 207, 213, 216, 220, 223, 224, 240, 242, 270 | Current ruling, preserved render path or genuine restart contract |
| `docs/design/PRESENTATION_TIME_WRAP.md` | 31 | Unrelated sense or preserved holdover evidence |
| `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` | 566, 567, 1201, 1202, 1204, 1457, 1893, 1913, 1931 | Unrelated sense or preserved holdover evidence |
| `docs/design/TIME_SYNC.md` | 113, 255, 259, 354 | Current ruling, preserved render path or genuine restart contract |
| `docs/findings/117_GPTP_SILICON_EVIDENCE.md` | 500 | Unrelated sense or preserved holdover evidence |
| `docs/fpga/FPGA_DESIGN.md` | 178 | Current ruling, preserved render path or genuine restart contract |
| `docs/integration/BAREMETAL_FIRMWARE.md` | 1469, 1470, 1471, 1522, 1524 | Current gate contract and deliberate refusal fixtures |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md` | 120, 206 | Current ruling, preserved render path or genuine restart contract |
| `docs/reference/REGISTER_MAP.md` | 128, 181 | Current ruling, preserved render path or genuine restart contract |
| `docs/testing/TESTING.md` | 273, 514 | Current ruling, preserved render path or genuine restart contract |
| `hdl/ieee1722/avtp/KL_media_clock_restart.sv` | 105, 171 | Current ruling, preserved render path or genuine restart contract |
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` | 707 | Unrelated sense or preserved holdover evidence |
| `hdl/milan/milan_datapath.sv` | 3097, 3098, 3124, 3125, 3128, 3130, 3132 | Current ruling, preserved render path or genuine restart contract |
| `sw/builder/test_builder.py` | 10718, 10719, 10766, 10768, 10773, 12478, 12499, 12500, 15098, 15099, 15115, 15116, 16654 | Current gate contract and deliberate refusal fixtures |
| `tb/verilator/milan_dp/Makefile` | 19, 20, 21, 117, 397, 398, 399 | Checks, controls, inventory and explicit evidence bounds |
| `tb/verilator/milan_dp/README.md` | 79, 93, 650, 657, 658, 659, 663, 665, 670, 671, 697, 700, 701, 706, 707, 708, 709, 710, 711, 712, 713, 727, 728, 730, 731, 744, 745, 746, 754, 990, 997, 999, 1001 | Checks, controls, inventory and explicit evidence bounds |
| `tb/verilator/milan_dp/gmstep_mutants.py` | 4, 6, 7, 8, 15, 16, 60, 130, 132, 133, 142, 185, 188, 189, 190, 193, 194, 197, 198, 199, 207, 208, 209, 210, 219, 220, 221, 222, 224, 225 | Checks, controls, inventory and explicit evidence bounds |
| `tb/verilator/milan_dp/sim_aclk.cpp` | 148 | Checks, controls, inventory and explicit evidence bounds |
| `tb/verilator/milan_dp/sim_gmstep.cpp` | 7, 11, 13, 20, 21, 887, 1060, 1061, 1062, 1065, 1073, 1075, 1079, 1080, 1091, 1099, 1100, 1137, 1138, 1139, 1143 | Checks, controls, inventory and explicit evidence bounds |
| `tb/verilator/milan_dp/sim_main.cpp` | 1050, 1061, 1062, 1064, 1065, 1085, 1087, 1089 | Checks, controls, inventory and explicit evidence bounds |
| `tb/verilator/mmcm_servo/sim_main.cpp` | 25, 26, 521, 525, 526, 527, 530, 554 | Unrelated sense or preserved holdover evidence |
| `tb/verilator/nvm_cosim/cosim_case_map.py` | 221, 224, 258, 327 | Unrelated sense or preserved holdover evidence |
| `tb/verilator/nvm_cosim/cosim_cases.cpp` | 1171 | Unrelated sense or preserved holdover evidence |
| `tb/verilator/tkdiag/sim_main.cpp` | 652 | Checks, controls, inventory and explicit evidence bounds |

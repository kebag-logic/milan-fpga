# Independent source sampling

Exact source head: 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee. Public author sampling is taken only from the evidence commit 8e15dcfa654286db6da6d970b480b786a105d634, not a private handoff. Raw excerpts: contradiction-source-excerpts.txt and review-source-excerpts.txt.

Fifteen deeper-sampling findings checked against their exact quotations and sources:

| Finding | Source check and outcome |
|---|---|
| D0-034 | milan_soc.py:1404,1502-1530,1746,1806-1809; shipping configuration:43-44. PASS: 16-beat buffered crossings, separate transmit packet FIFO, 50/100 MHz boundary. |
| D0-035 | milan_baremetal.c:1836-1867. Contradiction confirmed: own copy loop, magic and post-copy CRC. Correction has an extra length-check claim: report F2. |
| D0-036 | milan_soc.py:3054-3076. PASS: single-lane fast read, 12.5 MHz request, calibration skipped; request is not asserted to be effective SCK. |
| D0-037 | build.sh:378-399 and milan_soc.py:3049-3055. PASS: different board/flash and retired recipe, not merely dataplane shape. No new hardware claim. |
| D0-038 | milan_soc.py:3037-3041,4042-4044. PASS: zero L2 and nonzero override refused. |
| D0-039 | milan_soc.py:4039-4041. PASS: RV64 command rejected by current product profile. |
| D0-040 | KL_pp_shadow.sv:1123; milan_baremetal.c:1393,1641,1669; milan_datapath.sv:6678-6679; SAVED_STATE_MATERIALIZATION.md:163. PASS: live persistence separate from retired CSR zero. Cold-cycle statement accepted only as dated existing documentation. |
| D0-041 | milan_baremetal.c:1796-1805,1881. PASS: firmware configures identity/enables; retired init script is not current boot authority. |
| D0-042 | milan_datapath.sv:654-670; milan_csr.sv:1996-2000,2050-2084; csr/sim_main.cpp:531-542. PASS on absent shaper and no consumer. Project wording 'write-only scratch' permits shadow readback; do not interpret it as WO access. Suggested clarification in report S1. |
| D0-043 | SAVED_STATE_MATERIALIZATION.md:19-24,203; parent map restore owner. PASS: parent writes/restores map records, physical cold cycle still owed. |
| D0-044 | Same map owner, backend instance and firmware journal as D0-040/043. PASS: global absence of persistence is false. |
| D0-045 | milan_datapath.sv:654-657,8812-8824 and KL_gptp_txret.sv. PASS: retired record stamper is not live owner; RX tap and launch reconstruction are. |
| D0-047 | milan_feature_status.json:40 (all-fabric section); README gated block; current setters in matrix. PASS: no mandatory operation is listed missing in the shipping placement; do not conflate split status. |
| D0-048 | milan_baremetal/Makefile:6; no firmware include/call of trace producer; TRACE_LOGGING.md:246-250. PASS: supplied trace ABI does not establish shipping-image integration. |
| D0-049 | milan_datapath.sv:6678-6679; milan_baremetal.c:463-465,1669-1675. PASS: retired CSR zeros cannot supply journal verdict; firmware maintains slot verdicts. |

Ten sentences the author marked verified in author-r2/data/verdicts/docs_integration_c.json (all on docs/integration/INTEGRATION_GUIDE.md):

| Line | Claim | Independent source / result |
|---|---|---|
| 3 | Current all-fabric shipping control plane | milan_soc.py:2621, default mailbox off. PASS. |
| 58 | GET_STREAM_INFO has two owners | milan_datapath.sv:5995-6025 and processor top:3566-3588. PASS. |
| 64 | Parent answers every other word and validity flag | Processor top:3573-3585 substitutes VLAN and masks validity flags. FAIL: report F1. |
| 119 | Shipping axis clock is 50 MHz | endstation_ax7101_1x1_tdm8.yaml:44. PASS. |
| 120 | PHC runs at 50 MHz | milan_datapath.sv:3128-3137 plus SoC:850-852. PASS. |
| 121 | gtx_clk is not the PHY 125 MHz clock | SoC:850-852 ties it to milan_cd. PASS. |
| 159 | Load/verify descriptors before restore | milan_baremetal.c:1881-1890; image proof and CLOSED contract in processor restore. PASS. |
| 162 | Start restore on boot | milan_baremetal.c:1664-1665,1777-1780,1890; start when not already terminal, including failed-image path. PASS as fresh boot requirement. |
| 166 | Per-wait deadline 20 ms | processor top:169-170 derives ceil(clock/50); parent shadow:1227-1234 leaves derivation intact. PASS. |
| 167 | Whole restore bound 1,000 ms | processor top:171-179; parent shadow same binding. PASS as configured aggregate deadline, not total physical reboot/restore qualification. |

All 62 finding quotations were located. These samples do not assert every sentence was independently reverified. No licensed standard was newly rederived; sampled contradictions are code/interface claims. Prior clause-only findings remain outside this delta.

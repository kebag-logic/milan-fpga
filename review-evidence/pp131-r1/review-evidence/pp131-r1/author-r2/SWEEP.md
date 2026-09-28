# Section 15.2 contract sweep: statement-by-statement reconciliation

Processor head `2b38d68e704e8a62fbeae8171c9195ca93728488`; lane range `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3..HEAD`.
The contract's named search over `docs hdl tb` returned 658 matching lines (multiline, case-insensitive). 311 of them were rewritten or added by this lane; every other one carries its location-specific scope reason. Unreviewed: 0.

| Location | Matching text | Disposition |
|---|---|---|
| `tb/side_port/side_port_tb_wrap.sv:27` | input  wire          entity_enable_i, | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/side_port_tb_wrap.sv:127` | .entity_enable_i(entity_enable_i), | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/side_port_tb_wrap.sv:193` | .entity_enable_i(entity_enable_i), | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/sim_main.cpp:234` | dut->entity_enable_i = 0; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/sim_main.cpp:313` | dut->entity_enable_i = 0; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/sim_main.cpp:321` | dut->entity_enable_i = 1; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/sim_main.cpp:330` | dut->entity_enable_i = 0; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `hdl/aecp/KL_aecp_dyn_state.sv:47` | //                PERSISTENCE: a saved-state restore has to write these rows, | design rationale: the D3 restore writes these rows with their valid flags; still true |
| `hdl/aecp/KL_aecp_dyn_state.sv:67` | //                (the µprogram does), and it does not persist anything. The | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_dyn_state.sv:68` | //                D3 writer (KL_aecp_nvm_writer) persists selectors 0 to 5 one | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_dyn_state.sv:130` | //! DIAGNOSTIC, sticky: a persisted row was written; no manager reads it | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_dyn_state.sv:132` | //! one cycle, with an accepted write that CHANGES a persisted row's | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_dyn_state.sv:324` | //! cycle" EXCEPT the IDENTIFY value, so only the persisted set marks | the diagnostic dirty (port comment marks it so); IDENTIFY excluded |
| `hdl/aecp/KL_aecp_desc_store.sv:41` | //                The names are not persisted yet: the saved-state contract's | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/ucpu/sim_main.cpp:112` | std::vector<uint8_t> nvm_marks; | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:387` | if (dut->eff_nvm_stb_o) nvm_marks.push_back(dut->eff_nvm_mark_o); | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:426` | stw.clear(); commits = 0; nvm_marks.clear(); notify_classes.clear(); | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:559` | CHECK(h.commits == 0 && h.nvm_marks.empty() && h.notify_classes.empty(), | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:630` | CHECK(h.nvm_marks.size() == 1 && h.nvm_marks[0] == 0x21, | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:631` | "P7 NVM_MARK 0x21"); | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:639` | CHECK(h.commits == 0 && h.nvm_marks.empty() && h.notify_classes.empty(), | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:668` | CHECK(h.stw.empty() && h.commits == 0 && h.nvm_marks.empty() && | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:719` | CHECK(h.commits == 1 && h.nvm_marks.size() == 1 && | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:720` | h.nvm_marks[0] == 7 && h.notify_classes.size() == 1 && | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:731` | CHECK(h.commits == 0 && h.nvm_marks.empty() && h.notify_classes.empty(), | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:741` | CHECK(h.stw.empty() && h.commits == 0 && h.nvm_marks.empty() && | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:956` | CHECK(h.commits == 0 && h.nvm_marks.empty() && h.notify_classes.empty(), | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:1059` | CHECK(h.commits == 0 && h.nvm_marks.empty() && h.notify_classes.empty(), | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:1324` | CHECK(h.nvm_marks.size() == 1 && h.nvm_marks[0] == 1, | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:1348` | CHECK(h.stw.empty() && h.nvm_marks.empty(), | grades the NVM_MARK completion strobe itself; retained |
| `tb/ucpu/sim_main.cpp:1418` | CHECK(h.nvm_marks.size() == 1 && h.nvm_marks[0] == 1, | grades the NVM_MARK completion strobe itself; retained |
| `docs/architecture/06_aecp_engine.md:23` | (NVM manager 1, [07 §5.3](07_memory_maps.md#fig-07-nvmflow)), which persists and restores | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/06_aecp_engine.md:134` | - **Change snoop.** The dynamic-state store's accepted write that changes a persisted | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/06_aecp_engine.md:144` | descriptor's name is a persisted user name; IDENTIFY's value is not. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/06_aecp_engine.md:378` | emits none of them. The accepted name-lane write is the name group's persistence | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/06_aecp_engine.md:405` | `aecp_nvm_mark_o`, [02 §8.1](02_interfaces.md#81-what-the-integrator-reads-while-a-commit- | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/06_aecp_engine.md:406` | It is never a persistence trigger: the accepted `WRITE_ST` that changes the row selects | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/06_aecp_engine.md:467` | notification or mark. The mark is a completion notification, not a persistence | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/06_aecp_engine.md:636` | no PERSISTENT handling. (`CONTROLLER_AVAILABLE` origination exists solely for the | the lock's PERSISTENT flag, or waived MVU fields that store nothing |
| `docs/architecture/06_aecp_engine.md:687` | \| SET/GET_SYSTEM_UNIQUE_ID (0x0001/0x0002, rec) \| waived; VU response with MVU status 1  | the lock's PERSISTENT flag, or waived MVU fields that store nothing |
| `docs/architecture/06_aecp_engine.md:688` | \| SET/GET_MEDIA_CLOCK_REFERENCE_INFO (0x0003/0x0004, rec) \| waived; VU response with MVU | the lock's PERSISTENT flag, or waived MVU fields that store nothing |
| `docs/architecture/06_aecp_engine.md:904` | \| Effects \| `COMMIT`, `NVM_MARK`, `NOTIFY_ENQ` \| commit is the atomicity point \| | the effect micro-op list: mark retained as a completion effect |
| `docs/architecture/06_aecp_engine.md:919` | SEND_RESPONSE; END                    COMMIT; NVM_MARK sampling_rate  (completion only) | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/06_aecp_engine.md:938` | ([07 §5.3](07_memory_maps.md#fig-07-nvmflow)). `NVM_MARK` remains a completion effect | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/06_aecp_engine.md:939` | on `aecp_nvm_stb_o` / `aecp_nvm_mark_o`, with no record-selection authority. | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/ucpu/README.md:32` | chain (state write-back strobes, COMMIT, NVM_MARK, NOTIFY_ENQ — and their | grades the NVM_MARK completion strobe itself; retained |
| `tb/acmp_nvm/sim_main.cpp:2` | // KL_acmp_nvm_shadow suite — persistence shadow against an INDEPENDENT | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:16` | // Proven: debounce coalescing (N changes in one T-NVM-DEBOUNCE window -> | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:55` | constexpr int DEB_TICKS = 50;      // -GDEB_TICKS_P | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:56` | //! DR2c: cycles a failed attempt waits before the next (-GRETRY_BACKOFF_CYC_P) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/sim_main.cpp:142` | // build an F07.6 image: the persisted set from b, volatile fields = junk | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:241` | //! The persistence shadow, the physical-NVM device model, the monitors and | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:392` | long done_cyc = -1;              // restore_done_o first seen | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:698` | if (d->restore_done_o && done_cyc < 0) done_cyc = cycles; | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:829` | bool restore_done() { return d->restore_done_o != 0; } | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:903` | CHECK(!d->restore_fail_o && d->restore_cause_o == 0, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:909` | // cannot tell the two apart. restore_blank_o is the pin that can. | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:910` | CHECK(d->restore_blank_o, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:931` | "B3 burst released after T-NVM-DEBOUNCE"); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:947` | inject(2, b2b, 0x77);                        // same persisted set, new junk | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1021` | "E9 DR2c timing: each retry starts RETRY_BACKOFF_CYC_P cycles or more " | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/sim_main.cpp:1081` | CHECK(!d->restore_fail_o && d->restore_cause_o == 0, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1087` | CHECK(!d->restore_blank_o, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1135` | CHECK(d->restore_fail_o && d->restore_cause_o == 1, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1144` | CHECK(d->restore_blank_o, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1185` | CHECK(!d->restore_fail_o, "H3 live changes are not a failure"); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1232` | // protocol_processor_top publishes this vector as nvm_unflushed_o (issue | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1233` | // #90) and an integrator ORs it with d3_unflushed_o into a "saved state | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/acmp_nvm/sim_main.cpp:1236` | // cycle: it rises when a change is ACCEPTED (a capture whose persisted set | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1381` | if (!d->restore_done_o \|\| d->restore_fail_o) bad("the walk is not done, or failed"); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1470` | return d->restore_done_o && !d->pre_valid_o && !d->lsn_busy_o | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1810` | // change still lands once, after the second walk, and persists | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1824` | "%s: answered once and persisted after the second walk", tag); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2018` | if (!d->restore_done_o \|\| !d->restore_fail_o \|\| d->restore_cause_o != cause) { | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2020` | unsigned(d->restore_done_o), unsigned(d->restore_fail_o), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2026` | if (!d->restore_blank_o) bad("a failed walk reports records it discarded"); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2093` | CHECK(!d->restore_fail_o && d->restore_cause_o == 0 && !d->restore_blank_o | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2116` | // commands are served on defaults; persistence is not | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2179` | && !d->restore_fail_o, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2185` | // persists once the device ended the read | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2210` | "%s: the later change persists and the saved records stay", tag); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2248` | "%s: the change then persists and the saved records stay", tag); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2291` | const bool walk = l_walk_ok(why) && !d->restore_fail_o && d->restore_cause_o == 0 | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2329` | CHECK(wd_max == RS_TMO - 1 && aborts == 0 && !d->restore_fail_o | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2438` | // full restore, which is why restore_blank_o exists. | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2483` | CHECK(d->restore_done_o && !d->restore_fail_o && d->restore_cause_o == 0 | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2484` | && d->restore_blank_o && !pre_valid_seen && d->dbg_valid_o == 0 | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `docs/architecture/04_adp_engine.md:98` | \| AEM_PERSISTENT_ACQUIRE_SUPPORTED \| 0x00002000 \| 0 \| | unrelated capability flag (AEM_PERSISTENT_ACQUIRE_SUPPORTED) |
| `docs/architecture/04_adp_engine.md:159` | \| Held in DOWN until `entity_enable` (boot gate) \| Milan §5.6.1. The engine's `entity_en | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:52` | parameter int unsigned  DEB_TICKS_P   = 500, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:53` | parameter int unsigned  RETRY_MAX_P   = 2, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:55` | parameter int unsigned  RETRY_BACKOFF_CYC_P = 600, | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:66` | output logic                     restore_done_o,  //! restore complete level | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:67` | output logic                     restore_fail_o,  //! whole-restore abort level | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:68` | output logic                     restore_blank_o, //! completed walk validated ZERO record | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:251` | .DEB_TICKS_P  (DEB_TICKS_P), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:252` | .RETRY_MAX_P  (RETRY_MAX_P), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:254` | .RETRY_BACKOFF_CYC_P (RETRY_BACKOFF_CYC_P) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:261` | .restore_done_o  (restore_done_o), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:262` | .restore_fail_o  (restore_fail_o), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:263` | .restore_blank_o (restore_blank_o), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:405` | .walk_done_i    (restore_done_o), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/Makefile:16` | -GDEB_TICKS_P=50 -GRS_TMO_CYC_P=3000 -GRETRY_BACKOFF_CYC_P=600 \ | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:9` | //                02 §8 F02.8 class-F manager face; 08 §2 T-NVM-DEBOUNCE; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:86` | //                THE RECORDS (scalar stage). One record per persisted | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:101` | //                µCPU's accepted state-bus write to a persisted row that | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:118` | //                (T-NVM-DEBOUNCE). Its close arms one burst that drains | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:121` | //                DR2c (parent D3 §6.1): at most 1 + RETRY_MAX_P = 3 attempts | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:124` | //                BACKOFF waits RETRY_BACKOFF_CYC_P complete clk_i cycles | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:161` | //! T-NVM-DEBOUNCE in ms, counted on tick_i, the 1 ms tick (F08.1: 500 | rewritten or added by this lane (2b38d68e); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:162` | //! ms; the binding manager's DEB_TICKS_P is the same count) | rewritten or added by this lane (2b38d68e); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:165` | parameter int unsigned RETRY_MAX_P    = 2, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:169` | parameter int unsigned RETRY_BACKOFF_CYC_P = 50_000_000, | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:170` | //! T-NVM-RS-DEADLINE (F08.1), P-NVM-RS-TMO-CYC (F01.5): clocks a restore | rewritten or added by this lane (66267d9f); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:173` | //! T-NVM-RS-AGGREGATE (F08.1), P-NVM-RS-AGG-CYC (F01.5), DR3a: clock | rewritten or added by this lane (380a3e47); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:277` | if (RETRY_BACKOFF_CYC_P < 1) begin : g_backoff_check | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:278` | $error("KL_aecp_nvm_writer: RETRY_BACKOFF_CYC_P must be at least 1"); | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:830` | S_BACKOFF   // DR2c: RETRY_BACKOFF_CYC_P cycles from a failed attempt | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:921` | assign giveup_w    = write_err_w && (attempts_r >= 32'(1 + RETRY_MAX_P)); | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:1012` | bo_cnt_r <= RETRY_BACKOFF_CYC_P; | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/srp/KL_srp_listener_fsm.sv:346` | logic [N_SINKS_P-1:0]        rec_valid_r;   // record latched (persists past A8) | unrelated sense: a latched SRP record persists |
| `tb/acmp_nvm/README.md:2` | # acmp_nvm — KL_acmp_nvm_shadow persistence suite | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:8` | exit 0 = PASS, 353 checks. `-GDEB_TICKS_P=50` pins the debounce window the C++ | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/README.md:10` | `-GRS_TMO_CYC_P=3000` the walk's read deadline (`T-NVM-RS-DEADLINE`) that group N | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:11` | places its boundaries against, and `-GRETRY_BACKOFF_CYC_P=600` the DR2c wait | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/README.md:12` | after a failed commit attempt (`T-NVM-RETRY-BACKOFF`, 500 ms in the product) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/README.md:15` | Every restore verdict graded here (`restore_done_o`, `restore_fail_o`, | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/acmp_nvm/README.md:16` | `restore_blank_o`, `restore_cause_o`) is the binding manager's RAW verdict on | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/acmp_nvm/README.md:44` | bookkeeping, GET_RX-style — cost zero NVM traffic); T-NVM-DEBOUNCE | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:51` | starting `RETRY_BACKOFF_CYC_P` cycles or more after the failed attempt's | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/README.md:58` | `restore_blank_o` separating a walk that validated records from one that | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:59` | read blank or unframed media (`restore_done_o` is set on BOTH, which is | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:68` | bytes) aborting the WHOLE restore — `restore_fail_o`, not one preload | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:75` | `protocol_processor_top` exports as `nvm_unflushed_o` (issue #90) — the bit | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:119` | reset lands once after the second walk and persists. | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:147` | walk is graded whole: `restore_done_o` and `restore_fail_o` with the named | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:170` | issued only after the drain ended, and a later change persists. **N5c**: the | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:219` | violation (07 §5.3 restores before entity_enable) and are not defended | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:235` | - **M6** `restore_blank_o` hard-wired to `1'b0`: fails 2 of 76 (A2b empty | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `hdl/aecp/KL_aecp_engine.sv:270` | //                its done with the binding walk's end into restore_done_o, | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:273` | //                persistence work. | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:309` | //! T-NVM-RS-DEADLINE (F08.1), P-NVM-RS-TMO-CYC (F01.5): the D3 restore's | rewritten or added by this lane (66267d9f); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:312` | //! T-NVM-RS-AGGREGATE (F08.1), P-NVM-RS-AGG-CYC (F01.5), DR3a: the D3 | rewritten or added by this lane (380a3e47); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:318` | parameter int unsigned NVM_RETRY_BACKOFF_CYC_P = 50_000_000, | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:607` | output logic        d3_unflushed_o, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:611` | //! select no record; the D3 writer persists from the accepted change ---- | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:613` | output logic  [7:0] eff_nvm_mark_o, | the completion-mark export and its wiring; export comment rewritten |
| `hdl/aecp/KL_aecp_engine.sv:656` | //! DIAGNOSTIC: some persisted row was written since reset (sticky); | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:657` | //! not pending and not a persistence trigger (d3_unflushed_o is) | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:1695` | .eff_nvm_mark_o     (eff_nvm_mark_o), | the completion-mark export and its wiring; export comment rewritten |
| `hdl/aecp/KL_aecp_engine.sv:1840` | .RETRY_BACKOFF_CYC_P (NVM_RETRY_BACKOFF_CYC_P) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:1891` | .unflushed_o (d3_unflushed_o), | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/ucpu_pkg.sv:79` | OP_NVM_MARK   = 5'd22, | the NVM_MARK micro-op and its completion strobe, retained (15.2: mark instructions stay valid) |
| `docs/architecture/05_acmp_engine.md:16` | \| Binding persistence via NVM \| honoring STREAMING_WAIT on outputs (Δ14) \| | scope/delta table rows naming binding persistence; still true |
| `docs/architecture/05_acmp_engine.md:160` | \| The faces are **released once**, when the binding walk has drained. \| the shadow's own | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/05_acmp_engine.md:161` | \| The release is **the binding walk's end**, not the restore's. \| the release starts the | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/05_acmp_engine.md:186` | is bounded by `T-NVM-RS-DEADLINE`: a device that stops answering fails the whole walk at | the binding walk's own read deadline and listener release; raw facts of that walk, still true |
| `docs/architecture/05_acmp_engine.md:189` | are released and the listener answers, so persistence that wedges never holds ACMP | the binding walk's own read deadline and listener release; raw facts of that walk, still true |
| `docs/architecture/05_acmp_engine.md:207` | [`tb/pp_top`](../../tb/pp_top/README.md) (section BW; BW4 grades `restore_done_o` and | suite pointer; the sentence now adds the D3 grading |
| `docs/architecture/05_acmp_engine.md:576` | Δ14 (STREAMING_WAIT outputs) · Δ15 (listener SM + persistent binding) — master table | scope/delta table rows naming binding persistence; still true |
| `tb/prng/sim_main.cpp:229` | CHECK(dut->dbg_seeded_o == 1, "D: seeded flag persists"); | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `docs/architecture/01_overview.md:9` | Vendor Unique execution, unsolicited notifications, counters, and persistence. | scope statements; still true |
| `docs/architecture/01_overview.md:39` | \| Timers/deadlines, PRNG, persistence orchestration \| AVTP streaming datapath, CBS shapi | scope statements; still true |
| `docs/architecture/01_overview.md:111` | engine's enable is the requested `entity_enable` AND `restore_done_o` (both walks) | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/01_overview.md:143` | \| Δ15 \| Listener behavior = Milan 8-state binding/probing SM; binding persists across po | scope statements; still true |
| `docs/architecture/01_overview.md:176` | \| P-NVM-RS-TMO-CYC \| ceil(P-CLK-HZ / 50) (20 ms) \| above the slowest single record read | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/architecture/01_overview.md:177` | \| P-NVM-RS-AGG-CYC \| P-CLK-HZ (1,000 ms) \| DR3a **ratified** as an enforced bound (`NVM | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/architecture/01_overview.md:178` | \| P-NVM-RETRY-BACKOFF-CYC \| ceil(P-CLK-HZ / 2) (500 ms) \| DR2c ruled value: `(CLK_HZ_P  | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `docs/architecture/01_overview.md:179` | \| P-NVM-DEB-TICKS \| 500 ticks of `tick_ms` (500 ms) \| DR2a ruled value; a module parame | rewritten or added by this lane (2b38d68e); states the D3 contract |
| `docs/architecture/01_overview.md:180` | \| P-NVM-RETRY-MAX \| 2 additional retries = 3 attempts \| DR2c ruled value; a module para | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_ucpu.sv:106` | output logic  [7:0] eff_nvm_mark_o, | the NVM_MARK micro-op and its completion strobe, retained (15.2: mark instructions stay valid) |
| `hdl/aecp/KL_aecp_ucpu.sv:435` | eff_nvm_stb_o      = advance_e_w && (uop_e_r.op == OP_NVM_MARK); | the NVM_MARK micro-op and its completion strobe, retained (15.2: mark instructions stay valid) |
| `hdl/aecp/KL_aecp_ucpu.sv:436` | eff_nvm_mark_o     = uop_e_r.imm[7:0]; | the NVM_MARK micro-op and its completion strobe, retained (15.2: mark instructions stay valid) |
| `docs/architecture/08_timing.md:43` | \| T-NVM-DEBOUNCE \| 500 ms: 500 ticks of the 1 ms `tick_ms` (`DEB_TICKS_P` in the binding | rewritten or added by this lane (2b38d68e); states the D3 contract |
| `docs/architecture/08_timing.md:44` | \| T-NVM-RS-DEADLINE \| `P-NVM-RS-TMO-CYC` clocks without progress (20 ms, ceil(`P-CLK-HZ` | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/architecture/08_timing.md:45` | \| T-NVM-RS-AGGREGATE \| `P-NVM-RS-AGG-CYC` clocks from the accepted restore start (1,000  | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/architecture/08_timing.md:46` | \| T-NVM-RETRY-BACKOFF \| `P-NVM-RETRY-BACKOFF-CYC` clocks (500 ms) from a failed record w | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `docs/architecture/08_timing.md:56` | govern persistence; none stands for another. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/08_timing.md:60` | \| producer debounce \| each record producer (binding manager, D3 writer) \| `T-NVM-DEBOUN | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/08_timing.md:62` | \| producer retry \| each record producer \| at most **three attempts** per record (the fi | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/08_timing.md:64` | \| per-wait restore deadline \| each restore walk \| `T-NVM-RS-DEADLINE`, 20 ms = ceil(`P- | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/architecture/08_timing.md:65` | \| aggregate restore deadline \| from the accepted restore start (`restore_go_i`, the inte | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/architecture/08_timing.md:77` | **One alarm.** `nvm_alarm_o` is the only reset-sticky persistence alarm, and only a | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/08_timing.md:160` | \| T-LOCK-UNLOCK, T-IDENT-BURST, T-IDENT-REARM, T-CTR-OBSERVE, T-NVM-DEBOUNCE \| singleton | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/08_timing.md:166` | The persistence times take no timer-service slot: each record producer counts | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/08_timing.md:167` | `T-NVM-DEBOUNCE` in `tick_ms` ticks and `T-NVM-RETRY-BACKOFF` in clocks, and each restore | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/08_timing.md:168` | walk counts `T-NVM-RS-DEADLINE` in clocks, all in counters of their own (two producers, | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/08_timing.md:169` | two walks). The T-NVM-DEBOUNCE singleton keeps its reserved slot so no later base moves. | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/ucode/gen_ucode.py:27` | 'COMMIT': 21, 'NVM_MARK': 22, 'NOTIFY_ENQ': 23, | mark instruction retained as a completion effect; its comment rewritten where it claimed persistence |
| `hdl/aecp/ucode/gen_ucode.py:472` | u('NVM_MARK', imm=0x21),                     # completion mark only: the | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/ucode/gen_ucode.py:1365` | u('NVM_MARK', imm=1),                        # completion mark (the WRITE_ST persists) | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/ucode/gen_ucode.py:1440` | u('NVM_MARK', imm=1),                        # completion mark (the WRITE_ST persists) | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/ucode/gen_ucode.py:1586` | # no NVM_MARK here is a separate fact about completion notifications, not the | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/ucode/gen_ucode.py:1587` | # persistence exclusion; persisting it would violate the clause and burn | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/ucode/gen_ucode.py:1679` | u('NVM_MARK', imm=1),                        # completion mark (the WRITE_ST persists) | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/ucode/gen_ucode.py:1795` | u('NVM_MARK', imm=6),                        # completion mark of a changed map | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/ucode/gen_ucode.py:1929` | u('NVM_MARK', imm=1),                    # completion mark (the WRITE_ST persists) | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/ucode/gen_ucode.py:2006` | u('NVM_MARK', imm=1),                        # completion mark (the WRITE_ST persists) | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/ucode/gen_ucode.py:2095` | u('NVM_MARK', imm=7),                       # naming completion mark | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/09_verification.md:56` | \| **NVM** \| power-cut/restore: cut at randomized commit points, verify CRC fallback + re | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/09_verification.md:162` | Reset and persistence semantics: dyn_state A (everything invalid out of reset), | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/09_verification.md:163` | E (the diagnostic dirty marks the persisted set, and only it) and H (the change | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/dyn_state/sim_main.cpp:89` | void mark_dirty_only_for_persisted_fields(); | diagnostic dirty (section E) and the change qualifier (section H); section E title updated |
| `tb/dyn_state/sim_main.cpp:231` | // ---- E: the diagnostic dirty marks the persisted set, and only it ----- | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/dyn_state/sim_main.cpp:235` | void DynStateHarness::mark_dirty_only_for_persisted_fields() { | diagnostic dirty (section E) and the change qualifier (section H); section E title updated |
| `tb/dyn_state/sim_main.cpp:246` | "E: a persisted clock-source write did NOT mark the store dirty"); | diagnostic dirty (section E) and the change qualifier (section H); section E title updated |
| `tb/dyn_state/sim_main.cpp:356` | // `wr_chg_o` marks an accepted write that changes a persisted row's | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/dyn_state/sim_main.cpp:389` | "H: IDENTIFY is never a persisted change"); | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/dyn_state/sim_main.cpp:407` | mark_dirty_only_for_persisted_fields(); | diagnostic dirty (section E) and the change qualifier (section H); section E title updated |
| `hdl/adp/KL_adp_engine.sv:16` | //                    entity_enable_i — Milan §5.6.1 boot gate); | module-internal use of its entity_enable_i input, which the top drives with the effective enable (port comment updated) |
| `hdl/adp/KL_adp_engine.sv:101` | //! drives it with the effective enable: requested AND restore_done_o | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/adp/KL_adp_engine.sv:102` | input  wire                        entity_enable_i, | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/adp/KL_adp_engine.sv:244` | assign enable_rise_w = entity_enable_i && !enable_q_r; | module-internal use of its entity_enable_i input, which the top drives with the effective enable (port comment updated) |
| `hdl/adp/KL_adp_engine.sv:245` | assign enable_fall_w = !entity_enable_i && enable_q_r; | module-internal use of its entity_enable_i input, which the top drives with the effective enable (port comment updated) |
| `hdl/adp/KL_adp_engine.sv:256` | enable_q_r <= entity_enable_i; | module-internal use of its entity_enable_i input, which the top drives with the effective enable (port comment updated) |
| `hdl/adp/KL_adp_engine.sv:657` | if (entity_enable_i && !enable_fall_w | module-internal use of its entity_enable_i input, which the top drives with the effective enable (port comment updated) |
| `docs/README.md:35` | \| 10 \| [07 Memory maps](architecture/07_memory_maps.md) \| records, register and memory  | index entry pointing at 07 section 5, the updated authority |
| `docs/README.md:51` | \| System integrator \| steps 2 and 3, then persistence, then the side-port \| [07 persist | index entry pointing at 07 section 5, the updated authority |
| `docs/README.md:142` | \| `NVM` \| persistence manager \| | index entry pointing at 07 section 5, the updated authority |
| `docs/architecture/07_memory_maps.md:2` | # 07 — Memory Maps, Records, Persistence | section titles and the normative persisted/volatile table header |
| `docs/architecture/07_memory_maps.md:53` | side-port is read-only everywhere after `entity_enable` except the control window. | side-port access rules keyed to the requested enable; unchanged |
| `docs/architecture/07_memory_maps.md:200` | and so before `entity_enable` — **not** through the side-port window, and not as a | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:332` | included. Persisting them is the name stage of the saved-state contract: its | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:356` | sticky `dirty_o` (`aecp_dyn_dirty_o` at the top) is a diagnostic, not the trigger. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:438` | ## 5. Persistence | section titles and the normative persisted/volatile table header |
| `docs/architecture/07_memory_maps.md:440` | ### 5.1 Persisted vs volatile (normative set — REQ-PER-001/002) | section titles and the normative persisted/volatile table header |
| `docs/architecture/07_memory_maps.md:442` | \| Persisted (Milan clause) \| Volatile (clause) \| | section titles and the normative persisted/volatile table header |
| `docs/architecture/07_memory_maps.md:447` | The earlier design intention to persist `system_unique_id`, `user_mcr_prio` | MVU-waiver deferral; SUID/MCR spans stay deliberately erased (DR5) |
| `docs/architecture/07_memory_maps.md:450` | stored nor persisted by the processor in this release. | MVU-waiver deferral; SUID/MCR spans stay deliberately erased (DR5) |
| `docs/architecture/07_memory_maps.md:456` | name like any other and is persisted with the name group. Which record carries each | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:457` | persisted item, and which stage writes it, is §5.2's inventory. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:518` | dirty --> deb["first-dirty window of 500 ticks (T-NVM-DEBOUNCE) arms one burst"] | rewritten or added by this lane (2b38d68e); states the D3 contract |
| `docs/architecture/07_memory_maps.md:525` | ok -- "err, attempt 1 or 2" --> bo["BACKOFF RETRY_BACKOFF_CYC_P (500 ms), then a fresh lat | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:545` | aecp --> en["restore_done_o = both walks: entity_enable_i reaches ADP (Milan 5.6.1)"] | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:557` | and a row becoming valid at its reset value is a change. The µprogram's `NVM_MARK` | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:558` | instructions keep their completion effects (`aecp_nvm_stb_o` / `aecp_nvm_mark_o`, | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:565` | `T-NVM-DEBOUNCE` window (500 ticks of `tick_ms`: `DEB_TICKS_P`, `DEB_MS_P`); its close arm | rewritten or added by this lane (2b38d68e); states the D3 contract |
| `docs/architecture/07_memory_maps.md:574` | producer. A failed attempt waits `RETRY_BACKOFF_CYC_P` clocks (`NVM_RETRY_BACKOFF_CYC_P` | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:575` | at the top, 500 ms, [F08.1](08_timing.md) `T-NVM-RETRY-BACKOFF`) holding neither the | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:577` | The third failed attempt (`1 + RETRY_MAX_P`, `RETRY_MAX_P = 2` additional retries) drops | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:580` | `nvm_unflushed_o` (binding sinks) and `d3_unflushed_o` (any D3 record dirty); the | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:582` | `aecp_dyn_dirty_o` is a sticky diagnostic of the store, not persistence work. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:594` | \| `restore_done_o` = both walks \| the ADP engine's enable, `entity_enable_i && restore_d | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:604` | `restore_done_o` / `restore_fail_o` / `restore_blank_o` combine them with the D3 walk's | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:614` | \| waits `P-NVM-RS-TMO-CYC` consecutive clocks without progress (`T-NVM-RS-DEADLINE`): for | the binding walk's failure table (DEVICE/UNFRAMED and per-walk atomicity preserved) |
| `docs/architecture/07_memory_maps.md:621` | no record, a failed one included; the top's combined `restore_blank_o` never does (below). | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:651` | restore by a second count: `P-NVM-RS-AGG-CYC` clocks (1,000 ms, `T-NVM-RS-AGGREGATE`) | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/architecture/07_memory_maps.md:682` | \| `restore_done_o` \| the drained binding terminal AND the D3 walk's done (COMPLETE or DE | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:684` | \| `restore_fail_o` \| either walk failed \| | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:685` | \| `restore_blank_o` \| done, **not failed**, and neither walk validated a record: a faile | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:695` | persistence is a design decision (Milan silent), retained by the parent D3 contract | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:696` | (§16, "design-affirmative"). The earlier system_unique_id and MCR persistence plans are | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:707` | (`T-NVM-DEBOUNCE`, 500 ms), draining one burst; only a proven unchanged | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:721` | \| 0x30000–0x300FF \| RW \| control/status: entity_enable, boot state, NVM alarm, version/ | side-port access rules keyed to the requested enable; unchanged |
| `docs/architecture/07_memory_maps.md:737` | accesses — a write to a read-only window, an image write after `entity_enable`, or any | side-port access rules keyed to the requested enable; unchanged |
| `tb/acmp_talker/retry_cases.hpp:167` | // the retry's own response. Persistent silence saturates stale credits | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `tb/tx_slots/README.md:25` | a stalled byte and its ser_last must persist unchanged, the stream stalls and | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `tb/acmp_talker/retry_mutants.py:273` | "accept_kill_no_disable": "An accept-edge disable sets OFF, which persists and " | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:101` | persists across power cycles (§5.3.8.2). "Milan as additive profile" (original §17) | requirement text, the original-document finding or the retained decision table; statuses updated only where a stage has executable evidence |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:204` | the root validates every row, and commit is all-or-nothing. Persisting and | requirement text, the original-document finding or the retained decision table; statuses updated only where a stage has executable evidence |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:211` | names as the name group's persistence trigger; the group-7 mark is a completion | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:212` | notification, never a persistence trigger. The name stage's writer and its replay | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:216` | #### <a id="gap-09"></a>GAP-09 [Major] — Persistence requirements absent | requirement text, the original-document finding or the retained decision table; statuses updated only where a stage has executable evidence |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:223` | SM in `PRB_W_AVAIL` (§5.5.3.5.2). Persistence of the current configuration index is | requirement text, the original-document finding or the retained decision table; statuses updated only where a stage has executable evidence |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:234` | saved-state acceptance, which is the integrating platform's. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:319` | \| REQ-ADP-002 \| Milan §5.6.2 \| entity_capabilities: AEM, VU, CLASS_A, GPTP =1; PERSISTE | requirement text, the original-document finding or the retained decision table; statuses updated only where a stage has executable evidence |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:357` | \| REQ-ACMP-021 \| Milan §5.3.8.2/.3, §5.5.3.5.2 \| Binding (talker EID, source idx, contr | requirement text, the original-document finding or the retained decision table; statuses updated only where a stage has executable evidence |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:375` | \| REQ-AEM-011 \| Milan §5.4.2.11/.12 \| SET/GET_NAME for all names of implemented descrip | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:377` | \| REQ-AEM-013 \| Milan §5.4.2.15/.16 \| SET/GET_CLOCK_SOURCE per Clock Domain; persisted  | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:379` | \| REQ-AEM-015 \| Milan §5.4.2.19/.20 \| START/STOP_STREAMING: INPUT only (OUTPUT → NOT_SU | requirement text, the original-document finding or the retained decision table; statuses updated only where a stage has executable evidence |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:385` | \| REQ-AEM-021 \| Milan §5.4.2.27/.28 \| ADD/REMOVE_AUDIO_MAPPINGS: all-or-nothing BAD_ARG | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:428` | ### 6.7 Persistence | requirement text, the original-document finding or the retained decision table; statuses updated only where a stage has executable evidence |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:432` | \| REQ-PER-001 \| Milan §5.3.5.1, §5.3.7.1/.6, §5.3.8.1/.2/.3/.7, §5.3.9.1, §5.3.10.1, §5. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:434` | \| REQ-PER-003 \| (unstated) \| Current configuration index persistence — Milan silent; de | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:524` | \| 1 \| Current configuration index persistence unstated by Milan \| **Persist** (least su | requirement text, the original-document finding or the retained decision table; statuses updated only where a stage has executable evidence |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:527` | \| 4 \| `system_unique_id` / `user_mcr_prio` / media-clock-domain-name persistence unstate | requirement text, the original-document finding or the retained decision table; statuses updated only where a stage has executable evidence |
| `docs/architecture/02_interfaces.md:93` | loaded via `mgmt`) is written only while `entity_enable = 0` and is treated as | quasi-static load and side-port rules keyed to the requested enable; unchanged |
| `docs/architecture/02_interfaces.md:96` | order ([01 §5](01_overview.md)); `entity_enable` is the master gate implementing | rule 5's first line; its continuation now names the restore release |
| `docs/architecture/02_interfaces.md:98` | both restore walks are done (`restore_done_o`, [07 §5.3](07_memory_maps.md#fig-07-nvmflow) | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/02_interfaces.md:486` | \| `0x30000` \| RW \| control/status: `entity_enable`, `shutdown_req`, boot status, profil | quasi-static load and side-port rules keyed to the requested enable; unchanged |
| `docs/architecture/02_interfaces.md:499` | free. Long busy periods expected; the device's commits are asynchronous to protocol | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/02_interfaces.md:546` | unprovable image: never done). ADP's enable is `entity_enable_i && restore_done_o`, the | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/02_interfaces.md:558` | \| `nvm_unflushed_o` \| out \| `P-N-STREAM-IN` \| the binding manager's: bit k is 1 from t | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/02_interfaces.md:559` | \| `d3_unflushed_o` \| out \| 1 \| the D3 writer's: 1 from the cycle after the dynamic-sta | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/02_interfaces.md:561` | \| `aecp_dyn_dirty_o` \| out \| 1 \| a sticky diagnostic of the dynamic-state store (any r | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/02_interfaces.md:563` | \| `aecp_nvm_stb_o` / `aecp_nvm_mark_o` \| out \| 1 / 8 \| one `clk_i` cycle per committed | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/02_interfaces.md:574` | `restore_done_o`, `restore_busy_o`, `restore_fail_o`, `restore_blank_o` (done and not | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/02_interfaces.md:597` | \| The drain ends **only** on that operation's own `done` or `err`. \| never on time. A de | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/README.md:35` | \| [07 memory maps](../architecture/07_memory_maps.md) \| the entity model, records, the s | index entry pointing at 07 section 5, the updated authority |
| `docs/10_RESOURCE_AND_EFFORT.md:165` | store, dynamic-field mux, lock, timers, persistence, patch — costs ≈ 417 ± 208 LUT | historical estimate of the earlier front end; not a contract; D3 area is the packet's DR4 |
| `docs/10_RESOURCE_AND_EFFORT.md:298` | persistence (the ≈ 417-LUT front end), keep its ADP and ACMP engines, and point this | historical estimate of the earlier front end; not a contract; D3 area is the packet's DR4 |
| `docs/guides/operator.md:80` | \| 0x00000 \| write before `entity_enable`, read \| reserved seam. **Reads 0x00000000** —  | side-port window rules and the requested enable's shutdown semantics; unchanged |
| `docs/guides/operator.md:88` | `entity_enable`, or an unmapped address — answers with the error flag one cycle later and | side-port rule keyed to the requested enable |
| `docs/guides/operator.md:107` | \| 3 \| 0 \| `entity_enable_i` \| | side-port window rules and the requested enable's shutdown semantics; unchanged |
| `docs/guides/operator.md:206` | \| 1 \| read only \| bit 0 `entity_enable_i` (the **requested** enable) · bit 1 restore bu | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/operator.md:233` | \| Situation \| Terminal \| Busy \| Done \| Failed \| Blank (`restore_blank_o`) \| | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/operator.md:274` | enable the machine sees is the **effective** one, `entity_enable_i` AND restore done; cont | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/operator.md:280` | - **deasserting `entity_enable_i`** is the shutdown — it emits ENTITY_DEPARTING and | side-port window rules and the requested enable's shutdown semantics; unchanged |
| `tb/acmp_talker/README.md:93` | the teardown itself is never delayed by it (WITHDRAW_TALKER, timer cancel | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `tb/acmp_talker/README.md:300` | - `accept_kill_no_disable`: An accept-edge disable sets OFF, which persists and latches th | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `hdl/top/protocol_processor_top.sv:128` | //! T-NVM-RS-DEADLINE (F08.1), P-NVM-RS-TMO-CYC (F01.5): each restore | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:138` | //! T-NVM-RS-AGGREGATE (F08.1), P-NVM-RS-AGG-CYC (F01.5): the D3 walk | rewritten or added by this lane (380a3e47); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:149` | parameter int unsigned NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2), | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:214` | //! restore_done_o; the side port's image-window lock sees it as is | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:215` | input  wire         entity_enable_i, | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:455` | output logic        restore_done_o, | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:465` | output logic        restore_fail_o, | declaration under its rewritten combined-verdict comment |
| `hdl/top/protocol_processor_top.sv:470` | output logic        restore_blank_o, | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:477` | //! restore_done_o and restore_fail_o). Completed bindings stay restored. | rewritten or added by this lane (505524e5); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:479` | //! the D3 walk's first abort cause, valid with restore_fail_o: 0 none, | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:491` | //! Bit k rises on the cycle the manager ACCEPTS a changed persisted set | the binding manager's own pending vector, raw by design; the OR with d3_unflushed_o is stated |
| `hdl/top/protocol_processor_top.sv:494` | //! so a write-back that changes no persisted field never raises it — and | the binding manager's own pending vector, raw by design; the OR with d3_unflushed_o is stated |
| `hdl/top/protocol_processor_top.sv:499` | //! with d3_unflushed_o below (aecp_dyn_dirty_o stays a diagnostic); | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:502` | output logic [N_STREAM_IN_P-1:0] nvm_unflushed_o, | the binding manager's own pending vector, raw by design; the OR with d3_unflushed_o is stated |
| `hdl/top/protocol_processor_top.sv:505` | //! write that changed a persisted dynamic-state row (configuration, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:510` | output logic                     d3_unflushed_o, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:666` | //! Quasi-static (02 §2 rule 4: set before entity_enable, stable after). | MAAP quasi-static inputs set before the requested enable; unrelated to the restore |
| `hdl/top/protocol_processor_top.sv:703` | //! DIAGNOSTIC only: some persisted dynamic-state row was written since | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:704` | //! reset (sticky). Not pending and not a persistence trigger: the D3 | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:705` | //! writer's d3_unflushed_o above is the pending of these rows. | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:706` | output logic                         aecp_dyn_dirty_o, | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:716` | //! record group a committed command changed (KL_aecp_ucpu OP_NVM_MARK: | the completion-mark export (comment rewritten: completion only, no record selection) |
| `hdl/top/protocol_processor_top.sv:724` | //! changing write itself; groups 6 and 7 are the saved-state contract's | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:728` | output logic  [7:0]                  aecp_nvm_mark_o,     //! that group's mark code, vali | the completion-mark export (comment rewritten: completion only, no record selection) |
| `hdl/top/protocol_processor_top.sv:1697` | assign adp_enable_w = entity_enable_i && restore_done_o; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:1715` | //! ended (restore_done_o): no advertisement precedes a restore write. | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:1717` | .entity_enable_i       (adp_enable_w), | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:1846` | //! END, and restore_done_o below takes it. | the admission release is one term of the combined restore_done_o; true |
| `hdl/top/protocol_processor_top.sv:2551` | .RETRY_BACKOFF_CYC_P (NVM_RETRY_BACKOFF_CYC_P) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2558` | .restore_done_o   (nvm_walk_done_w), | wiring of the binding manager's raw verdicts and pending, or the diagnostic dirty, to their named nets |
| `hdl/top/protocol_processor_top.sv:2559` | .restore_fail_o   (nvm_walk_fail_w), | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2560` | .restore_blank_o  (nvm_walk_blank_w), | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2588` | .dbg_dirty_o      (nvm_unflushed_o), | wiring of the binding manager's raw verdicts and pending, or the diagnostic dirty, to their named nets |
| `hdl/top/protocol_processor_top.sv:2601` | assign restore_done_o   = nvm_walk_done_w && lsn_released_w && d3_done_w; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2603` | \|\| (nvm_walk_done_w && !restore_done_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2605` | assign restore_fail_o   = nvm_walk_fail_w \|\| d3_fail_w; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2608` | assign restore_blank_o  = restore_done_o && !restore_fail_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:3488` | .NVM_RETRY_BACKOFF_CYC_P (NVM_RETRY_BACKOFF_CYC_P) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:3636` | .d3_unflushed_o     (d3_unflushed_o), | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:3638` | .eff_nvm_mark_o     (aecp_nvm_mark_o), | the completion-mark export (comment rewritten: completion only, no record selection) |
| `hdl/top/protocol_processor_top.sv:3673` | .dyn_dirty_o        (aecp_dyn_dirty_o) | wiring of the binding manager's raw verdicts and pending, or the diagnostic dirty, to their named nets |
| `hdl/top/protocol_processor_top.sv:4369` | .entity_enable_i (entity_enable_i), | side-port lock and status words: the requested enable beside the combined verdicts (comments added) |
| `hdl/top/protocol_processor_top.sv:4441` | 8'd1:    sp_ctrl_rdata_r <= {28'd0, restore_fail_o, restore_done_o, | side-port lock and status words: the requested enable beside the combined verdicts (comments added) |
| `hdl/top/protocol_processor_top.sv:4442` | restore_busy_o, entity_enable_i}; | side-port lock and status words: the requested enable beside the combined verdicts (comments added) |
| `hdl/top/protocol_processor_top.sv:4453` | link_up_i, entity_enable_i}; | side-port lock and status words: the requested enable beside the combined verdicts (comments added) |
| `docs/guides/integrator.md:90` | \| `NVM_RS_TMO_CYC_P` \| [F01.5](../architecture/01_overview.md#fig-01-params), `P-NVM-RS- | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/guides/integrator.md:91` | \| `NVM_RS_AGG_CYC_P` \| [F01.5](../architecture/01_overview.md#fig-01-params), `P-NVM-RS- | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/guides/integrator.md:92` | \| `NVM_RETRY_BACKOFF_CYC_P` \| [F01.5](../architecture/01_overview.md#fig-01-params), `P- | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:212` | \| `DESC_BASE_P` \| your descriptor image, sized by your entity model \| **your software** | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:236` | them before `entity_enable_i` and leave them alone. The two dynamic rows are | quasi-static inputs set before the requested enable, or MAAP's unrelated persistence seed |
| `docs/guides/integrator.md:244` | \| Level controls \| `entity_enable_i`, `link_up_i` \| | quasi-static inputs set before the requested enable, or MAAP's unrelated persistence seed |
| `docs/guides/integrator.md:268` | `entity_enable_i` is the boot gate of Milan §5.6.1, as a **request**. The ADP engine's | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:269` | effective enable is `entity_enable_i && restore_done_o`: the processor releases your | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:311` | \| NVM device \| `nvm_dev_*`, plus `restore_go_i`, `restore_busy_o`, `restore_done_o`, `re | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:320` | `cfg_maap_internal_i` to 1 (quasi-static, set before `entity_enable_i`) | quasi-static inputs set before the requested enable, or MAAP's unrelated persistence seed |
| `docs/guides/integrator.md:324` | optionally a persistence seed (`cfg_maap_seed_offset_i` + `cfg_maap_seed_valid_i`), | quasi-static inputs set before the requested enable, or MAAP's unrelated persistence seed |
| `docs/guides/integrator.md:352` | \| `nvm_unflushed_o` \| per-sink binding state the binding manager has accepted and not ye | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:353` | \| `d3_unflushed_o` \| the D3 writer's pending: 1 while any scalar record (configuration,  | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:354` | \| `aecp_dyn_dirty_o` \| a sticky **diagnostic**: some dynamic-state row was written since | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:356` | \| `restore_done_o`, `restore_busy_o`, `restore_fail_o`, `restore_blank_o` \| the combined | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:359` | \| `aecp_nvm_stb_o`, `aecp_nvm_mark_o` \| one cycle per committed command that marked a re | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:385` | 3. Pulse `restore_go_i`, **on every boot**; wait for `restore_done_o` or | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:386` | `restore_closed_o`, then read `restore_fail_o` **and** `restore_blank_o`. Three | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:394` | - `restore_done_o` (both walks done) releases your requested enable to ADP. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:395` | `restore_done_o` says the walks sequenced, not that anything came back: every | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:396` | per-record default sets it. `restore_blank_o` separates a restore from walks over | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:398` | `restore_closed_o` without `restore_done_o` means the descriptor image could not be | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:410` | 5. Assert `entity_enable_i` when you are ready; the processor forwards it to ADP only | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:411` | once `restore_done_o` is 1. Only then may the entity advertise. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/hdl-engineer.md:25` | hdl/acmp/           Milan binding and probing, plus the binding persistence shadow | directory map and shutdown semantics; consistent (module table updated) |
| `docs/guides/hdl-engineer.md:251` | \| There is no shutdown port \| [01 §5](../architecture/01_overview.md) describes a `SHUTD | directory map and shutdown semantics; consistent (module table updated) |
| `tb/pp_top/pp_top_wrap.sv:52` | input  wire         entity_enable_i, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:169` | output logic        restore_done_o, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:170` | output logic        restore_fail_o, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:171` | output logic        restore_blank_o, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:177` | output logic  [7:0] nvm_unflushed_o, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:178` | output logic        d3_unflushed_o, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/pp_top_wrap.sv:264` | //! the binding manager's OWN terminal (KL_acmp_nvm_shadow restore_done_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:265` | //! which the top's restore_done_o follows once the listener admission | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:271` | //! restore_done_o and restore_busy_o against them every cycle | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:334` | //! OP_NVM_MARK strobe and the OP_NOTIFY_ENQ strobe (06 section 8). The | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:339` | output logic  [7:0] aecp_nvm_mark_o, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:434` | //! NVM_RS_TMO_CYC_P, NVM_RS_AGG_CYC_P and NVM_RETRY_BACKOFF_CYC_P are | rewritten or added by this lane (b06130d8); states the D3 contract |
| `tb/pp_top/pp_top_wrap.sv:452` | .entity_enable_i       (entity_enable_i), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:496` | .aecp_dyn_dirty_o      (), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:499` | .aecp_nvm_mark_o       (aecp_nvm_mark_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:567` | .restore_done_o        (restore_done_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:568` | .restore_fail_o        (restore_fail_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:569` | .restore_blank_o       (restore_blank_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:575` | .nvm_unflushed_o       (nvm_unflushed_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:576` | .d3_unflushed_o        (d3_unflushed_o), | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/pp_top_wrap.sv:700` | assign dbg_adp_enable_o = u_dut.u_adp.entity_enable_i; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/gsi_internal.hpp:33` | while (!io.d->restore_done_o && budget-- != 0) io.step(); | boot helper waiting for the combined restore_done_o before its section |
| `tb/pp_top/gsi_internal.hpp:34` | CHECK(io.d->restore_done_o && !io.d->restore_fail_o, | boot helper waiting for the combined restore_done_o before its section |
| `tb/pp_top/gsi_internal.hpp:37` | io.d->entity_enable_i = 1; | boot helper waiting for the combined restore_done_o before its section |
| `tb/pp_top/d3_mutants.py:173` | (TOP, "  assign adp_enable_w = entity_enable_i && restore_done_o;\n", | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:174` | "  assign adp_enable_w = entity_enable_i;\n"),), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:177` | (TOP, "  assign restore_done_o   = nvm_walk_done_w && lsn_released_w && d3_done_w;\n", | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:178` | "  assign restore_done_o   = nvm_walk_done_w && lsn_released_w;\n"),), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:196` | ("D3R5: once the device ends the drained read a later SET persists",)), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:231` | (WRITER, "  assign giveup_w    = write_err_w && (attempts_r >= 32'(1 + RETRY_MAX_P));\n", | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:232` | "  assign giveup_w    = write_err_w && (attempts_r >= 32'(2 + RETRY_MAX_P));\n"),), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:244` | (SHADOW, "  assign fl_giveup_w = fl_err_w && (fl_retry_r >= RETRY_MAX_P);\n", | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:245` | "  assign fl_giveup_w = fl_err_w && (fl_retry_r >= RETRY_MAX_P + 1);\n"), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:246` | (SHADOW, "          if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P) begin | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:247` | "          if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P + 1) begin\n"), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:248` | (SHADOW, "end else if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P) begin\ | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:249` | "end else if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P + 1) begin\n")), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:258` | (TOP, "NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2),", | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:259` | "NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd200),"),), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:324` | //! one persisted row the service phase sets, and what its record must hold | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:339` | //! T-NVM-DEBOUNCE at the wrap's 1 ms = 100 clk | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:436` | if (!x.d->d3_unflushed_o && x.nv_st == H::NvState::NV_IDLE | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:481` | void s1_every_group_persists_its_record() { | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:505` | // D3S2: the pending export. d3_unflushed_o rises in the cycle after the | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:522` | if (rise < 0 && x.d->d3_unflushed_o) rise = at + 1; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:524` | if (rise >= 0 && fall < 0 && !x.d->d3_unflushed_o) fall = at + 1; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:525` | if (rise >= 0 && done < 0 && !x.d->d3_unflushed_o) ++holes; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:649` | void s7_identify_is_never_persisted() { | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:656` | pending += x.d->d3_unflushed_o ? 1 : 0; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:675` | pending += x.d->d3_unflushed_o ? 1 : 0; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:688` | // in all, each retry granted RETRY_BACKOFF_CYC_P cycles or more after the | rewritten or added by this lane (b06130d8); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:735` | && x.d->nvm_alarm_o && !x.d->d3_unflushed_o, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:738` | unsigned(x.d->d3_unflushed_o)); | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:794` | s1_every_group_persists_its_record(); | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:800` | s7_identify_is_never_persisted(); | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:914` | //! every persisted row at its reset value with its valid flag clear | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:935` | long done_early = 0;     //! cycles restore_done_o led the D3 terminal | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:941` | if (b.done < 0 && d->restore_done_o) b.done = c; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:945` | b.pending += d->d3_unflushed_o ? 1 : 0; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:947` | b.done_early += (d->restore_done_o && !both) ? 1 : 0; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1021` | return all && !x.d->d3_unflushed_o; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1044` | x.d->entity_enable_i = 1;                     // requested from reset (W14) | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1047` | CHECK(b.done > b.release && !x.d->restore_fail_o && !x.d->restore_blank_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1063` | pending += x.d->d3_unflushed_o ? 1 : 0; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1160` | CHECK(b.done > b.release && !d->restore_fail_o && d->dbg_d3_applied_o == 1 | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1181` | CHECK(b.done > b.release && !d->restore_fail_o && d->dbg_d3_applied_o == 3 | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1207` | CHECK(b.done > b.release && !d->restore_fail_o | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1267` | CHECK(erased && applied_before && b.done > b.release && x.d->restore_fail_o | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1270` | && !x.d->restore_blank_o, | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1296` | CHECK(planted && applied_before && b.done > b.release && x.d->restore_fail_o | rewritten or added by this lane (b06130d8); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1323` | // later SET persists. | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1332` | CHECK(b.done > b.release && d->restore_fail_o && !d->restore_blank_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1351` | "D3R5: once the device ends the drained read a later SET persists"); | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1357` | // SET persists and nothing stays unflushed. | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1361` | CHECK(b.done > b.release && d->restore_fail_o && d->rs_cause_o == 3 | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1375` | CHECK(drained_busy && set && writes == 1 && !x.d->d3_unflushed_o | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1379` | "persists (%d WRITEs, unflushed %u)", writes, unsigned(x.d->d3_unflushed_o)); | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1388` | CHECK(b.done > b.release && !x.d->restore_fail_o && x.d->restore_blank_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1396` | CHECK(b.done > b.release && !x.d->restore_fail_o && x.d->restore_blank_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1408` | CHECK(b.done > b.release && x.d->restore_fail_o && !x.d->restore_blank_o | rewritten or added by this lane (81c8a5f7); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1424` | && x.d->restore_fail_o && x.d->rs_cause_o == 6 && x.d->restore_rb_o | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1466` | : (b.done >= 0 && !x.d->restore_fail_o && x.d->dbg_dyn_rate_v_o); | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1534` | x.d->entity_enable_i = 1; | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1540` | CHECK(b.closed > b.release && b.done < 0 && x.d->restore_fail_o | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1541` | && !x.d->restore_done_o && x.d->dbg_d3_own_o && !x.d->dbg_adp_enable_o | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1545` | x.d->entity_enable_i = 0; | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1566` | // the drain, and once the device ends it a later SET persists. Over an | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1579` | CHECK(b.done + 1 == AGG && d->restore_fail_o && d->rs_cause_o == 3 | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1600` | "the device ends it a later SET persists"); | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1605` | CHECK(e.done + 1 > AGG && e.done + 1 <= AGG + RS_TMO && d->restore_fail_o | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1649` | : !d->restore_fail_o ? "COMPLETE" : "DEFAULTS"; | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1734` | if (rise < 0 && x.d->d3_unflushed_o) rise = c; | rewritten or added by this lane (81c8a5f7); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1735` | if (rise >= 0 && fall < 0 && !x.d->d3_unflushed_o) fall = c; | rewritten or added by this lane (81c8a5f7); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1763` | CHECK(armed && b.done > b.release && x.d->restore_fail_o == late | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1767` | hold, unsigned(x.d->restore_fail_o), unsigned(x.d->rs_cause_o)); | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1787` | CHECK(b.done > b.release && b.done - b.release < 2 * RS_TMO && d->restore_fail_o | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `hdl/packet_engine/KL_pp_nvm_port.sv:25` | //                asynchronous to protocol responses (03 §6 ordering rule d) | port-level fact: the device's commits stay asynchronous; 03 section 6 rule (d) now bounds the separate latch hold |
| `tb/adp_engine/sim_main.cpp:403` | d->entity_enable_i = 0;       d->link_up_i = 0; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/sim_main.cpp:426` | d->entity_enable_i = 1; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/sim_main.cpp:601` | d->entity_enable_i = 0; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/sim_main.cpp:616` | d->entity_enable_i = 1; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/sim_main.cpp:651` | d->entity_enable_i = 0;                    // departing | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/sim_main.cpp:656` | d->entity_enable_i = 1; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `hdl/packet_engine/KL_pp_side_port.sv:25` | //                write after entity_enable (07 §2: "read-only everywhere | the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design |
| `hdl/packet_engine/KL_pp_side_port.sv:26` | //                after entity_enable except the control window"), or any | the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design |
| `hdl/packet_engine/KL_pp_side_port.sv:50` | input  wire         entity_enable_i,  //! 1 = image window is write-locked | the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design |
| `hdl/packet_engine/KL_pp_side_port.sv:63` | output logic        img_we_o,         //! write strobe (only while !entity_enable_i) | the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design |
| `hdl/packet_engine/KL_pp_side_port.sv:133` | WIN_IMG_C:   fwd_ok_w = we_i ? !entity_enable_i : 1'b1;  // W pre-enable, R | the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design |
| `docs/diagrams/src/01-top-level.drawio:106` | <mxCell id="legend" value="Solid = transaction / data path &#183; dashed = events, configu | F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two producers; draw.io cannot export headless here (diagrams README), so source and export stay paired |
| `docs/diagrams/src/01-top-level.drawio:158` | <mxCell id="e24" value="persist" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;das | F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two producers; draw.io cannot export headless here (diagrams README), so source and export stay paired |
| `docs/diagrams/src/01-system-context.drawio:25` | <mxCell id="proc" value="&lt;b&gt;IEEE 1722.1 PROTOCOL PROCESSOR&lt;/b&gt;&#10;(this archi | F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two producers; draw.io cannot export headless here (diagrams README), so source and export stay paired |
| `docs/diagrams/21-integration-faces.svg:44` | <text x="464" y="560">NVM_RETRY_BACKOFF_CYC_P · SRP_DOM_DEF_VID_P</text> | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/diagrams/21-integration-faces.svg:67` | <text x="42" y="357" font-size="11.5" fill="#4a5058">entity_enable_i · link_up_i · gm_chan | requested-enable semantics (shutdown, Milan 5.6.1 gate) beside the added restore release |
| `docs/diagrams/21-integration-faces.svg:68` | <text x="42" y="380" font-size="11.5" fill="#a03030">entity_enable_i requests; ADP sees it | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/21-integration-faces.svg:120` | <text x="968" y="704" font-size="11.5" fill="#4a5058">pending: \|nvm_unflushed_o \| d3_unf | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/README.md:55` | **D3S1** every persisted group at its first and last declared index | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/README.md:60` | other record id moves. **D3S2** `d3_unflushed_o` rises the cycle after | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/README.md:137` | a later SET persists. **D3R5b** the same containment in pass 1: its header | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/README.md:140` | later SET persists with nothing left unflushed. **D3R6** an erased device restores blank a | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/README.md:172` | SET persists. Over an erased device the bound falls in pass 1, which | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/README.md:182` | `restore_done_o` is the COMBINED terminal: the binding walk's release | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/README.md:415` | `aecp_nvm_mark_o` export (issue #90) on this face and the name store: a | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:419` | notification: R21 proves the notification, never persistence (section D3 | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/README.md:423` | manager's own terminal (`dbg_walk_done_o`), not on `restore_done_o`, so every | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:425` | - **S0/S1** quiescence + snapshot identity, and `restore_done_o` has followed | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:442` | vendor default at the listener's release, while `entity_enable_i` is | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/README.md:452` | (issue #93 S4) grades the top's `restore_done_o` and `restore_busy_o` in | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:456` | next reset one of the two reads 1; `restore_done_o` never reads 1 while | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:458` | discovery arm of a walk lands in a cycle at or after its `restore_done_o` | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:484` | face, and the `nvm_unflushed_o` export (issue #90) sampled every cycle | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:487` | D3 records' is `d3_unflushed_o` (D3S2), and an integrator's pending is | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/README.md:569` | \| M36 \| the top's `restore_done_o` without the release (`= nvm_walk_done_w`) \| default  | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:621` | \| `identify_is_a_change` \| IDENTIFY (selector 7) made a persisted change \| `D3S7` \| 1  | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/README.md:641` | \| `quarantine_released_by_time` \| the arbiter ends a drain after 1,000 cycles \| `D3R5:  | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/README.md:688` | `restore_go_i` (and so before `entity_enable`); the "software has not | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/24-adp-acmp-states.svg:40` | <text x="305" y="214" font-size="10.5" fill="#4a5058">entity_enable_i AND restore_done_o</ | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/24-adp-acmp-states.svg:59` | <text x="42" y="579" font-size="11" fill="#4a5058">Deasserting entity_enable_i is the shut | requested-enable semantics (shutdown, Milan 5.6.1 gate) beside the added restore release |
| `docs/diagrams/23-bringup-decision.svg:32` | <text x="42" y="256" font-size="11.5" fill="#4a5058">Word 3 bit 0 is the REQUESTED entity_ | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/23-bringup-decision.svg:38` | <text x="630" y="256" font-size="11.5" fill="#4a5058">Milan §5.6.1 holds the advertise mac | requested-enable semantics (shutdown, Milan 5.6.1 gate) beside the added restore release |
| `hdl/acmp/KL_pp_acmp_lsn_admit.sv:59` | //                binding manager's walk at its terminal (restore_done_o, | the gate's input is the binding manager's raw terminal; release paragraph updated |
| `hdl/acmp/KL_pp_acmp_lsn_admit.sv:65` | //                on it, and the top's restore_done_o (both walks; it releases | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/acmp/KL_pp_acmp_lsn_admit.sv:95` | input  wire                 walk_done_i,     //! KL_acmp_nvm_shadow restore_done_o | the gate's input is the binding manager's raw terminal; release paragraph updated |
| `docs/diagrams/20-rtl-dataflow.svg:197` | <text x="40" y="851" font-size="10.5" fill="#4a5058">three boot releases: the binding walk | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/20-rtl-dataflow.svg:203` | <text x="40" y="948" font-size="10.5" fill="#4a5058">class-D status wires read every clock | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:10` | //                manager face; 08 §2 T-NVM-DEBOUNCE) | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:12` | //  Description : The per-sink ACMP binding persistence shadow of 05 §5 — | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:19` | //                each written F07.6 record onto the persisted field set | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:31` | //                (T-NVM-DEBOUNCE via tick_i, F07.9 coalescing) and bounded | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:32` | //                by DR2c: at most 1 + RETRY_MAX_P = 3 attempts per record, | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:33` | //                each failed one followed by RETRY_BACKOFF_CYC_P cycles | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:38` | //                RAW VERDICTS. restore_done_o/fail_o/blank_o/cause_o are | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:46` | //                and only a DIFFERING persisted field marks dirty — so | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:63` | //                aborts the WHOLE restore: restore_fail_o, no preload is | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:90` | //  Blank arm   : restore_done_o is SEQUENCING, not a verdict. Every | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:97` | //                did not), so restore_blank_o carries it: it is done AND no | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:118` | //! shipped firmware persisted carries started = 0 - and started = 0 now | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:125` | //! T-NVM-DEBOUNCE in tick_i units (F08.1: 500 ms at a 1 ms tick, DR2a) | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:126` | parameter int unsigned DEB_TICKS_P   = 500, | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:129` | parameter int unsigned RETRY_MAX_P   = 2, | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:133` | parameter int unsigned RETRY_BACKOFF_CYC_P = 50_000_000, | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:134` | //! T-NVM-RS-DEADLINE (F08.1) in clocks: the restore walk's read phase | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:148` | output logic                       restore_done_o, //! level: restore sequencing complete | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:149` | output logic                       restore_fail_o, //! level: the WHOLE restore aborted, a | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:150` | output logic                       restore_blank_o,//! level: the completed walk validated | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:151` | //! level, with restore_fail_o: why the walk failed. 0 it did not, 1 a | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:211` | // ---- the persisted projection (05 §5 NVM shadow field set) ------------- | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:406` | // ---- debounce (T-NVM-DEBOUNCE, F07.9 coalescing) ------------------------ | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:419` | deb_cnt_r  <= DEB_TICKS_P; | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:516` | if (RETRY_BACKOFF_CYC_P < 1) begin : g_backoff_check | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:517` | $error("KL_acmp_nvm_shadow: RETRY_BACKOFF_CYC_P must be at least 1"); | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:593` | assign fl_giveup_w = fl_err_w && (fl_retry_r >= RETRY_MAX_P); | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:890` | if (fl_retry_r >= RETRY_MAX_P) begin | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:894` | fl_bo_r    <= RETRY_BACKOFF_CYC_P; | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:911` | if (fl_retry_r >= RETRY_MAX_P) begin | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:915` | fl_bo_r    <= RETRY_BACKOFF_CYC_P; | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:922` | //! RETRY_BACKOFF_CYC_P complete cycles from the err, holding | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:954` | assign restore_done_o  = done_r; | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:955` | assign restore_fail_o  = fail_r; | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:956` | assign restore_blank_o = done_r && !any_rec_r; | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `tb/adp_engine/tb_adp_top.sv:29` | input  wire                    entity_enable_i, | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/tb_adp_top.sv:116` | .entity_enable_i       (entity_enable_i), | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/pp_top/sim_main.cpp:773` | //! memory behind a live bridge); unlike dram_stuck_next it persists | rewritten or added by this lane (66267d9f); states the D3 contract |
| `tb/pp_top/sim_main.cpp:1067` | uint64_t nvm_marks = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1075` | uint8_t  nvm_mark_last = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1076` | uint64_t nvm_marks_cls6 = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1077` | uint64_t nvm_marks_cls7 = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1079` | //! the same vector as it stands now (nvm_unflushed_o, issue #90) | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1093` | long rs_done_owned = 0;   // cycles restore_done_o read 1 while owned | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1095` | long rs_pre_late = 0;     // ...of them, those at or after restore_done_o | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1228` | if (d->aecp_nvm_mark_o == 7) name_mark_cycle = t; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1229` | ++nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1230` | nvm_mark_last = d->aecp_nvm_mark_o; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1231` | if (d->aecp_nvm_mark_o == 6) ++nvm_marks_cls6; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1232` | if (d->aecp_nvm_mark_o == 7) ++nvm_marks_cls7; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1235` | nvm_unflushed_seen \|= d->nvm_unflushed_o; | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1254` | if (d->restore_done_o && !rs_done) { rs_done = true; ++rs_dones; } | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1255` | if (rs_on && !d->restore_busy_o && !d->restore_done_o) ++rs_hole; | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1256` | if (d->restore_done_o && owned) ++rs_done_owned; | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1680` | d->entity_enable_i = 0; d->link_up_i = 0; d->gm_change_i = 0; | harness drive of the requested enable, or a comment on software load order (updated) |
| `tb/pp_top/sim_main.cpp:1726` | nvm_marks = 0; notify_enqs = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1728` | nvm_marks_cls6 = 0; nvm_marks_cls7 = 0; nvm_mark_last = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3903` | // R21: THE EXPORT (issue #90). aecp_nvm_stb_o / aecp_nvm_mark_o carry the | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3904` | // uCPU's OP_NVM_MARK effect out of the top, and the mark is the micro-op | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3907` | // persistence trigger: the saved-state contract's map and name stages | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/sim_main.cpp:3916` | const uint64_t m0 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3917` | const uint64_t c6_0 = h.nvm_marks_cls6; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3921` | CHECK(h.nvm_marks == m0 + 1 && h.nvm_marks_cls6 == c6_0 + 1 | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3922` | && h.nvm_mark_last == 6, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3925` | static_cast<unsigned>(h.nvm_marks - m0), | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3926` | static_cast<unsigned>(h.nvm_mark_last)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3929` | const uint64_t m1 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3932` | CHECK(h.nvm_marks == m1, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3934` | static_cast<unsigned>(h.nvm_marks - m1)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3940` | const uint64_t m2 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3941` | const uint64_t c7_0 = h.nvm_marks_cls7; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3946` | CHECK(h.nvm_marks == m2 + 1 && h.nvm_marks_cls7 == c7_0 + 1 | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3947` | && h.nvm_mark_last == 7, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3950` | static_cast<unsigned>(h.nvm_marks - m2), | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3951` | static_cast<unsigned>(h.nvm_mark_last)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:4622` | //! ...and the PERSISTENT flag changes nothing (the blanket refusal) | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:4628` | "L1b: PERSISTENT ACQUIRE refused the same way"); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:6815` | // or notified" has no wire shape at all: an NVM_MARK and a NOTIFY_ENQ | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6819` | // WRITE_ST that KL_aecp_dyn_state took), the OP_NVM_MARK strobe | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6820` | // (aecp_nvm_stb_o, counted in H::step as nvm_marks) and the | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6850` | const uint64_t m0 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6854` | const uint64_t mb = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6869` | CHECK(h.nvm_marks == mb, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6870` | "W10j5: the refusal of %u raised OP_NVM_MARK %u times, want 0", | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6871` | bad, static_cast<unsigned>(h.nvm_marks - mb)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6906` | CHECK(h.nvm_marks == m0 + 1, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6907` | "W10j11: the accepted SET raised OP_NVM_MARK %u times, want 1", | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6908` | static_cast<unsigned>(h.nvm_marks - m0)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7761` | // OP_NVM_MARK and OP_NOTIFY_ENQ strobes, and a second controller | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7787` | const uint64_t m0 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7792` | const uint64_t mb = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7806` | CHECK(h.nvm_marks == mb, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7807` | "W9k5: the refusal of 0x%08X raised OP_NVM_MARK %u times, " | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7808` | "want 0", bad, static_cast<unsigned>(h.nvm_marks - mb)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7831` | CHECK(h.nvm_marks == m0 + 1, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7832` | "W9k11: the accepted SET raised OP_NVM_MARK %u times, want 1", | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7833` | static_cast<unsigned>(h.nvm_marks - m0)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7913` | const uint64_t m0 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7924` | CHECK(d->dbg_dyn_writes_o == w0 && h.nvm_marks == m0 | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7928` | static_cast<unsigned>(h.nvm_marks - m0), | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:8462` | // The claim needs no entity_enable: addresses are owned before the | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:8521` | d2->entity_enable_i = 1; | harness drive of the requested enable, or a comment on software load order (updated) |
| `tb/pp_top/sim_main.cpp:8789` | entity_enable_adpdu_window_and_cadence(); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:8915` | //! top's restore_done_o now follows that terminal by the listener | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:8920` | CHECK(d->restore_fail_o == 0, "R: no restore_fail on a blank device"); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:8943` | CHECK(d->restore_done_o == 1 && d->restore_busy_o == 0, | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:8944` | "S0: restore_done_o has followed both walks' terminals (issue #92, D3)"); | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9006` | void entity_enable_adpdu_window_and_cadence() { | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9009` | d->entity_enable_i = 1; | harness drive of the requested enable, or a comment on software load order (updated) |
| `tb/pp_top/sim_main.cpp:9243` | h.run_ms(700);                       // > T-NVM-DEBOUNCE at 1 ms ticks | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9266` | //! this vector ORed with d3_unflushed_o (D3S2), so the port has to carry the | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9272` | "S9: nvm_unflushed_o[0] rose while the binding was unflushed " | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9274` | CHECK(d->nvm_unflushed_o == 0, | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9275` | "S9: nvm_unflushed_o clears on the commit's done (reads 0x%02x)", | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9276` | d->nvm_unflushed_o); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9334` | while (!d->restore_done_o && guard--) h.step(); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9335` | return d->restore_done_o != 0; | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9361` | // left to persist | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9372` | h.run_ms(1500);                      // T-NVM-DEBOUNCE, then the burst | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9386` | CHECK(h.q_acmp.empty() && !d->restore_busy_o && !d->restore_done_o, | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9397` | && !d->restore_done_o, | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9400` | while (!d->restore_done_o && guard--) h.step(); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9429` | // read the arbiter drains it; a later BIND then persists, and the next | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9449` | CHECK(d->dbg_walk_done_o && d->restore_fail_o && d->restore_cause_o == 3 | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9450` | && d->entity_enable_i == 0 && waited < BW_TMO + 200 | harness drive of the requested enable, or a comment on software load order (updated) |
| `tb/pp_top/sim_main.cpp:9459` | && d->entity_enable_i == 0 && !d->restore_done_o, | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9465` | while (!d->restore_done_o && waited2 < 4 * BW_TMO) { h.step(); ++waited2; } | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9466` | CHECK(d->restore_done_o && d->restore_fail_o && d->rs_cause_o == 3 | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9467` | && !d->restore_closed_o && !d->restore_blank_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9510` | CHECK(bw_boot() && !d->restore_fail_o, "BW3: the next walk ends clean"); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9519` | // BW4 (issue #93 S4): the top's restore_done_o waits for the binding walk's | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9535` | CHECK(bw_boot() && !d->restore_fail_o, | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9545` | "BW4: %ld walks, each ended with restore_done_o, the walk's terminal " | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9548` | "BW4: restore_busy_o or restore_done_o read 1 in every cycle from " | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9551` | "BW4: restore_done_o never read 1 while the admission gate still " | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9555` | "before its restore_done_o (%ld of %ld after it)", h.rs_pre_late, | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9759` | const auto marks = h.nvm_marks_cls7; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:9767` | CHECK(h.nvm_marks_cls7 == marks + (changed ? 1 : 0), | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:9861` | const auto marks = h.nvm_marks_cls7; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:9877` | CHECK(h.nvm_marks_cls7 == marks, "NW ABORT: no group-7 completion mark"); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:9917` | h.d->entity_enable_i = 1; | harness drive of the requested enable, or a comment on software load order (updated) |
| `docs/diagrams/01-system-context.svg:3` | <svg xmlns="http://www.w3.org/2000/svg" style="background: transparent; background-color:  | F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two producers; draw.io cannot export headless here (diagrams README), so source and export stay paired |
| `docs/diagrams/01-top-level.svg:3` | <svg xmlns="http://www.w3.org/2000/svg" style="background: transparent; background-color:  | F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two producers; draw.io cannot export headless here (diagrams README), so source and export stay paired |

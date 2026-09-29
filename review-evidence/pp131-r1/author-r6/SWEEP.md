# Section 15.2 contract sweep: statement-by-statement reconciliation

Processor head `9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f`; lane range `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3..HEAD`.
The contract's named search over `docs hdl tb` returned 705 matching lines (multiline, case-insensitive). 358 of them were rewritten or added by this lane; every other one carries its location-specific scope reason. Unreviewed: 0.

| Location | Matching text | Disposition |
|---|---|---|
| `tb/side_port/side_port_tb_wrap.sv:27` | input  wire          entity_enable_i, | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/side_port_tb_wrap.sv:127` | .entity_enable_i(entity_enable_i), | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/side_port_tb_wrap.sv:193` | .entity_enable_i(entity_enable_i), | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/acmp_talker/retry_cases.hpp:167` | // the retry's own response. Persistent silence saturates stale credits | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `tb/tx_slots/README.md:25` | a stalled byte and its ser_last must persist unchanged, the stream stalls and | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `tb/acmp_talker/retry_mutants.py:273` | "accept_kill_no_disable": "An accept-edge disable sets OFF, which persists and " | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `tb/side_port/sim_main.cpp:234` | dut->entity_enable_i = 0; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/sim_main.cpp:313` | dut->entity_enable_i = 0; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/sim_main.cpp:321` | dut->entity_enable_i = 1; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/side_port/sim_main.cpp:330` | dut->entity_enable_i = 0; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
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
| `tb/adp_engine/sim_main.cpp:403` | d->entity_enable_i = 0;       d->link_up_i = 0; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/sim_main.cpp:426` | d->entity_enable_i = 1; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/sim_main.cpp:601` | d->entity_enable_i = 0; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/sim_main.cpp:616` | d->entity_enable_i = 1; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/sim_main.cpp:651` | d->entity_enable_i = 0;                    // departing | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/sim_main.cpp:656` | d->entity_enable_i = 1; | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `hdl/adp/KL_adp_engine.sv:16` | //                    entity_enable_i — Milan §5.6.1 boot gate); | module-internal use of its entity_enable_i input, which the top drives with the effective enable (port comment updated) |
| `hdl/adp/KL_adp_engine.sv:101` | //! drives it with the effective enable: requested AND restore_done_o | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/adp/KL_adp_engine.sv:102` | input  wire                        entity_enable_i, | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/adp/KL_adp_engine.sv:244` | assign enable_rise_w = entity_enable_i && !enable_q_r; | module-internal use of its entity_enable_i input, which the top drives with the effective enable (port comment updated) |
| `hdl/adp/KL_adp_engine.sv:245` | assign enable_fall_w = !entity_enable_i && enable_q_r; | module-internal use of its entity_enable_i input, which the top drives with the effective enable (port comment updated) |
| `hdl/adp/KL_adp_engine.sv:256` | enable_q_r <= entity_enable_i; | module-internal use of its entity_enable_i input, which the top drives with the effective enable (port comment updated) |
| `hdl/adp/KL_adp_engine.sv:657` | if (entity_enable_i && !enable_fall_w | module-internal use of its entity_enable_i input, which the top drives with the effective enable (port comment updated) |
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
| `hdl/aecp/KL_aecp_dyn_state.sv:47` | //                PERSISTENCE: a saved-state restore has to write these rows, | design rationale: the D3 restore writes these rows with their valid flags; still true |
| `hdl/aecp/KL_aecp_dyn_state.sv:67` | //                (the µprogram does), and it does not persist anything. The | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_dyn_state.sv:68` | //                D3 writer (KL_aecp_nvm_writer) persists selectors 0 to 5 one | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_dyn_state.sv:130` | //! DIAGNOSTIC, sticky: a persisted row was written; no manager reads it | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_dyn_state.sv:132` | //! one cycle, with an accepted write that CHANGES a persisted row's | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_dyn_state.sv:324` | //! cycle" EXCEPT the IDENTIFY value, so only the persisted set marks | the diagnostic dirty (port comment marks it so); IDENTIFY excluded |
| `tb/adp_engine/tb_adp_top.sv:29` | input  wire                    entity_enable_i, | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/adp_engine/tb_adp_top.sv:116` | .entity_enable_i       (entity_enable_i), | module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1 |
| `tb/acmp_talker/README.md:93` | the teardown itself is never delayed by it (WITHDRAW_TALKER, timer cancel | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `tb/acmp_talker/README.md:300` | - `accept_kill_no_disable`: An accept-edge disable sets OFF, which persists and latches th | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `docs/architecture/04_adp_engine.md:98` | \| AEM_PERSISTENT_ACQUIRE_SUPPORTED \| 0x00002000 \| 0 \| | unrelated capability flag (AEM_PERSISTENT_ACQUIRE_SUPPORTED) |
| `docs/architecture/04_adp_engine.md:159` | \| Held in DOWN until `entity_enable` (boot gate) \| Milan §5.6.1. The engine's `entity_en | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:270` | //                its done with the binding walk's end into restore_done_o, | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:273` | //                persistence work. | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:309` | //! T-NVM-RS-DEADLINE (F08.1), P-NVM-RS-TMO-CYC (F01.5): the D3 restore's | rewritten or added by this lane (66267d9f); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:312` | //! T-NVM-RS-AGGREGATE (F08.1), P-NVM-RS-AGG-CYC (F01.5), DR3a: the D3 | rewritten or added by this lane (380a3e47); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:318` | parameter int unsigned NVM_RETRY_BACKOFF_CYC_P = 50_000_000, | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:610` | output logic        d3_unflushed_o, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:614` | //! select no record; the D3 writer persists from the accepted change ---- | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:616` | output logic  [7:0] eff_nvm_mark_o, | the completion-mark export and its wiring; export comment rewritten |
| `hdl/aecp/KL_aecp_engine.sv:659` | //! DIAGNOSTIC: some persisted row was written since reset (sticky); | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:660` | //! not pending and not a persistence trigger (d3_unflushed_o is) | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:1698` | .eff_nvm_mark_o     (eff_nvm_mark_o), | the completion-mark export and its wiring; export comment rewritten |
| `hdl/aecp/KL_aecp_engine.sv:1843` | .RETRY_BACKOFF_CYC_P (NVM_RETRY_BACKOFF_CYC_P) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_engine.sv:1895` | .unflushed_o (d3_unflushed_o), | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `docs/architecture/05_acmp_engine.md:16` | \| Binding persistence via NVM \| honoring STREAMING_WAIT on outputs (Δ14) \| | scope/delta table rows naming binding persistence; still true |
| `docs/architecture/05_acmp_engine.md:160` | \| The faces are **released once**, when the binding walk has drained. \| the shadow's own | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/05_acmp_engine.md:161` | \| The release is **the binding walk's end**, not the restore's. \| the release starts the | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/05_acmp_engine.md:186` | is bounded by `T-NVM-RS-DEADLINE`: a device that stops answering fails the whole walk at | the binding walk's own read deadline and listener release; raw facts of that walk, still true |
| `docs/architecture/05_acmp_engine.md:189` | are released and the listener answers, so persistence that wedges never holds ACMP | the binding walk's own read deadline and listener release; raw facts of that walk, still true |
| `docs/architecture/05_acmp_engine.md:207` | [`tb/pp_top`](../../tb/pp_top/README.md) (section BW; BW4 grades `restore_done_o` and | suite pointer; the sentence now adds the D3 grading |
| `docs/architecture/05_acmp_engine.md:576` | Δ14 (STREAMING_WAIT outputs) · Δ15 (listener SM + persistent binding) — master table | scope/delta table rows naming binding persistence; still true |
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
| `hdl/aecp/ucpu_pkg.sv:79` | OP_NVM_MARK   = 5'd22, | the NVM_MARK micro-op and its completion strobe, retained (15.2: mark instructions stay valid) |
| `hdl/acmp/KL_pp_acmp_lsn_admit.sv:59` | //                binding manager's walk at its terminal (restore_done_o, | the gate's input is the binding manager's raw terminal; release paragraph updated |
| `hdl/acmp/KL_pp_acmp_lsn_admit.sv:65` | //                on it, and the top's restore_done_o (both walks; it releases | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/acmp/KL_pp_acmp_lsn_admit.sv:95` | input  wire                 walk_done_i,     //! KL_acmp_nvm_shadow restore_done_o | the gate's input is the binding manager's raw terminal; release paragraph updated |
| `tb/ucpu/README.md:32` | chain (state write-back strobes, COMMIT, NVM_MARK, NOTIFY_ENQ — and their | grades the NVM_MARK completion strobe itself; retained |
| `hdl/aecp/KL_aecp_ucpu.sv:106` | output logic  [7:0] eff_nvm_mark_o, | the NVM_MARK micro-op and its completion strobe, retained (15.2: mark instructions stay valid) |
| `hdl/aecp/KL_aecp_ucpu.sv:435` | eff_nvm_stb_o      = advance_e_w && (uop_e_r.op == OP_NVM_MARK); | the NVM_MARK micro-op and its completion strobe, retained (15.2: mark instructions stay valid) |
| `hdl/aecp/KL_aecp_ucpu.sv:436` | eff_nvm_mark_o     = uop_e_r.imm[7:0]; | the NVM_MARK micro-op and its completion strobe, retained (15.2: mark instructions stay valid) |
| `docs/architecture/01_overview.md:9` | Vendor Unique execution, unsolicited notifications, counters, and persistence. | scope statements; still true |
| `docs/architecture/01_overview.md:39` | \| Timers/deadlines, PRNG, persistence orchestration \| AVTP streaming datapath, CBS shapi | scope statements; still true |
| `docs/architecture/01_overview.md:111` | engine's enable is the requested `entity_enable` AND `restore_done_o` (both walks) | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/01_overview.md:143` | \| Δ15 \| Listener behavior = Milan 8-state binding/probing SM; binding persists across po | scope statements; still true |
| `docs/architecture/01_overview.md:176` | \| P-NVM-RS-TMO-CYC \| ceil(P-CLK-HZ / 50) (20 ms) \| above the slowest single record read | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/architecture/01_overview.md:177` | \| P-NVM-RS-AGG-CYC \| P-CLK-HZ (1,000 ms) \| DR3a **ratified** as an enforced bound (`NVM | rewritten or added by this lane (f8d1a83e); states the D3 contract |
| `docs/architecture/01_overview.md:178` | \| P-NVM-RETRY-BACKOFF-CYC \| ceil(P-CLK-HZ / 2) (500 ms) \| DR2c ruled value: `(CLK_HZ_P  | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `docs/architecture/01_overview.md:179` | \| P-NVM-DEB-TICKS \| 500 ticks of `tick_ms` (500 ms) \| DR2a ruled value; a module parame | rewritten or added by this lane (2b38d68e); states the D3 contract |
| `docs/architecture/01_overview.md:180` | \| P-NVM-RETRY-MAX \| 2 additional retries = 3 attempts \| DR2c ruled value; a module para | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/08_timing.md:43` | \| T-NVM-DEBOUNCE \| 500 ms: 500 ticks of the 1 ms `tick_ms` (`DEB_TICKS_P` in the binding | rewritten or added by this lane (2b38d68e); states the D3 contract |
| `docs/architecture/08_timing.md:44` | \| T-NVM-RS-DEADLINE \| `P-NVM-RS-TMO-CYC` clocks without progress (20 ms, ceil(`P-CLK-HZ` | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/architecture/08_timing.md:45` | \| T-NVM-RS-AGGREGATE \| `P-NVM-RS-AGG-CYC` clocks from the accepted restore start (1,000  | rewritten or added by this lane (84572585); states the D3 contract |
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
| `hdl/srp/KL_srp_listener_fsm.sv:346` | logic [N_SINKS_P-1:0]        rec_valid_r;   // record latched (persists past A8) | unrelated sense: a latched SRP record persists |
| `docs/architecture/09_verification.md:56` | \| **NVM** \| power-cut/restore: cut at randomized commit points, verify CRC fallback + re | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/09_verification.md:162` | Reset and persistence semantics: dyn_state A (everything invalid out of reset), | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/09_verification.md:163` | E (the diagnostic dirty marks the persisted set, and only it) and H (the change | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/09_verification.md:190` | \| the aggregate is inert after COMPLETE, DEFAULTS and CLOSED, and never fires with an eve | rewritten or added by this lane (e94bea85); states the D3 contract |
| `docs/architecture/09_verification.md:191` | \| an abort presented in the arbiter's issue cycle arms the drain, for either manager: the | rewritten or added by this lane (014e679c); states the D3 contract |
| `hdl/aecp/KL_aecp_desc_store.sv:41` | //                The names are not persisted yet: the saved-state contract's | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/pp_top_wrap.sv:52` | input  wire         entity_enable_i, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:174` | output logic        restore_done_o, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:175` | output logic        restore_fail_o, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:176` | output logic        restore_blank_o, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:182` | output logic  [7:0] nvm_unflushed_o, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:183` | output logic        d3_unflushed_o, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/pp_top_wrap.sv:269` | //! the binding manager's OWN terminal (KL_acmp_nvm_shadow restore_done_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:270` | //! which the top's restore_done_o follows once the listener admission | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:276` | //! restore_done_o and restore_busy_o against them every cycle | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:339` | //! OP_NVM_MARK strobe and the OP_NOTIFY_ENQ strobe (06 section 8). The | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:344` | output logic  [7:0] aecp_nvm_mark_o, | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:459` | //! NVM_RS_TMO_CYC_P, NVM_RS_AGG_CYC_P and NVM_RETRY_BACKOFF_CYC_P are | rewritten or added by this lane (b06130d8); states the D3 contract |
| `tb/pp_top/pp_top_wrap.sv:477` | .entity_enable_i       (entity_enable_i), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:521` | .aecp_dyn_dirty_o      (), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:524` | .aecp_nvm_mark_o       (aecp_nvm_mark_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:592` | .restore_done_o        (restore_done_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:593` | .restore_fail_o        (restore_fail_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:594` | .restore_blank_o       (restore_blank_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:600` | .nvm_unflushed_o       (nvm_unflushed_o), | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/pp_top_wrap.sv:601` | .d3_unflushed_o        (d3_unflushed_o), | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/pp_top_wrap.sv:725` | assign dbg_adp_enable_o = u_dut.u_adp.entity_enable_i; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/prng/sim_main.cpp:229` | CHECK(dut->dbg_seeded_o == 1, "D: seeded flag persists"); | unrelated sense of 'persist' (a flag, a byte or a kill persists) |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:10` | //                manager face; 08 §2 T-NVM-DEBOUNCE) | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:12` | //  Description : The per-sink ACMP binding persistence shadow of 05 §5 — | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:19` | //                each written F07.6 record onto the persisted field set | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:31` | //                (T-NVM-DEBOUNCE via tick_i, F07.9 coalescing) and bounded | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:32` | //                by DR2c: at most 1 + RETRY_MAX_P = 3 attempts per record, | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:33` | //                each failed one followed by RETRY_BACKOFF_CYC_P cycles | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:38` | //                A DIRECT INSTANTIATOR DERIVES ITS CLOCK. RETRY_BACKOFF_CYC_P | rewritten or added by this lane (84572585); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:42` | //                its CLK_HZ_P (NVM_RETRY_BACKOFF_CYC_P = ceil(CLK_HZ_P / 2), | rewritten or added by this lane (84572585); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:48` | //                RAW VERDICTS. restore_done_o/fail_o/blank_o/cause_o are | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:56` | //                and only a DIFFERING persisted field marks dirty — so | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:73` | //                aborts the WHOLE restore: restore_fail_o, no preload is | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:103` | //  Blank arm   : restore_done_o is SEQUENCING, not a verdict. Every | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:110` | //                did not), so restore_blank_o carries it: it is done AND no | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:131` | //! shipped firmware persisted carries started = 0 - and started = 0 now | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:138` | //! T-NVM-DEBOUNCE in tick_i units (F08.1: 500 ms at a 1 ms tick, DR2a) | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:139` | parameter int unsigned DEB_TICKS_P   = 500, | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:142` | parameter int unsigned RETRY_MAX_P   = 2, | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:147` | parameter int unsigned RETRY_BACKOFF_CYC_P = 50_000_000, | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:148` | //! T-NVM-RS-DEADLINE (F08.1) in clocks: the restore walk's read phase | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:169` | output logic                       restore_done_o, //! level: restore sequencing complete | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:170` | output logic                       restore_fail_o, //! level: the WHOLE restore aborted, a | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:171` | output logic                       restore_blank_o,//! level: the completed walk validated | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:172` | //! level, with restore_fail_o: why the walk failed. 0 it did not, 1 a | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:232` | // ---- the persisted projection (05 §5 NVM shadow field set) ------------- | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:427` | // ---- debounce (T-NVM-DEBOUNCE, F07.9 coalescing) ------------------------ | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:440` | deb_cnt_r  <= DEB_TICKS_P; | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:537` | if (RETRY_BACKOFF_CYC_P < 1) begin : g_backoff_check | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:538` | $error("KL_acmp_nvm_shadow: RETRY_BACKOFF_CYC_P must be at least 1"); | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:621` | assign fl_giveup_w = fl_err_w && (fl_retry_r >= RETRY_MAX_P); | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:918` | if (fl_retry_r >= RETRY_MAX_P) begin | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:922` | fl_bo_r    <= RETRY_BACKOFF_CYC_P; | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:939` | if (fl_retry_r >= RETRY_MAX_P) begin | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:943` | fl_bo_r    <= RETRY_BACKOFF_CYC_P; | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:950` | //! RETRY_BACKOFF_CYC_P complete cycles from the err, holding | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:982` | assign restore_done_o  = done_r; | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:983` | assign restore_fail_o  = fail_r; | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
| `hdl/acmp/KL_acmp_nvm_shadow.sv:984` | assign restore_blank_o = done_r && !any_rec_r; | raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines |
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
| `docs/architecture/07_memory_maps.md:615` | \| is still reading when the restore's aggregate deadline fires (`T-NVM-RS-AGGREGATE`, bel | rewritten or added by this lane (014e679c); states the D3 contract |
| `docs/architecture/07_memory_maps.md:622` | no record, a failed one included; the top's combined `restore_blank_o` never does (below). | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:652` | restore by a second count: `P-NVM-RS-AGG-CYC` clocks (1,000 ms, `T-NVM-RS-AGGREGATE`) | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/architecture/07_memory_maps.md:690` | \| `restore_done_o` \| the drained binding terminal AND the D3 walk's done (COMPLETE or DE | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:692` | \| `restore_fail_o` \| either walk failed \| | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:693` | \| `restore_blank_o` \| done, **not failed**, and neither walk validated a record: a faile | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:703` | persistence is a design decision (Milan silent), retained by the parent D3 contract | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:704` | (§16, "design-affirmative"). The earlier system_unique_id and MCR persistence plans are | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:715` | (`T-NVM-DEBOUNCE`, 500 ms), draining one burst; only a proven unchanged | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/architecture/07_memory_maps.md:729` | \| 0x30000–0x300FF \| RW \| control/status: entity_enable, boot state, NVM alarm, version/ | side-port access rules keyed to the requested enable; unchanged |
| `docs/architecture/07_memory_maps.md:745` | accesses — a write to a read-only window, an image write after `entity_enable`, or any | side-port access rules keyed to the requested enable; unchanged |
| `tb/acmp_nvm/sim_main.cpp:2` | // KL_acmp_nvm_shadow suite — persistence shadow against an INDEPENDENT | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:16` | // Proven: debounce coalescing (N changes in one T-NVM-DEBOUNCE window -> | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:55` | constexpr int DEB_TICKS = 50;      // -GDEB_TICKS_P | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:56` | //! DR2c: cycles a failed attempt waits before the next (-GRETRY_BACKOFF_CYC_P) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/sim_main.cpp:142` | // build an F07.6 image: the persisted set from b, volatile fields = junk | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:241` | //! The persistence shadow, the physical-NVM device model, the monitors and | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:422` | long done_cyc = -1;              // restore_done_o first seen | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:747` | if (d->restore_done_o && done_cyc < 0) done_cyc = cycles; | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:901` | bool restore_done() { return d->restore_done_o != 0; } | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:978` | CHECK(!d->restore_fail_o && d->restore_cause_o == 0, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:984` | // cannot tell the two apart. restore_blank_o is the pin that can. | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:985` | CHECK(d->restore_blank_o, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1006` | "B3 burst released after T-NVM-DEBOUNCE"); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1022` | inject(2, b2b, 0x77);                        // same persisted set, new junk | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1096` | "E9 DR2c timing: each retry starts RETRY_BACKOFF_CYC_P cycles or more " | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/sim_main.cpp:1156` | CHECK(!d->restore_fail_o && d->restore_cause_o == 0, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1162` | CHECK(!d->restore_blank_o, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1210` | CHECK(d->restore_fail_o && d->restore_cause_o == 1, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1219` | CHECK(d->restore_blank_o, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1260` | CHECK(!d->restore_fail_o, "H3 live changes are not a failure"); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1307` | // protocol_processor_top publishes this vector as nvm_unflushed_o (issue | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1308` | // #90) and an integrator ORs it with d3_unflushed_o into a "saved state | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/acmp_nvm/sim_main.cpp:1311` | // cycle: it rises when a change is ACCEPTED (a capture whose persisted set | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1456` | if (!d->restore_done_o \|\| d->restore_fail_o) bad("the walk is not done, or failed"); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1545` | return d->restore_done_o && !d->pre_valid_o && !d->lsn_busy_o | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1885` | // change still lands once, after the second walk, and persists | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:1899` | "%s: answered once and persisted after the second walk", tag); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2093` | if (!d->restore_done_o \|\| !d->restore_fail_o \|\| d->restore_cause_o != cause) { | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2095` | unsigned(d->restore_done_o), unsigned(d->restore_fail_o), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2101` | if (!d->restore_blank_o) bad("a failed walk reports records it discarded"); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2168` | CHECK(!d->restore_fail_o && d->restore_cause_o == 0 && !d->restore_blank_o | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2191` | // commands are served on defaults; persistence is not | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2254` | && !d->restore_fail_o, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2260` | // persists once the device ended the read | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2285` | "%s: the later change persists and the saved records stay", tag); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2323` | "%s: the change then persists and the saved records stay", tag); | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2366` | const bool walk = l_walk_ok(why) && !d->restore_fail_o && d->restore_cause_o == 0 | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2404` | CHECK(wd_max == RS_TMO - 1 && aborts == 0 && !d->restore_fail_o | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2513` | // full restore, which is why restore_blank_o exists. | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2558` | CHECK(d->restore_done_o && !d->restore_fail_o && d->restore_cause_o == 0 | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2559` | && d->restore_blank_o && !pre_valid_seen && d->dbg_valid_o == 0 | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/sim_main.cpp:2601` | CHECK(l_walk_ok(why) && !d->restore_fail_o && d->restore_cause_o == 0 | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/acmp_nvm/sim_main.cpp:2667` | const bool walk = l_walk_ok(why) && !d->restore_fail_o && d->restore_cause_o == 0; | rewritten or added by this lane (9dce84ea); states the D3 contract |
| `tb/acmp_nvm/sim_main.cpp:2712` | const bool walk = l_walk_ok(why) && !d->restore_fail_o && d->restore_cause_o == 0; | rewritten or added by this lane (9b4da6b5); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:9` | //                02 §8 F02.8 class-F manager face; 08 §2 T-NVM-DEBOUNCE; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:97` | //                THE RECORDS (scalar stage). One record per persisted | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:112` | //                µCPU's accepted state-bus write to a persisted row that | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:129` | //                (T-NVM-DEBOUNCE). Its close arms one burst that drains | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:132` | //                DR2c (parent D3 §6.1): at most 1 + RETRY_MAX_P = 3 attempts | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:135` | //                BACKOFF waits RETRY_BACKOFF_CYC_P complete clk_i cycles | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:172` | //! T-NVM-DEBOUNCE in ms, counted on tick_i, the 1 ms tick (F08.1: 500 | rewritten or added by this lane (2b38d68e); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:173` | //! ms; the binding manager's DEB_TICKS_P is the same count) | rewritten or added by this lane (2b38d68e); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:176` | parameter int unsigned RETRY_MAX_P    = 2, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:180` | parameter int unsigned RETRY_BACKOFF_CYC_P = 50_000_000, | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:181` | //! T-NVM-RS-DEADLINE (F08.1), P-NVM-RS-TMO-CYC (F01.5): clocks a restore | rewritten or added by this lane (66267d9f); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:184` | //! T-NVM-RS-AGGREGATE (F08.1), P-NVM-RS-AGG-CYC (F01.5), DR3a: clock | rewritten or added by this lane (380a3e47); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:292` | if (RETRY_BACKOFF_CYC_P < 1) begin : g_backoff_check | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:293` | $error("KL_aecp_nvm_writer: RETRY_BACKOFF_CYC_P must be at least 1"); | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:866` | S_BACKOFF   // DR2c: RETRY_BACKOFF_CYC_P cycles from a failed attempt | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:957` | assign giveup_w    = write_err_w && (attempts_r >= 32'(1 + RETRY_MAX_P)); | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/aecp/KL_aecp_nvm_writer.sv:1048` | bo_cnt_r <= RETRY_BACKOFF_CYC_P; | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `docs/10_RESOURCE_AND_EFFORT.md:165` | store, dynamic-field mux, lock, timers, persistence, patch — costs ≈ 417 ± 208 LUT | historical estimate of the earlier front end; not a contract; D3 area is the packet's DR4 |
| `docs/10_RESOURCE_AND_EFFORT.md:298` | persistence (the ≈ 417-LUT front end), keep its ADP and ACMP engines, and point this | historical estimate of the earlier front end; not a contract; D3 area is the packet's DR4 |
| `tb/dyn_state/sim_main.cpp:89` | void mark_dirty_only_for_persisted_fields(); | diagnostic dirty (section E) and the change qualifier (section H); section E title updated |
| `tb/dyn_state/sim_main.cpp:231` | // ---- E: the diagnostic dirty marks the persisted set, and only it ----- | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/dyn_state/sim_main.cpp:235` | void DynStateHarness::mark_dirty_only_for_persisted_fields() { | diagnostic dirty (section E) and the change qualifier (section H); section E title updated |
| `tb/dyn_state/sim_main.cpp:246` | "E: a persisted clock-source write did NOT mark the store dirty"); | diagnostic dirty (section E) and the change qualifier (section H); section E title updated |
| `tb/dyn_state/sim_main.cpp:356` | // `wr_chg_o` marks an accepted write that changes a persisted row's | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/dyn_state/sim_main.cpp:389` | "H: IDENTIFY is never a persisted change"); | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/dyn_state/sim_main.cpp:407` | mark_dirty_only_for_persisted_fields(); | diagnostic dirty (section E) and the change qualifier (section H); section E title updated |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:52` | parameter int unsigned  DEB_TICKS_P   = 500, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:53` | parameter int unsigned  RETRY_MAX_P   = 2, | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:55` | parameter int unsigned  RETRY_BACKOFF_CYC_P = 600, | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:66` | output logic                     restore_done_o,  //! restore complete level | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:67` | output logic                     restore_fail_o,  //! whole-restore abort level | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:68` | output logic                     restore_blank_o, //! completed walk validated ZERO record | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:256` | .DEB_TICKS_P  (DEB_TICKS_P), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:257` | .RETRY_MAX_P  (RETRY_MAX_P), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:259` | .RETRY_BACKOFF_CYC_P (RETRY_BACKOFF_CYC_P) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:268` | .restore_done_o  (restore_done_o), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:269` | .restore_fail_o  (restore_fail_o), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:270` | .restore_blank_o (restore_blank_o), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:412` | .walk_done_i    (restore_done_o), | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `hdl/top/protocol_processor_top.sv:128` | //! T-NVM-RS-DEADLINE (F08.1), P-NVM-RS-TMO-CYC (F01.5): each restore | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:138` | //! T-NVM-RS-AGGREGATE (F08.1), P-NVM-RS-AGG-CYC (F01.5): the restore | rewritten or added by this lane (f8d1a83e); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:151` | parameter int unsigned NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2), | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:216` | //! restore_done_o; the side port's image-window lock sees it as is | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:217` | input  wire         entity_enable_i, | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:457` | output logic        restore_done_o, | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:468` | output logic        restore_fail_o, | declaration under its rewritten combined-verdict comment |
| `hdl/top/protocol_processor_top.sv:473` | output logic        restore_blank_o, | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:482` | //! restore_done_o and restore_fail_o). Completed bindings stay restored. | rewritten or added by this lane (505524e5); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:484` | //! the D3 walk's first abort cause, valid with restore_fail_o: 0 none, | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:497` | //! Bit k rises on the cycle the manager ACCEPTS a changed persisted set | the binding manager's own pending vector, raw by design; the OR with d3_unflushed_o is stated |
| `hdl/top/protocol_processor_top.sv:500` | //! so a write-back that changes no persisted field never raises it — and | the binding manager's own pending vector, raw by design; the OR with d3_unflushed_o is stated |
| `hdl/top/protocol_processor_top.sv:505` | //! with d3_unflushed_o below (aecp_dyn_dirty_o stays a diagnostic); | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:508` | output logic [N_STREAM_IN_P-1:0] nvm_unflushed_o, | the binding manager's own pending vector, raw by design; the OR with d3_unflushed_o is stated |
| `hdl/top/protocol_processor_top.sv:511` | //! write that changed a persisted dynamic-state row (configuration, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:516` | output logic                     d3_unflushed_o, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:672` | //! Quasi-static (02 §2 rule 4: set before entity_enable, stable after). | MAAP quasi-static inputs set before the requested enable; unrelated to the restore |
| `hdl/top/protocol_processor_top.sv:709` | //! DIAGNOSTIC only: some persisted dynamic-state row was written since | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:710` | //! reset (sticky). Not pending and not a persistence trigger: the D3 | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:711` | //! writer's d3_unflushed_o above is the pending of these rows. | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:712` | output logic                         aecp_dyn_dirty_o, | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:722` | //! record group a committed command changed (KL_aecp_ucpu OP_NVM_MARK: | the completion-mark export (comment rewritten: completion only, no record selection) |
| `hdl/top/protocol_processor_top.sv:730` | //! changing write itself; groups 6 and 7 are the saved-state contract's | rewritten or added by this lane (39789f98); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:734` | output logic  [7:0]                  aecp_nvm_mark_o,     //! that group's mark code, vali | the completion-mark export (comment rewritten: completion only, no record selection) |
| `hdl/top/protocol_processor_top.sv:1703` | assign adp_enable_w = entity_enable_i && restore_done_o; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:1721` | //! ended (restore_done_o): no advertisement precedes a restore write. | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:1723` | .entity_enable_i       (adp_enable_w), | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:1852` | //! END, and restore_done_o below takes it. | the admission release is one term of the combined restore_done_o; true |
| `hdl/top/protocol_processor_top.sv:2560` | .RETRY_BACKOFF_CYC_P (NVM_RETRY_BACKOFF_CYC_P) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2568` | .restore_done_o   (nvm_walk_done_w), | wiring of the binding manager's raw verdicts and pending, or the diagnostic dirty, to their named nets |
| `hdl/top/protocol_processor_top.sv:2569` | .restore_fail_o   (nvm_walk_fail_w), | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2570` | .restore_blank_o  (nvm_walk_blank_w), | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2598` | .dbg_dirty_o      (nvm_unflushed_o), | wiring of the binding manager's raw verdicts and pending, or the diagnostic dirty, to their named nets |
| `hdl/top/protocol_processor_top.sv:2611` | assign restore_done_o   = nvm_walk_done_w && lsn_released_w && d3_done_w; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2613` | \|\| (nvm_walk_done_w && !restore_done_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2615` | assign restore_fail_o   = nvm_walk_fail_w \|\| d3_fail_w; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:2618` | assign restore_blank_o  = restore_done_o && !restore_fail_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:3498` | .NVM_RETRY_BACKOFF_CYC_P (NVM_RETRY_BACKOFF_CYC_P) | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:3648` | .d3_unflushed_o     (d3_unflushed_o), | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `hdl/top/protocol_processor_top.sv:3650` | .eff_nvm_mark_o     (aecp_nvm_mark_o), | the completion-mark export (comment rewritten: completion only, no record selection) |
| `hdl/top/protocol_processor_top.sv:3685` | .dyn_dirty_o        (aecp_dyn_dirty_o) | wiring of the binding manager's raw verdicts and pending, or the diagnostic dirty, to their named nets |
| `hdl/top/protocol_processor_top.sv:4381` | .entity_enable_i (entity_enable_i), | side-port lock and status words: the requested enable beside the combined verdicts (comments added) |
| `hdl/top/protocol_processor_top.sv:4453` | 8'd1:    sp_ctrl_rdata_r <= {28'd0, restore_fail_o, restore_done_o, | side-port lock and status words: the requested enable beside the combined verdicts (comments added) |
| `hdl/top/protocol_processor_top.sv:4454` | restore_busy_o, entity_enable_i}; | side-port lock and status words: the requested enable beside the combined verdicts (comments added) |
| `hdl/top/protocol_processor_top.sv:4465` | link_up_i, entity_enable_i}; | side-port lock and status words: the requested enable beside the combined verdicts (comments added) |
| `tb/acmp_nvm/Makefile:16` | -GDEB_TICKS_P=50 -GRS_TMO_CYC_P=3000 -GRETRY_BACKOFF_CYC_P=600 \ | rewritten or added by this lane (f72a2d2d); states the D3 contract |
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
| `tb/pp_top/gsi_internal.hpp:33` | while (!io.d->restore_done_o && budget-- != 0) io.step(); | boot helper waiting for the combined restore_done_o before its section |
| `tb/pp_top/gsi_internal.hpp:34` | CHECK(io.d->restore_done_o && !io.d->restore_fail_o, | boot helper waiting for the combined restore_done_o before its section |
| `tb/pp_top/gsi_internal.hpp:37` | io.d->entity_enable_i = 1; | boot helper waiting for the combined restore_done_o before its section |
| `hdl/packet_engine/KL_pp_nvm_port.sv:25` | //                asynchronous to protocol responses (03 §6 ordering rule d) | port-level fact: the device's commits stay asynchronous; 03 section 6 rule (d) now bounds the separate latch hold |
| `docs/guides/operator.md:80` | \| 0x00000 \| write before `entity_enable`, read \| reserved seam. **Reads 0x00000000** —  | side-port window rules and the requested enable's shutdown semantics; unchanged |
| `docs/guides/operator.md:88` | `entity_enable`, or an unmapped address — answers with the error flag one cycle later and | side-port rule keyed to the requested enable |
| `docs/guides/operator.md:107` | \| 3 \| 0 \| `entity_enable_i` \| | side-port window rules and the requested enable's shutdown semantics; unchanged |
| `docs/guides/operator.md:206` | \| 1 \| read only \| bit 0 `entity_enable_i` (the **requested** enable) · bit 1 restore bu | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/operator.md:233` | \| Situation \| Terminal \| Busy \| Done \| Failed \| Blank (`restore_blank_o`) \| | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/operator.md:284` | enable the machine sees is the **effective** one, `entity_enable_i` AND restore done; cont | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/operator.md:290` | - **deasserting `entity_enable_i`** is the shutdown — it emits ENTITY_DEPARTING and | side-port window rules and the requested enable's shutdown semantics; unchanged |
| `docs/guides/README.md:35` | \| [07 memory maps](../architecture/07_memory_maps.md) \| the entity model, records, the s | index entry pointing at 07 section 5, the updated authority |
| `tb/pp_top/d3_mutants.py:181` | (TOP, "  assign adp_enable_w = entity_enable_i && restore_done_o;\n", | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:182` | "  assign adp_enable_w = entity_enable_i;\n"),), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:185` | (TOP, "  assign restore_done_o   = nvm_walk_done_w && lsn_released_w && d3_done_w;\n", | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:186` | "  assign restore_done_o   = nvm_walk_done_w && lsn_released_w;\n"),), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:204` | ("D3R5: once the device ends the drained read a later SET persists",)), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:239` | (WRITER, "  assign giveup_w    = write_err_w && (attempts_r >= 32'(1 + RETRY_MAX_P));\n", | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:240` | "  assign giveup_w    = write_err_w && (attempts_r >= 32'(2 + RETRY_MAX_P));\n"),), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:252` | (SHADOW, "  assign fl_giveup_w = fl_err_w && (fl_retry_r >= RETRY_MAX_P);\n", | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:253` | "  assign fl_giveup_w = fl_err_w && (fl_retry_r >= RETRY_MAX_P + 1);\n"), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:254` | (SHADOW, "          if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P) begin | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:255` | "          if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P + 1) begin\n"), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:256` | (SHADOW, "end else if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P) begin\ | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:257` | "end else if (nvm_err_i) begin\n            if (fl_retry_r >= RETRY_MAX_P + 1) begin\n")), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:266` | (TOP, "NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2),", | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/d3_mutants.py:267` | "NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd200),"),), | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `docs/guides/integrator.md:90` | \| `NVM_RS_TMO_CYC_P` \| [F01.5](../architecture/01_overview.md#fig-01-params), `P-NVM-RS- | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/guides/integrator.md:91` | \| `NVM_RS_AGG_CYC_P` \| [F01.5](../architecture/01_overview.md#fig-01-params), `P-NVM-RS- | rewritten or added by this lane (84572585); states the D3 contract |
| `docs/guides/integrator.md:92` | \| `NVM_RETRY_BACKOFF_CYC_P` \| [F01.5](../architecture/01_overview.md#fig-01-params), `P- | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:213` | \| `DESC_BASE_P` \| your descriptor image, sized by your entity model \| **your software** | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:237` | them before `entity_enable_i` and leave them alone. The two dynamic rows are | quasi-static inputs set before the requested enable, or MAAP's unrelated persistence seed |
| `docs/guides/integrator.md:245` | \| Level controls \| `entity_enable_i`, `link_up_i` \| | quasi-static inputs set before the requested enable, or MAAP's unrelated persistence seed |
| `docs/guides/integrator.md:269` | `entity_enable_i` is the boot gate of Milan §5.6.1, as a **request**. The ADP engine's | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:270` | effective enable is `entity_enable_i && restore_done_o`: the processor releases your | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:312` | \| NVM device \| `nvm_dev_*`, plus `restore_go_i`, `restore_busy_o`, `restore_done_o`, `re | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:321` | `cfg_maap_internal_i` to 1 (quasi-static, set before `entity_enable_i`) | quasi-static inputs set before the requested enable, or MAAP's unrelated persistence seed |
| `docs/guides/integrator.md:325` | optionally a persistence seed (`cfg_maap_seed_offset_i` + `cfg_maap_seed_valid_i`), | quasi-static inputs set before the requested enable, or MAAP's unrelated persistence seed |
| `docs/guides/integrator.md:353` | \| `nvm_unflushed_o` \| per-sink binding state the binding manager has accepted and not ye | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:354` | \| `d3_unflushed_o` \| the D3 writer's pending: 1 while any scalar record (configuration,  | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:355` | \| `aecp_dyn_dirty_o` \| a sticky **diagnostic**: some dynamic-state row was written since | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:357` | \| `restore_done_o`, `restore_busy_o`, `restore_fail_o`, `restore_blank_o` \| the combined | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:360` | \| `aecp_nvm_stb_o`, `aecp_nvm_mark_o` \| one cycle per committed command that marked a re | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:386` | 3. Pulse `restore_go_i`, **on every boot**; wait for `restore_done_o` or | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:387` | `restore_closed_o`, then read `restore_fail_o` **and** `restore_blank_o`. Three | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:395` | - `restore_done_o` (both walks done) releases your requested enable to ADP. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:397` | `restore_done_o` says the walks sequenced, not that anything came back: every | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:398` | per-record default sets it. `restore_blank_o` separates a restore from walks over | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:400` | `restore_closed_o` without `restore_done_o` is CLOSED: AECP and ADP stay held until | rewritten or added by this lane (9d660959); states the D3 contract |
| `docs/guides/integrator.md:438` | `restore_done_o` or `restore_closed_o` cover 1,000 ms plus two per-wait deadlines | rewritten or added by this lane (84572585); states the D3 contract |
| `docs/guides/integrator.md:443` | 5. Assert `entity_enable_i` when you are ready; the processor forwards it to ADP only | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/integrator.md:444` | once `restore_done_o` is 1. Only then may the entity advertise. | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/guides/hdl-engineer.md:25` | hdl/acmp/           Milan binding and probing, plus the binding persistence shadow | directory map and shutdown semantics; consistent (module table updated) |
| `docs/guides/hdl-engineer.md:251` | \| There is no shutdown port \| [01 §5](../architecture/01_overview.md) describes a `SHUTD | directory map and shutdown semantics; consistent (module table updated) |
| `tb/acmp_nvm/README.md:2` | # acmp_nvm — KL_acmp_nvm_shadow persistence suite | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:8` | exit 0 = PASS, 360 checks. `-GDEB_TICKS_P=50` pins the debounce window the C++ | rewritten or added by this lane (9b4da6b5); states the D3 contract |
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
| `tb/acmp_nvm/README.md:280` | violation (07 §5.3 restores before entity_enable) and are not defended | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `tb/acmp_nvm/README.md:296` | - **M6** `restore_blank_o` hard-wired to `1'b0`: fails 2 of 76 (A2b empty | raw binding-manager suite: the module's own verdicts and parameters (README says so); historical counts keep their heads |
| `hdl/packet_engine/KL_pp_side_port.sv:25` | //                write after entity_enable (07 §2: "read-only everywhere | the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design |
| `hdl/packet_engine/KL_pp_side_port.sv:26` | //                after entity_enable except the control window"), or any | the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design |
| `hdl/packet_engine/KL_pp_side_port.sv:50` | input  wire         entity_enable_i,  //! 1 = image window is write-locked | the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design |
| `hdl/packet_engine/KL_pp_side_port.sv:63` | output logic        img_we_o,         //! write strobe (only while !entity_enable_i) | the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design |
| `hdl/packet_engine/KL_pp_side_port.sv:133` | WIN_IMG_C:   fwd_ok_w = we_i ? !entity_enable_i : 1'b1;  // W pre-enable, R | the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design |
| `tb/pp_top/README.md:60` | **D3S1** every persisted group at its first and last declared index | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/README.md:65` | other record id moves. **D3S2** `d3_unflushed_o` rises the cycle after | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/README.md:142` | a later SET persists. **D3R5b** the same containment in pass 1: its header | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/README.md:145` | later SET persists with nothing left unflushed. **D3R6** an erased device restores blank a | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/README.md:177` | SET persists. Over an erased device the bound falls in pass 1, which | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/README.md:191` | once the device ends the drained READ a later SET persists. With the | rewritten or added by this lane (f8d1a83e); states the D3 contract |
| `tb/pp_top/README.md:212` | persists with nothing unflushed. **D3R18** (R390-3 F1) an abort in the | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/pp_top/README.md:222` | drained READ the port is idle and a later SET persists. **D3R19** to | rewritten or added by this lane (8610ab35); states the D3 contract |
| `tb/pp_top/README.md:249` | `restore_done_o` is the COMBINED terminal: the binding walk's release | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/README.md:482` | `aecp_nvm_mark_o` export (issue #90) on this face and the name store: a | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:486` | notification: R21 proves the notification, never persistence (section D3 | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/README.md:490` | manager's own terminal (`dbg_walk_done_o`), not on `restore_done_o`, so every | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:492` | - **S0/S1** quiescence + snapshot identity, and `restore_done_o` has followed | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:509` | vendor default at the listener's release, while `entity_enable_i` is | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/README.md:519` | (issue #93 S4) grades the top's `restore_done_o` and `restore_busy_o` in | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:523` | next reset one of the two reads 1; `restore_done_o` never reads 1 while | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:525` | discovery arm of a walk lands in a cycle at or after its `restore_done_o` | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:551` | face, and the `nvm_unflushed_o` export (issue #90) sampled every cycle | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:554` | D3 records' is `d3_unflushed_o` (D3S2), and an integrator's pending is | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/README.md:636` | \| M36 \| the top's `restore_done_o` without the release (`= nvm_walk_done_w`) \| default  | the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R) |
| `tb/pp_top/README.md:689` | \| `identify_is_a_change` \| IDENTIFY (selector 7) made a persisted change \| `D3S7` \| 1  | rewritten or added by this lane (2fbe7926); states the D3 contract |
| `tb/pp_top/README.md:709` | \| `quarantine_released_by_time` \| the arbiter ends a drain after 1,000 cycles \| `D3R5:  | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/pp_top/README.md:769` | `restore_go_i` (and so before `entity_enable`); the "software has not | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/20-rtl-dataflow.svg:197` | <text x="40" y="851" font-size="10.5" fill="#4a5058">three boot releases: the binding walk | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/20-rtl-dataflow.svg:203` | <text x="40" y="948" font-size="10.5" fill="#4a5058">class-D status wires read every clock | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/src/01-top-level.drawio:106` | <mxCell id="legend" value="Solid = transaction / data path &#183; dashed = events, configu | F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two producers; draw.io cannot export headless here (diagrams README), so source and export stay paired |
| `docs/diagrams/src/01-top-level.drawio:158` | <mxCell id="e24" value="persist" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;das | F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two producers; draw.io cannot export headless here (diagrams README), so source and export stay paired |
| `docs/diagrams/src/01-system-context.drawio:25` | <mxCell id="proc" value="&lt;b&gt;IEEE 1722.1 PROTOCOL PROCESSOR&lt;/b&gt;&#10;(this archi | F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two producers; draw.io cannot export headless here (diagrams README), so source and export stay paired |
| `docs/diagrams/24-adp-acmp-states.svg:40` | <text x="305" y="214" font-size="10.5" fill="#4a5058">entity_enable_i AND restore_done_o</ | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/24-adp-acmp-states.svg:59` | <text x="42" y="579" font-size="11" fill="#4a5058">Deasserting entity_enable_i is the shut | requested-enable semantics (shutdown, Milan 5.6.1 gate) beside the added restore release |
| `docs/diagrams/21-integration-faces.svg:44` | <text x="464" y="560">NVM_RETRY_BACKOFF_CYC_P · SRP_DOM_DEF_VID_P</text> | rewritten or added by this lane (380a3e47); states the D3 contract |
| `docs/diagrams/21-integration-faces.svg:67` | <text x="42" y="357" font-size="11.5" fill="#4a5058">entity_enable_i · link_up_i · gm_chan | requested-enable semantics (shutdown, Milan 5.6.1 gate) beside the added restore release |
| `docs/diagrams/21-integration-faces.svg:68` | <text x="42" y="380" font-size="11.5" fill="#a03030">entity_enable_i requests; ADP sees it | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/21-integration-faces.svg:120` | <text x="968" y="704" font-size="11.5" fill="#4a5058">pending: \|nvm_unflushed_o \| d3_unf | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:374` | //! one persisted row the service phase sets, and what its record must hold | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:389` | //! T-NVM-DEBOUNCE at the wrap's 1 ms = 100 clk | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:486` | if (!x.d->d3_unflushed_o && x.nv_st == H::NvState::NV_IDLE | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:531` | void s1_every_group_persists_its_record() { | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:555` | // D3S2: the pending export. d3_unflushed_o rises in the cycle after the | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:572` | if (rise < 0 && x.d->d3_unflushed_o) rise = at + 1; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:574` | if (rise >= 0 && fall < 0 && !x.d->d3_unflushed_o) fall = at + 1; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:575` | if (rise >= 0 && done < 0 && !x.d->d3_unflushed_o) ++holes; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:699` | void s7_identify_is_never_persisted() { | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:706` | pending += x.d->d3_unflushed_o ? 1 : 0; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:725` | pending += x.d->d3_unflushed_o ? 1 : 0; | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:738` | // in all, each retry granted RETRY_BACKOFF_CYC_P cycles or more after the | rewritten or added by this lane (b06130d8); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:785` | && x.d->nvm_alarm_o && !x.d->d3_unflushed_o, | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:788` | unsigned(x.d->d3_unflushed_o)); | rewritten or added by this lane (f72a2d2d); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:844` | s1_every_group_persists_its_record(); | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:850` | s7_identify_is_never_persisted(); | rewritten or added by this lane (4dd37c2c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:970` | //! every persisted row at its reset value with its valid flag clear | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:991` | long done_early = 0;     //! cycles restore_done_o led the D3 terminal | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:997` | if (b.done < 0 && d->restore_done_o) b.done = c; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1001` | b.pending += d->d3_unflushed_o ? 1 : 0; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1003` | b.done_early += (d->restore_done_o && !both) ? 1 : 0; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1077` | return all && !x.d->d3_unflushed_o; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1100` | x.d->entity_enable_i = 1;                     // requested from reset (W14) | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1103` | CHECK(b.done > b.release && !x.d->restore_fail_o && !x.d->restore_blank_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1119` | pending += x.d->d3_unflushed_o ? 1 : 0; | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1216` | CHECK(b.done > b.release && !d->restore_fail_o && d->dbg_d3_applied_o == 1 | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1237` | CHECK(b.done > b.release && !d->restore_fail_o && d->dbg_d3_applied_o == 3 | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1263` | CHECK(b.done > b.release && !d->restore_fail_o | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1323` | CHECK(erased && applied_before && b.done > b.release && x.d->restore_fail_o | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1326` | && !x.d->restore_blank_o, | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1352` | CHECK(planted && applied_before && b.done > b.release && x.d->restore_fail_o | rewritten or added by this lane (b06130d8); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1379` | // later SET persists. | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1388` | CHECK(b.done > b.release && d->restore_fail_o && !d->restore_blank_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1407` | "D3R5: once the device ends the drained read a later SET persists"); | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1413` | // SET persists and nothing stays unflushed. | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1417` | CHECK(b.done > b.release && d->restore_fail_o && d->rs_cause_o == 3 | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1431` | CHECK(drained_busy && set && writes == 1 && !x.d->d3_unflushed_o | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1435` | "persists (%d WRITEs, unflushed %u)", writes, unsigned(x.d->d3_unflushed_o)); | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1444` | CHECK(b.done > b.release && !x.d->restore_fail_o && x.d->restore_blank_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1452` | CHECK(b.done > b.release && !x.d->restore_fail_o && x.d->restore_blank_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1464` | CHECK(b.done > b.release && x.d->restore_fail_o && !x.d->restore_blank_o | rewritten or added by this lane (81c8a5f7); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1480` | && x.d->restore_fail_o && x.d->rs_cause_o == 6 && x.d->restore_rb_o | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1522` | : (b.done >= 0 && !x.d->restore_fail_o && x.d->dbg_dyn_rate_v_o); | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1590` | x.d->entity_enable_i = 1; | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1596` | CHECK(b.closed > b.release && b.done < 0 && x.d->restore_fail_o | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1597` | && !x.d->restore_done_o && x.d->dbg_d3_own_o && !x.d->dbg_adp_enable_o | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1601` | x.d->entity_enable_i = 0; | rewritten or added by this lane (505524e5); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1622` | // the drain, and once the device ends it a later SET persists. Over an | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1635` | CHECK(b.done + 1 == AGG && d->restore_fail_o && d->rs_cause_o == 3 | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1656` | "the device ends it a later SET persists"); | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1661` | CHECK(e.done + 1 > AGG && e.done + 1 <= AGG + RS_TMO && d->restore_fail_o | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1701` | // ends the drained READ a later SET persists. With an image the store | rewritten or added by this lane (f8d1a83e); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1714` | x.d->entity_enable_i = 1; | rewritten or added by this lane (f8d1a83e); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1738` | && d->restore_fail_o && d->restore_cause_o == 3 | rewritten or added by this lane (f8d1a83e); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1747` | CHECK(b.done >= 0 && b.closed < 0 && in_time && d3_wait == 0 && d->restore_done_o | rewritten or added by this lane (f8d1a83e); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1774` | "the device ends the drained binding READ a later SET persists (%d WRITEs)", | rewritten or added by this lane (f8d1a83e); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1778` | && d->rs_cause_o == 7 && !d->restore_done_o && d->dbg_d3_own_o | rewritten or added by this lane (f8d1a83e); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1786` | x.d->entity_enable_i = 0; | rewritten or added by this lane (f8d1a83e); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1910` | && d->rs_cause_o == a.cause && !d->restore_done_o && !d->restore_rb_o | rewritten or added by this lane (58c5fe93); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1963` | const bool done0 = d->restore_done_o; | rewritten or added by this lane (e94bea85); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1964` | const bool fail0 = d->restore_fail_o; | rewritten or added by this lane (e94bea85); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1985` | CHECK(reached && set && strobes == 0 && rows && d->restore_done_o == done0 | rewritten or added by this lane (e94bea85); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1986` | && d->restore_fail_o == fail0 && d->restore_rb_o == rb0 | rewritten or added by this lane (e94bea85); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1992` | "the terminal, the rows %s", a.what, unsigned(d->restore_done_o), | rewritten or added by this lane (e94bea85); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:1993` | unsigned(d->restore_fail_o), unsigned(d->restore_rb_o), | rewritten or added by this lane (e94bea85); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2005` | // owns to the drain; once the device ends it, a later SET persists. Firing | rewritten or added by this lane (e94bea85); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2046` | && done_t - bound < RS_TMO && d->restore_fail_o && d->rs_cause_o == 3 | rewritten or added by this lane (e94bea85); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2061` | CHECK(set && writes == 1 && !x.d->d3_unflushed_o | rewritten or added by this lane (e94bea85); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2065` | "SET persists (%d WRITEs, unflushed %u)", writes, unsigned(x.d->d3_unflushed_o)); | rewritten or added by this lane (e94bea85); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2081` | // idle and a later SET persists. An arbiter that arms the drain only for | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2088` | x.d->entity_enable_i = 1; | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2144` | CHECK(drain_next && own_next == 1 && d->dbg_nvm_drain_o && d->restore_fail_o | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2145` | && d->restore_cause_o == 3 && b.done >= 0 && b.closed < 0 && d->restore_done_o | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2167` | && x.d->dbg_nvm_own_o == 0 && !x.d->d3_unflushed_o | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2171` | "SET persists (%d WRITEs, the port busy %ld of %ld clocks, unflushed %u)", | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2172` | unsigned(idle), writes, busy, 2 * WINDOW, unsigned(x.d->d3_unflushed_o)); | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2173` | x.d->entity_enable_i = 0; | rewritten or added by this lane (014e679c); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2193` | x.d->entity_enable_i = 1; | rewritten or added by this lane (8610ab35); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2201` | x.d->entity_enable_i = 0; | rewritten or added by this lane (8610ab35); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2250` | if (p.term < 0 && (d->restore_done_o \|\| d->restore_closed_o)) p.term = now; | rewritten or added by this lane (8610ab35); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2287` | && d->restore_done_o && d->restore_fail_o && d->rs_cause_o == 3 | rewritten or added by this lane (8610ab35); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2294` | : !d->restore_done_o ? "no terminal" | rewritten or added by this lane (8610ab35); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2295` | : d->restore_fail_o  ? "DEFAULTS" : "COMPLETE"; | rewritten or added by this lane (8610ab35); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2341` | if (p.term < 0 && (d->restore_done_o \|\| d->restore_closed_o)) p.term = now; | rewritten or added by this lane (8610ab35); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2449` | if (term < 0 && (d->restore_done_o \|\| d->restore_closed_o)) term = now; | rewritten or added by this lane (8610ab35); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2458` | CHECK(failed == bound + 2 && d->restore_fail_o && d->restore_cause_o == 3 | rewritten or added by this lane (8610ab35); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2505` | : !d->restore_fail_o ? "COMPLETE" : "DEFAULTS"; | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2599` | if (rise < 0 && x.d->d3_unflushed_o) rise = c; | rewritten or added by this lane (81c8a5f7); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2600` | if (rise >= 0 && fall < 0 && !x.d->d3_unflushed_o) fall = c; | rewritten or added by this lane (81c8a5f7); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2628` | CHECK(armed && b.done > b.release && x.d->restore_fail_o == late | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2632` | hold, unsigned(x.d->restore_fail_o), unsigned(x.d->rs_cause_o)); | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/d3_phases.hpp:2652` | CHECK(b.done > b.release && b.done - b.release < 2 * RS_TMO && d->restore_fail_o | rewritten or added by this lane (85b2f6f0); states the D3 contract |
| `docs/diagrams/23-bringup-decision.svg:32` | <text x="42" y="256" font-size="11.5" fill="#4a5058">Word 3 bit 0 is the REQUESTED entity_ | rewritten or added by this lane (39789f98); states the D3 contract |
| `docs/diagrams/23-bringup-decision.svg:38` | <text x="630" y="256" font-size="11.5" fill="#4a5058">Milan §5.6.1 holds the advertise mac | requested-enable semantics (shutdown, Milan 5.6.1 gate) beside the added restore release |
| `tb/pp_top/sim_main.cpp:795` | //! memory behind a live bridge); unlike dram_stuck_next it persists | rewritten or added by this lane (66267d9f); states the D3 contract |
| `tb/pp_top/sim_main.cpp:1089` | uint64_t nvm_marks = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1097` | uint8_t  nvm_mark_last = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1098` | uint64_t nvm_marks_cls6 = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1099` | uint64_t nvm_marks_cls7 = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1101` | //! the same vector as it stands now (nvm_unflushed_o, issue #90) | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1115` | long rs_done_owned = 0;   // cycles restore_done_o read 1 while owned | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1117` | long rs_pre_late = 0;     // ...of them, those at or after restore_done_o | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1250` | if (d->aecp_nvm_mark_o == 7) name_mark_cycle = t; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1251` | ++nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1252` | nvm_mark_last = d->aecp_nvm_mark_o; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1253` | if (d->aecp_nvm_mark_o == 6) ++nvm_marks_cls6; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1254` | if (d->aecp_nvm_mark_o == 7) ++nvm_marks_cls7; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1257` | nvm_unflushed_seen \|= d->nvm_unflushed_o; | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1276` | if (d->restore_done_o && !rs_done) { rs_done = true; ++rs_dones; } | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1277` | if (rs_on && !d->restore_busy_o && !d->restore_done_o) ++rs_hole; | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1278` | if (d->restore_done_o && owned) ++rs_done_owned; | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:1720` | d->entity_enable_i = 0; d->link_up_i = 0; d->gm_change_i = 0; | harness drive of the requested enable, or a comment on software load order (updated) |
| `tb/pp_top/sim_main.cpp:1768` | nvm_marks = 0; notify_enqs = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:1770` | nvm_marks_cls6 = 0; nvm_marks_cls7 = 0; nvm_mark_last = 0; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3945` | // R21: THE EXPORT (issue #90). aecp_nvm_stb_o / aecp_nvm_mark_o carry the | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3946` | // uCPU's OP_NVM_MARK effect out of the top, and the mark is the micro-op | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3949` | // persistence trigger: the saved-state contract's map and name stages | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/sim_main.cpp:3958` | const uint64_t m0 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3959` | const uint64_t c6_0 = h.nvm_marks_cls6; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3963` | CHECK(h.nvm_marks == m0 + 1 && h.nvm_marks_cls6 == c6_0 + 1 | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3964` | && h.nvm_mark_last == 6, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3967` | static_cast<unsigned>(h.nvm_marks - m0), | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3968` | static_cast<unsigned>(h.nvm_mark_last)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3971` | const uint64_t m1 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3974` | CHECK(h.nvm_marks == m1, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3976` | static_cast<unsigned>(h.nvm_marks - m1)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3982` | const uint64_t m2 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3983` | const uint64_t c7_0 = h.nvm_marks_cls7; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3988` | CHECK(h.nvm_marks == m2 + 1 && h.nvm_marks_cls7 == c7_0 + 1 | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3989` | && h.nvm_mark_last == 7, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3992` | static_cast<unsigned>(h.nvm_marks - m2), | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:3993` | static_cast<unsigned>(h.nvm_mark_last)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:4664` | //! ...and the PERSISTENT flag changes nothing (the blanket refusal) | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:4670` | "L1b: PERSISTENT ACQUIRE refused the same way"); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:6857` | // or notified" has no wire shape at all: an NVM_MARK and a NOTIFY_ENQ | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6861` | // WRITE_ST that KL_aecp_dyn_state took), the OP_NVM_MARK strobe | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6862` | // (aecp_nvm_stb_o, counted in H::step as nvm_marks) and the | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6892` | const uint64_t m0 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6896` | const uint64_t mb = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6911` | CHECK(h.nvm_marks == mb, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6912` | "W10j5: the refusal of %u raised OP_NVM_MARK %u times, want 0", | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6913` | bad, static_cast<unsigned>(h.nvm_marks - mb)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6948` | CHECK(h.nvm_marks == m0 + 1, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6949` | "W10j11: the accepted SET raised OP_NVM_MARK %u times, want 1", | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:6950` | static_cast<unsigned>(h.nvm_marks - m0)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7803` | // OP_NVM_MARK and OP_NOTIFY_ENQ strobes, and a second controller | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7829` | const uint64_t m0 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7834` | const uint64_t mb = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7848` | CHECK(h.nvm_marks == mb, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7849` | "W9k5: the refusal of 0x%08X raised OP_NVM_MARK %u times, " | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7850` | "want 0", bad, static_cast<unsigned>(h.nvm_marks - mb)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7873` | CHECK(h.nvm_marks == m0 + 1, | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7874` | "W9k11: the accepted SET raised OP_NVM_MARK %u times, want 1", | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7875` | static_cast<unsigned>(h.nvm_marks - m0)); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7955` | const uint64_t m0 = h.nvm_marks; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7966` | CHECK(d->dbg_dyn_writes_o == w0 && h.nvm_marks == m0 | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:7970` | static_cast<unsigned>(h.nvm_marks - m0), | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:8504` | // The claim needs no entity_enable: addresses are owned before the | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:8563` | d2->entity_enable_i = 1; | harness drive of the requested enable, or a comment on software load order (updated) |
| `tb/pp_top/sim_main.cpp:8831` | entity_enable_adpdu_window_and_cadence(); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:8957` | //! top's restore_done_o now follows that terminal by the listener | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:8962` | CHECK(d->restore_fail_o == 0, "R: no restore_fail on a blank device"); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:8985` | CHECK(d->restore_done_o == 1 && d->restore_busy_o == 0, | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:8986` | "S0: restore_done_o has followed both walks' terminals (issue #92, D3)"); | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9048` | void entity_enable_adpdu_window_and_cadence() { | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9051` | d->entity_enable_i = 1; | harness drive of the requested enable, or a comment on software load order (updated) |
| `tb/pp_top/sim_main.cpp:9285` | h.run_ms(700);                       // > T-NVM-DEBOUNCE at 1 ms ticks | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9308` | //! this vector ORed with d3_unflushed_o (D3S2), so the port has to carry the | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9314` | "S9: nvm_unflushed_o[0] rose while the binding was unflushed " | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9316` | CHECK(d->nvm_unflushed_o == 0, | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9317` | "S9: nvm_unflushed_o clears on the commit's done (reads 0x%02x)", | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9318` | d->nvm_unflushed_o); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9376` | while (!d->restore_done_o && guard--) h.step(); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9377` | return d->restore_done_o != 0; | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9403` | // left to persist | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9414` | h.run_ms(1500);                      // T-NVM-DEBOUNCE, then the burst | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9428` | CHECK(h.q_acmp.empty() && !d->restore_busy_o && !d->restore_done_o, | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9439` | && !d->restore_done_o, | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9442` | while (!d->restore_done_o && guard--) h.step(); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9471` | // read the arbiter drains it; a later BIND then persists, and the next | rewritten or added by this lane (380a3e47); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9491` | CHECK(d->dbg_walk_done_o && d->restore_fail_o && d->restore_cause_o == 3 | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9492` | && d->entity_enable_i == 0 && waited < BW_TMO + 200 | harness drive of the requested enable, or a comment on software load order (updated) |
| `tb/pp_top/sim_main.cpp:9501` | && d->entity_enable_i == 0 && !d->restore_done_o, | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9507` | while (!d->restore_done_o && waited2 < 4 * BW_TMO) { h.step(); ++waited2; } | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9508` | CHECK(d->restore_done_o && d->restore_fail_o && d->rs_cause_o == 3 | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9509` | && !d->restore_closed_o && !d->restore_blank_o | rewritten or added by this lane (5e1476d1); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9552` | CHECK(bw_boot() && !d->restore_fail_o, "BW3: the next walk ends clean"); | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9561` | // BW4 (issue #93 S4): the top's restore_done_o waits for the binding walk's | rewritten or added by this lane (39789f98); states the D3 contract |
| `tb/pp_top/sim_main.cpp:9577` | CHECK(bw_boot() && !d->restore_fail_o, | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9587` | "BW4: %ld walks, each ended with restore_done_o, the walk's terminal " | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9590` | "BW4: restore_busy_o or restore_done_o read 1 in every cycle from " | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9593` | "BW4: restore_done_o never read 1 while the admission gate still " | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9597` | "before its restore_done_o (%ld of %ld after it)", h.rs_pre_late, | boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own tap, as the README names them |
| `tb/pp_top/sim_main.cpp:9801` | const auto marks = h.nvm_marks_cls7; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:9809` | CHECK(h.nvm_marks_cls7 == marks + (changed ? 1 : 0), | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:9903` | const auto marks = h.nvm_marks_cls7; | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:9919` | CHECK(h.nvm_marks_cls7 == marks, "NW ABORT: no group-7 completion mark"); | R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten) |
| `tb/pp_top/sim_main.cpp:9959` | h.d->entity_enable_i = 1; | harness drive of the requested enable, or a comment on software load order (updated) |
| `docs/diagrams/01-system-context.svg:3` | <svg xmlns="http://www.w3.org/2000/svg" style="background: transparent; background-color:  | F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two producers; draw.io cannot export headless here (diagrams README), so source and export stay paired |
| `docs/diagrams/01-top-level.svg:3` | <svg xmlns="http://www.w3.org/2000/svg" style="background: transparent; background-color:  | F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two producers; draw.io cannot export headless here (diagrams README), so source and export stay paired |

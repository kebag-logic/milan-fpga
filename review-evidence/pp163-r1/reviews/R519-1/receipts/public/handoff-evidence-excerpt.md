Source: https://github.com/kebag-logic/milan-fpga/blob/fc0046724b1416d5f87451c52eaac1a2668ae4ad/review-evidence/pp163-r1/author/HANDOFF.md

Verbatim sections 1 through 7; full published source sha256 cd6f544d316ea6b8202b620beb38144cd9dde9d8a950ea2f1f7b89a071fde94b.

## 1. Measurement, OOC 1x1 at 50 MHz (#638 recipe)

Recipe: the scratch parent at dev `28f9666f` with the 148 and then the 22 patch, processor
gitlink staged at the revision, `sw/litex/build.sh ax7101 --dry-run` export, integrated
elaboration, `syn/ooc/pp_baseline.py --integrated-clock` (KL_pp_shadow, `synth_design
-directive AreaOptimized_high -mode out_of_context`, 20.000 ns clock), then
`pp_resource_gate.py record` and `check` for the `ooc-1x1` endpoint. Vivado v2026.1, run
alone under the Vivado lock. The head run (at `912ee6ef`; `hdl/` and `syn/` are identical
at `cd9825c9`) re-elaborated at its own revision. The wrapper parameters it bound are
identical to base's.

Base OOC timing summary: WNS -3.562 ns, TNS -37.519 ns, 16 failing endpoints of 62840,
WHS +0.159 ns. Every failing endpoint is in the transmit arbiter.

Cone survey (scratch `scripts/arb_cone.tcl`): every startpoint in the fan-in of the 187
arbiter sequential cells (561 endpoint pins), and the worst path from each startpoint to
each endpoint.

| | Before | After |
|---|---:|---:|
| Startpoints in the arbiter's input cone | 1,631 | 328 |
| Start/end pairs (worst path each) | 263,154 | 17,990 |
| Pairs above 20 levels | 146,535 | 0 |
| Deepest (levels) | 51 | 16 |

Per arbiter endpoint (deepest path, worst slack):

| Arbiter endpoint | Levels before | Slack before (ns) | Levels after | Slack after (ns) |
|---|---:|---:|---:|---:|
| `slot_r` | 51 | -3.562 | 16 | +11.912 |
| `owner_r` | 50 | -3.417 | 15 | +12.057 |
| `arb_st_r` (FSM) | 46 | -2.106 | 12 | +12.848 |
| `start_sent_r` | 46 | -1.514 | 12 | +13.440 |
| `age_r` | 35 | +2.490 | 9 | +13.827 |
| `cnt_r` | 34 | +3.371 | 8 | +14.710 |
| `gnt_r` | 34 | +4.001 | 8 | +15.341 |
| `pend_r` | 34 | +4.152 | 8 | +15.393 |
| `pace_nonsol_r` | 33 | +4.491 | 8 | +15.341 |

Every source above 20 levels before (assignment item 1), with its deepest path. That path
ends at `slot_r` for every source; `owner_r`, the FSM and `start_sent_r` follow, and the
counters, `pend_r` and `pace_nonsol_r` are shallower (the per-endpoint table above):

| Source | Levels | Worst slack (ns) | Route into the arbiter |
|---|---:|---:|---|
| notify `wr_ix_r` | 51 | -2.981 | identity-index row read (`rows_r[wr_ix_r]`), own-row compare (`ix_own_w`), command hit, CA cancel pick, originator cancel, withdraw mask, lane head, arbiter select |
| rx validator `hdr_src_mac_r` | 50 | -1.795 | notify index / originator response CAM, withdraw mask, arbiter |
| notify `rows_r` LUTRAM (all 64 column pairs) | 41-50 | -2.527 | as `wr_ix_r` |
| notify `pend_r` | 47 | -3.562 | parked-expiry drain pick, CA cancel, originator, mask, arbiter |
| rx validator `hdr_ctlr_eid_r` | 46 | -1.753 | as `hdr_src_mac_r` |
| notify `ca_probe_r` | 43 | -1.341 | CA cancel |
| rx validator `hdr_msg_type_r`, `hdr_protocol_r` | 41 | -1.047 | originator response valid |
| notify index chunk memories, `n_st_r`, `ix_set_r`, `ix_clr_r` | 40-41 | -1.389 | command hit |
| originator `key_r` | 41 | +2.962 | response CAM |
| rx validator `cp_r` (header valid) | 40 | -0.233 | response/command valid |
| notify `valid_r` | 39 | +0.078 | command hit |
| rx validator `hdr_target_eid_r` | 37 | +3.456 | response CAM |
| `entity_id_i` (port) | 36 | unconstrained | response valid |
| originator `seq_r`, rx validator `hdr_seq_r` | 33 | +3.510 | response CAM |
| rx validator `hdr_opcode_r` | 32 | +3.852 | response valid |
| originator `owner_r`, `valid_r`, `cancel_pend_r` | 29-32 | +3.671 | cancel pick, mask |
| originator `exp_pend_r`, `accept_pend_r`, `txs_r`, `retried_r` | 25-27 | +6.525 | mask |
| originator `release_*_o`, CA builder `cancel_release_*_o`, release merge `pending_r` | 24-25 | +7.698 | released head drop, arbiter select |
| top `laneq_org_r`, `laneq_org_cnt_r`, tx slots `st_r` | 21 | +9.371 | lane head ready, arbiter select |

Two structures made every one of these deep:
1. Every deep cone reached the arbiter through the originator's combinational
   `withdraw_slot_mask_o`, which fed the originator lane's request, the lane-queue
   compaction and the arbiter's `start_abort_i`.
2. The arbiter's selection was a serial best-so-far loop, 17 levels from `req_valid_i` to
   `slot_r`/`owner_r` (19 in a standalone synthesis of the module; 8 after), so even
   registered requesters (release, lane queue) landed at 21-25.

After: the deepest sources are the registered releases (originator `release_*_o`, CA builder
`cancel_release_*_o`, 16 levels, +11.912 ns), then release merge `pending_r` (15), then
`org_withdraw_mask_r`, tx slots `st_r` and `laneq_org_r` (12). The cut cone now ends at the
new register: `notify wr_ix_r -> org_withdraw_mask_r` 28 levels, +7.229 ns. The lane queue
gains too: worst path into `laneq_org_r` was 37 levels, +0.424 ns (from notify `pend_r`),
now 14 levels, +12.303 ns; `laneq_org_cnt_r` 35 levels, +1.591 ns, now 10, +13.582 ns.

## 2. Changes

RTL (`912ee6ef`):

| File:line | Change |
|---|---|
| `hdl/top/protocol_processor_top.sv:4371-4386` | `org_withdraw_mask_r`, an 8-bit register of the originator's `withdraw_slot_mask_o` (block `withdraw_mask_stage`), with the reason |
| `hdl/top/protocol_processor_top.sv:4407` | originator lane head withdrawal reads `org_withdraw_mask_r` |
| `hdl/top/protocol_processor_top.sv:4427` | lane-queue compaction reads `org_withdraw_mask_r` |
| `hdl/top/protocol_processor_top.sv:4505` | the arbiter's `start_abort_i` (`arb_start_abort_w`) reads `org_withdraw_mask_r` |
| `hdl/packet_engine/KL_pp_tx_arbiter.sv:161-196` | selection: the serial best-so-far scan replaced by a pairwise rank (winner = the eligible requester no other eligible one outranks; ties to the lowest index), the same function |

All three readers of the mask move together: a lane that dropped its head on the
combinational mask while the arbiter accepted it on the registered one would pop twice.
No existing register could be moved instead: the arbiter's existing `pend_r` cut is
re-entered by `start_abort_i` and the live request, and both carry the mask in the clock
the originator decides, so a cut on this cone necessarily delays that decision by one
clock. The selection restructure adds no clock.

Benches and documentation (`916f53c7`, `2ef802cb`, `cd9825c9`):

| File:line | Change |
|---|---|
| `tb/pp_top/notify_phases.hpp:1642-1824, 1856-1861` | section WD (`WithdrawStagePhase`), `run_withdraw` |
| `tb/pp_top/sim_main.cpp:836-838, 1620-1624, 2058` | harness: let a byte held at eof go on a bit of the validator's commit shift |
| `tb/pp_top/sim_main.cpp:14062, 14069-14070, 14090` | `--withdraw-only`; WD in the default run (after CS, before the counters and AQ) |
| `tb/pp_top/pp_top_wrap.sv:487-495, 905-910` | taps `dbg_rxv_commit_o`, `dbg_arb_st_o`, `dbg_arb_owner_o`, `dbg_arb_sent_o` |
| `tb/pp_top/Makefile:122-124, 228` | `make withdraw` |
| `tb/pp_top/notify_mutants.py:353-384` | arms `withdraw_unregistered`, `withdraw_abort_ignored` (suite `--withdraw-only`), `cancel_one_clock_late` (`tb/aecp_notify`) |
| `tb/aecp_notify/sim_main.cpp:84, 98-147, 273, 717-750` | section CX (`cancel_clock`); `registers()`/`draws()` split out of `register_row`/`complete_draw` so CX's setup adds no unmutated check |
| `tb/pp_top/README.md:2229-2241, 2466-2501, 2503-2595` | the C6 intro, section WD, the notify mutation record (three rows, the re-run, `ix_new_identity_unset` +CX1) |
| `tb/aecp_notify/README.md` | build table, mutation record row, `ix_new_identity_unset` +CX1, section CX (204-220) |
| `tb/tx_arbiter/README.md:53, 59-67` | M3's planted text, the M1-M5 re-plant and the equivalence proof |
| `docs/architecture/03_packet_engine.md:488` | a "Withdrawal" rule row in §8 |

### Pre-edit grep (assignment item 3)

Before the RTL edit, every removed line (12) was searched with `git grep -F` at `86a7b0c5`
across `tb/**/*.patch`, `tb/**/*.py` (every exact-text driver table) and `tb/**/README.md`,
then across all of `tb`, `scripts`, `syn` and `docs`: 0 hits for every line. No patch or
exact-text arm carries a changed line.

Every arm still plants:
- All 283 `tb/**/*.patch` apply (`git apply --check` on an export) at base and at the head,
  0 refused.
- Every campaign arm planted at the head: no REFUSED verdict in any campaign (sections 6).
- The arbiter README's M1-M5 (hand-planted records) were re-planted at base and head in
  scratch copies, with identical failing-check lists at both: M1 13, M2 6, M3 23, M4 30 and
  M5 2 of 66. M3's text moved with the selection (`<=`/`<` to `>=`/`>`), the same inversion.

### Arbiter equivalence

Yosys `equiv_make`, `equiv_simple -seq 2`, `equiv_induct -seq 2` and `equiv_status -assert`
on the old and the new `KL_pp_tx_arbiter` (lowered with sv2v, memories mapped to flops):
438 of 438 `$equiv` cells are proven at the top's parameters (8 lanes, the top's priority
map and solicited mask), and 386 of 386 at the module defaults. Control: the same proof
with the tie compare `<=` planted as `<` leaves 3 unproven and fails. The selection adds no
cycle and changes no behaviour; `tb/tx_arbiter` passes 66 of 66, unchanged.

## 3. The added cycle, its graded checks and mutants

One cycle is added. A cancellation (the originator's response, cancel or final-expiry
choice) now reaches the originator lane, the lane compaction and the arbiter's pre-start
abort one clock after the originator takes it. That is the clock its registered release
reaches the slot pool. The protocol-visible effect is that the race between a cancellation
and the serializer's acceptance moves by one clock:

- A probe whose cancellation lands on its acceptance clock is now sent (before, it was
  withdrawn). Its exchange is gone (no timer, no retry), the originator drops the
  acceptance, and the pool frees the slot after the last byte.
- A cancellation on the selection clock still withdraws the probe, one clock later and
  before the pool starts it.

| Check | Bench | Grades | Mutant(s) that fail it |
|---|---|---|---|
| WD1 | `tb/pp_top` (section WD, `--withdraw-only` and the default run) | cancellation on the acceptance clock: the probe leaves once, byte-exact; no retry and no deregistration in 1.5 s; both answers leave; 5 slots, the originator and its lane idle | `withdraw_unregistered` (the three readers back on the combinational mask) |
| WD2 | `tb/pp_top` | cancellation on the selection clock: the arbiter's start state holds that selection the next clock, aborted, and is idle the clock after; no pool start | `withdraw_unregistered`, `withdraw_abort_ignored` (`start_abort_i` tied low) |
| WD3 | `tb/pp_top` | that probe never reaches the wire; answers leave; slots, the originator and its lane idle | `withdraw_abort_ignored` |
| CX1 | `tb/aecp_notify` | the registry monitor's cancellation is in the command's own clock and in none of the 8 after it: the notification module adds no clock, so the top's stage is the only one | `cancel_one_clock_late` (also fails the existing IX3); `ix_new_identity_unset` (existing arm) now fails it too |

In the campaigns (section 6), `notify_mutants.py` kills all three new arms by exactly their
named checks at the head, and its goldens (`tb/aecp_notify` run, `tb/pp_top
--withdraw-only`) pass. WD's clock trace at the head:
- acceptance case: `[-1 idle] [0 start, lane 7, not started, pool start] [+1 started]`,
  1 probe;
- selection case: `[0 idle, head queued] [+1 start, lane 7, not started, no pool start]
  [+2 idle]`, 0 probes.

WD lets every waiting lane age past T-TX-AGING (12 ms) before the race. Without that, an
aged SRP frame outranks the fresh probe and WD has no probe to race (seen and fixed during
development).

Records the assignment names, so expected to differ base to head:
- `tb/pp_top`: +3 checks (WD in the default build).
- `tb/aecp_notify`: +1 check (CX1).
- `notify_mutants.py`: +3 arms and +1 golden; `ix_new_identity_unset` fails CX1 as well.
- Two parent-consumer counts move with those files: the parent's Python idiom gate counts
  31 more first-party Python lines (the new arms), and the port-contract gate 6 more
  test-only hierarchical observations (the 6 internal nets the new wrap taps read).

## 4. OOC 1x1 area and timing, before and after

| Scope (#638 recipe, OOC 1x1) | LUT before | LUT after | delta | FF before | FF after | delta |
|---|---:|---:|---:|---:|---:|---:|
| wrapper (KL_pp_shadow) | 23179 | 23160 | -19 | 19779 | 19787 | +8 |
| `u_pp` (processor) | 22517 | 22478 | -39 | 18941 | 18951 | +10 |
| `(u_pp)` own logic | 939 | 780 | -159 | 2033 | 2039 | +6 |
| `u_tx_arbiter` | 185 | 234 | +49 | 187 | 187 | 0 |
| `u_originator` (unchanged) | 697 | 676 | -21 | 885 | 885 | 0 |
| `u_notify` (unchanged) | 2125 | 2157 | +32 | 1256 | 1258 | +2 |

The STOP bar (60 LUT, 120 FF) is not reached on any scope. The processor is -39 LUT / +10
FF, the two changed blocks' own logic -110 LUT / +6 FF together, and the arbiter alone +49
LUT. `pp_resource_gate.py check` RESULT PASS at both (against the parent's recorded
baseline: LUT -18, FF +11 at head). Unchanged blocks move by synthesis noise only.

| OOC timing summary | Before | After |
|---|---:|---:|
| WNS (ns) | -3.562 | +3.337 |
| TNS (ns) | -37.519 | 0.000 |
| Failing endpoints | 16 of 62840 | 0 of 62857 |
| WHS (ns) | +0.159 | +0.159 |
| Worst path | notify `pend_r` -> arbiter `slot_r`, 47 levels | `u_aecp/u_ucpu desc_base_r` -> `u_aecp/u_d3 deb_cnt_r`, 32 levels (not this cone) |

Worst five paths into the arbiter (`report_timing -to` the arbiter's sequential cells):

| # | Before: source -> endpoint, levels, slack (ns) | After: source -> endpoint, levels, slack (ns) |
|---|---|---|
| 1 | notify `pend_r[2]` -> `slot_r[0]`, 47, -3.562 | CA builder `cancel_release_slot_o[2]` -> `slot_r[0]`, 16, +11.912 |
| 2 | notify `pend_r[2]` -> `slot_r[1]`, 47, -3.562 | same -> `slot_r[1]`, 16, +11.912 |
| 3 | notify `pend_r[2]` -> `slot_r[2]`, 47, -3.562 | same -> `slot_r[2]`, 16, +11.912 |
| 4 | notify `pend_r[2]` -> `owner_r[0]`, 46, -3.417 | same -> `owner_r[1]`, 15, +12.057 |
| 5 | notify `pend_r[2]` -> `owner_r[1]`, 45, -2.930 | same -> `owner_r[0]`, 14, +12.296 |

The parent three-directive sweep is for the pin adoption (acceptance item 3), not run here.

## 5. Processor suites and gates

Base `86a7b0c5`, head `2ef802cb` (the full set), and final head `cd9825c9` (the full set
again; `2ef802cb..cd9825c9` changes two README files only). Every run has its own `git
archive` export, log, rc and command/time record. `make check` ran in the lane: base on a
detached checkout, then back to the branch.

| Gate | Base rc | `2ef802cb` rc | Final rc | Records |
|---|---:|---:|---:|---|
| `scripts/run_suites.sh` | 0 | 0 | 0 | base 1,028,235 checks, 0 failing; head 1,028,239, 0 failing. Every suite line is identical except `aecp_notify` 45 -> 46 and `pp_top` 10,444 -> 10,447. The final log is byte-identical to `2ef802cb`'s |
| `scripts/lint_hdl.sh` | 0 | 0 | 0 | byte-identical at all three |
| `make -j8 check` | 0 | 0 | 0 | identical sorted records (concurrent recipe order varies) |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 | 0 | byte-identical (`matrix: OK (94 rows, 0 untested)`) |
| `syn/yosys/run.sh` | 0 | 0 | 0 | identical except the lowered `all.v` line numbers cited in four memory-to-register warnings (the arbiter's source is 11 lines longer); every verdict identical. Final byte-identical to `2ef802cb` |

Suites (base / head): acmp_listener 3111, acmp_nvm 388, acmp_talker 1342, adp_engine 1348,
aecp_notify 45 / 46, ca_originator 16, desc_mem_guard 78, desc_store 586, dispatch 211,
dyn_state 118, event_router 81, lsn_admit 18, maap 196, nvm_port 1219, originator 107,
pp_top 10444 / 10447, prng 76, release_merge 18, resp_buf 64, rx_slots 130,
rx_validator 555, scoreboard 3705, side_port 368, srp_admission 991231, srp_decoder 190,
srp_encoder 581, srp_stream_fsms 1347, srp_top 8656, timer_map 1360, timer_service 48,
tx_arbiter 66, tx_slots 95, ucpu 437. All PASS at both.

## 6. Campaigns (base / head)

Every campaign driver in the tree, `--jobs 2`, at base and at `2ef802cb`, then at the final
head. Seconds are wall time under the shared two-build limit. At the final head every
campaign's records equal `2ef802cb`'s (driver logs byte-identical, or identical when sorted
where arms complete in a varying order); no arm was REFUSED at any revision.

| Campaign | Base | `2ef802cb` | Final | Comparison |
|---|---|---|---|---|
| `tb/pp_top/d3_mutants.py` | rc 0, 110 of 110 KILLED, goldens PASS (7794 s) | rc 0, same (8020 s) | rc 0, same (7186 s) | records identical; driver log identical when sorted (completion order) |
| `tb/pp_top/aecp_mutants.py` | rc 0, `67 checks: 67 PASS` (2022 s) | rc 0, same (2144 s) | rc 0, same (1704 s) | driver log byte-identical |
| `tb/pp_top/notify_mutants.py` | rc 0, 56 of 56 KILLED, goldens PASS (1659 s) | rc 0, 59 of 59 KILLED, goldens PASS (1735 s) | rc 0, 59 of 59 KILLED (1594 s) | named: +3 arms, +1 golden; `ix_new_identity_unset` fails CX1 too; the other 55 earlier records identical. Final identical to `2ef802cb` when sorted |
| `tb/pp_top/aecp_dispatch_mutants.py` | rc 0, `44 checks: 44 PASS`, 40 KILLED (1367 s) | rc 0, same (1425 s) | rc 0, same (1147 s) | driver log byte-identical |
| `tb/pp_top/acmp_mutants.py` | rc 0, 33 of 33 KILLED (2051 s) | rc 0, same (2041 s) | rc 0, same (2288 s) | records identical; log identical when sorted |
| `tb/pp_top/gsi_mutants.py` | rc 0, 20 detected, golden and restored PASS (1471 s) | rc 0, same (1408 s) | rc 0, same (729 s) | driver log byte-identical |
| `tb/pp_top/ctr_mutants.py` | rc 0, `18 checks: 18 PASS` (958 s) | rc 0, same (542 s) | rc 0, same (614 s) | driver log byte-identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0, decode killed, golden and restored PASS (151 s) | rc 0, same (165 s) | rc 0, same (80 s) | driver log byte-identical |
| `tb/adp_engine/mutants.py` | rc 0, `43 checks: 43 PASS` (365 s) | rc 0, same (490 s) | rc 0, same (352 s) | driver log byte-identical |
| `tb/maap/mutants.py` | rc 0, `32 checks: 32 PASS` (668 s) | rc 0, same (760 s) | rc 0, same (241 s) | driver log byte-identical |
| `tb/srp_top/mutants.py` | rc 0, `137 checks: 137 PASS` (2515 s) | rc 0, same (2884 s) | rc 0, same (2791 s) | driver log byte-identical |
| `tb/srp_admission/mutants.py` | rc 0, `12 checks: 12 PASS` (521 s) | rc 0, same (541 s) | rc 0, same (730 s) | driver log byte-identical |
| `tb/acmp_talker/retry_mutants.py` | rc 0, 62 killed, 7 equivalence and 1 performance controls (462 s) | rc 0, same (383 s) | rc 0, same (332 s) | driver log byte-identical |

## 7. Parent consumer set (17), dev `28f9666f` + 148 + 22

The scratch parent: a clone at dev `28f9666feab2b2ba287643c63ed3a16b1e0bb863`, the supplied
`parent-adoption-148-6c22d3ca.patch` applied first with `git apply`, then
`parent-adoption-22-28f9666f.patch`; never committed or pushed. Both patches reverse-check
cleanly against the tree, and the tree differs from dev only by them and the staged
processor gitlink. Timing processor `5dce647a` and AXIS dependency `48ff7a7e` stay at their
recorded pins; the external leaf is not initialized. Each submodule's top level is verified
before any Git command in it and before each consumer starts. The OOC recipe's links (the
builder output and two ROM links) were removed before the consumers ran. Each run's
generated files were moved aside before the next revision was staged.

The set ran at base (gitlink `86a7b0c5`), at `2ef802cb` (all but 09) and at the final head
(gitlink `cd9825c9`, where the scratch parent is left). 09 ran last, alone, at base and at
the final head, each after queueing for the shared Vivado lock.

| Consumer | Command | Base rc | `2ef802cb` rc | Final rc | Comparison |
|---|---|---:|---:|---:|---|
| 01_cpp | `python3 scripts/check_cpp_idiom.py` | 0 | 0 | 0 | identical (at `916f53c7` it refused one multi-declarator line: fixed by `2ef802cb`) |
| 02_py | `python3 scripts/check_py_idiom.py` | 0 | 0 | 0 | named: first-party Python lines 199,997 -> 200,028 (the new arms) |
| 03_sources | `python3 scripts/check_rtl_source_lists.py` | 0 | 0 | 0 | identical |
| 04_pp_sources | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0 | 0 | identical |
| 05_ports | `python3 scripts/check_port_contracts.py` | 0 | 0 | 0 | named: test-only hierarchical observations 317 -> 323 (the wrap's 6 new reads) |
| 06_naming | `python3 scripts/measure_naming.py --check` | 0 | 0 | 0 | identical |
| 07_evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | 0 | 0 | identical |
| 08_docs | `python3 scripts/docs_check.py` | 0 | 0 | 0 | identical |
| 09_xvlog | `python3 scripts/xvlog_gate.py --check` (under the Vivado lock, alone) | 0 | not run | 0 | 0 findings at both (73 parent and 52 pinned-processor sources); identical except the pinned-revision line |
| 10_builder | `python3 sw/builder/test_builder.py` | 0 | 0 | 0 | identical except temp-directory names and durations; 1 gate arm not run at each (gate 11's calibration needs a reference build tree that is not on disk), as recorded before |
| 11_lint | `python3 scripts/lint_rtl.py --check` | 0 | 0 | 0 | identical (90 <= ratchet 90) |
| 12_shadow | `make -j8 -C tb/verilator/pp_shadow` | 0 | 0 | 0 | 606, 606, 646, 311 checks, 0 failures at each (print order varies with build concurrency); per-check lines identical |
| 13_nvm_lint | `make -j8 -C tb/verilator/nvm_cosim lint` | 0 | 0 | 0 | identical except Verilator wall-time lines |
| 14_nvm_quick | `make -j8 -C tb/verilator/nvm_cosim quick` | 0 | 0 | 0 | nvm_cosim 315 checks, 315 PASS at each |
| 15_datapath | `make -j8 -C tb/verilator/milan_dp VERILATOR_JOBS=2` | 0 | 0 | 0 | every tally line identical (sorted) at each |
| 16_render | `make -j8 -C tb/verilator/milan_dp_render VERILATOR_JOBS=2 MUTANT_JOBS=2` | 0 | 0 | 0 | tdm8_render 65 and 245 checks, 0 failures; 5 leg-defect arms PASS; identical at each |
| 17_shell | `python3 scripts/check_sh_idiom.py` | 0 | 0 | 0 | identical |

15_datapath records (each run): gmstep 104; 182 and 182; milan_datapath 236 (1 guarded);
421; 416; 1961, 1961, 3746, 1961; milan_datapath 236 (1 guarded); 33; milan_datapath 233
(5 guarded); media_aclk 193; 6 and 6; all 0 failures.


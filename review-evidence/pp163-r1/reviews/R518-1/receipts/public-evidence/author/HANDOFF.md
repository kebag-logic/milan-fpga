# [A553] HANDOFF: processor #163 (transmit-arbiter input cone)

Status: REVIEW READY at `cd9825c947cf67b735d26cc1c42541ccd9d7f637` (not pushed; no PR opened).

- Branch `pp163-txarb-cone` from processor `main` `86a7b0c5`. Head
  `cd9825c947cf67b735d26cc1c42541ccd9d7f637` (four commits, not pushed):
  - `912ee6ef` Cut the transmit-arbiter input cone: register the withdraw mask, rank
    requesters in parallel (RTL)
  - `916f53c7` Grade the withdraw stage in tb/pp_top (WD) and tb/aecp_notify (CX), with
    planted mutants (benches, mutant driver, READMEs, 03 §8 row)
  - `2ef802cb` Declare section WD's clock-sample members one per line (the parent's C++
    idiom gate refused one multi-declarator line in `916f53c7`)
  - `cd9825c9` Record the #163 notify-campaign re-run and CX1 in the ix_new_identity_unset
    rows (README text only)
- TAKEN posted on #163 (comment 6015592098); REVIEW READY posted with the head (comment
  6023577480). The previous session was ended by the service
  memory cap before any commit; this session resumed from a clean tree and posted nothing
  twice.
- No port, register-map or parameter change. No STOP condition was hit.
- Acceptance: items 1 and 2 and the area half of item 3 are met here. The parent
  three-directive sweep on the merged pin (item 3's second half) belongs to the pin
  adoption, so the PR body says "Relates to #163".

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

## 8. Environment and method

- Pinned Verilator 5.050, ahead of the host default on PATH, through a scratch wrapper.
  The wrapper allows two `--build` invocations at once service-wide and turns their
  `--build -j 0` into `-j 2`. `MAKEFLAGS=-j8`, `VERILATOR_JOBS=2`, campaign drivers
  `--jobs 2`.
- The memory logger (20 s) reclaims page cache through the service's `memory.reclaim` when
  memory.current passes 8 GiB. Peak anonymous memory during the gate runs was 5.6 GB (the
  parent's lint fan-out); Vivado's OOC synthesis peaked at 10.2 GB anonymous and ran alone.
- Vivado ran only under the lock and never beside another job of this lane.
- No hardware, bench or flashing; no push, PR or comment other than TAKEN/REVIEW READY.

## 9. Retained evidence (scratch root; sizes and sha256)

Scratch root: `$VALIDATION_STORAGE/pp163-a553`. Scripts: `scripts/` (measure.py, stage.sh, export.sh, arb_paths.tcl, arb_cone.tcl, cone_summary.py, stage_paths.tcl, gates2.py, run_parent.py, patch_audit.py, txarb_mutants.py, compare_camps.py, memlog.sh, wait.sh, wait2.sh). Each gate run keeps a `.log`, `.rc` and command/time `.json` under `logs/base`, `logs/head` (`2ef802cb`), `logs/final` (`cd9825c9`) and `logs/parent-*`. The small evidence files are also copied into `evidence/` beside this handoff.

| Scratch-relative artifact | Bytes | sha256 |
|---|---:|---|
| `evidence/arbiter-equivalence.txt` | 320 | 56a0117007841c866b578ad6c208b59dbf24085f5bb5515894296dda8eb5f8d4 |
| `evidence/arbiter-standalone-levels-base.tsv` | 18958 | a01b06cc4cea9666de79f2d98acd7dda3d95e214a7b6187d0d4aa772e2f2a04f |
| `evidence/arbiter-standalone-levels-head.tsv` | 18953 | bdb82da04751159721a40885f2cd1cfa68e2f5d5ec7d1a52417f5ebb63a5f0d5 |
| `evidence/cone-summary-base-over20.txt` | 98928 | a5c7ee23b571f3b722053e997079d84b845608cba9e4b483a82c6a5c417608d0 |
| `evidence/cone-summary-head-all.txt` | 16459 | 58cc8133286563c8b2f55f6aef68e48801f4cc6c85f607cd61986e8b30646984 |
| `evidence/parent-diff.patch` | 1648 | ef03d745d30bcd624ce76a61d778d7d98dbfa2fbdd37b4540ee926fa0f3bda11 |
| `evidence/patch-audit-base.json` | 88 | 8f6f7008610fe65bf5d8a52336e1e0c4c583cb2a1ce56021d0e6cf3d797e8232 |
| `evidence/patch-audit-final.json` | 88 | f108fd46d3698c439cdaa23b96e09c25743dd50c5d27139c91fc7e379ac13add |
| `evidence/patch-audit-head.json` | 88 | 9d9412f1acc96da0540a686bdb5f57cb2b48f2bda9bd0e7e16378778518b476a |
| `evidence/pre-edit-grep-alltb.txt` | 515 | 18685df0ac73161c162af6619300f8f930b2bbf6878fb3945ecbd293f600944f |
| `evidence/pre-edit-grep.txt` | 589 | 66c8296db91cdbf9cd74c4d0103bfa369f036c94bb22fd024e94d3498cd50db5 |
| `evidence/rtl-old-lines.txt` | 554 | b4101fbcbaf0eeffb70bcab8722e0aac52abed2e21dd1b747680c17873af947e |
| `evidence/stage-paths-base.tsv` | 562 | 6d462ddec875a4c14568e03b1db303146aa77d78167db3921eaf1bf8c4bbfaf1 |
| `evidence/stage-paths-head.tsv` | 951 | f449b7f5d0745b093814ee56d06206bb26b6c9fa99c1bf4cd54985bc0e454d65 |
| `evidence/txarb-m1-m5-base.json` | 1085 | da93656a59b071291ecc1ed345fc610dc5eb79b51753c92f6500ab069150b535 |
| `evidence/txarb-m1-m5-head.json` | 1085 | da93656a59b071291ecc1ed345fc610dc5eb79b51753c92f6500ab069150b535 |
| `meas/paths-base/arb_cone.tsv` | 23794238 | f847be597785eacc0748770ee088ab56ffbbfefab46b6a37af23cbab47c7a132 |
| `meas/paths-base/arb_worst5.rpt` | 94864 | 5bd1965e1f417346aca683fbf8d9d234080cd79d24e22598ed0d831fa98af784 |
| `meas/paths-base/arb_deep5.rpt` | 96657 | 6159610327c57e38d6d6283540643a87aa52c1b97e7ddef556b5246cd158db32 |
| `meas/paths-base/arb_timing_summary.rpt` | 175884 | 390f5eac466068362bce9f35ebcd978cd9a580f678455f880950b1bb613f7846 |
| `meas/ooc-base/baseline_timing.rpt` | 175838 | aaf226628c53e1cf849a2e0acdf49fb5a7f44fece170b5dc02c00fcdbff0f0ad |
| `meas/ooc-base/baseline_hierarchy.rpt` | 10264 | a0892e836ee2f3393f5ef385a3ff092e1ad132d063fe151ba1d7d007269a1181 |
| `meas/ooc-base/baseline_synth.dcp` | 8906633 | d82658c001fe58f3c8eb3951ff3367ee623f3da872db310af11970a6154721ba |
| `meas/ooc-base/baseline_parameters.json` | 638 | 62cff771bc5f5552dccea38044605d4d146e039201a43993f95514c359538f4c |
| `meas/record-base.stdout` | 6945 | b583d463c9e7ce70b300c115f7b925c60d3e83ff5641ead47aacc989d881ed9d |
| `meas/gate-base.stdout` | 856 | f4e435b6625858d4727638dc95d0e73292662cffaa124d4ce87102a45ea5205b |
| `meas/paths-head1/arb_cone.tsv` | 1467745 | d859df8d7d8dc5993980804a35cb1f99101fa9656ed6e22a6f812069d4a83447 |
| `meas/paths-head1/arb_worst5.rpt` | 43261 | 25b8853af6b545aca2393a6f33f91b9d7cc03436a9c3df52fe13e06750850996 |
| `meas/paths-head1/arb_deep5.rpt` | 45343 | b30160923cdce7d404992639bd7c6772f32b154e5a9ca66b404e86329fd76a99 |
| `meas/paths-head1/arb_timing_summary.rpt` | 155738 | f7854dac2c73c637ed2402cd0bed3c316cb8da0475aa540b7b7a8054dc11673c |
| `meas/ooc-head1/baseline_timing.rpt` | 155691 | 8af230c3804166c7321679ae4b44c0f438f91d95c2fd59bfe4e34fb2faf582c6 |
| `meas/ooc-head1/baseline_hierarchy.rpt` | 10264 | 2b2e177b330cd354fc27dd77174a3e342885a2e0bde5aa666df33a24deeab7a8 |
| `meas/ooc-head1/baseline_synth.dcp` | 8896835 | 158c11f359d9d5163cce8a48a839686af0664100576c7abd41c84e8abf46f183 |
| `meas/ooc-head1/baseline_parameters.json` | 638 | 62cff771bc5f5552dccea38044605d4d146e039201a43993f95514c359538f4c |
| `meas/record-head1.stdout` | 6944 | 0aa0e19eeec986168f27e860b8e2556fe570bc28e4aa652446bf61bbcf92111e |
| `meas/gate-head1.stdout` | 862 | 538a97c7863f0c74b609be7e1bdfb697caf017b858b62bb7cac9136db0715cf2 |
| `logs/base/suites.log` | 1750 | df917fd7f7c567301910a597e0d8b8f4fb8f6423c269b6dace013323b7d5e751 |
| `logs/base/check.log` | 410 | 4988bca941797441c2381dcd8f2a89caa2d9efe1b1b89cedecedfd2cf2cbf9d7 |
| `logs/base/lint.log` | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |
| `logs/base/matrix.log` | 33 | 7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097 |
| `logs/base/yosys.log` | 3548 | 5918894aeb86257a2ba105f0914f534c8ab77338863151178375bed543a51a82 |
| `logs/base/camp-notify.log` | 4605 | 561658100a8cdf3a4aafcfe5ad13501ad478e59fc1227133a59066344769bfce |
| `logs/base/camp-d3.log` | 8131 | 64ff44059ffa0c9d990ef26621d85cf8c6f1278329aa7f1c47d929b0ed7f537d |
| `logs/base/camp-aecp.log` | 78512 | 53d881784de32314b33d1e973813dacb1f3d85468dc2d1e6e94b1efe1d5ab698 |
| `logs/base/camp-aecp_dispatch.log` | 28893 | 0dd8b97ab8f9a89f6dad0388f0e6c83eb7bd37eb5a6f5bf47eda9954ff4222f6 |
| `logs/base/camp-acmp.log` | 2904 | 16c1e07d5077b54ba84a5d7e187ecacd3a9cf3622d6fa6c221fe3427365e1963 |
| `logs/base/camp-gsi.log` | 4150 | 5f6d67707db7bfed9d8aa1e323a7f3b0884134404c78e43b0b2afbd99953237b |
| `logs/base/camp-ctr.log` | 11207 | dcd55eac8ffb06c36b2366e59a0ef5c517271e7751a3e948aa650dcffa178570 |
| `logs/base/camp-name_wr.log` | 2550 | 055560a7d55d359d9281385f1d47fcddba0b082ac963195a2ce4201fdd4efe7a |
| `logs/base/camp-adp.log` | 33445 | f69c577b96367e850478d3068e7bca2d77be103f747ff6e9bd1cceec8485e95e |
| `logs/base/camp-maap.log` | 7591 | 823ef7e638f720b03e151b4954e75a5b023fa034efda1171f57264a208ff3c81 |
| `logs/base/camp-srp_top.log` | 9988 | ec920575b69b9fccc7fa3d0a279308d3465887cc59c7c5747aea6a374be00467 |
| `logs/base/camp-srp_admission.log` | 479 | 6977d367d954c85cbb07f2f44ac0fb7a5ab3267f627556647a22a1bf95b798fc |
| `logs/base/camp-retry.log` | 3865 | 7bda8adf83703e45161d30a04b76f39855701cbb5b9b7c1979473aa7ba6c2512 |
| `logs/head/suites.log` | 1750 | db2b89a5fc8c41c9f40f791c12e5713560694cefbdb2a19d6ef64600d4922bfb |
| `logs/head/check.log` | 410 | ad4d29d74bf789a44ee31cc6398be449e4d465735b95f3bb8c25564c62e8b2bb |
| `logs/head/lint.log` | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |
| `logs/head/matrix.log` | 33 | 7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097 |
| `logs/head/yosys.log` | 3548 | bee608b28b73fa2fa502b40b30dbdeada7560af46bd0a21f0bece4b3ca0b23fb |
| `logs/head/camp-notify.log` | 4883 | 7312611052d60315c351cfcd62143efe69b7b79f5a5f4516381435a2560718c9 |
| `logs/head/camp-d3.log` | 8131 | d78468b85c9902d16b9e35c883312ecccd10650b0dc23ffd8177e4c9914ab36b |
| `logs/head/camp-aecp.log` | 78512 | 53d881784de32314b33d1e973813dacb1f3d85468dc2d1e6e94b1efe1d5ab698 |
| `logs/head/camp-aecp_dispatch.log` | 28893 | 0dd8b97ab8f9a89f6dad0388f0e6c83eb7bd37eb5a6f5bf47eda9954ff4222f6 |
| `logs/head/camp-acmp.log` | 2904 | da12ea3006e0fe79e1cc637417ba9cb195e02b550523b5a4eb2fc376de19fc85 |
| `logs/head/camp-gsi.log` | 4150 | 5f6d67707db7bfed9d8aa1e323a7f3b0884134404c78e43b0b2afbd99953237b |
| `logs/head/camp-ctr.log` | 11207 | dcd55eac8ffb06c36b2366e59a0ef5c517271e7751a3e948aa650dcffa178570 |
| `logs/head/camp-name_wr.log` | 2550 | 055560a7d55d359d9281385f1d47fcddba0b082ac963195a2ce4201fdd4efe7a |
| `logs/head/camp-adp.log` | 33445 | f69c577b96367e850478d3068e7bca2d77be103f747ff6e9bd1cceec8485e95e |
| `logs/head/camp-maap.log` | 7591 | 823ef7e638f720b03e151b4954e75a5b023fa034efda1171f57264a208ff3c81 |
| `logs/head/camp-srp_top.log` | 9988 | ec920575b69b9fccc7fa3d0a279308d3465887cc59c7c5747aea6a374be00467 |
| `logs/head/camp-srp_admission.log` | 479 | 6977d367d954c85cbb07f2f44ac0fb7a5ab3267f627556647a22a1bf95b798fc |
| `logs/head/camp-retry.log` | 3865 | 7bda8adf83703e45161d30a04b76f39855701cbb5b9b7c1979473aa7ba6c2512 |
| `logs/final/suites.log` | 1750 | db2b89a5fc8c41c9f40f791c12e5713560694cefbdb2a19d6ef64600d4922bfb |
| `logs/final/check.log` | 410 | ad4d29d74bf789a44ee31cc6398be449e4d465735b95f3bb8c25564c62e8b2bb |
| `logs/final/lint.log` | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |
| `logs/final/matrix.log` | 33 | 7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097 |
| `logs/final/yosys.log` | 3548 | bee608b28b73fa2fa502b40b30dbdeada7560af46bd0a21f0bece4b3ca0b23fb |
| `logs/final/camp-notify.log` | 4883 | 44b7646ab978406dd9d2910cec7f27da2525559a5c93ff0e6032622ab33ea55d |
| `logs/final/camp-d3.log` | 8131 | edaf2137c3bb27ae3aaad71228fca4d9fa7324562e36afdbab85556b1432a50e |
| `logs/final/camp-aecp.log` | 78512 | 53d881784de32314b33d1e973813dacb1f3d85468dc2d1e6e94b1efe1d5ab698 |
| `logs/final/camp-aecp_dispatch.log` | 28893 | 0dd8b97ab8f9a89f6dad0388f0e6c83eb7bd37eb5a6f5bf47eda9954ff4222f6 |
| `logs/final/camp-acmp.log` | 2904 | c670e10aaf6a258f7f11d11b168c11840913b288dc60c295d5e65c4ef96de163 |
| `logs/final/camp-gsi.log` | 4150 | 5f6d67707db7bfed9d8aa1e323a7f3b0884134404c78e43b0b2afbd99953237b |
| `logs/final/camp-ctr.log` | 11207 | dcd55eac8ffb06c36b2366e59a0ef5c517271e7751a3e948aa650dcffa178570 |
| `logs/final/camp-name_wr.log` | 2550 | 055560a7d55d359d9281385f1d47fcddba0b082ac963195a2ce4201fdd4efe7a |
| `logs/final/camp-adp.log` | 33445 | f69c577b96367e850478d3068e7bca2d77be103f747ff6e9bd1cceec8485e95e |
| `logs/final/camp-maap.log` | 7591 | 823ef7e638f720b03e151b4954e75a5b023fa034efda1171f57264a208ff3c81 |
| `logs/final/camp-srp_top.log` | 9988 | ec920575b69b9fccc7fa3d0a279308d3465887cc59c7c5747aea6a374be00467 |
| `logs/final/camp-srp_admission.log` | 479 | 6977d367d954c85cbb07f2f44ac0fb7a5ab3267f627556647a22a1bf95b798fc |
| `logs/final/camp-retry.log` | 3865 | 7bda8adf83703e45161d30a04b76f39855701cbb5b9b7c1979473aa7ba6c2512 |
| `camp/base/camp-notify/results.json` | 108474 | 20944a574eae961e9ff19ee5da60c9496ed8d0c3068cf5038521f44cb775bedb |
| `camp/base/camp-d3/results.json` | 155047 | 17f15ea2380a1ba3ecb84bb0876a1433825cbba2f57b977e2eaffc928f6f4d2f |
| `camp/base/camp-acmp/results.json` | 96457 | f21adc920863fd17d46e096d1799fb7134bb140c0ac1e11790eca49c8ba7bea0 |
| `camp/base/camp-aecp_dispatch/results.json` | 7629 | f82db07ae244a5947b85a1b3c55b8afb4930eba7267667179945155db01c5167 |
| `camp/head/camp-notify/results.json` | 110558 | dd5a904ddbbbef908591f6182eaf47ddef8415521bbe2f08d8477f2bd2f0b523 |
| `camp/head/camp-d3/results.json` | 155047 | bfc74e3034cd9e59531a2430057852ab8843f4df1ae9be5a71c8f856e1296e40 |
| `camp/head/camp-acmp/results.json` | 96457 | 10ce2ad4196ff1e3919ceec4b07c663966464578d7d2db9ae4706bd53158136b |
| `camp/head/camp-aecp_dispatch/results.json` | 7629 | f82db07ae244a5947b85a1b3c55b8afb4930eba7267667179945155db01c5167 |
| `camp/final/camp-notify/results.json` | 110558 | 38a8d4255f840468aa64213ce1d66a4c3e72c77c9dfe9e027c14fc0691546a54 |
| `camp/final/camp-d3/results.json` | 155047 | 543192023b2940a82fb4cb3d4d43da9ab822e4ecb17bec6cb884702288db2b90 |
| `camp/final/camp-acmp/results.json` | 96457 | 5ba1a4604dfd9a3996963d42f701178cff49054acd01fd821cdd705f2764d0ba |
| `camp/final/camp-aecp_dispatch/results.json` | 7629 | f82db07ae244a5947b85a1b3c55b8afb4930eba7267667179945155db01c5167 |
| `logs/parent-base/01_cpp.log` | 315 | 20d9e296340ae6319c913211b7a2b7d63b6cc89798c011092c87908916634810 |
| `logs/parent-base/02_py.log` | 461 | f88c9566c9b5ef80cc54f722065566445a1849097ba87a7c50f07f2be6ecf0c6 |
| `logs/parent-base/03_sources.log` | 153 | ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95 |
| `logs/parent-base/04_pp_sources.log` | 955 | fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a |
| `logs/parent-base/05_ports.log` | 421 | b04fbab06614655f710f529fa8d2cdbd59073e9a63f179b308734b9e21f35c23 |
| `logs/parent-base/06_naming.log` | 36608 | db23d3d49d070f855b77fbe71e83f3cc24b00ae81d2c288082eb016ac2820e77 |
| `logs/parent-base/07_evidence.log` | 13902 | bb9aadc07a14eb4e219e87fa681571c7886f1ef0be545cbae69d099b66fd7f44 |
| `logs/parent-base/08_docs.log` | 127 | 6a6b0baa714d34c94d863882cab86a5eac8309164fc1a6c99cb5659f049510ee |
| `logs/parent-base/09_xvlog.log` | 721 | 764444287ab24c7e9a58eae8261d5ee31e46da0ca6e59798c254107bef0a47c3 |
| `logs/parent-base/10_builder.log` | 101822 | 0b6afed831b34f10a78416a619988086839f37805d03af5fc5082c5d1657d0c3 |
| `logs/parent-base/11_lint.log` | 14186 | 9087b44973869192bcab894931d990c7976fb895a8d92b6c243c555087f69d6e |
| `logs/parent-base/12_shadow.log` | 276059 | 6a48c4ea0e1210f146e6c42bec83dd02a1b9ca595e0122e0b29b440a0ed4f3ee |
| `logs/parent-base/13_nvm_lint.log` | 29864 | b7bfe3b4cf82fd4b2cba2f271aa60c8463295dbc91bd0e3c6974780b50e3f276 |
| `logs/parent-base/14_nvm_quick.log` | 394 | cb802d0dfa07167eca0a998f0c041397eedf41d13b79f86c5090bc932b00c174 |
| `logs/parent-base/15_datapath.log` | 1951604 | 135b056afc3372be44b8036064b1ad3b2c81c059d9091fab33edb49f62bd14df |
| `logs/parent-base/16_render.log` | 156092 | e5f13d743645e338156ad940e80a54f44395cdfdd159337f9f0a3609c270d74c |
| `logs/parent-base/17_shell.log` | 235 | 7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9 |
| `logs/parent-head/01_cpp.log` | 315 | 20d9e296340ae6319c913211b7a2b7d63b6cc89798c011092c87908916634810 |
| `logs/parent-head/02_py.log` | 461 | e69f71258598b816549611332bba555ed3bfd91bf372cc7291568a2ee9870c2e |
| `logs/parent-head/03_sources.log` | 153 | ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95 |
| `logs/parent-head/04_pp_sources.log` | 955 | fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a |
| `logs/parent-head/05_ports.log` | 421 | 774375e7ac9c65d58d1828460de6529193dc26a096daa71c548e214bb3404380 |
| `logs/parent-head/06_naming.log` | 36608 | db23d3d49d070f855b77fbe71e83f3cc24b00ae81d2c288082eb016ac2820e77 |
| `logs/parent-head/07_evidence.log` | 13902 | bb9aadc07a14eb4e219e87fa681571c7886f1ef0be545cbae69d099b66fd7f44 |
| `logs/parent-head/08_docs.log` | 127 | 6a6b0baa714d34c94d863882cab86a5eac8309164fc1a6c99cb5659f049510ee |
| `logs/parent-head/10_builder.log` | 101822 | bca8346974b814e489bd69f28d3c994ffd1fad535a745e7250bcd1d01030117e |
| `logs/parent-head/11_lint.log` | 14186 | 9087b44973869192bcab894931d990c7976fb895a8d92b6c243c555087f69d6e |
| `logs/parent-head/12_shadow.log` | 273214 | 0f2901c31d7216d22e49be11a2f50dedf1cc4616f3fb8cc0b396f156c64dc339 |
| `logs/parent-head/13_nvm_lint.log` | 29864 | 849367624676a1ad5458ab831f0fff82337c9d532cde64d5a213db58801a8430 |
| `logs/parent-head/14_nvm_quick.log` | 394 | cb802d0dfa07167eca0a998f0c041397eedf41d13b79f86c5090bc932b00c174 |
| `logs/parent-head/15_datapath.log` | 1949053 | 52b52e94554f8ad5435791b3444250d337a564c68c6344e3e5230d430bb4bd0b |
| `logs/parent-head/16_render.log` | 155211 | d9d30767301c23059aea90c01b1360e0d731b5157ceae310e19dd072f6007d8b |
| `logs/parent-head/17_shell.log` | 235 | 7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9 |
| `logs/parent-final/01_cpp.log` | 315 | 20d9e296340ae6319c913211b7a2b7d63b6cc89798c011092c87908916634810 |
| `logs/parent-final/02_py.log` | 461 | e69f71258598b816549611332bba555ed3bfd91bf372cc7291568a2ee9870c2e |
| `logs/parent-final/03_sources.log` | 153 | ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95 |
| `logs/parent-final/04_pp_sources.log` | 955 | fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a |
| `logs/parent-final/05_ports.log` | 421 | 774375e7ac9c65d58d1828460de6529193dc26a096daa71c548e214bb3404380 |
| `logs/parent-final/06_naming.log` | 36608 | db23d3d49d070f855b77fbe71e83f3cc24b00ae81d2c288082eb016ac2820e77 |
| `logs/parent-final/07_evidence.log` | 13902 | bb9aadc07a14eb4e219e87fa681571c7886f1ef0be545cbae69d099b66fd7f44 |
| `logs/parent-final/08_docs.log` | 127 | 6a6b0baa714d34c94d863882cab86a5eac8309164fc1a6c99cb5659f049510ee |
| `logs/parent-final/09_xvlog.log` | 721 | 38138808e435728c8d32be1f3dabe801b8271e08e30edb5df7bdd79df0757fba |
| `logs/parent-final/10_builder.log` | 101822 | 9d84bbc6a4e2ae5cad10ea22bd7ff027c58d6de7166d50d325abe4d0ae4d76a4 |
| `logs/parent-final/11_lint.log` | 14186 | 9087b44973869192bcab894931d990c7976fb895a8d92b6c243c555087f69d6e |
| `logs/parent-final/12_shadow.log` | 273214 | aba35820297764884f80b1d66b34b434fa30957955dba537b433e9f66bfd9c86 |
| `logs/parent-final/13_nvm_lint.log` | 29864 | 1c9a26a8fa9b575506a1af900dbfb2653291af049608c20a6a745f87650d46f0 |
| `logs/parent-final/14_nvm_quick.log` | 394 | cb802d0dfa07167eca0a998f0c041397eedf41d13b79f86c5090bc932b00c174 |
| `logs/parent-final/15_datapath.log` | 1949056 | e66dc7a14fed57ff9aafe738cd71a35946b654e5a73694b7143ee91864c74713 |
| `logs/parent-final/16_render.log` | 155211 | 980b9675c2c29a2689eeae4041061411475489ca6b3cb5d0d70dd1e3182ec101 |
| `logs/parent-final/17_shell.log` | 235 | 7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9 |

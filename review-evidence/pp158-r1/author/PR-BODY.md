[A541]

Closes #158

This is the #158 lane (assignment: #158 comment 5991577974; area ruling: #158 comment 5997990838). Branch `pp158-dereg-round`
is cut from `main` `054d01c7`, with #148 merged. `main` `21c6f709` (C11, PR #156) is merged in with `--no-ff`.
Head: `79571006b803a4ab4af65358f0d87bc3af73180e`.

**Area: within the limit, as ruled.** The 40 LUT / 60 FF limit counts the change's own logic. Variance in modules whose RTL did
not change is recorded, not counted (section 5).
- Own logic: `KL_aecp_notify` synthesized alone moves **-3 LUT / +2 FF**; its `u_notify` row in the 1x1 build moves -1 LUT / -3 FF.
- Whole OOC 1x1 `KL_pp_shadow` delta: **+50 LUT / -6 FF**, all of the LUT growth in rows whose RTL is unchanged (per-row table in
  section 5).

`KL_aecp_notify` drains a parked registry expiry between two jobs of a notification round. The expiry is a TIME_LIMITED
expiry or a failed CONTROLLER_AVAILABLE retry. Draining latches the expired controller's own DEREGISTER notification. The
DEREGISTER was emitted at once, and its single-shot job rewrote `em_kind_r`, `em_dt_r`, `em_di_r` and `em_arg0/1_r`. Nothing
restored them, so every remaining controller of the round received a DEREGISTER_UNSOLICITED_NOTIFICATION (kind 0, descriptor
0000:0) instead of the round's notification.

The drained DEREGISTER now waits for the round's boundary. That is one gate on an existing condition. The round's remaining jobs
keep its notification. The expired controller still receives its own DEREGISTER, with the same tuple, sequence_id and frame,
right after the round. No port, parameter or register changes.

| Commit | Item |
|---|---|
| `5343cd7` | 1, red first: `tb/aecp_notify` section DR (bench only). It fails on `main`'s RTL |
| `27992ce` | 2, the fix: `KL_aecp_notify.sv` (+7 -3, one logic line) and 06 section 7 |
| `3dbc229` | The three controls in `tb/pp_top/notify_mutants.py` |
| `e3c9f0b` | The READMEs, 09 section 8.4, and a reflow of the 06 paragraph |
| `7957100` | Merge of `main` `21c6f709` (C11): docs, scripts, and comment-only edits to three RTL files and one bench. No conflicts |

## 1. Red first

`5343cd7` adds section DR to `tb/aecp_notify`. Its `KL_aecp_notify.sv` is byte-identical to `main`'s. `make run`: rc 2,
`[build default] 41 checks, 3 failures`.

```
  [i] DR1: after the drain, ms 20009: kind 0, 0000:0, args 0/0, seq 1, to 020000000003
  [i] DR1: after the drain, ms 20013: kind 0, 0000:0, args 0/0, seq 0, to 020000000004
FAIL: DR1: in a GET_COUNTERS round on 0009:0, C's registration expires while its job waits, and the round's remaining controller D still receives the round's GET_COUNTERS 0009:0 (2 jobs after the drain)
  [i] DR2: after the drain, ms 25008: kind 0, 0000:0, args 0/0, seq 1, to 020000000003
  [i] DR2: after the drain, ms 25012: kind 0, 0000:0, args 0/0, seq 0, to 020000000004
FAIL: DR2: in a SET_NAME round on 0005:1 (arguments 2 and 3), C's CONTROLLER_AVAILABLE retry fails while its job waits, and the round's remaining controller D still receives the round's notification (2 jobs after the drain)
  [i] DR3: the job after the drain (kind 0 to 020000000003) sent at ms 31504; D's GET_COUNTERS sent at ms 31513 and next presented at ms 0
FAIL: DR3: C's registration expires in a GET_COUNTERS round, the job after the drain waits for the TX slot until ms 31504 and a change arrives at ms 30104: D's GET_COUNTERS sent at ms 31513, the next at ms 0, want 32513 to 32521 (1 of D's GET_COUNTERS seen)
```

DR1 is the issue's probe as a standing check. It reproduces the published trace: C gets its DEREGISTER at seq 1, and D gets
kind 0, 0000:0 at seq 0. DR1b and DR2b (C's own DEREGISTER) pass on `main`.

## 2. The fix (`hdl/aecp/KL_aecp_notify.sv`)

- `:1253`: `if (dh_v_r) begin` becomes `if (dh_v_r && !em_active_r) begin`.
  - While a round is active, `N_IDLE` takes the round's next job through the existing arm (`wk_ix_r <= em_ix_r`), so the round's
    `em_*` state is never rewritten mid-round.
  - When the round ends (`em_active_r` falls in `N_EMIT_WB` or `N_EMIT_RD`), the DEREGISTER arm is checked first, as before. So
    the held DEREGISTER goes out before any new round is claimed.
- `:1254-1257` (the arm's comment) and `:129-130` (the banner's DEREGISTER sentence). 06 section 7 gains one sentence
  (`docs/architecture/06_aecp_engine.md:887-889`).

**Why a hold, not save/restore.** The assignment allows either. Saving and restoring `em_kind_r`, `em_dt_r`, `em_di_r` and
`em_arg0/1_r` takes 68 flops, which alone exceeds the 60 FF stop. The hold adds no state.

**The targeted controller's own DEREGISTER is unchanged.** It still goes to that controller alone, with the tuple and
sequence_id latched at drain (`dh_*`): kind 0, descriptor 0000:0, arguments 0, the same `em_*` constants and the same frame.
Only its time moves. It used to go right after the drain; now it goes right after the round's remaining jobs, at most
`P-N-CONTROLLERS` - 1 jobs later.

**#148's rule and R477-1 S2 (PR #159).** No DEREGISTER job runs inside a round now. So the GET_COUNTERS stamp follows every job
of the round to its send (`:1449`), and there is no interleaved job to stop that follow. DR3 grades this with a TW-style
scenario:
- C's registration expires in a GET_COUNTERS round;
- the job after the drain waits 1.5 s for the TX slot;
- a change arrives during the wait.

D's next GET_COUNTERS must then be presented 1,000 to 1,008 ms after D's own send. At the head it is presented 1,004 ms after.
The control `dereg_pending_stops_follow` stops the follow while the DEREGISTER is pending, which is S2's hazard in this design.
It fails DR3: D's next notification comes 8 ms after D's send.

## 3. Tests and controls

`tb/aecp_notify` section DR (`sim_main.cpp:540-702`) has 11 checks: five named checks plus six REGISTER checks. The bench is the
engine, as in TW, with C in row 0 and D in row 1. The checks accept D's job and C's DEREGISTER in either order. They grade the
round's notification and the DEREGISTER's own semantics, not the order the fix chose.

| Check | Scenario | Head | Failed by |
|---|---|---|---|
| DR1 | GET_COUNTERS round on 0009:0; C's TIME_LIMITED registration expires while C's job waits; D still gets GET_COUNTERS 0009:0 | D at ms 20010 | `dereg_mid_round_no_hold` |
| DR1b | C alone gets its own DEREGISTER (kind 0, 0000:0, seq 1), once | C at ms 20013 | `dereg_lost_at_round_end` |
| DR2 | SET_NAME round on 0005:1 with arguments 2 and 3; C's CONTROLLER_AVAILABLE retry fails while C's job waits; D still gets every field of it | D at ms 25009 | `dereg_mid_round_no_hold` |
| DR2b | as DR1b | C at ms 25012 | `dereg_lost_at_round_end` |
| DR3 | TW with the drain (R477-1 S2), above | 31504, then 32508 | `dereg_mid_round_no_hold`, `dereg_pending_stops_follow`, #148's three TW controls |

| Control (`notify_mutants.py:330-353`) | Planted | Failing checks |
|---|---|---|
| `dereg_mid_round_no_hold` | `if (dh_v_r) begin` (`main`'s rule: the mutant without the restore) | 3: DR1, DR2, DR3 |
| `dereg_pending_stops_follow` | the stamp's follow gated `&& !dh_v_r` | 1: DR3 |
| `dereg_lost_at_round_end` | the round's last write-back also clears `dh_v_r` | 2: DR1b, DR2b |

These are the failures at the merged head `7957100`, and they match the ones at `e3c9f0b5`.

## 4. Planting (item 3)

**Before the edit.** Each changed line of `KL_aecp_notify.sv`, and the line on each side of it (`:128-130`, `:1251-1254` at
`5343cd7`), was searched with `git grep` across `tb/**/*.patch` and every `tb/**/*.py` mutant table. There were no matches, and
no reviewed patch has a hunk near either edit. The merge makes no notify edit: C11 does not touch `KL_aecp_notify.sv`, and no
arm names a file C11 changed.

**Every arm plants at the merged head `7957100`.**
- Every `tb/**/*.patch` (through `git apply --check` at an extraction root) and every exact-text arm of the notify, d3 and acmp
  drivers (through the driver's own `plant()`): **476 of 476**. That is the same list as at `e3c9f0b5`: 473 at base, plus the
  three new controls. At `main` `21c6f709`: 473 of 473.
- The exact-text arms of the other text-planting drivers, each under its driver's own anchor-count rule: **96 of 96** at
  `7957100`, `21c6f709`, `e3c9f0b5` and `054d01c7`. The count is `tb/acmp_talker/retry_mutants.py` (70 mutations and its two
  bench probes), `gsi_mutants.py` (20), `name_wr_mutant.py` (1) and `tb/srp_admission/mutants.py` (3). (`tb/desc_store`'s
  lint mutations edit descriptor models, not sources.)
- All 54 arms that plant into `KL_aecp_notify.sv` plant the same design at base and head: the ten patches, 42 notify arms and
  2 d3 arms. In each case, the lane's RTL diff applied to the planted base file gives the planted head file byte for byte.
  The merge leaves `KL_aecp_notify.sv` and every arm's table byte-identical, so this holds at `7957100`.
- The notify driver at `7957100`: 56 of 56 KILLED, 7 goldens PASS. All 64 per-arm records are identical to the ones at
  `e3c9f0b5`.

## 5. Area: OOC 1x1 (#638's recipe), within the limit

Measured in a scratch parent at milan-fpga dev `fa450d30` with the c8, p2-p1, c10, 232 and 148 patches. Vivado 2026.1,
`xc7a100t-fgg484-2`; the RTL elaboration served as the integrated log; `--integrated-clock` (20 ns). Every Vivado run held
`flock $VIVADO_LOCK`, and nothing else of the lane ran meanwhile. Parameters and every image hash are identical at base
and head.

| `KL_pp_shadow` standalone 1x1 | LUT | FF | RAMB36 / 18 | DSP |
|---|---:|---:|---:|---:|
| base `054d01c7` | 23,161 | 19,783 | 16 / 3 | 8 |
| head `e3c9f0b5` | 23,211 | 19,777 | 16 / 3 | 8 |
| **whole delta** | **+50** | **-6** | 0 | 0 |

**Own logic (what the limit counts, per the ruling).**

| Measure | LUT | FF |
|---|---:|---:|
| `KL_aecp_notify` synthesized alone (1x1 binding, `AreaOptimized_high`, out of context): base 2,474 / 1,280, head 2,471 / 1,282 | **-3** | **+2** |
| its `u_notify` row in the 1x1 build: base 2,169 / 1,259, head 2,168 / 1,256 | -1 | -3 |

The module-alone base figures equal #148's measured head.

**Per-row table** (`baseline_hierarchy.rpt`, every row under `u_pp` that moved). Only `u_notify` has changed RTL.

| Row (module) | dLUT | dFF | RTL changed? |
|---|---:|---:|---|
| `u_notify` (`KL_aecp_notify`) | -1 | -3 | **yes** (the one gate) |
| `u_tx_slots` (`KL_pp_tx_slots`) | +121 | 0 | no |
| `u_timer` (`KL_pp_timer_service`) | +44 | 0 | no |
| `u_srp` (`KL_srp_top`: `u_admission` +17, `u_encoder` +14, `u_talker` +2, own +1, `u_listener` -2, `u_domain` -1, `u_vlan` -1) | +30 | 0 | no |
| `u_dispatch` (`KL_pp_dispatch`: `u_acmp_q` +12, `u_maap_q` +7, own +6, `u_adp_q` +1, `u_aecp_q` -7) | +19 | 0 | no |
| `u_originator` (`KL_pp_originator`) | +14 | 0 | no |
| `u_tx_arbiter` (`KL_pp_tx_arbiter`) | +6 | 0 | no |
| `u_listener` (`KL_pp_acmp_listener`), `u_prng` (`KL_pp_prng`) | +2, +2 | 0 | no |
| `u_aecp` (`KL_aecp_engine`: `u_ucpu` +11, `u_dyn` -8, own -5, `u_resp` -3) | -5 | 0 | no |
| `u_talker` (`KL_acmp_talker`), `u_adp` (`KL_adp_engine`), `u_nvm_shadow` (`KL_acmp_nvm_shadow`) | -5, -4, -1 | 0 | no |
| `u_ca_builder`, `u_trace`, `u_maap`, `u_rx_validator`, `u_scoreboard`, `u_normalizer` | -8, -10, -15, -16, -17, -27 | 0 | no |
| `u_pp` own logic (`protocol_processor_top`) | -79 | -1 | no |
| **`u_pp` total** | **+50** | **-4** | |
| `KL_pp_shadow` own logic | 0 | -2 | no |

These are the rebuilt hierarchy's cross-boundary moves. The head log also has 12 fewer `Synth 8-3917` warnings on the top's glue
partition. #638's gate passes at base and at head (rc 0, "re-baseline recommended"). There is no `Synth 8-7186` or `Synth 8-4445`
diagnostic.

**Not re-measured after the merge.** C11 changes three RTL files (`KL_pp_side_port.sv`, `KL_pp_trace_ring.sv`,
`KL_pp_tx_slots.sv`) and only in comments. The preprocessor's comment-stripped output of each is byte-identical at `e3c9f0b5`
and `7957100`. Line counts are unchanged too. So every synthesis and simulation input of this measurement is the same at the
merged head.

## Validation

Everything below is rc 0 unless stated. Runs used the pinned Verilator 5.050 in `git archive` extractions. `make check`,
`make ids` and `gen_matrix.py` ran in the tree at each revision, because they read git.

**After the merge: base `main` `21c6f709`, head `7957100`.** Following the ruling, these re-run what C11 feeds (docs, scripts,
comment-only RTL and bench edits), plus the planting and the assignment's named campaigns.

| Gate | Base `21c6f709` | Head `7957100` |
|---|---|---|
| `make ids` | 30 self-test cases; 531 files, 91 IDs, 47 P-IDs, 36 T-IDs, OK | identical |
| `make check` (Mermaid and WaveDrom lint, WaveDrom freshness, links, both matrices, parameters, IDs, figures, staleness) | 41 Mermaid + 18 WaveDrom blocks; 1,168 links; 115 REQ, 17 GAP; 94 rows, 0 untested; 28 parameters; 17 figure self-test cases, 3 draw.io + 18 WaveDrom + 5 hand-authored | identical |
| `scripts/gen_matrix.py --check` | 94 rows, 0 untested | identical |
| `./scripts/run_suites.sh` | 33 suites, 1,021,640 checks; log byte-identical to `054d01c7`'s | 33 suites, 1,021,651 checks (`aecp_notify` 45); log byte-identical to `e3c9f0b5`'s |
| `tb/pp_top` `make` (six builds) | 10,444 | the same; graded lines identical to each other and to round 1 |
| `tb/aecp_notify` `make` | 34 | 45 |
| `./scripts/lint_hdl.sh` | 41 of 41 | 41 of 41; logs byte-identical to round 1 |
| `./syn/yosys/run.sh` | 42 tops, `all.v` parsed once | byte-identical to base and to round 1 |
| `notify_mutants.py` (2 jobs) | 53 of 53 KILLED, records identical to `054d01c7`'s | 56 of 56 KILLED, records identical to `e3c9f0b5`'s; the base-to-head difference report is byte-identical to round 1's |
| `ctr_mutants.py` (2 jobs) | control PASS, 17 of 17 KILLED | the same; driver logs and 18 of 18 per-arm files identical, at both and to round 1 |
| Parent gates 1-8, 3b, 11, 13 | rc 0 | rc 0; identical except the Python line count (200,087 to 200,111, `notify_mutants.py` +24) and gate 13's Verilator timing lines |
| Parent gates 12, 14 (`pp_shadow`, `nvm_cosim quick`) | legs 606, 606, 646, 311, 0 failures; 315 of 315 | the same |
| Parent gate 9 (`flock $VIVADO_LOCK scripts/xvlog_gate.py --check`) | PASS, 2 findings == ratchet | the same; logs identical but for the pinned sha |

The other campaigns (d3, aecp, aecp_dispatch, acmp, gsi, name_wr, adp, maap) and parent gates 10, 15 and 16 were not re-run.
Their inputs at the merged head differ from round 1's only by the comment-only RTL edits above, and every one of their arms
plants (section 4).

**Round 1: base `054d01c7`, head `e3c9f0b5`.**

| Gate | Base `054d01c7` | Head `e3c9f0b5` |
|---|---|---|
| `./scripts/run_suites.sh` | 33 suites, 1,021,640 checks | 33 suites, 1,021,651 checks. `aecp_notify` goes from 34 to 45 (DR +11); every other suite's tally is identical |
| `tb/pp_top` `make` (six builds) | 10,444 | the same; the full logs are byte-identical |
| `tb/aecp_notify` `make` | 34 | 45; the full logs differ only in the five DR `[i]` lines and the tallies |
| `./scripts/lint_hdl.sh` | 41 of 41 | 41 of 41; identical log |
| `./syn/yosys/run.sh` | 42 tops, `all.v` parsed once | byte-identical log |
| `make check`, `scripts/gen_matrix.py --check` | 1,136 links; 115 REQ, 17 GAP; 94 rows, 0 untested; 28 parameters | identical logs |

**Campaigns.** These are every campaign that builds a changed file: the eight `tb/pp_top` drivers, plus the `tb/pp_top` arms of
`tb/adp_engine` and `tb/maap`. Each ran at base and head. Records were compared arm by arm: the verdict, every failing check,
and every `[i]` figure.

| Driver (`--jobs`) | Base | Head | Records |
|---|---|---|---|
| `notify_mutants.py` (2) | 53 of 53 KILLED, 7 goldens PASS | 56 of 56 KILLED, 7 goldens PASS | 57 of 60 identical. Three TW controls add DR3 (below); three controls are new |
| `ctr_mutants.py` (2) | control PASS, 17 of 17 KILLED | the same | driver logs byte-identical |
| `d3_mutants.py` (3) | 110 of 110 KILLED, 6 goldens PASS | the same | 116 of 116 identical |
| `aecp_mutants.py` (2) | 6 controls PASS, 61 KILLED | the same | 67 of 67 identical |
| `aecp_dispatch_mutants.py` (2) | 4 controls PASS, 40 KILLED | the same | 44 of 44 identical |
| `acmp_mutants.py` (2) | 33 of 33 KILLED, goldens PASS | the same | 37 of 37 identical |
| `gsi_mutants.py` (2), `name_wr_mutant.py` | 20 detected; decode killed; goldens and restored PASS | the same | identical |
| `tb/adp_engine/mutants.py` (2), `tb/maap/mutants.py` (2) | 2 + 41 and 3 + 29 PASS | the same | 43 and 32 identical |

The only record moves are the new check's. `counter_spacing_from_selection_tw` goes from 2 to 3 failing checks,
`counter_stamp_at_send_only` from 1 to 2, and `counter_stamp_first_job_only` from 2 to 3. Each keeps its TW failures exactly
and adds DR3 (D's next notification at ms 31512, 8 ms after D's send), because none of them follows D's wait after the drain.

Every other notify arm that runs `tb/aecp_notify` differs only by the five DR `[i]` lines and its build tally. In the d3 and
aecp_dispatch logs, the unbound `%d` at `d3_phases.hpp:2963` and `:2993` prints garbage at base and head alike, as before.
That integer is masked in the comparison.

**Parent consumer set (17)** at milan-fpga dev `fa450d30`, with the c8, p2-p1, c10, 232 and 148 patches applied in that order
(each `git apply --check` clean). The scratch parent is uncommitted; its processor gitlink is set to base, then head. Every gate
is rc 0 at both:

| # | Gate | Result |
|---:|---|---|
| 1-8, 3b, 11 | C++ and Python idiom, RTL source lists and their self-test, `pp_srcs`, port contracts, naming, test evidence, docs, `lint_rtl` | identical at both, except the Python module line count (+24, `notify_mutants.py`). Port contracts: protocol-processor 1,759 ports at both |
| 9 | `flock $VIVADO_LOCK scripts/xvlog_gate.py --check` | PASS, 2 findings == ratchet, identical but for the pinned sha |
| 10 | `sw/builder/test_builder.py` | Make 4.4.1: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, the mf48 tree) at both; only timing figures differ. Make 4.3, at both: also gate 1b's `MAKEFLAGS += -e` arm, as in earlier lanes |
| 12 | `tb/verilator/pp_shadow` | legs of 606, 606, 646 and 311 checks, 0 failures at both |
| 13, 14 | `nvm_cosim` lint, quick | identical |
| 15 | `tb/verilator/milan_dp` | every leg passes; all 1,236 check, result and verdict lines are identical |
| 16 | `tb/verilator/milan_dp_render` | identical tallies and graded lines |

## What remains

- **A held DEREGISTER reaches its controller later.** The delay is up to the rest of the round, where `main` sent it after one
  job. If that controller re-registers in the meantime, it receives the DEREGISTER after its new REGISTER. `main` has the same
  ordering when a REGISTER withdraws the DEREGISTER job; the window is now longer.
- **A second expiry parked while a DEREGISTER is held drains after the round.** The drain already waits for the held
  DEREGISTER (`:1247-1251`). So that controller can still receive the round's remaining notification.
- **Not run.** No hardware or bench access; physical behaviour is not tested.

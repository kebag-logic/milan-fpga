[R477] POSITIVE - exact head bed5f47785839800bb640d7c747f5435f84ab5a3

# R477-1: external independent review of issue #148 / PR #159

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #159 (`pp148-notify-spacing` into `main`).
- Exact head `bed5f47785839800bb640d7c747f5435f84ab5a3`, tree `1bc22d81da063fc5288627a54c2cca502808a826`.
- Lane base `07b1469ddf1e2a54e4a42cac06c41f084ecffd6c`. Processor `main` is `ead8036035affd53ef4b29979190f2f4f67084c0`, unchanged throughout this review.
- Review start: PR #159 comment 5988345794.

## Verdict

**POSITIVE.**
- The fix in `KL_aecp_notify` makes every GET_COUNTERS round of a descriptor begin no sooner than one second after the previous round's last send. That send is the TX arbiter's grant of the frame.
- The red checks fail at `main`'s RTL with the PR's exact figures, and pass at the head.
- All seven named controls fail their named checks. Four further reviewer probes, on the parts the named controls do not cover, are each caught by an existing check.
- The full notify campaign (7 goldens, 53 of 53 KILLED) and the ctr campaign (control PASS, 17 of 17 KILLED) re-ran at the head. Their records match the published head records arm for arm.
- Both main merges are exact, and the union counts hold.
- The area is within the stop.
- The parent patch is right and bounded.
- The PR does not make #158 worse.

There are no open MINOR, MAJOR or BLOCKER findings. One RESIDUE (PR-body wording only) and two SUGGESTIONs are recorded below.

## 1. What was reconstructed, in order

1. **Repository rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md` (checked with `git ls-files`). I used `README.md` and `docs/README.md`: the single-source rules, timers quantized to 1 ms (08 §3), and Milan winning over IEEE.
2. **Issue #148.** The body's three acceptance items, the lane assignment (comment 5982500256), and the round-1b and round-1b-amended merge orders (5985998608, 5986055260). The two REVIEW READY posts were read as claims to check, not as evidence.
3. **Authorities.**
   - F08.1 `T-CTR-NOTIF`: "≥ 1 s between GET_COUNTERS notifications per descriptor", Milan Table 5.22. Table 5.22 is in Milan v1.2 §5.4.5, which the issue cites with IEEE 1722.1-2021 §7.5.2.
   - 06 §7, 09 §8.4, the integrator guide's counters face, and REQ-NOT-003. The specification PDFs are not distributed, so the clause is taken as the repository quotes it.
   - The recorded one-tick decision: R420-1 S4, retained in the `tb/pp_top` README. "Once per second" is counted on the 1 ms timebase, so the bound is 1,000 ticks, at most one tick short of a second in core clocks. This predates the lane and is not re-graded here.
4. **Diff and history.** `git diff 07b1469d..bed5f477` (26 files) and the lane-only diff `ead80360..bed5f477` (9 files, RTL +9 −1). The commits are abbe55b, 82e1664, 5f458aa, 221fd63, a369cdd, the merges 415a9fd and 4ed463b, and bed5f47.
5. **Public evidence.** kebag-logic/milan-fpga `1de9179a`, `review-evidence/pp148-r1`.
   - All 216 files' sha256 match its `MANIFEST.json`, and no file is unlisted.
   - Issue #148 has no manager comments with evidence, and PR #159 has only the two review-start comments.
   - The PR has no prior reviews, review comments or findings, so there is nothing to resolve or retain.

## 2. Executed evidence (this review)

All runs used the pinned Verilator 5.050 wrapper (`Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…e92f`). Trees came from `git archive` under `scratch/`. Every receipt is listed in `MANIFEST.sha256`.

| # | What | Result | Receipts |
|---|---|---|---|
| E1 | Red at main: head bench with `ead80360`'s `KL_aecp_notify.sv` (byte-identical to `07b1469d`'s) | `tb/aecp_notify`: TW1 FAIL (next round ms 3005, want 3600–3608) and TW2 FAIL (ms 6508, want 7504–7512); 30 checks, 2 failures. `tb/pp_top --spacing-only`: CS2a passes at 99,994; CS2b FAIL at 99,854 (row 0, 0006:0); CS2c FAIL at 99,590 (row 0, 0005:1); 9 checks, 2 failures. All figures equal the PR's | `receipts/redmain-*` |
| E2 | Head | `tb/aecp_notify` 34 of 34, with TW1 at ms 3603 and TW2 at ms 7507. CS 9 of 9, closest 115,077 / 115,070 / 115,077 clocks, at least 4 rounds at every row. rc 0 | `receipts/head-*` |
| E3 | `notify_mutants.py --jobs 4` on the six new controls plus `counter_limit_500ms` | goldens PASS (3); 7 of 7 KILLED with their named checks; `counter_limit_500ms` fails 7 checks, ST2b x5 named | `receipts/notify-new*` |
| E4 | Full `notify_mutants.py --jobs 5` at head | 7 goldens PASS, 53 of 53 KILLED, rc 0. All 60 records agree with the published head records in verdict, missing checks and failing-check count | `receipts/notify-full*` |
| E5 | Full `ctr_mutants.py --jobs 2` at head | control PASS, 17 of 17 KILLED, rc 0. Every arm line is identical to the published head log; `ctr-notify-one-window` fails 4 (K15 x2, K16, K17) | `receipts/ctr-full*` |
| E6 | Reviewer probes (`scripts/probe_mutants.py`, `--jobs 3`), each graded by `tb/aecp_notify` and `tb/pp_top` `--spacing-only`, `--notify-only` and `--counters-only` | see §3 Tests; golden 0 failures in all four runs | `receipts/probes*` |
| E7 | CS phase sweep, starts 0 to 199 (`scripts/sweep_patch.py`, scratch-only bench edit) | head: 200 starts, min 115,036, max 115,100, none below 99,900, at least 4 rounds per row. main RTL: min 99,587, 144 starts below the bound (phases 27 to 98 of every 100). This reproduces both published sweeps | `receipts/cs-sweep-*.txt` |
| E8 | #158 interplay: the published DEREGISTER probe plus a reviewer extension (`scripts/p158_ext.py`) | The corrupted job sequence is identical at main and head. The next counter round is presented at ms 21006 at main and ms 21008 at head: later, never earlier | `receipts/p158-*` |
| E9 | `verilator --lint-only -Wall` with `KL_aecp_notify` as top (the lint script's flags), head and base | rc 0, no warnings at either | `receipts/lint-notify-*` |
| E10 | Merge reconstruction with `git merge-tree --write-tree` | `a369cdd`+`b0a74196` gives `64d2c466…`, equal to `415a9fd`'s tree. `415a9fd`+`ead80360` conflicts only in `tb/pp_top/sim_main.cpp`; `4ed463b` resolves it as the union (`spacing_only` and `aq_only` both declared and both in `one_section`), and that is its only difference from the automatic merge. `4ed463b..bed5f47` touches only `tb/pp_top/README.md` | this report |
| E11 | Clone and extraction integrity after all probes | Clone HEAD, tree and index are exact; worktree equals index equals HEAD; all 558 tracked blobs and modes match; no gitlinks (the processor repository has no submodules). The head extraction used by the campaigns: 0 mismatches | `receipts/clone-integrity.txt`, `receipts/head-extraction-integrity.txt` |

## 3. Lenses

### Conformance: CLEAN

**The rule.** The window check `(now_ms_i - ctr_last_r[c]) >= 1000` (`hdl/aecp/KL_aecp_notify.sv:1099-1101`) reads one stamp per descriptor. At the head that stamp is:
- written at the round's claim (`:1302`);
- then written with `now_ms_i` in every `N_EMIT_WAIT` cycle of the round's GET_COUNTERS jobs (`:1443`), including the `uns_done_i` cycle.

`uns_done_o` is `(a_st_r == A_FREE) && uns_r` (`hdl/aecp/KL_aecp_engine.sv:2636`). `A_TXW` reaches `A_FREE` only on `txreq_uns_ready_i` (`:3838`), so "send" is the TX arbiter's grant, as the PR states.

**Spacing at every controller.**
- Every job of round n is sent no later than the stamp.
- Round n+1 cannot pend until `now ≥ stamp + 1000`, and it cannot start while round n is active.
- So every frame of round n+1 leaves at least 1,000 ticks after every frame of round n, whatever the row order or registrations between rounds.

This satisfies Milan Table 5.22 / §5.4.5 and the repository's `T-CTR-NOTIF` for the round that waits for the TX slot (acceptance 1). It is subject only to the recorded one-tick quantization of the ms timebase.

**Over-spacing.** The rule is conservative: the first controller's gap is one second plus the round's duration. That is permitted, because the clause bounds the rate from above. The PR and 06 §7 state it.

**Scope.** Only GET_COUNTERS carries a one-second window: `ctr_last_r` is the only `_last_r` stamp, and `32'd1000` appears only at `:1101`.
- IDENTIFY_NOTIFICATION is a separate path (`gen_ident`). It already spaces its frames from departure (`uns_tx_busy_i`, `:803`, `:813`).
- No other class is rate-limited.
- The PR's scope statement is correct, and no other kind shares this code path.

**Residual.** A MAC stall after the grant can shorten the wire gap by that stall. This is disclosed under "What remains" in the PR. Seeing departure would need the identify-only `uns_tx_busy_i` tap, which is a top-level change and outside the lane's no-port rule.

### RTL: CLEAN

- **The change.** +9 −1: `em_ctr_ix_r` is declared (`:469`), reset (`:1043`) and latched at the claim (`:1297`). The stamp follows in `N_EMIT_WAIT` under `em_kind_r == PP_UNS_CTRS_C` (`:1443`).
- **Write conflicts.** The two writers of `ctr_last_r` sit in mutually exclusive FSM states (`N_IDLE` claim and `N_EMIT_WAIT`), so they never write in the same cycle.
- **Interface.** No port, parameter or register changed: the module's declarations are byte-identical to `07b1469d`'s, per the published provenance, and the parent's port gate counts 1,759 at both.
- **Lint.** Clean (E9).
- **Area** (published reports, read by this review):
  - OOC 1x1 `KL_pp_shadow` 23,448 → 23,434 LUT (−14) and 20,968 → 20,969 FF (+1). The stop is 40 LUT / 60 FF.
  - `KL_aecp_notify` synthesized alone: 2,508 → 2,474 LUT (−34) and 1,277 → 1,280 FF (+3). The +3 FF is `em_ctr_ix_r`'s 3 bits.
  - The hierarchical `u_notify` row moves +41 LUT. Under the rebuilt hierarchy the attribution crosses block boundaries, and the module-alone run is −34. The gate is the total, which is within the stop.
  - `u_notify` internal WNS 10.821 → 10.933 ns. The whole-design WNS (−3.136 → −3.162 ns at the 20 ns integrated clock) is pre-existing, outside `u_notify`, and not moved by this RTL.
- **Measured RTL.** The measured head `5f458aa` has the same `KL_aecp_notify.sv` as `bed5f47`. The HDL that differs, from #155, is in the top and the listener, so retaining the measurement under the targeted re-measure rule is sound.

### Robustness: CLEAN

- **Withdrawal** (`rgy_new_w` in `N_EMIT_WAIT`): the stamp is written in that cycle too. The registry op that follows is bounded in cycles, far below 1,000 ms, before the job is presented again.
- **Identify owning the job face:** the GET_COUNTERS job stays in `N_EMIT_WAIT` and the stamp keeps following. That is correct, because it is a wait for the TX slot.
- **Warm reset:** `ctr_sent_r` clears and `em_ctr_ix_r` resets, so stamps stay bulk data, read only after their valid bit is set. TS still passes.
- **32-bit ms wrap:** modular subtraction, unchanged.
- **Processor #158** (a DEREGISTER drained mid-round): not worse.
  - The corrupted job sequence is identical at main and head (E8, matching the published probe).
  - The stamp is only ever later than main's (21008 against 21006).
  - Once #158 turns the round into DEREGISTER jobs, the kind guard stops the follow, so no counter frame is sent early.
  - See SUGGESTION S2 for the eventual #158 fix.

### Tests: CLEAN

- **Acceptance 2.** Two independent red checks exist, and they fail at main's RTL (E1).
  - TW drives the block directly. It has tight lower and upper bounds (send + 1,000 to + 1,008 ms), so a held change must be sent, not lost.
  - CS grades every row of every descriptor. It has a premise (CS1) and a non-vacuity floor (at least 3 rounds per row).
- **The control the assignment requires.** `counter_spacing_from_selection` restarts the spacing at selection and fails CS2b and CS2c. Its `tb/aecp_notify` twin fails TW1 and TW2. `counter_stamp_at_send_only` (TW2), `counter_stamp_first_job_only` (TW1, ms 3007), `counter_limit_500ms_cs` (CS2a–c) and `registry_holds_15_cs` (CS1) each fail their named checks (E3, E4).
- **Reviewer probes on parts no named control covers** (E6). Every one is caught by an existing check:
  - `kind_guard_dropped`: the follow writes for every kind. Caught by K14 and K15 in `--counters-only`.
  - `slot_from_live_pick` and `slot_zero`: the follow writes the wrong descriptor. Caught by TW1, TW2, CS2a–c, ST2 and ST2b.
  - `selection_stamp_dropped`: caught by ST2b x5 (rounds about 15,100 clocks apart), ST3 and ST3b. This confirms the PR's claim that the selection stamp closes the window before the round's first job.
- **Acceptance 3.** The notify and ctr campaigns are green at head with the published counts. The published round-1b base/head logs for the other campaigns, the suites, the six `pp_top` builds, lint, `make check` and Yosys are all rc 0. Their compare files show only the two explained record moves and figure-only diagnostics. The suite union holds:
  - 1,021,485 + 142 (#154 → `ead80360`) = 1,021,627 at base;
  - + 13 (TW 4, CS 9) = 1,021,640 at head;
  - `pp_top` 10,435 → 10,444, `aecp_notify` 30 → 34, `acmp_listener` 3,111 unchanged.
- **The AQ coverage line** (8,270 → 8,273 arms issued) is an informational figure, not a check. Its AQ checks are 4 of 4 at both, and the published logs differ only in that line.

### Docs: CLEAN (one RESIDUE, two SUGGESTIONs)

- **Figures checked against my runs:**
  - 06 §7, and the 09 §8.4 CS and TW rows ("four of the notification block's": FT, IX, TS, TW);
  - the `tb/aecp_notify` README: TW figures 2600/3603 and 6504/7507, main 3005/6508, mutant rows 6508, 3007/7503, "all ten KILLED" (10 `make run` mutants in the driver);
  - the `tb/pp_top` README: ST2 at 4 rounds, 115,077; ST3 at 70,681 / 485; the CS section; the `counter_limit_500ms` row (7: ST2b x5, ST3, ST3b); the `ctr-notify-one-window` row (4); "seven sections" with `make timer-defaults`.
- **PR body.** Its line references (`:136`, `:469`, `:1043`, `:1297`, `:1299-1302`, `:1099-1101`, `:1443`) and red and green figures are exact.
- F08.1 needs no change: it already states "≥ 1 s between … notifications".

## 4. Findings

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R477-1-RES1 | RESIDUE | Docs | PR #159 body, round-1b union table, row "Six `pp_top` builds", Head column: "default 9,956; other five unchanged; TD 6 probes" | `r1c-base-out-pp_top-tdf.log` and `r1c-head-out-pp_top-tdf.log` both read "TD: 3 checks … 6 monitor probes answered" | Wording only. "TD 6 probes" in a count column can be read as TD moving from 3 to 6 checks. No figure is wrong | Replace the cell with: "default 9,956; other five unchanged (TD 3 checks, 6 monitor probes answered, as at base)" | Read the edited PR body |
| R477-1-S1 | SUGGESTION | RTL, Docs | `hdl/aecp/KL_aecp_notify.sv:1299-1300` ("Measure the one-second limit from emission selection, …") and `:399-401` ("is written in the cycle that sets the bit") | the banner `:136` and `:1438-1442` now state the send rule | Both comments are still true but now incomplete. A reader at the claim site sees the pre-#148 rule | Next time the file is touched, say the claim stamp opens the limit at selection and `N_EMIT_WAIT` carries it to the round's last send, and that stamps are also rewritten while their bit is set | Comment only; no behaviour change |
| R477-1-S2 | SUGGESTION | Robustness, Conformance | `:1443` guard `em_kind_r == PP_UNS_CTRS_C`, together with #158 | E8; the RTL reading in §3 Robustness | None at this head. If #158 is fixed by restoring the round's kind after an interleaved DEREGISTER job, a DEREGISTER job that waits more than a second for the TX slot mid-round would stop the follow and could open the window inside the round | Carry to #158: keep the stamp following through an interleaved job of a GET_COUNTERS round, for example with a guard on the round's own kind, and grade it with a TW-style check | #158's own review |

## 5. Parent adoption patch (`parent-adoption-148-6c22d3ca.patch`)

**Right.**
- At dev `6c22d3ca`, `drain_tx` (`tb/verilator/milan_dp/sim_nxn.cpp:893`) keeps its frame buffer `cur` local to each call. The section calls it in 10 ms windows, so a frame that straddles a window edge is cut in two.
  - The first part is dropped at return.
  - The tail fails the EtherType test in the next call, so it is dropped too.
- The published probe shows the processor did send A's second push: 48 bytes captured, DA matching.
- The patch is a bench fix for a bench defect, and it does not mask a processor defect.

**Bounded.**
- The loop condition is `c < cyc || (!cur.empty() && c < cyc + 2048)`. It only extends while a frame is mid-flight, and it stops at that frame's `tlast`, because `cur.clear()` makes the condition false.
- The extension is at most 2,048 cycles. A 1,514-byte frame needs at most 190 beats at 8 bytes, with `tready` held at 1.
- No state crosses calls, and the bench's other trunk readers are untouched.

**At base.**
- When no frame is mid-flight at a window's end, the condition reduces exactly to the original, so behaviour is identical cycle for cycle.
- When one is mid-flight, the frame is captured instead of lost.
- The author states that the base five-patch run is rc 0 with leg lines identical to the four-patch base run. The published evidence carries gate 15's head receipts (round 1b: rc 0; 11,466 lines identical to the original accepted head) but no raw base five-patch log. I did not run the parent bench (outside this review's allowance). See the pending manager duties.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_aecp_notify.sv:1099-1101,1294-1302,1438-1443`; `KL_aecp_engine.sv:2636,3838`; F08.1 `T-CTR-NOTIF`; 06 §7; REQ-NOT-003; Milan Table 5.22 / §5.4.5 and IEEE 1722.1-2021 §7.5.2 as cited; scope search over the module; E1, E2, E7 | R477-1 | bed5f47785839800bb640d7c747f5435f84ab5a3 |
| RTL | CLEAN | lane RTL diff; E9 lint; published OOC 1x1 and module-alone Vivado reports and gate logs (`vivado/ooc1-*`, `notify-module-*`); E6 probes | R477-1 | bed5f47785839800bb640d7c747f5435f84ab5a3 |
| Robustness | CLEAN | withdrawal, identify ownership, reset, wrap, MAC-stall residual; #158 interplay E8 and the published probe | R477-1 | bed5f47785839800bb640d7c747f5435f84ab5a3 |
| Tests | CLEAN | `tb/aecp_notify/sim_main.cpp` TW; `tb/pp_top/notify_phases.hpp` CS; `notify_mutants.py`; E1–E7; published round-1b compare files, suite-union and rc files | R477-1 | bed5f47785839800bb640d7c747f5435f84ab5a3 |
| Docs | CLEAN | 06 §7, 09 §8.4, `tb/aecp_notify/README.md`, `tb/pp_top/README.md` (ST, CS, ctr and notify records, section count), PR body; RES1, S1 | R477-1 | bed5f47785839800bb640d7c747f5435f84ab5a3 |

## 7. Real limits

- I did not run the full processor suite bank, Yosys, `make check` or the other campaigns (acmp, aecp, aecp_dispatch, d3, gsi, name write, ADP, MAAP). For those I relied on the published round-1b rc files, compare files and records.
- No parent gate was run: not gate 15, and not the base five-patch leg.
- No Vivado run was made. The area figures are the published reports, which I read and cross-checked.
- The specification PDFs are not distributed. Clause conformance is judged against the repository's quotations (F08.1, the integrator guide, REQ-NOT-003).
- Hosted CI at the exact head, last read 2026-10-05 05:16 UTC (`receipts/hosted-ci-snapshot-3.txt`):
  - `docs-gates` and `portability` completed with success in both the push and the pull_request context;
  - `suites` was still in progress in both, so it is not evidence here.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## 8. Pending manager duties

1. Carry RES1 to the residue checklist.
2. Read the outcome of the hosted `suites` jobs at `bed5f477` (runs 37265363833 push and 37265367596 pull_request), and own hosted acceptance.
3. Build and validate the final current-dev candidate at the merge turn: source base `07b1469d`, live dev `e617275074e370cec342af99b929e2588fc8d43f`. Adopt the fifth parent patch with this processor pin, and keep a raw receipt of gate 15 at base with and without the fifth patch (§5).
4. Carry S2 to processor #158.
5. Merge requires the second independent positive review and the full completion bar.

R477-1 FINISHED

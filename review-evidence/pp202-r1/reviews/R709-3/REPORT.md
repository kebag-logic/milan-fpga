[R709] POSITIVE - exact head 429c909cb8a60398a2028436932e04b95dd0a0bd

# R709-3: independent review of PR #204 (issue #202) at exact head

- **Head:** `429c909cb8a60398a2028436932e04b95dd0a0bd`, tree `338b112f854a16ef831c39dc1b3a3f66108190a2`.
- **Source base:** `ed211803`.
- **Previous head reviewed by R709:** `ebb1f001` (R709-2).
- **Delta judged:** `ebb1f001..429c909`, the six round-4 commits answering R709-2 and R710-2. It changes 37 files: the ACMP talker, the SRP talker FSM, one port comment in the top, documents, benches and mutation arms.
- **Earlier rounds:** the full `ed211803..429c909` diff was read again where the delta depends on it. That covers the move rule, the PCP gap, the disable move and the parent patch.
- **Assignment text:** the round-3 assignment named the `a8aa626e..ebb1f001` focus. Its six round-1 probes were re-run at this head (section 3). Code the delta does not touch keeps R709-2's lens verdict.

**Verdict.** No BLOCKER, MAJOR or MINOR finding is open. Two RESIDUE items (wording only) and four SUGGESTIONs are recorded below. Every prior finding of R709-1, R710-1, R709-2 and R710-2 is resolved at its cause.

## 1. How the review was done

1. **Scope.** The repository has no tracked AGENTS.md or CONTRIBUTING.md. I read `docs/README.md`, which sets the single-source rules for timing values and IDs. Then I read the issue's frozen acceptance and the owner's option-A decision (issuecomment-6408987895), the round-3 assignment (issuecomment-6414935566) and the round-4 assignment (issuecomment-6421118089). I also read the author's round-4 ready note.
2. **Independent diff pass, before any prior finding was read:**
   - `hdl/acmp/KL_acmp_talker.sv`: the quarantine records, the cursor guard, the keep path and the search exit;
   - `hdl/srp/KL_srp_talker_fsm.sv`: the parked Leave, the leave copy and the deferred Join!;
   - `hdl/top/protocol_processor_top.sv`;
   - 00, 02, 05, 08, 09, 10 and the integrator guide;
   - the new bench cases (S5, S11, TP1-TP9, WK13, MP9) and the arms.
3. **Evidence.** I read the public evidence at `kebag-logic/milan-fpga@878a2394…/review-evidence/pp202-r1/author-r4` by section and verified it against its manifest.
4. **Prior findings.** These were read only after steps 1-3, and are resolved in section 5.

The probes ran in `git archive` copies under the packet's scratch directory. The clone was never written to (section 7).

## 2. What I executed at this head

All runs used the pinned simulator 5.050, whose identity was checked. Receipts are listed in `MANIFEST.sha256`.

| Run | Result | Receipt |
|---|---|---|
| `tb/acmp_talker` suite, exact head | rc 0, 1540/1540 PASS, includes S5 and S11 | `receipts/head-acmp_talker.{log,rc}` |
| `tb/srp_stream_fsms` all (walk shapes + suite), exact head | rc 0: walk 48/64/96/176, suite 1435/1435 | `receipts/head-srp_stream_fsms.{log,rc}` |
| `tb/pp_top maap-internal`, exact head | rc 0, 46 checks, 0 failures, includes MP8 and MP9 | `receipts/head-pp_top-maap.{log,rc}` |
| The same three benches with `hdl/` from `ebb1f001` | all fail on the new cases: S5 and S11 (8 checks), WK13 (2 + 3 checks at two shapes), MP9 (Lv frames -1, 0) | `receipts/oldrtl-*.{log,rc}` |
| Reviewer-owned mutant `none_sticky` (a blocked search's "no ID" never clears) | KILLED (S11) | `receipts/m_none_sticky-acmp_talker.*` |
| Reviewer-owned mutant `record_holds_new_id` (the record keeps the ID moved onto, not the one left) | KILLED (S5) | `receipts/m_record_holds_new_id-acmp_talker.*` |
| Reviewer-owned mutant `epoch_never_ticks` (the quarantine never ends) | KILLED (S5, S11) | `receipts/m_epoch_never_ticks-acmp_talker.*` |
| Reviewer-owned mutant `join_never_follows_leave` (the deferred Join! never fires) | KILLED (WK13 at all four shapes) | `receipts/m_join_never_follows_leave-srp_stream_fsms.*` |
| Reviewer-owned mutant `parked_txla_sends_new_value` | survives; **equivalent** (see below) | `receipts/m_parked_txla_sends_new_value-srp_stream_fsms.*` |
| Author arms, round 4, talker: `move_ignores_left_ids`, `record_lapses_in_one_epoch`, `record_overwritten_while_young`, `cursor_reenters_early`, `cursor_guard_three_epochs`, `blocked_move_declares_at_once`; plus `disable_keeps_declared_id`, `publish_upper_from_slot0`, `pcp_skips_the_gap` | 9/9 KILLED by their named checks, golden PASS | `receipts/acmp_mutants-round4-talker.{log,rc}` |
| Author arm `moved_open_skips_leave` at `pp_top` | KILLED (MP9), golden PASS | `receipts/acmp_mutants-moved_open_skips_leave.{log,rc}` |
| Author arms `pcp_after_withdrawal_skips_the_gap`, `pcp_pending_not_held`, `move_lost_on_disable` | 3/3 KILLED, golden PASS | `receipts/acmp_mutants-round1-talker.{log,rc}` |
| Author arms `conflict_keeps_old_wait`, `conflict_reuses_old_id` (talker and `pp_top`), `reopen_sends_new` | 5/5 KILLED, both goldens PASS | `receipts/acmp_mutants-round1-pp_top.{log,rc}` |
| Author SRP leave-copy arms (15) | all KILLED by their tags (TP1-TP9, WK13); both controls PASS | `receipts/srp_mutants-leave-copy.{log,rc}` |

**Why `parked_txla_sends_new_value` is equivalent.** The mutant lets a txLA! walk of a parked source build the new value's FirstValue. Under txLA!, LA and LO send no message (`KL_srp_talker_fsm.sv:356`, Table 10-3 "optional"). So the value is never pushed and the mutant cannot be observed. The parked value is used by the tx! that follows, and TP7 and the `talker-park-retires-on-txla` arm grade that.

## 3. The round-1 probes, re-run at this head

1. **Every same-Stream-ID re-declaration after a withdrawal keeps IEEE 802.1Q-2018 35.2.2.8's gap.**
   - The PCP change after a withdrawal waits: `EVC_PCP` from a used `DA_OK` enters BACKOFF.
   - The disable and re-enable moves the source to a new ID.
   - A move that finds no ID outside the quarantine keeps the current ID and waits `T-SRP-LEAVEALL2` from the grant (`KL_acmp_talker.sv:884-890`).
   - One arm per path is killed: `pcp_after_withdrawal_skips_the_gap`, `pcp_pending_not_held`, `disable_keeps_declared_id`, `move_lost_on_disable`, `blocked_move_declares_at_once`.
   - **Holds.**
2. **The parent wiring patch.** It is published at `author-r4/parent-src-stream-id-wiring.patch`, sha256 `e3991176…`, and matches the manifest. The framer stamp and GET_STREAM_INFO selector 2 read `src_stream_id_o`. The scratch-parent receipt (`receipts/parent/consumer/milan_dp.sidmove-legs.txt`, processor pinned at `ffc76f1`) shows both legs passing with 0 failures, 50 checks on AX 1x1 and 52 on 8x8. In both legs, after the conflict-and-move, the PROBE_TX stream_id, GET_STREAM_INFO selector 2, the Talker Advertise and every AVTP PDU on the wire equal `src_stream_id_o`. `ffc76f1..429c909` changes only three bench READMEs, so that pin carries this head's RTL. **Holds** (by published receipt).
3. **Each slot's published upper 48 bits are bound to its own slot.** S4 checks this, and `publish_upper_from_slot0` is killed. **Holds.**
4. **Join! where the RTL issues Join!** 10 F10.4 and §6.3 say Join! (New! only at the first open since reset), matching `KL_srp_talker_fsm.sv` `app_arb`. MP8 and MP9 observe a JoinMt, and `reopen_sends_new` is killed. The new §6.3 text cites Table 10-3 only within one attribute value. That corrects the R709-2 F1 docs outcome. **Holds.**
5. **Residues.** No bench label, lane name, round, reviewer or comment ID appears in the delta's `hdl/` comments. The parent patch's labels are gone (0 hits). One provenance wording remains, in a bench README (RESIDUE-1 below).
6. **Nothing else changed behaviour; the distinctness proof still holds.**
   - The behavioural changes are limited to the talker's move search and records, and to the SRP talker's re-open under another stream_id while a Leave is owed. Both are in scope.
   - Distinctness: at most 3 × `P-N-STREAM-OUT` candidates are refused (a current, a configured and a record ID per source). The search still exits within 3 × `P-N-STREAM-OUT` + 1 clocks (`:1173`), or earlier with no ID when the guard blocks it.
   - The search compares whole 64-bit IDs under each slot's own upper 48 bits, so a provisioned slot under another MAC never refuses a candidate wrongly.
   - **Holds.**

## 4. Independent judgement of the round-4 delta

**Quarantine proof (05 §"Why no move takes an ID declared within *Q*").** I checked it against the RTL step by step:

- A record is written at move time *l* with age 0. It ages at global epoch ticks every 30 s and refuses until age 2 (`:1415-1425`). So it refuses for more than 30 s after *l*, and no move overwrites it while it is younger (`:1465-1474`).
- The cursor only increases within a half. It reaches a passed value again only by leaving that half and re-entering it. Re-entry is blocked until the half was left four ticks ago (more than 90 s), and the leave time is never earlier than the pass time (`:1476-1480`).
- A record is skipped only while the source's record is young. Every ID that source has taken since the record was written came from the cursor after the write. That is the proof's second case, and it reduces to the first.
- The conflict and disable withdrawals happen before the grant that moves, so the record starts after the withdrawal.

I found no counter-example. The mutants that break each term (records, epoch, guard, overwrite, "no ID" exit) are all killed. `T-MRP-LEAVEALL` is a fixed 10..15 s draw (`KL_pp_prng.sv:15`), so the hard-coded `SIDQ_MS_C` (30 s, `:479`) matches the longest `T-SRP-LEAVEALL2`.

**SRP parked Leave.** I checked it against IEEE 802.1Q-2018 Table 10-3 as coded:

- A re-open on the held stream_id keeps the applicant: LA + Join! → AA, LO + Join! → VP.
- A re-open on another stream_id while LA or LO parks the old value. The applicant event is suppressed (`:511`), and the leave copy is written once, from the matcher and TSpec record (`:597-606`).
- The next tx! sends the Lv or s with the parked FirstValue (`:584-587`) and ends the park (`:695`). The deferred Join! then fires (`:514`).
- rLA!, periodic and received events leave a parked LA or LO unchanged, or are masked.
- A close keeps the park and drops the waiting Join!.
- The attribute type of the parked Leave follows `fail_r`, which a close clears and which only a declaring state re-sets. That is the same behaviour as a close without a park, so it is not changed by the delta.

**Measured cost.** The published out-of-context `KL_pp_shadow` grows from 59,862 to 61,219 LUT, as stated in the ready note. I did not re-measure it.

## 5. Prior public findings at this head

| Prior item | Disposition | Evidence at this head |
|---|---|---|
| R709-1 F-1: disable/re-enable re-declares the same ID with another DA | **RESOLVED** | `EVC_OFF` books the move. `disable_keeps_declared_id` and `move_lost_on_disable` are KILLED in my runs |
| R709-1 F-2: no check binds a slot's upper 48 bits | **RESOLVED** | S4; `publish_upper_from_slot0` KILLED in my run |
| R709-1 F-3: New vs Join! | **RESOLVED** | 10 F10.4 and §6.3; MP8/MP9 JoinMt; `reopen_sends_new` KILLED in my run |
| R709-1 RESIDUE-1: provenance wording | **RESOLVED** | no "lane tree" wording remains. The new round-3 wording is RESIDUE-1 below |
| R709-1 S-1 to S-5 | addressed (S-1 was superseded by R709-2 F1, now resolved) | as recorded in R709-2 |
| R710-1 F01: PCP change after withdrawal skips the gap | **RESOLVED** | `pcp_after_withdrawal_skips_the_gap` and `pcp_pending_not_held` KILLED in my run |
| R710-1 F02: parent TCTX UID overrides the published ID | **RESOLVED** | probe 2 above; both parent legs agree on the wire, in GET_STREAM_INFO and in PROBE_TX |
| R710-1 R01: bench labels in source comments | **RESOLVED** | none in the delta's `hdl/` comments |
| R709-2 F1: a return inside one `T-MRP-JOIN` replaces the withdrawn ID's owed Leave | **RESOLVED** at its cause, by outcome (a) | SRP park (section 4). MP9 puts the Lv on the wire before the new ID's JoinMt. MP9 and WK13 fail on the `ebb1f001` RTL (my `oldrtl` receipts). `moved_open_skips_leave` and 15 SRP arms are KILLED. The 05 and 10 texts R709-2 cited are corrected (10 §6.3 `sec-10-talker-owed-leave`) |
| R709-2 F2: 8x8 figure without a receipt | **RESOLVED** | the PR body (live, identical to the published `PR-BODY.md`) says 1,816 ms. The receipt `milan_dp.sidmove-legs.txt:166,172` says 1816 ms, and AX 1x1 1735 ms (`:69,75`) |
| R709-2 RESIDUE-1: port comments omit the disable move | **RESOLVED** | `protocol_processor_top.sv:680-682`, `KL_acmp_talker.sv:326-327` |
| R709-2 RESIDUE-2: PR body supersedes itself | **RESOLVED** | the live PR body has no "supersede" |
| R709-2 SUG-1: lap assumption for disables | **SUPERSEDED** | replaced by the quarantine and its proof |
| R709-2 SUG-2: pending PCP after a moving grant | retained as SUGGESTION (SUG-1 below) | `KL_acmp_talker.sv:892` is unchanged |
| R709-2 SUG-3: PCP-hold guard on the `DA_OK --> DECLARING` arc | retained as SUGGESTION (SUG-2 below) | 05:443 is unchanged |
| R710-2 F01: rapid disable laps reuse a historical ID inside the gap | **RESOLVED** at its cause | Records plus the cursor guard (section 4). S11 runs 65,528 disable moves in 1 ms, and S5 is a paced lap with a per-ID history oracle. Both fail on the `ebb1f001` RTL (my `oldrtl-acmp_talker`). Six new arms and three reviewer mutants are KILLED |
| R710-2 F02: 8x8 figure | **RESOLVED** | as for R709-2 F2 |
| R710-2 R01: PR self-supersession | **RESOLVED** | as for R709-2 RESIDUE-2 |
| R710-2 R02: bench identifiers in the parent patch's comments | **RESOLVED** | 0 added comment lines carry `[BOOT]`, `[A]`, `[MOVE]`, `[AFTER]`, `obj_sidmove`, `crflic`, `TSPEC8` or "three sources". The usage text moved to the README table |

## 6. Findings

### RESIDUE-1: a bench README names a review round as provenance

- **Lenses:** Docs (wording only; no lens made unclean).
- **Where:** `tb/pp_top/README.md:2076-2077`: "on the round-3 SRP talker FSM the Lv never goes out (frames -1, 0)."
- **Authority:** the owner's comment and provenance rule (2026-10-15). A review round is not a stable reference; a commit is.
- **Impact:** none on behaviour, figures or verdicts.
- **Exact fix:** "on the SRP talker FSM at `ebb1f001` the Lv never goes out (frames -1, 0)."
- **Verification:** inspect the line.

### RESIDUE-2: the quarantine's value is copied outside F08.1

- **Lenses:** Docs (wording only; no lens made unclean).
- **Where:**
  - `docs/architecture/02_interfaces.md:304` and `:566`: "within the last 30 s";
  - `docs/architecture/09_verification.md:800`: "the 30 s quarantine";
  - `docs/architecture/05_acmp_engine.md:528-529`: "(`T-MRP-LEAVEALL`, 10 to 15 s, F08.1)" and "*Q* is 30 s".
- **Authority:** `docs/README.md` §2 single-source rules. Timing values live only in F08.1. "A timing or parameter value copied outside its table … are review findings". Q is defined as the longest `T-SRP-LEAVEALL2`, an existing F08.1 row.
- **Impact:** none on code or claims. Today the values agree with F08.1, but a later edit to F08.1 would leave these copies stale.
- **Exact fix:**
  - 02:304 and 02:566: "within the longest `T-SRP-LEAVEALL2` (the [quarantine](05_acmp_engine.md#sec-05-sidq))";
  - 09:800: "within the quarantine";
  - 05:528-529: "A LeaveAll period is at most the longest `T-MRP-LEAVEALL` (F08.1), so the quarantine *Q* is the longest `T-SRP-LEAVEALL2`."
  - The integrator guide may keep "30 s", because the rule binds the architecture documents only.
- **Verification:** `grep -n "30 s" docs/architecture/0[25]*.md docs/architecture/09*.md` shows no quarantine hit; `make check` passes.

### SUGGESTIONs (do not affect the verdict)

- **SUG-1 (Robustness, `KL_acmp_talker.sv:892`; carried from R709-2 SUG-2).** A PCP change pending when a moving grant declares the new ID still withdraws that never-before-declared ID into a full `T-SRP-LEAVEALL2` backoff. This is conformant but costs 20-30 s in a rare interleaving. Option: clear the source's pending PCP bit when a moving grant declares.
- **SUG-2 (Docs, 05:443; carried from R709-2 SUG-3).** The `DA_OK --> DECLARING` arc could name the PCP-hold guard, as the new `NO_DA --> BACKOFF` arc at 05:442 names the quarantine outcome.
- **SUG-3 (Docs/RTL).** Give the quarantine its own F08.1 row (for example `T-ACMP-SIDQ`, "= longest `T-SRP-LEAVEALL2`, 30 s"). Then `SIDQ_MS_C`'s comment (`KL_acmp_talker.sv:472-479`), 02, 05 and 09 cite one ID, and `check-ids.py` guards it. This would also close RESIDUE-2 at its root.
- **SUG-4 (Tests).** A short bench note that LA and LO send nothing under txLA! would record why a FirstValue mutation of a txLA! walk of a parked source is equivalent (section 2). That saves the next reviewer the analysis.

## 7. Ledger (reviewer-owned)

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 802.1Q-2018 35.2.2.8 for every move and keep path, including historical IDs via the quarantine proof. 10.7.7 / Table 10-3 for the parked Leave, Join! after it and txLA! rows. 1722.1-2021 7.4.16.2 and 1722-2016 4.4.4.8 via the parent legs. Milan 5.5.4.1 PROBE_TX during the keep gap (S11) | R709-3 (round-4 delta) + R709-2 for untouched code | `429c909cb8a60398a2028436932e04b95dd0a0bd` |
| RTL | CLEAN | `KL_acmp_talker.sv` quarantine, guard, keep path, search exit, record write. `KL_srp_talker_fsm.sv` park/leave copy/deferred Join!/walk override. Top port comment. 3 reviewer mutants killed, 1 shown equivalent | R709-3 | same |
| Robustness | CLEAN | rapid-disable laps (S11), record overwrite, epoch saturation, wrap-safe tick, close/re-open/third-ID/back-to-parked sequences (TP1-TP9). Area cost +1,357 LUT out of context (published, not re-measured). SUG-1 open as suggestion | R709-3 | same |
| Tests | CLEAN | head suites rc 0; the new cases fail on `ebb1f001` RTL. 18 author talker/top arms and 15 SRP arms re-run and KILLED by name. Reviewer mutants. Published gate-status (50 rc 0, 3 expected old-RTL failures) | R709-3 | same |
| Docs | CLEAN (RESIDUE-1, RESIDUE-2 carried) | 00 REQ-ACMP-010, 02 F02.10, 05 F05.12 and quarantine proof, 08 F08.1, 09 rows, 10 §5.1/§6.3, integrator guide, bench READMEs, live PR body | R709-3 | same |

**Clone integrity after the probes** (`receipts/clone-integrity.txt`):

- HEAD `429c909…`; the HEAD tree and the index tree are both `338b112f…`.
- No modified, untracked or ignored files.
- The `ls-files -s` digest is recorded.
- The processor repository has no submodule gitlinks (mode 160000: none).

## 8. Real limits

- **Source validation.** At this source head, the source validation is my own focused runs (section 2) and the author's published gate receipts. These are a sweep at `ffc76f1` (RTL-identical to this head) and lint, `make check` and the talker suite at `429c909`. I ran no full parent, processor, gPTP, synthesis or builder bank. No manager source bank ran at this head, and none is claimed or inferred.
- **Parent patch.** Probe 2 is judged by reading and by the published scratch-parent receipts. I did not rebuild the parent.
- **Area.** The out-of-context area figure was not re-measured.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. No hardware was used.
- **Hosted checks at the head** (read-only, fetched 2026-10-27T00:58Z, `receipts/hosted-check-runs.tsv`): `docs-gates` ×2 and `portability` ×2 completed with success; `suites` ×2 still in progress. Hosted and act acceptance is the manager's.
- **Standards.** The standard texts are cited as quoted in the repository and issue; no full licensed-standard inspection is claimed.
- **Evidence commit.** The evidence commit `878a2394` carries no cryptographic signature. Its integrity rests on the manifest: all 1,768 `author-r4` files match their `published_sha256` (`receipts/evidence-verification.txt`).
- **Session restart.** This review's first session stopped on a memory limit before its arm campaigns finished. Those partial campaign logs are not used. Every arm cited here was re-run to completion in this session, and the phase-1 receipts are complete runs with rc files.

## 9. Pending manager duties

- Build and validate the current-dev merge candidate (source base `ed211803`, live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`) with the builder and native banks. Link the receipts on the PR.
- Accept the hosted `suites` jobs at this head once they complete.
- Carry RESIDUE-1 and RESIDUE-2 to the residue checklist.
- Land the parent wiring patch in the milan-fpga pin adoption PR, with its consumer gates at the adopted pin. Keep the recorded pre-existing parent CRF source-index limitation (power-of-two AAF shapes) in view.
- Obtain the second independent review. Merge needs two positive reviews and the full completion bar.

## Packet

- `REPORT.md` (this file) and the files listed in `MANIFEST.sha256`.
- Portable scripts:
  - `scripts/setup_trees.sh` builds the probe trees from the clone with `git archive`;
  - `scripts/plant_mutant.py` plants the reviewer mutants and refuses non-unique text;
  - `scripts/run_phase1.sh` runs the head, old-RTL and mutant benches;
  - `scripts/run_phase2.sh` runs the author arms one campaign at a time.
- Disposable trees and campaign directories stay in `scratch/`, which is not published.

R709-3 FINISHED

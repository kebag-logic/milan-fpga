[R710] NEGATIVE - exact head 429c909cb8a60398a2028436932e04b95dd0a0bd

# R710-3: external delta review of PR #204 (issue #202)

One MINOR finding is open, in the Tests lens. The quarantine's "a young record is kept" rule is one of the two pillars of the new reuse proof, and the suite grades it only inside the record's first epoch. A plant that lets a record be overwritten once it is one epoch old passes all 1,540 talker checks. My randomized probe shows that the same plant re-declares a Stream ID with another DA 3.9 s after its withdrawal, which breaks IEEE 802.1Q-2018 35.2.2.8. The RTL at this head is correct: about 23 million declarations under the same probe gave no violation.

Every earlier MAJOR and MINOR from R710-1, R709-1, R710-2 and R709-2 is resolved at its cause. One new wording residue is recorded.

- **Head:** `429c909cb8a60398a2028436932e04b95dd0a0bd`, tree `338b112f854a16ef831c39dc1b3a3f66108190a2`.
- **Source base:** `ed211803`. The live dev for the merge turn is `76de691e5625cc4ea2f9a19def9e07c1183a14ee`; this review does not cover it.
- **Previously reviewed head:** `ebb1f0010bde76c38cc5270a6366ee9e3157ec54` (R710-2, R709-2).
- **Delta:** six commits, `8310771`, `59f34d3`, `3cf5334`, `7e0ff0b`, `ffc76f1` and `429c909`, touching 37 files (+1,253/−142). The RTL is final at `ffc76f1`; `429c909` changes three test READMEs only.
- **What the delta answers:** the round-4 assignment (issue #202, issuecomment-6421118089).
  - R709-2 F1 and R710-2 F01: the owed Leave on a fast return, and historical reuse before the gap.
  - The 8×8 figure (R709-2 F2, R710-2 F02).
  - The residues.
- **Round-1 probes:** the six probes of the round-1 assignment were rerun at this head; results are below.

## Reconstruction

- **Contributor guidance:** the repository has no tracked AGENTS.md or CONTRIBUTING.md. I read docs/README (conventions and the ID registries) instead.
- **Issue #202:** the body, the assignment, the author's STOP, the option-A owner decision, and the round-3 and round-4 assignments.
- **Authorities:**
  - IEEE 802.1Q-2018 35.2.2.8 (Table 10-7), 10.7.7 and Table 10-3;
  - Milan v1.2 5.5.4.1 and Table 5.3 (5.3.7.5, informative);
  - REQ-ACMP-010;
  - 05 F05.12, 08 F08.1 (`T-SRP-LEAVEALL2`, `T-MRP-LEAVEALL`, `T-MRP-JOIN`), 10 §5.1 and §6.3, 02 §4.2 and F02.10, and the integrator guide §8.
- **Diffs and history:** `git diff ebb1f001..429c909` read in full, RTL and documents line by line (`receipts/round-delta.diff`, `receipts/delta-stat.txt`). The full issue diff `ed211803..429c909` was used for context.
- **Public evidence:** `kebag-logic/milan-fpga@878a2394…/review-evidence/pp202-r1/author-r4`.
- **Prior findings:** I read the prior public findings only after my own pass over the diff was complete. Other reviewers' reports under `reviews/` were not read.

## Evidence verification

- **The packet** (`receipts/evidence/packet-verification.txt`):
  - The evidence commit is **unsigned**, so integrity rests on `MANIFEST.json`.
  - All **1,768 / 1,768** `author-r4/` files match their published SHA-256, with no file missing or extra.
  - `MANIFEST.json` SHA-256: `71b7f161…d388`.
- **Gate return codes:** `gate-status.json` lists rc 0 for every accepted receipt.
  - The processor sweep, final gates (lint, make check, yosys, elaboration guards, talker suite) and all 13 campaign drivers ran at `ffc76f1` (`HEAD.txt` = `ffc76f1741e3…`).
  - Lint, make check and the talker suite were repeated at `429c909`.
  - `ffc76f1..429c909` touches `tb/*/README.md` only, so the RTL receipts apply to this head.
- **Parent consumer gate:** the author's executions on a scratch parent.
  - It ran at `ffc76f1`, with the processor RTL identical to this head: pp_shadow 2,187, maap 251, render 347 and milan_dp 13,685 checks, all rc 0, 0 failures.
  - The final pin at `429c909` re-ran pp_shadow and the out-of-context check and recorded the ROM digests.
  - The two sidmove legs record 1,735 ms (AX 1×1) and **1,816 ms** (8×8). After the move, the wire stream_id, PROBE_TX, GET_STREAM_INFO selector 2 and the Talker Advertise all equal `src_stream_id_o`.
  - This is not a manager bank. No manager source bank runs at this head.
- **PR body:** the live text equals the packet's `PR-BODY.md` apart from one trailing blank line.

## My executions at this head

All ran on disposable copies (`git archive 429c909`) using the pinned simulator, Verilator 5.050 rev v5.050, wrapper SHA-256 `905795b9…e92f` (`receipts/verilator-identity.txt`).

| Run | Result | Receipt |
|---|---|---|
| `tb/acmp_talker` golden | 1,540 / 1,540 PASS (S5: 65,523 moves to the wrap; S11: 65,528 moves before the guard) | `receipts/stress-head/build_and_suite.log` |
| `tb/srp_stream_fsms` golden (walk shapes 1x1, 2x2, 3x5, 9x9, then the suite) | 48, 64, 96, 176 and 1,435 checks, 0 FAIL, rc 0 | `receipts/srp/golden.log` |
| Author's ACMP driver, 16 named arms (`--jobs 10`): the round-1 controls, the quarantine arms and both pp_top MP arms | **19 / 19 arm runs KILLED** by their named checks; goldens PASS, including `pp_top --maap-internal-only` (MP8, MP9) | `receipts/acmp-campaign-subset.log`, `receipts/acmp-campaign-subset/` |
| Lint, `KL_acmp_talker` and `KL_srp_talker_fsm` (`-Wall`) | rc 0, no warnings | `receipts/lint-*.log` |
| `make check` (docs, IDs, figures, matrix, req-tags 245, parameters) | rc 0 | `receipts/make-check.log` |
| **Stress probe** (my own, below), 8 seeds × 3,000 steps at head | about 23.3 M declarations: 0 inside the gap, 0 quarantine-claim breaches, 0 shared IDs. Closest move onto a reused ID came 35.2 s after its withdrawal; closest same-ID re-declaration with another FirstValue came 20.0 s after | `receipts/stress-head/` |
| The stress probe's teeth, against planted controls | records off → C20 (5.5 s); guard off → C20 (17 ms); records lasting one epoch → C20 (9.6 s); guard opening after two epochs → not reached by the stress, but killed by the suite (rc 2) | `receipts/plant-*/` |
| My own SRP plants, through the `tb/srp_stream_fsms` suite | 5 / 5 caught (Join! after the park issued as New!; Join! while still parked; parked Lv taking its DA from the new value; parked Lv taking its VLAN from the new value; a close dropping the park) | `receipts/srp/*.log` |
| My own ACMP plants, through the talker suite | record written with the new ID: caught. Guard blocking the first crossing: caught. **Record overwritten at age 1: survives (1,540 / 1,540)** → F01. Keep path leaving the move booked: survives, and is behaviour-equivalent (below) | `receipts/acmp/*.log`, `receipts/plant-record-overwritten-at-age1/`, `receipts/plant-keep-leaves-move-booked/` |

**Stress probe** (`probes/r710_stress.hpp`, `probes/run_stress.sh`; plants are in `probes/plants/`, applied with `probes/run_stress.sh` or `probes/run_plant.sh`):

- **What it drives:** all eight sources of the talker unit, each under a Listener Ready, with a randomized mix of:
  - disable/return cycles, with or without time off;
  - MAAP conflicts;
  - PCP changes;
  - Listener withdrawals and returns;
  - bursts of up to 70,000 fast cycles, during which the timebase either holds still or jumps up to 35 s per chunk;
  - "ambushes": one source leaves an ID, sometimes twice in a row so its record stays on the older ID. Another source's moves then drive the cursor to just below that ID and attempt the landing after a delay of 0–45 s, 29–31 s or 29.99–30.01 s.
- **Timers:** every timer arm is honoured at its deadline, and the `T-MRP-LEAVEALL` draw is random in 10,000–15,000 ms.
- **Oracle**, kept per 64-bit ID independently of the suite's `SidHistory`:
  - **C20:** a re-declaration with another FirstValue (DA, VLAN, PCP epoch or source) less than 2 × LeaveAllTime = 20 s after the ID's last withdrawal;
  - **C30:** a move onto an ID withdrawn less than Q = 30 s before;
  - **DIST / DUP:** two sources publishing or declaring the same ID.

**Plant `acmp_keep_leaves_move_booked`** (removes `if (ev_sid_keep_w) sid_move_r[ev_src_r] <= 1'b0;`). It is behaviour-equivalent: `sid_used_r` stays set across a keep, so the next conflict or disable books the move anyway. The suite passes it and 6 stress seeds show no violation. No action is needed.

## Findings

### R710-3-F01 — MINOR — the record-keep rule is not graded across its second epoch; a plant that overwrites a one-epoch-old record breaks 35.2.2.8 and passes every check

- **Lenses:** Tests.
- **Where:**
  - The rule under test: `hdl/acmp/KL_acmp_talker.sv:1469-1470`, `!(sid_rec_v_r[ev_src_r] && (sid_rec_age_r[ev_src_r] != 2'd2))`. It is stated at `:80-90` and in `docs/architecture/05_acmp_engine.md:533-535`, the "Records" bullet.
  - The only check of it: `tb/acmp_talker/sid_cases.hpp:380`, where `conflict(2); conflict(2);` makes both of src2's moves in the same instant, so the record is at age 0.
  - The only control: `tb/pp_top/acmp_mutants.py:571-576`, `record_overwritten_while_young`, which plants "always overwrite".
  - Its records: `tb/pp_top/README.md:2114`, `tb/acmp_talker/README.md:401`, `docs/architecture/09_verification.md:809`.
- **Authority:**
  - IEEE 802.1Q-2018 35.2.2.8: two LeaveAllTime periods between a StreamID's withdrawal and its declaration with another FirstValue.
  - REQ-ACMP-010.
  - The round-4 assignment, item 1: "A move never picks an ID that was declared within the last two LeaveAllTime … with a test that fails on `ebb1f001`".
  - 05's proof, second case: "younger than two epochs, so written after l_c − 2Q". That case relies on a record surviving both of its epochs.
- **Evidence:**
  - Plant `probes/plants/acmp_record_overwritten_at_age1.sub` changes `!= 2'd2` to `== 2'd0` at `:1470`. A record can then be replaced from its first epoch tick onward, which may be 1 ms after it was written.
  - `tb/acmp_talker` at this head with the plant: **1,540 / 1,540 PASS, rc 0** (`receipts/acmp/acmp_record_overwritten_at_age1.log`).
  - The stress probe with the plant, 8 seeds × 1,500 steps (`receipts/plant-record-overwritten-at-age1/`): 5 of 8 seeds fail. The worst case is `ab0000000000801c`, declared with another DA **3,924 ms** after its withdrawal (C20). Others fail at 10,338 ms and 18,387 ms (C20), and at 20,012 ms and 20,892 ms (C30).
  - The unmodified head under the same probe: 0 violations in about 23.3 M declarations (`receipts/stress-head/`).
- **Impact:**
  - The RTL is correct, so this is not a conformance defect at this head.
  - The rule that prevents a normative violation can still be weakened in a way that no committed check sees, and the documented control covers only the coarsest form of the defect.
  - The 09 row's "a younger move keeps the record" is graded only for a record younger than one epoch tick.
- **Required outcome:**
  - Add a check in which a source's second move comes after an epoch boundary but within two epochs of its first move, followed by another source reaching the first left ID within Q. For example: extend S5's src2 sequence with `advance_to` across one epoch boundary between the two `conflict(2)` calls, or add a dedicated case.
  - The check must fail on the age-1 overwrite plant. Add that plant as a named `STREAM_ID` arm, for example `record_overwritten_after_one_epoch`, and update the README mutation records and the 09 row.
- **Verification:**
  - `probes/run_plant.sh` with `probes/plants/acmp_record_overwritten_at_age1.sub` must now fail the new named check.
  - The new arm must be KILLED by the driver, and the golden must still pass.

### R710-3-R01 — RESIDUE — a test README names a review round

- **Lens:** Docs; it leaves no lens unclean.
- **Where:** `tb/pp_top/README.md:2076-2077`, added in this delta: "…fails it by name; on the round-3 SRP talker FSM the Lv never goes out (frames -1, 0)."
- **Authority:** the owner's comment rule (2026-10-15): repository text states behaviour and reasons, not review rounds. This is wording only; it changes no figure, check or measurement.
- **Exact fix:** replace "on the round-3 SRP talker FSM" with "on the SRP talker FSM before the leave copy (`ebb1f001`)".

### Suggestions (they do not affect the verdict)

- **R710-3-S1 (Docs, 05:499-507, 10 §6.3):**
  - The LO row of the park table also applies to a conflict re-open. A received LeaveAll, or an rLv!, inside the last `T-MRP-JOIN` takes the idle applicant from VO to LO, so the new ID's first Talker Advertise waits one more `T-MRP-JOIN`.
  - 05's "a conflict cannot" is true of the withdrawal's Lv but not of the park.
  - Suggest one sentence saying that the park is latency-only and can rarely add one `T-MRP-JOIN` to the conflict-to-wire time (on the measured 8×8 run: 1,816 ms + ≤ 240 ms).
- **R710-3-S2 (Docs, 05 proof):** "its last declaration ended at or before l_c" holds for the MAD Leave request. On the fast-return path, though, the Lv message reaches the wire up to one `T-MRP-JOIN` after l_c. Q = 30 s against 2 × LeaveAllTime = 20 s (Table 10-7) absorbs this; suggest stating that margin explicitly.
- **R710-3-S3 (Robustness, 05):** the records and the cursor restart at reset, like all MRP state, so a move shortly after a processor reset may take `{MAC, P-N-STREAM-OUT}` even if it was declared just before the reset. This is inherent to a reset (the configured IDs restart in the same way) and outside 35.2.2.8's tear-down and bring-up sequence. Suggest one sentence in 05 next to the stable-since-reset assumption.
- **R710-3-S4 (Tests, `tb/acmp_talker/sid_cases.hpp:19-47`):** `SidHistory` compares only DA and VLAN. Tracking PCP changes, which are part of FirstValue (35.2.2.8.5), and the declaring source would let S5 and S11 grade the PCP and cross-source cases too, as the reviewer probe does.

## Prior public findings at this head

| Prior item | State at `429c909` | Evidence at its cause |
|---|---|---|
| R710-2-F01 MINOR: disable laps reuse a historical ID before the gap | **RESOLVED** | Per-source quarantine records plus the half-cursor guard (`KL_acmp_talker.sv:472-491`, `:1409-1500`). A blocked search keeps the ID behind `T-SRP-LEAVEALL2` (`:884-890`). R710-2's shape (65,529 fast disable moves) is S11 here: the return the guard blocks keeps its ID and waits. My stress (bursts, ambushes, epoch-boundary jumps) finds 0 C20/C30 at head; planted removal of the records or the guard produces violations. The test gap is F01 above, a new finding. |
| R710-2-F02 MINOR: 8×8 figure versus receipt | **RESOLVED** | The PR body and `milan_dp.sidmove-legs.txt` both say 1,816 ms (AX 1×1 1,735 ms), re-measured at `ffc76f1`. |
| R710-2-R01 RESIDUE: the PR supersedes itself | **RESOLVED** | The PR body now reads "This revision addresses the reviews of PR #204 at `a8aa626e` … and at `ebb1f001` …". |
| R710-2-R02 RESIDUE: bench identifiers in the parent patch comments | **RESOLVED** | No `[BOOT]`, `[A]`, `[MOVE]`, `[AFTER]`, `obj_sidmove`, `crflic grid` or `TSPEC8 shape` remains in the patch's added comment lines; the usage moved to the bench README. The patch's HDL hunks are byte-identical to round 3 (SHA-256 of the hunks `6003d7e5…5465` in both). |
| R709-2 F1 MINOR: the owed Leave is lost on a fast return | **RESOLVED** | `KL_srp_talker_fsm` parks the old value (`lvp_r`, `lvj_r`, `lwid_r`, `lwtsp_r`, `:481-492`, `:584-608`, `:661-675`, `:693-695`). The Lv carries the declared FirstValue, and the Join! follows that tx!. TP1-TP9, WK13 and MP9 on the wire pass. The author's 15 SRP arms and `moved_open_skips_leave` are killed; I re-killed the latter, and my own 5 SRP plants are caught. |
| R709-2 F2 MINOR: 8×8 figure | **RESOLVED** | As for R710-2-F02. |
| R709-2 RESIDUE-1: port comments | **RESOLVED** | `protocol_processor_top.sv:681-682` and `KL_acmp_talker.sv:326-327` now name the disable move. |
| R709-2 RESIDUE-2: the PR supersedes itself | **RESOLVED** | As for R710-2-R01. |
| R709-2 SUG-1: no rate floor on disable laps | ADDRESSED | 05 now proves the bound "whatever the rate of disables". |
| R709-2 SUG-2 and SUG-3 | Not taken (suggestions) | No change in the delta. |
| R710-1 F01, R710-1 F02, R710-1 R01; R709-1 F-1, F-2, F-3, RESIDUE-1 | **Remain RESOLVED** | The probes below. |

## Round-1 probes, rerun unmodified at this head

1. **Every same-ID re-declaration after a withdrawal keeps the 35.2.2.8 gap.** The PCP change after a withdrawal waits the gap (S7, S8, S9), and a disable and re-enable moves to a new distinct ID (S10). At this head `pcp_after_withdrawal_skips_the_gap`, `pcp_skips_the_gap` and `disable_keeps_declared_id` are KILLED. The new keep path is a third same-ID path: it waits `T-SRP-LEAVEALL2` from the grant (S11), and `blocked_move_declares_at_once` is KILLED. Across about 23.3 M stress declarations, the closest same-ID re-declaration with another FirstValue (PCP changes included) came 20,035 ms after the withdrawal. **Holds.**
2. **The parent patch.** The framer stamp and GET_STREAM_INFO read `src_stream_id_o`, and the HDL hunks are unchanged since round 3. The author's consumer legs at an RTL-identical pin show that after the move the wire, GSI selector 2, PROBE_TX and the Talker Advertise agree on 1×1 and 8×8. These are author executions; parent banks are outside my allowance. **Holds on published evidence.**
3. **Upper-48 binding.** S4 binds each slot's upper 48 bits to its own slot, and `publish_upper_from_slot0` is KILLED at this head. The new record compare also uses each record's own slot bits (`:1420`). **Holds.**
4. **Join! where the RTL issues Join!** 10 §F10.4 and §6.3 match the RTL: the open is `rec_valid ? AE_JOIN_C : AE_NEW_C` (`KL_srp_talker_fsm.sv:512`), and a parked re-open's Join! is issued after the tx! (`:514-518`). `reopen_sends_new` is KILLED, and my plant issuing New! after the park is caught. **Holds.**
5. **Residues.**
   - No new bench lane label, round or reviewer ID appears in an added `hdl/` or `tb/` source comment; the added test comments name check IDs, which is the existing convention.
   - The parent patch is clean.
   - One README round reference remains (R01).
   - The provenance lines name commits (`Measured 2026-10-26 at ffc76f1741e3`).
   - **Holds, except R01.**
6. **Nothing else changed behaviour.**
   - The SRP change only affects a gate open under another stream_id while the applicant is LA or LO.
   - The ACMP change only affects grants with a booked move.
   - All goldens pass: talker 1,540, stream FSMs 1,435 plus four walk shapes, and pp_top MP; `make check` and lint are clean.
   - **Distinctness holds:** across about 23.3 M declarations, no two sources ever published or declared the same ID. The proof bound "at most 3 × P-N-STREAM-OUT refused" matches the RTL's three refusal terms (`sid_hit_w` covers configured and current IDs, `sid_qhit_w` the records).

## Lens verdicts

- **Conformance** (CLEAN):
  - 35.2.2.8 is kept on every path I could drive: moves, keeps, PCP, and fast returns with the parked Lv. 10.7.7 has one applicant per value with no Leave lost.
  - Milan 5.5.4.1: the kept-ID PROBE_TX returns SUCCESS with the new DA (S11).
- **RTL** (CLEAN):
  - The quarantine and guard logic are correct as reviewed. Epoch counts saturate, so no compare wraps. Writes win over the tick in the same cycle.
  - The search is bounded at 3N + 1 clocks.
  - The leave copy is written only at `gnew_w` and read only under `lvp_r`. The 128-bit stride keeps both of its reads as multiplexers (area receipts: SRP lane 16,583 cells against 20,995 at the 124-bit stride).
  - Lint is clean.
- **Robustness** (CLEAN): the bound is independent of the disable rate, and the guard degrades to keep-and-wait rather than to reuse. The reset behaviour is suggestion S3.
- **Tests** (UNCLEAN): F01.
- **Docs** (CLEAN apart from residue): 05, 02, 08, 09, 10, the integrator guide and REQ-ACMP-010 match the RTL. R01 and suggestions S1, S2 and S4 are wording or optional.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta `ebb1f001..429c909`; `KL_acmp_talker.sv` quarantine, keep path and move rule; `KL_srp_talker_fsm.sv` park; REQ-ACMP-010; 05 F05.12 proof; stress probe (about 23.3 M declarations); 19 arm runs | R710-3 | 429c909cb8a60398a2028436932e04b95dd0a0bd |
| RTL | CLEAN | both RTL files line by line, the top port comment, lint, the author's yosys/elaboration receipts at `ffc76f1`, area receipts | R710-3 | 429c909cb8a60398a2028436932e04b95dd0a0bd |
| Robustness | CLEAN | burst, ambush and epoch-boundary stress; guard and keep behaviour; reset/re-provisioning assumptions | R710-3 | 429c909cb8a60398a2028436932e04b95dd0a0bd |
| Tests | **UNCLEAN** (F01) | S5, S11, TP1-TP9, WK13, MP9; author arms (19 re-run); 9 own plants (7 caught, 1 equivalent, 1 surviving = F01) | R710-3 | 429c909cb8a60398a2028436932e04b95dd0a0bd |
| Docs | CLEAN (R01 residue) | 00, 02, 05, 08, 09, 10, integrator guide, test READMEs, PR body, parent patch comments, `make check` | R710-3 | 429c909cb8a60398a2028436932e04b95dd0a0bd |

Code outside this delta keeps my round-1 and round-2 lens verdicts. The delta changes what the Stream ID move and the SRP re-open depend on, and both were re-judged above.

## Real limits

- My executions are processor unit and sub-system benches only: `tb/acmp_talker`, `tb/srp_stream_fsms`, and `tb/pp_top` through the author's driver. I ran no parent, gPTP, Yosys or full bank. The parent evidence is the author's published receipts.
- The stress probe drives the talker unit's public faces with a modelled allocator, timer service and PRNG. It is not a wire-level or SRP-coupled campaign, and its oracle uses DA, VLAN, PCP epoch and source as the FirstValue proxy. The TSpec is quasi-static and is not varied.
- The licensed standards were read only as far as the clauses quoted in the issue and the documents allow. Table 10-3 transitions (LO + Join! → VP, LA + txLA! → LO) are taken from the RTL tables graded in earlier issues, not re-derived.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- No hosted or act evidence was judged; the manager owns hosted/act acceptance.
- The review clone was verified after the probes: HEAD `429c909`, tree `338b112f`, 720 tracked blobs byte- and mode-identical, index clean, no untracked or ignored files. The repository has no submodule gitlinks.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `ed211803`, live dev `76de691e`) with the builder and native banks at the merge turn, and link those receipts on the PR.
- Hosted/act acceptance.
- Carry R710-3-R01 to the residue checklist.
- At milan-fpga pin adoption: land `parent-src-stream-id-wiring.patch` (SHA-256 `e3991176…f1fa`) with its sidmove legs.

R710-3 FINISHED

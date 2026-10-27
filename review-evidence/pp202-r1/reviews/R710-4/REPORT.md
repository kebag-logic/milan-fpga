[R710] POSITIVE - exact head 98e0137cfaf07b3b3efd21d2bd19648762e86f2b

# R710-4: external delta review of PR #204 (issue #202)

**Verdict.** No BLOCKER, MAJOR or MINOR finding is open, and all five lenses are CLEAN.

- R710-3-F01, the one open MINOR, is resolved at its cause. S5 now grades a quarantine record past its first epoch. My own probe shows the new check sits exactly on the epoch boundary that the age-1 overwrite needs.
- Both round-4 residues (R710-3-R01, R709-3 RESIDUE-1 and RESIDUE-2) are applied.
- Every earlier MAJOR and MINOR stays resolved. The RTL is byte-identical to the head where they were last verified.
- New items: one SUGGESTION. There is no new residue.

## Identity

- **Head:** `98e0137cfaf07b3b3efd21d2bd19648762e86f2b`, tree `9fdc9864d6ad8a900403a0ba81969b028c8d8140`. The live PR head (`headRefOid`) is the same commit.
- **Source base:** `ed211803`. The live dev for the merge turn is `76de691e5625cc4ea2f9a19def9e07c1183a14ee`; this review does not cover it.
- **Previously reviewed head:** `429c909cb8a60398a2028436932e04b95dd0a0bd` (R710-3 NEGATIVE with 1 MINOR; R709-3 POSITIVE).
- **Delta:** three commits, `b2b2bfd`, `83c2eef` and `98e0137`, touching 7 files (+94/−45); see `receipts-delta-stat.txt` and `receipts-round-delta.diff`.
  - `b2b2bfd` changes `tb/acmp_talker/sid_cases.hpp` and `tb/pp_top/acmp_mutants.py`.
  - `83c2eef` and `98e0137` change documents and test READMEs only.
  - `git diff 429c909..HEAD -- hdl syn` is empty, and so is `git diff ffc76f1..HEAD -- hdl syn`. The RTL is still as at `ffc76f1`.
- **Scope this round:** the round-5 assignment (issue #202, manager comment of 2026-10-27 01:02Z). It covers tests, mutant tables and documents only: R710-3-F01, R710-3-R01, and R709-3 RESIDUE-1 and RESIDUE-2.

## Reconstruction

- **Contributor guidance:** the repository has no tracked AGENTS.md or CONTRIBUTING.md, so I used `docs/README.md` (single-source and ID rules).
- **Issue #202:**
  - the body's frozen acceptance;
  - the option-A owner decision (one new output `src_stream_id_o`; move at the next `ALLOC_DA` grant; distinctness; `TALKER_DEST_MAC_FAILED` only before the grant; same-Stream-ID paths keep IEEE 802.1Q-2018 35.2.2.8's gap; documents; tests and mutants; consumer gate);
  - the round-3, round-4 and round-5 manager assignments;
  - the author's public REVIEW READY notes.
- **Authorities:**
  - IEEE 802.1Q-2018 35.2.2.8 (two LeaveAllTime periods, same StreamID, another FirstValue);
  - Milan v1.2 5.5.4.1 step 3 / Table 5.42, and Table 5.3 (5.3.7.5, informative);
  - REQ-ACMP-010;
  - 05 F05.12 and its quarantine section `#sec-05-sidq`;
  - 08 F08.1 (`T-SRP-LEAVEALL2`, `T-MRP-LEAVEALL`);
  - 02 F02.10; 09 issue-#202 rows.
- **Diff:** `429c909..98e0137` was read in full. The RTL it depends on was re-read: `KL_acmp_talker.sv:60-104` (banner rule and proof), `:472-491`, `:1409-1475` (record write, aging, refusal terms). The full issue diff `ed211803..98e0137` (41 files) was used for context only.
- **Prior public findings:** I read R710-3 and R709-3 only after my own pass over the delta and my own probes were complete. No private author material, lane scratchpad or management checkout was read.

## Evidence verification (author receipts; not a manager bank)

- **Packet** `kebag-logic/milan-fpga@0f19350815d085d6fae85bf28fdc30c2814555fc/review-evidence/pp202-r1/author-r5`:
  - The evidence commit is **unsigned** (GitHub verification reason `unsigned`), so integrity rests on `MANIFEST.json` (sha256 `98fddfcb…2406`).
  - All 287 / 287 `author-r5/` files match their published SHA-256, with none missing or extra. All 286 generated `INDEX.md` rows (file bytes and hashes, sub-index hashes and counts) match. Receipt: `receipts-evidence-verify.txt`; script: `verify_evidence.py`.
- **Gate return codes:** `gate-status.json` lists rc 0 for every accepted receipt. The reviewer plant fails at this head (rc 2) and survived at `429c909` (rc 0).
- **Provenance:**
  - `processor/final-head/HEAD.txt` = `98e0137…`: lint, make check, talker suite 1,545 / 1,545, pp_top 10,753 / 10,753.
  - The sweep ran at `b2b2bfd`: 1,030,593 checks, 0 failing; req-tags 246. `b2b2bfd..HEAD` touches only `docs/architecture/0{2,5,9}*.md` and two test READMEs, so the sweep's suite inputs equal this head's.
  - The ACMP campaign ran at `b2b2bfd`: started 01:19:18Z, after `b2b2bfd`'s commit time of 01:15:42Z. Result: 98 / 98 KILLED, eight goldens PASS. The retry campaign: 62 killed, 7 equivalent, 1 performance control.
- **README counts against receipts:** every changed figure in the two READMEs matches `acmp-results-summary.tsv` and `retry/*.txt`:
  - conflict_keeps_old_wait 128 / 9; conflict_reuses_old_id 36 / 8; output_ignores_move 23 / 2;
  - move_cursor_stuck 11; used_not_marked_by_event 27; declare_carries_configured_id 21; record_overwritten_after_one_epoch 3;
  - source_alias 255; no_requests 307; no_command_ready 771; no_conflict_wait_clear 27;
  - 33 STREAM_ID arm runs, 28 talker + 5 pp_top. I counted them in `acmp_mutants.py` (30 names).
- **Parent consumer gate (author executions on a scratch parent):**
  - The pin is at this head (`submodules.txt` names `98e0137…`). pp_shadow, the out-of-context check, the ROM-digest record and both sidmove legs (fresh build) are rc 0.
  - The patch SHA-256 `e3991176…` is identical to round 4.
  - This is not a manager bank.
- **PR body:** the live body is byte-identical to the packet's `PR-BODY.md` (sha256 `508763f8…`). Its figures (1,545; 65,520; 33 of 33 with 30 names; 98 of 98; 1,030,593 swept at `b2b2bfd`) match the receipts.
- **Hosted checks at this head** (`receipts-hosted-checks.txt`, read-only):
  - `docs-gates` and `portability` completed with success in both workflow instances.
  - Both `suites` runs were still **in progress** when I read them, so they have no conclusion yet.
  - The manager owns hosted and act acceptance.

## My executions at this head

All runs used the pinned simulator: Verilator 5.050 rev v5.050, wrapper sha256 `905795b9…e92f` (`receipts-verilator-identity.txt`). Build parallelism was capped by `vl_j3.sh`. Every run was on a disposable copy; the clone was never written.

| Run | Result | Receipt |
|---|---|---|
| Author driver `acmp_mutants.py --jobs 3 --only` on the five quarantine arms: `record_overwritten_after_one_epoch`, `record_overwritten_while_young`, `record_lapses_in_one_epoch`, `move_ignores_left_ids`, `cursor_reenters_early` | golden `acmp_talker` PASS: 1,545 / 1,545, S5 65,520 moves, S11 65,528. **5 / 5 KILLED** by their named checks, with failing counts 3, 1, 1, 2, 6 as the README states. The new arm fails `S5 a record one epoch old is kept…`, the S5 history check (`ab0000000000000b` again after 10,056 ms) and the after-wrap check | `runs/acmp-arms.log`, `runs/acmp-arms/` |
| Placement probe `plant` (the R710-3 age-1 plant, suite as committed) | rc 2, 1,542 / 1,545: the same three failures | `runs/probe/plant.log` |
| Placement probe `plant-pre` (the same plant, with src5's second move 1 ms **before** the epoch boundary instead of 1 ms after) | rc 0, 1,545 / 1,545: the plant survives | `runs/probe/plant-pre.log` |
| Placement probe `golden-pre` (head RTL, the same moved test) | rc 0, 1,545 / 1,545 | `runs/probe/golden-pre.log` |
| `make -j4 check` on a local clone at the exact head | rc 0: links 1,257, matrix, req-tags 246, ids, figures, aecp commands, parameters, wavedrom | `runs/make-check.log` |
| `scripts/lint_hdl.sh` with the pinned Verilator first on PATH | rc 0, 41 LINT OK | `runs/lint-hdl.log` |

**What the placement probe shows:** the new check depends on src5's second move crossing an epoch tick. Its record must be at age 1, not age 0, when it moves again. This is exactly the condition R710-3-F01 said was ungraded.

- The S5 comment's claim that "every epoch ends on the Q grid from reset" holds. `move_once` does not advance the timebase, the lap steps 5 ms (30,000 is a multiple of 5), and `count_to` steps 1 ms.
- The next grid point, `end + 2Q`, is not reached before the after-wrap move (`end + Q + 56 ms`).

## Findings

None open at MINOR or above.

### R710-4-S1 — SUGGESTION — give `record_overwritten_while_young` a normative witness too

- **Lenses:** Tests.
- **Where:**
  - `tb/acmp_talker/sid_cases.hpp:396-403`: src2's double move at `end + 1`; src1 leaves at `end + Q + 1`; the after-wrap move is at about `end + Q + 56`.
  - `tb/pp_top/README.md` row `record_overwritten_while_young`: one failing check, the exact-value after-wrap check.
- **Evidence:** src2's first left ID `...09` is reached about Q + 55 ms after its withdrawal. That is past both Q and 2 × LeaveAllTime, so the young-overwrite arm is killed only by the design-specific value check (`after_wrap == ...0C`), not by the 35.2.2.8 history check. This was already so at `429c909` (Q − 1 + 56 ms), so it is not a regression. The age-1 arm now has a normative witness (the history check fails at 10,056 ms).
- **Option:** place src2's double move inside the window, as src5's moves now are (for example 10 s before `end + Q`). The young-overwrite plant would then also fail `S5 no ID is declared again with another DA inside two LeaveAllTime periods`.
- Optional; it does not affect the verdict.

## Prior public findings at this head

| Prior item | State at `98e0137` | Evidence at its cause |
|---|---|---|
| **R710-3-F01** MINOR (Tests): the record-keep rule is not graded across its second epoch; the age-1 overwrite plant passes 1,540 / 1,540 | **RESOLVED** | New check `S5 a record one epoch old is kept when its source moves again…` with `REQ_TAG("REQ-ACMP-010", …)` (`sid_cases.hpp:421-426`). src5 leaves `...0B` 10 s before an epoch ends and moves again 1 ms after it (`:399-402`). The after-wrap move reaches `...0B` 10,056 ms after its withdrawal, inside Q and inside 2 × LeaveAllTime. The plant is the named arm `record_overwritten_after_one_epoch` (`acmp_mutants.py:577-584`), KILLED by both its named checks (my run and the author's campaign); golden PASS. The R710-3 plant via the author's `run_plant.sh` receipt: rc 2 at head, rc 0 at `429c909`; reproduced by my `plant` probe. Records updated: `tb/pp_top/README.md` table row and "33 of 33 / 98 of 98"; `tb/acmp_talker/README.md` S5 row, arm list and retry re-measure line; 09 row (`09_verification.md:809`). |
| **R710-3-R01** RESIDUE (Docs): a test README names a review round | **RESOLVED** | `tb/pp_top/README.md:2077` now reads "on the SRP talker FSM at `ebb1f001`, before the leave copy, the Lv never goes out (frames -1, 0)". This merges R710-3-R01's text with R709-3 RESIDUE-1's, which named the same line differently; the result carries both and names no round. |
| **R709-3 RESIDUE-1** (Docs): same line | **RESOLVED** | As above. |
| **R709-3 RESIDUE-2** (Docs): the quarantine's 30 s copied outside F08.1 | **RESOLVED** | `02_interfaces.md:304-306` and `:567`, `05_acmp_engine.md:528-529`, `09_verification.md:800` now name the longest `T-SRP-LEAVEALL2` / the quarantine. `grep "30 s"` over 02, 05, 09 and 10 finds no quarantine hit. The 30 s left in 08 F08.1 itself is the single source. `make check` (links included) passes. |
| R710-3-S1, S2, S3, S4 (suggestions) | Retained as suggestions | The delta does not touch 05's park and proof wording, the reset note, or `SidHistory`'s FirstValue fields. |
| R709-3 SUG-1 to SUG-4 (suggestions) | Not taken; they remain the other reviewer's suggestions | `KL_acmp_talker.sv` is unchanged, 05:443 is unchanged, and there is no new F08.1 row. |
| R710-2 F01, F02, R01, R02; R709-2 F1, F2, RESIDUE-1, RESIDUE-2 | **Remain RESOLVED** | Verified resolved at `429c909` by R710-3 and R709-3. Since then `hdl/`, `syn/`, the parent patch (same SHA-256 `e3991176…`) and the PR-body passages they depend on are unchanged. The delta's document edits touch only the quarantine sentences. |
| R710-1 F01, F02, R01; R709-1 F-1, F-2, F-3, RESIDUE-1 | **Remain RESOLVED** | As above. The same-ID paths are still graded (S7-S11 arms in the 98 / 98 campaign at `b2b2bfd`, with the same RTL). |

**Residue scan:** the added lines of `429c909..98e0137` contain no bench lane label, lane name, review round, reviewer ID or issue-comment ID (`receipts-residue-scan.txt`, 0 hits). The new test comments state behaviour (Q as the longest `T-SRP-LEAVEALL2`, the epoch grid) and name the check IDs, as the convention is.

## Lens verdicts

- **Conformance — CLEAN.**
  - The RTL is unchanged since `ffc76f1`, so R710-3's Conformance verdict carries.
  - IEEE 802.1Q-2018 35.2.2.8: the same-ID paths wait `T-SRP-LEAVEALL2`, and a move takes no ID declared within Q.
  - Milan v1.2 5.5.4.1 step 3: `TALKER_DEST_MAC_FAILED` only before the grant.
  - The new check grades 35.2.2.8 on the second-epoch keep that the proof's second case relies on.
- **RTL — CLEAN.** It is unchanged (`git diff ffc76f1..HEAD -- hdl syn` empty) and lint-clean under the pinned simulator. R710-3's RTL verdict carries.
- **Robustness — CLEAN.** It is unchanged and carries. S11 (65,528 fast disable moves) and the guard arms are KILLED in the 98 / 98 campaign, and `cursor_reenters_early` is re-killed by me.
- **Tests — CLEAN.**
  - F01 is resolved: the new named check exists, the plant is an arm, and both are executed by me.
  - The placement probe shows the check is aimed at the age-1 keep.
  - Mutation records and counts match the receipts. Golden 1,545 / 1,545.
  - S1 is a suggestion.
- **Docs — CLEAN.**
  - Both residues are applied.
  - The 09 row, the two README mutation tables, the S5 row and the PR body agree with the code and the receipts.
  - The `#sec-05-sidq` links resolve (`make check` links 1,257 OK).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #202 acceptance and owner decision; IEEE 802.1Q-2018 35.2.2.8; Milan v1.2 5.5.4.1 / Table 5.3; REQ-ACMP-010; `KL_acmp_talker.sv:60-104`, `:1409-1475` (unchanged); the new S5 check; the ACMP campaign 98 / 98 | R710-4 (delta); RTL verdict carried from R710-3 | `98e0137cfaf07b3b3efd21d2bd19648762e86f2b` |
| RTL | CLEAN | `git diff ffc76f1..HEAD -- hdl syn` empty; `scripts/lint_hdl.sh` with pinned 5.050, 41 OK | R710-4 (no RTL delta); carried from R710-3 | `98e0137cfaf07b3b3efd21d2bd19648762e86f2b` |
| Robustness | CLEAN | unchanged quarantine and guard logic; S11 and guard arms in the author campaign; `cursor_reenters_early` re-killed | R710-4 (no delta); carried from R710-3 | `98e0137cfaf07b3b3efd21d2bd19648762e86f2b` |
| Tests | CLEAN | `sid_cases.hpp` S5 delta; `acmp_mutants.py` new arm; my 5-arm driver run plus golden; placement probe (3 variants); author campaigns, final-head suites and the reviewer-plant receipts | R710-4 | `98e0137cfaf07b3b3efd21d2bd19648762e86f2b` |
| Docs | CLEAN | 02, 05, 09 delta; `tb/acmp_talker/README.md`, `tb/pp_top/README.md`; 08 F08.1 row; live PR body versus the packet; `make check` | R710-4 | `98e0137cfaf07b3b3efd21d2bd19648762e86f2b` |

## Real limits

- **No manager source bank** ran at this head, and I claim none. Source-head execution evidence is the author's published gate receipts plus my focused runs above.
- **Not re-run by me:**
  - the full processor sweep (1,030,593 checks);
  - the full pp_top suite (10,753 checks);
  - the full 98-arm ACMP campaign and the retry campaign;
  - the parent consumer legs.

  For these I rely on the author's receipts, verified by hash. The pp_top inputs (`hdl/`, `tb/common`, `tb/pp_top/sim_main.cpp`, `pp_top_wrap.sv`) are unchanged since `429c909`.
- **Unsigned packet:** the evidence commit is unsigned. Integrity rests on the manifest hashes I verified, not on a signature.
- **Campaign provenance:** the campaign receipts carry no `HEAD.txt`. I bind them to `b2b2bfd` by timestamps and the author's records, and by my own exact-head re-run of the five quarantine arms.
- **Hosted checks:** `suites` had not concluded when I read them.
- **Not covered:**
  - the current-dev merge candidate (live dev `76de691e…`);
  - physical calibration: NOT RUN;
  - hardware: none.

  Field skips are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR.
- Conclude hosted and act acceptance once the exact-head `suites` runs finish.
- Land the parent wiring patch (`e3991176…`) in the milan-fpga pin adoption PR, as the owner decision states.
- Carry the open suggestions (R710-4-S1, R710-3-S1 to S4, R709-3 SUG-1 to SUG-4) at their owners' discretion. There is no new residue for the checklist.
- Confirm a second independent positive review at this exact head before merge.

## Packet

Every publishable file is listed in `MANIFEST.sha256`:

- **Scripts:** `verify_evidence.py`, `probe_s5_boundary.sh`, `vl_j3.sh`.
- **Receipts:** `receipts-*.txt`, `receipts-round-delta.diff`, `runs/`.

`scratch/` is disposable and not published. The review clone was restored and verified: HEAD and tree are exact, `git status --porcelain --ignored` is empty, the worktree blob bytes equal HEAD's blobs, index tree = `9fdc9864…`, and there are no submodule gitlinks (none are tracked); see `receipts-clone-restore.txt`.

R710-4 FINISHED

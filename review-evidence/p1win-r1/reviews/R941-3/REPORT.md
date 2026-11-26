[R941] NEGATIVE - exact head 079c4fa1514be460949ddc28ae3277ea1873cb48

Round R941-3, an internal independent review of kebag-logic/milan-fpga#1009 / PR #1017. It was a narrow evidence re-review at the same head as R941-2: head `079c4fa1514be460949ddc28ae3277ea1873cb48`, tree `be2122cbd487361b4ed8a99ff283565c1bec3eb2`, source base `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`. There was no code change since R941-2. The packet under review is `review-evidence/p1win-r3/author` on `p1win-review-evidence` at `ad4ae8da2`.

## Summary

- **R941-2-F1 (notice 140 ms) is resolved.** I recomputed the six notice-arm runs from their published `results.json`, without using the author's `notices_r3.py`. Every figure in the PR table and in `worst.txt` matches. Each run's identity names this head with 0 status entries, and the hashes of `results.json` and `table.md` match their identity files.
- **R941-2-F2 (the 47 power cuts) is resolved.** I recounted the cuts: 47 ran (38 + 9), 44 are graded (36 + 8) and 3 are retries with no bind since the previous cut. The 44 graded cut times and inputs match the round-2 board summaries line by line.
- **RES1, RES2, S1 and S2 are done**, with the prescribed text or an equivalent. I re-ran the store gate to confirm S2's breakdown of 640 + 16 = 656 tests.
- **One new finding blocks: R941-3-F1 (MINOR).** The input-0 case at 8x8/1if (si0) failed three attempts under the published test. It now passes only under a "corrected test" that has no public artifact. Its rerun receipt carries no identity, and the PR's diagnosis and restore timings for that case have no receipt.
- **One wording residue: R941-3-RES1.** The PR's `answering-every-port` row says "then a burst" for all 16 groups; only 8 of them carry the burst.

## How I reconstructed the task

- **Contract and scope.** I read `AGENTS.md` and the issue's frozen acceptance criteria. I then read the issue's rulings: Ruling 3 (comment 7176978406) items 3 and 4 frame step 1, and the clause 5.5.3.5.3 re-ruling (7170938286) is the background.
- **The notice bound.** The authority for "notice 140 ms" is `docs/reference/FR_NFR.md:416-417`: 140 ms is the owner's bound on the last queued notice, and the tree states 130 ms (`AECP_QUEUED_MS` / `CTRL_LOOP_QUEUED_MS`).
- **The code.** The delta `c34e7d8b..079c4fa1` is 31 files, all under `sw/firmware/ctrl_nvm`, `tb/verilator/{ctrl_service_budget,nvm_split_target}` and `docs`. No HDL, SoC or gateware file is in it. Its 7 commits are unchanged since R941-2.
- **The harness.** I read how it grades the notice rows:
  - A row's budget is the family's 20 ms plus the probe's `wait_ms` (`grade.py:530`). For queued notices `wait_ms` = `queued_ms - T_SVC_MS`, so 130 ms in total (`notice_window.py:170`).
  - The harness takes a queue's first notice as the group's minimum and holds it to `AECP_QUEUED_FIRST_MS` (`run.py:383-389`).
  - A `notice-retried-<k>` group with no timer-driven MRPDU is a miss (`run.py:380-382`).
- **Order of reading.** I did my own pass over the packet first, and only then read R941-2's findings (`review-evidence/p1win-r1/reviews/R941-2/REPORT.md` at `ca832e568`). I read no other reviewer's report for this round.

## Evidence checked against its receipt

| Claim (PR body / packet) | Receipt | Result |
|---|---|---|
| Packet integrity | `MANIFEST.json`, 40 entries | All 40 published hashes match. `author/MANIFEST.txt` fails only on `cuts/cuts.py`, which `MANIFEST.json` marks `path_redacted` |
| The live PR body is the packet's | `gh pr view 1017` against `PR-BODY.md` | They differ only by the `[A844]` header line and a trailing blank line |
| Six notice arms, clean clone of the head, rc 0 | `notice-arms/*-identity.txt`, `*-rc.txt` | Each records head `079c4fa1…`, tree `be2122cb…`, status entries 0 before and after, the head's submodule gitlinks, and rc 0. Each `results.json` and `table.md` hash matches its identity file. Each `results.json` `build` equals the identity's `native/Vsim` sha256 |
| 0 refusals, 0 misses, 0 notice_misses | each `results.json` | Confirmed for all six (`receipts-check_notices.txt`) |
| `notice.retried` worst 8.184 ms (1x1/1if), 8.157 ms (8x8/1if); bound 20 ms | `*-answering-later-results.json` | 8 rows each, worst 8.184 and 8.157 ms, budget 20 ms, 0 over |
| Every `answering-later` group carries its MRPDU | same | Each of the 8 groups at both points has one `mrpdu` row |
| Queue's last 20.707 ms (192 rows) and 27.647 ms (640 rows); bound 140 ms, harness row bound 130 ms | `*-answering-every-port-results.json` | Confirmed. Every row's `budget_ms` is 130.0, with 0 over. This meets both the owner's 140 ms and the tree's 130 ms |
| Queue's first 6.847 ms and 2.633 ms; bound 20 ms | same | Confirmed by the harness's own definition (the group minimum) |
| Talker declared and withdrawn: 5.343 / 5.219 ms (1x1/1if), 11.958 / 10.447 ms (8x8/1if) | `*-talker-notices-results.json` | Confirmed: 8 + 8 rows each, budget 20 ms, 0 over |
| 47 cuts, 44 graded (36 + 8), 3 retries with no bind | `cuts/cuts-{8x8,1x1}.txt` | Recounted independently (`scripts/check_cuts.py`). Ungraded cuts: 8x8 #29 and #30 (input 0) and 1x1 #5 (input 1). In all three "bind since previous cut" is False and "hold reading" is no. No cut has a bind without a hold reading |
| Graded cuts are the round-2 summary lines | r2 `board/summary-*.txt` | The off-after-response times and the inputs equal the summaries' 36 and 8 sink lines, in order. All PASS, all idle at the bind |
| Off 1.47-1.67 s after the response; at least 1.27 s before the DUT's last frame; at most 603 / 330 ms to durable | same | 1.469-1.674 s; least margin 1.271 s; durable at most 602.6 ms (8x8/1if) and 330.1 ms (1x1/1if) |
| "0.579 s, before cut 28" and "0.327 s, before cut 4" | r2 summary-8x8 line 28, summary-1x1 line 4 | Confirmed: 0.579 s (8x8/1if, sink 0) and 0.3274 s (1x1/1if, sink 1) |
| si0 rerun: idle (first sample 0.079 s), durable 0.586 s (bracket 48.8 ms), off 1.551 s, 1.196 s before the last frame, scenario passed | `board/summary-8x8-input0.txt` | Each of these figures is in the receipt. **But** the receipt has no image, test-revision, command or date identity. The "Talker Failed declared 4.74 s after power-on … ENTITY_AVAILABLE, 4.73 s", the "0.62 s" board run-down and the test correction appear in no receipt (F1) |
| RES1 text | PR body lines 112-114 | Exactly R941-2's prescribed replacement |
| RES2 | PR body line 66 | Takes R941-2's second option: "its verdict lines are identical to round 1's". "byte-identical" no longer appears |
| S1 | PR body line 67 | "(the flip check's 0.75; ruling 3's 0.76)" |
| S2: 656 = 5 × 128 + 16, named | PR body lines 123-126; my re-run `receipts-gate-store-tally.log` | My run of `test_ctrl_nvm.py --require-rv32 --jobs 16` at the head gives PASS, 656 tests: 5 × 128, plus vectors 2 + 2, walk/sizes 1, no name record 1, NAME capacity 6, LiteSPI 3, ASan prefixes 1. This matches the PR |

## Findings

**R941-3-F1 MINOR - Conformance, Robustness, Tests, Docs - the si0 board case. Artifacts: `review-evidence/p1win-r3/author/board/summary-8x8-input0.txt`; `cuts/cuts-8x8.txt` (attempts section for "a Talker Failed declared at the DUT's first ENTITY_AVAILABLE", STREAM_INPUT 0: RETRY, RETRY, RETRY, "FAIL at attempt 3"); PR body "On the board", lines 164-173. The finding: the case's pass rests on a test correction that has no public artifact.**

- **Authority and evidence.**
  - The issue's acceptance criterion 2 requires the four power-cycle scenarios to pass on the bench with the harness timing unchanged. Ruling 3 item 3 sets the per-cut rule.
  - `AGENTS.md` §2 says a cold reviewer must be able to reconstruct the task from public state. §8 forbids weakening a test to obtain a pass.
  - Under the published test, the fourth 8x8/1if scenario failed on input 0 at all three attempts (cuts 28-30).
  - The PR calls this "a fault of the test, not of the store". It then reports a pass "with the test corrected (the withdraw waits for the board to go down, and only probes after the attempt's own power-on count)".
  - The power-cycle test is not in this repository. No revision, diff or command of the correction is published anywhere public.
  - The rerun receipt (`summary-8x8-input0.txt`) records the durability figures and "1 scenario passed". It names no image or head, no test revision, no command and no date.
  - Three PR statements have no receipt at all: the board's "up to 0.62 s" after the outlet's command returned, the probe being "taken as the attempt's settle", and the restore timings (4.74 s and 4.73 s).
- **What is shown.** The store-side per-cut rule holds at cut 28 with a receipt: durable at 0.579 s, 1.328 s before the last frame (r2 `summary-8x8.txt`, sink line 28). So durability is shown.
- **What is not shown.** The case's "binding restored after power-on" verdict rests only on a test whose change cannot be inspected.
- **Impact.** A cold reviewer cannot tell whether the correction tightened the check or relaxed it. Nor can they tell whether the rerun ran this head's image under the unchanged cut hold. Until then, criterion 2's fourth scenario at 8x8/1if is shown only by an unreviewable test, and the failing run's diagnosis is the author's word.
- **Required outcome.** Either of these:
  1. Publish three things:
     - the rerun's identity: the image or head it ran, the test's revision, the command, start and end times, and rc;
     - its report lines (bind, cut, verdict, the post-power-on ENTITY_AVAILABLE and Talker declaration times, the Listener's Asking Failed);
     - the correction, as a diff or a public revision, with one sentence on why it leaves the cut timing (`CERT_CUT_HOLD_S` 1.0) and the restore check no weaker.

     Then state the diagnosis with the receipt it rests on, for example the failing attempt's outlet-return and last-frame times. Otherwise reword it as the author's reading.
  2. Or obtain a public manager ruling that accepts the board harness's correction and the rerun on the qualification lane's own evidence, and cite it in the PR.
- **Verification.** The new receipts bind the rerun to `079c4fa1` (or its successor's image) and to a named test revision. The diff shows no relaxed verdict and an unchanged cut hold. Every figure the PR states for the case is in a receipt.

**R941-3-RES1 RESIDUE - Docs - PR body, notice-arm table, `answering-every-port` row: "every port answering, then a burst (16 groups)".**

- **Evidence.** The arm's 16 groups are 8 `notice-every-<k>` groups without the burst and 8 `notice-burst-<k>` groups with the composed burst 6 ms after the answer (`notice_window.py` `every_groups`; `tb/verilator/ctrl_service_budget/README.md:160`; `worst.txt`). The row's figures are right. Only the description is off.
- **Exact fix.** Replace "every port answering, then a burst (16 groups)" with "every notice the model holds pending at once and every port answering at the same attempt, 8 phases without and 8 with the composed burst 6 ms after the answer (16 groups)".

**Wording and comment-rule scan.** The delta is unchanged since R941-2, so no source comment is new this round and there is no new lane-label or round-label residue in source. The PR body's `[A844]` header and the packet's "A844" are PR and packet text, which the comment rule allows.

## Prior public findings, resolved or retained at this head

| Finding | Disposition |
|---|---|
| R941-2-F1 MINOR, "notice 140 ms" not measured | **Resolved.** The three arms ran at both points from a clean clone of the head, with published identity, results, tables, rc and verdict lines. There are 0 refusals and 0 notice_misses. The worst rows are stated in the PR and match my recomputation (table above) |
| R941-2-F2 MINOR, 47 cuts against 44 accounted | **Resolved.** The counts reconcile: 38 = 36 + 2 and 9 = 8 + 1. Each of the three is identified by scenario, input, no bind since the previous cut and no hold reading, and the PR states the 47 and the 44 |
| R941-2-RES1 RESIDUE, LUT attribution | **Resolved** with the exact prescribed text |
| R941-2-RES2 RESIDUE, "byte-identical" firmware | **Resolved** by the second prescribed option |
| R941-2-S1 SUGGESTION, 0.75 / 0.76 | **Done** |
| R941-2-S2 SUGGESTION, the 16 extra tests | **Done**, and confirmed by my gate re-run |
| R941-2-S3 SUGGESTION, size-fixture arms still from round 1 | Not in this round's scope. It stays optional, since the arms' inputs are unchanged |
| R942-1-F1 / F2, R941-1-RES1 / S1 / S2 | Carried as R941-2 disposed them. Nothing at this head changes them |

## Lens results

```text
[R941] PASS RTL - git diff --stat c34e7d8b..079c4fa1 (31 files under sw/firmware/ctrl_nvm, tb/verilator, docs; no HDL/SoC/gateware) and notice-arms/*-identity.txt (Vsim/ELF of the head) - no RTL in the delta and no change since R941-2; the notice arms on the head's simulated SoC show 0 traps, 0 bus errors and longest step pass 1.102 ms against the 2.0 ms share
[R941] MINOR Conformance - board/summary-8x8-input0.txt; cuts/cuts-8x8.txt si0 attempts; PR body lines 164-173 - R941-3-F1 (criterion 2's fourth 8x8/1if scenario rests on an unpublished test correction); the notice part of ruling 3 item 3 is otherwise clean against the six results.json and FR_NFR.md:416-417
[R941] MINOR Robustness - board/summary-8x8-input0.txt; r2 board/summary-8x8.txt sink line 28 - R941-3-F1 (restore after a power cut at si0 shown only by the corrected test); the per-cut durability of all 44 graded cuts and the 3 bindless retries is clean (receipts-check_cuts.txt)
[R941] MINOR Tests - board/summary-8x8-input0.txt (no test identity) - R941-3-F1; the notice arms' grading (grade.py:530, notice_window.py:170, run.py:368-389) and the store gate re-run (receipts-gate-store-tally.log, 656 tests PASS) are clean
[R941] MINOR Docs - PR body lines 164-173 (0.62 s, settle diagnosis, 4.74 / 4.73 s with no receipt) - R941-3-F1; plus R941-3-RES1 (wording only); RES1, RES2, S1 and S2 of R941-2 verified in PR-BODY.md
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: R941-3-F1 | Ruling 3 items 3-4; issue criteria 1-4; FR_NFR.md:416-417; the six notice-arm `results.json` and identity files; `cuts/*.txt`; r2 board summaries; `summary-8x8-input0.txt` | R941-3 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| RTL | CLEAN | delta stat (no HDL); arms' Vsim identity and summaries (0 traps, 0 bus errors); R941-2's RTL coverage of the unchanged delta | R941-3 (R941-2 at the same head) | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Robustness | UNCLEAN: R941-3-F1 | 44 graded cuts plus 3 retries against the summaries; the si0 rerun receipt | R941-3 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Tests | UNCLEAN: R941-3-F1 | `grade.py:530`, `notice_window.py:64-83,150-180`, `run.py:368-389`; store gate re-run (656 tests); the si0 rerun receipt | R941-3 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Docs | UNCLEAN: R941-3-F1 (R941-3-RES1 is residue only) | `PR-BODY.md` (equal to the live body), packet `README.md` and `REVIEW-READY.md` | R941-3 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |

## Probes and receipts (this packet)

- `scripts/check_cuts.py` and `receipts-check_cuts.txt`: an independent recount of the power cuts against the round-2 summaries.
- `scripts/check_notices.py` and `receipts-check_notices.txt`: an independent recomputation of the notice arms' rows, bounds and misses, plus the MRPDU-per-group check.
- `receipts-gate-store-tally.log`: `test_ctrl_nvm.py --require-rv32 --jobs 16` at the head, 0 status entries before and after, rc 0. It gives the per-binary tally behind S2.
- `receipts-clone-integrity.txt`: after the probes the clone is at HEAD `079c4fa1…` and tree `be2122cb…`. Worktree, index and HEAD agree in mode, blob and path. There are 0 porcelain entries, the six submodule gitlinks are as at the head (`external` not initialized, as published), and the ignored `__pycache__` directories were removed.

## Real limits

- **Physical calibration NOT RUN.** No hardware was touched. Every board figure is the author's published summary, checked for internal consistency and against its listings only. A field skip or a summary is not hardware proof.
- I did not re-run the notice arms (about one hour each). Their results are accepted on their identity and hash binding, and on my recomputation from the published `results.json`.
- The board grader and the power-cycle test are outside this repository. I could not inspect the test correction that R941-3-F1 concerns.
- No manager source bank exists or is inferred at this head. I did not inspect hosted runs or act this round.
- Code the delta does not touch, and the delta itself, keep R941-2's and R941-1's lens verdicts, since nothing changed since R941-2.

## Pending manager duties

- The current-dev merge candidate: source base `c34e7d8b` on live dev `e275d795`, with the builder and native banks and their receipts.
- Hosted and act acceptance at the exact head.
- A ruling on R941-3-F1 route 2 if the board harness's correction is to be accepted on the qualification lane's evidence.
- The PR's own "Before it lands" items: the boot comparison and the decision on board reading resolution.
- Carrying R941-3-RES1 to the residue checklist.

R941-3 FINISHED

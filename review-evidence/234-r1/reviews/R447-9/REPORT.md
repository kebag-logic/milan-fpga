[R447] POSITIVE - exact head 68d26ea034789ce2519db22d0df4e4328bc1b0de

# R447-9: external re-review of issue #234 / PR #638, PR body only, at the unchanged head

- Head `68d26ea034789ce2519db22d0df4e4328bc1b0de`, tree `4bc95158cc7e2b5f64051a100b770298ef194a70`. Both were verified in the clone, which is clean (`receipts/restore-verify.txt`).
- Live dev is `5fabb46e767c9308ab2580916237f43577698c6e`, an ancestor of the head. Against it the PR is the same 15 files, with no HDL, configuration, constraint, Yosys or gitlink path (`receipts/delta-scope.txt`).
- PR body read at 2026-10-03T21:17:00Z (`receipts/pr-body-live.md`, last edited 21:06:51Z). It was read again before this report was written and was byte-identical.

## Verdict

**POSITIVE.** Both round-8 items on the PR body are resolved:

- **R447-8 F1 (MINOR):** the "Gate on real data at this head" paragraph now gives every verdict against the committed record C.
  - Every figure in it matches the published round-7 receipts.
  - I reproduced every verdict with the gate's own `judge()` against the committed record.
- **R447-8 R2 (RESIDUE):** both occurrences of the old head now read `68d26ea0`.

The body's only change since round 8 is on those three lines.

This round raises three new findings, all RESIDUE (R3, R4 and R5), each with its exact fix. All three are wording or citation. None changes a figure or a verdict, and I checked that each underlying fact holds at this head:

- the gate verdicts, with `judge()`;
- the gates, with 42 of the executor's 43 rerun at rc 0 here;
- the attribution, from the findings page.

R4 is a side effect of my own round-8 R2 fix. That fix replaced the head SHA but left the sentence's other head-bound claims as they were.

The other prior findings are carried as they stood, all RESIDUE or SUGGESTION:

- R447-8 R1, carried to #495;
- R446-5 R1;
- R447-8 S1 and S2, and the earlier suggestions.

## What I examined, in order

1. AGENTS.md (sections 3, 6 and 7), the #234 acceptance as ruled, and the round-7 and round-7b assignments: issue comments 5967852698, 5972491855 and 5973328289. Also the executor's round-7b REVIEW READY (5973356984) and the review-start comment 5973558906.
2. **The body diff.**
   - I took the round-8 body from GitHub's edit history of the PR body: the 20:51:12Z edit, the version live while round 8 ran (21:05Z), saved as `receipts/pr-body-r8-edit-2026-10-03T20-51-12Z.md`. Round 8 did not save its own snapshot, so this is the reconstruction.
   - Its line numbers match round 8's report: F1 at line 60, R2 at lines 22 and 429, R446-5 R1 at line 286.
   - `diff` against the live body changes exactly lines 22, 60 and 429 (`receipts/pr-body-r8-to-live.diff`). Neither copy contains a CR.
3. **The published round-7 receipts.**
   - Evidence commit `22b292d3ac9c3f80131e07d4e2a16e8afd068578`, `review-evidence/234-r1/author-r7/receipts/`:
     - `final-real/gate-check-{A,B,C}-{route,ooc-1x1,ooc-8x8}.{log,rc}`;
     - `real/pre-check-C-*`;
     - `gates/gate-results.json`.
   - Round 1 at `43ad8362`:
     - `gate-check-B-route.log`, `# rc=1`;
     - `gate-check-A-ooc-1x1-10ns.log`, `# rc=2`;
     - the published A and B records.
   - All are copied byte for byte under `receipts/r7-evidence/` and `receipts/r1-evidence/`.
4. **Independent reproduction.** `judge_against_record.py` imports the gate at this head. It judges the seven published A and B records, the 10 ns control included, against `syn/ooc/pp_resource_baseline.json` as committed (`receipts/judge-against-committed-record.txt`).
5. **The executor's round-7 gate list** (43 gates, run at `aabdc283`), rerun at `68d26ea0`: 42 of 43 at rc 0 (`receipts/gates/`, `run_gates.sh`).
   - `em-dash` and `diff-check-base` use `--base 5fabb46e`.
   - `gptp-docs-make` was left out. It runs `make` inside the unchanged `gptp-processor` submodule, which is outside this review's allowance, and the head's delta since `aabdc283` touches no file it reads.
6. The hosted check runs at the exact head, read only (`receipts/hosted-check-runs.tsv`).

## The changed paragraph (line 60), claim by claim

| Claim in the body | Published receipt | Reproduced at this head (`judge()` against the committed record) |
|---|---|---|
| C's three endpoints exit 0 at 0 deltas | `final-real/gate-check-C-*.rc` = 0; LUT and FF deltas 0 on all three | C's figures are the record's own |
| A exits 0 on all three, "re-baseline recommended" on the route (-639 LUT) | `gate-check-A-*.rc` = 0; route line 14 "re-baseline recommended: LUT, FF improved…"; -639 / -628 | rc 0, 0, 0; route -639 LUT / -628 FF |
| B exits 0 on the route at -14 LUT | `gate-check-B-route.rc` = 0; -14 LUT / -620 FF | rc 0; -14 / -620 |
| B's standalone endpoints exit 0 (+173 / -166 LUT) | `gate-check-B-ooc-1x1` +173, `-8x8` -166, rc 0 | rc 0 / 0; +173 / -166 |
| Against the first record, B's route exited 1 (+625) | round 1 `gate-check-B-route.log`: +625, "MATERIAL REGRESSION", `# rc=1` | (first record; not re-judged) |
| Against the first record, C's route exits 1 (+639 / +628) | `real/pre-check-C-route-1x1.rc` = 1; +639 / +628, both "REGRESSION" | (first record) |
| A's 1x1 control at 10 ns exits 2 (standalone clock identity) | round 1 `gate-check-A-ooc-1x1-10ns.log`: `# rc=2`, "NOT COMPARABLE: … standalone_clock_ns" | rc 2, same reason: the record's `ooc-1x1` clock is `20.000`, the control's `10.000` (`receipts/first-record-rcs.txt`) |

Line 22 now names `68d26ea034789ce2519db22d0df4e4328bc1b0de`, and so does line 429, the `git switch --detach` command. No other line of the body changed.

## Findings

[R447] R3 RESIDUE Docs, RTL - PR #638 body, line 60 ("only because B lacks PR #634's meter") and line 457, Known limitations ("only because it lacks the meter") - the cause of B's pass is attributed to the meter alone

- **Authority and evidence:** `receipts/r3-attribution.txt`.
  - B's pass against C's record does not turn on the meter.
  - B with the meter and no other PR #634 change would sit at -14 + 483 = +469 LUT and -620 + 630 = +10 FF. Both are under the route tolerances, so it would still exit 0.
  - B passes because C's record carries all of PR #634's +639 LUT. Of that, the meter is 483 (`docs/findings/234_PP_SHADOW_AREA_BASELINE.md:70-78`, `docs/design/AREA_BUDGET.md:123`), and B's `1269cdaf` tree has none of it.
  - The repository pages state the split correctly.
  - The phrase on line 60 is the wording I prescribed in round 8's required outcome. Round 8 also missed the same phrase on line 457.
- **Impact:** prose only. No figure, verdict or receipt changes. Line 457's next sentences already say the pass says nothing about the next adoption.
- **Exact fix:**
  - line 60: "only because B lacks PR #634's +639 LUT of growth (the meter's 483 the largest part), which C's record carries";
  - line 457: "but only because it lacks PR #634's growth, the meter's 483 LUTs the largest part".
- **Verification:** both lines read as above.

[R447] R4 RESIDUE Docs, Tests - PR #638 body, Status, line 22 - after R2's substitution, two head-bound claims in the sentence describe `aabdc283`, not the named `68d26ea0`

- **Authority and evidence:**
  - "(the merge and three commits on round 6's `d5f56313`)": since `d5f56313` there are now two merges, `4d81e10d` and `68d26ea0`, and three commits.
  - "43/43 touched local gates rc 0 … at the head": the 43 ran at `aabdc283` and `4d81e10d` (`receipts/r7-evidence/gate-results-r7-head.json`, head `aabdc283`, and body line 412). At `68d26ea0` the executor ran round 7b's subset (body line 387, comment 5973356984).
  - Round 8's R2 exact fix caused this: it swapped only the SHA.
  - The underlying fact holds at this head: I reran 42 of the 43 at `68d26ea0`, all rc 0 (`receipts/gates/summary.txt`).
- **Impact:** wording and provenance only. The gates are green at the named head.
- **Exact fix:** "…43/43 touched local gates rc 0 under GNU Make 4.3 at round 7's head `aabdc283` and at the merge commit `4d81e10d`, and round 7b's docs gates, gate self-test and `check-baseline` rc 0 at `68d26ea0` … Head `68d26ea034789ce2519db22d0df4e4328bc1b0de` (round 7's merge and three commits on round 6's `d5f56313`, then round 7b's `--no-ff` merge of dev `5fabb46e`)."
- **Verification:** line 22 reads as above.

[R447] R5 RESIDUE Docs, Conformance - PR #638 body, line 60, last sentence ("Receipts: the round-7 packet's `final-real/gate-check-{A,B,C}-*`") - the pointer does not reach three of the paragraph's verdicts

- **Authority and evidence:**
  - B's first-record exit 1 is in round 1's `gate-check-B-route.log`.
  - C's first-record exit 1 is in round 7's `real/pre-check-C-route-1x1.*`.
  - The 10 ns control has no round-7 receipt. Its only receipt is round 1's `gate-check-A-ooc-1x1-10ns.log`, judged against A's record.
  - Against C's record it still exits 2 (`receipts/judge-against-committed-record.txt`), because the record's standalone clock is unchanged at `20.000` ns.
- **Impact:** a citation only. Every claim holds, but a cold reader following the pointer finds three of the verdicts elsewhere.
- **Exact fix:** "Receipts: the round-7 packet's `final-real/gate-check-{A,B,C}-*` and `real/pre-check-C-*`; round 1's `gate-check-B-route.log` and `gate-check-A-ooc-1x1-10ns.log` (the record's standalone clock is still 20 ns, so the control's identity refusal stands against C)."
- **Verification:** the sentence reads as above.

No BLOCKER, MAJOR or MINOR finding is open.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (R5 RESIDUE) | #234 criterion 4 as ruled (5967852698): the body's real-data verdicts against `final-real/*.rc`, `real/pre-check-C-*`, round-1 `gate-check-B-route.log` and `-10ns.log`. Every verdict reproduced by `judge()` against `syn/ooc/pp_resource_baseline.json` (`receipts/judge-against-committed-record.txt`: rc 0×6, rc 2 for the 10 ns control). `check-baseline` "baseline PASS: 3 endpoints" (`receipts/gates/resource-gate-check-baseline.log`). | R447-9 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| RTL | CLEAN (R3 RESIDUE) | No HDL, configuration, constraint, Yosys or gitlink path in the PR against dev `5fabb46e` (`receipts/delta-scope.txt`); gitlinks `631eeb34`, `5dce647a`, `48ff7a7e`, `efeb541a` (`receipts/restore-verify.txt`). Resource attribution in body lines 60, 405-408 and 457 checked against `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:36-78` and `AREA_BUDGET.md:123` (`receipts/r3-attribution.txt`). | R447-9 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| Robustness | CLEAN | Identity refusal on real data: the 10 ns control gives rc 2 against the committed record through `judge()` (`pp_resource_gate.py:319-323`). `resource-gate-selftest` (260 arms, 500 cases, digest `151eb3fc6a0d989c`, malformed-baseline arms) and `resource-gate-mutants` (174 of 174 fail) at this head (`receipts/gates/`). The body's robustness statements (lines 460-464) are unchanged since round 8 (`receipts/pr-body-r8-to-live.diff`). | R447-9 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| Tests | CLEAN (R4 RESIDUE) | The executor's 43-gate list, 42 rerun at this head, all rc 0, every log headed with `68d26ea0` (`receipts/gates/*.log`, `summary.txt`, `gates.list`), including `ooc-tcl-selftest` (475 s), `pp-baseline` self-test and mutants, `ci-scope`, `ci-events`, `py-idiom`, `test-evidence` and `em-dash --base 5fabb46e` (0 findings over 746 added lines). Gate and test code is the same blob set as round 8 (unchanged head). | R447-9 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |
| Docs | CLEAN (R3, R4, R5 RESIDUE; R447-8 R1 and R446-5 R1 RESIDUE retained) | The live PR body (`receipts/pr-body-live.md`), byte diff against the round-8 version (`receipts/pr-body-r8-to-live.diff`: lines 22, 60 and 429 only). `docs/design/AREA_BUDGET.md:115-123,184`; `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:30-110`. Docs gates at this head: `docs-check` with and without git, `toc-check`, `toc-verify-anchors`, `doc-paths`, `doc-style`, `doc-map-check`, `archive`, `module-matrix-check`, `solution-docs`, `feature-status`, all rc 0. | R447-9 | `68d26ea034789ce2519db22d0df4e4328bc1b0de` |

## Prior findings at this head

I wrote this section after the verdict, findings and ledger above.

| Prior finding | State at `68d26ea0` | Evidence |
|---|---|---|
| R447-8 F1 (MINOR Docs): line 60 gave B's route as exit 1 and stale standalone deltas | **Resolved** | The table above: every figure and verdict matches the receipts and the `judge()` reproduction. The required outcome is met: A three exit 0 with "re-baseline recommended", B route 0 at -14 and standalone +173 / -166, and the first-record verdicts labelled. The causal phrase I prescribed is corrected under R3. |
| R447-8 R2 (RESIDUE Docs): head named `aabdc283` at lines 22 and 429 | **Resolved** as specified | Both lines now read `68d26ea034789ce2519db22d0df4e4328bc1b0de`. The fix was incomplete, which R4 records. |
| R447-8 R1 (RESIDUE Docs): `docs/design/AREA_BUDGET.md:184` | **Retained** as RESIDUE, carried to #495 at merge | Line 184 is unchanged: "Accepting B means recording its route as the new baseline, a reviewed decision." Round 8's exact fix stands. |
| R446-5 R1 (RESIDUE Docs, body line 286) | **Retained** as RESIDUE | The body still says "run by `strict()` on every JSON the gate reads". R446-5's exact fix stands. |
| R447-8 S1, S2, and the earlier suggestions round 8 retained | **Retained**, optional | Unchanged head. |
| Every BLOCKER, MAJOR and MINOR of earlier rounds | **Remain resolved** | Unchanged head. The self-test, mutants and `check-baseline` rerun green here. |

## Hosted evidence at the exact head (read only, 2026-10-03T21:29:52Z)

- 16 completed success.
- 3 in progress: Verilator shards 1, 2 and 4 of 5.
- 1 skipped: Physical gPTP, nightly and manual. A skip is not an executed job.

Hosted and act acceptance belong to the manager.

## Real limits

- No Vivado run. A, B and C are judged from published records and receipts.
- The 10 ns control against C is a `judge()` replay of the published round-1 record, not a new measurement.
- `gptp-docs-make` was not rerun (see above).
- Physical calibration was not run, and skipped hosted contexts are not hardware proof.
- The round-8 body was reconstructed from GitHub's edit history, not from a round-8 snapshot.
- At my read time, I found no public manager receipt for the full static, builder and native banks at this head, on the PR, on the issue or on the evidence branch tip `3ff83770`. This review does not depend on one.
- I did not read any other reviewer's report for this round.

## Pending manager duties

- Hosted acceptance at the exact head: Verilator shards 1, 2 and 4 were still in progress at my snapshot. Act acceptance too.
- Validation of the final current-dev candidate at the merge turn. Live dev is still `5fabb46e`, already merged into the head.
- Carry the residues R3, R4 and R5 (this round), R447-8 R1 (#495) and R446-5 R1 to the residue checklist.
- Merge only with maintainer authorization, then post-merge containment.

R447-9 FINISHED

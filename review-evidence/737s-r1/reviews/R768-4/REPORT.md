[R768] POSITIVE - exact head 9104a8fc68979a7a8795859e8704aef27ea0634d

# R768-4: external review of PR #836 (Issue #737), round 4

- **Head:** `9104a8fc68979a7a8795859e8704aef27ea0634d`, tree `858d8230dbb684404e9b1a3c033ebfe6aa68ddc7`. The live PR head equals this head. The PR is open, not a draft, with base `dev`.
- **Source base and live dev:** `e61a4afaa54a598ceec08b7b5879285256cc60b6`.
- **Round 4 delta:** `3b323864..9104a8fc`, three commits. Four files change:
  - `scripts/ci_litex_legs.py`;
  - `scripts/ci_gate_workflows.py`, a comment only;
  - `ci/image/command-table.json`, one pin;
  - `docs/testing/CI_WORKFLOWS.md`.
  
  The PR body changes too.
- **Authority:** the manager's round 4 ruling on #737 (issuecomment-6615561789), items 1 to 4 and its "take in the same pass" list.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open. Three RESIDUE items (wording and wrap only) and one SUGGESTION are listed below, so the author can take them in one pass.

## Method

1. **Reading order.** I read AGENTS.md, the ruling, the REVIEW READY comment, the PR body and the delta. I did my own pass over the delta before opening any prior report.
2. **Evidence packet.** I downloaded `review-evidence/737s-r1/author-r4/` from evidence commit `24a7eef7` blob by blob.
   - All 80 blobs match their git blob ids.
   - All 79 `author-r4/` entries match `published_sha256` in `MANIFEST.json`, and no file is unlisted.
   - The evidence commit has no cryptographic signature (`verification.reason = unsigned`); see Real limits.
   - The live PR body is byte-equal to `author-r4/PR-BODY.md`.
   - Every author receipt `.rc` names head `9104a8fc…`. Every gate exits 0. The two refusal controls, `g10a` (`union`) and `g11b` (verifier), exit 1 by design.
3. **Hosted data, fetched independently.** I fetched the jobs API for run 41705989293 attempts 1 and 2 myself (`receipts/hosted/jobs-41705989293-a{1,2}.json`).
   - They equal the author's copies on job id, name, timestamps, conclusion and every step.
   - I recomputed every component with my own script (`scripts/recompute_r4.py`, which writes `receipts/recompute-41705989293.txt`).
   - I read attempt 2's three LiteX job logs for their verdict rows.
   - I spot-checked leg 0's step boundaries: 20:37:11.488 to 20:45:12.121 is 480.63 s, against a 477 s row.
4. **Local probes at the exact head**, on 16 CPUs:
   - the command-table pin (`p01`);
   - `ci_litex_legs.py legs`, `ci_litex_legs_selftest.py`, `ci_gate_workflows.py --check` and `ci_gate_workflows_selftest.py` (`p02`, each rc 0);
   - a `LEG_BUDGET` boundary probe on a disposable `git archive` copy (`scripts/budget_probe.sh`, `p03`);
   - a tree, delta-path and comment-rule scan (`p04`);
   - a wrap scan, a stale-figure grep and a tree-integrity check (`p05`). The worktree and index equal HEAD, and the submodule gitlinks are unchanged.
5. **Exact-head hosted runs.** I recorded the four runs at `9104a8fc` and judged them only by ruling item 3.

## Check (1): the re-measurement, recomputed over the frozen set

These are run 41705989293 attempts 1 and 2, from the jobs API, in whole seconds. Every stated figure agrees with my recomputation.

| Component | Stated | Independent result |
|---|---:|---|
| Setup (span less gate steps less Verilator build) | 739 | `elaborate-gates-1` attempt 2: 1449 - 710 - 0 = 739. Every other worker in both attempts is 197 to 559 |
| `test_gptp_tx_timestamp` (`LARGEST`) | 477 | attempt 2 leg 0 log: `PASS test_gptp_tx_timestamp (477s)`. Attempt 1: 459 |
| Self-test (leg step less rows) | 4 | attempt 2 leg 0: 481 - 477 = 4. The other five legs: 3, 2, 3, 3, 2 |
| Cold Verilator | 431 | this run at most 393, so run 41678609075's figure stands |
| Builder legs 0 / 1 | 1130 / 1119 | this run: 1010 and 1098 / 737 and 710 |
| Collector | 183 | attempt 1: 183 (attempt 2: 182) |
| Tail | 29 | attempt 1: 29 |
| Depth-one checkout | 26 | `Cancel late CI failures` attempt 1: 26. The aggregate's checkouts are 3 and 15 |
| Aggregate span less checkout | 85 | this run: 18 and 14, so run 41678609075 attempt 3 stands |
| Worker checkout / LiteX install / VexiiRiscv placement | 274 / 277 / 108 | 274 (w1 a2), 277 (w2 a1), 108 (w1 a2) |
| Other `LARGEST` rows | unchanged | attempt 2 rows (70/0/25/14/331, 277/472) are each at or below `LARGEST` |

The derived figures agree across the code, `CI_WORKFLOWS.md` and the PR body. I did the arithmetic by hand, and the author's `components.txt` gives the same results.

- **`LEG_BUDGET`** = 2700 - 600 - 739 - 431 - 4 = 926.
  - It is at `scripts/ci_litex_legs.py:80`, with its constants at lines 65-76.
  - The same figure is at `CI_WORKFLOWS.md:1678` and `:3169`, and in the PR body's Round 4 table.
- **Legs at `LARGEST`:** 477 / 448 / 794, which fit. The partition from `SECONDS` is unchanged (`p02`).
- **Projections against 2700 s:**
  - builders: 739 + 1130 = 1869 and 739 + 1119 = 1858, margins 831 and 842;
  - LiteX cold: 739 + 431 + 4 + leg = 1651 / 1622 / 1968, margins 1049 / 1078 / 732;
  - LiteX with Verilator restored: 1220 / 1191 / 1537.
  
  The table at `CI_WORKFLOWS.md:3238-3242` matches.
- **Measured spans are below their projections.**
  - Attempt 1, cold: 1414 / 1148 / 1233.
  - Attempt 2, warm: 907 / 909 / 948.
  - Builders: 1535 and 1449, against 1869 and 1858.
- **Aggregate:** 26 + 85 = 111, with 69 s of margin under 180. The comment at `scripts/ci_gate_workflows.py:62-63` matches.
- **Allowance:** 111 + 183 + 120 + 29 = 443.
- **Workflow figure:** 1869 + 443 = 2312 s (38.5 min, 512 s over 1800), and 1968 + 443 = 2411 s (40.2 min, 611 s over 1800).
- **Pin:** `ci/image/command-table.json:13614` equals the sha256 of `scripts/ci_litex_legs.py` at the head (`p01`).

**The author's departures from the ruling's arithmetic, judged on their evidence:**

- **`LEG_BUDGET` 926 instead of 927: accepted.**
  - The ruling quoted 927 with a 3 s self-test.
  - Round 3's own method is the leg step less its verdict rows, in whole seconds. Over the frozen set it gives 4 (481 - 477, attempt 2 leg 0). The log's 480.63 s against a 477 s row agrees.
  - The ruling's principle is "the maxima over the frozen set as you measure them, and state the arithmetic". Keeping 3 would state a maximum the frozen set exceeds.
  - 926 is the stricter budget, and the partition still fits.
- **Allowance 443 instead of 436: accepted.** The aggregate's checkout is a named component under the rule (`CI_WORKFLOWS.md:3192-3194`). Its depth-one maximum over the frozen set is 26 s (`Cancel late CI failures`, attempt 1), so keeping 19 would break the rule.
- **Workflow figure 2312 / 2411: accepted.** It follows from the two departures above. It is stated as a measurement against #737 acceptance 1, not as a bound.

**Control (`p03`).** The budget refuses 927 and accepts 926 on two different legs:

| Probe | Result |
|---|---|
| `LARGEST` `test_gptp_tx_timestamp` = 927 | refused: "a LiteX leg holds 927 measured seconds at its largest, above its 926" |
| `LARGEST` `test_gptp_tx_timestamp` = 926 | accepted |
| Leg 2 at 926 (`test_soc_timing_cuts` 642) | accepted |
| Leg 2 at 927 (643) | refused |
| `SELFTEST = 3` (the ruling's 927 budget), gptp at 927 | accepted, so the control tells the two budgets apart |

After the restore the file equals the head. The author's `g10-control-largest-over-budget.txt` agrees.

## Check (2): the frozen set and the merge bar

- **The freeze meets ruling item 2.** `CI_WORKFLOWS.md:3187-3191`:
  - freezes the cited runs at the list at `:3137-3141`, which is the list after step 1;
  - says that hosted runs at later heads, "including those of the change that set these figures, do not reopen them";
  - applies "a later hosted measurement" only to "the next re-measurement under #737 acceptance 1".
- **The merge bar meets ruling item 3.** `CI_WORKFLOWS.md:3201-3206` sits directly after the re-measurement rule. It names four findings:
  - a job at its timeout;
  - an elaborate worker's span above 2100 s;
  - a LiteX simulation unrun, run twice or unreported;
  - a refusing union verifier.
  
  A component above its figure is recorded as an observation for acceptance 1.
- **The PR body links the ruling in one sentence**, in the Round 4 paragraph at body line 94, and states the same bar.
- **Scoping the 2100 s line to the elaborate workers: accepted, matching the ruling's intent.**
  - The ruling's parenthetical, "its 2700 s limit less the 600 s headroom", defines the line only for jobs with a 2700 s limit and the stated 600 s headroom. Those are the five 45-minute elaborate workers.
  - The watcher `Fail fast across this head` runs for the life of the workflow under a 120-minute limit (`elaborate.yml:1350`). It ran 2299 s at `3b323864` and 1940 s here, so a literal reading would fail every run.
  - The 45-minute jobs in `docs.yml` and `rtl-fast.yml` carry their own 60% bounds, not this headroom.
  - Every job is still judged by "a job reaches its timeout".
  - The manager's review brief states the bar the same way.

## Check (3): residues and suggestions taken in this pass

I judged each prior finding at its cause at this head, after my own pass over the delta.

| Prior finding | State at 9104a8fc |
|---|---|
| R767-3-F1 = R768-3-F1 (exact-head run above the stated figures) | **Resolved by ruling items 1 to 3.** Run 41705989293 attempts 1 and 2 are cited and every figure is recomputed and agrees (Check 1). The set is frozen and the merge bar is written (Check 2). |
| R768-3-F2 (`rtl-full` union 2-minute limit) | **Settled by the ruling** as #837's class, because `rtl.yml` is unchanged by #836. At this head `rtl-full` was still running when this report was written (see Hosted). |
| R767-3-R1 | **Resolved.** `CI_WORKFLOWS.md:3147-3149` reads "Their largest measured job times with the LiteX legs apart are 1535 … and 1449". That is the exact fix, with the figures re-measured under item 1. 1535 is `elaborate-gates-0` attempt 1 and 1449 is `elaborate-gates-1` attempt 2, both verified. `:3285`'s "1535 and 1233" needs no scope, because both are maxima over every cited run (`components.txt` lines 112-116). |
| R767-3-R2 | **Resolved, in both the docs and the PR body.** `CI_WORKFLOWS.md:3170-3172` carries the exact docs text. The PR body's Round 3 item 1 reads "The gate workflow self-test requires". How to validate (line 224) reads "fails `ci_gate_workflows_selftest.py` in its LiteX leg controls". The attribution still holds: `worker_controls` (`ci_litex_legs_selftest.py:158`) is called from `ci_gate_workflows_selftest.py:546`, which passes at this head (`p02`). |
| R768-3-RS1 | **Resolved.** `CI_WORKFLOWS.md:3216` reads "on metadata that builder leg 1 had generated", and no other instance remains. |
| R768-3-S2 | **Taken.** The overlong line at `:1674` is gone. The reflow stopped one line early and leaves a 53-character seam at `:1679`, folded into R768-4-RS1. |
| R767-3-S2 | **Taken.** Round 2's "Derived per job" table and workflow paragraph sit under `## Superseded (round 2)` (body line 135), with a contents entry. The section comes after Round 4, so it is still after Round 3. |
| R767-3-S1, R768-3-S1 and the round 3 observations | Declined by the ruling and not taken, which is correct. R767-3-S1 is now #837. |

**Comment rule.** The added source-comment lines (`p04`) carry run ids, worker numbers and `#737` only. They contain no bench lane label, lane name, review round, reviewer id or issue-comment id, so there is no new instance.

## Hosted at 9104a8fc, judged by ruling item 3 only

This is a snapshot at 23:07 UTC, from `receipts/hosted/runs-9104a8fc.tsv` and `jobs-*.json`. No job in any of the four runs has a conclusion other than success or skipped.

**`elaborate`, run 41732022509 attempt 1: completed success, all 9 jobs at head `9104a8fc`. Clean under item 3.**

- **Timeouts:** none reached.
- **Elaborate worker spans:** 1216 / 1260 / 627 / 591 / 876 s. The largest, 1260 s, is 840 s inside the 2100 s line.
- **LiteX simulations:** each of the 8 inventory members has exactly one `PASS` row across the three LiteX logs (`receipts/hosted/exact-head-litex-rows.txt`):
  - leg 0: gptp 457;
  - leg 1: cpu 67, gmii 1, boot 23, mem 14, retained 305;
  - leg 2: ctrl 270, soc 478.
- **Union verifier:** `ci_gate_receipts.py verify` passed, logging "elaborate: 5 source gates exactly once; all worker jobs successful".
- **Observations, not findings:**
  - Every component is at or below its frozen figure. Setup is at most 223, self-test at most 3, the collector 40, the tail 7, and the aggregate 14 with a 3 s checkout. Every row is at or below `LARGEST`.
  - The workflow took 1951 s from first job start to last job end, above 1800 s. This is the open #737 acceptance 1, as stated.
  - The watcher took 1940 s, under its 120-minute limit.

**The other three runs were unfinished at the snapshot:**

| Run | State at the snapshot |
|---|---|
| `docs` 41732022313 | 8 of 9 jobs succeeded and 1 is queued. The longest is `docs-gates-1`, at 1111 s |
| `rtl-fast` 41732022398 | 15 of 16 succeeded and 1 is in progress |
| `rtl-full` 41732022450 | 12 succeeded, 1 was skipped and 14 are in progress. No failure |

Judging these by item 3 is a pending manager duty. A failure in `rtl.yml`, which this PR does not change, is judged by its cause, and the union 2-minute limits are #837.

## Findings

No BLOCKER, MAJOR or MINOR.

### R768-4-RS1 - RESIDUE - Docs - wrap seams in the re-measured paragraphs

- **Where:** `docs/testing/CI_WORKFLOWS.md`, which wraps at about 78 columns.

  | Line | Length | Note |
  |---|---:|---|
  | `:1679` | 53 | "simulation cannot join a leg unmeasured. `LEG_BUDGET`", where the R768-3-S2 reflow stopped |
  | `:1721` | 91 | |
  | `:3142` | 44 | "build, so it holds checkout, installs, cache" |
  | `:3149` | 31 | "run 41705989293 attempt 2). The" |
  | `:3294` | 114 | "… up to 108. Two candidates for acceptance 1 are not taken here. A" |

- **Evidence:** the line-length scan in `receipts/p05-wrap-stale-tree.txt`. Lines 3163 and 3185 in that scan are paragraph ends and are not seams. It is wrap only. It changes no figure or claim, and `git diff --check` is clean.
- **Exact fix:** reflow the four paragraphs at `:1666-1692`, `:1716-1726`, `:3137-3163` and `:3280-3300` to the file's width, changing no words.

### R768-4-RS2 - RESIDUE - Docs - the `LARGEST` comment still points at "a later hosted measurement"

- **Where:** `scripts/ci_litex_legs.py:46-51`.
- **Evidence:** ruling item 2 changed the document's rule so that it applies to the next re-measurement under #737 acceptance 1, not to later runs of this PR (`CI_WORKFLOWS.md:3187-3191`). The comment still reads "docs/testing/CI_WORKFLOWS.md states the rule a later hosted measurement follows". Line 49 also breaks short: "41705989293 (attempts 1 and 2). Every". This is comment wording only, with no code change.
- **Exact fix:**
  - Replace "docs/testing/CI_WORKFLOWS.md states the rule a later hosted measurement follows (#737)." with "docs/testing/CI_WORKFLOWS.md freezes these runs and states the rule the next re-measurement under #737 acceptance 1 follows (#737)."
  - Reflow lines 46-51.
  - Re-pin the script in `ci/image/command-table.json`.

### R768-4-RS3 - RESIDUE - Docs - "Over attempt 1's maxima" no longer names its run

- **Where:** `docs/testing/CI_WORKFLOWS.md:3290-3291`.
- **Evidence:** the paragraph now names run 41705989293, which also has an attempt 1, just before "Over attempt 1's maxima, which gave 1723 seconds". Commit `3b323864` set the 1723 s figure as the maxima through run 41678609075 attempt 1.
- **Exact fix:** replace "Over attempt 1's maxima" with "Over the maxima through run 41678609075 attempt 1".

### R768-4-S1 - SUGGESTION - Docs, Robustness - say where the 2100 s line does not apply

- **Where:** `docs/testing/CI_WORKFLOWS.md:3201-3206`.
- **Suggestion:** add one clause saying that the watcher (`Fail fast across this head`, 120 minutes) and the other elaborate jobs are judged by their own timeout only. A later reader would then not have to work out from the parenthetical why a 1940 s or 2299 s watcher span is not a finding.
- **Status:** optional. The current text is correct.

## Lens results

```text
[R768] PASS Conformance - scripts/ci_litex_legs.py:46-80, scripts/ci_gate_workflows.py:62-63, docs/testing/CI_WORKFLOWS.md:1672-1691, :3137-3206, :3238-3242, :3282-3294, PR body Round 4 (lines 90-133) - ruling items 1 to 3, checked against the jobs API of run 41705989293 attempts 1 and 2, fetched independently. Every figure recomputes and agrees. The 926 and 443 departures follow from the frozen-set maxima. The freeze and the merge bar are written, and the 2100 s scoping matches the ruling's parenthetical.
[R768] PASS RTL - git diff --name-only e61a4afa..9104a8fc (receipts/p04) - no HDL path in the PR, and only four CI and doc files in the delta. This lens's architecture content for the PR is the job-limit and leg-budget arithmetic and the partition contract. The delta changes one constant set and leaves partition() (scripts/ci_litex_legs.py:95-122) unchanged; re-checked by p02 and p03. Prior RTL verdicts on untouched code stand.
[R768] PASS Robustness - receipts/p03 (budget boundary on two legs: 926 accepted, 927 refused; SELFTEST=3 contrast accepts 927; byte-equal restore), author g10a/g11b dropped-simulation refusals (rc 1, restored rc 0), exact-head hosted run 41732022509 - clean under item 3.
[R768] PASS Tests - receipts/p02 (ci_litex_legs.py legs, ci_litex_legs_selftest.py, ci_gate_workflows.py --check, ci_gate_workflows_selftest.py: rc 0, 14 s), author receipts g01-g19 and d05-d50 at head 9104a8fc (all rc 0), real LiteX legs 518/410/643 s with each simulation PASS once, and union and verifier passing - the delta changes no test, and the budget control can fail (927 refused, p03).
[R768] PASS Docs - docs/testing/CI_WORKFLOWS.md delta hunks, live PR body = author-r4/PR-BODY.md - figures agree across code, doc and body. The named prior Docs findings are resolved (Check 3). No stale round 3 elaborate figure remains in docs/, scripts/, ci/ or .github/ (receipts/p05). The only hit is the deliberate history sentence at CI_WORKFLOWS.md:3289. Remaining wording and wrap items: RESIDUE R768-4-RS1 to RS3.
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling items 1-3; `ci_litex_legs.py:46-80`; `ci_gate_workflows.py:62-63`; `CI_WORKFLOWS.md:1672-1691, 3137-3242, 3282-3294`; PR body Round 4; jobs API 41705989293 a1/a2 | R768-4 | 9104a8fc68979a7a8795859e8704aef27ea0634d |
| RTL | CLEAN | delta and PR path list (no HDL); `partition()` and the budget constants; `elaborate.yml` limits (unchanged in the delta) | R768-4 | 9104a8fc68979a7a8795859e8704aef27ea0634d |
| Robustness | CLEAN | `p03` boundary, contrast and restore; author g10, g10a and g11b controls; exact-head hosted run 41732022509 | R768-4 | 9104a8fc68979a7a8795859e8704aef27ea0634d |
| Tests | CLEAN | `p02` tool runs; author receipts g01-g19 and d05-d50; leg receipts `litex-leg-{0,1,2}.json` | R768-4 | 9104a8fc68979a7a8795859e8704aef27ea0634d |
| Docs | CLEAN (RESIDUE RS1-RS3 carried) | `CI_WORKFLOWS.md` delta; PR body; prior Docs findings R767-3-R1/R2, R768-3-RS1/S2, R767-3-S2 | R768-4 | 9104a8fc68979a7a8795859e8704aef27ea0634d |

## Real limits

- **Unsigned evidence commit.** `24a7eef7` has no cryptographic signature. I verified the packet by git blob ids and the manifest's `published_sha256` only.
- **Author receipts not re-run by me:** `ci_events.py --selftest`, behave, `ci_scope.py --selftest`, the docs workflow steps, the act sandbox validation and the three real LiteX legs.
- **Attempt 1 rows.** The verdict rows of run 41705989293 attempt 1 come from the author's `member-rows-41705989293.txt`. I read attempt 2's rows myself. No attempt 1 row sets a maximum.
- **Earlier cited runs not re-fetched.** Their maxima were verified in round 3 and are unchanged by this delta.
- **Unfinished hosted runs.** The exact-head `docs`, `rtl-fast` and `rtl-full` runs had not finished when this report was written.
- **No manager source bank** runs at this head, and none is inferred. The current-dev merge candidate is not built here.
- **No hardware proof.** Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Judge the unfinished exact-head `docs`, `rtl-fast` and `rtl-full` jobs by ruling item 3. An `rtl.yml` failure is judged by its cause, and the union 2-minute limits are #837.
- Own hosted and act acceptance.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- Carry R768-4-RS1 to RS3 to the residue checklist.
- Confirm the second independent positive review and the full completion bar before any authorized merge. #737 acceptance 1 stays open.

R768-4 FINISHED

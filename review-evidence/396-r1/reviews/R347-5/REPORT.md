[R347] POSITIVE - exact head 07f72ad640f99c43bc1354642ad4d7ed8ba410cc

# R347-5 external independent review: issue #396 / PR #586

- **Role:** external independent reviewer, cleared context, round R347-5.
- **Exact head:** `07f72ad640f99c43bc1354642ad4d7ed8ba410cc`, tree `d1b61e4301b6cd7fcf6d2536329cb329d6ae5c67`. This is one commit on `54d9beea2888bd07369e67e5cb025d1405d03495`.
- **Source base:** `ac18b50968b12efe4d15c0a06301264b35656b31`.
- **Delta judged:** `54d9beea..07f72ad6`, six files, +111/-4 (`receipts/diff-scope.txt`, `receipts/delta.patch`):
  - `REQUIREMENTS.md`;
  - `docs/testing/TESTING.md`;
  - `tb/tools/torture_campaign.py`;
  - `tb/tools/torture_release_mutants.py`;
  - `tests/features/torture_campaign_plan.feature`;
  - `tests/steps/torture_release_steps.py`.
- **Scope check:** across the full PR `ac18b509..07f72ad6`, no file under `hdl/`, firmware or `sw/builder` changes, and no gitlink changes (`receipts/diff-scope.txt`).
- **Authorities, read in this order:**
  - AGENTS.md and CONTRIBUTING.md;
  - docs/README.md;
  - the #396 issue body and the manager's decisions 5854692245, 5854930205, 5855515133, 5855792297 and 5856062292;
  - REQ-VER-06;
  - TESTING.md 6d;
  - `KL_ptp_clock_validity.sv`, `KL_aaf_packetizer.sv` and `KL_crf_tx.sv`;
  - then the delta, the history, and the public evidence.

## Verdict summary

This delta answers R347-4 F1 exactly as the round-5 decision (5856062292) specifies:

- The oracle now counts a recorded discontinuity as contained when it lies in `[observed_start - observation_resolution_s, clear)`. The start edge is inclusive and the clear edge is exclusive (`tb/tools/torture_campaign.py:3555-3556`).
- The clearing deadline is unchanged: the last contained event plus 0.5 s plus the resolution (`:3560`). The allowance is therefore applied at the start edge exactly as at the clear edge.
- The same rule is stated identically in five places:
  - REQUIREMENTS.md:263-264, :270 and :273;
  - the TESTING 6d row (:915) and its prose (:924, :929-936, :951-955);
  - the assertion text (`:3394`, `:3399`);
  - the emitted `tu_event_window` argument (`:3581`);
  - the oracle docstring.
- Every verification the finding named was reproduced:
  - Part B of the unchanged `tu_oracle_probe.py` passes for every lag within the resolution.
  - A lone event 0.5x resolution before the start passes.
  - A lone event 2x resolution before the start fails.
  - A lone event exactly at the start passes, and T02 is killed.
  - The -0.1 s arm still fails.
- No firmware, RTL or builder change.

**R347-4 F1 is CLOSED.** No new BLOCKER, MAJOR or MINOR finding. All five lenses are covered clean at this head. Two non-blocking suggestions are recorded below.

## Findings

No BLOCKER, MAJOR or MINOR finding at this head.

### Suggestions (non-blocking; no effect on coverage)

- **S1 - Conformance, Docs - retained from R347-4 S1, now disclosed.** Under the decided containment rule, a `tu` interval that rises long before its first recorded discontinuity still passes.
  - Example: interval (0, 10.4 s) with one event at 10.0 s passes. See `receipts/r4-tu_oracle_probe.log` Part D and `receipts/start_edge_probe.log` Part 5.
  - The executor took R347-4 S1 as text:
    - TESTING.md:957-961 says the decided rule adds no separate bound for that preceding duration;
    - `test_release_tu_before_first_discontinuity` (`tb/tools/torture_campaign.py:5204`) pins PASS at 10.4 s and FAIL at 10.6 s.
  - The round-5 decision's own rationale says the wire start *lags* the cause by at most the resolution. By that rationale, an observed start more than the resolution *before* the first event is not explained by any recorded discontinuity. The original pass criterion was "no `tu` beyond holdover" (5854692245).
  - The rule is the decision owner's, and it is now public rather than hidden, so this stays a suggestion. The owner may bound the first contained event against the observed start, e.g. require it within `[observed_start - resolution, observed_start + resolution]`, in a later issue.
  - REQUIREMENTS.md does not repeat the 6d disclosure. The rule it states implies it.
- **S2 - Robustness - floating-point knife edge at exactly 1x lag.** Both edges compare binary floats.
  - `receipts/start_edge_probe.log` Part 2 and `receipts/float_edge_breakdown.log` cover 80,000 lone-event cases whose lag is entered as exactly the resolution, at absolute times near 3-277 s.
  - In 37,180 of them, the float verdict differs from exact arithmetic on the same inputs. All of these differences are at 1x lag, and every gap is at most 4.8e-15 s.
  - 2 cases are excluded when they should have been contained.
  - No case at 0.5x or 2x lag changes. The clear edge had 0 of 20,000 flips.
  - This is physically irrelevant, because capture timestamps are at best nanosecond-quantized. A bench runner that grades integer nanoseconds would make the inclusive edges exact.

## R347-4 findings at this head

| Finding | State | Evidence |
|---|---|---|
| R347-4 F1 MINOR (no start-edge allowance; a lone discontinuity is graded uncorrelated) | **CLOSED** | See the closure note below the table. |
| R347-4 S1 (pre-first-event `tu` unbounded) | Taken as text; retained as S1 above | TESTING.md:957-961; `test_release_tu_before_first_discontinuity` (`:5204`). The decision owner did not change the rule. |
| R347-4 S2 (REVIEW READY carries only the head) | Addressed | The round-5 decision again ordered a head-only notification (5856187600). The PR body's "Round 5" section states that it carries the change, validation, acceptance and open risks. Its counts match my reruns: 54 tests, 86 scenarios / 353 steps, 25 mutations. |

Closure note for R347-4 F1. Each named verification was checked at this head:

- **Oracle probe.** `scripts/prior-r4/tu_oracle_probe.py` was rerun unchanged: sha256 `62153e7e…`, equal to R347-4's MANIFEST and to blob `6a8bc63b` on `396-review-evidence@6579fbd1`. See `receipts/r4-tu_oracle_probe.log`.
  - Part A: all PASS for d = 0-0.2 s.
  - Part B: all 6 lags (1.25 µs to 1 ms, the last equal to the resolution) are PASS, anchored at the event with deadline 10.501.
  - Part B': PASS.
  - Part C: PASS.
- **Arms.**
  - `test_release_tu_start_resolution` (`tb/tools/torture_campaign.py:5184-5202`) covers:

    | Event before start | Verdict |
    |---|---|
    | 0.5x resolution | PASS |
    | 2x resolution | FAIL |
    | exactly at start, 0.001 s resolution | PASS |
    | exactly at start, zero resolution | PASS |
    | -0.1 s | FAIL |
    | exactly 1x resolution (inclusive) | PASS |
    | -0.001001 s | FAIL |
    | at clear | FAIL |
    | after clear | FAIL |

  - PASS arms also check that the anchor is the event itself.
  - The same nine rows appear as the feature outline `tests/features/torture_campaign_plan.feature:421-436`, with the step at `tests/steps/torture_release_steps.py:292-298`. The step takes the bound from the emitted plan.
  - The original -0.1 s chained arm (`:5162`) is unchanged and still fails.
- **Mutants.** `scripts/prior-r4/mutants_r4.py` was rerun unchanged: sha256 `dfb7ad14…`, killed=16, survived=0, invalid=0 (`receipts/r4-mutants_r4.log`).
  - T02 (exclusive start) is now KILLED by both gates. It survived at R347-4.
  - Informational I01 (which added a second allowance on top of the fix) is KILLED by the 2x arm.
  - The executor's `tb/tools/torture_release_mutants.py` kills 25/25 with named behavioural failures, and the source is unchanged (`receipts/gates/release-mutants.log`). These kills include the six new start-edge, event-window and text mutants (`:78-97`).
- **Texts agree with the oracle.** See the Verdict summary. The 6d prose defines the observed start as the first captured `tu=1` packet and the clear as the first subsequent `tu=0` packet. It also gives the reason for the allowance: AAF and CRF latch `tu` at frame launch.
  - This reason matches the RTL: `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:615` `etu_r <= ts_uncertain_i; //! frozen for the whole frame`, and `hdl/ieee1722/crf/KL_crf_tx.sv:501` `tu_r <= ts_uncertain_i;`.

Earlier rounds' findings (R347-1 to R347-3) stay closed. They were all closed at R347-3/R347-4, and this delta touches their artifacts only in the `tu` rule and its tests. Every earlier mutant suite that R347-4 reran is subsumed at this head by:
- the green self-test (54 tests);
- the plan feature (86 scenarios / 353 steps);
- the `@torture` tier (231 scenarios / 898 steps);
- the 25/25 repository mutation controls.

## Clean results per lens (reviewer-applied, exact head)

```text
[R347] PASS Conformance — tb/tools/torture_campaign.py:3555-3560, REQUIREMENTS.md:262-273, docs/testing/TESTING.md:915,929-936 at 07f72ad6 — containment window [observed_start - resolution, clear), inclusive start, exclusive clear, deadline from last contained event + 0.5 s + resolution, checked against decisions 5856062292 and 5855792297; all decided arms reproduce (receipts/start_edge_probe.log Part 1, receipts/r4-tu_oracle_probe.log)
[R347] PASS RTL — hdl/ieee1722/aaf/KL_aaf_packetizer.sv:615, hdl/ieee1722/crf/KL_crf_tx.sv:501, clock-validity cycle model (unchanged tu_anchor_model.py via tu_oracle_probe Part A) at 07f72ad6 — the start allowance models latch-at-launch lag; Part B passes every lag up to the resolution; no hdl/firmware/builder/gitlink change in ac18b509..07f72ad6 (receipts/diff-scope.txt)
[R347] PASS Robustness — tb/tools/torture_campaign.py:3546-3562 and SKIP arms :5173-5182 at 07f72ad6 — exactly at start, at 1x, just beyond 1x, at clear, zero resolution, pre-start GM edge plus inside step, empty and after-clear events; incomplete/non-finite/bool/negative inputs still SKIP; float edge quantified at <=4.8e-15 s (S2) (receipts/start_edge_probe.log, receipts/float_edge_breakdown.log)
[R347] PASS Tests — tb/tools/torture_campaign.py:5184-5210, tests/features/torture_campaign_plan.feature:421-436, tests/steps/torture_release_steps.py:267,292-298, tb/tools/torture_release_mutants.py:78-97 at 07f72ad6 — T02 and I01 now killed (16/16 unchanged R347-4 mutants), 25/25 repository controls killed by named tests; self-test 54 OK, plan feature 86/353 with no skips, @torture tier 231/898 (receipts/r4-mutants_r4.log, receipts/gates/)
[R347] PASS Docs — REQUIREMENTS.md:262-273, docs/testing/TESTING.md:915-961, tb/tools/torture_campaign.py:3391-3405, PR #586 body "Round 5" at 07f72ad6 — one rule stated identically in requirement, 6d row and prose, assertion text and emitted arg; decided pre-event behavior disclosed; docs_check, doc paths (850), doc style, em-dash (339/339 arms, pinned renderer), TOC gates rc 0 (receipts/gates/gate-summary.txt)
```

## Commands and results (this reviewer, exact head, foreground)

All commands ran in the detached clone at the exact head, except the mutant drivers, which work on disposable copies. Receipts are under `receipts/`.

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0; 54 tests OK |
| `python3 -B tb/tools/torture_release_mutants.py` | rc 0; 25 mutations killed; source unchanged |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | rc 0; 86 scenarios / 353 steps; 0 skipped |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | rc 0; 231 scenarios / 898 steps passed; 172 scenarios excluded by tag |
| `scripts/check_feature_status.py --self-test` / plain | rc 0 / rc 0 |
| `scripts/docs_check.py` | rc 0; 0 findings |
| `scripts/check_doc_paths.py` | rc 0; 850 paths resolve |
| `scripts/check_doc_style.py`, `scripts/check_py_idiom.py` | rc 0 |
| `scripts/check_em_dash.py --base ac18b509…` | Under the pinned renderer: rc 0; 0 findings, 339/339 arms. Under the system interpreter: rc 2, "cannot judge", because the pinned renderer is not installed. Superseded by the pinned rerun. |
| `scripts/gen_toc.py --check` | Under the pinned renderer: rc 0. Under the system interpreter: rc 2 for the same reason. |
| `--coverage-by-area --areas soak,power`, `--plan --areas soak,power --json` | rc 0 |
| `git diff --check` on the delta and on base..head | rc 0 |
| `scripts/prior-r4/tu_oracle_probe.py` (unchanged) | rc 0; Part B all PASS |
| `scripts/prior-r4/mutants_r4.py` (unchanged) | rc 0; 16/16 killed |
| `scripts/start_edge_probe.py` (new) | rc 0; decision arms OK |
| `scripts/float_edge_breakdown.py` (new) | rc 0; differences only at 1x lag, ≤4.8e-15 s |
| `scripts/clone_integrity.sh` | rc 0 |

The pinned Markdown dependencies (`tools/markdown/requirements.txt`, `--require-hashes`) were installed into a disposable virtual environment under `scratch/`. The Verilator binary was not used, because nothing in this delta or PR is RTL.

Clone integrity after all probes (`receipts/clone-integrity.log`):
- HEAD and tree are exact.
- The worktree, index and status are clean.
- All 925 tracked blobs rehash to HEAD's ids with their recorded modes.
- The gitlinks `gptp-processor` `5dce647a`, `protocol-processor` `0922e434` and `third_party/verilog-axis` `48ff7a7e` are checked out at their recorded commits.
- `external` `efeb541a` is recorded but not initialized in this clone.

Hosted evidence at this exact head, read-only (`receipts/hosted-check-runs.tsv`, sampled 2026-09-27 during this round):
- Executed with success: `changes`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`, `verilator-lint`, `full-ci-gate`, and Yosys shards 0-3/4.
- Still in progress when sampled: Verilator shards 0-4/5, `yosys-elaboration`, `elaborate` and `docs-check`.
- Skipped (a skip, not an execution): `Physical gPTP (nightly and manual)`.
- The PR is non-draft, based on `dev`, and MERGEABLE, with head `07f72ad6`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `tb/tools/torture_campaign.py:3536-3562`, `:3391-3405`, `:3581`; REQUIREMENTS.md:250-280; TESTING.md:915-965; decisions 5854692245 to 5856062292 | R347-5 | `07f72ad640f99c43bc1354642ad4d7ed8ba410cc` |
| RTL | CLEAN | `KL_aaf_packetizer.sv:615`, `KL_crf_tx.sv:501`, clock-validity model via unchanged `tu_anchor_model.py`; PR-wide diff scope (no `hdl/`, firmware, builder or gitlink change) | R347-5 | `07f72ad640f99c43bc1354642ad4d7ed8ba410cc` |
| Robustness | CLEAN (S2 non-blocking) | `check_release_tu` boundary, ordering, zero-resolution, multi-event and SKIP arms; `start_edge_probe.py`, `float_edge_breakdown.py` | R347-5 | `07f72ad640f99c43bc1354642ad4d7ed8ba410cc` |
| Tests | CLEAN | `test_release_tu_start_resolution`, `test_release_tu_before_first_discontinuity`, `test_release_tu_contract`, `test_release_assertion_text`; feature `:421-436`; steps `:267`, `:292-298`; `torture_release_mutants.py:78-97`; unchanged R347-4 mutants 16/16 | R347-5 | `07f72ad640f99c43bc1354642ad4d7ed8ba410cc` |
| Docs | CLEAN (S1 non-blocking) | REQUIREMENTS.md:262-273; TESTING.md 6d row and prose; assertion text; PR body "Round 5"; docs, path, style, em-dash and TOC gates | R347-5 | `07f72ad640f99c43bc1354642ad4d7ed8ba410cc` |

All five lenses are banked at the merge candidate head itself, so no later commit has un-covered any of them.

## Other public findings on this PR at this head

I read these after the verdict and ledger above were written.

**Internal reviewer.** The latest verdict is R346-3 POSITIVE at `8153576a` (issuecomment-5855777031). It raised no BLOCKER, MAJOR or MINOR. Its suggestions, and what became of them:

| Suggestion | State |
|---|---|
| S1 (resolution ceiling or source) | Addressed as text. REQUIREMENTS.md:269-271 and TESTING.md:923-925 give the source and what the resolution includes. There is still no numeric ceiling; that is optional. |
| S2 (B.1.1 "minimum") | Taken as text. REQUIREMENTS.md:275 and TESTING.md:963. |
| S3 (assertion texts unpinned) | Taken. `test_release_assertion_text` (`:5212`) pins the new phrases, and the repository mutant "tu assertion drops the event window" is killed. |
| S4 (boot-time figures) | Unchanged, and optional. |
| S5 (stale round labels) | Unchanged, and optional. |

Its carried-over R346-1 S3 (a malformed `--dut` value raises a traceback) is outside this delta and unchanged. The internal reviewer's round-1 and round-2 findings were closed at R346-3 and stay closed: this delta touches their artifacts only in the `tu` rule text and its tests.

**External reviewer (this role).** The R347-1, R347-2 and R347-3 findings stay closed. R347-4 F1 is closed above.

**No public finding at MINOR or above remains open on this PR at this head.**

## Real limits

- This is a desk review. Physical calibration was NOT RUN. Acceptance items 3 and 4 (the seven-day soak, the 200 cold cuts, the #366/persistence-disabled negative control, and retained bench evidence) remain open, and no hardware result is claimed or implied. Field skips are not hardware proof.
- The oracle is a desk function. Its verdict is only as good as the bench runner's interval extraction, event recording and measured resolution, and that runner lives in a private repository not reviewed here.
- `restore_bound_s = 30` stays provisional pending manager ratification from #397/#75 measurements.
- S1's pre-first-event behaviour is decided, not verified as intended by the owner beyond the round-5 decision's silence on it.
- I did not run the full parent, PP, gPTP, Yosys or builder banks (not allowed). I did not run act, Docker or the host-side replica. Hosted long jobs were still running when sampled.
- Source validation is not candidate-merge validation. This review judges the source head against base `ac18b509`, not a merge with live dev `63fe4fb0`.

## Pending manager duties

- Build and validate the final current-dev candidate (source base `ac18b509`, live dev `63fe4fb0`) at the merge turn.
- Own the hosted and act acceptance. At sampling time, Verilator shards 0-4/5, `yosys-elaboration`, `elaborate` and `docs-check` were still in progress at this head.
- Ratify or replace the provisional 30 s restoration bound, and decide on S1 if a pre-event bound is wanted.
- Decide whether the internal positive still counts for the merge bar. The lane's internal positive (R346-3) is at `8153576a`. Since then, `54d9beea` and `07f72ad6` changed the `tu` oracle, its tests and its texts, which falls within the Conformance, Robustness, Tests and Docs scope. Under AGENTS.md section 7, coverage is banked against a commit. This external round covers all five lenses at the exact head.
- Keep acceptance items 3 and 4 open until bench evidence exists. Obtain explicit maintainer authorization before any merge, then do the post-merge containment.

R347-5 FINISHED

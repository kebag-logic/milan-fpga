[R626] NEGATIVE - exact head a57d384dc697249c2a69f80079b676875d4f7560

Round R626-1, internal cleared-context review of issue #727 / PR #728.
Head `a57d384dc697249c2a69f80079b676875d4f7560`, tree `a2fada192e36369be7fb6202c8f9618021c31c77`, source base `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
Diff: `scripts/suite_shards.py` (+/- 648 lines) and `docs/testing/CI_WORKFLOWS.md` (+31/-19), in three one-line commits with no trailers.
Lenses applied: Conformance, RTL, Robustness, Tests, Docs.

The verdict is NEGATIVE for one open MINOR (F1, Tests).
Every other part of the change checked out, as follows:

- Every table figure re-derives from the hosted logs.
- The split is deterministic and disjoint, and the five lists' union equals the inventory.
- The specialized owners and the dedicated `milan_dp` worker hold.
- The serial 0/1 selection and `rtl.yml` are byte-unchanged.
- The four assigned gate cases each have a control that escapes under its mutant.
- The refresh procedure runs verbatim.

F1 is a gap in that control set: no self-test arm can detect a change to the 60 % figure itself.

## Context reconstructed

- AGENTS.md, CONTRIBUTING.md sections 2-3, and docs/README.md (map).
- Issue #727: body (acceptance 1-4), lane assignment 6121794007, TAKEN 6121909841 and REVIEW READY 6122246247.
- PR #728 body.
- Authorities:
  - `.github/workflows/rtl.yml` job `verilator-shards`: `timeout-minutes: 120`, `matrix.total: [5]`, step "Prove specialized suite ownership" at :208-222, tsn-gen on `matrix.shard == 1` at :278-279, Yosys on `matrix.shard == 3`.
  - `scripts/run_all_suites.sh`: selection at :168-189, preflight at :291, and the sweep loop with its `shard:` line at :388-418.
  - `scripts/test_suite_cancellation.py` selector fixture at :68-89.
  - `scripts/ci_events.py` ownership pin.
  - `docs/testing/{CI_WORKFLOWS,TESTING,RUNNING_TESTS}.md`.
- `git diff c6bd08c6..a57d384dc` and its history.
- Public evidence tree `ba5d7c36:review-evidence/727-r1`:
  - `MANIFEST.json`, `author/mutants-final.txt` and `author/mutants_727.py` were read, and their sha256 values match the manifest.
  - `author/HANDOFF.md` and `author/PR-BODY.md` were fetched and hash-checked, but not relied on.
- Prior public review findings on PR #728: none exist at this head. The PR carries no reviews, no inline comments, and only the two review-start comments for R626-1 and R627-1. So there is nothing to resolve or retain.

## Findings

### F1 - MINOR - Tests - `scripts/suite_shards.py:77`, `:281-283`, `:585-596`, `:643-646` - no self-test arm detects a change to the 60 % headroom figure itself

**Authority and evidence.**
- Acceptance 1 makes 60 % of `timeout-minutes` the gate, and acceptance 3 states the 72-minute consequence.
- The assignment (6121794007, step 3) requires each gate case to have a control that is `[ok]` at the head and `ESCAPED` under its mutant.
- AGENTS.md section 6, under Tests, says: "Each new test can fail for the defect it claims to detect."

The case-3 control ("rtl.yml timeout-minutes 116 ... is refused ... and 117 minutes is not") and both heavy-duration arms derive their thresholds from `bound_seconds()`. So they move with whatever percentage or arithmetic the bound uses. Reviewer mutants on disposable copies (`receipts/mutate.out`) all end in `selftest: PASS` with rc 0 and no arm failing:

| Mutant | Bound the self-test prints |
|---|---|
| `HEADROOM_PERCENT = 75` | 5400 s |
| `HEADROOM_PERCENT = 100` | 7200 s |
| `bound_seconds` dividing by 10 instead of 100 | 43200 s |

The author's control for case 3 (mirroring the timeout as 120) escapes correctly. That control proves the "read from rtl.yml" half of case 3, not the "60 %" half.

**Impact.**
- A one-token edit loosens the gate this PR exists to add, and the gate keeps reporting PASS.
- That holds on every hosted worker's ownership step, in the physical job, and in the local sweep preflight.
- A future lane under timeout pressure could raise the figure and still get a green self-test. This is the "weaken a test to obtain a pass" shape that AGENTS.md section 8 forbids, with no executable tripwire.

**Required outcome.** `--selftest` fails when the bound it applies to `rtl.yml`'s Verilator `timeout-minutes` is anything other than 60 % of that value. One option is an arm that computes the expected bound independently of `bound_seconds` and `HEADROOM_PERCENT` (`timeout-minutes` x 36 s, which is 4320 s at 120). Another is a landmark pin of the percentage beside the existing specialized-owner landmarks. The control must be shown `ESCAPED` under a loosened-percentage mutant and a loosened-arithmetic mutant.

**Verification.** Rerun `scripts/mutate.py` (cases `headroom-75-percent`, `headroom-100-percent` and `bound-formula-div10`). Each must exit 1 with the new arm `ESCAPED`, and `tree-head` must stay rc 0 with `selftest: PASS`.

**Why only Tests.** At the head the gate does hold 60 % (the `tree-timeout-116` and `tree-gptp_plane+500` plantings fail closed). The assignment's case-3 control escapes under its named mutant, so no acceptance criterion is unmet.

### R1 - RESIDUE - Docs - `docs/testing/CI_WORKFLOWS.md:191-192` - provenance of the table stated as one dev run

The page says the selector records each duration "measured from one dev run". `maap` (1375 s) comes from #696's pull-request run 38208503834; the code comment at `scripts/suite_shards.py:86-89` and the docstring at :46-48 say so. The wording changes no figure or test.

Exact fix: "... and each worker's job overhead, measured from one dev run; `maap` keeps #696's figure from its pull-request run until a dev run measures that change."

### R2 - RESIDUE - Docs - `.github/workflows/rtl.yml:136-137` - comment still says "four hashed workers"

This comment is now stale, because the hash rule is gone. The executor published it as an open decision. Acceptance 2 keeps `rtl.yml` unchanged, so it is comment-only wording, and the manager decides whether it lands here or as a follow-up.

Exact fix: "four workers balanced by measured hosted time (#727)".

### S1 - SUGGESTION - Robustness/Tests - `scripts/suite_shards.py:541-545`, `:628-631` - head arms skip based on the file's own name

`in_checkout()` keys the skip on the filename and parent directory. With it forced False, the whole #727 gate disappears and the result is `selftest: PASS` with a "skip head arms" line (`receipts/mutate.out`, case `head-arms-skipped`). No realistic trigger exists without a code edit: CI and the sweep always run `scripts/suite_shards.py` in a checkout.

Option: skip only when neither `rtl.yml` nor `tb/verilator` exists beside the file, or have `test_suite_cancellation.py` request the skip explicitly.

### S2 - SUGGESTION - Tests - `scripts/suite_shards.py:197-200`, `:278` - two refusals have no in-self-test plant

- **Non-positive duration.** With the `> 0` check weakened to `>= 0`, the self-test passes (case `table-zero-duration-allowed`).
- **Mirrored worker count.** With `matrix total` mirrored as 5, the self-test passes (case `worker-count-mirrored-5`). The head does fail closed when `rtl.yml` is planted with six workers (`tree-six-workers`).

Neither is an assigned gate case. Planting both would complete the set.

## Per-lens results

[R626] PASS Conformance - `scripts/suite_shards.py:90-158` at a57d384dc, `receipts/rederive.out`, `receipts/refresh_verbatim.out`, `receipts/selftest_head.txt`, `receipts/list_*.txt`, `receipts/union.txt`, `receipts/serial_and_refusal.txt`, `git diff c6bd08c6 a57d384dc -- .github tb hdl` (empty) - checked against issue #727 acceptance 1, 2 and 4 and assignment steps 1-5:

1. **The table figures re-derive.** An independent parser (`scripts/rederive.py`: Decimal timestamps, not the selector's `--measure`) on all five worker logs of dev run 38217650945 reproduces all 62 entries of `SUITE_SECONDS` exactly. That run is rtl-full, schedule, dev `c6bd08c6`, with all five Verilator jobs `success`. The run used `maap` = 185 s. The reviewer derivation replaces it with 1375 s from run 38208503834, worker 1/5, where the window is 1374.1774735 s, PASS, ceil 1375.
2. **The overheads re-derive.** `WORKER_OVERHEAD_SECONDS` = (83, 115, 80, 93, 80) matches exactly, and each worker's setup is recorded separately from its first suite.
3. **The `maap` figure follows the assignment's window rule.** The issue and assignment quote "1,380 s". The assignment's own rule (window between consecutive result lines) gives 1375. With 1380 planted (`tree-maap-1380`), the maximum worker is 4207 s, still at or under 4320 s.
4. **The docstring refresh procedure runs verbatim** with rc 0 and reproduces both tables, except `maap` (185), which the docstring holds back by design.
5. **The in-sample model checks.** For the old hash split, predicted minus API job time is +5, +8, +5, +3 and -1 s. The old worker 1/5 with #696's `maap` comes to 7504 s (125.1 min), which matches the PR body.
6. **The new split predicts under the bound.** Predicted times are 4204, 4205, 4203, 4205 and 2877 s against a bound of 4320 s, so 60 % of 120 min is met.
7. **The selection is deterministic.** The five `--shard I/5` lists are identical:
   - across `PYTHONHASHSEED` = 0, 1, 2, 12345 and random (`receipts/hashseed.txt`);
   - between CPython 3.14.7 and 3.12.13.
8. **The split is disjoint and complete.** The lists hold 15, 16, 14, 16 and 1 suites. Their union equals the 62-suite inventory with no duplicates, and the inventory equals the base inventory.
9. **The required owners hold.** 4/5 is exactly `milan_dp`, `tsn_fuzz` is in 1/5 and `chmap_capture` in 3/5. These are the workers `rtl.yml:220-222` proves.
10. **The base behaviour is unchanged.** Five workers remain, and `rtl.yml` is byte-identical. The serial `--list`, `--shard 0/1 --list` and `--physical-gptp --list` outputs are byte-identical to `c6bd08c6` (sha256 `cad83149...` both sides).

[R626] PASS RTL - `git diff --quiet c6bd08c6 a57d384dc -- hdl tb .github` (rc 0); interface contracts `scripts/run_all_suites.sh:168-189,290-295,388-391`, `scripts/suite_tally.py:398-399`, `scripts/measure_test_evidence.py:680,817-819`, `scripts/test_suite_cancellation.py:68-89`, `.github/workflows/rtl.yml:208-222,364` - no HDL, testbench, workflow or submodule gitlink changes. The selector's caller contracts are preserved:

- `sweep_suites` and the `--suite-root/--shard/--physical-gptp` CLI are unchanged.
- The exit status on refusal is still the argparse 2 that the driver maps to exit 2.
- `measure_test_evidence.py --check`, `suite_tally.py --selftest` and `test_suite_cancellation.py` are rc 0.

I checked cross-suite build sharing, because moving a suite to another worker could change its time. `capture_coherence`, `pp_shadow`, `milan_dp_render` and `milan_dp_mclk` only query `../milan_dp` (`print-srcs` / `print-dp-vflags`), and `pp_shadow` builds its own hex images. `milan_dp_gm_steps` was alone on its worker in the measured run, so its figure includes its cold `../milan_dp gmstep` build. No measured figure relied on a predecessor's warm artifacts.

[R626] PASS Robustness - `receipts/mutate.out` (11 tree plantings), `receipts/serial_and_refusal.txt`, `scripts/suite_shards.py:253-278,329-372` - the plantings below were run in disposable tree copies:

| Planting | Result |
|---|---|
| Unmeasured suite directory | FAIL head |
| Removed suite | FAIL head (stale entry) |
| `gptp_plane` +500 s | Four workers over: FAIL |
| `timeout-minutes` 116 | FAIL |
| `timeout-minutes` 117 | PASS |
| Six workers | FAIL |
| Missing `rtl.yml` | FAIL |
| `timeout-minutes: ${{ 120 }}` | Refused (0 values) |
| Step-level `timeout-minutes` added | Ignored, and the job value is still read |

Further results:
- A sharded `--list` with an unmeasured suite exits 2 naming the suite, while the serial `--list` still lists it (rc 0).
- `measure_log` refuses a non-PASS verdict, a missing `shard:` line and a short result count (in-self-test arm).
- The hosted variance against #696's run (`receipts/variance_696.out`) shows per-suite ratios from 0.547 to 1.048. On those figures the head split predicts at most 4208 s.

The one-sample spare of 115-117 s (2.7 %) is the published, acceptance-sanctioned risk for acceptance 3, which belongs to the manager.

[R626] UNCLEAN Tests - `scripts/suite_shards.py:411-669` at a57d384dc, `receipts/mutate.out` (18 source mutants), `receipts/selftest_head.txt`, `receipts/gates_summary.txt` - F1 is open. The assigned controls behave as required:

| Mutant | Control that escapes |
|---|---|
| Missing duration made free | Both "no recorded duration" arms |
| Stale-entry check deleted | The stale arm |
| Timeout mirrored as 120 | The 116-minute arm |
| Overhead dropped | The +1 s dedicated arm |
| `>=` at the bound | The at-bound arm |
| Mean-only check | Three arms |

The following mutants also FAIL the self-test: pins dropped, `tsn_fuzz` pin moved, dedicated set dropped, `--measure` timed from job start, and `--measure` rounding down. The existing regressions are green: all 17 listed gates have rc 0, including `ci_events.py --check` and `--selftest` (1821 items, 2530 arms) and `test_suite_cancellation.py`. The removed hash-rule landmarks (`pp_shadow`, `mmcm_servo` and `milan_dp_gm_steps`) pinned the outputs of the rule being replaced, so removing them is justified.

[R626] PASS Docs - `docs/testing/CI_WORKFLOWS.md:183-211,320-326` and the `scripts/suite_shards.py:1-49` docstring at a57d384dc; `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base c6bd08c6` (31 added lines) and `check_doc_paths.py` all rc 0 - the text matches the code: four workers balanced longest-first to the least-loaded worker, the `milan_dp` dedication, the pinned owners, the 60 % of `rtl.yml`'s `timeout-minutes`, and the refresh procedure. The PR body's numeric claims were re-derived:

- 15/16/14/16/1 suites per list;
- eight `[ok]` lines;
- 4204/4205/4203/4205/2877 s predicted;
- the in-sample model within 8 s;
- 125.1 min for the old worker 1/5 with #696's `maap`.

The unchanged pages `RUNNING_TESTS.md:93`, `TESTING.md:206,515-521` and `milan_dp/README.md:440-442` stay accurate. R1 and R2 are RESIDUE only.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `scripts/suite_shards.py` tables, balance and selection; rtl.yml job; dev run 38217650945 and run 38208503834 logs; the five lists and the inventory | R626-1 | a57d384dc697249c2a69f80079b676875d4f7560 |
| RTL | CLEAN | Empty hdl/tb/.github/gitlink diff; caller contracts in run_all_suites.sh, suite_tally.py, measure_test_evidence.py, test_suite_cancellation.py and rtl.yml; cross-suite build sharing | R626-1 | a57d384dc697249c2a69f80079b676875d4f7560 |
| Robustness | CLEAN | 11 tree plantings; refusal exits; rtl.yml parser edge cases; hosted variance | R626-1 | a57d384dc697249c2a69f80079b676875d4f7560 |
| Tests | UNCLEAN (F1) | `--selftest` arms; 18 source mutants; 17 listed gates | R626-1 | a57d384dc697249c2a69f80079b676875d4f7560 |
| Docs | CLEAN (R1 and R2 are RESIDUE) | CI_WORKFLOWS.md diff; selector docstring; PR body figures; unchanged pages that cite shards; docs gates | R626-1 | a57d384dc697249c2a69f80079b676875d4f7560 |

## Real limits

**No manager source bank runs at this head, and none is claimed.**

**Execution evidence here is the reviewer's own:**
- the self-test on CPython 3.14.7 and 3.12.13;
- the shard lists;
- the 17 listed gates, run with a disposable environment carrying the pinned Markdown renderer and PyYAML;
- the mutation and planting campaign.

**Not run:** the serial local sweep, `syn/yosys/run.sh`, any act replica, any Vivado run, and any hardware. Physical calibration was not run, and field skips are not hardware proof.

**Planting and mutation cases** used minimal disposable trees: the inventory directories with their real Makefiles, plus `rtl.yml` and the selector. Those are the only inputs the self-test reads. The full-tree copies were used only for the serial and refusal lists.

**Hosted state at the exact head**, as of 2026-10-12T14:05:55Z, for rtl-full run 38258772791:
- `full-ci-gate` succeeded.
- The step "Prove specialized suite ownership", which runs this head's `--selftest` and the owner greps, reached `completed/success` on all five Verilator workers.
- All five Verilator shard jobs were still in progress, so acceptance 3 is not yet measurable.

**The table is one sample**, as the issue specifies. Cross-run ratios of 0.55 to 1.05 against the #696 run show runner-class variance that can exceed the 2.7 % spare on a slow runner.

## Pending manager duties

- **Acceptance 3.** Every Verilator worker of the PR's ready-state rtl-full run must take at most 4320 s (API `completedAt - startedAt`). Record predicted against measured on the PR.
- **The merge turn.** The act replica, the current-dev candidate merge validation (builder and native banks, the serial sweep and Yosys), and post-merge containment.
- **The decision on R2** (the `rtl.yml` comment against acceptance 2), plus carrying R1 and R2 to the residue checklist.
- **Re-review after F1 is fixed.** The Tests lens must be re-covered at the new head. Any change to `scripts/suite_shards.py` also un-covers Conformance, RTL, Robustness and Docs for that file's scope.

R626-1 FINISHED

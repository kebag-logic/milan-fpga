[R627] POSITIVE - exact head 2c2f336979e4fdb1da444f041f37551e2c9175df

External independent review R627-3 of issue #727 / PR #728. All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR remains. Both previous MINOR findings are resolved. One previously assigned wording RESIDUE remains for #495. This source-review verdict does not discharge hosted acceptance 3 or authorize merge.

Reviewed tree: `4c0af06c96b3c3809b22f86d9280d50e603c3237`. Source base and supplied live dev: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. The full eleven-commit diff changes only `scripts/suite_shards.py`, `docs/testing/CI_WORKFLOWS.md` and `docs/testing/TESTING.md`. The full diff and both later-round deltas were examined. Workflow, driver, suite/testbench, RTL, firmware and gitlinks are unchanged.

The public contract was reconstructed from AGENTS.md/CONTRIBUTING.md, docs/README.md, the [frozen issue and assignment](https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6121794007), [round-2 decision](https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6126048117), [round-3 decision](https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6126613714), REQUIREMENTS.md section 8 and workflow/driver interfaces. Diff/history preceded executable evidence and prior findings. `receipts/independent-verdict.md` records my independent verdict and ledger before prior review findings were opened; `receipts/reconciliation-start.json` records its hash. No private author material or management files were read. [Public review start](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6129130290).

**Measurements and assignment.**

All 62 `SUITE_SECONDS` entries and five `WORKER_OVERHEAD_SECONDS` entries match independent decimal timestamp arithmetic on the hosted logs. The script's `--measure` agrees. `receipts/hosted/`, `suite-measurements.csv` and `overhead-measurements.csv` retain raw logs, every suite's source job/start/end/window/ceiling, and setup/tail overheads.

The five successful workers of dev run `38217650945` supply the figures except `maap`. Its completed window in run `38208503834`, job `114677344710`, is `1374.1774735` seconds, rounded up to `1375`. That worker's later cancellation supplies no completion overhead. The assignment's approximate 1380-second figure does not replace its specified measurement rule; the published harness's `tree-maap-1380` control also passes. Dev's superseded `maap` value is 185 seconds. Overheads are exactly `(83, 115, 80, 93, 80)`, with setup excluded from each first-suite figure.

The docstring refresh commands ran verbatim, with temporary storage redirected into packet scratch. They reproduce the dev tables, including 185 for `maap`; the prose correctly requires retaining #696's 1375 until dev measures that change. Receipt: `refresh-verbatim.log`, rc 0.

An independent longest-first allocator reproduces every owner and load. Actual driver lists contain all 62 filesystem inventory suites exactly once. Separate process seeds 0, 1, 2 and 12345 agree. Serial/default selection equals the base selector's lexical selection. Tables, five lists and predictions equal rounds 1 and 2. The unchanged workflow's actual ownership shell was executed for every worker, all rc 0.

| Worker | Suites | Predicted seconds, including overhead | Bound | Spare seconds |
|---|---:|---:|---:|---:|
| 0/5 | 15 | 4204 | 4320 | 116 |
| 1/5 | 16 | 4205 | 4320 | 115 |
| 2/5 | 14 | 4203 | 4320 | 117 |
| 3/5 | 16 | 4205 | 4320 | 115 |
| 4/5 | 1 | 2877 | 4320 | 1443 |

`milan_dp` remains alone on 4/5, `tsn_fuzz` on 1/5, and `chmap_capture` on 3/5. Acceptance 1, 2 and 4 are supported. Acceptance 3 requires the manager's completed PR-head worker measurements.

**Round-2 control results.**

At `scripts/suite_shards.py:726-730`, the independent expectation is literally `minutes * 36`. Inspection and an AST check confirm it reads neither `bound_seconds` nor `HEADROOM_PERCENT`. Pristine applied bounds are `{116: 4176, 117: 4212, 120: 4320}`.

The published R626-1 `mutate.py` was fetched from the requested [public evidence tree](https://github.com/kebag-logic/milan-fpga/tree/dfdd39ff0eb50992be0cca34797ddd41e556dc01/review-evidence/727-r1), checked against its manifest, and rerun with `--jobs 8`. Original SHA-256: `571bd0aabb766efeec0f0274909d181e81ed6f25b609b76a5c9c0c2fffcfc031`.

Its original fixture omits the now-required driver. Unmodified, its runnable cases fail closed on the missing driver, including pristine; these are not credited as mutation detection. A second run adds exactly one fixture-copy line for `run_all_suites.sh`, recorded in `r626-harness-adaptation.diff`, preserving every original mutation. Of 29 cases, 28 execute; the old missing-duration textual replacement reports DRIFT against the corrected refusal wording. My independent missing-duration mutant covers it and exposes both required ESCAPED arms.

| Case with complete fixture | Result | Named failure |
|---|---|---|
| `tree-head` | rc 0, PASS | None |
| `headroom-75-percent` | rc 1 | Only the independent 36-second arm ESCAPED; 5400 s applied at 120 minutes |
| `headroom-100-percent` | rc 1 | Only that arm ESCAPED; 7200 s applied |
| `bound-formula-div10` | rc 1 | Only that arm ESCAPED; 43200 s applied |
| `table-zero-duration-allowed` | rc 1 | Zero-duration arm ESCAPED |
| `worker-count-mirrored-5` | rc 1 | Six-worker arm ESCAPED |
| `head-arms-skipped` | rc 1 | Refuses skipping when checkout inputs exist |
| `nondeterministic-tie` | rc 1 | Separate hash-seed worker lists disagree |

My separate 20-mutant campaign verifies assigned refusals, boundary/heavy-load controls, pins, measurement origin and provisional-duration controls. Eleven direct tree plants refuse missing, stale, zero and heavy durations; a lower timeout; six workers; a mismatched provisional figure; and a missing/malformed driver. Receipts record case rc and named failures, not merely the harness exit code.

**Round-3 new-suite walkthrough.**

`scripts/new_suite_review.py` plants `zz_review_suite` in a disposable clone and follows the docstring:

| Stage | Executed result |
|---|---|
| No figure | Selector self-test rc 1; sharded list rc 2; real serial driver rc 2 at selector preflight. The refusal names the provisional source, extra worker and hosted replacement. |
| Step 1 | The real shell `suite_timeout` returns 1800 s. Recording it in `SUITE_SECONDS` and `PROVISIONAL_SUITES` satisfies the provisional check; five-worker headroom still refuses. |
| Step 2 | Apply the named workflow matrix/total/verifier/ownership updates, canonical and fixture-count updates in `ci_events.py`, selector landmark and maximum-overhead insertion. Selector rc 0: 3746/3746/3746/3747/3747/2877 s. Workflow check/self-test rc 0: 1822 items, 2530 arms. |
| Selection/preflight | Six real driver lists cover 63 suites exactly once; 5/6 holds only `milan_dp`, and specialized owners remain 1 and 3. All eight real serial preflight gates pass. The copied driver's final dispatch stops after preflight, before any suite runs. |
| Step 3 mechanics | Explicitly synthetic hosted-format data measures 121 s for the planted suite and 118 s for the added worker's overhead. Replacing those values and removing the provisional marker leaves the self-test green. A real hosted run does not exist for this unpublished disposable suite; this proves replacement mechanics only. |

The provisional checker reads the driver's function text. Mirroring 1800, ignoring named arms, suppressing figure comparison or ignoring a missing provisional figure each produces its corresponding ESCAPED control. Missing/malformed-driver refusals execute. `TESTING.md:513-519` and the current PR body state the serial preflight precondition accurately. The original branch still has five workers and byte-identical `rtl.yml`.

**Prior findings, resolved or retained at this head.**

The [R626-1](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6125953320), [R627-1](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6126041660), [R626-2](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6126536374) and [R627-2](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6126597327) findings were reconciled after the independent verdict. Inspected formal-review and inline-comment lists are empty.

| ID | Severity; ALL attributable lenses | Disposition | Artifact, authority/evidence, impact, required outcome and verification |
|---|---|---|---|
| R626-1/F1 = R627-1-F1 | MINOR; Tests | RESOLVED | `suite_shards.py:726-730`; round-2 item 1 requires an independent 60% oracle. Silent loosening is now detected: all three required mutations give rc 1 with the new arm ESCAPED, pristine rc 0. |
| R626-2/F1 | MINOR; Docs, Robustness | RESOLVED | `suite_shards.py:54-87,239-244,336-382,812-826`; `TESTING.md:513-519`; round-3 items 1-3. The former remedy could not bootstrap a new suite. Driver-sourced provisional timing, documented worker expansion and replacement now provide a working procedure. The planted-suite walkthrough reaches all eight passing preflights. |
| R626-1/R1 = R627-1-R1 | RESIDUE; Docs | RESOLVED | `CI_WORKFLOWS.md:191-194` distinguishes dev-run figures and #696's PR-run exception. The provenance summary matches unchanged measurements; documentation gates pass. |
| R627-1-R2 | RESIDUE; Docs | RESOLVED | Current PR body says `Overheads assume warm Verilator and Yosys caches; worker 1's overhead includes the tsn-gen build.` It matches `rtl.yml:278-292`. No timing figure changes; historical receipts remain historical. |
| R626-2/R2 | RESIDUE; Docs | RESOLVED | Current PR body's sharded-selection row uses the requested distinction between table-free serial selection and table-dependent self-test/preflight. Verified against `run_all_suites.sh:291` and real serial refusal. |
| R626-1/S1 = R626-2/S2 | SUGGESTION; Robustness, Tests | RESOLVED | `suite_shards.py:800-808`; forcing the checkout predicate false now fails with checkout inputs present. Both harnesses give rc 1; cancellation fixture compatibility passes. |
| R626-1/S2 | SUGGESTION; Tests | RESOLVED | `suite_shards.py:704-707,734-739`; zero-duration and extra-worker plants refuse; weakening either guard exposes its named ESCAPED arm. |
| R626-2/S1 | SUGGESTION; Tests | RESOLVED | `suite_shards.py:857-881`; separate-process comparisons detect hash-based tie breaking in both harnesses. Actual lexical selection agrees across four seeds. |
| R626-1/R2 = R626-2/R1; retained as R627-3-R1 | RESIDUE; Docs | RETAINED for #495 | `rtl.yml:136-137` still says `four hashed workers`. Round-2 item 4 and round-3 item 5 preserve workflow bytes and route this wording to #495. Exact fix: replace that phrase with `four workers balanced by measured hosted time (#727)`. Impact is stale comment wording only. Manager carries the residue; verify the eventual edit changes only the comment. |

The retained residue changes no measurement, figure, verdict, test, code, generated artifact, conformance/clause claim or privacy rule. It therefore leaves Docs CLEAN under the supplied rule. No code defect is cleared by moving it to another issue.

**Independent lens results and reviewer-owned ledger.**

[R627] PASS Conformance - `suite_shards.py:129,255,390`, frozen issue decisions, measurement CSVs and `inventory.json` - All figures, placement, coverage, owners and 60% construction checked. Hosted acceptance 3 remains reserved.

[R627] PASS RTL - `receipts/diff.txt`; `run_all_suites.sh:168,245,291`; `rtl.yml:148,208`; `ci_events.py:1921`; `suite_tally.py:398`; `measure_test_evidence.py:817` - Discovery, refusal, preflight and setup interfaces remain valid. No clock/reset/CDC/FSM, RTL, suite or gitlink changes. Cross-suite Makefiles query datapath source/flag lists; the GM-step suite invokes its separate `obj_gmstep` leg, measured on a separate old worker. No dependence on another suite's warm build was found in those recipes.

[R627] PASS Robustness - `suite_shards.py:234,304,336,433,679,768,797`; `plants.json`, `mutations.json`, `r626-mutation-summary.json`, new-suite receipts - Table disagreements, missing/malformed inputs, timeout/count drift, heavy/exact-bound cases, pin perturbations and bootstrapping checked with actual refusals.

[R627] PASS Tests - `suite_shards.py:726,768,857`; independent measurement/allocation oracles; mutation receipts; selector/tally/cancellation/workflow/test-evidence gates - Required controls detect their defects; former optional escapes now fail. Fixture omissions, syntax errors and DRIFT are not counted as detection.

[R627] PASS Docs - `suite_shards.py:30,54`; `CI_WORKFLOWS.md:183,191,328`; `TESTING.md:513`; current PR body and public receipts - Refresh and new-suite procedures run as documented, the preflight precondition is explicit, and prose matches provenance and implementation. R627-3-R1 remains wording RESIDUE only.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue/decisions; tables/allocator/bound; all 67 measured figures; inventory lists | R627-3 | 2c2f336979e4fdb1da444f041f37551e2c9175df |
| RTL | CLEAN | Full diff; driver/tally/test-evidence interfaces; executed ownership step; cross-suite recipes; blob/index/gitlink audit | R627-3 | 2c2f336979e4fdb1da444f041f37551e2c9175df |
| Robustness | CLEAN | Entry-point plants; mutations; workflow/driver/log parsing; boundaries; provisional-suite walkthrough; cancellation | R627-3 | 2c2f336979e4fdb1da444f041f37551e2c9175df |
| Tests | CLEAN | Independent 36-second oracle; mutation escapes; measurement/allocation oracles; process seeds; integration/preflight receipts | R627-3 | 2c2f336979e4fdb1da444f041f37551e2c9175df |
| Docs | CLEAN | Both changed pages; executed docstring procedures; corrected PR body; public evidence; documentation gates | R627-3 | 2c2f336979e4fdb1da444f041f37551e2c9175df |

**Execution and restoration.**

Selector self-test, workflow check/self-test (1821 items, 2530 arms), tally, cancellation, Python idiom, test-evidence, documentation/style/path, contents/anchor, em-dash and diff checks pass. Two initial renderer-dependent checks returned 2 for an absent dependency; both pass with hash-locked requirements installed in a disposable environment. Initial refusals and successful reruns are retained. No shared installation changed.

Portable scripts are under `scripts/`; commands, rc files and raw outputs are under `receipts/`. `scripts/REPRODUCE.md` gives the order. Temporary trees are under `scratch/` and excluded from publication. An initial reviewer-written table replacement also touched a printed string; the corrected fixture targets the actual table. An initial worker-count fixture omitted an expected diagnostic explicitly named by the docstring. Neither preliminary harness error is counted as source evidence; final scripts and receipts contain corrected probes.

Final `integrity.json` verifies 1295 parent blobs, 562 protocol-processor blobs, 104 gPTP-processor blobs and 214 axis blobs against committed bytes/modes. Every index entry and stage equals its HEAD tree. Required registered submodule heads equal their gitlinks:

- protocol-processor: `2ad2f845dd583f8310075fa2380cb60a04fd091a`;
- gptp-processor: `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`;
- third_party/verilog-axis: `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.

The review-created bytecode cache was removed. Parent status, including ignored files, is empty. No source fix, commit, push, GitHub write, merge, author contact, sub-agent or other-checkout edit occurred. Foreground child work was joined before completion.

**Real limits and pending manager duties.**

- The table is one dev sample plus #696's completed window. Four workers retain only 115-117 seconds of margin against 72 minutes. Predictions do not guarantee runtime under runner/cache variation.
- Deleting the head's call to `provisional_problems` is a published coverage limit, not claimed as detected. The actual call is present and a direct mismatched-provisional plant refuses. Current `PROVISIONAL_SUITES` is empty.
- Source-head execution evidence is the author's published gate receipts and this focused review. **No manager source bank runs at this exact head; none is claimed or inferred.** No full parent/processor, synthesis or builder bank, suite build, local workflow replica or host workflow orchestrator ran here. The supplied simulation compiler was not needed or invoked.
- The recorded exact-head hosted snapshot has all five Verilator workers in progress in rtl-full run `38283356358`. `full-ci-gate` and four Yosys workers succeeded; Physical gPTP was explicitly skipped. Other required workflows remained in progress. Worker success does not establish completed aggregates. Raw run/job snapshots do not clear acceptance 3.
- The manager owns acceptance 3: every actual PR-head worker must finish within 4320 seconds, with predicted versus measured results published. Required hosted contexts and local-replica acceptance remain manager duties.
- At the merge turn the manager must build and validate the current-dev candidate, including builder and native banks, and publish receipts. These source checks are distinct from that final candidate and claim no already-tested candidate.
- The manager must reconcile both ledgers, wait for outstanding rounds, carry R627-3-R1 to #495/residue tracking, obtain merge authorization, perform post-merge containment, and close the issue/project item only after the complete bar is met.
- Physical calibration was NOT RUN. Field skips and desk verification provide no hardware proof. Synthetic new-suite data is excluded from hosted/hardware evidence.

`MANIFEST.sha256` enumerates every publishable script and receipt with packet-relative paths. Only those files and this report are for publication.

R627-3 FINISHED

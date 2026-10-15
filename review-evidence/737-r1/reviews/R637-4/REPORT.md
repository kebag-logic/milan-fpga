[R637] POSITIVE - exact head 08adb21af0a72d839ce30b6c461503dad269d4d6

External independent delta review R637-4, issue #737 / PR #739. Tree: `e5cc5d163c974aaf1b6cb888dae9881267d787e6`.

All five lenses are CLEAN for this source head. No BLOCKER, MAJOR or MINOR remains in the reviewed delta. R636-3-F1 is resolved: removing the shared read deadline now makes the collector self-test fail. One PR-body wording residue remains. This is a source review verdict, not completion of the merge or hosted acceptance bar.

## Scope and reconstruction

Read the repository operating contract and contribution rules, documentation index, frozen issue scope and public decisions, verification requirements and CI interfaces before the implementation. Examined the original `fa7347fc59173f90e4feec2df207692e6e6e72ec..08adb21af0a72d839ce30b6c461503dad269d4d6` history and relevant diff, with this round's independent code review focused on `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf..08adb21af0a72d839ce30b6c461503dad269d4d6`.

The delta changes 14 files. No RTL, firmware behavior, submodule gitlink, suite gate body, or host runner changes in this delta. The earlier merge of separately published development changes is not represented as round-four implementation.

Authorities:

- [Round-four assignment](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6180908502).
- [Builder entry-point STOP answer](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6181778634).
- [Fixes-only scope and follow-up boundary](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6169768594).
- [Round-three observer, headroom and resource decisions](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6176299708).
- `REQUIREMENTS.md` section 8, `CONTRIBUTING.md` verification/merge rules, `docs/testing/CI_WORKFLOWS.md`, and `docs/testing/CI_SIGNATURE.md`.
- [Published execution evidence](https://github.com/kebag-logic/milan-fpga/tree/988e9e8946ddd86e7ade82874a4e580c2ec61681/review-evidence/737-r1), restricted to execution receipts and measurement records. No author handoff or private lane material was read.

The independent verdict and five-lens ledger were written before reading prior public review reports. Prior public findings were then reconciled. No other round-four review was read.

## Findings

**R637-4-R1 - RESIDUE - Docs - PR #739 body, current Status paragraph.**

Authority/evidence: round-four item R2 requires publication wording to identify the coordinating role. The current paragraph says, "This head is not pushed; the coordinating role publishes it." The read-only PR API identifies the already-published head as `08adb21af0a72d839ce30b6c461503dad269d4d6`. The older round-three sentence was corrected, but the current paragraph reintroduces the stale statement.

Impact: contradictory publication tense only. This changes no code, measurement, figure, verdict, test, generated artifact, conformance/clause claim or privacy rule.

Required outcome / exact fix: replace that sentence with "The coordinating role published this head."

Verification: read the current Status paragraph against the PR head. The coordinating role carries this item to the residue checklist. It does not make any lens unclean.

## Independent results

**[R637] PASS Conformance - `sw/builder/test_builder.py:29146`, `scripts/ci_builder_legs.py:131`, `scripts/ci_gate_receipts.py:61`, `.github/workflows/elaborate.yml:189`.**

The driver exposes the ordered inventory and runs only an inventory-order subsequence. Unknown, repeated, out-of-order and empty selections are refused before invoking a gate. The original 103 names and their order are preserved. All 335 pre-existing function bodies are byte-identical to round three; the pre-entry-point code AST is identical, apart from the explanatory module docstring. No gate assertion, fixture, timeout or NOT RUN arm changed.

`audit_driver.py` also executes the old and new entry points with inert, call-recording functions. Default order, stdout, exit status and NOT RUN ledger match with no flags, with required elaboration, and with both required instruments. It checks subset receipts and verifies that a failing selected gate leaves no receipt. These are entry-point controls, not a full builder-bank run.

The partition isolates `test_baremetal_profile_contract` in leg 0 and assigns the other 102 gates to leg 1. The generated steps preserve the template's command and scope, adding the selection wrapper and receipt. Leg 1 runs before the standalone simulation aggregate. Both worker limits remain 45 minutes; no limit was raised in this delta.

The aggregate requires both executed leg receipts, exactly-once ordered gate coverage, matching source identities and fresh inventory, passing per-gate verdicts, and the owning flags for all 15 elaboration gates and the RV32 gate. It judges the combined NOT RUN ledger using the driver's own elaboration verdict. Missing/deleted/moved/skipped owners and a non-flag elaboration leg are refused by name. A wholly skipped elaboration division cannot carry builder receipts.

**[R637] PASS RTL - `scripts/ci_gate_workflows.py:166`, `scripts/ci_gate_receipts.py:61`, `scripts/ci_runtime_workflows.py:78`, `checkout-integrity.json`.**

Applied the architecture lens to job ownership, ordering, dependency completion, evidence handoff and failure propagation. The two-worker split does not change the product interfaces or gate predicates. The aggregate remains dependent on both successful workers; missing or inconsistent observations cannot become success. Generated-graph controls cover collector and late watcher failures, including the same-repository write restriction. CPU preparation precedes the bounded field-oracle build.

The changed-path census confirms no RTL, CDC, reset, firmware or submodule-pin delta. `scripts/act_ci.py` is byte-identical to round three, SHA-256 `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`; its host trust boundary was therefore not re-audited or executed. Evidence-helper pin checking passes.

**[R637] PASS Robustness - `scripts/ci_fail_fast.py:45`, `scripts/ci_runtime_evidence.py:196`, `scripts/ci_builder_legs.py:102`.**

Watcher and collector controls exercise both sides of the error classification. HTTP 400/401/404 fail after one request, without retry or observer-only output. HTTP 403/429/502, timeout and exhausted transport retries produce observer-only results; collector manifests remain incomplete. Genuine collection/upload/tail failures retain cancellation authority. Tests also retain malformed, unknown and overlapping raw/expanded matrix refusals and first-failure conclusion coverage.

The new collector control drives the production entry point through a late recovery followed by a permanently failing jobs read. It stops after 480 simulated seconds within the shared 600-second budget; the same reads without sharing take 960 seconds. The independent `i3-no-shared-budget` mutation fails with `collector reads took 960.0s`.

Builder controls refuse missing/duplicated legs, bad source identities, changed inventories/selections, failed verdicts, unknown requirements and toolchain skips. The public exact-head receipts are additionally accepted by the production aggregate with explicitly synthetic successful step contexts. Removing the elaboration flag from their owning leg is refused naming all affected gates.

**[R637] PASS Tests - `scripts/ci_runtime_evidence_selftest.py:165`, `scripts/ci_gate_workflows_selftest.py:28`, `scripts/ci_gate_workflows_selftest.py:185`, `focused-results.json`, `mutation-results.json`.**

All ten focused commands return zero:

| Check | Result |
|---|---|
| Workflow generator `--check` | PASS |
| CI-event contract `--check` | 2,186 contract items PASS |
| CI-event contract `--selftest` | 5,212 arms PASS, 200.965 seconds |
| Gate workflow/union self-test | PASS |
| Runtime evidence self-test | PASS |
| Fail-fast self-test | PASS |
| Manifest self-test | PASS |
| Workflow-plan self-test | PASS |
| Case-receipt self-test | PASS |
| Evidence-helper pin check | PASS |

Nine independent in-memory production mutations all make their named self-tests return 1: shared collector deadline removed; conditional preparation accepted; client errors made observer-only in watcher and collector; HTTP 403 made genuine in watcher and collector; builder owner refusal removed; union ledger judgement removed; receipt-defined inventory accepted. Every failure was inspected for its intended assertion. In particular, the preparation mutation fails on the planted conditional preparation, and the union mutations fail on deleted ownership, toolchain skip or altered inventory respectively.

A separate field-oracle mutation removes only `"$CI_TOOL_BUILD_JOBS"`, regenerates the workflow in memory and receives the two named canonical-command findings. Pristine contract input has zero findings. No tracked file was mutated.

**[R637] PASS Docs - `docs/testing/CI_WORKFLOWS.md:1408`, `:2367`, `:2684`, `:2775`, `docs/testing/CI_SIGNATURE.md`, `public-evidence-audit.json`.**

Documentation records the measured split, union-level requirements, shared read budget, error classes, source-tool bound and timing projections. R636-3-R1's exact Yosys/Verilator wording is present. Authentication, image adoption and RTL-trigger changes remain follow-up work under the public fixes-only ruling; incomplete manifests do not authenticate builds.

The hosted baseline was independently read from job `115631440899`, run `38495894212`, at `7032bca5a51d8d97fcb73d7fc106ca4af21de38e`: 2,144 seconds total, 1,441 for builder gates, 593 for the standalone aggregate, and 3 for the retained cache window. Applying `1441 / 1292.671` to the recorded leg measurements gives the documented rounded windows of 1,146 and 409 seconds:

| Worker | Projection | Own 60% bound | Margin |
|---|---:|---:|---:|
| elaborate-gates-0 | 1,313 s | 1,620 s | 307 s |
| elaborate-gates-1 | 1,172 s | 1,620 s | 448 s |

The slower worker plus the stated 270-second aggregate/collector/watcher/tail allowance gives 1,583 seconds, or 26.4 minutes. These are projections from a cache-hit baseline, not a hosted cold-build or exact-head wall-clock proof. Hosted capacity, cache misses and actual tails remain coordinating acceptance work.

## Published source execution evidence

`public-fetch-index.json` records each immutable public evidence path and fetched SHA-256. `audit_evidence.py` reruns the production union/comparator on the three published exact-head receipts, and independently compares their rows:

- 103 per-gate verdict/NOT RUN rows equal the unsharded reference, partitioned 1 + 102.
- The ordered NOT RUN ledger is equal: gate 1b's inert Make environment mutation and gate 11's absent physical calibration report.
- The author records exact-head times of 1,311.061 seconds unsharded, 984.818 for leg 0, and 348.095 for leg 1; all return zero with zero memory-event counters.
- Public calibration paths were redacted before publication. The recomputed published-byte verdict digest is `003e9b0c438eae6cba6532698d8349998c3283de4883df2a41cd50b9d2c573e1`; the original execution record carries `47dc3c6ac362ed2038a1ff6391ef54334cc0edb665870a0e5d3980ec3216988f`. Equality passes on the published bytes; these two different byte digests are not claimed equal.
- The author's printed-output comparison reports 96 identical gate segments and seven equal after masking temporary paths and durations. This reviewer did not reproduce those complete stdout segments.
- Public planted execution receipts at `0838c64f` show the boot-claim defect failing the reference and leg 0 while leg 1 passes; the removed FPU refusal fails the reference and leg 1 while leg 0 passes. `0838c64f..08adb21a` changes documentation only. These are author execution receipts, distinct from the reviewer's guard mutations.
- The exact-head docs bank records 40 executed steps with rc 0, including the default builder command. The runner contract is explicitly omitted from that bank and separately recorded rc 0 in its isolated boundary; it is not counted as an executed bank step. The no-metadata docs check also records rc 0.
- The bounded field-oracle receipt at `6ab22bca` records configure/build/executable-check success, 17.355 seconds, eight build jobs and 836,313,088-byte peak, with zero memory events. The network clone arm was not executed. That build body is unchanged at this head.

No coordinating source bank ran at this exact head and none is inferred. The source execution evidence above belongs to the author. The current-development merge candidate is separate.

## Prior public findings reconciled

The following are dispositions at this head, not a claim to have repeated old full banks. Unchanged earlier fixes retain their published closure, checked against the delta and the indicated source/evidence; touched paths were independently exercised above.

| Prior finding | Disposition at this head | Evidence |
|---|---|---|
| R637-1-F1, nested compiler budget | Resolved, retained | `tb/verilator/media_nco/Makefile:17`; unchanged child recipes; real-child CPU controls in the passing gate self-test |
| R637-1-F2, collector/watcher-tail cancellation | Resolved, retained | `ci_runtime_workflows.py` watcher/collector/tail graph; passing fail-fast and runtime controls |
| R637-1-F3, cache prose | Resolved, retained | `CI_WORKFLOWS.md:1508,1602`; exact-key templates, no install-cache prefix fallback |
| R636-1-B1, union inventory prerequisites | Resolved, retained | `ci_suite_workflows.py:21`; generated preparation; public `round3-fresh-collector.json` explicitly uses synthetic unions to check dependencies |
| R636-1-B2, fixture Git identity | Resolved, retained | Explicit fixture identities in `ci_workflow_plan_selftest.py`; passing focused self-tests |
| R636-1-F1 and R637-2-F1, skipped matrices | Resolved, retained | Production raw-name validation and passing watcher/collector raw-skip controls; no successful execution manufactured |
| R636-1-F2, R637-2-F3 and R636-2-S5(b), observer failures | Resolved | Shared bounded retries, successful observer-only exit and incomplete manifest; both error-class boundaries independently exercised |
| R636-1-F3 and R636-2-F1, worker headroom | Resolved at source/projection level | Own-limit contract, separate contract worker and synthesis preparation; round-four elaboration arithmetic above; hosted acceptance still pending |
| R636-1-F4 and R636-2-F2, memory sizing | Resolved, retained | Public resource receipts and `round3-source-sizing.json`; accepted builds leave more than 25% of the 8 GiB cap; unchanged caps and bound |
| R636-1-F5, first-failure conclusions | Resolved, retained | Passing controls separately exercise failure, cancelled, timed_out and action_required |
| R636-1-F6, publicly reconstructible suite comparisons | Resolved, retained | Public round-two comparison summary binds all six suites to `cf9c9366`; no round-four suite driver changes; no new full suite execution claimed |
| R637-2-F2, collector inventory dependencies | Resolved, retained and strengthened | All generated readers prepared; missing and conditional preparation controls; `i1-conditional-prep-accepted` killed |
| R636-2-S1/S2/S4, ineffective outcome/skip/scope controls | Resolved, retained | Passing case-receipt, manifest and gate-union controls retain real failed outcomes, skipped-step incompleteness and mixed-scope refusal |
| R636-3-F1, shared-deadline control | Resolved | Production collector 480 s versus 960 s unshared; required mutation returns 1 |
| R636-3-S1, conditional preparation control | Resolved | 26 conditional/continue-on-error preparation refusals over 13 readers; independent mutation returns 1 |
| R636-3-S2, non-transient client errors | Resolved | 400/401/404 genuine versus observer-only 403/429/5xx/timeout/exhaustion in both consumers |
| R636-3-S3, elaboration span | Resolved at source/projection level | Authorized driver split, exact-head receipt equality, 1,583-second projection and own-limit margins |
| R636-3-S4, unbounded field-oracle build | Resolved | Template and generated `--parallel "$CI_TOOL_BUILD_JOBS"`; independent removal refused twice |
| R636-3-R1 | Resolved | Exact measured-class wording at `CI_WORKFLOWS.md:2367` |
| R636-3-R2 | Retained as R637-4-R1 RESIDUE | Historical paragraph corrected; current Status paragraph still needs the publication-tense fix |
| R636-1-S3 / R636-2-S3, hosted capacity; R636-2-S5(a), cache-conditioned equality | Retained optional follow-up | Public round-three ruling explicitly carries these to #495; not represented as implemented authentication or hosted timing proof |
| R636-1-S4, inherited parent timeout | Retained documented behavior | `scripts/run_all_suites.sh` piece timeout explanation; unchanged this round |
| R636-1-S5, Make environment sensitivity | Source execution evidence now available; hosted observation pending | Exact-head author builder receipts preserve the explicit inert-Make NOT RUN arm; no claim that the skipped arm executed |

## Reviewer-owned coverage ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue decisions 6180908502/6181778634; `test_builder.py:29146`; `ci_builder_legs.py:131`; `ci_gate_receipts.py:61`; published exact-head builder receipts | R637-4 | 08adb21af0a72d839ce30b6c461503dad269d4d6 |
| RTL | CLEAN | `ci_gate_workflows.py:166`; generated elaboration workers/aggregate; `ci_runtime_workflows.py:78`; unchanged gate-body, RTL, pin and host-runner comparisons | R637-4 | 08adb21af0a72d839ce30b6c461503dad269d4d6 |
| Robustness | CLEAN | `ci_fail_fast.py:45,141`; `ci_runtime_evidence.py:196`; `ci_builder_legs.py:102`; shared-budget, error-class and malformed-union controls | R637-4 | 08adb21af0a72d839ce30b6c461503dad269d4d6 |
| Tests | CLEAN | `ci_runtime_evidence_selftest.py:165`; `ci_gate_workflows_selftest.py:28,185`; `focused-results.json`; `mutation-results.json`; `driver-audit.json`; `field-bound-probe.json` | R637-4 | 08adb21af0a72d839ce30b6c461503dad269d4d6 |
| Docs | CLEAN | `CI_WORKFLOWS.md:1408,2367,2684,2775`; `CI_SIGNATURE.md`; public scope/evidence; PR body with publication-tense RESIDUE explicitly retained | R637-4 | 08adb21af0a72d839ce30b6c461503dad269d4d6 |

## Real limits and pending coordinating duties

- No full builder, parent, processor or synthesis banks were run by this reviewer. No container replay, host runner/self-test, hardware or privileged operation was executed. The explicit exclusions govern the otherwise optional shipping-image rerun.
- Focused controls used Python 3.14.7 and PyYAML 6.0.3, not the shipping Python 3.12.3/pinned reader environment. Published shipping-environment receipts supply that separate evidence. The scoped 5.050 compiler identity was verified; no compiler build was needed.
- At `2026-10-15T03:17:48Z`, exact-head API readback returned zero workflow runs and zero check runs. There is therefore no executed or skipped hosted context to count at this head, and no exact-head hosted span is claimed.
- Physical calibration remains NOT RUN. Field skips and synthetic step contexts are not hardware proof. The inert Make control remains NOT RUN, not a killed mutation.
- The coordinating role must construct and validate the merge result against live development, identified in the assignment as `f62602531d415d6c1cae1374a3cc2938faf54049`, rather than the frozen source base `fa7347fc59173f90e4feec2df207692e6e6e72ec`. Publish the candidate builder/native-bank and required replay receipts on the PR when available.
- The coordinating role owns hosted/act acceptance, actual workflow spans, per-job and slot memory/placement evidence, cold-tool and artifact-handoff behavior, and live cancellation acceptance. Source projections do not replace these duties.
- Complete the other independent review, handle any new source changes with appropriate re-review, carry the wording residue and agreed optional follow-ups, obtain explicit merge authorization, then perform containment and issue/project completion. This source verdict does not authorize merge.

## Integrity and reproduction

`verify_checkout.py` directly hashes committed blob bytes, checks executable/symlink modes, and compares every stage-zero index entry against the real commit tree with replacement objects disabled. It verifies 1,364 superproject entries and all required initialized dependencies: protocol processor `2ad2f845`, gPTP processor `7dda9c3b`, TSN stack `70936b77`, axis library `48ff7a7e`, and registration library `08ee86e8`. All bytes, modes, indices and gitlinks match. The unused `external` gitlink remains uninitialized. No tracked source edits, commits, pushes, GitHub writes, author contact or delegated work occurred.

Portable entry points, given the candidate root as their argument: `run_focused.py`, `probe_mutations.py`, `audit_driver.py`, `probe_field_bound.py`, `verify_checkout.py`. `fetch_public.py` retrieves only explicitly selected public execution receipts; `audit_evidence.py` rechecks the downloaded builder receipts. Each independent check ran under a foreground supervisor; at most three were active together and all children were joined.

`MANIFEST.sha256` lists the publishable scripts, logs, return-code files, receipt audits and the three published builder receipts. Disposable material and unsanitized local-path logs stay under `scratch/`, excluded from publication. `log-redactions.json` records any path-only substitutions and the original/published log hashes; test outcomes are unchanged.

R637-4 FINISHED

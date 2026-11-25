[R924] NEGATIVE - exact head 9c62539365fea8316dae2b9fd7c68defeff5cb31

R924-2, external independent review of issue #998 / PR #1003. One new MINOR finding remains open. Two wording-only RESIDUE items are listed separately. All five lenses were applied. This is a source-review verdict, not merge authorization.

## Scope and provenance

Reviewed source tree: `bbbe38c7db0b82682798e8afb1feb3a41a4ff491`. The complete range is `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f..9c62539365fea8316dae2b9fd7c68defeff5cb31`, stacked on the now-merged #1001. This later round concentrated on the six-commit delta after `13e6d869d842fc06155ef5dae9b0347596d6d4df` and the causes of every named prior finding. Unchanged earlier code was inspected where the delta changes its dependencies; previously accepted execution evidence was retained rather than repeating full banks.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, [issue #998](https://github.com/kebag-logic/milan-fpga/issues/998), the supplied scope decisions and their current [PR-body record](https://github.com/kebag-logic/milan-fpga/pull/1003), REQUIREMENTS.md section 8, the CI/testing authorities, then the diff/history and published evidence. The issue-comments API returned no comments. The current PR body records the manager's rulings; [#1008](https://github.com/kebag-logic/milan-fpga/issues/1008) independently records the untouched over-limit jobs and watcher/physical-job exceptions. `public-scope.json` retains these references.

For this PR, the timing criterion applies to touched jobs, with the stated indivisible media-clock exception. Untouched over-limit jobs belong to #1008. This interpretation does not waive the requirement to preserve cancellation and fork safety.

The [published packet at 726d9d25](https://github.com/kebag-logic/milan-fpga/tree/726d9d2597c965868995948d16dac921bd5a1752/review-evidence/cicd3-r1) supplied author-r4 through author-r7 evidence. All 290 selected files matched their publication-manifest SHA-256 values. Reports, measurement tables, retained logs and receipt objects were read by relevant section. No private source, author scratchpad or parallel review report was read. `independent-verdict.md` records my verdict and ledger before I read the two prior public reviews.

## New finding

### R924-2-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Title:** The new capture matrix disables the fork-safe cancellation mechanism.

**Artifacts:** `.github/ci-templates/rtl-fast.yml:579`; generated `.github/workflows/rtl-fast.yml:1154`; `scripts/ci_events.py:1364`, `:3885`, `:8410`; watcher guard at `.github/workflows/rtl-fast.yml:1691`; `cancellation-policy.json`.

**Authority/evidence:** The requested scope preserves the cancellation contract. `docs/testing/CI_WORKFLOWS.md:2483` requires hosted matrices to retain `fail-fast: true`, including forks; lines 3565-3567 say forks retain native matrix cancellation and never enter the write-token job. The new `firmware-boundary-capture` matrix instead explicitly sets `fail-fast: false`. Its privileged watcher still correctly excludes forks.

The independent `probe_cancellation.py <clone>` reads the actual parsed workflow and invokes the production boundary-leg checker. The committed `false` configuration passes. Changing only that in-memory value to `true` produces the checker's strategy finding. The newly added mutation arm explicitly expects `true` to be rejected. The full event self-test passes 5,967 arms despite this policy reversal.

**Impact:** On a fork PR, if one capture leg fails while the sibling is running or queued, the matrix does not cancel that sibling, and no privileged watcher can compensate. The sibling may continue for the rest of its 30-minute allowance, consuming capacity and delaying completion of the matrix dependency. The required aggregate still fails; this is a cancellation/resource-policy defect, not a demonstrated false-green verdict. On same-repository events, the watcher remains available, but it does not restore native matrix cancellation semantics.

**Required outcome:** Preserve native failure cancellation for the capture matrix while retaining the existing fork permission guard and fail-closed aggregate. Correct the template, generated workflow, contract constant and regression control together. An intentional exception would need an explicit scope/authority decision; the current unchanged-cancellation claim does not provide one.

**Verification:** The healthy matrix must satisfy the retained fail-fast policy. A planted disabled-cancellation configuration must fail the contract check. A failed fork capture leg must cancel a queued/running sibling through the native matrix mechanism without granting a fork a write token. The judge and `rtl-fast` must remain non-passing after failure or missing evidence. Re-run generation, event and fork/cancellation controls at the corrected head. This review injected no hosted failure.

## Wording residue

### R924-2-R1 - RESIDUE - Docs

**Artifacts:** New behavior-comment blocks at `tb/verilator/follow_ring/Makefile:94`, `small_pulls.py:76`, `settle_control.py:180`; `.github/ci-templates/rtl-fast.yml:566`; the capture/leg explanations in `sw/firmware/ctrl/test/ctrl_boundary.py:69`, `ctrl_configs.py:101`, `ctrl_runs.py:26`; and the new boundary-leg explanatory blocks in `scripts/ci_events.py:270`, `:1360`, `:2265`, `:2609`, `:3886`, `:8403`.

**Authority/evidence:** The owner comment rule requires behavior/reason explanations to identify their issue and requirements. These additions omit the verification requirement IDs; several cite only the PR number. The earlier four blocks named by R924-1-R1 now contain the requested attribution and are resolved.

**Impact:** Attribution wording only. No behavior, measurement, test, verdict, privacy rule or clause interpretation changes.

**Exact fix / required outcome:** Add `Issue #998; REQ-VER-01 and REQ-VER-04.` to the listed explanatory blocks, or their explicitly shared section contract, preserving their existing behavior/reason explanation. Do not mechanically annotate every incidental inline comment. For the cancellation explanation, apply the behavioral correction in F1 first.

**Verification:** Inspect the changed comments and run the applicable style/documentation checks. No new bench lane, review-round, reviewer or issue-comment identifier was found in added source comments. Existing labels in unchanged neighboring comments remain outside this delta.

### R924-2-R2 - RESIDUE - Docs

**Artifact:** `sw/firmware/ctrl/README.md:631`.

**Authority/evidence:** The new sentence says, “That job runs no builder itself”. The surrounding text is describing the transferred standalone builders. The judge still calls `owned()` and `stack_gate()` at `ctrl_boundary.py:534-536`; the published judge log records those retained operations. This is an overbroad noun phrase, not missing execution evidence.

**Impact:** Wording only; all recorded build counts, controls and verdicts remain unchanged.

**Exact fix / required outcome:** Replace the opening with: `Those standalone builders run in firmware-boundary-capture; firmware-boundary still runs its owned image builders, the stack gate and controls, then judges the joined captures.` Retain the following leg/argument explanation.

**Verification:** Compare the corrected sentence with the calls and the published judge receipt. This residue does not leave a lens unclean.

## Prior public findings: disposition at this head

The [R924-1 review](https://github.com/kebag-logic/milan-fpga/pull/1003#issuecomment-7140670982) and [R923-1 review](https://github.com/kebag-logic/milan-fpga/pull/1003#issuecomment-7142915497) were read only after the independent pass and initial verdict/ledger were written.

| Prior item | Disposition and evidence |
|---|---|
| R924-1-F1, MAJOR, Conformance/Robustness/Tests/Docs | **RESOLVED.** `mutant_stage.py:143-190` locks the physical slot directory and rechecks its identity. The independent probe reproduces live-slot deletion at 13e6d869 for different TMPDIRs with one parent, and for aliased TMPDIR spellings. At this head both pairs receive distinct physical slots and both markers survive. |
| R923-1-F1, MINOR, RTL/Robustness/Tests | **RESOLVED.** `proved_root()` at `mutant_stage.py:90` verifies directory type, owner, permissions, resolved parent and descriptor/path identity. The independent probe rejects symlink, writable, regular-file and nonsticky-parent roots with safe fallback and preserves external markers. Published controls additionally cover foreign ownership, readable-root upgrade, slot exhaustion, stale contents, concurrent holders and the old `locks` entry. Foreign-UID execution was not repeated here. |
| R923-1-F2, MINOR, Conformance | **RESOLVED for this PR under the recorded ruling.** Re-keyed figures, measured subdivisions, 26 workers and the firmware capture split now have executed hosted evidence. All touched jobs finish within 30 minutes at this head; slowest shard is 27.7 minutes, leaving 138 seconds. This does not certify every future runner or close #1008. |
| R924-1-R1 | **RESOLVED.** The four named source blocks now cite Issue #998 and REQ-VER-01/04. New attribution residue is separately R924-2-R1. |
| R923-1-R1 | **RESOLVED.** TESTING.md:174 explicitly names the two in-tree staging callers and their checkout-local paths. |
| R923-1-R2 | **RESOLVED.** CI_WORKFLOWS.md:510-512 qualifies preflight watcher cancellation to pushes and same-repository PRs and states fork behavior. F1 concerns the newly added capture matrix, not that earlier wording. |
| R923-1-R3 | **RESOLVED.** The duplicate phrase in PR Description item 3 is removed. |
| R923-1-S1, SUGGESTION, Tests/Docs, `ci_make_cases.py:155` | **RETAINED OPTIONAL.** Frame-output serialization still uses measured start order. The finer partitions do not increase shared writers within a piece. Clarifying that order or preserving driver order in this special mode remains optional; no newly demonstrated output defect is claimed. Verify with a deliberate multiwriter case if adopted. |
| R923-1-S2, SUGGESTION, Robustness, `ci_suite_workflows.py:76` | **RETAINED OPTIONAL.** Explicit read-only permissions for preflight remain a reasonable hardening change. Its inherited checkout/permission pattern is unchanged. Verify generation and fork checks if adopted. |
| R923-1-S3, SUGGESTION, Docs, PR queue limitation / CI_WORKFLOWS.md:500 | **RETAINED OPTIONAL.** The PR now discloses queueing. Preflight start priority is still not guaranteed; a short policy-page qualification would be useful. Verify any claimed scheduling improvement by measured queue/start times. |

## Independent evidence and lens application

**Conformance:** Checked #998's frozen output/timing criteria under the explicit scope rulings against source scheduling, measurements and executed jobs. The figure-refresh comparison proves that only re-keyed `milan_dp` legs decreased in `59f4f478`; the retained old-run table's 38 named window maxima are covered. The subsequent splits preserve driver inventories and change scheduling estimates, not graded figures. F1 prevents clean coverage.

**[R924] PASS RTL - `tree-integrity.json`, `delta-paths.txt`, the full source range and the two new Makefile case interfaces - no production RTL, firmware C/C++, harness assertion code or gitlink changes.** Examined `follow_ring/Makefile:94-169`, `media_phase/Makefile:168-213`, the deterministic print changes, and the boundary capture dispatch against their existing execution/build commands. The case entry points retain the same simulation arguments and failure exits. The previously defective staging interface is repaired as recorded above. This is a scoped architecture/interface result, not a new hardware or full-bank proof.

**Robustness:** Examined unsafe roots, aliases, simultaneous holders, stale-slot cleanup, missing/failed capture evidence, invalid leg selection, preflight result/SHA binding and fork behavior. The production union controls reject omitted cases, missing/duplicate legs, wrong head/tree and failing/missing logs for all eight partitioned suites. Capture aggregation still requires successful captures and all known builders. F1 leaves fork cancellation unclean.

**Tests:** `run_focused.py <clone>` joined three concurrent command groups at most, with all seven groups exiting zero. It ran workflow generation/checking, event checking, case controls, piece controls, shard controls, the independent staging probe and the full event self-test. Piece controls report 65 parents and 94 scheduled units. Event controls report 2,378 contract items and 5,967 arms. `probe_cancellation.py` demonstrates why those green controls do not establish the cancellation requirement. No full simulation, synthesis or builder bank was run.

**Docs:** Compared CI_WORKFLOWS.md, TESTING.md, RUNNING_TESTS.md, the firmware README, PR body and author-r4..r7 evidence with actual code and logs. Staging, partition membership, timing projections and unchanged required context names are supported. The unconditional preserved-cancellation claim conflicts with the new matrix. R1/R2 are wording-only additions to the residue checklist.

### Published receipt checks

`verify_public.py <clone>` recomputed archive digests and four complete gPTP output hashes. It checked same-pin equality across raw piece result objects, including 38 repeated case comparisons, and reconciled 28 direct-run table entries plus 12 piece executions: 18 old-pin and 22 new-pin gPTP executions. The only cross-pin output difference is one response-pointer observation line per case. Each same-pin receipt digest equals its retained full output's digest. The old/new A/B receipts also match for 7 `milan_dp`, 10 `capture_coherence` and 9 continuous media-clock cases.

The public checkout receipts distinguish hosted merge `dd5cf5798833575a051a7dccf4e248ba290702a7` into base `2509db684b58b920e215b0d5d327b4a845bac3f4` from `241f036e9e93c6cb84acca8bf9c78beefa8b1e94` into base `e608f8d82a88bca8b3996677ff4113aef353ce88`. The latter includes #995's gPTP pin change. This supports the supplied ruling; comparing those two hosted runs without holding the base does not isolate this PR.

The firmware evidence compares the former whole step with the two captures plus judge, locally and hosted. The hosted judge retains 4,032 compiled sources / 4,325 invocations, 112 boundary controls, 192 pin controls, four figure controls, zero findings and PASS. The retained diff shows transferred builder lines and a random sysroot path, not changed observations. The local one-capture negative receipt refuses missing builders. These are published executions inspected here, not newly run firmware banks.

### Hosted durations from the Actions jobs API

`read_hosted.py` retrieved every jobs page, retained timestamps and computed wall minutes. All four runs are successful on attempt 1; all seven required contexts executed successfully, rather than merely appearing as skipped contexts.

| Run / examined jobs | Result |
|---|---|
| [45528738009](https://github.com/kebag-logic/milan-fpga/actions/runs/45528738009), capture 0 / capture 1 / judge | 13.200 / 14.133 / 5.467 minutes, all success |
| [45528738040](https://github.com/kebag-logic/milan-fpga/actions/runs/45528738040), preflight | 1.933 minutes, success |
| Same run, all 26 suite workers | All success; maximum 27.700 minutes; continuous media-clock worker 14.083 minutes |
| Same run, eight unions and exhaustive aggregates | All executed successfully; nightly physical gPTP job skipped |
| [45528737977](https://github.com/kebag-logic/milan-fpga/actions/runs/45528737977), documentation contexts | `docs-check`, `docs-check-no-git`, `wire-accountability` executed successfully |
| [45528738049](https://github.com/kebag-logic/milan-fpga/actions/runs/45528738049), elaboration context | Executed successfully |

Untouched `publication-census` and `firmware-control-mutants` took 37.167 and 38.833 minutes; they remain #1008 work. Watcher durations span their workflows and are the documented exception. The raw API contains an inverted one-second timestamp for the skipped physical job; that is not an executed negative duration or physical evidence. The firmware family's observed cost rises to 1,968 runner-seconds; its faster completion comes with extra setups, as disclosed. No universal runner-speed or future cost guarantee is inferred.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN - F1 | #998 / #1008; REQUIREMENTS.md:326; CI_WORKFLOWS.md:2483; rtl-fast.yml:1154; hosted-minutes.tsv; public-comparison.json | R924-2 | 9c62539365fea8316dae2b9fd7c68defeff5cb31 |
| RTL | CLEAN | Full source path diff; follow_ring/Makefile:94; media_phase/Makefile:168; mutant_stage.py:90; ctrl_runs.py:70; tree-integrity.json | R924-2 | 9c62539365fea8316dae2b9fd7c68defeff5cb31 |
| Robustness | UNCLEAN - F1 | mutant_stage.py:143; stage-probe.log; piece-controls.log; rtl-fast.yml:1691; cancellation-policy.json | R924-2 | 9c62539365fea8316dae2b9fd7c68defeff5cb31 |
| Tests | UNCLEAN - F1 | ci_events.py:1364,3885,8410; focused-results.json; event-controls.log; public-comparison.json; published negative capture receipts | R924-2 | 9c62539365fea8316dae2b9fd7c68defeff5cb31 |
| Docs | UNCLEAN - F1; R1/R2 nonblocking | CI_WORKFLOWS.md:2483,3565; TESTING.md:173; RUNNING_TESTS.md; firmware README:631; PR body; publication manifest | R924-2 | 9c62539365fea8316dae2b9fd7c68defeff5cb31 |

## Limits and pending manager duties

- Correct F1 and obtain an independent verdict at the corrected head. Carry R1/R2 to the residue checklist. The optional prior suggestions do not block coverage.
- The manager owns hosted/local-replica acceptance. No container replay, host CI orchestrator or its self-test ran here. No GitHub write, source fix, commit, push, author contact, privilege change or hardware operation occurred.
- Source validation here consists of the author's published gate receipts, inspected hosted evidence and focused reviewer controls. **No manager source bank at this exact head is claimed or inferred.** The full serial sweep was not executed by this review.
- At the merge turn, construct and validate the candidate against the then-current remote dev tip, including the manager's builder/native banks and required local/hosted evidence. The supplied live-dev reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`; the reviewed source base remains `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f`. The observed hosted merge is not that final candidate.
- Green controls do not waive F1. Exact-head successful runs did not inject a fork matrix failure. The foreign-UID staging tests, larger campaigns and timing repeats are published author evidence, not independently re-executed here. No simulator was invoked, so no new simulator-identity or hardware proof is claimed.
- Publication SHA-256 and per-case output digests were verified. No detached cryptographic signature was supplied with this archive; checksum/source binding is not an authenticated author signature. The 40-execution reconciliation uses retained tables and piece receipts, not 40 freshly executed or individually archived full logs.
- The disclosed image inventory/audit provenance is not certified here. It was already stale against all four workflows at the stacked base; this PR does not provide a refreshed image audit. Do not present it as exact-head image evidence. The manager/image owner retains that acceptance duty.
- Physical calibration was **NOT RUN**. The skipped nightly job and field skips are not hardware proof. Release requirements remain separate.
- After probes, `verify_tree.py` proved all 1,974 superproject entries and 1,362 entries across five initialized submodules against their commit blobs, modes and index records, with replacement objects disabled. Required gitlinks and registrations match. The unused external submodule remains uninitialized. No tracked restoration was necessary; disposable writes stayed under this packet's scratch directory.
- Finish the other independent review, candidate validation, explicit maintainer authorization, post-merge containment and issue/project completion before declaring the task done.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. All manifest paths are relative to this packet; scratch is excluded. Portable scripts take the review clone as an argument, except `read_hosted.py`, which reads the fixed public run IDs.

R924-2 FINISHED

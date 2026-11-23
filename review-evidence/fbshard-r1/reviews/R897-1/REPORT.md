[R897] NEGATIVE - exact head b7b351935f65416c8632c21dd13e08fb2e9c1d9c

External independent review of issue #980 / PR #982, round R897-1. Tree: `bcebbd36ca937a68b9323f962711c42f80e4ccdd`. Reviewed all three commits from `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`. All five lenses applied. One open MINOR prevents clean coverage; two wording residues do not affect the verdict. No source changes or GitHub writes were made.

## Findings

### R897-1-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Artifact:** `.github/workflows/rtl-fast.yml:1731`; generator `scripts/ci_runtime_workflows.py:135`; consumer `scripts/ci_fail_fast.py:120`; test `scripts/ci_fail_fast_selftest.py:74`; contract `docs/testing/CI_WORKFLOWS.md:3479`.

**Title:** The new skipped-matrix name is evaluated inside the non-matrix watcher.

**Authority/evidence:** The generated `SKIPPED_MATRICES` environment value contains the key `firmware-boundary shard ${{ matrix.shard }}/${{ matrix.total }}`. The watcher has no matrix. GitHub's [context semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#available-contexts) make nonexistent properties empty strings; matrix properties belong to the current job. The key delivered to this step therefore becomes `firmware-boundary shard /`. YAML single quotes do not make embedded workflow expressions literal.

The skipped-matrix API contract is the raw expression name, documented in the CI policy and exercised by `ci_fail_fast_selftest.py:91`. `probe_skipped_matrix.py` applies the documented evaluation to the two expressions actually present, then calls the real `observe()` and `watch()` with a completed/skipped raw-name job. The fixture passes with the unevaluated dictionary. The runtime dictionary raises `API returned an unplanned job name`; `watch()` returns 0 after one read with `observer_error=true`. See `skipped-matrix.log` and `skipped-matrix.rc`.

This is a static runtime-semantics inference plus an executable consumer reproduction, not an observed hosted failure. This PR introduces the matrix into `rtl-fast`, whose previous skipped-matrix map was empty. A similar pre-existing pattern elsewhere does not make this newly affected path correct.

**Impact:** On documentation-only runs, or another path skipping the matrix before expansion, this workflow's watcher stops monitoring. It cannot detect a later failure and promptly cancel sibling work. This does not establish a false green required check: the required `rtl-fast` verdict and collector retain independent checks. MINOR reflects loss of fail-fast observation, not loss of the required verdict. It is not wording residue.

**Required outcome:** Preserve the raw skipped-matrix key through workflow expression evaluation, through the generator. Keep expanded and unexpanded identities distinct. Accept the completed/skipped matrix while continuing to observe unfinished jobs and detect subsequent failures. The documented skipped-matrix support must hold for the new matrix.

**Verification:** Regenerate the workflow and add a control that evaluates the actual step environment in the non-matrix watcher context before calling the observer. Exercise a raw skipped matrix, unfinished remaining work and a subsequent failure. The current self-test directly parses the unevaluated YAML, which misses this defect. Re-run the workflow/CI contract gates and re-review the corrected head. Hosted confirmation remains the manager's responsibility.

### R897-1-R2 - RESIDUE - Docs

**Artifact:** `sw/firmware/ctrl/README.md:171`.

**Authority/evidence:** The new paragraph correctly describes capture jobs compiling and the aggregate judging. The retained sentence still says each compile is judged "in the job that ran it."

**Impact:** A redundant location phrase is stale. The surrounding commands and instructions already describe the correct behavior. No measurement, test, verdict, implementation, or normative boundary claim changes.

**Exact fix / required outcome:** Replace the sentence with: `The boundary and Verilator paths partition the builders. Each recorded compile is judged whole; the boundary aggregate judges the shard captures.`

**Verification:** Read against both workflow paths and run documentation checks. Carry this wording-only item on the residue checklist.

### R897-1-R3 - RESIDUE - Docs

**Artifact:** PR #982 body, opening line, as read during this review.

**Authority/evidence:** CONTRIBUTING section 2.1 requires role-prefixed PR bodies. This body begins `Closes #980`, without a role prefix.

**Impact:** Public activity labeling only; no implementation, evidence or verdict changes.

**Exact fix / required outcome:** Prepend `[A10] Shard the firmware-boundary CI job` and a blank line, retaining `Closes #980`.

**Verification:** Read back the first line and closing keyword. Carry this wording-only item on the residue checklist.

## Applied lenses

**Conformance.** Reconstructed AGENTS, CONTRIBUTING, the documentation index, [issue #980](https://github.com/kebag-logic/milan-fpga/issues/980), TAKEN/REVIEW READY comments, REQUIREMENTS section 8 (particularly REQ-VER-01 through REQ-VER-04), and the CI/firmware-boundary contracts before judging the diff. The issue freezes the 30-minute cap, deterministic partition, exact union, one judging self-test, stable aggregate, local timings/plants, hosted timing, and documentation updates. The generated graph implements three capture jobs plus the stable aggregate. `ctrl_configs.py:478` derives eight units from existing builder commands. `plan_findings()` reads the current table at call time. Independent probes remove and duplicate each unit and verify named refusal before building; unknown units/commands refuse too. F1 prevents clean coverage.

**[R897] PASS RTL - full 11-file diff and `tree-verification.json` - unchanged product implementation and interfaces.** No HDL, firmware C/C++, configuration, CSR, clock/reset/CDC, protocol ownership, timeout, or gitlink changes occur. The CI capture/consumer boundary was inspected in the template, generated workflow, `ctrl_runs.py:129`, and loader. Ordered dispatch matches the base: 88 build-only calls and 1,843 complete normal/self-test calls. Detailed AECP call arguments, including output paths, match for 18 ordinary and 9 coverage calls. Geometry files are created when their arm executes; suite calls and order remain unchanged. This does not renew hardware qualification.

**Robustness.** Inspected argument refusal in `ctrl_boundary.py:532`, builder failures in `ctrl_runs.py:157`, and incomplete captures in `ctrl_capture.py:515`. A real small C compile survived copying only `records.jsonl`, `manifest.jsonl`, and `text/`; decoded commands/invocations were equal. Removing each component or changing the builder return code refused. Per-unit missing/duplicate commands refused. The actual required-verdict shell rejected failure, cancellation, timeout, empty/missing, in-progress and unknown shard results, plus failed judgement after successful shards. F1 prevents clean coverage of skipped-matrix handling.

**Tests.** The pre-change/current dispatch comparison supplies an oracle outside the new list implementation. Build partitions of 1, 2, 3 and 4 retain the original invocation multiset, with dropped/duplicated-suite plants caught. The two-part inventory is 51 plus 37 calls, totaling 88. Production shard controls return four controls with zero misbehavior. The author's source-union receipt reports 1,262 distinct normalized compiles per side, zero missing/extra. That is a set comparison, not equality of raw compiler-invocation multiplicity; extra raw invocations do not establish duplicated suites. F1 exposes the scheduling tests' unevaluated-environment gap.

**Docs.** Inspected the CI policy, firmware README, changed docstrings, PR body, public issue comments and selected executable receipts. The updated design distinguishes captures, judgement, measured local times and hosted projections. No added source comment contains prohibited bench-lane labels, review rounds, reviewer identities or issue-comment IDs. F1 contradicts the raw skipped-matrix support claim. R2/R3 are wording-only residue.

## Validation and acceptance

Reproduce using the portable scripts in this packet:

```sh
python3 probe.py CHECKOUT PACKET
python3 probe_skipped_matrix.py CHECKOUT PACKET
python3 run_gates.py CHECKOUT PACKET PYTHON_WITH_PINNED_MARKDOWN_REQUIREMENTS
python3 inspect_public_evidence.py CHECKOUT PACKET
python3 verify_tree.py CHECKOUT
```

The focused probe passed. The skipped-matrix probe reproduced F1; its rc 0 means the reproduction assertions held. All **28 independent gate commands passed**, including `ci_events.py --check`, its **2,369-item / 5,881-arm self-test**, generator check, wire-accountability and the documented CI/docs checks. Individual logs/return codes and durations are in `gates/` and `gates.json`. Four concurrent gate processes were used; no heavy bank was run. The campaign consists of the author's 27 permitted commands plus `ci_events.py --selftest`. The author's 28th command, the local-replica orchestrator self-test, was read as published evidence only and was not executed here.

The [published evidence packet](https://github.com/kebag-logic/milan-fpga/tree/26ba6dd9bfa2f73c191b38aab918c7c1dfefa660/review-evidence/fbshard-r1) was read after the independent diff pass. `public-evidence.json` lists selected receipt paths and verified published SHA-256 values. No private author handoff or scratchpad was read.

| Acceptance item | Evidence and disposition |
|---|---|
| Local shard builds and union | Author's final shard receipts at `d7da99cf`: 462, 393, 449 seconds; aggregate 259 seconds. Head judgement: 250.42 seconds, 3,851 compiled sources / 4,132 recorded invocations; 112 boundary, 185 pin, 4 figure and 4 shard controls; zero findings/misbehavior. The later two commits change plan binding and docs, not the successful partition. No fresh head shard rebuild by this reviewer is claimed. |
| Dropped/duplicated work | Author's capture/table plants and independent per-unit and dispatch probes refused all planted defects. |
| Runtime target/cap | Local shards are under eight minutes, comfortably below 15/30 minutes. Stated 8-minute shards, 5-minute aggregate and 13-14-minute critical path remain setup-inclusive projections, not hosted completion or queue-time measurements. |
| Hosted timing | PENDING. Exact-head `rtl-fast` run `45144982744` was queued when inspected; no shard execution time was available. The other three workflows were queued too. Queued/skipped contexts were not counted as executed evidence. |
| Upload/download | YAML selects unique shard/SHA names and records/manifest/text sharing a capture-directory root. Download uses a pattern and separate artifact directories. The aggregate enumerates those directories; no match produces an invalid capture path and refusal. Public full-capture emulation and the independent small-capture roundtrip passed. Hosted transfer and actual local workflow replication remain manager acceptance. |
| Workflow/docs updates | Generated-workflow and documentation gates pass. F1 remains an open scheduling defect. |

`firmware-boundary` itself skips when a shard fails. The required check is `rtl-fast`, which also needs and examines the shard matrix result; that is the failure-closing path tested here. Under whole-workflow cancellation the required check cannot become a successful completed validation. The unchanged stable aggregate name is not mistaken for an independently required ruleset context.

Source-head execution evidence is the author's public receipts. **No manager source bank exists at this head, and none is inferred.**

`ci/image/tool-inventory.json` and `ci/image/command-table.json` are unchanged in this delta and acknowledged as unregenerated snapshots. They are not freshness evidence for this head. New jobs repeat existing tool/package requests; no new tool dependency was identified. No hosted workflow invokes their freshness checker. Image preparation does invoke it (`ci/image/build.py:211`), so lack of a hosted gate does not waive regeneration for a future image build. No image-build or inventory-check pass is claimed. The claimed October 16 regeneration date was not independently established; Git history contains later edits/re-pins. Nothing here treats either snapshot as current.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #980 acceptance; REQUIREMENTS section 8; template/generated workflow; ctrl_configs plan/union; probe.log; F1 | R897-1 applied; no clean covering round | b7b351935f65416c8632c21dd13e08fb2e9c1d9c |
| RTL | CLEAN | Full 11-file diff; unchanged product sources/interfaces/gitlinks; ordered dispatch; tree-verification.json | R897-1 | b7b351935f65416c8632c21dd13e08fb2e9c1d9c |
| Robustness | UNCLEAN | ctrl_boundary.py:532; ctrl_runs.py:157; ctrl_capture.py:515; required-verdict shell; both probes; F1 | R897-1 applied; no clean covering round | b7b351935f65416c8632c21dd13e08fb2e9c1d9c |
| Tests | UNCLEAN | test_ctrl_firmware_shards.py:166; old/new dispatch; ci_fail_fast_selftest.py:74; gate receipts; F1 | R897-1 applied; no clean covering round | b7b351935f65416c8632c21dd13e08fb2e9c1d9c |
| Docs | UNCLEAN | CI_WORKFLOWS.md:76,3479; ctrl/README.md:161; public PR/issue evidence; F1 | R897-1 applied; no clean covering round | b7b351935f65416c8632c21dd13e08fb2e9c1d9c |

The independent verdict/ledger were written in `independent-verdict.md` before reading review submissions, threads or the combined review timeline. Subsequent readback returned only the review-start comment, zero reviews and zero threads. **No earlier public finding was available to resolve or retain.** Issue readback contained TAKEN and REVIEW READY; no later manager execution receipt was available.

## Limits and pending manager duties

- Fix F1 and obtain review of the corrected head. Carry R2/R3 on the residue checklist. This round does not approve a later fix.
- Publish and judge hosted shard times, artifact transfer, actual local workflow-replica receipts and required contexts. An orchestrator self-test is not an executed replica.
- Obtain the second independent review and satisfy the full completion bar. This negative verdict does not authorize merging.
- Validate the final current-dev merge candidate at the merge turn with the manager-owned builder/native banks. Source base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6` differs from supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`; this review proves neither that composition nor a future live tip. Publish candidate receipts and complete post-merge containment only through the authorized process.
- No full parent/processor, synthesis, builder or hardware banks were run. No container/local workflow replica or host orchestrator was executed, no shared installation made and no other checkout edited. Physical calibration was **NOT RUN**. Field skips and desk passes are not hardware proof.
- Tracked blob bytes, modes and index match the exact head, verified directly, together with all five required initialized submodule pins and their tracked bytes. The unused external gitlink remains pinned but uninitialized. See `tree-verification.json`. Disposable files are under packet `scratch/`; publish only files in `MANIFEST.sha256` and this report.

R897-1 FINISHED

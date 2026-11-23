[R897] POSITIVE - exact head 5392adf989349b68cfbb54d91fd0413c5b745521

External independent delta review of issue #980 / PR #982, round R897-2. Tree: `766ccefea747fa53f340cb99578f943b5279893c`. The two commits after `b7b351935f65416c8632c21dd13e08fb2e9c1d9c` change seven files, +144/-14. All five lenses were applied. The prior MINOR is resolved; no MINOR, MAJOR or BLOCKER remains. One new wording-only RESIDUE is recorded below. This source-review verdict does not discharge pending execution acceptance or authorize merging.

Reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, the [frozen issue and public decisions](https://github.com/kebag-logic/milan-fpga/issues/980), REQUIREMENTS section 8, and the CI/firmware-boundary contracts before examining the diff and history. Examined the source range from `854bd7236792ce1adbd10c43b13a6a5002ad3bb6` for context and judged the two-commit delta. Untouched code retains prior conclusions. Prior public findings were read only after the independent diff pass. No private author material or other reviewer's report was read. The independent verdict and ledger were saved before subsequent review-submission/thread readback.

**Prior findings, explicitly reconciled**

The [R897-1 findings](https://github.com/kebag-logic/milan-fpga/pull/982#issuecomment-7096749092) are resolved as follows:

- **R897-1-F1, MINOR, Conformance/Robustness/Tests/Docs: RESOLVED.** `scripts/ci_runtime_workflows.py:125` serializes JSON and escapes the `$` opening each expression as `\u0024`. YAML preserves that escape, expression evaluation sees no `${{`, and `json.loads` recovers the exact raw matrix name. Both watcher job-list fields use this helper. Generated `rtl-fast.yml:1731` and `rtl.yml:1591` contain escaped names. Consumer `scripts/ci_fail_fast.py:118` and generator line 204 reject raw/expanded identity collisions. The corrected watcher keeps observing unfinished work and detects the subsequent failure. The new control, applied to the actual previous committed workflows, rejects both old matrix-bearing forms after their first read with `observer_error`; see `probe.log`.
- **R897-1-R2, RESIDUE, Docs: RESOLVED.** `sw/firmware/ctrl/README.md:171` contains the requested replacement verbatim: the boundary aggregate judges shard captures, while each compile is judged whole.
- **R897-1-R3, RESIDUE, Docs: RESOLVED.** Public PR readback begins `[A827] Shard the firmware-boundary CI job` and retains `Closes #980`. The executor's correct role prefix satisfies CONTRIBUTING section 2.1; the prior suggested manager prefix was not a requirement to misattribute authorship.

**R897-2-R1 - RESIDUE - Docs - `scripts/ci_fail_fast_selftest.py:179`**

**Title:** New source docstring names a review round.

**Authority/evidence:** The owner's source-comment rule prohibits review rounds in source comments. The added docstring says `then on the round-one form of its skipped matrices`. The behavior is testing the unescaped form, independently of review history.

**Impact:** Wording only. It changes no measurement, figure, verdict, assertion, generated artifact, conformance claim or privacy rule. This item neither makes the verdict negative nor leaves Docs unclean.

**Required outcome / exact fix:** Replace that docstring with `"""Exercise each committed workflow and refuse unescaped skipped-matrix names (#980)."""`.

**Verification:** Inspect the one-line replacement and confirm executable statements remain unchanged. Carry this item on the manager's residue checklist. No other new finding or suggestion was identified.

**Applied lenses and evidence**

**[R897] PASS Conformance - `scripts/ci_runtime_workflows.py:125,204`, `.github/workflows/rtl-fast.yml:1731`, `.github/workflows/rtl.yml:1591` - raw names survive evaluation as required.** The frozen #980 partition, union, stable aggregate, single judging self-test and 30-minute cap remain unchanged. REQ-VER-04's generated-artifact consistency is supported by the independent generator check. All four workflows were checked: `docs` and `elaborate` retain `{}`; `rtl` preserves both raw shard names; `rtl-fast` preserves the firmware-boundary name. No remaining `matrix.` expression occurs in a non-matrix job. The evaluation premise agrees with GitHub's rule that missing properties evaluate empty and matrix values belong to the current job. [GitHub context reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#available-contexts).

**[R897] PASS RTL - seven-file delta, `scripts/ci_runtime_workflows.py:138`, `scripts/ci_fail_fast.py:114`, `tree-verification.json` - product architecture and interfaces remain unchanged.** No HDL, firmware implementation, configuration, CSR, clock/reset/CDC, protocol ownership, builder dispatch, partition table, capture format or gitlink changes occur in the delta. The generator/environment/JSON/observer interface now preserves its documented identities. Collision refusal affects invalid identities; valid expanded results and skipped raw results retain existing behavior. Prior dispatch/partition conclusions and clean RTL coverage remain applicable; no fresh firmware-bank execution is claimed.

**[R897] PASS Robustness - `scripts/ci_fail_fast.py:118,152`, `scripts/ci_fail_fast_selftest.py:137`, `probe.log` - skipped matrices do not terminate observation early.** The runtime control evaluates the committed environment before `watch()`. It presents completed/skipped raw matrices and unfinished work, then a later failure, requiring two reads, one wait, rc 1, the named first failure and no observer-error output. Independent probes repeat this across all four workflows for failure, cancellation, timeout and action-required conclusions. Raw/expanded overlap is refused. Both generator and consumer collision plants are refused. Literal JSON round-trips preserve quotes and literal backslashes. Cancellation fixtures confirm requests reach all eligible same-head siblings. These are offline fixture requests; no GitHub writes occurred.

**[R897] PASS Tests - `scripts/ci_fail_fast_selftest.py:108,137,178,236`, `probe.log`, `gates.json`, `public-evidence.json` - the new control detects the original defect.** The evaluator handles the actual absent `matrix.<property>` expressions, rejects unrelated expressions in literal job lists, and runs before JSON decoding and observation. Testing the old committed files supplies an oracle beyond a newly constructed mutation: both matrix-bearing workflows fail with `watcher stopped observing: observer_error after 1 read(s), rc=0`. Old workflows without matrices still pass. Four focused gates independently pass at this head. The cancellation control is a separate fixture call after observer assertions, not an executed hosted cancellation step; the unchanged generated step condition was inspected to confirm the rc-1/no-observer-error path still requests cancellation.

**[R897] PASS Docs - `docs/testing/CI_WORKFLOWS.md:3479`, `sw/firmware/ctrl/README.md:171`, PR body and published receipt index - documentation matches the correction.** The CI page explains escaping, identity separation and the evaluated-environment control. The README locates judgement in the aggregate. The PR accurately leaves hosted timing and replication open. New source comments were checked against the owner rule; R897-2-R1 is the sole wording residue. Published CI/docs gate receipts are green at the requested head.

**Validation and provenance**

The [published packet](https://github.com/kebag-logic/milan-fpga/tree/2c1b14774f3429806ba8d2e51973f1225761ee0c/review-evidence/fbshard-r1) was inspected by section. `public-evidence.json` verifies published SHA-256 hashes of all 13 round-two receipts and seven selected earlier build/union/plant receipts. The packet's delta byte-equals the local exact-head delta. The evidence commit has no embedded signature and the packet contains no detached signature file. Therefore cryptographic signer authentication was **not** established; this report does not call the packet signed.

The author's round-two gate log names the requested head and records 28/28 rc 0, including CI scheduling, wire accountability, documentation, paths/style, em-dash, hygiene, TODO ownership, shell/Python idioms and documentation inventory. The separate contract self-test records 2,369 items, 5,881 arms, rc 0, 251.51 seconds. The orchestrator self-test is published evidence only; it was not executed here and does not demonstrate an actual workflow replica.

The reviewer independently ran four focused gates concurrently, each with its own raw log and rc file: `ci_gate_workflows.py --check`, `ci_events.py --check`, `ci_fail_fast_selftest.py`, and `ci_runtime_evidence_selftest.py`. All returned 0. `probe.py` also returned 0. Commands ran under foreground supervisors; no detached job was left running.

| Acceptance item | Evidence and current disposition |
|---|---|
| Local shard builds and union | Earlier author's receipts retain their named commits: shard walls 462.01, 393.04 and 449.20 seconds at `d7da99cf`; judgement at `b7b35193` is 250.42 seconds with zero findings/misbehavior and 112 boundary, 185 pin, 4 figure and 4 shard controls. This delta changes none of that compile/judging code. These are not fresh builds at `5392adf9`. |
| Dropped and duplicated work | Published dropped/duplicated captures return 2 and name missing/repeated units. The normalized source-union receipt records 1,262 distinct compiles per side and zero missing/extra. It proves set equality, not equality of raw invocation multiplicity. Prior independent dispatch/union conclusions stand. |
| Generated workflows and docs | Independent generator/contract checks pass; published exact-head docs receipts pass. F1 and R2 are resolved. |
| Hosted execution and timings | PENDING. Exact-head `rtl-fast` run `45151518705`, `rtl-full` run `45151518484` and `elaborate` run `45151518628` were pending; `docs` run `45151518606` was queued. The rtl-fast jobs query returned zero jobs. No measured shard execution, completed required context or successful hosted transfer is claimed. |
| Runtime target | Local measurements are below 15 minutes; setup-inclusive eight-minute shard and five-minute aggregate figures remain projections. Hosted measurements remain required by #980. |
| Local replica and final candidate | Manager-owned and pending. No executed replica or current-dev candidate acceptance is inferred from source-head receipts. |

Issue readback contained the takeover and two review-ready comments. PR readback contained the two review-start comments and R897-1 findings; no manager execution receipt was present. After writing `independent-verdict.md`, review-submission and inline-thread queries returned empty lists. No additional public findings require reconciliation in that readback.

**Reviewer-owned ledger**

Each row applies the delta at the current head and retains prior conclusions only for artifacts and dependencies unchanged since R897-1. R897-2-R1 does not unclean a lens under the owner's residue rule.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #980 acceptance; REQUIREMENTS.md:333; ci_runtime_workflows.py:125,204; generated envs; probe.log | R897-2; untouched R897-1 conclusions retained | 5392adf989349b68cfbb54d91fd0413c5b745521 |
| RTL | CLEAN | Seven-file delta; unchanged builders/interfaces/gitlinks; ci_runtime_workflows.py:138; ci_fail_fast.py:114; tree-verification.json | R897-2; untouched R897-1 coverage retained | 5392adf989349b68cfbb54d91fd0413c5b745521 |
| Robustness | CLEAN | ci_fail_fast.py:118,152; ci_fail_fast_selftest.py:137; four workflow envs; collision/failure probes | R897-2; untouched R897-1 conclusions retained | 5392adf989349b68cfbb54d91fd0413c5b745521 |
| Tests | CLEAN | ci_fail_fast_selftest.py:108,137,178,236; old committed negative controls; gates.json; public-evidence.json | R897-2; untouched R897-1 conclusions retained | 5392adf989349b68cfbb54d91fd0413c5b745521 |
| Docs | CLEAN | CI_WORKFLOWS.md:3479; ctrl/README.md:171; PR/issue bodies; comment delta; published receipts | R897-2; untouched R897-1 conclusions retained | 5392adf989349b68cfbb54d91fd0413c5b745521 |

**Limits and pending manager duties**

- Carry R897-2-R1 on the residue checklist. This verdict applies only to the named head; subsequent artifact changes require appropriate coverage.
- Obtain the second independent positive review and complete hosted/replica acceptance, including shard times and artifact transfer. A hosted skipped-matrix observation would complement the modeled control. Queued, pending and skipped contexts are not executed-job evidence.
- No manager source bank exists at this head, and none is claimed. Source execution evidence is the author's published receipts, supplemented by the focused reviewer checks above.
- Validate the current-dev merge candidate with manager-owned builder/native banks at the merge turn, publish receipts, then complete authorized merge and post-merge containment. Source base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6` differs from supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`; this review does not validate their composition or a future tip.
- Physical calibration **NOT RUN**. Field skips and desk checks are not hardware proof. No full parent/processor, synthesis, builder or hardware banks, container/local workflow replica, host orchestrator or its self-test were run. No source edits, commits, pushes, GitHub writes, shared installations or other-checkout edits occurred.
- Direct verification confirms all 1,935 superproject tracked blobs, kinds/modes and index match the exact head. All five required initialized submodules match their gitlinks, tracked bytes/modes and indexes; the unused external gitlink remains pinned and uninitialized. See `tree-verification.json`. No restoration was needed because probes mutated only in-memory fixtures. Disposable files remain under packet `scratch/`.

Portable reproduction: `python3 probe.py CHECKOUT PACKET`, `python3 run_gates.py CHECKOUT PACKET`, `python3 inspect_evidence.py CHECKOUT PACKET`, and `python3 verify_tree.py CHECKOUT`. Use an existing packet directory with `scratch/`; the published evidence commit must be available in the clone. Publish only `REPORT.md` and files listed in `MANIFEST.sha256`.

R897-2 FINISHED

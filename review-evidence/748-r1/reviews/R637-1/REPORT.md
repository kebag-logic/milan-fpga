[R637] NEGATIVE - exact head c48bfe38b25f002d24898cec265520b9fc1a7111

R637-1, external independent review of issue #748 / PR #749.
Tree: `33e999cb842593dbbd9d2e97cfeea587d581b63a`.
Compared against `9ef717727e6fdac11ee7f01672fefae948452343`.
All five lenses were applied. Two findings prevent a positive verdict: one MAJOR and one MINOR. One new comment-only RESIDUE and the retained prior findings are separate. The workflow isolation change looks correct; the new native control needs correction before approval.

Authority and scope: [frozen assignment](https://github.com/kebag-logic/milan-fpga/issues/748#issuecomment-6200705849), issue body and public scope comments; `AGENTS.md` sections 6-7; `CONTRIBUTING.md` sections 2-3 and 6; `docs/README.md`; `REQUIREMENTS.md:307` (REQ-VER-02/03/04); `docs/testing/CI_WORKFLOWS.md:1401` and its act replication boundary; `scripts/ci_litex_env.py`; `sw/litex/patches/apply.sh`; builder gate 23h. The decision selects a job-private toolchain and shared cache input, with no product or test-semantics changes. The three-commit history and complete five-file diff were examined before public review findings.

## Findings

### R637-1-F01 - MAJOR - Conformance, Robustness, Tests, Docs

Artifact: `scripts/ci_toolcache_isolation.py:194`, particularly line 207; `sw/builder/test_builder.py:22661`, `:24451`, `:24547`; claimed guarantee at `docs/testing/CI_WORKFLOWS.md:1442`.

Authority/evidence: the control promises that both gate 23h and its negative control pass, and the review contract requires tests that detect the defects they claim to detect. `verify()` probes only `litex` and `pythondata_cpu_vexiiriscv`, then accepts the builder process exit code. The builder needs `migen`, `litex` AND `litex_boards` to select an interpreter. With a dependency absent it skips both selected gates and exits zero. No receipt or NOT RUN result is examined by the new caller.

The disposable probe installed the real pinned packages in a private Python 3.12.13 environment, excluding `litex-boards`, and deliberately left the checkout/patch setup absent. The actual `verify()` returned `[]`; its actual builder output said `ALL GATES PASS EXCEPT 2 NOT RUN`. Restoring only the pinned `litex-boards` dependency made the same unpatched tree fail gate 23h. The cache sentinel remained unchanged. See `probe-skipped-gate.json`, `probe-skipped-gate.log` and `probe-skipped-gate-steps.log`; reproduce with `probe_skipped_gate.py <repo> <packet> --python python3.12` in a fresh packet scratch directory.

Impact: an incomplete interpreter can suppress both patch checks while the isolation verifier reports no problem. A skipped negative control is accepted as successful patch evidence. This does not show that the published normal runs skipped, or that the venv isolation fix fails; it demonstrates a false acceptance path in the new validator.

Required outcome: the isolation verdict must require actual successful execution of both selected patch checks, and refuse either unavailable or skipped check. Keep the documented guarantee, or narrow any claim that cannot be proved; merely preserving exit-code checking is insufficient.

Verification: the missing-dependency fixture must produce an isolation failure with the skipped check identified. A complete correctly patched interpreter must pass, and an available but unpatched interpreter must still fail. Preserve the existing shared-cache negative controls.

### R637-1-F02 - MINOR - Robustness, Tests

Artifact: `scripts/ci_toolcache_isolation.py:218`, `:231`, `:234`, `:171`, `:186`.

Authority/evidence: `--work` accepts an empty directory without requiring an absolute path. That relative path is retained in the leg base, interpreter PATH, environment files and script argument. `Leg.run()` then changes its child working directory to the exported workspace. A step path created relative to the caller is consequently opened relative to a different directory.

`probe_relative_work.py <repo> <packet>` exercised the production `Leg` and `drive` methods with the harmless script `true`. Relative base `run/leg` failed with `bash: run/leg/step.sh: No such file or directory`, rc 1. The equivalent absolute base passed, rc 0. Receipt: `probe-relative-work.log`.

Impact: the documented native control fails on an ordinary relative `--work` argument before testing isolation; relative environment paths would also resolve against the wrong directory.

Required outcome: normalize the work root before deriving child paths, or explicitly reject relative paths before planting/copying any state. Make the CLI contract and example agree with the chosen behavior.

Verification: exercise an empty relative work directory and an absolute directory through the CLI. They must either perform equivalent checks or the unsupported form must receive an immediate, explicit argument refusal. Neither may fail later as a missing step script.

### R637-1-F03 - RESIDUE - Docs

Artifact: `.github/ci-templates/elaborate.yml:148`; `scripts/ci_toolcache_isolation.py:4`; explanatory additions at `scripts/ci_events.py:565` and `:7454`.

Authority/evidence: the supplied owner comment rule asks source explanations to carry issue and requirement IDs. The template explanation and control module explanation carry neither; the two contract explanations cite #748 but no requirement. No newly added bench label, lane name, reviewer ID or issue-comment ID was found in source comments.

Impact: comment attribution only; no behavior, measurement, test result or privacy finding. This is RESIDUE under the specific comment rule and does not independently prevent clean coverage.

Exact fix: append `(#748; REQ-VER-04)` to the template and module explanations, and change the two new explanatory #748 citations to `(#748; REQ-VER-04)`, preserving their behavior/reason text. Regenerate the workflow if required by the normal process; generated commands must remain identical.

Verification: inspect only the added comment text for the two IDs and prohibited provenance labels. Carry this item on the residue checklist.

## Independent lens evidence

**Conformance.** The assignment selects the implemented isolation boundary. Both generated workers put `python3 -m venv "$RUNNER_TEMP/litex-venv"` and the GITHUB_PATH prepend after setup-python and before installation. `scripts/ci_events.py:565`, `:1217`, `:7453` pin the script and position. Core workflow behavior meets the scope; F01 leaves the control guarantee unclean.

**RTL.** PASS - `reviewed.diff`, `.github/workflows/elaborate.yml:111` and `:346`, `scripts/ci_gate_workflows.py:61` and `:190`, `scripts/ci_litex_env.py:84`, `sw/litex/patches/apply.sh:32`, and builder interpreter selection at `sw/builder/test_builder.py:22634`. The diff changes no RTL, firmware, product configuration, patch content, source pin or gitlink. The existing generator treats `Put ` as setup and preserves its order in both workers; no generator source edit was necessary. Consumers resolve the active Python environment; the venv isolates mutable packages without changing the generated hardware contract. No clock/reset/CDC or protocol-field change is introduced.

**Robustness.** The cache comparison covers additions, deletions, bytes, types, modes and link targets. Step failures and incomplete result counts prevent success, and a failed leg aborts the rendezvous so its sibling can finish. The published shared-cache controls fail as intended. F01 and F02 remain open for unavailable dependencies and ordinary path input.

**Tests.** The reviewer executed focused falsification probes, not full banks. `probe-contract.log` records a pristine 2199-item contract with zero findings, byte-exact regeneration of all four workflows, all three required semantic mutations caught, and deletion from either generated worker caught. `probe-skipped-gate*` and `probe-relative-work.log` establish F01/F02. Existing public executions are evaluated below; they were not relabeled as reviewer executions.

**Docs.** `docs/testing/CI_WORKFLOWS.md:1422` accurately describes the job boundary and the race. The new control declares each omitted setup-window step and refuses an unknown step. Public scope and receipts distinguish native setup from container replay and product execution. F01 leaves the assertion that both patch checks must pass unproved by the validator; F03 is comment residue.

## Workflow write inventory and caches

The complete generated-run inventory is retained in `generated-write-inventory.txt`, with its template search in `workflow-write-search.txt`.

| Writers examined | Destination and isolation |
|---|---|
| setup-python | Present only in the two elaborate workers; selects the seeded cache interpreter. |
| LiteX installation, CPU checkout/submodules, cached metadata copy, patch series, Scala generation | Active venv site-packages; each job has its own RUNNER_TEMP. The later sbt and Verilator PATH additions contain no competing Python. |
| Other pip installations, including rtl-fast firmware-boundary LiteX and generated evidence readers | Jobs without setup-python use their image interpreter; download caches are under each HOME. Elaborate aggregate/collector readers also have no setup-python. |
| Repository and processor fetches | Per-job workspace. |
| sbt | Per-job HOME archive cache and image-private `/opt/sbt`. |
| Verilator/Yosys builds, installs and symlinks | Image-private `/tmp`, `/opt/verilator`, `/opt/yosys`, `/usr/local/bin` and apt state. |
| sv2v, apt download planner, field oracle | RUNNER_TEMP archives/builds plus image-private extraction/install paths. |
| RV32 SDK, including elaborate | Per-job `$HOME/br-milan-rv32/host`; download scratch is private. |

The [upstream v0.2.89 mount implementation](https://github.com/nektos/act/blob/v0.2.89/pkg/runner/run_context.go#L127) confirms one `act-toolcache` mount and job-named workspace/environment volumes, with RUNNER_TEMP `/tmp`. The reviewed workflow does not add another shared writable mount. An independent read of the public runner image registry configuration (`runner-image-config.json`, digest-bound) found no tool-cache directory on its default PATH. This is current image metadata, not an inspected replay container; no container was executed.

Cache formulas and source template cache paths are unchanged. Keys hashing workflow YAML miss once, as documented. The generated apt cache changes `ci_packages_16` to `ci_packages_17`, including its path/version. The SDK formula is unchanged and does not include the workflow hash; this is preservation of eligibility, not a new observed cache hit.

## Published executable evidence

The [published evidence tree](https://github.com/kebag-logic/milan-fpga/tree/9ae6b8b2e900a3c6d076a2eb345916231515f045/review-evidence/748-r1) was fetched after the independent diff pass. All 27 selected author receipt/script files matched the published SHA-256 manifest (`evidence-fetch.log`). Public handoff prose and another review report were not used as technical authority.

- `control/fix-3.json` binds c48bfe38: both legs report all four setup steps and gate 23h rc 0; 6303 planted paths, zero changes; 47.9 s setup. The earlier two fixed runs agree. The published receipt records a gate process rc, so F01 limits what that rc alone proves.
- `control/shared-3.json` binds this head: a placement fails, 9296 paths change, isolation is false. The other two shared runs and both controls at dev 9ef71772 agree. This is direct evidence that sharing exposes the race, not merely a source-text assertion.
- `applyrace/summary.txt` reports 20/20 shared trials with a failing leg and 0/20 private trials. Its published script was inspected; individual trial logs are not included, so this remains supporting summarized evidence.
- Native full elaboration-driver tails report 987.33 s and 452.45 s at a0d65349. The final commit changes only the control docstring, so those product-execution artifacts are unchanged at this head. Gate 11 calibration is explicitly NOT RUN; this supplies no physical proof.
- `docs-gates-c48bfe38.tsv` and JSON record 46 rc-zero commands at the head. Installation substitutions and omitted runner plumbing are explicit in `run_docs_gates.py`; this is native gate evidence, not a full hosted execution.

Measured venv cost is 2.3-2.4 s per leg. Published #737 estimates of 1475/1353 s against 1620 s become approximately 1478/1356 s. These are projections using native setup timing, not new hosted timing measurements. Native VexiiRiscv placement costs approximately 12-14 s per private leg; Scala work is private as intended.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F01) | Frozen assignment; template:143-184; ci_events.py:565,1217,7453; control:194-208; published controls | R637-1 applied; no clean covering round | c48bfe38b25f002d24898cec265520b9fc1a7111 |
| RTL | CLEAN | Complete reviewed.diff; generator:61,190; generated elaborate workers; ci_litex_env.py:84; apply.sh:32; builder:22634; unchanged gitlinks | R637-1 | c48bfe38b25f002d24898cec265520b9fc1a7111 |
| Robustness | UNCLEAN (F01, F02) | control:95-117,123-208,218-253; dependency and relative-path probes; shared/dev receipts | R637-1 applied; no clean covering round | c48bfe38b25f002d24898cec265520b9fc1a7111 |
| Tests | UNCLEAN (F01, F02) | Three semantic arms and two generated-leg probes; gate 23h/negative control; public setup, driver and docs receipts | R637-1 applied; no clean covering round | c48bfe38b25f002d24898cec265520b9fc1a7111 |
| Docs | UNCLEAN (F01; F03 is residue only) | CI_WORKFLOWS.md:1422-1453; PR scope/cache/cost claims; added source comments; published evidence manifest | R637-1 applied; no clean covering round | c48bfe38b25f002d24898cec265520b9fc1a7111 |

## Limits and manager duties

The independent verdict and ledger were written before the final public-finding readback. That readback returned [R636-1](https://github.com/kebag-logic/milan-fpga/pull/749#issuecomment-6203272953), published meanwhile. Its verdict does not resolve F01/F02 above. There were no submitted PR reviews or inline review comments. `prior-findings-reconciliation.json` records the readback and dispositions:

- **R636-1/F1, RESIDUE, Conformance/Docs: RETAINED.** The PR inventory parenthesis still omits the LiteX pin install in `rtl-fast` firmware-boundary, independently present in `generated-write-inventory.txt`. Exact fix: expand `(pyyaml, behave, renderer, HDL reference, wavedrom, evidence reader)` to `(pyyaml, behave, renderer, HDL reference, wavedrom, evidence reader, and the LiteX pins in rtl-fast firmware-boundary)`. This is an enumeration omission; the stated private destination is correct. It remains a residue checklist item.
- **R636-1/F2, SUGGESTION, Tests: RETAINED OPTIONAL.** The published 27-file evidence selection contains no post-builder cache comparison receipt for the reported 0-of-6299 comparison. Publishing that comparison would strengthen the later-generation evidence. Its absence does not negate the setup cache manifest or turn this optional request into a blocking finding.

No prior finding is silently marked resolved. The new F01/F02 require correction and independent re-review.

No manager source bank was run or inferred. The author receipts are the source execution evidence. The manager owns hosted/act acceptance and current-dev candidate validation. At API readback, elaborate/docs were still running, rtl-fast/rtl-full were queued; only wire-accountability and docs-check-no-git had completed successfully in the inspected job lists. No skipped context was counted as execution. The returned PR comments contained review-start notices and, on final readback, the internal review, but no four-job replay receipt, despite the assignment saying it had been posted; this review cannot certify that unavailable receipt. The manager must attach or identify it and settle acceptance.

The merge turn must build and validate the final candidate against live dev (the supplied live tip is `973e681be51882840670b8bc566f02b8005b1996`), publish the builder/native and hosted/replay receipts, obtain the required independent approvals, and perform containment after authorized merge. This source-head review does not approve that future merge tree. Physical calibration NOT RUN and field skips are not hardware proof.

No full parent, processor, gPTP, portability or builder bank was rerun. No hardware, container execution, host replay orchestration, privilege, source fix, commit, push or GitHub write was performed. No other review report was consulted before the independent verdict and ledger were written; the public internal findings were then reconciled as required. No private author material was consulted. All disposable work stayed inside the packet scratch directory. The initial probe preparation used an incompatible host Python for the pinned wheel constraint and stopped at dependency resolution (`probe-preparation-failure.log`); the recorded finding uses Python 3.12.13 instead (`probe-python-version.txt`, `probe-pinned-packages.txt`).

`checkout-integrity.json` directly verifies all 1371 superproject blobs, their modes and index entries, plus the four required registered submodules and their pinned blobs. The checkout remains exactly at the requested head/tree and its status is empty. Final publication is limited to REPORT.md and MANIFEST.sha256-listed files; scratch is excluded.

R637-1 FINISHED

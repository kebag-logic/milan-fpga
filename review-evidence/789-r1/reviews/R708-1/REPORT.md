[R708] POSITIVE - exact head fddf3671ebc96a953755fa1b9a3ecec5f071a350

# R708-1 external independent review: issue #789, PR #794

Source review is positive. No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is filed. This does not declare issue acceptance complete or authorize merge. Required hosted timings and live replay remain pending; the manager owns their acceptance.

Head `fddf3671ebc96a953755fa1b9a3ecec5f071a350`, tree `d758e8963591f123d3398719f0a331f9cc9bbf91`, base `76de691e5625cc4ea2f9a19def9e07c1183a14ee`. One commit, five files, 458 additions and 31 deletions. The complete examined delta is `reviewed.diff`.

## Reconstruction and authorities

Read repository operating instructions and CONTRIBUTING, then `docs/README.md`, the [issue body](https://github.com/kebag-logic/milan-fpga/issues/789) and [frozen assignment](https://github.com/kebag-logic/milan-fpga/issues/789#issuecomment-6413044539), linked requirements and CI authorities, then the complete diff/history, then public executable evidence. No other review of PR #794 informed this verdict or ledger.

Authorities examined: `REQUIREMENTS.md:305` (REQ-VER-01 through REQ-VER-06), CONTRIBUTING sections 2 and 3, `docs/testing/CI_WORKFLOWS.md` Fast feedback, source-tool provenance and act trust boundary, `.github/ci-templates/rtl-fast.yml:134`, and `scripts/ci_suite_workflows.py:68` as the existing separation model. No product protocol, RTL or hardware release contract changes.

The assignment keeps other jobs unchanged and forbids timeout increases. Existing jobs above 30 minutes are outside this delta; this review does not claim they satisfy a new universal 30-minute policy.

## Findings and lens results

There are no findings. Each clean result below names examined artifacts and evidence.

**[R708] PASS Conformance - `scripts/ci_gate_workflows.py:197,240`; `.github/workflows/rtl-fast.yml:254,341`; `probe.log`, `drift-probe.log` - source satisfies the frozen #789 decision.**

- `ci_gate_workflows.py --check` regenerates all four workflows through the gate, suite, installation and runtime generators and passes. The templates remain unchanged. This is the workflow-writing entry point; the component generators are invoked through it. Evidence-pin generation and documentation TOC check also pass.
- Independently calculated SHA-256 of the complete template build step's sorted compact JSON: `06e5a02fa8b585ca1b3cc3153245cd97f8b1009666d3b15728f325ed9bd22279`. Producer and consumer keys match and contain version, immutable source commit, that digest, `ubuntu-24.04` and `runner.os`. Neither contains a workflow hash or fallback key.
- An independent disposable fixture plants the old installation under its complete key. Recipe, version, image and build-step environment changes each miss that key. An unrelated elaboration-check edit retains it. This proves generated key identity/policy, not remote cache-service behavior.
- Four hand-edited workflow defects are refused by the real generator check: accepting a cache miss, sharing a stale recipe key, sharing a stale version, and raising the new job's timeout. Controls pass before and after.
- The consumer needs `changes` and `yosys-tool`, restores `/opt/yosys` with `fail-on-cache-miss: true`, and never builds Yosys. All pre-existing timeouts are unchanged; the new job has 30 minutes. Hosted timing acceptance remains pending below.

**[R708] PASS RTL - `reviewed.diff`; `scripts/ci_gate_workflows.py:240`; `.github/workflows/rtl-fast.yml:377`; `probe.log` - validation architecture and consumer checks are preserved.**

- No HDL, firmware, submodule pin, clock, reset, CDC, FSM, width or product interface artifact changes.
- Every consumer step from installed-version verification onward equals its base step except generated IDs. This retains bundled ABC, sv2v, all three integration-heavy tops, OOC read sets and source/resource checks, ROM/failure controls, active-guard controls and result-cache controls. Dependency fetching remains before restoration.
- Every unrelated parsed job equals its base job. Only the new producer, consumer, verdict, manifest dependencies and fail-fast job inventory change.
- The new producer carries the original checkout/cache/build. Source-commit verification precedes compilation and bundled ABC is installed. Existing installation/runtime transformations remain in force.

**[R708] PASS Robustness - `scripts/ci_gate_workflows.py:215,245,262`; `.github/workflows/rtl-fast.yml:1298`; `probe.log`, `generator_selftest.log` - cache and failure paths fail closed.**

- The actual aggregate shell rejects `failure`, `cancelled` and an empty tool result when the consumer is skipped. It accepts all-success. The repository self-test also proves the documentation-only skip case.
- Tool and consumer use identical paths/keys without fallback. The [upstream action implementation](https://github.com/actions/cache/blob/v4/src/restoreImpl.ts) fails on an ordinary cache miss with this input and names the requested key. Its [action definition](https://github.com/actions/cache/blob/v4/action.yml) saves in the successful post-step, before a dependent job starts.
- Seventeen planted generated-graph defects and five malformed template cases are refused by name, including missing/reordered/interposed build steps, missing dependencies/key inputs, fallback keys and disconnected verdict results.
- The key isolates ordinary repository-controlled recipes, not a hostile cache service. It identifies the runner image label; weekly updates within `ubuntu-24.04` intentionally share it, as the public PR states.

**[R708] PASS Tests - `scripts/ci_gate_workflows_selftest.py:114,182,234`; `checks.json`, `more-checks.json`, `probe.log`, `drift-probe.log` - executable checks discriminate the changed contracts.**

- All 23 reviewer-run checks pass: the complete 14-command scheduling/evidence block, scope self-test, event check/self-test, and six documentation/code-quality checks. The event gate reports 2,199 contract items and 5,258 self-test arms; the self-test took 186.492 seconds.
- Local environment: Python 3.14.8 and PyYAML 6.0.3. Locked Markdown dependencies were installed only in packet scratch. Each command has its own raw log, return code and elapsed time. At most four independent check processes ran concurrently; no heavy build ran.
- The runner was read, never imported or executed here. `scripts/act_ci.py` is unchanged from base, blob `865867c373646d33322250e353ddc4cfa2f777b8`. Its generic label/action validation covers the new job's ordinary actions and label. The reviewer executed `ci_workflow_plan.py`'s planner and confirmed the new display name and producer-to-consumer/verdict edges. `ci_local_manifest.py:51` maps events by job ID, matrix and workflow, so it needs no per-job table edit.
- The [published author packet](https://github.com/kebag-logic/milan-fpga/tree/787d005e43b130fb18d0f44078a46fe3d1883324/review-evidence/789-r1) supplies the runner tests forbidden to this review: ordinary self-test, 623 successful controls, and flat-install contract self-test, 621, both PASS. Its Python 3.12.3 and 3.14.8 summaries report zero return codes. Its offline mapping receipt binds this exact head and unchanged trusted runner. These are author evidence, not reviewer execution or proof of live replay.
- Nine downloaded author artifacts match the publication manifest's SHA-256 values (`integrity.log`). No manager source bank is claimed.

**[R708] PASS Docs - `docs/testing/CI_WORKFLOWS.md:317,341,3286`; `docs/testing/TESTING.md:331`; `docs_check.log`, `em_dash.log` - documentation matches source and evidence boundaries.**

- Policy explains the separate build, key inputs, dependency/failure semantics, unchanged publication census and rerunning all jobs after an unsuccessful cache save. Historical build-step figures remain historical, not measurements of this PR.
- R705-1-01's replacement sentence is present verbatim at line 331; `probe.py` checks its exact bytes.
- Documentation/privacy, style, paths, TOC, Python idiom and added-line em-dash gates pass. The last judges 39 added lines with zero findings.
- Added source comments contain no newly introduced bench lane label, lane name, review round, reviewer ID or issue-comment ID. The existing documentation reference to #665's comment is retained through a reflow, not newly introduced. No wording residue is filed.

## Reviewer-owned ledger

Every lens was applied independently. CLEAN means no open source-review finding; it does not discharge pending hosted acceptance.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #789 scope; `ci_gate_workflows.py:197,240`; `rtl-fast.yml:254,341`; generator/key/drift receipts | R708-1 | fddf3671ebc96a953755fa1b9a3ecec5f071a350 |
| RTL | CLEAN | `reviewed.diff`; consumer/base comparison in `probe.log`; `ci_suite_workflows.py:68` | R708-1 | fddf3671ebc96a953755fa1b9a3ecec5f071a350 |
| Robustness | CLEAN | `ci_gate_workflows.py:215,245,262`; aggregate outcomes; graph/template controls; key fixture | R708-1 | fddf3671ebc96a953755fa1b9a3ecec5f071a350 |
| Tests | CLEAN | new self-test; 23 local check receipts; independent probes; published runner receipts; planner/event mapper | R708-1 | fddf3671ebc96a953755fa1b9a3ecec5f071a350 |
| Docs | CLEAN | `CI_WORKFLOWS.md:317,341,3286`; `TESTING.md:331`; public evidence; documentation gates; comment review | R708-1 | fddf3671ebc96a953755fa1b9a3ecec5f071a350 |

## Hosted observations and pending manager duties

At **2026-10-26 10:51:31 UTC**, the exact-head [rtl-fast run 40309456540](https://github.com/kebag-logic/milan-fpga/actions/runs/40309456540) lists `bdd-conformance` successfully completed, the fail-fast watcher in progress, and `changes` queued. Neither `yosys-tool` nor `yosys-elaboration` has an execution/log yet. There is therefore no live tool-build log to grade and no cold-build or restored-consumer duration to report. Other runs are in `hosted-snapshot.json`; no completed required-context acceptance is claimed. Queued/skipped contexts are not executed evidence.

The manager must still:

1. Read the first new-key cache-miss tool job's log and measure its whole job, including setup and successful cache save, below 30 minutes. Stop for a decision if the cold tool build cannot fit.
2. Confirm the consumer restores that key, runs every existing check without rebuilding, and finishes below 30 minutes on this workflow-editing head. Record both timings and links in the PR body. Historical timings do not satisfy these acceptance items.
3. Publish trusted-runner live replay evidence, including the new job, and obtain the required hosted contexts. Offline mapping does not discharge live replay.
4. Obtain the other independent review and resolve its findings; validate the final current-dev merge candidate with required builder/native banks. Source-head and final-candidate evidence are distinct. No manager source bank ran at this head.
5. Complete merge authorization, post-merge containment, authoritative status updates and issue closure. This review performs none of those actions.

## Prior findings and real limits

The initial and final PR #794 comment reads contained only two review-start notices. Submitted reviews and inline review threads were empty when checked after the independent diff pass. No prior PR #794 finding required disposition. The final issue-comment read adds no new manager execution evidence. Linked R705-1-01 is resolved verbatim. R705-1-02's build/cache separation is implemented, while the required hosted outcome remains pending under #789; it is not cleared using historical timings.

No full parent, processor, gPTP, Yosys or builder bank ran. No simulator was invoked. No Docker, act, host runner/self-test, privilege, shared install, hardware, source fixes, commits, pushes, GitHub writes, author contact or sub-agents. Physical calibration **NOT RUN**; field skips and skipped hosted contexts are not hardware proof.

All disposable inputs/environments are under packet `scratch/`, excluded from publication. Source bytes were never edited. Integrity verification checks 1,442 parent blobs and all blobs/modes/index entries of the four required submodules at their gitlinks: protocol processor `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8`, gPTP processor `55680bff3b287b9a7b0c759f51471fa617c17335`, axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, TSN stack `70936b77dc41981e192438388cd0aced69954f18`. The TSN stack was initialized at its existing pin for verification. The parent remains detached, clean and at the assigned head/tree. `MANIFEST.sha256` enumerates publishable receipts and scripts; scratch is excluded.

Publication note: local scratch prefixes in two logs are replaced with `<scratch>`; `REDACTIONS.json` records original and published digests. Unmodified originals remain in unpublished scratch. Public author receipts retain their published bytes and hashes.

R708-1 FINISHED

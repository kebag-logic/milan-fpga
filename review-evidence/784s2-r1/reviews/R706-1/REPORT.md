[R706] POSITIVE - exact head 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0

# R706-1 external independent review: issue #784 / PR #788

Source review is positive across all five lenses. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is filed. This verdict does not assert that hosted acceptance or the merge bar is complete. Independent runner execution was prohibited by the brief; published runner receipts were examined instead.

Reviewed tree: `05ae0179dbffa852651aa7ec8367758b380672d0`. Base: `a8594bb95631fa5c49d18fa0bbc9530e31ad59aa`. One commit, 20 changed files.

## Authority and reconstruction

Read AGENTS.md / CONTRIBUTING.md, docs/README.md, the [issue body](https://github.com/kebag-logic/milan-fpga/issues/784), the [step 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/784#issuecomment-6409728491), and the [temporary ruleset/restore decision](https://github.com/kebag-logic/milan-fpga/issues/784#issuecomment-6400810252). REQ-VER-04 governs generated artifacts and documentation; REQ-VER-02/03 retain the separate exact-candidate obligations. The applicable interface authority is `docs/testing/CI_WORKFLOWS.md:1734` and its single-label contract at `:2036`.

The complete diff and history were examined before the [public author evidence](https://github.com/kebag-logic/milan-fpga/tree/042bf69d5a754170863d6504e25f940c1ec32342/review-evidence/784s2-r1). No private author material was used.

## Findings and prior dispositions

No new finding.

**R697-1-01 is resolved:** `CI_WORKFLOWS.md:2043` contains the prescribed replacement sentence verbatim after normalizing line wrapping. It distinguishes an unmapped label absent from the built-in table from a built-in label using the default image. See `prior-wording-finding.txt` and `documentation-review.log`.

**No prior finding on PR #788 was published at inspection.** The complete public discussion returned only the two review-start notices, without a submitted review or inline finding. See `pr-public-discussion.json`. No current-PR peer report was consulted.

## Five-lens results

**[R706] PASS Conformance - source.diff; source-audit.log; scripts/act_ci.py:92,2062,4828 - source criteria match #784 step 2.**

The independent census covers all Python scripts, then CI generation modules and alternate label sources. Three modules emit literal job labels: `ci_gate_workflows.py:165`, `ci_runtime_workflows.py:127,145,159`, and `ci_suite_workflows.py:44,76`. Four templates supply 22 source jobs. `ci_install_workflows.py` preserves labels and introduces none. `yosys_shards.py` schedules top names; it has no workflow writer or generator check mode. Its only label reference was historical commentary.

`ci_gate_workflows.py` is the sole workflow-writing entry point. Its check passes. Normal generation and check over a disposable copy reproduce all committed workflows exactly. The runtime, suite and installation helpers are exercised through that entry point; they have no independent command-line check modes.

There are 46 generated job definitions: docs 9, elaborate 6, rtl-fast 15, rtl 16. Independent byte comparison proves each base workflow becomes its head version by replacing only `runs-on: ubuntu-latest` with `runs-on: ubuntu-24.04`. No steps, conditions, permissions, timeouts, matrices, dependencies or digests change.

No floating label remains in workflows, templates or the five generation/scheduling modules. The runner's accepted-label literal is exactly `("ubuntu-24.04",)`. Its remaining `ubuntu-latest` references are comments or negative probes. The membership check names the refused value; the command builder emits one platform mapping from the same tuple.

Source criteria pass. The issue's all-jobs hosted-image and green-check criterion is **not yet established**; it remains a separately assigned manager acceptance duty.

**[R706] PASS RTL - source.diff; scripts/act_ci.py:5987-6015; checkout-verification.log - no product architecture change, validation order preserved.**

The full 20-file delta contains no RTL, timing constraint, firmware implementation, interface or gitlink change. CDC, reset, FSM, widths and backpressure behavior have no changed implementation in this PR. The runner still validates checkout bytes and workflow sandbox before submodule initialization and runtime boundary entry. Only allowed-label behavior changes; memory/swap limits and image mapping architecture remain intact. Exact workflow comparison excludes scheduling or command changes.

No full RTL, processor, synthesis or builder bank was run by this reviewer. This lens result makes no new functional or hardware claim.

**[R706] PASS Robustness - scripts/act_ci.py:2045,6719,6741,6809,13275 - exact labels, named refusals and independent restriction reasons.**

The loader uses scalar strings and refuses duplicate keys. Tuple membership admits only the exact scalar label: missing labels, expressions, lists, mappings, case changes, ARM variants and other labels cannot equal it. Refusals quote the actual value and precede runtime entry.

The changed tests exercise production sandbox and command construction. Positive fixtures now use the accepted label. Container/service, reusable-workflow and action negative tests demand their own reason fragments, preventing an earlier label refusal from making those restrictions vacuously pass.

Published raw receipts show passing controls on CPython 3.12.3 / PyYAML 6.0.2. Re-admitting `ubuntu-latest` fails three named checks. Dropping platform words fails the replay mapping, exact platform-list and accepted-equals-mapped checks. Definitions and raw outputs were inspected and verified against the published SHA-256 manifest. These were author executions, not reviewer executions.

**[R706] PASS Tests - focused-results.json; source-audit.log; public-author/receipts/gates-py312/ and mutants/ - meaningful controls and reproducible focused gates.**

Reviewer executions:

| Command | Result |
|---|---|
| `python3 scripts/ci_gate_workflows.py --check` | rc 0, all generated workflows match |
| `python3 scripts/ci_events.py --check` | rc 0, 2,199 contract items |
| `python3 scripts/ci_events.py --selftest` | rc 0, 5,236 arms; 209.941 seconds |
| `python3 scripts/ci_gate_workflows_selftest.py` | rc 0, scheduling and union controls PASS |
| `python3 scripts/ci_workflow_plan_selftest.py` | rc 0 |
| `python3 scripts/yosys_shards.py --selftest` | rc 0 |
| `python3 scripts/docs_check.py` | rc 0, zero findings; scrub 23/23, routing 4/4 |
| `audit_sources.py <checkout>` | rc 0, comparison, regeneration and receipt hashes |
| `verify_documentation.py <checkout>` | rc 0, prescribed wording and added-comment audit |
| `verify_checkout.py <checkout>` | rc 0, tracked bytes, modes, index and required pins |

The six independent focused commands ran concurrently under one foreground driver, with six workers and a 540-second timeout. No heavy build ran.

An independently planted hand edit changed one regenerated docs job back to `ubuntu-latest` in scratch. Generator check returned 1 and named `.github/workflows/docs.yml: regenerate the gate jobs`, proving drift detection.

Runner self-test, installed runner contract gate, re-admission mutation and dropped-platform mutation were **NOT RUN independently**. The public controls end PASS; both public mutations end with three named failures. `source-audit.log` verifies those receipts against the published manifest. Static inspection is not represented as executable runner probing.

**[R706] PASS Docs - docs/testing/CI_WORKFLOWS.md:7,2036; docs/testing/TESTING.md:174,331; three changed READMEs - pinned environment and historical limits preserved.**

CI_WORKFLOWS states the pinned image and CPython-wheel installation reason. TESTING updates the current worker label and links the workflow policy. The firmware harness and both physical-suite READMEs name the current image. Physical deadlines remain explicitly pending completed hosted physical evidence.

Historical wording was checked against actual logs: job 113696564335 reports `Image: ubuntu-24.04`; job 96546610543 reports that image and `yosys 0.33-5build2`. These are historical receipts, not current-head execution.

Added source comments describe behavior/reason and retain the applicable issue reference. No added lane, review-round, reviewer or issue-comment identity was found. Nearby old review references are unchanged context. The documentation gate passes.

## Reviewer-owned ledger

CLEAN means no open source-review finding under the lens. It does not substitute for outstanding hosted/candidate acceptance.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #784 step 2; source-audit.log; four workflows/templates; act_ci.py:92,2062,4828; generator census | R706-1 | 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 |
| RTL | CLEAN | full source.diff; act_ci.py:5987-6015; checkout-verification.log | R706-1 | 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 |
| Robustness | CLEAN | act_ci.py:2045,6719,6741,6809,13275; published controls and two mutation raw logs | R706-1 | 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 |
| Tests | CLEAN | focused-results.json; generator/event logs; independent drift probe; manifest-verified public runner receipts | R706-1 | 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 |
| Docs | CLEAN | CI_WORKFLOWS.md:7,2036; TESTING.md:174,331; changed READMEs; documentation-review.log; historical excerpts | R706-1 | 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 |

## Hosted observation: acceptance pending

Read-only observation around 2026-10-26 07:40-07:41 UTC: 42 emitted checks, all associated with the reviewed head: **7 successful, 20 in progress, 14 queued, 1 skipped**. This is a snapshot, not the final expanded job population.

Runs: [docs 40286249788](https://github.com/kebag-logic/milan-fpga/actions/runs/40286249788), [elaborate 40286249845](https://github.com/kebag-logic/milan-fpga/actions/runs/40286249845), [rtl-fast 40286249749](https://github.com/kebag-logic/milan-fpga/actions/runs/40286249749), [rtl-full 40286249776](https://github.com/kebag-logic/milan-fpga/actions/runs/40286249776).

All seven successful jobs' actual setup logs were read and report `Image: ubuntu-24.04`: wire-accountability, docs-check-no-git, changes, bdd-conformance, firmware-aecp-mutants, full-ci-gate and verilator-lint. Selected raw setup/provenance lines are retained in `hosted/*-excerpt.log`. Checkout logs identify GitHub's synthetic merge `b0840c8a5fffd08cc822a6183ac38d7bf74837cc`, merging this head into `a8594bb9`; this is not a manager candidate-bank receipt.

The running docs-gates-2 log endpoint returned 404, retained as a receipt. Its runner contract step had not executed in the earlier snapshot. No image or passing execution is inferred for unfinished jobs.

Only wire-accountability and docs-check-no-git of the seven required contexts had completed successfully. The other five were not yet emitted. Physical gPTP was skipped as designed for a PR; that context proves no execution.

**No all-jobs image proof or all-required-checks-green conclusion is claimed.** Hosted/act acceptance remains with the manager.

## Real limits and pending manager duties

- The brief requested runner reruns but explicitly prohibited host runner/self-test execution, Docker and act. The prohibition was honored. Clarification was requested; no exception was received. No runner code was imported or executed. Published receipts supply that portion of the review.
- The upstream R697 wording comment was fetched after the independent diff pass but before the first recorded source verdict/ledger, earlier than the requested order for other reviewer reports. No current-PR peer report was read. The prescribed sentence was independently compared afterward.
- No manager source bank ran at this head, and none is claimed. Source-head runner evidence is the author's published evidence.
- The manager must complete hosted/act acceptance, obtain the remaining required-context results and job setup logs, and distinguish executed jobs from skipped contexts.
- At the merge turn, the manager must validate the current-dev candidate with builder and native banks and publish receipts. Source base and stated live dev are both `a8594bb95631fa5c49d18fa0bbc9530e31ad59aa`; that does not waive candidate validation.
- Merge still needs the other independent review, completed gates, explicit authorization and subsequent containment.
- Keep #784 open until the post-merge dev push proves the image and green required checks; then restore all seven required checks and complete the issue.
- Physical calibration was **NOT RUN**. Field skips and software receipts are not hardware proof.

## Checkout and packet integrity

`checkout-verification.log` proves raw blob bytes, executable/symlink modes and stage-0 index entries against HEAD, with replacement objects disabled: 1,442 superproject files, 704 processor files, 107 gPTP files and 214 AXI dependency files. All six superproject gitlinks match. The three required initialized submodules match their pins and registered superproject. The other three remain unchanged and uninitialized; they were unused. Status is clean.

No source fix, commit, push, GitHub write, merge, privileged action or hardware action occurred. Disposable material is confined to `scratch/` and excluded from publication. Portable scripts, raw receipts and selected public-log excerpts are listed in `MANIFEST.sha256`.

R706-1 FINISHED

[R637] NEGATIVE - exact head f643377f15c0d939d875ae5698672f1b0a99a644

R637-1 external independent review of issue #744 / PR #745. All five lenses applied; two open MAJOR findings prevent approval. Reviewed tree: `3e77395e26cb6216d0908fbec71cec87421d826f`; source base: `84f9e3001b7d9b77835c4a9a599dbe6230a8031b`. This is source-head review, not validation of a merge into live dev `9ef717727e6fdac11ee7f01672fefae948452343`.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue's frozen public scope, linked authorities, the complete eight-file diff and three-commit history, then public executable evidence. No private author material, management checkout, or other reviewer report informed this independent verdict and ledger.

Authorities: [assignment](https://github.com/kebag-logic/milan-fpga/issues/744#issuecomment-6197842304), [clarification](https://github.com/kebag-logic/milan-fpga/issues/744#issuecomment-6197855588), REQUIREMENTS.md:307 (REQ-VER-01 through REQ-VER-06), CONTRIBUTING.md sections 2/3/6, and docs/testing/CI_WORKFLOWS.md:1675, :2026, :2397, :2480. The [Linux cgroup v2 interface](https://docs.kernel.org/admin-guide/cgroup-v2.html) corroborates hierarchical memory events and the local-events mount exception.

## Findings

### R637-1-F1: MAJOR - Conformance, Robustness, Tests, Docs

Artifacts: `scripts/ci_runtime_workflows.py:64`, emitted at `.github/workflows/rtl-fast.yml:443`; `scripts/ci_gate_workflows_selftest.py:283`; `docs/testing/CI_WORKFLOWS.md:2037`.

The census budget ignores an existing unreadable limit. The `if [ -r "$cgroup/memory.max" ]` branch treats denied read access as though no controller existed. The step succeeds and exports a pool derived from host RAM without proving the enforced job or ancestor limit.

Authority/evidence: issue item 2 requires a memory-bounded pool; the CI policy explicitly says an unreadable limit fails the step. `probe_census.py` executes the exact emitted shell, changing only fixture paths and nproc. With 16 CPUs and 61 GiB MemTotal, a readable 8 GiB limit selects 4. Changing that fixture to mode 000 selects 16, rc 0. An unreadable 4 GiB ancestor also selects 16, rc 0. Both should refuse. Readable garbage correctly refuses; a genuinely absent controller retains the existing fallback. See `probe-census.log` and `.rc`.

Impact: denied access restores the 16-worker configuration that the published 8 GiB negative control demonstrates can exhaust memory. This is a fault-path defect, not evidence that ordinary readable cgroups select the wrong count. The committed case named "an unreadable limit" supplies readable `garbage`, so all eleven current cases pass without exercising permission denial. The local generator self-test passed despite this defect.

Required outcome: distinguish an absent controller from a present but unreadable limit; refuse unprovable leaf/ancestor accounting before exporting CI_CENSUS_JOBS. Add executable permission-denial controls and keep generator, workflow, contract and documentation consistent. Do not weaken the refusal contract to describe current behavior.

Verification: unreadable leaf and ancestor return nonzero without an export; readable 8 GiB remains 4, a readable 4 GiB ancestor 2, and the supported no-controller case retains its intended behavior. Re-run generator controls and generated-file check. The reproduction script asserts the defect at this head; invert those expectations for regression verification after fixing it.

### R637-1-F2: MAJOR - Conformance, Tests, Docs

Artifacts: `scripts/act_ci.py:4618`, `scripts/ci_runtime_workflows.py:58`, `.github/workflows/rtl-fast.yml:437`, `scripts/ci_gate_workflows_selftest.py:249`, `docs/testing/CI_WORKFLOWS.md:2039`, and [hosted docs job 116583405450](https://github.com/kebag-logic/milan-fpga/actions/runs/38781738587/job/116583405450).

The required bare-metal-only gate fails on 21 references introduced by this change. New host pseudo-filesystem paths and associated prose/fixtures are not integrated with the gate's narrowly scoped host-tooling allowances.

Authority/evidence: REQ-VER-04 requires this gate green with zero policy findings. `scripts/check_baremetal_only.py:315` and :644 define exact host-runtime masks and their application. The hosted job executes `python3 scripts/check_baremetal_only.py --check` and exits 1 with 21 findings. `probe_policy.py` invokes the unchanged content scanner on the eight changed files: zero findings on source-base contents, 21 at the reviewed head, matching the hosted list. See `probe-policy.log` and `hosted-policy-failure.log`.

Impact: docs-check fails and remaining hosted validation is cancelled. The required verification bar is not satisfied. This is policy integration for legitimate host tooling, not evidence of a new target operating system. The author's final-gates.tsv omits this required check. The checked PR-body assertion "Required local verification bar passes" cannot serve as proof of an all-green bar.

Required outcome: make intended host accounting paths and fixtures pass the existing narrow host-tooling policy while preserving rejection of unrelated product/runtime references; adjust prose where appropriate and correct the validation claim. Do not remove or broadly bypass the gate. Regenerate the workflow from its source.

Verification: the corrected exact head passes `check_baremetal_only.py --check` and `--selftest`, including narrow-allowance negative controls, plus generated-workflow checks. Publish replacement required local/hosted evidence. Even prose edits here affect an executable verdict, so this is not RESIDUE.

## Independent lens results

Conformance: `scripts/act_ci.py:4621`/:5945 read hierarchical events, require oom/oom_kill/max, reject a local-events mount, and read memory.peak before teardown. The normal path satisfies item 1. The formula matches `max(1,min(nproc,floor(2*M/(3*1234825216))))` for readable inputs. F1 violates its failure-path contract; F2 violates REQ-VER-04. Item 2's concurrent replay remains a separate manager receipt.

[R637] PASS RTL - complete `84f9e300..f643377f` eight-file diff, `sw/mailbox/publication_census.py:598`, `sw/mailbox/census_selftest.py:182`, and unchanged processor/axis/stack gitlinks - no RTL, firmware interface, clock/reset, CDC, width, FSM, datapath configuration, or census rule changes. The same shape and mutation inventories remain. The full act_ci.py diff was audited as a trust boundary: no new candidate import, execution route, credential forwarding, mount, or privilege grant. Cleanup ownership remains intact. This is scoped review coverage, not new RTL execution or hardware proof.

Robustness: `scripts/act_ci.py:4621`, :4663, :5945, :14734, :14813 cover hierarchical/local counts, oom-only, kill-only, malformed/missing fields, missing/local mounts, unreadable peak, clean high-max counts, failing jobs and body exceptions. Slot accounting reaches workflow validation through a callback; invalid accounting is recorded before Refusal, and main maps Refusal to rc 2. Exceptional bodies preserve their exception and print accounting; they do not acquire successful-run evidence. Slot 0 remains outside slice OOM accounting. F1 leaves census input handling unclean.

Tests: inspected every changed self-test and public seven-mutant results. Mutants catch local-events regression, either refusal removed, oom-only handling lost, locality guard removed, exceptional report removed, and refusal before manifest. The public allocation control proves the hierarchical/local distinction; its reader-harness rc 0 is not a live replay rc 2 receipt. Source wiring and planted validation controls exercise that refusal path. Eleven generator cases execute emitted shell and check sole job ownership/order. Local generator check and self-test pass. F1 exposes the missing permission-denial case; F2 exposes omitted required validation. No host runner/self-test was executed in this review.

Docs: CI_WORKFLOWS.md and MAILBOX_SPLIT.md reflect the measured constant, native/concurrent distinction, OOM invalidation, slot-0 limit and remeasurement obligation. F1 contradicts the unreadable-limit claim; F2 contradicts the policy/validation bar. No prose-only RESIDUE finding is recorded.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #744 scope; REQUIREMENTS.md:307; act_ci.py:4621/:5945; ci_runtime_workflows.py:53; public receipts; hosted gate failure | R637-1, applied but not banked | f643377f15c0d939d875ae5698672f1b0a99a644 |
| RTL | CLEAN | Full eight-file diff; publication_census.py:598; census_selftest.py:182; unchanged RTL/configuration/gitlinks; full act_ci.py diff | R637-1 | f643377f15c0d939d875ae5698672f1b0a99a644 |
| Robustness | UNCLEAN (F1) | act_ci.py:4621/:4663/:5945/:14734/:14813; ci_runtime_workflows.py:53; probe-census.log | R637-1, applied but not banked | f643377f15c0d939d875ae5698672f1b0a99a644 |
| Tests | UNCLEAN (F1, F2) | act_ci.py:6991/:14734; ci_gate_workflows_selftest.py:235; public mutants.txt/real-control.txt; local generator/probe receipts | R637-1, applied but not banked | f643377f15c0d939d875ae5698672f1b0a99a644 |
| Docs | UNCLEAN (F1, F2) | CI_WORKFLOWS.md:2026/:2397/:2480; MAILBOX_SPLIT.md:1030; PR body; public final-gates.tsv | R637-1, applied but not banked | f643377f15c0d939d875ae5698672f1b0a99a644 |

## Evidence and limits

The [public source evidence](https://github.com/kebag-logic/milan-fpga/tree/36ab73f9de00f81e3449633cbbfbde812c94c61f/review-evidence/744-r1/author/evidence) was examined independently. Downloaded bytes are bound to Git blob identities and the published SHA-256 manifest. No author handoff or private scratchpad was read.

- sv2v-rss.log: six elaboration peaks plus a version invocation; maximum 1205884 KiB = 1234825216 bytes. yosys-rss.log maximum 386824 KiB.
- census-capped-jobs4.txt: budget 4/16 within 8589934592 bytes; 234 checks, zero failures, 0/120 failing arms, 0/31 unproved rules; peak 5806784512 bytes, all memory events zero. The 591-second native run is not a four-job replay.
- census-capped-jobs16.txt: 113/120 failing arms, 209 oom_kill, 2298 oom, peak at the 8 GiB cap, rc 1. This supports the failure mode without repeating a heavy bank.
- real-control.txt: 400 MiB allocation in a 200 MiB scope below 36G; allocation rc 137; hierarchical oom=1/oom_kill=1 and clean local counts. The copied runner fixture has max=37, while this published control has max=35; decisive OOM counts agree. These are not claimed as identical independent runs.
- final-gates.tsv: 29 reported rc-0 commands, including runner, workflow/event, scheduling/evidence and quality checks. Public author commentary reports 610/608 direct/isolated runner controls and 2187 contract items/5218 CI-event arms. These are author source receipts, not a manager source bank or full-bank proof.

Independently measured re-pin digest: `scripts/act_ci.py` SHA-256 `9ce3a6604486c99209333430b09f8892bc2a5c0f5ed87b052a2ddc85577ffee8`. This identifies the audited runner diff; a future changed file needs its own review/digest.

Hosted API evidence records four cancelled workflows at this head. The census budget step succeeded; census execution was skipped after cancellation during dependency setup. Physical gPTP was skipped. Failed/cancelled aggregates and skipped execution provide no acceptance pass. The source-level policy failure above was independently reproduced rather than inferred from aggregate status.

No full parent/processor/gPTP/Yosys/builder bank, privileged action, shared install, hardware action, or host runner/self-test was performed. Small probes ran unprivileged in foreground; scratch trees stayed under the packet scratch directory. An accidental full policy-scanner invocation during report assembly was interrupted; it supplies no gate result. The focused source comparison completed independently. Final verification proves every tracked blob, mode, and index entry equals the exact head; no source changes remain.

Physical calibration NOT RUN; field skips are not hardware proof. No manager source bank at this head is claimed. At merge time the manager must build and validate the current-dev candidate, including builder/native banks, and link receipts. Source evidence does not substitute for candidate evidence.

## Pending manager duties

Resolve both findings and obtain re-review at the corrected head; publish/accept the complete four-job replay receipt for item 2; resolve hosted acceptance; re-pin the reviewed runner digest as appropriate. Two independent positives, current clean lens coverage, final candidate validation, authorized merge, post-merge containment and issue closure/Done remain required. No GitHub writes or merge were performed by this reviewer.

After writing the independent verdict and ledger, the issue comments, PR comments, formal reviews, and inline review comments were queried again. No prior reviewer findings, formal reviews, or inline review comments were present. The newly published [manager finding M1](https://github.com/kebag-logic/milan-fpga/pull/745#issuecomment-6199082046) independently reports the same 21 policy failures in the manager's cancelled replay. M1 is RETAINED, unresolved at this head, as R637-1-F2. Its public scope decision requires exact spelling/file/content-bound host-tooling declarations, following the existing declaration approach, with unnecessary prose reworded. Apply that decision when fixing F2. It confirms a failed replay, not the complete passing four-job item-2 receipt. See prior-findings-audit.json and manager-findings.json.

`checkout-integrity.log` verifies all 1370 superproject tracked blobs and index entries, all six gitlinks, and exact tracked bytes/modes/index in five initialized dependencies (protocol processor, gPTP processor, axis, TSN stack and lwSRP). The inactive external dependency remains uninitialized. No restoration was required. Runner SHA-256 matches the supplied re-pin identity.

Local completed commands and receipts:

| Command | Result | Receipt |
|---|---|---|
| `python3 probe_census.py <checkout> --scratch <packet>/scratch` | rc 0; defect reproduced, not a clean budget verdict | probe-census.log / .rc |
| `python3 probe_policy.py <checkout> --scratch <packet>/scratch` | rc 0; 0 base versus 21 head findings reproduced | probe-policy.log / .rc |
| `python3 scripts/ci_gate_workflows.py --check` | rc 0; committed workflow matches generation | generator-check.log / .rc |
| `python3 scripts/ci_gate_workflows_selftest.py` | rc 0; eleven current census cases and surrounding generator controls pass | generator-selftest.log / .rc |
| `python3 verify_checkout.py <checkout>` | rc 0; exact tracked bytes/modes/index/pins | checkout-integrity.log / .rc |

For generator controls, set `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR=<packet>/scratch` from the checkout. The generator controls and generated-file check ran concurrently, with foreground command ownership and separate receipts. Neither compiler builds nor heavy banks were needed. Portable probes execute no runner code. Public receipt hashes, Git blob identities, and equality of the published budget shell with the generated shell are recorded in public-evidence-audit.json. MANIFEST.sha256 enumerates the publishable packet; scratch is excluded.

R637-1 FINISHED

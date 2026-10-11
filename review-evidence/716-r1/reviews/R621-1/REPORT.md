[R621] POSITIVE - exact head f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48

External independent review, round R621-1, issue #716 / PR #724.
Reviewed tree: `6fab4d33da2dfeb5c349911088b17d40e23b81f3`.
Source comparison base: `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`.

All five lenses were applied independently. No BLOCKER, MAJOR, MINOR,
RESIDUE, or SUGGESTION was found in the reviewed change.
This verdict covers the source change. It does not authorize merging.

The public task was reconstructed from AGENTS.md, CONTRIBUTING.md,
docs/README.md, the issue and its assignment, REQ-VER-04, the CI policy,
firmware harness contracts, the complete five-file diff and both commits,
then public execution evidence. Neither commit has a body or trailers;
both subjects carry a `ci:` prefix.

Authorities and evidence:

- [Frozen issue acceptance](https://github.com/kebag-logic/milan-fpga/issues/716).
- [Public assignment and scope](https://github.com/kebag-logic/milan-fpga/issues/716#issuecomment-6107547907).
- [Author source-head receipts](https://github.com/kebag-logic/milan-fpga/tree/3dff3266c96285ad82226beb84721b2622f3ac57/review-evidence/716-r1).
- [Manager's ten-attempt table](https://github.com/kebag-logic/milan-fpga/pull/724#issuecomment-6113578810).
- [Public start of this round](https://github.com/kebag-logic/milan-fpga/pull/724#issuecomment-6113601403).

Acceptance results:

| Requirement | Independent result |
|---|---|
| Identify the original cost | All 223 published step records across 17 historical jobs match Actions API timestamps and durations. Total durations span 1662-2450 seconds. At the assigned-base job, control takes 1882 seconds, saved-state 103, and coverage 255. The published timestamped reporting windows identify control mutations and the two SRP campaigns as the dominant phases. Buffered logs do not establish individual binary durations. |
| Ten consecutive hosted attempts, each job at most 70% | Run 38162821680 attempts 1-10 all identify the exact source head. All 40 firmware jobs executed successfully. Every timestamp-derived duration matches the manager's table. Maxima: unit 703, control mutations 841, AECP mutations 260, SRP mutations 625 seconds. Worst usage is 841/2700 = 31.148148%, below 1890 seconds. |
| Pre-review prediction | Published source-head command receipts all return zero. Their arithmetic reproduces conservative predictions 631/879/256/608 seconds, each below 1620. Four-CPU affinity is author-reported evidence; this round does not claim a new calibration. |
| Preserve commands and conditions | The census's recorded baseline equals the actual base workflow. Its 19 original script lines and 55 current lines yield identical command/condition sets after removing only the four terminal shard suffixes. Repeated setup accounts for extra lines. Complete step contracts also pin checkout and the SDK cache. |
| Exclusive, exhaustive suite assignment | Independently intercepted the actual base `main()`, current default `main()`, and each current shard `main()`. All 844 identities match in order; sizes are 59/472/75/238. The ordinary invocation without self-test also matches. Production ownership checking rejects independently planted omission and duplication. Repository controls discover a future suite and reject nine invalid/narrowing combinations. |
| Coverage preservation | The coverage function's syntax tree is identical. Coverage implementation, exclusions, ratchet, arm implementations and saved-state directory are byte-unchanged. Coverage remains unsplit. The published comparison contains 30 equal file rows; no local coverage recompilation is claimed. All 28 coverage self-test cases pass locally. |
| Required layout, budget and fresh builds | Four 45-minute firmware jobs retain the relevance guard. The aggregate requires all four. Actual aggregate shell tests reject failure, cancellation, empty and unknown results for every job. CI contracts reject removed dependencies, disabled jobs, raised timeouts and build-output cache paths. CI_WORKFLOWS.md records each 45-minute, 1890-second and 1620-second budget. Only the authenticated SDK is persisted. |

[R621] PASS Conformance - `.github/workflows/rtl-fast.yml:246`,
`scripts/ci_events.py:3561`, `receipts/hosted-attempt-01.json` through
`receipts/hosted-attempt-10.json` - frozen acceptance, command/guard equality,
four required jobs, and the ten-attempt bound verified.

[R621] PASS RTL - complete diff from `ac2c5e77` to the exact head,
`sw/firmware/ctrl/test/test_ctrl_firmware.py:141`,
`sw/firmware/ctrl/test/test_ctrl_firmware.py:201`,
`docs/overview/ARCHITECTURE.md:3`, `receipts/tree-integrity.log` - no RTL,
firmware behavior, interface, clock/reset, CDC, configuration or gitlink change.
The refactor preserves the existing arm calls, campaign tables, default order,
and unsplit coverage population. No new hardware timing claim is made.

[R621] PASS Robustness -
`sw/firmware/ctrl/test/test_ctrl_firmware.py:127`,
`sw/firmware/ctrl/test/test_ctrl_firmware.py:162`,
`sw/firmware/ctrl/test/test_ctrl_firmware.py:253`,
`.github/workflows/rtl-fast.yml:399`, `receipts/focused-review.log` - malformed
and incompatible shard selections refuse; every phase propagates failure;
an SRP refusal restores the full mutable table; the aggregate fails on failed,
cancelled or absent results. The documented docs-only skip remains accepted.

[R621] PASS Tests -
`sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:29`,
`sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:102`,
`sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:131`,
`scripts/ci_events.py:7946`, `receipts/focused-review.log` - real default/shard
dispatch compared against the actual base; missing and duplicate ownership
mutants rejected; future-suite injection detected; actual aggregate tested
in 24 cases; 16 independent workflow mutations rejected. The CI self-test
passes all 2672 arms over 1944 contract items.

[R621] PASS Docs - `docs/testing/CI_WORKFLOWS.md:62`,
`docs/testing/CI_WORKFLOWS.md:2348`, PR #724 body and public source receipts,
`receipts/receipt-audit.log` - job ownership, timing ceilings, reproduction
commands, unsplit coverage and evidence limits agree with the implementation.
Documentation, style, Python idiom and added-line wording checks pass.

Reviewer-owned completion ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #716 assignment; rtl-fast.yml:246; ci_events.py:3561; ten hosted attempt receipts | R621-1 | f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48 |
| RTL | CLEAN | Complete five-file diff; test_ctrl_firmware.py:141,201; ARCHITECTURE.md:3; tree-integrity.log | R621-1 | f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48 |
| Robustness | CLEAN | test_ctrl_firmware.py:127,162,253; rtl-fast.yml:399; focused-review.log | R621-1 | f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48 |
| Tests | CLEAN | test_ctrl_firmware_shards.py:29,102,131; ci_events.py:7946; focused-review.log; ci-events-selftest.log | R621-1 | f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48 |
| Docs | CLEAN | CI_WORKFLOWS.md:62,2348; public PR/evidence; receipt-audit.log; docs-check.log; em-dash-pinned.log | R621-1 | f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48 |

This independent verdict and ledger were written before checking prior public
review findings. That subsequent check found no reviewer finding or verdict
on either issue/PR comment stream, and zero PR reviews or inline review
comments. There are therefore no prior public findings to resolve or retain.
`receipts/prior-review-audit.json` records the queried endpoints, counts,
timestamp and the hash of the independently written report.

Reproduction and receipts:

The portable scripts in `scripts/` accept the candidate checkout where needed.
Run `public_evidence.py`, `audit_receipts.py`, `focused_review.py <checkout>`,
`run_focused_gates.py <checkout>` and `verify_tree.py <checkout>` in the foreground.
The two API scripts need read access to the public repository. The focused
gate runner uses four concurrent processes and no detached jobs. Disposable
dependencies and downloads reside only under `scratch/`.

For the Markdown check, install `tools/markdown/requirements.txt` with
`--require-hashes --target <packet>/scratch/markdown-deps`, then set
`PYTHONPATH=<packet>/scratch/markdown-deps` when invoking the gate runner.

The first added-line wording check refused missing pinned Markdown dependencies
(exit 2). Installing the repository's hash-locked dependencies into the packet's
scratch directory and rerunning passed: zero findings, 339/339 controls.
Both receipts are retained, so the initial setup refusal is not reported green.

No tracked source bytes were edited. In-memory probes restored their patches.
The final integrity check hashes every tracked blob directly and checks kinds,
executable modes and index entries against Git trees with replacement objects
disabled. It proves 1273 superproject blobs and 940 blobs in the four required
submodules. The optional external submodule remains uninitialised.

Limits and pending manager duties:

- Source execution evidence is the author's published gate receipts. There is
  no manager source bank at this head, and none is inferred here.
- The reviewer reran focused checks and fault probes, not the full firmware
  campaigns, parent/processor banks, portability banks or builder banks.
  Intercepted inventories prove scheduling; they do not execute firmware tests.
- Exact-head hosted check records show successful fast, documentation,
  elaboration and exhaustive aggregates, with their worker contexts successful.
  The physical gPTP context is skipped. Physical calibration is NOT RUN;
  field skips and desk checks provide no hardware proof. Hosted/local-replica
  acceptance remains the manager's responsibility.
- Historical reporting windows and author four-CPU measurements have the
  limitations stated above. Ten hosted attempts establish the assigned sample
  bound, not a guarantee against future runner variance or dependency changes.
- The final current-dev merge candidate remains distinct from this source head.
  At assignment, live dev was `cfadd767a7ad47aaee68de655e1066cc000fb8a0`.
  The manager must construct the candidate against live dev at the merge turn,
  run its required builder and native banks, and link those receipts on the PR.
- The manager still owns reconciliation of both independent reviews, required
  evidence and completion gates, explicit merge authorization, post-merge
  containment, and closing/moving the issue to Done. No GitHub write or merge
  was performed by this review.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable.
Nothing under scratch/ is publishable.

R621-1 FINISHED

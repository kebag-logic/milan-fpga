[R637] POSITIVE - exact head 43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e

R637-2 external independent delta review of issue #744 / PR #745.
Tree: `9c0a8e43b66f420cd9a581460a81f62184bb05dc`.

All five source-review lenses are CLEAN. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION was found. The named prior findings are resolved at their causes. This is a positive source-review verdict, not completion of the manager-owned replay, hosted acceptance, candidate validation or merge duties.

The complete source diff from `84f9e3001b7d9b77835c4a9a599dbe6230a8031b` was reconstructed; the substantive re-review covers the four commits after `f643377f15c0d939d875ae5698672f1b0a99a644`. The unchanged portions retain their earlier scope and limits. No private author material or other checkout was used. Prior public finding sections were reconciled after the independent code pass; no current-round peer verdict was used.

## Authority and evidence

The contract is AGENTS.md and CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md sections 1 and 8 (particularly REQ-VER-04), issue #744 and its frozen assignment/clarification/round-two decision, and the relevant CI policy and generator interfaces.

Public scope: [round-two assignment](https://github.com/kebag-logic/milan-fpga/issues/744#issuecomment-6199231775), [M1 decision](https://github.com/kebag-logic/milan-fpga/pull/745#issuecomment-6199082046). Execution evidence: [published packet at 67e05179](https://github.com/kebag-logic/milan-fpga/tree/67e05179f28bc777a18f136cfdb759e2adf9750c/review-evidence/744-r1), `author-r2/evidence`, and the public REVIEW READY comment.

`public-audit.log` verifies all 39 selected author execution receipts against the publication manifest SHA-256 values. These are public execution artifacts, not the author handoff. GitHub reports that publication commit as **unsigned**. Consequently this review verifies published content hashes, not a cryptographic signature or signer. No separate signed packet was available at the supplied location; `public/commit-verification.json` records that limit.

`receipt-audit.log` checks the exact-head marker, clean status before/after, 47 of 47 docs-gate commands returning zero, 16 executed census-budget cases without skips, the bare-metal results and measurement totals. The command inventory was compared with the generated docs workflow. Local package setup substitutes for hosted installation; hosted receipt aggregation is separate. The source-head receipts are the author's. No manager source bank is claimed.

## Prior findings: resolved

**M1 / R636-1 BLOCKER / R637-1-F2 MAJOR: RESOLVED.** Attributable lenses: Conformance, RTL, Tests, Docs. Artifacts: scripts/check_baremetal_only.py:359-409,1274-1312, the four declared source/workflow files, and docs/testing/CI_WORKFLOWS.md:2357-2367.

Authority: REQ-VER-04 and M1 require exact file/content-bound host allowances. There are exactly 14 whole-line declarations: five runner lines and three each in the generator, emitted workflow and generator self-test. Every declaration occurs exactly once in its current source file. Anchored prefix lookbehind and suffix lookahead surround only each matched path token; scanning continues for other runtime surfaces. Prose is reworded where no path declaration is needed.

The earlier impact was 21 gate failures and cancelled validation. The required outcome is met: published 16.log records zero findings across 1344 files and PASS for 790 arms. The 90 new arms comprise 20 allowed/unrelated-reference cases across five files and 70 wrong-file/product-file/prefix/suffix/changed-path cases for the 14 declarations. All six mask mutants are caught. Dropping a declaration is caught by the actual-tree check; its declaration-derived self-test alone shrinks and passes, so that mutant is not misreported as killed by the self-test. The full 47-command receipt replaces the omitted-gate evidence, and the PR body explicitly retracts the earlier all-green claim.

Hosted confirmation: [docs-gates-0 job 116625786754](https://github.com/kebag-logic/milan-fpga/actions/runs/38794076964/job/116625786754) completed successfully for this PR head. Its Bare-metal scope gate executed successfully, rather than being skipped. The whole hosted workflow was still in progress at the snapshot.

**R637-1-F1 MAJOR: RESOLVED.** Attributable lenses: Conformance, Robustness, Tests, Docs. Artifacts: scripts/ci_runtime_workflows.py:55-91, .github/workflows/rtl-fast.yml:433-464, scripts/ci_gate_workflows_selftest.py:235-339, docs/testing/CI_WORKFLOWS.md:2026-2050.

Authority: issue item 2 and the explicit unreadable-limit refusal contract. The old readability predicate silently treated denial as absence and could restore sixteen workers. The new existence predicate attempts the read and refuses failure; the ancestor walk also refuses an unsearchable cgroup. All checks precede the environment export. A genuinely absent controller retains the fallback.

Verification: the public controls execute mode-000 leaf, ancestor-file and ancestor-directory denials, plus both directory-as-limit controls. Root skips are explicit and only affect the three permission cases. The old readability predicate and removed searchability guard are caught by mutations. The surviving cat-status mutant still encounters the empty/non-numeric refusal, so it is not evidence of an accepted unreadable limit.

The independent probe_delta.py executes the current emitted shell with fixture paths and a fixed CPU count. Readable 8 GiB selects 4; a readable 4 GiB ancestor selects 2; no controller selects 16. All five denial/directory cases return 1 with no environment file. None was skipped. The published exact-head shell equals the current generator output byte-for-byte. Template and scripts/ci_events.py:2476 still require the census-specific worker variable; published generator/contract receipts pass.

**R636-2 RESIDUE: RESOLVED.** Lens: Docs. Artifacts: docs/testing/CI_WORKFLOWS.md:2016-2017,2517-2523 and the PR limitations bullet. The requested texts now say the accounting records whether an OOM invalidated the slot and that manifest completeness does not read slot memory events. This matches scripts/ci_manifest.py:176-197 and scripts/ci_local_manifest.py:132; completeness also depends on provenance and cannot be inferred from a clean slot. Verification was direct text and implementation comparison.

**R636-3 SUGGESTION: RESOLVED.** Lenses: Tests, Conformance (the round-two assignment made the update required). Artifacts: scripts/ci_runtime_workflows.py:47-51, workflow arithmetic, docs/testing/CI_WORKFLOWS.md:2416-2434, and published RSS receipts. There are 133 timed sv2v runs, maximum 1212036 KiB, and 141 timed Yosys runs, maximum 380492 KiB. The earlier capped self-test receipt records the larger 1213100 KiB. The constant is exactly 1213100 * 1024 = 1242214400 bytes. The four/two-worker boundary checks and real-cap receipts agree. This closes the measurement gap without asserting a permanent bound for future datapaths.

**R636-4 SUGGESTION: RESOLVED.** Lenses: Docs, Conformance (required by the round-two assignment). Artifacts: scripts/act_ci.py:4608-4612,7021-7028 and CI policy at :2517-2523. The evidence field is oom_free, and tests assert the renamed field for both refused and clean accounting. Printed "valid build: False" remains as item 1 requires. Exact-head published direct/isolated runner self-tests pass. The earlier native OOM receipt still spells valid_build; it proves the unchanged hierarchical reader/refusal behavior, not the new field name.

## Reviewer-owned lens ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #744 frozen scope; REQUIREMENTS.md:307-316; scripts/ci_runtime_workflows.py:47-91; scripts/check_baremetal_only.py:359-409; scripts/act_ci.py:4608; exact-head author gate receipts | R637-2 | 43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e |
| RTL | CLEAN | source.diff and delta.diff: no HDL, firmware, register/interface or gitlink changes; host/product boundary checked through exact declarations; publication worker inputs unchanged | R637-2 | 43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e |
| Robustness | CLEAN | scripts/ci_runtime_workflows.py:68-85; scripts/ci_gate_workflows_selftest.py:235-339; permission/ancestor/absence probes in probe-delta.log; changed accounting serialization | R637-2 | 43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e |
| Tests | CLEAN | scripts/check_baremetal_only.py:1274-1312; six published mask mutants; permission mutants and 16 controls; 47-command docs receipts; runner field assertions; independent shell probes | R637-2 | 43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e |
| Docs | CLEAN | docs/testing/CI_WORKFLOWS.md:2016-2050,2357-2367,2416-2434,2517-2535; docs/design/MAILBOX_SPLIT.md:1031-1036 unchanged in delta; corrected PR verification claim; source-comment delta audit | R637-2 | 43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e |

The comment-rule audit found no new prohibited lane name, review-round/reviewer ID or issue-comment ID in the four-commit delta. The older template comment identifier predates this delta and is not reopened here; existing residue remains under #746.

## Verification limits and pending manager duties

- New runner SHA-256: b8a786cec30be9eff9f2e72c6b59e21c06d27e1f36e055a7929c3cc3b59e3ba8, 698735 bytes. The manager must re-pin this value; no re-pin was performed by this reviewer.
- The latest retrieved PR comments contained **no published exact-head four-job replay receipt**, despite the assignment describing it as posted. public-snapshot.json records the comment IDs and hosted state. The PR body also says that receipt is outstanding. Item 2's concurrent replay acceptance therefore remains unproved here and belongs to the manager. The native capped census is not substituted for it. Publish/link the receipt before declaring acceptance complete.
- Hosted docs-gates-0, docs-gates-2, docs-check-no-git and wire-accountability had executed successfully; docs-gates-1 and other workflows were still pending/in progress. No complete hosted acceptance, successful exhaustive aggregate or signed complete CI manifest is inferred. The manager owns final hosted/replay acceptance.
- The author receipts prove the source-head gates described above. No manager source bank ran at this head. The final merge candidate is distinct: source base 84f9e3001b7d9b77835c4a9a599dbe6230a8031b, supplied live dev 9ef717727e6fdac11ee7f01672fefae948452343. The manager must construct the candidate from the current dev tip at the merge turn, run its builder/native banks and required gates, and publish receipts.
- Builder calibration is explicitly NOT RUN. The no-git docs check skips inventory parity by design. Field skips and calibration absence are not hardware proof. No hardware or physical calibration was performed.
- The independent work used receipt verification and eight focused shell cases. No full banks, host runner execution/self-test, containers, privilege, shared installs, source edits, commits, pushes or GitHub writes occurred. No sub-agents were used.
- Final byte/mode/index verification passed for 1370 parent tracked blobs and all tracked blobs in the four required submodules (214, 562, 107 and 98). Their HEADs equal the recorded gitlinks. checkout-integrity.json records the exact identities. No source restoration was needed because probes wrote only disposable fixtures.
- Before merge: complete the separate review/completion bar, ensure no round remains in flight, obtain maintainer authorization, validate the current-dev candidate, and perform post-merge containment and issue closure. This review authorizes none of those actions.

## Packet

MANIFEST.sha256 lists the publishable scripts and raw receipts relative to this directory. scratch/ is excluded. Reproduce the focused checks with python3 probe_delta.py <candidate-clone> and python3 verify_checkout.py <candidate-clone>; audit_public.py retrieves and hashes only public author execution receipts, and audit_receipts.py checks the retained receipts and snapshot. Public scope and prior findings remain linked above; no private material is a dependency.

R637-2 FINISHED

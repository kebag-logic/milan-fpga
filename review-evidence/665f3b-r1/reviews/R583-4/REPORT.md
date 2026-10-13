[R583] POSITIVE - exact head 6b4feeca5d2fab0ec35cf071322cc775a5b15cb5

# R583-4: external delta review of PR #736 (issue #665, F3b round 4)

Scope: the round 4 assignment (issue #665 comment 6156987825), which answers R582-3
(PR #736 comment 6156867741) and R583-3 (PR #736 comment 6156980716). The delta is
`532ab871272597d83fa08506bcb05298fbe87806..6b4feeca5d2fab0ec35cf071322cc775a5b15cb5`,
one commit. Head tree `4358f8ec29f0e104c8fe32dcd01dc719104ea44f` verified. Earlier
rounds stand for everything outside the delta.

The verdict is POSITIVE. No new finding is raised. Both round 3 findings and both
round 3 residues are resolved at this head.

## Assignment items

| Item | Result | Evidence |
|---|---|---|
| `CI_WORKFLOWS.md:179` states no count, or the right one | Met. It now opens "These pages under `docs/`". No number word or digit precedes "pages" anywhere in the paragraph (lines 179-204). | `receipts/delta.txt`; `receipts/gate_read_paragraph.txt` |
| The paragraph still lists every `GATE_READ_DOCS` page | Met. 8 linked pages under `docs/` equal the 8 entries of `scripts/ci_scope.py:69-78`, none missing, none extra, all exist. The same checker returns rc 1 on the `532ab871` page ("Seven"). | `scripts/check_gate_read_paragraph.py`; `receipts/gate_read_paragraph.txt`; `receipts/gate_read_paragraph_control_532ab871.txt` |
| `scripts/ci_events.py --check` rc 0 | Met: 2169 contract items, rc 0. | `receipts/scripts_ci_events.py_--check.txt` |
| `scripts/check_doc_style.py` rc 0 | Met: 22 current documents, rc 0. | `receipts/scripts_check_doc_style.py.txt` |
| `scripts/docs_check.py` rc 0 | Met: 0 findings across 206 md files, scrub 23/23, routing 4/4, rc 0. | `receipts/scripts_docs_check.py.txt` |
| PR body names the new head as published (R582-3-R1 / R583-3-R1) | Met. "Status": "`6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` is the published head of PR #736"; GitHub `headRefOid` is the same SHA; PR is open, not draft, base `dev`. | `receipts/pr736.json` |
| Nothing else changed | Met. `git diff --stat` is one file, 1 insertion and 1 deletion; mode 100644 unchanged; all six gitlinks unchanged (tsn-c-stack `70936b77`). The commit message is one line with no trailers. | `receipts/delta.txt`; `receipts/clone_integrity.txt` |

Additional local checks: `scripts/ci_scope.py --selftest` PASS (rc 0); the
changed page classifies as documentation only (`ci_scope.py
docs/testing/CI_WORKFLOWS.md` prints `false`); the added-line em-dash gate
against `532ab871` reports 0 findings, 339/339 arms, run with the pinned
renderer from `tools/markdown/requirements.txt` in a disposable environment. The
author's published paragraph check (`author-r4/round4/gate_read_paragraph.py` in
evidence tree `8ab95062`) returns rc 0 at this head, and all 6 planted controls
are refused.

## Hosted checks at the exact head (read only)

Snapshot taken 2026-10-13T23:33:27Z (`receipts/hosted_check_runs_6b4feeca.tsv`,
`receipts/hosted_workflow_runs.tsv`, `receipts/hosted_rtl_fast_docs_jobs.tsv`).
Every listed job has `head_sha` `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5`.

- `docs` run 38482104571: completed success. `docs-check` (job 115586874121)
  executed all 55 steps with success and none skipped
  (`receipts/hosted_docs_check_steps.txt`). `docs-check-no-git` and
  `wire-accountability` also succeeded.
- `rtl-fast` run 38482104542: completed success. The `rtl-fast` aggregate
  succeeded, as did `changes`, `bdd-conformance`, `firmware-unit`,
  `firmware-boundary`, `firmware-verilator`, the three firmware mutant jobs,
  `verilator-lint`, `yosys-elaboration` and `publication-census`. The only
  skipped steps are four "build from source on cache miss" steps
  (`receipts/hosted_skipped_steps.txt`).
- `rtl-full` run 38482104553: Yosys shards 0-3 succeeded. Verilator shards 0-4
  were still in progress at the snapshot. `full-ci-gate` succeeded.
  "Physical gPTP (nightly and manual)" was skipped, which is not hardware proof.
- `elaborate` run 38482104536: in progress at the snapshot.

The manager owns hosted and replica acceptance. This review claims no result for
the in-progress contexts.

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R582-3-F1 (MINOR, Docs): "Seven pages" at `CI_WORKFLOWS.md:179` | Resolved | The count is gone and the paragraph links all 8 registered pages (above). |
| R583-3-F1 (MINOR, Docs): the same stale count | Resolved | As R582-3-F1. |
| R582-3-R1 (RESIDUE): PR body published-head sentence stale | Resolved | The body names `6b4feeca` as the published head. |
| R583-3-R1 (RESIDUE): the same, plus "Round 3 local checks pass" | Resolved | The body now reads "Round 4 local checks pass; exact-head hosted acceptance follows the manager's push", which is accurate: hosted runs at this head exist and some are still running. |
| R583-3-S1 (SUGGESTION): mechanise the page count | Moot, optional | The page states no count, so nothing remains to check. The author's packet check enforces the link-to-registration match. |
| R582-1-S2, R582-1-S3 (SUGGESTION) | Retained, optional | The delta touches no test or firmware. |
| All earlier BLOCKER, MAJOR and MINOR findings | Still resolved | The delta touches nothing they cover (`receipts/delta.txt`). |

## Lens results

- `[R583] PASS Conformance` - `docs/testing/CI_WORKFLOWS.md:179-204`, PR #736 body, hosted runs 38482104571/38482104542 - checked against round 4 items 1-3 and AGENTS.md section 7 exact-head `rtl-fast`.
- `[R583] PASS RTL` - `receipts/delta.txt` (`git diff --raw 532ab871..6b4feeca`) - no HDL, harness, synthesis, firmware or gitlink change, so nothing in RTL scope moved since R582-3/R583-3 covered it at `532ab871`. Hosted `verilator-lint`, `yosys-elaboration` and Yosys shards 0-3 succeeded at this head.
- `[R583] PASS Robustness` - `scripts/ci_scope.py:69-78` with `ci_scope.py --selftest` and the docs-only classification of the changed page - the countless sentence cannot go stale when the list changes; the paragraph checker refuses the old page (rc 1).
- `[R583] PASS Tests` - `receipts/gate_read_paragraph_control_532ab871.txt`, `receipts/author_gate_read_paragraph_at_head.txt` - the paragraph check fails on the defect it targets; the author's 6 controls are refused; no test or gate changed in the delta.
- `[R583] PASS Docs` - `docs/testing/CI_WORKFLOWS.md:179-204`, PR #736 body "Status", "Linked Issue / roles" and "Round 4" - wording, count and links agree with `GATE_READ_DOCS`; doc gates rc 0 locally and hosted; no other count of these pages exists in the tree.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round 4 items 1-3; `CI_WORKFLOWS.md:179-204`; PR body; hosted `docs` and `rtl-fast` runs | R583-4 | `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` |
| RTL | CLEAN | Raw delta (one doc file, no gitlink change); hosted lint, elaboration and Yosys shards | R583-4 (delta); R582-3/R583-3 at `532ab871`, unchanged in scope since | `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` |
| Robustness | CLEAN | `ci_scope.py:69-78`; `--selftest`; changed-page classification; old-page control | R583-4 | `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` |
| Tests | CLEAN | Reviewer paragraph check plus old-page control; author paragraph check and its 6 controls; hosted `docs-check` | R583-4 | `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` |
| Docs | CLEAN | `CI_WORKFLOWS.md:179-204`; tree-wide count search; doc gates; PR body | R583-4 | `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` |

## Limits

- This is a delta review. For everything outside `532ab871..6b4feeca`, earlier rounds stand.
- No manager source bank ran at this head, and none is claimed. Source-head execution evidence is the author's published receipts plus the hosted runs above.
- The hosted Verilator shards and `elaborate` were in progress at the snapshot, so this review reports no result for them.
- Physical calibration was NOT RUN. The skipped physical gPTP context is not hardware proof.
- No GitHub write, push, Docker, replica run or hardware access. The clone was restored and verified: HEAD and index tree `4358f8ec`, a clean worktree, unchanged gitlinks, and a generated `__pycache__` removed (`receipts/clone_integrity.txt`).

## Pending manager duties

- Accept exact-head hosted contexts once complete: `verilator-suites` (Verilator shards 0-4), `yosys-portability`, `elaborate`.
- Validate the current-dev merge candidate (source base `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`, live dev `0136de16291a127e0a34627c77ac09cd41efc08b`) with the builder and native banks, and link the receipts.
- Pair this verdict with the internal cleared-context re-review at this head.
- Merge only with maintainer authorization, then check post-merge containment.

R583-4 FINISHED

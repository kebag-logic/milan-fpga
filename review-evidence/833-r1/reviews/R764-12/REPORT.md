[R764] POSITIVE - exact head 3e475161e528baa655a5ba84d6a38d78f8c64f3b

# R764-12: external independent review of PR #834 (issue #833), round 12

- **Head:** `3e475161e528baa655a5ba84d6a38d78f8c64f3b`, tree `e07572ea9d7973c84470cf63341597a47c4a0f95`, in an isolated detached clone. The PR's `headRefOid` is the same and the PR is not a draft.
- **Scope:** only the round 12 delta, `5843d1af..3e475161`, under the owner's later-round rule. It has two commits:
  - `3f4e39f3`, the merge of dev `cc204c6f` (PR #836, the elaborate-gate split, and PR #815, the documentation audit);
  - `3e475161`, the regeneration of `docs/DOCUMENTATION_AUDIT.md`.
- **Result:** no BLOCKER, MAJOR, MINOR or new RESIDUE. Two optional SUGGESTIONs. Every prior finding is resolved or retained below.
- **Order followed:** AGENTS.md and CONTRIBUTING.md; the #833 issue body and the manager's rulings; the PR body's Round 12 section; then the delta and its history; then my own probes. Only after that did I read the author's round 12 packet (`review-evidence/833-r1/author-r12/` at `a73ec2da`) and the two round 11 reviews.

## Check 1: the merge keeps both sides, and its conflicts are resolved as the handoff lists

The handoff says the merge had no conflict. TESTING.md was changed on both sides and git merged it automatically. All of the following holds:

| Claim | Evidence | Result |
|---|---|---|
| The merge commit's parents are `5843d1af` and `cc204c6f` | `git log --format='%H %P'` | yes |
| The committed merge tree is git's own automatic merge | `git merge-tree --write-tree 5843d1af cc204c6f` gives `f3379b02…`, rc 0 (no conflict). That equals `3f4e39f3^{tree}` | identical |
| No hand-made hunk in the merge | `git show --cc 3f4e39f3` prints 0 lines | none |
| The PR's own change is unchanged by the merge | stable patch-id of `git diff 1f29f189 5843d1af` and of `git diff cc204c6f 3f4e39f3`: both `a5e12980a28b73885022d9b0d029df8f1555af6e` | equal |
| The four PR files other than TESTING.md are round 11's bytes | blobs at the head equal those at `5843d1af`. Example: `scripts/owned_process.py` is `6495a47b` at both | equal |
| TESTING.md differs from round 11 only by dev's lines | patch-id of `git diff 1f29f189 cc204c6f -- docs/testing/TESTING.md` and of `git diff 5843d1af 3e475161 -- docs/testing/TESTING.md`: both `b49f608f…` | equal |
| Dev's side is unchanged apart from the regenerated page | `git diff 3f4e39f3 3e475161 -- . ':!docs/DOCUMENTATION_AUDIT.md'` is empty | yes |
| One merge base | `git merge-base --all HEAD cc204c6f` gives only `cc204c6f`. `origin/dev` is `cc204c6f` | yes |

Receipts: `receipts/merge_checks.txt`, `receipts/merge_regen_check.txt`, and the portable script `merge_regen_check.sh`.

## Check 2: regeneration only through the generator, and how TESTING.md is counted

- **The page is byte-identical when I regenerate it.** On a fresh clone at the merge commit `3f4e39f3`:
  - `python3 -I scripts/docs_inventory.py --check` is rc 1: `STALE (4 lines differ)`, first at `| stale | 16 | 10,638 |` against `10,722`.
  - `--write` is rc 0. The page it writes is blob `9fdb8bf4`, the head's blob.
  - `scripts/docs_inventory.json` stays `242c0553`, the same at dev, at the head and after `--write`.
- **The head is fresh.** At the head, `--check` is rc 0 (`OK (540 lines, … is fresh)`) and `--selftest` is rc 0 (`OK (50 controls)`). Running `--write` there leaves the tree clean, and `--check` afterwards is rc 0 again.
- **The regeneration commit changes one file, 4 lines.** Its changed lines are identical to the author's `receipts/regen/regen.diff`.
- **TESTING.md is counted by the generator's own rules:**
  - Its row reads 2019, which is `wc -l` of the head's TESTING.md (dev's has 1935).
  - Its status stays `stale`, with its one finding D0-057.
  - D0-057's line for TESTING.md is 1902. At the head that line is `* **Presentation-time offset is pinned at the Milan 2 ms DEFAULT** for every`; at dev the same line is 1818.
  - The stale and total line sums each move by +84, which is 2019 − 1935. Page counts stay 213 / 176 / 16 / 21.

Receipts: `receipts/inventory_regen.txt`, `receipts/testing_md_counting.txt`.

## Check 3: the docs workflow steps and the two tests this PR changes, at the head

All runs were on fresh clones of the head, with the host load average near 79.

- **`python3 scripts/test_suite_cancellation.py`:** rc 0. `suite cancellation: PASS (…stated seconds, reused identity, unsafe negative controls)`. Receipts: `receipts/suite_cancellation.{log,rc}`.
- **`make --no-print-directory -C tb/verilator/gptp_shadow lifecycle`:** rc 0. `mutant lifecycle: PASS (normal/repeat, nine named defects, …)`. Receipts: `receipts/lifecycle.{log,rc}`.
- **Spot-check of `docs.yml` `run:` steps:** this was my own run, not a full replay. It ran every step that needs no apt package, RV32 SDK, sv2v or builder leg.
  - Steps run: `docs_check.py`; `check_doc_style.py` and its `--selftest`; `DOC_MAP.gen.py --check`; `check_doc_paths.py`; `gen_toc.py --selftest`, `--verify-anchors` and `--check`; `docs_inventory.py --check` and `--selftest`; `check_archive.py`; `check_hygiene.py --check` and `--selftest`; `check_py_idiom.py` and `--selftest`; `measure_fail_fast.py --check`; `measure_test_evidence.py --check`; `check_todo_ownership.py`; `check_feature_status.py` and `--self-test`; `measure_control_flow.py --selftest`; `measure_cohesion.py --selftest`; `check_gptp_docs.py --with-submodule`; `ci_gate_workflows.py --check`; `ci_events.py --check`; and the added-line `check_em_dash.py --base cc204c6f` (0 findings over 94 added lines). That is 26 commands, and every one is rc 0.
  - The first pass, `docs_*.log`, has 8 refusals with rc 2. Each one names a missing prerequisite on my host: the pinned Markdown renderer, or uninitialized submodules.
  - The second pass, `docs2_*.log`, re-ran those 8 with the pinned renderer, in a venv built from `tools/markdown/requirements.txt` with `--require-hashes`, and with the submodules at their pinned gitlinks. All are rc 0.
  - No tracked file changed during these runs.
  - Receipts: `receipts/docs_steps_rc.txt`, `receipts/docs_steps2_rc.txt`, `receipts/em_dash.txt`, the script `docs_steps.sh`.
- **The author's full replay, spot-checked:**
  - `receipts/gates/docsyml-verify.rc` is 0.
  - In `docsyml-table.md`, `gate_46`, the inventory freshness gate, is rc 0, and the hosted-only record step is `ci_step_55`, NOT RUN with its reason.
  - Lane rc files: `test_suite_cancellation` 0 and `lifecycle` 0. `mergebase.log` names `cc204c6f` alone.
  - `merge.log`: "Auto-merging docs/testing/TESTING.md / Merge made by the 'ort' strategy", rc 0.
- **The image command-table checker (#838):** `scripts/ci_tool_inventory.py --check` is rc 2 at both the head and dev. Both logs are byte-identical: `REFUSED: CI_IMAGE_SHFMT must name the checksum-pinned Bash parser`. Receipts: `receipts/tool_inventory_*`.
- **Does this round add a pin mismatch?**
  - Measured directly with `pin_staleness.py`, which compares each `sha256` pin in `ci/image/command-table.json` with the pinned file's bytes.
  - The pins stale at the head and not at dev are exactly the 4 scripts this PR changes. They were disclosed in the PR body in round 1 and are byte-identical to round 11's head.
  - Nothing is stale at dev that is not stale at the head. So this round adds no mismatch. Receipt: `receipts/pin_staleness.txt`.
  - This counter counts pins slightly differently from the round 1 script the PR body cites, so its absolute numbers differ. The comparison between head and dev is what this check establishes.
- **Commit hygiene:** both commit messages are one line with no trailers. `git diff --check cc204c6f HEAD` is rc 0.
- **Comment rule:** the regeneration commit adds no source comment. Its added lines contain no lane label, round, reviewer ID or comment ID. The merge adds no line of its own. So the delta has no new RESIDUE.

## Findings

None at BLOCKER, MAJOR, MINOR or RESIDUE.

**R764-12-S1 - SUGGESTION - Docs - PR body "Round 12 gates", the `docs.yml` row - the discarded first replay attempt is disclosed only in the packet**
- **Evidence:** the packet's `author-r12/HANDOFF.md` ("A first docs.yml attempt, discarded") says the first replay failed `ci_step_28` with `SDK provenance mismatch`. The cause was a copied SDK cache in the gate home. The author restarted all five jobs, and that attempt's logs are kept in `receipts/gates/attempt-sdk-copied/`.
- The PR body states the second run's result alone.
- **Impact:** none on any verdict. The first failure was caused by the setup (`ci_rv32_sdk.py` binds the receipt to the absolute destination), and it is disclosed publicly in the packet.
- **Optional change:** one clause in the row, for example "a first attempt with a copied SDK cache failed `ci_step_28` on provenance and was discarded; its logs are in the packet".
- **Verification:** reading the PR body.

**R764-12-S2 - SUGGESTION - Docs - `docs/DOCUMENTATION_AUDIT.md` "Findings cite source lines at dev `1f29f189`" (generator `scripts/docs_inventory.py:585`, `cited_at` in `scripts/docs_inventory.json:3`) - pre-existing on dev, outside #833**
- **Evidence:** the finding rows' line cell is computed from the current tree:
  - at the head, 1902 for TESTING.md;
  - at dev, 1818;
  - at `1f29f189`, the same statement is at line 1810.
- So the header's "at dev `1f29f189`" already fails to match the D0-057 TESTING.md cell on dev. It may describe only the evidence column's citations.
- This PR changes nothing in the generator or the json. It regenerates through them, which is the required path.
- **Impact:** a reader may take the cell as a line at `1f29f189`. No count or status changes.
- **Optional change:** for the #797 audit owner, not this PR. Make the header say which column it governs.
- **Verification:** reading the generated page after that lane's change.

## Prior findings at this head

| ID | Severity | Status at `3e475161` | Evidence |
|---|---|---|---|
| R763-11-R1 | RESIDUE | RETAINED, untouched by the delta. The text is still at `docs/testing/TESTING.md:298` and `scripts/test_suite_cancellation.py:779` | The blob of `test_suite_cancellation.py` is round 11's. TESTING.md line 298 is unchanged by dev's lines |
| R763-11-S1 | SUGGESTION | RETAINED, not taken | blob unchanged |
| R764-11-S1 | SUGGESTION | RETAINED, not taken. The `for at, entry` loop is still at `scripts/test_suite_cancellation.py:827` with no comment of its own | blob unchanged |
| R763-10-R2, R764-10-R3 | RESIDUE | RETAINED for #495 (out-of-domain sweep classes) | unchanged |
| R764-10-S1 | SUGGESTION | NOT TAKEN with a reason, accepted in round 11 | unchanged |
| R764-6-S1 | SUGGESTION | RETAINED, outside #833 | unchanged |
| R763-10-F1 and every earlier MINOR or MAJOR | — | RESOLVED in rounds up to 11. The merge does not change what they depend on: the patch-id is equal, and the four PR files are byte-identical | Check 1 |
| Command-table pins for the 4 changed scripts | disclosed since round 1 | RETAINED as disclosed. This round adds no mismatch | Check 3 |

## Lens results

```text
[R764] PASS Conformance — scripts/owned_process.py blob 6495a47b (= round 11 head), patch-id a5e12980 equal before and after the merge — #833 acceptance items 1 and 2 depend only on files the delta leaves byte-identical; the change under review is the one both round 11 reviews approved.
[R764] PASS RTL — git diff --stat cc204c6f 3e475161 (6 files: 4 Python, 2 Markdown; no .sv/.v/.cpp) and git show --cc 3f4e39f3 (empty) — no RTL or harness in this PR's diff; dev's RTL and CI-side files enter only through git's own conflict-free merge (tree f3379b02 = merge-tree result).
[R764] PASS Robustness — receipts/inventory_regen.txt, receipts/merge_regen_check.txt — generator stale→rc 1, write→rc 0, re-check→rc 0, idempotent --write at head; merge reproduced conflict-free; the changed tests pass on a fresh clone at load ~79.
[R764] PASS Tests — receipts/suite_cancellation.{log,rc}, receipts/lifecycle.{log,rc}, receipts/docs_steps*_rc.txt, receipts/em_dash.txt — both changed tests rc 0 at the head; 26 docs.yml run-step commands rc 0; inventory selftest 50 controls; command-table checker rc 2 identical to dev.
[R764] PASS Docs — docs/DOCUMENTATION_AUDIT.md blob 9fdb8bf4 (regenerated byte-identical), scripts/docs_inventory.json blob 242c0553 (unchanged), TESTING.md row 2019 / D0-057 line 1902, PR body Round 12 — page regenerated only through the generator; counts follow TESTING.md's merged length; PR body claims verified. S1 and S2 are optional.
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `scripts/owned_process.py` (unchanged blob); patch-id equality; #833 acceptance and the round 11 ruling | R764-12 | `3e475161e528baa655a5ba84d6a38d78f8c64f3b` |
| RTL | CLEAN | PR diff file list against `cc204c6f`; combined diff of `3f4e39f3`; `merge-tree` result | R764-12 | `3e475161e528baa655a5ba84d6a38d78f8c64f3b` |
| Robustness | CLEAN | generator stale, write and check cycle on `3f4e39f3` and at the head; merge reproduction; tests under load | R764-12 | `3e475161e528baa655a5ba84d6a38d78f8c64f3b` |
| Tests | CLEAN | `test_suite_cancellation.py` and `lifecycle` rc 0; 26 docs.yml step commands; em-dash gate; the author's docs.yml verifier rc 0 (spot-checked) | R764-12 | `3e475161e528baa655a5ba84d6a38d78f8c64f3b` |
| Docs | CLEAN | `docs/DOCUMENTATION_AUDIT.md`, `scripts/docs_inventory.json`, `docs/testing/TESTING.md`, PR body Round 12; R763-11-R1 carried as RESIDUE; S1 and S2 optional | R764-12 | `3e475161e528baa655a5ba84d6a38d78f8c64f3b` |

## Real limits

- **The `docs.yml` replay was a spot-check, not a full one.** I did not run the apt, RV32 SDK, sv2v or builder-leg steps (`docs-gates-1`, `docs-gates-2`, `ci_step_25` and `ci_step_28` among them), `act_ci.py --selftest`, or the hosted-only record and upload steps. For those I rely on the author's published replay, which I spot-checked.
- **Not re-run by me in this round:** `--mutants`, `--matrix`, `behave`, the full sweep and my own row sweeps. The delta leaves every file they exercise byte-identical to round 11's head.
- **The author's packet commit `a73ec2da` is not signature-verified.** GitHub reports `unsigned`, and the round 12 subtree carries no checksum manifest. I verified the receipts I used against my own reproduction instead: the regeneration diff, the merge log and the merge base.
- **No manager source bank runs at this head, and I claim none.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Hosted contexts at this head were mostly in flight when I looked.** 5 had succeeded (`full-ci-gate`, `wire-accountability`, `bdd-conformance`, `changes`, `elaborate-gates-3`), 1 was skipped (`Physical gPTP (nightly and manual)`), and 41 were queued or running (`receipts/hosted_checkruns.tsv`). I give no hosted verdict.
- **The clone was restored and verified after the probes.** HEAD is `3e475161`, the tree is `e07572ea`, and the worktree and index match HEAD. The tree listing and the index listing, with the same fields, have equal sha256. All 6 submodule gitlinks match HEAD (`receipts/clone_integrity.txt`). All probe copies were under `scratch/`.

## Pending manager duties

- Hosted and act acceptance at this exact head, with `rtl-fast`, `verilator-suites` and `yosys-portability` evidence.
- The current-dev merge candidate: its builder and native banks, with receipts linked on the PR. Source base and live dev are both `cc204c6f`.
- Carry R763-11-R1, R763-10-R2 and R764-10-R3, and the SUGGESTIONs (R764-12-S1, R764-12-S2 for the #797 owner, R763-11-S1, R764-11-S1), to the residue checklist.
- #838, the command-table checker refusal, stays tracked outside this PR.
- Merge only with explicit maintainer authorization, then post-merge containment.

R764-12 FINISHED

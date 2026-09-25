[R266] POSITIVE - exact head b74fb11162fba8f019110d9f2c21492300857da2

# R266-5: composition review of issue #532 / PR #533 (merge-train candidate)

- **Candidate:** `b74fb11162fba8f019110d9f2c21492300857da2`, tree `f64880a6c1719e28de9e3de266f7aa65bcd214f5`.
  - First parent: `7ddbbdc9be73728b239718c8976261c7e0ad0563` (dev plus the queued predecessors).
  - Second parent: the reviewed source head `022290e4c94a23b9ee97852b6c1c2ee2c1f25352`.
- **Scope of this round:** composition acceptance only. The source head already has two independent POSITIVE source reviews: R266-4 (issuecomment-5810373076) and R267-4 (issuecomment-5811497248), both at `022290e4`.
- **Verdict: POSITIVE.** The composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR or MINOR is open under any lens. All five lenses were applied at this head.

## Reconstruction

- **Order read:** AGENTS.md sections 3-8, then CONTRIBUTING.md (the act-first and merge-bar references), then docs/README.md.
- **Issue #532:** the body, acceptance 1-6, and the "Manager integration (outside this PR)" note.
- **Interface authority:** `docs/testing/CI_WORKFLOWS.md`, "Act-first local replication" (`:1258`) and "Parallel replay slots" (`:1735`).
- **Diff:** `git diff 7ddbbdc9..b74fb111` and the history of both parents.
- **Hosted evidence:** check runs for the source head.
- **Prior public review findings:** read only after my independent pass and my gate runs were complete.
- **Not read:** any other reviewer's packet, and any private author or manager material.

## Composition scope (receipts/diff_scope.txt, receipts/blob_identity.txt, receipts/merge_reconstruction.txt)

1. **The merge reproduces exactly.** `git merge-tree --write-tree 7ddbbdc9 022290e4` returns `f64880a6`, which is the candidate tree. The merge is clean and has no hand resolution.
2. **The PR delta is identical.** The candidate's own delta `7ddbbdc9..b74fb111` and the source delta `759da623..022290e4` have the same stable patch-id, `9233e7cc3fe3...`. Both cover the same four files: `docs/testing/CI_WORKFLOWS.md`, `scripts/act_ci.py`, `scripts/act_slot_proof.sh` and `scripts/check_baremetal_only.py`.
3. **Three of the four files are byte-identical to the source.** `scripts/act_ci.py` (`3655988c`), `scripts/act_slot_proof.sh` (`f756400f`) and `scripts/check_baremetal_only.py` (`b488d3c2`) have the same blobs at `022290e4` and `b74fb111`.
4. **One file is shared with a predecessor, `docs/testing/CI_WORKFLOWS.md`.** Between `759da623` and `7ddbbdc9`, seven commits touched it: 387b, 408, #387 margin and GM-step, and the containment-retention commits. This confirms the declared overlap `{"532": {"dev+train": ["docs/testing/CI_WORKFLOWS.md"]}}`, and there is no other overlap.
   - **The hunks are disjoint.**
     - Predecessor hunks: `:156-192` (the `milan_dp` budget table), `:1154-1155` (the gate 1b text refusals, in "Elaboration") and `:2133-2139` at the candidate (the containment proof paragraph, in "Issue closing on merge").
     - Every PR hunk lies inside "Act-first local replication".
     - That whole section, including "Parallel replay slots", is byte-identical between source and candidate: sha256 `15d9ac87...`, 823 lines, shifted +26 lines (`receipts/doc_section_identity.txt`).
     - The predecessor delta equals the source-to-candidate delta of this file line for line (`receipts/pred_ci_workflows.diff`, `receipts/source_vs_candidate_ci_workflows.diff`).
5. **Live dev:** `0755923d` (PR #556) is not an ancestor of the candidate. However, `git merge-tree --write-tree b74fb111 0755923d` returns the same tree `f64880a6`, so live dev adds no content beyond this candidate. #556's five files do not include any file this PR changes (`receipts/live_dev_relation.txt`).
6. **Gitlinks and `.gitmodules`:** the four gitlinks at the candidate equal the train parent's. The PR changes none. `.gitmodules` is the same blob at S, B and H.

## Semantic interactions checked

| Interaction | Check at the candidate | Result |
|---|---|---|
| `ci_events.py` pins the prose of `CI_WORKFLOWS.md` (`POLICY`, `:258`), and a predecessor changed both files | `ci_events.py --check` / `--selftest` | OK: 1647 contract items across 4 workflows plus the policy page. Selftest PASS: 2188 arms. |
| Contents and anchors of the shared page, with gen_toc rewritten upstream to use the hash-locked renderer and `gen_toc_shapes.json` | `gen_toc.py --selftest` / `--verify-anchors` / `--check`, run with the renderer installed from `tools/markdown/requirements.txt` with `--require-hashes` | Selftest PASS: 1501/1501 arms. 173 cross-page fragments reproduced. TOC OK on 107 pages. The one shapes-corpus row citing `CI_WORKFLOWS.md` is a synthetic page and does not read the live page. |
| Em-dash on added lines, where the gate now imports `RendererError` and shape arms from gen_toc | `check_em_dash.py --base 7ddbbdc9` | 0 findings over 359 added lines. Arms 339/339. |
| The PR's `check_baremetal_only.py` masks and arms over a tree to which predecessors added 130 files | `--check` / `--selftest` | 0 findings across 864 files. Selftest PASS: 441 arms, including `_arms_act_slot_masks` (`:965`). |
| The runner's offline self-test reads the shipping workflows (`selftest_shipping_workflows`, `act_ci.py:12495`), and a predecessor changed `docs.yml` (two steps added) | The two pure validators behind those arms (`validate_workflow_sandbox` `:1970`, `workflow_job_volume_scope` `:2216`), applied to exported source and candidate trees with a planted control (`scripts/workflow_policy_probe.sh`) | Both trees PASS both validators. The planted `someone/untrusted@v1` is REFUSED. The action set is unchanged: `actions/cache@v4` is already in `TRUSTED_ACTION_USES` (`:191`). |
| Acceptance 6 (no workflow semantics change) | `git diff --name-only 7ddbbdc9 b74fb111 -- .github` | 0 files. `elaborate.yml`, `rtl-fast.yml` and `rtl.yml` are the same blobs as at the source; `docs.yml` differs only by the predecessor's two steps. |
| `milan_dp` budget 2700 s to 3600 s (`run_all_suites.sh`) against the PR's per-slot CPU/memory bounds | Read `CI_WORKFLOWS.md:156-192`, `:1535-1540` and the slot section | The change only lengthens a deadline. The slot section states no suite duration. No contradiction. |
| Governance links (`CONTRIBUTING.md`, `AGENTS.md`), both changed upstream | `docs_check.py`, `check_doc_paths.py`, `DOC_MAP.gen.py --check`, anchor check | All OK. The predecessor edits contain no act or replay text. `#act-first-local-replication` still resolves. |
| Ratchets and budgets that read the PR's scripts | `measure_naming`, `measure_fail_fast`, `measure_test_evidence` (`--check` and `--selftest`), `check_hygiene`, `check_py_idiom`, `check_sh_idiom`, `check_todo_ownership`, `measure_control_flow --selftest`, `ci_scope --selftest`, `check_archive`, `check_doc_style` (`--selftest` too) | All rc 0 (`receipts/gates_candidate/SUMMARY.txt`). |

All 24 gate invocations returned rc 0 (`scripts/run_gates.sh`, at most 8 jobs in parallel, logs in `receipts/gates_candidate/`).

## Findings

No BLOCKER, MAJOR, MINOR or new SUGGESTION.

## Prior public findings: status at this head

| Finding(s) | As filed | Status at b74fb111 | Evidence |
|---|---|---|---|
| Manager source validation r1 (`check_baremetal_only --check`, 29 findings at `fcce541b`) | failure | still RESOLVED | `--check` gives 0 findings across 864 files at the candidate |
| R266-1 F1-F6; R267-1 F1-F5 | MAJOR/MINOR | still RESOLVED | Resolved at source rounds 2-4. The runner, the proof script and the whole act-first doc section are byte-identical to `022290e4`. |
| R266-2 F1; R267-2 F1-F2 | MINOR | still RESOLVED | same identity |
| R266-3 F1-F3; R267-3 F1-F3 | MINOR | still RESOLVED | R266-4 and R267-4 resolved them at `022290e4`. Same bytes here. |
| R266-4 S1 (late-refusal holder's fixed hold not named in the doc) | SUGGESTION; Tests, Docs | retained, not taken; optional | `act_slot_proof.sh:222-232,464-466` unchanged. The doc passage moved from `:1986-1996` to `:2012-2022` with the same bytes (sha256 `3ee42f7d...`). |
| R267-4 S1 (unannounced-run case holds for a fixed time) | SUGGESTION; Tests, Docs | retained, not taken; optional | `act_slot_proof.sh:459-466,630` unchanged. The doc is at `:2012-2022` at the candidate. |
| R267-2 S1 (no workflow runs `act_slot_proof.sh --selftest`) | SUGGESTION | retained, not taken; optional | `grep -rn act_slot_proof .github/` has no match at the candidate. Taking it would edit a workflow, which acceptance 6 constrains. |

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Acceptance 4 and 6 against the composed tree: 0 `.github` files in the PR delta; the three non-doc PR blobs are identical to the source. `ci_events.py --check` is OK over the composed `CI_WORKFLOWS.md` and workflows. The shared page's hunks are disjoint and do not contradict each other (`:156-192`, `:1154-1155`, `:1258-2080`, `:2133-2139`). **Composition touches scope:** yes, through the shared policy page and the pinned prose. Behavioural conformance of the runner is covered by R266-4 and R267-4 at `022290e4`, with identical bytes. | R266-5 (composition); R266-4, R267-4 (source) | b74fb111 (composition); 022290e4 (source) |
| RTL | CLEAN | The PR changes no HDL. Neither `c266432d..0755923d` nor any predecessor touches a PR file other than the doc. The runner's resource and timing logic (`act_ci.py:132-166` timeouts, slot CPU/memory bounds, `CI_WORKFLOWS.md:1535-1540`) is byte-identical. The `milan_dp` deadline change is only an extension. **Composition touches scope:** no. It is covered by the source reviews R266-4 and R267-4. | R266-5 (applied, no composition surface); R266-4, R267-4 | b74fb111; 022290e4 |
| Robustness | CLEAN | Sandbox refusal on the composed workflows: PASS, plus a planted untrusted-action control that is REFUSED (`receipts/workflow_policy_probe.txt`). Job-volume lease prefixes are unchanged. The slot uplink gives the new `docs.yml` pip step outbound reach (`CI_WORKFLOWS.md:1768-1797`). The runner's refusal paths have identical bytes. **Composition touches scope:** yes, the runner's workflow input (`docs.yml`) changed. | R266-5; R266-4, R267-4 | b74fb111; 022290e4 |
| Tests | CLEAN | 24 gate invocations with rc 0 at the candidate, including the selftests of `ci_events` (2188 arms), `check_baremetal_only` (441 arms, with the PR's act-slot mask arms), `gen_toc` (1501 arms) and em-dash (339 arms). The inputs of the runner self-test's shipping-workflow arms were validated at the candidate. The PR's own self-tests have bytes identical to the source. **Composition touches scope:** yes, the shared gates and workflow inputs. | R266-5; R266-4, R267-4 | b74fb111; 022290e4 |
| Docs | CLEAN | `docs/testing/CI_WORKFLOWS.md` at the candidate: the act-first section is byte-identical to the source. Predecessor paragraphs are intact. `gen_toc --check`/`--verify-anchors`, `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `DOC_MAP.gen.py --check` and `check_archive.py` are all OK. The `act_slot_proof.sh:7` pointer to "Parallel replay slots" resolves (`:1735`). **Composition touches scope:** yes. | R266-5; R266-4, R267-4 | b74fb111; 022290e4 |

## Real limits

- **The runner's full offline self-test was not run at the candidate**, by instruction: no host `act_ci.py` or its self-test. Only the two pure workflow validators behind its shipping-workflow arms were exercised. Its other arms read the fixture, not the composed tree, and the file is byte-identical to the reviewed source.
- **`act_slot_proof.sh --selftest` was not re-run.** Its bytes are identical to the source, where R266-4 and R267-4 ran it and its mutants.
- **Not run:** Docker, act, privileged or live slot proofs, hardware, the full parent/PP/gPTP/Yosys/builder banks, and Verilator (not needed: no HDL or testbench is in the composition scope).
- **Hosted evidence exists only for the source head `022290e4`.** Every executed job there succeeded; `Physical gPTP (nightly and manual)` was **skipped**, not executed. The candidate commit `b74fb111` is not known to GitHub (HTTP 422 on its check runs), so it has no hosted evidence (`receipts/hosted_check_runs.tsv`).
- **Physical calibration was NOT RUN.** Field skips are not hardware proof.
- The Markdown renderer was installed from its hash lock into a disposable environment under `scratch/` and is not published.

## Pending manager duties

- Publish the source static/builder and native bank results for this head. They are not claimed or inferred here.
- Build and validate the final current-dev candidate at the merge turn (source base `7ddbbdc9`, live dev `0755923d`, or whatever dev is at that point). The receipt shows that today's live dev adds no content to this tree.
- Hosted and act acceptance of the exact merge head, including `docs-check` running `act_ci.py --selftest` on the composed tree.
- Maintainer merge authorization. Post-merge containment.

## Integrity

- The clone is at `b74fb111`, tree `f64880a6`, and the index tree equals HEAD.
- `git status --porcelain --ignored` is empty.
- All 890 tracked blobs hash equal to HEAD with modes unchanged.
- The required gitlinks match HEAD.
- Evidence: `receipts/clone_integrity_after.txt`.

R266-5 FINISHED

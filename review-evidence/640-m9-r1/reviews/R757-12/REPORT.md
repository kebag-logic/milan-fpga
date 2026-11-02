[R757] POSITIVE - exact head e377f0dde52fed99de54d9449c48ab22152dcf2e

# R757-12: composition review of the issue #640 merge-train candidate (PR #828)

Candidate `e377f0dde52fed99de54d9449c48ab22152dcf2e`, tree `5936f42145c658cd9d939b6d33c9610235897c21`. Parents: live dev `1f29f189279f9fc0132f4918e47342b87d22f33a` and PR head `c576fe540838c353a1cfc9455a6b89eff2b77ffc`.

## Result

- **No BLOCKER, MAJOR or MINOR, and no new RESIDUE or SUGGESTION.** The composed tree introduces no defect beyond the reviewed source head.
- **The composition is an identity.** No predecessor PR is queued in this candidate. The merge base of dev and the PR head is dev itself (`1f29f189`). `git merge-tree --write-tree` of the two parents gives `5936f421`. That equals the candidate tree and the PR head tree, and `git diff c576fe54 e377f0dd` is empty (`receipts/composition.txt`).
- **The overlap set is `{}`.** No file this PR changes was also changed by a predecessor. Dev has no change since the merge base, so no shared registry, workflow or record pin, gate inventory, docs table, TOC or anchor can interact.
- **The signed local-CI packet verifies.** Its key is the required one, the signature is good, and the subject names this candidate and head. All 47 coverage entries are `ok`, and the workflow definitions hash to the candidate's files (details below).
- **Every docs-reading gate passes on the candidate:** 13 gates, all rc 0.
- **The source head's two POSITIVE reviews cover the tree byte for byte:** R757-11 (comment 6564722042) and R758-11 (comment 6564695818), both at `c576fe54`. Every prior finding is resolved or retained below, with its state at this head.

## Signed local CI packet (aff1c618, `review-evidence/640-m9-r1/local-ci/c576fe54`)

| Check | Result | Receipt |
|---|---|---|
| `manifest.json` sha256 | `9c7a546c228ea61a3d3a7edae3980397a4e0bc87ae9b75e3cd73f03f43b98d68`, as stated | `receipts/signed/manifest.json` |
| (1) The `allowed_signers` key | One line, principal `milan-local-ci`, namespace `milan-local-ci`, ED25519 `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`: the required key, and no other key | `receipts/signature_verify.txt` |
| (2) `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` | `Good "milan-local-ci" signature`, rc 0 | `receipts/signature_verify.txt` |
| (3) Subject | candidate `e377f0dd`, candidate_parent `1f29f189`, candidate_tree `5936f421`, head `c576fe54`, head_tree `5936f421`, PR 828, `kebag-logic/milan-fpga` | `receipts/signed/manifest.json` |
| (3) Coverage | 47 entries, all `ok: true`: 46 `by: act` and 1 `not-run` (`rtl/physical-gptp`, which runs only on schedule and dispatch, is reported nightly and is not hardware evidence). Every referenced act job ran to `success`. The only act job no entry references is that skipped physical gPTP job. | same |
| Act and banks | act exit 0; 67 jobs succeeded and 1 was skipped. The `full-native` bank ran 5 commands and `manager-builder` ran 48, every one with exit 0. `result: success` | same |
| Workflow definitions | `docs`, `elaborate`, `rtl-fast` and `rtl` hash to the same sha256 in the manifest (candidate and head) as the candidate's `.github/workflows/*.yml` | `receipts/workflow_sha256_at_candidate.txt` |

## Gates re-run on the candidate

The docs-reading gates were re-run with `run_checks.sh`. The TOC and em-dash gates used the pinned renderer from `tools/markdown/requirements.txt`, installed with `--require-hashes` into a scratch venv (`receipts/venv_freeze.txt`).

| Gate | rc | Summary line |
|---|---|---|
| `docs_check.py` | 0 | 0 findings across 213 md files and 1436 scrubbed files; scrub self-test 23/23 |
| `gen_toc.py --check` | 0 | 152 pages carry a contents list |
| `gen_toc.py --verify-anchors` | 0 | 581 cross-page fragment links reproduced |
| `check_em_dash.py --base 1f29f189` | 0 | 0 findings over 1915 added lines in 23 pages; arms 339/339 |
| `check_baremetal_only.py --check` | 0 | 0 findings across 1434 files |
| `check_doc_paths.py` | 0 | 1084 cited paths resolve |
| `check_doc_style.py` | 0 | 23 current documents |
| `check_feature_status.py` | 0 | 0 findings |
| `check_solution_docs.py` | 0 | OK |
| `check_gptp_docs.py` | 0 | 8 current pages |
| `ci_events.py --check` | 0 | 2199 contract items across 4 workflows and `docs/testing/CI_WORKFLOWS.md` |
| `ci_gate_workflows.py --check` | 0 | generated workflows match their templates |
| `git diff --check 1f29f189 HEAD` | 0 | clean |

`check_hygiene.py` refuses to run without initialised submodules, so it was not run. It reads code quality, not anything this docs-only diff changes. The act `docs`/`rtl-fast` jobs in the signed packet cover it.

## Independent pass over the diff (`1f29f189..e377f0dd`)

- **Files:** 23 Markdown pages (`receipts/pr_changed_files.txt`). The diff has no HDL, firmware, generator, workflow, constraint, script or test path. All six gitlinks equal dev's (`receipts/gitlinks_head.txt`). It adds no source comments, so the comment rule has nothing to apply to.
- **Last source commit `c576fe54`:**
  - MAILBOX_SPLIT:42-44 bounds the gPTP plane at F6, which agrees with `REQUIREMENTS.md:36,43`.
  - AREA_BUDGET:130, 140 and 180 add "at 32x32", which agrees with the NFR-RES-01 row in FR_NFR.
  - The history sentence count at AREA_BUDGET:182 is bounded.
  - MANAGER.md:8-9 scopes the guide to the fabric plane until F6 and links the split contract.
  - ieee8021q.md:37-45 moves the Mark II sentences out of the list item.
- **Spot checks:**
  - The headline figures appear only where expected, and in agreement: 143.347, 95.867, 63.431, 359.75, 21.45k, 144.5 and 38,040 match across FR_NFR, the stream-engine design, the area plan and the area budget.
  - Every remaining "build-selectable" for the placement is scoped "Until the switch-over" (`README.md:62`, `REQUIREMENTS.md:27`, both overview pages).
- **Own findings:** the only one is that the PR body stops at round 9. That is retained item R757-11-R2 below, not a new item.

## Prior findings at this head

Prior reports were read only after the pass above. The candidate tree equals `c576fe54`, so each item's state is the one at that head. Each was re-confirmed at this head (`receipts/retained_items_at_head.txt`).

| Item | State at e377f0dd | Evidence |
|---|---|---|
| R757-10-F1 MINOR (MS: gPTP plane without an F6 bound) | **Resolved** | MAILBOX_SPLIT:42-44 |
| R757-10-R1, R758-10-R1 RESIDUE (ieee8021q list) | **Resolved** | ieee8021q.md:37-45 |
| R758-10-R2, R758-10-R3, R758-10-R4 RESIDUE | **Resolved** | AREA_BUDGET:130, 140, 180, 182; MANAGER.md:8-9 |
| R757-10-R2 RESIDUE | **Retained**, part. AB:129 still reads "is the accepted headroom target", and AB:180 lacks "fitting Block RAM". | Exact fix: AB:129 "is the accepted target"; AB:180 "That is fewer than 20,000 LUTs at 32x32, fitting Block RAM, with timing met." |
| R757-10-R3 RESIDUE | **Retained**. MS:13 "defines the Mark II default"; `docs/findings/README.md:26` "a tenth of the NFR-RES-01 gap" | Exact fix: MS:13 "The [placement contract](../ARCHITECTURE_HW_SW_SPLIT.md) defines the transition and end state." |
| R757-10-S1 SUGGESTION | **Retained**, optional | `docs/guides/SYSTEM_INTEGRATOR.md:95`, `docs/BUILD_FLASH_BOOT.gen.py:44` |
| R757-11-R1, R758-11-R2, R758-11-R3 RESIDUE (author-r10 handoff wording) | **Retained**: evidence prose only, outside the tree | `review-evidence/640-m9-r1/author-r10/HANDOFF.md` |
| R757-11-R2, R758-11-R1 RESIDUE (PR body stops at round 9) | **Retained**, and confirmed independently in this round: the live body has no row for `c576fe54` and no Round 10 section. Its Status line (line 24) and its evidence (line 298) name `d63b378d`. | Exact fix: add a contents entry and a `## Round 10` section for `c576fe54`. Point the status line at the candidate evidence: the signed packet at `aff1c618`. |
| R758-11-R4 RESIDUE, for #495 | **Retained** | MS:134 "grandmaster change published by the gPTP plane". Exact fix: append "until F6" |
| R757-11-S1, R758-11-S1, R758-10-S1 SUGGESTION | **Retained**, optional | MS:43 "F6" meaning; MS:43-44 wrap; PR body "documentation only" |
| R757-8-R1, R757-8-R2 RESIDUE | **Retained** | FR_NFR:306 still reads "that derivation" |
| R757-7 RR13 RESIDUE (manager's) | **Retained** | The #640 acceptance still reads "Every talker stream meets the 65 µs target", but NFR-LAT-03 is now a target |
| Named for the owner (R758-10): whether D8's 1 percent margin applies to the 20,000-LUT ceiling | **Open owner question**, not a finding | `docs/design/AREA_BUDGET.md:370,398` |

## Lens results

```text
[R757] PASS Conformance - receipts/composition.txt; receipts/pr_changed_files.txt; MAILBOX_SPLIT.md:42-44, AREA_BUDGET.md:127-131,178-182 against REQUIREMENTS.md:27,36,43 and FR_NFR.md NFR-RES-01/NFR-LAT-03 - the composed tree equals the reviewed source tree, so every requirement and clause claim is the one R757-11 and R758-11 judged; the c576fe54 claims re-read against their clauses
[R757] PASS RTL - receipts/pr_changed_files.txt; receipts/gitlinks_head.txt; receipts/workflow_sha256_at_candidate.txt - no HDL, register, generator, constraint or workflow path in 1f29f189..e377f0dd; gitlinks equal dev; the signed packet's rtl-fast, rtl-full and elaborate act jobs all succeeded on these workflow bytes
[R757] PASS Robustness - receipts/composition.txt; receipts/signed/manifest.json - no runtime path in the diff and no predecessor interaction (overlap {}); the act coverage ran every PR-event job on the candidate's workflows with ok on all 47 entries
[R757] PASS Tests - receipts/*.rc (13 gates rc 0); receipts/ci_events_check.log; receipts/ci_gate_workflows.log - no test or gate inventory in the diff; CI event contract and generated workflows check clean on the candidate
[R757] PASS Docs - receipts/docs_check.log, gen_toc_check.log, gen_toc_anchors.log, em_dash.log, doc_paths.log, doc_style.log, baremetal.log - every docs-reading gate passes on the candidate; README/TOC/anchor tables have no competing predecessor edit; the retained residue is wording only
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition identity; c576fe54 claims against REQUIREMENTS.md and FR_NFR.md; source coverage R757-11 and R758-11 | R757-12 (composition); R757-11, R758-11 (source) | e377f0dd (tree 5936f421, the same tree as c576fe54) |
| RTL | CLEAN. The composition does not touch its scope: no RTL path, and the gitlinks equal dev | `pr_changed_files.txt`, `gitlinks_head.txt`, workflow hashes, signed act RTL jobs | Covered by the source reviews R757-11 and R758-11; confirmed by R757-12 | e377f0dd |
| Robustness | CLEAN. The composition does not touch its scope: no runtime path | `composition.txt`, signed coverage | Covered by the source reviews R757-11 and R758-11; confirmed by R757-12 | e377f0dd |
| Tests | CLEAN. The composition does not touch its scope: no tests, and the gate inventories are unchanged | 13 gate receipts; `ci_events --check`; `ci_gate_workflows --check` | R757-12; source R757-11, R758-11 | e377f0dd |
| Docs | CLEAN, with retained RESIDUE only | Docs gate receipts on the candidate, the c576fe54 diff, and the retained-item lines | R757-12; source R757-11, R758-11 | e377f0dd |

## Real limits

- This is a composition review. The 1,915-line source diff was spot-checked, not re-derived. The latency, save and area derivations rest on the source reviews of `c576fe54`, whose tree this candidate equals.
- `check_hygiene.py` was not run: it needs the submodules, and this round does not initialise them. The act jobs in the signed packet cover it.
- The other gates and the signed packet were not re-run, because no claim needed falsifying. The packet was verified, not replayed.
- Physical calibration was not run. The physical gPTP job is skipped on PR events. Neither is hardware proof.
- Hosted exact-head contexts were not judged here.

## Pending manager duties

- Carry the retained RESIDUE (R757-10-R2, R757-10-R3, R757-11-R1, R757-11-R2/R758-11-R1, R758-11-R2, R758-11-R3, R758-11-R4, R757-8-R1, R757-8-R2) to the residue checklist. Owner-side items: R757-7 RR13 (the #640 acceptance wording) and the D8 margin question.
- Accept the hosted and act results, and confirm that live dev is still `1f29f189` at the merge turn; otherwise this composition must be rebuilt.
- Merge only with explicit maintainer authorisation. The PR states it does not complete #640, so #640 stays open.

R757-12 FINISHED

[R731] POSITIVE - exact head 3ae30dc3fcd3d7b65e8e121d3e0596cc31abfe07

# R731-8: composition review of the #787 merge-train candidate (PR #822)

This is a cleared-context composition review of issue #787 / PR #822. The candidate is `3ae30dc3fcd3d7b65e8e121d3e0596cc31abfe07`, tree `43d185333ff4048986a2080996ed5e482af3f3bc`. Its parents are live dev `e5b8405db4c1f7cbdafb5df92b15b580142e0232` and PR head `455a3953bf49efda23be4e73447a25b66a5c4bf7`.

**Verdict: POSITIVE.** The composed tree adds no defect beyond the reviewed sources. No MINOR, MAJOR or BLOCKER is open against it.

The candidate tree is **byte-identical** to the PR head tree. R731-7 and R732-7 reviewed that head POSITIVE (PR comments 6550541073 and 6550586671). The tree is also identical to `86a349d5`'s and `cbc7c604`'s. The composition delta is therefore empty. Every gate that reads a file shared with the predecessors passes on this candidate. The signed local-CI packet verifies, and its subject is this candidate and head. The two manager-owned conditions from the earlier composition round, R731-6 MD-1 and MD-2, are **resolved** at this head.

## 1. Reconstruction

- **Contract.** `AGENTS.md` sections 6-8 (lenses, verdict line, completion ledger) and `CONTRIBUTING.md`. The issue scope is frozen as the source reviews recorded it: the end station resets on an AECP REBOOT (IEEE 1722.1-2021 7.4.43; Milan v1.2 5.4.5.2) and keeps ENTITY_DEPARTING on the wire (Milan v1.2 5.6.3.3), with `KL_reboot_ctrl` and the processor pin `a9e84b66`. This round judges composition only. It does not re-judge the source design.
- **Candidate shape** (`receipts/composition.txt`):
  - `git rev-parse` gives `43d18533` for all three of `3ae30dc3^{tree}`, `455a3953^{tree}` and `86a349d5^{tree}`.
  - `git merge-base --all e5b8405d 455a3953` prints exactly one base, `e5b8405d`.
  - `git merge-tree --write-tree e5b8405d 455a3953` gives `43d18533` with no conflict.
  - `git ls-remote` (read-only) shows `refs/heads/dev` at `e5b8405d` and `refs/pull/822/head` at `455a3953`. So the candidate is live dev plus this PR. No other queued predecessor is in the composition.
  - The head merge `455a3953` itself adds no byte: `git diff 86a349d5 455a3953` is empty.
- **Predecessors.** These landed on dev since the PR's base `1e80128f`: #816, #821, #813, #826 and #820. The branch merged them at `5640e4d7`, `f7d5fc3c`, `6ffadb07`, `86a349d5` and `455a3953`. All of these merges come before the source-reviewed head.
- **Shared files.** The PR (dev..candidate, 63 files) and the predecessors (`1e80128f..e5b8405d`) both change these 17 files:
  - `CHANGELOG.md`
  - `docs/design/AREA_BUDGET.md`
  - `docs/diagrams/PNG_MANIFEST.json` and `submodule_boundaries.{drawio,png,svg}`
  - `docs/integration/BAREMETAL_FIRMWARE.md` and `docs/integration/BUILDING.md`
  - `docs/litex/CLOCK_DOMAINS.md`
  - `docs/reference/SUBMODULES.md`
  - `docs/testing/TESTING.md`
  - `hdl/milan/milan_datapath.sv`
  - `scripts/port_docs.budget`
  - `sw/litex/milan_soc.py`
  - `syn/yosys/rom_digests.tsv`
  - `tb/verilator/milan_dp/{Makefile,README.md}`
- **Hunk check.** I read every deleted line in those 17 files against dev. Each one is the PR's own intended change, and no predecessor hunk is dropped. The changes are:
  - the pin text `f65c8ff7` -> `a9e84b66`;
  - the port census 2162/1766 -> 2181/1771;
  - the TX-good wire in `milan_datapath.sv`, replaced by the REBOOT egress-wait wiring;
  - the `KL_reboot_ctrl.sv` source-list addition beside `KL_link_guard.sv`;
  - the AREA_BUDGET sentence "this change meets the build floor", re-attributed to #806's route, with the #787 route lines added after it. The #818 table, which is the gate's record, is not touched.
- **`git diff --check e5b8405d 3ae30dc3`:** rc 0. This is the check that refused `667b9bbc` earlier.

## 2. Gates on the candidate (shared registries, records, TOC and anchors)

All gates ran at the exact head in this clone. Logs and rc files are in `receipts/gates/`, and the summary is in `receipts/gates/SUMMARY.txt`. **51 of 51 pass with rc 0.**

- **Documentation and style:**
  - `docs_check.py`
  - `check_feature_status.py`, plus its `--self-test`
  - `check_wire_accountability.py --self-test`
  - `check_em_dash.py --base e5b8405d`: 0 findings over 588 added lines in 25 pages, arms 339/339
  - `check_doc_style.py`, plus its selftest
  - `check_gptp_docs.py`, plus its selftest and `--with-submodule`
  - `check_solution_docs.py`, plus its selftest
  - `check_submodule_docs.py`, plus its selftest
  - `check_diagram_pngs.py`, plus its selftest. This covers the shared `PNG_MANIFEST.json` and the `submodule_boundaries` diagram.
  - `check_doc_paths.py`
  - `check_archive.py`
- **Table of contents and anchors:**
  - `gen_toc.py --selftest`: 1501/1501 arms
  - `gen_toc.py --verify-anchors`: 552 cross-page fragments reproduced
  - `gen_toc.py --check`: 151 pages OK
- **Registries and inventories:**
  - `check_port_contracts.py`, plus its selftest. This covers the shared `port_docs.budget`.
  - `check_soc_sources.py`, plus its selftest
  - `check_rtl_source_lists.py`, plus its selftest. This covers the shared `milan_dp/Makefile`.
  - `pp_srcs.py --check --selftest`
  - `suite_shards.py --selftest`
  - `ci_scope.py --selftest`
  - `ci_gate_workflows.py --check`
  - `generate_ci_evidence_pins.py --check`
  - `ci_events.py --check` and `ci_events.py --selftest`
  - `check_baremetal_only.py --check`
  - `check_nvm_record_space.py`
  - `check_nvm_capture.py`
- **Measures and idiom checks:**
  - `measure_naming.py --check`
  - `measure_fail_fast.py --check`
  - `measure_test_evidence.py --check`, plus its selftest
  - `check_todo_ownership.py`
  - `check_hygiene.py --check`
  - `check_sv_idiom.py`, `check_cpp_idiom.py` and `check_sh_idiom.py`
  - `check_py_idiom.py`, plus its selftest
- **The #818 resource gate**, run because `AREA_BUDGET.md` is shared with #820:
  - `syn/ooc/pp_resource_gate.py --selftest`: PASS, with "unchanged acceptance schema, record and policy"
  - `pp_resource_gate_mutants.py`: the control passes and all 236 mutants fail
  - `pp_resource_gate.py check-baseline`: PASS, 3 endpoints

**Environment note.** The four Markdown-renderer gates (`check_em_dash`, `gen_toc` x3) first reported "pinned Markdown renderer not installed". I installed the pinned `tools/markdown/requirements.txt` (`--require-hashes`) into a private venv under `scratch/` and reran them; all four pass. That first failure was in the host, not in the candidate.

## 3. Signed local CI packet (owner 2026-10-14)

Packet: `review-evidence/787-r1/local-ci/455a3953` at `1aa019b6`. Copies are in `receipts/signed/`.

1. **Key.** `allowed_signers` has exactly 1 line, principal `milan-local-ci`, `namespaces="milan-local-ci"`. Its key fingerprint is `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`, which is the required key.
2. **Signature.** `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` returns rc 0 with `Good "milan-local-ci" signature` (`receipts/signed/verify.log`). The `manifest.json` sha256 is `9b290e11eef07de6a279ff91aa3497dfc63e8032abf6dc911136c8c282c79c0c`, as required.
3. **Subject and coverage** (`receipts/signed/verify_fields.txt`):
   - The subject names candidate `3ae30dc3…`, candidate parent `e5b8405d…`, candidate tree and head tree `43d18533…`, head `455a3953…`, PR 822, repository `kebag-logic/milan-fpga`. The schema is `milan-local-ci/act-1` and the result is `success`.
   - Coverage: all 47 entries have `ok: true`. 46 are covered by act. `rtl/physical-gptp` is `not-run`, with a named reason: it runs only on schedule or dispatch, and it is not hardware evidence.
   - Act: exit 0. Every job is `success` except the schedule-only `rtl-full/Physical gPTP (nightly and manual)`, which is `skipped`.
   - Banks: `full-native` ran 5/5 commands with rc 0, and `manager-builder` ran 48/48 with rc 0. Both banks exit 0.
   - The `definitions` sha256 of all four workflow files match this candidate's `.github/workflows/{docs,elaborate,rtl-fast,rtl}.yml`, for both the candidate and the head.
4. **Hosted checks** at `455a3953` (read-only, `receipts/hosted_checks_455a3953.tsv`): 68 check runs. 67 completed `success`, and 1 completed `skipped` (the schedule-only physical gPTP run). This is the manager's to accept; I record it here only as corroboration.

## 4. Prior public findings (read after the independent pass)

| Prior finding | Severity; lens | Status at `3ae30dc3` |
|---|---|---|
| R731-6 MD-1: criss-cross history; GitHub DIRTY; the act classifier exits 128 | manager condition; Robustness, Tests | **Resolved.** `merge-base --all` prints one base (`e5b8405d`). The GitHub PR API reports `mergeable: true`, `mergeable_state: clean`. My offline replay of the act-path `changes` step (`rtl-fast.yml:50-58`) against `origin/dev = e5b8405d` gives base `e5b8405d` and merged tree `43d18533`, lists 63 changed files and classifies `true` with rc 0 (`receipts/probe_act_classifier.txt`, `scripts/probe_act_classifier.sh`). |
| R731-6 MD-2: `act_runner` label did not match a reproducible base | manager condition; Tests | **Resolved.** The new packet records `act_runner: e5b8405d` for head `455a3953`. That head has a single merge base with that runner's dev tip, so the recorded `changes: success` can be reproduced (probe above). |
| R731-3 F1 = R732-3 F1; R732-3 F2 | MINOR (earlier) | Resolved since `cbc7c604`. The tree is identical. |
| R731-7 RES-1 = R732-7 R1 (and R731-6 RES-1, R731-5 RES-1, R732-5 F1, R731-4 RES-B/RES-C, R732-4 R1): the PR body predates the dev merges | RESIDUE; Docs | **Retained** as RES-1 below. The body is still stale. |
| R731-4 RES-A: body "that file is not part of this PR" | RESIDUE; Docs | **Retained** (part of RES-1). It still wraps across lines in the current body. |
| R732-4 R2: `docs/reference/SUBMODULES.md:503` "this change" | RESIDUE; Docs | Retained. The bytes are unchanged; the line reads "That path lies outside this change." |
| R732-4 R3 = R731-4 RES-D/RES-E: `AREA_BUDGET.md:149-150`, `SUBMODULES.md:511-517`, re-pin route record pointer | RESIDUE; Docs | Retained (bytes unchanged). The fix is as given in R732-4 R3. |
| R731-1 F1 = R732-1 R2: `tb/verilator/reboot_ctrl/mutants.py:113-114`, a lane label and an issue-comment ID in a comment | RESIDUE; Docs | Retained. Blob `2528a927` is unchanged, and #746 tracks it. |
| R732-1 R1: `tb/tools/torture_campaign.py:3135-3139`, the link-down comment omits the egress wait | RESIDUE; Docs | Retained (blob `43b1fc40` unchanged). |
| R732-5 S1; R732-4 S1/S2/S3; R731-4 SUG-1/SUG-2; R731-3 S2/S3; R731-1 S1/S2; R732-1 S1/S2 (including `KL_reboot_ctrl.sv` blob `d2c74f47`) | SUGGESTION | Retained (optional). The bytes are unchanged. |

No prior MINOR or worse is open.

## 5. Findings this round

No BLOCKER, MAJOR or MINOR finding.

**Comment rule.** The composition delta, from the source-reviewed head `455a3953` and from the prior composition `808e64e3`, changes no tree byte. So no new comment instance is possible, and there is no new RESIDUE under the rule.

### RES-1 - RESIDUE - Docs (PR body) - PR #822 body (`receipts/pr822_body_at_review.md`) - the body still describes `cbc7c604` and the pre-merge order

- **Evidence:**
  - The Status section still reads "**REVIEW READY** at `cbc7c6043ebf…`. `787-reboot-reset` -> `dev` (`02ca829a`)".
  - The body says the PR "merges after" #826 and #820. Both are in dev (`8adf5c99`, `e5b8405d`).
  - It reads "**Gates at the head pass.**".
  - "that file is not part of this PR" is still present.
  - The Contents line says "carrying PR #826's commits" only.
  - Neither `86a349d5` nor `455a3953` is described.
- **Why RESIDUE:** the trees at `cbc7c604`, `455a3953` and `3ae30dc3` are identical. So every measurement, figure, gate result and clause claim in the body describes the same bytes. Only the head SHA, the dev SHA and the merge-order wording are stale.
- **Exact fix:**
  - Status: "**REVIEW READY** at `455a3953bf49efda23be4e73447a25b66a5c4bf7` (tree `43d18533`, identical to `cbc7c604`). `787-reboot-reset` -> `dev` (`e5b8405d`)."
  - Replace "merges after both" / "merges after it" with "PR #826 and PR #820 are merged into dev; the branch has one merge base with dev at `e5b8405d`."
  - Replace "**Gates at the head pass.**" with "**Gates at `cbc7c604` pass; the tree at `455a3953` is identical.**"
  - Delete "that file is not part of this PR".
  - Contents: "carrying PR #826's and PR #820's commits".
- **Verification:** the body names `455a3953` and `e5b8405d` and no longer says "merges after".

### SUG-1 - SUGGESTION - Tests (reproducibility) - `tools/markdown/requirements.txt` / `scripts/gen_toc_renderer.py`

The four Markdown-renderer gates fail closed with an install hint when the pinned renderer is missing. That behaviour is correct. A composition reviewer must build a private venv to run them. A one-line pointer in `CONTRIBUTING.md`'s local-gate list to the venv recipe would save a rerun. This is optional and outside the PR's scope.

## 6. Lens application (clean-lens lines)

```text
[R731] PASS Conformance - receipts/composition.txt (tree 43d18533 == 455a3953^{tree}); dev..candidate diff of hdl/milan/milan_datapath.sv, sw/litex/milan_soc.py, docs/design/AREA_BUDGET.md - the composition changes no byte relative to the source-reviewed head, so the 7.4.43 / Milan 5.4.5.2 / 5.6.3.3 behaviour judged by R731-7/R732-7 is exactly what merges; the predecessor hunks in the shared files are preserved
[R731] PASS RTL - hdl/milan/milan_datapath.sv, tb/verilator/milan_dp/Makefile and syn/yosys/rom_digests.tsv deleted-line audit against dev; check_rtl_source_lists.py, pp_srcs.py --check --selftest, check_port_contracts.py (port_docs.budget 2181/127/1771), check_sv_idiom.py; signed packet act elaborate/verilator/yosys jobs + hosted 67/68 success - the shared RTL files keep #813/#816/#821/#826 content and add only the KL_reboot_ctrl wiring; no source-list or port-census drift
[R731] PASS Robustness - receipts/probe_act_classifier.txt; git merge-base --all (one base); git diff --check rc 0; PR API mergeable_state clean - the earlier merge-mechanics hazard (R731-6 MD-1) is gone; the composition cannot change reset/backpressure/timeout behaviour because it adds no byte
[R731] PASS Tests - receipts/signed/{verify.log,verify_fields.txt} (key SHA256:dRI12…, Good signature, subject = 3ae30dc3/455a3953, 47/47 coverage ok, banks 5/5 and 48/48 rc 0, workflow definition hashes match); receipts/gates/SUMMARY.txt (51/51 rc 0 incl. ci_events --check/--selftest, ci_gate_workflows --check, generate_ci_evidence_pins --check, suite_shards --selftest, pp_resource_gate selftest/236 mutants/check-baseline) - every gate inventory and record shared with the predecessors is consistent on the candidate
[R731] PASS Docs - receipts/gates (docs_check, gen_toc --check/--verify-anchors/--selftest, check_em_dash --base e5b8405d 0/588, check_diagram_pngs, check_submodule_docs, check_solution_docs, check_doc_paths); AREA_BUDGET.md:143-150 and BUILDING.md:522-527 read against #820's text - shared docs tables, TOC and anchors are consistent; PR-body staleness is wording only (RES-1)
```

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition touches no byte. Source content was covered by R731-7 and R732-7 at `455a3953`. Shared-file hunk audit. | R731-8 (composition); R731-7, R732-7 (source) | `3ae30dc3fcd3d7b65e8e121d3e0596cc31abfe07` (tree `43d18533` = `455a3953`) |
| RTL | CLEAN | `milan_datapath.sv`, `milan_dp/Makefile`, `rom_digests.tsv` against dev; source-list, port-contract and idiom gates; signed act jobs | R731-8; R731-7, R732-7 | `3ae30dc3fcd3d7b65e8e121d3e0596cc31abfe07` |
| Robustness | CLEAN | Merge mechanics: one merge base, merge-tree, `diff --check`, act-classifier probe, PR mergeability | R731-8; R731-7, R732-7 | `3ae30dc3fcd3d7b65e8e121d3e0596cc31abfe07` |
| Tests | CLEAN (SUG-1 optional) | Signed packet (key, signature, subject, 47 coverage entries, banks, definition hashes); 51 gates; resource-gate mutants; hosted 67 success, 1 schedule-skip | R731-8; R731-7, R732-7 | `3ae30dc3fcd3d7b65e8e121d3e0596cc31abfe07` |
| Docs | CLEAN (RES-1 and retained RESIDUE go to the checklist) | docs_check, TOC/anchors, em-dash, diagrams, submodule/solution docs; AREA_BUDGET/BUILDING/SUBMODULES shared text; PR body | R731-8; R731-7, R732-7 | `3ae30dc3fcd3d7b65e8e121d3e0596cc31abfe07` |

## 8. Limits and pending manager duties

- **Limits:**
  - I ran no full parent, PP, gPTP, Yosys or builder bank, and no Docker or act. Execution evidence for those is the signed packet (act replay of `455a3953` and banks on `3ae30dc3`) and the hosted checks at `455a3953`.
  - Physical calibration was NOT RUN. Field skips and the schedule-only physical gPTP job are not hardware proof.
  - The signed packet's act replay ran the PR head, not the candidate commit. The two trees are byte-identical, so the replay applies to the merged bytes. Gates that depend on history, such as em-dash against a base, I ran myself on the candidate.
  - I did not re-judge the source design. It keeps the R731-7 and R732-7 lens verdicts, because the composition changes nothing those verdicts depend on.
- **Pending manager duties:**
  - Own the hosted and act acceptance at the merge turn.
  - If dev moves past `e5b8405d` before the merge, this candidate is stale and needs a new composition check.
  - Carry RES-1 and the retained RESIDUE (R732-4 R2, R732-4 R3, R731-1 F1 under #746, R732-1 R1) to the residue checklist.
  - Merge only with explicit maintainer authorization.
- **Clone state after probes** (`receipts/restore_check.txt`):
  - HEAD is `3ae30dc3`, and `write-tree` equals `43d18533`.
  - `git status --porcelain` is empty, and the worktree equals HEAD.
  - The gitlinks are `gptp-processor` `135afd04`, `protocol-processor` `a9e84b66` and `third_party/verilog-axis` `48ff7a7e`.
  - The probes ran in a disposable clone under `scratch/`.

R731-8 FINISHED

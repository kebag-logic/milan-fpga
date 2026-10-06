[R506] POSITIVE - exact head 618875364d864c9c2d9f7a74fcad66c2d3ceefee

# R506-4: composition review of the issue #665 lane FT merge-train candidate (PR #675)

Role: composition reviewer for the lane's internal review, in a cleared context. Scope: **composition acceptance only**.

- Candidate: merge commit `618875364d864c9c2d9f7a74fcad66c2d3ceefee`, tree `a7c029500f102da623ad7f28c0da3be77c105d6e`.
- Parent 1 is the #664 candidate `5615f52eb810c6104a8250b44004df3a2917cec8`. Its tree, `d6b6c595…`, equals live dev `16af003a22556fff8b4160ed7d80f3c908239688`.
- Parent 2 is the PR #675 source head `6ca834a782a1bd5574d44998c8e214cf16df3441`.
- The merge base of the two parents is `423ac5d910d09ab189b3acc39ae3ae1d10d50b19` (the PR #669 merge).

Verdict basis: the composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR or MINOR is open. One RESIDUE, R506-4-O1, is recorded. It sits outside the composition: it is a wording slip already present at the source head, and the merge did not touch the line.

## 1. Reconstruction (public state only)

- **Contract.** I read AGENTS.md (sections 3, 6 and 7), the CONTRIBUTING docs-gate sections and the docs/README map.
- **Issue #665.**
  - The body sets the scope: F0 to F5 and the rules while #664 is open.
  - Owner directive 6008744385 chose GoogleTest/GoogleMock, gcov coverage, a 100 % branch target, a ratchet, the tally listener and graded mutation arms.
  - The FT lane comment 6009234414 sets items 1 to 6, the gates, and "No RTL change".
  - The FT round comments are 6012062072, 6014362247 and 6015346011.
- **#664 authorities in the candidate.**
  - `docs/ARCHITECTURE_HW_SW_SPLIT.md:192-224` is §6, the verification boundary.
  - `docs/reference/FR_NFR.md:323` is NFR-SCOUT-03, `:328` is NFR-SCOUT-08, `:330` is §3.4.1, and `:393-427` is §3.4.2, the hooks.
  - `REQUIREMENTS.md:93` holds the filter additions, which wait for the contract lane after FT.
- **Diff and history.** I read `git diff 5615f52e..61887536`, which is 68 files, and each side's diff from the merge base: #664 has 42 files and FT has 68.
- **Public evidence.**
  - The review-start comment is 6021220602.
  - The public evidence tree `b7eb2edc…/review-evidence/665ft-r1` holds only the author's round-1 HANDOFF and PR-BODY.
  - Hosted checks: GitHub knows no commit `61887536` (HTTP 422), so this candidate has no hosted run. The PR head on GitHub is `6ca834a7`, ready, base `dev`.

## 2. Composition facts (receipts/merge_facts.txt, receipts/overlap_check.txt, receipts/gitlinks_by_rev.txt)

- `git merge-tree --write-tree 5615f52e 6ca834a7` gives `a7c02950…`, the candidate tree exactly. The merge is clean, with no hand resolution.
- **Files changed by both sides since the merge base: exactly four.** They are `docs/README.md`, `docs/design/MAILBOX_SPLIT.md`, `sw/firmware/ctrl/README.md` and `sw/firmware/ctrl_nvm/README.md`. This matches the manager's list.
- Each of the four is byte-identical to `git merge-file` of base, #664 and FT, with rc=0 and no conflict.
- Every line either side added is present in the candidate:

  | File | #664 lines | FT lines |
  |---|---|---|
  | `docs/design/MAILBOX_SPLIT.md` | 39 | 1 |
  | `docs/README.md` | 1 | 1 |
  | `sw/firmware/ctrl_nvm/README.md` | 8 | 42 |
  | `sw/firmware/ctrl/README.md` | 7 | 25 |

  That is 123 lines with 0 missing.
- The other 64 files FT changes are byte-identical between the FT head and the candidate. So the source reviews' artifacts carry over unchanged.
- The candidate changes the same file set relative to `5615f52e` as FT changes relative to the merge base.
- No submodule gitlink moves. All four gitlinks are identical at the base, both parents and the candidate:
  - external `efeb541a`
  - gptp-processor `5dce647a`
  - protocol-processor `ead80360`
  - third_party/verilog-axis `48ff7a7e`
- Relative to live dev, the candidate changes nothing under `hdl/`, `syn/`, `configs/`, `sw/builder/`, `sw/litex/` or `tb/` except FT's own `tb/verilator/mbx/suite.hpp` (receipts/scope_diffs.txt).

## 3. Semantic interaction review

**Shared docs: both sides kept.**
- `docs/README.md:76`: #664's "Review Mark II placement and timing" row stays in the review table. `:89`: FT's "Run or extend the firmware's host unit tests" row is in the Verification table. Two different tables, so no ordering clash.
- `docs/design/MAILBOX_SPLIT.md`: #664's text is all present: the placement preamble, the implemented-F0-filter paragraph with NFR-SCOUT-08, the F3 H-DISC paragraph, and the Service-latency lead-in ending "F0 does not prove that target-time budget" (`:375`). FT's `sw/firmware/gtest` row sits inside the intact Verification table, between the `sw/firmware/ctrl/test` row and the processor-walk row.
- `sw/firmware/ctrl/README.md:15-20`: #664's split-contract paragraph is kept. FT's GoogleTest arm table, the `unit` arm, the planted-defect text and the prerequisites follow it, unchanged from the FT head.
- `sw/firmware/ctrl_nvm/README.md`: #664's split-contract paragraph and "F0's merged HAL" seam line are kept. FT's GoogleTest suite description (53 checks in 85 tests per shape), the coverage-path list and "(106 defects)" are kept.

**No contradiction between FT's testing text and #664's rules.** I checked each §6 statement (`ARCHITECTURE_HW_SW_SPLIT.md:194-212`) against what FT ships in the candidate:
- *GoogleTest/GoogleMock, C11 code, `extern "C"`, and mocks of the mailbox HAL, flash port and lwSRP adapter.* The FT arm table (`sw/firmware/ctrl/README.md`, the `unit` row) names the `mbx_hal.h` and `shlan_port.h` mocks. The ctrl_nvm README names GoogleMock's flash port and command master.
- *Every exclusion needs a reason in the relevant test README.* The gate reads only `sw/firmware/gtest/README.md` §"Coverage exclusions" (`:221`, and `fw_coverage.py:81-88`), an FT-only file. #664 touched no README that the gate parses.
- *A ratchet refuses reductions.* `coverage.ratchet` holds 14 files, every one at 100 % lines and branches after the listed exclusions. `fw_coverage.py --check` returns PASS on the candidate.
- *The listener prints `checks: N   failures: M`.* The candidate's ctrl and nvm logs print that line for every arm.
- *Existing mutation arms remain graded.* #664's sentence "Existing mutation arms remain required" agrees with FT's `--self-test` text, which needs a `[FAIL]` that names the GoogleTest test.
- *lwSRP's upstream suites run unchanged at the pin.* FT's `gtest/README.md:380-386` defers them to F4, as lane item 6 directs. §6 states the obligation for Mark II software and does not tie it to FT.
- *"This document does not claim that FT has landed"* (`:212`). It stays a true non-claim once FT lands, and no #664 sentence claims FT is absent.
- *NFR-SCOUT-03 hooks.* §3.4.2 says the hooks "are not claims of implemented instrumentation or passing target timing". #664's README paragraphs call the service budget "an integration obligation, not a target-time result established here". FT's text adds no service-time, NFR or hook claim: no hit for latency, budget, NFR or hook in `sw/firmware/gtest/README.md`. FT keeps F0's existing statement of the mailbox-access bound per path unchanged, and MAILBOX_SPLIT's #664 lead-in classes that bound as conditional F0 evidence.
- *Ingress filter.* FT does not touch `sw/mailbox/mailbox.yaml` or its generated outputs. #664's text leaves the filter additions to the contract lane after FT. `gen_mailbox.py --check --crosscheck` passes.

**Cross-side readers: none.**
- No FT reader depends on a #664 non-Markdown file. The firmware gates read `tb/adp_engine/sim_main.cpp` (in the PP submodule), `hdl/adp/pp_adp_pkg.sv`, `tb/verilator/mbx`, `tb/common` and `tb/verilator/nvm_backend`, and #664 changes none of them.
- The basename hits `sim_main.cpp` and `milan_datapath.sv` are different files, or ci_scope selftest rows.
- FT's `ci_events.py`, `ci_scope.py`, `rtl-fast.yml` and `CI_WORKFLOWS.md` do not encode #664's milan_dp inventory.
- #664's new `scripts/measure_test_evidence_readers.py` and `tb/verilator/milan_dp/*` files are classified by directory, and the classifier and contract self-checks pass on the candidate.

## 4. Gates run on the candidate (receipts/static_candidate/, receipts/firmware_candidate/)

All return 0. Thirty-two static gates (`scripts/run_static_gates.sh`, 16-way parallel, the pinned Markdown renderer from `tools/markdown/requirements.txt` in a disposable venv):

| Group | Gates and results |
|---|---|
| Documentation | `docs_check.py`: 0 findings, 197 md files<br>`check_em_dash.py --base 5615f52e`: 0 findings over 494 added lines in 6 pages, arms 339/339<br>`check_em_dash.py --selftest`<br>`check_doc_style.py`<br>`check_doc_paths.py`<br>`DOC_MAP.gen.py --check`<br>`check_solution_docs.py`<br>`check_submodule_docs.py`<br>`check_gptp_docs.py`<br>`check_feature_status.py`<br>`check_archive.py`<br>`check_todo_ownership.py` |
| TOC and anchors | `gen_toc.py --selftest`<br>`gen_toc.py --verify-anchors`: 383 cross-page fragment links reproduced<br>`gen_toc.py --check`: 137 pages |
| Module matrix | `gen_module_matrix.py --check`: 77 modules, 0 untested |
| Test evidence | `measure_test_evidence.py --check`: PASS, 0 unexplained DUT readers, 3 <= 3 wall-clock files<br>`measure_test_evidence.py --selftest` |
| Idiom and code-quality ratchets | `check_hygiene.py --check`<br>`check_cpp_idiom.py`<br>`check_py_idiom.py`<br>`check_sh_idiom.py`<br>`measure_naming.py --check`<br>`measure_fail_fast.py --check`<br>`check_port_contracts.py`<br>`check_baremetal_only.py --check` |
| CI contract | `ci_events.py --check`: 1741 contract items<br>`ci_events.py --selftest`<br>`ci_scope.py --selftest`: PASS |
| Mailbox contract | `gen_mailbox.py --check --crosscheck` |
| Firmware harness self-tests | `fw_coverage_selftest.py`<br>`tally_selftest.py` |

The `firmware-unit` job's gates, run locally on the candidate (GoogleTest 1.18.0 from the host package):

| Gate | Result |
|---|---|
| `test_ctrl_firmware.py` | PASS. Every arm prints its tally. The rv32 arm is not required here. |
| `test_ctrl_nvm.py --jobs 8` | OK across 5 shapes, 434 tests. rv32 built at 83.333 MHz and 100 MHz. |
| `fw_coverage.py --selftest` | 28/28 |
| `fw_coverage.py --check --jobs 8` | PASS, 14 files |

## 5. Findings

No BLOCKER, MAJOR or MINOR is attributable to the composition.

**R506-4-O1 (RESIDUE, outside the composition).**
- Lens: Docs.
- Location: `sw/firmware/ctrl/README.md:25`.
- What is wrong: the contents entry says "The seven arms". FT's arm table in the same file now has eight rows: model, port, unit, adp, walk, entity, rv32 and lwsrp.
- Evidence: the base `423ac5d9` had seven arms and the same words. FT added `unit` and left this label alone. The FT head `6ca834a7` and the candidate both carry the line. #664 does not touch it, so the composition neither introduced nor altered it.
- Impact: the prose label miscounts the table. No gate reads the count, and no measurement, test, figure or claim depends on it.
- Exact fix: change "The seven arms" to "The eight arms" on that line. Re-run `gen_toc.py --check`, which keeps label text that the page's author supplied.
- Verification: `grep -n 'eight arms' sw/firmware/ctrl/README.md` returns line 25, and the TOC gate passes.

## 6. Reviewer-owned completion ledger (composition)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The composition touches this lens's scope: #664's requirement text and FT's testing claims now sit together. Examined `docs/ARCHITECTURE_HW_SW_SPLIT.md:192-224`, `docs/reference/FR_NFR.md:323,328,393-427`, `REQUIREMENTS.md:93`, `docs/design/MAILBOX_SPLIT.md` (the filter paragraph, the H-DISC paragraph and `:375`), `sw/firmware/ctrl/README.md:15-20`, `sw/firmware/gtest/README.md:221,380-386` and `sw/firmware/gtest/coverage.ratchet`. Each §6 rule matched against FT's shipped behaviour (section 3), with no contradiction. | R506-4 (this round) | `618875364d864c9c2d9f7a74fcad66c2d3ceefee` |
| RTL | CLEAN | The composition does not touch this lens's scope. Against live dev the candidate changes nothing under `hdl/`, `syn/` or `configs/`, and under `tb/` only FT's `tb/verilator/mbx/suite.hpp` (receipts/scope_diffs.txt). Gitlinks are unchanged (receipts/gitlinks_by_rev.txt). FT's RTL-lens coverage is banked by the source reviews R506-3 and R507-3 at `6ca834a7`, whose 64 non-shared files are byte-identical in the candidate. #664's `hdl/milan/milan_datapath.sv` is dev's blob, reviewed in its own lane. | R506-3 and R507-3 (source); R506-4 confirms no composed change | `6ca834a782a1bd5574d44998c8e214cf16df3441` (an ancestor of the candidate; nothing in the lens's scope touched since); composition check at `61887536` |
| Robustness | CLEAN | The composition does not change any input the firmware gates read (section 3, cross-side readers). Checked on the candidate anyway: `test_ctrl_firmware.py`, `test_ctrl_nvm.py` across 5 shapes, and `fw_coverage.py --check` and `--selftest`, all rc 0 (receipts/firmware_candidate/). Failure paths in the firmware tests are covered by the source reviews R506-3 and R507-3. | R506-4 (composition); R506-3 and R507-3 (source) | `618875364d864c9c2d9f7a74fcad66c2d3ceefee` |
| Tests | CLEAN | Composed gate inventories and the classifier: `ci_scope.py --selftest`, `ci_events.py --check/--selftest`, `measure_test_evidence.py --check/--selftest` (with #664's new readers module), the idiom ratchets, `tally_selftest.py`, `fw_coverage_selftest.py`, and the four `firmware-unit` gates. All rc 0 on the candidate (receipts/static_candidate/SUMMARY.tsv, receipts/firmware_candidate/). | R506-4 (this round) | `618875364d864c9c2d9f7a74fcad66c2d3ceefee` |
| Docs | CLEAN | The four shared files: three-way identity, and the survival of all 123 lines either side added (receipts/overlap_check.txt). Gates: `docs_check.py`, `check_em_dash.py --base 5615f52e`, `gen_toc.py --selftest/--verify-anchors/--check`, `gen_module_matrix.py --check`, `DOC_MAP.gen.py --check`, `check_doc_paths.py` and `check_doc_style.py`, all rc 0. The anchors `#6-verification-boundary`, `#341-…` and `#342-…` resolve. RESIDUE R506-4-O1 is recorded and does not affect coverage. | R506-4 (this round) | `618875364d864c9c2d9f7a74fcad66c2d3ceefee` |

## 7. Prior public review findings on this PR

I read these only after the independent pass, the verdict and the ledger above were written. Sources: PR #675 conversation comments 6011948437 (R506-1), 6012056114 (R507-1), 6014209924 (R507-2), 6014356451 (R506-2), 6015612359 (R507-3) and 6015762631 (R506-3).

**Why the source dispositions carry over.** Every artifact these findings name is in an FT-only file, except the ctrl_nvm README text of R506-2-F1. FT-only files are byte-identical between `6ca834a7` and this candidate (receipts/overlap_check.txt: 0 of 64 differ). The ctrl_nvm README text survives the merge verbatim (`sw/firmware/ctrl_nvm/README.md:450`, "each guard pinned at its exact end"). So each disposition below holds at `61887536`.

| Finding | Lenses (as published) | Disposition at `61887536` |
|---|---|---|
| R506-1-F1, reachable pool exclusion | Conformance, Robustness, Tests, Docs | **RESOLVED.** Resolved at R506-2. The coverage gate passes here with 14 files at 100 %, and `fw_coverage.py --selftest` passes 28/28. |
| R506-1-F2, tally line not asserted | Conformance, Tests (+Robustness, Docs per R507-1) | **RESOLVED.** Resolved at R506-2. `tally_selftest.py` passes 18 of 18 here. |
| R506-1-F3, toolchain not printed | Docs | **RESOLVED.** Each candidate firmware log prints `toolchain:` on line 2 (receipts/firmware_candidate/). |
| R506-1-S1, R506-1-S2 | Tests, Docs; Robustness | **RESOLVED** at R506-2. The files are unchanged here. |
| R507-1-F1, R507-1-F2 (MAJOR) | Conformance, Robustness, Tests, Docs | **RESOLVED.** Resolved at R506-2, with the F1 remainder carried as R506-2-F1 and resolved at R506-3. `fw_coverage.py` and `coverage.ratchet` are unchanged here. |
| R506-2-F1, loaded-prefix guard not pinned at its exact end | Conformance, Robustness, Tests | **RESOLVED.** Resolved at R506-3. `test_nvm_codec.cpp` is unchanged, and the README text is kept at `:450`. |
| R506-2-F2, ADP exclusions rest on an unstated premise | Conformance, Tests, Docs | **RESOLVED.** Resolved at R506-3. `sw/firmware/gtest/README.md:262-267` still marks the rows as resting on #678. |
| R506-2-F3, listener behaviours not planted | Tests, Docs | **RESOLVED.** Resolved at R506-3. The tally self-test passes 18 of 18 here. |
| R506-2-S1 | Docs | **RESOLVED** at R506-3. |
| R506-3-S1, crash-case exit status unpinned | Tests | **RETAINED as SUGGESTION.** The files are unchanged, and it does not affect the verdict. |
| R506-3-S2, suite loop skipping the last-registered suite escapes | Tests | **RETAINED as SUGGESTION.** The files are unchanged, and it does not affect the verdict. |
| R506-1-R1 / R507-2-R1 / R506-2-R1 / R506-3-R1 / R507-3-R1, stale hosted-status sentence in the PR body | Docs (RESIDUE) | **RETAINED as RESIDUE.** The live PR body still says "The round-3 head has no hosted run" (Status, and Known limitations at body lines 21 and 416-417). The exact fixes are as published in R506-3-R1 and R507-3-R1. This is PR prose, not tree content, and the composition does not affect it. |

No prior finding is reopened by the composition.

## 8. Real limits

- **No hosted run exists for the candidate:** GitHub has no commit `61887536`. Hosted and act acceptance belong to the manager at the merge turn.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Not run here:**
  - the full builder, parent, PP, gPTP and Yosys banks, and any Verilator suite (no RTL is composed);
  - both mutation campaigns (`--self-test`) and `tally_selftest.py --mutants`;
  - the ctrl `lwsrp` arm.

  The manager reports builder 48/48 and native 5/5 at this candidate, and the source mutation campaigns ran at `6ca834a7`.
- **rv32 builds.** The ctrl rv32 arm ran unrequired. The nvm gate built rv32 here, but without `--require-rv32`.
- **No baseline counts.** I did not reproduce the test-evidence ratchet counts at the two parents: archived trees lack initialised submodules. The candidate passes the gate.
- **Hidden conflicts.** A semantic conflict in a file neither side touched would show only through the gates above.
- **No fault or mutation probes were planted in the clone.** After all runs the clone is at the exact head with a clean index and worktree, no untracked files, and unchanged gitlinks (receipts/integrity.txt). The `external` submodule is not initialised in this clone, as at the start.

## 9. Pending manager duties

- Rebuild the final current-dev candidate at the merge turn, and confirm it still equals this tree, or re-review if dev moved.
- Hosted acceptance (`rtl-fast` including `firmware-unit`, the docs workflow, `verilator-suites` and `yosys-portability` as applicable) and act on the exact merged head.
- Carry RESIDUE R506-4-O1 to the residue checklist.
- Candidate-merge validation and post-merge containment under CONTRIBUTING. A maintainer must explicitly authorize the merge.

R506-4 FINISHED

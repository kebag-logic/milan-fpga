[R533] POSITIVE - exact head 135cc8eee08aa4bea55965e897a0887178bc7448

# R533-15: composition review of the #665 F4 merge-train candidate (PR #690)

- **Subject:** merge-train candidate `135cc8eee08aa4bea55965e897a0887178bc7448`, tree `f0780a31280924c73fa225bf0bd6d70c93eb4cae`. Parents: live dev `17f62ef64a66562384e8a93b1d6be6f86e51f95c` and PR #690 head `fe1cd0679f5028c749af7242c903a82ca2b3d692`.
- **Role:** [R533], cleared-context composition reviewer. Scope is composition acceptance only. The source head already carries two POSITIVE source reviews: R532-14 ([6056144852](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6056144852)) and R533-14 ([6056271554](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6056271554)).
- **Verdict:** POSITIVE. The composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR, MINOR or RESIDUE is open. One optional SUGGESTION is recorded.
- **Process:** I made no source fix, commit, push, GitHub write, merge or hardware operation, and used no Docker or act runner. All probes ran in disposable scratch. Section 7 records the restore proof.

## 1. Reconstruction

I read the following in order:

1. AGENTS.md and CONTRIBUTING.md (sections 6 and 7, and the documentation gates).
2. docs/README.md.
3. The #665 body and the F4 assignments and decisions on the issue, through round 14 (6055458854).
4. The authorities that the overlapping artifacts cite:
   - `docs/design/MAAP_FABRIC.md#annex-b-contract`;
   - `hdl/ieee1722/maap/KL_maap.sv:126-169` (the probe draw);
   - `sw/firmware/ctrl/app/ctrl_app.h:58-76` (the pass bounds).
5. `git diff 17f62ef6..135cc8ee` and the history from the merge base `99e4eb6c`.
6. The hosted check runs at the exact head.

I wrote the independent verdict before reading the source reviews' finding sections (`receipts/independent_verdict_before_prior_findings.txt`). One disclosure: a search of the PR and issue threads for the manager's candidate-bank comments displayed the opening paragraphs of five early-round reports (R533-1, R532-1, R532-2, R533-2, R533-3). Those reports concern source defects at older heads, which were later resolved. They did not inform this composition verdict.

## 2. Composition facts

- **The merge is clean and exact.** `git merge-tree --write-tree 17f62ef6 fe1cd067` reproduces the candidate tree `f0780a31…` byte for byte, so no manual resolution was made (`receipts/composition_diff.txt`).
- **Predecessors in the candidate.** Dev gained two PRs after F4's last dev merge `99e4eb6c`:
  - #694 (#654, SoC CPU option refusals);
  - #695 (#686, fabric MAAP Annex B).
  
  These are the only predecessors. No other queued PR is in this candidate.
- **One file overlaps.** Of the 60 paths the PR changes and the 24 paths dev changed since `99e4eb6c`, only `sw/firmware/ctrl/maap/README.md` is common. The two hunks are disjoint:
  - F4 changes one line, `:134` (`CTRL_APP_PASS_MAX` becomes `CTRL_APP_THREE_PASS_MAX`, R532-8-F3).
  - #686 rewrites `:170-189`, the differential deviations, which became equalities.
  
  The candidate differs from dev on this page by exactly the F4 line, and from the PR head by exactly the #686 hunk.
- **The PR touches none of the differential's inputs.** It changes none of `maap/maap.c`, `test/test_maap_differential.cpp`, `test/maap_differential.py`, `hdl/ieee1722/maap/KL_maap.sv`, `ctrl_build.py` or `fw_gtest.py`.
- **The PR changes no RTL, testbench or synthesis files.**
- **Dev changes no file in F4's workflow, runner or registry set:**
  - `.github/workflows/*`;
  - `scripts/ci_events.py`, `scripts/act_ci.py`, `scripts/check_submodule_docs.py`;
  - `.gitmodules`;
  - `docs/testing/CI_WORKFLOWS.md`;
  - `sw/firmware/gtest/coverage.ratchet`.
- **Semantic touch points.** The gates in section 3 checked each of these:
  - the test-evidence reader registry, which gained a `tb/verilator/maap/mutants.py` entry from dev while F4 adds SRP mutation drivers;
  - docs anchors into `MAAP_FABRIC.md` (rewritten by #686) and `FR_NFR.md` (one dev line);
  - the docs map, TOC and em-dash added-line judgement over both sides;
  - the `ci_events` workflow pins, which F4 changed in rtl-fast's firmware-unit step.

### Merged `maap/README.md` coherence

- **Both edits are kept.**
- **The pass figures match the headers.** `:131-135` states 616/664 for a standalone pass and `CTRL_APP_THREE_PASS_MAX` = 1,580/1,659. A scratch compile of the candidate headers at MBX_N_IF=1 and 2 prints:
  - three-way 1580 and 1659;
  - MAAP 616 and 664;
  - four-way 3224 and 4073.
  
  Receipt: `receipts/passmax_probe.log`, script `passmax_probe.sh`. The four-way 3,224 agrees with `docs/design/MAILBOX_SPLIT.md:715`.
- **The probe draw matches the RTL.** `:189` gives the parent's 518..581 ms probe draw, which matches `KL_maap.sv:126-128` and `MAAP_FABRIC.md:89`.
- **The core text agrees with #686.** `:21-22` (initial PROBE plus three retransmissions, so four PROBEs) agrees with #686's "Four PROBEs, the first at Begin!" at `:175`.
- **The remaining claims hold.** `:182-192` (frames equal; residual deviations behind the `#annex-b-contract` anchor; parent probe bound and count controls) matches `maap_differential.py`'s `parent-probe-bound` and `parent-probe-count` plants.
- **No PR page describes the parent engine.** No F4-changed page describes the parent fabric engine's pre-#686 deviations: I searched for 627, 5.047, "three delayed" and "parent MAAP" across MAILBOX_SPLIT, ctrl/README, srp/README, gtest/README and CI_WORKFLOWS.

## 3. Executed evidence at this exact head

All runs used `TMPDIR` under the packet's scratch directory and the pinned simulator wrapper `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator` ("Verilator 5.050 2026-07-01 rev v5.050", wrapper sha256 `905795b9…`). RV32 used `riscv64-elf-gcc`. The lwSRP submodule was materialised at its gitlink `9197193e` and de-initialised afterwards. Scripts: `run_gates.sh` and `run_campaign.sh`. Each gate has its own `receipts/<name>.log` and `.rc` file.

| Gate | rc | Result |
|---|---|---|
| `maap_differential.py --self-test` | 0 | Unmutated 12/12 tests PASS; 16/16 differential plants caught, including `parent-probe-bound` and `parent-probe-count` |
| `test_ctrl_firmware.py --require-rv32 --jobs 4` | 0 | 46/46 arm verdicts PASS, including MAAP Annex B (37), H-MAAP at IF=1 (12) and IF=2 (13), lwSRP port, SRP mailbox and composition arms, and RV32 objects |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` (the composed rtl-fast firmware-unit step) | 0 | Control plants 471/471 caught; 237 SRP plant verdicts (full table plus the IF=1 subset) all caught; both lwSRP pin controls caught; zero escapes |
| `fw_coverage.py --check --jobs 4` | 0 | 22 files at 100% lines and branches |
| `docs_check.py` | 0 | 0 findings over 200 md files |
| `gen_toc.py --verify-anchors` / `--check` / `--selftest` (pinned renderer) | 0 | 411 cross-page anchors reproduced; TOC OK; 1501/1501 arms |
| `check_em_dash.py --base 17f62ef6` and `--base 99e4eb6c`, plus `--selftest` | 0 | 0 findings over 525 and 741 added lines; 339 arms |
| `ci_events.py --check` / `--selftest` | 0 | 1741 contract items OK |
| `measure_test_evidence.py --check` / `--selftest` | 0 | Ratchet PASS: 0 unexplained DUT-source readers; the dev `maap/mutants.py` entry is classified |
| `check_doc_paths`, `DOC_MAP --check`, `check_doc_style`, `check_solution_docs`, `submodule_boundaries --check`, `check_submodule_docs` (and its selftest), `check_diagram_pngs`, `check_feature_status`, `gen_module_matrix --check`, `check_baremetal_only`, `measure_naming`, `check_port_contracts`, `measure_fail_fast`, `check_todo_ownership`, `check_hygiene`, `check_cpp_idiom`, `check_py_idiom`, `check_sh_idiom` | 0 each | See the individual receipts |

Note: the first attempts at the four renderer-dependent commands exited 2 because the pinned Markdown renderer was absent from the host. I installed it from `tools/markdown/requirements.txt` (hash-locked) into a private scratch venv and reran the commands. Their log and rc files hold the reruns (`receipts/run_gates.summary`).

**Hosted evidence (inspected, not owned).** The candidate `135cc8ee` is not on GitHub, so it has no hosted runs. At the PR head `fe1cd067`, every executed context completed successfully: rtl-fast, firmware-unit, docs-check, docs-check-no-git, verilator-suites (5 shards), yosys-portability (4 shards), full-ci-gate, wire-accountability and the others. The "Physical gPTP (nightly and manual)" context was skipped, which is not hardware proof.

**Bank coverage question (manager note).** By repository content, `sw/builder/test_builder.py` and `scripts/run_all_suites.sh` invoke neither `test_ctrl_firmware.py` nor `maap_differential.py`. The ctrl suite and campaign run in rtl-fast's firmware-unit job, and the MAAP differential runs in no workflow. So a builder 48/48 / native 5/5 receipt covers them only if the manager's bank invokes them explicitly. This review ran both at the candidate (above). See S1.

## 4. Findings

**R533-15-S1 | SUGGESTION | Tests | `sw/firmware/ctrl/maap/README.md:160-168`; `.github/workflows/*` (no reader of `maap_differential.py`)**

- **Evidence:** The F2 MAAP differential is the only executable check that the parent fabric engine's frames equal the core's. #686 turned its recorded deviations into equalities, and this candidate is where F4's composition first meets them. No workflow or named bank runs the differential, so its passing at a merge candidate depends on someone invoking it by hand.
- **Impact:** None at this head: it passes 12/12 with 16/16 plants caught. A later RTL change to `KL_maap.sv` could regress the equality unobserved.
- **Optional outcome:** Either name `maap_differential.py --self-test` in the manager's candidate bank, or open an Issue to wire it into a hosted job.
- **Verification:** A bank receipt or workflow step that runs it.

No other finding. No RESIDUE.

## 5. Prior public findings at this head

I read these after the independent pass.

- **R532-14 and R533-14 (POSITIVE at `fe1cd067`)** leave no BLOCKER, MAJOR, MINOR or RESIDUE open.
- **R532-8-F3** (the three-module attribution at `maap/README.md:134`): retained RESOLVED at the candidate. The composed line `:134` still reads `CTRL_APP_THREE_PASS_MAX`, and the figures compute (section 2).
- **Composition-neutral findings.** Every other prior finding is retained with its R533-14 disposition. Dev changes no artifact those findings name (`srp_*`, `acmp.*`, `ctrl_app_srp.c`, `act_ci.py`, `MAILBOX_SPLIT.md`, `CI_WORKFLOWS.md`, lwSRP pin), so the composition cannot reopen them.
- **SUGGESTIONs R532-12-S1, R532-14-S1 and R532-14-S2:** optional, unaffected.
- **R532-8-F1 hosted half:** remains a manager duty.

## 6. Reviewer-owned lens ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `maap/README.md:21-22,131-135,170-192` against `KL_maap.sv:126-128`, `MAAP_FABRIC.md:89` and `#annex-b-contract`, and `ctrl_app.h:58-76`; `receipts/passmax_probe.log`; `receipts/maap_differential_selftest.log` | R533-15 | 135cc8eee08aa4bea55965e897a0887178bc7448 |
| RTL | CLEAN (composition touches no RTL; the only RTL interaction is the differential built from `KL_maap.sv` against F4's tree, rerun here) | `receipts/composition_diff.txt` (no hdl/tb/syn path from the PR); `receipts/maap_differential_selftest.log`; RV32 freestanding objects in `receipts/ctrl_suite.log`. Unchanged F4 RTL-lens scope is covered by R532-14 and R533-14 at `fe1cd067` | R533-15 | 135cc8eee08aa4bea55965e897a0887178bc7448 |
| Robustness | CLEAN (no behaviour-bearing file overlaps; the composed firmware and campaign rerun) | `receipts/ctrl_suite.log` (refusal, stall, link-loss and backlog arms at IF=1/2); `receipts/ctrl_campaign.log`. F4's robustness scope is covered by R532-14 and R533-14 at `fe1cd067` | R533-15 | 135cc8eee08aa4bea55965e897a0887178bc7448 |
| Tests | CLEAN (S1 is optional) | `receipts/ctrl_campaign.log` (471/471, 237 SRP verdicts, 2 pin controls); `receipts/fw_coverage_check.log`; `receipts/maap_differential_selftest.log`; `receipts/test_evidence.log`; `receipts/ci_events_check.log` | R533-15 | 135cc8eee08aa4bea55965e897a0887178bc7448 |
| Docs | CLEAN | Merged `sw/firmware/ctrl/maap/README.md` (both hunks); `receipts/docs_check.log`, `toc_anchors.log`, `toc_check.log`, `em_dash_base.log`, `em_dash_base_mergebase.log`, `doc_paths.log`, `doc_map.log`, `submodule_docs.log` | R533-15 | 135cc8eee08aa4bea55965e897a0887178bc7448 |

## 7. Restore proof

- HEAD and tree are unchanged.
- The `git ls-files -s` fingerprint before and after is identical: `e370f846…c96b`.
- The worktree and index both equal HEAD.
- `git submodule status` is identical to the start: lwSRP gitlink `9197193e` (de-initialised again), protocol-processor `2ad2f845`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`, external `efeb541a`.
- I removed the bytecode caches the gate runs created.
- Receipts: `receipts/restore_verify.txt`, `receipts/index_before.sha256`, `receipts/submodules_before.txt`.

## 8. Real limits

- **No source bank at this head.** No manager source bank exists here, and none is claimed or inferred. Source-head execution evidence is the author's published receipts.
- **Banks not run here.** I did not run the builder bank, the native, parent, processor, gPTP or Yosys banks, the saved-state campaign, the linked-image auditors, act, or the act_ci selftest. No receipt here covers them at the candidate, and they remain the manager's merge-turn duty.
- **No hosted runs for the candidate.** The hosted evidence inspected is for `fe1cd067` only.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Ratchet note.** The test-evidence ratchet passes with "70 <= 77" and reports that it could be lowered. That is an informational tightening opportunity, not a failure.

## 9. Pending manager duties

- The current-dev merge-candidate builder and native banks at the merge turn, with receipts linked on the PR. Also confirm whether those banks invoke the ctrl suite and the MAAP differential (S1).
- Hosted and act acceptance, including the hosted half of R532-8-F1 and the act replay with the lwSRP manifest entry.
- Candidate-merge validation and post-merge containment under CONTRIBUTING.

R533-15 FINISHED

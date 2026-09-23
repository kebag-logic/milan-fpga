[R262] POSITIVE - exact head 5fbb02202f165c7c53a1207432e67dbc7dbb5968

Round R262-3, composition acceptance for issue #74 (ledger item 2) / PR #528.
Candidate `5fbb02202f165c7c53a1207432e67dbc7dbb5968`, tree `d5bc65c7fa99581a18d3f3b25ebb01b78c4f0344`.
Parents: live `dev` `759da623072358afdb0e9d570a7b4b6a788492c9` and PR head `2accfadfd3d4d8a318e3e714ee0dc87fc84e4164`.
PR merge base: `ede8d48ecd7c7f589a14b957951f040d92c99c70`.

Verdict: the composed tree introduces no defect beyond the reviewed sources. No finding.

## 1. What the composition is

- Predecessors in the candidate: PR #526 (`07d85dac`) and PR #521 (`759da623`), the two `dev` first-parent merges after the PR's merge base.
- The candidate tree equals an independent `git merge-tree --write-tree 759da623 2accfadf`: `d5bc65c7`, no conflict (`receipts/merge_tree_recompute.txt`).
- The 12 PR paths and the 22 predecessor paths share exactly one file: `docs/testing/TESTING.md` (`receipts/pr_files.txt`, `receipts/pred_files.txt`).
- Every other PR path is byte-identical to the PR head, and every other predecessor path is byte-identical to `dev` (`receipts/blob_provenance.txt`).
- Candidate vs `dev` differs in exactly the 12 PR paths; candidate vs PR head differs in exactly the 22 predecessor paths.
- No `hdl/` path, no submodule gitlink and no RTL build list changed on the predecessor side.
- The four gitlinks are identical on both parents and the checkouts sit at their pins (`receipts/state_before.txt`).

### 1.1 The shared file

`docs/testing/TESTING.md` (`receipts/testing_md_threeway.diff`):

- The predecessor side adds the cancellation and hard-stop paragraphs, now at candidate lines 210-255. It adds no heading.
- The PR side rewrites one suite-table cell, the `tb/verilator/media_grid_align` row, now at candidate line 475.
- The hunks are disjoint. Candidate vs `dev` is exactly the PR row. Candidate vs PR head is exactly the predecessor paragraphs.
- Probe P2 (`receipts/probe_P2_testing_md_loss.txt`): no gate notices either side's hunk going missing, so the three-way blob evidence above is what proves this file. It holds.

### 1.2 Semantic interactions checked

| Interaction | Predecessor artifact | PR artifact | Evidence at this head |
|---|---|---|---|
| Sweep driver runs the PR suites | `scripts/run_all_suites.sh:119` now re-enters under `owned_process.py`; `prepare_logs`; cancellation preflight | `tb/verilator/media_grid_align/Makefile` (3 extra builds, 3 negative controls), `tb/verilator/chmap_capture` | Both suites run the way the candidate sweep runs one suite: `owned_process.py -- timeout 1800 make -C`, then `suite_tally.py --verdict` (`scripts/run_all_suites.sh:398`). `media_grid_align` rc 0, 45 checks, 150 s. `chmap_capture` rc 0, 204 + 20 checks, 58 s. Verdict recogniser rc 0 on both logs, although the negative-control lines echo `[FAIL] G7`/`[FAIL] G9`. Tally 269 checks, 0 failures (`receipts/suites/`) |
| Suite budget | `suite_timeout()` default 1800 s (`scripts/run_all_suites.sh:243`) | `media_grid_align` runtime grows with G7-G9 and two mutants | 150 s measured, well inside 1800 s |
| Suite inventory and shard pins | `scripts/ci_events.py:1905` pins `chmap_capture` to worker 3; `scripts/suite_shards.py:186` | no suite added or removed | 56 suite Makefiles identical at `dev` and candidate; both touched suites land in shard 3/5; `suite_shards.py --selftest` and `ci_events.py --check`/`--selftest` pass (`receipts/suite_inventory.txt`) |
| Test-evidence registry | `scripts/measure_test_evidence.py:603` adds a DUT-reader disposition | new mutants and arms in two suites | `--check` PASS (74 <= 77, 0 <= 0 unexplained DUT readers); `--selftest` pass |
| Generated module matrix | `tb/verilator/gptp_shadow/*` changed | `docs/traceability/MODULE_MATRIX.md`, `hdl/ieee1722/aaf/README-tests.md` regenerated for the `media_grid_align` reader | `gen_module_matrix.py --check`: up to date, 69 modules. Probe P1 puts `dev`'s two generated files back under the PR's test inventory and the gate refuses them as STALE (rc 1); restored rc 0 (`receipts/probe_P1_module_matrix.txt`) |
| Em-dash provenance | `CONTRIBUTING.md`, `CI_WORKFLOWS.md`, `BAREMETAL_FIRMWARE.md`, `TESTING.md` lines | 6 changed Markdown pages | `--base 759da623` (the base CI derives for this candidate): 0 findings over 54 added lines in 6 pages. `--base ede8d48e`: 0 over 351 lines in 10 pages. Self-test 57/57 arms |
| Contents blocks and anchors | `CONTRIBUTING.md` Contents entry reworded; `tb/verilator/gptp_shadow/README.md` gains a heading | intra-page links only (`#arms`, `#boundaries`, `#the-negative-control`, ...) | `gen_toc.py --check` OK (106 pages); `--verify-anchors` 147 links reproduced; `--selftest` pass |
| Docs workflow step contract | `docs.yml` +3 steps (47), `elaborate.yml` +2 steps (20), both pinned in `ci_events.py` | no workflow change | `ci_events.py --check` OK, 1631 items; `--selftest` PASS, 2183 arms |
| RTL-reading gates | none of their inputs changed by predecessors | `KL_media_grid_align.sv`, `KL_chan_map_capture.sv` | `lint_rtl.py --check` 90 <= 90; `xvlog_gate.py --check` PASS, 0 `hdl/` findings; `check_rtl_source_lists.py` OK; `check_sv_idiom.py`, `check_port_contracts.py`, `measure_naming.py --check`, `pp_srcs.py --check` pass |

All 44 static gate commands exit 0 at this head (`receipts/gates/gates.tsv`, one log per command).

## 2. Findings

None. No BLOCKER, MAJOR, MINOR or SUGGESTION is raised by this round.

## 3. Lens ledger (reviewer-owned)

| Lens | Composition touches scope? | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | No. No requirement, clause or acceptance artifact changed on the predecessor side; every PR path is the PR-head blob | CLEAN | `receipts/blob_provenance.txt`. The item-2 acceptance arms re-executed at this head: `media_grid_align` G7 (0 dups, 0 skips over 8 x 0.2 s, clearance 15 cycles, held frame 1 dup, surplus frame 1 skip), G8 (0/0, clearance 14), G9 (one dup slow, one skip fast) | Source: R262-2 and R263-2 (both POSITIVE). Composition identity: R262-3 | Source `2accfadf`, an ancestor of this head whose Conformance scope nothing on the `dev` side touched; identity and arms at `5fbb0220` |
| RTL | No. No `hdl/` path, gitlink or RTL source list changed on the predecessor side | CLEAN | `hdl/ieee1722/crf/KL_media_grid_align.sv:117,147,182-186,267` and `hdl/ieee1722/aaf/KL_chan_map_capture.sv:521-551` at blobs `cc418322`/`a46611c4`, identical to the PR head; `receipts/gates/39-lint_rtl_check.log`, `40-xvlog_gate_check.log`, `22-rtl_source_lists.log`, `31-sv_idiom.log`, `25-port_contracts.log` | Source: R262-2 and R263-2. Composition identity and RTL gates: R262-3 | Source `2accfadf`; gates at `5fbb0220` |
| Robustness | No. Same identity as RTL | CLEAN | Held-frame, surplus-frame and passage arms and the three negative controls re-executed at this head, each RED on its own arm: `MGA_MUT_U_SIGN` fails G2, `MGA_MUT_NO_KEEPOFF` fails G7 (5203 dups), `MGA_MUT_COIN` fails G9 (11 dups) (`receipts/suites/media_grid_align.log:223-230`) | Source: R262-2 and R263-2. Composition re-execution: R262-3 | Source `2accfadf`; re-execution at `5fbb0220` |
| Tests | Yes. The predecessors changed the sweep driver, the test-evidence registry and the pinned CI step contract | CLEAN | `scripts/run_all_suites.sh:119,243,398`; `scripts/measure_test_evidence.py:603`; `scripts/ci_events.py:1905`; `scripts/suite_shards.py:186`; `receipts/suites/` (owned-process runs, verdict recogniser, tally); `receipts/suite_inventory.txt`; `receipts/gates/28-test_evidence.log`, `35-ci_events_check.log`, `36-ci_events_selftest.log`, `42-suite_shards_selftest.log` | R262-3 | `5fbb02202f165c7c53a1207432e67dbc7dbb5968` |
| Docs | Yes. `docs/testing/TESTING.md` is changed by both sides, and the Contents, anchor, em-dash and generated-matrix gates read the composed tree | CLEAN | `docs/testing/TESTING.md:210-255,475` (`receipts/testing_md_threeway.diff`); `receipts/gates/01-03` (em-dash), `05` (docs_check, 0 findings over 164 md + 848 text files), `06`, `16`, `19-21`, `17`, `18`, `09-15`; probes P1 and P2 | R262-3 | `5fbb02202f165c7c53a1207432e67dbc7dbb5968` |

## 4. Real limits

- **This result is for this candidate only.** It is `dev` `759da623` plus PR head `2accfadf`. If `dev` moves before the merge, the candidate changes and this composition check must be redone on the new one.
- **No hosted run has executed the composed tree.**
  - The hosted check-runs on `2accfadf` were triggered at 15:15:10Z (`receipts/hosted_timing.txt`).
  - PR #526 landed at 15:26:50Z and PR #521 at 15:51:58Z, so those `pull_request` runs composed the PR with `ede8d48e`.
  - In particular, the `elaborate` job's new RV32 SDK install and `--require-rv32` builder gate from PR #521 have not run with this PR's RTL.
  - Executed hosted contexts at `2accfadf` all concluded success; `Physical gPTP (nightly and manual)` is a skipped context, not evidence (`receipts/hosted_checkruns_prhead_2accfadf.tsv`).
- **Not run in this round:**
  - full parent, protocol-processor, gPTP, Yosys and builder banks;
  - act and hosted CI;
  - the `milan_dp` legs;
  - physical calibration.
  Field skips are not hardware proof, and #74 ledger items 1 and 4 remain bench lines.
- **The manager's bank at this head has no public receipt yet.** I found none for `5fbb0220` on the `74-review-evidence` branch (tip `1c4e97d2`) or in the issue and PR comments at review time. This verdict does not rely on it.
- **Parallelism.** It was bounded by an 8-CPU affinity mask. The Makefiles' own Verilator `-j 0` was not edited.
- **Tools.** Scoped Verilator identified as `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/suites/verilator-version.txt`).
- **Commit `5fbb0220` is local only.** It does not exist on the remote.

## 5. Pending manager duties

- At the merge turn, build the current-`dev` candidate and gate it with the full local bar of CONTRIBUTING section 2.1 step 7, recording both object IDs. If `dev` is still `759da623`, the merge tree must equal `d5bc65c7`.
- Own hosted/act acceptance on the composed tree. That includes the `elaborate` RV32 path and the 47-step `docs-check` job that PR #521 introduced.
- Publish the static/builder/native bank receipts for this head.
- After merge, run containment (`scripts/check_merge_containment.py`). Keep #74 open for items 1, 3 and 4 (the PR says `Relates to #74`). Carry the recorded VERSION/release-note item.

## 6. Prior public findings on this PR

Pending: this section is written after the verdict and ledger above.

## 7. Restoration

- Probes P1 and P2 edited tracked files in the worktree only, and each was restored with `git checkout --`.
- Build outputs were removed with each suite's `make clean`.
- The before and after snapshots are identical (`receipts/state_before.txt`, `receipts/state_after.txt`, `receipts/state_compare.txt`). They cover HEAD, tree, index records, worktree bytes against index blobs, modes, the four gitlinks with checkouts at their pins, and an empty porcelain status.

R262-3 FINISHED

[R373] POSITIVE - exact head 0ba810fea6a994e6dc8ba927c0c94c6fe24ae5a3

# R373-4: composition review of the #395 / PR #605 merge-train candidate

- **Candidate:** `0ba810fea6a994e6dc8ba927c0c94c6fe24ae5a3`, tree `702a78ea93c7519566a903f8d0dbb2205f21c58b`.
- **Parents:** `7d29909d` (the train after #577 / PR #612) and `895be307` (the PR #605 source head, with R372-4 POSITIVE at that head and R372-3 and R373-3 POSITIVE at its branch parent `3b5603e3`).
- **Scope:** composition acceptance only. The question is whether the composed tree adds any defect beyond the reviewed sources. The #395 frozen items 1, 2 and 5 apply, under the owner grade decision (comment 5789765635), the margin decision and its correction (5860418611, 5860783553) and the merge-dev rules (5866780445, 5867242613). Items 3 and 4 stay open ("Relates to #395").
- **Method:** I worked in a cleared context from public state only: AGENTS/CONTRIBUTING, docs/README, the issue body and comments, the diff and history, the public evidence branch, and a snapshot of hosted check state. I read prior public review findings only after my own pass and ledger.

**Verdict: POSITIVE.** The composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR, MINOR or new SUGGESTION is open. All five lenses are covered clean at `0ba810fe`.

## 1. Composition identity (`receipts/01_composition_identity.txt`, `03_source_vs_candidate.txt`, `04_pr_owned_blobs_and_loop_union.txt`)

- **The tree reproduces exactly.** `git merge-tree --write-tree 7d29909d 895be307` gives `702a78ea…`, which equals the candidate tree. The merge bases are `54ce8773` and `9c180685`.
- **The PR's own patch is carried unchanged.** The PR's patch against the dev tip it merged (`1fa2357f..895be307`, 12 files, +673/-15) equals the candidate delta (`7d29909d..0ba810fe`) line for line. The only differences are two hunk offsets in `sw/builder/test_builder.py`, caused by #577's 240 inserted lines.
- **Ten of the twelve PR-owned paths are byte- and mode-equal to the source head:**
  - the record and the findings index;
  - BUILDING, RUNNING_TESTS and LITEX_SOC;
  - `test_timing_grade.py`, `ax7101_timing.py`, `alinx_ax7101.py`, `timing_grade.tcl` and `report_timing_grade.py`.
- **The files shared with a predecessor are exactly the two the manager named.** Of the paths #577 (and the train since `1fa2357f`) changed, only these overlap with this PR:
  - `sw/litex/milan_soc.py`: #577 adds `validate_shipping_image` in `build_desc_image` (`:3359`, `:3369-3373`). #395 derives the PLL speed grade at `:229` and edits the comment at `:219-221`. The regions are disjoint, and nothing else in `sw/litex/` differs from the source head.
  - `sw/builder/test_builder.py`: #577 adds the gate-36b block (`:27232-27467`) and four loop entries. #395 adds `test_commercial_timing_grade` (`:27795-27803`) and one loop entry (`:27815`).

## 2. Assigned composition checks

### (a) Both `milan_soc.py` changes run in the composed build path without reordering or masking each other

`probe_composed_build_path.py` drives the real composed `milan_soc.main()` for the shipping `endstation_ax7101_1x1_tdm8` builder-emitted argv, run with the LiteX interpreter. Only `Builder.build` is replaced, by a recorder, so no software compile or Vivado runs. The result is rc 0 (`receipts/60_probe_composed_build_path.log`).

**Positive run:**

- The call order is exactly `validate` then `build`. The checked bytes (7352 B, CRC32 `0x93742dd2`) are the bytes bound as `MILAN_AEM_IMAGE_CRC32`/`_BYTES` and later written as `aem_desc.bin`. No image exists on disk when the build step starts (`milan_soc.py:3955-3964`, `:4010`, `:4018-4019`).
- The platform part is `TIMING_GRADE["part"]`.
- The pre-placement commands contain `configure_commands()` contiguously: `source {…/timing_grade.tcl}` and `kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}`.
- The first post-route command is `kl_timing_grade_reports candidate_signoff`.
- The PLL is constructed with `speedgrade=-2`, which is derived from the part.

**Negative run:** a planted `ImageCheckError` raises `RuntimeError("aem_desc.bin: planted composition refusal")`. The build step is never reached and no `aem_desc.bin` is written, even though the #395 hooks are already installed on the platform.

**Conclusion:** the image check still refuses before CRC binding, before the build and before the write. The #395 hooks are installed at platform construction (`milan_soc.py:3792`) and run inside Vivado after routing. Neither change reorders or masks the other.

### (b) The corner reports still derive from the #582 contract clock

- In the same probe, the PLL outputs are `sys` 100 MHz, `milan` 50 MHz, `sys4x`/`sys4x_dqs` 400 MHz and `idelay` 200 MHz. The `milan` domain equals the recipe `CPU_HZ` (50 MHz, `tb/verilator/nvm_capture_cpu/recipe.py`), and the #582 contract check (`milan_soc.py:3713-3716`) passes on the shipping argv.
- `timing_grade.tcl` names no clock. Its reports analyse the design's generated clocks, which come from this PLL plan.
- The candidate does not change this path relative to the source head: `sw/litex` differs only by #577's six lines.

### (c) The composed `test_builder.py` has no collision and runs both sets

- **No collisions.** There are no duplicate top-level `def`s and no duplicate loop entries.
  - The `[gate 36b]` labels belong to #577 only. The timing gate prints `[timing grade]` and has no gate number.
  - `_litex_or_skip("timing grade platform")` is unique.
  - Evidence: `receipts/02_builder_collision_check.txt`.
- **Exact union.** The `__main__` loop (`:27815-27892`) has 95 entries, exactly the union of the source loop (91) and the predecessor loop (94) (`receipts/04_…`, `UNION_EXACT`).
- **Both sets run in both bank modes.** Each bank log shows all 95 function headers and the 3 `[timing grade]` lines. It also shows 67 `[gate 36b]` lines from the four #577 functions. No skip line names either set.
- **Only unrelated skips.** Present mode records only the gate 11 historical Arty calibration report. Absent mode records that plus the expected compiler-dependent gate 1b stand-down. Neither is coverage.

### (d) Each half still bites in the composed tree

`probe_mutations.py` runs on a disposable export and restores from git, verifying the tree is clean after each arm. The result is rc 0 (`receipts/61_probe_mutations.log`).

| Arm | #577 `test_soc_shipping_image_contract` | #395 `test_commercial_timing_grade` |
|---|---|---|
| control | pass | pass |
| #577 check removed from `build_desc_image` | **fail** (`gate 36b: empty rates accepted; missing L10_EMPTY`) | pass |
| #395 PLL grade restored to literal `-2` | pass | **fail** (`call(speedgrade=-2)`, changed-part control) |
| both removed | **fail** | **fail** |

## 3. Gates run on the candidate

All results below are rc 0. Logs are in `receipts/`, with start and end times, wall time and rc in each.

- **`python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration`:** rc 0, 788.0 s. The last line is `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, historical report), and the required-elaboration verdict passes (`10_builder_present.log`).
- **Compiler-absent full bank:** rc 0, 575.4 s (`11_builder_absent.log`). It ran on a byte-identical copy of the candidate via `scripts/run_builder_absent.py`, which:
  - hides exactly the three RV32 cross candidates;
  - keeps `--require-elaboration`;
  - asserts that every hidden candidate was probed.
- **Static gates:** 38 commands, all rc 0 (`static_gates_summary.txt`). Markdown gates used the pinned environment `md-venv-40cdefe08ebd`, whose hash matches `tools/markdown/requirements.txt`.
  - `docs_check.py`: 0 findings across 174 md files.
  - `gen_toc.py --selftest`, `--verify-anchors` and `--check`.
  - `check_doc_paths.py`.
  - `check_em_dash.py --base 7d29909d` (the candidate's first parent): 0 findings over 306 added lines in 5 pages. Its `--selftest` ran 339 arms.
  - `check_doc_style` and `check_solution_docs`, each with its self-test. `check_feature_status` and its self-test.
  - `check_baremetal_only.py --check`: 0 findings across 924 files. Its `--selftest` also passed.
  - `ci_events.py --check`: 1655 contract items. Its `--selftest` also passed.
  - `ci_scope.py --selftest`, plus a classification of the composition's file list: `true`, so the PR is RTL/tooling relevant.
  - `check_py_idiom` and its self-test; `check_hygiene --check` and `--selftest`.
  - `measure_test_evidence --check` (ratchet PASS) and `--selftest`.
  - `check_todo_ownership`, `DOC_MAP.gen.py --check`, `check_archive`, `check_soc_sources`, `check_gptp_docs` and `check_submodule_docs`.
  - `iob_pack_selftest`, and the `check_sweep_shape`, `check_deploy_shape` and `check_entity_shape` self-tests.
  - standalone `test_timing_grade.py <litex-python>` (three arms).
  - `git diff --check` against `7d29909d` and against `2180c73e`.
- **Environment note.** Gates 25 and 26 (`check_em_dash`) first ran under the system interpreter. They stopped with rc 2, "cannot judge: pinned Markdown renderer not installed". This was an environment refusal, not a verdict. Both were re-run in the pinned environment, and the retained logs are those re-runs.

## 4. Semantic interactions examined

- **Citations.** I found no line-number citation into a shared file that drifts.
  - The record cites `milan_soc.py:1520-1534` and `:1550-1556` pinned at `66001a30`, so they are immutable. #577's insertion is at `:3359+` in any case.
  - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:99,341` name `build_desc_image` by symbol, not by line.
  - `CODE_QUALITY.md:1582-1583` cite `test_builder.py:1439/1557`, which lie above both insertions.
- **Registries and pins.** The `ci_events` contract, the `ci_scope` routing, the test-evidence ratchet, `rom_digests.tsv` and the protocol-processor gitlink (`c951a9ff`, from the train) are all consistent.
  - The composition adds no workflow or record pin.
  - The PLL grade is unchanged at -2, so no ROM or digest input moves.
- **Docs tables and anchors.** Composing both sides adds no table row, and `docs/findings/README.md` is byte-equal to the source head. The TOC and anchor gates pass over the union tree.
- **Import-time coupling.** #577's `from sw.builder import aem_image_checks` is imported lazily inside `build_desc_image`. It therefore does not affect `test_pll_grade`'s `import milan_soc`. #577's `_soc_image_emitter` extracts only `build_desc_image`, so the #395 platform hooks do not reach it.

## 5. Findings

No BLOCKER, MAJOR, MINOR or new SUGGESTION.

**Out-of-scope observation (for triage; not attributed to this composition).** `scripts/lint_rtl_policy.py:70` cites `sw/litex/milan_soc.py:528` for `axis_resetn`. That line is already stale at `7d29909d` (it points into the `pp_srcs` loader). Neither side of this composition introduces or changes it.

## 6. Prior public findings (read after my own pass)

| Finding | Status at `0ba810fe` | Evidence |
|---|---|---|
| R372-1 F1 (MAJOR) = R373-1 F1; R372-1 F2, F3 (MINOR) | Resolved in rounds 2 and 3; unchanged | Record, BUILDING, RUNNING_TESTS, LITEX_SOC and `test_timing_grade.py` blobs equal to `895be307` (`receipts/04_…`). The timing arms pass in both banks |
| R372-2-F1 = R373-2 R2-F1 (BLOCKER), bare-metal scope gate | Resolved; re-verified on the composed tree | `check_baremetal_only.py --check` rc 0 (0 findings, 924 files) and `--selftest` rc 0 |
| R372-3 S1–S4, R373-3 S1–S4, R372-4-S1 and older retained SUGGESTIONs | Retained as SUGGESTIONs | The files involved (the record, `test_timing_grade.py`, `docs/BUILD_FLASH_BOOT.gen.py` and `docs/findings/README.md`) are unchanged by the composition |

None of the retained items is MINOR or above.

## 7. Reviewer-owned ledger

Every lens is touched by the composition in at least the shared build path or the shared test file, so each was applied to the candidate. Content that exists only in the source is additionally covered by the source reviews: R372-4 at `895be307`, and R372-3 and R373-3 at `3b5603e3`.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #395 items 1, 2 and 5 in the composed tree. The part and conditions flow from `ax7101_timing.py` into the platform (`alinx_ax7101.py:298-305`) and the PLL (`milan_soc.py:229`). The #577 refusal runs before binding, build and write (`milan_soc.py:3369-3373`, `:3955-4019`). Merge rule 3: the corner reports derive from the #582 contract clock (`receipts/60_…`) | R373-4 | `0ba810fea6a994e6dc8ba927c0c94c6fe24ae5a3` |
| RTL | CLEAN | `milan_soc.py:216-265` `_CRG` in the composed tree: `speedgrade=-2` from the declared part, and exact 100/50/400/400/200 MHz outputs with `milan` = `CPU_HZ` (`receipts/60_…`). The composition delta has no HDL. The predecessor's pp_shadow/gitlink changes are its own, and the PR's files are byte-equal to source (`receipts/03_…`, `04_…`). `timing_grade.tcl` is unchanged | R373-4 | `0ba810fea6a994e6dc8ba927c0c94c6fe24ae5a3` |
| Robustness | CLEAN | A planted image refusal on the composed `main()` stops before the build step and before any write, with the timing hooks present (`receipts/60_…`). The mutation arms show that each half's removal is caught only by its own gate, and both together are caught by both (`receipts/61_…`). The absent-compiler bank runs both sets (`11_…`) | R373-4 | `0ba810fea6a994e6dc8ba927c0c94c6fe24ae5a3` |
| Tests | CLEAN | `test_builder.py:27232-27467`, `:27795-27803` and `:27815-27892`. There are no duplicate defs, loop entries, gate numbers or labels, and the loop union is exact at 95. Both full banks returned rc 0, with all 95 functions executed, the timing and gate-36b arms run and no skip in either set (`receipts/02_…`, `04_…`, `10_…`, `11_…`) | R373-4 | `0ba810fea6a994e6dc8ba927c0c94c6fe24ae5a3` |
| Docs | CLEAN | The PR's docs are byte-equal to the source head (`receipts/04_…`), and citation drift was checked (section 4). The docs gates pass over the union tree: docs_check, doc paths, TOC selftest/anchors/check, em-dash against the parent, style, solution docs, feature status, DOC_MAP, archive and bare-metal scope (`receipts/2*_…`–`5*_…`) | R373-4 | `0ba810fea6a994e6dc8ba927c0c94c6fe24ae5a3` |

All five lenses are covered clean at the candidate head, with no BLOCKER, MAJOR or MINOR open under any lens.

## 8. Real limits

- **No Vivado run.** No synthesis, implementation or routed-timing run was made. The corner numbers in the record belong to the fixed `9e9954e9` checkpoint, and the composition changes neither that checkpoint nor its record. The post-route hook was shown to be installed, not executed.
- **The build step was stubbed.** The build-path probe replaces `Builder.build`, so firmware compilation and bitstream generation were not exercised through `main()`. The full banks cover their own elaboration arms.
- **Verilator was not used.** The composition delta carries no HDL, so the scoped Verilator binary was not needed and its identity was not checked.
- **The banks ran detached.** Each full bank takes longer than a single foreground call allows. So each ran as a detached logged process, while this session stayed in blocking foreground waits until both exited. Neither was left running.
- **No hosted evidence exists for the candidate.** `0ba810fe` is not on the remote (HTTP 422). The hosted snapshot at the PR source head `895be307` (`receipts/70_hosted_checks_snapshot.txt`) shows:
  - success: `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `yosys-elaboration`, the four Yosys shards, Verilator shards 0, 2 and 3, `verilator-lint`, `bdd-conformance`, `wire-accountability`, `changes` and `full-ci-gate`;
  - in progress: Verilator shards 1/5 and 4/5;
  - skipped: Physical gPTP, which is not hardware evidence.
- **The manager's source banks were not re-read.** I did not re-examine the manager's source-bank receipts beyond noting them. My own two banks ran on this candidate.
- **No physical evidence.** Physical calibration was not run, and field skips are not hardware proof. Items 3 and 4 remain open.
- **This is not the final candidate.** The review covers this merge-train candidate. The final current-dev candidate (live dev `7a7582f0`) will be built at the merge turn and needs its own validation.

## 9. Pending manager duties

- Build and validate the final current-dev candidate, and repeat the composition check if dev moved into either shared file.
- Hosted exact-head completion for the PR head (Verilator shards 1 and 4 were still in progress at the snapshot), the act replica, the ready-state exhaustive gates, merge authorisation (`--partial`), and post-merge containment.
- The PR stays "Relates to #395". Retained SUGGESTIONs and the out-of-scope observation in section 5 go to optional triage.

## 10. Receipts and reproduction

All scripts are under `scripts/` and take paths as arguments:

- `run_logged.sh <log> <dir> <cmd…>`
- `run_static_gates.sh <repo> <receipts> <markdown-python> [jobs]`, which runs the `static_gates.txt` list
- `run_builder_absent.py <repo>`
- `probe_composed_build_path.py <repo> <work>`, run with the LiteX interpreter
- `probe_mutations.py <disposable repo>`
- `verify_restore.sh <repo> <head> <tree>`

The probes and the absent bank ran only on disposable copies under `scratch/`. That directory is not published.

**Restore verification** (`receipts/90_restore_verification.txt`), after removing only the ignored byproducts my own runs created (bytecode caches, `sw/builder/out/` and two generated hex files, all timestamped after this review started):

- HEAD and tree are exact;
- status, including ignored files, is empty;
- index entries equal the HEAD tree (954 entries);
- all 950 non-gitlink tracked files re-hash to their blobs with matching modes;
- the gitlinks `gptp-processor 5dce647a`, `protocol-processor c951a9ff` and `third_party/verilog-axis 48ff7a7e` are initialised and clean;
- `external efeb541a` is not initialised, as before (`receipts/00_pre_state.txt`).

Every published file is listed in `MANIFEST.sha256`.

R373-4 FINISHED

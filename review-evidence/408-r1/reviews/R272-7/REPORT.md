[R272] POSITIVE - exact head 4487359031b52b0b92e526839473f2e9c956c967

Round R272-7: composition review of issue #408 and #409, PR #535.
The candidate is the merge-train commit `4487359031b52b0b92e526839473f2e9c956c967`, tree `5b0645c82cf9930675c87c14340800dd7aaabf82`.
Its parents are live `dev` `573f0052a0e4412e81f0845438fcec2086ce5d55` and PR head `062e89ad098806ae5def8341fcb8c2815583ca00`.
Scope: composition acceptance only. The source content of PR #535 was reviewed at the source heads named in the ledger.
All five lenses were applied to the composed tree. There are no findings at any severity.

## 1. What the composition is

Receipt: `receipts/composition-identity.txt` (script `scripts/composition_identity.sh`).

- **Predecessor set: empty.** The candidate's first parent is `573f0052`, which `git ls-remote` shows is the live `refs/heads/dev`. The second parent is `062e89ad`, the live `refs/pull/535/head`. No queued PR sits between them.
- **The candidate is the clean merge.** `git merge-tree --write-tree 573f0052 062e89ad` gives `5b0645c8`, the candidate tree. No conflict was resolved by hand.
- **The candidate adds nothing beyond its two sides.** The stable patch-id of `dev..candidate` equals that of `merge-base..PR` (`5ececc7e…`). The patch-id of `PR..candidate` equals that of `merge-base..dev` (`0ec9b18e…`). The merge base is `759da623`, with 87 commits on the dev side and 11 on the PR side.
- **Hosted runs cover this exact tree.** GitHub's own merge ref for PR #535 is `175568934fb6c77e9eb9389a847d37cebb8ab390`. Its parents are `573f0052` and `062e89ad` and its tree is `5b0645c8`, the same tree (`receipts/hosted/github-merge-ref-commit.json`). Hosted `pull_request` runs check out that ref (`receipts/hosted/docs-check-job107790356062-excerpt.log`: `HEAD is now at 175568934`).

### Files both sides change

The PR changes 3 files. Only one of them also changed on the dev side:

| File | PR side | Dev side | Composed result |
|---|---|---|---|
| `docs/integration/BAREMETAL_FIRMWARE.md` | +/- 677 lines | unchanged | byte-identical to `062e89ad` |
| `sw/builder/test_builder.py` | +/- 4846 lines, gate 1b only | unchanged | byte-identical to `062e89ad` |
| `docs/testing/CI_WORKFLOWS.md` | hunk `-1129 +1129,2` (gate 1b compiler-absent sentence) | `20b7bdaa`, `3f2fe73d`: hunk `-1753,0 +1754,8` (containment verdicts) | lines 1-1125 byte-identical to `dev`. Disjoint hunks. |

### Other ways the two sides meet

These go through files that only one side changed:

1. **Gate 1b reads RTL that dev changed.** The PR's gate 1b elaborates RTL mutants against the real `milan_dp` source closure, taken from `tb/verilator/milan_dp` `make print-srcs` (`sw/builder/test_builder.py:11380-11400`). It also reads `hdl/milan/milan_datapath.sv` (`sw/builder/test_builder.py:3048`, `:3056`).
   - Dev changed `milan_datapath.sv` (+212/-88) and the `milan_dp` Makefile (+77/-5).
   - Dev also changed 5 more closure files: `KL_chan_map_capture.sv`, `KL_talker_diag_ctx.sv`, `KL_crf_rx.sv`, `KL_mmcm_drp_servo.sv`, `KL_media_grid_align.sv`.
   - Dev changed the three product YAMLs, in a comment line only.
   - The firmware directory `sw/firmware/milan_baremetal/` and the rest of `sw/builder/` are unchanged on the dev side.
   - Receipt: `receipts/gate1b-dev-inputs.txt`.
2. **The Contents and em-dash gates were rewritten on dev.** They now read Markdown through the pinned cmark-gfm renderer (`scripts/gen_toc.py`, `scripts/gen_toc_renderer.py`, `scripts/check_em_dash.py`, `tools/markdown/requirements.txt`). The PR's 677-line page was checked at its source under the old reader. It is now judged by the new one.
3. **`ci_events.py` pins `CI_WORKFLOWS.md`.** Dev changed `scripts/ci_events.py` (docs-check step count 47 to 49) and `.github/workflows/docs.yml` (renderer install). `ci_events.py --check` reads the shared page.
4. **Ratchets are tree-wide.** The Python idiom, fail-fast, hygiene, test-evidence and TODO ratchets count over the whole tree. Dev added Python files (`gen_toc_renderer.py`, `gen_toc_shape_cases.py`, `merge_containment_selftest_linear.py` and others). The PR's `test_builder.py` counts against the same limits.
5. **Links go into pages dev changed.** The PR's page links to `../testing/CI_WORKFLOWS.md#elaboration`, which is at line 1018 of the composed file. No line the PR adds cites a line number in any file the dev side changed.
6. **Merged-in wording.** None of the lines dev added mentions gate 1b, `#408`, `#409`, the retired rules, `BAREMETAL_FIRMWARE` or `test_builder`. So no dev text restates a rule the PR retires.

## 2. Gates run on the candidate

All gates were run in the candidate clone, read-only (`PYTHONDONTWRITEBYTECODE=1`).
The Python was a disposable virtual environment carrying the hash-locked `tools/markdown/requirements.txt` and PyYAML 6.0.3.
Exit codes are in `receipts/gates/gates.tsv`, one log per gate beside it. The script is `scripts/run_composition_gates.sh`.

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | rc 0: 0 findings, 165 md + 858 scrubbed files, scrub self-test 23/23 |
| `scripts/check_em_dash.py --base 573f0052` (the candidate's parent) | rc 0: 0 findings over 507 added lines in 2 pages, arms 339/339 |
| `scripts/check_em_dash.py --base 759da623` (merge base) | rc 0: 0 findings over 2213 added lines in 37 pages |
| `scripts/check_em_dash.py --selftest` | rc 0 |
| `scripts/gen_toc.py --selftest` / `--verify-anchors` / `--check` | rc 0 / 0 / 0: 165 cross-page fragment links reproduced, 107 pages OK |
| `scripts/check_doc_style.py` (+ `--selftest`) | rc 0 / 0 |
| `scripts/check_doc_paths.py` | rc 0: 841 cited paths resolve |
| `docs/DOC_MAP.gen.py --check`, `docs/traceability/gen_module_matrix.py --check`, `scripts/check_feature_status.py`, `scripts/check_archive.py` | rc 0 each |
| `scripts/ci_events.py --check` / `--selftest` | rc 0 / 0: 1647 contract items across 4 workflows and `CI_WORKFLOWS.md` |
| `scripts/check_baremetal_only.py --check` / `--selftest` | rc 0 / 0: 0 findings, 856 files (#408 acceptance 5) |
| `scripts/check_py_idiom.py` | rc 0 (too many parameters 7 <= 7, every other count at 0 <= 0) |
| `scripts/check_hygiene.py --check`, `scripts/measure_fail_fast.py --check`, `scripts/measure_test_evidence.py --check`, `scripts/check_todo_ownership.py` | rc 0 each. The test-evidence ratchet reports 74 <= 77. |
| `git diff --check 573f0052 HEAD` and `git diff --check 759da623 HEAD` | rc 0 / 0 |

### Focused gate 1b on the composed tree

Receipts: `receipts/focused/`. The runner is `scripts/run_gate1b_focused.py`, which calls only `test_baremetal_profile_contract()`.

- **Tools.** Verilator is the scoped 5.050 wrapper, which reports `Verilator 5.050 2026-07-01 rev v5.050`; wrapper sha256 `905795b9…`. sv2v is v0.0.13. The RV32 compiler is the local `riscv32-linux-gcc` (Buildroot 2026.05, GCC 14.3.0). Identities are in `receipts/focused/tool-identity.log` and the gate's own compiler line.
- **`--require-rv32`: rc 0 in 417 s** (`gate1b-sdk.log`, `gate1b-sdk.rc`).
  - `280/280 mutations rejected on the safety property they break`. That is 280, not below the 163 floor of #408/#409 acceptance 4.
  - `46/46 RTL mutation variants elaborated as the real option-on milan_datapath or milan_csr top`. These are elaborated against dev's changed datapath and Makefile.
  - `4/4` reset and `20/20` object-list spellings.
  - The `TEXT RULES + INSTRUMENTS` arm graded.
  - The 23 `[gate 1b]` lines match the source-head author log line for line. The only differences are the compiler's ISA string and how that compiler lowers float and double struct-overlay stores. Both come from the local compiler, not from the composition.
- **Compiler-absent control.**
  - `sw/builder/test_firmware_compiler.py --selftest`: rc 0.
  - `--absent`: rc 0 in 330 s, `GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations` (`gate1b-absent.log`, `rv32-absent.jsonl`).
- **Hosted run on the same tree.** The docs-check job on the same tree printed `3 NOT RUN`. Two of them are local to that runner: `no Verilator on this runner` and the `MAKEFLAGS += -e` construct. Both ran here.

### Hosted runs

Receipt: `receipts/hosted/check-runs-062e89ad.tsv`, recorded only.

- These succeeded on the merge ref with tree `5b0645c8`: `docs-check`, `docs-check-no-git`, `rtl-fast`, `elaborate`, `verilator-suites` (5 shards), `yosys-portability` (4 shards), `yosys-elaboration`, `verilator-lint`, `bdd-conformance`, `wire-accountability` and `full-ci-gate`.
- `Physical gPTP (nightly and manual)` is **skipped**. It is not evidence.
- The docs-check job's builder step ran gate 1b with the pinned hosted compiler (Buildroot 2021.11-18033-g83947c7bb6, GCC 14.3.0) and graded `TEXT RULES + INSTRUMENTS`. RTL-mutant elaboration was `SKIP` there (no Verilator). The focused local run above covers that arm on this tree.

### Clone state after the probes

Receipts: `receipts/clone-state-final.log`, `scripts/verify_clone_state.sh`.

- HEAD, tree and index tree are `4487359…`/`5b0645c8…`. The worktree equals HEAD (bytes and modes) with 0 untracked and 0 ignored entries.
- Gitlinks: `gptp-processor` `e5dcea6e`, `protocol-processor` `09f9bf38`, `third_party/verilog-axis` `48ff7a7e`, each checked out at the recorded commit and clean.
- The one probe by-product was `sw/builder/out/`, created by the focused gate 1b run. I removed it after recording its listing (`receipts/removed-probe-output-listing.txt`).

## 3. Findings

None at any severity.

## 4. Per-lens results

[R272] PASS Conformance - `receipts/focused/gate1b-sdk.log`, `receipts/gates/baremetal_only_check.log`, `receipts/gates/docs_check.log` at `4487359` - #408/#409 acceptance 1, 4 and 5 re-measured on the composed tree.
- The -E, -H and resolved-census arm graded with an RV32 compiler.
- 280 mutations, which is at least 163.
- `docs_check.py` and `check_baremetal_only.py --check` pass.
- The compiler-absent stand-down names its arm (`gate1b-absent.log`).
- Acceptance 2 and 3 read only the firmware, `test_builder.py` and `BAREMETAL_FIRMWARE.md`, all byte-identical to `062e89ad`, so the source reviews' judgement carries over unchanged.

[R272] PASS RTL - `receipts/gate1b-dev-inputs.txt`, `receipts/focused/gate1b-sdk.log` (46/46 line) at `4487359`.
- The PR changes no RTL.
- The only way the composition reaches RTL is gate 1b's RTL-mutant elaboration over dev's changed `milan_datapath.sv`, the `milan_dp` Makefile and 5 other closure files. All 46 variants elaborated under Verilator 5.050 as the real option-on top, and the malformed-RTL self-test was refused.
- Hosted `elaborate`, `verilator-lint`, `verilator-suites` and `yosys-portability` succeeded on the same tree (recorded, not re-run).

[R272] PASS Robustness - `receipts/focused/gate1b-absent.log`, `receipts/focused/rv32-absent.jsonl`, `receipts/focused/firmware-compiler-selftest.log`, `receipts/gates/ci_events_selftest.log` at `4487359`.
- The fail-closed paths hold on the composed tree: absent cross tools make 0 firmware compiles and the arm is declared `NOT RUN`.
- Host-compiler fallback is refused (self-test).
- The workflow step and order contract that dev changed (47 to 49 docs-check steps) still carries the PR's compiler-absent and builder steps (`ci_events.py --check`/`--selftest`).
- The refusal paths themselves read only the firmware, which is unchanged on dev.

[R272] PASS Tests - `receipts/gates/py_idiom.log`, `hygiene_check.log`, `fail_fast_check.log`, `test_evidence_check.log`, `todo_ownership.log`, `receipts/focused/gate1b-sdk.log` at `4487359`.
- Every tree-wide ratchet holds with dev's new Python files and the PR's builder together.
- Gate 1b's mutation, RTL-variant and equivalence counts on the composed tree equal the source-head counts.
- `test_builder.py` is byte-identical to `062e89ad`, so no test was weakened by the merge.

[R272] PASS Docs - `receipts/gates/{docs_check,em_dash_parent,em_dash_mergebase,gen_toc_check,gen_toc_anchors,doc_style,doc_paths,ci_events_check}.log` and `docs/testing/CI_WORKFLOWS.md:1121-1132` and `:1754-1761` at `4487359`.
- The shared page's two hunks are disjoint.
- The composed sentence at 1129-1130 matches the hosted absent-control output on this tree.
- The PR's page passes dev's new cmark-gfm Contents, anchor and em-dash gates.
- The `#elaboration` target it links to exists.
- No line the PR adds cites a line number in a file dev changed, and no text dev added restates a retired rule.

## 5. Ledger (reviewer-owned)

The composed tree touches every lens's scope in some way, so every lens was applied at the candidate head. The source-content coverage these rows rely on is that of the source reviews, per section 7's "ancestor that nothing in that lens's scope has touched since" rule. The candidate's PR-owned files are byte-identical to `062e89ad`.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gate 1b SDK and absent runs, `check_baremetal_only`, `docs_check` on the composed tree; acceptance 1, 4, 5 re-measured | R272-7 (composition); source content: R273-8 | `4487359031b52b0b92e526839473f2e9c956c967`; source `062e89ad098806ae5def8341fcb8c2815583ca00` |
| RTL | CLEAN | gate 1b RTL-mutant elaboration 46/46 over dev's changed closure; hosted elaborate, lint, suites, portability on the same tree (recorded) | R272-7; source: R273-8 | `4487359031b52b0b92e526839473f2e9c956c967`; source `062e89ad…` |
| Robustness | CLEAN | compiler-absent control and self-test, `ci_events` step-order contract | R272-7; source: R273-8 | `4487359031b52b0b92e526839473f2e9c956c967`; source `062e89ad…` |
| Tests | CLEAN | tree-wide ratchets, gate 1b counts, builder byte-identity | R272-7; source: R273-8 | `4487359031b52b0b92e526839473f2e9c956c967`; source `062e89ad…` |
| Docs | CLEAN | shared `CI_WORKFLOWS.md` hunks, TOC/anchor/em-dash/docs/style/path gates, cross-page links | R272-7; source: R273-8 | `4487359031b52b0b92e526839473f2e9c956c967`; source `062e89ad…` |

About the source reviews:
- The source positives are `[R273] POSITIVE` at `062e89ad` (PR comment 5820959513) and `[R272] POSITIVE` at `991d5965` (PR comment 5820082965).
- `991d5965` is an ancestor of `062e89ad`. The one commit between them changes `sw/builder/test_builder.py` (one lexer-corpus case added and comment wording, +19/-15) and `docs/integration/BAREMETAL_FIRMWARE.md` (+22/-16 wording), which is within Tests and Docs scope.
- So at the exact source head only R273-8 is nameable for Tests and Docs. Whether the two-positive bar is met at the source head is the manager's call (section 7 below).

## 5a. Prior public findings

I read the prior findings only after the verdict and ledger above were written.
- Every prior finding is about PR-owned content. `sw/builder/test_builder.py` and `docs/integration/BAREMETAL_FIRMWARE.md` are byte-identical to `062e89ad` in the candidate, and the PR's `CI_WORKFLOWS.md` hunk is carried unchanged.
- So each status at `062e89ad` carries to this head.
- The focused gate 1b run above re-graded the subset, lexer-corpus and closure checks on the composed tree, rc 0.

| Finding | Status at `4487359` | Evidence |
|---|---|---|
| R273-7 F1 MINOR, Docs (unscoped closure claim at the gate call site) | **Resolved, retained.** | `sw/builder/test_builder.py:11294-11299` scopes agreement to the table's 23 positions and the two corpora. |
| R272-6 S1 SUGGESTION, Tests (no `/*/` row) | **Resolved, retained.** | The row is at `sw/builder/test_builder.py:5614`. Gate 1b (which runs `assert_lexer_matches_compiler()`) passes on the composed tree. |
| R272-6 S2, R272-6 S3, R273-7 S1 SUGGESTIONs | Resolved or addressed at `062e89ad` (R273-8 table), unchanged here. | byte identity |
| R273-8 S1 SUGGESTION, Tests (no `/**/` row) and R273-8 S2 SUGGESTION, Docs (boundary label names 13 of 14) | **Open as SUGGESTIONs**, which is optional and does not affect coverage. The composition does not touch them. | `grep '/**/'` finds no row; the label text is unchanged from `062e89ad`. |
| R272-5 F1, R273-6 F1 (MINOR); R272-4 F1 = R273-5 F1, R272-3 F1 (MAJOR); R273-4 F1, R272-2 F1 (BLOCKER); R272-1 F1-F4; R273-1 F1; R273-3 F1/F2 | **Remain resolved** as tabled by R272-6, R273-7 and R273-8. R273-3 F1 was superseded by decision 5815136430, and F2 is a documented bound. | These are PR-owned mechanisms, byte-identical here. The composed gate 1b passes. |

No prior MINOR, MAJOR or BLOCKER is open at this head.

## 6. Limits

- **Composition only.** I did not re-review the source content of the PR (the directive readers, the subset S, the closure table or the mutation table). That is the source reviews' coverage.
- **Local compiler.** My RV32 compiler is a local Buildroot 2026.05 build of GCC 14.3.0, not the pinned hosted SDK archive (Buildroot 2021.11-18033-g83947c7bb6). Its ISA string differs, and it lowers float and double struct-overlay stores as integer stores. The pinned-SDK run on this tree is the hosted docs-check builder step (recorded, not reproduced).
- **Not run by me.** I did not run the full builder bank (every `test_builder.py` function), the parent, PP, gPTP, Yosys or native banks, `act`, or `act_ci.py`. For those I rely on the hosted runs on the same tree and on the manager.
- **Recorded, not reproduced.** The hosted results are recorded from the GitHub API. I did not reproduce them.
- **Hardware.** Physical calibration was NOT RUN. The `Physical gPTP` hosted context is skipped. Nothing here is hardware proof.
- **Manager evidence.** I did not find a public manager evidence packet for the candidate head itself. The evidence tree at `485f866f` holds source-head material (`author-r6` and earlier). My verdict rests on the receipts above.

## 7. Pending manager duties

- Confirm the source bar at `062e89ad`: two independent positives covering every lens at that exact head, or an ancestor untouched in that lens's scope (see the note under the ledger).
- The hosted/act acceptance of the exact merge candidate, and a fresh candidate if `dev` moves past `573f0052` before the merge.
- Maintainer authorization for the merge. After it: candidate-merge validation, post-merge containment and closing #408 and #409.

R272-7 FINISHED

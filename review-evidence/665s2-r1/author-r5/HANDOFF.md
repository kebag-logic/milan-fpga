# [A681e] #665 lane S2, round 5: the CPU cycle and latency budget (HANDOFF)

Status: **REVIEW READY**, 2026-10-26. Both R703-4 findings are fixed. R703-4-R1 is applied to the PR body. No firmware change, and no measured cycle count changed. The rows still miss T_svc = 10 ms (the measurement STOP; the later owner decision puts the instruction cache, S2c, before firmware-only tuning, S2b).

- Head: `f58d049beb377c3f535628067022d4d5b51e8208`, two commits on round 4's `a66148f6b7e59e3f42c939f464fe76e2b05404d7`:
  - `ee710802b6c3708d92a2595b514d2051966562a6` `Label a composed maximum partial when a run leaves out a backlog row, and pin its lower bound and the record the table renders (#665)`;
  - `f58d049beb377c3f535628067022d4d5b51e8208` `Name the refusal that catches two mutants in the self-test's mutant table (#665)`.
  - Both are one-line subjects with no body and no trailers.
- Branch `665-s2-cpu-budget`, base `origin/dev-soft-core` `e76a755afc0536453161e3cd33f6f4d2dcd7641f` (`git merge-base --is-ancestor` verified). The lane is not rebased. The PR (#792) targets `dev-soft-core`.
- Remote `https://github.com/kebag-logic/milan-fpga.git` (verified). No git command ran inside a submodule this round.
- Assignment: issue #665 issuecomment-6426822636. Finding: R703-4 (PR #792 issuecomment-6426817061, NEGATIVE, 2 MINOR). R704-3 stays POSITIVE.
- TAKEN: issuecomment-6426888094 (`TAKEN-COMMENT.md`).
- REVIEW READY: issuecomment-6428302802 (its body is `REVIEW-READY-COMMENT.md`). The PR body for the manager is `PR-BODY.md`.
- Every change is under `tb/verilator/ctrl_service_budget/`: `README.md`, `run.py`, `selftest.py` and `selftest_mutants.py`. No file was added.
  - `grade.py`, `scenario.py`, `sim_main.cpp`, `observe.vlt`, `build.py`, `oracle.json` and `fixture.log` are unchanged. So round 2's attested builds still reuse, every group script is unchanged, and the fixture needs no regeneration.
  - No firmware change and no new measurement. Every figure is a regrade of round 3's logs.
  - Nothing pushed. No PR, issue or comment edited. No Vivado, bench or hardware.

## Contents

1. [Result](#1-result)
2. [Findings and their fixes](#2-findings-and-their-fixes)
3. [Changes, file:line and reason](#3-changes-fileline-and-reason)
4. [New checks, planted mutants and failing words](#4-new-checks-planted-mutants-and-failing-words)
5. [Gate table](#5-gate-table)
6. [Run history and reproducibility](#6-run-history-and-reproducibility)
7. [The reviewers' probes, rerun unmodified](#7-the-reviewers-probes-rerun-unmodified)
8. [Acceptance](#8-acceptance)
9. [Open items, risks and questions](#9-open-items-risks-and-questions)

## 1. Result

Round 3's logs were regraded from copies at the head, on round 2's attested builds, in six arms and three controls (`scripts/regrade_r5.sh`). They were compared with round 4's regrade of the same logs at `a66148f6` (`scripts/compare_regrade.py`; `receipts/head-regrade/compare_a66148f6_vs_head.txt`):

- every log and every group's graded JSON is byte-identical (18, 17, 8, 8, 2, 2, 1, 1 and 1 groups);
- every `results.json` key is identical except `composed_maximum`, whose record only gains `rows`, `not_run` and `partial`;
- every `table.md` is identical except arm B's composed-maximum line, at both points.

The printed summaries are unchanged from round 4:

| Arm | Groups | Paths missing T_svc | Probe instances missing T_svc | Refusals |
|---|---:|---:|---:|---:|
| A 1x1 | 18 | 22 of 81 | 58 of 141 | 0 |
| A 8x8 | 17 | 60 of 129 | 102 of 182 | 0 |
| B 1x1 | 8 | 18 of 44 | 41 of 68 | 0 |
| B 8x8 | 8 | 36 of 68 | 60 of 92 | 0 |
| SHUTDOWN arm 1x1 / 8x8 | 2 / 2 | 0 of 1 / 0 of 2 | 0 of 2 / 0 of 3 | 0 |

The three controls print `CONTROL slow-adp-rx caught`, `CONTROL slow-adp-shutdown caught` and `CONTROL as-built caught: an instruction access fault (cause 1)`, rc 0 each.

The composed-maximum lines, as each run's `table.md` now prints them (`receipts/head-regrade/<arm>/table.md`):

| Arm | Line |
|---|---|
| A1 (unchanged) | `Composed maximum over the 4 backlog windows: at least 1,565,803 CPU cycles (31.316 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).` |
| A8 (unchanged) | `Composed maximum over the 4 backlog windows: at least 2,209,308 CPU cycles (44.186 ms), backlog-adp-refill, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).` |
| B1, was `Composed maximum over the 3 backlog windows: 740,260 CPU cycles (14.805 ms), backlog.` | `Composed maximum over 3 of 4 backlog windows, a partial figure (backlog-adp-refill not run): 740,260 CPU cycles (14.805 ms), backlog.` |
| B8, was `... over the 3 backlog windows: 1,392,016 CPU cycles (27.840 ms), backlog.` | `Composed maximum over 3 of 4 backlog windows, a partial figure (backlog-adp-refill not run): 1,392,016 CPU cycles (27.840 ms), backlog.` |
| S1, S8 and the controls | no backlog window, so no composed maximum (`null`), as before |

Arm B's `results.json` records carry `"windows": 3, "rows": 4, "not_run": ["backlog-adp-refill"], "partial": true`. Arm A's carry `"not_run": [], "partial": false`.

## 2. Findings and their fixes

| Finding | Fix (file:line at the head) | Check that fails without it |
|---|---|---|
| R703-4-F1 (MINOR; Robustness, Tests, Docs): a composed maximum over an incomplete set of backlog rows was reported as the composed maximum, and arm B's was | The reviewer's first option. `run.py:80-82`: `composed_maximum` names the `BACKLOG_ROWS` a run did not include (`not_run`), with `rows` and `partial`. `run.py:139-142`: the table line reads "over N of 4 backlog windows, a partial figure (<rows> not run)". A run of all four rows prints the line it printed before. `results.json` carries the record (`run.py:166-171`, `summary`). Arm B is **not** re-measured: adding `backlog-adp-refill` to its command needs no new measurement of arm A, but it would be a new arm B measurement that changes arm B's published figures (its counts, its composed maximum and its tables), and the round's scope allows no change to a measured cycle count. So the README (`:66`, `:157`, `:170`, `:202`, `:204`, `:209-210`, `:214`, `:441-443`, `:446`) and the PR body state arm B's coverage exactly: `backlog`, `backlog-adp` and `backlog-owed`, without `backlog-adp-refill`, a partial figure. | `a run without every backlog row names the rows not run, and its composed maximum is partial` (`selftest.py:424-433`); mutant `composition: the composed maximum does not name the backlog rows a run did not include`. R703-4's D1 now prints `not_run` and the partial line. |
| R703-4-F2 (MINOR; Tests): the check did not pin its own lower-bound rule, nor the published label | `selftest.py:417-423`: the longest window released its load and a shorter one did not; `lower_bound` must be `True`. `selftest.py:434-453`: `run.summary`'s record (what `results.json` holds) must equal the expected record, and the table's two composed lines rendered from it must match word for word. There are three cases: a lower bound over every window, a partial figure, and both at once (an unreleased window run alone, with no released window). | `the composed maximum is a lower bound while a window shorter than the longest left its load unreleased` (fails under P7 and its own mutant); `results.json's composed maximum is the record the table renders, with its lower-bound and partial labels` (fails under P3, P4, P5 and three own mutants) |
| R703-4-R1 (residue) | PR body: the row is renamed "A recipient's cost, every fan-out, both arms (arm A in brackets)", as written. | wording |
| Found this round: two rows of the README's mutant table named a check that no longer fails first | Round 4's records-ahead check grades a synthetic window. Under `worst pass: the run's last pass is dropped` and `composition: the load is the stimulus's own declaration (earlier rule)`, that grade refuses before any named check runs, and the self-test counts a refusal as caught. Both mutants were still caught at `a66148f6`, but the README named the round-3 checks. `README.md:561`, `:564` now name the refusal printed, and `:601` explains it (commit `f58d049b`). `scripts/mutant_table_check.py` confirms that all 62 rows match the self-test's output at the head, and that two rows did not at `a66148f6`. | `receipts/mutant_table_check.txt` (head: 62 rows, 0 mismatches); `receipts/mutant_table_check_a66148f6.txt` (2 mismatches) |
| R703-1 R-4 / R704-3-R1 (retained) | **Not applied.** `docs/testing/TESTING.md` is in the release lanes' file map and outside this round's scope. It stays on the residue checklist. | - |
| R703-4 S1 to S3 (optional) | Not applied; they are outside the round-5 assignment. P6, P9 and H3 still escape. | - |

## 3. Changes, file:line and reason

| File:line (head `f58d049b`) | What | Reason |
|---|---|---|
| `run.py:67-85` | `composed_maximum`: docstring; `not_run` (the backlog rows absent from the run); `rows`, `not_run` and `partial` in the record. The `lower_bound` line and the released-only line are byte-identical, so P7's and P8's anchors stay unique. | F1 |
| `run.py:136-146` | `table`: the composed line names the rows not run and says "a partial figure"; for a run of all four rows the line is unchanged | F1 |
| `run.py:166-171` | `summary`: the `results.json` record, with the same keys in the same order as before. The P5 anchor moves here. | F2: the self-test can check the record `results.json` holds |
| `run.py:317-318` | `main` writes `summary(...)` | F2 |
| `selftest.py:13-18` | module docstring | the new checks |
| `selftest.py:393-455` | `maximum_checks`: the round-4 check moves here and now uses all four backlog windows; three new checks (section 4) | F1, F2 |
| `selftest.py:725-726` | `checks()` runs `maximum_checks` | F1, F2 |
| `selftest_mutants.py:14` | `import re` | `_maximum_line` |
| `selftest_mutants.py:117-136` | `_maximum_edited`, `_maximum_line` | the new mutants |
| `selftest_mutants.py:370-379` | five new mutants | section 4 |
| `README.md:66` | arm B runs three of the four backlog rows, so its composed maximum is partial | F1 |
| `README.md:157` | Markers and grading: a run without every backlog row names the rows and labels the figure partial | F1 |
| `README.md:170` | each run's composed maximum, labelled partial where a row was left out | F1 |
| `README.md:202`, `:204` | Passes table: arm B's cells are "partial, 3 of 4 windows (`backlog-adp-refill` not run)" | F1 |
| `README.md:209-210`, `:214` | Passes text: arm B's three rows, its partial figure | F1 |
| `README.md:441-443` | Findings: arm B's three rows, a partial figure, not the composed maximum | F1 |
| `README.md:446` | Findings, the S2b/S2c baseline: a partial figure is no baseline either | F1 (the reviewer's impact on the S2b/S2c re-base) |
| `README.md:522-524` | the self-test's check list | F1, F2 |
| `README.md:561`, `:564`, `:601` | the mutant table names the refusal that catches two mutants | found this round (section 2) |
| `README.md:573-577` | the mutant table: five new rows | F1, F2 |

## 4. New checks, planted mutants and failing words

`python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` prints 87 `PASS` lines (84 in round 4), 62 `MUTANT caught` (57) and `self-test: 0 failures`, rc 0 (`receipts/gates/harness_selftest.log`). A failing check prints `FAIL: <check>: <detail>`. An uncaught mutant prints `MUTANT ESCAPED: <mutant>` and fails the run.

| New check (`selftest.py`) | Planted mutant (`selftest_mutants.py`) | Failing words, as printed |
|---|---|---|
| `the composed maximum is a lower bound while a window shorter than the longest left its load unreleased` (`:421`) | `composition: the composed maximum is a lower bound only where its own window left its load unreleased` (`:370`); R703-4's P7 | `MUTANT caught: composition: the composed maximum is a lower bound only where its own window left its load unreleased: the composed maximum is a lower bound while a window shorter than the longest left its load unreleased ({'cycles': 1800000, 'ms': 36.0, 'group': 'backlog', 'windows': 4, 'rows': 4, 'not_run': [], 'partial': False, 'lower_bound': False, 'unreleased': ['backlog-adp')`; P7: `FAIL: the composed maximum is a lower bound while a window shorter than the longest left its load unreleased: {'cycles': 1800000, ...` |
| `a run without every backlog row names the rows not run, and its composed maximum is partial` (`:432`) | `composition: the composed maximum does not name the backlog rows a run did not include` (`:372`) | `MUTANT caught: composition: the composed maximum does not name the backlog rows a run did not include: a run without every backlog row names the rows not run, and its composed maximum is partial ([{'cycles': 740260, 'ms': 14.8052, 'group': 'backlog', 'windows': 3, 'rows': 4, 'not_run': [], 'partial': False, ...` |
| `results.json's composed maximum is the record the table renders, with its lower-bound and partial labels` (`:452`) | `tables: results.json omits the composed maximum` (`:374`); R703-4's P5 | `MUTANT caught: tables: results.json omits the composed maximum: results.json's composed maximum is the record the table renders, with its lower-bound and partial labels (results.json None; table ['Composed maximum over the 4 backlog windows: at least 1,500,000 CPU cycles (30.000 ms), backlog-adp, a lower bound (load unreleased i)` |
| the same | `tables: the composed maximum line drops its lower-bound label` (`:376`); R703-4's P3 and P4 | `MUTANT caught: tables: the composed maximum line drops its lower-bound label: results.json's composed maximum is the record the table renders, with its lower-bound and partial labels (results.json {'cycles': 1500000, ...` |
| the same | `tables: the composed maximum line drops its partial label` (`:378`) | `MUTANT caught: tables: the composed maximum line drops its partial label: results.json's composed maximum is the record the table renders, with its lower-bound and partial labels (results.json {'cycles': 740260, 'ms': 14.8052, 'group': 'backlog', 'windows': 3, 'rows': 4, 'not_run': ['backlog-adp-refill'], 'partial': True, ...` |
| changed: `the composed maximum is the longest pass of every backlog window, a lower bound while one left its load unreleased` (`:414`) | the round-4 mutants, unchanged: released windows only (earlier rule), no lower bound, the fixture's window included; R703-4's P8 | still caught. Its cases are now every backlog window with the longest unreleased (a lower bound), and every window released (no lower bound). The round-4 two-window case, which R703-4-F1 flagged as calling a partial set the composed maximum, is replaced by the partial check above. |

- The new mutants are function patches, like every other in `selftest_mutants.py`. They leave the `run.py` lines that R703-4's source probes edit byte-identical, so all 10 of its anchors stay unique, as do R703-3's and R703-2's 46 (`receipts/review-probes/anchor_check.txt`, 56 of 56).
- The 57 round-4 mutants are all still caught. `scripts/mutant_table_check.py` matches all 62 rows of the README's mutant table to the self-test's output (`receipts/mutant_table_check.txt`).

## 5. Gate table

Every gate ran at the head `f58d049beb377c3f535628067022d4d5b51e8208`, one at a time, in a single runner (`scripts/gates_r5.py`, round 4's runner with only its docstring changed). Each gate's output went to its own log; nothing was piped. The runner was started detached (`setsid nohup`), because the compiler-absent and end-station builder gates take 11 and 24 minutes alone. It was polled with foreground waits.

- The runner refuses to start on a dirty tree.
- After every gate it checks `git status --porcelain --untracked-files=all --ignore-submodules=none`, and it stops at the first gate that leaves the tree dirty. None did.
- Each log is in `receipts/gates/`, with its rc and the tree's state on its last lines. `HEAD.txt` names the head, `summary.md` is the runner's table (with each gate's seconds), and `serial.out` is its console.
- Two logs exceed 200 KB: `bdd_conformance.log` (377,097 B) and `ci_events_selftest.log` (336,198 B). Each is kept out of the packet, with its size, sha256 and last lines in `<log>.digest.txt`.

Environments:

- The Markdown gates and the rest ran with the pinned renderer (`tools/markdown/requirements.txt`), PyYAML and the docs workflow's `wavedrom==2.0.3.post3`.
- The HDL reference ran with `tools/hdl_reference/requirements.txt`.
- The end-station builder gate ran with the product LiteX environment and the pinned RV32 SDK first on `PATH`.
- Each environment is round 4's scratch virtual environment, outside the packet.

Key verdicts:

- `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))`.
- `self-test: 0 failures` (87 checks, 62 mutants caught).
- `check_em_dash: 0 finding(s) over 643 added line(s) in 1 changed Markdown page(s) ... [e76a755a..HEAD]`.
- `docs_check: 0 finding(s) across 211 md files + 1433 scrubbed text files`.
- `TOC gate: OK`, and the anchor check reproduces all 545 cross-page fragment links. `doc path gate: OK (1062 cited paths all resolve ...)`. `documentation style: OK`.
- `GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations`. This is the compiler-absent control; the NOT RUN is the compiled census, which this mode hides by design.
- `ALL GATES PASS EXCEPT 1 NOT RUN`, from the end-station builder. Its gate 11 needs an mf48 calibration build tree that this host does not have (round 4: the same).
- behave: 14 features passed, 406 scenarios passed, 1977 steps passed.

| Gate (log `receipts/gates/<gate>.log`) | Command | rc | Tree after |
|---|---|---:|---|
| `harness_selftest` | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | 0 | clean |
| `baremetal_check` | `python3 scripts/check_baremetal_only.py --check` | 0 | clean |
| `baremetal_selftest` | `python3 scripts/check_baremetal_only.py --selftest` | 0 | clean |
| `wire_accountability_selftest` | `python3 scripts/check_wire_accountability.py --self-test` | 0 | clean |
| `docs_check` | `python3 scripts/docs_check.py` | 0 | clean |
| `feature_status` | `python3 scripts/check_feature_status.py` | 0 | clean |
| `feature_status_selftest` | `python3 scripts/check_feature_status.py --self-test` | 0 | clean |
| `traceability_matrix` | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | clean |
| `em_dash` | `python3 scripts/check_em_dash.py --base e76a755afc0536453161e3cd33f6f4d2dcd7641f` | 0 | clean |
| `em_dash_selftest` | `python3 scripts/check_em_dash.py --selftest` | 0 | clean |
| `doc_style` | `python3 scripts/check_doc_style.py` | 0 | clean |
| `doc_style_selftest` | `python3 scripts/check_doc_style.py --selftest` | 0 | clean |
| `gptp_docs` | `python3 scripts/check_gptp_docs.py` | 0 | clean |
| `gptp_docs_selftest` | `python3 scripts/check_gptp_docs.py --selftest` | 0 | clean |
| `gptp_docs_with_submodule` | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | clean |
| `gptp_processor_docs` | `make -C gptp-processor docs PYTHON=python3` | 0 | clean |
| `doc_map` | `python3 docs/DOC_MAP.gen.py --check` | 0 | clean |
| `doc_map_selftest` | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | clean |
| `timesync_chain` | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | clean |
| `timesync_chain_selftest` | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | clean |
| `solution_docs` | `python3 scripts/check_solution_docs.py` | 0 | clean |
| `solution_docs_selftest` | `python3 scripts/check_solution_docs.py --selftest` | 0 | clean |
| `submodule_boundaries` | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | clean |
| `submodule_boundaries_selftest` | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | clean |
| `submodule_docs` | `python3 scripts/check_submodule_docs.py` | 0 | clean |
| `submodule_docs_selftest` | `python3 scripts/check_submodule_docs.py --selftest` | 0 | clean |
| `wavedrom_selftest` | `python3 scripts/gen_wavedrom.py --selftest` | 0 | clean |
| `wavedrom_axis_backpressure` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | clean |
| `wavedrom_cdc_handshake` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | clean |
| `wavedrom_gptp_pdelay` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | clean |
| `diagram_pngs` | `python3 scripts/check_diagram_pngs.py` | 0 | clean |
| `diagram_pngs_selftest` | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | clean |
| `control_flow_selftest` | `python3 scripts/measure_control_flow.py --selftest` | 0 | clean |
| `cohesion_selftest` | `python3 scripts/measure_cohesion.py --selftest` | 0 | clean |
| `rv32_sdk_selftest` | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | clean |
| `firmware_compiler_selftest` | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | clean |
| `firmware_compiler_absent` | `python3 sw/builder/test_firmware_compiler.py --absent --audit <scratch>/tmp/rv32-absent.jsonl` | 0 | clean |
| `nvm_record_space` | `python3 scripts/check_nvm_record_space.py` | 0 | clean |
| `nvm_record_space_selftest` | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | clean |
| `nvm_capture` | `python3 scripts/check_nvm_capture.py` | 0 | clean |
| `nvm_firmware_selftest` | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | clean |
| `soc_sources` | `python3 scripts/check_soc_sources.py` | 0 | clean |
| `soc_sources_selftest` | `python3 scripts/check_soc_sources.py --selftest` | 0 | clean |
| `iob_pack_selftest` | `python3 sw/litex/iob_pack_selftest.py` | 0 | clean |
| `rtl_source_lists` | `python3 scripts/check_rtl_source_lists.py` | 0 | clean |
| `rtl_source_lists_selftest` | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | clean |
| `naming` | `python3 scripts/measure_naming.py --check` | 0 | clean |
| `naming_selftest` | `python3 scripts/measure_naming.py --selftest` | 0 | clean |
| `port_contracts` | `python3 scripts/check_port_contracts.py` | 0 | clean |
| `port_contracts_selftest` | `python3 scripts/check_port_contracts.py --selftest` | 0 | clean |
| `fail_fast` | `python3 scripts/measure_fail_fast.py --check` | 0 | clean |
| `fail_fast_selftest` | `python3 scripts/ci_fail_fast_selftest.py` | 0 | clean |
| `todo_ownership` | `python3 scripts/check_todo_ownership.py` | 0 | clean |
| `todo_ownership_selftest` | `python3 scripts/check_todo_ownership.py --selftest` | 0 | clean |
| `test_evidence` | `python3 scripts/measure_test_evidence.py --check` | 0 | clean |
| `test_evidence_selftest` | `python3 scripts/measure_test_evidence.py --selftest` | 0 | clean |
| `hygiene` | `python3 scripts/check_hygiene.py --check` | 0 | clean |
| `hygiene_selftest` | `python3 scripts/check_hygiene.py --selftest` | 0 | clean |
| `sv_idiom` | `python3 scripts/check_sv_idiom.py` | 0 | clean |
| `sv_idiom_selftest` | `python3 scripts/check_sv_idiom.py --selftest` | 0 | clean |
| `cpp_idiom` | `python3 scripts/check_cpp_idiom.py` | 0 | clean |
| `cpp_idiom_selftest` | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | clean |
| `py_idiom` | `python3 scripts/check_py_idiom.py` | 0 | clean |
| `py_idiom_selftest` | `python3 scripts/check_py_idiom.py --selftest` | 0 | clean |
| `sh_idiom` | `python3 scripts/check_sh_idiom.py` | 0 | clean |
| `sh_idiom_selftest` | `python3 scripts/check_sh_idiom.py --selftest` | 0 | clean |
| `doc_paths` | `python3 scripts/check_doc_paths.py` | 0 | clean |
| `archive` | `python3 scripts/check_archive.py` | 0 | clean |
| `archive_selftest` | `python3 scripts/check_archive.py --selftest` | 0 | clean |
| `toc_selftest` | `python3 scripts/gen_toc.py --selftest` | 0 | clean |
| `toc_verify_anchors` | `python3 scripts/gen_toc.py --verify-anchors` | 0 | clean |
| `toc_check` | `python3 scripts/gen_toc.py --check` | 0 | clean |
| `aem_store_selftest` | `python3 avdecc/gen_aem_store.py --self-test` | 0 | clean |
| `sweep_shape_selftest` | `python3 scripts/check_sweep_shape.py --self-test` | 0 | clean |
| `deploy_shape_selftest` | `python3 scripts/check_deploy_shape.py --self-test` | 0 | clean |
| `entity_shape_selftest` | `python3 scripts/check_entity_shape.py --self-test` | 0 | clean |
| `gate_workflows` | `python3 scripts/ci_gate_workflows.py --check` | 0 | clean |
| `gate_workflows_selftest` | `python3 scripts/ci_gate_workflows_selftest.py` | 0 | clean |
| `case_receipts_selftest` | `python3 scripts/ci_case_receipts_selftest.py` | 0 | clean |
| `make_cases_selftest` | `python3 scripts/ci_make_cases_selftest.py` | 0 | clean |
| `maap_cases_selftest` | `python3 scripts/ci_maap_cases_selftest.py` | 0 | clean |
| `capture_cases_selftest` | `python3 scripts/ci_capture_cases_selftest.py` | 0 | clean |
| `suite_pieces_selftest` | `python3 scripts/ci_suite_pieces_selftest.py` | 0 | clean |
| `suite_collect_selftest` | `python3 scripts/ci_suite_collect_selftest.py` | 0 | clean |
| `fail_fast_selftest` | `python3 scripts/ci_fail_fast_selftest.py` | 0 | clean |
| `install_cache_selftest` | `python3 scripts/ci_install_cache_selftest.py` | 0 | clean |
| `workflow_plan_selftest` | `python3 scripts/ci_workflow_plan_selftest.py` | 0 | clean |
| `manifest_selftest` | `python3 scripts/ci_manifest_selftest.py` | 0 | clean |
| `evidence_pins` | `python3 scripts/generate_ci_evidence_pins.py --check` | 0 | clean |
| `ci_events` | `python3 scripts/ci_events.py --check` | 0 | clean |
| `ci_events_selftest` | `python3 scripts/ci_events.py --selftest` | 0 | clean |
| `git_diff_check` | `git diff --check e76a755afc0536453161e3cd33f6f4d2dcd7641f HEAD` | 0 | clean |
| `bdd_conformance` | `cd tests && behave` | 0 | clean |
| `hdl_reference_selftest` | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | clean |
| `hdl_reference` | `python3 scripts/gen_hdl_reference.py --output <scratch>/tmp/milan-hdl-reference` | 0 | clean |
| `builder_require_rv32` | `python3 sw/builder/test_builder.py --require-rv32` | 0 | clean |

96 gates, every one rc 0, the tree clean after each.

Not run, with the reason:

- `act_ci.py --selftest`: AGENTS.md lets a candidate's copy run it only inside the disposable CI job. This lane does not change it.
- `ci_rv32_sdk.py --destination ...` installs the SDK, which is already at its pinned path. `ci_rv32_sdk_selftest.py` passed.
- The full serial sweep: the lane changes only files under `tb/verilator/ctrl_service_budget/` and no shared file, as the brief allows.

## 6. Run history and reproducibility

- **No simulation ran this round.** Every figure comes from round 3's logs, regraded from fresh copies on round 2's attested builds. `build.reused` accepts each build, because no build input changed. The scenario is unchanged, so the regrade refused no stale script.
- **Regrades.** The logs were regraded at `ee710802` and again at the head `f58d049b`. The two result trees are byte-identical (`diff -r`), as expected, since the second commit changes the README only. `receipts/head-regrade/` holds the head's comparison with round 4's regrade, each arm's `table.md` and run log, the `results.json` digests and each arm's composed-maximum record.
- **Reviewer probes** ran at `ee710802` first, then again at the head on the same clone, checked out at `f58d049b` (section 7). The results are the same at both.
- **Disclosed: one gate run was stopped and is not evidence.**
  - The first full gate run started at `ee710802`.
  - My own receipt check then found the two stale rows of the README's mutant table (section 2), so the head had to move.
  - I stopped that runner between gates: its parent process was killed while its child, the compiler-absent gate, still ran. I let the child finish, so it restored what it plants.
  - The tree was then verified clean at `ee710802`, the README fix was committed, and the whole gate set was rerun from the start at `f58d049b` (section 5).
  - The stopped run's logs stay in scratch and are not cited.
- **No git command ran inside a submodule.** The gates' submodule-aware status checks run from the superproject.
- Round 3's logs and round 2's builds stay in scratch; their paths in receipts are replaced by role placeholders (`receipts/INDEX.md`).


## 7. The reviewers' probes, rerun unmodified

The three scripts are byte-identical to R703-4's published copies: `r703_4_probes.py` `a5977aa5…`, `review_mutants3.py` `54f6855e…` and `review_mutants2.py` `974d0bf7…` (`receipts/review-probes/script_identity.txt`, against R703-4's `MANIFEST.sha256`).

- `r703_4_probes.py` ran on a local clone of the head, with a clean tree before and an empty `git status --porcelain` after.
- `review_mutants2.py` and `review_mutants3.py` ran in R703's own sandbox layout (`sandbox.sh`), built from that clone. The sandbox's harness copy is identical to the head's (`diff -r`).

| Probe | At `a66148f6` (R703-4) | At the head `f58d049b` |
|---|---|---|
| P1, P2 (`BACKLOG_ROWS` drops a row) | caught | caught. The self-test exits 1 with an uncaught `grade.Refusal: backlog-adp-refill: no defined composed load` (or `backlog-owed`), as before. |
| P3 (no "at least") | ESCAPED | **caught**: `FAIL: results.json's composed maximum is the record the table renders, with its lower-bound and partial labels` |
| P4 (no lower-bound clause) | ESCAPED | **caught**, the same check |
| P5 (`results.json` without the record) | ESCAPED | **caught**, the same check (`results.json None`) |
| P6 (fan-out recipients unsorted) | ESCAPED | ESCAPED (R703-4 S1, optional, not applied) |
| P7 (a lower bound only when the longest window is unreleased) | ESCAPED | **caught**: `FAIL: the composed maximum is a lower bound while a window shorter than the longest left its load unreleased` |
| P8 (the released-only figure over every window) | caught | caught |
| P9 (`r >= commit`) | ESCAPED | ESCAPED (R703-4 S2, optional, not applied) |
| P10 (every earlier record ahead) | caught | caught |
| D1 (arm B's three rows; one row) | `windows: 3` / `1`, no label | `"not_run": ["backlog-adp-refill"], "partial": true` / `"not_run": ["backlog-adp", "backlog-adp-refill", "backlog-owed"], "partial": true`. The table prints `Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 740,260 CPU cycles (14.805 ms), backlog.` |
| `review_mutants3.py` (21) | 18 caught; G2, G3, H3 escape | 18 caught; G2, G3, H3 escape (`receipts/review-probes/review_mutants3.log`) |
| `review_mutants2.py` (25) | 23 caught; N11, N12 escape | 23 caught; N11, N12 escape (`receipts/review-probes/review_mutants2.log`) |

The probes' raw output is `receipts/review-probes/r703_4_probes.json` and `.log`; `r703_4_probes_summary.txt` lists it a probe a line.

## 8. Acceptance

| Item (round 5) | Status | Evidence |
|---|---|---|
| 1. F1: `composed_maximum` names the backlog rows not run; the table line and `results.json` label the figure partial; arm B's coverage stated exactly in the README and PR body; a named check with a row missing, and a mutant that drops the rule | met | sections 1 to 4; README `:66`, `:202-214`, `:441-446`; PR body |
| 2. F2: a check where the longest window released and a shorter one did not (`lower_bound: True`); a check on the `composed_maximum` record the table renders; a mutant for each | met | section 4 |
| 3. `r703_4_probes.py` unchanged: D1, P3, P4, P5, P7 caught; bare-metal gate; full docs-check set; behave | met: P3, P4, P5, P7 caught; D1 names the rows not run and the label; bare-metal gate rc 0; 96 gates rc 0; behave 406/406 | sections 5 and 7 |
| Scope: `tb/verilator/ctrl_service_budget/` and the PR body only; no firmware change; no measured cycle count changed | met | `git diff --stat a66148f6 f58d049b`: four files, all in the harness; section 1 |
| Rows within T_svc | **not met**: the measurement STOP, under owner decision D4 and the cache-first decision | README Findings |

So the PR body says "Relates to #665".

## 9. Open items, risks and questions

- **For S2b and S2c:** re-base against arm A's composed maximum over every backlog window, at least 31.32 ms (1x1) and at least 44.19 ms (8x8), window by window and over the same four backlog rows. A re-measure that leaves out a row now prints "a partial figure (<row> not run)" and records `"partial": true`. Neither that figure nor the released-only one is a baseline.
- **Arm B is partial by design here.** If a later round wants arm B's composed maximum, it must run `backlog-adp-refill` in arm B: a new measurement, which this round's scope did not allow.
- **For the manager (carried):** whether the ACMP owed-capacity drop (`ACMP_OWED_MAX` 8 against the ring's 12), the SRP starvation (`srp_mbx.c:441-451`) and the per-recipient fan-out cost (11,786 to 22,030 CPU cycles) become Issues or S2b scope.
- **R-4 / R704-3-R1 not applied** (`docs/testing/TESTING.md:518`, a release-lane file).
- **Optional, not applied:** R703-4 S1 (P6), S2 (P9) and S3 (R703-3's S1 to S3: H3, the idle minimum, R703-2's S1 to S3). G2, G3, N11 and N12 also still escape; R703's reports record that no published value changes under them.
- **P1 and P2 are caught by an uncaught refusal**, a traceback rather than a `FAIL` line, as at `a66148f6`. They still fail the run.
- The act runner's `--selftest` was not run on the host: AGENTS.md lets a candidate's copy run it only inside the disposable CI job.
- Physical calibration NOT RUN; nothing here is hardware evidence.

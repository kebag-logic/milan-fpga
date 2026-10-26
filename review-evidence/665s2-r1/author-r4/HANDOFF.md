# [A681d] #665 lane S2, round 4: the CPU cycle and latency budget (HANDOFF)

Status: **REVIEW READY**, 2026-10-26. Every R703-3 finding is fixed, both reports' wording residue inside the lane is applied, and no measured cycle count changed. The rows still miss T_svc = 10 ms (the measurement STOP; the later owner decision puts the instruction cache, S2c, before firmware-only tuning, S2b).

- Head: `a66148f6b7e59e3f42c939f464fe76e2b05404d7`, one commit on round 3's `f887663852d118e810ef690c3dd5cf9fe2292588`. Subject `Take the composed maximum over every backlog window, state the fan-out ranges whole and check the cost a recipient and the records ahead (#665)`, no body, no trailers.
- Branch `665-s2-cpu-budget`, base `origin/dev-soft-core` `e76a755afc0536453161e3cd33f6f4d2dcd7641f` (verified with `git merge-base`; `dev-soft-core` has since moved to `9220f9b3`, and the lane is not rebased). The PR targets `dev-soft-core`.
- Remote `https://github.com/kebag-logic/milan-fpga.git` (verified). Git inside the submodules was read-only: `rev-parse --show-toplevel` and `remote get-url origin` in each of the five, and one `status` through `submodule foreach`, which ran before those checks (section 6).
- Assignment: issue #665 issuecomment-6423962540. Findings: R703-3 (PR #792 issuecomment-6423951390, NEGATIVE) and R704-3 (issuecomment-6423238751, POSITIVE). TAKEN: issuecomment-6424008568. REVIEW READY: issuecomment-6426473926 (its body is `REVIEW-READY-COMMENT.md`).
- Every change is under `tb/verilator/ctrl_service_budget/`: `README.md`, `grade.py`, `run.py`, `scenario.py`, `selftest.py` and `selftest_mutants.py`, with no new file.
  - `sim_main.cpp`, `observe.vlt`, `build.py`, `oracle.json` and `fixture.log` are unchanged. So round 2's attested builds still reuse, and the fixture needs no regeneration.
  - No firmware change and no new measurement. Every figure is a regrade of round 3's logs, and no measured cycle count changed (section 1).
  - Nothing pushed; no PR, issue or comment edited; no Vivado, bench or hardware.

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

Round 3's logs were regraded at the head, from copies, on round 2's attested builds: six arms and three controls (`scripts/regrade_r4.sh`).

- Every group's graded JSON is byte-identical to the regrade at `f8876638`.
- So is every `results.json` key, apart from the one addition, `composed_maximum` (`receipts/head-regrade/compare_base_f8876638_vs_head.txt`).
- The printed summaries are unchanged:

| Arm | Groups | Paths missing T_svc | Probe instances missing T_svc | Refusals |
|---|---:|---:|---:|---:|
| A 1x1 | 18 | 22 of 81 | 58 of 141 | 0 |
| A 8x8 | 17 | 60 of 129 | 102 of 182 | 0 |
| B 1x1 | 8 | 18 of 44 | 41 of 68 | 0 |
| B 8x8 | 8 | 36 of 68 | 60 of 92 | 0 |
| SHUTDOWN arm 1x1 / 8x8 | 2 / 2 | 0 of 1 / 0 of 2 | 0 of 2 / 0 of 3 | 0 |

The composed maximum, as the run now reports it (`receipts/head-regrade/<arm>/summary.json`, `table.md`):

| Figure | 1x1 | 8x8 |
|---|---|---|
| **Composed maximum over every backlog window, arm A** (the formal arm; the S2b and S2c baseline) | **at least 1,565,803 CPU cycles (31.32 ms)**, backlog-adp, a lower bound: backlog-adp and backlog-adp-refill never release SRP's 32 records | **at least 2,209,308 (44.19 ms)**, backlog-adp-refill, a lower bound, likewise |
| Over arm A's windows that released their load only (labelled; not the composed maximum) | 740,260 (14.81 ms), backlog | 1,392,016 (27.84 ms), backlog |
| Composed maximum, arm B (3 windows, every one released) | 740,260 (14.81 ms), backlog | 1,392,016 (27.84 ms), backlog |
| Worst pass, A | 1,565,803 (31.32 ms), backlog-adp | 2,989,496 (59.79 ms), acmp-notk |

The fan-out ranges, over every measured fan-out on every interface (`receipts/f3/fanout_cells_and_ranges.txt`, 58 fan-outs):

| Range | Every fan-out (A and B) | Arm A |
|---|---|---|
| A recipient's cost, CPU cycles | 11,786 to 22,030 | 11,818 to 20,486 |
| ... 1x1 / 8x8 | 11,818 to 21,875 / 11,786 to 22,030 | 11,818 to 20,358 / 11,844 to 20,486 |
| SET_NAME's cost | 20,358 to 20,486 | the same |
| SET_STREAM_INFO / BIND_RX's GET_STREAM_INFO notice (arm B only) | 21,875 to 22,030 / 18,358 to 18,475 | - |
| Every other fan-out's cost | 11,786 to 13,440 | 11,818 to 13,440 |
| The 16 recipients at 1x1 | 7.77 to 14.80 ms | 7.77 to 11.33 ms |
| The 32 recipients at 8x8 | 12.39 to 32.78 ms | 12.39 to 22.98 ms |

- R703-3's suggested low end is 11,800. Arm B's SET_CONFIGURATION at 8x8 costs 11,786, and that is a cell of the README's table, so the stated range starts there.
- The README's SET_CONTROL cell is the worse of identify on and identify off. The better ones, 7.77 ms (1x1) and 12.39 ms (8x8 if0), set the time ranges' low ends, and the README says so.

## 2. Findings and their fixes

| Finding | Fix (file:line at the head) | Check that fails on `f8876638` |
|---|---|---|
| R703-3-F1 (MAJOR): `check_baremetal_only.py --check` exits 1 on `scenario.py:805` ("TX ring") | `scenario.py:805-806` now reads "the egress held and the ACMP transmit ring filled", as `mailbox.yaml` names its rings ("the transmit ring", `:438`, `:445`). The gate's term table is unchanged. The gate is in the validation list of the PR body and REVIEW READY. The gate's own per-file scanner judged every file in the PR's diff (`scripts/baremetal_scan_files.py`): 15 files, 0 findings. | The bare-metal gate itself. At `f8876638` the scanner prints `scenario.py:805: [H] retired target host-plane surface 'TX ring'` (`receipts/f1/scan_base_f8876638.txt`). At the head it prints `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))` (`receipts/gates/baremetal_check.log`). |
| R703-3-F2 (MINOR): arm A's composed maximum left out the windows it never finished | `run.py:67` `composed_maximum` takes the longest pass over every backlog row's window (`grade.py:54` `BACKLOG_ROWS`; the fixture's short window is excluded). Each window committed its defined load, since `grade.check_load` refuses any other. The figure is labelled a lower bound while any window left its load unreleased, and the released-only figure is given beside it. `run.py:132` prints both in `table.md`, and `:306` writes them to `results.json`. The text: README `:152-157` (definition), `:197-214` (Passes table and text) and `:437-441` (Findings, and the S2b/S2c baseline); PR body Status, Description and figures. | `the composed maximum is the longest pass of every backlog window, a lower bound while one left its load unreleased`; mutants `composition: the composed maximum is taken over the windows that released their load (earlier rule)`, `... is no lower bound where a window left its load unreleased`, `... includes the fixture's short window` |
| R703-3-F3 (MINOR): the fan-out ranges were below the table's own cells | README `:310-313` (fan-out notes), `:454-456` (Findings) and `:461` (D4 (a)); PR body figures and D4 (a). Every range contains every cell, with arm A's range beside it (section 1). | `scripts/fanout_ranges.py` over the regraded results: every stated range contains every measured fan-out (`receipts/f3/fanout_cells_and_ranges.txt`) |
| R703-3-F4 (MINOR): G6 (cost a recipient) and G9 (records ahead) escaped | `selftest.py:334-339`: a synthetic SET_NAME fan-out to three recipients, 400,000 bus cycles first to last, must cost 100,000 CPU cycles a recipient. `selftest.py:354-367`: two ACMP records in a composed window, released one a pass; the second has 1 ahead when committed before the first's release, and 0 when committed after it. Mutants: `selftest_mutants.py:76`, `:90`. `grade.py:15-16`, `:22-25` and `:711-712` name both rules. The rule lines R703-3's G6 and G9 edit (`grade.py:525-527`, `:728`) are byte-identical, so its anchors stay unique. | `a fan-out's cost a recipient is its first to last commit over the gaps between them` (fails under G6: 66,666); `a served record's records ahead are those not yet released at its commit` (fails under G9: 0). R703-3's `review_mutants3.py`, unmodified: G6 CAUGHT, G9 CAUGHT (both ESCAPED at `f8876638`). |
| R703-3-R1 | README `:622`, after the START_STREAMING line, as written: "SET_STREAM_FORMAT is refused in both arms, whose format port answers unsupported (`ctrl_aecp_image.c`, `a_format`), so its fan-out is not run." Verified in the code: `aecp_commands.c:211-215` returns BAD_ARGUMENTS when the port answers false, `ctrl_aecp_image.c:73` `a_format` returns false, and arm B's edits (`build.py:67-77`) leave it. | wording |
| R704-3-R2 | `scenario.py:845-852`: the opening sentences are replaced as written. The new text is "Each composed window carries its row's defined load (#665; MAILBOX_SPLIT.md:753-758), including MAAP, SRP and fifteen grandmaster changes. The row's input is last on its channel except in the owed row, which places the remaining admitted ACMP commands behind it." The refill explanation is kept. The paragraph is rewrapped to keep the module within the idiom gate's 1,000 lines. | wording |
| R704-3-R3 | README `:362`: "the owed response, from the moment the room returns". The figures (66.29 / 101.10 / 66.28 / 101.10) are unchanged. | wording |
| R704-3-R4 | PR body Status: "so the measurement STOP stands; the later owner decision puts instruction-cache evaluation before firmware-only tuning", linked. Known limitations point to the same decision. | wording |
| R703-1 R-4 / R704-3-R1 | **Not applied**: `docs/testing/TESTING.md` is in the release lanes' file map. It stays on the residue checklist. | - |
| R703-3 S1-S3 | Not applied (optional suggestions, not in the assignment). H3 still escapes (S1). | - |

## 3. Changes, file:line and reason

| File:line | What | Reason |
|---|---|---|
| `scenario.py:805-807` | the owed row's comment names "the ACMP transmit ring" | R703-3-F1 |
| `scenario.py:845-852` | `backlog_groups` docstring | R704-3-R2 |
| `grade.py:15-16` | module docstring: the fan-out cost rule | R703-3-F4 |
| `grade.py:19-20`, `:22-25` | module docstring: `run.composed_maximum`; the service rows' records ahead | R703-3-F2, F4 |
| `grade.py:52-57` | `BACKLOG_ROWS`, and `COMPOSED_ROWS` built from it (same value) | F2: the composed maximum ranges over the backlog rows, not the fixture's short window |
| `grade.py:711-712` | `service` docstring: the records ahead | R703-3-F4 |
| `grade.py:756-761` | `composed` docstring: `serviced` flags a lower bound; the composed maximum is taken in `run.composed_maximum` | R703-3-F2 |
| `run.py:67-81` | `composed_maximum` | R703-3-F2 |
| `run.py:125-140` | `table`: the windows' heading restated; the composed maximum and the released-only figure | R703-3-F2 |
| `run.py:306` | `results.json` gains `composed_maximum` | R703-3-F2 |
| `selftest.py:3-21` | docstring | the new checks |
| `selftest.py:201` | check renamed "... its window reports its load unreleased"; it was "... is no composed maximum", false under F2's definition | R703-3-F2 |
| `selftest.py:334-339` | the three-recipient fan-out cost | R703-3-F4 (G6) |
| `selftest.py:354-367` | the records ahead of a served record | R703-3-F4 (G9) |
| `selftest.py:388-403` | the composed maximum over synthetic windows (fixture, released, unreleased) | R703-3-F2 |
| `selftest_mutants.py:76-114` | `_cost_over_recipients`, `_ahead_never_released`, `_maximum_of` | section 4 |
| `selftest_mutants.py:339-348` | mutant renamed "... reports it released (earlier rule)"; five new mutants | section 4 |
| `README.md:152-157` | Markers and grading: a served record's records ahead; the composed maximum's definition, its lower bound and the released-only figure | R703-3-F2, F4 |
| `README.md:168` | each run reports the composed maximum | R703-3-F2 |
| `README.md:197-214` | Passes table and text: the composed maximum over every window, the released-only column labelled, the consumers of arm A's 8x8 maximum | R703-3-F2 |
| `README.md:310-313` | fan-out cost and time ranges | R703-3-F3 |
| `README.md:362` | the owed row's label | R704-3-R3 |
| `README.md:437-441` | Findings: arm A's composed maximum, and the S2b/S2c baseline | R703-3-F2 |
| `README.md:454-456`, `:461` | Findings and D4 (a): fan-out ranges | R703-3-F3 |
| `README.md:508-521` | the self-test's check list | R703-3-F2, F4 |
| `README.md:560-566` | the mutant table: one row renamed, five new | section 4 |
| `README.md:622` | Limits: SET_STREAM_FORMAT | R703-3-R1 |

## 4. New checks, planted mutants and failing words

`python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` prints 84 `PASS` lines (81 in round 3), 57 `MUTANT caught` (52) and `self-test: 0 failures`, rc 0 (`receipts/gates/harness_selftest.log`). A failing check prints `FAIL: <check>: <detail>`. An uncaught mutant prints `MUTANT ESCAPED: <mutant>` and fails the run.

| New check (`selftest.py`) | Planted mutant | Failing words, as printed |
|---|---|---|
| `a fan-out's cost a recipient is its first to last commit over the gaps between them` (`:337`) | own: `notify: the cost a recipient divides by the recipients, not the gaps`; R703-3's G6 (source edit of `grade.py:527`) | `MUTANT caught: notify: the cost a recipient divides by the recipients, not the gaps: a fan-out's cost a recipient is its first to last commit over the gaps between them ({'recipients': 3, 'first_sys': 401173, 'last_sys': 801173, 'per_recipient_cpu_cycles': 66666})`; G6: `G6 CAUGHT rc=1 ... FAIL: a fan-out's cost a recipient is its first to last commit over the gaps between them: {'recipients': 3, ...` |
| `a served record's records ahead are those not yet released at its commit` (`:366`) | own: `service: the records ahead count only those never released`; R703-3's G9 (source edit of `grade.py:728`) | `MUTANT caught: service: the records ahead count only those never released: a served record's records ahead are those not yet released at its commit ([[('service.acmp.first.if0', 0), ('service.acmp.last.if0', 0)], ...])`; G9: `G9 CAUGHT rc=1 ... FAIL: a served record's records ahead are those not yet released at its commit: [[('service.acmp.first.if0', 0), ('service.` |
| `the composed maximum is the longest pass of every backlog window, a lower bound while one left its load unreleased` (`:402`) | `composition: the composed maximum is taken over the windows that released their load (earlier rule)` | `... ([{'cycles': 700000, 'ms': 14.0, 'group': 'backlog', 'windows': 2, 'lower_bound': False, ...` |
| the same | `composition: the composed maximum is no lower bound where a window left its load unreleased` | `... ([{'cycles': 1500000, 'ms': 30.0, 'group': 'backlog-adp', 'windows': 3, 'lower_bound': False, ...` |
| the same | `composition: the composed maximum includes the fixture's short window` | `... ([{'cycles': 9000000, 'ms': 180.0, 'group': 'fixture', 'windows': 4, ...` |
| renamed: `a starved channel is reported by name, and its window reports its load unreleased` (`:201`) | renamed: `service: a window that left its load unreleased reports it released (earlier rule)` (same patch) | `MUTANT caught: service: a window that left its load unreleased reports it released (earlier rule): a starved channel is reported by name, and its window reports its load unreleased (...)` |

- The "(earlier rule)" on the first composed-maximum mutant restores round 3's rule: the longest pass of the windows that released their load (README at `f8876638`, `:200`).
- The mutants are function patches, like every other in `selftest_mutants.py`. The cost and records-ahead mutants recompute their figure under the defective rule. That keeps the `grade.py` lines R703-3's source mutants edit byte-identical.
- All 46 of R703's anchors (`review_mutants2.py`, `review_mutants3.py`) are unique at the head (`receipts/review-probes/anchor_check.txt`).
- The 52 round-3 mutants are all still caught.

Full-harness controls, regraded at the head (`receipts/head-regrade/C-*/run.log`), each rc 0:

- `CONTROL slow-adp-rx caught: every control path missed T_svc`
- `CONTROL slow-adp-shutdown caught: every control path missed T_svc`
- `CONTROL as-built caught: an instruction access fault (cause 1)`

## 5. Gate table

Every gate ran at the head `a66148f6b7e59e3f42c939f464fe76e2b05404d7`, one at a time, in the foreground of one runner (`scripts/gates_r4.py`), unpiped. Each log is in `receipts/gates/`, with its rc and the tree's state on its last lines (`HEAD.txt` names the head, and `summary.md` is the runner's table). The runner refuses to start on a dirty tree. After every gate it checks `git status --porcelain --untracked-files=all --ignore-submodules=none`, and it stops at the first gate that leaves the tree dirty; none did.

Environments:

- The Markdown gates and the rest ran with the pinned renderer (`tools/markdown/requirements.txt`), PyYAML and the docs workflow's `wavedrom==2.0.3.post3`.
- The HDL reference ran with `tools/hdl_reference/requirements.txt`.
- The end-station builder gate ran with the product LiteX environment and the pinned RV32 SDK first on `PATH`.
- Each environment is a scratch virtual environment outside the packet.

Key verdicts:

- `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))`.
- `self-test: 0 failures` (84 checks, 57 mutants caught).
- `check_em_dash: 0 finding(s) over 629 added line(s) in 1 changed Markdown page(s) ... [e76a755a..HEAD]`.
- `docs_check: 0 finding(s) across 211 md files + 1433 scrubbed text files`.
- `GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations`: the compiler-absent control, whose NOT RUN is the compiled census this mode hides by design.
- `ALL GATES PASS EXCEPT 1 NOT RUN`: the end-station builder. Gate 11 needs an mf48 calibration build tree that this host does not have.
- behave: 14 features, 406 scenarios, 1977 steps passed. The full log (377,097 B) is kept out of the packet, by sha256.

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
| `gptp_processor_docs` | `make -C gptp-processor docs python3` | 0 | clean |
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

- `act_ci.py --selftest`: AGENTS.md lets the candidate's copy run it only inside the disposable CI job. This lane does not change it.
- `ci_rv32_sdk.py --destination ...`: it installs the SDK, which is already at its pinned path; `ci_rv32_sdk_selftest.py` passed.
- The full serial sweep: the lane changes only files under `tb/verilator/ctrl_service_budget/`, and no shared file, as the brief allows.

Earlier, overlapping gate runs are kept in `receipts/superseded-concurrent/` (section 6). They are not this table's evidence.

## 6. Run history and reproducibility

- **No simulation ran this round.** Every figure comes from round 3's logs, regraded from copies on round 2's attested builds. `build.reused` still accepts those builds, because no build input changed. The scenario's group scripts are unchanged: the regrade refuses a stale script by name, and it refused none.
- **Regrades.** The first regrade ran at the unchanged `f8876638`. It is byte-identical to round 3's published `results.json` and `table.md` in all nine arms. The logs were then regraded at the working tree, and again at the committed head. Each time:
  - every group's JSON was byte-identical to the base;
  - `results.json` added only `composed_maximum`;
  - `table.md` changed only in the composed-window heading and the two composed-maximum lines.
- **Disclosed corrections during the round.**
  - The first edit of `scenario.py`'s docstring took the module to 1,001 lines, and the idiom gate's long-module ratchet failed. The paragraph was rewrapped before the commit, to 999 lines.
  - The first full gate run was stopped at the session's background limit inside the compiler-absent builder gate, which takes 635 to 828 s alone. Its wavedrom gates had failed for a missing package, which the docs workflow installs (`wavedrom==2.0.3.post3`). The package was installed in the scratch environment, and those gates were rerun.
  - The gate runs then overlapped. The first runner was still inside its own compiler-absent run when a second compiler-absent run and the next batch of gates started beside it. The first runner was then stopped at the session's limit, in the middle of that gate.
  - Several gates plant a defect in the checkout and restore it in a `finally`, among them the entity-shape self-test, the compiler-absent control and the end-station builder. A stopped process restores nothing. So `tb/verilator/csr/Makefile` was left holding one of the entity-shape self-test's planted arms: a rule-line `$(LATE_DIR)` reference.
  - My first tree checks piped `git status --short` through a counting command that a command wrapper rewrites. So they read "clean" while the tree was not, and the end-station builder gate ran once on the planted Makefile.
  - The file was restored to the committed content (`git checkout -- tb/verilator/csr/Makefile`, after its diff was confirmed to be exactly that arm). The tree and every submodule were then verified clean.
  - Every gate was then rerun, one at a time, by a runner that checks the tree after each (section 5). The overlapped runs' logs are in `receipts/superseded-concurrent/` and are not evidence.
  - Nothing in the harness, the regrades or the reviewers' probes reads that Makefile. The probes and the regrade were nonetheless rerun on the verified-clean head. The regrade is byte-identical to the earlier one (`receipts/head-regrade/compare_clean_tree.txt`); the probes are in section 7.
  - Checking the submodules' state, I ran a read-only `git submodule foreach ... git status` before the per-submodule toplevel and origin check the brief requires. The check followed at once: every submodule is its own toplevel, with its expected origin (`gptp-processor`, `protocol-processor`, `third_party/lwSRP`, `third_party/tsn-c-stack`, `third_party/verilog-axis`), and every one was clean.
  - The behave and `ci_events --selftest` logs exceed 200 KB. They are kept out of the packet; their tallies, sizes and sha256 are in their `receipts/gates/` logs.

## 7. The reviewers' probes, rerun unmodified

R703-3's scripts are byte-identical to their published copies (`review-evidence/665s2-r1/reviews/R703-3/scripts`, archive commit `5307bb5b`). They ran in R703's own sandbox layout, built from the committed head. That is `sandbox.sh`: links to the checkout, and a private copy of the harness.

| Probe | At `f8876638` (R703-3) | At the head |
|---|---|---|
| `review_mutants3.py` (21 source mutants) | 16 caught; G2, G3, G6, G9, H3 escaped | **18 caught; G6 and G9 CAUGHT**; G2, G3, H3 escape (`receipts/review-probes/review_mutants3.log`) |
| `review_mutants2.py` (25) | 23 caught; N11, N12 escaped | 23 caught; N11, N12 escape, unchanged (`receipts/review-probes/review_mutants2.log`) |
| Anchors of both (46) | - | every one unique at the head (`receipts/review-probes/anchor_check.txt`) |

- The scripts' digests are in `receipts/review-probes/script_identity.txt`.
- The sandbox's harness copy was compared with the head's (`diff -r`): identical.
- G6 fails `a fan-out's cost a recipient is its first to last commit over the gaps between them`, and G9 fails `a served record's records ahead are those not yet released at its commit`.
- R704-3 asked for no probe this round. Its residue items are R704-3-R1 to R4 in section 2.

## 8. Acceptance

| Item (round 4) | Status | Evidence |
|---|---|---|
| 1. F1: the bare-metal gate exits 0; the ring named as `mailbox.yaml` does; term table unchanged; gate in the validation list; every touched comment line checked | met | section 2; `receipts/f1/`; `receipts/gates/baremetal_check.log` |
| 2. F2: arm A's composed maximum over every window that commits the defined load, labelled a lower bound; the released-only figure beside it, labelled; README, PR body and hand-off agree; the S2b/S2c baseline named | met | section 1; README `:197-214`, `:437-441`; PR body Status |
| 3. F3: every fan-out range contains every cell | met | `receipts/f3/fanout_cells_and_ranges.txt` |
| 4. F4: named checks fail under G6 and G9; `review_mutants3.py` reports both caught | met | sections 4 and 7 |
| 5. Wording residue as written | met inside the lane's files and the PR body; `TESTING.md` (R-4 / R704-3-R1) left for the residue checklist | section 2 |
| STOP if a fix needs a firmware change or changes a measured cycle count | not triggered: no firmware change, and every group's grade is byte-identical | section 1 |
| Rows within T_svc | **not met**: the measurement STOP, under owner decision D4 and the cache-first decision | section 1 |

So the PR body says "Relates to #665".

## 9. Open items, risks and questions

- **For S2b and S2c:** re-base against arm A's composed maximum over every backlog window, window by window: at least 31.32 ms (1x1) and at least 44.19 ms (8x8). The released-only figure (14.81 / 27.84 ms) is not a baseline. A change that lets SRP be served in `backlog-adp` adds that window to it.
- **For the manager (carried from round 3):** whether these become Issues or S2b scope:
  - the ACMP owed-capacity drop (`ACMP_OWED_MAX` 8 against the ring's 12);
  - the SRP starvation under passes longer than the tick (`srp_mbx.c:441-451`);
  - the per-recipient fan-out cost (11,786 to 22,030 CPU cycles).
- **R-4 / R704-3-R1 not applied** (`docs/testing/TESTING.md:518`, a release-lane file).
- **R703-3 S1-S3 not applied** (optional). H3, a filter that drops passes over 1 M cycles, still escapes the self-test. G2 and G3 also escape and change no published value (R703-3).
- **N11 and N12** (R703-2) still escape, as before; no published value changes under either.
- The act runner's `--selftest` was not run on the host. AGENTS.md lets the candidate's copy run it only inside the disposable CI job, and this lane does not change it.
- `ci_rv32_sdk.py` was not run. It installs the SDK, which is already at its pinned path, and its self-test passed.
- Physical calibration NOT RUN; nothing here is hardware evidence.

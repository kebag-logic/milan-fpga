[R582] POSITIVE - exact head 8c8f82f628a24223e4ff7459f46a51735915351e

# R582-7: composition review of issue #665 / PR #704 (merge-train candidate)

- Candidate: `8c8f82f628a24223e4ff7459f46a51735915351e`, tree `126de790c9ebab9bbb0d95dd661ee6324a082ce9`.
- Parents: live dev `6bfeeb132fa0b1ad8a5b957446c66a498e633af7` and PR source head
  `67c1285b3b28b12a3af4f3f3aae6e92befd5febb`. Their merge-base is `554e61d299ef7ddb5aca6fb9ce0e6a6cd076d8cb`.
- Scope: composition acceptance only. The source head already has two independent POSITIVE reviews:
  - R583-6, #704 comment 6101681004;
  - R582-6, #704 comment 6101700655.
- Verdict: the composed tree adds no defect beyond the reviewed sources. This round opens no BLOCKER, MAJOR,
  MINOR, RESIDUE or SUGGESTION. Earlier public items are retained as listed in section 5. None of them is above
  RESIDUE.

## 1. What the composition is

Receipt: `receipts/composition_overlap.log`.

- The candidate is exactly dev plus the PR's 63 files, and exactly the PR head plus dev's 37 files. Every file
  that only one side changed carries that side's blob byte for byte (0 mismatches).
- Queued predecessors: none beyond live dev. M2 (#710, `ac2c5e77`) and M6 (#719, `6bfeeb13`) are already in dev.
- One file is changed by both sides: `sw/litex/milan_soc.py`.
  - PR #704 (+21/-2) touches only `class CtrlMailbox`: the docstring, the publication port widths, and the 11
    unread `o_pub_*` outputs (`milan_soc.py:2682-2703` at this head).
  - M2 #710 (+140/-8) adds `_cross_csr_bus`, `_crossing_storage`, `_payload_in_block_ram` and
    `_mac_cdc_rename`, and the two `MilanMAC` calls (`milan_soc.py:768-799`, `:1397-1490` and `:1801-1807`).
  - The hunks are about 1,700 lines apart. `git merge-file` merges them with no conflict, and the candidate's blob
    equals that three-way merge byte for byte (sha256 `8ea93ea66e1c69ad...`, 266,073 bytes).
- The submodule gitlinks are identical at the candidate, dev and the PR head.
- Semantic interactions examined. In each case the PR reads something dev changed, or the reverse:
  - **The census reads dev's RTL.** `publication_census.py` elaborates `milan_datapath`, which M6 changed: the
    `KL_avtp_rx_monitor_ctx` port `diag_cnt_o` became `diag_col_i`/`diag_q_o` (`milan_datapath.sv:3505-3533` at
    this head). It also reads `KL_pp_shadow`'s class-D ports; dev changed one comment line in that file.
  - **Gate 23m reads the composed `milan_soc.py`.** It holds `eb.datapath_params()` to the `Instance` that
    `add_milan_datapath` builds. M2 rewrote that function's CSR-crossing lines.
  - **The mailbox window and M2's crossings.** The mailbox window is a Wishbone slave in `sys`. M2's crossings
    are the datapath's AXI-Lite CSR bus (`milan_axil_cdc`) and the two MAC crossings.
  - **Registries and inventories.**
    - `scripts/ci_events.py` and `rtl-fast.yml`: changed by the PR only.
    - `scripts/measure_test_evidence_readers.py` (dev added two dispositions) against the PR's new campaigns.
    - `scripts/run_litex_sims.sh` (dev added `test_retained_cdc_storage`); the PR adds no LiteX simulation.
  - **Docs.** Dev's statements about the mailbox, against what the PR does:
    - `MARK_II_AREA_PLAN.md`: "holds packet and event inputs idle", "Its outgoing packet stream has no datapath
      consumer";
    - `AREA_BUDGET.md`: "The mailbox remains idle";
    - `PP_SHADOW_BASELINE_RECIPE.md:201`.
  - **TOC, anchors and em-dash** over both sides' Markdown.

## 2. Executed evidence on the candidate

Every gate was run from the candidate clone at the exact head. Each has a `.log` and a `.rc` file
(rc, wall time, head, argv) under `receipts/`.

| Gate | Result |
|---|---|
| `publication_census.py --check --selftest --jobs 6` (sv2v v0.0.12 and Yosys 0.66, the `rtl-fast.yml` pins) | rc 0. 6 shapes, `checks: 234 failures: 0`. 25 class-D nets (4 unread) and 39 reads of 21 nets in each shape, the source head's figures, now over dev's M6 datapath. `selftest: 0 of 120 arm(s) failed`, 31 `[ok] rule` lines, `mutations: 0 of 31 rule(s) no arm proves`. `--check` 95 s, self-test 343 s |
| `scripts/soc_gates.py`: the 16 `test_builder.py` gates that elaborate `milan_soc.py`, with the `--require-elaboration` verdict | rc 0. All 16 ran, `--require-elaboration: every elaboration arm ran`. Gate 23m: 5 real elaborations, 3/3 cuts rejected. 23g 5/5 (mutation 2/2). 23f 8 elaborations (mutation 8/8). 23d 7/7, 6/6 and 10/10. 1e 8 (mutation 6/6). 23l 4 (mutation 7/7). 23h 5 patches (mutation 5/5) |
| `sw/litex/test_retained_cdc_storage.py`, M2's own test of the composed `milan_soc.py` | rc 0: `0 failure(s)`, `RESULT: PASS`. Storage, block RAM, lockstep, order, depth and reset checks, with its controls failing as named |
| `scripts/mbx_soc_probe.py` + `scripts/mbx_soc_compare.py`: all 5 configs, `--ctrl-mailbox` on and off, stopped at `Builder()` | rc 0, `0 difference(s)`. Details below the table |
| `scripts/mbx_port_width_lint.py`, pinned Verilator 5.050, all 5 configs | rc 0, 0 WIDTH/PIN warnings. Every `KL_mbx`/`KL_mbx_wb` port the SoC binds has the RTL's width. Plant control: `pub_sid_o` one bit short is caught (1 WIDTH line) |
| `make -C tb/verilator/mbx -j6` with pinned Verilator 5.050 | rc 0: 402 (Wishbone), 447 (AXI4-Lite), 32 (cosim), 404, 449 and 389 (two interfaces) checks, 0 failures. `mbx mutants: 6 of 6 caught`. These equal the PR's stated figures |
| `scripts/builder_emit_compare.sh` (dev against the candidate) | rc 0. Every `configs/*.yaml` built at both revisions: 58 files written by the builder and the emitted SoC argv, 0 differences. The default build is unchanged by the composition |
| `gen_mailbox.py --check` / `--crosscheck` / `--selftest` | rc 0 each: 0 findings, 0 arms failed |
| `ci_events.py --check` / `--selftest`; `ci_scope.py --selftest` | rc 0: 1821 contract items over 4 workflows plus `CI_WORKFLOWS.md`; selftest 2530 arms; scope PASS |
| `check_baremetal_only.py --check` / `--selftest` | rc 0: 0 findings over 1261 files; 700 arms |
| `docs_check.py`, under both the system interpreter and the pinned Markdown venv | rc 0: 0 findings, 203 md files |
| `gen_toc.py --check` / `--verify-anchors` (pinned Markdown venv) | rc 0: 143 pages; 477 cross-page fragment links reproduced |
| `check_em_dash.py --base 6bfeeb13` / `--base 554e61d2` (pinned venv) | rc 0: 0 findings over 679 added lines in 9 pages (the same count R582-6 reported for the source), and over 2091 lines in 17 pages, arms 339/339 |
| `git diff --check 6bfeeb13 HEAD` | rc 0 |
| `measure_test_evidence.py --check` / `--selftest` | rc 0: dev's reader registry accepts the PR's new campaigns; 105/105 |
| `check_soc_sources`, `check_port_contracts`, `check_rtl_source_lists`, `lint_rtl --check` | rc 0 each. Lint is 90 at a ratchet of 90; 43 modules registered |
| `check_sweep_shape`, `check_deploy_shape`, `check_entity_shape --self-test`; `check_wire_accountability --self-test` | rc 0 each. The builder-generated headers equal the tracked ones (clean `git status` afterwards) |
| `check_doc_paths`, `check_doc_style`, `check_hygiene --check`, `check_solution_docs`, `check_feature_status`, `check_todo_ownership` | rc 0 each |
| `check_sv_idiom`, `check_cpp_idiom`, `check_py_idiom`, `measure_naming --check`, `measure_fail_fast --check`, `gen_module_matrix --check` | rc 0 each |

Details of the `--ctrl-mailbox` probe, per config:

- **Mailbox window.** Switching the mailbox on adds exactly one region (`ctrl_mbx` at `0x90100000`, size
  `0x8000`), one CSR bank (30) and one interrupt (3). No other region, CSR bank or interrupt moves, and no regions
  overlap.
- **M2 crossings.** All 49 storage arrays are identical with the mailbox on and off. M2's 8 split arrays are
  present, each read through a synchronous READ_FIRST port:
  - MAC TX and RX: 72x16 in block RAM and 2x16 in distributed RAM;
  - CSR W and R: 36x4 and 34x4 in block RAM, and 2x4 in distributed RAM.
- **Publication ports.** The 11 `pub_*` outputs have the contract's widths, and none is bound to a constant.
- **Negative control** (`receipts/mbx_soc_compare_plant.log`): a block array relabelled distributed and one
  moved CSR bank are both reported (rc 1).

The clone is restored (`receipts/clone_integrity_after.log`):

- `git status` is empty, and the index and worktree equal HEAD.
- The `ls-files -s` digest equals the HEAD tree's `ls-tree` digest (`71d9df56...`).
- The submodules are clean at their gitlinks.
- Ignored build products were removed.

## 3. Findings

None in this round.

## 4. Lens results

[R582] PASS Conformance - `receipts/composition_overlap.log`; `receipts/census_check_selftest.log`;
`receipts/builder_emit_compare.log`; `receipts/mbx_soc_compare.log`; `sw/litex/milan_soc.py:768-799,1801-1807,2682-2703` -
both acceptance sets hold together:
- PR 1's publication completeness, from rulings 6088423771 to 6100024293: the census over the composed datapath
  finds the same 25 nets and 39 reads in all 6 shapes with 0 failures.
- The "default build unchanged" rule (issue body: "behind a build switch whose default is the current
  all-fabric placement"): builder emission is identical to dev, and with the switch off the SoC holds no mailbox
  and its arrays are unchanged.
- M2's storage contract: 8 split arrays as specified in every config, with the switch on or off.

[R582] PASS RTL - `sw/litex/milan_soc.py:768-799` (`_cross_csr_bus`), `:1397-1490` (`_crossing_storage`,
`_payload_in_block_ram`), `:2636-2721` (`CtrlMailbox`, `add_ctrl_mailbox`);
`hdl/milan/milan_datapath.sv:3505-3533`; `receipts/mbx_soc/*.json`; `receipts/mbx_width_*.log`;
`receipts/test_retained_cdc_storage.log` - the crossing and the mailbox stay separate:
- `KL_mbx`/`KL_mbx_wb` run on `sys` on the CPU's Wishbone bus. They do not use `milan_axil_cdc` or the MAC
  crossings. Those crossings keep their depth (4 and 16), their widths and their READ_FIRST registered read
  word, and are identical with the mailbox on.
- Every bound port width matches the RTL, with a plant control.
- M6's port change is internal to the datapath and is elaborated by the census.
- No new clock crossing appears in the composition.

[R582] PASS Robustness - `receipts/test_retained_cdc_storage.log` (reset in flight, full depth, lockstep at two
clock ratios on the composed file); `receipts/mbx_soc_compare.log` and `receipts/mbx_soc_compare_plant.log` (the
switch-on and switch-off configurations of all 5 configs); `receipts/mbx_make_all.log` (the bench's reset, hole
and strobe paths); `receipts/soc_gates_require_elaboration.log` (`test_soc_option_refusals`) - the M2
crossings' reset and depth behaviour, and the mailbox's configuration-dependent presence, are unchanged by the
composition.

[R582] PASS Tests - gate 23m and its 3 cuts on the composed `milan_soc.py`; the census self-test (120 arms) and
rule removals (31) over dev's datapath; `receipts/ci_events_check.log` and `ci_events_selftest.log` (job
inventory); `receipts/measure_test_evidence_check.log` (dev's reader registry against the PR's campaigns); the
mbx bench and 6/6 plants; M2's test - every inventory both sides feed agrees, and every gate that reads
`milan_soc.py` passes. My own probes carry negative controls: the width plant and the comparator plant.

[R582] PASS Docs - `receipts/docs_check_mdvenv.log`, `gen_toc_check.log`, `gen_toc_verify_anchors.log`,
`check_em_dash_base_dev.log`, `check_em_dash_base_prsrc.log`; `docs/design/MARK_II_AREA_PLAN.md:416-421`,
`docs/design/AREA_BUDGET.md` ("The mailbox remains idle"), `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:201`
against `milan_soc.py:2636-2650` - the documents are consistent:
- Dev's statements about the mailbox stay true: the PR's publication outputs are unread and the inputs are
  still tied idle.
- There is no shared table or anchor collision.
- The composition adds no Markdown beyond the PR's 679 lines.

## 5. Earlier public findings, resolved or retained at this head

I read these after my own pass.

- **Resolved findings.** Every MAJOR and MINOR of rounds R582-1 to R582-5 and R583-1 to R583-5 is recorded as
  resolved by both source reviews. The composition changes none of their files except `milan_soc.py`, and only
  outside `CtrlMailbox`, so they stay resolved.
- **Retained RESIDUE.** These are pre-existing and wording only. They are carried to the manager's residue
  checklist with the exact fixes their authors gave:
  - **R582-6-R1** (PR body: hosted figures and review status). Still present: PR body Status "No review of this
    head has run yet" and Known limitations "No hosted run of this head exists".
  - **R583-6-R1** (PR body, round-3 "Item 3" row). Still present.
  - **R583-6-R2** (`tb/verilator/mbx/Makefile:64-65` comment). Unchanged at this head; dev does not touch the
    file.
- **Retained SUGGESTION** (optional; nothing in the composition changes them):
  - **R583-6-S1**: still 5 `configs/*.yaml` = the 5 `CONFIGS` at `sw/builder/test_builder.py:347`.
  - **R582-6-S1** and **R583-6-S2 = R582-6-S2**.
  - **R582-6-S3**: its `milan_soc.py:811,2550-2551` are now `milan_soc.py:841` (`milan_cd`) and `:2682-2683`
    (`KL_mbx` on `sys`). M2's CSR crossing does not change which crossing PR 2 owes.

## 6. Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition: overlap/merge receipt, census over the composed datapath, builder emission against dev, mailbox on/off probe. Parts the composition does not touch (firmware writers, contract, census logic): R583-6 (6101681004) and R582-6 (6101700655) | R582-7 (this round); source part R583-6, R582-6 | `8c8f82f628a24223e4ff7459f46a51735915351e`; source `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |
| RTL | CLEAN | `milan_soc.py` M2 and mailbox hookup, the M6 datapath via the census, port-width lint, the M2 crossing test. Mailbox RTL internals (untouched by dev): R583-6, R582-6 | R582-7; source part R583-6, R582-6 | `8c8f82f6...` as above; `67c1285b...` |
| Robustness | CLEAN | M2 reset and depth on the composed file, switch-on/off configurations, the bench's reset and strobe paths. Firmware failure paths (untouched by dev): R583-6, R582-6 | R582-7; source part R583-6, R582-6 | `8c8f82f6...`; `67c1285b...` |
| Tests | CLEAN | Gate 23m and cuts, the 16 SoC-elaborating builder gates, census self-test and mutations, `ci_events` / `measure_test_evidence` registries, mbx bench. Firmware plants and the 175 RTL plants (untouched by dev): R583-6, R582-6 | R582-7; source part R583-6, R582-6 | `8c8f82f6...`; `67c1285b...` |
| Docs | CLEAN | Docs, TOC, anchor and em-dash gates on the composed tree; dev's mailbox statements against the PR. PR-authored pages: R583-6, R582-6 (RESIDUE retained, section 5) | R582-7; source part R583-6, R582-6 | `8c8f82f6...`; `67c1285b...` |

The composition touches every lens. Each lens is CLEAN at the candidate for the composed scope, and is covered
at the source head by both source reviews for the rest. Each source part is an ancestor whose lens scope dev does
not touch, except `milan_soc.py`, which this round covers.

## 7. Real limits

- **No synthesis or implementation.** Block-RAM inference of M2's arrays with `--ctrl-mailbox` on is shown
  structurally only: the arrays and their attributes are identical on and off. No Vivado and no hardware.
  Physical calibration NOT RUN; field skips are not hardware proof.
- **Builder gates are a focused subset.** I ran the 16 `test_builder.py` gates that elaborate `milan_soc.py`,
  not the full builder bank. The manager's candidate bank was not re-run or relied on.
- **Not run here, because dev changes none of their inputs:**
  - the firmware gates (they need `third_party/lwSRP`, not checked out in this clone);
  - the Yosys run of the mailbox tops;
  - the full 175-arm `mutants.py`;
  - the parent, protocol-processor and gPTP suites;
  - `run_litex_sims.sh` beyond M2's own member.
- **Interpreter.** The local interpreter is CPython 3.14.7; CI uses the runner's Python 3. The first runs of
  `gen_toc`/`check_em_dash` under the system interpreter refused for want of the pinned Markdown renderer.
  The receipts are the reruns with the pinned renderer venv (exact `tools/markdown/requirements.txt` set).
- **No hosted or act evidence at the candidate.** The candidate is a local merge commit. Hosted and act
  acceptance are the manager's.

## 8. Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts
  on the PR.
- Hosted exact-head `rtl-fast` (including `publication-census` and `firmware-unit`), `verilator-suites` and
  `yosys-portability` on the PR head that merges, and the act replica.
- Carry R582-6-R1, R583-6-R1 and R583-6-R2 to the residue checklist.
- Obtain the maintainer's explicit merge authorization, then the post-merge containment check and the issue
  bookkeeping.

R582-7 FINISHED

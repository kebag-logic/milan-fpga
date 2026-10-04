[R479] POSITIVE - exact head d5e743440a56c77c43241879226b851abb3c62ac

# R479-2: external review of PR #660 / issue #652, round 2

- Head `d5e743440a56c77c43241879226b851abb3c62ac`, tree `9a481b19651cc534966c94be0a68e3487299e6e2`, in a detached clone that was byte-verified after the probes (`receipts/c9_clone_integrity.txt`).
- Source base `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`. Merged dev `c0280fc008ef9c5c1650402a58bab3e47a92127b`, which is still the live dev tip (`receipts/c8/c8_merge.txt`).
- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs. Every lens is CLEAN at this head.
- Open items: three new SUGGESTIONs (S4 to S6) and one RESIDUE (R1). Two earlier SUGGESTIONs stay open (S1 and S3). No BLOCKER, MAJOR or MINOR is open.

## Reconstruction

I read the following, in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. The #652 issue body and acceptance 1 to 3.
3. The lane comment, the executor's STOP, and the ruling (option 1, items 1 to 4).
4. The round-2 assignment (#652 comment 5984666082) and REVIEW READY round 2 (5985156837).
5. The PR #660 body.
6. `git diff 6c22d3ca..d5e74344` and the history. I read the lane's own delta `ef236411..d5e74344` (4 commits) in full, and the merge `ef236411` separately.
7. The published evidence on `652-review-evidence`. This means the round-1b packet at `7ac6966b` and the round-2 author packet at `9a0b6ded` (`author-r2/r2/...`).

I read the prior round's findings (R478-1 and R479-1) only after my own pass and draft verdict, and resolved them in "Prior public review findings" below. I read no other reviewer's round-2 material.

## Delta under review (`2f0f5929..d5e74344`)

| Commit | Change | What I checked |
|---|---|---|
| `ef236411` | `--no-ff` merge of dev `c0280fc0` | Its tree `7d14122b` equals `git merge-tree` of its two parents. Dev's 12 files are identical to `c0280fc0` at the merge and at the head. The lane's 12 files are identical to `2f0f5929` at the merge. The two file sets do not overlap. |
| `b71979dc` | Check 14 moved to `scripts/nvm_allocation_table.py`. A row whose cell count differs from the header's is a finding. Two new controls: `short_allocation_row` and `long_allocation_row`. | c1, c2 (`a_*`), c3 |
| `694e2b18` | `generate_shapes()` split out of `command_shapes`. Stand-in-builder arm `_shapes` in `syn/resmap/yosys_sweep_selftest.py`. End-to-end `build()` arm `_selftest_build` in `resmap_models.py`. | c2 (r3, r11 and others) |
| `94a12eb8` | `"cause"` pinned on both expected refusals. `load_plan` refuses a refusal with no cause, and a cause on a variant expected to build. The real builder's line is read for both variants. | c2 (`y_*`), c4 |
| `d5e74344` | Each plan-validation arm now requires its own refusal message. | c2 (`y_plan_*`) |

## Findings

### S4 - SUGGESTION - Robustness, Tests - `scripts/nvm_allocation_table.py:112-113`: check 14 does not require the two summary rows

- **Evidence.**
  - Check 14 requires a row for every `ALLOC` group: deleting the user-name row gives "no row for ['NAME']", rc 1 (`receipts/c3/c3_plants.txt`, p7).
  - The `records` and `highest id` rows are not required. Deleting the `records` row gives rc 0, along with the line "every allocation-table figure ... is the derived one" (p6).
- **Impact.** No wrong figure can pass. A deleted row states nothing, and every row that is present is checked cell by cell (p1 to p5, p8 all give rc 1). The page would simply stop stating the record total, or the highest id, without the gate noticing.
- **Optional outcome.** Require the two summary rows as the group rows are required. Or scope the docstring at `scripts/check_nvm_record_space.py:90-91` ("a dropped figure is never an unchecked one") to figures dropped from a row.
- **Verification.** Re-run `scripts/c3_page_plants.sh`. Plant p6 should then give rc 1.

### S5 - SUGGESTION - Robustness - `scripts/nvm_allocation_table.py:52-60` (`_allocation_width`): a width finding names the last column, whichever cell was dropped

- **Evidence.**
  - Dropping the 1x1 figure from the `highest id` row reports "highest id has no 8x8 figure" (p4).
  - Dropping the block cell from the user-name row reports "user name has no 8x8 figure" (p8).
  - The verdict is right in both cases (rc 1). The message also prints the cell count ("5 cells under a 6-column header").
- **Impact.** Diagnostic only: an editor is pointed at the wrong column. The PR body's "naming the column with no figure" holds only when the dropped cell is the trailing one.
- **Optional outcome.** Word the width finding positionally, for example "a figure is missing: the row ends at the 1x1 column".

### S6 - SUGGESTION - Tests - `.github/workflows/` (no reference to `syn/resmap`): the resmap self-tests run in no hosted workflow

- **Evidence.** Neither `.github/workflows/*.yml` nor any repository suite runner calls `yosys_sweep.py --selftest` or `resmap_models.py --selftest`, at base `6c22d3ca` or at the head. R478-1 F1's arms live in those self-tests.
- **Impact.** The arms are now correct and turn red for r3 and r11 (below). They still hold the `shapes` verdict and the `by_builder` producer only when someone runs them, as the docs.yml record-space gate does for check 14.
- **Scope.** This predates #652 (#649's design) and is outside its acceptance. It is a candidate new Issue, not a change for this lane.

### R1 - RESIDUE - Docs - PR #660 body, "Status", second paragraph: "No RTL, testbench, builder or configuration file of this lane changed after it."

- **Evidence.** `git diff --stat d33bdc3d 2f0f5929 -- sw hdl tb configs` shows `sw/builder/test_builder.py` changed after `d33bdc3d`, in commit `0da678f0` (gate 24a). No RTL, testbench, `endstation_builder.py` or configuration file changed. The conclusion the sentence supports therefore stands: the Verilator sweep and Yosys tops read none of the changed files. Only the wording is wrong.
- **Exact fix.** Replace the sentence with: "No RTL, testbench, `endstation_builder.py` or configuration file of this lane changed after it; the builder's test bank `test_builder.py` did (gate 24a), and that bank was re-run at this head."

## Prior public review findings, resolved or retained at this head

| Finding | Status at `d5e74344` | Evidence |
|---|---|---|
| R478-1 F1 (MINOR, Tests and Docs): the `shapes` fail-closed comparison and the `by_builder` producer held by no self-test | **Resolved** | See the notes below this table. |
| R479-1 F1 (MINOR, Robustness and Tests): check 14 passes a 4.2 row that lost a column figure | **Resolved** | See the notes below this table. |
| R479-1 S2 / R478-1 S2 (SUGGESTION): `expect: refused` accepts any refusal | **Resolved (taken)** | `sweep_plan.json:58,62` pin `"writable names and the saved-state backend holds"`. On the real step, a plan pinning a foreign cause gives rc 1, "refused without the cause the plan pins" (`c4_foreign`). Planting `y_foreign_false` or `y_foreign_not_counted` turns the self-test red ("a refusal without the pinned cause exited 0, not 1"). A plan pinning a true substring ("NAME records") still passes (`c4_othertext`, rc 0), as a substring pin should. |
| R479-1 S1 / R478-1 S1 (SUGGESTION): `nvm_contract.py` `ALLOC["NAME"] = (0x80, 128)` | **Retained as SUGGESTION, ruled no change** (#652 comment 5984666082, item 4) | `ALLOC` is the record-space gate's independent expectation, and the PR body says so (Round 2, "S1, no change"). The drift path is disclosed under Known limitations. |
| R479-1 S3 / R478-1 S3 (SUGGESTION): `ID_NAME_C + N_NAME_MAX_C` filling `record_id[7:0]` unchecked | **Retained, open, disclosed** | The PR body lists it under Known limitations ("Open (R479-1 S3, R478-1 S3)"). |

- **R478-1 F1, resolved.**
  - r3 (`failures += outcome != expected` -> `failures += outcome == "failed"`), re-planted with R478-1's own `scripts/mutate_module.py` (sha256 `e0a4c996...`, unchanged), turns `yosys_sweep.py --selftest` red. Its two problems are "an unexpected refusal exited 0, not 1" and "an expected refusal that builds exited 0, not 1" (`receipts/c2/r3.log`).
  - r11 (`result["guards"]["by_builder"] = builder` -> `pass`) turns `resmap_models.py --selftest` red: "with a builder-refused point, guards.by_builder is None" (`r11.log`).
  - Both unmutated controls are green (`ctl_ys`, `ctl_rm`).
  - Four further mutants also go red: `y_shapes_rc0`, `y_crash_is_built`, `m_by_builder_every_point` and `m_by_builder_always_written`.
  - The PR body's claims (Description, `yosys_sweep_selftest.py` row; Round 2, `694e2b18` row; Known limitations) match what the arms hold.
- **R479-1 F1, resolved.**
  - My round-1 reproduction (the 8x8 user-name figure dropped) now gives rc 1: "0x80 .. 0xFF user name has no 8x8 figure" (`c3`, p1).
  - An extra cell (p2), a short `records` row (p3), a short `highest id` row (p4) and a dropped block cell (p8) each give rc 1. An emptied cell gives a value finding (p5).
  - `--self-test` runs 21 controls, all red as required, `short_allocation_row` and `long_allocation_row` among them (`c1/nvm_space_self.log`).
  - Disabling the width rule (with `strict=False`) leaves both new controls rc 0, so the self-test goes red (`a_width_off_nonstrict`).
  - Disabling the width rule alone turns both new controls into tracebacks, which the self-test also counts as red (`a_width_check_off`).

## Lens results (clean lenses in findings format)

```text
[R479] PASS Conformance - issue #652 acceptance 1-3, ruling 5983995755 items 1-3, round-2 assignment 5984666082 items 1-5, against syn/resmap/sweep_plan.json:58,62, syn/resmap/yosys_sweep.py:111-135,353-382, scripts/nvm_allocation_table.py, docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md tables; receipts c4/, c5/, c6/, c8/ - checked:
  - The real `shapes` step at the head gives rc 0, with 7 built and the 2 eight-stream TDM8 variants refused as expected. Each refusal line names 235, 128 and hdl/milan/KL_nvm_backend.sv:247 (c4_tracked).
  - Each of three planted plans gives rc 1: a foreign cause, an unmarked refusal, and the 2x2 expected refused (c4_foreign, c4_unmarked, c4_2x2refused).
  - The #649 page was regenerated from #649's published inputs (113a1fb9). The base code reproduces the published models.json byte for byte.
  - The head's models over the reconstructed summary (57 published entries, plus 2 builder records carrying my own live refusal lines) have sha256 659e3420..., identical to the author's round-2 figure. guards.by_builder = [streams-8, streams-8-chans-2].
  - `resmap_tables.py --page`: "every table equals a fresh generation", rc 0, over 26 table blocks (c6).
  - Five tracked configurations: base 6c22d3ca and head builders give 50 artifacts. They are byte-identical (diff -r rc 0, sha256 list cmp rc 0), and both trees stay clean. Every hash is in the author's round-2 manifest (c5).
  - The --no-ff merge keeps both sides (c8).
  - Round-2 item 4: the S1 statement is in the PR body, and S3 is listed open.
[R479] PASS RTL - hdl/milan/KL_nvm_backend.sv:247,293-295 at base and head; tb/verilator/nvm_backend; merge ef236411; receipts c7/, c8/c8_merge.txt, c1/lint_rtl.log - checked:
  - The lane's round-2 delta touches no RTL or testbench file. The dev RTL and testbench the merge brought in (KL_crf_rx.sv, milan_datapath.sv, crf_rx and milan_dp benches) are byte-identical to dev c0280fc0 at the head.
  - Pinned Verilator 5.050 (wrapper $VALIDATION_TOOLS/pinned-verilator-5.050, reports "5.050 2026-07-01 rev v5.050"), lint-only -Wall, N_NAME_P 0/1/99/128/129/235: identical rc and identical g_refuse_names message at base and head (0, 129 and 235 refused; 1, 99 and 128 clean).
  - The builder's nvm_name_capacity() returns (128, hdl/milan/KL_nvm_backend.sv:247).
  - nvm_backend suite: 541 + 210 = 751 checks, 0 failures, its four negative controls red.
  - lint_rtl --check: 90 <= ratchet 90.
[R479] PASS Robustness - scripts/nvm_allocation_table.py:52-114, syn/resmap/yosys_sweep.py:111-135,336-382; receipts c3/c3_plants.txt, c4/, c2/ y_plan_*, y_crash_is_built - checked:
  - Eight planted 4.2 edits on a disposable copy:
    - short and long rows, an interior cell dropped, an emptied cell, a dropped block cell and a deleted group row each give rc 1 with no traceback;
    - a deleted summary row gives rc 0 (S4, suggestion).
  - load_plan refuses each of: an expectation that is neither built nor refused; an expected refusal with no cause; a cause on a built variant. Each is refused with its own message: removing any one check reddens its own arm.
  - A crash is never read as a build or a refusal.
  - A substring pin that is true of the real line still passes.
  - S4 and S5 are recorded as suggestions.
[R479] PASS Tests - syn/resmap/yosys_sweep_selftest.py:47-151, syn/resmap/resmap_models.py:477-497, scripts/check_nvm_record_space.py:303-336, sw/builder/test_builder.py gates 38 and 24a; receipts c2/c2_mutations.json, c1/ - checked:
  - 22 in-memory runs: 3 unmutated controls are green; 15 targeted mutants are red; 4 informational probes are logged as they fell (y_cause_ignored_case and a_strict_off green; m_build_ignores_plan_path and a_width_no_continue red).
  - r3 and r11 are red, as above.
  - The _outcome arm runs the real builder on BOTH plan variants and requires the pinned cause, with nothing written.
  - The _shapes arm passes when every outcome is the expected one, and gives rc 1 for each of four surprises.
  - The five resmap self-tests give rc 0.
  - check_nvm_record_space and --self-test give rc 0 (21/21 controls red). The three allocation --mutate controls give rc 1 with their required FINDING.
  - Gate 38 is 9/9 with its RTL arm under pinned Verilator. Gate 24a (d) is 2/2 and (e) is 2/2. Gate 24b is 8/8.
  - The builder bank was not re-run here. The author's published bank at this exact head gives rc 0 and ends "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11: mf48 tree absent) (9a0b6ded author-r2/r2/gates/bank).
[R479] PASS Docs - docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:88, syn/resmap/sweep_plan.json:3, syn/resmap/yosys_sweep.py:34-41,61-64, scripts/check_nvm_record_space.py:88-91, scripts/nvm_allocation_table.py:1-13, syn/resmap/yosys_sweep_selftest.py:1-19, PR #660 body (Round 2, Description, Known limitations); receipts c1/ - checked:
  - Each changed statement matches the behaviour measured in c2, c3 and c4.
  - These gates give rc 0 under the pinned Markdown renderer environment: docs_check, check_doc_paths (912 paths), check_doc_style, gen_toc --check and --check-anchors.
  - check_em_dash gives 0 findings, both with --base c0280fc0 (66 added lines) and with --base 6c22d3ca (179 added lines).
  - check_py_idiom reports "long module: 10 <= 10". The two moved modules are 951 and 949 lines.
  - Commits since 2f0f5929 are one line each with no trailers.
  - R1 (PR-body wording) is RESIDUE and does not affect the lens.
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #652 acceptance, ruling, round-2 items; `sweep_plan.json`; `yosys_sweep.py` shapes/load_plan; the #649 page against a fresh generation (c6); byte identity (c5); real and planted `shapes` (c4); merge (c8) | R479-2 | `d5e743440a56c77c43241879226b851abb3c62ac` |
| RTL | CLEAN | `KL_nvm_backend.sv:247,293-295` guard parity, base vs head (c7); `nvm_backend` suite, 751 checks; merged dev RTL byte-identical to `c0280fc0`; `lint_rtl` | R479-2 | `d5e743440a56c77c43241879226b851abb3c62ac` |
| Robustness | CLEAN (S4, S5 suggestions) | check 14 page plants p1 to p8 (c3); `load_plan` and classifier mutants (c2); planted plans (c4) | R479-2 | `d5e743440a56c77c43241879226b851abb3c62ac` |
| Tests | CLEAN (S6 suggestion) | 22 in-memory mutants including r3 and r11 (c2); `--self-test` 21/21; resmap self-tests; gates 38, 24a and 24b (c1); the published builder bank at this head | R479-2 | `d5e743440a56c77c43241879226b851abb3c62ac` |
| Docs | CLEAN (R1 residue) | 649 page line 88; plan description; module docstrings; PR body; doc gates under the pinned renderer (c1) | R479-2 | `d5e743440a56c77c43241879226b851abb3c62ac` |

## Real limits

- **Full builder bank not run by me** (scope). I ran gates 38, 24a and 24b alone. The full-bank PASS at this head is the author's published receipt, not my run. Gate 11 is NOT RUN on that host.
- **No full Verilator sweep, Yosys, PP or gPTP bank** (scope). `nvm_cosim` was not run by me. The dev RTL the merge carried (#653/#655) was not re-validated here beyond confirming its bytes equal dev `c0280fc0`.
- **The #649 summary was reconstructed, not re-run.** The head's `summary` step needs #649's point receipts, which are not published. I replaced the two refused points' published entries with builder records carrying my own live refusal lines, then ran the head's models and tables code on it. No point was re-priced, and no Yosys or Vivado ran.
- **Hosted CI.** At 2026-10-04T22:42Z the exact head had these results (`receipts/c8/c8_check_runs_head.tsv`):
  - success: bdd-conformance, changes, docs-check-no-git, full-ci-gate, verilator-lint, wire-accountability, Verilator shard 3/5, Yosys shards 0-3/4;
  - still in progress: docs-check, elaborate, yosys-elaboration, Verilator shards 0, 1, 2 and 4/5;
  - skipped context, not executed: Physical gPTP (nightly and manual).
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Third-party tool.** The mutation tool `scripts/mutate_module.py` is R478-1's published script, copied unchanged (sha256 recorded in MANIFEST). `check14_mutant.py` is mine: the record-space self-test re-runs itself per control, so it plants the defect in each control's own process instead.
- **Redaction.** One receipt (`receipts/c7/c7_nvm_backend.log`) had a host-local tool image path, replaced by `$PINNED_VERILATOR_IMAGE`.
- **Restore.** The `external` submodule is uninitialised in this clone, as cloned. The three required gitlinks match their checkouts. All probes ran in disposable copies under `scratch/`, and all eight copies were clean at the end (`receipts/c9_scratch_copies_status.txt`). The review clone: HEAD, tree, index modes and oids, and all 1,011 tracked blobs re-hashed are equal to the head (`receipts/c9_clone_integrity.txt`).

## Pending manager duties

- The exact-head hosted contexts still in progress (above) must complete green. Run the `act` replica per AGENTS.md section 5.
- Build and validate the candidate merge on the live dev tip. That was `c0280fc0` at review time, and source validation here is distinct from it.
- Carry R1 to the residue checklist.
- Consider new Issues for S4 to S6 and the retained S1 and S3. None blocks this PR.
- Physical calibration remains NOT RUN.
- Publish this report and the listed receipts. Merge only on explicit maintainer authorization.

## Receipts

The scripts under `scripts/` are portable. Each takes its tree and receipt paths as arguments.

| Campaign | Script | Receipts |
|---|---|---|
| c1: focused gates | `scripts/c1_focused_gates.sh` | `receipts/c1/` |
| c2: in-memory mutants | `scripts/c2_mutations.py`, `scripts/mutate_module.py`, `scripts/check14_mutant.py` | `receipts/c2/` |
| c3: 4.2 page plants | `scripts/c3_page_plants.sh` | `receipts/c3/` |
| c4: real and planted `shapes` | `scripts/c4_shapes.sh` | `receipts/c4/` |
| c5: byte identity | `scripts/c5_byte_identity.sh` | `receipts/c5/` |
| c6: #649 page | `scripts/c6_page649.sh` | `receipts/c6/` |
| c7: RTL guard and nvm_backend | `scripts/c7_rtl.sh` | `receipts/c7/` |
| c8: merge and hosted contexts | (inline git and API reads) | `receipts/c8/` |
| c9: restore and integrity | (inline) | `receipts/c9_*.txt` |

R479-2 FINISHED

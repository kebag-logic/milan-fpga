[R828] POSITIVE - exact head 2155eb9666693c0404aadb34ac4dad10a2466e24

External independent review, round R828-3, of issue #870 / PR #889: a composition review of the merge-train candidate on `dev-soft-core`.

- **Head and tree.** Head `2155eb9666693c0404aadb34ac4dad10a2466e24`, tree `ea03711b42313e28662ea623301a0c5b2c435b37`.
- **Base.** Merge base `1d6bf555`. `dev-soft-core` is at `8b1bdfaf` (S7 #874 and #823 #880 merged), whose tree `466d464a` is the recorded #823 candidate `e282ecd2`'s.
- **Previously reviewed head.** `a69fc0f5`, which is composed in the manager's candidate `7a4871d5`.
- **The delta since then** is one line: `sw/builder/test_builder.py:23853` adds `"nvm_split"` to gate 23o's `RECIPE_SHAPE_ARTIFACTS`.

The verdict is POSITIVE. Every intent of both sides survives the composition. The one gap open at `7a4871d5` was the previous round's F1: gate 23o did not hold #823's `nvm_split.json`. That gap is closed at this head, and the fix is shown to bite. Every lens is clean. No BLOCKER, MAJOR or MINOR is open. Three suggestions and three carried RESIDUE items are listed below.

## 1. Composition identity

These results come from `receipts/composition.log`, produced by `scripts/composition.sh`.

- **`7a4871d5` reproduces exactly.** `git merge-tree --write-tree 8b1bdfaf a69fc0f5` gives `63b2a1605248b1804de5d22e4cdf134fa41981e7` with no conflict. That is `7a4871d5`'s tree, read from its commit object: parents `e282ecd2` and `a69fc0f5`.
- **The head composes cleanly.** `git merge-tree --write-tree 8b1bdfaf 2155eb96` gives `d5cf412b54aa3e0c87781495eb5c289ac6d76649` with no conflict. Its only difference from `7a4871d5` is the one line of `test_builder.py` above.
- **No side loses a line.** For each of the seven files both sides changed, every line each side added or removed appears in the composition unchanged. The comparison is `-U0` in both directions: `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md`, `endstation_builder.py`, `test_builder.py`, `ctrl_memory_ledger.py`, `milan_soc.py` and `test_ctrl_memory.py`, each "S9 lines kept; dev-soft-core lines kept". Six of the seven have identical per-file patch-ids. `endstation_builder.py` differs only in context lines, because `_derive_artifacts` and `BuildArtifacts` are adjacent hunks.
- **Submodules agree.** All six gitlinks are equal at the base, on `dev-soft-core`, at the head and in the composition.

## 2. Semantic composition, file by file

The composition is `d5cf412b`, checked out in a scratch clone as commit `ac5ee529`.

- **`endstation_builder.py`.** S9's `_derive_artifacts(config_path, placement)` applies `with_placement` before #823's `emit_nvm_split(overlay)`. So the split recipe writes `nvm_split.json` from the same overlay as the all-fabric build. The `paths` dict carries both sides' keys, and `--placement split` still refuses `--write-rtl` and `--write-fragment`.
- **`milan_soc.py`.** In the `--ctrl-mailbox` branch, #823's read of `nvm_split.json`, `split_constants(...)` and `stage_bytes(_nvm_shape)` sit after S9's DDR3, bridge and manifest changes, with no duplicated statement. No caller of the old `stage_bytes(shape, donor)` signature remains: `git grep "stage_bytes("` finds only the one-argument form. #823's `journal_klj3` entry in `FLASHBOOT_RESERVED` and S9's CSR-map changes meet in the split flash map, which the split boot simulation generates from the split export's `csr.csv`. Both shapes boot to ready on it (section 4).
- **`ctrl_memory_ledger.py` and `test_ctrl_memory.py`.** S9's mapper arm (item 8) runs on #823's `STAGE_1X1, STAGE_8X8 = 3454, 13594`. `test_ctrl_memory.py`: 0 failures, `RESULT: PASS`.
- **`test_builder.py`.** The gate IDs do not collide: S9 adds 23n, 23o and 23p, and #823 adds 39. No `def test_` name is defined twice.
- **`MAILBOX_SPLIT.md`.**
  - S7's `make srptx` paragraph (`:2027-2035`) and S9's identity section (`:1602-1648`) agree.
  - "Its shape artifacts are the all-fabric build's byte for byte (builder gate 23o)" (`:1607-1610`) is true at this head and was not true at `7a4871d5`.
  - `docs/ENDSTATION_BUILDER.md:1073` (row 34a) says the same and gives no artifact count.
- **`SPLIT_CONTROL_MEMORY.md`.** S9's section 4 replaces the "DDR3 stays instantiated" paragraph. #823's KLJ3 lines (`:147-148`, `:178-179`, the section 5 KLJ3 table) are separate, dated statements, so none contradicts S9's section 4.

## 3. The delta at this head, and the previous round's F1

The probe is `scripts/probe_23o.py`. It runs only `test_placement_recipe`. Its plant patches `_derive_artifacts` so that only the split recipe's `nvm_split` differs: the first block's count plus one.

| Tree | Unplanted | Planted `nvm_split` divergence |
|---|---|---|
| head composition `d5cf412b` | PASS, "9 shape artifacts" (`receipts/probe23o-compH-clean.log`) | **caught**: "the recipe's nvm_split is not the all-fabric build's" for all 5 configs, rc 1 (`receipts/probe23o-compH-plant.log`) |
| candidate `7a4871d5` (tree `63b2a160`) | PASS, "8 shape artifacts" (manager's `manager-builder/48.log:159`) | **not caught**: rc 0, "8 shape artifacts" (`receipts/probe23o-cand7a-plant.log`) |

The full builder bank at the head composition is also green (section 4). The previous round asked for "the PLANT line must read caught, and gate 23o plus `test_builder.py --require-rv32` must stay green". Both hold.

The comment rule: the delta adds no source comment, so there is no new RESIDUE.

## 4. Gates at the head composition (`d5cf412b`, commit `ac5ee529`)

The tools were:

- the pinned Verilator `5.050 2026-07-01 rev v5.050`;
- the RV32 SDK verified by `scripts/ci_rv32_sdk.py --verify-only` (archive sha256 `d42680e9...`);
- the bank interpreter used by the manager's candidate run;
- the product LiteX tree's interpreter for the split boot and the memory test.

| Gate | Result | Receipt |
|---|---|---|
| `test_builder.py --require-rv32`, the full inventory | rc 0. Ends `ALL GATES PASS EXCEPT 1 NOT RUN`; the only NOT RUN arm is gate 11, the calibration report, which needs the mf48 build tree, as at the candidate. 23n, 23o (9 artifacts), 23p (1 bound-bitstream control and 13 plants) and 39 (10/10 plants) all pass. The SDK made 2,472 compiler calls, 51 of them nonzero, the same profile as the manager's candidate run. | `receipts/builder-compH.log`, `receipts/builder-compH-sdk-argv.jsonl` |
| `sw/litex/test_ctrl_memory.py` | 0 failures, `RESULT: PASS` | `receipts/ctrlmem-compH.log` |
| split boot, 1x1 | PASS, 0 findings. Ready at 86.487 ms (the source-head receipt says 84.425 ms). The trace's first 18 writes equal `configure_fabric()`'s 15 and MAAP's 3. | `receipts/splitboot-1x1-compH.log` |
| split boot, 8x8 | PASS, 0 findings. Ready at 189.328 ms; the same trace verdict. | `receipts/splitboot-8x8-compH.log` |
| the 8x8 two-interface platform image (probe) | The link refuses at 59 RAMB36 against 56, as designed, because this point is ledgered by name. `ctrl_memory.py plan --ledgered-point platform-8x8-two-interfaces` accepts it at 59.0 of a ledgered 59.0 (rc 2 without the override, rc 0 with it): rom 125,760 B in 126,976, sram 114,512 B in 114,688. | `receipts/splitboot-8x8-if2-compH.log`, `receipts/plan-8x8-if2-compH.log` |
| `scripts/check_py_idiom.py` | rc 0 (the first attempt was refused only because the scratch clone's submodules were not yet registered; the receipt is the rerun) | `receipts/q-check_py_idiom.py.log` |
| docs gates for the two design pages | `docs_check.py` 0 findings; `check_doc_style.py` OK; `gen_toc.py --check` OK; `gen_toc.py --verify-anchors` 627 reproduced; `check_doc_paths.py` OK; `check_em_dash.py --base 8b1bdfaf` 0 findings over 495 added lines; `check_solution_docs.py` OK; `check_hygiene.py --check` PASS | `receipts/q-*.log` |
| `git diff --check 8b1bdfaf HEAD` | clean | this report |

The candidate's own receipts at `7a4871d5`, in the manager's candidate directory now marked superseded, were spot-checked:

- `manager-builder.json` and `full-native.json` name head `7a4871d5` and base `e282ecd2`.
- All 48 builder commands and all 5 native commands exit 0.
- `48.log` ends `ALL GATES PASS EXCEPT 1 NOT RUN`, gate 11.
- Its `FAIL` lines at 553-554 are the disabled-writer mutant's planted states ("caught in both states").

Those native suites carry over to the head composition, because the only change is to `test_builder.py`, which no native suite reads. The builder bank does not carry over: it was rerun here.

One published source-head receipt was spot-checked: `author-r4/receipts/gates/split-boot-1x1.log` hashes to `702942f9...`, its `MANIFEST.json` entry.

## 5. Findings

There is no BLOCKER, MAJOR or MINOR.

### S-1 - SUGGESTION - Tests - `sw/builder/test_builder.py:23878-23881` (gate 23o)

**Evidence.** Gate 23o compares a label only when one of the two builds produces it. When neither does, `(a is None) != (b is None)` is false, so the label passes. This is how `"nvm_split"` passes vacuously on the PR's own tree, where the gate prints "9 shape artifacts" and the builder writes 8. At the merge result all 9 exist, so nothing is wrong today.

**Impact.** If a later change renames or drops a shape artifact on both paths, the gate stays green and keeps counting it.

**Suggested outcome.** Require every label except the optional `gptp_ucode` to be present in the all-fabric build's `paths`. A dropped artifact would then be a finding, with a plant that removes one. It can only land once the PR is on `dev-soft-core`, so a follow-up Issue is fine.

**Verification.** The plant turns 23o red, and the unplanted bank stays green.

### S-2 - SUGGESTION - Docs - `docs/design/MARK_II_AREA_PLAN.md:1057-1067`, `:1081` (retains the previous round's S1, with a measurement)

**Evidence.** S9's firmware ledger is dated "linked at `5d6d2835`", so it is true as recorded. It gives the largest point as 125,048 / 113,936 B, with 2,680 B unused in the banks, and the stage as 13,264 / 3,344 B (KLJ2). In the composed tree the split stage is KLJ3, 13,594 / 3,454 B. The composed 8x8 two-interface platform image measures 125,760 / 114,512 B: still 59.0 planned, but only 1,392 B unused, and **176 B of `sram` before the next bank**, which would take it past its ledgered 59.0 (`receipts/plan-8x8-if2-compH.log`).

**Suggested outcome.** Add one line under the two tables:

> Linked with KLJ2. With the split's KLJ3 stage (#823) the largest point needs 125,760 / 114,512 B, still 59.0 planned, 176 B of `sram` below its next bank.

It could alternatively be linked again at the merge. This is optional: no statement is false.

### S-3 - SUGGESTION - Tests - `tb/verilator/ctrl_split_boot/run.py` (retains the previous round's S2)

**Evidence.** The map-stability comparison depends on the interpreter's hash seed through LiteX's ISA string. This round set `PYTHONHASHSEED=0`, which the prerequisites name, so the refusal was not seen again.

**Suggested outcome.** As published: open a new Issue, outside either side's delta.

### Carried RESIDUE (still present at this head; wording only)

- **R827-2 N2.** `sw/builder/test_builder.py:23727`'s docstring omits the bound-bitstream control. Exact fix: `"""gate 23p - the identity gate passes the two real images and a copy of the split one that binds its bitstream, and fails every planted one by its kind."""`.
- **R828-2 RES-1.** The PR body's line 99 reads "`test_builder.py` prints `ALL GATES PASS`". Exact fix: "`test_builder.py --require-rv32` prints `ALL GATES PASS EXCEPT 1 NOT RUN`, the row being gate 11's calibration report, which needs the mf48 build tree".
- **R828-2 RES-2.** The provenance claim that covers 3 of 9 reports: retained with the exact fix as published in R828-2.

## 6. Prior public findings on this PR, at this head

| Finding | Severity, lenses | State at `2155eb96` |
|---|---|---|
| R827-3 F1: gate 23o does not hold `nvm_split.json` (at `7a4871d5`) | MINOR, Tests and Docs | **Resolved.** The label is added at `:23853`. The plant is caught at the head composition and missed at `7a4871d5`. The full bank is green. `MAILBOX_SPLIT.md:1607-1610` is now true. |
| R827-3 S1: the area plan's KLJ2 ledger figures | SUGGESTION, Docs | Retained as S-2, with the composed measurement |
| R827-3 S2: the split boot's hash-seed sensitivity | SUGGESTION, Tests | Retained as S-3 |
| R827-1 F1, R828-1 F1: bound-bitstream control; manifest-ident plant | MINOR, Tests (and Conformance) | Resolved. 23p passes 1 bound-bitstream control and 13 plants at the head composition. |
| R827-1 F2, R828-1 F2: check ID `H0` reused | MINOR, Tests and Docs | Resolved (`U0`). The delta does not touch it. |
| R827-1 R1, R828-1 R1: routed-net counts | RESIDUE | Resolved |
| R827-1 S1: bus-clock path headers | SUGGESTION | Taken |
| R827-1 S2: FSM default in `KL_mbx_rx.sv` | SUGGESTION, RTL and Robustness | Retained on #495, per the ruling. The blob is unchanged. |
| R828-1 S1 / R828-2 S-C: A5 against `axil-rdata-follows-port` | SUGGESTION | Retained |
| R828-2 S-A / R827-2 N1, S-B / S-a, S-D / N4 | SUGGESTION | Retained |
| R828-2 RES-1, RES-2; R827-2 N2, N3 | RESIDUE | Retained (section 5) |

## 7. Lens results

[R828] PASS Conformance - `receipts/composition.log`; `receipts/builder-compH.log` (23n, 23o, 23p, 39); `receipts/splitboot-{1x1,8x8}-compH.log` - #870 scope at the head composition: the recipe keeps the config's shape (AC2), now including #823's `nvm_split.json`. The D2 identity, the manifest and D4's split without DDR3 are graded by 23p. #823's KLJ3 constants and `journal_klj3` reach the split SoC, and the split boots to ready on its generated flash map. S7's transmit-path statement is intact.

[R828] PASS RTL - `hdl/milan/mailbox/KL_mbx.sv` blob `4a164486`, `KL_mbx_rx.sv` blob `a7f14523`, `sw/mailbox/gen_mailbox.py` blob `db97ce8a`, identical at the head and in `d5cf412b`; the dev side changes 0 files under `hdl/`, `syn/`, `tb/verilator/mbx` or `sw/mailbox` - S9's timing cuts and mapper reach the merge unchanged. The split SoC elaborates and its native model passes at both shapes. The candidate's native bank (mbx, milan_dp) carries over, because the delta is `test_builder.py` only.

[R828] PASS Robustness - `receipts/builder-compH.log` (23o's two planted recipes and three refusals; `--ctrl-mailbox --with-dram` refused; 39's 10/10 plants), `receipts/plan-8x8-if2-compH.log`, `receipts/ctrlmem-compH.log` - the refusals of both sides compose: the split output over layout 3; the 56-RAMB36 refusal of the unledgered 8x8 two-interface image, accepted only under its ledgered name at 59.0; the mapper override's refusal on another image and on a stray tag, with 3 mutants; the stage-size rule on the 3,454 / 13,594 B stages.

[R828] PASS Tests - `sw/builder/test_builder.py:23852-23853`, `receipts/probe23o-{compH-clean,compH-plant,cand7a-plant}.log`, `receipts/builder-compH.log`, `receipts/ctrlmem-compH.log` - the delta's check can fail for the defect it names: the plant is caught at the head composition and missed at `7a4871d5`. The full `--require-rv32` bank and the memory test are green at the head composition. S-1 is optional.

[R828] PASS Docs - `docs/design/MAILBOX_SPLIT.md:1602-1648`, `:2027-2035`; `docs/design/SPLIT_CONTROL_MEMORY.md:138-180`; `docs/ENDSTATION_BUILDER.md:1073`; `receipts/q-*.log` - both pages keep each side's statements, with none lost, duplicated or contradictory. The 23o citation is true at this head. The docs gates pass at the head composition. S-2 is optional, and the RESIDUE items are carried.

## 8. Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | the 7 shared files at `d5cf412b`; the composition proof; gates 23n, 23o, 23p and 39; split boot 1x1 and 8x8 | R828-3 | `2155eb9666693c0404aadb34ac4dad10a2466e24`, composed as tree `d5cf412b54aa3e0c87781495eb5c289ac6d76649` on `dev-soft-core` `8b1bdfaf` |
| RTL | CLEAN | `KL_mbx.sv`, `KL_mbx_rx.sv`, `gen_mailbox.py` blob identity; the dev side's 0 HDL files; split SoC elaboration and native models; the candidate's native bank | R828-3 | same |
| Robustness | CLEAN | the refusal arms of 23o, 23p and 39; memory test arm 8 and its mutants; the ledgered and unledgered plans of the 8x8 two-interface image | R828-3 | same |
| Tests | CLEAN | 23o probe, clean and planted, on both trees; the full `--require-rv32` bank; `test_ctrl_memory.py`; split boot | R828-3 | same |
| Docs | CLEAN | `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md`, `ENDSTATION_BUILDER.md:1073`, `MARK_II_AREA_PLAN.md:1057-1081`; the docs gates | R828-3 | same |

## 9. Real limits

- **Which candidate was rerun.** The gates in section 4 ran on this round's own composition of the exact head onto `dev-soft-core` `8b1bdfaf`. They did not run on the manager's `7a4871d5`, which is superseded by this head, nor on a live-`dev` (`fa6c094b`) candidate. No manager source bank was run or inferred for this head.
- **Banks run here.** Only the full builder bank was rerun at the head composition. The full native, Yosys, protocol-processor and gPTP banks were not rerun. Their candidate receipts at `7a4871d5` cover a tree that differs only in `test_builder.py`.
- **Split boot.** It ran at 1x1 and 8x8 with one interface each, as its README runs it. The 8x8 two-interface point is over the 56-tile budget by design, so it was only linked and planned. It was not booted.
- **Not run.** There was no Vivado run, no route, and no hardware. Physical calibration was NOT RUN, and gate 11 was NOT RUN. A skip is not hardware proof.
- **Hosted checks.** At the time of this review the checks on `2155eb96` were queued or in progress, and none was complete. They were not used as evidence.
- **Side effects in the review clone.** Read-only fetches updated its remote-tracking refs for `dev` and `dev-soft-core`, and `git merge-tree` wrote loose objects into it. HEAD, the index, the tracked blobs and modes, and all six gitlinks were verified unchanged at the exact head (`receipts/restore-check.log`).

## 10. Pending manager duties

- Build the final current-`dev` merge candidate with head `2155eb96`, not `a69fc0f5`, and run the builder and native banks on it. `7a4871d5`'s receipts no longer describe the head.
- Own the hosted and act acceptance of the exact head's protected contexts.
- Carry the three RESIDUE items in section 5 to the residue checklist. Decide whether S-1, S-2 and S-3 become follow-up Issues.

R828-3 FINISHED

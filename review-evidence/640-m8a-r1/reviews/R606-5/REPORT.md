[R606] POSITIVE - exact head 42678ae2f77fbbef056f7fb99859e0193181e6d7

# R606-5: internal cleared-context review of PR #721 (issue #640, Mark II lane M8a-1), round 5

- Head `42678ae2f77fbbef056f7fb99859e0193181e6d7`, tree `1508b29c3603a36349665938939fa00c871cbd7e`. This is a delta review of one documentation commit on round 4's head `8ab2b539`; the source base and live dev are both `c6bd08c6`.
- Scope: the round-5 assignment (#640 comment 6118560882), answering R606-4-F1 and R607-4-F1, under ruling 6101485877 and the owner's 224 KB decision (6081706413).
- Result: no BLOCKER, MAJOR, MINOR or RESIDUE is open, and all five lenses are covered clean at this head. One new SUGGESTION is optional.
- Every command ran in the foreground with its rc recorded. Receipts are under `receipts/` and listed in `MANIFEST.sha256`.

## 1. What changed, and what it can affect

- `git diff 8ab2b539..42678ae2` touches three pages and nothing else: `SPLIT_CONTROL_MEMORY.md` (+20/-14), `MARK_II_AREA_PLAN.md` and `AREA_BUDGET.md`.
- The lane's code diff against dev is the same before and after the dev merge. The `+`/`-` line digest of `git diff ac2c5e77..ce10328c` equals that of `git diff c6bd08c6..42678ae2` for `sw` (`19c035f2…`), `syn` (`81ae83c3…`) and `scripts` (`618cda1c…`). Neither range touches `hdl` or `configs`.
- So the firmware these pages measure is dev `c6bd08c6`'s, and the memory planner and mapping recipe that measure it are unchanged since round 3.

## 2. Independent reproduction at this head

All of this ran in disposable clones under `scratch/`: the head with gitlinks `2ad2f845` (processor), `7dda9c3b` (gPTP) and `08ee86e8` (lwSRP), and `ce10328c` with `2ad2f845`, `5dce647a` and `9197193e`. Both clones stayed clean (`receipts/docs-gates/status-*.txt`).

| Step | Result | Receipt |
|---|---|---|
| Pinned RV32 SDK, installed fresh from the archive (digest `d42680e9…`) and verified | rc 0 / rc 0, GCC 14.3.0 | `receipts/sdk/` |
| Runtime: the repository recipe as written, and the same recipe through the earlier reviewer's `runtime_probe.py`, which only adds `-fno-stack-protector` (#723) | Both rc 0. The plain archives hold 4 `__stack_chk` references and the probe's hold 0. The probe was used only for linking, as the assignment allows | `receipts/runtime/` |
| R607-4 `run_fit.py`, unmodified, on both trees (CPython 3.12.3, PyYAML 6.0.3), then `compare_fit.py` | 8 of 8 links rc 0 (08:47:23 to 08:47:28). `compare_fit.py` rc 0: `PASS reproduction`. Planned at head: 35.5 / 38.0 / 48.5 / 55.0 | `receipts/run_fit/` |
| ELF identity against the author's published `fit-head/elf.sha256` and `fit-prev/elf.sha256` | **8 of 8 byte-identical**, with an independently installed SDK and runtime | `receipts/run_fit/elf.sha256` |
| R606-4 `link_points.sh` (split and flat) on both trees, then `fit_summary.py` | 24 of 24 rc 0. Largest at head: rom 111,848 in 64+32+8+4+2 KiB, sram 112,464 in 64+32+8+4+2 KiB, flat span 223,776, floor 55, headroom 5,064 B | `receipts/links/` |
| `syn/ooc/ctrl_memory_ooc.py` on the four head ELFs (pinned LiteX `a1e1c365` sources) | rc 0. `ctrl_memory_plan.json` and `ctrl_memory_ooc.tcl` are identical to the author's | `receipts/map/emit.log` |
| The Tcl in Vivado 2026.1 (`xc7a100t-fgg484-2`, `AreaOptimized_high`), alone under `$VIVADO_LOCK` from 08:48:40 to 08:50:44 | rc 0. **`ctrl_memory_ooc.tsv` is byte-identical to the author's** | `receipts/map/` |
| Bank placement from the synthesis report | At 8x8 with one interface, `rom_bank3` (1,024 words) is absent from the Block RAM table, so it is in logic. At 8x8 with two interfaces, `rom_bank4` (512 words) is in logic and `rom_bank3` (1,024 words) is in block RAM. At 1x1 every `rom` bank is in block RAM. `s8i2_rom` reports 161 Slice LUTs | `receipts/map/mapping-report-lines.txt`, `util/` |
| Symbols at both revisions | `aecp_entity_image` 7,512 / 19,520 and `nvm_stage` 3,344 / 13,264 | `receipts/fit/symbols.txt` |
| `scripts/fit_check.py`, this round's own checker: it derives every figure the three pages state from the receipts above and string-matches it against the page text | 45 of 45 checks PASS | `receipts/fit/fit_check.log` |
| `scripts/plant_check.sh`: four stale figures planted in copies of the pages (ledger total 113, LUT/FF 328/40, headroom 7,112 B, arithmetic `+53 = 124`) | All four rc 1, each failing on the check that names it | `receipts/fit/plants.txt` |
| Docs gates at the head: `docs_check`, `check_em_dash --base c6bd08c6` (0 findings over 324 added lines), `check_doc_style`, `check_doc_paths`, `gen_toc --verify-anchors` / `--check`, `check_archive`, `ci_scope --selftest`, `pp_resource_gate.py check-baseline`, `check_solution_docs` | 10 of 10 rc 0, with the hash-locked Markdown renderer | `receipts/docs-gates/` |
| `test_ctrl_memory.py`'s own arms (banks, rules, simulation, link, register) and the mutants they grade, run through `scripts/ctrl_memory_arms.py`; the SoC arm and its 6 mutants were left out (section 6) | rc 0. 103 `[ok]` checks and 38 of 38 mutants caught. The register arm passes: section 3 lists the 17 rules of `ctrl_memory.RULES` after this commit's edit to that section. The simulation covers 5 banks (64, 32, 8, 4, 2 KiB), the head's largest bank set in both regions | `receipts/ctrl-memory-arms/` |

### Figures confirmed against the pages

- **`SPLIT_CONTROL_MEMORY.md:147-150`** (all four rows, every column):
  - 35.5 / 38.0 / 48.5 / 55.0 planned;
  - 34/2, 37/1, 46/2 and 53/2 as mapped, which is 35.0 / 37.5 / 47.0 / 54.0 tiles;
  - LUT/FF 128/8, 89/7, 417/42 and 266/34;
  - floors 35 / 38 / 48 / 55.
- **`SPLIT_CONTROL_MEMORY.md:142-178`:**
  - `:153`: fill 97.2 to 99.8 percent.
  - `:156`: 2 tiles left as mapped.
  - `:157`: 4 KiB (1.0 tile) of planned headroom, and 5,064 B counting bank slack. 5,064 B is the most any growth can add. Growth of 4,096 B is always admitted, however it splits between `rom` and `sram`.
  - `:162`, `:164`: the banks Vivado puts in logic.
  - `:165-167`: 327 of 417 LUT cells, 169 of 266, 161 Slice LUTs, 36 and 97.
  - `:173`: `ce10328c` (on dev `ac2c5e77`, an ancestor that was merged) planned 35.0 / 38.0 / 48.5 / 54.5. The 34.0 / 37.5 / 47.0 / 53.0 mapped figures are the round-3 table this commit replaced, so they keep their source.
  - `:174`: `.text` grew by 1,792 B (84,444 to 86,236) and `.bss` by 264 B (103,556 to 103,820). The `rom` went from 4 banks to 5.
  - `:177`: 221,728 B is the `e8454e27` STOP figure, and it names its revision.
  - `:111`: the over-budget control linked at `c20ed894` refused rom 110,056 B (author round-1 receipt). The `ce10328c` ELFs are byte-identical to round 1's final-fit ELFs, so that revision is stated correctly.
- **Ledgers:**
  - Rows in both pages: `MARK_II_AREA_PLAN.md:811-813`, `AREA_BUDGET.md:246-248`.
  - Arithmetic and headroom in both pages: `MARK_II_AREA_PLAN.md:821-843,872-873`, `AREA_BUDGET.md:233,259-271,283,388`.
  - The firmware row is +53 RAMB36 and +2 RAMB18, which is +54 tiles.
  - `87.5 - 6.5 + 6 - 18 + 54 + 2 = 125`, 3.5 over 121.5. After the release it is 114, which leaves 7.5.
  - With every bank in block RAM it is 126 and 115, which leaves 6.5.
  - Keeping the BIOS gives 143 and 132. The partial placement gives `125 + 6 = 131`, 9.5 over.
  - The 56-tile total of 116 is unchanged.
  - The 13.5-tile reserve is untouched.
- **Limits:** every planned allocation is at most 56 RAMB36, and the largest is 55.0. Every flat span is within 224 KiB (229,376 B), and the largest is 223,776 B. There is no STOP condition.

## 3. Findings at this head

### R606-5-S1 - SUGGESTION - Tests, Docs - `sw/litex/test_ctrl_memory.py:93-94`: `LARGEST_NEED = 112_208` is the `ce10328c` figure

- **Evidence:** the comment calls 112,208 B "the largest shipped image's sram need". At this head the largest need is 112,464 B (`receipts/links/head/8x8_i2_split.plan`).
- **Impact:** none on grading.
  - The value is used to produce a bank set, and 112,208 and 112,464 both give 64+32+8+4+2 KiB.
  - That bank set is the head's largest image in both `rom` and `sram`, and the simulation arm grades exactly those five banks (`receipts/ctrl-memory-arms/arms.log:47`).
  - The test docstring's coverage claim and the `TESTING.md` paragraph remain true.
  - The round-5 assignment did not name this file. The previous round examined it and recorded that the banks still match.
- **Why not RESIDUE:** the fix edits a constant in code.
- **Optional outcome:** state the constant as a need that produces the largest image's banks, naming the revision it came from, or update it to 112,464. Either way the test's graded behaviour is unchanged.

## 4. Prior public findings on this PR, at this head

| Prior finding | Status at `42678ae2` | Evidence |
|---|---|---|
| R606-4-F1 = R607-4-F1, MINOR (Conformance, Tests, Docs): the documented fit was the `ce10328c` firmware's | **Resolved** | Section 2. The relink at the head reproduces every figure on the three pages, with ELFs byte-identical to the author's. The isolated mapping reproduces the TSV byte for byte. The earlier figures are kept only at `SPLIT_CONTROL_MEMORY.md:173` and `:177`, each with its revision named. The 45-check reconciliation and the four plants pass |
| R606-4-R1, R606-3-R1, R607-3-R1, RESIDUE (PR body: live dev tip) | **Resolved** | PR body Status, third bullet: it now carries R606-4-R1's exact sentence, and "The live `dev` tip is still `ac2c5e77`" no longer appears. The round-2 and round-3 change tables keep their figures under their own round headings, which is historical attribution, not stale present-tense text |
| R607-1-R1, RESIDUE (superseded by R606-4-F1 in round 4) | **Resolved with F1** | `SPLIT_CONTROL_MEMORY.md:156-157,171` now state 2 tiles as mapped, 1.0 tile / 4 KiB planned and 5,064 B, all matching the receipts |
| R606-4-S1, SUGGESTION (no standing gate links the real largest image) | **Retained, optional** | This round shows the drift it describes: one dev merge cost 0.5 planned RAMB36 at the largest point |
| R606-2-S1 to S4, R606-3-S-a, S-b, S-c, SUGGESTION | **Retained, optional, unchanged** | Their artifacts' line digests equal `ce10328c`'s (section 1) |
| R606-2-S5 = R607-1-S3, SUGGESTION (runtime stack protector, #723) | **Retained, separate** | Reproduced here: the plain recipe's archives hold 4 `__stack_chk` references (`receipts/runtime/stack-protector.txt`) |
| R606-1-F1..F5, R607-1-F1..F3, R607-1-S1, S2, R606-2-F1 BLOCKER, R606-2-F2 MAJOR, R606-2-F3 MINOR, R607-2-F1 MINOR, R606-1-R1 | **Resolved, preserved** | Same code digests as `ce10328c`. In this round: register arm PASS; 38 of 38 non-SoC mutants caught; `ci_scope --selftest` PASS; ledger texts recomputed (section 2) |
| R606-4 observation, outside this PR (M6/M7 "unpriced" sentences, dev's text) | **Unchanged, not a finding here** | This commit does not touch those sentences |

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Checked ruling 6101485877 items 1-2 and the round-5 items 1-5. The four points were relinked at the head and at `ce10328c` (`receipts/run_fit/`, `receipts/links/`), with ELFs byte-identical to the author's receipts. The isolated mapping was reproduced (`receipts/map/ctrl_memory_ooc.tsv`, identical). Read against them: `SPLIT_CONTROL_MEMORY.md:87,140-178`, ledgers `MARK_II_AREA_PLAN.md:805-873` and `AREA_BUDGET.md:229-290,386-390`. Limits: 55.0 ≤ 56 planned, 223,776 ≤ 229,376 B | R606-5 | `42678ae2f77fbbef056f7fb99859e0193181e6d7` |
| RTL | CLEAN | `git diff 8ab2b539..42678ae2` is three docs pages. The lane's `sw`/`syn`/`scripts` diff equals `ce10328c`'s, and there is no `hdl`/`configs` change. `CtrlMemory` was emitted for the four head images (plan and Tcl identical) and synthesised out of context; the bank-to-primitive table is in `receipts/map/mapping-report-lines.txt` (16384x31 as 15+1, the logic banks, sram banks as planned). The simulation arm drives the real `milan_soc.CtrlMemory` at the 5-bank set with an err hole to the 256 KiB window: PASS | R606-5 | `42678ae2f77fbbef056f7fb99859e0193181e6d7` |
| Robustness | CLEAN | The largest image is checked at 55.0 against the 56.0-accepted / 56.5-refused boundary (rules arm, `receipts/ctrl-memory-arms/arms.log`). The headroom statement was derived exactly: 4,096 B always admitted, 5,064 B at most. Every refusal arm for truncated, overlapping, wrong-shape and over-budget images passes, and so does the link arm with emptied or short load segments. `test_ctrl_memory.py:94` was examined (S1, optional) | R606-5 | `42678ae2f77fbbef056f7fb99859e0193181e6d7` |
| Tests | CLEAN | `sw/litex/test_ctrl_memory.py`: banks, rules, simulation, link and register arms, with 103 checks and 38 of 38 mutants. The register arm reads `SPLIT_CONTROL_MEMORY.md` section 3, which this commit edited at `:111`. `scripts/fit_check.py` passes 45 of 45 and fails on all 4 plants. 10 docs gates are rc 0. Only S1 (optional) | R606-5 | `42678ae2f77fbbef056f7fb99859e0193181e6d7` |
| Docs | CLEAN | Line by line against the receipts: `docs/design/SPLIT_CONTROL_MEMORY.md` (whole page), `docs/design/MARK_II_AREA_PLAN.md:40-44,805-873`, `docs/design/AREA_BUDGET.md:229-290,386-390`. The earlier figures keep their sources (`:173`, `:177`, `:111`). Also read: the PR body (Status, Round 5, Fit) and the merged `ARCHITECTURE_HW_SW_SPLIT.md:189-195`. Docs gates 10 of 10 rc 0 (`receipts/docs-gates/`) | R606-5 | `42678ae2f77fbbef056f7fb99859e0193181e6d7` |

## 6. Real limits

- **Out-of-context only.** The mapping and the "54 tiles" are not integrated consumption. M8a-2's integrated route, the split-image boot and the service checks are not part of M8a-1 and were not run.
- **Not run here.** The SoC-build arm of `test_ctrl_memory.py` and its 6 mutants were not run, because they elaborate the split CPU and can write a netlist into the shared LiteX install. The full LiteX aggregate, the elaboration gate, the firmware host suites, the suite sweep, Yosys and every builder or parent bank were not run either. This commit touches none of their inputs (section 1). The author's published round-5 aggregate (7 of 7, 44 of 44) is author evidence, not mine.
- **Interpreter and LiteX.** LiteX ran from the pinned source revision (`a1e1c365`, with the patch series), not from a fresh pins-only install. The emitted plan and Tcl are identical to the author's, and so is the synthesis result.
- **The runtime used the `-fno-stack-protector` probe (#723).** Its archive hashes differ from the author's because `ar` stores member times, but the linked ELFs are byte-identical.
- **The "224 KB" limit.** Ruling 6101485877 and `SPLIT_CONTROL_MEMORY.md:87` define it as 56 RAMB36 at 4,096 B, which is 229,376 B. Read decimally (224,000 B), the largest flat span (223,776 B) is still inside, but the largest split need is not: `rom` + `sram` is 224,312 B. The recorded ruling settles which reading applies, so this is not a finding.
- **Hosted checks at this head, read only.** `receipts/hosted-checks-42678ae2.tsv` was read at review time:
  - 10 completed `success`: bdd-conformance, changes, docs-check-no-git, full-ci-gate, verilator-lint, wire-accountability and Yosys shards 0-3.
  - 1 was a skipped context: the nightly physical gPTP check.
  - 10 were still in progress: docs-check, elaborate, firmware-unit, publication-census, yosys-elaboration and Verilator shards 0-4.
  - A skipped context is not an executed job.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.

## 7. Pending manager duties

- Accept the hosted and Actions-replica evidence at the exact head once the in-progress contexts finish.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, from source base `c6bd08c6`. This review claims no manager source bank.
- Carry S1 (optional) and the retained suggestions as the manager sees fit. No RESIDUE is open.

## 8. Clone state after the probes

The reviewed clone was read and never written. All builds, links and probes ran in separate clones under `scratch/`. `receipts/clone-integrity.txt` records the clone's state after the probes:
- HEAD `42678ae2`, tree `1508b29c`, and `write-tree` gives the same tree;
- `git status --porcelain` is empty;
- worktree, index and tree are identical, including blob ids and modes;
- the gitlinks are unchanged: `external` efeb541a, `gptp-processor` 7dda9c3b, `protocol-processor` 2ad2f845, `third_party/lwSRP` 08ee86e8 and `third_party/verilog-axis` 48ff7a7e.

R606-5 FINISHED

[R825] POSITIVE - exact head 55cb24911471afa2eace404888df95f9563e2724

# R825-6: internal cleared-context composition review of PR #888 (issue #791)

- Head `55cb24911471afa2eace404888df95f9563e2724`, tree `3b4b1b9fb64fb7be69a1ec16f0740149fbd383a4`. This is the sync merge of dev-soft-core `38967e26` (S9, PR #889) into #888's reviewed head `6a5acf06`. Its tree is the tree of the merge-train candidate `96034d53`.
- Scope: the COMPOSITION only. That means what S9's 33 commits after `a69fc0f5` do to #888's change, and the reverse. Code the merge does not touch keeps its prior lens verdict (R826-5 POSITIVE at `6a5acf06`; R825-1 at `03447eaa`).
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open.
  - This round records two new SUGGESTIONs and one limit.
  - It carries forward the earlier RESIDUE items (R5, R6, R7, R8) and SUGGESTIONs (S3, S4, R825-S-2) unchanged.

## 1. What the merge is

- **The merge is mechanical.** `git merge-tree --write-tree 6a5acf06 38967e26` reproduces `3b4b1b9f` exactly, with no conflict (`receipts/merge_tree_recompute.txt`).
- **On the four files both sides changed, the merge adds exactly S9's own patch.** The four files are `docs/design/SPLIT_CONTROL_MEMORY.md`, `sw/litex/ctrl_memory.py`, `sw/litex/milan_soc.py` and `sw/litex/test_ctrl_memory.py`.
  - The diff `a69fc0f5..38967e26` and the diff `6a5acf06..55cb2491` over these files hash the same: `8dfbf199...`, with index and hunk-position lines dropped.
  - So every #888 line in them is byte-preserved, and S9's lines land as S9 wrote them (`receipts/shared_file_patch_equality.txt`).
- **S9 touches none of #888's other artifacts.** The diff `a69fc0f5..38967e26` is empty for all of these:
  - `docs/testing/TESTING.md`
  - `sw/litex/ctrl_memory_decode.py`
  - `sw/litex/ctrl_memory_mutant.py`
  - `scripts/check_py_idiom.py`
  - `scripts/py_idiom.budget`
  - `tb/verilator/ctrl_region_decode/`
  - `tb/verilator/ctrl_split_boot/`
  - `tb/verilator/ctrl_service_budget/`
  - `sw/litex/patches/`
- **What S9 changes in the shared files:**
  - `ctrl_memory.stage_bytes` now reads `nvm_klj3.stage_bytes`. The stage size is 3,454 / 13,594 B, against KLJ2's 3,344 / 13,264 B.
  - The two LEDGERED overrides use 13,594 B.
  - `milan_soc` imports `nvm_klj3.split_constants` and adds the `journal_klj3` flash slot (0xE4_0000, 640 KiB).
  - In `main()` under `--ctrl-mailbox`, `milan_soc` reads the builder's `nvm_split.json` and publishes its constants.
  - The stage constants in `test_ctrl_memory.py` are updated.
  - In the doc, S9 adds a KLJ3 fit table and a KLJ2/KLJ3 stage sentence.

## 2. The four composition checks

### (1) The region decode still covers every region, with no overlap or gap, at every shape

- **S9 adds no CPU bus region.** Its full diff adds no `add_region`, `SoCRegion`, `mem_map` or `memory_regions` line.
  - `journal_klj3` is a flash offset inside the 16 MiB flash window. The generator gets that window as one aligned piece.
  - `nvm_split.json` is a builder output file, not a region.
  - The identity gate came in with `a69fc0f5`, which #888 already carried and R826-5 reviewed. S9's later identity-related addition is a csr.csv constant check (`milan_flash_journal_klj3_offset`/`_size`). That is a constant, not a region row.
- **The decode does not depend on the shape.**
  - `rom` and `sram` are `Region(..., BUDGET_BYTES)` at fixed origins (`sw/litex/ctrl_memory.py:132-133`), and S9 does not touch them.
  - A larger KLJ3 image changes only what is inside the 224 KiB, and the decode is exact over all of it.
- **Probe `scripts/probe_pieces.py`** (`receipts/probe_pieces.log`, PROBE PASS) tiles the split region list with the composed `ctrl_memory.cpu_regions`. The list is `rom`, `sram`, flash window, Milan CSR and the control mailbox window. Results:
  - Each region becomes aligned power-of-two pieces, contiguous from origin to end.
  - The piece total equals the region total, so there is no overlap or gap.
  - `journal_klj3` [0xE40000, 0xEE0000) lies inside the flash window.
- **The composed split export hands the generator the pieces.** `test_ctrl_memory.py` ran the export through `milan_soc.main()`, which now includes S9's `nvm_split.json` path, and printed `[ok] the split export hands the CPU generator rom and sram as their decode pieces, and every row it hands it is an aligned power of two (#791)`.
- **The region-decode simulation passes at this head** (`receipts/region_decode.log`, rc 0):
  - It ran on the cached pieces netlist `VexiiRiscvLitex_d43c74db…` with pinned Verilator 5.050, whose identity was checked.
  - Results: `PASS DECODE the fetch decode admits exactly the SoC regions it may fetch`, `PASS DECODE the load decode admits exactly the SoC regions it may load`, `ctrl_region_decode: PASS (0 finding(s))`.

### (2) `test_ctrl_memory.py` holds both sides' checks, passes, and is under the module limit

- **Both sides' checks are present.**
  - S9's side: the stage refusal now reads `nvm_stage is 13594 bytes; the endstation_ax7101_1x1_tdm8 shape stages 3454`, along with the planted-stage arms.
  - #888's side: the `-- CPU decode` arm (decode_pieces, cpu_regions, exact_cpu_decode and its refusals) and the export pieces check.
- **It passes.** Run with the LiteX venv at this head: `test_ctrl_memory: 0 failure(s)`, `RESULT: PASS`, rc 0, 192 `[ok]` lines and 0 failures (`receipts/test_ctrl_memory.log`).
  - The mutants section grades 59 mutants. That equals the "fifty-nine" in `docs/testing/TESTING.md:792`, which the merge does not touch.
- **Hosted CI agrees.** The exact-head hosted `elaborate` run 43149571824 shows `PASS     test_ctrl_memory` in its LiteX aggregate (`receipts/hosted_elaborate_litex_aggregate_excerpt.txt`).
- **Line count: 972 lines** (`receipts/line_counts.txt`). That is under `LONG_MODULE_LINES = 1000` (`scripts/check_py_idiom.py:148`).
  - The 1003-line composition that R826-4 found came before #888 moved mutant planting into `ctrl_memory_mutant.py` (46 lines).
  - S9 adds no lines; it changes only the two stage constants.
  - The Python idiom gate passes with `long module: 10 <= 10`. It passed locally (docs-gates-0 step 43, rc 0), in the builder bank at `96034d53` (command 11, rc 0), and in hosted docs-gates-0 step 45.
- **docs-gates-0 at `96034d53`: passes.**
  - Hosted docs run 43149571862 at `55cb2491` (tree `3b4b1b9f`, which is `96034d53`'s tree) shows `docs-gates-0 success`. All of its steps conclude `success`, with 0 non-success steps (`receipts/hosted_docs_gates_0_steps.txt`).
  - Locally I ran 33 of the job's run steps at this head (`receipts/gates_rc_summary.txt`). 31 exit 0.
  - The other two could not run here because the pinned Markdown renderer is not installed and I may not install it:
    - step 12, the em-dash gate (an environment error);
    - step 47, the per-page contents gate.
  - Both of those ran with rc 0 in the builder bank at `96034d53`:
    - `check_em_dash.py --base 38967e26`: 0 findings over 167 added lines.
    - `gen_toc.py --verify-anchors`, `--check` and `--selftest`.
  - S9's new gates `check_nvm_format_32x32.py` and `check_nvm_klj3.py` (step 30) exit 0 locally.

### (3) `SPLIT_CONTROL_MEMORY.md` states one consistent set of figures

- **The two sides' figures do not overlap.**
  - #888's figures are in section 1 ("The CPU's region decode", `:38-68`: 224 KiB, pieces of 128/64/32 KiB at origin, +0x2_0000, +0x3_0000) and in the section 7 cache note.
  - S9's figures are in section 3 (the `:119` KLJ3 rule row and the `:129-130` 13,594 B overrides), section 4 (the stage sentence) and section 5 (the KLJ3 fit table).
  - No figure from one side contradicts one from the other.
- **The stage figures agree everywhere.** The `:129-130` override rows, `ctrl_memory.LEDGERED`, `test_ctrl_memory.STAGE_*`, the `:360` reproduce command (`--stage-bytes 13594`) and the passing test's refusal text all give 3,454 / 13,594 B.
  - The KLJ2 sizes still appear in three places. Each one is labelled or scoped as KLJ2-era:
    - `:177`, the planted controls at `c20ed894`, with `:179` "That run printed KLJ2 stage sizes";
    - `:211`, which gives both formats;
    - `:311`, the target-platform measurement at `b8628704`, which S9's paragraph says was not linked again.
  - That last one is a reading point on S9's side; see S-6-2.

### (4) The candidate banks ran at `96034d53` and cover the composed files' gates

- **They ran at the right head.** Both banks record head `96034d5389fbc7d3f0dba5fc2e4cac44aa39ed70` and integrity `PASS` over tree `3b4b1b9f` (1,561 files) with the same six gitlinks as this clone (`receipts/candidate_bank_summary.txt`).
  - manager-builder: 48 of 48 commands rc 0, complete with exit 0.
  - full-native: 5 of 5 commands rc 0. These are the parallel suites, Yosys, the PP suites, gPTP and behave, complete with exit 0.
- **What the banks cover:** the idiom, docs, TOC, em-dash, NVM record-space and hygiene gates, and `test_builder.py --require-rv32`, which builds S9's `nvm_split.json`.
- **What they leave out:**
  - `test_ctrl_memory.py`;
  - S9's `check_nvm_klj3.py` and `check_nvm_format_32x32.py`;
  - the region-decode and split-boot simulations.
- **How the gap is closed at this exact head:**
  - `test_ctrl_memory.py` is covered by hosted `elaborate` and by this round's run.
  - The two NVM gates are covered by hosted docs-gates-0 step 32 and by this round's step 30.
  - The region-decode simulation is covered by this round's run.
  - See S-6-1.

## 3. Findings

### S-6-1 - SUGGESTION - Tests - `$VALIDATION_STORAGE/791-candidate-0923/manager-builder.json`, `full-native.json` - the candidate banks do not run the composed test file or S9's two NVM format gates

- **Evidence:** the 48 builder and 5 native commands do not include:
  - `sw/litex/test_ctrl_memory.py`, which is in `scripts/run_litex_sims.sh`'s inventory;
  - `scripts/check_nvm_klj3.py` and `scripts/check_nvm_format_32x32.py`, which are in docs-gates-0 "NVM record-space gate".
- **Impact:** none at this head. The hosted exact-head runs and this round's runs execute them green.
  - But the banks' "PASS 48/48, 5/5" does not by itself show that the composed files' own gates ran at the candidate.
- **Outcome:** at the merge turn's current-dev candidate, either include these three commands in the bank, or cite the exact-head hosted `elaborate` and `docs` runs for them.
- **Verification:** the candidate receipt lists them with rc 0.

### S-6-2 - SUGGESTION - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:311` - S9 side (#823/#889), not this PR

- **Evidence:** "F1's `nvm_stage` (13,264 B)" is the target platform's KLJ2-era figure at `b8628704`.
  - It is correct for that measurement. `:211` and S9's KLJ3 paragraph ("The target platform's image was not linked again") make it readable.
  - Only this line carries an unlabelled KLJ2 figure.
- **Outcome (optional, S9's lane):** write "F1's KLJ2 `nvm_stage` (13,264 B)".
- **Verification:** grep the page for `13,264`. Every hit names KLJ2.

### Comment rule on the delta

- The lines the merge adds to the four shared files contain no lane label, review round, reviewer ID or comment ID.
- The existing "lane S14" strings in `ctrl_memory.LEDGERED` sit on lines the merge does not modify; only the constant on the line before changed. #746 tracks them.
- No RESIDUE.

## 4. Prior findings at this head

I read these only after my own pass above. Every artifact they name is byte-unchanged by the merge, unless stated otherwise.

| Prior finding | At this head | Disposition |
|---|---|---|
| R825-RES-1 / R826-1 F1, MINOR Docs: the generator described as one mask compare per region | `SPLIT_CONTROL_MEMORY.md:40-42` states the `AddressMapping.terms` mechanism; the merge does not touch section 1 | Resolved (R826-2); holds |
| R825-S-1 / R826-1 F2, SUGGESTION: the guard misses re-collected or instance-kept lists | Refusals printed `[ok]` in this round's run (re-collected, kept on the instance, under another name) | Resolved (R826-2); holds |
| R826-1 F3, F4, RESIDUE (`ctrl_region_decode/README.md:7,101`) | README byte-unchanged | Resolved; holds |
| R826-2 F5, MINOR: the guard compares against the live list | The in-place shapes (`re-collected in place after naming`, `a row appended in place after naming`) are refused `[ok]` in this run | Resolved (R826-3); holds |
| R826-4 F1, MAJOR Tests: idiom gate red at 1003 lines | 972 lines; gate rc 0, `long module: 10 <= 10` | Resolved (R826-5); holds at the composition |
| R826-4 F2, MINOR Docs: TESTING.md mutant figure | "fifty-nine" = the 59 graded mutants in this run; page unchanged by the merge | Resolved (R826-5); holds |
| R826-4 S1, SUGGESTION: wrap items 8/9 | Wrapped (`test_ctrl_memory.py:61-64`) | Taken; holds |
| R5, RESIDUE Docs: "instead of building a decode other than the pieces" | `SPLIT_CONTROL_MEMORY.md:55`, `milan_soc.py:3288-3289` | Retained as RESIDUE (exact fix as published in R826-3) |
| R6, RESIDUE Tests/Docs: label "may read the whole rows after naming" | `ctrl_memory_decode.py:200` | Retained as RESIDUE (exact fix as published in R826-4) |
| R7, RESIDUE: "Twelve of them are its CPU decode arm's" | `docs/testing/TESTING.md:795` | Retained as RESIDUE (exact fix as published in R826-5) |
| R8, RESIDUE: `mutated` also rebuilds `ctrl_memory_ooc.py`'s `main` | `ctrl_memory_mutant.py:3-4`, `check_py_idiom.py:194-198` | Retained as RESIDUE (exact fix as published in R826-5) |
| S3, SUGGESTION Robustness: refuse before the generator writes the cache | `milan_soc.py` `exact_cpu_decode`, unchanged | Retained as SUGGESTION |
| S4, SUGGESTION Robustness: unreachable `else []` | `milan_soc.py:3318` | Retained as SUGGESTION |
| R825-S-2, SUGGESTION Tests: no workflow runs the region-decode simulation at a re-pin | Unchanged; `test_ctrl_memory.py` runs in hosted `elaborate` | Retained as SUGGESTION, mitigated |

## 5. Lens results

```text
[R825] PASS Conformance - issue #791 Required items against the composed head:
  - exact decode: probe_pieces PASS; test_ctrl_memory CPU-decode and export-pieces checks [ok];
  - last word and one word past in the CPU simulation: ctrl_region_decode rc 0, 0 findings;
  - all-fabric CPU: S9 adds no bus region and no CPU parameter, and exact_cpu_decode is reached only from add_ctrl_memory (milan_soc.py:3273).
  The single-mask mutant was not re-run: its artifacts are byte-unchanged by the merge.
[R825] PASS RTL - generator region rows (test log "-- SoC build" / "-- CPU decode"); cached pieces netlist VexiiRiscvLitex_d43c74db decode read at every address by ctrl_region_decode; flash slot journal_klj3 inside the one-piece flash window; ctrl_memory.py:132-133 regions unchanged by S9.
[R825] PASS Robustness - exact_cpu_decode refusals (never named; re-collected; kept on the instance; under another name; re-collected in place; row appended in place; not aligned; non-VexiiRiscv untouched), all [ok] at this head; S9's main() nvm_split.json path exercised by the split export (rc 0) and by the stage-size refusal (rc 1, named rule).
[R825] PASS Tests - sw/litex/test_ctrl_memory.py at 55cb2491: rc 0, 0 failures, 59 graded mutants, both sides' arms present; 972 lines under the 1000-line module limit; idiom gate rc 0; hosted elaborate PASS test_ctrl_memory; candidate banks 48/48 and 5/5 at 96034d53 (S-6-1: they omit this file and two NVM gates).
[R825] PASS Docs - docs/design/SPLIT_CONTROL_MEMORY.md sections 1, 3, 4, 5 and 7 cross-checked against ctrl_memory.LEDGERED, test_ctrl_memory.STAGE_* and the run's refusal text; docs gates: hosted docs-gates-0 all steps success, local 31 of 33 steps rc 0 plus the two renderer-bound steps rc 0 in the builder bank; RESIDUE R5-R8 carried.
```

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #791 Required items; composed `ctrl_memory.py`/`milan_soc.py`; `probe_pieces.log`; `region_decode.log`; `test_ctrl_memory.log` | R825-6 | 55cb24911471afa2eace404888df95f9563e2724 |
| RTL | CLEAN | Generator region rows; netlist decode via `ctrl_region_decode`; flash layout `milan_soc.py:176-188`; `ctrl_memory.py:132-133` | R825-6 | 55cb24911471afa2eace404888df95f9563e2724 |
| Robustness | CLEAN | `exact_cpu_decode` / `cpu_region_lists` refusal arms; S9's `nvm_split.json` path through the split export and the stage refusal | R825-6 | 55cb24911471afa2eace404888df95f9563e2724 |
| Tests | CLEAN (S-6-1 SUGGESTION) | `test_ctrl_memory.py` run; line count; idiom gate; hosted elaborate; candidate bank receipts | R825-6 | 55cb24911471afa2eace404888df95f9563e2724 |
| Docs | CLEAN (RESIDUE R5-R8 carried; S-6-2 on the S9 side) | `SPLIT_CONTROL_MEMORY.md`; `TESTING.md:790-799`; docs-gates-0 hosted and local; PR comments | R825-6 | 55cb24911471afa2eace404888df95f9563e2724 |

The tree `3b4b1b9f` is identical to the candidate `96034d53`'s tree, so each row also holds for that candidate's content.

## 7. Real limits

- **The split-boot simulation was not run.** `tb/verilator/ctrl_split_boot/run.py` needs CPU netlist `VexiiRiscvLitex_539e73872d28536ce763854feff20f01`, which is not in the shared generator cache. Generating it would write to a shared install.
  - A refusing `sbt` stub (`scripts/sbt_guard.sh`) stopped the generation before any write. 0 files in the cache are newer than this round's start (`receipts/split_boot_1x1.log`, rc 2).
  - So I have no execution evidence of S9's KLJ3 firmware booting under #888's decode.
  - The composition argument stands without it. The decode is exact over the whole 224 KiB regardless of what the image holds, and the composed planner accepts the KLJ3 image (`test_ctrl_memory` link and SoC arms).
- **The single-mask mutant of the region-decode simulation was not re-run.** Its artifacts are byte-unchanged by the merge.
- **Two docs-gates-0 steps (em-dash, per-page contents) could not run locally** because the pinned renderer is not installed. They are evidenced by the builder bank and hosted docs-gates-0.
- **Out of scope here:** physical calibration (NOT RUN) and hardware. Field skips are not hardware proof. No manager source bank ran at `55cb2491` itself, and none is inferred. Hosted/act acceptance is the manager's.

## 8. Pending manager duties

- At the merge turn, validate the current-dev candidate (live dev `fa6c094b`) and publish its receipts.
  - Include `test_ctrl_memory.py`, `check_nvm_klj3.py` and `check_nvm_format_32x32.py`, or cite the exact-head hosted runs for them (S-6-1).
- Carry RESIDUE R5, R6, R7 and R8 to the residue checklist. Route S-6-2 to the S9/#823 lane.
- If a split boot of the composed firmware is wanted as execution evidence, run it where generating its netlist is permitted.

## 9. Receipts

- Every receipt is listed in `MANIFEST.sha256`.
- Scripts:
  - `scripts/extract_job.py` extracts a workflow job's run steps.
  - `scripts/run_gates.sh` runs them, with one log and rc per step.
  - `scripts/probe_pieces.py` is the region-tiling probe.
  - `scripts/sbt_guard.sh` is the generator-write guard.
- Paths in the receipts are written as `<clone>`, `<packet>` and `$HOME`.
- After the probes, the clone was cleaned and verified (`receipts/restore_verify.txt`, `receipts/submodules_after_clean.txt`):
  - index tree = HEAD tree `3b4b1b9f`;
  - worktree and index match HEAD in bytes and modes;
  - all six gitlinks are as recorded;
  - every submodule worktree is clean.

R825-6 FINISHED

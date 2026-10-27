[R714] NEGATIVE - exact head a611785f2afe5bbe587f74034d869e869a1c8d37

# [R714] R714-1: external independent review of issue #665 lane S2c / PR #796

- Head: `a611785f2afe5bbe587f74034d869e869a1c8d37`, tree `690ebd66c89c11c9d8a2a13c792daa98bf3951d9` (verified in the isolated clone).
- Delta reviewed: `f58d049beb377c3f535628067022d4d5b51e8208..a611785f2afe5bbe587f74034d869e869a1c8d37`, six commits, 12 files (+682 / -44). PR #792's content below `f58d049b` is not re-reviewed.
- Scope: the S2c assignment (issue #665 comment 6421463860) and the re-base round (comment 6431653823), with S2's round-4 and round-5 rules (comments 6423962540 and 6426822636).
- Every lens was applied. Two open MINOR findings (F1 under `Tests`, F2 under `Docs`) make the verdict NEGATIVE. `Conformance`, `RTL` and `Robustness` are clean at this head.

## Verdict basis

- **The code does what the assignment asks.**
  - The split CPU (`--ctrl-mailbox` only) gets the pinned generator's own fetch L1: `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1`. That is 4 KiB, direct-mapped, 64-byte lines, one refill slot, and no LSU L1.
  - The all-fabric CPU's arguments are unchanged, and no shipped config sets `ctrl_mailbox`.
  - NFR-SCOUT-01 is not edited, and the PR states the conflict.
- **Every published figure I checked regrades from the archived per-group grades with the head's own `run.py`.** The cacheless tables are byte-identical to S2's final A1 and A8 tables.
- **Two defects stay open:**
  - **F1 (`Tests`):** `test_soc_options.py` does not pin the split CPU's 4 KiB, direct-mapped geometry. A planted 8 KiB, 2-way or 2 KiB cache passes it.
  - **F2 (`Docs`):** one README sentence misstates the measured block-RAM rate of the cache.

## Findings

### F1: MINOR, Tests: the split-cache option test accepts any cache geometry

- **Where:** `sw/builder/test_soc_options.py:228` and `:229`, with `:48`.
- **Authority:**
  - The assignment's item 1 states the parameters (4 KiB, direct-mapped). `docs/design/SPLIT_CONTROL_MEMORY.md` section 7 and the `MARK_II_AREA_PLAN.md` ledger debit exactly that cache: +1 RAMB36, +1 RAMB18, 1.5 tiles.
  - The PR says the check requires "the split CPU to add exactly the cache". The review focus asks whether the test proves that the split CPU gets only the 4 KiB, direct-mapped fetch L1.
  - AGENTS.md section 6, `Tests`: each new test can fail for the defect it claims to detect.
- **Evidence:**
  - `_split_cache` checks `split_args` only against `r"--fetch-l1 --fetch-l1-sets=\d+ --fetch-l1-ways=\d+"`.
  - `split_args` is computed inside the probe from the module under test (`mod.ctrl_cpu_args(mod.CTRL_FETCH_L1)`), so the equality at `:229` is self-referential for the geometry.
  - Planted probes (`scripts/probe_soc_geometry.sh`, receipts `receipts/probe-*.log` and `receipts/probe-soc-summary.txt`) change `CTRL_FETCH_L1 = (64, 1)` to `(128, 1)` (8 KiB), `(64, 2)` (8 KiB, 2-way) and `(32, 1)` (2 KiB). Each returns `RESULT: PASS`, rc 0, as does the unmutated control.
  - No other test pins `CTRL_FETCH_L1`. The harness's `--fetch-l1 split` follows whatever the constant holds.
- **Impact:** the shipped geometry can change silently. The 1.5-tile ledger debit, the section 7 parameter table and every "4 KiB (split)" figure would then describe a cache the split SoC no longer builds, with every gate green.
- **Required outcome:** the option test fails when the split CPU's generator options are not exactly the documented 4 KiB, direct-mapped fetch L1. For example, it could compare against `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1`, or against the documented (64, 1) restated in the test, not read back from the module under test. It should also kill a planted geometry change as a fourth control.
- **Verification:** rerun `scripts/probe_soc_geometry.sh <head tree with submodules> <out>`. `sets128`, `ways2` and `sets32` must return nonzero, and `control` must stay rc 0. `python3 sw/builder/test_soc_options.py` must still print `RESULT: PASS`.

### F2: MINOR, Docs: the README misstates the cache's block-RAM rate

- **Where:** `tb/verilator/ctrl_service_budget/README.md:751`.
- **Authority:**
  - Review focus item 4: every published figure in the README regrades from the archived logs.
  - AGENTS.md section 6, `Docs`.
- **Evidence:**
  - The line reads "in Vivado, one tile for each 2 KiB of data and half a tile of tags".
  - The archived Vivado out-of-context reports (`author-r1/a685/receipts/ooc/sweep/*/route_util.rpt`, tabulated in `receipts/ooc-tiles.txt`) give these increments over the cacheless 4.5 tiles:

    | Cache | Increment, tiles | Data | Tags |
    |---|---:|---:|---:|
    | 2 KiB | +1 | 0.5 | 0.5 |
    | 4 KiB | +1.5 | 1 | 0.5 |
    | 8 KiB | +2.5 | 2 | 0.5 |
    | 16 KiB | +4.5 | 4 | 0.5 |
    | 32 KiB | +8.5 | 8 | 0.5 |

  - The same rows appear in the README's own table at lines 739-746.
  - So the data side costs one tile per 4 KiB, not per 2 KiB. A reader applying the sentence would price the split's cache at 2.5 tiles instead of the measured 1.5.
- **Impact:** a published derived cost figure contradicts the measured table beside it and the ledger debit. This is a figure, not only wording.
- **Required outcome:** the sentence states the measured rate: one tile for each 4 KiB of data, half a tile of tags, and half a tile more per extra way.
- **Verification:** every row of the README's Vivado table satisfies the stated rate: 4.5 + 0.5 + size/4 KiB, plus 0.5 per extra way.

### RES1: RESIDUE (owner comment rule of 2026-10-15), new lane names in source comments

- **Where:** `tb/verilator/ctrl_service_budget/build.py:149` ("(#665, D3 and lane S14)") and `:151` ("F1's flash driver").
- **Evidence:** both lines are added in this delta (`receipts/comment-rule-scan.txt`). `S14` and `F1` are lane names.
- **Exact fix:**
  - `:149`: "(#665, D3 and lane S14)" becomes "(#665, decision D3)".
  - `:151`: "F1's flash driver" becomes "the saved-state flash driver (`nvm_flash_litespi.c`)".
- **Not counted:** the check and mutant names that carry "F1's" (`selftest.py:759`, `selftest_mutants.py:441` and the README mutant table) are strings, not comments, so they are not counted here.

### RES2: RESIDUE, the XIP conclusion is worded as if no path met T_svc from flash

- **Where:**
  - The PR body, Hybrid XIP: "No path inside T_svc holds from flash, so D3's rule stands."
  - `tb/verilator/ctrl_service_budget/README.md:728`: "So no path inside T_svc can execute from the flash ... as D3 rules."
- **Evidence:** read literally, the sentence contradicts the figures printed beside it.
  - Behind 32 KiB with the code in flash, 62 of 81 paths (1x1) and 79 of 129 (8x8) still fit T_svc.
  - Behind 4 KiB, 7 of 78 and 14 of 125 fit.
  - The measured conclusion that is supported: moving all code to flash makes more paths miss (19 against 13 at 1x1; 50 against 34 at 8x8), and the released windows' longest pass becomes 2.2 to 2.7 times as long. So the T_svc service paths stay in block RAM, as D3 rules.
  - No figure, grade or verdict changes.
- **Exact fix:**
  - PR body: "With every function but the reset entry and the flash driver in flash, more paths miss T_svc (19 of 81 and 50 of 129 behind 32 KiB, against 13 and 34 with the code in block RAM), so the T_svc service paths stay in block RAM, as D3 rules."
  - README `:728`: "So the T_svc service paths stay in block RAM behind the split's cache, or behind one eight times its size, as D3 rules."

### S1: SUGGESTION, Tests: the refill-wait accounting in `sim_main.cpp` has no self-test

- **Where:** `tb/verilator/ctrl_service_budget/sim_main.cpp:265-288`.
- **Gap:** the five new checks test `fetch_bus`'s return value, `built_as`/`selected` and `xip_script`. No self-test exercises how the native model closes a refill's wait at its last beat, or at its error.
- **Mitigation:** the archived real runs corroborate the logic.
  - Every cached arm's `fetch_rom` minimum and maximum wait is 42 to 45 CPU cycles a refill, where a first-beat close would give about 9.
  - The netlist's `FetchL1Plugin_logic_bus_rsp_ready = 1'b1` means every `rsp_valid` is a beat.
- **Optional:** a fixture-level check of the per-region fetch wait.

### S2: SUGGESTION, Tests: `xip_offset()` is not covered

- **Gap:** the XIP check passes a literal origin (`0x20410000`), so a mutant of `build.xip_offset()` (`build.py:160`) survives. One example is placing the code at the AEM slot's offset instead of the first erase block after it.
- **Impact:** low. The arm is labelled, and its flash image is erased bytes before the code.

## Requested checks (review focus)

### 1. The all-fabric CPU keeps exactly its arguments, and its export is byte-identical for every shipped config

Holds. Evidence:

- `milan_soc.py:2900-2903` adds the cache only under `ctrl_mailbox`. No shipped config, builder script or workflow sets `ctrl_mailbox` (repository grep).
- `test_soc_options.py` at the head asserts `vexii_args == "--xlen=32"` for the all-fabric probe and kills "the all-fabric CPU with the cache" (`receipts/soc-options-head.log`, rc 0).
- The export digests are the author's receipt (`author-r1/a685/receipts/export/export-digests.txt`). Five shipped configs have the same normalised digest at base `e76a755a` and at the pre-rebase head. It still applies at this head:
  - `git diff e76a755a f58d049b -- sw/ configs/ hdl/` is empty;
  - the range-diff (`author/receipts/rebase/range_diff.txt`) shows the lane's `sw/` commit unchanged, and commit 1 differs only in `selftest.py`.

### 2. The split CPU gets only the fetch L1, and `test_soc_options.py` proves it

- The code holds: `ctrl_cpu_args` builds exactly `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1`, with no `--lsu-l1`.
- The test proves "only a fetch L1, no LSU L1, split only". It does not prove "4 KiB, direct-mapped": see F1.

### 3. Harness options, refill observers, reuse identity, self-test checks and mutants

The behaviour holds, and each new mutant is caught by the check it names. Evidence:

- `run.py --self-test` at the head gives 92 checks and 67 of 67 mutants caught, `self-test: 0 failures`, rc 0 (`receipts/selftest-head.log`).
- The observers are correct for this netlist: one refill slot, a line-aligned address `{...[31:6],6'h0}`, and response ready held at `1'b1` (netlist sha256 matches `author-r1/a685/receipts/netlists/netlists-sha256.txt`).
- Reuse refuses another fetch L1 or arm. It refuses a `64x1` build under `--fetch-l1 split` (a conservative string identity), and it treats an S2 build that records no fetch L1 as cacheless (`receipts/robustness-probe.txt`).
- The geometry parser refuses `0x1`, `64x0`, `48x1`, `064x1`, padded and other malformed values.
- The native-model accounting has no self-test: see S1.

### 4. Every published figure regrades from the archived logs under S2's final rules

Every figure I checked regrades, except F2's prose rate (and RES2's wording). Method and coverage:

- `scripts/regrade_tables.py` rebuilds every one of the 23 arms' `table.md` with the head's `run.table` and `run.composed_maximum` from the archived per-group grades. All 23 are byte-identical to the author's head regrade (`receipts/regrade-summary.txt`). The archived per-group JSON equals the author's head-regrade digests, 302 of 302 (`receipts/group-json-vs-head-regrade.txt`).
- The sweep table, and the composed maximum over every backlog window labelled a lower bound, check out:

  | Arm | Composed maximum, ms | Released windows only, ms |
  |---|---:|---:|
  | 1x1, cacheless | at least 31.32 | 14.81 |
  | 1x1, 4 KiB | at least 19.32 | 8.60 |
  | 8x8, cacheless | at least 44.19 | 27.84 |
  | 8x8, 4 KiB | at least 29.12 | 14.03 |

- Arm B's partial figure is 8.61 and 14.07 ms, labelled "3 of 4 backlog windows, a partial figure (backlog-adp-refill not run)".
- These also reproduce:
  - the per-window table (`receipts/figures-windows.txt`);
  - the path counts of every arm;
  - the backlog rows;
  - the 47 rows of the two "paths that still miss" tables, with the listed set equal to the regrade's missing set (`receipts/miss-tables-check.txt`);
  - the CPI and fetch table and the XIP CPI and refill means (`receipts/cpi-table.txt`);
  - the fan-out ranges, whole over both arms and every interface (`receipts/fanout-ranges.txt`): 7,054 to 15,334 per recipient (arm A 7,144 to 13,114), 4.42 to 8.70 and 8.25 to 18.19 ms, and 5 of 13 and 10 of 22 misses, none over the ceiling;
  - the consumer shares: memset/memcpy 65 / 43 %, AECP/ACMP/`mrp_mad` 18 / 39 %, mailbox driver 7 / 6 %;
  - the planned block RAM (35.5 to 15 tiles, 56 to 35 tiles);
  - the Vivado out-of-context and Yosys tables (`receipts/ooc-tiles.txt` and `author-r1/a685/receipts/yosys/*.json`);
  - the ledger arithmetic: 114 + 1.5 = 115.5, 115 + 1.5 = 116.5, 121.5 - 115.5 = 6.0 and 121.5 - 116.5 = 5.0, and 116 + 1.5 = 117.5, which is 4.0 below.
- The PR body's expected run lines and composed line match the regrade.

### 5. The cacheless arms reproduce S2's final tables byte for byte

Holds.

- `P1-none` and `P8-none`, rebuilt independently, equal S2's final `author-r5/receipts/head-regrade/A1/table.md` (sha256 `a835c98b...`) and `A8/table.md` (`599f1961...`). These come from the `665s2-review-evidence` branch at `1fd9dc27`.
- S2's final B1 and B8 counts (18 of 44 / 41 of 68 and 36 of 68 / 60 of 92) match the README's baseline column.

### 6. The hybrid-XIP arm and the rule that the flash driver stays in block RAM

The claims hold (the wording issue is RES2). Evidence:

- The link script keeps `.text.start` and `*-nvm_flash_litespi.o(.text .text.*)` in `rom`.
- Inside a chip-select window the driver (`nvm_flash_litespi.c:120-166`) uses only inline CSR accessors and power-of-two arithmetic, so no call leaves block RAM while the device is selected.
- All four XIP arms record 0 traps and 0 bus errors.
- The 4 KiB XIP arms' 3 and 4 refusals are "no end" bounded-wait expiries.
- The all-flash first run's trap is archived (`allflash-xip/acmp-notk-trap-excerpt.txt`: `TRAP ... 0 2 2041effc`, cause 2).
- The block RAM freed (20.5 and 21 tiles) matches `ctrl_plan`.

### 7. NFR-SCOUT-01's "cacheless" text is not edited, and the PR states the conflict

Holds.

- The delta touches neither `docs/reference/FR_NFR.md` nor `docs/ARCHITECTURE_HW_SW_SPLIT.md`.
- The PR body's Known limitations, and `SPLIT_CONTROL_MEMORY.md:243-245`, state the conflict as open for the owner.
- The other "cacheless" statements in `docs/` describe the shipping all-fabric profile, which stays cacheless.

## Lens results (clean lenses, with artifacts)

- [R714] PASS Conformance — `sw/litex/milan_soc.py:2815-2833,2900-2903`; `docs/design/SPLIT_CONTROL_MEMORY.md` section 7; PR #796 body; `receipts/regrade-summary.txt`; `receipts/regrade/` — checked against assignment items 1-5, the re-base round's items, and the STOP conditions:
  - the generator patches and pin are unchanged;
  - the all-fabric path is unchanged;
  - the route at 20 / 10 ns has positive slack (`ooc/product/*/timing.rpt`);
  - the firmware and mailbox contract are untouched;
  - "Relates to #665" is stated.
- [R714] PASS RTL — `milan_soc.py:2900-2909` (argument plumbing); pinned netlists `VexiiRiscvLitex_2c4bb987….v` and `…77fd592c….v` (`FetchL1Plugin` refill slot, line address, `rsp_ready = 1'b1`, PMA decode); `sw/litex/patches/0005` (coherency only with an LSU L1); `observe.vlt`; `sim_main.cpp:262-288`; `author-r1/a685/receipts/pma/*.txt` — checked:
  - the generator options against patch 0005's non-coherent fabric;
  - that the fetch L1's region decode equals the cacheless one in the cover, as-built and product split netlists;
  - the observers against the bus protocol;
  - the routed WNS and WHS of the product split CPU.
- [R714] PASS Robustness — `split_soc.py:257-271`, `run.py:285-293` and `build.py:149-211`, `335-353`, probed in `receipts/robustness-probe.txt` — checked:
  - malformed and zero-size geometries are refused;
  - mismatched reuse is refused, and old builds read as cacheless;
  - a netlist without a line-aligned refill address is refused;
  - a link script without its anchor is refused;
  - a refill error closes its wait;
  - the XIP flash code region lies past the AEM slot and far from the journal at `0xEE0000`;
  - the XIP arms record 0 traps and 0 bus errors, and their refusals are bounded-wait expiries.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment and re-base comments; `milan_soc.py`; section 7; `MARK_II_AREA_PLAN.md`; PR body; the 23-arm regrade; S2 final A1/A8/B1/B8 | R714-1 | `a611785f2afe5bbe587f74034d869e869a1c8d37` |
| RTL | CLEAN | `milan_soc.py` CPU arguments; pinned cached and cacheless netlists; patch 0005; PMA decode receipts; `observe.vlt`; `sim_main.cpp`; Vivado out-of-context timing | R714-1 | `a611785f2afe5bbe587f74034d869e869a1c8d37` |
| Robustness | CLEAN | `split_soc.fetch_l1_geometry`; `run.built_as`/`selected`; `build.fetch_bus`/`xip_script`/`xip_offset`; refill error path; XIP traps and refusals; `receipts/robustness-probe.txt` | R714-1 | `a611785f2afe5bbe587f74034d869e869a1c8d37` |
| Tests | UNCLEAN (F1 open) | `test_soc_options.py` and geometry probes; `selftest.py`/`selftest_mutants.py` (92 checks, 67 of 67 caught); `sim_main.cpp` coverage (S1) | R714-1 | `a611785f2afe5bbe587f74034d869e869a1c8d37` |
| Docs | UNCLEAN (F2 open) | harness README cache section; `SPLIT_CONTROL_MEMORY.md` section 7; `MARK_II_AREA_PLAN.md` ledger; PR body; docs gates at the head | R714-1 | `a611785f2afe5bbe587f74034d869e869a1c8d37` |

RESIDUE items RES1 and RES2 leave no lens unclean. They go to the manager's residue checklist.

## Gates run by this reviewer at the head (foreground, tree clean after each)

- `run.py --self-test`: rc 0, 92 PASS, 67 of 67 mutants caught.
- `sw/builder/test_soc_options.py` (product LiteX environment, read only): rc 0, `RESULT: PASS`.
- `scripts/check_baremetal_only.py --check`: rc 0, `baremetal-only: OK`.
- These rc 0:
  - `scripts/docs_check.py`;
  - `scripts/check_doc_paths.py`;
  - `scripts/check_py_idiom.py`;
  - `scripts/check_hygiene.py --check`;
  - `docs/DOC_MAP.gen.py --check`;
  - `git diff --check f58d049b HEAD`.
- `scripts/check_em_dash.py --base e76a755a` and `scripts/gen_toc.py --check` returned rc 2 under the system interpreter, which lacks the pinned renderer. Both ran rc 0 under the existing pinned Markdown environment: 0 findings over 974 added lines, and the TOC gate OK. All logs are in `receipts/gates/`.
- Not run here: `cd tests && behave` and `test_builder.py --require-rv32`. The delta touches no feature file or step, and these are the author's receipts.

## Prior public review findings on PR #796

Read after this verdict and ledger were written (`receipts/pr796-comment-index.tsv`):

- PR #796 carries no prior review finding. Its only comments are the manager's two review-start notices (R713-1 and R714-1). There are no PR reviews and no inline review comments.
- The pre-rebase head `2a7b0df5` was never published for review.
- So there is nothing to resolve or retain. This round's findings are the first on this PR.

## Real limits

- **No harness simulation, CPU generation, Vivado or Yosys ran in this review.**
  - Figures are regraded from the archived per-group grades with the head's aggregation. The grades come from the archived logs.
  - I did not re-grade raw logs to per-group JSON: rebuilding the scenario groups needs each build's generated entity headers, which are not archived.
  - The per-group grades' byte identity rests on the author's head regrade digests (302 of 302 equal). It is corroborated independently by `P1-none`/`P8-none` from this lane's own runs equalling S2's separately run A1/A8 tables.
- **The all-fabric export digest is the author's receipt at the pre-rebase head.** It carries to this head by the empty `sw/`, `configs/` and `hdl/` diff and the range-diff.
- **Hosted contexts at the exact head did not complete green.** The record holds 30 cancelled runs, 11 failures and 23 successes (`receipts/hosted-check-runs.tsv`). The inspected failures (`docs-check`, `elaborate`, `Union maap`) fail at the gate-union step ("Require every gate exactly once") after cancelled shards; they are not executed gate failures. The manager owns hosted and act acceptance.
- **No manager source bank ran at this head, and none is claimed or inferred.**
- **No physical calibration, bench or hardware evidence is claimed by the PR or by this review.** Field skips are not hardware proof.

## Pending manager duties

- Carry RES1 and RES2 to the residue checklist.
- Route F1 and F2 to the executor and re-review at the corrected head.
- Validate the current-dev merge candidate (source base `f58d049b`, live dev `76de691e`) with the builder and native banks at the merge turn, after PR #792 lands. Settle hosted acceptance at the final head.
- NFR-SCOUT-01's amendment stays the owner's.

R714-1 FINISHED

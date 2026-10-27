[R713] NEGATIVE - exact head a611785f2afe5bbe587f74034d869e869a1c8d37

# R713-1: internal cleared-context review of PR #796 (issue #665, lane S2c)

- **Head:** `a611785f2afe5bbe587f74034d869e869a1c8d37`, tree `690ebd66c89c11c9d8a2a13c792daa98bf3951d9`.
- **Delta reviewed:** `f58d049beb377c3f535628067022d4d5b51e8208..a611785f`, six commits, 12 files. PR #792 (S2, base of the stack) is not re-reviewed.
- **Lenses applied:** Conformance, RTL, Robustness, Tests, Docs. Each one is covered below with the artifacts examined.
- **Verdict:** NEGATIVE. Four MINOR findings are open: one under Conformance and Docs, one under Docs, one under Docs and Tests, and one under Tests. None of them is a defect in the cache, the product change or the measured cycle counts. The independent reruns reproduce the archived results exactly. All four findings are about labels, a derived rate, reproduction text, or what a check actually proves.
- **Prior public review findings on PR #796:** none. The PR carries only the two review-start comments, so there is nothing to resolve or retain.

## What the task is, reconstructed from public state

- **Assignment** (issuecomment-6421463860, owner decision 2026-10-26):
  - Give the split SoC's VexiiRiscv an L1 instruction cache through the pinned generator's own options, and state its parameters.
  - Keep the all-fabric CPU byte-identical.
  - Measure on S2's harness at both points against S2's cacheless tables, and sweep at least two sizes.
  - Price the cache's block RAM, LUT and FF with Yosys and out of context, against the 56-tile allocation and the area plan.
  - Measure a hybrid-XIP arm, and state the remaining T_svc gap.
  - Leave firmware behaviour, firmware tests and the mailbox contract unchanged.
  - STOP on a generator version change, an all-fabric change or a shipping-clock timing change.
- **Owner clarification** (issuecomment-6410301079): the all-fabric placement stays a supported build, and every split-lane PR keeps the all-fabric export byte-identical for every shipped config.
- **Re-base round** (issuecomment-6431653823):
  - Re-base onto S2's final `f58d049b`.
  - Resolve toward S2's round-4 and round-5 rules: the composed maximum over every backlog window, the partial and lower-bound labels, and the fan-out ranges.
  - Rerun the self-test and its mutants.
  - Regrade every arm, with the cacheless tables byte-identical to S2's final ones.
  - Run the bare-metal scope gate, the docs gates and behave.
  - The PR says "Relates to #665" and states the NFR-SCOUT-01 conflict as open.
- **Requirements read:**
  - `docs/reference/FR_NFR.md` NFR-SCOUT-01 ("one cacheless RV32I control hart") and 3.4.1 (T_svc = 10 ms);
  - `docs/ARCHITECTURE_HW_SW_SPLIT.md:62`;
  - `docs/design/SPLIT_CONTROL_MEMORY.md`;
  - `docs/design/MARK_II_AREA_PLAN.md`;
  - decisions D3 and D4 (issuecomment-6409738976).

## Findings

### R713-1-F1 MINOR - Conformance, Docs - `tb/verilator/ctrl_service_budget/README.md:658, :663, :664, :690, :700, :701` - unbounded rows shown as measured ceiling misses, without S2's lower-bound labels

- **Requirement/evidence.**
  - The S2 rules on the same page say a record never released "carries the time it had waited by the run's end, a lower bound, and fits neither T_svc nor its ceiling" (`README.md:167`), and that its cell "gives the time it had waited, at least" (`:186`).
  - `run.verdict_word` renders such a row as `STARVED: never released` or `NEVER ANSWERED`.
  - The re-base round requires S2's "partial and lower-bound labels".
  - The archived head-regrade tables give these rows as follows:

    | Row | 1x1 | 8x8 |
    |---|---|---|
    | ACMP command behind the owed input | `at least 363.984 NEVER ANSWERED` (none), `at least 363.686` (4 KiB) | `at least 860.001` (none), `at least 369.841` (4 KiB) |
    | SRP record, first / last | `at least 628.320 / 628.299 STARVED: never released` (none), `at least 574.319 / 574.299` (4 KiB) | `at least 658.793 / 658.773` (none), `at least 591.988 / 591.968` (4 KiB) |

  - The two "Paths that still miss T_svc" tables print all twelve of those cells as `NNN.NN **over ceiling**` with no "at least". The CPU-cycles column (for example `28,715,962`) carries the same unlabelled bound. Receipt: `receipts/unbounded_rows.txt`.
- **Impact.**
  - Lower bounds of waits that never ended read as measured service times with a measured ceiling verdict.
  - The none-to-4 KiB comparison then reads as a measured improvement, for example 628.32 to 574.32 ms for SRP. In fact both are bounds on records the firmware never released.
- **Required change.** Each of the six rows carries "at least X, never answered" or "at least X, never released" in both ms columns, with its cycles cell marked the same way, as the archived `table.md` and S2's own tables (`README.md:381`, `:406-407`) do.
- **Verification.** Each cell is compared with the verdict in the archived head regrade for P1-none, P1-64x1, P8-none and P8-64x1.

### R713-1-F2 MINOR - Docs - `tb/verilator/ctrl_service_budget/README.md:751` - the cache's block-RAM rate is stated at twice the measured cost

- **Requirement/evidence.**
  - The README says the cache costs "in Vivado, one tile for each 2 KiB of data and half a tile of tags".
  - Its own table (`:739-746`) and the archived `synth_util.rpt`/`route_util.rpt` (parsed by this review) show, over the cacheless 4.5 tiles:
    - 2 KiB +1 tile;
    - 4 KiB +1.5;
    - 8 KiB +2.5;
    - 16 KiB +4.5;
    - 32 KiB +8.5.
  - That is one tile per 4 KiB of data plus half a tile of tags (a RAMB36 holds 4 KiB). A two-way size adds a second half-tile of tags.
- **Impact.** The stated rate doubles the planning cost of any later size. A 16 KiB cache would be planned at 8.5 tiles instead of the measured 4.5, against a ledger that has 4.0 to 6.0 tiles of headroom.
- **Required change.** The sentence states the measured rate: one tile per 4 KiB of data and half a tile of tags per way.
- **Verification.** The rate is recomputed against the README table rows and the out-of-context reports.

### R713-1-F3 MINOR - Docs, Tests - `tb/verilator/ctrl_service_budget/README.md:891, :896-911` (and `:36-39` with `:180`) - S2's control and fixture commands no longer reproduce the figures printed beside them

- **Requirement/evidence.**
  - This PR makes `run.py`'s default the split cache (`run.py:186`, `--fetch-l1` default `split`).
  - S2's control commands at `:896-902` carry no `--fetch-l1 none`, but the text after them still states S2's cacheless figures:
    - "it measures 24.614 ms" and "the ordinary image ... 0.294 ms" (`:906-907`);
    - "24.903 ms against 0.582 ms" (`:909`).
  - This review ran the documented `--mutation slow-adp-rx` command at the head: it measured **16.556 ms**, rc 0 (`receipts/rerun-C1-slow.log`). That is the cached figure `:780` gives, not the one printed at `:906`.
  - `:891` regenerates the self-test fixture "from a fresh 1x1 run of the `fixture` group", which is now the cached CPU, while `fixture.log` and `oracle.json` were recorded on the cacheless core.
  - The Results reproduction block (`:36-39`) also builds the cached CPU. `:180` says those results need `--fetch-l1 none`, but the commands do not show it.
- **Impact.**
  - A reader who runs a documented control command gets a figure that disagrees with the page.
  - A fixture regenerated as documented would come from a different CPU than the oracle it is checked against.
- **Required change.** Every S2 reproduction command on the page (controls, fixture regeneration, and the block that reproduces Results) either selects `--fetch-l1 none` or states the figure for the head's default, so that each command agrees with the figure printed beside it.
- **Verification.** Rerun a documented control command and compare its figure with the page.

### R713-1-F4 MINOR - Tests - `tb/verilator/ctrl_service_budget/selftest.py:752-756`, `run.py:317-318`, `build.py:519` - the reuse check never exercises the refusal it is named for

- **Requirement/evidence.**
  - AGENTS.md section 6, Tests lens: "Each new test can fail for the defect it claims to detect".
  - The new check is named "a reused build of another fetch L1 or arm is refused" (README `:810`, PR body "A reused build must be the selected cache and arm"). It compares only `run.built_as()` with `run.selected()`.
  - Reviewer mutants on a disposable copy of the head (`receipts/harness_probes.txt`), each with the full self-test still rc 0 (92 checks, 67 of 67 mutants caught):
    - replacing `run.py:317`'s condition with `False`, which removes the refusal entirely, survives;
    - recording `spec['xip'] = False` at `build.py:519`, which makes a reused XIP build attest as a block-RAM build, survives.
- **Impact.** The reuse guard can be removed, or the arm recorded wrongly, with the self-test green. A regrade or reuse could then silently grade one cache or arm under another's label.
- **Required change.** A check drives the refusal path itself, for example `main()` or a factored refusal helper, run on a temporary `build.json` that records another fetch L1 or arm, and asserts the refusal. It also checks what `build()` records for `fetch_l1` and `xip`. Each part has a mutant.
- **Verification.** Both reviewer mutants above are killed, and the rest of the self-test stays green.

### RESIDUE (wording only; the exact fix is given; does not affect the verdict or any lens)

- **R713-1-RS1 - comment rule (owner 2026-10-15)** - `tb/verilator/ctrl_service_budget/build.py:149` "(#665, D3 and lane S14)" and `:151` "F1's flash driver" name lanes in new source comments.
  - Fix `:149`: `#: The labelled hybrid-XIP arm (#665, the hybrid-XIP decision): the anchor in plat/ctrl_split.ld that`.
  - Fix `:151`: `... rom keeps the reset entry, the saved-state flash driver (nvm_flash_litespi.c),`.
  - The check and mutant names at `selftest.py:761` and `selftest_mutants.py:441` carry the same "F1's" in strings; renaming them to "the flash driver" is optional.
- **R713-1-RS2** - `docs/design/MARK_II_AREA_PLAN.md:897-898` now follow four totals (the new `:896` adds two), so "Both" and "Neither number" no longer agree with them.
  - Fix: `All four leave the separate 13.5-tile reserve untouched.` and `None of these numbers proves integrated fit; M8a-2's route does.`
- **R713-1-RS3** - PR body, Status: "It roughly halves the split firmware's service times". The measured cuts are 34 to 39 % on the composed maxima and 42 to 50 % on the released windows.
  - Fix: `It cuts the split firmware's longest passes by a third to a half, but it does not close T_svc = 10 ms at either point.`
- **R713-1-RS4** - `README.md:723` "A 32 KiB cache, 13 tiles out of context" and `:727` "(13 tiles of cache against 6, ...)", and the PR body's "Behind 32 KiB (13 tiles)". The 13 and 6 are the whole CPU's tiles; the cache's own share is 8.5 and 1.5.
  - Fix `:723`: `A 32 KiB cache, on a CPU of 13 tiles out of context, ...`.
  - Fix `:727`: `(a CPU of 13 tiles against 6, and 20.5 or 21 tiles of rom)`.
  - Fix the PR body: `Behind 32 KiB (a CPU of 13 tiles), ...`.

### SUGGESTION (optional)

- **R713-1-S1 - Tests** - `sw/builder/test_soc_options.py:228` accepts any sets and ways.
  - `CTRL_FETCH_L1 = (64, 2)` and `(256, 1)` both pass the test (`receipts/soc_options_probe.log`).
  - The test does prove the split-only, fetch-L1-only, no-LSU-L1 shape: three controls are killed, and a planted prefetch option is killed by this review's probe.
  - It does not pin the documented 4 KiB direct-mapped geometry that `SPLIT_CONTROL_MEMORY.md` section 7 and the +1.5-tile ledger debit rest on. Asserting the literal options would pin it.
- **R713-1-S2 - Robustness** - `run.py:290-293` compares the label `split`, not the geometry it resolved to.
  - `build.json` already records `fetch_l1_geometry`.
  - A `split` build made before a change to `CTRL_FETCH_L1` would still attest on reuse, because the recorded netlist is unchanged.
  - Comparing `fetch_l1_geometry(args.fetch_l1)` with the recorded geometry closes that.
- **R713-1-S3 - Robustness** - `--xip --fetch-l1 none` is accepted, although the arm is defined as "behind the instruction cache" (`run.py:189-191`, `README.md:73`). Refuse that combination, or label it.
- **R713-1-S4 - Tests** - `sim_main.cpp` times a refill to its last beat, and nothing gates that.
  - A first-beat mutant survives (`receipts/harness_probes.txt`).
  - The archived 42-cycle mean refill (against 9.1 cacheless) shows the semantics hold today.
  - A synthetic refill trace in the self-test would gate it.

## Lens results with evidence

- **Conformance - UNCLEAN (F1).** Checked, at the head:
  - Acceptance items 1 to 5 of issuecomment-6421463860:
    - the generator's own options (`sw/litex/milan_soc.py:2815-2833`, `:2900-2903`);
    - the parameters stated (`SPLIT_CONTROL_MEMORY.md` section 7);
    - a five-size sweep plus a two-way size at both points;
    - Yosys and out-of-context pricing;
    - the XIP arm;
    - the gap stated;
    - no change under `sw/firmware/` or `sw/mailbox/` (`git diff --stat f58d049b..HEAD`).
  - None of the STOP conditions holds:
    - the generator is pinned at `235753e2`;
    - all-fabric behaviour is unchanged by construction: the only product change sits under `if ctrl_mailbox:`, and no shipped config sets it;
    - the out-of-context route closes at 20 / 10 ns.
  - #791's decode is unchanged. `receipts/fetch_decode.txt` shows the fetch fault and io expressions identical in all three netlist pairs (as-built, cover, product split), and the cached as-built control reproduces the same trap.
  - NFR-SCOUT-01's text is not edited (`docs/reference/` is not in the diff). The conflict is stated in the PR body and in `SPLIT_CONTROL_MEMORY.md:243-245`.
  - The re-base round: the self-test passes with 92 checks and 67 of 67 mutants caught (`receipts/selftest-head.log`). Every arm regrades at the head (see Tests). The cacheless tables are byte-identical (see Tests). The labels are S2's, except the six rows in F1.
- **RTL - CLEAN.**
  - `[R713] PASS RTL - sw/litex/milan_soc.py:2815-2833,2900-2903; the pinned generator's Param.scala:144-150,835 and the patched Soc.scala; netlist VexiiRiscvLitex_2c4bb987d123aab6d38527891a2d9fd1.v:11440,13936; receipts/fetch_decode.txt; the archived out-of-context timing.rpt - the following were checked:`
    - the split CPU only gains FetchL1Plugin: 64 sets, 1 way, 64-byte line, one refill slot, no prefetch;
    - there is no LSU L1. The patched `Soc.scala` sets `lsuL1Coherency = lsuL1Enable && (cpuCount > 1 || withDma)` and builds the unified fabric when `!lsuL1Enable`, so patch 0005's non-coherent fabric stays;
    - the refill bus is 32-bit with one slot and no id, which matches `build.fetch_bus`'s 16 beats and id-0 accessors;
    - the fetch region check is the cacheless expression with io constant false, so every executable region is cacheable;
    - there is no new clock crossing: the cache sits inside the CPU domain, behind the existing `--with-cpu-clk` CDC;
    - out of context, the product split CPU closes at WNS +0.607 / WHS +0.003 ns.
  - The sizes and figures in the design doc and the README match the Vivado and Yosys reports for all eleven netlists.
- **Robustness - CLEAN** (suggestions S2 and S3 only).
  - `[R713] PASS Robustness - split_soc.py:257-271, build.py:149-210,335-351, run.py:285-293, sim_main.cpp:266-287, sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c, sw/litex/milan_soc.py:137-175; receipts/flash_driver_calls.txt; receipts/rerun-C1-asbuilt.log - the following were checked:`
    - a malformed or non-power-of-two `--fetch-l1` is refused;
    - a cached netlist without a line-aligned refill address is refused;
    - the XIP link script is refused if its anchor moved;
    - a refill error ends the wait once;
    - the XIP code sits at 0x410000, clear of the journal at 0xEE0000;
    - inside the driver's chip-select window the driver calls only its own block-RAM functions (the 64-bit library helpers sit in `ls_now_us`, outside the window), so D3's driver-in-block-RAM rule holds for the arm;
    - the cached as-built control traps at the same cycle and address as archived (`TRAP 151504 0 1 00006880`).
- **Tests - UNCLEAN (F3, F4).** Checked, at the head:
  - Self-test rc 0: 92 checks, 67 of 67 mutants caught. The README mutant table matches the self-test output on all 67 rows, the five new ones exactly; the one paraphrased row is an S2 row outside this delta (`receipts/mutant_table.txt`).
  - `test_soc_options.py` rc 0 with its three controls killed (`receipts/test_soc_options-head.log`).
  - Every one of the 23 archived arms' `table.md` recomputes byte-identically with the head's `run.table()` from the archived graded JSONs, and every graded JSON equals the head regrade's hash list (`receipts/recompute_tables.txt`).
  - Independent reruns at the head with the pinned 5.050 simulator:
    - **1x1 split cache:** `table.md` byte-identical to the archived head regrade (sha256 `8760d2193f9d9855...`), and all 18 graded JSONs equal (`receipts/compare-rerun-P1-64x1.txt`).
    - **1x1 cacheless:** `table.md` sha256 `a835c98b8bb613937463a54deb91aa251e3b6cb144486ea59195cb34abed11e5`, the hash the evidence records for S2's final A1 table, and all 18 JSONs equal (`receipts/compare-rerun-P1-none.txt`).
    - **The as-built and slow-adp-rx controls:** both caught.
  - Reviewer mutants: `receipts/harness_probes.txt` (eight mutants, all survive the self-test, two of them against claims the self-test makes) and `receipts/soc_options_probe.log`.
- **Docs - UNCLEAN (F1, F2, F3).**
  - Re-derived from the archived JSONs and reports, and matching the README, `SPLIT_CONTROL_MEMORY.md` section 7, the `MARK_II_AREA_PLAN` ledger and the PR body:
    - the sweep table (every composed and released figure and path count);
    - the window table;
    - the arm table, including arm B's partial 8.61 / 14.07;
    - CPI and fetch and data waits;
    - the worst passes;
    - the residual shares (65/43 %, 18/39 %, 7/6 %, 3 %; 40-42 %, 15-21 %, 12-21 %, 7 %);
    - the fan-out ranges, whole and per row;
    - the backlog rows;
    - the XIP table (CPI, refill, tiles 35.5 to 15, 56 to 35);
    - the Vivado and Yosys tables;
    - the ledger arithmetic (114 + 1.5, 115 + 1.5, 116 + 1.5; 6.0, 5.0, 4.0 left);
    - the cached controls' figures.
  - Receipts: `receipts/composed_lines.txt`, `arm_figures.txt`, `pass_shares.txt`, `fanout_ranges.txt`.
  - Docs gates at the head all return rc 0, and the tree is clean after them (`receipts/gates-head.txt`): `check_baremetal_only.py --check`, `docs_check.py`, `check_em_dash.py --base f58d049b` (0 of 335 added lines), `gen_toc.py --check` and `--verify-anchors`, the Python and C++ idiom gates, hygiene, and `git diff --check`.
  - Exceptions: F1, F2 and F3, plus the four residue items.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 open) | issue scope and decisions; `milan_soc.py` delta; `FR_NFR.md` NFR-SCOUT-01; README path tables; archived regrades | R713-1 | `a611785f2afe5bbe587f74034d869e869a1c8d37` |
| RTL | CLEAN | `milan_soc.py:2815-2833,2900-2903`; generator `Param.scala`, `FetchL1Plugin.scala`, patched `Soc.scala`; netlists 2c4bb987, 77fd592c, dd10544c, 1e5f104c, 30427aa8, 3432f054; archived out-of-context reports | R713-1 | `a611785f2afe5bbe587f74034d869e869a1c8d37` |
| Robustness | CLEAN | `split_soc.py`, `build.py`, `run.py`, `sim_main.cpp` deltas; `nvm_flash_litespi.c` and its object's call relocations; flash layout; as-built control rerun | R713-1 | `a611785f2afe5bbe587f74034d869e869a1c8d37` |
| Tests | UNCLEAN (F3, F4 open) | `selftest.py`, `selftest_mutants.py`, `test_soc_options.py`; self-test; 23-arm recomputation; two full reruns and two control reruns; reviewer mutants | R713-1 | `a611785f2afe5bbe587f74034d869e869a1c8d37` |
| Docs | UNCLEAN (F1, F2, F3 open) | harness README, `SPLIT_CONTROL_MEMORY.md` section 7, `MARK_II_AREA_PLAN.md` ledger, PR body; docs gates | R713-1 | `a611785f2afe5bbe587f74034d869e869a1c8d37` |

## Real limits

- **Not re-executed by this review:**
  - the 8x8 points;
  - the 2, 8 and 16 KiB sweep points;
  - arm B and the SHUTDOWN arm;
  - the XIP arms;
  - the slow-adp-shutdown control.

  Their figures were checked by recomputing every table at the head from the archived graded JSONs, which were themselves graded from logs that are only partly archived (28 of the run logs are published). For the groups whose logs are not archived, the per-group grade is the archive's.
- **Vivado and Yosys were not rerun.** Their figures were checked against the archived reports.
- **The all-fabric export digest was not rerun.** Byte identity rests on three things:
  - the construction (the only product change is under `if ctrl_mailbox:`, and no shipped config sets it);
  - `git diff` showing `sw/`, `configs/` and `hdl/` identical between `f3c71e42` (where the five-config digest receipts were taken) and the head;
  - the author's digest receipts.
- **Not run:** behave, the four-shard sweep, `test_builder.py --require-rv32` and hardware or bench work. Physical calibration was NOT RUN, and no hardware or bench evidence is claimed.
- **Exact-head hosted contexts** (read-only snapshot, `receipts/hosted-checks-a611785f.tsv`): 23 success, 11 failure, 30 cancelled, 1 skipped.
  - The failures sit in workflow meta-steps: "Require every gate exactly once" in docs-check and elaborate, and the TSN-boundary hold in firmware-boundary.
  - This review does not attribute or diagnose them.
- **Clone state.** Fetching the public evidence commit `80437076` with depth 1 left that id in the clone's `.git/shallow`. Tracked blobs, modes, the index (`write-tree` = `690ebd66...`) and all six gitlinks are verified equal to the head (`receipts/clone-integrity.txt`).

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `f58d049b`; live dev `76de691e`), with its builder and native banks, at the merge turn.
- Accept or diagnose the exact-head hosted contexts and act; the failures above are unattributed.
- Carry RS1 to RS4 to the residue checklist.
- NFR-SCOUT-01's amendment is the owner's; this PR correctly leaves the requirement text unedited.
- PR #792 merges first; the integrated route for the cache's tiles is M8a-2's.

R713-1 FINISHED

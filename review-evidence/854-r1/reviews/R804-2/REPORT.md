[R804] NEGATIVE - exact head de71984e4fc1b568065dffec483ea3ff51518604

# External independent review R804-2: issue #854 / PR #862 (round 2 delta)

Head `de71984e4fc1b568065dffec483ea3ff51518604`, tree `33ee98fa7e7df8f2534daa08bc435f12deb3ff6d`. The remote branch tip equals that head at review time. Source base: `dev` `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`, the live `dev` tip.

Delta judged: `e87f2179..de71984e`, four commits (`7a19f62b`, `4d6a165c`, `3a7660b1`, `de71984e`), against the round 2 ruling on #854 (issuecomment-6739837279). The RTL, the overflow test and the mutants were accepted at `e87f2179`.

## Verdict basis

**NEGATIVE, for one MINOR under `Docs` (R804-2-F1).** One sentence in the new findings section says a flip-flop delta is the change's. Part of that delta is placement movement in the SoC.

The fix is one sentence in `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`. It needs no re-measurement, no record change and no RTL or test change.

Everything else the ruling asked for is met and verified at the head:

- **Ruling item 1.** Record 16 at all three endpoints, written by `record --write`. The `measured` notes name #854. `check-baseline` passes. The selected route fits: 15,820 of 15,850 slices, WNS +0.166 ns against the +0.030 ns floor.
- **Ruling item 2.** The area text gives the wrapper as the instance total including `u_pp` +27 LUT. It states the tap's own share, and gives the same-directive comparison.
- **Ruling item 3.** The drain-rate and per-leg tally wording is corrected.
- **Ruling item 4.** The runt and oversize legs are in place, and their mutants are killed.
- **Ruling item 5.** The RTL change is comments only.

Every round 1 finding, mine and the internal reviewer's, is resolved or was carried by the ruling.

The other new items are one RESIDUE and two SUGGESTIONs. None of them affects coverage.

## Findings

### R804-2-F1: MINOR, lens `Docs`. The new findings section credits all +13 FFs to the change; 3 of them are placement replication in the SoC

- **Where:** `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:110`:
  > The LUT figure moves with placement at either directive; the flip-flop figure, +13 at both, is the change's.
- **Evidence:** `receipts/hier_attribution.txt`, from `scripts/hier_attribution.py` over the published hierarchy reports. Their hashes are listed in that receipt, and the published packet's manifest verifies them.
  - The change's own flip-flops are the wrapper's +10: the tap's +9 plus `ctl_fifo`'s +1. That is the same in every run at the head: the wrapper is 20,038 FF in all three routes, and both standalone endpoints move by +10.
  - The head's ExtraPostPlacementOpt route has 3 more FFs than its AltSpreadLogic_high and ExtraTimingOpt routes (54,850 against 54,847). All 3 are in `VexiiRiscvLitex_…/dma_bridge_write_bridge/aligner` (146 FF against 143), in the SoC. This RTL does not touch it.
  - Same directive against same directive, the flip-flop figure also moves with placement:
    - AltSpreadLogic_high: 54,837 to 54,847, which is +10.
    - ExtraTimingOpt: 54,838 to 54,847, which is +9.
    - ExtraPostPlacementOpt: +13.
  - So the sentence's contrast ("LUTs move with placement, the FF figure is the change's") is false.
- **Why MINOR and not RESIDUE:**
  - This is an attribution claim about a measured area figure. It is the same class as R803-1-F1, which the internal reviewer classed MINOR ("a figure and attribution claim, not pure wording") and which the ruling required to be fixed.
  - The rule in this assignment also says an uncertain case is MINOR.
  - Other lenses are not attributable. `Conformance` is clean, because the ruling's item 2 content is present and correct elsewhere: `:112-124`, `AREA_BUDGET.md:256-259` and the PR body. The defect is one additional sentence.
- **Impact:** a cold reader of the authoritative findings page learns that the drop count costs 13 FFs structurally. It costs 10, and the other 3 move with placement. That misleads the next attribution of a route FF delta against this record.
- **Required outcome:** the sentence no longer credits the SoC's 3 FFs to the change. Suggested text:
  > Both figures move with placement. The change's own flip-flops are the wrapper's +10 (the tap's +9 and `ctl_fifo`'s +1), at all three directives and both standalone endpoints. The other +3 are register replication in the SoC's DMA aligner in the ExtraPostPlacementOpt route alone; the head's AltSpreadLogic_high route is +10 FF against the preceding record's.

  If the same claim appears in the PR body, apply the same correction there. It does not appear there at this head.
- **Verification:** re-read the sentence against `author-r2/receipts/area/runs/{eppo,aslh}/baseline_hierarchy.rpt`, using `scripts/hier_attribution.py`. This is a docs-only change: no synthesis input moves, so record 16 and every other lens stay valid.

### R804-2-R1: RESIDUE, source docstring wording. `drops_mutant.py` still speaks of one clean control

- **Where:** `tb/verilator/pp_shadow/drops_mutant.py:25` ("Exit 0 = the clean control passed") and `:111` ("The clean control, then every arm"). The driver now runs two controls (`:130-135`), and its final line (`:162`) says "both clean controls pass".
- **Classification:** wording only. No check, figure or behaviour changes.
- **Exact fix:**
  - `:25`: "Exit 0 = both clean controls passed and every arm was caught by its named check; 1 = otherwise."
  - `:111`: "The two clean controls, then every arm; 0 when each arm was caught."

### R804-2-S1: SUGGESTION, lens `Docs`. "The wrapper less its children" is the change of a remainder, not a count of the tap's cells

- **Where:** `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:113` and `:121-123`; `docs/design/AREA_BUDGET.md:258-259`; the PR body's "tap's own share" table.
- **Evidence:** `receipts/hier_attribution.txt`.
  - Vivado's hierarchical LUT totals are not additive at this boundary.
  - At the head, the wrapper's own-cell row `(pp_shadow)` is 18 LUT in every run.
  - "Total minus children" is +1, 0 and 0 on the three routes, and -5 and -6 on the standalone endpoints. Cells shared across the boundary are counted in both the parent and the child rows.
  - So "+8 / +7 / +6 LUT" is the change in that remainder. It is a fair estimate, and the PR body already says "about +8". It is not a direct count of the tap's cells.
  - The FF figures are additive (the remainder equals the own-cell row, 332), so "+9 FF" is exact.
- **Optional outcome:** say that the LUT share is the change in the remainder, because the hierarchy's LUT totals are not additive. Or quote the change in the own-cell row when the preceding record's hierarchy report is to hand. The ruling's "about +8 LUT or not separable" is already met.

### R804-2-S2: SUGGESTION, lenses `Tests` and `Robustness`. The `RXFILT=0` runt grade runs only in the local mutant driver

- **Where:** `tb/verilator/pp_shadow/Makefile:163-171` (`RXFILT`, not in `RUN_CASES`); `scripts/suite_shards.py:159-167` (`PIECE_SECONDS["pp_shadow"]` has four legs); `sw/builder/endstation_builder.py:412` (`--no-rx-mac-filter` maps to `RXFILT_P`, a supported build option).
- **Evidence:** my probe `receipts/probe_counts_runts_filtered.log` builds the `counts-runts` plant in the filtered build. It passes `[DR]`, 19 checks with 0 failures, which confirms the PR's statement that it is an equivalent mutant there. Only the `RXFILT=0` build catches it (`receipts/drops_mutant.log`, KILLED). No hosted or default `make` path builds `RXFILT=0`.
- **Judgement of the PR's choice:** acceptable for this PR.
  - The hosted piece windows are keyed by leg index, and the driver deals cases round-robin across them (`suite_shards.py:159-160`). A fifth case would re-target a measured window that #804 owns.
  - The ruling asked for "a `-GRXFILT_P=0` build, which kills `counts-runts`", and that is delivered.
  - The default legs still grade that no runt reaches the FIFO.
  - The PR publishes the choice and its reason under "Known limitations".
- **Optional outcome:** a follow-up Issue to run `RXFILT=0 --drops-only` in a hosted context the next time the `pp_shadow` windows are re-measured. Until then, a regression of the runt exclusion in the `--no-rx-mac-filter` configuration is caught only when someone runs `make drops-mutant`.

## Round 1 findings, resolved at this head

| Finding | Severity then | Status at `de71984e` | Evidence |
|---|---|---|---|
| R804-1-F1, area not re-recorded | MAJOR | **RESOLVED** (option a) | See the record chain after this table. |
| R804-1-S1, runt leg in a `-GRXFILT_P=0` build | SUGGESTION | **TAKEN** | `Makefile:163-171`; `drops_mutant.py` `counts-runts` on the `RXFILT=0` leg, KILLED. My clean `RXFILT=0` probe passes with 157 overflows and count +108, as published (`receipts/probe_clean_rxfilt0.log`). |
| R804-1-R1, the "317 checks" tally | RESIDUE | **RESOLVED** | PR body "Status" and gate table: "base 738, vid73 738, crf 778, pending 317". My run gives the same four tallies (`receipts/pp_shadow_all.log:1627,2056,2801,2937`). |
| R804-1-R2, the drain rate | RESIDUE | **RESOLVED** | `README.md:175-176`, `sim_main.cpp:94-95` and the PR's limitation item 1 say "eight bytes every nine cycles". This matches `KL_pp_shadow.sv:945` (`ff_ready_w = ~ser_busy_r`), one pop cycle and then one byte a cycle. |
| R803-1-F1, area attribution | MINOR | **RESOLVED** as required | Required items: the wrapper is given as the instance total including `u_pp` +27 LUT; the tap's share is +9 FF and about +8 LUT; the same-directive table against record 15's ExtraPostPlacementOpt row (53,383 / 54,837 / 15,848 / +0.112 ns, which matches `ac0a01e3:docs/findings/234_PP_SHADOW_AREA_BASELINE.md:82`). These appear in the PR body, `234_…:98-124` and `AREA_BUDGET.md:256-259`. The sentence at `234_…:110` added with that text is a new defect (R804-2-F1). |
| R803-1-F2, the drain rate | RESIDUE | **RESOLVED** | As R804-1-R2. |
| R803-1-F3, oversize wording and grade | SUGGESTION | **TAKEN** | The comments at `KL_pp_shadow.sv:70-73,752,857-866`, `milan_csr.sv:699` and the `REGISTER_MAP.md` `PP_DIAG` row say "or longer than the FIFO". `[DR]` grades both sides of the boundary: 4,096 B kept and not counted; 4,097 B lost and counted +1, with the frame behind it handed out. `misses-oversize` is KILLED. |
| R803-1-F4, reset during a burst; `RXFILT_P=0` | SUGGESTION | Reset part **carried to #495** by ruling item 5; the `RXFILT_P=0` part **TAKEN** | Ruling item 5; R804-1-S1 above. |

The record chain for R804-1-F1, from `receipts/baseline_json_chain.txt`:

- The published `baseline-dev-ac0a01e3.json` equals `git show ac0a01e3:syn/ooc/pp_resource_baseline.json`.
- From dev to `baseline-recorded.json`, 52 paths change, all inside `endpoints/*/record` (the `record --write` output). No tolerance, floor or ceiling path changes.
- From recorded to final, only the three `measured` notes change, and each names #854 and `7a19f62b`.
- `baseline-final.json` equals the head's JSON.
- At the head, `check-baseline` reports `baseline PASS: 3 endpoints` (`receipts/resource_gate_selftest_baseline.log`).

## Answers to the review focus

1. **Area re-baseline (item 1).**
   - **Endpoints and directives.** All three endpoints were measured at `7a19f62b` on dev `ac0a01e3`: the route set at three directives, `ooc-1x1` and `ooc-8x8`. Every published `.rc` is 0 (`author-r2/receipts/area/record/`).
   - **Measured commit.** The synthesis inputs at `7a19f62b` equal the head's: `7a19f62b..HEAD` touches no `hdl/` file and no gitlink (`input-diffs.txt`, re-derived in `receipts/rtl_comment_only.txt`). They differ from `e87f2179` by comment tokens only (`receipts/rtl_comment_only.txt`, a token comparison with comments stripped).
   - **Record 15 to dev.** From `e44a4d20` to `ac0a01e3` only documentation, testbench files and the baseline JSON change, and every gitlink is equal (`receipts/synthesis_input_scope.txt`, re-derived with git).
   - **Fit and floors.** The selected ExtraPostPlacementOpt route uses 15,820 slices against 15,850 (`runs/eppo/baseline_utilization.rpt:76`) and has 0 routing errors (`route_status.rpt`). Its corners are Slow +0.166 / +0.050 ns and Fast +1.633 / +0.032 ns. The other two directives also meet both floors at every corner (`paths/*/slacks.tsv`).
   - **Gate checks.** `check` against record 15 exits 0 at all three endpoints, and again against the new record (`check-r15-*.rc`, `after-*.rc`).
   - **Text consistency.** The area page, CHANGELOG, findings entry, findings README row and `MARK_II_AREA_PLAN.md` agree with the record: 53,534 / 54,850 / 15,820, +0.166 ns, +106 / +13 / -9, and the "+0.166 ns record" warning anchor. The arithmetic checks: +35 = 27 + 1 - 1 + 8; +10 = 0 + 1 + 0 + 9; +10 = 3 + 7 and 4 + 6 out of context; +106 = +133 - 27.
2. **Area text (item 2).** Met, apart from R804-2-F1 (one sentence) and the optional R804-2-S1.
3. **Drain rate and per-leg tally (item 3).** Met; see R804-1-R1 and R804-1-R2 above.
4. **Runt and oversize legs (item 4).**
   - **Runt sub-leg.** It runs in every default build, where it grades that the filter stops every runt (one overflow per kept frame lost). It runs again in the `RXFILT=0` build inside `drops-mutant`, where runts meet the full FIFO (157 overflows) and the count is still +108.
   - **Oversize sub-leg.** It grades 4,096 B kept and 4,097 B lost and counted. The 4,097 B case matches `axis_fifo.v:204,217,275-283` (`full_wr` with `DROP_OVERSIZE_FRAME`, `overflow_reg` after the last beat), and `.DROP_OVERSIZE_FRAME(1)` is set at `KL_pp_shadow.sv:896`.
   - **Mutants.** `counts-runts` and `misses-oversize` are KILLED by their named checks.
   - **Wording.** "Or longer than the FIFO" is in the banner, the drop-logic comment, the port comment, `milan_csr.sv` and the register row.
   - **Not a fifth leg.** Judged acceptable; see R804-2-S2.
   - **Saturation.** Lost frames stay below 255 until the flood (209 counted before it), so the runt and oversize equalities are not masked by saturation.
5. **RTL unchanged except comments (item 5).** Proven by `receipts/rtl_comment_only.txt` for `KL_pp_shadow.sv` and `milan_csr.sv`, `e87f2179` to head: RESULT PASS. The new comments match the FIFO's code. No new comment in the delta carries a lane label, round, reviewer ID or comment ID (`hdl`, `tb` and `syn` added lines scanned).

## Reviewer-run gates at the exact head

All ran on this clone at `de71984e`, with the pinned simulator (`Verilator 5.050 rev v5.050`, wrapper hash in `receipts/environment.txt`).

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| `make -C tb/verilator/pp_shadow` (base, vid73, crf, pending) | 0 | 738, 738, 778 and 317 checks, 0 failures; `[DR]` in base, vid73 and crf: burst 31 / 31, refused +69 / +69 (158), runts +108 / +108 (108, filtered), 4,096 B kept, 4,097 B +1, flood 501 | `receipts/pp_shadow_all.log`, `.rc` |
| `make -C tb/verilator/pp_shadow drops-mutant` | 0 | both clean controls PASS; 8 of 8 KILLED by their named checks | `receipts/drops_mutant.log`, `.rc` |
| probe: clean `RXFILT=0 --drops-only` | 0 | 19 checks PASS; runts 157 overflows, count +108 | `receipts/probe_clean_rxfilt0.log` |
| probe: `counts-runts` plant in the filtered build | 0 | survives (equivalent mutant there), as the PR states | `receipts/probe_counts_runts_filtered.log`, `plant_counts_runts.*` |
| `pp_resource_gate.py --selftest`; `check-baseline` | 0; 0 | `312 arms and 500 generated cases PASS`; `baseline PASS: 3 endpoints` | `receipts/resource_gate_selftest_baseline.log` |
| `python3 -X cpu_count=2 syn/ooc/pp_resource_gate_mutants.py` | 0 | `control passes, all 236 mutants fail` | `receipts/resource_gate_mutants.log`, `.rc` |
| `docs_inventory.py --check`, `check_doc_style.py`, `docs_check.py`, `DOC_MAP.gen.py --check`, `check_feature_status.py`, `check_solution_docs.py`, `git diff --check ac0a01e3 de71984e` | 0 each | OK; `docs_check: 0 finding(s)` | `receipts/docs_gates.log` |
| `check_em_dash.py --base ac0a01e3` | 2 | cannot judge: the pinned Markdown renderer is not installed here. Substituted with a raw scan: 0 U+2014 in added Markdown lines | `receipts/docs_gates.log`, `receipts/em_dash_raw_scan.txt` |
| published evidence packet `edebc85d…/review-evidence/854-r1` | 0 | 1,169 files match `MANIFEST.json`, none missing or unlisted | `receipts/evidence_manifest_verify.txt`, `scripts/verify_evidence_manifest.py` |
| restore check | - | `HEAD` and `write-tree` both give `33ee98fa…`; `diff-index` clean; porcelain status empty; gitlinks at their recorded commits; submodule worktrees clean; only ignored build outputs remain | `receipts/restore_verify.txt` |

## Lens coverage and ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| `Conformance` | CLEAN | #854 Required items (round 1's RTL, unchanged in logic: `receipts/rtl_comment_only.txt`); ruling items 1-5; `syn/ooc/pp_resource_baseline.json` chain (`receipts/baseline_json_chain.txt`); `AREA_BUDGET.md:591-594`; selected-route fit and floors (`runs/eppo/baseline_utilization.rpt:76`, `paths/*/slacks.tsv`); `check-baseline` at the head | R804-2 | `de71984e4fc1b568065dffec483ea3ff51518604` |
| `RTL` | CLEAN | `hdl/milan/KL_pp_shadow.sv:70-73,752,857-896` and `hdl/common/csr/milan_csr.sv:699`, comment-only against `e87f2179` (token comparison); comment claims checked against `third_party/verilog-axis/rtl/axis_fifo.v:204,217,275-283`; logic carries its round 1 verdict, since the delta changes nothing it depends on | R804-2 | `de71984e4fc1b568065dffec483ea3ff51518604` |
| `Robustness` | CLEAN | `sim_main.cpp` `grade_runts_at_a_full_fifo_are_not_counted` and `grade_a_frame_longer_than_the_fifo_is_counted` (4,096 / 4,097 boundary, runts in both builds, saturation not masking); `RXFILT=0` probe; reset during a burst carried to #495 by the ruling (a round 1 SUGGESTION, not an open finding); R804-2-S2 optional | R804-2 | `de71984e4fc1b568065dffec483ea3ff51518604` |
| `Tests` | CLEAN | `drops_mutant.py` arms and two controls (8 of 8 KILLED); `Makefile:163-171`; all four `pp_shadow` legs at the head; equivalence probe; resource gate selftest and 236 mutants; R804-2-S2 optional | R804-2 | `de71984e4fc1b568065dffec483ea3ff51518604` |
| `Docs` | **UNCLEAN** (R804-2-F1, MINOR, open) | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` new section; `docs/design/AREA_BUDGET.md:240-259,692-697`; `MARK_II_AREA_PLAN.md`; `docs/findings/README.md`; `CHANGELOG.md`; `REGISTER_MAP.md` `PP_DIAG` row and prose; `TESTING.md` row; `pp_shadow/README.md`; PR #862 body; docs gates | R804-2 | `de71984e4fc1b568065dffec483ea3ff51518604` |

A fix for R804-2-F1 that touches only `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` (and, if wanted, the PR text) touches no artifact in the scope of `Conformance`, `RTL`, `Robustness` or `Tests`. Those lenses would stay covered at this head, and `Docs` must be re-covered at the fixed head.

## Real limits

- **Area.** I did not run Vivado. The area figures are the author's published runs, checked through the manifest hashes, the reports and the JSON chain. The evidence packet commit (`edebc85d`) is not cryptographically signed; its integrity rests on the manifest hashes, all of which match.
- **R804-2-S1.** Record 15's hierarchy report is not in the published packet. So the "+8 LUT" share cannot be checked against the change in the wrapper's own-cell row; only the remainder's change is checkable.
- **Em-dash gate.** `check_em_dash.py` could not run here, because its pinned renderer is missing. A raw scan of the added Markdown lines substitutes for it. The author's published docs.yml run reports it among 65 steps, 0 bad.
- **Out of scope for this round.** I did not run the docs.yml steps in full, the full sweep or the firmware, builder or BDD banks. The RTL logic is unchanged, so per the ruling no full sweep is due.
- **Hosted runs.** At review time, the head's hosted checks were 10 completed successfully, 1 skipped (Physical gPTP, nightly and manual), and 36 queued or in progress (`receipts/environment.txt`). No hosted verdict is claimed.
- **Hardware.** Physical calibration was not run. Field skips are not hardware proof.
- **Manager bank.** No manager source bank ran at this head, and none is claimed. The current-dev merge candidate is the manager's to build and validate at the merge turn.

## Pending manager duties

- Carry R804-2-R1 to the residue checklist with its exact fix.
- Route R804-2-F1, a one-sentence docs fix, and re-review `Docs` at the fixed head.
- Decide whether R804-2-S2 becomes a follow-up Issue (hosted `RXFILT=0` `[DR]` when the #804 windows are next re-measured).
- Confirm that #495 records reset during an overflow burst (ruling item 5).
- Own hosted and act acceptance at the exact head: the `rtl-fast`, `verilator-suites` and `yosys-portability` contexts were still queued or running at review time.
- Build and validate the current-dev merge candidate (builder and native banks) and link its receipts.
- Ignored build outputs (`tb/verilator/pp_shadow/obj_*`, `*.hex`) remain in this disposable clone. They are not tracked bytes.

R804-2 FINISHED

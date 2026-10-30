# HANDOFF: #806 round 2, executor [A701b]: the two other placement directives, and the R736-1-R1 wording

Status: **REVIEW READY** at `0c45ebf28e2c11352aa4ad40d46780143b1a77ab` (one commit on `f99405af`, no rebase, worktree clean, every submodule at its gitlink; live remote dev `1e80128f` unchanged; the remote branch is still `f99405af`). Nothing pushed.

- Lane: $LANES/806-adopt-gptp, branch `806-adopt-gptp-135afd04` (PR #813), origin https://github.com/kebag-logic/milan-fpga.git (verified); the lane branched from dev `1e80128f` (`git merge-base --is-ancestor 1e80128f HEAD` rc 0)
- Assignment: the latest [A10] comment on #806 (2026-10-30T12:17:39Z), under the #814 ruling (issuecomment-6522621984: WNS judged on the build floor at every corner on the best of the recipe's three directives; the fall from the record becomes a warning; the gate change is #818, open)
- Round 1: `806-a701/` (route-1x1 at ExtraPostPlacementOpt from the synthesis checkpoint at `cf3ef596`)
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/806#issuecomment-6523386592
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/806#issuecomment-6524308429
- No submodule git command was run this round.

## Items of the assignment

| # | Item | Result |
|---|---|---|
| 1 | route-1x1 at AltSpreadLogic_high and ExtraTimingOpt from the round-1 synthesis checkpoint, in parallel through `vivado-slot.sh` | done: both Vivado rc 0, placed and routed, 0 routing errors |
| 2 | each directive's WNS / WHS at every signoff corner, worst path and family, LUT / FF / slices; the best directive by worst-corner WNS | done (table below): **AltSpreadLogic_high, +0.235 ns** |
| 3 | do not re-record | nothing re-recorded; `syn/ooc/pp_resource_baseline.json` and the AREA_BUDGET policy table untouched (`pp_resource_gate.py check-baseline` rc 0) |
| 4 | R736-1-R1: replace the "owner decision" sentences in the PR body and docs | done, commit `0c45ebf2` and `PR-BODY.md` |

## Commit (one-line, no body, no trailer)

| Commit | Change |
|---|---|
| `0c45ebf2` | R736-1-R1: the owner-decision sentences on the route-1x1 WNS refusal replaced with the #814/#818 ruling |

| File:line at the head | Before | After | Clause / gate |
|---|---|---|---|
| `docs/design/AREA_BUDGET.md:144-145` | "...so the gate refuses it; [#806] holds the owner decision that refusal needs." | "...so the gate refuses it." then the assigned sentence verbatim, `#814` and `#818` linked: "Timing recovery is ruled under #814/#818; this change meets the build floor at every corner on its best directive." | the #814 ruling; R736-1-R1. The page is outside `check_doc_style.py`'s list |
| `docs/reference/SUBMODULES.md:429`, `:431` | "#806 holds the owner decision this refusal needs." | "Timing recovery is ruled under #814/#818." and "The best directive meets the build floor at every corner." (two paragraphs) | `scripts/check_doc_style.py` (10 words per sentence; 2 sentences and 20 words per paragraph) |
| `CHANGELOG.md:76-77` | "- That refusal needs an owner decision (#806)." | "- Timing recovery is ruled under #814/#818." and "- The best directive meets the build floor at every corner." | the same gate |

**Deviation, published:** in the two pages under the concise-style gate, the assigned sentence (20 words) cannot stand as one sentence. Each page carries it as two sentences of 7 and 10 words. The meaning is unchanged; only "this change meets ... on its best directive" is worded "The best directive meets ...", because "This change's best directive meets the build floor at every corner." is 11 words and the gate refused it (`CHANGELOG.md:77` and `SUBMODULES.md:431`, "sentence has 11 words; maximum is 10"). The PR body and AREA_BUDGET carry the sentence verbatim.

Kept unchanged on purpose: `AREA_BUDGET.md:146` ("The next growth on the shipping image therefore has no slice room and needs its own owner decision") is the #770 extension's slice-room rule, not the WNS refusal; `:147`, `:121` and `:524` are the #799 owner decision on that record's growth. Every measured figure, the route refusal and the open acceptance boxes are kept.

## The three directives (route-1x1, the shipping AX7101 1x1 export, at `f99405af`)

Method: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, "Repeat implementation with the repository's other two placement directives", its script text (`scripts/make_directive_runs.py`, the recipe's Python with only the `subprocess.run` moved out). The two runs reuse the round-1 synthesis checkpoint `alinx_ax7101_synth.dcp`, synthesised at `cf3ef596`. Its sha256 is `7253a8c0...81e5fb` before and after (`receipts/directives/synth-dcp.sha256.*`). `git diff cf3ef596 f99405af` changes four documents and no synthesis input, and `0c45ebf2` changes three documents. Each script differs from round 1's `baseline_integrated.tcl` implementation tail in one line, `place_design -directive` (receipts `*/baseline_implementation.tcl`). The other settings match round 1: default seed, `general.maxThreads 32`, Vivado 2026.1 Build 6511674.

Runs: started 12:58:07Z, both through `vivado-slot.sh` (slots 1 and 2, MemAvailable 43 GB). AltSpreadLogic_high ended 13:11:54Z and ExtraTimingOpt 13:12:09Z, each rc 0, peak 5.2 GB (`receipts/directives/timeline.txt`). Each ran in its own user unit (`systemd-run --user`, MemoryMax 12G, CPUs 32-47), because two routes would not fit this session's 16 GB unit. No sweep ran beside them.

| Directive | Slow 0C WNS / WHS | Slow 85C WNS / WHS | Fast 0C WNS / WHS | Fast 85C WNS / WHS | Worst-corner WNS | LUT | FF | Slices (free of 15,850) | Nets, errors | IOB pack |
|---|---|---|---|---|---|---:|---:|---|---|---|
| ExtraPostPlacementOpt (round 1, the shipping directive) | +0.032 / +0.052 | +0.032 / +0.052 | +1.638 / +0.034 | +1.638 / +0.034 | +0.032 | 51,837 | 53,788 | 15,823 (27) | 102,983, 0 | 21 PASS, 0 FAIL, 1 INERT |
| **AltSpreadLogic_high** | **+0.235** / +0.037 | +0.235 / +0.037 | +1.633 / +0.011 | +1.633 / +0.011 | **+0.235** | 51,874 | 53,787 | 15,837 (13) | 102,971, 0 | 21 PASS, 0 FAIL, 1 INERT |
| ExtraTimingOpt | +0.218 / +0.037 | +0.218 / +0.037 | +1.633 / +0.011 | +1.633 / +0.011 | +0.218 | 51,849 | 53,787 | 15,837 (13) | 102,962, 0 | 21 PASS, 0 FAIL, 1 INERT |

TNS and THS are 0.000 at every corner of every run. RAMB36 74, RAMB18 27 and DSP 13 are the same in all three. **The best directive by worst-corner WNS is AltSpreadLogic_high (+0.235 ns).** Every directive meets the build floor (`docs/integration/BUILDING.md` section 5: WNS >= +0.03 ns, WHS >= 0) at every corner.

Worst setup path per directive (Slow corners, `receipts/directives/*/worst-setup-path-Slow_0C.txt`; round 1's is `806-a701/receipts/vivado/route-1x1-worst-setup-path.txt`):

| Directive | Slack | Path | Family |
|---|---|---|---|
| ExtraPostPlacementOpt | +0.032 | `FSM_onehot_socbushandler0_axilite2wishbone_state_reg[3]` -> `milansoc_spiflash_phy_cnt_reg[8]/D`; 18 levels (CARRY4 3, LUT 15); data 9.835 ns (route 6.251) | SoC AXI-Lite-to-Wishbone bridge to the SPI-flash PHY counter (the path `AREA_BUDGET.md` names; #814's cut) |
| AltSpreadLogic_high | +0.235 | `FDPE_17/C` -> `KL_mac_rmon_events/fcs_cnt_r_reg[17]/R`; 0 levels; data 9.105 ns (route 8.757), net `macsys_rst`, fan-out 212, `SLICE_X45Y41` to `SLICE_X36Y186` | the sys-clock reset synchroniser's output (`FDPE_16` -> `FDPE_17`) fanning out to the MAC RMON counters' synchronous reset: a reset-distribution route across the die, same clock (`milansoc_crg_clkout0`), outside the wrapper and the datapath |
| ExtraTimingOpt | +0.218 | the same bridge-to-flash path as the shipping directive; 18 levels; data 9.703 ns (route 6.137) | SoC bridge to SPI-flash PHY |

Worst hold: Slow corners in each run are a `chan_tdm_render` bank register to its `u_fcdc` FIFO RAM input (+0.052 / +0.037 / +0.037). Fast corners are `milansoc_dd_reg[30]` -> `storage_37_reg` (+0.034, ExtraPostPlacementOpt) and the VexiiRiscv `unified_mBus_to_ioBus` data to its `ioBus_to_peripheral_bus_cc` RAM (+0.011, the other two). The worst Fast setup is the reset synchroniser's `FDPE` chain (+1.638 / +1.633).

Against the twelfth record (52,012 LUT / 53,707 FF / 15,780 slices / WNS +0.440 / WHS +0.036; tolerances 500 / 600 / 80 / 0.25):

| Directive | LUT | FF | Slices | WNS fall (warning under #814) | WHS |
|---|---|---|---|---|---|
| ExtraPostPlacementOpt | -175 | +81 | +43 | -0.408 | -0.002 |
| AltSpreadLogic_high | -138 | +80 | +57 | -0.205 | -0.025 |
| ExtraTimingOpt | -163 | +80 | +57 | -0.222 | -0.025 |

Against dev's own route (the #803 merge route, ExtraPostPlacementOpt, synthesis inputs equal to dev `1e80128f`: 51,801 / 53,760 / 15,834 / +0.303 / +0.028), the AltSpreadLogic_high route is +73 LUT, +27 FF and +3 slices.

The gate at its committed rule: `python3 syn/ooc/pp_resource_gate.py check <dir> --endpoint route-1x1`.
- ExtraPostPlacementOpt reproduces round 1: rc 1, "REGRESSION: fell by more than 0.25".
- AltSpreadLogic_high and ExtraTimingOpt are refused unread: rc 2, "NOT COMPARABLE: ... holds 0 recipe scripts, not one". The recipe's implementation script is not `baseline_integrated.tcl`, so today's gate cannot read a directive run. That comparison is #818's change.
- The figures above are therefore read with the gate's own parsers (`utilization()`, `timing()`), by `scripts/directive_figures.py`. Its WNS and WHS equal each run's per-corner minimum. Receipts: `receipts/directives/gate/`, `receipts/directives/directive-figures.txt`.
- For information only: every AltSpreadLogic_high and ExtraTimingOpt figure, its WNS fall included, is within the twelfth record's tolerances.

For the re-record after #818 (not done here): the ruling builds the shipping image from the best directive. AltSpreadLogic_high places 15,837 slices, so 13 of 15,850 would remain, not the 27 that `AREA_BUDGET.md:143`, `SUBMODULES.md` and the CHANGELOG record for the ExtraPostPlacementOpt route. Those figures stay as committed until the re-record.

## New checks

None. This round changes no test, RTL or generated record. The round-1 checks and their planted mutants stand (`806-a701/HANDOFF.md`).

## Gate table (head `0c45ebf2` unless noted; each command unpiped, its own log and rc)

| Gate | rc | Seconds | Result | Receipt |
|---|---:|---:|---|---|
| Vivado AltSpreadLogic_high, ExtraTimingOpt (at `f99405af`, from the `cf3ef596` synthesis checkpoint) | 0, 0 | 827, 842 | placed and routed, 0 routing errors, every corner at or above the floor | `receipts/directives/` |
| `pp_resource_gate.py check ... --endpoint route-1x1` | 1, 2, 2 | - | EPPO: WNS regression only (round 1 reproduced); the two directive runs: NOT COMPARABLE (no recipe script) | `receipts/directives/gate/` |
| `python3 scripts/check_doc_style.py` | 0 | 0 | OK, 23 current documents | `receipts/static-0c45ebf2/` |
| `gen_toc.py --selftest`, `--verify-anchors`, `--check` (the pinned Markdown venv) | 0, 0, 0 | 1, 5, 6 | - | same |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | 0 | the record and policy unchanged | same |
| `check_submodule_docs.py`; `check_gptp_docs.py` with and without `--with-submodule` | 0, 0, 0 | - | - | same |
| `check_hygiene.py --check`, `check_todo_ownership.py`, `check_feature_status.py`, `docs_check.py` | 0 x4 | - | the clone stays clean after | same |
| Docs workflow replica (`docs_steps.py`, GNU Make 4.3, CPython 3.12.3), the LiteX builder leg, the CPython 3.12.3 Markdown gates, the no-git gates | 0, 0, 0, 0 | 2,563 | 44 steps, 0 failed, 2 skipped by rule (gate_42 runs the candidate act runner on the host; the no-git step deletes `.git`); builder leg 1 with the LiteX interpreter 1/1; the five Markdown gates (link health, added-line em-dash, concise style, cited path, per-page contents) on CPython 3.12.3 5/5; `docs_check.py` and `check_feature_status.py` on a `git archive` export rc 0; base the live dev `1e80128f` | `receipts/docs-0c45ebf2/` |

Not run, by the assignment ("no full sweep and no other change"): the sweep, the simulation legs, Yosys, rtl-fast, the mutant campaign, ooc-1x1 and ooc-8x8. The commit changes three documents only. No RTL, test, script or synthesis input changes, so the round-1 results at `f99405af` and `cf3ef596` cover every other input.

## STOP conditions

None met. Both routes complete with 0 routing errors, and every corner of every directive meets the build floor.

## Open risks and questions

1. **The re-record after #818** uses the merge route's best directive. On this tree that is AltSpreadLogic_high, with 13 slices free rather than 27. The slice sentence on the three pages changes with the re-record.
2. **AltSpreadLogic_high's worst path is a reset-distribution route** (`macsys_rst`, fan-out 212, 0 logic levels, 8.757 ns of routing). The #814 ruling's item 3 names #817 for "the reset-synchroniser crossing". This path is same-clock, so this lane does not claim #817 covers it.
3. Round 1's open items stand unchanged: the hosted window of the `milan_dp` gptp case, the bench scenario (`Relates to #806`), pttPortEnabled, and the guard check's place in the leg.

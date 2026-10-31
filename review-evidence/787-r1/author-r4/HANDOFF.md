# [A700e] milan-fpga #787 round 4 handoff: merge dev `02ca829a` into `787-reboot-reset`

Status: **STOP** at `3e67de9c` (local, not pushed): **the route misses the floor.** All three placement directives
land below the +0.030 ns setup floor at the slow corners, and the #818 gate from PR #820 at `50e5d08d` refuses
the set (rc 1, `RESULT: MATERIAL REGRESSION`). The merge itself is complete and clean: six conflicts resolved
by keeping both sides' facts, every regenerated record equal to the union of the two sides, no behaviour choice. No
fix and no further route was attempted. Nothing was pushed, and no PR was created or edited.

## Assignment

- Issue #787, round 4: [A10] issuecomment-6541732410. Merge dev `02ca829a` only: conflict resolution and
  regeneration, no behaviour change. STOP if a conflict needs a behaviour choice, a regenerated record disagrees
  with what both sides recorded, or the route misses the floor.
- Executor [A700e]. TAKEN: issuecomment-6541766621 (`taken.md`). STOP: issuecomment-6543378747 (`stop.md`). These
  are the lane's only posts this round.
- Start: branch `787-reboot-reset` at `4aa5666e` (PR #822), branched from dev `1e80128f`, processor pin `a9e84b66`.
  `git remote get-url origin` is `https://github.com/kebag-logic/milan-fpga.git`. Dev was fetched from that URL:
  `02ca829a`, the live remote dev tip (`git ls-remote`). Each submodule's `rev-parse --show-toplevel` was its own
  directory, and its origin was its own repository, before any git command in it.
- Dev gained three merges since `1e80128f`: PR #813 (#806, gPTP `f97c1803` -> `135afd04`), PR #821 (#817, the servo
  reset synchroniser cut) and PR #816 (#70, the entity enable request and the volatile set).

## Commits (no rebase, nothing pushed)

| Commit | Subject |
|---|---|
| `5640e4d7` | Merge dev 02ca829a (PR #813 for #806, gPTP 135afd04; PR #821 for #817; PR #816 for #70) into 787-reboot-reset, keeping both CHANGELOG entries, pin rows, adoption records and area notes and regenerating the boundary diagram and its PNG manifest through submodule_boundaries.gen.py |
| `3e67de9c` | Re-record the port census in scripts/port_docs.budget through check_port_contracts.py --write-budget at the merged tree, hdl 2181, gptp-processor 127 and protocol-processor 1771 ports, the ratchets unchanged (#787) |

Head: **`3e67de9c1d42557f222edd2b079d23265bf1b726`**. The parents of `5640e4d7` are `4aa5666e` (the lane) and
`02ca829a` (dev). Gitlinks at the head: `protocol-processor` `a9e84b66` (this lane's) and `gptp-processor`
`135afd04` (dev's). The other four are unchanged on both sides.

`git diff --check $(git merge-base FETCH_HEAD HEAD) HEAD`, with FETCH_HEAD = dev `02ca829a`, gives rc 0
(`receipts/merge/diff-check.txt`).

## The conflicts and their resolution

`git merge --no-ff --no-commit` reported exactly the six files the assignment lists
(`receipts/merge/merge-tree-conflicts.txt`). Every other file merged textually, among them `syn/yosys/rom_digests.tsv`,
`docs/diagrams/submodule_boundaries.svg`, `milan_datapath.sv` and `milan_soc.py`. `git show --remerge-diff 5640e4d7`
touches only the six (`receipts/merge/remerge-diff.txt`). Dev's RTL and SoC hunks are disjoint from this lane's:
`.port_enabled_i (eff_link_w)` on the gPTP shadow, and #817's `add_servo_reset_constraints` hook.

| File:line at the head | Conflict | Resolution | Rule |
|---|---|---|---|
| `CHANGELOG.md:11-13` | both sides added a contents line | both lines: the REBOOT entry first, then gPTP `135afd04`, then the older entries | newest first, as the file orders them; the REBOOT entry lands after #806 |
| `CHANGELOG.md:53`, `:81` | both sides added an Unreleased section at the same place | both sections whole, in the same order, separated by one blank line | keep both sides' facts |
| `docs/design/AREA_BUDGET.md:143-149` | dev rewrote the base's binding-limit sentence (gPTP `135afd04`, 27 slices free) and added two; this lane kept the base sentence and added four #787 route sentences | dev's three sentences, then this lane's four. The base sentence dev replaced is dropped | a three-way resolution: each side's change kept, the base text dev changed not restored |
| `docs/reference/SUBMODULES.md:24-25` | the pin table's adjacent rows | dev's `gptp-processor` row (`135afd04`) and this lane's `protocol-processor` row (`a9e84b66`) | both pin rows; `check_submodule_docs.py` holds them to the index gitlinks |
| `docs/reference/SUBMODULES.md:383`, `:435` | both sides added an adoption record at the same place | #806's record, then #787's, chronologically as the page records adoptions | keep both records |
| `docs/reference/SUBMODULES.md:453` | this lane's record said "FPGA-gPTP stays at `f97c1803`." | "FPGA-gPTP stays at `135afd04`." | the only changed word. The sentence states that #787 does not move the gPTP pin, and that pin is now `135afd04`; the page's earlier records do the same (`:267`, `:283`, `:323`). #806's own "The processor stays at `f65c8ff7`." (`:385`) is true of #806 and is kept |
| `docs/diagrams/PNG_MANIFEST.json`, `submodule_boundaries.{drawio,png}` (generated) | both sides re-recorded the diagram from their own pins | dev's copy taken as the starting point, then `python3 docs/diagrams/submodule_boundaries.gen.py` at the merged index, which rewrote the SVG, drawio, PNG and the manifest's own entry | generated, never hand-merged |

`receipts/merge/resolution-vs-4aa5666e.diff` and `resolution-vs-02ca829a.diff` show the three prose files against
each parent. Against this lane only dev's facts are added (plus the one word above). Against dev only this lane's are.

No conflict needed a behaviour choice: no RTL, test, script or build file conflicted.

## Regenerated records, compared with both sides

| Record | Generator, run at the merged tree | Result | Against both sides |
|---|---|---|---|
| `docs/diagrams/submodule_boundaries.{svg,drawio,png}` and its `PNG_MANIFEST.json` entry (`:10-15`) | `python3 docs/diagrams/submodule_boundaries.gen.py`, then `--check` | rc 0; `OK (6 exact gitlinks, decoded PNG)` | Against this lane's copy, only the gPTP card's pin differs (`f97c18035be6` -> `135afd043309`, dev's fact). Against dev's copy, only the processor card's pin differs (`f65c8ff7c673` -> `a9e84b66d4cd`, this lane's fact). The textually merged SVG was byte-identical to the generator's (`receipts/merge/diagram-against-both-sides.txt`) |
| `syn/yosys/rom_digests.tsv` (`:15`, `:61-62`) | `syn/yosys/ooc.sh --record-rom-digests` | rc 0; it rewrote the rows of both owning pins | byte-identical to the textual merge: the union of this lane's six rows (`013ee63f`, `1be824fc`, `a9e84b66`) and dev's one (`135afd04` `gptp_ucode.hex`). Every digest equals the one its side recorded (`receipts/merge/rom-ledger-against-both-sides.txt`); the static bank re-recorded it again in a clean clone, `git diff --exit-code` rc 0 |
| `scripts/port_docs.budget:21` (commit `3e67de9c`) | `python3 scripts/check_port_contracts.py --write-budget` | rc 0; only the "ports per tree" comment line changes, to `hdl 2181, gptp-processor 127, protocol-processor 1771`. The ratchets and the recorded connections are unchanged | the union of both sides' measured deltas (below) |
| SUBMODULES.md pin table (`:24-25`) | no generator; `python3 scripts/check_submodule_docs.py` | `OK (6 exact gitlinks)` | both rows, each as its side recorded it |
| `docs/diagrams/timesync_chain.*` (dev's gPTP re-record) | `timesync_chain.gen.py --check` | `OK (RTL, features, Gitlink, decoded PNG)` | dev's copy stands unchanged |
| gPTP donor links and guide pins (dev's) | `python3 scripts/check_gptp_docs.py` (and `--with-submodule`) | `OK (8 current pages)` | dev's copy stands unchanged |

**The port census, counted per file** (`receipts/merge/port-census-summary.txt`, the four per-file TSVs from
`scripts/port_census.py`, which calls `check_port_contracts.py`'s own scanner):

| Tree | Measured: hdl / gptp-processor / protocol-processor | Committed comment line |
|---|---|---|
| base `1e80128f` | 2161 / 125 / 1766 | 2158 / 125 / 1764 (already stale at the base) |
| this lane `4aa5666e` | 2180 / 125 / 1771 (+19 / 0 / +5: `KL_reboot_ctrl` +14, `milan_datapath` +4, `KL_pp_shadow` +1, five processor files +1 each) | 2158 / 125 / 1764 (never re-recorded on this lane) |
| dev `02ca829a` | 2162 / 127 / 1766 (+1 / +2 / 0: `KL_gptp_shadow`, `KL_gptp_engine`, `KL_gptp_tx_slot` +1 each) | 2162 / 127 / 1766 (dev re-recorded it, `f475329c`) |
| merged `5640e4d7` | **2181 / 127 / 1771**: base plus both sides' per-file deltas, exactly | 2162 / 127 / 1766 (dev's line, merged textually) |

The regenerated line is the union of both sides' measured facts. The gPTP figure is dev's, and the processor figure
is this lane's own measurement at its pin. The gate does not read the comment line (only the `undocumented`
ratchets and the recorded connections), and this lane never re-recorded it. That is why it differs from both
committed copies. It does not disagree with either side's measurement, so the second STOP condition is not met.

**Checked and current at the merged tree, nothing regenerated:** the MAC transmit-chain model
(`gen_mac_tx_model.py --check`, plain and LiteX interpreters), the module matrix, the naming, lint, hygiene,
fail-fast and test-evidence ratchets, the four idiom gates, the solution documents' port groups, the HDL reference
comments, and the flash-layout and audio-path diagrams (generator output byte-equal to the committed files). The CI
command table's script hashes are not a gate pin. They show 27 mismatches at the base, 27 on this lane, 30 on dev,
and the same 30 at the merge, so the merge adds none.

**Found, pre-existing, not changed (outside a merge-only round):**

- `docs/diagrams/cdc_census.{svg,drawio}` has been stale on this lane since round 2
  (`receipts/merge/cdc-census-stale-on-lane.txt`). `python3 docs/diagrams/cdc_census.gen.py docs/diagrams/cdc_census`
  at this lane's head and at the merge writes "MultiReg 2-FF ... x3 call sites" where the committed file says x2. The
  third call site is this lane's PHY-hold MultiReg in `milan_soc.py`. At the base and at dev the generator
  reproduces the committed file, and the merge changes nothing (merged output == this lane's output). No gate reads
  it, and it is not pin-derived, so it is reported here rather than folded into a merge round. Regenerating it takes
  one command.
- `docs/diagrams/egress_queue_map.gen.py` and `nxn_window_map.gen.py` refuse at the base, on both sides and at the
  merge ("the RTL shape changed; fix this generator"), so their committed diagrams cannot be regenerated today. No
  gate runs them (`receipts/merge/generators-refusing-at-base.txt`).
- `make -C tb/verilator/milan_dp dynmap-mutants`, the command `docs/testing/TESTING.md` names, did not produce a
  complete verdict from a clean clone in this round. Its two end-to-end legs build with `make -o` over their
  generated inputs, so the listener leg (milan_dp_render) needs `tdm8r_aemi.bin`, `ltn_rom.hex` and `ucode.hex` made
  by its suite first. The talker leg (capture_coherence) built under the outer make, with `MAKEFLAGS=-j4` in my
  driver's environment, and spliced make's "Entering directory" lines into its datapath source list. Neither side
  changed those Makefiles or the two arms. With the inputs made and the script run directly, both arms pass
  (`receipts/campaigns-3e67de9c/dynmap-summary.txt`). Which of the two factors the talker needs is not separated.

## Route: route-1x1 at the merge, three directives, the #818 gate (the STOP)

Vivado 2026.1, recipe unchanged (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, "Integrated measurements"), default
seed, in a clean clone at `5640e4d7` (`scripts/make_clone.sh`). The export is the shipping AX7101 1x1 one, built from
`build.sh ax7101 --dry-run`'s own argv with `--build` removed, then `pp_baseline.py --single-thread-synthesis`
(`scripts/prep_route.sh`). The three artifact links stayed in place for the life of the runs (round 3's harness
lesson; `scripts/unlink_links.sh` removes them afterwards). One synthesis: 09:44 -> 10:31 UTC, 46 min 54 s
single-threaded, checkpoint SHA-256 `9f026a24...`. Then ExtraPostPlacementOpt continued in the shipping script,
and AltSpreadLogic_high and ExtraTimingOpt started from that checkpoint (`scripts/launch_comparisons.sh`). The runs
used slots 0, 1 and 2 of `vivado-slot.sh`, each in its own user scope. Every Vivado run ended rc 0: shipping 4,831 s
in total, AltSpreadLogic_high 2,388 s, ExtraTimingOpt 2,375 s.

The route at `5640e4d7` stands for the head `3e67de9c`. `git diff 5640e4d7 3e67de9c` touches only
`scripts/port_docs.budget`, and no synthesis script or image manifest of the export names it.

**The #818 gate** (`syn/ooc/pp_resource_gate.py` and its four self-test modules, byte-equal to `git show
50e5d08d:syn/ooc/...`, in a scratch copy of the head's `syn/ooc` and `docs/design`; nothing from #820 entered the
tree), `receipts/results/head-set-check.log`, **rc 1**:

```text
route set: the recipe's 3 placement directives, worst-corner WNS_ns and WHS_ns
  ExtraPostPlacementOpt      0.018   0.033
  AltSpreadLogic_high          0.0    0.03
  ExtraTimingOpt             0.017   0.013
directive ExtraPostPlacementOpt selected: the best worst-corner WNS, 0.018 ns
LUT 52012 -> 52291 (+279) ok; FF 53707 -> 53833 (+126) ok; SLICE 15780 -> 15837 (+57) ok
RAMB36 74, RAMB18 27, DSP 13: unchanged
WNS_ns 0.44 -> 0.018 (-0.422)  REGRESSION: below the floor 0.03 at Slow_0C, Slow_85C; WARNING: fell by more than 0.25 from the record
WHS_ns 0.036 -> 0.033 ok
route status: complete, no unrouted net and no routing error
RESULT: MATERIAL REGRESSION
```

With the comparisons given in reverse order the gate prints the same lines and rc 1
(`head-set-check-reversed.log`).

### Per directive (`receipts/results/head-figures.md`, from each run's signoff and utilization reports)

| Directive | Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt (selected) | Slow_0C | **+0.018** | 0.000 | +0.062 | 0.000 |
| | Slow_85C | **+0.018** | 0.000 | +0.062 | 0.000 |
| | Fast_0C | +1.633 | 0.000 | +0.033 | 0.000 |
| | Fast_85C | +1.633 | 0.000 | +0.033 | 0.000 |
| AltSpreadLogic_high | Slow_0C | **+0.000** | 0.000 | +0.058 | 0.000 |
| | Slow_85C | **+0.000** | 0.000 | +0.058 | 0.000 |
| | Fast_0C | +1.456 | 0.000 | +0.030 | 0.000 |
| | Fast_85C | +1.456 | 0.000 | +0.030 | 0.000 |
| ExtraTimingOpt | Slow_0C | **+0.017** | 0.000 | +0.051 | 0.000 |
| | Slow_85C | **+0.017** | 0.000 | +0.051 | 0.000 |
| | Fast_0C | +1.513 | 0.000 | +0.013 | 0.000 |
| | Fast_85C | +1.513 | 0.000 | +0.013 | 0.000 |

Every slow-corner WNS is under the +0.030 ns floor. TNS is 0 everywhere: no endpoint is negative. Hold meets 0 ns at
every corner of every directive.

| Directive | LUT | FF | Slices (free of 15,850) | Block RAM tiles (ceiling 121.5) | RAMB36 / RAMB18 / DSP |
|---|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt | 52,291 | 53,833 | 15,837 (13) | 87.5 | 74 / 27 / 13 |
| AltSpreadLogic_high | 52,370 | 53,833 | 15,824 (26) | 87.5 | 74 / 27 / 13 |
| ExtraTimingOpt | 52,367 | 53,833 | 15,824 (26) | 87.5 | 74 / 27 / 13 |

Every resource figure is inside its tolerance (record LUT 52,012 +500, FF 53,707 +600, SLICE 15,780 +80, RAM and DSP
+0); no ceiling is exceeded.

Worst setup path per directive (both slow corners; all in `milansoc_crg_clkout0`, the 100 MHz `sys` clock, a
10 ns requirement; all in LiteDRAM's controller, from the ZQ-calibration timer into a bank machine):

| Directive | Slack | Source -> destination | Levels | Data path (logic / route) |
|---|---:|---|---:|---|
| ExtraPostPlacementOpt | +0.018 | `milansoc_sdram_zqcs_timer_count1_reg[2]` -> `subfragments_bankmachine3_state_reg[0]/CE` | 18 | 9.654 ns (25.8 % / 74.2 %) |
| AltSpreadLogic_high | +0.000 | `milansoc_sdram_zqcs_timer_count1_reg[13]` -> `subfragments_bankmachine2_state_reg[0]/CE` | 16 | 9.771 ns (21.1 % / 78.9 %) |
| ExtraTimingOpt | +0.017 | `milansoc_sdram_zqcs_timer_count1_reg[10]` -> `milansoc_sdram_bankmachine0_level_reg[2]/CE` | 17 | 9.756 ns (24.3 % / 75.7 %) |

None of the three is in `KL_reboot_ctrl`, the frame-end toggle, the MAC transmit side, the gPTP plane or the
servo. All are SoC SDRAM-controller logic that neither side of the merge changes.

### Against the two sides' own routes (one seed per directive each)

| Directive | worst-corner WNS: this lane, round 3 `667b9bbc` -> #806 (PR #813) -> merge | WHS | LUT | FF | Slices (free) |
|---|---|---|---|---|---|
| ExtraPostPlacementOpt | +0.165 -> +0.032 -> **+0.018** | +0.036 -> +0.034 -> +0.033 | 51,568 -> 51,837 -> 52,291 | 53,680 -> 53,788 -> 53,833 | 15,749 (101) -> 15,823 (27) -> 15,837 (13) |
| AltSpreadLogic_high | +0.151 -> +0.235 -> **+0.000** | +0.032 -> +0.011 -> +0.030 | 51,520 -> 51,874 -> 52,370 | 53,682 -> 53,787 -> 53,833 | 15,837 (13) -> 15,837 (13) -> 15,824 (26) |
| ExtraTimingOpt | +0.120 -> +0.218 -> **+0.017** | +0.036 -> +0.011 -> +0.013 | 51,524 -> 51,849 -> 52,367 | 53,680 -> 53,787 -> 53,833 | 15,837 (13) -> 15,837 (13) -> 15,824 (26) |

Round 3's figures are its own published set (PR #822's body, the #820 gate at `32f0d9b5` passing it). #806's are
PR #813's published set, whose best directive was AltSpreadLogic_high at +0.235 ns. The merge carries both changes
plus #817's and #70's. Its best directive is 0.147 ns below this lane's round 3 best and 0.217 ns below #806's. Its
LUT count is 723 above round 3's shipping route and 454 above #806's. In the placed hierarchy (shipping directive)
against round 3, `milan_datapath` moves from 43,011 to 43,398 LUTs and `pp_shadow` from 23,946 to 24,334, its FFs
unchanged at 19,438, on the same processor pin. That is not traced. With one seed per directive and the three
worst paths all in SDRAM-controller logic outside the change, this round cannot separate a design effect from
placement. Issue #787's bench comment (issuecomment-6529314868) reports an integration image of dev, #806, #787, #70,
#817 and #814 routed at +0.246 ns. #814 is not in dev yet, and the train order is #818, #814, #787.

### This PR's own logic in the route (shipping directive)

- The frame-end toggle crossing, `eth_clocks0_rx` -> `milansoc_crg_clkout1`, is `Max Delay Datapath Only` 8.00 ns at
  +6.62 ns over 51 endpoints (round 3: +5.87 ns, 51). The reverse pair is +6.63 ns over 14 endpoints (round 3: +6.73,
  14).
- `CONSTRAINTS: MultiReg eth=12 part=199`, round 3's census. check_timing's summary equals round 3's. The shipping
  log has no CRITICAL WARNING and no ERROR. ICAPE2 1 and STARTUPE2 1 are placed.
- IOB packing: `IOB-PACK OK: 22 port(s) constrained IOB TRUE checked, none unpacked` on all three directives.

## Gates

Every rc is the command's own exit status. Each bank ran in a clean clone at the stated head (`scripts/make_clone.sh`:
the lane's tree, its submodules from the lane's checkouts, origin/dev the live remote dev tip `02ca829a`).

| Gate | Head | rc | Result | Receipt |
|---|---|---:|---|---|
| `git diff --check $(git merge-base FETCH_HEAD HEAD) HEAD` (FETCH_HEAD dev `02ca829a`) | `3e67de9c` | 0 | no whitespace finding | `merge/diff-check.txt` |
| Static and pin-record bank (`static_bank.sh`, 32 gates one at a time) | `3e67de9c` | 0 x 32 | check-baseline PASS; ROM ledger re-recorded byte-identical (`git diff --exit-code`); both diagram checks; submodule docs (6 exact gitlinks); gPTP docs with and without the submodule; port contracts (hdl 2181, gptp-processor 127, protocol-processor 1771, every ratchet held); naming; test evidence; integrator params; RTL lint and its self-test; the four idiom gates and two self-tests; RTL source lists and self-test; `pp_srcs.py`; hygiene; fail-fast; TODO ownership; module matrix; SoC sources; NVM capture; feature status; docs_check | `static-3e67de9c/` |
| The builder bank (`python3 sw/builder/test_builder.py`, in that bank) | `3e67de9c` | 0 | `ALL GATES PASS EXCEPT 2 NOT RUN` (round 2's two: gate 1b's `MAKEFLAGS += -e` arm, which this make cannot exercise, and gate 11, which needs an Arty build tree not on disk). Gates 1f (9/9 cuts), 23m (5 configs), 1d and 1b pass, and so do #817's servo reset synchroniser cut and refusal controls | `static-3e67de9c/builder_bank.log` |
| `scripts/xvlog_gate.py --check` (through `vivado-slot.sh`) | `3e67de9c` | 0 | `PASS (0 finding(s) == ratchet)` | `xvlog/` |
| milan_dp suites, as the sweep runs each (`dp_suites.sh`: `timeout <budget> make -C tb/verilator/<suite>`, verdict by `suite_tally.py --verdict`) | `3e67de9c` | 0 x 4 | milan_dp 13,796 checks (20 tallies), milan_dp_gm_steps 202, milan_dp_mclk 171 (its mutants included), milan_dp_render 347; 0 in-suite failures; `suite_tally.py` over the four logs rc 0, 14,516 checks | `dp-3e67de9c/` |
| The milan_dp count against both sides | - | - | 13,796 = this lane's round 2 13,757 + 16 (the gptp and gptp-lat legs, 202 -> 210 each: #806, as PR #813 records) + 23 (the dynmap leg 688 -> 711: #70's `[VOLATILE]` block, every one of round 2's 688 check lines still present). Every other tally is unchanged | `dp-3e67de9c/milan_dp-against-round2.txt` |
| Campaigns whose inputs the merge changed (`campaigns_run.sh`) | `3e67de9c` | 0 x 7 | `[RB]` alone 68 checks, 0 failures (round 2: 68); `reboot-mutant` 6 of 6 caught (21, 5, 8, 8, 3, 2 failing checks, round 2's counts); LiteX simulations 7 of 7; `gen_mac_tx_model.py --check` OK at both levels; #70's `fw_service_budget` 14 + 55 = 69 checks, 0 failures (the sweep's recorded 69) | `campaigns-3e67de9c/` |
| #70's `make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4` (`dynmap_run.sh`) | `3e67de9c` | 2 | `71 checks: 67 PASS, 4 FAIL`. 64 of 66 arms caught, among them #70's three processor-copy arms. The dynmap (711 checks), maprec8 and maprec4 clean legs pass. The four failures are the two end-to-end legs' clean controls and their two arms, from harness preconditions (below), not from the merge | `campaigns-3e67de9c/dynmap_mutants-rerun.log`, `dynmap-summary.txt` |
| The same campaign's two end-to-end arms, 36 and 37, after their legs' own suites made their generated inputs, run directly with MAKEFLAGS cleared (`dynmap_e2e_run.sh`) | `3e67de9c` | 0 | `4 checks: 4 PASS, 0 FAIL`: the listener and talker clean legs pass, and both arms are caught (8 of 261 and 108 of 480 failing checks). **With the full run: 66 of 66 arms caught, every clean leg passing**, the README's count | `campaigns-3e67de9c/dynmap_mutants_e2e_arms.log` |
| rtl-fast replica (`rtl_fast_steps.py`, every job of the aggregate's `needs:`), behave included | `3e67de9c` | 0 | `rtl-fast: success; failed jobs: none`: 12 of 12 jobs, 56 steps rc 0. Behave: 14 features, 508 scenarios and 2,330 steps passed (round 2's counts). 7,889 s; base the live dev `02ca829a` | `rtlfast-3e67de9c/` |
| Docs workflow (`docs_steps.py`, GNU Make 4.3, CPython 3.12.3), builder leg 1 with the LiteX interpreter, the five markdown gates, the no-git step | `3e67de9c` | 0 | 44 steps, 0 failed: 42 run, all rc 0, and 2 skipped by rule (the act runner contract gate, and the no-git job's own step, run separately). Gate 9 (concise documentation) and gate 12 (verified submodule documentation) pass. Leg 1 with LiteX: 0 failed (`ALL GATES PASS EXCEPT 1 NOT RUN`, gate 11). Markdown gates 5 of 5. No-git `docs_check` 0, `feature_status` 0 | `docs-3e67de9c/` |
| Route-1x1, three directives, the #818 gate at `50e5d08d` | `5640e4d7` (stands for `3e67de9c`) | **1** | **`RESULT: MATERIAL REGRESSION`**: the selected ExtraPostPlacementOpt at +0.018 ns, below the 0.03 floor at both slow corners; every other figure inside its tolerance | `results/head-set-check.log` |
| The same gate, comparisons reversed (control) | `5640e4d7` | 1 | the same lines | `results/head-set-check-reversed.log` |
| `pp_resource_gate.py --selftest` and `check-baseline` (the `50e5d08d` files, scratch copy) | `50e5d08d` files, head record | 0, 0 | every arm PASS; `baseline PASS: 3 endpoints` | `offline/gate820-*` |
| #607 log check on each route log (`log_gate.py`, `clock_constraints.check_implementation_log`) | `5640e4d7` x 3 | 0 | no 12-4739, 20-1307 or 12-5201 diagnostic in any of the three logs | `results/head-607.log` |
| #607 control: the shipping log with one planted `CRITICAL WARNING: [Vivado 12-4739]` line | scratch copy | 1 (wanted) | `REFUSED: constraint application failed (#607)`, naming the planted line | `results/plant-607.log` |
| `python3 sw/litex/iob_pack_selftest.py` | `5640e4d7` | 0 | 22 arms, 21 mutants, 0 failures | `offline/iob_pack_selftest.log` |

**The targeted re-measure, campaign by campaign.** A campaign is affected when the merge changed its inputs relative
to the side that owns it (`git diff` of its inputs):

- **Affected, run above:**
  - `pp_shadow` `[RB]` and `reboot-mutant`. Dev changed `milan_datapath.sv`, `KL_gptp_shadow.sv` and the gPTP pin,
    all built into the leg.
  - The LiteX simulations and the MAC model check. Dev changed `milan_soc.py`.
  - #70's `dynmap-mutants`. Its three processor-copy arms now copy this lane's pin, and every arm plants into the
    merged `milan_datapath.sv`.
  - #70's `fw_service_budget`. Its capture SoC reads the merged `milan_soc.py`.
  - The builder gate bites and #817's constraint tests, in the builder bank.
- **Not affected, not run:**
  - `reboot_ctrl` and its 30 mutants: `KL_reboot_ctrl.sv` and `tb/verilator/reboot_ctrl/` are unchanged from this
    lane.
  - The #396 planner, its behave feature and the UART smoke self-test: `tb/tools`, `tests` and
    `scripts/baremetal_uart_smoke.py` are unchanged.
  - #806's gPTP suites: their wrappers and the engine are unchanged from dev, and this lane changes neither.

**Harness events.** The first start of `dynmap-mutants` was stopped by hand 54 s in, still building its
prerequisite legs. My unit had reached 14.9 GB beside rtl-fast's publication census (nine 700 MB workers). Its log
is kept as `dynmap_mutants-first-start-stopped-for-memory.log`; it is not a result. The campaign was restarted
alone (`scripts/dynmap_run.sh`). Its two end-to-end arms then needed the second run described in the table. The
unit's sampled peak was 14.0 GB, mostly reclaimable file cache: anonymous memory stayed under 7.5 GB where
measured. The host's MemAvailable never fell below 27.8 GB (`mem.tsv`).

Not run, by the assignment's gate list: the full sweep, and the full Yosys gate (`syn/yosys/run.sh`). Round 2 ran
them at `e12147d4`. rtl-fast's Yosys jobs ran at this head.

## STOP conditions

| Condition | Met? |
|---|---|
| A conflict cannot be resolved without a behaviour choice | no: the six conflicts are two documents' prose, the pin table and three generated diagram records; none is RTL, a test or a build input |
| A regenerated record disagrees with what both sides recorded | no: every regenerated record equals the union of the two sides' facts (above) |
| The route misses the floor | **yes**: every directive is under +0.030 ns at both slow corners, and the best, ExtraPostPlacementOpt, is at +0.018 ns. The #818 gate refuses the set, rc 1 |

So this round ends in STOP, not REVIEW READY. Per AGENTS.md section 2, the conflict is published and the choice is
left to the owner. The figures above are what that choice needs.

## Receipts

`INDEX.md` lists every file in this directory, generated by `scripts/gen_index.py` from the files present.
`RAW-RECORDS.txt` (per receipt directory) and `receipts/route/large.sha256` record by SHA-256 and size every file
over 200 KB: the full suite and Vivado logs and the route and synthesis checkpoints. Host paths in the receipts are
replaced by `<scratch>`, `<work>`, `<lane>`, `<lanes>`, `<home>`, `<tools>` and similar.

| Directory | Contents |
|---|---|
| `receipts/merge/` | the conflict list, the remerge diff, the resolutions against each parent, the diagram, ROM ledger and port census comparisons with both sides, `git diff --check`, the stale CDC census and the two refusing generators |
| `receipts/static-3e67de9c/` | the 32 static and pin-record gate logs, the builder bank and their table |
| `receipts/dp-3e67de9c/` | the four milan_dp suite logs (large ones by digest), verdicts, tally, and the count comparison with round 2 |
| `receipts/campaigns-3e67de9c/` | the campaign logs and tables, the dynmap re-run, its end-to-end arms' second run, the stopped first start, and `dynmap-summary.txt` |
| `receipts/rtlfast-3e67de9c/`, `receipts/docs-3e67de9c/` | the rtl-fast and docs workflow replicas' step tables, step bodies, logs and receipts. rtl-fast's per-job runner directories are not kept: they hold each job's virtual environment. The docs bank's hold only the builder legs' gate-result JSON and are kept |
| `receipts/route/` | per directive: route status, utilization (flat and placed hierarchical), IOB packing, clock interaction, check_timing, CDC summary, every timing report's design table, the log excerpt and rc; the gate logs, figures, #607 logs, gate self-test and check-baseline, IOB self-test, xvlog, slot wrapper logs and the prep log |
| `receipts/mem.tsv` | the unit's MemoryCurrent and the host's MemAvailable, every 15 s |

`scripts/` holds the drivers this round ran. From rounds 2 and 3, paths changed: `make_clone.sh`, `env.sh`,
`fw_env.sh`, `static_bank.sh`, `rtlfast_run.sh` with `rtl_fast_steps.py`, `docs_run.sh` with `docs_steps.py` and
`docs_steps_md312.py`, `prep_route.sh`, `launch.sh`, `viv.sh`, `xvlog_run.sh`, `route_figures.py`, `log_gate.py`,
`collect.py`, `collect_bank.sh`, `make_sweep_spec.py` (copied, not used) and `gen_index.py`. New:
`resolve_hunks.py`, `port_census.py`, `dp_suites.sh`, `campaigns_run.sh` (this round's selection), `dynmap_run.sh`,
`dynmap_e2e_run.sh`, `launch_comparisons.sh`, `unlink_links.sh`, `collect_route.py`, `mem_sampler.sh` and
`splice_pr_body.py`.

## For the manager

- Nothing to push. The branch's local head is `3e67de9c`, two commits on top of the pushed `4aa5666e`. PR #822 still
  shows `4aa5666e`. `PR-BODY.md` is PR #822's current body with the status, gate and timing sections updated for this
  round, Status STOP.
- The decision the STOP needs is the owner's, on the route. The merged image's best directive is +0.018 ns, under
  the +0.030 ns floor, while each side's own best met it (round 3 +0.165 ns, #806 +0.235 ns). The paths are in SDRAM
  logic outside both changes.
- No hardware or bench access and no flashing. No sub-agents.

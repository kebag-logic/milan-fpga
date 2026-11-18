# HANDOFF, round 5: the final head and attempt 2 (#665), [A794]

## Status (kept current, 15:16; final)

**The final head is `73272666` on `flip-train-1117-p11`: ready for the composition review.** RULING-1118f (#665
issuecomment-6981065172) resolves the CDC stop below. CDC-15 on the gray-pointer LUTRAM FIFO is the expected report,
accepted with no waiver. So the record-only re-baseline is made: `73272666`, on `05dc1791`. Nothing is pushed; the
manager pushes.

| Check at `73272666` | Result |
|---|---|
| `pp_resource_gate.py record … --write`, on p11's three release routes | rc 0; the written record is the dry run's, byte for byte (`receipts/step11/release/record-write.txt`): LUT 54,002, FF 55,203, SLICE 15,849, 84.5 block RAM tiles, RAMB36 71, RAMB18 27, DSP 15, CARRY4 3,760, WNS 0.194 / WHS 0.017 ns, ExtraTimingOpt selected. The endpoint's provenance note (`measured`) is restated with the rulings, the head and the attribution. Every tolerance, floor and ceiling is unchanged. One file, `syn/ooc/pp_resource_baseline.json`; the gitlinks stay `1616fc8f` / `801ef228` |
| `pp_resource_gate.py check --endpoint route-1x1` (both comparisons) | **exit 0, RESULT: PASS**, every figure 0 delta (`receipts/step11/release/gate-after.txt`) |
| `check-baseline`; `--selftest`; the set, placement and baseline-report self-tests | all exit 0 (`baseline PASS: 3 endpoints`) |
| The docs, idiom and hygiene checks | all 8 PASS, clean tree (`receipts/step11/gates/q-73272666/`). `doc_paths` counts 1 allowlisted build artifact here and in the lane, against 2 at 14:10; the count follows which build outputs are present in a checkout, not the commit |
| `git diff --check origin/dev-soft-core...HEAD` | prints nothing |
| The 12 split firmware images | **all EQUAL** to `3e908539`'s (`receipts/step11/images/hashes-73272666.txt`) |

**Not changed, by ruling (record-only):** `docs/design/AREA_BUDGET.md`:158-159 (the utilisation table's LUT and FF
column) and `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`'s record table still quote the previous record, 53,461 LUT
and 54,971 FF. The composition review may ask for them; they would be a docs-only follow-up.

**The PR body** (`round5/PR-BODY.md`) records:

- the three rulings (1118d, 1118e, 1118f) and the hierarchy table;
- the CDC check: covered, 201 of 201 Safe, and CDC-15 x192 on the render crossing beside the capture crossing's x50;
- the safety argument, and that the check closes R863's stated limit;
- the corrected premise and the re-baseline;
- Status: ready for the composition review at `73272666`.

`round5/DEBT-640.md` carries the attribution of 1118e item 5, the commit and one line on the CDC-15 rows (the #495
residue).

**RULING-1118e's STOP (15:08), resolved by RULING-1118f:** the render crossing's CDC-15 rows were held as a flag, and
the re-baseline was not made until the ruling.

RULING-1118e (#665 issuecomment-6979996755) resolves the 1118d stop below and asks for one check first, from the
existing routed checkpoints (no new route): `u_fcdc`'s new crossing, the RAM32M storage written on the write clock and
read into the 192-bit register on the read clock, must be covered by the crossing's timing exceptions and clean in the
CDC report, or the lane stops. It is covered, and it is not clean (`receipts/step11/cdc/fcdc-summary.txt`):

| Image (routed checkpoint) | Covered by an exception | `report_cdc` rows naming `u_fcdc` | `report_methodology` |
|---|---|---|---|
| p11's release image, ExtraTimingOpt (the selected route) | **yes:** every storage-to-register path is `Timing Exception: Asynchronous Clock Groups`, slack inf (`set_clock_groups -asynchronous` between `milan_clk` and `audio_clk`; `report_exceptions` lists none, since a clock group is not a path exception) | **CDC-15 Warning x192** ("Clock enable controlled CDC structure detected": each storage leaf's write clock to a `rdata_o` bit, depth 0), and CDC-2 x2 and CDC-5 x2 on its pointer synchronizers (missing `ASYNC_REG`) | no line names `u_fcdc` |
| p11's 1x1/1if split image, ExtraPostPlacementOpt (its best) | yes, the same | the same: CDC-15 x192, CDC-2 x2, CDC-5 x2 | no line names `u_fcdc` |
| p11's 8x8/1if split image, ExtraPostPlacementOpt (its best) | not applicable | none: this image carries no render master and no `u_fcdc`; its only `cdc_pair_fifo` is the capture's `u_tcdc` | no line names `u_fcdc` |
| for comparison, the candidate `c8ff391a`'s release image (block RAM, before #927) | | CDC-2 x2 and CDC-5 x2 only: the block RAM holds the crossing inside the primitive, so no storage row | three SYNTH-6 lines on its block RAMs (no output register merged) |

**What the flag is.** Vivado's summary puts all of the write clock's endpoints into the read clock in its **Safe**
column (201 of 201 at release and 1x1/1if; 0 unsafe, 0 unknown; 9 without `ASYNC_REG`, as before). CDC-15 is the
clock-enable-controlled structure: the read register loads only on `ren_i && !rempty_o`, and `rempty_o` comes from the
synchronized write pointer. That matches the safety argument both reviews made (R863: "Each entry is read at least
two synchronizer stages after its write"). **The same rule already fires on the base's unchanged TDM capture FIFO
`u_tcdc`**, whose LUTRAM storage has CDC-15 x50 (x52 at 8x8/1if) in every image, the candidate's included. The project
has not waived CDC-15 anywhere (`docs/findings/COMMERCIAL_TIMING_395.md` lists 249 and says they "have not been waived
or repaired"). What #927 adds is 192 more of the same rows. There is no new CDC-26 (LUTRAM read/write collision), and
nothing Critical. The two TIMING-47 lines in every image are on the sys and milan clocks, not this crossing.
**The reviews:** neither recorded a CDC report. R863 (#939 issuecomment-6978630716) states the limit: "the distributed
RAM's inter-clock arc was judged from 0 failing endpoints, not read in the report". R864 checks the branch identity and
the plants.

**The decision needed:** whether CDC-15 on `u_fcdc`'s storage, classified Safe and the same rule the shipping `u_tcdc`
already carries, counts as clean for item 3. If it does, items 3 to 5 are ready: the record by
`pp_resource_gate.py record … --write` with the dry run's figures, then the gate, the checks and the hashes. The PR body
states both outcomes. The #640 note (`round5/DEBT-640.md`) is written to be posted with the re-baseline commit;
it describes the record moving by that commit.

**Done at 15:12:** item 1 (this check; `receipts/step11/cdc/`); item 2 (the wording: no train docs or comments call
the distributed-RAM option split-only; the PR body's step-11 row and its route note, and this handoff's FIFO cell,
now say the render master's crossing is shared and the release image takes it, 74 to 71 RAMB36); item 4 (the PR
body); item 5 (`DEBT-640.md`). Item 3 is held.

**RULING-1118d's STOP (14:17), resolved by RULING-1118e item 1: the re-baseline was not made.** A release-image CDC FIFO instance changed
primitives and its flop count. `KL_tdm_render_master`'s frame crossing `u_fcdc` (`cdc_pair_fifo`, WIDTH 192, LOG2D 2)
holds its storage in **3 RAMB36E1** in the candidate's routed release image and in **32 RAM32M (128 LUTRAMs)** in p11's.
Its flops go from **24 to 216**: the 192-bit read register, which the block RAM's output register held before. This is
#927's `DIST_RAM_P = 1` on that one instance. #927's comment gives the reason: the slot bank's registers are written
straight into the storage, and "a block RAM's write-data hold requirement left those writes about +0.014 ns of hold at
the fast corner". So #927 states the change as intended, but the ruling stops on any primitive change of a release
FIFO, so task 5 (the record-only commit) is held. The other release FIFO, the TDM capture's `u_tcdc`, keeps its
storage and flops (34 LUTRAMs, 82 flops, no block RAM). **Decided by RULING-1118e item 1:** `u_fcdc`'s move from
block RAM to distributed RAM in the release image is accepted, and the re-baseline is the record alone, by the gate's own
`pp_resource_gate.py record … --write`. Run without `--write` at `05dc1791`, on p11's three routes, it prints the
record it would store (`receipts/step11/release/record-dryrun.txt`; rc 0; nothing written, the tree clean):
ExtraTimingOpt selected; LUT 54,002, FF 55,203, SLICE 15,849, 84.5 block RAM tiles, RAMB36 71, RAMB18 27, DSP 15,
CARRY4 3,760, WNS 0.194 ns and WHS 0.017 ns.

**The release image's delta by hierarchy**, from the two routed checkpoints (ExtraPostPlacementOpt; the candidate
`c8ff391a`'s release route and p11's; `report_utilization -hierarchical`; `receipts/step11/release/hier-diff.txt`):

| Where | LUT | FF | RAMB36 | LUTRAM | Step 11 changes its RTL? |
|---|---:|---:|---:|---:|---|
| The whole image | 53,571 to 53,971, **+400** | 54,944 to 55,206, **+262** | 74 to 71, **-3** | 3,822 to 3,950, +128 | |
| `u_fcdc`, the render master's frame FIFO, with its storage | +121 (logic -7, LUTRAM +128) | **+192** | **-3** | **+128** | yes: #927's `DIST_RAM_P = 1`. The 32 RAM32M are named `milan_datapath/u_fcdc/g_mem.mem_r_reg*`, so the report counts them in the datapath's own cells |
| `KL_aaf_clock_meter` | +41 | -18 | 0 | 0 | yes: #927, the group reference loaded through its adder (two registers, 53 bits, become one of 32) |
| The datapath's EDIT-window claim registers (`amap_edit_oclaim_expect_r`, `amap_edit_oclaim_word_r`) | | +96 (112 to 208 bits kept) | | | #927 moved the capture-source word's encode out of `amap_edit_validate`; all-fabric it is the same combinational function, and synthesis keeps 96 more of these bits |
| Every other module | about +238 | about -8 | 0 | 0 | no. The largest are `milan_csr` +338 and `KL_render_queue` -213; three transmit arbiters (-152) are absorbed into the datapath's own cells; the soft core is -25 and the top's own cells -45. `ptp_clock_validity`'s +64 flops are `gsi_gm_q_r`, moved there from the datapath's own cells |

So the -3 RAMB36 is `u_fcdc` alone, and most of the +262 flops are `u_fcdc` (+192) and the EDIT claim registers
(+96). The LUTs are `u_fcdc`'s storage (+128) and the meter (+41), plus about +230 of synthesis and placement
variation in modules whose RTL step 11 leaves unchanged (`git diff c8ff391a 05dc1791 -- hdl` touches seven files:
`cdc_pair_fifo`, the render master, the meter, two mailbox files that only the split build carries, the datapath and
a README). Vivado counts a LUT that packs logic from two instances in each of them, so the rows are each instance's own
report line and do not sum exactly.

**In short.**

- **The CPU verdict:** PASS, on U (unit 375) over every arm, at the candidate `4374cc27`.
- **p11 is at `05dc1791` (task 1 done, 14:12).** `74481d2e` plus one commit that drops the blank line `6ad5c259` left at
  the end of `plat_mutants.py`. `git diff --check origin/dev-soft-core...HEAD` now prints nothing over the whole train;
  that was its only hit. The docs, idiom and hygiene checks (`docs_check`, `doc_style`, `doc_paths`, `emdash`,
  `hygiene`, `py_idiom`, `toc_check`, `toc_anchors`) all PASS, with a clean tree. All 12 split firmware images are
  hash-equal to `3e908539`'s (`receipts/step11/images/hashes-05dc1791.txt`). p10 has the same blank line; it was not
  asked for there.
- **The receipts (task 3), regenerated at the end:** every cited file is under `receipts/`, re-collected from scratch;
  host paths, account names and the host's name are replaced (0 residual tokens); the repository's privacy scrub
  (`docs_check.scrub_files`) finds nothing over the whole folder; no file is over 200 KB; `INDEX.md` is generated
  from the files present.
- **Step 11, p11:**
  - every firmware image is hash-equal to the candidate's;
  - the confirmation diff is empty in all 7 groups, so the CPU rows carry;
  - the split routes meet #818's floor at both points: 1x1/1if +0.141 / +0.033 ns and 8x8/1if +0.073 / +0.034 ns
    (+0.005 before #927; the EDIT path no longer binds);
  - every gate passes.
- **The release image's resource gate:** exit 1 on LUTs alone, 54,002 against the record's 53,461 (+541 past 500).
  #927 brings about +400 of it. RAMB36 falls 74 to 71, and timing holds (+0.194 / +0.017). Re-baselined at
  `73272666` (RULINGs 1118d, 1118e and 1118f); the gate now exits 0.
- **`cdc_pair_fifo`'s default branch:** behaviour-identical by reading and by a bounded proof, complete at every LOG2D a
  default instance takes: **LOG2D 2, 3 and 4, no counterexample in 30 steps** (`fifo-bmc4` ended 14:25:40, rc 0;
  LOG2D 4 took 1,184 s, 220,519 variables). Vivado alone maps it identically at three of four parameter sets; at 48/4, an instance not in these
  images, it uses 2 fewer LUTs.

**THE CPU VERDICT: PASS.** U, the image that carries 8x8/1if's SRP unit at 375 us, holds every test of RULING-1118b
item 2b at 8x8/1if over every arm (arm A, answering-every-port, answering-ports, valid-destinations; complete 12:25;
`receipts/regrade/verdict-unit375-final.txt`):

| Test (item 2b) | U, unit 375 |
|---|---|
| the SRP record within its unit | 35,547 cycles, 375 us, **within 375** (167 cycles of margin) |
| every statement within its figure | one over, then restated by the unchanged rule: ADP's record 12,779 cycles in arm A's `backlog-adp-refill`, 135 us against 130 (as on B's image). Restated, so 0 exceeded |
| the load at 0.75 or less | **0.744** (with ADP's 135) |
| THE TRANSMIT's row within its figure | 76.81 ms of 77 |
| no budget miss | none, apart from the seven `backlog-owed` egress-hold rows the harness README ledgers ("miss their budget at every point"; the scenario's 60 ms hold), as at every point since round 4 |
| join intervals in range (181 to 239 ms) | 119 lines, 187.15 to 190.41 ms |
| the code: shards, the control campaign, the twin; no plant removed | PASS (797 of 797 caught; twin and its plants) |
| the 1x1/1if and 8x8/2if images byte-identical to the measured head's | yes, every arm (hash table below) |

**The lowest unit that holds is 375**, so U+1 (380) is not taken. U+1 holds too, over every arm: the SRP record within 380 by 643 cycles, the same ADP restatement, the load 0.744, 119 join lines in range and the seven egress-hold rows (`receipts/regrade/verdict-unit380-final.txt`).

**The final step-10 candidate is `flip-train-1117-p10` at `4374cc27`.** It is `c8ff391a` plus ADP's restatement, with
`load_grade`'s two own-record controls re-anchored to read the measurement's figure from `OWN_MEASURED` rather than a
literal 130 (28 of 28 refused, before and after). The images are unchanged. Its quick list passes but for `flip_check`, which reports exactly 8x8/2if's base eleven and, at 8x8/1if, only THE TRANSMIT's HELD line (76.81 of 77). `run.py --self-test` has 0 failures and `load_grade` 28 of 28.

**Step 11 (RULING-1118c): `flip-train-1117-p11`, final head `73272666`**: #939's `0297a19a` merged on the candidate
(`3e908539`), then `4374cc27` carried (`74481d2e`), then the preflight fix (`05dc1791`), then the record-only
re-baseline (`73272666`). Its RTL and images are `3e908539`'s. Nothing is pushed; the manager pushes.

| Step 11 item | State | Lands (estimate) |
|---|---|---|
| Hashes: every split firmware image at p11, per arm and point, against the candidate's | **all 12 EQUAL** (`receipts/regrade/image-hashes-p11.txt`) | done |
| Confirmation run on p11's RTL against the candidate's receipts: 8x8/1if `srp-talker-held` and the answering-ports arm (`aecp`, `aecp-largest-notice`, `aecp-fanout`); 1x1/1if `aecp-largest-notice` and `aecp-fanout`; 8x8/2if `aecp-fanout` | **EMPTY DIFF, all 7 groups:** the same stimulus, byte-identical logs (`srp-talker-held` alone is 761,187 SPAN lines, every one equal) and every measured figure equal (`receipts/regrade/confdiff-final.txt`). **The CPU rows carry to p11** (RULING-1118c item 2: hashes equal and the diff empty) | done 12:50 |
| Split routes at p11, three directives each, #818's floor (WNS >= +0.030 ns, WHS >= 0 at every corner) | **8x8/1if: MEETS on its best of three**: ExtraPostPlacementOpt **+0.073 / +0.034** (both floors; #927's own head +0.073 on that directive), ExtraTimingOpt +0.064 / +0.027 (met), AltSpreadLogic_high +0.006 / +0.036 (not met). Its worst paths are now on the mailbox clock (`KL_mbx` register read, `u_rx`). The datapath clock's worst is +0.835 to +0.989 ns, so the EDIT-window path no longer binds (+0.005 before #927). **1x1/1if: MEETS on all three**: ExtraPostPlacementOpt **+0.141 / +0.033** (the best; both floors), ExtraTimingOpt +0.054 / +0.036, AltSpreadLogic_high +0.031 / +0.036 (`receipts/regrade/fit-summary-p11.txt`) | **done 13:15** |
| The release (all-fabric) image's route set and resource gate at p11 | **Timing: the floors hold.** ExtraPostPlacementOpt +0.115 / +0.033, AltSpreadLogic_high +0.053 / +0.017, ExtraTimingOpt **+0.194** / +0.017 (selected); the route is complete. **`pp_resource_gate.py check --endpoint route-1x1`: exit 1, MATERIAL REGRESSION, on LUTs alone:** 54,002 against the record's 53,461, +541 past the 500 tolerance. FF 55,203 (+232, ok), SLICE 15,849 (0), **RAMB36 74 to 71** (the gate recommends a re-baseline for that), RAMB18 27, DSP 15, WNS 0.194 (record 0.334, a fall under the warning), WHS 0.017. The sub-block movements are protocol-processor LUTs of +-53 or less (not gated). At synthesis the candidate's release image has 56,526 LUTs and p11's 56,946 (+420). **Attribution, on the same directive** (ExtraPostPlacementOpt): the candidate's release image (`c8ff391a`, before #927) places 53,571 LUTs, 54,944 flops and 87.5 block RAM tiles, and p11's 53,971, 55,206 and 84.5. So **#927 brings about +400 LUTs** (+420 at synthesis), +262 flops and -3 tiles. The train before it is +110 over the record, inside the tolerance, and #927's share takes the image past it. RULING-1118d's re-baseline is held at its item 2, since `u_fcdc` changed primitives (the STOP above; `receipts/step11/release/resource_gate.log`, `receipts/step11/release/hier-diff.txt`) | done 13:40; the hierarchy 14:17 |
| Gates at p11: four shards, the twin, the milan_dp suites #927 touches | **ALL PASS:** the four shards (797 of 797 caught), the twin and its plants and maps legs, split, split-mutants, split-cdc, dynmap, maprec8, maprec4, aaf_clock_meter all and mutants, tdm8render and tdm8render-mutants (32 of 32), mbx all and dma-mutants (`receipts/step11/gates/`) | done 13:28 |
| `cdc_pair_fifo.sv`'s default branch (review point) | **Behaviour: identical by reading.** The write fires on `wrst_n && wen_i && !wfull_o`, as the old write sat in the reset's `else`. `rdata_o` resets on `!rrst_n` and loads on `ren_i && !rempty_o`, on the same clock. **A bounded Yosys equivalence of the old against the new module** (a miter; both clocks free under `clk2fflogic`, so any interleaving of write and read edges; from the zero state; every output equal at each of 30 steps; WIDTH 4, since no logic crosses data bits, at each LOG2D a default instance takes) finds **no counterexample at LOG2D 2, 3 and 4** (`SAT proof finished - no model found`; LOG2D 4 at 14:25:40; `receipts/step11/fifo/bmc4.out`). The 40-step full-width runs timed out without a counterexample. **Inference:**
(1) Vivado's standalone synthesis of the module alone is **identical, primitive for primitive, at 48/3, 52/3 and 192/2**. 52/3 is the TDM capture's `u_tcdc`, the default-branch instance the shipping images carry. At **48/4** (the I2S playback's FIFO) the storage and flops are identical (32 LUTRAMs, 88 flops), but the control logic maps to **22 LUTs instead of 24** (LUT6 14 to 11). It is not identical there, and that is the reviewer's to judge; that instance is in none of the release or split images measured here, whose reports list only `u_tcdc` and `u_fcdc` (`receipts/regrade/fifo-ooc-vivado.txt`).
(2) Yosys maps all four sets to identical Xilinx cells.
(3) In the built images, `u_tcdc` keeps 36 LUTRAMs, no block RAM and the same flops at 1x1/1if, 8x8/1if and the release image, and its logic LUTs move with the context (+1 and -1 at the split points; 32 to 21 at the release image).
Only `KL_tdm_render_master`'s `u_fcdc` takes `DIST_RAM_P = 1`: 3 RAMB36 to 0 and 24 flops to 216, so the 1x1/1if split image falls from 83 to 80 block RAM tiles, and the release image from 74 to 71 RAMB36: the render master's crossing is shared, not split-only, so every image that carries it takes the distributed storage (RULING-1118e item 2). The sims (split, split-mutants, split-cdc, dynmap, maprec, the meter, tdm8render, the twin) PASS | done 14:25 |

## The step-10 candidate and how it was built

**The candidate is a real commit on `flip-train-1117-p10`, now `4374cc27`** (`c8ff391a` until 12:40). It is B (`41d2bc2b`, the notice and listener
cuts on the final head) with:

- `3cdc613b`: 8x8/1if's `CTRL_LOOP_TX_MS` 77 (its row 76.81 rounded up; at most 80, so `SRP_REDECLARE_CS` stays
  8 cs) and its `CTRL_LOOP_SRP_UNIT_US` 375, with `record.srp` restated to 375 there;
- `0cfe1ddc`: every other restated statement;
- `7a536fc5`: one control re-anchored;
- `0b054867`: the prose;
- `c8ff391a`: a self-test check re-anchored to item 2b (`run.py --self-test`: 0 failures);
- `4374cc27`: 8x8/1if's ADP record restated to 135 (U's arm A), the two own-record controls reading it;
- `bf2c1184`: the ledger.

**Its images hash-equal the measured ones**, `ctrl_app.elf` sha256 per arm (`receipts/regrade/image-hashes.txt`):

| Point | Arm A | answering-every-port | answering-ports | valid-destinations | Equal to |
|---|---|---|---|---|---|
| 1x1/1if | `55484254` | `4e7b53c7` | `6971e95c` | `8ca50418` | B's, every arm |
| 8x8/1if | `175418f4` | `ea87356a` | `3c15ec34` | `e764b2fe` | U's, every arm |
| 8x8/2if | `ba343fd4` | `f64be15e` | `8c9fe28b` | `cf299386` | B's, every arm |

So U's 8x8/1if measurement is the candidate's, and B's 1x1/1if and 8x8/2if measurements stand for it. `CTRL_LOOP_TX_MS`
reaches the image only through `SRP_REDECLARE_CS`'s `(TX + 9) / 10`, 8 at both 75 and 77. The unit changes one
immediate.

**Done:** B at every point. The candidate's shards (797 of 797) and twin at `0b054867`, whose images `c8ff391a` keeps.
The quick list at the final tip `c8ff391a` passes but for 8x8/2if's base eleven (`flip_check`: exactly those 11; at
8x8/1if only THE TRANSMIT's HELD line, 76.81 of 77), with `run.py --self-test` at 0 failures. Fit and the timing floor
are in on the candidate at both points (below). U's answering-ports, valid-destinations and answering-every-port arms
are complete.

**B is complete at every point**, graded against the candidate's tables: 1x1/1if and 8x8/2if (the candidate's
images there) have no statement exceeded. The paced records are 310 of 310 and 585 of 595. The only budget findings
are the seven `backlog-owed` egress-hold rows at each point, as at round 4's tip.

**The candidate's own routes, before step 11** (the candidate `3cdc613b`, the AX7101 split route by the #810 route lane's recipe,
08:51 to 10:00; the floor is WNS >= +0.030 ns and WHS >= 0 at every signoff corner, and the stricter WHS >= +0.030
too; `receipts/regrade/fit-summary.txt`):

| Point | Directive | Worst WNS (Slow) | Worst WHS (Fast) | Failing setup / hold | LUT | BRAM tiles | Floor |
|---|---|---:|---:|---:|---:|---:|---|
| 1x1/1if | ExtraPostPlacementOpt (integrated) | +0.119 ns | +0.032 ns | 0 / 0 | 32,095 (50.6 %) | 83 | **met, both floors (the best set)** |
| 1x1/1if | ExtraTimingOpt | +0.002 ns | +0.014 ns | 0 / 0 | | | not met |
| 1x1/1if | AltSpreadLogic_high | +0.147 ns | +0.014 ns | 0 / 0 | 32,193 (50.8 %) | 83 | met; the stricter WHS not |
| 8x8/1if | ExtraPostPlacementOpt (integrated) | +0.005 ns | +0.036 ns | 0 / 0 | 43,361 (68.4 %) | 94.5 | not met |
| 8x8/1if | ExtraTimingOpt | **-0.019 ns** | +0.036 ns | 5 / 0 | 43,317 (68.3 %) | 94.5 | not met |
| 8x8/1if | AltSpreadLogic_high | +0.005 ns | +0.036 ns | 0 / 0 | 43,313 (68.3 %) | 94.5 | not met |

The routes carry the target platform's image at one interface, linked from the candidate (`ctrl_app.elf` sha256
`a00828fe` at 1x1/1if and `5edbba3a` at 8x8/1if). They are measurement routes: checkpoints and reports, with no
bitstream written.

**1x1/1if meets the floor on its best of three** (ExtraPostPlacementOpt: +0.119 / +0.032, both floors).

**8x8/1if MISSES the timing floor on all three directives:** best +0.005 ns, 0.025 short of +0.030. Hold is met at
every corner. Every directive's worst path is the same one, on the datapath clock (`milansoc_crg_clkout1`): from the
map edits' EDIT-window request in the mailbox's clock crossing (`KL_mbx_cdc/u_edit/rq_r[80..82]`) to a clock enable
in the datapath's AAF map state (`milan_datapath/amap_edit_oclaim_expect_r`, `amap_out_owner_r`). It has 33 to 38
logic levels and 71 to 74 % routing, over 19.5 to 19.7 ns. It is the same path family the #810 route lane's report
names at that PR's head (30 to 40 levels there, +0.001 ns on one directive, +0.292 on its best): placement-sensitive
RTL in the mailbox's EDIT window and the datapath's AAF map.

**The miss is the composed train's, not the candidate's.** The candidate changes no RTL, and its 8x8/1if image differs
from B's in the ROM's contents only. B's own image (`bf2c1184`, firmware `d0e19e37`, 2 bytes from the candidate's),
routed the same way, gives the same three results on the same paths: +0.005, -0.019 (5 failing) and +0.005 ns.
This lane may not change RTL. The cut would be the RTL's: pipelining the EDIT request into the AAF map's claim and
owner clock enables, or narrowing that cone. It belongs to the EDIT window's owner, and the owner decides whether
8x8/1if's floor gates the flip.

**Already in.**

- **B's 1x1/1if, every arm complete, graded against the candidate's tables** (the candidate's images there are B's):
  no statement exceeded. The paced record is 29,331 cycles, 310 of 310, and the long record 865 of 975. Its 7 BUDGET
  findings are all the `backlog-owed` group's egress-hold rows (`backlog.owed*`, `backlog-owed.service.*.last`, 62 to
  64 ms against 20). They are set by the scenario's 60 ms egress hold, which the harness README says "miss their
  budget at every point" and records without failing; the egress ledger holds them. Round 4's tip had the same 7
  there and at 8x8/1if. No other budget finding.
- **A self-test check re-anchored (to commit):** `run.py --self-test` failed one check at the candidate. It asserted
  8x8/1if's `record.srp` equal to 8x8/2if's, the nearest-point premise that item 2b replaces. Now every 8x8/1if
  record and event must be 8x8/2if's raised to its own where OWN states one, which covers more keys and still fails
  when the two disagree. The re-run is in progress; the images do not change.
- **The candidate's gates at `0b054867`:** the four firmware shards PASS, the control campaign catching 797 of 797
  (no plant removed; one re-anchored this round, `7a536fc5`). The twin PASSES: the two-placement comparison, its
  plants, the maps leg and its plant.
- With the candidate's tables, B's 1x1/1if PASSES (ACMP 29.93 of 30, txL 48.89 of 49, the last queued notice 137.97
  of 140; the load 0.522) and 8x8/2if has the base's eleven findings only (its tx row 104.69 within its 105).
- At 8x8/1if the tables pass `flip_grade.py --check` on B's figures: THE TRANSMIT's row 76.81 ms within 77, the load
  0.744 of 0.75. U's own figures replace B's there as they land.
- The host tests that read `CTRL_LOOP_TX_MS` (`srp_talker.cpp`: `kHoldOffMs` and `kLatestLeaveMs`) PASS at 1x1/1if,
  8x8/1if and 8x8/2if (16 of 16 each; `receipts/regrade/talker81.txt`). The suite runs them at 1x1/1if and 8x8/2if;
  8x8/1if was run in addition, since its figure moved.

**S12b.** The gating S12b runs, uncut, on the final bitstream only (RULING-1118c item 3), that is p11's image once
#939's two reviews are POSITIVE at its frozen head. A run on a pre-#927 image is a rehearsal. p11's split routes meet
#818's floor at both points so far (status table); the release image's route and gate land about 13:45. The CPU pass
is in, so nothing on this lane's side holds S12b beyond those routes and #939's reviews.

## The rule for the pass (RULING-1118b, item 2b), at 8x8/1if over every arm of the image that carries the unit

- the SRP record within its unit, and every statement within its figure;
- the load at 0.75 or less;
- no budget miss, and join intervals in range;
- the code passing the firmware shards, the control campaign and the two-placement comparison, with no plant removed;
- the 1x1/1if and 8x8/2if images byte-identical to the measured head's (shown above).

The lowest unit that its own image holds is taken: 375 (U) if it holds, else 380 (U+1).

## The figures at each point (B's restated tables, now the candidate's)

The figures are `flip_grade.py --check --point` (`receipts/regrade/rows-0cfe1ddc.md`, the tables before the 8x8/1if
unit and figure moved). A row's figure is against its bound, and a negative margin is inside. 1x1/1if's and
8x8/2if's carry to the candidate unchanged.

### 1x1/1if: PASS

| Row | Figure, ms | Bound, ms | Margin, ms |
|---|---:|---:|---:|
| R4 | 13.43 | 20 | -6.57 |
| R5 | 76.55 | 90 | -13.45 |
| R6 | 74.05 | 90 | -15.95 |
| first | 14.75 | 20 | -5.25 |
| last (queued notice) | 137.97 | 140 | -2.03 |
| R4L | 203.58 | 238 | -34.42 |
| ACMP | 29.93 | 30 | **-0.07** |
| ADP | 28.14 | 30 | -1.86 |
| MAAP | 28.23 | 30 | -1.77 |
| tx | 34.30 | 49 | -14.70 |
| txL | 48.89 | 49 | **-0.11** |

The load is 0.522 of 0.70. The one restatement is the paced record: 29,331 cycles, **310 us** (stated 305; 192 cycles
from 315, at which the last notice would be 141.39 ms of 140).

### 8x8/1if: decided on U's figures

- **On B's image** (the unit at 365): the load 0.744 of 0.75; THE TRANSMIT's row 76.81 ms, which `CTRL_LOOP_TX_MS`
  now states as 77 (RULING-1118b, item 2a: the figure follows its row and is not an owner bound; txL's 49 ms, held at
  1x1/1if, is). The rows are reported, not held (#872).
- **The SRP record**, 35,547 cycles (375 us), restated to 375 with the unit (item 2b). U measures it on the image
  that carries the unit.
- **Restated by the rule:** the polls base **300** (28,417 cycles), the apply **375** (35,350), the MAAP record **180**
  (16,682, `srp-talker-loss`) and the SRP record **375**.
- **The tx row against the figure**, for reading U's figures (the candidate's tables, `events_none` 45 from 8x8/2if
  by the nearest-point rule): a polls base of 295 gives 76.65 ms, 300 gives 76.81, 305 gives 76.97, and 310 gives
  77.13. So 77 holds while U's base is 305 us or less (29,047 cycles; B's 28,417 is 630 under). Past that, the figure
  follows the row up, and it must stay 80 or less. The base's heaviest pass and its cause are traced in the evidence
  below.

### 8x8/2if: the base's eleven findings, no twelfth

| Row | Figure, ms | Bound, ms | Margin, ms |
|---|---:|---:|---:|
| R4 | 45.24 | 20 | +25.24 |
| R5 | 209.68 | 90 | +119.68 |
| R6 | 199.36 | 90 | +109.36 |
| first | 21.13 | 20 | +1.13 |
| last | 867.89 | 125 | +742.89 |
| R4L | 211.12 | 238 | -26.88 |
| ACMP | 69.22 | 30 | +39.22 |
| ADP | 69.16 | 30 | +39.16 |
| MAAP | 73.41 | 30 | +43.41 |
| tx | 104.69 | 49 | +55.69 |
| txL | 474.19 | 49 | +425.19 |

The load is 0.799 of 0.70. The eleven are the base's: the load, R4, R5, R6, first, last, ACMP, ADP, MAAP, tx and
txL. **THE TRANSMIT's held figure is within: the tx row's 104.69 ms against `CTRL_LOOP_TX_MS` 105** (0.31 ms
margin). The notice item is 25,561 cycles (270 of 275 us, 629 cycles inside); before attempt 2 it was
28,960, the twelfth finding. Restated by the rule: the MAAP record **160** (14,770), a pass's events' fixed part
**45** (4,069) and AECP's timer event **120** (11,404, its cause traced below).

### The fixture and the platform ROM (S14 debt)

The size fixture is within its 60.5 in all six arms (130,952 to 131,448 B of `rom`; S14 debt of 4.5, unchanged). The
platform's 8x8/1if image needs 137,472 B, 256 B past 57.5, so **its entry is 58.0, S14 debt of 2.0** (`bf2c1184`). Its
other points are within their entries.

## Owed at the final tip

- The #495 residue (RULING-1118f item 5): the timing findings document is to list the render crossing's CDC-15 x192
  beside the capture crossing's; the waiver question waits for after the flip.
- Everything else of RULING-1118c is in: the routes, the release route set and gate, the confirmation, the hashes, the
  gates and the FIFO review point.

## The evidence (the measurements and traces behind the figures above)

- **B, the answering-ports arm** (all three points): the 8x8/2if notice item is 25,561 cycles (270 of 275 us, 629
  cycles of margin), and the 8x8/2if paced record (SET_CONFIGURATION) 55,239 (585 of 595). The 1x1/1if paced record is
  29,331 (310 us by the rule, restated from 305; 192 cycles from 315).
- **The 8x8/1if polls base**, the heaviest pass of `srp-talker-held` (sys about 5.04e8, the pass after a Listener
  Ready licenses a declared Talker): **B 28,417 cycles (300 us), 322 past the 28,095 that 295 holds**; A 28,258 (300);
  the final head `b5802de9` 30,631 (325); round 4's tip 29,933. In that pass every source's Listener presence changes,
  so the listener cut saves nothing there. Its polls: `maap_mbx:poll` 8,367, `ctrl_app_aecp:deliver` 7,736,
  `aecp_mbx:poll` 6,192 (a 3,582-cycle transmit in it), `ctrl_app_srp:deliver` 2,545, `srp_mbx:poll` 2,310, ACMP's
  and ADP's 620. B's SRP record there is 35,547 (375 us) and its apply 35,350 (375).
- **The first re-grade with B's figures** (06:30, superseded by the tip's figures above; real edits, the rest at round 4's: 1x1/1if paced 310, 8x8/1if base 300,
  apply 375, SRP record 375, MAAP event 240, 8x8/2if MAAP record 160 and AECP event 120, the notice item within its
  275): 1x1/1if PASS (the last notice 137.97 of 140, ACMP 29.93 of 30, txL 48.89 of 49); 8x8/2if the base's eleven
  only (its tx row 104.50 of 105); **8x8/1if: THE TRANSMIT's row 76.61 ms against the 75 then stated**, the load 0.743
  of 0.75. At a base of 295 the same tables give 74.89 ms, the manager's figure, so the step lies between 295 and 300
  and the base must be measured at 28,095 cycles or less.
- **Gates.** At the p10 tip `bf2c1184`: the four firmware shards PASS, the control campaign catching 797 of 797
  (as at `082d0037`; no plant removed, three re-anchored), and the twin (the two-placement comparison, its plants and
  the maps leg) PASS. At the step-9 head `112ab9b1`: the four shards PASS (797 of 797), the twin PASS and firmware
  coverage PASS (40 files; T8 restores `mbx.c`'s 194 of 194). At `7b3c1c94` (the listener cut, before T8): the four
  shards and the twin PASS.
- **The ROM ledger at the p10 tip `bf2c1184`**, restated to the measured images: PASS at four points, 9 of 9 controls,
  and `test_ctrl_memory` PASS. The size fixture needs 130,952 to 131,448 B over its six arms, within its 60.5 (S14 debt
  of 4.5, unchanged). The platform's 8x8/1if image needs 137,472 B, 256 B past the 137,216 that 57.5 holds, so its
  entry is **58.0, S14 debt of 2.0**. `ctrl_plat` is 18,048 B at 1x1/1if and 21,568 at 8x8/2if (#936's 64 B).
- **The 8x8/1if miss's measured cause** (B's heaviest pass traced by committed PC on B's own build, `cut/b81-base`):
  28,417 cycles, 4,550 instructions, CPI 6.2, fetch-bound. 855 cycles run in code the list leaves cold, among them
  `aecp owed_drain` (470) and `aecp_mbx fan_end` (347). `owed_drain` is one of the filter's two drops: the 8x8/2if
  images do not link it, but 8x8/1if's do. By function, the dearest:

  | Function | Instr. | Cycles |
  |---|---:|---:|
  | `ctrl_app_srp deliver` | 445 | 2,317 |
  | `aecp fan_out` | 122 | 1,719 |
  | `ctrl_app_srp source` (ACMP's forwarding source callback, 9 calls) | 54 | 1,674 |
  | `acmp acmp_declaring` (TSN stack) | 468 | 1,366 |
  | `srp_mbx poll` | 199 | 1,283 |
  | `ctrl_mem memset` (ACMP's source state, each source) | 405 | 1,206 |
  | `ctrl_app_aecp deliver` | 159 | 1,188 |
  | `aecp arm` | 266 | 1,114 |
  | `maap_mbx refresh_demand` | 120 | 1,076 |
  | `aecp_nvm_poll` | 188 | 981 |

  MAAP's demand, which asks ACMP's `acmp_declaring` about each of the nine sources every pass (through `memset`, the
  forwarding callback and the fixture's source port, with ACMP's `now`), is about 6,600 cycles of it. The store and
  face publication (`aecp_nvm_poll`, `nvm_mark`, `ctrl_app_aecp_store_words`, `nvm_rec_id_known`, the face's
  `publish`) is about 4,900. This is the pass after a Listener Ready licenses a declared Talker, in which every module's
  state moves at once. So a cut that skips unchanged work saves nothing here, as the listener cut showed. A cut must
  make the change itself cheaper, take it out of `acmp_declaring` (the TSN stack, a pin move), or move code into the
  fetch cache's reach (the list's procedure, a ruling).
- **What the filter costs at 8x8/1if, measured** (a moot option since RULING-1118b keeps the LINKED gate; the manager
  stopped N and NU at about 08:40, and their finished legs are receipts). N is B's code with its traced list unfiltered (268 entries:
  `aecp owe` and `aecp owed_drain` kept where the trace put them; `21486e00`, scratch). In `srp-talker-held` its 8x8/1if
  polls base is **27,792 cycles (295 us), 303 cycles inside the 28,095**, and 625 under B's 28,417. Its SRP record is
  35,589 (375) and its apply 35,392 (375). Both entries link in the 8x8/1if and 1x1/1if images; only the size
  fixture's 8x8/2if images lack them, and with the gate unchanged the LINKED rule refuses those builds. The target
  platform's image already links the same script without that check, where "an entry it lacks places nothing there".
  So the cut the 8x8/1if row needs is exactly what ruling item 1's filter took away there.
- **The 8x8/2if `event.AECP`, traced before it is restated** (as asked). B's dearest AECP timer event (TIMER#6) is
  11,404 cycles (120 us against its 115; round 4 measured the same 120), in the answering-every-port arm's
  `notice-burst-6`. The traced one is the same burst step in `notice-burst-3` (`aep/part1`, CPU cycle 306,501,852),
  11,381 cycles. Traced by committed PC on B's own build
  (`cut/b2-aecp-event`): 1,770 instructions, all in listed code. `aecp arm` is 975 instructions and 3,790 cycles, and
  `aecp_poll` 398 and 3,683. The rest is the loop's take and the other modules' event stubs (about 150 cycles each).
  The event runs the core's `aecp_poll` (`aecp_mbx.c` `event`). Each time the core re-arms its timer, `arm()`
  (`aecp.c:181`) walks every registration on both interfaces and then the live notice list, to find the earliest
  deadline. In a notice burst with every port's controllers registered, that walk is the cost. It is the core's
  design, unchanged by attempt 2 (`git diff ed5855fe 41d2bc2b -- sw/firmware/ctrl/aecp/aecp.c` touches only the
  notice fan-out: `address`, the new `source` and `fan_out`), so it is restated by the rule: **120**. A cut would keep the earliest registration deadline
  as registrations change instead of scanning on each arm.
- **The 8x8/1if SRP record and its header constant** (raised at 06:25; RULING-1118b, item 2b, settles it: the unit
  follows its record on the image that carries it). The record (`srp-talker-held`'s
  Listener Ready) is 35,571 cycles at `b5802de9` (375 us) and 35,805 at round 4's tip (380), against a statement of
  365. `load_grade.py --check` refuses a `record.srp` other than `ctrl_loop.h`'s `CTRL_LOOP_SRP_UNIT_US` at the point's
  shape (its `srp_unit` check). The manager's what-if restates `OWN['8x8/1if']['record.srp']` to 380 but runs only
  `flip_grade.py`, so that check does not run. With the real edit, restating the record moves the header constant,
  which ruling item 2 rules out, though ruling item 3 says the record holds "its statement (restated)". The unit is
  not an immediate the measurement can ignore. In `b5802de9`'s run, 49 SRP records start between 1,095 and 1,120 us
  into their 1,475 us slice, which a unit of 380 would defer. So a moved unit needs 8x8/1if measured again, which the
  precedent did too ("every one-interface leg was measured again").
- **Ruling item 3, why the relearned list costs the SRP record.** The three windows are 1x1/1if arm A's (backlog,
  backlog-adp, aecp-largest-notice), and none runs SRP's Listener path. The relearned list therefore leaves cold what
  the pre-relearn 206-entry list (step 9's) kept hot: `memcmp`, `msrp_attr_cmp`, `rx_on_attr`, `parse_pass`, `same`,
  `mrp_attr_registered_ports`, `interested_msrp`, `apply_receive`, `msrp_decode_attr` and `listener`. In round 4's
  trace of this record, 21,396 of its 35,506 cycles ran in cold code. #930 measured the record at 32,936 cycles on the
  older list.
- **Ruling item 3, measured: the relearned list is no worse for the SRP record at any point.** The old list was run on
  B's own code (`b4f9f26c`, a scratch commit of `6448e431` with `082d0037`'s list and link script) in
  `srp-talker-held`, the group holding the SRP record at every point (other groups' records are 21,000 to 23,000
  cycles at 8x8/1if). Cycles, each run's whole group (`results.json`, and its heaviest `srp_mbx:receive` span):

  | Point | SRP record, relearned (B) / old | Its apply, relearned / old | Polls base, relearned / old |
  |---|---:|---:|---:|
  | 1x1/1if | **23,103 (245)** / 23,662 (250) | 22,748 / 23,188 | 19,248 / 18,908 |
  | 8x8/1if | **35,547 (375)** / 36,377 (385) | 35,350 / 36,012 | 28,417 / 27,814 |
  | 8x8/2if | **30,391 (320)** / 30,898 (325) | 30,061 / 30,405 | 27,633 / 27,443 |

  Keeping the SRP receive path hot does not help: in the 4 KiB direct-mapped fetch cache, where code lands outweighs
  whether it is listed. The old list measures better on the polls base, by 190 to 600 cycles. At 8x8/1if that is
  27,814 (295), inside the 28,095 target, but the list is not the ruled procedure's, so it is a measurement, not an
  option.

## Heads

| Head | Branch | What |
|---|---|---|
| `112ab9b1` | `flip-train-1117`, the step-9 branch with the cuts | `ed5855fe` (round 4); the notice cut `067c319d` and its include fix `0bc158a7`; the listener cut `7b3c1c94`; the DMA driver's T8 test `112ab9b1` |
| **`4374cc27`** | `flip-train-1117-p10`, the step-10 candidate (the CPU pass) | rebuilt from `ed5855fe` (round 4's tip kept as `refs/ref/p10-r4`): #944's frozen head `d1aa4c44` merged (`49f005b9`); the idiom fix `082d0037`; the filtered relearn `b5802de9`; the cuts carried and re-traced (`26f30fea`, `3e1c3dd9`, `68c97849`, `08c28218`, `41d2bc2b` = B); T8 (`6448e431`); the ledger (`bf2c1184`); a control re-anchored (`7a536fc5`); B's restatements (`0cfe1ddc`); 8x8/1if's TX 77 and SRP unit 375 (`3cdc613b`); the prose (`0b054867`); a self-test check re-anchored (`c8ff391a`); ADP's restatement (`4374cc27`). From `41d2bc2b`'s cuts on, its 8x8/1if images are U's measured ones and its other images B's |
| **`73272666`** | `flip-train-1117-p11`, step 11 (RULING-1118c), the final head (`05dc1791` plus the record-only re-baseline, RULING-1118f) | #939's frozen `0297a19a` merged on `c8ff391a` (`3e908539`), then `4374cc27` carried (`74481d2e`), then the preflight fix: `plat_mutants.py`'s blank line at the end dropped. Built in a scratch clone and fetched into the lane repo. No re-baseline commit (the STOP at RULING-1118d item 2) |

Nothing is pushed. The scratch variants (`b4f9f26c` old list, `21486e00` N, `dd5f60e0` NU, `40a6c1a5` U, `b1a8424f` U+1)
exist only in their clones.

## The re-grade before measuring (ruling item 4), by real edits

Round 4's figures, restated by the unchanged rule as real edits to `edit_rows.PACED`, `load_grade.OWN`,
`poll_grade.EIGHT_ONE` and `TWO`, and `load_grade.STATED_US` / `STATED_US_DONOR` at 8x8/2if, at `082d0037`.
`flip_grade.py --check` reproduces the ruling's figures: 8x8/1if's load is 0.752 of 0.75 and THE TRANSMIT's row 77.09
against 75 ms; at 8x8/2if a twelfth finding, THE TRANSMIT's row 107.79 against 105 ms; 1x1/1if holds, ACMP's margin
0.07 ms.

| Case (the rest as round 4 measured) | 8x8/1if | 8x8/2if |
|---|---|---|
| polls base 295, the 8x8/2if notice item 305 | FAIL: load 0.752 | twelfth finding (tx 107.79) |
| polls base 295, the notice item kept at 275 | PASS: load 0.746, tx 74.89 of 75 | the eleven only |
| polls base 295, SRP 370 / apply 365, the notice item 305 | PASS | twelfth finding (tx 107.79) |

So attempt 2 needs both: the 8x8/1if polls base measured at 28,095 cycles or less (295 us by the rule), and the
8x8/2if notice item at 26,190 or less (275 us). The 1x1/1if paced record must stay within 310 us (29,523 cycles).

## The final head, `d1aa4c44` merged

#944's frozen head (GitHub head checked) merged `--no-ff` on the rebuilt p10, round 4's resolutions reused
(RESOLUTIONS.md). The size moves of #936's last commit left the union's `run.py` at 1,013 lines; `082d0037` moves
#936's talker-notice plants' verdict into `talker_notice.py`, its body unchanged, so `run.py` is 994 and the idiom
gate passes. At `082d0037`: the four shards PASS (the control campaign 797 of 797), the twin and its plants PASS,
and the quick list PASSES but for the base's eleven 8x8/2if flip findings.

**The hot list, ruling item 1.** Re-traced by the three windows at `082d0037`: 269 functions, the same set as round 4's.
The filter kept every entry whose section links in every split image `ctrl_srp_image.py` holds to the list: the
size fixture at the three points in all six arms, as itself and as the SoC plan's stand-in and mapped images (54
link maps). It drops `aecp owe` and `aecp owed_drain`, which the 8x8/2if images lack in every arm; 267 are kept
(`b5802de9`). The target platform's image links the same script but is not held to it. On the stricter reading
that counts the platform's four images as served, five more would go: the size fixture's own `ctrl_aecp_image`
functions (`source`, `allocation`, `notice`, `a_random`) and `ctrl_loop_run`, none of which the platform links.
That reading was not taken, and it is flagged for the manager.

**At the final head (`b5802de9`), the answering-ports arm** (cycles; by the rule):

| Point | Long record | Paced record | Other record | `aecp` notice item |
|---|---:|---:|---:|---:|
| 1x1/1if | 83,269 (875 of 975) | **29,998 (315 of 305)** | 22,138 (235 of 245) | |
| 8x8/1if | 153,733 (1,615 of 1,715) | 56,826 (600 of 685) | 19,911 (210 of 265) | |
| 8x8/2if | 148,840 (1,565 of 1,650) | 55,926 (590 of 595) | 18,780 (200 of 265) | **28,960 (18 over 27,500)** |

So the final head without attempt 2 cannot pass. The 8x8/2if notice item gives the twelfth finding, and a paced
record at 315 puts the last queued notice at 141.39 of 140 ms (ruling item 2).

## Attempt 2, cut 1: a notice's per-recipient work (`067c319d`, `0bc158a7` on the step-9 branch)

The 8x8/2if notice item (the `aecp:transmit` span, 32 recipients), traced by function in round 4's variant:
`mbx_tx_begin` 3,200 instructions / 10,753 cycles in 33 calls, `fan_out` 2,439 / 10,522, `mbx_tx_commit` 1,223 /
4,840 in 35 calls, `aecp_mbx fan` 320 / 1,024, about 850 cycles a recipient. The cut:

- a buffer's source MAC is stored only when its interface changes (the fan port's two buffers alternate, and each
  keeps its source from one recipient to the next);
- the port's calls and context and the registration's sequence_id are read once (a frame's byte stores could
  alias them, so the compiler reloaded them for every recipient);
- the transmit's commit and the record mover's wait are inline in `mbx_tx_begin` (`CTRL_CC_INLINE` in `ctrl_cc.h`,
  GNU always_inline, plain inline in the portable build), so a transmit calls nothing and saves no registers.

No record, frame or response changes. Three plants were re-anchored to the same defect: `aecp_fan_mutants.py`'s
`notice-source-of-the-first-interface` and `notice-sequence-low-byte-unwritten`, and `poll_items.py`'s `FAN_NOW`,
the walk `notice-fan-out-as-it-was` replaces. Every other anchor of every test module was checked against the
changed files.

| The 8x8/2if notice item, `aecp-fanout`, the same old list | Cycles | Over 27,500 |
|---|---:|---:|
| the final head's code (`082d0037`) | 28,828 | 20 |
| the source and read-once parts alone | 27,852 | 3 |
| **the whole cut** | **25,785** (275 us, the statement exactly) | 0 |

## Attempt 2, cut 2: SRP's delivery tells ACMP only a changed Listener presence (`7b3c1c94`)

The 8x8/1if polls base (the valid-destinations arm's `srp-talker-held`, 29,933 cycles at round 4's tip) traced by
function: 4,861 instructions at CPI 6.2, no function over 2,400 cycles. Its per-source work: MAAP's demand asks
ACMP's `acmp_declaring` for each source every pass, through `memset` and three forwarding `source` callbacks; and
SRP's delivery calls `acmp_listener_registered` for every source every pass. Both entries are in the TSN stack
(changed only through its own review and a pin move). The forwarding callbacks cost 3,114 cycles for 90
instructions (fetch), but ACMP's environment holds one context for every callback, so a hop cannot go without
widening that interface. SRP's delivery can skip the call where ACMP's flag already equals the presence: the call
sets that flag and nothing else (`enter`'s cleared clock cache is cleared by every ACMP entry), so ACMP's state is
the same at every point. That is nine calls a pass at 8x8/1if (252 instructions, 662 cycles in round 4's trace).

## Rejected: the paced record's echo inline

The 1x1/1if paced record (a one-row REMOVE in the answering-ports arm's `aecp-fanout`) is fetch-bound: 3,990
instructions in 29,445 cycles at round 4's tip (CPI 7.4), its `memcpy` echo of one mapping 1,492 cycles for 57
instructions. Echoing one or two mappings by an inline byte loop measured worse on the same list (29,426 cycles
without it, 29,872 with it: 310 and 315 us), the code's placement outweighing the call, so it was not taken.

## Attempt 2's heads, the answering-ports arm (cycles; by the rule against the statement)

| Point | Long record | Paced record | Other record | `aecp` notice item |
|---|---:|---:|---:|---:|
| 1x1/1if, A | 82,292 (865 of 975) | 29,466 (310 of 305; 310 restated) | 21,597 (230 of 245) | 13,492 (of 21,000) |
| 8x8/1if, A | 152,799 (1,605 of 1,715) | 56,486 (595 of 685) | 19,465 (205 of 265) | 13,095 (of 14,500) |
| 8x8/2if, A | 149,525 (1,575 of 1,650) | **56,969 (600 of 595)** | 20,454 (215 of 265) | **25,730 (275 of 275)** |

The re-grade with A's 8x8/2if paced record restated to 600 (and the rest as above) holds: 8x8/1if PASS if its
polls base is 295 or less, and 8x8/2if the eleven findings only.

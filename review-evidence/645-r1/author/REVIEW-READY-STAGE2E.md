[A531] REVIEW READY -- stage 2e

Commit: `4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f`
Branch: `645-ring-slip` (local; not pushed).
Executor [A531]; internal reviewer [R474]; external reviewer [R475].

The [stage-2e ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5994641859) is satisfied: the identical three-directive signoff at dev `fa450d301805881ad713b67521477bf042ddadfd` misses the +0.030 ns margin on AltSpreadLogic_high. The ruled baseline-miss branch therefore permits REVIEW READY. Both baseline and candidate failed grades remain failed; this is not timing closure or proof that the same path failed in both designs.

Changed: `e80dd7ad43574b109b51d4f586efad776d547553` corrects the capture summary from eight to sixteen after the exact old-line search across tracked `tb/**/*.patch` and mutant tables. No patch context depends on it; all five follow-ring and twenty capture-coherence arms still plant. Required clean no-fast-forward merges are `f325c3ab4a9faa0e2b7784e796728ebe6acf3fd3` (dev `510fae60`) and the current head (dev `28f9666f`). All three subjects are one line with no bodies or trailers. No rebase or amendment.

The first merge adopts processor pin `ead8036035affd53ef4b29979190f2f4f67084c0`, so full-system acceptance was rerun. The last merge modifies only `docs/findings/653_DISCONNECT_ORDER_BENCH.md`; all 132 export inputs, test inputs and OOC source bytes are unchanged. The documentation-only binding records why the freshly compiled evidence applies at this head. Live dev was checked again and remains `28f9666feab2b2ba287643c63ed3a16b1e0bb863`.

Timing (ns; each cell is WNS / WHS):

| Measured tree | Directive | Slow | Fast | Margin grade |
|---|---|---:|---:|---|
| Required dev fa450d30 | ExtraPostPlacementOpt | +0.244 / +0.102 | +1.638 / +0.036 | PASS (0) |
| Required dev fa450d30 | AltSpreadLogic_high | +0.026 / +0.049 | +1.478 / +0.014 | FAIL (1) |
| Required dev fa450d30 | ExtraTimingOpt | +0.056 / +0.049 | +1.478 / +0.017 | PASS (0) |
| Current head 4e1ddee9 | ExtraPostPlacementOpt | +0.151 / +0.099 | +1.552 / +0.036 | PASS (0) |
| Current head 4e1ddee9 | AltSpreadLogic_high | +0.101 / +0.097 | +1.385 / +0.033 | PASS (0) |
| Current head 4e1ddee9 | ExtraTimingOpt | -0.209 / +0.062 | +1.420 / +0.030 | FAIL (1) |

The former candidate that triggered the ruling (b2c81239, also applicable to its comment-only child e80dd7ad) is retained separately:

| Directive | Slow WNS / WHS | Fast WNS / WHS | Margin grade |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.120 / +0.053 | +1.633 / +0.019 | PASS (0) |
| AltSpreadLogic_high | +0.142 / +0.065 | +1.483 / +0.026 | PASS (0) |
| ExtraTimingOpt | +0.001 / +0.001 | +1.476 / +0.012 | FAIL (1) |

All six fresh implementation processes and rejected-constraint checks return 0. Base TNS/THS are zero. Current ExtraTimingOpt has Slow TNS -0.294 ns at two failing setup endpoints, THS zero, and Fast TNS/THS zero; all other current TNS/THS values are zero. Its critical-warning census contains one `Route 35-39` timing diagnostic; the other five fresh runs have none. Both fixed timing models are reported at 0 and 85 C power settings, which do not create four independent timing models.

The same shipping 1x1 recipe, part, 32 threads and default seed were used, sequentially under the shared lock; each tree's alternatives reuse its own fresh synthesis checkpoint. No bitstream was generated. The required base used a separate detached scratch worktree; the lane checkout was never switched.

The failing baseline minimum is SDRAM `zqcs_timer_count1_reg[26]` to `bankmachine0_level_reg[1]` (16 levels, 9.699 ns). The old candidate minimum was receive-validator `hdr_src_mac_r_reg[0]` to the transmit-arbiter FSM (39 levels, 19.728 ns). The current minimum is notification `wr_ix_r_reg[0]_replica_4` to transmit-arbiter `slot_r_reg[0]/D` (42 levels, 20.130 ns). For the manager-owned timing follow-up, current worst-five slack values are -0.209, -0.085, +0.073, +0.229 and +0.265 ns. Full source/destination paths, logic levels, report line numbers and raw-report hashes are retained in HANDOFF.md and the per-directive extracts.

Area acceptance: fresh vendor OOC synthesis measures recentre 41/51 -> 67/92 LUT/FF and complete capture 1076/1336 -> 1130/1368, totaling **+80 LUT / +73 FF**. Capture retains one block RAM tile. Fresh routed own-logic attribution is **112 LUT / 73 FF**, below 120/120. It counts the full new cone plus the capture delta, excluding only identical direct functions and ten shared functions proved equal over all 65,536 signed-error assignments. The planted truth-table control is caught. Four OOC runs, both routed queries, proof, area limit and final 132-input verification all return 0. Whole-design changes from the required processor adoption are reported separately from this lane's own logic.

Validation at the merged inputs, all listed functional commands rc 0:

- Full datapath: 11,877 checks / 0 failures.
- Render: 259 shipping + 65 multistream + 5 stimulus controls.
- Media-clock: 55 + 32 + 50 positive checks + 31 controls.
- Processor integration: 646 + 606 + 606 + 311 checks.
- Capture coherence: 332 datapath + 20,832 core + 30 controls.
- Physical: 143 normal + 40 accounting + 14 ordering controls = **197 checks / 0 failures**. The normal leg runs 16.992556520 simulated seconds, with 6,517,344 payload, 814,666 ordering and 135,936 sequence comparisons.
- Pull-in: 18 phases, zero slips during/after; 17 fully gradable render cases. Phase +1042 is NOT GRADABLE after settle because the boundary is four cycles from a PDU end.
- Boundary: 81/81 checks; 123 positive, 246 correctly rejected and 195 NOT GRADABLE windows. The five-cycle allowance and nine-cycle ambiguity are unchanged.
- Portability: 55/55 tops. Builder with required RV32 and elaboration: rc 0; its historical Arty area-calibration arm remains NOT RUN because its reference report is absent.
- Source/documentation: 26/26 commands rc 0, lint 90 <= 90. Source-list and wire-truth self-tests pass.
- Vendor parser: rc 0, 125 files, zero hdl/ findings and two existing processor diagnostics matching the ratchet (`cancel_hit_w` at `KL_pp_originator.sv:194`, `vd_push_w` at `KL_pp_rx_validator.sv:383`). Analysis does not establish elaboration.

At startup and reset, the fresh physical run independently declares and observes step -5 events at output PDUs 6047 and 92220, respectively. Both slip counters remain 0 -> 0. Both decisions complete; plan, span, payload, order, sequence and counter error totals are zero. The two controls reject an undeclared repeat outside the decision PDU and a step larger than declared. All original checks remain.

The four arrival campaigns, INTERNAL cases and five controls remain applicable through the recorded source-identity proof (all twenty standalone inputs unchanged except the summary comment; that model does not instantiate the processor):

| Arrival envelope | Runs / decisions | Post-decision slips | Min empty / full margin (ticks) |
|---|---:|---:|---:|
| None | 16 / 48 | 0 | 4.984320 / 5.076480 |
| Uniform 0..5 us | 16 / 48 | 0 | 4.899840 / 4.907520 |
| Uniform 0..2 us plus 1e-4 tail to 24 us | 16 / 48 | 0 | 3.893760 / 5.091840 |
| Uniform 0..60 us | 16 / 48 | 0 | 2.565120 / 2.234880 |
| INTERNAL holds 52 and 56 us | 32 / 32 | 0 | 4.984320 / 5.091840 |

Phases k/16, seeds 645+k, uncompressed 512 ms windows; first hold 40 s, both following switches 20 s each. Late-arrival campaigns grade slips/margins, not the render law. The no-lateness case has 45 on-law and three ungradable observations; INTERNAL has 27 fully gradable pairs, two BEFORE and three AFTER ungradable observations. NO-SETTLE, RENDER-ONLY, EARLY, W1 and OVERSHOOT17 are caught.

Reproduction entry points (external staging and pinned simulator as recorded in HANDOFF.md; every applicable campaign has its jobs option):

```sh
make -j16 -C "$BROAD/tb/verilator/milan_dp" VERILATOR_JOBS=2 SIM_JOBS=2
make -j16 -C "$BROAD/tb/verilator/milan_dp_render" VERILATOR_JOBS=2
make -j16 -C "$BROAD/tb/verilator/milan_dp_mclk" VERILATOR_JOBS=2
make -j16 -C "$BROAD/tb/verilator/pp_shadow" VERILATOR_JOBS=2
make -j16 -C "$PHYSICAL/tb/verilator/milan_dp" ax1x1gptp-build VERILATOR_JOBS=3
(cd "$PHYSICAL/tb/verilator/milan_dp" && ./obj_ax1x1gptp/Vmilan_dp_ax1x1gptp)
(cd "$PHYSICAL/tb/verilator/milan_dp_gptp" && python3 -B verify_abort.py)
(cd "$PHYSICAL/tb/verilator/milan_dp_gptp" && python3 -B verify_recentres.py --jobs 2)
make -j16 -C "$FOCUSED/tb/verilator/milan_dp_render" tdm8render-pullin PULLIN_JOBS=8 VERILATOR_JOBS=2
(cd "$FOCUSED/tb/verilator/milan_dp_render" && python3 -B tdm8_render_mutants.py --law-boundary --jobs 4)
python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration
bash syn/yosys/run.sh
flock $VIVADO_LOCK python3 -B scripts/xvlog_gate.py --check
```

HANDOFF.md contains the classification, every fix option's area/protocol effect/test plan, exact campaign commands, traces, current timing and area tables, source binding, setup attempts and limits. PR-BODY.md follows the repository template and contains the requested closure lines except the bench items. `stage2e/merged/REPRODUCE.md`, command manifests and 314 artifact receipts locate the full evidence; 342 retained-file hashes were checked. Large originals, builds and dependencies remain outside the output directory; no output file exceeds 200,000 bytes. The lane, all three initialized submodules and the baseline scratch worktree are clean, including ignored files. Run-owned generated links were removed after target verification.

Acceptance criteria: the stage-2e author acceptance is met under the recorded rulings. Recommendation: retain option C and hand this head to independent review. Its depth-16 / PDU-end-11 loopback adds 62.5 us over target eight; the AAF presentation law is unchanged, and the startup/reset/source-change recentre is a declared bounded discontinuity.

Open limits: the four historical full render-mutation failures remain assigned to #657. Bench/physical-compliance items remain with the manager; licensed ACMP/SRP streaming, physical TDM render, CRF recovery, multiple-responder cease, PHY/MAC calibration and CPU/DDR are not established by these desk tests. The original first-10-ms warm-up exclusion remains. No independent approval, hosted result, merge-result validation or post-merge containment is claimed. No push, PR publication, hardware operation or merge into dev was performed.

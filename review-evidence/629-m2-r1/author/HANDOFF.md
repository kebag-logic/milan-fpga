# HANDOFF: [A491], lane M2 for #629 (implementation of the media-clock following design)

Status: STOP (condition 4: named design statements below), posted https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5946475441 at head `57f4b742b504f5e69293aaa3e00d0470aa9b6071`; every item implemented and committed, every gate green at the head

- Branch: `629-media-clock-impl`, from dev `cdf49d1a28527562888f0a903de51b6b15b1244f`
- Worktree: `$LANES/629-m2-impl`
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5942692103
- Design: `docs/design/MEDIA_CLOCK_FOLLOWING.md` (merged by PR #631)

## Setup

- `git remote get-url origin`: `https://github.com/kebag-logic/milan-fpga.git`
- HEAD at start: `cdf49d1a28527562888f0a903de51b6b15b1244f`
- Submodules at recorded gitlinks: `third_party/verilog-axis` `48ff7a7e`, `gptp-processor` `5dce647a`, `protocol-processor` `b2db3a97` (each `rev-parse --show-toplevel` is its own directory)

## Items

1. Requirements: done, commit `baa0a8a1`. `docs/reference/FR_NFR.md` FR-CLK-03 and FR-CLK-04 rows and the FR-CLK-03/04 status row (the in-tree #389 record) amended to the owner decision, citing the design.
2. Model and builder: done, commit `0b074298`. `input_stream` accepted; `_overlay_clock_sources` emits D1 class order; shape header gains `AEM_CLKSRC_{INTERNAL,CRF,AAF}_C`, `AEM_CLKSRC_KIND_C`, `AEM_CLKSRC_SI_C`, `AEM_N_AAF_CLKSRC_C`; `names.clock_sources.stream`; all five configs regenerated (builder per config, `--write-rtl` for ax7101_1x1_tdm8, `avdecc/gen_aem_store.py`, `scripts/check_nvm_record_space.py --emit-record-table` for the two NVM tables); arty_current pin `...0005` -> `...0006`; `scripts/nvm_map_checks.py` 1x1 image digest re-pinned (one NAME record more).
   - Finding (design statement, test plan): "a listener-only shape without INTERNAL (CRF at 0)" is not buildable: the loader refuses a config with no talker. The rule is graded at `_overlay_clock_sources` directly.
   - `clock_source_flags` decided: value 0x0002 kept, label corrected to LOCAL_ID (IEEE 1722.1-2021 Table 7-16).
3. Fabric: committed `d676ecfd`.
   - `hdl/ieee1722/crf/KL_aaf_clock_meter.sv` (new): the AAF clock meter (D2 = M1, 48 kHz Base format with `stream_data_length` = 24 x channels, group-of-16 mean, 4,096 ns jump bound and in-group void, rule (b) with the k = 2 check at 5,120 ns and the midpoint fill, E8 8-entry snapshot ring, lock 8 in / 100 ms out, era rules, `disrupt_p` only on its own timeout, silent `mr` seed, status word).
   - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`: one-bit `sel_i`; `ref_locked_i`, `ref_rate_valid_i`, `ref_rate_ns_i`; new `locked_o` (state == LOCKED). State machine and arithmetic unchanged.
   - `hdl/milan/milan_datapath.sv`: `media_clk_resolve` decodes through `AEM_CLKSRC_KIND_C` / `AEM_CLKSRC_SI_C` (`crf_clk_selected_r` text kept); meter instance on the parser bundle (`tu` from `avtprx_tu_bit`); reference mux with W2's one-cycle unlocked presentation (`ref_src_chg_w`); `mcr_restart_p_w` gains the meter's two pulses and a `public_flat_rd` tap; C1 counter level `~tu & (~follow_sel_r | mcsrv_locked_w)`; A2-a `mga_sel_w = int_clk_selected_r | follow_sel_r` for the aligner and NCO; #386 settle and I2S `servo_en_i` on `follow_sel_r`; stale comments fixed.
   - `hdl/common/csr/milan_csr.sv`: `A_AAFM_STAT` 0x8E0, `A_AAFM_RATE` 0x8E4 (RO live, read-window terms); VERSION 0x0002_0061.
   - Source lists: `sw/litex/milan_soc.py`, `syn/yosys/run.sh`, `syn/yosys/ooc.sh`, `tb/verilator/milan_dp/Makefile`.
4. Tests: in progress.
   - VERSION: kept at `0x0002_0060` (commit `b5d9e705`), following the recorded practice of the #443 ruling ("VERSION is unchanged; the release step owns the minor bump"), with an `Unreleased` CHANGELOG entry and the register-map note. The design's Registers row says "VERSION moves": a named design statement, flagged for a decision (see Open questions).
   - `tb/verilator/csr/sim_main.cpp`: 0x8E0 was pinned unmapped; it now grades both words read through, ignore writes, and 0x8E8 unmapped.
   - `tb/verilator/milan_dp/sim_nxn.cpp`: [AECP-MODEL] set walk to #629's class order; new [CLKSRC-WALK] (every listed index accepted, read back, decoded as its class, the meter following the listener); [CLKSRC-RANGE] keeps count and 0xFFFF refused (NSTREAMS + 1 is now AAF listener N-1's source); [CRF-SEL] grades follow_sel_r with the NCO gate engaged at both ends (A2-a); 0x0041 grid wiring gate = int | follow; T67 holds the 1:1 audio clock so the aligner's dead-feed watchdog disengages it (the leg's audio clock is a harness artifact).
   - `tb/verilator/milan_dp/sim_main.cpp` [SERVO]: NCO aligned at INTERNAL, follow_sel 0.
   - `tb/verilator/milan_dp/gmstep_mutants.py`: the restart anchors moved past the meter's terms (two controls had stopped planting).
   - `tb/verilator/milan_dp_render/sim_tdm8_render.cpp` (A2-a pins): T30's INTERNAL window must not walk at the plan's rate and costs no counted skip or underrun; T31 back at INTERNAL grades the settled walk (under 5 ppm; one cycle is 2 ppm in that 5 ms window) and the engaged loop; T14 opens its commit record one PDU before the decoder re-arms; `--crf-only` dwells 0.3 s at INTERNAL for the boot pull-in before its CRF phase (a CRF selection keeps the engaged aligner, so the #386 settle waits for the pull, bounded by its 32768-tick ceiling); the INTERNAL-select leg defect is graded at the resolve.
   - `sw/builder/test_builder.py`: the media restart contract pins #629's request, `(crf_clk_selected_r & ...) | aafm_disrupt_p_w | aafm_mr_toggle_p_w`, with its two mutants re-anchored.
   - Root rows: `tb/verilator/milan_dp_mclk` (new suite, legs A, B, C; 14 named mutants as schemata).
   - Meter rows M1 to M14: `tb/verilator/aaf_clock_meter` (`sim_main.cpp`), 308 checks; 22 named mutants killed (`mutants.py`).
   - Servo row S1 (W2 switch with the select held): `tb/verilator/mmcm_servo/sim_main.cpp` [U16]; mutant W1 killed.
   - Servo-with-meter row S2: `tb/verilator/aaf_clock_meter/sim_servo.cpp` (180 s, silicon loop; worst |e| 717 / 717 / 724 ns; mean trim +30.619 -> +34.631 ppm for the 4 ppm step); mutants E1, restart on any loss, held lock cleared on a gap killed.
   - Existing pins of the INTERNAL free run updated in `tb/verilator/milan_dp/sim_aclk.cpp` (A2-a).
5. Area and timing: area below (Yosys OOC); timing of the shipping AX7101 image below.
6. Limits: the owner's oscillator-grade risk is recorded where a reader of the product limits looks:
   - `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 7.4 row: KNOWN RISK, plan A 10.64 ppm under nominal, so INTERNAL meets Milan v1.2 7.4's +/-50 ppm only for an oscillator grade of +/-39 ppm or better (+/-49 ppm on plan B); the grade is unmarked, assumed adequate by the owner's decision (#629 comment 5937848189), unconfirmed.
   - `docs/design/TIME_SYNC.md` Media boundary: the same, in the page's short-sentence form.
   - `CHANGELOG.md` Unreleased entry: KNOWN RISK lines.
   - `hdl/milan/milan_datapath.sv` A2-a banner (from commit `d676ecfd`): the same statement beside the gate.
   - The design page's Limits already carried it; its Implementation notes list the named deviations.

## Named design statements (STOP condition 4) and open questions

Each design statement below did not hold as written in implementation. The lane implemented the nearest faithful equivalent, recorded it in the design page's Implementation notes, and stops for a ruling:

1. Registers row: "VERSION moves". VERSION stays `0x0002_0060`, following the recorded #443 practice (the release step owns the minor bump; `Unreleased` CHANGELOG entry). Decision needed: keep, or step to `0x0002_0061` with its documentation cascade.
2. Builder row: "a listener-only shape without INTERNAL (CRF at 0)". The loader refuses a configuration with no talker, so the shape cannot be built; the rule is graded at `_overlay_clock_sources` directly (gate 33).
3. AECP model walk: "the servo leaves IDLE for every stream source". The servo leaves IDLE only with a locked reference (`KL_mmcm_drp_servo` IDLE, unchanged), and the walk streams nothing; `[CLKSRC-WALK]` grades acceptance, readback, the decode, the servo's select and the meter's status word instead. The row's named mutant (a stale decode table) is planted in the root suite (id 14).
4. Counter row: "60 s with one PDU lost in every 0.3 s". At the root 60 s costs about 20 minutes, past the 1800 s suite guard; the root loss leg is 3 s (its mutant fails at the first lost PDU), and the 60 s leg with the meter in front of the servo runs in the meter suite (S2).
5. Counter row at the root needs `tu` valid: the ownerless elaboration holds `tu` at 1 structurally, so the root suite substitutes a test double of `KL_ptp_clock_validity` (that suite only).
6. Switch row: "one #386 recentre" per switch at every phase. At the root suite's 4 MHz clock the settle band (1/64 sample) is one cycle, so a settle can take its 32768-tick ceiling (683 ms); one recentre per switch kind is graded over 0.8 s gaps, and the 16-phase sweep grades that none is queued. Related, at any clock: under A2-a a CRF selection keeps the engaged aligner, so a selection during the boot pull-in waits for that pull before the recentre (bounded by the same ceiling); the render leg's `--crf-only` now dwells 0.3 s.
7. Servo-with-meter row: suite `tb/verilator/mmcm_servo`. It runs in `tb/verilator/aaf_clock_meter` (`sim_servo.cpp`), beside the meter build; `mmcm_servo`'s default target is already near its guard (#545).
8. Area: the meter's 270 to 420 FF estimate. 636 FF out of context (630 placed); LUT inside the estimate. The pipelines register their 32-bit operands.

Open risk recorded: INTERNAL accuracy under A2-a rests on the board-oscillator grade (owner's known risk). Parent-visible: the shipping image's slice occupancy is 99.98 %.

## Test rows and failing mutants

Every row of the design's test plan (docs/design/MEDIA_CLOCK_FOLLOWING.md, Test plan / Simulation), where it is graded, and the named mutant that must fail it. Verdicts: see the Gates table (mutant campaigns' own tallies).

| # | Design row | Graded in | Named mutant (runner, id) |
|---|---|---|---|
| M1 | rates at 0, +/-10.64, +/-50, +/-100 ppm vs KL_crf_rx within 1 LSB | `tb/verilator/aaf_clock_meter` `rates` | decimation by 1 (`aaf_clock_meter/mutants.py`) |
| M2 | timestamp error shapes at the design point, 120 s, pinned seed | `aaf_clock_meter` `shapes` | E1 rate over 512 ms; bound 2,048 ns (B1); first-PDU pick (P1) |
| M3 | beyond the tolerance; one- and half-sample steps at 16 positions | `aaf_clock_meter` `beyond` | bound 16,384 ns (B3); within-group void removed |
| M4 | format: 6 samples accepted, 12/8 samples, sparse, 96 kHz, INT_24 refused | `aaf_clock_meter` `format` | stream_data_length check removed |
| M5 | sequence wrap, 10 s | `aaf_clock_meter` `wrap` | continuity without the 8-bit wrap |
| M6 | lock and unlock | `aaf_clock_meter` `lock` | timeout disabled |
| M7 | history restarts (tu edge, selection change, entry, bind, ts wrap) | `aaf_clock_meter` `restarts` | no restart on the tu edge; tu from the tv net |
| M8 | periodic single-PDU loss, 120 s x 4 | `aaf_clock_meter` `loss_periodic` | restart on any loss |
| M9 | a loss in a snapshot group | `aaf_clock_meter` `loss_snapshot` | snapshot from the next pick less 2 ms; voided snapshot restarting |
| M10 | the gap bound | `aaf_clock_meter` `bound` | gap of more than one voided group accepted |
| M11 | the gap bound's value (a)/(b) | `aaf_clock_meter` `gap_value` | bound at 4,096 ns; bound scaled with k |
| M12 | a step inside a loss-voided group | `aaf_clock_meter` `step_in_gap` | no check across a gap |
| M13 | selection (other listener, subtype, tv, STOPPED) | `aaf_clock_meter` `selection` | listener compare ignored |
| M14 | the meter's pulses | `aaf_clock_meter` `pulses` | no re-seed at an era start; era-start clear on disrupt_p; disrupt_p tied low; enable tied high |
| S1 | servo: one-bit select, switch with the select held | `tb/verilator/mmcm_servo` [U16] | switch through IDLE (W1) |
| S2 | servo with the meter in front, 180 s | `aaf_clock_meter/sim_servo.cpp` | E1; restart on any loss; held lock cleared on a gap |
| R1 | true ratio: INTERNAL, AAF, CRF in turn within 0.5 ppm; A2-a at INTERNAL | `tb/verilator/milan_dp_mclk` legs A, B | decode CRF-only (id 1); ref mux stuck on KL_crf_rx (id 2); aligner disengaged at INTERNAL (id 3) |
| R2 | W2 at the root | `milan_dp_mclk` leg A [W2] | one-cycle unlocked presentation removed (id 4) |
| R3 | switches (i) 16 phases, (ii) silent talker, (iii) INTERNAL dwell | `milan_dp_mclk` leg B | no re-seed (id 5); raw lock-fall as disruption (id 6); enable tied high (id 7) |
| R4 | lock loss of AAF and CRF, return | `milan_dp_mclk` legs A, B | disrupt_p not ORed (id 8) |
| R5 | echo | `milan_dp_mclk` leg A [ECHO] | echo ungated (id 9) |
| R6 | CLOCK_DOMAIN counters C1 | `milan_dp_mclk` legs A, B | C0's level (id 10); C2's level (id 11); held lock cleared on a gap (id 12) |
| R7 | CSR words | `milan_dp_mclk` leg A [CSR]; `tb/verilator/csr` | read-window terms missing (id 13) |
| R8 | AECP model walk | `tb/verilator/milan_dp` sim_nxn [AECP-MODEL] + [CLKSRC-WALK] (4 shapes) | decode table one source short (milan_dp_mclk id 14) |
| B1 | builder: input_stream, class order, servo prune refusal, tables, model id | `sw/builder/test_builder.py` gates 33, 15, 23b, 28 | L2-order overlay (gate 33 bite) |

## Area against the design estimate

`syn/yosys/ooc.sh KL_aaf_clock_meter KL_mmcm_drp_servo` (synth_xilinx -family xc7 -flatten, a Yosys estimate, not a placement), at the branch head:

| Block | LUT (of which LUTRAM) | FF | RAMB18 | DSP | CARRY4 | Design estimate | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| `KL_aaf_clock_meter` (E8) | 574 (16) | 636 | 0 | 0 | 102 | 380 to 580 LUT, 270 to 420 FF, 0 RAMB18 | LUT inside; FF 216 over the top of the range: the three-stage per-PDU pipeline and the six-stage group-end sequence register their 32-bit operands (S1/S2 timestamp and deviation, pick, spacing, midpoint, snapshot pair, rate difference). Named as a design-statement deviation. The E8 ring is LUTRAM (16), no RAMB18 |
| `KL_mmcm_drp_servo` | 865 | 792 | 0 | 1 | 150 | 871 LUT, 792 FF at the design base; "Servo select about -10 LUT" | -6 LUT, FF unchanged |
| Decode table, reference mux, A2-a, C1 | (in `milan_datapath`) | | | | | 50 to 80 LUT, 20 to 40 FF; under 5 each for A2-a and C1 | measured in the placed image (see Timing) |

The meter's DSP was removed by the shift-add `sdl_for` (commit `0d00ad75`): Yosys ignores `use_dsp`, and the 24 x channels product mapped to a DSP48.

## Timing of the shipping image

Built through the repository's build path, `TAG=a491m2dfa8f360 sw/litex/build.sh ax7101` (one heavy build; Vivado v2026.1; synth AreaOptimized_high, opt ExploreArea, place ExtraPostPlacementOpt, route AggressiveExplore; design argv from `sw/builder/out/endstation_ax7101_1x1_tdm8/soc_params.json`), at `dfa8f360`. Every later commit leaves `hdl/`, `sw/litex/`, `syn/` and `configs/` unchanged (`git diff dfa8f360 HEAD -- hdl sw/litex syn configs` is empty), so the image is the head's.

| Metric | This image | Baseline (dev `ec0cc0c1`, same recipe, 60 commits before the base) |
|---|---|---|
| WNS / TNS | +0.107 ns / 0.000 (0 of 180,768 endpoints failing) | +0.109 ns / 0.000 |
| WHS / THS | +0.014 ns / 0.000 (0 of 180,687 failing) | +0.036 ns / 0.000 |
| WPWS / TPWS | +0.264 ns / 0.000 | +0.264 ns / 0.000 |
| CRITICAL WARNING in `gateware/vivado.log` | 0 (one grep hit is the IOB-pack Tcl source echo, `##` line) | 0 (the same echo) |
| #607 constraint refusal | "no 12-4739, 20-1307 or 12-5201 diagnostics"; bitstream not quarantined | clean |
| Slice LUTs | 51,087 (80.58 %) | 48,798 (76.97 %) |
| Slice Registers | 59,522 (46.94 %) | 58,268 (45.95 %) |
| Slices | 15,847 of 15,850 (99.98 %) | 15,734 (99.27 %) |
| Block RAM Tile | 92.5 (68.52 %) | 92.5 |
| DSPs | 14 | 11 (the +3 are in `pp_shadow/u_nvm`, `KL_nvm_backend`, from commits before the base) |
| `milan_datapath` | 42,272 LUT, 48,317 FF | 40,258 LUT, 47,067 FF |
| `KL_aaf_clock_meter` (placed) | 481 LUT (449 logic, 32 LUTRAM), 630 FF, 0 RAMB, 0 DSP | absent |
| `KL_mmcm_drp_servo` (placed) | 898 LUT, 814 FF (own logic 791 / 770) | 898, 814 (793 / 770) |

Bitstream `alinx_ax7101.bit`: 3,825,992 B, sha256 `3218143c337220062757a909be8bc8e79313ea47e38aa69fbe673451bfa052f3` (not copied here). The image meets timing with no new critical warning. Parent-visible risk: slice occupancy is 99.98 %, up from 99.27 %; the LUT delta against the old baseline mixes #629 with the 60 commits between `ec0cc0c1` and the base, and only the meter's own row isolates #629.

## Gates

All commands run from the worktree at its physical `/data` path, unpiped, logs kept locally; pinned Verilator 5.050; Markdown gates with the pinned md venv. "Head" is the commit the run read.

| Gate | Command | Head | Result |
|---|---|---|---|
| Every suite | `scripts/run_all_suites.sh <outdir> --shard I/5`, all five shards in turn (one sweep at a time; the unsharded sweep exceeds one background run's two hours) | shard 1 at `5609ab07`; shards 2, 3 at `97bede46`; shards 4, 0 at `f6eb80e9` (later commits touch no suite source but the render leg, re-run in shard 0) | 59 of 59 suites PASS, 2,148,251 checks, 0 in-suite failures, none timed out: s0 11/11 (401,934), s1 23/23 (196,276), s2 12/12 (1,523,553), s3 12/12 (14,649), s4 1/1 milan_dp (11,839, 1810 s) |
| Root suite (with its campaign) | `make -C tb/verilator/milan_dp_mclk` | `bc3c43a5` | rc 0: legs A 50/0, C 32/0, B 44/0; 10 controls pass; 14/14 mutants caught; 426 s |
| Meter suite (with its campaign) | `make -C tb/verilator/aaf_clock_meter` | `0d00ad75` (meter unchanged since) | rc 0: 308/0 and 6/0; mutants 27/27 as required; 701 s |
| milan_dp | `make -C tb/verilator/milan_dp` | working tree of `94e71891` | pool rc 0 (sim_main 236/0, notify 383/0, crflic 416/0, nxn 1961/0, nxndv 1961/0, nxn8 3746/0, nxn4c, nolpf, prune, ax1x1, aclk 193/0); render_mutants 6/6; gmstep_mutants 6/6 re-run after the anchor fix |
| CSR bench | `make -C tb/verilator/csr` | working tree of `b5d9e705` | rc 0 (408/0, 121/0, 44/0 ...) |
| Builder test | `python3 sw/builder/test_builder.py` | `5609ab07` (no later builder or RTL change) | rc 0: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs an Arty `milanfinal48` build tree on disk; environmental) |
| Entity shape | `python3 scripts/check_entity_shape.py`; `--self-test` | `57f4b742` | 166/0; 219/0 (after classifying the root suite's builder-written header, commit `57f4b742`) |
| Lint ratchet | `python3 scripts/lint_rtl.py --check`; `--check --self-test` | `dfa8f360` | PASS, 90 <= 90 |
| Idiom gates | `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sv_idiom.py`, `check_sh_idiom.py` | `dfa8f360` | rc 0 each |
| Test evidence | `python3 scripts/measure_test_evidence.py --check` | `dfa8f360` | rc 0 (two new dispositions) |
| Docs gates (re-run at `f6eb80e9`, all rc 0) | docs_check, check_em_dash (`--base` merge-base, `--selftest`), check_doc_style (+selftest), check_gptp_docs (+selftest, `--with-submodule`), DOC_MAP, timesync_chain, check_solution_docs, submodule_boundaries, check_submodule_docs, check_diagram_pngs, check_feature_status `--self-test`, gen_module_matrix `--check`, measure_control_flow/measure_cohesion `--selftest`, check_baremetal_only, gen_toc `--check`/`--verify-anchors`, check_doc_paths | `dfa8f360` | rc 0 each |
| Yosys portability | `syn/yosys/run.sh` | `dfa8f360` | rc 0 (TAP-PURITY PASS), 793 s |
| OOC area | `syn/yosys/ooc.sh KL_aaf_clock_meter KL_mmcm_drp_servo` | `0d00ad75` | see Area |
| Light CI self-tests | pp_srcs `--check --selftest`, ci_scope, dp_srcs, ooc_selftest, cache_selftest, check_nvm_record_space, suite_shards `--selftest` | `dfa8f360` | rc 0 each |
| Shards | `scripts/run_all_suites.sh --shard I/5 --list` | `dfa8f360` | `aaf_clock_meter` and `milan_dp_mclk` land in shard 2/5; `milan_dp` alone in 4/5 |
| Shipping image | `sw/litex/build.sh ax7101` (TAG a491m2dfa8f360) | `dfa8f360` (no later change to hdl, sw/litex, syn or configs) | WNS +0.107 ns, WHS +0.014 ns, 0 failing endpoints, 0 critical warnings, #607 refusal clean, bitstream written |

## Parent-visible changes

Repository paths at the branch head; clause in brackets.

- Requirements: `docs/reference/FR_NFR.md` FR-CLK-03, FR-CLK-04 and their status row (the in-tree #389 record) to the owner decision [Milan v1.2 5.3.3.6 as a minimum; IEEE 1722.1-2021 7.2.32 and Table 7-141 for the refusal; 7.4.23.1 for the carried index].
- Configuration: the five `configs/endstation_*.yaml` declare `input_stream`; `names.clock_sources.stream` (schema 1.2).
- Builder: `sw/builder/endstation_builder.py` admits `input_stream`, emits the D1 class order, names the per-listener sources, and writes `AEM_CLKSRC_{INTERNAL,CRF,AAF}_C`, `AEM_CLKSRC_KIND_C`, `AEM_CLKSRC_SI_C`, `AEM_N_AAF_CLKSRC_C` into the shape header; the servo-prune gate refuses an `input_stream`-only offer (test case added).
- Entity model: `avdecc/aem_specs.py` `CS_TYPE` gains `input_stream` 0x0002, `CS_RETIRED` empties; `avdecc/aem_descriptors.py` `clock_source_table`; `aem_assemble.py`, `aem_emit.py`, `gen_aem_store.py` carry `CLKSRC_TABLE`; `clock_source_flags` 0x0002 relabelled LOCAL_ID [IEEE 1722.1-2021 Table 7-16]; every image's `entity_model_id` moves [6.2.2.8]; `scripts/nvm_map_checks.py` 1x1 digest re-pinned.
- Generated (by the generators only): five shape headers, `hdl/common/gen/adp_shape_defaults.svh`, `avdecc/aem_rom.json`, two NVM record tables, `docs/traceability/MODULE_MATRIX.md` and the `README-tests.md` pages.
- RTL new: `hdl/ieee1722/crf/KL_aaf_clock_meter.sv` [IEEE 1722-2016 4.3.2, 4.4.4.3, 4.4.4.5, 4.4.4.6, 4.4.4.7, 7.2.4, 7.3.3, 7.3.5, 10.8; Milan v1.2 6.2, 7.3.2].
- RTL changed: `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` ports (`sel_i`, `ref_*`, `locked_o`; behaviour unchanged); `hdl/milan/milan_datapath.sv` decode, meter, W2 reference mux, restart request, C1 level, A2-a, #386 settle and I2S servo enable on the follow select, public taps (`mcr_restart_p_w`, `ref_locked_w`, `aafm_stat_w`, `aaf_follow_idx_r`, `ctr_mlock_r`, `ctr_munlock_r`); `hdl/common/csr/milan_csr.sv` `AAFM_STAT` 0x8E0, `AAFM_RATE` 0x8E4 (RO live, read-window terms); comments in `KL_media_grid_align.sv`, `KL_media_nco.sv`.
- No top-level port, pin, SoC change or root parameter; no processor-boundary port change; no protocol-processor change (STOP condition not reached).
- VERSION: unchanged `0x0002_0060` (design said "moves"; see Open questions).
- Source lists: `sw/litex/milan_soc.py`, `syn/yosys/run.sh`, `syn/yosys/ooc.sh`, `tb/verilator/milan_dp/Makefile`.
- Tests new: `tb/verilator/aaf_clock_meter` (meter rows, servo-with-meter, 26 mutants), `tb/verilator/milan_dp_mclk` (root rows, 14 mutants as schemata, a `KL_ptp_clock_validity` test double in that suite only).
- Tests changed: `tb/verilator/mmcm_servo` [U16] and renames; `mmcm_servo/mmcm_model.h` (configurable PSDONE latency, default unchanged); `mmcm_servo_autorepair`; `crf_rx` wrappers and mutant anchor; `csr` (0x8E0/0x8E4 graded); `milan_dp` sim_main [SERVO], sim_nxn ([AECP-MODEL], [CLKSRC-WALK], [CLKSRC-RANGE], [CRF-SEL], 0x0041 grid, T67), sim_aclk (A2-a), gmstep_mutants anchors; `sw/builder/test_builder.py` gates 33, 15, 23b and pins.
- Gate tables: `scripts/naming.budget` (one fewer), `scripts/measure_test_evidence.py` (two mutant-driver dispositions).
- Docs: CHANGELOG (Unreleased entry, release note on saved state, KNOWN RISK); REGISTER_MAP (0x8E0 section, 0x8F8 banner, SLIP text); REGISTER_MAP_CLASSES; feature ledger (`aaf.media-clock-following` added, `crf.media-clock-consumption` summary) and its three rows; MILAN_COMPLIANCE_MATRIX (5.4.2.15/.16, 5.3.11.1, 7.2.2, 7.2.3, 7.4, 4.4.4.3, new 4.3.5/10.8 row); PP_DESCRIPTOR_OWNERSHIP L6; TIME_SYNC media boundary; GM_LOSS_RECOVERY; FPGA_DESIGN; ARCHITECTURE; CHANNEL_MAP_64; TESTING (two suites); ENDSTATION_BUILDER rows 9, 9a, 11 and counts; README-parameters; the design page status and Implementation notes; suite READMEs.

## Commits

Head: `57f4b742b504f5e69293aaa3e00d0470aa9b6071` (17 commits on `cdf49d1a`; nothing pushed).

```
57f4b742b Classify the root suite's builder-written shape header in the consumer inventory
f6eb80e9a Point the servo-with-meter deviation at its TESTING row and record the root suite's measured time
93d036cfd State the render lane's aligned INTERNAL window in TESTING and the time-sync render-path row
97bede46a Grade the render lane's INTERNAL window as aligned under A2-a, the settled walk back at INTERNAL, and the INTERNAL-select leg defect at the resolve
5609ab078 Pin the builder's media restart contract to #629's request with the AAF meter's two terms, and name the servo-with-meter row's suite in the design notes
dfa8f3609 Hold the root leg's frame byte tables in std::array for the C++ idiom gate
bc3c43a58 Grade the #629 root rows at the true audio ratio in tb/verilator/milan_dp_mclk: AAF, CRF and INTERNAL followed, W2, the switch rows, lock loss, echo, C1 and the CSR words, with the fourteen named mutants as schemata
7f2678ba1 Hold the #629 doc lines to the house sentence length, drop the em dashes from the edited rows, and link the bare references
94e718913 Hold the 1:1 audio clock for T67 so the NCO's own rate is measured, repoint the gmstep restart anchors past the meter's terms, and state A2-a in the aligner, NCO and aclk comments
5b05e962d Mark the media-clock following design implemented with its named deviations, record the INTERNAL oscillator-grade risk, and refuse a servo prune that offers only an AAF source
931ac84f3 State the selected AAF, CRF or INTERNAL source and A2-a's aligned INTERNAL grid in the time-sync, compliance, descriptor-ownership and architecture pages
b5d9e7054 Keep VERSION at 0x0002_0060 for the release step, map AAFM_STAT and AAFM_RATE in the register map and the CSR bench, record #629 in the changelog and feature ledger, and walk every listed clock source in milan_dp
0d00ad758 Check the AAF meter's stream_data_length with a shift-add so the meter maps to no DSP
c6f6a4971 Grade the servo with the AAF clock meter in front of it over 180 s, the W2 switch with the select held, and the true-ratio leg's INTERNAL phases under A2-a
d676ecfd4 Follow one selected AAF or CRF source: the AAF clock meter (E8, loss rule (b)), the table decode into the servo's one-bit select and W2 reference, mr from the meter, C1 counters, A2-a, two CSR words at VERSION 0x0061, and the meter suite with its named mutants
0b0742981 Advertise one INPUT_STREAM CLOCK_SOURCE per AAF listener after INTERNAL and CRF (#629 D1) and regenerate the five shipping shapes
baa0a8a19 Amend FR-CLK-03 and FR-CLK-04 and the #389 record to #629's owner decision: one selected INTERNAL, CRF or per-AAF-input source
```

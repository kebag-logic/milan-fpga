# HANDOFF: lane M5 of #640 (plan L8, CSR read path), executor [A590]

Status: REVIEW READY at head `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` (local branch, not pushed). Resumed 2026-10-10 21:34 after a usage-limit stop; every gate, suite and route below was run in the resumed session.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6098404907
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6098441921 (posted once; not re-posted on resume)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6104904445 (head `988ec7f6`)
- Branch `640-m5` from dev `e8454e2751d05b02ee8e5a571857589ab358ab86`; remote `https://github.com/kebag-logic/milan-fpga.git` verified.
- Roles: executor [A590]; internal reviewer [R598]; external reviewer [R599].
- Commits (one-line, configured identity, no body, no trailers):
  - `02ce5844` Load the CSR window's SNAP count words raw with a per-word kind and land the read path in one stage-1 word with an OR stage (RTL)
  - `df3128be` Lock the CSR read path to the frozen e8454e27 block in two shipping-shape legs, with seven planted defects that each fail a named check (tests)
  - `32ffe181` Span the CSR SNAP kind array over all twelve shadow words so the Yosys elaboration finds no undriven element (RTL, and the matching mutant text)
  - `93fe7405` Gate the CSR stage-1 live word on the window or the read window again, as the old final select did (RTL)
  - `1abe18eb` Describe the CSR read path's stage-1 live word, OR stage and SNAP kinds in the module page (docs) - the measured product commit
  - `d31e6e86` Count the CSR lockstep's random-traffic reads and fail the lockstep check when that traffic completes none (tests)
  - `988ec7f6` Record lane M5's measured CSR read-path saving in the Mark II plan's L8 entry and ledger (docs)
- `git diff 1abe18eb 988ec7f6 -- hdl syn sw configs` is empty: the head's RTL is the routed RTL.

## 1. Measurement of the current block

Three views of the block at dev `e8454e27`, before any change:

| View | LUT | FF | F7 / F8 | RAMB18 | Notes |
|---|---:|---:|---:|---:|---|
| Routed hierarchy, `milan_datapath/csr` (placed report of the base route at `e8454e27`) | 3,037 | 2,143 | 111 / 4 (cells) | 2 | this lane's base route (section 5), equal to the `route-1x1` record in every gated figure |
| Out of context, `milan_csr` alone, 1x1 shipping parameters | 2,955 | 3,557 | 387 / 59 | 2 | every input free |
| Out of context, `milan_csr` alone, 8x8 shipping parameters | 3,038 | 3,560 | 386 / 59 | 2 | about 12 LUT per stream, not #649's 211 |
| Out of context, integration proxy, 1x1 | 2,058 | 2,428 | 220 / 18 | 2 | `milan_csr` inside a wrapper that ties the 30 inputs `milan_datapath` ties to a module-level zero and leaves its 43 open outputs open |
| Out of context, integration proxy, 8x8 | 2,494 | 2,508 | 169 / 12 | 2 | as above |

Shipping parameters: `N_LISTENERS_P = N_TALKERS_P = N`, `SRP_LSN0_ROW_P` 2 (1x1) or 16 (8x8), `GPTP_PLANE_EN_P` 1, `MILAN_CLK_FREQ_HZ_P` 50 MHz, `CHMAP_RDBK_P` 3, `PPS_P` 0.

Where the LUTs are. Each LUT cell is attributed to the register groups its output reaches (`all_fanout -endpoints_only`). The routed column was taken in the earlier session on another lane's base route checkpoint of `e8454e27` (sha256 `017a9a6c...`); that route's gated figures and `csr` scope equal this lane's own base route:

| Group | Routed `csr` scope (cells) | Integration proxy 1x1 (cells) |
|---|---:|---:|
| live read mux, `live_mux_q` | 1,019 | 1,253 |
| 0x800 window read mux, `strm_mux_q` | 288 | 293 |
| window SNAP shadow load, `snap_shadow_r` | 356 | 374 |
| final select, `r_data` | 66 | 66 |
| shadow RAM write port | 60 | 60 |
| shared by several groups | 479 | 134 |
| logic of OTHER modules placed in the `csr` scope (cross-boundary optimization) | about 700 | 0 |

- The routed 3,037 is not all CSR logic. About 700 LUT cells in the `csr` scope feed other modules' registers. Examples: `chan_map_render/sel_r` (351), the AXI CDC `storage_25` (175), `pp_shadow` registers, `amap_*`, `wing_sid_*`, the MAAP LFSR, the TCAM. The plan's basis (the historical 2,907-LUT routed block) carries the same absorption.
- The live mux is near its floor. It carries about 3,000 live data bits in the integration proxy. A micro-experiment priced 128 random 32-bit words at their real addresses: the existing `unique case` on the 16-bit address mapped to 1,203 LUT with 512 F7 and 256 F8 (3.4 data bits per LUT). The same words as an array indexed by `[11:2]` took 1,762 LUT.

## 2. Changes (file:line at the head `988ec7f6`)

RTL: `hdl/common/csr/milan_csr.sv` only. No port, parameter, address, width, reset value or access semantic changes. Docs: `hdl/common/csr/doc/milan_csr.md` (signals and processes, `1abe18eb`) and `docs/design/MARK_II_AREA_PLAN.md` (one line in L8 and the ledger's "M5 intermediate measurement", `988ec7f6`). Tests: section 3 (`tb/verilator/csr/` and one reader entry in `scripts/measure_test_evidence_readers.py`).

1. Window SNAP count words, raw plus kind.
   - `:1463-1469`: `SK_ZERO_C`, `SK_RAW_C`, `SK_POISON_C` and `snap_kind_r[0:11]`, a two-bit kind per window word. Only `[1:10]` (CNT0-9) are ever written; `[0]` and `[11]` (STATE, PDUS) hold `SK_ZERO_C` from reset, so the array spans the same twelve words as `snap_shadow_r` and Yosys finds no undriven element (`32ffe181`).
   - `:2930`: every kind resets to `SK_ZERO_C`.
   - `strm_snap_S`: an out-of-range SNAP zeroes STATE and PDUS and writes zero kinds (`:2940`). An index-0 SNAP latches the ten full-width counters and writes the kinds in the same cycle: raw for a listener (`:2963`), POISON for a talker (`:2972`). An extra talker context writes POISON kinds before its burst (`:2980`).
   - `:3033-3035`: a listener burst writes the word and a raw kind. That arm elaborates only when `N_LISTENERS_P > 1`, the only build in which an extra listener context can be selected, so a one-listener build loads each CNT word straight from its one source.
   - `:2591-2593` (`strm_read_mux`): the CNT read applies the word's kind. Before, every bit of the ten words was loaded through a three-way select of the counter, zero and POISON.
2. One stage-1 word.
   - `:2292-2293`: `strm_mux` and `strm_hit` are declared with `live_mux`, ahead of `read_mux`, their first reader (#193).
   - `:2487-2491`: the 0x800 window (0x800-0x86F) is one more range leaf of the live tree.
   - `:1078`: `strm_mux_q` and the three hit flags are gone; `live_mux_q` holds the claimed word.
   - `:2656`: stage 1 still applies the old select's order: `live_mux_q <= (strm_hit || rd_in_window) ? live_mux : 0` (`93fe7405`). Every live address at or above 0x800 is in `rd_in_window` today, so in the current map this term changes no value. It keeps the old contract that a live arm added above 0x800 without a read-window term reads 0. `milan_dp_mclk`'s mutant 13 ("the read-window terms missing", `tb/verilator/milan_dp_mclk/mclk_mutants.py:166`) plants exactly that, and at `32ffe181` (without this term) it escaped: 31 checks, 30 PASS, 1 FAIL. With the term the suite passes.
3. Stage 2 is an OR.
   - `:2635-2641` (`shadow_out_reg`): the shadow word is zeroed in the block RAM's own output register unless the shadow serves the read (`shadow_rd_w = rd_in_window && !live_hit`). The reset is synchronous, so the RAM absorbs it.
   - `:2643-2664` (`read_data_reg`): `r_data <= live_mux_q | shadow_qq` (`:2660`), where the old code selected four ways between `strm_mux_q`, 0, `live_mux_q` and `shadow_qq`.

Why each is identical function:
- `live_mux` reads 0 wherever `live_hit` is 0. `strm_mux` reads 0 outside 0x800-0x86F, where no other live arm or range exists.
- The old select was: window hit, then 0 outside `rd_in_window`, then live hit, then shadow. Stage 1 keeps the first two in that order (`:2656`). The shadow is zeroed whenever a live arm, a range or the window claims the read, or the address is outside `rd_in_window` (`:2635`). So at most one stage-2 operand is nonzero, and it is the one the old select picked.
- A kind is written in the same cycle as its word, from the same branch that wrote POISON or zero before.

AXI-Lite read latency: unchanged. AR handshake, then `rd_pend`, `rd_pend2`, RVALID: three cycles, as before. Slow (engine) window reads are unchanged. The lockstep below compares RVALID and RDATA (and every other output) cycle for cycle against the e8454e27 block.

Rejected on measurement (recorded so a reviewer does not retry them):
- Candidate 1: one case on the word index `rd_addr_q[11:2]` merging both trees. Integration proxy 1x1 2,590 LUT (+532); the merged mux alone was 2,347 cells against 1,546.
- Variant A: the two trees kept, their outputs ORed into one stage-1 register. Integration proxy 1x1 2,290 (+232). The OR cost about 77 cells, and the SNAP saving did not appear because synthesis did not prove the extra-context burst unreachable at N = 1.

## 3. Tests and the planted defect each catches

New lockstep legs in the CSR suite (`tb/verilator/csr`):
- `obj_lock1/Vcsr_lock`: the 1x1 shipping parameters.
- `obj_lock8/Vcsr_lock`: the 8x8 shipping parameters.

The bench:
- `milan_csr_ref.sv` is the block as dev `e8454e27` shipped it, byte for byte, with only the module renamed. `gen_lockstep.py` refuses it unless its SHA-256, with the name read back, is `c3106a14...` (git blob `3392e01a`).
- The generator emits the top at build time from the block's own port list: 143 inputs (4,514 bits), 157 outputs (2,525 bits).
- It refuses a port list it parsed short, or one that differs from the reference's.
- Both instances take the same inputs; every output is compared on every cycle.

Named checks (`sim_lock.cpp`):

| Check | What it requires |
|---|---|
| `reset-values` | Every byte address 0x000-0xFFF and a sample above it, read after a cold reset and after a reset that lands with a read in flight: no output differs. The window's CNT/STATE/PDUS and STAT0-8 read 0 after the reset, whatever was latched before. |
| `decode` | The same sweep with every input word distinct and every mapped register written, under listener idx 0, talker idx 0, out-of-range and (8x8) extra-context selections: no output differs. |
| `snapshot-coherence` | STAT0-8, the window SNAP of idx 0 in both directions, an extra context's burst (8x8), both gPTP identity pairs in either half order, and PTP_TOD_RD each read the values of their capture instant while the sources change on every cycle afterwards. Expectations come from the harness. |
| `snapshot-freshness` | A later capture replaces an earlier one: a re-snapshot, a MAC reinit release zeroing STAT0-8, listener then talker then listener SNAPs, an out-of-range SNAP wiping the block the next in-range selection reads, a talker burst then a listener burst (8x8), and a new identity pair. |
| `lockstep` | Four 60,000-cycle segments of random AXI traffic (aimed at the map's 199 addresses), random values on every other input and periodic resets, with and without the modelled engines. No output differs on any cycle of any phase, and the random traffic completes reads (its R handshakes are counted, `sim_lock.cpp:298`; the check fails on none, `:717-718`, `d31e6e86`). |

Results at the head `d31e6e86` (CSR suite under GNU make 4.3, `MAKEFLAGS=w`, rc 0, `suite_tally.py --verdict` rc 0):
- 1x1 leg: 5/5, 340,861 cycles; 8,248 reset reads, 16,456 decode reads, 28,167 random-traffic reads.
- 8x8 leg: 5/5, 374,265 cycles; 24,699 decode reads, 22,750 random-traffic reads. 0 mismatching cycles in either leg.

Control for the read-count clause (one-off, in a scratch copy of the suite, not in the tree): with the random phase's ARVALID forced to 0 (`sim_lock.cpp:659`), the 1x1 leg exits 1 with `[FAIL] lockstep: the random traffic completed no read`, 4/5 checks passing. Before `d31e6e86` the same bench printed `lockstep: 0 reads` and passed, because the random phase drives the bus pins directly and nothing counted its reads.

Planted defects (`lock_mutants.py`), each in a copy of the block, rebuilt through the Makefile's own recipe:

| Defect | Leg | Must fail | Observed failing checks |
|---|---|---|---|
| wrong address decode: IRQ_RAW's live word answers at IRQ_MASK | 1x1 | `decode` | reset-values, decode, lockstep |
| torn snapshot: window CNT3 reads its live counter | 1x1 | `snapshot-coherence` | snapshot-coherence, lockstep |
| stale snapshot: a listener SNAP after a talker SNAP keeps the POISON kind | 1x1 | `snapshot-freshness` | decode, snapshot-coherence, snapshot-freshness, lockstep |
| stale snapshot: an extra listener's burst word keeps its previous kind | 8x8 | `snapshot-freshness` | decode, snapshot-coherence, snapshot-freshness, lockstep |
| reset-value drift: the CNT kinds reset to POISON | 1x1 | `reset-values` | reset-values, lockstep |
| the shadow word is not zeroed under a claim | 1x1 | `decode` | reset-values, decode, snapshot-coherence, snapshot-freshness, lockstep |
| the window's range leaf answers 0 | 1x1 | `decode` | reset-values, decode, snapshot-coherence, snapshot-freshness, lockstep |

The positive control passes; the driver reports 8 checks: 8 PASS, 0 FAIL. The whole CSR suite passes under GNU make 4.3 with `MAKEFLAGS=w` (rc 0): the six earlier legs, both lockstep legs and the controls.

Other suites, each one at a time under the sweep's own wall-clock budget, pinned Verilator 5.050, `VERILATOR_JOBS=2`; every make rc 0 and every `suite_tally.py --verdict` silent. `suite_tally.py` over the nine logs: 38,033 checks, 0 in-suite failures, rc 0.

| Suite | Head | make rc | Checks / failures | Note |
|---|---|---:|---:|---|
| `csr` (GNU make 4.3, `MAKEFLAGS=w`) | `d31e6e86` | 0 | 1,815 / 0 | six earlier legs, both lockstep legs, reset bits, `lock_mutants.py` 8/8 |
| `tcam_csr` | `1abe18eb` | 0 | 2 / 0 | |
| `milan_dp` | `1abe18eb` | 0 | 12,065 / 0 | both shipping shapes (`obj_ax1x1`, `obj_nxn8`) and the NxN, gPTP, notify, CRF, prune and aclk legs; render and gmstep mutants |
| `milan_dp_mclk` | `d31e6e86` | 0 | 168 / 0 | 31 controls including mutant 13 (read-window terms missing), caught |
| `milan_dp_render` | `d31e6e86` | 0 | 342 / 0 | |
| `capture_coherence` | `d31e6e86` | 0 | 21,194 / 0 | |
| `follow_ring` | `d31e6e86` | 0 | 66 / 0 | |
| `pp_shadow` | `d31e6e86` | 0 | 2,184 / 0 | |
| `milan_dp_gptp` | `d31e6e86` | 0 | 197 / 0 | the `ax1x1gptp` and extended legs of `milan_dp` |

`1abe18eb` and `d31e6e86` differ only in `tb/verilator/csr/sim_lock.cpp` and `tb/verilator/csr/README.md`, which no suite but `csr` reads.

Firmware host tests at `d31e6e86` (the CI commands, RV32 compiler from the pinned SDK): `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` rc 0 (PASS); `test_ctrl_nvm.py --require-rv32 --jobs 4` rc 0 (5 shapes, 435 tests); `fw_coverage.py --selftest` rc 0 (28/28 planted cases) and `--check --jobs 4` rc 0 (30 files); `test_nvm_firmware.py --self-test` rc 0 (5 shapes, every planted defect caught). Builder: `test_builder.py --require-elaboration --require-rv32` rc 0, both shapes elaborated; one arm (gate 11, an Arty calibration report absent on this host) did not run, for its recorded reason.

Register-map checks at `1abe18eb` (no register-map file changes after it): `behave` 14 features, 404 scenarios, 0 failed (the counters-contract steps read `docs/reference/REGISTER_MAP.md`); `check_feature_status.py` 0 findings and its self-test rc 0; `check_entity_shape.py` and `--self-test` rc 0.

## 4. Primitive mapping before and after

Out of context, `milan_csr` alone at the shipping parameters, synthesized with the same scratch recipe (`AreaOptimized_high`, one synthesis thread, 50 MHz clock) at base `e8454e27` and at the head's RTL (`1abe18eb`, equal to `d31e6e86` in `hdl/`). Every primitive cell counted by `REF_NAME`:

| Primitive | 1x1 base | 1x1 head | delta | 8x8 base | 8x8 head | delta |
|---|---:|---:|---:|---:|---:|---:|
| LUT1 | 8 | 8 | 0 | 10 | 8 | -2 |
| LUT2 | 98 | 98 | 0 | 100 | 108 | +8 |
| LUT3 | 293 | 247 | -46 | 226 | 495 | +269 |
| LUT4 | 344 | 367 | +23 | 385 | 417 | +32 |
| LUT5 | 622 | 466 | -156 | 742 | 499 | -243 |
| LUT6 | 1,866 | 1,582 | -284 | 1,822 | 1,721 | -101 |
| MUXF7 | 387 | 393 | +6 | 386 | 394 | +8 |
| MUXF8 | 59 | 59 | 0 | 59 | 59 | 0 |
| FDRE | 3,499 | 3,451 | -48 | 3,502 | 3,476 | -26 |
| FDSE | 58 | 58 | 0 | 58 | 58 | 0 |
| RAMB18E1 | 2 | 2 | 0 | 2 | 2 | 0 |

No LUTRAM, SRL, RAMB36 or DSP appears in either build. The two RAMB18E1 are the shadow RAM and the defaults ROM, as before. The read path's mapping change: the ten window CNT words no longer each carry a three-way select per bit at load (fewer LUT5/LUT6); the read gains a two-bit kind decode per CNT word (LUT3/LUT4); the old final four-way select is gone. The 1x1 FDRE delta of -48, by register group: `strm_mux_q` -32 and the three stage-1 hit flags (`strm_hit_q`, `live_hit_q`, `rd_in_window_q`) -3, which this change removes; `strm_dir_r` replicas -5, `rd_addr_q` -3, `snap_shadow_r` -4 and `snap_st_r` -3, which synthesis trims or stops replicating; `snap_kind_r` +2 (at 1x1 the ten kinds always hold one value, so synthesis keeps two flops).

Utilization, same runs (Vivado "Slice LUTs" counts LUT sites):

| View | Base LUT / FF | Head LUT / FF | Delta |
|---|---:|---:|---:|
| `milan_csr` alone, 1x1 | 2,955 / 3,557 | 2,515 / 3,509 | -440 / -48 |
| `milan_csr` alone, 8x8 | 3,038 / 3,560 | 2,859 / 3,534 | -179 / -26 |
| Integration proxy, 1x1 | 2,058 / 2,428 | 1,903 / 2,391 | -155 / -37 |
| Integration proxy, 8x8 | 2,494 / 2,508 | 2,295 / 2,489 | -199 / -19 |

The integration proxy ties the 30 inputs `milan_datapath` ties and leaves its 43 open outputs open, so it is the closer model of the shipping instance. The routed census of the integrated image is in section 5.

## 5. Resource and route before and after (M0s recipe)

Both integrated routes follow `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` ("Prerequisites", "Export the shipping builds", "Integrated measurements"): a fresh clone at the commit, a fresh external work directory, the pinned RV32 SDK, `sw/litex/build.sh ax7101 --dry-run`, the LiteX elaboration with the exact printed arguments, `syn/ooc/pp_baseline.py <gateware> --single-thread-synthesis`, then `vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log`. Each Vivado run held the exclusive host lock and ran alone in this lane's service unit.

| Run | Commit | Lock held | Route rc | `pp_resource_gate.py check --endpoint route-1x1` |
|---|---|---|---:|---|
| Base | dev `e8454e27` | 2026-10-11 04:03-05:02 | 0 | rc 0, PASS, every gated figure equal to the record |
| Head | `1abe18eb` (RTL equal to `988ec7f6`) | 2026-10-11 01:43-02:33 | 0 | rc 0, PASS, "re-baseline recommended" (LUT improved past tolerance) |

The gate's tool, device, design, state and flow identity matched for both. XDC, shipping Tcl and `baseline_integrated.tcl` are byte-identical between the two exports apart from the checkout path, so no exception, constraint or flow change was added.

Whole image (gate figures from the routed reports; post-synthesis from the same runs):

| Figure | Record | Base route | Head route | Delta | Tolerance / floor | Verdict |
|---|---:|---:|---:|---:|---|---|
| LUT | 50,267 | 50,267 | 49,577 | -690 | +500 | ok, below baseline |
| FF | 54,413 | 54,413 | 54,226 | -187 | +600 | ok, below baseline |
| SLICE | 15,779 | 15,779 | 15,791 | +12 | +80 | ok |
| RAMB36 | 74 | 74 | 74 | 0 | 0 | ok |
| RAMB18 | 27 | 27 | 27 | 0 | 0 | ok |
| DSP | 14 | 14 | 14 | 0 | 0 | ok |
| BRAM tiles | 87.5 | 87.5 | 87.5 | 0 | ceiling 121.5 | ok |
| WNS, ns | +0.299 | +0.299 | +0.097 | -0.202 | -0.25, floor 0.03 | ok |
| WHS, ns | +0.031 | +0.031 | +0.036 | +0.005 | -0.25, floor 0.0 | ok |
| Post-synthesis LUT | - | 52,731 | 52,303 | -428 | - | - |
| Post-synthesis FF | - | 54,531 | 54,350 | -181 | - | - |

Every endpoint passes at the head route: setup 0 failing of 181,010 endpoints (TNS 0.000), hold 0 failing of 180,929 (THS 0.000), pulse width 0 failing of 61,083 (TPWS 0.000, WPWS +0.264 ns). Each of the four signoff corners (Slow/Fast at 0 C and 85 C) reports "No timing paths found" below zero slack. Route status: 100,776 routable nets, 100,776 fully routed, 0 with routing errors. The head's worst setup path (+0.097 ns) is in the CPU's DMA write bridge (`dma_bridge_write_bridge/aligner` to `onPerId_bridge/pendings_valids_reg[0]`, 20 logic levels), which M5 does not touch. The base's +0.299 ns worst setup path is also outside the CSR (`milansoc_write_w_buffer_level0_reg[1]` to `storage_13_dat1_reg[14]`, a LiteX FIFO). WNS sits above the 0.03 ns floor with no exception.

The `csr` scope (`milan_datapath/csr`, hierarchical reports of the same runs; slack from the routed checkpoints):

| Figure | Base | Head | Delta |
|---|---:|---:|---:|
| Routed LUT sites | 3,037 | 2,916 | -121 |
| Post-synthesis LUT sites | 3,130 | 3,003 | -127 |
| FF (routed and post-synthesis) | 2,143 | 2,110 | -33 |
| RAMB18 / RAMB36 / LUTRAM / DSP | 2 / 0 / 0 / 0 | 2 / 0 / 0 / 0 | 0 |
| Worst setup slack, paths from `csr` | +2.923 ns | +2.559 ns | |
| Worst setup slack, paths to `csr` | +1.353 ns | +3.189 ns | |
| Worst hold slack, from / to `csr` | +0.071 / +0.102 ns | +0.088 / +0.083 ns | |

Routed primitive census by `REF_NAME`, one Vivado session over both route checkpoints:

| Primitive | `csr` base | `csr` head | delta | image base | image head | delta |
|---|---:|---:|---:|---:|---:|---:|
| LUT1 | 15 | 14 | -1 | 1,652 | 1,696 | +44 |
| LUT2 | 341 | 359 | +18 | 9,626 | 9,609 | -17 |
| LUT3 | 704 | 371 | -333 | 9,979 | 9,819 | -160 |
| LUT4 | 565 | 548 | -17 | 9,628 | 9,681 | +53 |
| LUT5 | 847 | 634 | -213 | 9,429 | 8,617 | -812 |
| LUT6 | 1,213 | 1,458 | +245 | 17,256 | 17,304 | +48 |
| MUXF7 | 111 | 124 | +13 | 1,026 | 1,053 | +27 |
| MUXF8 | 4 | 6 | +2 | 49 | 49 | 0 |
| CARRY4 | 51 | 51 | 0 | 3,402 | 3,384 | -18 |
| FDRE | 2,114 | 2,081 | -33 | 50,334 | 50,299 | -35 |
| FDSE | 29 | 29 | 0 | 672 | 672 | 0 |
| FDCE | 0 | 0 | 0 | 3,327 | 3,177 | -150 |
| FDPE | 0 | 0 | 0 | 101 | 99 | -2 |
| RAMB18E1 | 2 | 2 | 0 | 27 | 27 | 0 |
| RAMB36E1 | 0 | 0 | 0 | 74 | 74 | 0 |

The `csr` scope packs 3,685 LUT cells into 3,037 sites at base and 3,384 into 2,916 at the head. The image's LUTRAM (RAM32M 663, RAM64M 59, RAM32X1D 47, RAM64X1D 290), SRL16E (5) and DSP48E1 (14) counts are unchanged.

Attribution. The routed image moved -690 LUT, but the gate's own sub-block list puts -344 in `u_pp` and -342 in the processor wrapper, both untouched. Post-synthesis, the image moved -428 LUT: `csr` -127, `pp_shadow` -375 and a net +74 over the other untouched blocks. Those blocks' FDCE drop (-150, async-clear flops that `milan_csr` does not use) comes from different register-merge decisions elsewhere in the same synthesis, for example in the gPTP engine; the two synthesis logs differ in 194 register merge/trim messages outside the CSR (and 14 inside it). None of that is credited.

Saving against the plan:

| Measure | Saving |
|---|---:|
| `csr` scope, routed | 121 LUT, 33 FF |
| `csr` scope, post-synthesis | 127 LUT, 33 FF |
| Integration proxy, out of context, 1x1 / 8x8 | 155 / 199 LUT |
| `milan_csr` alone, out of context, 1x1 / 8x8 | 440 / 179 LUT |
| Plan L8 estimate | 600 (400-1,000) |

The reproducible integrated saving is about 125 LUTs and 33 FFs, below the estimate's range. Out of context with every input free, the 1x1 block saves 440, inside the range. With the 30 inputs `milan_datapath` ties tied (the proxy), it saves 155, which is the figure the integrated image reproduces. The remaining read path is the live mux over about 3,000 live status bits the register map fixes, at about 3.4 data bits per LUT (section 1). Two larger restructurings were measured and rejected (section 2). #649's 211 LUTs per stream do not reproduce: out of context the block grows about 12 per stream.

8x8 shape. The recipe's 8x8 integrated endpoint stops after synthesis. The head's 8x8 synthesis was stopped after 40 minutes (02:49-03:29), before it finished, when this lane's unit reached 9.3 GB (8.5 GB anonymous), to keep the unit under its 9 GB working limit. So no 8x8 integrated figure is claimed. The 8x8 shape is measured out of context (section 4: -179 LUT alone, -199 in the proxy) and exercised by the `lock8` lockstep leg and `milan_dp`'s `obj_nxn8` leg.

Placement faces. The selected-split route stays at the M0s step-1 STOP (parent integration), so only the all-fabric route is measured. Split-face parity by elaboration: the head's `--ctrl-mailbox` elaboration (`sw/litex/milan_soc.py --ctrl-mailbox` with the shipping arguments) instantiates `milan_datapath` with a parameter block and a 128-port port map byte-identical to the all-fabric elaboration's, from the same `milan_csr.sv` (sha256 `5d6f56ef...`); the mailbox face adds its 15 mailbox sources and nothing inside the datapath. `milan_csr` sees no placement input, so both faces instantiate the identical block.

Record. Not re-recorded. AREA_BUDGET's Mark II exception D7 keeps the gate record until M9, and an improvement recommendation does not authorize an intermediate re-record. `pp_resource_gate.py record <head gateware> --endpoint route-1x1` without `--write` printed the would-be record (rc 0) and changed nothing. The measurement is published in the plan's ledger (`docs/design/MARK_II_AREA_PLAN.md`, "M5 intermediate measurement", and one line in L8), placed away from the open M2 lane's insertion points.

Artifacts (scratch, not in the tree; digests only): head route checkpoint sha256 `cf54ccc5d7edbe0ac6edf5723fe36c77a573b2f525894ec8d245bee694f2ac94` (108,266,520 bytes); base route checkpoint sha256 `11f00a4403abac999ae6fe45e21bfe30e2ce448202457a914e8b24f273a43f00` (109,284,693 bytes); route status reports `6d50e4ce...` (head) and `1e5c6395...` (base).

## 6. Gate table

Every command was run unpiped, each with its own log and exit status. Interpreters: CPython 3.12.3 (the hosted CI's), the docs virtualenv (Markdown gates), the LiteX virtualenv (it carries PyYAML, which `check_entity_shape.py` needs; the host interpreter lacks it), and the host `python3` where the CI job uses the runner's. Yosys 0.66 (the pinned v0.66) with sv2v 0.0.13 (the hosted job pins 0.0.12, so its elaboration is the authoritative run). A row at `1abe18eb` covers `d31e6e86` unless the gate reads `tb/verilator/csr/sim_lock.cpp` or `tb/verilator/csr/README.md`; every such gate was re-run at `d31e6e86` and appears twice.

| Gate | Command | Interpreter | Head | rc |
|---|---|---|---|---:|
| py_idiom | `python3 scripts/check_py_idiom.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| py_idiom_self | `python3 scripts/check_py_idiom.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| sh_idiom | `python3 scripts/check_sh_idiom.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| sh_idiom_self | `python3 scripts/check_sh_idiom.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| cpp_idiom | `python3 scripts/check_cpp_idiom.py` | CPython 3.12.3 | `d31e6e86` | 0 |
| cpp_idiom | `python3 scripts/check_cpp_idiom.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| cpp_idiom_self | `python3 scripts/check_cpp_idiom.py --selftest` | CPython 3.12.3 | `d31e6e86` | 0 |
| cpp_idiom_self | `python3 scripts/check_cpp_idiom.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| sv_idiom | `python3 scripts/check_sv_idiom.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| naming | `python3 scripts/measure_naming.py --check` | CPython 3.12.3 | `d31e6e86` | 0 |
| naming | `python3 scripts/measure_naming.py --check` | CPython 3.12.3 | `1abe18eb` | 0 |
| naming_self | `python3 scripts/measure_naming.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| fail_fast | `python3 scripts/measure_fail_fast.py --check` | CPython 3.12.3 | `d31e6e86` | 0 |
| fail_fast | `python3 scripts/measure_fail_fast.py --check` | CPython 3.12.3 | `1abe18eb` | 0 |
| fail_fast_self | `python3 scripts/measure_fail_fast.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| test_evidence | `python3 scripts/measure_test_evidence.py --check` | CPython 3.12.3 | `d31e6e86` | 0 |
| test_evidence | `python3 scripts/measure_test_evidence.py --check` | CPython 3.12.3 | `1abe18eb` | 0 |
| test_evidence_self | `python3 scripts/measure_test_evidence.py --selftest` | CPython 3.12.3 | `d31e6e86` | 0 |
| test_evidence_self | `python3 scripts/measure_test_evidence.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| hygiene | `python3 scripts/check_hygiene.py --check` | CPython 3.12.3 | `d31e6e86` | 0 |
| hygiene | `python3 scripts/check_hygiene.py --check` | CPython 3.12.3 | `1abe18eb` | 0 |
| hygiene_self | `python3 scripts/check_hygiene.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| todo | `python3 scripts/check_todo_ownership.py` | CPython 3.12.3 | `d31e6e86` | 0 |
| todo | `python3 scripts/check_todo_ownership.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| todo_self | `python3 scripts/check_todo_ownership.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| control_flow_self | `python3 scripts/measure_control_flow.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| cohesion_self | `python3 scripts/measure_cohesion.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| suite_tally_self | `python3 scripts/suite_tally.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| entity_shape | `python3 scripts/check_entity_shape.py --self-test` | LiteX venv (PyYAML) | `1abe18eb` | 0 |
| soc_sources | `python3 scripts/check_soc_sources.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| soc_sources_self | `python3 scripts/check_soc_sources.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| port_contracts | `python3 scripts/check_port_contracts.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| port_contracts_self | `python3 scripts/check_port_contracts.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| rtl_source_lists | `python3 scripts/check_rtl_source_lists.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| rtl_source_lists_self | `python3 scripts/check_rtl_source_lists.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| pp_srcs | `python3 scripts/pp_srcs.py --check --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| ci_scope_self | `python3 scripts/ci_scope.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| ci_events | `python3 scripts/ci_events.py --check` | host python3 | `1abe18eb` | 0 |
| wire | `python3 scripts/check_wire_accountability.py --self-test` | host python3 | `1abe18eb` | 0 |
| baremetal | `python3 scripts/check_baremetal_only.py --check` | host python3 | `1abe18eb` | 0 |
| baremetal_self | `python3 scripts/check_baremetal_only.py --selftest` | host python3 | `1abe18eb` | 0 |
| nvm_record_space | `python3 scripts/check_nvm_record_space.py` | host python3 | `1abe18eb` | 0 |
| nvm_record_space_self | `python3 scripts/check_nvm_record_space.py --self-test` | host python3 | `1abe18eb` | 0 |
| nvm_capture | `python3 scripts/check_nvm_capture.py` | host python3 | `1abe18eb` | 0 |
| docs_check | `python3 scripts/docs_check.py` | docs venv | `d31e6e86` | 0 |
| docs_check | `python3 scripts/docs_check.py` | docs venv | `1abe18eb` | 0 |
| docs_nogit | `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | docs venv | `d31e6e86` | 0 |
| docs_nogit | `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | docs venv | `1abe18eb` | 0 |
| em_dash | `python3 scripts/check_em_dash.py --base e8454e27` | docs venv | `d31e6e86` | 0 |
| em_dash | `python3 scripts/check_em_dash.py --base e8454e27` | docs venv | `1abe18eb` | 0 |
| em_dash_self | `python3 scripts/check_em_dash.py --selftest` | docs venv | `1abe18eb` | 0 |
| doc_style | `python3 scripts/check_doc_style.py` | docs venv | `d31e6e86` | 0 |
| doc_style | `python3 scripts/check_doc_style.py` | docs venv | `1abe18eb` | 0 |
| doc_style_self | `python3 scripts/check_doc_style.py --selftest` | docs venv | `1abe18eb` | 0 |
| toc_self | `python3 scripts/gen_toc.py --selftest` | docs venv | `1abe18eb` | 0 |
| toc_anchors | `python3 scripts/gen_toc.py --verify-anchors` | docs venv | `d31e6e86` | 0 |
| toc_anchors | `python3 scripts/gen_toc.py --verify-anchors` | docs venv | `1abe18eb` | 0 |
| toc_check | `python3 scripts/gen_toc.py --check` | docs venv | `d31e6e86` | 0 |
| toc_check | `python3 scripts/gen_toc.py --check` | docs venv | `1abe18eb` | 0 |
| doc_paths | `python3 scripts/check_doc_paths.py` | docs venv | `d31e6e86` | 0 |
| doc_paths | `python3 scripts/check_doc_paths.py` | docs venv | `1abe18eb` | 0 |
| doc_map | `python3 docs/DOC_MAP.gen.py --check` | docs venv | `1abe18eb` | 0 |
| feature_status | `python3 scripts/check_feature_status.py` | docs venv | `1abe18eb` | 0 |
| feature_status_self | `python3 scripts/check_feature_status.py --self-test` | docs venv | `1abe18eb` | 0 |
| archive | `python3 scripts/check_archive.py` | docs venv | `1abe18eb` | 0 |
| archive_self | `python3 scripts/check_archive.py --selftest` | docs venv | `1abe18eb` | 0 |
| solution | `python3 scripts/check_solution_docs.py` | docs venv | `1abe18eb` | 0 |
| module_matrix | `python3 docs/traceability/gen_module_matrix.py --check` | docs venv | `d31e6e86` | 0 |
| module_matrix | `python3 docs/traceability/gen_module_matrix.py --check` | docs venv | `1abe18eb` | 0 |
| resource_self | `python3 syn/ooc/pp_resource_gate.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| resource_baseline | `python3 syn/ooc/pp_resource_gate.py check-baseline` | CPython 3.12.3 | `1abe18eb` | 0 |
| dp_srcs_self | `python3 syn/ooc/dp_srcs.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| ooc_tcl_self | `python3 syn/ooc/ooc_tcl_selftest.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| pp_baseline_self | `python3 syn/ooc/pp_baseline.py --selftest` | CPython 3.12.3 | `1abe18eb` | 0 |
| pp_baseline_mutants | `python3 -X cpu_count=4 syn/ooc/pp_baseline_mutants.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| pp_baseline_reports_self | `python3 syn/ooc/pp_baseline_reports_selftest.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| resource_mutants | `python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| dp_srcs_datapath | `python3 syn/ooc/dp_srcs.py --top milan_datapath` | CPython 3.12.3 | `1abe18eb` | 0 |
| dp_srcs_shadow | `python3 syn/ooc/dp_srcs.py --top KL_pp_shadow` | CPython 3.12.3 | `1abe18eb` | 0 |
| lint | `python3 scripts/lint_rtl.py --check --self-test` | CPython 3.12.3, pinned Verilator 5.050 on PATH | `1abe18eb` | 0 |
| diff_base | `git diff --check e8454e27 HEAD` | - | `d31e6e86` | 0 |
| diff_base | `git diff --check e8454e27 HEAD` | - | `1abe18eb` | 0 |
| diff_tree | `git diff --check` | - | `d31e6e86` | 0 |
| diff_tree | `git diff --check` | - | `1abe18eb` | 0 |
| behave | `(cd tests && behave --no-capture -f plain)` | - | `1abe18eb` | 0 |
| yosys_elab | `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | - | `1abe18eb` | 0 |
| yosys_csr | `syn/yosys/run.sh --top milan_csr --results <results dir>` | - | `1abe18eb` | 0 |
| yosys_ooc_self | `python3 syn/yosys/ooc_selftest.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| yosys_guard_self | `python3 syn/yosys/guard_selftest.py` | CPython 3.12.3 | `1abe18eb` | 0 |
| entity_shape_check | `python3 scripts/check_entity_shape.py` | LiteX venv (PyYAML) | `1abe18eb` | 0 |
| docs_check | `python3 scripts/docs_check.py` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| docs_nogit | `GIT_DIR=/dev/null python3 scripts/docs_check.py` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| em_dash | `python3 scripts/check_em_dash.py --base e8454e27` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| doc_style | `python3 scripts/check_doc_style.py` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| toc_anchors | `python3 scripts/gen_toc.py --verify-anchors` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| toc_check | `python3 scripts/gen_toc.py --check` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| doc_paths | `python3 scripts/check_doc_paths.py` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| doc_map | `python3 docs/DOC_MAP.gen.py --check` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| feature_status | `python3 scripts/check_feature_status.py` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| archive | `python3 scripts/check_archive.py` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| solution | `python3 scripts/check_solution_docs.py` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| module_matrix | `python3 docs/traceability/gen_module_matrix.py --check` | docs venv | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| resource_baseline | `python3 syn/ooc/pp_resource_gate.py check-baseline` | CPython 3.12.3 | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| hygiene | `python3 scripts/check_hygiene.py --check` | CPython 3.12.3 | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| ci_scope_self | `python3 scripts/ci_scope.py --selftest` | CPython 3.12.3 | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| diff_tree | `git diff --check` | - | `988ec7f6` (working tree of the plan edit, committed unchanged) | 0 |
| em_dash | `python3 scripts/check_em_dash.py --base e8454e27` | docs venv | `988ec7f6` | 0 |
| diff_base | `git diff --check e8454e27 HEAD` | - | `988ec7f6` | 0 |
| diff_tree | `git diff --check` | - | `988ec7f6` | 0 |
| docs_check | `python3 scripts/docs_check.py` | docs venv | `988ec7f6` | 0 |
| toc_check | `python3 scripts/gen_toc.py --check` | docs venv | `988ec7f6` | 0 |
| route gate, head | `python3 syn/ooc/pp_resource_gate.py check <head gateware> --endpoint route-1x1` | CPython 3.12.3 | `1abe18eb` route | 0 |
| route gate, base | `python3 syn/ooc/pp_resource_gate.py check <base gateware> --endpoint route-1x1` | CPython 3.12.3 | `e8454e27` route | 0 |
| record, print only | `python3 syn/ooc/pp_resource_gate.py record <head gateware> --endpoint route-1x1` | CPython 3.12.3 | `1abe18eb` route | 0 |

Suites, firmware host tests, builder and register-map checks: section 3. Route gate and measurement checks: section 5.

## 7. Open risks and decisions

1. Saving below the estimate (decision for the manager). The reproducible integrated saving is about 125 LUTs and 33 FFs (`csr` scope: 121 routed, 127 post-synthesis), against L8's 600 (400-1,000). No register-map change was attempted, so the STOP condition was not reached. The ledger's cumulative tables keep the 600 planning figure, as M2's did, until the week-4 re-measure.
2. WNS margin. The head route's WNS is +0.097 ns against the base's +0.299 (floor 0.03, tolerance 0.25): it passes, but with less margin for later lanes. The worst path is in the CPU's DMA write bridge, which this lane does not change. Paths into and out of `csr` gained setup slack (worst +2.559 ns, against the base's +1.353 ns).
3. Whole-image movement not credited. Of the routed -690 LUT, about -686 is in untouched blocks (`u_pp`, the wrapper). It is synthesis and placement variation, not a saving, and could reverse in a later route.
4. 8x8 integrated synthesis not completed (memory limit; section 5). The 8x8 shape rests on the OOC figures and the 8x8 simulation legs.
5. Split-placement route not measured (M0s step-1 STOP). Parity is shown by elaboration identity only.
6. Record not re-recorded (D7). The gate prints "re-baseline recommended"; M9 decides.
7. The stage-1 gate `(strm_hit || rd_in_window)` (`milan_csr.sv:2656`) changes no value in today's map. It keeps the old contract that an unlisted live arm above 0x800 reads 0, and `milan_dp_mclk`'s mutant 13 catches its removal. The lockstep cannot catch that removal, because no such arm exists in the current map.
8. `measure_test_evidence.py` reports that its mutation ratchet "can be lowered to 69", because the CSR suite now has a mutation arm. The ratchet is left unchanged; lowering it is outside this lane.

Process notes (no effect on the evidence):
- An earlier session on this round was cut by a usage limit. Its route was killed mid-synthesis and every route, suite and gate was re-run in this session. No file planted by a mutation campaign was left in the tree; the tree held only the uncommitted module-page edit, which was finished and committed (`1abe18eb`).
- The base route of `e8454e27` that the earlier session relied on lived in another lane's scratch directory, which was removed during this session. So this lane re-ran its own base route (section 5), which reproduces the record exactly.
- The unit's memory peak reached 12.36 GB earlier in the session, while the gate batch, a `milan_dp` build and the firmware tests overlapped. That exceeded the 9 GB working limit, though no OOM kill occurred (`oom_kill 0`). Later work ran serially, and the 8x8 synthesis was stopped at 9.3 GB.

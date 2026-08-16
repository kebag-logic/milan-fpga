# Area budget — where the LUTs are, and which of them are optional

**Measured 2026-07-27** from the post-synthesis hierarchical utilisation of an
8×8 `xc7a100t` build (`report_utilization -hierarchical`, Vivado 2026.1). Every
number here is a **synthesis** figure from a real Vivado run — not an estimate,
and not a placement result.

This page deliberately **excludes the CPU**. The soft CPU and its caches are a
vendored component with their own configuration surface; everything below is
logic this project owns and can therefore choose not to build.

> **THE DIE CHANGED SHAPE ON 2026-08-13 — a whole plane left, and the
> protocol processor arrived.** This repository's ADP advertiser, ACMP talker
> and listener, AECP/AEM engine, persistence journal and lwSRP applicant were
> **deleted** and replaced by the pinned `protocol-processor` submodule. Every
> measurement on this page is still a real Vivado (or, where labelled, yosys)
> reading of the design **as it stood on 2026-07-27**, and is kept as such:
> the rows below are marked **REMOVED** where the block no longer exists, and
> no number has been invented to replace one.
>
> **The measured record of what that change cost and returned is
> [historical protocol-processor area measurement](../findings/PP_SHADOW_AREA_0812.md)**
> — same instrument, both sides in context. Read it, not an extrapolation
> from this page, for any question about post-substitution area. Two things
> from it are worth carrying here because they change how this page should be
> used:
>
> * the single biggest line item below, `u_bld` (`KL_aecp_response_builder`,
>   5,300 LUT here), was part of an AECP plane that measured **8,645 LUT
>   in context** for `KL_aecp_top` alone — larger than the entire replacement
>   plane costs in context (**+6,956**);
> * the tier-3 "core, not reclaimable by parametrisation" verdict was
>   correct about *parametrisation* and was overtaken by **deletion**: three
>   of its five entries are gone.
>
> **AECP came back, and not as fabric memory.** The processor's AECP µCPU has
> since landed and serves its declared command inventory, including
> `READ_DESCRIPTOR`, `GET_COUNTERS`, stream-state getters, clock-source
> operations, Identify controls, and Milan information. Unsupported commands
> receive the conformant fallback. Its cost is **not** in
> any figure on this page, and it is not in the `+6,956` either — that was
> measured with the AECP pop face tied off. Two area consequences are worth
> carrying: the **entity model is no longer in fabric at all** (the µCPU's
> descriptor store reads it from DDR3 over a read-only master at a compile-time
> base, so no descriptor ROM or store is charged to LUT or BRAM anywhere in the
> replacement), and the mass Vivado constant-propagated away while that face
> was tied off is back and un-repriced. The tracked builder generates the DRAM
> image and the board rootfs loads it with `aemi-load` before entity enable.
> Custom integrations that omit that step fail closed with `BAD_ARGUMENTS`.
>
> What is NOT changed by any of that: the governing fact in the next section
> (this design is **LUT-bound**, FFs sit at 42 %), the prune-parameter rules,
> the memory-cascade reasoning, and every honest limit at the bottom.

## Contents

- **[The budget](#the-budget)** — The four-way split of the device: 61,959 of 63,400 LUTs used, of which the datapath is 35,113 and the CPU 16,799. Also the fact that governs every other decision on this page — FFs are only 42 %, so **the design is LUT-bound** and trading LUTs for FFs is a win.
- **[The datapath, by block](#the-datapath-by-block)** — The leaderboard: every leaf block over 400 LUTs with its FF and BRAM cost. `KL_aecp_response_builder` at 5,300 LUTs is the single biggest thing this project owns.
- **[What is actually optional](#what-is-actually-optional)** — Three tiers, and tier 1 is now **implemented**: six blocks behind elaboration-time prune parameters worth a measured **4,515 LUT / 4,750 FF** (yosys estimate), each defaulting to PRESENT. Contains the per-block banked-lever entries — what each costs, what it buys, what re-measurement it forces — plus the estimator result that pulling all six takes the 8x8 shape out of the OVER band, and the section you should read before quoting any of it: which of the two measurement methods to trust when they disagree.
- **[The 9,993 LUTs outside the datapath](#the-9993-luts-outside-the-datapath)** — A sixth of the device is SoC glue — DMA writers, RX steering, CSR bridges, the MAC — and it has had **no area review at all**, despite being comparable to the whole tier-1 + tier-2 opportunity.
- **[The memory cascade: DDR3 for FIFOs, BRAM as register file](#the-memory-cascade-ddr3-for-fifos-bram-as-register-file)** — 44 BRAM tiles are free, which reorders the work: spend them turning LUT logic into memory lookups (`milan_csr`, `u_bld`) before freeing any. Names the one FIFO that must **not** move to DDR3 — the egress queues, because a late return mid-frame is a wire underrun, not a retry.
- **[Rules for adding a prune parameter](#rules-for-adding-a-prune-parameter)** — Five rules for the next `*_P`: default PRESENT, elaboration-time not runtime, tie outputs inert, state what re-measurement it forces, and make the builder refuse configs that want the pruned feature. How the six that exist satisfy each one is under 'The five rules, as implemented'.
- **[What was rejected, and the numbers that killed it](#what-was-rejected-and-the-numbers-that-killed-it)** — Five roads not taken, each with the figure that closed it: pricing a prune with `-flatten` (it read a deleted 1,691-flop block as −0 FF), `chparam` to set the ship shape (it cannot re-elaborate sv2v's interface names), a runtime capability bit per block (it would owe a `VERSION` bump), and two estimator designs — one of which double-booked a pruned block at −262 LUT.
- **[VERSION was deliberately NOT bumped](#version-was-deliberately-not-bumped)** — Why *this round* did not move `VERSION` (it was `0x0001_0014` then; a later, unrelated round took it to `0x0015`): at the default settings this round is a pure no-op parametrisation, and a bump announces *CSR-observable behaviour changed on a board that actually runs*. A build that pulls a lever changes plenty — that is declared by the config that pulled it, not by the version word.
- **[Honest limits](#honest-limits)** — What these numbers are not. They are **yosys** synthesis, not Vivado placement; the one block with both figures shows yosys running ~2x high on LUTs; the six levers together are worth 10 % less than summing them one at a time; no pruned bitstream has been built; and the servo prune has no software-visible contrast at all at internal clock.

## The budget

| region | LUTs | share of device |
|---|---|---|
| device capacity (`xc7a100t`) | 63,400 | 100 % |
| **total used** | **61,959** | **97.7 %** |
| soft CPU + caches | 16,799 | 26.5 % |
| **`milan_datapath`** | **35,113** | **55.4 %** |
| SoC glue outside the datapath | 9,993 | 15.8 % |
| **non-CPU total (this page's scope)** | **~45,160** | **71.2 %** |

Flip-flops are **53,217 / 126,800 = 42 %** and block RAM is **91 / 135 = 67 %**.
**The design is LUT-bound.** A change that trades LUTs for FFs is a win; a change
that only removes FFs buys nothing.

### 2026-07-28 evening — the DRC UTLZ-1 round (VERSION 0x0019), measured

The 0x0019 compliance fabric plus `rx_queues: 2` took the 8×8 to **66,290
LUT-as-logic against 63,400 sites** — every seed died at DRC, and the numbers
below are Vivado post-synth hierarchy, not estimates:

| delta vs the shipping 8×8 | LUTs | verdict |
|---|---|---|
| SoC glue for `rx_queues` 1→2 (steer + RX1 ring + RSC) | **+4,299** | required — the D7 GM-starvation fix |
| Vexii netlist drift (trunk hash change) | +2,406 | not ours |
| ACMP listener SM in fabric (`u_ctx` 444 → 2,182) | +1,738 | compliance |
| lwSRP licence work (`ctx`/`rx`) | +1,728 | compliance |
| `milan_csr` (journal group + growth) | +1,875 | compliance |
| counter mirror as FF (`avtp_rx_monitor`) | +894 | **recovered** — see below |
| depacketizer `frame_fifo` un-trimmed (266 → 1,344) | +1,078 | honest cost of real consumers |
| CRF shaped-queue work (`traffic_controller`) | +840 | partly **recovered** — see below |

Three lessons with mechanisms attached:

1. **The estimator ran ~15 points optimistic at this shape** (`resources OVER
   (worst LUT 85.4%)` printed for a design that needed 100.4 % of the device).
   Treat the builder's percentage as a trend indicator between two configs,
   never as a fit verdict — the fit verdict is Vivado's post-synth report and
   nothing else (which is this document's own rule 139 restated, now with a
   15-point casualty attached).
2. **Vivado does not read-replicate a multi-column array into LUTRAM.** The
   GET_COUNTERS mirror (`cnt_mir_r[N][10]`, one row read across all ten
   columns) synthesized to 2,560 flops + muxes even with
   `(* ram_style = "distributed" *)` on it — yosys maps the same code to
   RAM32M, which is exactly how the OOC estimate hid the cost. Ten separate
   per-column 1W1R arrays infer distributed RAM in both tools
   (`KL_avtp_rx_monitor_ctx.sv` `diag_mirror`, ~−1.1 k LUT / −2.5 k FF).
3. **The true audio shape costs what the wrong one did.** The dead seeds had
   built the default-I2S 2-channel front-end (the fragment gap now hard-gated
   by `check_sweep_shape`); a private-copy OOC of the datapath at the real
   tdm32/8-channel/8-stream shape measured **33,705 LUTs vs 33,712** for the
   wrong one. The NxN fabric is shape-dominated, not front-end-dominated, so
   the 63,644 post-prune figure transfers to the true shape.

New tier-1 lever landed this round: **`CBS_QUEUES_MASK_P`** (derived, not
declared — the builder computes it from `srp.class_queue`; the SR A/B queues
keep their `credit_based_shaper` instance, q0–q2 are strict-priority only,
which is bit-identical to the `cbs_shaped_i = 0` state every non-SR queue has
always run in). Worth ~3 × 425 LUT + 18 DSP on both boards, proven equivalent
by the `shaper_core` suite's dual-core mask oracle.

## The datapath, by block

Leaf blocks over 400 LUTs. Parent rows are omitted where a single child
dominates them.

| block | module | LUT | FF | BRAM | 2026-08-13 |
|---|---|---|---|---|---|
| `u_bld` | `KL_aecp_response_builder` | **5,300** | 2,342 | — | **REMOVED** |
| `csr` | `milan_csr` | **4,066** | 3,763 | R18×2 | present |
| `walker` | `KL_lwsrp_walker` | **2,938** | 904 | — | **REMOVED** |
| `u_ctx` | `KL_acmp_lstn_ctx` | **2,650** | 1,984 | — | **REMOVED** |
| `traffic_shaper` | `traffic_shaping_core` | **2,579** | 1,276 | — | present |
| `chan_map_render` | `KL_chan_map_render` | **2,547** | 1,625 | — | present |
| `ctx` | `KL_lwsrp_ctx` | 1,615 | 1,515 | R36×2 | **REMOVED** |
| `avtp_rx_monitor` | `KL_avtp_rx_monitor_ctx` | 1,268 | 1,113 | R18×1 | present |
| `aaf_packetizer` | `KL_aaf_packetizer` | 1,226 | 1,473 | R36+R18 | present |
| `ptp_timestamp` | `ptp_ts_top` | 1,069 | 1,669 | — | present |
| `mmcm_servo` | `KL_mmcm_drp_servo` | 933 | 807 | — | present, permanently idle |
| `acmp_responder` | `KL_acmp_tlkr_ctx` | 770 | 797 | — | **REMOVED** |
| `aaf_latency_taps` | `KL_aaf_latency_taps` | 696 | 614 | — | present |
| `maap_engine` | `KL_maap` | 621 | 268 | — | present — and now load-bearing |
| `rx_filter` | `rx_mac_filter` | 569 | 1,570 | — | present |
| `bw_gate` | `KL_lwsrp_bw_gate` | 564 | 676 | — | **REMOVED** |
| `i2s_player` | `KL_i2s_playback` | 552 | 624 | R36×1 | present |
| `buffer_queues` | `traffic_queues` | 531 | 321 | R36×6 R18×6 | present |
| `ctx_tx` | `KL_lwsrp_ctx_tx` | 505 | 312 | — | **REMOVED** |
| `mac_cam` | `tcam` | 504 | 1,568 | — | present |
| `pcm_lpf` | `KL_pcm_lpf` | 445 | 756 | — | present |

Seven of the twenty-one leaf blocks over 400 LUTs are gone, and **`KL_maap`
changed job**: it is the only 1722-family protocol engine left in this
repository's RTL, and the protocol processor's talker cannot declare a stream
without an `ALLOC_DA` success through it — so the `MAAP_P` prune below is no
longer a "static addresses" trade, it disables the talker. In their place
sits `KL_pp_shadow`, which is not in this table because this table predates
it; its measured cost is in the findings page named in the banner. The servo
row is marked *permanently idle* rather than removed: it is still built, but
`SET_CLOCK_SOURCE` was the only writer of its selector, so it can never leave
idle.

## What is actually optional

Before 2026-07-27 **only two elaboration prunes existed** — `AUDIO_IF_SLOTS_P`
and `AAF_PLAYBACK_P` — plus two SoC switches (`--aaf-playback`,
`--strip-probes`). Everything else was built unconditionally, whether or not a
given deployment could use it.

### Tier 1 — genuinely optional blocks · **IMPLEMENTED 2026-07-27**

Each is dead weight in a deployment that does not use the feature. All default
to **PRESENT**, so adding the parameter changed no shipping build — the
generated top of a default build is byte-identical, and `test_builder` gate 23a
enforces that on all three shipped configs.

| block | `milan_datapath` | SoC flag | `board.features` | dead when |
|---|---|---|---|---|
| media-clock servo | `MCSERVO_P` | `--no-media-clock-servo` | `media_clock_servo` | the media clock is internal — the servo idles unless the clock source is a recovered one |
| latency taps | `LTAP_P` | `--no-latency-taps` | `latency_taps` | pure instrumentation; nothing in the media path reads them |
| MAAP engine | `MAAP_P` | `--no-maap` | `maap` | stream destination addresses are statically provisioned |
| I2S playback | `I2SPB_P` | `--no-i2s-playback` | `i2s_playback` | the board has no DAC |
| RX address filter | `RXFILT_P` | `--no-rx-mac-filter` | `rx_mac_filter` | the port is promiscuous, or filtering is done in software |
| PCM low-pass | `LPF_P` | `--no-render-lpf` | `render_lpf` | render path only, and every digital acceptance measurement is taken upstream of it |
| datapath probe groups | `DPROBES_P` | `--no-datapath-probes` | `datapath_probes` | the APRB (0x8B4–0x8C4) and PBK (0x8C8–0x8D0) groups are closed-finding diagnostics (fabric-listener blocker + item-7 chain, both TB-pinned since); the range reads 0 on a pruned build — the LTAP precedent (added 2026-07-29 to unlock AreaOptimized_medium on the AX, whose AreaOptimized_high timing was congestion-systemic) |

#### What each one is worth — MEASURED, and every figure a yosys ESTIMATE

Measured 2026-07-27 with [`syn/yosys/ooc.sh`](../../syn/yosys/ooc.sh)'s toolchain (`sv2v` →
`yosys synth_xilinx -family xc7`) on `milan_datapath` at the **ship shape**
(`N_STREAMS = 8`, `AUDIO_IF_SLOTS_P = 16`), hierarchy preserved, per-module
`stat`. **These are synthesis estimates, not placement results**, and yosys
runs roughly 2× high on LUTs against Vivado for the one block where both
numbers exist (`KL_pcm_lpf`: yosys 864, Vivado place 428–445; the flip-flop
figures agree exactly at 756).

| block | LUT | FF | DSP | BRAM36 | replaces the estimate |
|---|---|---|---|---|---|
| media-clock servo (`KL_mmcm_drp_servo` + its `cdc_handshake`/`cdc_pulse`) | 814 | 789 | 1 | — | 933 / 807 |
| latency taps (`KL_aaf_latency_taps` + 2 × `KL_aaf_latency_chain`) | 948 | 614 | — | — | 696 / 614 |
| MAAP engine (`KL_maap`) | 634 | 269 | — | — | 621 / 268 |
| I2S playback (`KL_i2s_playback` + its `cdc_pair_fifo`/`cdc_pulse`) | 454 | 631 | — | 1 | 552 / 624 |
| RX address filter (`rx_mac_filter` 123/11 + `tcam` 678/1680) | 801 | 1,691 | — | — | 504 / 1,568 |
| PCM low-pass (`KL_pcm_lpf`) | 864 | 756 | 1 | — | 445 / 756 |
| **total** | **4,515** | **4,750** | **2** | **1** | 3,751 / 4,637 |

The measured LUT total is **20 % above** the Vivado-derived estimate this page
opened with and the flip-flop total is within **2.4 %** of it — consistent with
yosys over-counting LUTs and counting flops exactly. Read the LUT column as
*this is the block*, not *this is what placement will hand back*.

**~4.5 k yosys LUTs**, none of it requiring a functional change — only the
ability to say "this build does not include that".

#### What that is worth to the 8×8 shape, in the builder's own estimator

[`sw/builder`](../../sw/builder)'s resource model, run over `endstation_ax7101_8x8.yaml` with the
levers pulled (still an **estimate**, and a *different* model again — Vivado
place figures for the blocks it knows, yosys for the three it did not):

| configuration | LUT | FF | verdict |
|---|---|---|---|
| default — every block PRESENT | 56,537 | 53,751 | **OVER** 89.2 % |
| internal-only clocking alone, no prune (isolates the CRF sink) | 53,838 | 45,294 | OVER 84.9 % |
| five levers, servo kept | 53,081 | 49,902 | OVER 83.7 % |
| **all six levers** (servo ⇒ internal-only ⇒ CRF sink goes too) | **49,568** | **40,656** | **TIGHT** 78.2 % |

**Pulling every tier-1 lever takes the 8×8 shape out of the OVER band.** Read
the last row honestly: **−6,969 LUT total, of which −2,699 is `KL_crf_rx`**,
which is not a lever — pruning the servo *requires* an internal-only clock
config, and that drops the CRF sink with it. The six levers themselves are
**−4,270 LUT** in this model. That coupling is the single most important thing
to understand before quoting the number.

### Which method to trust when the two disagree

Two whole-design methods were run for every configuration, PRESENT and PRUNED:

| method | what it does | present total |
|---|---|---|
| **flatten** | `synth_xilinx -family xc7 -flatten` then `stat` — `ooc.sh`'s method | 31,645 LUT / 21,718 FF |
| **hierarchical** | `synth_xilinx -family xc7` (hierarchy kept) then `stat -top` | 125,639 cells |

Whole-design deltas, PRESENT minus PRUNED:

| pruned | flatten ΔLUT | flatten ΔFF | hierarchical Δcells |
|---|---|---|---|
| media-clock servo | −682 | −749 | −2,792 |
| latency taps | −987 | −584 | −3,577 |
| MAAP | −348 | −108 | −940 |
| I2S playback | −520 | −739 | −1,783 |
| RX address filter | **−1** | **0** | −2,560 |
| PCM low-pass | **−14** | **0** | −2,193 |
| all six together | −2,266 | −2,180 | −12,462 |

**The flatten method is wrong for two of the six, and provably so.** It reports
the flip-flop total as *bit-identical* after removing blocks that elaboration
shows carry 1,691 and 756 flip-flops. Deleting 1,691 flip-flops cannot leave
the flip-flop count unchanged, so that is an artefact of whole-design
flattening, not a measurement. The prune itself is not in doubt: with
`RXFILT_P = 0`, `yosys hierarchy -top milan_datapath` lists neither
`rx_mac_filter` nor `tcam` in the design at all.

**Trust the hierarchical figure.** It is the one that (a) agrees with each
block's standalone out-of-context synthesis, (b) agrees with the Vivado
hierarchical report this page is built from, and (c) is arithmetically possible.
This is the same disagreement a sibling lane recorded in the other direction
(a `-flatten` run reading **+97 LUT** where its hierarchical run read **−812**),
and the same conclusion: at ~50 k cells, optimisation noise swamps a ~1 k-cell
lever in a flattened netlist.

### The five rules, as implemented

1. **Default PRESENT** — every parameter defaults to 1. `test_builder` gate 23a
   asserts all three shipped configs carry every block, emit no `--no-*` flag,
   and count no prune row in the resource estimate.
2. **Elaboration-time** — each is a `generate if (…) … else …`, so synthesis
   drops the instance. Where a runtime enable already exists the two **compose**:
   the parameter decides whether the logic is *built*, the CSR bit decides
   whether the built logic *runs*, and the pruned tie-off is defined to be
   exactly the runtime-disabled state term by term (`LPF_CTRL 0x72C[0] = 0`,
   `MAAP_CTRL.en = 0`, `LTAP_CTRL` cleared, `promisc = 1`).
3. **Inert ties** — every pruned block's outputs are tied to that state, so the
   interface is defined, never floating. [`scripts/check_tied_inputs.sh`](../../scripts/check_tied_inputs.sh) is
   unaffected: it inventories `milan_datapath` **input** ports tied by the SoC,
   and none of these prunes ties an input — the SoC still wires the real MMCM,
   the real MAC and the real pins. The gate runs green with the same three
   justified TDM entries and **zero** new warnings.
4. **Stated re-measurement** — recorded per block below, and printed into every
   pruned config's `build_plan.md` by the builder, so the obligation travels
   with the artefact instead of with a reviewer's memory.
5. **Gated** — [`sw/builder/endstation_builder.py`](../../sw/builder/endstation_builder.py) `validate_features()` raises
   `ConfigError` for a config that asks for a feature the prune removed.
   Mutation-proven: neuter the function and gate 23b fails on its first case.

### The banked levers, in the `LPF_P` style

Each entry: what it costs, what it buys, what re-measurement it forces, and that
it defaults to PRESENT.

**`MCSERVO_P = 0` — media-clock servo.**
*Buys* 814 LUT / 789 FF / 1 DSP (yosys estimate).
*Costs* the ability to discipline the audio MMCM to a clock the fabric
recovers. `A_MCSRV_STAT 0x8F8` becomes a **structural** zero, the DRP and
phase-shift ports never move, and the MMCM is never reset by the datapath.
*Legal when* the media clock is internal: the builder gate refuses it unless
`clocking.media_clock_sources` is exactly `[internal]`.
*Forces re-measurement of* every CRF / input-stream lock result — servo
convergence, `MCSRV_STAT` state transitions, any recovered-clock jitter figure.
*Note* the servo already idles at `clock_source == 0`, so on an internal-clock
build this prune is **area-only**: [`tb/verilator/milan_dp`](../../tb/verilator/milan_dp)'s pruned shape and
its PRESENT shape both read `0x8F8` as 0 and both leave the MMCM pins still.
That is the honest statement — the contrast is invisible from software at
internal clock, which is exactly why the config, not a CSR bit, is what
declares it. **Defaults to PRESENT.**

**`LTAP_P = 0` — AAF latency taps.**
*Buys* 948 LUT / 614 FF (yosys estimate).
*Costs* the entire LTAP CSR window `0x870`–`0x8B0`, which reads 0. `LTAP_CTRL`
reads `0x2` (the reset-1 enable bit with no status behind it).
*Legal when* the build ships no instrumentation: the gate refuses it unless
`board.constraints.strip_probes` is true.
*Forces re-measurement of* **all of [`AAF_LATENCY_TAPS.md`](../AAF_LATENCY_TAPS.md)** — the CAP-SOF,
SOF-EOF and EOF-MAC silicon numbers were read out of this block and cannot be
re-read from a build that does not contain it. Nothing in the media path reads a
tap, so no acceptance surface moves. A zero here is structural, not 0 ns — the
same distinction `STATS_CAP` draws for the RMON lanes. **Defaults to PRESENT.**

**`MAAP_P = 0` — MAAP engine.**
*Buys* 634 LUT / 269 FF (yosys estimate).
*Costs* dynamic stream-DMAC allocation and defence. `MAAP_STAT0/1`
(`0x6D0`/`0x6D4`) read 0, the effective stream DMAC is always the
CSR-provisioned `AAF_DMAC`, and the engine's low-rate TX leg never wins the
arbiter. **`MAAP_CTRL.en` becomes effectively reserved**: setting it would pin
AAF admission *shut*, because the claim can never complete.
*Legal when* addresses are statically provisioned; the gate refuses it when
`srp.stream_dmac_base` is the literal `maap`.
*Forces re-measurement of* MAAP claim/defend behaviour and any address-collision
result that depended on the engine answering. **Defaults to PRESENT.**
**Re-read this lever after 2026-08-13**: the protocol processor implements no
MAAP by design and reaches `KL_maap` through `KL_pp_maap_shim`, and its
talker declares only after an `ALLOC_DA` success. So `MAAP_P = 0` no longer
means "static addresses" — **it means no source ever declares and the talker
half of ACMP is dead by construction**. The tie-off path is deliberately the
same one a still-probing allocator takes, so nothing takes an untested
branch; the capability loss is total and must be a config decision, never a
size-pressure reflex.

**`I2SPB_P = 0` — I2S DAC playback.**
*Buys* 454 LUT / 631 FF / 1 BRAM36 (yosys estimate).
*Costs* the DAC serializer and its rate servo: the four `i2s_dac_*` pins park at
0 and the I2SPB CSR group reads 0. Second-order effect worth stating —
`i2spb_converged` is `KL_avtp_rx_monitor`'s `servo_conv_i`, and that block's
media-lock rule is `clk_src == 0 || servo_conv`. So on a pruned build an
**external** media clock **never reaches media lock**. That is consistent
(there is no render device to converge) but it is a real behavioural
consequence and the sharpest reason this prune needs a config gate;
internal-clock media lock is immediate and unaffected.
*Legal when* the board has no DAC; the gate refuses it while
`audio_interface.kind` is `i2s_philips`, whose render half **is** this block.
*Forces re-measurement of* every analog measurement taken at the line out — the
loop THD+N record, the pilot-tone census — and the I2SPB underrun/overrun
census. **Defaults to PRESENT.**

**`RXFILT_P = 0` — RX station-address filter.**
*Buys* 801 LUT / **1,691 FF** (yosys estimate) — by far the largest flip-flop
saving of the six, and worth nothing on a LUT-bound design. Pull it for the
LUTs or not at all.
*Costs* hardware address filtering: the RX stream becomes a straight wire from
the PTP stage to the DMA port, which is bit-exactly what the shipping filter
emits with `promisc = 1`. **The port becomes promiscuous.** The `TCAM_*` window
still accepts writes and nothing reads them.
*Legal when* the port is meant to be promiscuous or the host does the dropping;
the gate refuses it unless `platform.rx_address_filter` says `software` or
`promiscuous`.
*Forces re-measurement of* the RX drop census and any claim about what the
station refuses. **Defaults to PRESENT.**

**`LPF_P = 0` — PCM render low-pass.** (Banked 2026-07-26, wired the same day
as the rest.)
*Buys* 864 LUT / 756 FF / 1 DSP (yosys estimate); 428–445 LUT / 756 FF / 1 DSP
on the shipping Vivado place report.
*Costs* nothing digital: the pruned tap is what `LPF_CTRL[0] = 0` already
produces.
*Legal when* — its **only** consumer inside `milan_datapath` is
`KL_i2s_playback`, so the gate runs the other way for this one: keeping the
filter in a build whose player is pruned is refused, because that synthesises a
render filter with nothing behind it.
*Forces re-measurement of* the analog loop THD+N record, which was measured
*through* this filter. **Defaults to PRESENT.**

### Tier 2 — blocks that should scale with the configured shape

These are not prune-or-keep; they are built for the largest shape regardless of
what the config asks for. Parameterising them to the *actual* shape is worth more
than pruning in a small build and costs nothing in a large one.

| candidate | LUT | scales with | 2026-08-13 |
|---|---|---|---|
| `chan_map_render` | 2,547 | physical channels and slot count — a 2-channel build should not carry a 64-channel crossbar | still open |
| `avtp_rx_monitor` | 1,268 | per-context counter banks | still open |
| `KL_lwsrp_ctx` + `ctx_tx` | 2,120 | the L+T attribute rows | **REMOVED** — the processor sizes its SRP arrays from the entity shape instead |
| `acmp_responder` | 770 | talker contexts — a listener-only entity needs none | **REMOVED** — same, via `ACMP_SRC_C` |

Half of tier 2 was answered by deletion rather than by parametrisation, and
the half that answered it did so *better*: the processor's ACMP and SRP arrays
are sized from `adp_shape_defaults.svh`, i.e. from the same config that
declares the shape, which is exactly what this tier was asking for.

### Tier 3 — core, not reclaimable by parametrisation

`u_bld` (5,300), `csr` (4,066), `walker` (2,938), `u_ctx` (2,650),
`traffic_shaper` (2,579). Together **17,533 LUTs, half the datapath.** These
implement mandatory behaviour; the only route into them is **structural** —
sequentialising wide parallel compares, sharing duplicated decode, replacing
per-index logic with a mux behind a counter. That is a redesign question, not a
parameter question, and it should be costed separately.

> **And that is precisely what happened (2026-08-13).** `u_bld`, `walker` and
> `u_ctx` — **10,888 of those 17,533 LUTs** — were not parameterised, dieted
> or shared: they were **REMOVED**, together with the rest of the 1722.1/SRP
> plane, and replaced by a processor plane that measures **+6,956 LUT in
> context** against **−15,474** removed
> ([historical protocol-processor area measurement](../findings/PP_SHADOW_AREA_0812.md),
> hierarchical utilization, both sides same instrument). The tier-3 verdict
> was right that no parameter could reach them, and wrong to imply that made
> them permanent. `csr` and `traffic_shaper` remain, and their structural
> question is unchanged. **Do not add these figures to the findings page's
> net** — this page is a 2026-07-27 synthesis snapshot at the 8×8 shape and
> that page is an in-context measurement at the shipping 1×1 shape; they are
> different instruments on different designs.

## The 9,993 LUTs outside the datapath

Roughly a sixth of the device sits in SoC glue that is neither CPU nor datapath —
DMA writers, the RX steering front end, CSR bridges, the Ethernet MAC core. It
has had **no area review at all**. It is called out here because "exclude the
CPU" makes it in-scope, and because 10 k LUTs is comparable to the entire tier-1
and tier-2 opportunity combined.

## The memory cascade: DDR3 for FIFOs, BRAM as register file

The device has **44 free BRAM tiles** (91 of 135 used). That single fact reorders
the work:

| consumer | tiles | note |
|---|---|---|
| soft CPU + caches | 29 | out of scope |
| SoC glue (DMA rings etc.) | 41 | largest single consumer, never reviewed |
| `traffic_queues` — egress FIFOs | 9 | largest datapath user |
| lwSRP (`top`+`rx`+`ingress`+`mrpdu_fifo`) | ~6.5 | **REMOVED 2026-08-13** |
| AECP ingress | 1.5 | **REMOVED 2026-08-13** |
| `milan_csr` | 1.0 | |
| **free** | **44** | |

### 2026-08-03 — the SLICEM census: the biggest LUTRAM array was never in the datapath

The audit below ("LUTRAM is 784 of 35,113 **across the whole datapath**") is true,
and the datapath was the wrong place to look. Vivado's own **`Distributed RAM:
Final Mapping Report`** in the synth log ranks every inferred array on the board —
use it, not a yosys estimate and not a hierarchy roll-up. Ranked (LUTRAM LUTs;
`RAM32M`/`RAM64M` = 4 LUTs each, `RAM64X1S` = 1, ~4 LUTs = 1 SLICEM):

| array | where | size | primitives | LUTs | ~slices |
|---|---|---|---|---|---|
| `storage_31` = `tx_sf` payload | LiteX glue, `milan_soc.py` | 512 × 82 | **RAM64M ×224** | **896** | **224** |
| `ctx_ram` | `KL_acmp_lstn_ctx.sv:282` — module REMOVED 2026-08-13 | 9 × 317 | RAM32M ×112 | 448 | 112 |
| `col_r` diag mirror (×10) | [`KL_avtp_rx_monitor_ctx.sv:750`](../../hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv#L750) | 8 × 32 | RAM32M ×6 ea | 240 | 60 |
| `mem` (3× `axis_fifo`) | `ptp_timestamp`, third_party | 2 × 73 | RAM32M ×13 ea | 132 | 33 |
| `cbuf_r` | `KL_aecp_response_builder.sv:360` — module REMOVED 2026-08-13 | 64 × 64 | RAM64M ×22 | 86 | 22 |
| `fword_r` ×2 | `KL_acmp_{lstn,tlkr}_ctx.sv` — both REMOVED 2026-08-13 | 9 × 64 | RAM32M ×11 ea | 88 | 22 |
| `mem_r` | [`cdc_pair_fifo.sv:45`](../../hdl/common/cdc_pair_fifo.sv#L45) | 8 × 52 | RAM32M ×9 | 36 | 9 |
| `rec_ram_r` | `KL_persist_journal.sv:179` — module REMOVED 2026-08-13 | 48 × 32 | RAM64X1S ×32 | 32 | 8 |

The table is the `AreaOptimized_medium` build (the only one that placed, so the
only one with a full report). `storage_31` sat in the *"SoC glue — largest single
consumer, never reviewed"* row above. It was distributed RAM for exactly one
reason: migen's fwft `SyncFIFO` reads its storage **asynchronously**, and an async
read can only be LUTRAM. `buffered=True` selects `SyncFIFOBuffered`, whose read
port is synchronous. Pinned by [`sw/litex/test_tx_sf_gapless.py`](../../sw/litex/test_tx_sf_gapless.py), which reads the
kwargs out of `milan_soc.py` rather than restating them.

**Measured, on the shipping recipe** (`AlternateRoutability` synth +
`ExtraNetDelay_high` place — the build that had been failing), same tree, one
keyword apart:

| | before | after | delta |
|---|---|---|---|
| Slice LUTs | 60,255 (95.0 %) | 59,204 (93.4 %) | **−1,051** |
| LUT as Logic | 57,274 | 57,007 | −267 |
| LUT as Distributed RAM | 2,962 | 2,178 | **−784** |
| LUT as Shift Register | 19 | 19 | 0 |
| `RAMD64E` | 1,070 | 286 | **−784** |
| `RAMD32` / `RAMS32` / `SRL16E` | 2,738 / 878 / 19 | 2,738 / 878 / 19 | 0 |
| Block RAM Tile | 100.5 (74.4 %) | 102 (75.6 %) | **+1.5** |

**784 LUTRAM LUTs = ~196 SLICEMs freed for 1.5 BRAM tiles**, plus 267 LUT-as-Logic
(the async read's address decode) that went with it. Note the count differs from
the 896 in the table: how many `RAMD64E` one array costs is a function of the
**synth directive**, so quote the delta from the recipe you actually ship.

**Why this outranks its LUT count.** Distributed RAM is the one primitive class
that pins a whole SLICEM *and* cannot LUT-combine with a neighbour, so it costs
**packing** far more than it costs the LUT total. 0x0019+ missed `Place 30-487` by
22–53 slices on four different place directives while sitting at only 95 % LUTs —
the shortfall was packing, and this one array was ~196 slices of it.

**Rule:** census with Vivado's RAM report, never by module. The array that decides
packing may be in generated glue that no module owner is watching.

Four of the eight rows above named modules that no longer exist (≈654 LUTRAM
LUTs, ≈164 SLICEMs, all of it in the deleted 1722.1 plane). The *rule* is
what survives and it is the point of the section — and it applies with more
force now, not less: the protocol processor brings its own arrays, so the
next census must be run on a build that contains it rather than
extrapolated from this one.

### Stage 1 — spend the free tiles first: BRAM as the register file

**BRAM is not the constraint; LUTs are.** So the trade that matters is *LUTs into
BRAM*, and there are 44 tiles to spend **before** anything has to be freed.

The prize is not flop arrays — an audit found the big blocks are logic-dominated
(LUTRAM is 784 of 35,113 across the whole datapath, and their declared arrays
total ~5.5 k bits, mostly already in RAM). The prize is **turning combinational
logic into memory lookups**:

* **`milan_csr` — 4,066 LUT / 3,763 FF / 1 tile.** A CSR block is address decode,
  a register file, and a read multiplexer. Held in flops with a LUT mux, that
  read path grows with every register added — and this one has grown a lot
  (`0x200` RMON, `0x400` CBS, the `0x800` window, `0x870` taps, `0x8B4` probes,
  `0x8C8` playback). A **BRAM-backed register file** replaces the flop array *and*
  the read mux with one block memory. The registers that cannot move are the ones
  with side effects — strobes, W1C, snapshot latches, anything a fabric consumer
  reads combinationally — so this is a partition exercise, not a wholesale swap.
* **`u_bld` — 5,300 LUT.** A response builder is largely a wide field mux over
  descriptor data. Whatever part is a pure function of a descriptor index is a
  ROM. The replacement took that argument to its end point rather than halfway:
  the protocol processor's AECP µCPU keeps no descriptor memory in fabric at
  all and fetches the model from DDR3.
* **`u_ctx` — 2,650 LUT**, `walker` — 2,938 LUT: same question, per block.

Each conversion costs a **read latency** and that is the real risk, not the
memory. `crf_rx` is the in-tree precedent: its `rate_o` moved one clock later and
that shift had to be pinned by a suite check before the change was accepted.

### Stage 2 — DDR3 for the bulk FIFOs, to free more tiles

Once the 44 free tiles are spent, the next tiles come from moving buffering into
the 512 MB DDR3. The candidates are **not equal**:

| FIFO | tiles | move to DDR3? |
|---|---|---|
| DMA / host rings (in the SoC glue's 41) | large | **yes** — already the pattern; the PCM ring already offers `--pcm-ring dram` |
| `mrpdu_fifo`, AECP ingress | ~3 | **moot** — both blocks REMOVED 2026-08-13. The processor's own control-frame FIFO is the equivalent candidate, and it is BRAM by construction |
| `traffic_queues` egress buffers | 9 | **NO, or only with proof** |

**The egress queue buffers are the dangerous one.** They feed the MAC at line
rate, and the CBS shaper makes credit decisions against them cycle by cycle. DDR3
latency is variable — refresh, bank conflicts, arbitration against the CPU and
the DMA engines — and a late return mid-frame is an underrun on the wire, not a
retry. Anything isochronous stays on-chip unless someone measures worst-case
latency under contention and shows the headroom. Elastic, deadline-free buffering
is what belongs in DRAM.

## Rules for adding a prune parameter

1. **Default PRESENT.** A parameter that changes a shipping build by existing is
   a behaviour change wearing a costume.
2. **Elaboration-time, not runtime.** A runtime enable still builds the logic.
   The point is for synthesis to drop the instance.
3. **Tie the outputs to their inert values**, so a pruned block leaves a defined
   interface rather than a floating one.
4. **State what re-measurement it forces.** `LPF_P` is the worked example: the
   analog loop record was measured *through* that filter, so removing it invalidates
   that measurement even though it changes no digital acceptance surface.
5. **Gate it.** The builder must refuse a config that asks for a feature the
   parameter pruned — a silently absent feature is the decorative-ABI failure in
   reverse.

## What was rejected, and the numbers that killed it

* **Pricing the prunes with `-flatten`.** It is the cheaper instrument (one
  synth per configuration, one number out) and it is what `ooc.sh` does. It was
  rejected for the RX filter and the LPF on the evidence in "Which method to
  trust": −1 LUT / −0 FF and −14 LUT / −0 FF for blocks that elaboration proves
  are gone, including an unchanged flip-flop total after deleting 1,691 flops.
  It is retained for the other four, where it agrees with the hierarchical
  figure to within the expected cross-boundary slack.
* **`chparam` to set the shape.** [`syn/yosys/ooc.sh`](../../syn/yosys/ooc.sh) sets the ship shape with
  `chparam -set`, but on `milan_datapath` that re-runs the AST frontend over
  sv2v's flattened interface names and dies (`Failed to detect width for
  identifier \traffic_controller.buffer_queues…`). The measurements here patch
  the SV **default** in a private copy instead, which is exactly equivalent —
  the parameter *is* its default in every build that does not override it — and
  the patched defaults are recorded per configuration.
* **A runtime capability bit per block** (a `STATS_CAP` for the optional
  blocks). Attractive, and it would let software distinguish "absent" from
  "idle" at `0x8F8` and `0x870`. Rejected for this round because it is a **CSR
  contract change** and would owe a `VERSION` bump at default settings, which
  this lane deliberately does not spend (see below). The declaration lives in
  the build config and in `build_plan.md` instead. It is the obvious follow-up.
* **Dropping pruned modules from the SoC source list.** An unused module in
  `_MILAN_DATAPATH_SOURCES` costs nothing (nothing instantiates it) and
  [`scripts/check_soc_sources.py`](../../scripts/check_soc_sources.py) gates the list's shape. Making the list
  conditional would make that gate configuration-dependent for no gain.
* **Adding positive `mmcm_servo` / `latency_taps` rows to the resource
  estimator.** Both are genuinely missing from `RESOURCE_COSTS` today, and
  adding them would be an accuracy fix — but it would move every existing
  config's estimate by ~1.6 k LUT and break the gate-11 calibration against the
  real `mf48` place report and the gate-13 envelopes. The accuracy fix is a
  separate change with its own re-calibration. What landed instead splits by
  whether the estimator already knew about the block: `rx_filter`,
  `i2s_renderer` and `maap_claim_ctx`/`maap_dmac_slot_extra` are existing
  **Vivado-derived** rows, so pruning counts them **0** — more accurate than
  subtracting a yosys figure from a Vivado one; the servo, the taps and the LPF
  (which is folded inside `aaf_listener_engine`) get a **subtractive** row
  counted 1 only when pruned. Either way a default config counts every prune
  row 0 and its estimate is byte-identical to what it was.
* **Subtracting the yosys figure from blocks the estimator already prices.**
  Tried first, and it double-books: the table would charge 539 LUT for
  `rx_filter` and then credit back 801, netting −262 LUT for a block that is
  simply absent. Caught by reading the generated `build_plan.md` of a pruned
  config, which is the argument for printing the whole row table in the first
  place.

## `VERSION` was deliberately NOT bumped

`milan_csr` `VERSION` stayed `0x0001_0014` **for this round**. (It has since moved
to `0x0001_0015` for an unrelated change — the ADP shape registers becoming
read-only — and to `0x0001_0016` for another, the AVTP `tu` bit becoming driven;
neither affects the reasoning below.) At the
**default** settings — every
parameter 1 — this change is a pure no-op parametrisation: the same instances,
the same wiring, the same CSR values, and [`tb/verilator/milan_dp`](../../tb/verilator/milan_dp)'s legacy and
NxN shapes pass unchanged at 196 / 135 / 147 checks. A `VERSION` bump announces
*CSR-observable behaviour changed at the settings a board actually runs*, and
nothing here does. A build that pulls a lever changes plenty — `0x8F8` reads 0,
the LTAP window reads 0, the port goes promiscuous — but that is declared by the
config that pulled it and printed into its `build_plan.md`, which is where a
build-shape declaration belongs. (Same reasoning a sibling lane used for its
byte-identical refactor.)

## Honest limits

* These are **synthesis** numbers, and the tier-1 table is a **yosys** estimate
  — a different tool from the Vivado report the rest of this page is built on.
  Placement can differ, and slice occupancy, not LUT count, is what actually
  failed on this design.
* The tier-1 total is what synthesis reports for those instances **today**; it is
  not a promise that removing them frees exactly that many slices, because
  packing and control-set effects dominate at this occupancy. The six together
  measure −12,462 hierarchical cells against −13,845 summed individually, i.e.
  **10 % of the saving is shared logic that only goes when its last consumer
  does** — pulling two levers is worth slightly less than pulling them one at a
  time and adding up.
* **No Vivado run backs any of these six numbers.** The only cross-check that
  exists is `KL_pcm_lpf`, where the shipping place report says 428–445 LUT and
  yosys says 864. Assume the same ~2× on the other five until someone places a
  pruned build.
* The prunes are proven in **elaboration and simulation**, not on silicon:
  [`tb/verilator/milan_dp`](../../tb/verilator/milan_dp)'s `obj_prune` shape builds with all six pruned and
  passes 31 checks, and the same binary against the PRESENT shape fails 12 of
  them (the mutation proof that the checks measure the prune). No pruned
  bitstream has been built or flashed.
* The `MCSERVO_P` prune has **no software-visible contrast** at internal clock,
  because the servo idles there anyway. Its correctness rests on the tie-off
  being the servo's own idle state, which is an inspection argument backed by
  the TB's "no MMCM pin ever moved" check — not on a behavioural difference.
* Tier 2 is un-costed: the savings depend on the configured shape, and nobody has
  measured a small-shape build.
* The CPU is excluded by scope, not because it is optimal. It is 26.5 % of the
  device and has its own configuration surface.

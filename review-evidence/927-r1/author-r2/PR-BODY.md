[A791]

## Contents

- **[Status](#status)** — The timing table at the head against #818's floor, and `927-8x8-timing` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — The public task, the executor and the reviewers.
- **[Description](#description)** — The paths, the four cuts, their tests, what binds now, and the area.
- **[Authoritative references](#authoritative-references)** — Requirements, contracts and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and environment.
- **[How to validate](#how-to-validate)** — Reviewer commands and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do, and what is the base's.
- **[Definition of Done](#definition-of-done)** — The merge bar.

## Status

REVIEW READY at `0297a19a` (`927-8x8-timing` -> `dev-soft-core`): thirteen one-line commits on `70f4056f`. Native
sweep 65 of 65 suites (2,713,101 checks, 0 failures); workflow jobs 118 steps rc 0, 0 bad; every clean-clone suite
and mutant campaign below passes but the twin, whose one finding is the base's (Known limitations).

The split images through S9's recipe (WNS / WHS at the worst corner, ns), graded against #818's floor: setup
+0.030 and hold 0 at every corner (#927 issuecomment-6930885657, which corrects the +0.030 on hold the round's
prompts applied):

| Shape | Directive | Base `70f4056f` | Head | #818's floor at the head |
|---|---|---|---|---|
| 8x8/1if | ExtraPostPlacementOpt (the recipe's) | +0.011 / +0.034 (setup missed) | +0.293 / +0.033 | met |
| 8x8/1if | ExtraTimingOpt | +0.171 / +0.014 | +0.073 / +0.029 | met |
| 8x8/1if | AltSpreadLogic_high | +0.215 / +0.014 | +0.058 / +0.034 | met |
| 1x1/1if | ExtraPostPlacementOpt (the recipe's) | +0.208 / +0.014 | +0.081 / +0.036 | met |
| 1x1/1if | ExtraTimingOpt | +0.260 / +0.014 | +0.135 / +0.033 | met |
| 1x1/1if | AltSpreadLogic_high | not run at the base | +0.126 / +0.033 | met |

The base's figures are this lane's reproduction (8x8/1if, the recipe's directive) and #919's, #920's and #925's
routes of the same netlist. Every route has 0 failing endpoints and 0 routing errors. The 8x8/1if routes ran on a
clone of `5d098172`, the others on `338ece89`; since `5d098172` nothing under `hdl/` has changed but comments in
`cdc_pair_fifo.sv` and a generated README, and `0297a19a` changes one test file.

- Both split shapes meet #818's floor on all three directives. The least margins are 8x8/1if's setup on
  AltSpreadLogic_high (+0.058) and its hold on ExtraTimingOpt (+0.029, on a path #927 does not name; see
  [What binds now](#what-binds-now)).
- Under #818's floor the base misses only 8x8/1if's recipe directive, on setup (+0.011): the edit path the first cut
  takes off.
- The release image meets the release's own floor (+0.553 / +0.023 against +0.03 / 0) and its resource gate passes.
- With the ROM padded to the composed train's size, both split images still meet on the recipe's directive:
  8x8/1if +0.213 / +0.033 at 56.5 RAMB36, 1x1/1if +0.049 / +0.036 at 43.5.

## Linked Issue / roles

Closes #927
Relates to #665

Executor: `[A791]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

### The paths

| Path | Shape, directive at the base | Cause |
|---|---|---|
| `KL_mbx_cdc/u_edit/rq_r[80]` -> `amap_edit_oclaim_{expect,word}_r` CE | 8x8/1if setup +0.011, the recipe's directive, 40 levels on the datapath clock | `amap_edit_out_encode`'s port-and-cluster search (about 27 levels) reads only the request's fields |
| `aaf_clock_meter` `s2_ts_r` -> `grp_ts0_r` | 8x8/1if hold +0.014, the two other directives | a copy with no logic across the clock backbone's centre (0.268 ns of skew); the router fixes hold to 0 and no further |
| `KL_mbx_dma/mask_r` -> `KL_mbx/face_f_fmt_in_lo_r` CE | 8x8/1if setup +0.023 at round 1's cut, the recipe's directive, 12 levels on the bus clock | the mover's `ring_addr_w = base_r + (index_r & mask_r)` is its host address, which `KL_mbx`'s host write decode reads for every register's enable |
| `chan_tdm_render/bank_r` -> `u_fcdc/mem_r` (block RAM) `DIADI` | 1x1/1if hold +0.014, every directive (#925) | a block RAM's write-data hold requirement (about 0.243 ns at the fast corner) against a register written straight into it |

### The cuts

| Commit | Change |
|---|---|
| `a4a0c7dc` | `milan_datapath.sv`: `amap_edit_out_enc_w` comes from a generate. `g_af_amap_enc` (all-fabric) keeps it combinational; `g_sp_amap_enc` (split) registers it. `KL_mbx_cdc_window` changes its fields only on an edge that leaves req low and raises req no earlier than the next edge (`PRE_S`), so the register holds the current request's word in every cycle req is high: no cycle and no stated latency changes. |
| `dfc6ce50` | `KL_aaf_clock_meter.sv`: the group's reference `grp_ref_r` is the next PDU's nominal timestamp, opened by `s2_ts_r + PDU_NS_C` and advanced by `PDU_NS_C`, exact mod 2^32; `pc_ts0_r` is derived from it. No copy is left on the reference, and the outputs are bit-exact. |
| `914d9d48` | `KL_mbx_dma.sv`: the mover's ring address is a register, `ring_addr_r`, loaded with `ring_word(ring_base_i, ring_mask_i, ring_index_i)` at a transfer's start and with `ring_word(base_r, mask_r, index_r + 1)` beside `index_r` at each answer. It equals the old `ring_addr_w` in every cycle, so no cycle and nothing the mailbox contract states changes, and `KL_mbx`'s write decode reads no mask-and-add. |
| `ef87d5c0` | `cdc_pair_fifo.sv` gains `DIST_RAM_P` (default 0): the storage is in `g_mem`, two branches that differ only in `(* ram_style = "distributed" *)`. `KL_tdm_render_master` sets it for its frame crossing (192 bits by 4): 3 RAMB36 become 32 RAM32M, whose write path holds +0.036 in the same routes. The 8x8/1if image builds no TDM render, so only 1x1/1if (and the release, below) changes. |
| `f6037ea4`, `a21e685d`, `3c18b5ec`, `5d098172`, `0297a19a` | The tests and plants below |
| `1010aa6f`, `f6170bf4`, `65c76c13`, `338ece89` | Docs: `MAILBOX_SPLIT.md` (the crossing's registered word, the registered ring address, split mutants 29), `MEDIA_CLOCK_FOLLOWING.md` (the meter's area), the `milan_dp` and `mbx` READMEs (25 plants), the regenerated module matrix, the pair FIFO's parameter doc |

### Tests and planted defects

| Suite | Plant | Caught by |
|---|---|---|
| `milan_dp` `split-mutants` | the window raising req in the clock its fields load | `[EDIT] phase 4: the next beat's held mapping 0 -> 0 is accepted` |
| same | the record's word registered a clock late | same |
| same | the record's word encoded from its stream channel | `[EDIT] the ADD writes cluster 2's word into channel 1` |
| `aaf_clock_meter` `mutants` | the group reference not advanced | `[M2 indep] no history restart` |
| same | the group reference opened without the first PDU | same |
| `mbx` `dma-mutants` | `ring-address-a-step-behind`: the answer's next address computed from `index_r`, not `index_r + 1` | `D1 memory holds the record's bytes in ring order` |
| `milan_dp_render` `tdm8render-mutants` | the render FIFO's distributed storage read at the write pointer | `T6 FIRST EVENT: ...in the frame its timestamp names` and `T6 PRESENTATION` (32 of 32 on a clean clone of `0297a19a`) |

- The split leg's `[EDIT]` checks drive the EDIT window through `KL_mbx`, `KL_mbx_cdc` and the split datapath: phase 4
  beat after beat with verdicts that alternate, a REMOVE and an ADD through every phase with the live map's word
  checked, and the map put back. At this head no split firmware drives the window.
- `ring-index-unwrapped` and `hold-address-moves` are re-anchored on the new code and still caught.
- The render FIFO's plant lives on the branch only the render takes (`PAIRFIFO_SRC`, a `fifo` source kind), so the
  render mutants build a planted copy of the shared FIFO without touching the gPTP or pair-path users.
- `5d098172`'s first plant, the storage *written* at the read pointer, survived the clean-clone run at `338ece89`
  (31 of 32). The render's prefetch drains the crossing before each frame is written, so the two pointers are equal at
  every write and that plant changes nothing the render can show. `0297a19a` replaces it with the read at the write
  pointer, which hands the serializer the frame written three ticks earlier: whole frames, so `T6 IDENTITY` still
  passes, three frames late, so the presentation checks fail.

### What binds now

- **The least hold, 8x8/1if ExtraTimingOpt, +0.029:** `KL_mbx/pub_src_sid_lo_r[0][5][26]` ->
  `KL_mbx_cdc/u_pub/data_hold_reg[1466]`, a copy with 0 logic levels across the clock backbone's centre, with 0.277 ns
  of clock skew at the fast corner. It is the meter pair's shape on the publication crossing's hold register, a path
  #927 does not name; it meets #818's hold floor of 0. On AltSpreadLogic_high the same family is the worst hold at
  +0.034.
- **Setup, on the bus clock:** 8x8/1if's recipe directive is +0.293, inside the CPU's DMA bridge
  (`downW_header_r` -> `pendings_valids_r`). Everywhere else the worst is the CPU bridge's decode into a `KL_mbx`
  register's enable, 11 to 15 levels: the face registers at 8x8/1if (+0.073 on ExtraTimingOpt, +0.058 on
  AltSpreadLogic_high) and at 1x1/1if's recipe directive (+0.081), the event block's `u_evt/tag_r` on 1x1/1if's two
  others (+0.135, +0.126). The datapath clock is +0.771 / +0.865 / +0.865 at 8x8/1if: the edit path binds nowhere,
  and the record mover's family is off every directive's worst list.
- **1x1/1if hold:** the render's `bank_r` -> `u_fcdc/g_mem.mem_r` (now RAM32M) is +0.036 on the recipe's directive;
  the two others' worst is the Ethernet receive converter's block RAM (+0.033).

### Area (placed, each directive's own report)

| Shape | | Base | Round 1's cut `1010aa6f` | Head |
|---|---|---|---|---|
| 8x8/1if, ExtraPostPlacementOpt | LUT | 42,607 | 42,090 (−517) | 41,906 (−701) |
| | FF | 50,722 | 50,642 (−80) | 50,655 (−67) |
| | slices | 15,415 | **15,602 (+187)** | **15,630 (+215)** |
| | BRAM tiles | 92.5 | 92.5 | 92.5 |
| 8x8/1if, ExtraTimingOpt | LUT / slices | 42,604 / 15,082 | | 41,886 (−718) / 15,187 (+105) |
| 8x8/1if, AltSpreadLogic_high | LUT / slices | 42,596 / 15,071 | | 41,896 (−700) / 15,179 (+108) |
| 1x1/1if, ExtraPostPlacementOpt | LUT (as memory) | 31,352 (1,120) | | 31,979 (1,249) |
| | FF | 42,127 | | 42,311 (+184) |
| | slices | 13,309 | | 13,575 (+266) |
| | BRAM tiles | 81 | | 78 (−3) |

- **The slice rise beside the LUT fall.** At 8x8/1if the logic falls on every directive (LUT −700 to −718, FF −67, one
  control set fewer: 2,614 to 2,613), while the slice count rises by +215, +105 and +108. A slice is counted once any of
  its LUTs or flops is used, so the count is the placer's packing, not the logic: on one netlist the base's own count
  moves 344 slices between directives (15,415, 15,082, 15,071), more than any of the head's rises. At 98.6 % of the
  device's slices on the recipe's directive, the timing-driven placer spreads the cut's registers rather than packing
  them.
- **1x1/1if:** the render FIFO is −3 RAMB36, +128 LUTs as memory (32 RAM32M) and +192 flops (its read register now
  in fabric, where the block RAM held it). The rest of the logic LUTs' +498 is spread by synthesis over modules this
  lane does not touch (for example the gPTP shadow +322 and the render queue −242 in the hierarchical report); the
  base's own count moves 693 slices between two directives (13,309, 14,002).
- The base's 8x8/1if figures are this lane's reproduction and #925's routes of the same netlist; 1x1/1if's are
  #925's route of `16ba667d`, whose tree is `70f4056f`.

### ROM

The ROM-fill spread runs each split shape once more on the recipe's directive with 2,168 B of read-only data in the
platform image (read once in `main`, so the link keeps it) and the control memory's budget lifted to 57 tiles, in a
scratch clone only:

| Image | ROM at the head | WNS / WHS | ROM padded | WNS / WHS | Placed BRAM tiles |
|---|---|---|---|---|---|
| 8x8/1if | 56.0 RAMB36 (130,200 B, one bank) | +0.293 / +0.033 | 56.5 (132,376 B: 128 KB + 2 KB banks), as #923's image | +0.213 / +0.033 | 92.5 at both |
| 1x1/1if | 43.0 RAMB36 (117,488 B) | +0.081 / +0.036 | 43.5 (119,664 B) | +0.049 / +0.036 | 78 -> 79 |

- Both meet at both fills. At 8x8/1if the 512-word tail bank maps to LUTs (it is under Vivado's ROM address
  threshold), so the placed count stays 92.5 tiles, as in #923's 56.5 image (92.5, 76 + 33).
- Padded, the worst setup is the bus bridge into `KL_mbx`'s face enables at 8x8/1if (10 levels), and at 1x1/1if
  `KL_mbx/u_evt`'s tick counter into its own reset (19 levels, +0.049).
- The product's firmware is unchanged; neither image at the head is ledgered past 56, so no S14 entry.

### CPU service-budget harness, on the cut's RTL

| Point | Groups | Refusals | Passes over the share | Probe misses | STATED lines | rc |
|---|---|---|---|---|---|---|
| 1x1/1if | 96 | 0 | 0 of 130,341 | 7, all `backlog-owed` | none | 0 |
| 8x8/1if | 95 | 0 | 0 of 270,769 | 7, all `backlog-owed` | `backlog-owed` (ACMP item, declined offer), polls base (`save-second`, `save-held`, `save-starved`) | 1 |

- Every row the harness bounds is within its bound except these, and each is the base's. The base build's
  `backlog-owed` gives the same 7 probe misses at both points (1x1/1if: 61.736 to 63.652 ms against 20 ms) and, at
  8x8/1if, the same STATED lines, `diff` empty. The base's `save-second` gives the same two polls-base lines (22,653
  and 23,164 against 22,500) and the same durable time. These are #914's per-shape statements, as #925 recorded at the
  base (up to 24,499); no stated cost changes.
- The harness built at `5d098172`; no later commit changes its recorded inputs.

### The release image

The release (`endstation_ax7101_1x1_tdm8`, all-fabric) reads the meter, the datapath and the render FIFO, so its
netlist changes: the meter's reference, the all-fabric encode's call site (the same function of the same nets), and
the render FIFO's storage. It reads neither mailbox file. Its integrated route at `338ece89`:

| Figure | The gate's record | Head | |
|---|---|---|---|
| WNS / WHS (worst corners) | +0.44 / +0.036 | +0.553 / +0.023 | the release's floor (WNS >= +0.03, WHS >= 0) met at every corner |
| LUT / FF / slices | 52,012 / 53,707 / 15,780 | 52,042 / 54,238 / 15,836 | within tolerance |
| RAMB36 / RAMB18 / DSP | 74 / 27 / 13 | 71 / 27 / 13 | the render FIFO's 3 RAMB36 |

- `pp_resource_gate.py check --endpoint route-1x1 --shipping-selection`: **PASS**. It recommends a re-baseline
  because RAMB36 improved past its tolerance; the record is not moved here.
- The worst hold, +0.023 at the fast corner, is the protocol processor's `u_aecp/u_resp/lane_ix_r` ->
  `storage_40_reg_0/DIADI`: a register written straight into a block RAM, RTL this lane does not touch.
- The release firmware image is byte-identical to the base's: `bios.bin` and its disassembly, and the ELF and the
  library once their debug sections (build paths) are stripped.

## Authoritative references

- #927 (the task, its scope widening issuecomment-6908876362, the ruling on round 1's STOP issuecomment-6914223799,
  and the scope change issuecomment-6930885657: #818's floor); #919's STOP and its ruling (#919 issuecomment-6907583837).
- #818: the timing floor, setup +0.030 ns and hold 0 at every corner, and the three placement directives.
- S9's image recipe: [MARK_II_AREA_PLAN.md, M8a-2](../docs/design/MARK_II_AREA_PLAN.md) and the M0s recipe at
  `full-split` ([PP_SHADOW_BASELINE_RECIPE.md](../docs/testing/PP_SHADOW_BASELINE_RECIPE.md#selected-placement-measurements)),
  on #818's three placement directives.
- [MAILBOX_SPLIT.md](../docs/design/MAILBOX_SPLIT.md): the face block (contract 2.3, the `EDIT` window and its
  64-cycle bound), the crossing, and the record mover.
- IEEE 1722.1-2021 7.4.45 and 7.4.46 (ADD and REMOVE_AUDIO_MAPPINGS); IEEE 1722-2016 4.4.4.6 and 7.2.4 (the AAF
  timestamps the meter reads).
- CONTRIBUTING.md section 1 (HDL house style, CDC primitives).

## How to get into the same state

```sh
git fetch origin && git checkout --detach 0297a19a
git submodule update --init --recursive
# pinned tools: Verilator 5.050, sv2v v0.0.12, Yosys 0.66, the pinned RV32 SDK, Vivado 2026.1
```

## How to validate

```sh
make -C tb/verilator/mbx all                        # record mover: 520,041 checks, 0 failures; its mutants 25 of 25
make -C tb/verilator/milan_dp split                 # checks: 143, failures: 0 ([EDIT] among them)
make -C tb/verilator/milan_dp split-mutants         # split mutants: 29 of 29 caught by the check each names
make -C tb/verilator/milan_dp split-cdc             # checks: 13, failures: 0
make -C tb/verilator/aaf_clock_meter                # 465 + 6 checks; mutants 38/38 as required
make -C tb/verilator/milan_dp_render tdm8render     # checks: 263, failures: 0
make -C tb/verilator/milan_dp dynmap-mutants        # 71 checks: 71 PASS, 0 FAIL
make -C tb/verilator/milan_dp_render tdm8render-mutants   # 32 checks: 32 PASS, 0 FAIL
python3 scripts/lint_rtl.py --check                 # LINT GATE: PASS (89 <= 89)
# every run: step of rtl-fast.yml, elaborate.yml and docs.yml, each job on a fresh clean clone of 0297a19a:
#   118 steps rc 0, 130 not run with a stated reason (the hosted-only steps), 0 bad
bash scripts/run_all_suites.sh <logs> --wait --shard k/4   # k = 0..3 on four clones of 0297a19a:
#   65 of 65 suites passed, 0 timed out; 2,713,101 checks, 0 in-suite failures
# the split images: S9's recipe (MARK_II_AREA_PLAN.md M8a-2), the integrated run, then the two other directives
# from its synthesis checkpoint; WNS and WHS >= +0.030 ns at every corner
```

Expected result / pass criteria: every suite above passes; each split image meets #818's floor (setup +0.030, hold 0)
at every corner on every directive, and the release image meets its own (WNS >= +0.03, WHS >= 0).

## Known limitations / out of scope

- **#927 is not a flip blocker** (issuecomment-6930885657): it lands after the flip unless the composed flip head
  misses #818 at a split shape, and the cuts are kept for the 8x8/1if setup margin. This lane's own reproduction of
  the base on 8x8/1if's recipe directive is +0.011 setup (round 1; #919's and #920's figure), under #818's +0.030.
- **The least hold, 8x8/1if ExtraTimingOpt +0.029**, is on the publication crossing's hold register, a path #927 does
  not name. No seed, constraint, pblock or directive beyond S9's three, and no floor exception.
- **The base's, unchanged by this lane:** the twin's owed row `split-talker-failed` and the `srp-plus-k` plant's
  escape (`milan_dp twin` and `twin-plants` exit 2 at the base and at the head with the same verdict lines); the CPU
  service budget's 7 `backlog-owed` probe misses at both points and its 8x8/1if STATED lines (above).
- **The release gateware changes** (the meter, the all-fabric encode's call site, the render FIFO's storage); its
  route meets the release's floor and its resource gate passes. The gate's re-baseline recommendation (RAMB36 74 ->
  71) is not taken here: moving `pp_resource_baseline.json` is outside #927.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

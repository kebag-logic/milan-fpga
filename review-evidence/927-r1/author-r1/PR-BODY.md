[A791]

## Contents

- **[Status](#status)** — BLOCKED on a STOP: the timing table at the cut, and `927-8x8-timing` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — The public task, the executor and the reviewers.
- **[Description](#description)** — The base's two paths, the two logic cuts, their tests and what now binds.
- **[Authoritative references](#authoritative-references)** — Requirements, contracts and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and environment.
- **[How to validate](#how-to-validate)** — Reviewer commands and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do, and what is owed.
- **[Definition of Done](#definition-of-done)** — The merge bar.

## Status

**BLOCKED: STOP on #927** (issuecomment-6912069366). Head `1010aa6f` (`927-8x8-timing` -> `dev-soft-core`), five one-line commits on `70f4056f`.

At the cut, the split's 8x8/1if image, through S9's recipe (WNS / WHS at the worst corner, ns; floor +0.030 at every corner):

| Directive | Base `70f4056f` | Cut `1010aa6f` |
|---|---|---|
| ExtraPostPlacementOpt (the recipe's) | +0.011 / +0.034 (this lane) | **+0.023** / +0.036: setup missed on the bus clock |
| ExtraTimingOpt | +0.171 / +0.014 (#919, #920) | +0.234 / +0.036: met |
| AltSpreadLogic_high | +0.215 / +0.014 (#919, #920) | +0.078 / +0.036: met |

Both of #927's paths are cut: the edit-claim enable binds on no directive, and the meter pair no longer holds hold under the floor. The recipe's directive now binds on the record mover's ring address into `KL_mbx`'s host write decode, on the bus clock, a path #927 does not name. The STOP asks whether a third cut, sketched there, belongs in this lane.

## Linked Issue / roles

Closes #927
Relates to #665

Executor: `[A791]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

### The base's two paths (`70f4056f`, before any change)

**Setup: `KL_mbx_cdc/u_edit/rq_r[80]` -> `amap_edit_oclaim_{expect,word}_r` CE**, 40 levels on the datapath clock (`clkout1`, 20 ns).
- `rq_r` is the EDIT window's request register. Bit 80 is record bit 16, the record's `cluster_offset[0]`.
- The first 4 CARRY4 and about 22 LUTs are `amap_edit_out_encode`'s port-and-cluster search, which yields the record's capture-source word and its valid bit. The rest are the verdict's compares, `amap_edit_accept_w` and the claim enable.
- The search reads the request's fields alone. Every later stage reads live state that a beat itself updates (the claims, the owners and clusters, the live map, the streaming levels).
- So a register can remove the search at no cycle cost. `KL_mbx_cdc_window` changes its fields only on an edge that leaves req low, and raises req no earlier than the next edge (`PRE_S`). A cut of the later stages would delay the answer, a change to the mailbox contract's latency, and is not taken.

**Hold: `g_aaf_meter.aaf_clock_meter` `s2_ts_r[6]` -> `grp_ts0_r[6]`**, +0.014 ns on #919's ExtraTimingOpt and AltSpreadLogic_high routes (same RTL).
- Both flops are on one global clock buffer (`BUFG_1`, the PLL's `CLKOUT1`). There is no gated clock, no derived clock and no second buffer.
- They are in adjacent slices across a clock-region boundary (`X43Y99`, `X43Y100`), the clock backbone's centre on this device. At the fast corner the clock reaches the destination 0.834 ns after `BUFG_1` and the source 0.567 ns after it. After 0.410 ns of common-path pessimism removal, that leaves 0.268 ns of skew.
- The data path is a copy with no logic (0.304 ns). The router fixes hold to 0 and no further.

### The cuts

| Commit | Change |
|---|---|
| `a4a0c7dc` | `milan_datapath.sv`: `amap_edit_out_enc_w` comes from a generate. `g_af_amap_enc` (all-fabric) keeps it the combinational `amap_edit_out_encode(...)`; `g_sp_amap_enc` (split) registers it (`amap_edit_enc_reg`). The validator reads it. The `i_ctl_edit_*` port doc and `KL_mbx_cdc_window`'s header state the property the register relies on. |
| `dfc6ce50` | `KL_aaf_clock_meter.sv`: `grp_ts0_r` and `grp_off_r` become `grp_ref_r`, the next PDU's nominal timestamp `ts_0 + i x PDU_NS_C`, exact mod 2^32. It is opened by `s2_ts_r + PDU_NS_C` and advanced by `PDU_NS_C`; the deviation is `s1_ts_r - grp_ref_r`, and `pc_ts0_r <= grp_ref_r - GRP_LAST_NS_C`, derived. No copy is left on the group's reference, and the outputs are bit-exact. Out of context it is 19 flops and 15 LUTs smaller (Yosys). |
| `f6037ea4` | The split leg's `[EDIT]` checks (`sim_split.cpp`, `tb_split_top.sv` probes, all derived from the shape's constants), and three plants in `split_mutants.py` |
| `a21e685d` | Two meter mutants in `tb/verilator/aaf_clock_meter/mutants.py` |
| `1010aa6f` | Docs: `MAILBOX_SPLIT.md` (the crossing; split mutants 29), `MEDIA_CLOCK_FOLLOWING.md` (the meter's area), the `milan_dp` README |

### Tests and planted defects

| Suite | Plant | Caught by |
|---|---|---|
| `milan_dp` `split-mutants` | the window raising req in the clock its fields load | `[EDIT] phase 4: the next beat's held mapping 0 -> 0 is accepted` |
| same | the record's word registered a clock late | same |
| same | the record's word encoded from its stream channel | `[EDIT] the ADD writes cluster 2's word into channel 1` |
| `aaf_clock_meter` `mutants` | the group reference not advanced | `[M2 indep] no history restart` |
| same | the group reference opened without the first PDU | same |

At this head no split firmware drives the EDIT window, so no co-simulation reaches the registered word. The split leg's `[EDIT]` checks drive it through `KL_mbx`, `KL_mbx_cdc` and the split datapath:
- phase 4 beat after beat, with verdicts that alternate;
- a REMOVE and an ADD through every phase, with the live map's word checked;
- the map put back.

### What now binds

On ExtraPostPlacementOpt the worst path is `KL_mbx_dma/mask_r[5]` -> `KL_mbx/face_f_fmt_in_lo_r[0][14][*]` CE, +0.023 ns, 12 levels, on the 100 MHz bus clock.
- At the base's run of this directive the same family was +0.133 ns.
- The record mover's `ring_addr_w = base_r + (index_r & mask_r)` is its default host address, which `KL_mbx`'s host write decode reads for every register's enable.

## Authoritative references

- #927 (the task); #919's STOP and its ruling (#919 issuecomment-6907583837).
- S9's image recipe: [MARK_II_AREA_PLAN.md, M8a-2](../docs/design/MARK_II_AREA_PLAN.md) and the M0s recipe at `full-split` ([PP_SHADOW_BASELINE_RECIPE.md](../docs/testing/PP_SHADOW_BASELINE_RECIPE.md#selected-placement-measurements)), on #818's three placement directives.
- [MAILBOX_SPLIT.md](../docs/design/MAILBOX_SPLIT.md): the face block (contract 2.3, the `EDIT` window and its 64-cycle bound) and the crossing.
- IEEE 1722.1-2021 7.4.45 and 7.4.46 (ADD and REMOVE_AUDIO_MAPPINGS); IEEE 1722-2016 4.4.4.6 and 7.2.4 (the AAF timestamps the meter reads).
- CONTRIBUTING.md section 1 (HDL house style, CDC primitives).

## How to get into the same state

```sh
git fetch origin && git checkout --detach 1010aa6f
git submodule update --init --recursive
# pinned tools: Verilator 5.050, sv2v v0.0.12, Yosys 0.66, the pinned RV32 SDK, Vivado 2026.1
```

## How to validate

```sh
make -C tb/verilator/milan_dp split            # checks: 143, failures: 0 ([EDIT] among them)
make -C tb/verilator/milan_dp split-mutants    # split mutants: 29 of 29 caught by the check each names
make -C tb/verilator/aaf_clock_meter           # 465 + 6 checks; aaf_clock_meter mutants: 38/38 as required
python3 scripts/lint_rtl.py --check            # LINT GATE: PASS (89 <= 89)
# the split images: S9's recipe (MARK_II_AREA_PLAN.md M8a-2), the integrated run, then the two other directives
# from its synthesis checkpoint; WNS and WHS >= +0.030 ns at every corner
```

Expected result / pass criteria: every suite above passes, and each image meets the floor on all three directives. At this head 8x8/1if does not (the STOP).

## Known limitations / out of scope

- **The STOP:** the recipe's directive misses by 0.007 ns on a mailbox path #927 does not name. The decision is the ruling's.
- **The release gateware changes:** the meter is in every shape, and the all-fabric datapath's elaboration moves the encode's call site (placement_identity's digest changes; the logic is the same). The release image's route is owed. The release firmware image is byte-identical.
- **Not run at this head:** the 1x1/1if routes, the release route and the native sweep (each owed at the ruling's head), and the 8x8/1if budget harness (stopped). The harness's recorded inputs include no file this head changes.
- No seed, constraint, pblock or directive beyond S9's three, and no floor exception.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

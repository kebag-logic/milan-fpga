# HANDOFF round 2 — [A789] lane 923 (#923 + #924) — REVIEW READY at `70c100da` (#923 issuecomment-6928332881)

Ruling: #923 issuecomment-6906679024, (A). Branch `923-aecp-maps`, base `16ba667d`, local only (the manager pushes).
Commits: `10264ac2`, `def26a61` (round 1); `6abb6cc6`, `679b4a44`, `6effb796`, `ac716674`, `13e7bed2`, `1e94b301`,
`e628d35a`, `70c100da` (round 2). Head `70c100da`, tree clean, nothing pushed.

**STOP** (round2/STOP-COMMENT.md, posted once as #923 issuecomment-6922227027): the 1x1/1if split image misses
WHS >= +0.030 ns on all three of S9's directives (+0.015 / +0.014 / +0.014 at the fast corners), always on the
datapath's TDM render FIFO crossing (`chan_tdm_render/bank_r` -> `u_fcdc/mem_r` DIADI, 0 levels); the base `16ba667d`
misses the same way (+0.014, the same crossing). The question: record it as #927's, as #919's ruling did, or hold
1x1/1if to the floor here (a seed, a directive or a datapath cut, none this lane's). Recommendation (A): #927's.
**Ruling** (#923 issuecomment-6923091710, (A)): the 1x1/1if TDM render FIFO crossing is #927's (its scope widened in
issuecomment-6908876362); the 1x1/1if routes are recorded as misses at the base, owed to #927; no seeds, no further
directives; route again only if the gateware changes. The rest of round 2 stands: the 8x8/1if base route (done), the
remaining gates and the sweep, then REVIEW READY. Standing rule: a miss on a path #927 names, reproduced at the
base, is owed to #927 and is not a STOP; the 8x8/1if base's EPPO setup miss (+0.011, `KL_mbx_cdc/u_edit/rq_r` ->
`amap_edit_oclaim_expect_r` CE) is one of them, and the head meets there.

## 1. Round-2 changes (file:line at `70c100da`, reason)

| File:line | Change | Reason |
|---|---|---|
| `sw/litex/ctrl_memory.py:278` | new `LEDGERED` entry `platform-8x8-one-interface`: `nvm_stage` 13,594, `ctrl_plat` 18,240, 56.5 RAMB36, "S14 debt", 1,280 B of rom | ruling (A): the shipping 8x8/1if image plans its measured 56.5 |
| `sw/litex/ctrl_memory.py:251`, `:264` | the size fixture's 8x8/2if entry 59.0 -> 59.5; the platform's 8x8/2if 60.5 -> 61.0, `ctrl_plat` 20,352 -> 20,416 | ruling: both raised to their measured figures (the 60.5 cap superseded by the owner's 11-15 rule until S14) |
| `sw/litex/ctrl_memory.py:288` | `own_point(image)`: the ledgered point whose every symbol size the image carries, else None | the product build plans a ledgered image at its own entry by its symbols |
| `sw/litex/milan_soc.py:3345` | `add_ctrl_memory` plans with `ledgered=own_point(image)` | as above; an unledgered image is still refused past 56 |
| `sw/litex/ctrl_memory_ledger.py:34-88,139-145` | `PRODUCT`, `PLAT_8X8_2` 20,416, OWN/HELD at 59.5 / 61.0 / 56.5, refused rows half a tile past each entry, planted ledger edits | the ledger's arms follow the entries |
| `sw/litex/test_ctrl_memory.py:20,236-240,319-356,778,849` | the SoC build plans each OWN image at its own entry; refuses each half a tile past, an unledgered 8x8 image at 56.5 with another `ctrl_plat` and with none; property "own entry", 3 mutants | tests for the new product path |
| `tb/verilator/ctrl_split_boot/plat_ledger.py:63,213-236` | the 8x8/1if point links with `--ledgered-point platform-8x8-one-interface`; controls retargeted | the platform ledger gate follows the entry |
| `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 | the three-entry ledger; "Since #923" and the per-file growth table | the fit page |
| `tb/verilator/ctrl_service_budget/edit_rows.py:40` | 1x1/1if one-row edit 260 -> 295 us | the answering-ports arm's REMOVE of one output row with its commit, 27,866 cycles (278.7 us; +5 %, up to 5 us = 295); arm A's 26,177 (275) |
| `sw/firmware/ctrl/test/test_aecp.cpp` (`Core.TheStoresResetSetIsTheClippedOne`), `aecp_map_mutants.py` row `restore-refused-reset-unclipped` | a refused restore removal of a port whose reset set the formats clip keeps the clipped set; its plant (the kept filter cut in `reset`) caught by name | `fw_coverage.py --check` found `aecp_maps.c:613`'s false arc untaken (418/419 branches) |
| `sw/firmware/gtest/coverage.ratchet` | the six changed files' totals (aecp_commands, aecp_face, aecp_maps, aecp_mbx, ctrl_app_aecp, mbx), each 100 % | `--write` on a clean clone of `6effb796`; `srp_mbx.c`'s stale record (from `f14e56a9`, not this lane's) left as it is |
| `tb/verilator/ctrl_service_budget/rows_tiers.py` | back to the base's text (its 1,000-line module limit) | `679b4a44`'s 2-line comment had made it 1,002 lines (`check_py_idiom.py` long module 11 > 10); the 975 us still comes from the larger kept, 92,766 |
| `tb/verilator/ctrl_service_budget/split_soc.py:498-507`, README:50 | `ledgered_plan`'s plan takes the SoC build's `ledgered=` and plans the harness's named point in its place | `6abb6cc6`'s `add_ctrl_memory` passed `ledgered=` and the patch passed it again: TypeError at the 8x8 (2if) point of the budget harness (and the hooks harness, same patch) |
| `tb/verilator/ctrl_service_budget/split_soc.py:242-258` | `slowest_edit`'s verdicts a constant on the port (`Replicate(Constant(1, 64), n_if)`) | at two interfaces migen emitted the per-interface slices as a comb block of constants, which the simulation never ran, so the data stayed 0 and every map edit read refused (NOT_SUPPORTED); found by the 8x8 (2if) run (REMOVE status 11, no notifications) and proven by an instrumented scratch build (status 17: the begin answered, verdict 0); at one interface the old code was `assign ... = 1'd1`, the same 64-bit 1 |
| `tb/verilator/ctrl_service_budget/edit_rows.py:32-42` (`e628d35a`) | the 8x8/2if one-row member 325 -> 355 us | measured with the commit at 8x8/2if, 33,481 cycles (28,627 at the base); `EDIT_RECORD_US` stays 595 (SET_CONFIGURATION's), so no tier input moves |
| `docs/design/SPLIT_CONTROL_MEMORY.md` section 13 "The map edits' commit (#923)", "The command, under #904", "The record classes graded (#895)"; `docs/reference/FR_NFR.md` | the commit's records at both points against the base; #895's head's figures attributed to #895's head; FR_NFR's paced members at 275 / 295 us | the docs' "head" figures had become stale with the commit |
| `sw/firmware/ctrl/README.md:255` (`70c100da`) | 183 -> 185 pin controls | `ctrl_boundary.py` (firmware-verilator, firmware-boundary jobs) counts one control per Makefile target that reaches the stack: the two `twin-maps` targets |

## 2. Findings this round (all fixed in the lane)

1. Coverage gap (`aecp_maps.c:613`), fixed in `6effb796`.
2. Module length (`rows_tiers.py` 1,002 lines), fixed in `6effb796`.
3. Harness TypeError at 8x8 (2if) from `own_point`, fixed in `ac716674`.
4. Harness EDIT verdict 0 at two interfaces, fixed in `1e94b301` (harness only; firmware unchanged, so the images,
   ROM and 1x1/8x8-1if measurements stand).
5. The 8x8/2if one-row edit past its stated member (355 against 325), restated in `e628d35a`.
6. The firmware page's pin-control figure, fixed in `70c100da` (found by the workflow pass at `e628d35a`).
7. The 1x1/1if timing miss (the STOP): not fixable in this lane.

Correction to round 1: `twin-maps` has 20 checks, not 21 (round 1's STOP and draft PR body said 21; its receipt has
20). Stated in the round-2 STOP.

Observed, not this lane's: `test_ctrl_firmware_shards.py:42` leaves `dispatch-build/` in the tree (DIRTY-after 2 on
the firmware shard runs); `coverage.ratchet` records `srp_mbx.c` at 736/663 where it measures 741/669 (100 %); the
control-memory plan counts a 2 KiB rom bank as a RAMB18 (half a tile) where the routed image places it as a RAMB36
(1x1/1if: RAMB36 63 -> 64, RAMB18 36 unchanged).

## 2b. Gate table (round 2)

| Gate | Head | Result | Receipt |
|---|---|---|---|
| Full arm A at 1x1/1if, 3 parts, 93 groups (+ the edit groups) | def26a61 firmware = head's | 0 refusals; budget misses only the 7 `backlog-owed` held-egress rows (base's, ruled); 0 passes over the share | budget/full-armA-1x1-*.txt |
| Full arm A at 8x8/1if, 3 parts (reported point) | same | 0 refusals; the same 7 `backlog-owed` rows; 0 passes over the share; STATED reports of the shape's costs past 1x1/1if's statements (polls base 22,829-23,775 against 22,500; ACMP items 6,270-7,208 against 5,500; declined offers 2,277-2,310 against 2,000), the point's purpose (harness README:49) | budget/full-armA-8x8-1if-*.txt |
| `record_classes.py` over every leg at both points | head tables | RESULT PASS (1x1/1if held: long 975 of 975, paced 295 of 300, ordinary 210 of 235) | budget/record-classes-every-leg-both-points.txt |
| `rows_tiers.py`, `load_grade.py --check`, `flip_grade.py --check --point 1x1/1if`, their self-tests, `record_classes.py --selftest` | e628d35a | tier table identical to the base's; load PASS; flip PASS; 1033/1033, 26/26, 585/585, 11/11 | (foreground) |
| Answering-ports and arm A edit legs, base and head, 1x1/1if, 8x8/1if, 8x8/2if | 1e94b301 / 16ba667d | see section 3 | budget/ |
| Release image | 679b4a44 | byte-identical | release/ |
| Six head routes | 6abb6cc6 | 8x8/1if meets on all three; 1x1/1if hold under on all three (STOP) | route/ |
| Workflow pass on clean clones (wf/run-e628d35a) | e628d35a | 3 bad: firmware-verilator and firmware-boundary (the pin-control figure, fixed in 70c100da); publication-census (sv2v's 900 s wall clock under load) | workflows/verify-e628d35a.md |
| AECP campaign (workflow job) | e628d35a | 329 of 329 caught | (scratch) |
| Coverage ratchet (workflow job) | e628d35a | PASS, 39 files | (scratch) |
| ctrl_hot, baremetal-only, cpp/py/sh idioms, docs_check, doc paths, doc style, diff --check | 70c100da / e628d35a | rc 0 each | (foreground) |
| Workflow pass on clean clones (wf/run-70c100da) | 70c100da | verify_wf.py: 118 steps rc 0, 130 not run with a reason, 0 bad (AECP 329/329, SRP 421/421, control 716/716; census PASS, self-test 0 of 163 arms failed; elaborate-gates-1 on its rerun) | workflows/verify-70c100da.md |
| 4-shard native sweep | 70c100da | every shard exit 0: 65 suites PASS, 2,713,040 checks, 0 failures, none timed out | sweep/ |
| twin-maps, twin-maps-plants | 70c100da | 20 checks PASS; the no-edit plant fails its 3 checks by name | twin/twin-maps-70c100da.txt |
| Base routes at ExtraPostPlacementOpt | 16ba667d | 1x1/1if +0.208 / +0.014 (the TDM crossing); 8x8/1if +0.011 / +0.034 (#927's edit-claim enable) | route/base-* |

## 3. Costs (base `16ba667d` -> head, CPU cycles; receipts/budget/)

| Record | Arm, point | Base | Head | Head by the rule | Stated |
|---|---|---:|---:|---:|---:|
| largest legal command | answering-ports 1x1/1if | 86,698 | 92,714 | 975 | 975 (LONG_RECORD_US) |
| largest legal command | arm A 1x1/1if | 86,556 | 92,489 | 975 | 975 |
| one-row REMOVE (output) | answering-ports 1x1/1if | 23,877 | 27,866 | 295 | 300 (class), member 295 |
| one-row REMOVE (input) | arm A 1x1/1if | 21,543 | 26,177 | 275 | 300 (class) |
| one-row REMOVE (output) | answering-ports 8x8/2if | 28,627 | 33,481 | 355 | 595 (class), member 325 -> 355 |
| largest legal command | answering-ports 8x8/2if | 126,152 | 132,751 | 1,395 | 1,650 |
| accepted SET_CONFIGURATION | answering-ports 8x8/2if | | 55,928 | 590 | 595 |
| largest legal command | answering-ports 8x8-1if (reported, not held) | 162,969 | 169,021 | 1,775 | none held |

Share (answering-ports, aecp-largest-notice): at 8x8/1if (reported) base 2 of 106 passes over 2 ms (longest
223,194), head 2 of 107 (228,776); at 8x8/2if base 2 of 140 (233,702), head 2 of 140 (240,969): not new. At 1x1/1if
no pass of any group is over it. 8x8/1if's STATED polls base in save-held is the base's too (23,756 base, 23,775 head).

## 4. ROM, device RAMB36, area, timing (receipts/route/)

Six head routes, S9's recipe (`round1/scripts/image.sh`), firmware `6abb6cc6` (identical to the head's), one at a
time through vivado-slot.sh; sign-off by `round1/scripts/signoff.py`; the identity gate rc 0 on each.

| Image | Directive | WNS / WHS, ns (worst corners) | Floor +0.030 | LUT / FF | Block RAM tiles (of 135) |
|---|---|---|---|---|---|
| 1x1/1if | ExtraPostPlacementOpt | +0.256 / +0.015 | hold under | 31,278 / 42,119 | 82 (64 RAMB36 + 36 RAMB18); control memory 43.5, fabric 38.5 |
| 1x1/1if | ExtraTimingOpt | +0.126 / +0.014 | hold under | 31,327 / 42,119 | 82 |
| 1x1/1if | AltSpreadLogic_high | +0.195 / +0.014 | hold under | 31,320 / 42,119 | 82 |
| 8x8/1if | ExtraPostPlacementOpt | +0.295 / +0.036 | met | 42,659 / 50,758 | 92.5 (76 + 33); control memory 56.5 (its own entry), fabric 36 |
| 8x8/1if | ExtraTimingOpt | +0.034 / +0.035 | met | 42,740 / 50,756 | 92.5 |
| 8x8/1if | AltSpreadLogic_high | +0.047 / +0.035 | met | 42,752 / 50,757 | 92.5 |
| 1x1/1if at the base `16ba667d` | ExtraPostPlacementOpt | +0.208 / +0.014 | hold under, the same crossing | 31,352 / 42,127 | 81 (63 + 36); control memory 43.0 |
| 8x8/1if at the base `16ba667d` | ExtraPostPlacementOpt | +0.011 / +0.034 | setup under (#927's path) | 42,607 / 50,722 | 92.5 (76 + 33); control memory 56.0 |

- 1x1/1if: the one path under the floor, on every directive and at both fast corners, is
  `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/bank_r_reg[3][22]` -> `u_fcdc/mem_r_reg_1/DIADI[22]`
  (0 levels), the TDM render FIFO crossing #919's round 2 recorded as #927's (receipts/route/1x1-timing-miss.txt).
  This is the STOP (round2/STOP-COMMENT.md).
- The 1x1/1if export against the base's (receipts/route/export-base-vs-head-1x1.txt): only the control memory differs
  (one 2 KiB rom bank more and the rom's contents); no RTL, constraint or generator input changed.
- Area delta at ExtraPostPlacementOpt, 1x1/1if: LUT -74, FF -8, Slice +46, Block RAM tiles +1 (one RAMB36). 8x8/1if: LUT +52, FF +36, Slice +254, Block RAM tiles 0 (92.5 at both, 76 RAMB36 + 33 RAMB18: the plan's 56.0 -> 56.5 takes no further tile on the device). The base 8x8/1if route at that directive misses setup, +0.011 ns, #927's edit-claim enable path; the head meets on all three directives.
- The base 8x8 route's first run was refused at once: its stand-in ELF was the head's image (56.5), past the base's
  budget. It reran with the base harness's 8x8-1if image as the stand-in (the CSR export pass only).

## 5. Release image

`679b4a44`: bios.bin byte-identical to the base at both configs; bios.elf stripped identical (receipts/release/).

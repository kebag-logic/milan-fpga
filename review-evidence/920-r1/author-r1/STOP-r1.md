[A786] STOP: the 8x8/1if split platform image misses the timing floor at all three directives
Branch: `920-save-burst`, head `54280c94` (code as `f1f7c3e8`; `54280c94` corrects one doc figure).

**The miss.** S9's recipe, one build at a time. Every build has 0 failing endpoints and passes the identity gate.

| 8x8/1if directive | WNS, slow corners | WHS, fast corners |
|---|---|---|
| ExtraPostPlacementOpt (the recipe's) | +0.011 | +0.034 |
| ExtraTimingOpt | +0.171 | +0.014 |
| AltSpreadLogic_high | +0.215 | +0.014 |

- The floor is WNS and WHS >= +0.030 ns at every corner. No build meets it.
- Two builds meet the issue's floors (WNS >= +0.030, WHS >= 0).
- The two hold misses are one path inside `milan_datapath`: `g_aaf_meter.aaf_clock_meter` `s2_ts_r_reg[6]` -> `grp_ts0_r_reg[6]`, on clkout1.
- The setup miss is `KL_mbx_cdc/u_edit/rq_r_reg[80]` -> `milan_datapath/amap_edit_oclaim_expect_r_reg[599]` (CE).
- This change has no RTL. The image differs from the base only in its firmware's bytes: 129,928 B of `rom` where the base has 129,624, in the same 56.0 RAMB36.
- **The base misses identically.** The base's own 8x8/1if image (`659d7687`), built at the recipe's directive, gives the same figures on the same paths: WNS +0.011 and WHS +0.034. The route does not see the firmware's bytes, so the miss is the base's.
- 1x1/1if meets at all three directives. The best is ExtraTimingOpt: WNS +0.133, WHS +0.036.

**Decision needed.** Which of these should apply to the 8x8/1if image?
- accept it at ExtraTimingOpt's or AltSpreadLogic_high's figures;
- run another directive or seed;
- owe the 8x8/1if image's timing to another issue, since the base misses with the same figures.

This round does not choose.

**Everything else, for the decision.**
- **The cause, proved before the fix.** The AECP owner's pending marks held 256 ids. Layout 3 puts the names at id 222 and up, so every name from ordinal 34 on was never delivered to the store. At 1x1/1if those are the five names the rehearsal lost. Three receipts show it at the base:
  - a unit test;
  - the save harness (1x1/1if loses names 34 to 38; at 8x8/1if the CPU traps);
  - the board on its current image: before the cut the store's console bits read backed, nothing dirty, nothing pending, verdict OK.
- **The fix.** `945a1217`: pending bits over layout 3's id space. `c1a24c18`: the ruling's three mechanisms only (a change joins the running capture; the next save starts at the first idle step; a step a pass in passes that took no input).
- **The target, met at both shapes under the held load.**

  | Group | 1x1/1if | 8x8/1if |
  |---|---|---|
  | `save-burst`, latest name to durable after its response | 1,101.7 ms | 1,367.5 ms |
  | `save-burst`, the cut's container | every name | every name |
  | `save-flight`, to durable after its response | 158.5 ms | 657.7 ms |
  | `save-flight`, steps to the next save's erase | 19 (want 19) | 59 (want 59) |

- **The budget harness, every group.**
  - 1x1/1if: exit 0, 0 refusals, 0 of 142,535 passes over the share.
  - 8x8/1if: 0 refusals, 0 of 251,469 passes over the share.
  - At both points the only row misses are the seven held-egress rows, as at the base.
  - 8x8/1if exits 1 on stated-cost lines, as it does at the base. This base keys the statements on the interface count, so 8x8/1if is held to 1x1/1if's. Every such line is within #914's own 8x8/1if statements; the tightest is the polls base, 23,251 of 23,500 cycles.
- **Controls caught by name.** `store-names-past-256-lost` and `store-next-save-waits` at 1x1/1if; `store-step-only-owed` at 8x8/1if. The capture's join has no harness control: without it the burst still meets 5 s (7 saves instead of 6). The store's units hold the join.
- **Gates.**
  - Harness self-test: 0 failures, 251 of 251 mutants caught.
  - Store suite with its mutants: 546 tests at 5 shapes, all 152 planted defects caught.
  - Firmware jobs: 0 failed steps in each (unit, with `fw_coverage --check` passing; the AECP, control and SRP mutant campaigns; verilator; boundary).
  - Docs jobs: 0 failed steps. Elaborate jobs: 0 failed steps, all 8 LiteX simulations passing.
  - Suite sweep: not run before this post, because no CPU range on the shared host came free during the gate run. It runs once one does, and its result goes to the round's record.
  - Load gate: 1x1/1if at 0.516 of 0.70.
  - Python idiom, docs, style and paths checks: pass.
  - Memory ledger: pass.
- **ROM.** Each image grows by 296 to 304 B. The target platform's 8x8 two-interface image is 131,224 B, ledgered at 60.5 RAMB36 as S14 debt (`11860de2`).
- **Ruling item 4.** #919 had no review head; the sync onto it is still open.

[A585] STOP
Head: `99a5a2ac6fbbf1268f57008b42b5b26ccf6ae731` (branch `708-pin3`, base dev `554e61d2`, not pushed)
Condition: route below the floor (assignment STOP condition; acceptance 2).

The shipping `route-1x1` of the adopted image (processor `2cbed0a9`) does not meet the WNS floor. It was measured with the recipe's default directives (`ExtraPostPlacementOpt`, one synthesis worker, the record's flow identity, Vivado 2026.1).
- **WNS +0.025 ns** at Slow_0C and Slow_85C, against the +0.030 ns floor. The 0.274 ns fall from the +0.299 ns record also exceeds the 0.25 ns limit.
- `pp_resource_gate.py check --endpoint route-1x1` exits 1: `REGRESSION: below the floor 0.03`.
- The route is otherwise complete: 100,885/100,885 nets routed, 0 routing errors, no negative-slack path at any corner. WHS is +0.015 ns (Fast corners), the IOB pack check passes, and there is no CRITICAL WARNING.

| route-1x1 | LUT | FF | Slice (of 15,850) | RAMB36/18 | DSP | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|
| record `a5ca6e51` | 50,267 | 54,413 | 15,779 | 74/27 | 14 | +0.299 / +0.031 |
| adopted | 49,787 | 54,172 | 15,831 | 74/27 | 14 | **+0.025** / +0.015 |

- **Worst setup path:** SoC side, `milansoc_crg_clkout0`, from `FSM_sequential_subfragments_fsm0_state_reg[0]` to `milansoc_tmod0_reg[10]/CE`. It has 10 logic levels, and 78 % of its 9.808 ns is routing. It is not a processor path.
- **Placement:** 19 slices are free; the record had 71.
- **Standalone syntheses:** both pass the gate. `ooc-1x1` is +135 LUT / +42 FF, and its ungated WNS moves from -3.562 to +3.884 ns (processor #166). `ooc-8x8` is +76 / +71.
- **Attribution:** the candidate and base exports differ only in the six processor RTL files the pin changes. Base and a fresh export of `a5ca6e51` differ only in a comment-only RTL change. ROM images are identical.

**Done, all rc 0** (expected control failures excepted):
- `parent-name-evidence.patch`; without it the test-evidence check exits 1.
- F3 normalisation retired in `acmp_walk.cpp`, where LD1 to LD3 are now controls. The new walk fails each of them by name against processor `2ad2f845`, and passes 127/127 at `2cbed0a9`.
- Control-firmware campaign: 471/471 mutants caught.
- ROM digests (unchanged contents), pin page, boundary diagram and port census re-recorded through their generators. The naming record is unchanged.
- Docs workflow: 48/48 steps, plus the no-git job.
- BDD: 404 scenarios. Lint: identical to base.
- `check_nvm_capture.py` passes. The firmware digest did not move, so the capture was not re-measured.

**Not run after the STOP:**
- the 61-suite sweep, the processor and gPTP sweeps, Yosys, `xvlog` and the builder elaboration bank;
- the recipe's other two directives and the image build;
- `record --write`. The gate record is unchanged.

**Needs a ruling:** how the route is to meet the floor, for example the other two directives (a flow-identity change), a placement change, or a processor-side change.

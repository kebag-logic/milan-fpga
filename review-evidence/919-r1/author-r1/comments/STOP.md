[A785] STOP — the 8x8/1if split image misses the timing floor on all three directives

Head: 55769f09 (nine commits on dev-soft-core 659d7687, 437b2bd4 to 55769f09; nothing pushed, no PR).
Stop condition: a timing miss after the three directives.

**The miss.** The 8x8/1if split platform image, built and routed with S9's recipe, measured against WNS and WHS >= +0.030 ns at every corner:

| Directive | Worst WNS / WHS, ns | Under the floor |
|---|---|---|
| ExtraPostPlacementOpt (the integrated run) | +0.011 / +0.034 | setup |
| ExtraTimingOpt | +0.171 / +0.014 | hold |
| AltSpreadLogic_high | +0.215 / +0.014 | hold |

Every net is routed with 0 routing errors and 0 failing endpoints, and every other corner value clears the floor. 1x1/1if (the shipping point) meets on all three directives. The best there is ExtraPostPlacementOpt at +0.390 / +0.058, then ExtraTimingOpt +0.177 / +0.036 and AltSpreadLogic_high +0.113 / +0.036.

**Why I don't think this change's logic causes it (evidence, not a ruling):**
- The RTL is unchanged. The 8x8/1if export at the head is identical to the base's (659d7687) except for the ROM's contents: one 32,768-word bank at both, the same integrated script, the same constraints.
- ExtraPostPlacementOpt's setup path is `KL_mbx_cdc/u_edit/rq_r[80]` -> `milan_datapath/amap_edit_oclaim_{expect,word}_r[599]` clock enable, 40 levels. That is the family that held #810's 8x8/1if ExtraPostPlacementOpt to +0.001.
- The hold path under ExtraTimingOpt and AltSpreadLogic_high is a single register pair inside `milan_datapath`: `g_aaf_meter.aaf_clock_meter/s2_ts_r[6]` -> `grp_ts0_r[6]`, 0 levels, 0.268 ns of clock skew, at the fast corner.
- #810's 8x8/1if route (084cf7a8, the same RTL, a different ROM banking) met on ExtraTimingOpt (+0.292 / +0.036) and AltSpreadLogic_high (+0.093 / +0.036).

**Decision needed.** Is this placement variance on an unchanged netlist accepted for #919? If not, who runs what further work (seeds, a directive beyond S9's three, a hold constraint, S14)? I have attempted none of it.

**Every other gate at this head:**
- Workflow jobs (rtl-fast, elaborate, docs), each on a fresh clean clone of 55769f09: 114 steps rc 0, 130 not run with a stated reason (the hosted-only steps). `firmware-srp-mutants` and `firmware-control-mutants` were still running when this was posted; their results go in the lane's handoff.
- Split boot simulation: rc 0 at 1x1/1if and 8x8/1if; the self-test rc 0, with the PHY's two plants caught; the platform ledger rc 0 at every point. The PHY figures equal the earlier run's at bdd44f96: a frame at most 14,537 CPU cycles (145.37 us) against the stated 155 us, a poll every 125 ms, and the return published 126.2 ms after the link.
- Release image: byte-identical at base and head, both shapes (`bios.bin` and its disassembly). The release build reads no file changed after that check.
- CPU service budget harness at 1x1/1if and 8x8/1if: still running. It runs at ec5bd171, and no input it builds from has changed since; the result goes in the handoff.
- Native Verilator sweep: not started. It is the one remaining gate, and I start no new long gate after a stop.
- ROM: 1x1/1if 43.0 RAMB36 (base 42.5); 8x8/1if 56.0 (56.0), with 4 B of `rom` left before 56.5. 8x8/2if 60.5 (60.0): the entry is raised to the owner's cap, and the 4.5 RAMB36 is named S14 debt.
- Area: 1x1/1if's netlist differs from the base's only in `rom_bank3`, 512 -> 1,024 words (+0.5 BRAM tile) and its decode. 8x8/1if differs only in the ROM's contents.

[A700d] REVIEW READY
Commit: `667b9bbc02b99a08d71efab750f95e8702cbbe57` (unchanged: route only, and the route shows no defect, so there is no commit this round; base dev `1e80128f`, still the live dev tip; processor pin `a9e84b66`)
Changed: nothing in the tree. Measured: route-1x1 at the head, recipe unchanged, Vivado 2026.1, default seed. One synthesis, then the recipe's three placement directives in parallel from its checkpoint.
Validation:
- `pp_resource_gate.py check <shipping> --endpoint route-1x1 --comparison <AltSpreadLogic_high> --comparison <ExtraTimingOpt>`, with PR #820's gate at `32f0d9b5` used from scratch and not committed: rc 0, `RESULT: PASS`, `directive ExtraPostPlacementOpt selected: the best worst-corner WNS, 0.165 ns`. LUT 51,568 (-444 against the record), FF 53,680 (-27), slices 15,749 (-31; 101 free), RAM and DSP unchanged. WNS fell 0.275 ns from the +0.440 ns record, printed as the #818 WARNING (reported, never gated). The comparisons reversed give the same selection and verdict.
- Per directive (WNS Slow 0C / 85C, Fast 0C / 85C; WHS Slow / Fast; TNS and THS 0 everywhere):
  - ExtraPostPlacementOpt: +0.165 / +0.165, +1.565 / +1.565; +0.102 / +0.036; 51,568 LUT, 53,680 FF, 15,749 slices (101 free)
  - AltSpreadLogic_high: +0.151 / +0.151, +1.331 / +1.331; +0.061 / +0.032; 51,520 / 53,682 / 15,837 (13 free)
  - ExtraTimingOpt: +0.120 / +0.120, +1.331 / +1.331; +0.101 / +0.036; 51,524 / 53,680 / 15,837 (13 free)
  - Every route: RAMB36 74, RAMB18 27, DSP 13, Block RAM tiles 87.5 (ceiling 121.5), route complete with 0 routing errors.
- Worst setup path, all in the 100 MHz `sys` clock, in SoC memory-path logic this PR does not change:
  - ExtraPostPlacementOpt: `milansoc_write_w_buffer_readable_reg` -> `storage_15_reg_1/ENARDEN`, 10 levels, 83 % route
  - AltSpreadLogic_high: `milansoc_write_w_buffer_level0_reg[0]` -> `storage_10_dat1_reg[20]/D`, 12 levels
  - ExtraTimingOpt: `FSM_sequential_subfragments_fsm2_state_reg[0]` -> `milansoc_tmod1_reg[11]/CE`, 16 levels
- Delta against dev's own #814 round 1 routes (the same gate passes them, ExtraPostPlacementOpt at +0.303 ns):
  - WNS: ExtraPostPlacementOpt +0.303 -> +0.165 (-0.138), AltSpreadLogic_high +0.230 -> +0.151 (-0.079), ExtraTimingOpt +0.106 -> +0.120 (+0.014)
  - WHS: +0.028 -> +0.036, +0.014 -> +0.032, +0.054 -> +0.036
  - LUT -233 / -326 / -309; FF -80 / -77 / -78; slices -85 / +42 / +43
- This PR's own logic in the route: `KL_reboot_ctrl` is 46 LUTs and 34 FFs. The frame-end toggle crossing is under the 8 ns datapath-only bound (pair +5.87 ns, 51 endpoints against dev's 50). The CDC report gains one ASYNC_REG synchroniser (the PHY hold into `sys`) and is otherwise dev's. check_timing is identical to dev's. ICAPE2 and STARTUPE2 are placed.
- `python3 scripts/xvlog_gate.py --check`: rc 0, 0 findings == ratchet, over 85 hdl/ and 52 pinned-processor files, the three changed RTL files among them.
- IOB packing: `IOB-PACK OK: 22 port(s) ... none unpacked` on all three directives; `python3 sw/litex/iob_pack_selftest.py` rc 0 (22 arms, 21 mutants).
- #607 log check (`check_implementation_log`) on each of the three route logs: rc 0, no 12-4739, 20-1307 or 12-5201 diagnostic. A copy with one planted 12-4739 line is refused (rc 1).
- One harness error came before any measurement. The first launch stopped at elaboration because my prep script had removed the checkout's ROM artifact links. They were restored, and the run relaunched into the same export.
Acceptance criteria: round 3 met. None of its STOP conditions holds: the best directive is at +0.165 / +0.036 ns, every run placed and routed, and no LUT, FF, slice or BRAM ceiling is exceeded. The area record was not re-recorded (the record rule). Issue #787 itself stays open for the bench REBOOT run.
Open risks/questions: one seed per directive, so the -0.138 ns move of the selected route against dev's does not separate this PR's effect from placement. All three worst paths are outside this PR's logic. The datapath's own cells show -153 FFs in the flattened hierarchy; that is not traced, and the datapath diff removes no register.

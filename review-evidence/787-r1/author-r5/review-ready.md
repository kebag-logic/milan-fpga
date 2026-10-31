[A700f] REVIEW READY
Commit: `f7d5fc3cc48ca80195428562fa86a46023df8e0d`, local and not pushed. It is the merge of `814-soc-timing-cut` at `4ee2aa96` (PR #826's head) into round 4's `3e67de9c`. The pushed head stays `4aa5666e`.
Changed: one merge commit, with no behaviour change of this branch's own.
- `git merge-tree` and the merge are clean, with no conflict. The merge's change against the branch has the same patch-id as #826's own change against dev `1e80128f` (`8fa226cc`). The three files both sides changed (`milan_soc.py`, `CLOCK_DOMAINS.md`, `TESTING.md`) are each the branch's copy plus #826's hunks.
- This PR now carries PR #826's commits and merges after it; PR-BODY says so.
- No record needed regenerating, so there is no second commit. #826 changes no gitlink, no HDL and no generator. The ROM ledger re-records byte-identical. The boundary diagram, the port census (hdl 2181 / gPTP 127 / processor 1771) and the MAC model check unchanged. The flash-layout and audio-path generators reproduce their committed files. The CDC census generator's output at the merge is this branch's (x3 MultiReg, stale since round 2 as round 4 reported), and at #826 it is the base's.
- `git diff --check $(git merge-base origin/dev HEAD) HEAD` against dev `02ca829a`: rc 0.
Validation at the head, each in a clean clone:
- LiteX simulations: `simulations: 8   passed: 8   failed: 0   skipped: 0   timed out: 0`, rc 0.
  - `test_soc_timing_cuts.py` passes 23 arms with `RESULT: PASS`, run alone (686 s) and in the aggregate (789 s).
  - The aggregate's first run hit the 900 s member limit under this host's load: TIMED OUT, result unknown, rc 92. It was re-run unchanged, and only scheduling changed: the other jobs ran at nice +10 and the Vivado runs were paused for 300 s.
- The MAC model check passes at both levels. #70's service budget: 69 checks, 0 failures.
- The static and pin-record bank: 32 of 32 rc 0.
- The builder bank: `ALL GATES PASS EXCEPT 2 NOT RUN`, round 2's two. Gate 1f 9/9, gate 23m on 5 configs, and #817's servo reset controls pass.
- xvlog: 0 findings.
- rtl-fast: `success; failed jobs: none`, 12 of 12 jobs, 56 steps. Behave: 14 features, 508 scenarios, 2,330 steps.
- The docs workflow: 44 steps, 0 failed (2 skipped by rule). Leg 1 with LiteX passes, the markdown gates pass 5 of 5, and the no-git gates pass.
- Route-1x1 on the three placement directives, from one synthesis in parallel, judged by #820's gate at `50e5d08d` from scratch: **rc 0, `RESULT: PASS`**.
  - AltSpreadLogic_high is selected at **+0.365 ns** at both slow corners and +1.633 ns at both fast corners. Hold is +0.053 / +0.015 ns.
  - ExtraTimingOpt has +0.204 ns and ExtraPostPlacementOpt +0.090 ns. Every corner of every directive meets the +0.030 ns floor.
  - LUT 52,021 (+9), FF 54,102 (+395), slices 15,787 (+7; 63 free). RAM and DSP are unchanged. The fall from the record is 0.075 ns, so there is no warning.
  - Every route is complete. The #607 log check is clean, and IOB packing is OK (22 ports).
- The deciding path of each directive:
  - AltSpreadLogic_high: **F4**, the CPU's DMA write bridge inside VexiiRiscv (`dma_bridge_write_bridge/aligner` -> `onPerId_bridge/pendings_valids_reg[0]`), `sys`, 18 levels, 76 % routing. The F4 ruling accepts that family.
  - ExtraTimingOpt (+0.204) and ExtraPostPlacementOpt (+0.090): the processor's AECP, in the 50 MHz Milan clock: the micro-CPU's `uop_e_r[imm]` into the NVM writer's `deb_cnt_r` reset, 36 levels, 65-66 % routing. Its cells are in `KL_aecp_ucpu`, `KL_aecp_nvm_writer` and `KL_aecp_dyn_state`, which this branch's processor pin does not change against dev's. It lies outside F1 to F4.
  - LiteDRAM's ZQCS timer (F3), round 4's deciding path, is no longer among any directive's listed `sys` paths.
Acceptance criteria: the round 5 assignment's items 1 to 6 are met; no STOP condition is met. #787 itself stays open for the bench REBOOT run.
Open risks/questions:
- `test_soc_timing_cuts`' wall time sits near the aggregate's 900 s member limit on a loaded host, as PR #826's review noted.
- The two non-selected directives are decided by the AECP path above, which no ruling covers. It is published, not ruled on.
- Nothing was pushed. HANDOFF.md, PR-BODY.md and the receipts are in the round's output directory.

[A785] REVIEW READY
Commit: 1a1e6665 (on 919-phy-link). Round 2's head afa3ea19, then round 3's 319afb3d, 5c2682a4, c79f1c76 and da8a8b84, then round 4's 8beada76, 33041d64 and 1a1e6665. Nothing pushed.

This covers rounds 3 and 4 together. Round 3's own REVIEW READY at da8a8b84 (issuecomment-6932294892) is superseded: its findings stand as answered there, and every gate below was run again at 1a1e6665.

Round 3 answered PR #933's two NEGATIVE reviews of afa3ea19:
- R852-F1 = R851-F1, MAJOR: negotiation restarts after every write that repaired the advertisement (319afb3d).
- R852-F2 = R851-F4: the frame and work counts.
- R851-F2: after a loss, register 4 lost alone and register 9 lost alone are each graded, with m3 and m3b planted (5c2682a4).
- R851-F3: the fit page's one history (c79f1c76).
- R1: the ledger's comments.

Round 4 closes the gap round 3 disclosed, before any review.

Changed in round 4:
- THE OUTCOME (8beada76). The restart's own write is never read back, because its bit clears itself (IEEE 802.3 22.2.4.1.7). So a restart the PHY drops leaves the earlier negotiation in force while registers 4 and 9 read back, and the restart is now verified by what it negotiates. The check is in `ctrl_plat_phy.c:246-265`:
  - it fires on a negotiation complete (BMSR bit 5) on a link up that shares no 1000BASE-T mode in registers 9 and 10, while the advertisement is verified;
  - the link resolves from registers 4 and 5 as the release does; they share no mode below 1000 Mb/s, so it is published down;
  - the next poll owes the advertisement again with its restart taken whatever the PHY holds;
  - each such restart is counted in `renegotiations`, a saturating counter in the struct's padding (no size change, `ctrl_plat` unchanged).
- A poll that takes the restart resolves from a BMSR read after it (`:233-238`), never the read before. Without that, a repair on a link published up resolved the stale BMSR and THE OUTCOME owed a needless restart; P17's new oracle found it.
- A 10/100 PHY is now `CTRL_PLAT_PHY_ADV_NONE`, so `adv == 0` means verified. The boot flag is renamed `CTRL_PLAT_PHY_ADV_RENEGOTIATE`.
- A forced mode is published as the release publishes it.
- The peer (`phy_peer.hpp`):
  - `drop_restarts` loses the next restart writes whole: register 0, the restart count, the abilities in force and the link stay the last negotiation's;
  - a negotiation sets BMSR's autonegotiation complete.
- P18 is the case the brief asks for: a 100BASE-TX-only partner, the register-0 write dropped once.
  - The boot publishes the earlier 100 Mb/s link down, and the next poll restarts once, counted. After recovery there is no link at 100, with one extra restart, and none follows.
  - Lost three times, the write is restarted once a poll, each counted, until one takes.
  - There is no restart while the negotiation is incomplete, none at 1000BASE-T, none on a PHY the advertisement is not for, and the count saturates.
- P17 now also requires that the repair's own restart did it, with THE OUTCOME owing none.
- The plants:
  - `plat-phy-outcome-unchecked`, the outcome check skipped, is caught by "P18 no link at 100 after recovery";
  - also planted: not renegotiated, uncounted, count wrapping, judging a 1000BASE-T link, judging a PHY the advertisement is not for, and resolving before the restart;
  - `plat-phy-restarted-before-verified` is re-needled to P17's new words, because THE OUTCOME now recovers that round-3 defect too.
- The coverage ratchet row for `ctrl_plat_phy.c` is at this head's measured 178/178 lines and 164/164 branches (1a1e6665). 33041d64 grades the counter's saturation, the one branch 8beada76 left untaken.
- The release firmware has the same gap: `phy_advertise_gigabit_only` writes the restart once and cannot read it back. That is noted in the PR body as a known release limitation, and the release firmware is unchanged.

Validation at 1a1e6665, each on a fresh clean clone:
- Workflow jobs `rtl-fast`, `elaborate` and `docs`, step by step: 89 steps rc 0, 159 not run with a stated reason, 0 bad. The not-run steps are the hosted-only steps, plus 29 steps of jobs these rounds do not touch (RTL lint, Yosys, BDD, CDC, census, the AECP and SRP campaigns), each rc 0 at afa3ea19.
- `firmware-unit`: `test_ctrl_firmware: PASS`. The coverage ratchet gives `ctrl_plat_phy.c` 178/178 and 164/164, `firmware coverage: PASS (40 files)`.
- `firmware-control-mutants`: `mutants: 769 of 769 caught`. The platform has 94 plants: the PHY's 53, and within those the advertisement's 27.
- Split boot simulation, rc 0 at both shapes: the longest frame is 14,537 cycles (145.37 us) at 1x1/1if and 14,545 (145.45 us) at 8x8/1if, against 155 us, unchanged by THE OUTCOME. Both show 59 frames, 10 publications, the advertisement's seven writes, and `[0, 13]` / `[0, 0]` / `[13]`.
- Boot self-test rc 0: 6/6 native controls, 6/6 plants and 8/8 placement controls. `plat_ledger.py --self-test` rc 0: four points and 8/8 controls. `test_ctrl_memory.py` PASS.
- Platform images: `rom` 119,500 / 121,084 / 132,204 / 133,772 B, at 43.5 / 44.5 / 56.5 / 61.0 RAMB36, with 916 B left at 8x8/1if and 1,396 B at 8x8/2if.
  - That is +64 B at every point, all in `ctrl_plat_phy.o`. `ctrl_plat`, the tiles and every ROM and SRAM bank are unchanged, so no route was repeated.
  - Under #818's floor, round 2's routes at c805f699 pass: 1x1/1if on all three directives, and 8x8/1if on ExtraPostPlacementOpt (+0.189 / +0.031). 8x8/1if's ExtraTimingOpt and AltSpreadLogic_high miss setup (+0.005, +0.002) on the mailbox event path, #927's family.
  - The CPU budget harness images are byte-identical to round 2's and the base's, so its verdict is the base's.
  - The release image's inputs are unchanged since c805f699, which was byte-identical.
- The native sweep was not re-run, since no RTL or Verilator testbench source changed; it was 65 of 65 at afa3ea19.

Acceptance criteria (round 4):
- The outcome check is met: P18's three tests pass. `plat-phy-outcome-unchecked` is caught by name, as are its six siblings.
- The pin-level peer is extended as asked.
- The frame is within 155 us, at the same figures as round 3.
- The ratchet row is rewritten.
- The release limitation is noted in the PR body.
- Both reviews' probes pass at 1a1e6665:
  - R852-1's retry probe: `advertised-at-last-restart=0001 active-Mbps=0 restarts=2`, control `restarts=1`;
  - R851-1's `retry_probe.sh`: 21 of 21.
- R851-1's `mutants.sh` no longer places m3, m3b and m8, whose anchors name the renamed flag and the old owed test. An executor's copy with only those three anchors renamed (diff in the receipt) catches all but m6, the review's equivalent mutant.

Open risks/questions:
- A PHY left in a forced mode before boot whose register-0 write is lost stays in that mode, as the release's does. THE OUTCOME judges a completed autonegotiation.
- A PHY that downshifts below 1000 Mb/s against a gigabit-only advertisement is restarted once a poll and holds no link. That is #840's outcome.
- Timing is restated by #818's floor (best of three directives: +0.030 ns setup, 0 ns hold). Rounds 2 and 3 had applied +0.030 to hold as well.

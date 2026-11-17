[A785] REVIEW READY
Commit: da8a8b84 (on 919-phy-link; round 2's head afa3ea19 + 319afb3d, 5c2682a4, c79f1c76, da8a8b84). Nothing pushed.

Answers PR #933's two NEGATIVE reviews of afa3ea19, the external R852-1 and the internal R851-1, as the manager's round 3 brief scopes them.

Changed:
- R852-F1 = R851-F1, MAJOR (319afb3d). Negotiation now restarts after every write that repaired the advertisement, so the abilities in force are the ones written (IEEE 802.3 28.2.4.1.3). At boot it restarts whatever the PHY held, as the release's init does. A PHY that still held the advertisement, as read before the writes, is written and not restarted, so a restart's own latched loss never restarts again.
  - `ctrl_plat_phy.c:223-233`: the `RESTARTED` flag, which was set before the read-back verified, is gone.
  - A dropped write leaves the advertisement owed, and the next poll writes it and restarts again.
  - `phy_peer.hpp` gains a negotiation latch: a restart latches registers 4 and 9 as the abilities in force and resolves the link against the partner's 5 and 10, apart from the registers.
  - P17 is the reviewers' case, at boot and after a loss: register 4's writes are dropped through a try, the partner offers 100BASE-TX full duplex alone, and after ten more periods the advertisement in force is 1000BASE-T only, the partner has no link, and no restart follows.
  - P15 now requires a restart on each repaired try and none once verified.
  - Plant `plat-phy-restarted-before-verified` (the round-2 rule) is caught by P17 ("P17 the active advertisement is 1000BASE-T only") and by P15. It replaces `plat-phy-restart-each-poll`, whose rule was the defect.
- R852-F2 = R851-F4, MINOR (319afb3d). `ctrl_plat_phy.h:62-64` and `plat/README.md:94` now say six reads (15, 4, 9, 0, then 4 and 9 back) and three writes (9, 4, 0), each frame 64 bit periods (`CTRL_PLAT_PHY_FRAME_BITS`), with the restart's write left out where the PHY held the advertisement.
- R851-F2, MINOR (5c2682a4). P14 grades the after-loss decision on a PHY that lost both registers, register 4 alone and register 9 alone. Each case requires three writes, one restart, then a poll with neither. The review's m3 and m3b are plants:
  - `plat-phy-lost-local-not-restarted` is caught by "P14 a PHY that lost the advertisement is written and restarted once, register 4 alone";
  - `plat-phy-lost-gig-not-restarted` is caught by the same words ending "register 9 alone".
- R851-F3, MINOR (c79f1c76). `SPLIT_CONTROL_MEMORY.md` section 3 now states one history for the platform 8x8/2if entry: 60.0 (`:142`), 60.5 by #895 (`:145`), and 61.0 by #919 and #840, refused at 61.5 (`:147`).
  - The round-1 sentence is removed, and `:146` is restated: the platform held #895's 60.5, refused at 61.0, until the PHY poll's merge.
  - Reread against `ctrl_memory.LEDGERED` (`:273` 61.0, `:288` 56.5) and section 5 (`:276`, `:282`, `:402`): they agree.
- R852-R1 = R851-R1, RESIDUE (c79f1c76). `ctrl_memory.py:237-238,255` now carry the decision and the issue in place of the issue-comment ID and the lane name. The entries' reason strings are data and are left for the residue checklist.
- Figures (da8a8b84) are restated as measured on a clean clone of c79f1c76.
  - Every platform image's `rom` is 8 B smaller (`ctrl_plat_phy.o` 1,883 -> 1,875 B). The RAMB36 counts (43.5, 44.5, 56.5, 61.0), `ctrl_plat` and the ROM banks are unchanged.
  - The longest frame is 14,537 CPU cycles (145.37 us) at 1x1/1if and 14,545 (145.45 us) at 8x8/1if. `CTRL_PLAT_PHY_STEP_US` stays 155 by the rule (145.45 x 1.05 = 152.7, rounded up to 155).
- No RTL, mailbox contract or CPU budget bound changed. `git diff --stat afa3ea19 da8a8b84 -- hdl sw/firmware/ctrl/mbx tb/verilator/ctrl_service_budget tb/verilator/fw_service_budget` is empty.

Validation at da8a8b84, each on a fresh clean clone:
- Workflow jobs `rtl-fast`, `elaborate` and `docs`, step by step: 89 steps rc 0, 159 not run with a stated reason, 0 bad. The not-run steps are the hosted-only steps, plus 29 steps of jobs this round does not touch (RTL lint, Yosys, BDD, CDC, census, the AECP and SRP campaigns), each rc 0 at afa3ea19.
- `firmware-unit`: `test_ctrl_firmware: PASS`. The coverage ratchet gives `ctrl_plat_phy.c` 172/172 lines and 158/158 branches, `firmware coverage: PASS (40 files)`.
- `firmware-control-mutants`: `mutants: 762 of 762 caught`. The platform has 87 plants: the PHY's 46, and within those the advertisement's 20.
- Split boot simulation, rc 0 at both shapes: 1x1/1if longest frame 14,537 cycles (145.37 us) and 8x8/1if 14,545 (145.45 us), against the stated 155 us. Both show 59 frames, 10 publications, the advertisement's seven writes, `[0, 13]` / `[0, 0]` / `[13]`, and MDC 950 / 1,120 / 2,260 ns.
- Boot self-test rc 0: 6/6 native controls, 6/6 plants (`phy-unadvertised` among them) and 8/8 placement controls. `plat_ledger.py --self-test` rc 0: four points and 8/8 controls. `test_ctrl_memory.py` PASS.
- Platform images: `rom` 119,436 / 121,020 / 132,140 / 133,708 B, at 43.5 / 44.5 / 56.5 / 61.0 RAMB36 with 980 B left at 8x8/1if and 1,460 B at 8x8/2if.
  - Every point's ROM and SRAM banks are round 2's, so no route was repeated and timing stays owed to #927 with round 2's figures.
  - The CPU budget harness images are byte-identical to round 2's and the base's at both shapes, so its verdict is the base's.
  - The release image's inputs are unchanged since c805f699, which was byte-identical.
- The native sweep was not re-run, since no RTL or Verilator testbench source changed; it was 65 of 65 at afa3ea19.

Acceptance criteria:
- R852-F1/R851-F1 met: P17, P15, P13 and P14 pass. The plant is caught by name. Both reviewers' own probes pass at da8a8b84:
  - R852's retry probe: `advertised-at-last-restart=0001 active-Mbps=0 restarts=2`, and its control `restarts=1`;
  - R851's `retry_probe.sh`: 18 of 18, `advertised-at-last-restart=0001 restarts=2 adv-owed=0`.
  The frame is within 155 us.
- R851-F2 met: m3 and m3b are caught by P14 in the campaign and in R851's own `mutants.sh`, where m6 still survives as its equivalent mutant.
- R851-F3, R852-F2/R851-F4 and R1 met as above.

Open risks/questions:
- The restart's own write (register 0) is not read back, because its restart bit clears itself (22.2.4.1.7). A dropped restart write is therefore not seen, and the advertisement reads back while the PHY keeps its earlier negotiation. The release's init has the same property. It is unchanged here (fix exactly) and disclosed in the PR body; it can become a new issue if wanted.
- A PHY that never takes the writes is restarted every poll and holds no link. That is #840's outcome for a PHY that cannot advertise 1000BASE-T alone.
- `coverage.ratchet:30` still records `ctrl_plat_phy.c` at round 2's 173/173 lines and 160/160 branches; this head measures 172/172 and 158/158. The check holds fractions, so it passes at 100 %. The row was not rewritten.
- Timing stays owed to #927 with round 2's routes (at c805f699), because the ROM banks are unchanged.

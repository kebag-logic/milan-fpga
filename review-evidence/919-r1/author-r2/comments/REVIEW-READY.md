[A785] REVIEW READY
Commit: afa3ea19 (on dev-soft-core 70f4056f by the merge 8670bfb0; round 2's commits 8670bfb0, fcceb603, 8b742277, c805f699, afa3ea19 on round 1's 55769f09). Nothing pushed; PR body in the lane's round-2 output.
Changed:
- Sync: one --no-ff merge of dev-soft-core 70f4056f (8670bfb0), six conflicts, both sides kept.
- #840 on the split (scope addition issuecomment-6907491954), fcceb603: `ctrl_plat_phy.{h,c}` THE ADVERTISEMENT, through the poll's own Clause-22 helpers (a write frame drives all 64 bits, 22.2.4.5).
  - The release's init values: register 9 keeps MASTER-SLAVE and advertises 1000BASE-T full duplex only; register 4 drops 10/100, T4 and bit 14; register 0 enables and restarts autonegotiation with reset and isolate clear.
  - Only a PHY with 1000BASE-T full duplex ability is written.
  - It runs after the first BMSR read and before the link is resolved, at boot and after every link loss. Registers 4 and 9 are read back, and it stays owed until they hold it.
  - Negotiation restarts at most once each time it is owed: at boot always, after a loss only where the PHY lost the advertisement. A restart latches a loss of its own, so restarting after every loss would loop.
- Boot simulation (8b742277, afa3ea19): its PHY takes writes, the grade checks the advertisement's writes, a plant leaves it unowed, and the native stand-in prints it.
- Ledger (c805f699), under the owner's rule as #923's ruling applies it (issuecomment-6906679024), with no STOP:
  - the platform's 8x8/2if entry 60.5 -> 61.0, its measured image;
  - a product entry for the platform's 8x8/1if image at its measured 56.5, which `milan_soc.add_ctrl_memory` and `ctrl_plat_image.py` plan by the image's symbols (`ctrl_memory.product_point`; `plan` is unchanged);
  - both are S14 debt. Growth by file: `ctrl_plat_phy.o` +1,883 B (the advertisement's share 529), `ctrl_plat.o` +60..68 B, `ctrl_plat_main.o` +12 B, nothing else.
Validation, each at afa3ea19 on a fresh clean clone:
- workflow jobs rtl-fast, elaborate, docs: 118 steps rc 0, 130 hosted-only steps not run with a stated reason, 0 bad. The census needed a booked range for sv2v's 900 s limit under load.
- control mutant campaign 760 of 760 caught: the platform's 85, the PHY's 44, the advertisement's 18, #840's "100BASE-TX left advertised" among them. The AECP and SRP campaigns PASS.
- coverage: `ctrl_plat_phy.c` 173/173 lines and 160/160 branches.
- split boot simulation 1x1/1if and 8x8/1if PASS: 59 frames; the boot's writes 9 0x0200, 4 0x0001, 0 0x1200, then 9 and 4 after each loss, read back; the longest frame 145.69 us against 155. Its self-test PASS: 6/6 native controls, 6/6 plants.
- platform ledger self-test PASS (4 points, 8/8 controls); `test_ctrl_memory.py` PASS.
- release image byte-identical, both configs (built at c805f699; afa3ea19 changes nothing the release build reads).
- native sweep, 4 shards: 65 of 65 suites, 2,713,040 checks, 0 failures.
- CPU budget harness (at c805f699; its images are byte-identical to the base's):
  - 1x1/1if rc 0: 96 groups, 0 refusals, 0 of 130,341 passes over the share.
  - 8x8/1if, as parallel parts on booked CPUs then one regrade: 95 groups, 0 refusals, 0 of 270,769 passes over the share. It exits 1 on 11 stated-cost lines, the base's (#920 issuecomment-6908928237).
  - At both points the only misses are the seven backlog-owed held-egress rows.
Acceptance criteria:
- the poll, its pace, its cost class, the consumers, the boot grade: met, as in round 1, at this head.
- #840's advertisement written and verified at boot and after every link loss: met. Host tests P11-P16, with dev's per-property grading in two arms, and 18 planted defects each caught by name. The boot simulation grades the writes.
- release image byte-identical: met.
- the harness at the final head: run at c805f699, whose harness inputs equal afa3ea19's and whose images equal the base's.
- routes (the ruling, issuecomment-6907583837): recorded as misses at the base, owed to #927, re-routed because the ROM banking changed. No seeds, no extra directives.
  - 1x1/1if meets on ExtraTimingOpt (+0.176/+0.032) and AltSpreadLogic_high (+0.090/+0.036). ExtraPostPlacementOpt misses hold, +0.414/+0.015, on the TDM render FIFO crossing.
  - 8x8/1if meets on ExtraPostPlacementOpt (+0.189/+0.031). ExtraTimingOpt (+0.005/+0.036) and AltSpreadLogic_high (+0.002/+0.036) miss setup on the mailbox event path.
  - Device block RAM: 82 of 135 tiles at 1x1/1if, 92.5 at 8x8/1if.
- the backlog-owed held-egress rows: the base's already-ruled rows, recorded as such.
Open risks/questions:
- #923's lane implements the same product-entry mechanism; the sync reconciles the two.
- Timing at both shapes is #927's.
- A restart after a loss where the PHY lost the advertisement costs one renegotiation.

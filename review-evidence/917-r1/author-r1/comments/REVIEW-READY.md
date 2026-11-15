[A784] REVIEW READY
Commit: 3926c271 (branch 917-aecp-hold: 84d8a214, bb001e10, 3926c271 on cec88385)
Changed:
- hdl/milan/mailbox/KL_mbx_rx.sv: a passing frame that finds its channel's bucket empty is held (words and header written past RX_HEAD, RX_HEAD unmoved) and committed at the channel's next refill, which it spends; one frame held per channel; a frame that finds the bucket empty behind a held one is refused and counted in RATE_DROP (and IRQ_STATUS.ERR). A per-channel write head keeps the next frame's words and free space off the held record; a tail ahead of RX_HEAD inside it still leaves no free word; a refill landing between the verdict and the header writes commits at once, so a channel never holds a frame beside a token. Generic over every channel of the table; a frame with a token takes the same clocks as before.
- Contract: no register, field, rate figure or version change (RATE_DROP counts the frames refused behind a held one); the generated package, skeleton and C header are byte-identical; only the reference page's filter sentence moved (mailbox_emit.py), plus the YAML's filter comment.
- The fabric's host model (sw/firmware/ctrl/host/mbx_model.c/.h, in no firmware image) follows the RTL; three ring-fill loops in test_acmp_mbx.cpp count committed records from RX_PASS and wait out a held one (expectations unchanged).
- Tests: tb/verilator/mbx T0, T1, Q10, V0 graded for the ruling; new group HeldNotDropped, B0-B4, on both adapters and the host model; B5, B6 on the RTL at the clock; seven planted RTL defects (rx-drop-instead-of-hold in the default make) and the model's twin in ctrl_mutants.py.
- Docs: MAILBOX_SPLIT.md ("The held frame", the filter section, the verification counts), tb/verilator/mbx/README.md and Makefile.
Validation (clean clones):
- Verilator sweep, every suite as four native shards at 84d8a214: 65/65 pass; shard 1/4 (holds mbx) at 3926c271: 17/17 pass, mbx 607/652/32/614/659/532 checks, 13/13 quick mutants.
- make -C tb/verilator/mbx mutants at 3926c271: 238/238 caught by their named checks.
- rtl-fast, elaborate, docs and the rtl yosys jobs at 3926c271, step by step: 139 steps rc 0, 226 not run with a stated reason (hosted orchestration, installs this host already has), 0 bad; firmware control mutants 699/699.
- Firmware images against cec88385: byte-identical, 46 fixture images and the split platform images 1x1/1if and 8x8/1if with their ROM banks.
- AX7101 split image, S9's recipe, three directives at 3926c271: best AltSpreadLogic_high WNS +0.203 ns, WHS +0.036 ns at every corner, 0 failing endpoints (ExtraTimingOpt +0.063/+0.036 also meets; ExtraPostPlacementOpt +0.202/+0.016 misses the hold floor). Area against the base's route: LUT +74 to +181, FF +75/+76, BRAM and DSP unchanged; KL_mbx_rx +124 to +133 LUT, +77 FF.
- CPU budget harness 1x1 (it Verilates this RTL; not a CI gate), base against head: all 94 groups' simulation logs, graded results and the table byte-identical; 0 refusals at both.
Acceptance criteria:
- Mailbox bench, 50 back-to-back AECP reads none lost (B0; one in flight, each at line rate as the one before it is delivered, as read at TAKEN; B2 also replays the hardware finding, a 1 kHz controller, none of 100 lost) and a third command behind a held one dropped and counted (B1): met, on the RTL through both adapters and on the host model; 'drop instead of hold' planted, caught by name.
- Three descriptor walks on hardware with none unanswered: not run here (no hardware in this lane).
- The load and every row unchanged, no firmware image change: images byte-identical; every commit still spends one token, so the committed rate and the load are the table's; the budget harness's rows at 1x1 are byte-identical to the base's (not run at 8x8).
- Timing met at every corner: met on the best of three (the base met the +0.030 hold floor on none).
Open risks/questions:
- The host model and three host-test loops live under sw/firmware/ctrl/ but are not image sources (stated at TAKEN); the images are proven identical.
- A frame held when its channel closes is still committed (it passed while open); a reset forgets it.
- ExtraTimingOpt's worst setup path is now the receive verdict (+0.063 ns).
- Pre-existing, not changed here: the budget harness cites MAILBOX_SPLIT.md by line number, already stale at the base; worth an Issue.

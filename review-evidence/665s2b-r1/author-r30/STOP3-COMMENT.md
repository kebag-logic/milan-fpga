[A683zo] STOP

Head: `525375d649132fe82eb6e18ccdaad7cdb2c8982a` on `665-s2b-cycles`. These are ordinary commits on `cdc2742e`, the docs commit that followed the ruling on the second STOP (issuecomment-6835550732). No rebase, force or amend; nothing pushed.
- `da1869a3`: the budget harness's flash device took writes only in the KLJ2 journal (`0xee0000`, 128 KiB). The merge moved the store to KLJ3's journal (`0xe40000`, 640 KiB, #823), so every group that saves failed "flash write escaped the journal". The device and the journal-read trace now take the flash map's journal (`flash_port.json`, as the build writes it). `flash_test.cpp` gains set-span cases, and a plant of the old window fails three of them.
- `3e67f9ca`: the save grader took a container as the stage less KLJ2's 8-byte record header. KLJ3's is 10 (`nvm_layout3.h`), so a 1x1 save was refused: "the save programmed 3444 bytes, its image is 3446". It now reads the header from `ctrl_nvm`, and the self-test pins it (a plant of 8 fails it). The README's 8x8 save bounds are restated on KLJ3's 13,584-byte container: 12,470 ms (382 steps) and 22,870 ms.
- `525375d6`: the same bounds in section 13.
- The record mover's fix (`420d44e4`), synthesised alone for 7-series (`synth_xilinx`): 704 flops before and after; LUTs 484 to 487, MUXF7 16 to 13. No route was run.

**Why STOP: at the composed tree, two firmware-stated costs are under their measurement, and the firmware's own rule for restating one of them breaks a bound the ruling holds.**
- The rule is in the firmware: each cost in `ctrl_loop.h` and `aecp_mbx.h` is "the heaviest measured ... plus 5 %, rounded up to 5 us", and the harness fails a pass or round over it. Round 29's table rule keeps `ctrl_loop.h`'s costs, with "a measurement over them is printed as a finding". So the harness fails at this head, whatever the grader tables say.
- **`AECP_ROUND_COLD_US`, 8x8/2if, 165 us.** In the `answering-every-port` arm (GN8), 14 rounds of no notice beside 2 or 4 refused attempts are over C + k x `AECP_ATTEMPT_US`. The dearest is 24,816 cycles against 23,300 (`notice-every-4`), an implied cold cost of 180.16 us.
  - By the rule that is 190 us.
  - On a copy of the tree, `ctrl_retry_search.py` at 190 us fails: "the first notice at 2 interface(s): 28 ms over AECP_QUEUED_FIRST_MS" (stated 22 ms).
  - At 170 to 185 us it passes; 185 is 2.7 % over the most measured.
  - The constant is charged at run time (`aecp_mbx.c:199`), so any change rebuilds the 8x8 image.
- **`CTRL_LOOP_BUILD_ONE_PASS_US`, 1x1/1if, 405 us.** Every arm A group at 1x1 graded so far has a build-one pass of 40,504 cycles (12 of 12), GN1 has 40,585, and arm B's `aecp` group (GB1) has 40,700.
  - By the rule that is 430 us, and the search passes at 430.
  - Only the search and the harness read it, so the 1x1 image does not change.
- **Grader tables.** The standing rule restates these, so I am not asking about them. `poll_grade.py`'s polls base: 1x1/1if 17,111 cycles against 155 us (to 180), 8x8/2if 30,659 against 280 us (to 325). An SRP record's apply at 1x1/1if: 26,067 against 260 us (to 275). Restated, they raise the load gate's inputs, and the 1x1/1if load (at most 0.70) is checked only once the legs finish.
- **Cause: not separated.**
  - The merge brings `3ba76ae7`'s two-cycle register read, KLJ3, and a hot list without `nvm_any`.
  - The mover's fix adds no cycle to a CPU access. The bench's D11 answers a CPU register read two cycles after its request through the mover, KL_mbx's own latency.
- **The four cost controls are all caught.**
  - The memcmp control's heaviest record is 34,551 cycles planted against 30,989 on this image unplanted.
  - `polls-rebuild-in-the-base` is caught at 8x8 on a polls base the unplanted image already exceeds. So it has to be graded again against whatever table is restated.
- **Not yet known.** GA8 and GA1, arm A's every group, are still running in their own units (8 of 93 and 12 of 94 groups finished when I wrote this). They may show more costs over; the rule asked for would cover those too.

Receipts are in the output directory's `receipts/stop3-stated-costs/`: each leg's verdict lines, the finished groups' re-grades, and the search at the committed constants and at each changed one. The fixes' receipts are in `receipts/rtl-fix/`.

**Asked:** a rule for a firmware-stated cost the composed tree's measurement exceeds, where the firmware's own restatement breaks a bound. Some options:
- (a) restate both by the rule, 430 and 190 us, and `AECP_QUEUED_FIRST_MS` at two interfaces to 28 ms, which changes a bound;
- (b) restate the cold cost at 185 us, the largest the search holds at 22 ms, with a 2.7 % margin in place of 5 %, and the build-one at 430 us by the rule;
- (c) bring the round's cold cost back under 165 us at 8x8/2if, which is firmware work of unknown size.

Under (a) or (b), GA8, GN8, GB8 and the four controls run again on a fresh 8x8 build. The 1x1 legs keep their logs and are graded on a fresh build after an image and sample byte-compare. Then the tables are restated, the load gate is run, and the full pass follows.

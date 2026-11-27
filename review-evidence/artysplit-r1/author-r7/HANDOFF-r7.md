Status: REVIEW READY (22:00). The Arty row is re-derived by the rule and installed in two steps, qualified by the complete 147-case census at it (PASS) and routed at every corner (PASS). Every round-5 gate passes.
ETA: done; independent review, hosted/replica/merge gates and maintainer authorization are next and external to this lane.

[A829], round 7, PR #1004 (Relates to #878). Head `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1` on `pf-arty-split-1`, local only. Nothing pushed or posted; no Arty access; no job left running.
Scratch `$VALIDATION_STORAGE/artysplit-a829/r7` (17 GB; /data has 32 GB free).

## Commits

- `f7b90e3b7` Step 1, the rule's row from round 6's derivation: slice 950 -> 1250 us, pace 9 -> 10 ms, TX 30 -> 35 ms, retry cold 125 -> 130 us, raised stated costs.
- `74f942be5` Step 2, the rule's row from the complete census at step 1: poll base 235, centisecond 160, LINK 190, MAAP 165, withdrawal 95 us. Slice, pace and queued bound unchanged. This is the manager's "one more step"; the census at it does not move the row again (derived = installed).
- `2d911d2bf` Docs section 15: qualification figures and held-egress note.
- `4adfa9dc8` The receipt regrader applies `run.py`'s #969 disposition in its cross-case step; before this it refused the five owed lines. A control packet without `srp-bound` is refused by name.

## Results

- Qualification PASS, 147 cases, all six checks. Load 0.5004771140/0.70, ACMP 29.77/30 ms, txL 48.82/49 ms, last notice 117.47/140 ms, longest pass 142775 cycles = 1.785/2 ms. Held-egress rows below their ledger.
- Route PASS at all four corners for all three directives. Selected AltSpreadLogic_high (ties ExtraTimingOpt): Slow 0.433/0.138, Fast 1.606/0.050 ns; ExtraPostPlacementOpt 0.064/0.126.
- LUT 33015 / FF 40369 / BRAM 78.0 / slices 13791, equal to round 6's route (round 5: 33411 / 40479 / 78.5 / 14119). No LUT band is defined in the repository or the rulings; these are the routed totals of rounds 5-7.
- Bitstream `24a782c505c1ae4aea61d2abf1b1dd2e2cf0e5aa08e12a717e10cfddb37a871e`, ELF `b6cfb9a4e051e865101ceb220a3dfe4f7c487938c97d3e764c0f7407085038d2` (44.5/56 RAMB36, ledger sections unchanged). Matched deployment inputs are in [image/](image/), local only (the manifest keeps a local path).
- Gates: at `74f942be5`, four firmware shards (`--jobs 4`), native boot, controls 6/6 and region. Service 297/297, standalone self-tests, `arty_grade`, `test_ctrl_memory`, MII/`lat` 15/15. At `4adfa9dc8`, all ten docs/idiom gates.
- `receipt_regrade.py` over [receipts/](receipts/INDEX.md): 147/147 grades reproduced, cross-case PASS, timing PASS.

## Decisions a reviewer should check

1. **#969's disposition in the derivation.** `srp-kept` and `srp-bound` (new base groups) register Talkers at up to 495 us per SRP record, and `srp-bound`'s build of one takes 740 us.
   #969's ruling (2026-11-22, amended 2026-11-23) owes those to #977 and says the unit and `CTRL_LOOP_BUILD_ONE_PASS_US` are not restated. `kept_grade.py` passes on this image.
   So the cost census (round 4's tool) now leaves exactly the owed kinds out of the maxima, where they exceed the installed statement. Those kinds are SRP record applies in both groups, and `srp-bound`'s walk, polls base and build of one.
   Every other measurement of the two groups counts (LINK 190, withdrawal 95, centisecond 160). Without the disposition the rule finds no row: last notice about 225 ms against 140.
2. **Step 2 reuses step 1's traces.** `CTRL_LOOP_TICK_US` is read only by the harness model, so no firmware byte changes.
   Every native executable, ELF, flash image and all 147 stimuli are identical. The build inputs differ only in generation dates, each compared with the date removed.
   Each case was regraded with the census runner's own code against step 2's statements. This is round 5's regrade method.

## Departures from round 5's method

- Census on 12 then 15 legs in one CPUWeight=20 scope, scheduled into 2 h foreground windows. Window 2 was ended early, so that the longest cases ran while the host was quiet. No case was cut off.
- The cost-census tool excludes #969's owed measurements (above), and the qualifier applies `kept_grade.Disposition` to the runner's STATED lines, as `run.py` does.
- Firmware shards ran with `--jobs 4` (round 5: 1).
- ExtraTimingOpt's first step-1 attempt was cut off by the route runner's 2 h limit, and routed again. Step 2 routed all three directives again.
- Step 1's scratch is kept under `r7/step1/`; nothing deleted. One slip: I emptied two temporary archive-extraction folders with `rm` before logging them; the late entry is in `disk-cleanup.log`.

Files: [PR-BODY.md](PR-BODY.md), [REVIEW-READY.md](REVIEW-READY.md), [receipts/INDEX.md](receipts/INDEX.md); the local control packet is in `control-packet-without-srp-bound/`.

REVIEW READY 4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1

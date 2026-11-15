[A761c] REVIEW READY
Commit: `33b0d03a` (branch `665-s11-aecp-reboot`; one commit on round 5's `d3566d44`; not pushed, the manager pushes)

Round 6 is the manager's ruling on R821-5 (NEGATIVE, F1) and R822-5 (POSITIVE) at `d3566d44`. No firmware image changes, so round 5's legs and final pass carry. The gates the touched files feed ran again on a clean clone of `33b0d03a`.

Changed (7 files, one commit):
- **F1, option (a):** `poll_grade.STATED_US[1]['retained']` is now 285, by its rule, at the SRP record's cost. Its docstring reads "285 and 365 us; 280 at 1x1/1if before AECP's REBOOT", and SPLIT_CONTROL_MEMORY's polls row reads `285 (280)`.
  - At 1x1/1if the polls' `retained`, both load columns' `item.retained` and `record.srp` are each 285. At 8x8/2if each is 365.
- **RS-1:** `test_plat_boot.cpp:187` now names `(ADepartingTheRingRefusedHoldsTheReset)`.
- **RS-2:** REBOOT_RESET `:315` and `:316` now read "in `aecp_reboot_mutants.py`, which `aecp_mutants.py` plants". The comments `test_plat_boot.cpp:76`, `plat_mutants.py:265`, and the same reference in B20's comment at `:982`, read "in aecp_reboot_mutants.py".
- **R822-5-R1:** the `plat_mutants.py` comment names `NoOtherChannelTransmitsAfterTheDeparting`, `NoFrameOfAnyChannelIsTakenFromTheSuccess` and `TheGateHoldsWhileTheResponseCannotBeHandedOver`. Its `(B18)` part is RS-1's line.
- **R822-5-R2:** REBOOT_RESET `:316` reads "SUCCESS. Its three layers each carry one: the loop's stop".
- **R822-5-R3:** REBOOT_RESET `:297` and `plat/README.md:89` carry the residue's sentence as given, and `ctrl_plat.h:38` reads "and, from ADP's shutdown, ADP until the port", within its line.

The survey of every stated table, for any figure stated twice with different values (`statement_survey.py`, at both points):
- **The tables:** `load_grade`'s two columns, `poll_grade`, the pass costs `ctrl_loop.h` states and `whole_grade` reads, `rows_grade`, `rows_tiers`' three tables and `edit_rows`, plus each documented derivation.
- **At `d3566d44`:** the only conflict among the pin's tables was F1.
- **At `33b0d03a`:** none.
- **Every instance of the remaining 11:** each sets the donor column, measured on tsn-c-stack#32's image, against the pin's. All are identical at #902's head `41ca9f87`:
  - 1x1/1if: `event.ACMP` 185/170, `event.MAAP` 165/170, `record.acmp` 280/265, `record.adp` 105/100;
  - 8x8/2if: `build` 1,995/2,035, `event.ACMP` 350/210, `event.AECP` 105/110, `event.TICK` 40/85, `item.reclaim` 35/40, `record.acmp` 440/305, `record.adp` 240/125.

Validation:
- **Image identity:** the size fixture's and the platform's split images at 1x1/1if and 8x8/1if, linked at `d3566d44` and `33b0d03a` against one map and runtime. All 8 files (each image's ELF and loadable binary) are byte-identical by sha256.
- **At `33b0d03a`, on a clean clone:**
  - R821-5's `model_gates.sh` list, rc 0. `flip_grade.py --check --point 1x1/1if` PASS, the last queued notice 134.74 of 135; `load_grade.py --check` 0.520; load 26 of 26, record classes 14 of 14, flip 585 of 585; the rules: pace 8, ruled 135.
  - `rows_tiers` 1,033 of 1,033; `tier_grid` chooses 950 us.
  - The polls checks, 33 of 33.
  - The harness self-test: 0 failures, 246 of 246 mutants.
  - `firmware-unit`, every step rc 0. It compiles and runs `test_plat_boot.cpp` at one and two interfaces; coverage PASS (39 files).
  - `docs.yml`: 64 steps rc 0, 31 not run with a reason, 0 bad.
  - Whitespace against three bases, the idiom gates, and the docs, path, style, em-dash and TOC checks: rc 0.

Acceptance criteria: items 2 to 5 met. Item 1 is met for six of the eight items and the binding, as before, so the PR still says Relates to #871.

Open risks/questions:
- Not taken, as optional: R821-5 S1 and S2, and R822-5 S1 to S11.
- The #898 sync reruns the survey; the 1x1/1if margins are 0.25, 0.26 and 0.78 ms.
- The packet is `665s11-a761c/round6/` (PR body, HANDOFF-r6, receipts, INDEX).

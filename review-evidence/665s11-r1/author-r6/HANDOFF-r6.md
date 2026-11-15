# HANDOFF: #871 (#665 S11), AECP REBOOT, round 6 ([A761c])

Status: REVIEW READY at `33b0d03a` (#871 issuecomment-6901282063), one commit on round 5's `d3566d44`; nothing pushed by this lane. Next: one delta
review (R821-6) from `d3566d44`; the sync onto #898's head when the manager relays it.

## The ruling

R822-5 POSITIVE at `d3566d44` (PR #881 issuecomment-6900286461); R821-5 NEGATIVE (issuecomment-6900325190;
`review-evidence/665s11-r1/reviews/R821-5/REPORT.md`, archive `d41d571b`) on one MINOR, F1: the polls gate's retained
retry still stated at 280 us at 1x1/1if while the load gate states it at the SRP record's 285. The manager's ruling: F1
option (a); survey every stated table for any other figure stated twice with different values; RS-1 and RS-2 exactly
as written, and R822-5's three wording residues where they are exact fixes; no firmware image may change, proved by
sha256 for the 1x1/1if and 8x8/1if split images; then round 5's legs and full pass carry, and only the gates the touched
files feed run again on a clean clone of the final head.

## The commit `33b0d03a` (7 files)

| File | Change |
|---|---|
| `tb/verilator/ctrl_service_budget/poll_grade.py` | `STATED_US[1]['retained']` 285; the docstring "285 and 365 us; 280 at 1x1/1if before AECP's REBOOT" |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | the polls table's `retained` row `285 (280)` |
| `sw/firmware/ctrl/test/test_plat_boot.cpp` (comments) | RS-1 `(ADepartingTheRingRefusedHoldsTheReset)`; RS-2 "in aecp_reboot_mutants.py" at `:76` and in B20's comment `:982` |
| `sw/firmware/ctrl/test/plat_mutants.py` (comments) | R822-5-R1: the tests named for B20, B19, B23; RS-2 |
| `docs/design/REBOOT_RESET.md` | RS-2 at `:315`, `:316`; R822-5-R2 at `:316`; R822-5-R3 at `:297` |
| `sw/firmware/ctrl/plat/README.md` | R822-5-R3 at `:89` |
| `sw/firmware/ctrl/plat/ctrl_plat.h` (comment) | R822-5-R3 at `:38`, within its line |

## Results

- Retained: `poll_grade` 285, both load columns' `item.retained` 285, `record.srp` 285 at 1x1/1if; 365 each at 8x8/2if.
- The statement survey (`scripts/statement_survey.py`): 0 conflicts among the pin's tables at `33b0d03a` (F1 the only
  one at `d3566d44`); 11 donor-against-pin differences, each identical at #902's head `41ca9f87` (the PR body lists
  them).
- Image identity: the fixture's and the platform's split images at 1x1/1if and 8x8/1if, ELF and loadable binary, 8 of
  8 byte-identical between `d3566d44` and `33b0d03a`.
- The gates rerun at `33b0d03a`: the PR body's round 6 table.

## Not taken

- R821-5 S1, S2 and R822-5's suggestions S1 to S11: optional, outside the ruling.
- R821-4 S-A/S-B/S-C: optional, retained.

## Status

STOP at `187eeed89235d5ab7ce68bcd4953c7ef118e9245` (`665-s2b-cycles` -> `dev-soft-core`):
- nine ordinary commits on round 29's head `b2d39235` (the ruling's items 1 to 3);
- then one merge commit of the TSN stack pin move's round 4 head `8bc1dfc0` (PR #892), which carries `dev-soft-core` `0fb66211`.

No rebase, no force, no amend. The tsn-c-stack submodule stays at `715589c`; no change to tsn-c-stack, lwSRP or any donor. This lane makes no RTL or mailbox-contract change; the merge brings `dev-soft-core`'s own.

**Why STOP:** at the merge, the size fixture's 8x8 image with two interfaces plans 58.5 RAMB36, against the 58.0 the ruling holds it at (the owner's decision caps it at 58.5, refused).
- Its `rom` is 123,808 B, in the 61 granules it already took at round 29.
- Its `sram` is 113,168 B: KLJ3's stage and open bits push it 528 B past the 55 granules round 29 filled.
- Neither side is over alone.
- The CPU budget harness's 8x8/2if build is refused at the same plan, so the re-grade the merge owes cannot run.

Getting back to 58.0 needs 928 B of `rom` or 528 B of `sram`, a firmware change outside this round, or a ledger decision.

- **1x1/1if: 0.486 at the pin and 0.483 in the column with tsn-c-stack#32**, each held at 0.70 by `load_grade.py --check` (exit 0) on round 29's costs; the merge's costs are not yet measured.
- **8x8/2if: 0.816 at the pin** on round 29's costs, held by the flip check, which exits 1; the 8x8/2if flip waits on #890.
- **Decision D's tier bounds by every source:** 1x1/1if misses tier 1 at R4, 66.12 ms against 20 ms; the tiers are #894's.

The full gate pass did not run at this head ([How to validate](#how-to-validate)).


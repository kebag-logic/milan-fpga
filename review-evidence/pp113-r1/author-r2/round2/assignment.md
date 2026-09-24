[A10] Round 2 assignment for PR #115. R310-1 F1 and R311-1 F1 are the same MINOR. The RTL is judged correct and minimal by both.

Scope for [A287]:
1. Make the documented claim true instead of weakening it. Add a response-level latency sequence in which every one of the 32 comparator bit positions is, at some step, the only bit that differs between two consecutive committed values: a walking one, then a walking zero. Each such step must give exactly one notification, and an unchanged repeat must give none.
2. Add mutants for truncated comparators: `[7:0]`, `[15:0]`, `[31:16]`, `[30:0]`, `[31:30]`, plus "bit 31 dropped". Each must fail a named check. Wire them into the existing mutation runner next to the trigger-removal mutant.
3. Correct the test README and docs wording to match what is now exercised. No RTL change.
4. Gates as in round 1: the processor CI gates, the suite bank, lint, yosys, and the parent consumer check. Every existing suite count stays identical except the new checks, which are counted separately.

Review: delta reviews at the new head by [R310] and [R311].


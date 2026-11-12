**Proposed issue (the manager opens it; S2b round 28's finding under the ruling's item 4)**

Title: Mark II split: the flip at 1x1/1if misses tier 1 at R4 by every source (`flip_grade.py --check --point 1x1/1if`)

The S2b lane (#665) holds each point's flip to decision D's tier bounds (round 28 ruling, item 4): `tb/verilator/ctrl_service_budget/flip_grade.py --check` solves the rows by every source (`rows_grade.py`, round 22's response-time method on this tree's pin costs) and holds R4 to tier 1's 20 ms, R5 and R6 to SRP's 90 ms, the first queued notice to 20 ms and the last to 125 ms. The flip at 1x1/1if must pass it at that point.

**Evidence at S2b's round 28 head** (the check's own output):
- 1x1/1if R4 (the AECP channel's last record of its burst, beside the composed burst, every notice queued): **73.02 ms** by every source against 20 ms. Its largest terms: SRP's records ahead of AECP's, 16.50 ms; the other channels' records, 10.96 ms; the retained retries, 9.00 ms.
- 1x1/1if R5 37.19 ms and R6 32.69 ms, within SRP's 90; the first queued notice at its 20 ms bound and the last at 22 ms, within 125.
- The cause the model shows: THE DRAIN (`ctrl_loop.h`) takes SRP's records first, past `CTRL_LOOP_RX_PER_PASS`, and a pass that took more than that takes no other channel's. Round 23's tier design (a tier-1 record served before any tier-2 work, tier-2 work in slices of a stated length with tier 1 checked between them) is not built. Round 22's model of THE DRAIN in slices of 1 gave R4 34.76 ms at 1x1/1if, over 20 as well.
- By measurement (the CPU budget harness), R4's rows fit: the least AECP row margin at 1x1/1if is 10.434 ms in arm A and 8.349 ms in the `answering-every-port` arm. Round 23 rules that no row is held by measurement alone.

**Acceptance**
1. `python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if` exits 0 at the 1x1/1if flip's head: every row by every source within its tier's bound, at that head's stated costs.
2. `flip_grade.py --selftest` refuses every one of its controls at that head.

**Options** (the owner chooses): build round 23's tiers (THE DRAIN in slices with tier 1 between them) and measure them; or a decision on R4's bound or on how its every-source count charges THE DRAIN's backlog.

**Dependencies:** #665 (the flip, due around 11-20); #890 (8x8/2if, where every solved row misses as well: R4 489.97, R5 162.96, R6 149.57 ms, and the first queued notice is stated at 22 ms against 20).

Relates to #665.

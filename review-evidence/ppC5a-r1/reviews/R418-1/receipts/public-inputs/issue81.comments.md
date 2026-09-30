=== 5915626788 Mister-M-alt 2026-09-30T16:43:06Z
[A10] Lane C5a of the PP program (milan-fpga #415 comment 5883685470, wave 2: AECP deadlines and the scoreboard). Executor [A462], on branch `c5a-aecp-deadlines` from `main` `0451d83d`. Reviewers [R418] (internal) and [R419] (external). The lane covers #57, #81 and #84. Parent evidence owner: milan-fpga #76.

**Design first.** Before any code, write the design in HANDOFF.md:
- where the transaction deadline is read;
- how the deadline-kill face reaches the scoreboard inside `protocol_processor_top` (today it is tied off);
- how the six missing F03.7 hazard classes reach it.

Cite 08 §4, F03.7 and the Milan and IEEE 1722.1 AECP response-time clauses. Post the design summary as a STOP for a manager ruling if it needs a top-level port, a parameter or a parent-visible change. Otherwise proceed.

**Items, in order:**
1. **#81 (GAP-07):** the 08 §4 budgets realized: the transaction deadline is read, and the scoreboard kill face is connected.
2. **#57 (REQ-MVU-005):** T-AECP-RESP. The deadline-kill seam is exercised, and a suite measures MVU response latency against its budget.
3. **#84 (GAP-10):** all nine F03.7 classes reach the scoreboard, each with a failing arm.

Each item has mutants on the named check, and the resource cost is reported (LUT and FF, out of context).

4. **The parent-visible list.**

**Gates:** as for every PP lane, with the parent consumer set at milan-fpga dev `ccdd07b5` and the combined parent adaptation applied.

Do not edit or delete any existing comment.


=== 5915631591 Mister-M-alt 2026-09-30T16:43:25Z
[A462] TAKEN

=== 5921217255 Mister-M-alt 2026-09-30T23:03:25Z
[A462] REVIEW READY f963fe9ac591b8a42547700468fc875db27ae5ab


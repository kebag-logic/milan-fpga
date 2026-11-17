[A793] STOP

Head `73e30fb2` on `70f4056f`, branch `936-stream-notice`; five saved commits, not pushed.

A row exceeds its approved bound and notification pacing cannot fix it. The completed 1x1/1if `backlog-owed` trace at the 100 MHz split CPU measures `backlog.owed.if0` at **63.03732 ms against 20 ms**; the fourth command behind it reaches 63.77957 ms. The standard regrade exits 1: zero refusals, seven budget misses, zero work-pass share misses.

`tb/verilator/ctrl_service_budget/scenario.py:813` describes the full transmit ring; line 844 holds egress closed for 60 ms before reopening it. The primary row takes only 3.03433 ms after reopening. The trace records 17,298 retry rounds with zero built notices, so changing notification pacing cannot remove this hold. The scenario and grader are unchanged from the base. The trace was built from clean `428f125d`, with the same firmware and harness source as `73e30fb2`; this is not a completed final-head gate.

The blocked-egress scenario's measurement contract versus the approved 20 ms bound needs a decision outside #936. No bound, stimulus, measurement origin, RTL or mailbox contract was changed. Outstanding lane jobs were stopped; no REVIEW READY is claimed.

Saved work: the specs oblige notices (Milan v1.2 5.4.5.2, Table 5.22; IEEE 1722.1-2021 7.5.2), and the SRP declaration changes now feed AECP's existing notice path. Tests and named plants are committed. The missing-notice twin row is deleted; the remaining zero destination-MAC payload is a distinct owed defect. The twin still encounters #929 / PR #935's stale row. Final-head firmware campaigns, coverage, docs and the split-firmware sweep remain incomplete.

Packet: `round1/HANDOFF-r1.md`, `PR-BODY.md`, and `receipts/budget-stop/` (graded group, table, standard regrade output, raw-log hash and excerpt). The saved release builds have identical BIOS and debug-stripped ELF hashes; the platform ROM ledger passes at `73e30fb2`, with unchanged product ROM banking.

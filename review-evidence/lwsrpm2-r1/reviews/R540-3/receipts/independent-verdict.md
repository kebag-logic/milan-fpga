# R540-3 independent verdict (written before reading prior public findings at this head)

Head 82422d6ffe38d430576cd9d874a45b9e124e6c63, tree 02fda6f08254fc7dd5c259c996cfbb31e76682d7.

Verdict: NEGATIVE.

- R540-2-01: RESOLVED (probe_rx p1a-p1d pass in both profiles; changed-in-only reversal killed).
- R540-2-02: RESOLVED (p2, p2b, p2c pass in both profiles; stream-list-boundary reversal killed).
- R540-2-03: RESOLVED (author reversals for x02-x07, x12, x16 equivalents all killed with named tests).
- R540-2-R1, R540-2-R2: RESOLVED (exact text applied).
- New R540-3-01 MINOR (Robustness, Tests, Docs): Flush! via mrp_port_role_change under reservation failure is silently dropped, unreported and not retried; withdrawal waits for LeaveAll plus LeaveTime. Both profiles; pre-existing at a9cd5ef5.
- New R540-3-02 MINOR (Robustness, Tests): Talker replacement under reservation failure indicates Join(Talker Failed) before Leave(Talker Advertise). Both profiles; converges; pre-existing.
- New R540-3-03 MINOR (Tests, Docs): plants y01 (stop after failure), y02 (policy mask honoured), y07 (no reservation without policy) survive both suites; probes show each is observable.

| Lens | Result |
| --- | --- |
| Conformance | CLEAN |
| RTL | CLEAN (no HDL; embedded/freestanding checks pass) |
| Robustness | UNCLEAN (R540-3-01, R540-3-02) |
| Tests | UNCLEAN (R540-3-01, R540-3-02, R540-3-03) |
| Docs | UNCLEAN (R540-3-01, R540-3-03) |

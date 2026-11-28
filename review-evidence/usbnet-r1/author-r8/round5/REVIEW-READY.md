Status: NOT REVIEW READY — the required 100 Mb/s egress allowance remains unproved.

Candidate: `ddda29e1e28ec5b1a58786a750fd1f21b8f6c0d0`. Nothing pushed or posted; bench and flash untouched.

The implementation follows the [ruling on #1020](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7213370880). The firmware LED observer and its 45 plants are removed. No firmware-written LED register or LED code remains; the diagnostic state is read-only. LD2 and LD3 use registered fabric predicates and two-stage synchronization. Their exact semantics and source traces are in [CDC findings](receipts/CDC-FINDINGS.md).

Completed evidence: byte-identical Arty and ALINX control ELFs and map headers at matching pins; all 147 census cases across eight images with the unchanged rule; the installed scheduling row is a fixed point; four routes with sixteen passing internal timing corners; 92,755 functional checks; four SET_CLOCK_SOURCE cases; all 72 named plants; and existing shaping regressions. The command tests use explicit lock levels and are not a full processor-bus/physical-lock test. [Full handoff](HANDOFF-r5.md) records pins, hashes, bounds and limitations.

| Quantity | Qualified value | Unchanged bound |
|---|---:|---:|
| Load | 0.5004771140 | 0.70 |
| ACMP CPU row | 29.77 ms | 30 ms |
| ACMP plus conservative local-merger wait | 29.808075 ms | 30 ms |
| txL | 48.82 ms | 49 ms |
| Last notice | 117.47 ms | 140 ms |
| Longest measured pass | 1.7846875 ms | 2 ms |

The [local receive wait](receipts/MAILBOX-WAIT.md) fits the ACMP margin. #969's disposition and seven held-egress misses remain explicitly recorded under the same qualification method; census PASS does not clear the physical egress proof.

The blocking gap is the [egress allowance](receipts/EGRESS-FINDING.md): the published gigabit capacity proof does not establish a 100 Mb/s bound that includes the injected frame. A capacity witness refutes that argument at this rate; it does not claim reachable production backlog or an observed endpoint deadline violation. No bound is changed.

Two baseline gate problems remain reproduced: six bare-metal wording findings and two stale register-reference artifacts. Existing whole-image CDC and external-I/O findings remain. Full exhaustive repository and hosted checks, independent review, physical validation and slave-FIFO attachment are outstanding. Neither issue is complete, and no executor approval is asserted.

[A307]

Closes #559

Status: ready for independent review.

Description: measure the complete saved-state capture on the product CPU and SoC buses under continuous controller descriptor traffic. Across 16 captures per shape, the worst 8x8 result is 19.00433 ms, giving 2.6310x margin against the unchanged 50 ms hold. The 1x1 maximum is 6.55479 ms. The first assigned remedy applies: 50 ms is enough for this simulation route; firmware and hold settings are unchanged.

How to reproduce: use the commands and environment links in [snapshot ownership section 18](docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md#18-cost). Its linked measurement receipt contains all 32 rows and input hashes. Each capture checks the complete closed-record copy, attestation, ownership and traffic during the copy.

How to validate: all requested local gate commands returned zero, including both builder modes, the backend and firmware suites, and both documentation inventory modes. Both named negative controls are detected. The compiler-absent run explicitly skips its compiled census; both builder modes lack the historical placement calibration report.

DoD: the runnable harness, measured remedy, section 18 and UNRESOLVED 6 are updated. Physical timing and memory-ordering claims remain open. Independent review and hosted checks remain to be completed.

REVIEW READY 166dfdc9f (branch 1009-save-latency, base dev-soft-core 5de21ff3)

The store's binding-class window and the delta-frame save (#1009, #876). The PR body has the change, the measurements and what is still owed; receipts/ holds the gates, measurement table, image sign-off, ledger and identity lists, and the earlier frame, burst and first-save measurements.

Owed before merge: the board measurement of BIND_RX response to durable, and the power-cycle cases on images built from this change. dev-soft-core has moved to c34e7d8b (PR #987), so a merge and re-run of affected gates is needed.

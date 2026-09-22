# Failed author probes

Original production-driver failures are retained byte-for-byte under `original-public/`, with the public reproduction script and source provenance. They establish the original in-place mutation residue and sweep continuation defects.

Author-stage probes retained without replacing their logs:

- `001-foreign-state-oracle/`: first fixture used scheduler-state equality for a foreign sibling. The process changed from running to sleeping; the assertion was too strong. The archived fixture source and observed tool output are retained. The corrected check verifies start identity, a non-zombie state, and a live Popen child.
- `receipts/sweep-002/` and `002-transition/`: INT at the tally transition returned 130 but left the lock owner file. Root escalation preempted terminal cleanup. Final code stops the root, terminates descendants first and resumes its pending trap.
- `receipts/lifecycle-002/`: nested sweep cancellation left private mutation scratch. Intermediate owners now receive a bounded opportunity to finish after stubborn leaves die. `receipts/nested-003/` records both corrected nested signal paths.
- `receipts/python-idiom-001/`: one new `os.path.samefile` use exceeded the fixed ratchet. Changed to `Path.samefile`; no budget edit.
- `receipts/evidence-001/`: new lifecycle source reader lacked an exact-file disposition. Added its orchestration/input-integrity classification; no discovery or budget changes.
- `004-integrity-symlink-mode/`: the external receipt collector incorrectly applied regular-file execute-bit comparison to a vendor README symlink. Its bytes and pin were already correct. Corrected the collector; production snapshot copies only required dependency source directories.
- `receipts/gptp-shadow-full-001/`: real baseline passed 309/309, then input preflight refused RTK's `GIT_PAGER=cat`. The presentation-only variable is now allowed and has a positive control. Identity overrides still fail.
- `receipts/log-edges-before/`: retained preflight output exposed stale prior logs and a relative-output-path regression. `probe_log_edges.py` reproduces both with production-driver handshake fixtures. `receipts/log-edges-after/` records both corrected results.

No failed run is counted as passing validation. Intermediate failures occurred before the final source head. Final receipts name their exact head and tree.

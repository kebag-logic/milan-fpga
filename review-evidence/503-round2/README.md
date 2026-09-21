# PR 503, second contract-review evidence

Byte-identical copies of the completed R217 and R218 reports, focused fault-injection sources and recorded observations. SHA256.json identifies every copied file. Both reviewed page head `40d14d92bfcf3823ed7b227537630f444b1f4f73` and executable evidence `ca8cb5943f885c22aec397ff75059e2d4791f4fb`. Both verdicts are NEGATIVE and published on PR #503. All five review lenses remain open.

This archival branch must never be merged. The immutable proposal evidence supplies the original model, runner and baseline build instructions. Reviewer scripts contain explicit checkout and scratch paths; adapt those constants in disposable copies before reproduction. No private reasoning or agent transcript is included. Compiled binaries and generated build trees are excluded.

R217 independently ran 17 builds, 175 focused runs, 1,565 checks and seven process controls. Its probes reproduce repeated/balanced header errors, descriptor-memory failure and timeout, and the original fixed rollback case. R218 reproduced the entire 55-build, 230-run, 2,524-check evidence byte-for-byte and all seven process controls, plus the repeated-header and original failure/timeout probes. Their reports distinguish successful baseline reproduction from the remaining contract defects. Publication is evidence, not approval.

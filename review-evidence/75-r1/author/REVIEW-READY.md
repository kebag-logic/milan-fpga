[A386] REVIEW READY

Refs #75. Local head: `0e8ec0d2bd78b1d87f84d96e095966ae7c07c525` (not pushed).

Changed: only `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md`.
The assigned image passes identity checks before and after measurement.
Measured matching CRF streams, one direction at a time, with a two-second
unbound hold and response-to-first-valid-AVTP timing on one tap clock.

| Direction | Cycles | Below 1 s | Min, s | Median, s | p95, s | Max, s | Result |
|---|---|---|---|---|---|---|---|
| DUT listener | 100 | 100 | 0.006641168 | 0.110279505 | 0.188503018 | 0.204858977 | PASS |
| DUT talker | 100 | 100 | 0.000296777 | 0.019165141 | 0.039613701 | 0.117736084 | PASS |

p95 uses nearest rank. The early-stop condition never triggered.
Restart latency shows no progressive growth; both fitted slopes are negative.
Captured MSRP remains bounded, with periodic refresh and short LeaveAll
bursts. Every captured declaration and withdrawal is attributed to the DUT
or adjacent bridge. The reference peer's original link-local exchange is
outside this tapped segment.

Separate observation: the initial DUT-talker bind takes 6.889398468 seconds
and is excluded from numbered reconnect quantiles. Bridge Listener Ready
arrives after 6.888605306 seconds; CRF follows 0.000793162 seconds later.
The capture locates that wait before Ready reaches the DUT but does not
establish the peer-side cause. AAF remains unmeasured.

Acceptance: all three #75 criteria PASS for the measured CRF reconnects.
This operator evidence does not close the issue or provide independent review.
The initial-bind delay and unmeasured format remain explicit limitations.

Validation at this exact head: all nine assigned gates return 0:
`docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`,
`check_em_dash.py --base 8bc97021`, `check_doc_paths.py`,
`ci_scope.py --selftest`, `check_baremetal_only.py --check`,
`check_feature_status.py --self-test`, and `git diff --check`.
Commands use the physical candidate worktree, explicit timeouts, and no pipes.
All 206 full captures replay successfully; live and offline timing agree.
All raw sizes and SHA-256 values verify, with zero capture-host packet drops.
The new page also passes direct prose and rendered-table checks.

Full restoration PASS: all 18 stream states unbound, original settings and
image CRCs unchanged, final UART grading 10/10, final capture quiescent.
Temporary scripts and the capture driver are removed; the original capture
interface set is restored. All children exited and the bench lock is free.
No power, reboot, flash, wiring, or excluded-equipment action occurred.

Evidence packet `2026-09-23/75-a386` contains `HANDOFF.md` with one row per
cycle, `PR-BODY.md`, exact gate logs, acquisition and analysis source, and
recursive `MANIFEST.sha256` files. `RAW-ARTIFACTS.json` indexes raw captures
outside the packet by size and SHA-256. No push or PR operation was performed.

[A386]

Refs #75

Records phase-2 CRF reconnect measurements on the assigned running image.
All 100 DUT-listener and 100 DUT-talker reconnects resume below one second.
Neither direction shows progressive latency growth or a sustained MSRP storm.

| Direction | Cycles | Min, s | Median, s | p95, s | Max, s | Result |
|---|---|---|---|---|---|---|
| DUT listener | 100 | 0.006641168 | 0.110279505 | 0.188503018 | 0.204858977 | PASS |
| DUT talker | 100 | 0.000296777 | 0.019165141 | 0.039613701 | 0.117736084 | PASS |

The separate initial talker bind takes 6.889398468 seconds.
Bridge Listener Ready arrives after 6.888605306 seconds; CRF follows
0.000793162 seconds later. The captured segment cannot establish the
peer-side cause. This initial bind is excluded from reconnect quantiles.
AAF remains unmeasured; this evidence does not close the issue.

Adds only docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md, covering
method, identity, growth, every captured MSRP exchange, counter limits,
restoration, and all 206 raw capture sizes and SHA-256 values.
Raw captures remain outside the repository and evidence packet.

Full restoration passes: all 18 stream states are unbound, original settings
and image checks match, final UART grading is 10/10, and the final wire
capture has no valid CRF. Temporary scripts and the capture driver are
removed. Every child exited and the bench lock is free.

Validation: all nine assigned documentation and policy gates return zero.
All 206 captures replay successfully; live and offline timing agree.
The page passes direct prose analysis and rendered-table checks.
The evidence packet includes HANDOFF.md, recursive MANIFEST.sha256 files,
acquisition and analysis source, and complete per-cycle records.

Independent reviews remain required.

Local head: `0e8ec0d2bd78b1d87f84d96e095966ae7c07c525`.

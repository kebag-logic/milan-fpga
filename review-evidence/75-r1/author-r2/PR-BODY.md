[A386]

Refs #75

Records phase-2 CRF reconnect measurements on the assigned running image.
All 100 DUT-listener and 97 demonstrated DUT-talker restarts remain below one second.
Three talker attempts never stop transmitting and are excluded from restart quantiles.
The talker direction remains three demonstrated restarts short of the requirement.
Neither demonstrated series shows progressive latency growth or a sustained MSRP storm.

| Direction | Cycles | Min, s | Median, s | p95, s | Max, s | Result |
|---|---|---|---|---|---|---|
| DUT listener | 100 | 0.006641168 | 0.110279506 | 0.188503018 | 0.204858977 | PASS |
| DUT talker | 97 | 0.017426921 | 0.019174613 | 0.042346644 | 0.117736084 | 97 pass; count incomplete |

The separate initial talker bind takes 6.889398468 seconds, owned by #606.
The DUT declares no Talker Advertise before that bind; its first follows
the response by 0.079237250 seconds. The bridge remains silent until its
LeaveAll at +6.080007742 seconds. Listener Ready arrives at +6.888605306
seconds, with valid CRF another 0.000793162 seconds later.
The initial bind differs in DUT-side state; causal attribution remains open.
It has no preceding disconnect and two-second hold, so the recorded
round-2 decision excludes it from criterion 1 and reconnect quantiles.
AAF remains unmeasured; #75 stays open.

Adds docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md, covering
method, identity, growth, every captured MSRP exchange, counter limits,
restoration, and all 206 raw capture sizes and SHA-256 values.
The findings index links this measured result and its open exceptions.
Raw captures remain outside the repository and evidence packet.

Full restoration passes: all 18 stream states are unbound, original settings
and image checks match, final UART grading is 10/10, and the final wire
capture has no valid CRF. DUT Stream Output 1 retains a MAAP-range destination
where its initial dynamic state was all-zero; this is not a setting or binding.
Temporary scripts and the capture driver are
removed. Every child exited and the bench lock is free.

## Round 2

[A389] answers both round-1 reviews using recorded data only.

- The SRP citation uses the pinned upstream URL and resolves without submodules.
- Every cycle publishes its asserted stop result and DUT/active-talker counter deltas.
  Talker attempts 13, 24, and 75 contain continuous 2 ms traffic through the hold.
  Their zero start/stop increments explain the +97/+97 retained counter totals.
  These non-restarts and the missing three cycles remain owned by #75.
- Criteria 1 and 2 explicitly cover the two CRF pairs after `DISCONNECT_RX`,
  a two-second hold, and `CONNECT_RX`. The 6.889-second initial-bind exception
  appears in the acceptance table with #606 and its exclusion rationale.
- The page adds slope confidence intervals, tap resolution, the complete
  measured validity predicate, the restore residue, and the findings-index row.

The round-2 addendum contains independent replay source, all 200 stop checks,
recomputed distributions, slope intervals, capture-size explanations, and source hashes.
The original packet remains unchanged.

All nine assigned gates return zero at the local committed head.
The documentation gate also passes in an exact-head clone without submodules,
then again without Git metadata. Every table renders with all cells preserved.
Direct page prose analysis and the full committed-diff whitespace check pass.
These are local results; no new hosted-context pass is claimed.

Independent reviews remain required.

Local head: `5c7577e51702b00683a121f97a9806c167eb072b`. No push or PR edit performed.

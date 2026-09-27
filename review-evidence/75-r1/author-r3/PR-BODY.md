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
Cycle 1 also lacks declarations through its hold, yet restarts in 0.117736084 s.
Only 99/100 holds carry DUT declarations; #606 must consider this exception.
Causal attribution remains open.
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
  Round 3 assigns these non-restarts to #608; the missing three restarts remain under #75.
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

Round-2 head: `5c7577e51702b00683a121f97a9806c167eb072b`.

## Round 3

[A391] answers both round-2 reviews using recorded data only.

- Declaration-only replay derives 99/100 holds with DUT Talker Advertise.
  Cycle 1 withdraws, carries only Mt through the hold, and restarts in
  0.117736084 s. Its first declaration follows reconnect success by
  0.111313165 s; Ready follows 0.006299407 s later. This counterexample
  qualifies the initial-bind inference and supplies evidence for #606.
- Cycles 13, 24, and 75 receive bridge Listener Lv at 0.009770679,
  0.010356881, and 0.025307595 s after disconnect success. Re-declaration
  arrives only after reconnect success: +0.073776413, +0.018704540,
  and +0.018687732 s. The DUT continues at 2 ms intervals throughout,
  with no STREAM_STOP increment. This supports DUT-side non-stop behavior
  at the tapped boundary; internal receipt and cause remain unproved.
  #608 owns that behavior and is linked from stop checks, acceptance,
  and the findings index. The addendum includes all three cycles' records.
- Replay classification and consistency checks use explicit conditions.
  Optimized execution is refused, including PYTHONOPTIMIZE. Printed totals
  and excluded cycle identifiers derive from the computed rows.
- All 200 stop results, distributions, and slope intervals remain unchanged.
  Raw MSRP replay matches the 100 talker TSVs and the setup TSV.
  Focused controls reject the old declaration claim and verify both refusals.

The round-3 addendum retains source hashes, exact Listener-event times,
bracketing CRF times, the declaration census, and publication transformations.
The original round-1 and round-2 packets remain unchanged.

All nine assigned gates pass at `9c18068512dec844d24fdff7fe0a3eb0d63c14f5`.
The documentation gate also passes without submodules, then without Git metadata.
The complete committed diff passes its whitespace check.
Table rendering and packet integrity are recorded in the round-3 handoff.
Independent re-review remains required. Refs #75; AAF remains unmeasured.
No push, PR edit, or hardware action performed.

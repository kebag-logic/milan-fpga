[A567]
Closes #168

Return zero talker identifiers on successful UNBIND, retain ACMP status across retries, use CONTROLLER_NOT_AUTHORIZED (16) for lock refusals, and return TALKER_UNKNOWN_ID for invalid DISCONNECT sources. Keep all 16 received VLAN bits in listener and input-stream readback. Check probe responses against the controller of the probe actually sent, and preserve that probe on retry after a same-talker rebind. The parent VID output keeps its existing width and meaning.

## Round 2

Main `09e357fb` is merged. The selected reduction compares before selection and selects the controller byte before its source, retaining all six corrections and their checks. The fresh 1x1 result is 21,614 → 21,643 LUT (+29) and 18,908 → 18,922 FF (+14), within both +40 limits. The six individual deltas sum to +27 LUT / +4 FF; the unreduced combined change was +127 / +14.

Validation: all 33 processor suites pass at baseline and head (1,028,293 and 1,028,384 checks), along with lint, repository checks, matrix consistency and portability synthesis. All 13 affected campaigns and all 17 scratch-parent consumer commands return zero at both revisions. All 18 added controls fail their required checks; the complete ACMP campaign kills 51 controls and passes six goldens. Record comparisons permit only the documented clause-required differences.

The parent report-calibration arm remains unrun because its historical placement report is absent; it is not counted as an executed check.

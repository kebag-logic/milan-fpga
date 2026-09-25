[A305] REVIEW READY
Commit: b94f53cc4e5dbfd9527ba666922a55804515165c (local; not pushed, as assigned).

Round 2 implements assignment items 1-5: explicit slew campaign; boundary-coincident step deduplication and its named control; PHC-measured tail coverage with added-stage rejection; documented and tested guard-streak reset; current campaign inventories and triggers. Product RTL behavior is unchanged this round.

Validation:
- Clean two-CPU default wall clocks: base 516.943 s, round 1 1652.793 s, round 2 952.797 s. The unchanged 1800 s budget retains 847.203 s (47.1%). Default checks: 100 unit, 8 rails, 113 step, 90 slew, all passing.
- Explicit campaigns: servo 8/8; connected 16/16. Connected clean leg: 58/58. Every defect fails its named check, including the added addend stage, removed step exclusion and removed streak reset.
- Published coincidence and tail/latency probes reproduced their expected verdicts. The unit-only deduplication mutant survives; the full slew harness kills it at S5, 2 counts versus 1.
- Receiver and shadow suites pass. All 33 default datapath commands exit 0; affected connected commands were rerun after the final release assertion. Builder, both documentation modes, required-base em-dash, all assigned static gates and 344 behavior scenarios pass. Area reproduces +7 LUT/+2 FF for the servo and 1 LUT/4 FF for isolated alignment.

HANDOFF.md and the full updated PR-BODY.md are ready in the assigned output directory. The builder's board-report calibration arm is NOT RUN because its report is absent. No hardware, push, PR edit or dev merge was performed. Independent re-review and hosted checks and local workflow replication remain for the manager after publication; the #508 overlap remains deferred.

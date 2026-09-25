[A305]

Closes #545

A 100 us PHC slew at 200 ppm could move the CRF integrator and drop LOCKED. The servo now discards and counts every measurement window overlapping the plane's registered correction level, including the partial tail, while holding its integrator, trim and lock. Clean windows resume directly. A boundary-coincident step and slew count their shared window once.

The processor pin advances to `5dce647a`, with regenerated ROM records and current contract references. The level passes through the shadow and follows the effective PHC rate through the existing synchronous pipeline. Correction follows measured completion without a timeout. The connection makes no network-port assumption.

Validation:

- Both 100 us slew directions hold the integrator and command exactly through affected windows. The first clean update stays within 1 ppm and completes within 1.536 s of the disturbance's start; LOCKED holds throughout.
- Boundary, short-pulse, prolonged-level, reset, saturation and replacement-step cases pass. Real Sync pairs prove the level reaches the actual servo. Fractional PHC advances grade tail coverage, and the indication clears after completion.
- Both explicit campaigns pass their named controls: six servo defects and fourteen datapath defects, with two passing positive controls per campaign.
- All assigned local gate commands return zero, including all 33 commands in the default datapath sweep. The servo suites pass 100 unit, 8 rail, 113 step and 90 slew checks; the connected phase passes 58 checks.
- The builder's board-report calibration arm is NOT RUN because the required report is absent. Physical hardware and hosted checks were not run.

The standalone servo adds 7 LUTs and 2 registers. Isolated release alignment adds 1 LUT and 4 registers; memory and arithmetic resources are unchanged. These are isolated parent-logic measurements, not a whole-datapath area delta. The adopted processor's separate published area measurement is outside these figures.

## Round 2

The default servo suite retains unit, rails, step and slew checks. The long slew mutation campaign now runs through the explicit `slew-mutants` target. The 1800-second default budget is unchanged.

A boundary-coincident step case requires one discard. A unit case requires four fresh guard trips after a slew discard, matching the existing step-discard rule. The tail check measures the PHC itself and verifies eventual release. Added controls remove the step exclusion, retain the guard streak, and insert one addend stage without extending the tail. Each fails its named check. Campaign inventories, trigger files and the streak contract are current. Product RTL behavior is unchanged in this round.

| Clean two-CPU default | Base | Round 1 | Round 2 |
|---|---|---|---|
| Local wall clock | 516.943 s | 1652.793 s | 952.797 s |

The base and round-1 runs use CPUs 8-9; round 2 uses CPUs 10-11 on the same shared host. Round 2 leaves 847.203 seconds, or 47.1%, of the budget. The Makefile records the measurement.

The published coincidence, tail, latency and deduplication probes were rerun. Clean probes pass; the boundary-exclusion mutant fails the new shipped case. Shortened-tail controls fail as expected. The unit-only exclusion mutant remains a recorded survivor; its killing case is in the slew suite.

Independent re-review and hosted acceptance remain pending publication of this local head. No push, PR edit or dev merge was performed.

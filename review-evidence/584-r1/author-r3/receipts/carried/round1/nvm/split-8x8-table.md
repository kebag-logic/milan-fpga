# Saved-state cases on the split CPU, 8x8

Clocks, as this run's builds recorded them: CPU 100 MHz (100,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Verdict | Detail |
|---|---|---|
| commit | pass |  |
| step-over-t-svc | caught | every phase's longest step at T_svc (2,000,000 cycles) passes and one cycle past it is caught: capture, erase, idle, poll, program, read, seal |
| valid | pass | 141 apply entries, boot 35,378,320 CPU cycles |
| absent | pass | 0 apply entries, boot 1,595,173 CPU cycles |
| torn | pass | 141 apply entries, boot 55,240,711 CPU cycles |
| version | pass | 0 apply entries, boot 1,593,722 CPU cycles |
| guard | pass |  |
| reorder-settle | caught | apply order: entry 25 is aecp_value_restore, the container needs aecp_restore_settle (141 entries, 141 wanted) |
| reorder-bindings | caught | apply order: entry 0 is aecp_map_restore, the container needs acmp_restore_binding (141 entries, 141 wanted) |
| guard-removed | caught | flash write escaped the journal |
| slow-step | caught | step 0 (idle) takes 30.0058 ms of CPU time, over T_svc 20.0 ms |

Every service step is graded against T_svc = 20.0 ms of CPU time.

Clocks, as this run's builds recorded them: CPU 100 MHz (100,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Service steps | Longest step, CPU cycles | Longest, ms |
|---|---:|---:|---:|
| commit | 1195 | 103,861 | 1.039 |
| valid | 40 | 1,101 | 0.011 |
| absent | 40 | 1,093 | 0.011 |
| torn | 40 | 1,101 | 0.011 |
| version | 40 | 1,093 | 0.011 |
| guard | 40 | 1,216 | 0.012 |

Capture, measured (no bound of its own): 172 records in 173 steps; CPU time 2,888,803 cycles, 28.888 ms; elapsed 6,678,489 cycles, 66.785 ms; longest step 103,861 cycles, 1.039 ms.

Clocks, as this run's builds recorded them: CPU 100 MHz (100,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Phase | Steps | Longest step, CPU cycles | Longest, ms | Within T_svc | Total, CPU cycles |
|---|---:|---:|---:|---|---:|
| capture | 173 | 103,861 | 1.039 | yes | 2,888,803 |
| erase | 1 | 3,674 | 0.037 | yes | 3,674 |
| idle | 628 | 2,639 | 0.026 | yes | 550,566 |
| poll | 57 | 3,789 | 0.038 | yes | 176,492 |
| program | 56 | 79,762 | 0.798 | yes | 4,342,153 |
| read | 224 | 75,427 | 0.754 | yes | 16,563,214 |
| seal | 56 | 34,777 | 0.348 | yes | 1,129,372 |

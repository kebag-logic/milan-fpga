# Saved-state cases on the split CPU, 1x1

Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Verdict | Detail |
|---|---|---|
| commit | pass |  |
| step-over-t-svc | caught | every phase's longest step at T_svc (500,000 cycles) passes and one cycle past it is caught: capture, erase, idle, poll, program, read, seal |
| valid | pass | 44 apply entries, boot 5,050,293 CPU cycles |
| absent | pass | 0 apply entries, boot 506,900 CPU cycles |
| torn | pass | 44 apply entries, boot 8,300,664 CPU cycles |
| version | pass | 0 apply entries, boot 504,932 CPU cycles |
| guard | pass |  |
| reorder-settle | caught | apply order: entry 4 is aecp_value_restore, the container needs aecp_restore_settle (44 entries, 44 wanted) |
| reorder-bindings | caught | apply order: entry 0 is aecp_map_restore, the container needs acmp_restore_binding (44 entries, 44 wanted) |
| guard-removed | caught | flash write escaped the journal |
| slow-step | caught | step 0 (idle) takes 30.2028 ms of CPU time, over T_svc 10.0 ms |

Every service step is graded against T_svc = 10.0 ms of CPU time.

Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Service steps | Longest step, CPU cycles | Longest, ms |
|---|---:|---:|---:|
| commit | 330 | 101,139 | 2.023 |
| valid | 41 | 9,390 | 0.188 |
| absent | 41 | 9,384 | 0.188 |
| torn | 41 | 9,387 | 0.188 |
| version | 41 | 9,387 | 0.188 |
| guard | 41 | 9,351 | 0.187 |

Capture, measured (no bound of its own): 54 records in 55 steps; CPU time 1,367,366 cycles, 27.347 ms; elapsed 27,148,861 cycles, 542.977 ms; longest step 40,906 cycles, 0.818 ms.

Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Phase | Steps | Longest step, CPU cycles | Longest, ms | Within T_svc | Total, CPU cycles |
|---|---:|---:|---:|---|---:|
| capture | 55 | 40,906 | 0.818 | yes | 1,367,366 |
| erase | 1 | 12,431 | 0.249 | yes | 12,431 |
| idle | 203 | 10,012 | 0.200 | yes | 1,926,395 |
| poll | 15 | 11,727 | 0.235 | yes | 171,242 |
| program | 14 | 101,139 | 2.023 | yes | 1,327,091 |
| read | 28 | 96,248 | 1.925 | yes | 2,482,534 |
| seal | 14 | 34,468 | 0.689 | yes | 457,058 |

# Saved-state cases on the split CPU, 1x1

Clocks, as this run's builds recorded them: CPU 100 MHz (100,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Verdict | Detail |
|---|---|---|
| commit | pass |  |
| step-over-t-svc | caught | every phase's longest step at T_svc (2,000,000 cycles) passes and one cycle past it is caught: capture, erase, idle, poll, program, read, seal |
| valid | pass | 44 apply entries, boot 6,765,596 CPU cycles |
| absent | pass | 0 apply entries, boot 499,867 CPU cycles |
| torn | pass | 44 apply entries, boot 11,512,798 CPU cycles |
| version | pass | 0 apply entries, boot 498,218 CPU cycles |
| guard | pass |  |
| reorder-settle | caught | apply order: entry 4 is aecp_value_restore, the container needs aecp_restore_settle (44 entries, 44 wanted) |
| reorder-bindings | caught | apply order: entry 0 is aecp_map_restore, the container needs acmp_restore_binding (44 entries, 44 wanted) |
| guard-removed | caught | flash write escaped the journal |
| slow-step | caught | step 0 (idle) takes 30.0077 ms of CPU time, over T_svc 20.0 ms |

Every service step is graded against T_svc = 20.0 ms of CPU time.

Clocks, as this run's builds recorded them: CPU 100 MHz (100,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Service steps | Longest step, CPU cycles | Longest, ms |
|---|---:|---:|---:|
| commit | 472 | 77,978 | 0.780 |
| valid | 40 | 1,392 | 0.014 |
| absent | 40 | 1,392 | 0.014 |
| torn | 40 | 1,392 | 0.014 |
| version | 40 | 1,392 | 0.014 |
| guard | 40 | 1,392 | 0.014 |

Capture, measured (no bound of its own): 54 records in 55 steps; CPU time 733,406 cycles, 7.334 ms; elapsed 1,545,640 cycles, 15.456 ms; longest step 26,152 cycles, 0.262 ms.

Clocks, as this run's builds recorded them: CPU 100 MHz (100,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Phase | Steps | Longest step, CPU cycles | Longest, ms | Within T_svc | Total, CPU cycles |
|---|---:|---:|---:|---|---:|
| capture | 55 | 26,152 | 0.262 | yes | 733,406 |
| erase | 1 | 3,906 | 0.039 | yes | 3,906 |
| idle | 319 | 2,535 | 0.025 | yes | 327,031 |
| poll | 15 | 3,767 | 0.038 | yes | 45,247 |
| program | 14 | 77,978 | 0.780 | yes | 1,047,919 |
| read | 54 | 75,369 | 0.754 | yes | 4,001,152 |
| seal | 14 | 19,886 | 0.199 | yes | 265,443 |

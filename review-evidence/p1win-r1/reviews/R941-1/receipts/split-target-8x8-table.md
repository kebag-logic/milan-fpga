# Saved-state cases on the split CPU, 8x8

Clocks, as this run's builds recorded them: CPU 100 MHz (100,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Verdict | Detail |
|---|---|---|
| commit | pass |  |
| step-over-t-svc | caught | every phase's longest step at T_svc (2,000,000 cycles) passes and one cycle past it is caught: capture, erase, idle, poll, program, read, seal |
| valid | pass | 141 apply entries, boot 35,363,372 CPU cycles |
| absent | pass | 0 apply entries, boot 1,593,958 CPU cycles |
| torn | pass | 141 apply entries, boot 55,229,348 CPU cycles |
| version | pass | 0 apply entries, boot 1,592,573 CPU cycles |
| guard | pass |  |
| reorder-settle | caught | apply order: entry 25 is aecp_value_restore, the container needs aecp_restore_settle (141 entries, 141 wanted) |
| reorder-bindings | caught | apply order: entry 0 is aecp_map_restore, the container needs acmp_restore_binding (141 entries, 141 wanted) |
| guard-removed | caught | flash write escaped the journal |
| slow-step | caught | step 0 (idle) takes 30.0093 ms of CPU time, over T_svc 20.0 ms |

Every service step is graded against T_svc = 20.0 ms of CPU time.

Clocks, as this run's builds recorded them: CPU 100 MHz (100,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Service steps | Longest step, CPU cycles | Longest, ms |
|---|---:|---:|---:|
| commit | 1192 | 101,400 | 1.014 |
| valid | 40 | 1,321 | 0.013 |
| absent | 40 | 1,313 | 0.013 |
| torn | 40 | 1,321 | 0.013 |
| version | 40 | 1,313 | 0.013 |
| guard | 40 | 1,152 | 0.012 |

Capture, measured (no bound of its own): 172 records in 173 steps; CPU time 2,960,107 cycles, 29.601 ms; elapsed 7,437,852 cycles, 74.379 ms; longest step 101,400 cycles, 1.014 ms.

Clocks, as this run's builds recorded them: CPU 100 MHz (100,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Phase | Steps | Longest step, CPU cycles | Longest, ms | Within T_svc | Total, CPU cycles |
|---|---:|---:|---:|---|---:|
| capture | 173 | 101,400 | 1.014 | yes | 2,960,107 |
| erase | 1 | 4,205 | 0.042 | yes | 4,205 |
| idle | 625 | 2,689 | 0.027 | yes | 686,851 |
| poll | 57 | 3,899 | 0.039 | yes | 193,148 |
| program | 56 | 79,104 | 0.791 | yes | 4,332,412 |
| read | 224 | 75,843 | 0.758 | yes | 16,690,389 |
| seal | 56 | 35,524 | 0.355 | yes | 1,149,116 |

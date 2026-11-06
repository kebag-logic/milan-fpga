# Saved-state cases on the split CPU, 8x8

Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Verdict | Detail |
|---|---|---|
| commit | pass |  |
| step-over-t-svc | caught | every phase's longest step at T_svc (500,000 cycles) passes and one cycle past it is caught: capture, erase, idle, poll, program, read, seal |
| valid | pass | 133 apply entries, boot 24,519,265 CPU cycles |
| absent | pass | 0 apply entries, boot 1,747,362 CPU cycles |
| torn | pass | 133 apply entries, boot 37,436,744 CPU cycles |
| version | pass | 0 apply entries, boot 1,745,393 CPU cycles |
| guard | pass |  |
| reorder-settle | caught | apply order: entry 25 is aecp_value_restore, the container needs aecp_restore_settle (133 entries, 133 wanted) |
| reorder-bindings | caught | apply order: entry 0 is aecp_map_restore, the container needs acmp_restore_binding (133 entries, 133 wanted) |
| guard-removed | caught | flash write escaped the journal |
| slow-step | caught | step 0 (idle) takes 30.2724 ms of CPU time, over T_svc 10.0 ms |

Every service step is graded against T_svc = 10.0 ms of CPU time.

Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Service steps | Longest step, CPU cycles | Longest, ms |
|---|---:|---:|---:|
| commit | 643 | 132,073 | 2.641 |
| valid | 43 | 9,788 | 0.196 |
| absent | 43 | 9,550 | 0.191 |
| torn | 43 | 9,773 | 0.195 |
| version | 43 | 9,550 | 0.191 |
| guard | 43 | 9,491 | 0.190 |

Capture, measured (no bound of its own): 164 records in 165 steps; CPU time 5,168,647 cycles, 103.373 ms; elapsed 82,090,909 cycles, 1641.818 ms; longest step 132,073 cycles, 2.641 ms.

Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Phase | Steps | Longest step, CPU cycles | Longest, ms | Within T_svc | Total, CPU cycles |
|---|---:|---:|---:|---|---:|
| capture | 165 | 132,073 | 2.641 | yes | 5,168,647 |
| erase | 1 | 12,537 | 0.251 | yes | 12,537 |
| idle | 216 | 10,248 | 0.205 | yes | 2,101,484 |
| poll | 53 | 12,168 | 0.243 | yes | 632,282 |
| program | 52 | 101,549 | 2.031 | yes | 5,246,691 |
| read | 104 | 96,789 | 1.936 | yes | 9,812,290 |
| seal | 52 | 34,862 | 0.697 | yes | 1,793,766 |

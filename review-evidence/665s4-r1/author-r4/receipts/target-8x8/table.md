# Saved-state cases on the split CPU, 8x8

Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Verdict | Detail |
|---|---|---|
| commit | pass |  |
| step-over-t-svc | caught | every phase's longest step at T_svc (500,000 cycles) passes and one cycle past it is caught: capture, erase, idle, poll, program, read, seal |
| valid | pass | 133 apply entries, boot 24,423,878 CPU cycles |
| absent | pass | 0 apply entries, boot 1,746,898 CPU cycles |
| torn | pass | 133 apply entries, boot 37,255,159 CPU cycles |
| version | pass | 0 apply entries, boot 1,744,933 CPU cycles |
| guard | pass |  |
| reorder-settle | caught | apply order: entry 25 is aecp_value_restore, the container needs aecp_restore_settle (133 entries, 133 wanted) |
| reorder-bindings | caught | apply order: entry 0 is aecp_map_restore, the container needs acmp_restore_binding (133 entries, 133 wanted) |
| guard-removed | caught | flash write escaped the journal |
| slow-step | caught | step 0 (idle) takes 30.2139 ms of CPU time, over T_svc 10.0 ms |

Every service step is graded against T_svc = 10.0 ms of CPU time.

Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Case | Service steps | Longest step, CPU cycles | Longest, ms |
|---|---:|---:|---:|
| commit | 642 | 131,929 | 2.639 |
| valid | 43 | 9,784 | 0.196 |
| absent | 43 | 9,579 | 0.192 |
| torn | 43 | 9,775 | 0.196 |
| version | 43 | 9,594 | 0.192 |
| guard | 43 | 9,619 | 0.192 |

Capture, measured (no bound of its own): 164 records in 165 steps; CPU time 5,161,328 cycles, 103.227 ms; elapsed 81,903,050 cycles, 1638.061 ms; longest step 131,929 cycles, 2.639 ms.

Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).

| Phase | Steps | Longest step, CPU cycles | Longest, ms | Within T_svc | Total, CPU cycles |
|---|---:|---:|---:|---|---:|
| capture | 165 | 131,929 | 2.639 | yes | 5,161,328 |
| erase | 1 | 12,595 | 0.252 | yes | 12,595 |
| idle | 215 | 10,358 | 0.207 | yes | 2,110,050 |
| poll | 53 | 12,321 | 0.246 | yes | 639,043 |
| program | 52 | 101,577 | 2.032 | yes | 5,249,584 |
| read | 104 | 95,984 | 1.920 | yes | 9,734,962 |
| seal | 52 | 34,839 | 0.697 | yes | 1,792,186 |

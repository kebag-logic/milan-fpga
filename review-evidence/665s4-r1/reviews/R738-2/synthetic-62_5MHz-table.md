# Saved-state cases on the split CPU, 1x1

Clocks, as this run's builds recorded them: CPU 62.5 MHz (62,500,000 Hz), bus 125 MHz (125,000,000 Hz).

| Case | Verdict | Detail |
|---|---|---|
| commit | pass |  |
| step-over-t-svc | caught | every phase's longest step at T_svc (625,000 cycles) passes and one cycle past it is caught: capture, erase, idle, poll, program, read, seal |

Every service step is graded against T_svc = 10.0 ms of CPU time.

Clocks, as this run's builds recorded them: CPU 62.5 MHz (62,500,000 Hz), bus 125 MHz (125,000,000 Hz).

| Case | Service steps | Longest step, CPU cycles | Longest, ms |
|---|---:|---:|---:|
| commit | 11 | 40,000 | 0.640 |

Capture, measured (no bound of its own): 4 records in 5 steps; CPU time 161,000 cycles, 2.576 ms; elapsed 201,000 cycles, 3.216 ms; longest step 40,000 cycles, 0.640 ms.

Clocks, as this run's builds recorded them: CPU 62.5 MHz (62,500,000 Hz), bus 125 MHz (125,000,000 Hz).

| Phase | Steps | Longest step, CPU cycles | Longest, ms | Within T_svc | Total, CPU cycles |
|---|---:|---:|---:|---|---:|
| capture | 5 | 40,000 | 0.640 | yes | 161,000 |
| erase | 1 | 300 | 0.005 | yes | 300 |
| idle | 1 | 50 | 0.001 | yes | 50 |
| poll | 1 | 300 | 0.005 | yes | 300 |
| program | 1 | 300 | 0.005 | yes | 300 |
| read | 1 | 300 | 0.005 | yes | 300 |
| seal | 2 | 300 | 0.005 | yes | 600 |

# Saved-state cases on the split CPU, 1x1

| Case | Verdict | Detail |
|---|---|---|
| commit | pass |  |
| step-over-t-svc | caught | every phase's longest step at T_svc (500,000 cycles) passes and one cycle past it is caught: capture, erase, idle, poll, program, read, seal |
| valid | pass | 44 apply entries, boot 5,027,209 CPU cycles |
| absent | pass | 0 apply entries, boot 506,631 CPU cycles |
| torn | pass | 44 apply entries, boot 8,255,898 CPU cycles |
| version | pass | 0 apply entries, boot 504,698 CPU cycles |
| guard | pass |  |
| reorder-settle | caught | apply order: entry 4 is aecp_value_restore, the container needs aecp_restore_settle (44 entries, 44 wanted) |
| reorder-bindings | caught | apply order: entry 0 is aecp_map_restore, the container needs acmp_restore_binding (44 entries, 44 wanted) |
| guard-removed | caught | flash write escaped the journal |
| slow-step | caught | step 0 (idle) takes 30.2216 ms of CPU time, over T_svc 10.0 ms |

Every service step is graded against T_svc = 10.0 ms of CPU time.

| Case | Service steps | Longest step, CPU cycles | Longest, ms |
|---|---:|---:|---:|
| commit | 330 | 101,098 | 2.022 |
| valid | 41 | 9,414 | 0.188 |
| absent | 41 | 9,393 | 0.188 |
| torn | 41 | 9,408 | 0.188 |
| version | 41 | 9,381 | 0.188 |
| guard | 41 | 9,416 | 0.188 |

Capture, measured (no bound of its own): 54 records in 55 steps; CPU time 1,361,143 cycles, 27.223 ms; elapsed 26,745,259 cycles, 534.905 ms; longest step 40,771 cycles, 0.815 ms.

| Phase | Steps | Longest step, CPU cycles | Longest, ms | Within T_svc | Total, CPU cycles |
|---|---:|---:|---:|---|---:|
| capture | 55 | 40,771 | 0.815 | yes | 1,361,143 |
| erase | 1 | 12,416 | 0.248 | yes | 12,416 |
| idle | 203 | 10,022 | 0.200 | yes | 1,926,033 |
| poll | 15 | 11,851 | 0.237 | yes | 173,068 |
| program | 14 | 101,098 | 2.022 | yes | 1,325,294 |
| read | 28 | 95,354 | 1.907 | yes | 2,460,166 |
| seal | 14 | 34,384 | 0.688 | yes | 456,088 |

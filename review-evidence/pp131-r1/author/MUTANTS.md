# Mutation campaign at `e1ae468`

Driver: `d3_mutants.py` (this packet), run as `python3 d3_mutants.py --tree <processor checkout> --scratch <scratch dir> --jobs 3 --summary <file>`. Each mutant is planted in a fresh scratch copy of the tree, built and run; KILLED requires a successful build, a completed simulation with its tally, a failing exit and every named check failing. Goldens are the unmutated suites. Logs stay in scratch.

| Mutant | Verdict | Build rc | Run rc | Named checks that failed (first 2) |
|---|---|---:|---:|---|
| `golden-acmp_nvm` | PASS | 0 | 0 |  |
| `golden-pp_top` | PASS | 0 | 0 |  |
| `TRG_cfg` | KILLED | 0 | 1 | D3S1 cfg: record 0x00 written once, byte-exact (0 writes); D3R1: COMPLETE 1836 cycles after the release, applied 8 refused 0 blan |
| `hold_released_at_go` | KILLED | 0 | 1 | D3O1: released at 122, terminal at 880, own fell at 123, the held comm; D3O2: CLOSED at 164 after the release at 122, cause 7, own 0, 1 descri |
| `dispatch_not_held` | KILLED | 0 | 1 | D3O1: without the walk the writer owns every cycle (2000 of 2000), the; D3O1: released at 122, terminal at 880, own fell at 880, the held comm |
| `TRG_rate` | KILLED | 0 | 1 | D3S1 rate: record 0x02 written once, byte-exact (0 writes); D3R1: COMPLETE 1638 cycles after the release, applied 8 refused 0 blan |
| `TRG_clks` | KILLED | 0 | 1 | D3S1 clks: record 0x0a written once, byte-exact (0 writes); D3S6 index: the clock source changed during 0x50's WRITE is written af |
| `TRG_fmti` | KILLED | 0 | 1 | D3S1 fmti: record 0x30 written once, byte-exact (0 writes); D3S1 fmti: record 0x31 written once, byte-exact (0 writes) |
| `TRG_fmto` | KILLED | 0 | 1 | D3S1 fmto: record 0x40 written once, byte-exact (0 writes); D3S1 fmto: record 0x41 written once, byte-exact (0 writes) |
| `taint_ignored` | KILLED | 0 | 1 | D3S4 taint: 1 WRITEs of 0x50, the first carrying the latched value, th |
| `TRG_ptof` | KILLED | 0 | 1 | D3S1 ptof: record 0x50 written once, byte-exact (0 writes); D3S1 ptof: record 0x51 written once, byte-exact (0 writes) |
| `clear_wins_same_edge` | KILLED | 0 | 1 | D3S5 same edge: the change on the done edge is written (1 WRITEs) |
| `clear_by_index` | KILLED | 0 | 1 | D3S1 rate: record 0x02 written once, byte-exact (0 writes); D3S1 clks: record 0x0a written once, byte-exact (0 writes) |
| `clear_by_group` | KILLED | 0 | 1 | D3S1 fmti: record 0x31 written once, byte-exact (0 writes); D3S1 fmto: record 0x41 written once, byte-exact (0 writes) |
| `identify_is_a_change` | KILLED | 0 | 1 | D3S7: IDENTIFY set, 49787 pending cycles, 2 NVM operations |
| `unchanged_compare_ignores_validity` | KILLED | 0 | 1 | D3S8 validity: clock source 0 on the unset row is written (0) |
| `latch_ignores_program` | KILLED | 0 | 1 | D3S5 same edge: the change on the done edge is written (6 WRITEs); D3S11: the writer owned 3 cycles waiting for the running command, then |
| `fourth_attempt` | KILLED | 0 | 1 | D3S10 count: 4 failed attempts of 0x50 (4 grants), alarm 1, unflushed ; D3S10 timing: each retry granted RETRY_BACKOFF_CYC_P cycles or more af |
| `alarm_forgiven_by_success` | KILLED | 0 | 1 | D3S10 revocation: a later successful write leaves the alarm set |
| `image_unproven_continues` | KILLED | 0 | 1 | D3O2: CLOSED at -1 after the release at 122, cause 0, own 0, 2 descrip; D3O2: CLOSED holds AECP (185 busy cycles, the command still queued) an |
| `RPL_cfg` | KILLED | 0 | 1 | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blan; D3R1 cfg: configuration 1 restored with its valid flag, GET reads it |
| `RPL_rate` | KILLED | 0 | 1 | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blan; D3R1 rate: 48000 restored with its valid flag, GET reads it |
| `RPL_clks` | KILLED | 0 | 1 | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blan; D3R1 clks: clock source 2 restored with its valid flag, GET reads it |
| `RPL_fmti` | KILLED | 0 | 1 | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blan; D3R1 fmti: both input formats restored with their valid flags, GET rea |
| `RPL_fmto` | KILLED | 0 | 1 | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blan; D3R1 fmto: both output formats restored with their valid flags, GET re |
| `RPL_ptof` | KILLED | 0 | 1 | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blan; D3R1 ptof: both presentation offsets restored with their valid flags,  |
| `rule_ignored` | KILLED | 0 | 1 | D3R2: COMPLETE, applied 7 refused 4 blank 16 of 27; D3R2: only the neighbour's offset restored (valid 0x03) |
| `passes_may_disagree` | KILLED | 0 | 1 | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause  |
| `device_error_reads_as_blank` | KILLED | 0 | 1 | D3R5 device error on the header: DEFAULTS, cause 5, applied 1, rows at; D3R6: the one saved record lost to a device error is a failure (cause  |
| `unframed_reads_as_device_error` | KILLED | 0 | 1 | D3O1: a validated image is proven without a LOCATE (0 requests from th; D3O4: an image loaded late is walked at the writer's LOCATE (4 request |
| `desc_error_is_a_refusal` | KILLED | 0 | 1 | D3R7: the rule's descriptor fetch errs: cause 0, refused 1, rolled bac; D3R10 5000: done 5430 closed -1 cause 0 rolled back 0; the stores in r |
| `no_restore_watchdog` | KILLED | 0 | 1 | D3R5 the header never answered: DEFAULTS, cause 0, applied 0, rows at ; D3R8: a READ granted 20200 cycles late: fail 0, cause 0 |
| `restore_writes_are_changes` | KILLED | 0 | 1 | D3R1: no restore write is a change (50163 pending cycles, 12 device wr |
| `enable_not_released_by_restore` | KILLED | 0 | 1 | D3R1: the enable requested from reset reaches ADP only at the combined; D3R12: the re-walk cannot prove the image: CLOSED 9425, cause 2, the e |
| `done_without_d3` | KILLED | 0 | 1 | D3R1: COMPLETE 0 cycles after the release, applied 9 refused 0 blank 1; D3R1: the enable requested from reset reaches ADP only at the combined |
| `blank_ignores_d3` | KILLED | 0 | 1 | D3R1: COMPLETE 1867 cycles after the release, applied 9 refused 0 blan |
| `own_taken_at_the_walk` | KILLED | 0 | 1 | D3O1: without the walk the writer owns every cycle (0 of 2000), the en; D3O1: released at 122, terminal at 880, own fell at 0, the held comman |
| `no_rollback` | KILLED | 0 | 1 | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause ; D3R7: the rule's descriptor fetch errs: cause 6, refused 0, rolled bac |
| `dyn_not_rolled_back` | KILLED | 0 | 1 | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause  |
| `store_not_rolled_back` | KILLED | 0 | 1 | D3R10 5000: done -1 closed 6003 cause 6 rolled back 0; the stores in r; D3R10 16000: done -1 closed 17003 cause 6 rolled back 0; the stores in |
| `rollback_ignores_debt` | KILLED | 0 | 1 | D3R10 5000: done 6537 closed -1 cause 6 rolled back 1; the stores in r; D3R10 16000: done -1 closed 13277 cause 6 rolled back 0; the stores in |
| `no_backoff_binding` | KILLED | 0 | 2 | E9 DR2c timing: each retry starts RETRY_BACKOFF_CYC_P cycles or more a |
| `closed_releases_the_entity` | KILLED | 0 | 1 | D3R12: the re-walk cannot prove the image: CLOSED -1, cause 2, the ent |
| `fourth_attempt_binding` | KILLED | 0 | 2 | E8 DR2c count: three attempts in all (4 started, 4 failed); E9 DR2c timing: each retry starts RETRY_BACKOFF_CYC_P cycles or more a |
| `no_backoff_d3` | KILLED | 0 | 1 | D3S10 timing: each retry granted RETRY_BACKOFF_CYC_P cycles or more af |
| `alarm_forgiven_binding` | KILLED | 0 | 2 | E11 DR2c revocation: a later successful commit and time leave the alar |
| `store_not_cleared` | KILLED | 0 | 1 | D3R1: every row at its reset value, valid clear, when the D3 walk star; D3R2: only the neighbour's offset restored (valid 0x02) |
| `valid_not_cleared` | KILLED | 0 | 1 | D3R1: every row at its reset value, valid clear, when the D3 walk star; D3R2: only the neighbour's offset restored (valid 0x02) |
| `quarantine_released_by_time` | KILLED | 0 | 1 | D3R5: once the device ends the drained read a later SET persists |

Totals: 47 killed of 47 mutants; 2 goldens PASS; 0 survived, 0 refused.

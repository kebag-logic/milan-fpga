# D3 negative controls at the round-2 head

Driver: `tb/pp_top/d3_mutants.py` from the committed tree at `2b38d68e704e8a62fbeae8171c9195ca93728488`, run by the gate runner in a clean clone (`python3 tb/pp_top/d3_mutants.py --output <dir> --jobs 6`, Verilator 5.050): rc 0, 451.6 s.
results.json SHA-256 `84cdd3a21127b1956ea8f5a4624c55734925c7046bd6691b30d735393eddb3b7` (45080 bytes, kept in scratch).

Goldens: `golden-acmp_nvm` PASS, `golden-pp_top` PASS, `golden-rx_validator` PASS.
Mutants: 62 of 62 KILLED; none survived, none refused.

| Mutant | Suite | Verdict | Named checks (every one failed) | Failing checks | First failing check |
|---|---|---|---|---:|---|
| `TRG_cfg` | `tb/pp_top` | KILLED | `D3S1 cfg` | 3 | D3S1 cfg: record 0x00 written once, byte-exact (0 writes) |
| `TRG_clks` | `tb/pp_top` | KILLED | `D3S1 clks` | 5 | D3S1 clks: record 0x0a written once, byte-exact (0 writes) |
| `TRG_fmti` | `tb/pp_top` | KILLED | `D3S1 fmti` | 4 | D3S1 fmti: record 0x30 written once, byte-exact (0 writes) |
| `TRG_fmto` | `tb/pp_top` | KILLED | `D3S1 fmto` | 4 | D3S1 fmto: record 0x40 written once, byte-exact (0 writes) |
| `TRG_ptof` | `tb/pp_top` | KILLED | `D3S1 ptof` | 21 | D3S1 ptof: record 0x50 written once, byte-exact (0 writes) |
| `TRG_rate` | `tb/pp_top` | KILLED | `D3S1 rate` | 3 | D3S1 rate: record 0x02 written once, byte-exact (0 writes) |
| `RPL_cfg` | `tb/pp_top` | KILLED | `D3R1 cfg` | 5 | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blank 18 of 27 |
| `RPL_clks` | `tb/pp_top` | KILLED | `D3R1 clks` | 3 | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blank 18 of 27 |
| `RPL_fmti` | `tb/pp_top` | KILLED | `D3R1 fmti` | 2 | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blank 18 of 27 |
| `RPL_fmto` | `tb/pp_top` | KILLED | `D3R1 fmto` | 2 | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blank 18 of 27 |
| `RPL_ptof` | `tb/pp_top` | KILLED | `D3R1 ptof` | 6 | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blank 18 of 27 |
| `RPL_rate` | `tb/pp_top` | KILLED | `D3R1 rate` | 5 | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blank 18 of 27 |
| `hold_released_at_go` | `tb/pp_top` | KILLED | `D3O1: released at` | 10 | D3O1: released at 122, terminal at 880, own fell at 123, the held command taken at 124, 0 busy cycles while ow |
| `dispatch_not_held` | `tb/pp_top` | KILLED | `D3O1: without the walk the writer owns every cycle` | 4 | D3O1: without the walk the writer owns every cycle (2000 of 2000), the engine runs nothing (1998 busy) and the |
| `own_taken_at_the_walk` | `tb/pp_top` | KILLED | `D3R9: the held SET` | 10 | D3O1: without the walk the writer owns every cycle (0 of 2000), the engine runs nothing (1998 busy) and the co |
| `image_unproven_continues` | `tb/pp_top` | KILLED | `D3O2: CLOSED at`, `D3O3: CLOSED` | 6 | D3O2: CLOSED at -1 after the release at 122, cause 0, own 0, 2 descriptor requests |
| `latch_ignores_program` | `tb/pp_top` | KILLED | `D3S9` | 3 | D3S5 same edge: the change on the done edge is written (6 WRITEs) |
| `taint_ignored` | `tb/pp_top` | KILLED | `D3S4 taint` | 1 | D3S4 taint: 1 WRITEs of 0x50, the first carrying the latched value, the last the change made during it |
| `clear_wins_same_edge` | `tb/pp_top` | KILLED | `D3S5 same edge` | 1 | D3S5 same edge: the change on the done edge is written (1 WRITEs) |
| `clear_by_group` | `tb/pp_top` | KILLED | `D3S6 group` | 8 | D3S1 fmti: record 0x31 written once, byte-exact (0 writes) |
| `clear_by_index` | `tb/pp_top` | KILLED | `D3S6 index` | 14 | D3S1 rate: record 0x02 written once, byte-exact (0 writes) |
| `identify_is_a_change` | `tb/pp_top` | KILLED | `D3S7` | 1 | D3S7: IDENTIFY set, 49787 pending cycles, 2 NVM operations |
| `unchanged_compare_ignores_validity` | `tb/pp_top` | KILLED | `D3S8 validity` | 1 | D3S8 validity: clock source 0 on the unset row is written (0) |
| `rule_ignored` | `tb/pp_top` | KILLED | `D3R2: COMPLETE` | 3 | D3R2: COMPLETE, applied 7 refused 4 blank 16 of 27 |
| `passes_may_disagree` | `tb/pp_top` | KILLED | `D3R4:`, `D3R4b` | 3 | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause 0, rolled back 0: every row at its defau |
| `device_error_reads_as_blank` | `tb/pp_top` | KILLED | `D3R5 device error on the header`, `D3R6: the one saved record` | 4 | D3R5 device error on the header: DEFAULTS, cause 5, applied 1, rows at their defaults |
| `unframed_reads_as_device_error` | `tb/pp_top` | KILLED | `D3R6: an erased device restores blank` | 37 | D3O1: a validated image is proven without a LOCATE (0 requests from the release to the terminal), COMPLETE |
| `desc_error_is_a_refusal` | `tb/pp_top` | KILLED | `D3R7` | 4 | D3R7: the rule's descriptor fetch errs: cause 0, refused 1, rolled back 0 |
| `no_restore_watchdog` | `tb/pp_top` | KILLED | `D3R8: a READ granted`, `D3R8b` | 7 | D3R5 the header never answered: DEFAULTS, cause 0, applied 0, rows at their defaults |
| `restore_writes_are_changes` | `tb/pp_top` | KILLED | `D3R1: no restore write is a change` | 1 | D3R1: no restore write is a change (50163 pending cycles, 12 device writes) |
| `enable_not_released_by_restore` | `tb/pp_top` | KILLED | `D3R1: the enable requested from reset` | 2 | D3R1: the enable requested from reset reaches ADP only at the combined terminal (1989 early enable cycles, 0 e |
| `done_without_d3` | `tb/pp_top` | KILLED | `D3R1: the enable requested from reset`, `D3R1: COMPLETE` | 31 | D3R1: COMPLETE 0 cycles after the release, applied 9 refused 0 blank 18 of 27 |
| `blank_ignores_d3` | `tb/pp_top` | KILLED | `D3R1: COMPLETE` | 1 | D3R1: COMPLETE 1867 cycles after the release, applied 9 refused 0 blank 18 of 27 |
| `store_not_cleared` | `tb/pp_top` | KILLED | `D3R1: every row at its reset value` | 15 | D3R1: every row at its reset value, valid clear, when the D3 walk starts |
| `valid_not_cleared` | `tb/pp_top` | KILLED | `D3R1: every row at its reset value` | 15 | D3R1: every row at its reset value, valid clear, when the D3 walk starts |
| `quarantine_released_by_time` | `tb/pp_top` | KILLED | `D3R5: once the device ends the drained read a later SET persists` | 3 | D3R5: once the device ends the drained read a later SET persists |
| `no_rollback` | `tb/pp_top` | KILLED | `D3R4:` | 12 | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause 5, rolled back 0: every row at its defau |
| `dyn_not_rolled_back` | `tb/pp_top` | KILLED | `D3R4:` | 4 | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause 5, rolled back 1: every row at its defau |
| `store_not_rolled_back` | `tb/pp_top` | KILLED | `D3R10 5000` | 2 | D3R10 5000: done -1 closed 6003 cause 6 rolled back 0; the stores in reset from 5077 to 5999, the debt owed 92 |
| `rollback_ignores_debt` | `tb/pp_top` | KILLED | `D3R10 16000` | 2 | D3R10 5000: done 6537 closed -1 cause 6 rolled back 1; the stores in reset from 5077 to 5079, the debt owed 2  |
| `closed_releases_the_entity` | `tb/pp_top` | KILLED | `D3R12` | 1 | D3R12: the re-walk cannot prove the image: CLOSED -1, cause 2, the entity held |
| `no_backoff_d3` | `tb/pp_top` | KILLED | `D3S10 timing` | 2 | D3S10 timing: each retry granted after the derived 500001-cycle backoff and one relatch (15, 15) |
| `fourth_attempt` | `tb/pp_top` | KILLED | `D3S10 count` | 2 | D3S10 count: 4 failed attempts of 0x50 (4 grants), alarm 1, unflushed 0 |
| `alarm_forgiven_by_success` | `tb/pp_top` | KILLED | `D3S10 revocation` | 1 | D3S10 revocation: a later successful write leaves the alarm set |
| `no_backoff_binding` | `tb/acmp_nvm` | KILLED | `E9 DR2c timing` | 1 | E9 DR2c timing: each retry starts RETRY_BACKOFF_CYC_P cycles or more after the failed attempt's error (43, 43) |
| `fourth_attempt_binding` | `tb/acmp_nvm` | KILLED | `E8 DR2c count` | 3 | E8 DR2c count: three attempts in all (4 started, 4 failed) |
| `alarm_forgiven_binding` | `tb/acmp_nvm` | KILLED | `E11 DR2c revocation` | 1 | E11 DR2c revocation: a later successful commit and time leave the alarm set |
| `backoff_derivation` | `tb/pp_top` | KILLED | `D3S10 timing` | 2 | D3S10 timing: each retry granted after the derived 500001-cycle backoff and one relatch (5014, 5014) |
| `backoff_holds_dispatch` | `tb/pp_top` | KILLED | `D3S10 backoff` | 1 | D3S10 backoff: 999936 owned cycles inside the backoffs; a READ_DESCRIPTOR sent into the first is answered 5013 |
| `disagree_one_direction` | `tb/pp_top` | KILLED | `D3R4b` | 1 | D3R4b: a record blank in pass 0 and whole in pass 1 aborts, cause 0, rolled back 0, the offset not applied (va |
| `rollback_one_cycle` | `tb/pp_top` | KILLED | `D3R4 strobe` | 1 | D3R4 strobe: with no debt owed the roll-back holds both stores in reset 1 cycles, at least two |
| `pass1_read_not_drained` | `tb/pp_top` | KILLED | `D3R5b: once the device ends the drained pass-1 READ` | 1 | D3R5b: once the device ends the drained pass-1 READ a later SET persists (0 WRITEs, unflushed 1) |
| `judge_wait_unwatched` | `tb/pp_top` | KILLED | `D3R8b` | 1 | D3R8b: a silent judge ends DEFAULTS at -1, the release at 122, cause 0, rolled back 0 |
| `rate_walk_stuck_on_first_lane` | `tb/pp_top` | KILLED | `D3R3b entry 7` | 1 | D3R3b entry 7 of 10 (24000 Hz): applied 0 refused 1, rate 0 valid 0 |
| `rate_walk_unbounded` | `tb/pp_top` | KILLED | `D3R3b entry 8` | 1 | D3R3b entry 8 of 10 (16000 Hz): applied 1 refused 0, rate 16000 valid 1 |
| `no_aggregate_deadline` | `tb/pp_top` | KILLED | `D3R13 pass 0: DEFAULTS at clock`, `D3R13 pass 1` | 3 | D3R13 pass 0: DEFAULTS at clock 0 of the aggregate 1000001, cause 0, rolled back 0, applied 0, the longest wai |
| `aggregate_mirrored` | `tb/pp_top` | KILLED | `D3R13 pass 0: DEFAULTS at clock` | 3 | D3R13 pass 0: DEFAULTS at clock 0 of the aggregate 1000001, cause 0, rolled back 0, applied 0, the longest wai |
| `aggregate_from_the_walk` | `tb/pp_top` | KILLED | `D3R13 pass 0: DEFAULTS at clock` | 3 | D3R13 pass 0: DEFAULTS at clock 0 of the aggregate 1000001, cause 0, rolled back 0, applied 0, the longest wai |
| `per_wait_floor` | `tb/pp_top` | KILLED | `D3R8 deadline` | 1 | D3R8 deadline: the walk aborted on the 20000-th stalled cycle, the derived deadline is 20001 |
| `aecp_hold_unbounded` | `tb/pp_top` | KILLED | `D3O5: in CLOSED each GET_RX_STATE`, `D3O6: during the slowed walk` | 6 | D3O5: in CLOSED each GET_RX_STATE after each of 6 AECP commands is answered in 168 cycles, the idle latency (w |
| `held_drop_uncounted` | `tb/pp_top` | KILLED | `D3O5: one AECP command held`, `D3O6: at the terminal` | 4 | D3O5: one AECP command held, 0 dropped at the slot gate and counted, 0 answered |
| `validator_admits_held_aecp` | `tb/rx_validator` | KILLED | `F28 held AECP`, `F28 rx_aecp_held counts both` | 4 | F28 held AECP: slot taken and returned, no commit, no header beat, no other counter (allocs 1 aborts 0 commits |

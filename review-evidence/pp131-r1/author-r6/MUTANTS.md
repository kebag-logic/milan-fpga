# D3 mutation campaign at the head

`python3 tb/pp_top/d3_mutants.py` from a clean clone: 83 of 83 KILLED; goldens golden-acmp_nvm PASS, golden-pp_top PASS, golden-rx_validator PASS. KILLED means the build succeeded, the run completed with its tally, exited non-zero, and every named check failed. The count column is the number of failing checks; the README column says whether it equals the suite README's mutation record.

| Mutant | Suite | Verdict | Named checks (each failing) | Failing checks | = README | First failing message |
|---|---|---|---|---:|---|---|
| `RPL_cfg` | `tb/pp_top` | KILLED | `D3R1 cfg` | 6 | yes | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blank 18 of 27 |
| `RPL_clks` | `tb/pp_top` | KILLED | `D3R1 clks` | 3 | yes | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blank 18 of 27 |
| `RPL_fmti` | `tb/pp_top` | KILLED | `D3R1 fmti` | 2 | yes | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blank 18 of 27 |
| `RPL_fmto` | `tb/pp_top` | KILLED | `D3R1 fmto` | 2 | yes | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blank 18 of 27 |
| `RPL_ptof` | `tb/pp_top` | KILLED | `D3R1 ptof` | 6 | yes | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blank 18 of 27 |
| `RPL_rate` | `tb/pp_top` | KILLED | `D3R1 rate` | 6 | yes | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blank 18 of 27 |
| `TRG_cfg` | `tb/pp_top` | KILLED | `D3S1 cfg` | 3 | yes | D3S1 cfg: record 0x00 written once, byte-exact (0 writes) |
| `TRG_clks` | `tb/pp_top` | KILLED | `D3S1 clks` | 5 | yes | D3S1 clks: record 0x0a written once, byte-exact (0 writes) |
| `TRG_fmti` | `tb/pp_top` | KILLED | `D3S1 fmti` | 4 | yes | D3S1 fmti: record 0x30 written once, byte-exact (0 writes) |
| `TRG_fmto` | `tb/pp_top` | KILLED | `D3S1 fmto` | 4 | yes | D3S1 fmto: record 0x40 written once, byte-exact (0 writes) |
| `TRG_ptof` | `tb/pp_top` | KILLED | `D3S1 ptof` | 24 | yes | D3S1 ptof: record 0x50 written once, byte-exact (0 writes) |
| `TRG_rate` | `tb/pp_top` | KILLED | `D3S1 rate` | 3 | yes | D3S1 rate: record 0x02 written once, byte-exact (0 writes) |
| `aecp_hold_unbounded` | `tb/pp_top` | KILLED | `D3O5: in CLOSED each GET_RX_STATE`, `D3O6: during the slowed walk` | 7 | yes | D3O5: in CLOSED each GET_RX_STATE after each of 6 AECP commands is answered in 168 cycles, the idle latency (w |
| `agg_closes_before_proof` | `tb/pp_top` | KILLED | `D3R14 image valid: DEFAULTS` | 11 | yes | D3R14 image valid: DEFAULTS by clock 0, the D3 walk's longest wait 0 (no record READ requested), cause 3, roll |
| `agg_closes_during_proof` | `tb/pp_top` | KILLED | `D3R19 inside the LOCATE: DEFAULTS` | 2 | yes | D3R19 inside the LOCATE: the binding walk completes (0x27 done on its placed clock 1, longest wait 11328 of 20 |
| `agg_fires_with_event_in_hand` | `tb/pp_top` | KILLED | `D3R17: the writer's grant`, `D3R17: once the device ends` | 2 | yes | D3R17: the writer's grant lands on the bound's own clock (1, 0x56's READ steered 1, latency 9); DEFAULTS 1 clo |
| `agg_not_in_rollback` | `tb/pp_top` | KILLED | `D3R15 debt wait: CLOSED`, `D3R15 re-LOCATE: CLOSED` | 4 | yes | D3R15 debt wait: the pass-1 fault's READ (region 0x02 offset 8) granted on its steered cycle 1; at the bound t |
| `agg_not_stopped_at_terminal` | `tb/pp_top` | KILLED | `D3R16 COMPLETE`, `D3R16 DEFAULTS`, `D3R16 CLOSED` | 3 | yes | D3R16 COMPLETE: two per-wait deadlines past the bound the verdicts hold (done 1 fail 1 rolled back 0 closed 1  |
| `agg_o_pulse` | `tb/pp_top` | KILLED | `D3R21: the binding walk fails whole` | 3 | yes | D3R18: binding READ strobe 4 on agg_o's first clock 12398091 (strobe 0, abort 0, arbiter owner 0), the done be |
| `aggregate_from_the_walk` | `tb/pp_top` | KILLED | `D3R13 pass 0: DEFAULTS at clock` | 21 | yes | D3R13 pass 0: DEFAULTS at clock 0 of the aggregate 1000001, cause 0, rolled back 0, applied 0, the longest wai |
| `aggregate_mirrored` | `tb/pp_top` | KILLED | `D3R13 pass 0: DEFAULTS at clock` | 19 | yes | D3R13 pass 0: DEFAULTS at clock 0 of the aggregate 1000001, cause 0, rolled back 0, applied 0, the longest wai |
| `alarm_forgiven_binding` | `tb/acmp_nvm` | KILLED | `E11 DR2c revocation` | 1 | yes | E11 DR2c revocation: a later successful commit and time leave the alarm set |
| `alarm_forgiven_by_success` | `tb/pp_top` | KILLED | `D3S10 revocation` | 1 | yes | D3S10 revocation: a later successful write leaves the alarm set |
| `backoff_derivation` | `tb/pp_top` | KILLED | `D3S10 timing` | 2 | yes | D3S10 timing: each retry granted after the derived 500001-cycle backoff and one relatch (5014, 5014) |
| `backoff_holds_dispatch` | `tb/pp_top` | KILLED | `D3S10 backoff` | 1 | yes | D3S10 backoff: 999936 owned cycles inside the backoffs; a READ_DESCRIPTOR sent into the first is answered 5013 |
| `binding_walk_ignores_aggregate` | `tb/pp_top` | KILLED | `D3R14 image valid: the binding walk`, `D3R14 image refused: the binding walk` | 10 | yes | D3R14 image valid: the binding walk (longest wait 19002 of 20001) fails whole at the bound's clock 1000001 (ca |
| `blank_ignores_d3` | `tb/pp_top` | KILLED | `D3R1: COMPLETE` | 1 | yes | D3R1: COMPLETE 1867 cycles after the release, applied 9 refused 0 blank 18 of 27 |
| `clear_by_group` | `tb/pp_top` | KILLED | `D3S6 group` | 8 | yes | D3S1 fmti: record 0x31 written once, byte-exact (0 writes) |
| `clear_by_index` | `tb/pp_top` | KILLED | `D3S6 index` | 14 | yes | D3S1 rate: record 0x02 written once, byte-exact (0 writes) |
| `clear_wins_same_edge` | `tb/pp_top` | KILLED | `D3S5 same edge` | 1 | yes | D3S5 same edge: the change on the done edge is written (1 WRITEs) |
| `closed_releases_the_entity` | `tb/pp_top` | KILLED | `D3R12` | 2 | yes | D3R12: the re-walk cannot prove the image: CLOSED -1, cause 2, the entity held |
| `cross_own_m1_drains_m0` | `tb/acmp_nvm` | KILLED | `N11d manager 1's abort held while manager 0 owns each of the walk's READs` | 1 | yes | N11d manager 1's abort held while manager 0 owns each of the walk's READs: present in 45 of the 45 cycles mana |
| `desc_error_is_a_refusal` | `tb/pp_top` | KILLED | `D3R7` | 6 | yes | D3R7: the rule's descriptor fetch errs: cause 0, refused 1, rolled back 0 |
| `device_error_reads_as_blank` | `tb/pp_top` | KILLED | `D3R5 device error on the header`, `D3R6: the one saved record` | 5 | yes | D3R5 device error on the header: DEFAULTS, cause 5, applied 1, rows at their defaults |
| `disagree_one_direction` | `tb/pp_top` | KILLED | `D3R4b` | 1 | yes | D3R4b: a record blank in pass 0 and whole in pass 1 aborts, cause 0, rolled back 0, the offset not applied (va |
| `dispatch_not_held` | `tb/pp_top` | KILLED | `D3O1: without the walk the writer owns every cycle` | 5 | yes | D3O1: without the walk the writer owns every cycle (2000 of 2000), the engine runs nothing (1998 busy) and the |
| `done_without_d3` | `tb/pp_top` | KILLED | `D3R1: the enable requested from reset`, `D3R1: COMPLETE` | 42 | yes | D3R1: COMPLETE 0 cycles after the release, applied 9 refused 0 blank 18 of 27 |
| `drain_misses_issue_cycle_m1` | `tb/acmp_nvm` | KILLED | `N10 a manager-1 READ abandoned in its issue cycle` | 4 | yes | N10 a manager-1 READ abandoned in its issue cycle: the drain armed in the issue cycle (issued at 422951, drain |
| `drain_misses_issue_cycle` | `tb/pp_top` | KILLED | `D3R18: the READ abandoned in its issue cycle`, `D3R18: once the device ends` | 2 | yes | D3R18: the READ abandoned in its issue cycle is drained from the next clock (0, owner 1), the binding walk fai |
| `dyn_not_rolled_back` | `tb/pp_top` | KILLED | `D3R4:` | 4 | yes | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause 5, rolled back 1: every row at its defau |
| `enable_not_released_by_restore` | `tb/pp_top` | KILLED | `D3R1: the enable requested from reset` | 4 | yes | D3R1: the enable requested from reset reaches ADP only at the combined terminal (1989 early enable cycles, 0 e |
| `fourth_attempt_binding` | `tb/acmp_nvm` | KILLED | `E8 DR2c count` | 3 | yes | E8 DR2c count: three attempts in all (4 started, 4 failed) |
| `fourth_attempt` | `tb/pp_top` | KILLED | `D3S10 count` | 2 | yes | D3S10 count: 4 failed attempts of 0x50 (4 grants), alarm 1, unflushed 0 |
| `held_drop_uncounted` | `tb/pp_top` | KILLED | `D3O5: one AECP command held`, `D3O6: at the terminal` | 5 | yes | D3O5: one AECP command held, 0 dropped at the slot gate and counted, 0 answered |
| `hold_released_at_go` | `tb/pp_top` | KILLED | `D3O1: released at` | 16 | yes | D3O1: released at 122, terminal at 880, own fell at 123, the held command taken at 124, 0 busy cycles while ow |
| `identify_is_a_change` | `tb/pp_top` | KILLED | `D3S7` | 1 | yes | D3S7: IDENTIFY set, 49787 pending cycles, 2 NVM operations |
| `image_unproven_continues` | `tb/pp_top` | KILLED | `D3O2: CLOSED at`, `D3O3: CLOSED` | 9 | yes | D3O2: CLOSED at -1 after the release at 122, cause 0, own 0, 2 descriptor requests |
| `issue_arm_cross_intent` | `tb/acmp_nvm` | KILLED | `N11b manager 1's abort in the issue cycle of each of the walk's READs` | 1 | yes | N11b manager 1's abort in the issue cycle of each of the walk's READs: 1 of the walk's 1 READs issued with it, |
| `issue_arm_ignores_we` | `tb/acmp_nvm` | KILLED | `N11a a manager-1 WRITE presented with its abort` | 1 | yes | N11a a manager-1 WRITE presented with its abort: issued as a commit (1), never drained (from 423535), every by |
| `issue_arm_stale_we` | `tb/acmp_nvm` | KILLED | `N11a a manager-1 WRITE presented with its abort`, `N11c a manager-1 READ abandoned in its issue cycle after a WRITE` | 3 | yes | N11a a manager-1 WRITE presented with its abort: issued as a commit (1), never drained (from 423535), every by |
| `issue_arm_write_too` | `tb/acmp_nvm` | KILLED | `N11a a manager-1 WRITE presented with its abort` | 1 | yes | N11a a manager-1 WRITE presented with its abort: issued as a commit (1), never drained (from 423535), every by |
| `judge_wait_unwatched` | `tb/pp_top` | KILLED | `D3R8b` | 1 | yes | D3R8b: a silent judge ends DEFAULTS at -1, the release at 122, cause 0, rolled back 0 |
| `latch_ignores_program` | `tb/pp_top` | KILLED | `D3S9` | 3 | yes | D3S5 same edge: the change on the done edge is written (6 WRITEs) |
| `no_aggregate_deadline` | `tb/pp_top` | KILLED | `D3R13 pass 0: DEFAULTS at clock`, `D3R13 pass 1` | 16 | yes | D3R13 pass 0: DEFAULTS at clock 0 of the aggregate 1000001, cause 0, rolled back 0, applied 0, the longest wai |
| `no_backoff_binding` | `tb/acmp_nvm` | KILLED | `E9 DR2c timing` | 1 | yes | E9 DR2c timing: each retry starts RETRY_BACKOFF_CYC_P cycles or more after the failed attempt's error (43, 43) |
| `no_backoff_d3` | `tb/pp_top` | KILLED | `D3S10 timing` | 2 | yes | D3S10 timing: each retry granted after the derived 500001-cycle backoff and one relatch (15, 15) |
| `no_restore_watchdog` | `tb/pp_top` | KILLED | `D3R8: a READ granted`, `D3R8b` | 7 | yes | D3R5 the header never answered: DEFAULTS, cause 0, applied 0, rows at their defaults |
| `no_rollback` | `tb/pp_top` | KILLED | `D3R4:` | 17 | yes | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause 5, rolled back 0: every row at its defau |
| `own_taken_at_the_walk` | `tb/pp_top` | KILLED | `D3R9: the held SET` | 10 | yes | D3O1: without the walk the writer owns every cycle (0 of 2000), the engine runs nothing (1998 busy) and the co |
| `owned_arm_cross_intent` | `tb/acmp_nvm` | KILLED | `N11d manager 1's abort held while manager 0 owns each of the walk's READs` | 1 | yes | N11d manager 1's abort held while manager 0 owns each of the walk's READs: present in 45 of the 45 cycles mana |
| `owned_arm_write_too` | `tb/acmp_nvm` | KILLED | `N11a a manager-1 WRITE presented with its abort` | 1 | yes | N11a a manager-1 WRITE presented with its abort: issued as a commit (1), never drained (from 423536), every by |
| `pass1_read_not_drained` | `tb/pp_top` | KILLED | `D3R5b: once the device ends the drained pass-1 READ` | 1 | yes | D3R5b: once the device ends the drained pass-1 READ a later SET persists (0 WRITEs, unflushed 1) |
| `passes_may_disagree` | `tb/pp_top` | KILLED | `D3R4:`, `D3R4b` | 3 | yes | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause 0, rolled back 0: every row at its defau |
| `per_wait_floor` | `tb/pp_top` | KILLED | `D3R8 deadline` | 1 | yes | D3R8 deadline: the walk aborted on the 20000-th stalled cycle, the derived deadline is 20001 |
| `proof_default_only_from_img` | `tb/pp_top` | KILLED | `D3R19 past the bound: DEFAULTS`, `D3R19 inside the LOCATE: DEFAULTS`, `D3R20 W_IMGLOC: DEFAULTS` | 3 | yes | D3R19 past the bound: DEFAULTS with no record READ; the restore ends DEFAULTS 2713 clocks after the bound, cau |
| `proof_past_bound_needs_fired` | `tb/pp_top` | KILLED | `D3R20 W_IMG: DEFAULTS`, `D3R20 W_IMGLOC: DEFAULTS` | 2 | yes | D3R20 W_IMG: DEFAULTS with no record READ; the restore ends COMPLETE 2168 clocks after the bound, cause 0, rol |
| `proof_past_needs_fire` | `tb/pp_top` | KILLED | `D3R20 W_IMG: DEFAULTS`, `D3R20 W_IMGLOC: DEFAULTS` | 2 | yes | D3R20 W_IMG: DEFAULTS with no record READ; the restore ends COMPLETE 2168 clocks after the bound, cause 0, rol |
| `proof_reads_records_past_bound` | `tb/pp_top` | KILLED | `D3R14 image valid: DEFAULTS` | 6 | yes | D3R14 image valid: DEFAULTS by clock 1020006, the D3 walk's longest wait 20000 (no record READ requested), cau |
| `quarantine_released_by_time` | `tb/pp_top` | KILLED | `D3R5: once the device ends the drained read a later SET persists` | 10 | yes | D3R5: once the device ends the drained read a later SET persists |
| `rate_walk_stuck_on_first_lane` | `tb/pp_top` | KILLED | `D3R3b entry 7` | 1 | yes | D3R3b entry 7 of 10 (24000 Hz): applied 0 refused 1, rate 0 valid 0 |
| `rate_walk_unbounded` | `tb/pp_top` | KILLED | `D3R3b entry 8` | 1 | yes | D3R3b entry 8 of 10 (16000 Hz): applied 1 refused 0, rate 16000 valid 1 |
| `resident_never_returned` | `tb/pp_top` | KILLED | `D3O7: the returned slot frees the share` | 1 | yes | D3O7: the returned slot frees the share: the next command held, the one after it dropped (2 counted), none ans |
| `restore_writes_are_changes` | `tb/pp_top` | KILLED | `D3R1: no restore write is a change` | 1 | yes | D3R1: no restore write is a change (50163 pending cycles, 12 device writes) |
| `rollback_ignores_debt` | `tb/pp_top` | KILLED | `D3R10 16000` | 3 | yes | D3R10 5000: done 6537 closed -1 cause 6 rolled back 1; the stores in reset from 5077 to 5079, the debt owed 2  |
| `rollback_one_cycle` | `tb/pp_top` | KILLED | `D3R4 strobe` | 1 | yes | D3R4 strobe: with no debt owed the roll-back holds both stores in reset 1 cycles, at least two |
| `rule_ignored` | `tb/pp_top` | KILLED | `D3R2: COMPLETE` | 3 | yes | D3R2: COMPLETE, applied 7 refused 4 blank 16 of 27 |
| `store_not_cleared` | `tb/pp_top` | KILLED | `D3R1: every row at its reset value` | 17 | yes | D3R1: every row at its reset value, valid clear, when the D3 walk starts |
| `store_not_rolled_back` | `tb/pp_top` | KILLED | `D3R10 5000` | 3 | yes | D3R10 5000: done -1 closed 6003 cause 6 rolled back 0; the stores in reset from 5077 to 5999, the debt owed 92 |
| `taint_ignored` | `tb/pp_top` | KILLED | `D3S4 taint` | 1 | yes | D3S4 taint: 1 WRITEs of 0x50, the first carrying the latched value, the last the change made during it |
| `unchanged_compare_ignores_validity` | `tb/pp_top` | KILLED | `D3S8 validity` | 1 | yes | D3S8 validity: clock source 0 on the unset row is written (0) |
| `unframed_reads_as_device_error` | `tb/pp_top` | KILLED | `D3R6: an erased device restores blank` | 38 | yes | D3O1: a validated image is proven without a LOCATE (0 requests from the release to the terminal), COMPLETE |
| `valid_not_cleared` | `tb/pp_top` | KILLED | `D3R1: every row at its reset value` | 17 | yes | D3R1: every row at its reset value, valid clear, when the D3 walk starts |
| `validator_admits_held_aecp` | `tb/rx_validator` | KILLED | `F28 held AECP`, `F28 rx_aecp_held counts both` | 4 | yes | F28 held AECP: slot taken and returned, no commit, no header beat, no other counter (allocs 1 aborts 0 commits |

# D3 mutation campaign at the head

`python3 tb/pp_top/d3_mutants.py --output <out>/d3-mutants --jobs 6 --verilator <pinned 5.050>` from the clean clone at `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71` (the gates run, GATES.md): rc 0, 69 of 69 KILLED by their named checks, goldens golden-acmp_nvm PASS, golden-pp_top PASS, golden-rx_validator PASS. A mutant is KILLED only when its build succeeds, its run completes with its tally, exits non-zero and every named check fails. Every 'Failing checks' count equals its README record: the 65 rows of `tb/pp_top/README.md`, the 3 of `tb/acmp_nvm/README.md`, and `tb/rx_validator/README.md` M4 ("4 FAILs"); no mismatch. Rows marked **new** are this round's.

| Mutant | Suite | Verdict | Named checks (each failing) | Failing checks | First failing message |
|---|---|---|---|---|---|
| `hold_released_at_go` | `tb/pp_top` | KILLED | `D3O1: released at` | 16 | D3O1: released at 122, terminal at 880, own fell at 123, the held command taken at 124, 0 busy cycles while ow… |
| `dispatch_not_held` | `tb/pp_top` | KILLED | `D3O1: without the walk the writer owns every cycle` | 5 | D3O1: without the walk the writer owns every cycle (2000 of 2000), the engine runs nothing (1998 busy) and the… |
| `own_taken_at_the_walk` | `tb/pp_top` | KILLED | `D3R9: the held SET` | 10 | D3O1: without the walk the writer owns every cycle (0 of 2000), the engine runs nothing (1998 busy) and the co… |
| `image_unproven_continues` | `tb/pp_top` | KILLED | `D3O2: CLOSED at`, `D3O3: CLOSED` | 9 | D3O2: CLOSED at -1 after the release at 122, cause 0, own 0, 2 descriptor requests |
| `latch_ignores_program` | `tb/pp_top` | KILLED | `D3S9` | 3 | D3S5 same edge: the change on the done edge is written (6 WRITEs) |
| `TRG_cfg` | `tb/pp_top` | KILLED | `D3S1 cfg` | 3 | D3S1 cfg: record 0x00 written once, byte-exact (0 writes) |
| `TRG_rate` | `tb/pp_top` | KILLED | `D3S1 rate` | 3 | D3S1 rate: record 0x02 written once, byte-exact (0 writes) |
| `TRG_clks` | `tb/pp_top` | KILLED | `D3S1 clks` | 5 | D3S1 clks: record 0x0a written once, byte-exact (0 writes) |
| `TRG_fmti` | `tb/pp_top` | KILLED | `D3S1 fmti` | 4 | D3S1 fmti: record 0x30 written once, byte-exact (0 writes) |
| `TRG_fmto` | `tb/pp_top` | KILLED | `D3S1 fmto` | 4 | D3S1 fmto: record 0x40 written once, byte-exact (0 writes) |
| `TRG_ptof` | `tb/pp_top` | KILLED | `D3S1 ptof` | 23 | D3S1 ptof: record 0x50 written once, byte-exact (0 writes) |
| `taint_ignored` | `tb/pp_top` | KILLED | `D3S4 taint` | 1 | D3S4 taint: 1 WRITEs of 0x50, the first carrying the latched value, the last the change made during it |
| `clear_wins_same_edge` | `tb/pp_top` | KILLED | `D3S5 same edge` | 1 | D3S5 same edge: the change on the done edge is written (1 WRITEs) |
| `clear_by_group` | `tb/pp_top` | KILLED | `D3S6 group` | 8 | D3S1 fmti: record 0x31 written once, byte-exact (0 writes) |
| `clear_by_index` | `tb/pp_top` | KILLED | `D3S6 index` | 14 | D3S1 rate: record 0x02 written once, byte-exact (0 writes) |
| `identify_is_a_change` | `tb/pp_top` | KILLED | `D3S7` | 1 | D3S7: IDENTIFY set, 49787 pending cycles, 2 NVM operations |
| `unchanged_compare_ignores_validity` | `tb/pp_top` | KILLED | `D3S8 validity` | 1 | D3S8 validity: clock source 0 on the unset row is written (0) |
| `RPL_cfg` | `tb/pp_top` | KILLED | `D3R1 cfg` | 6 | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blank 18 of 27 |
| `RPL_rate` | `tb/pp_top` | KILLED | `D3R1 rate` | 6 | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blank 18 of 27 |
| `RPL_clks` | `tb/pp_top` | KILLED | `D3R1 clks` | 3 | D3R1: COMPLETE 1866 cycles after the release, applied 8 refused 1 blank 18 of 27 |
| `RPL_fmti` | `tb/pp_top` | KILLED | `D3R1 fmti` | 2 | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blank 18 of 27 |
| `RPL_fmto` | `tb/pp_top` | KILLED | `D3R1 fmto` | 2 | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blank 18 of 27 |
| `RPL_ptof` | `tb/pp_top` | KILLED | `D3R1 ptof` | 6 | D3R1: COMPLETE 1865 cycles after the release, applied 7 refused 2 blank 18 of 27 |
| `rule_ignored` | `tb/pp_top` | KILLED | `D3R2: COMPLETE` | 3 | D3R2: COMPLETE, applied 7 refused 4 blank 16 of 27 |
| `passes_may_disagree` | `tb/pp_top` | KILLED | `D3R4:`, `D3R4b` | 3 | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause 0, rolled back 0: every row at its defau… |
| `device_error_reads_as_blank` | `tb/pp_top` | KILLED | `D3R5 device error on the header`, `D3R6: the one saved record` | 5 | D3R5 device error on the header: DEFAULTS, cause 5, applied 1, rows at their defaults |
| `unframed_reads_as_device_error` | `tb/pp_top` | KILLED | `D3R6: an erased device restores blank` | 38 | D3O1: a validated image is proven without a LOCATE (0 requests from the release to the terminal), COMPLETE |
| `desc_error_is_a_refusal` | `tb/pp_top` | KILLED | `D3R7` | 6 | D3R7: the rule's descriptor fetch errs: cause 0, refused 1, rolled back 0 |
| `no_restore_watchdog` | `tb/pp_top` | KILLED | `D3R8: a READ granted`, `D3R8b` | 7 | D3R5 the header never answered: DEFAULTS, cause 0, applied 0, rows at their defaults |
| `restore_writes_are_changes` | `tb/pp_top` | KILLED | `D3R1: no restore write is a change` | 1 | D3R1: no restore write is a change (50163 pending cycles, 12 device writes) |
| `enable_not_released_by_restore` | `tb/pp_top` | KILLED | `D3R1: the enable requested from reset` | 4 | D3R1: the enable requested from reset reaches ADP only at the combined terminal (1989 early enable cycles, 0 e… |
| `done_without_d3` | `tb/pp_top` | KILLED | `D3R1: the enable requested from reset`, `D3R1: COMPLETE` | 39 | D3R1: COMPLETE 0 cycles after the release, applied 9 refused 0 blank 18 of 27 |
| `blank_ignores_d3` | `tb/pp_top` | KILLED | `D3R1: COMPLETE` | 1 | D3R1: COMPLETE 1867 cycles after the release, applied 9 refused 0 blank 18 of 27 |
| `store_not_cleared` | `tb/pp_top` | KILLED | `D3R1: every row at its reset value` | 17 | D3R1: every row at its reset value, valid clear, when the D3 walk starts |
| `valid_not_cleared` | `tb/pp_top` | KILLED | `D3R1: every row at its reset value` | 17 | D3R1: every row at its reset value, valid clear, when the D3 walk starts |
| `quarantine_released_by_time` | `tb/pp_top` | KILLED | `D3R5: once the device ends the drained read a later SET persists` | 8 | D3R5: once the device ends the drained read a later SET persists |
| `no_rollback` | `tb/pp_top` | KILLED | `D3R4:` | 17 | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause 5, rolled back 0: every row at its defau… |
| `dyn_not_rolled_back` | `tb/pp_top` | KILLED | `D3R4:` | 4 | D3R4: the record whole in pass 0 and unframed in pass 1 aborts, cause 5, rolled back 1: every row at its defau… |
| `store_not_rolled_back` | `tb/pp_top` | KILLED | `D3R10 5000` | 3 | D3R10 5000: done -1 closed 6003 cause 6 rolled back 0; the stores in reset from 5077 to 5999, the debt owed 92… |
| `rollback_ignores_debt` | `tb/pp_top` | KILLED | `D3R10 16000` | 3 | D3R10 5000: done 6537 closed -1 cause 6 rolled back 1; the stores in reset from 5077 to 5079, the debt owed 2 … |
| `closed_releases_the_entity` | `tb/pp_top` | KILLED | `D3R12` | 2 | D3R12: the re-walk cannot prove the image: CLOSED -1, cause 2, the entity held |
| `no_backoff_d3` | `tb/pp_top` | KILLED | `D3S10 timing` | 2 | D3S10 timing: each retry granted after the derived 500001-cycle backoff and one relatch (15, 15) |
| `fourth_attempt` | `tb/pp_top` | KILLED | `D3S10 count` | 2 | D3S10 count: 4 failed attempts of 0x50 (4 grants), alarm 1, unflushed 0 |
| `alarm_forgiven_by_success` | `tb/pp_top` | KILLED | `D3S10 revocation` | 1 | D3S10 revocation: a later successful write leaves the alarm set |
| `no_backoff_binding` | `tb/acmp_nvm` | KILLED | `E9 DR2c timing` | 1 | E9 DR2c timing: each retry starts RETRY_BACKOFF_CYC_P cycles or more after the failed attempt's error (43, 43) |
| `fourth_attempt_binding` | `tb/acmp_nvm` | KILLED | `E8 DR2c count` | 3 | E8 DR2c count: three attempts in all (4 started, 4 failed) |
| `alarm_forgiven_binding` | `tb/acmp_nvm` | KILLED | `E11 DR2c revocation` | 1 | E11 DR2c revocation: a later successful commit and time leave the alarm set |
| `backoff_derivation` | `tb/pp_top` | KILLED | `D3S10 timing` | 2 | D3S10 timing: each retry granted after the derived 500001-cycle backoff and one relatch (5014, 5014) |
| `backoff_holds_dispatch` | `tb/pp_top` | KILLED | `D3S10 backoff` | 1 | D3S10 backoff: 999936 owned cycles inside the backoffs; a READ_DESCRIPTOR sent into the first is answered 5013… |
| `disagree_one_direction` | `tb/pp_top` | KILLED | `D3R4b` | 1 | D3R4b: a record blank in pass 0 and whole in pass 1 aborts, cause 0, rolled back 0, the offset not applied (va… |
| `rollback_one_cycle` | `tb/pp_top` | KILLED | `D3R4 strobe` | 1 | D3R4 strobe: with no debt owed the roll-back holds both stores in reset 1 cycles, at least two |
| `pass1_read_not_drained` | `tb/pp_top` | KILLED | `D3R5b: once the device ends the drained pass-1 READ` | 1 | D3R5b: once the device ends the drained pass-1 READ a later SET persists (0 WRITEs, unflushed 1) |
| `judge_wait_unwatched` | `tb/pp_top` | KILLED | `D3R8b` | 1 | D3R8b: a silent judge ends DEFAULTS at -1, the release at 122, cause 0, rolled back 0 |
| `rate_walk_stuck_on_first_lane` | `tb/pp_top` | KILLED | `D3R3b entry 7` | 1 | D3R3b entry 7 of 10 (24000 Hz): applied 0 refused 1, rate 0 valid 0 |
| `rate_walk_unbounded` | `tb/pp_top` | KILLED | `D3R3b entry 8` | 1 | D3R3b entry 8 of 10 (16000 Hz): applied 1 refused 0, rate 16000 valid 1 |
| `no_aggregate_deadline` | `tb/pp_top` | KILLED | `D3R13 pass 0: DEFAULTS at clock`, `D3R13 pass 1` | 11 | D3R13 pass 0: DEFAULTS at clock 0 of the aggregate 1000001, cause 0, rolled back 0, applied 0, the longest wai… |
| `aggregate_mirrored` | `tb/pp_top` | KILLED | `D3R13 pass 0: DEFAULTS at clock` | 11 | D3R13 pass 0: DEFAULTS at clock 0 of the aggregate 1000001, cause 0, rolled back 0, applied 0, the longest wai… |
| `aggregate_from_the_walk` | `tb/pp_top` | KILLED | `D3R13 pass 0: DEFAULTS at clock` | 13 | D3R13 pass 0: DEFAULTS at clock 0 of the aggregate 1000001, cause 0, rolled back 0, applied 0, the longest wai… |
| `per_wait_floor` | `tb/pp_top` | KILLED | `D3R8 deadline` | 1 | D3R8 deadline: the walk aborted on the 20000-th stalled cycle, the derived deadline is 20001 |
| `agg_closes_before_proof` **new** | `tb/pp_top` | KILLED | `D3R14 image valid: DEFAULTS` | 3 | D3R14 image valid: DEFAULTS by clock 0, the D3 walk's longest wait 0 (no record READ requested), cause 3, roll… |
| `binding_walk_ignores_aggregate` **new** | `tb/pp_top` | KILLED | `D3R14 image valid: the binding walk`, `D3R14 image refused: the binding walk` | 5 | D3R14 image valid: the binding walk (longest wait 19002 of 20001) fails whole at the bound's clock 1000001 (ca… |
| `proof_reads_records_past_bound` **new** | `tb/pp_top` | KILLED | `D3R14 image valid: DEFAULTS` | 1 | D3R14 image valid: DEFAULTS by clock 1020006, the D3 walk's longest wait 20000 (no record READ requested), cau… |
| `agg_not_in_rollback` **new** | `tb/pp_top` | KILLED | `D3R15 debt wait: CLOSED`, `D3R15 re-LOCATE: CLOSED` | 4 | D3R15 debt wait: the pass-1 fault's READ (region 0x02 offset 8) granted on its steered cycle 1; at the bound t… |
| `agg_not_stopped_at_terminal` **new** | `tb/pp_top` | KILLED | `D3R16 COMPLETE`, `D3R16 DEFAULTS`, `D3R16 CLOSED` | 3 | D3R16 COMPLETE: two per-wait deadlines past the bound the verdicts hold (done 1 fail 1 rolled back 0 closed 1 … |
| `agg_fires_with_event_in_hand` **new** | `tb/pp_top` | KILLED | `D3R17: the writer's grant`, `D3R17: once the device ends` | 2 | D3R17: the writer's grant lands on the bound's own clock (1, 0x56's READ steered 1, latency 9); DEFAULTS 1 clo… |
| `aecp_hold_unbounded` | `tb/pp_top` | KILLED | `D3O5: in CLOSED each GET_RX_STATE`, `D3O6: during the slowed walk` | 7 | D3O5: in CLOSED each GET_RX_STATE after each of 6 AECP commands is answered in 168 cycles, the idle latency (w… |
| `held_drop_uncounted` | `tb/pp_top` | KILLED | `D3O5: one AECP command held`, `D3O6: at the terminal` | 5 | D3O5: one AECP command held, 0 dropped at the slot gate and counted, 0 answered |
| `resident_never_returned` **new** | `tb/pp_top` | KILLED | `D3O7: the returned slot frees the share` | 1 | D3O7: the returned slot frees the share: the next command held, the one after it dropped (2 counted), none ans… |
| `validator_admits_held_aecp` | `tb/rx_validator` | KILLED | `F28 held AECP`, `F28 rx_aecp_held counts both` | 4 | F28 held AECP: slot taken and returned, no commit, no header beat, no other counter (allocs 1 aborts 0 commits… |

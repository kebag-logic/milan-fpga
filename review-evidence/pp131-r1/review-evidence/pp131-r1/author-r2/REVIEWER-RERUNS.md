# The reviewers' own scripts, rerun at `2b38d68`

Each script is read from the review packets unchanged and run on an export of the head in scratch with the pinned Verilator 5.050, except that R390-1's `r390_mutants.py` has its hard-coded `HEAD` constant set to `2b38d68e704e8a62fbeae8171c9195ca93728488` (a one-line copy) and `mut_backoff_derivation.sh` takes `HEAD` from the environment. R390-1's three probe headers are appended to a scratch copy of `d3_phases.hpp` with their switches beside `--dr3a`, as its README describes.

## R391-1 `run_probes.sh` (P1-P5, the P3/P4 golden and mutant variants, `r391_mutants.py`)

```
R391-P1 CLOSED n_aecp=0 closed=1 acmp_before=168 acmp_after=168 acmp_after2=168 aecp_responses=0
R391-P1 CLOSED n_aecp=3 closed=1 acmp_before=168 acmp_after=168 acmp_after2=168 aecp_responses=0
R391-P1 CLOSED n_aecp=4 closed=1 acmp_before=168 acmp_after=168 acmp_after2=168 aecp_responses=0
R391-P1 CLOSED n_aecp=5 closed=1 acmp_before=168 acmp_after=168 acmp_after2=168 aecp_responses=0
R391-P1 CLOSED n_aecp=6 closed=1 acmp_before=168 acmp_after=168 acmp_after2=168 aecp_responses=0
R391-P1 CLOSED n_aecp=8 closed=1 acmp_before=168 acmp_after=168 acmp_after2=168 aecp_responses=0
R391-P2 WALK n_aecp=0 release=122 asked 0 cycles after the release, acmp_latency=168 d3_done_now=1 restore_fail=0 held_aecp_answered=0 acmp_after_terminal=168
R391-P2 WALK n_aecp=8 release=122 asked 512 cycles after the release, acmp_latency=168 d3_done_now=1 restore_fail=0 held_aecp_answered=1 acmp_after_terminal=168
R391-P3 pass-1 silent read: done 21643 closed -1 fail 1 rb 1 cause 3 rows_cleared 1 own 0 img_valid 1
R391-P4 judge silent: done 21455 closed -1 fail 1 rb 1 cause 3 rows_cleared 1 own 0
R391-P5 slow-but-inside device: 51 D3 reads each held 19801 cycles; terminal 1000421 cycles after the release = 50.0 x RS_TMO (the ratified aggregate is 50 x the per-wait candidate); fail 1 cause 3
golden R391-P3b after the device ends the abandoned read: SET ok 1, WRITEs of 0x50 1, unflushed 0
golden R391-P3 pass-1 silent read: done 21643 closed -1 fail 1 rb 1 cause 3 rows_cleared 0 own 0 img_valid 1
golden R391-P4 judge silent: done 21455 closed -1 fail 1 rb 1 cause 3 rows_cleared 1 own 0
mutant R391-P3b after the device ends the abandoned read: SET ok 1, WRITEs of 0x50 0, unflushed 1
mutant R391-P3 pass-1 silent read: done 21643 closed -1 fail 1 rb 1 cause 3 rows_cleared 0 own 0 img_valid 1
mutant R391-P4 judge silent: done -123 closed -1 fail 0 rb 0 cause 0 rows_cleared 0 own 1
pass1_read_not_drained             KILLED     rc=1 D3: 104 checks, 1 failures | FAIL: D3R5b: once the device ends the drained pass-1 READ a later SET persists (0 WRITEs, unflushed 1)
rate_walk_unbounded                KILLED     rc=1 D3: 104 checks, 1 failures | FAIL: D3R3b entry 8 of 10 (16000 Hz): applied 1 refused 0, rate 16000 valid 1
rate_walk_stuck_on_first_lane      KILLED     rc=1 D3: 104 checks, 1 failures | FAIL: D3R3b entry 7 of 10 (24000 Hz): applied 0 refused 1, rate 0 valid 0
judge_wait_unwatched               KILLED     rc=1 D3: 104 checks, 1 failures | FAIL: D3R8b: a silent judge ends DEFAULTS at -1, the release at 122, cause 0, rolled back 0
backoff_holds_dispatch             KILLED     rc=1 D3: 104 checks, 1 failures | FAIL: D3S10 backoff: 999936 owned cycles inside the backoffs; a READ_DESCRIPTOR sent into the first is answered 501303 cycles later, before the retry
disagree_whole_then_blank_only     KILLED     rc=1 D3: 104 checks, 1 failures | FAIL: D3R4b: a record blank in pass 0 and whole in pass 1 aborts, cause 0, rolled back 0, the offset not applied (valid 0x01)
rollback_strobe_one_cycle          KILLED     rc=1 D3: 104 checks, 1 failures | FAIL: D3R4 strobe: with no debt owed the roll-back holds both stores in reset 1 cycles, at least two
```

## R390-1 probes (`probe_hol`, `probe_hol_restore`, `probe_gaps`)

```
PROBE COMPLETE: done 1 closed 0 released 1 own 0
PROBE COMPLETE: k=0 AECP frames queued, GET_RX_STATE answered 1
PROBE COMPLETE: k=1 AECP frames sent, GET_RX_STATE answered 1, aecp head 0, aecp responses so far 0
PROBE COMPLETE: k=2 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE COMPLETE: k=3 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE COMPLETE: k=4 AECP frames sent, GET_RX_STATE answered 0, aecp head 0, aecp responses so far 2
PROBE COMPLETE: k=5 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 3
PROBE COMPLETE: k=6 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 3
PROBE COMPLETE: k=7 AECP frames sent, GET_RX_STATE answered 0, aecp head 0, aecp responses so far 5
PROBE COMPLETE: k=8 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 6
PROBE COMPLETE: k=9 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 6
PROBE COMPLETE: k=10 AECP frames sent, GET_RX_STATE answered 0, aecp head 0, aecp responses so far 8
PROBE COMPLETE: after 2000 ms, GET_RX_STATE answered 1
PROBE CLOSED: done 0 closed 1 released 1 own 1
PROBE CLOSED: k=0 AECP frames queued, GET_RX_STATE answered 1
PROBE CLOSED: k=1 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE CLOSED: k=2 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE CLOSED: k=3 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE CLOSED: k=4 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE CLOSED: k=5 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE CLOSED: k=6 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE CLOSED: k=7 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE CLOSED: k=8 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE CLOSED: k=9 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE CLOSED: k=10 AECP frames sent, GET_RX_STATE answered 1, aecp head 1, aecp responses so far 0
PROBE CLOSED: after 2000 ms, GET_RX_STATE answered 1
PROBE-R n_aecp=0: released at 123; after the GET was fed: GET_RX_STATE answered at 167, D3 terminal at 16089 (answered before the D3 terminal)
PROBE-R n_aecp=2: released at 123; after the GET was fed: GET_RX_STATE answered at 167, D3 terminal at 15961 (answered before the D3 terminal)
PROBE-R n_aecp=6: released at 123; after the GET was fed: GET_RX_STATE answered at 167, D3 terminal at 15705 (answered before the D3 terminal)
PROBE G1 blank-in-pass-0 then whole-in-pass-1: planted 1 done 1776 fail 1 cause 5 rolled back 1 applied 1 ptof0 valid 0 value 0
PROBE G2 SET ok 1; first failed attempt err at 49755; a READ_DESCRIPTOR sent 1000 cycles into the backoff answered after 2299 cycles (own now 0)
```

## R390-1 `r390_mutants.py` and `mut_backoff_derivation.sh`

```
backoff_holds_dispatch: KILLED run rc=1 ['D3: 104 checks, 1 failures'] first fails: ['FAIL: D3S10 backoff: 999936 owned cycles inside the backoffs; a READ_DESCRIPTOR sent into the first is answered 501303 cycles later, before the retry']
disagree_one_direction: KILLED run rc=1 ['D3: 104 checks, 1 failures'] first fails: ['FAIL: D3R4b: a record blank in pass 0 and whole in pass 1 aborts, cause 0, rolled back 0, the offset not applied (valid 0x01)']
rollback_one_cycle: KILLED run rc=1 ['D3: 104 checks, 1 failures'] first fails: ['FAIL: D3R4 strobe: with no debt owed the roll-back holds both stores in reset 1 cycles, at least two']
mutant backoff_derivation suite pp_top rc=2: make: *** [Makefile:71: run] Error 1
mutant backoff_derivation suite timer_map rc=0: 1360 checks: 1360 PASS, 0 FAIL
VERDICT backoff_derivation KILLED
```

Reading. R391-1 P1/P2: every GET_RX_STATE is answered in 168 cycles, the idle latency, for 0 to 8 held AECP commands in CLOSED and 8 during a stretched walk; the one held command is answered after the walk (`held_aecp_answered=1`). P5: a device answering every D3 read 200 cycles inside the deadline now ends at the aggregate bound (50.0 x the per-wait deadline). P3/P4 and the four R391-1 mutants and three R390-1 cross-checks: every mutant KILLED by the named check this round added. R390-1: `probe_hol` CLOSED answers every GET_RX_STATE for k = 0 to 10 and after 2,000 ms; `probe_hol_restore` answers in 167 cycles before the D3 terminal with 0, 2 and 6 AECP commands queued; G1 blank-then-whole aborts (cause 5, rolled back) and G2's READ_DESCRIPTOR in the backoff is answered in 2,299 cycles with `own` 0; its three mutants and the backoff-derivation mutant are KILLED.

Unchanged and outside the ruling: in `probe_hol`'s COMPLETE case (the hold released, the engine serving) GET_RX_STATE goes unanswered within the probe's 50 ms at k = 4, 7 and 10, byte-for-byte the pattern of R390-1's own receipt at `e1ae468` (`receipts/probe-hol.txt`): with the engine running, four READ_DESCRIPTORs in flight can still fill the four-slot pool for the few milliseconds each takes, and the frame arriving then is an ordinary counted overrun. The admission ruling bounds AECP's share only while the writer holds AECP; whether service time wants a share too is the manager's call, not taken here.

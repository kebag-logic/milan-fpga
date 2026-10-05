[A532]

Closes #148

The #148 lane (assignment: #148 comment 5982500256). Branch `pp148-notify-spacing` from
`main` `07b1469d`; current head `bed5f47785839800bb640d7c747f5435f84ab5a3`, including
`--no-ff` merges of `b0a74196` and `ead80360`. Not pushed.

`KL_aecp_notify` stamped a GET_COUNTERS round's one-second limit when it **selected** the
round. A round whose job then waited for the engine and the TX slot (a solicited answer
leaving just before it) was sent late, and the next round, on time, left less than a second
after it. Milan Table 5.22 (`T-CTR-NOTIF`) allows one GET_COUNTERS notification per
descriptor per second. The stamp now follows the clock while each of the round's jobs waits,
and holds the job's send, so the next round starts a second after the previous round's last
send, at every controller. #232's storage is kept. No port, parameter or register changes.

| Commit | Item |
|---|---|
| `abbe55b` | 1, red first: `tb/pp_top` section CS (#148's shifted timing, every row graded) and `tb/aecp_notify` section TW (a job held for the TX slot); both fail on `main`'s RTL |
| `82e1664` | 2, the fix in `KL_aecp_notify` (+9 -1) and 06 section 7 |
| `5f458aa` | the controls in `notify_mutants.py`; TW prints its send figures; ST's comment drops the selection stamp |
| `221fd63` | the READMEs and 09 section 8.4; `counter_limit_500ms` is now held by ST2b alone (below) |
| `a369cdd` | two more controls for CS's premise and phase-0 run; the ctr campaign's record at the head |

## Round 1b: union with PRs #157 and #155

`415a9fd` merges `b0a74196` with `--no-ff`; `4ed463b` merges `ead80360` with
`--no-ff`. The second merge resolves `sim_main.cpp`'s shared flag declarations and
`one_section` expression by retaining both `--spacing-only` and `--arm-queue-only`.
`bed5f47` corrects the README to seven notification sections, including TD.
No RTL fix was required after either merge.

Validation is complete at base `ead80360` and head `bed5f477`. Every compiled
input at `4ed463b` equals the final head's; documentation checks were repeated at
`bed5f477`. All required return codes are 0. The original-round tables below keep
their original revision labels; the current union results are:

| Gate | Base | Head |
|---|---|---|
| All processor suites | 33 suites; 1,021,627 checks | 33 suites; 1,021,640 checks: TW +4, CS +9 |
| Six `pp_top` builds | default 9,947; vid 20; identify 178; line 231; timebase 56; TD 3 | default 9,956; other five unchanged; TD 6 probes |
| `aecp_notify`; `acmp_listener` | 30; 3,111 | 34; 3,111 |
| Lint; Yosys | 41 LINT OK; 42 tops | identical verdicts |
| Documentation / matrix | 1,136 links; 115 REQ, 17 GAP; 94 rows, 0 untested; 28 parameters | identical |
| Notify campaign | 6 controls, 47 KILLED | 7 controls, 53 KILLED; six new arms fail their named checks |
| Ctr campaign | 1 control, 17 KILLED | same |
| AECP campaign, including TD/HZ | 6 controls, 61 KILLED | same; all 67 records agree |
| ACMP campaign, including AQ/listener | 4 controls, 33 KILLED | same; all 37 records agree |
| D3 campaign | 6 controls, 110 KILLED | same; all 116 verdicts, named checks and failure counts agree |
| AECP dispatch | 4 controls, 40 KILLED | same; all 44 result records agree |
| GSI; name write | 22; 3 passing campaign records | identical |
| ADP; MAAP | 43; 32 passing campaign records | identical |
| Parent gate 15 | original accepted head retained for comparison | current pin passes; all simulation legs, render 6/6, gmstep 6/6; all 11,466 check/info/verdict lines identical |

The two intended campaign changes remain `counter_limit_500ms` (12 to 7 failing
checks) and `ctr-notify-one-window` (3 to 4). Other numeric differences remain the
ST2c figures, four K14 latency messages, and existing unbound D3C diagnostic integers;
no other failing-check count changes. All six new mutants are killed by the named
CS/TW checks. The merged suite total is exactly upstream's +142 checks plus this
lane's +13.

The first AQ coverage line gains three ADP timer arms: `--arm-queue-only` reports
8,273 instead of 8,270; the full default run 8,283 instead of 8,280. An instrumented
scratch run traces this to U9's deferred counter update leaving 18 ms later under
#148's spacing. The later continuously advancing PRNG draws change ADP's subsequent
advertise schedule. All other faces' arm counts agree; AQ's forced-drive coverage,
all AQ checks, and all 33 ACMP mutants agree. No expectation was weakened.

The docs agree: 06 section 7's spacing and storage, 09 section 8.3's timer defaults
and hazards, and the README's CS, HZ and TD sections retain all three lanes' contracts.
All five parent patches apply in order at parent `6c22d3ca`; gate 15 passes with
processor pin `bed5f477`. The scratch parent remains uncommitted. The original
OOC measurement below is retained under the targeted re-measure rule; notify RTL
is byte-identical to that measured head.

## 1. Red first

Both checks were committed before the fix and fail on `main`'s RTL (`abbe55b`):

```
tb/aecp_notify:
FAIL: TW1: ... whose last job waited for the TX slot until ms 2600 ... next round at ms 3005, want 3600 to 3608
FAIL: TW2: ... waited for the TX slot until ms 6500 ... the round's last send at ms 6504: next round at ms 6508, want 7504 to 7512
tb/pp_top --spacing-only:
[i] CS2a: churn 0 clocks after ST's phase, closest rounds 99994 clocks apart (row 15, descriptor 0006:0)
FAIL: CS2b: churn started 30 clocks after ST's phase ... closest 99854 clocks (row 0, descriptor 0006:0), want at least 99900
FAIL: CS2c: churn started 95 clocks after ST's phase ... closest 99590 clocks (row 0, descriptor 0005:1), want at least 99900
```

**"Shifted timing".** The `tb/pp_top` README recorded that starting ST's churn 30 to 95
clocks later fails ST2b at `ddb3119d`. Section CS runs ST's churn (five descriptors at
10 Hz for 3.5 s, a GET_CONFIGURATION and a GET_RX_STATE every 700 ms, 1.5 s quiet) on a fresh
processor with all sixteen rows registered, at ST's phase and 30 and 95 clocks later. It
grades every row's rounds, not only row 0's, against ST2's bound (1,000 ms less the one tick
the limiter reads, 99,900 clocks) and at least three rounds per row. A sweep over 200 starts
at `main` (a scratch copy of the bench) puts every start 27 to 98 clocks after ST's phase
(of every 100) below the bound. With the fix, every start 0 to 199 leaves at least 115,036
clocks.

**TX slot.** Section TW drives the block directly: the bench is the engine, retires each job
when the section says, and its clock advances one ms per cycle.
- TW1: in a round, C's job is sent at once and D's waits until ms 2600. A change at ms 2700
  goes out a second after that last send (ms 3603; `main`: ms 3005).
- TW2: C's job waits 1.5 s for the TX slot, and a change arrives during the wait. It goes
  out a second after the round's last send (ms 7507; `main`: ms 6508, right after the round).

## 2. The fix (`hdl/aecp/KL_aecp_notify.sv`, +9 -1)

- `:469`, `:1043`, `:1297`: `em_ctr_ix_r`, the claimed round's descriptor slot (3 bits at
  1x1), reset with the other `em_*` registers and latched at the claim.
- `:1443`, in `N_EMIT_WAIT`:
  `if (em_kind_r == PP_UNS_CTRS_C) ctr_last_r[em_ctr_ix_r] <= now_ms_i;`
- `:136`, the banner's sentence.

The selection stamp (`:1299-1302`) stays: it closes the window between the round's selection
and its first job. The window check (`:1099-1101`), the stamps' storage and their valid bit
`ctr_sent_r` are #232's. "Send" is the engine's retirement of the job (`uns_done_i`), which
is the TX arbiter's grant of the frame. Two choices are graded by their own controls:
- The stamp follows a waiting job, rather than being written at the send alone. Otherwise a
  change made during a wait longer than a second opens the window inside the round (TW2).
- It follows every job, not only the first. A later job of the round can be the one that
  waits (TW1).

## 3. Scope

Only GET_COUNTERS has this spacing logic. IDENTIFY_NOTIFICATION's spacing is a separate path
(`gen_ident`) that already measures each gap from the frame's departure (`uns_tx_busy_i`).
The other classes are not rate-limited. Nothing else is changed.

## 4. Original-round area: OOC 1x1 (#638's recipe)

Scratch parent at milan-fpga dev `6c22d3ca` with the c8, p2-p1, c10 and 232 patches.
Vivado 2026.1, `xc7a100t-fgg484-2`, the RTL elaboration as the integrated log,
`--integrated-clock` (20 ns). Every Vivado run held `flock /tmp/milan-vivado.lock`, and the
lane's other jobs were stopped while it ran.

| `KL_pp_shadow` standalone 1x1 | LUT | FF | RAMB36 / 18 | DSP |
|---|---:|---:|---:|---:|
| base `07b1469d` | 23,448 | 20,968 | 21 / 3 | 8 |
| head (HDL of `82e1664`) | 23,434 | 20,969 | 21 / 3 | 8 |
| delta | **-14** | **+1** | 0 | 0 |

Within the 40 LUT / 60 FF limit.
- **Attribution.** The `u_notify` row moves +41 LUT (all logic) and +1 FF. Five rows whose
  RTL is unchanged move -55 LUT: under the rebuilt hierarchy, attribution crosses
  boundaries.
- **Module alone.** As a diagnostic, `KL_aecp_notify` synthesized alone at the 1x1 binding:
  -34 LUT, +3 FF. The +3 FF is `em_ctr_ix_r`.
- **#638's gate** passes at base and at head, rc 0, "re-baseline recommended".
- **Logs.** No `Synth 8-7186` or `Synth 8-4445` diagnostic. The same 266 warnings at base and
  head.

## Original-round validation

All rc 0 unless stated; pinned Verilator 5.050; base `07b1469d` and head from `git archive`.

| Gate | Base `07b1469d` | Head |
|---|---|---|
| `./scripts/run_suites.sh` | 33 suites, 1,021,485 checks | 33 suites, 1,021,498 checks: `aecp_notify` 30 to 34 (TW), `pp_top` 10,416 to 10,425 (CS); every other suite's tally identical |
| `./scripts/lint_hdl.sh` | 41 of 41 | 41 of 41, the log identical |
| `make check`, `scripts/gen_matrix.py --check` | 1,131 links, 115 REQ rows, 94 matrix rows, 0 untested, 28 parameters | the same |
| `./syn/yosys/run.sh` | 42 tops, `all.v` parsed once | the same verdicts |

**Campaigns.** Every campaign that builds `KL_aecp_notify.sv`: the eight `tb/pp_top`
drivers, plus the `tb/pp_top` arms of `tb/adp_engine` and `tb/maap`. Each was run at base and
at head and compared arm by arm (verdict and each failing check). Notify ran at the final
head; the rest ran at commits whose inputs equal the final head's (between them only
`notify_mutants.py` and Markdown differ).

| Driver (`--jobs`) | Base | Head | Records |
|---|---|---|---|
| `notify_mutants.py` (2) | 47 of 47 KILLED, 6 goldens PASS | 53 of 53 KILLED, 7 goldens PASS | 46 of 47 identical; `counter_limit_500ms` moves (below); six new controls |
| `ctr_mutants.py` (2) | control PASS, 17 of 17 KILLED | the same | 16 of 17 identical; `ctr-notify-one-window` moves (below) |
| `d3_mutants.py` (4) | 110 of 110 KILLED, 6 goldens PASS | the same | 116 of 116 identical |
| `aecp_mutants.py` (2) | 5 controls PASS, 55 KILLED | the same | 60 of 60 identical |
| `aecp_dispatch_mutants.py` (2) | 4 controls PASS, 40 KILLED | the same | 44 of 44 identical |
| `acmp_mutants.py` (2) | 19 of 19 KILLED, 3 goldens PASS | the same | 22 of 22 identical |
| `gsi_mutants.py` (2), `name_wr_mutant.py` | 20 detected; decode killed; goldens and restored PASS | the same | 22 and 3 identical |
| `tb/adp_engine/mutants.py` (2), `tb/maap/mutants.py` (2) | 2 + 41 and 3 + 29 PASS | the same | 43 and 32 identical |

Two records move with the fix. Both arms are still KILLED by a named check, and both rows are
updated in the `tb/pp_top` README.
- **`counter_limit_500ms`** (the limiter at 500 ms) goes from 12 failing checks to 7: ST2b x5,
  ST3 and ST3b. The limit now runs from a round's last send, so half a second leaves rounds
  75,504 clocks apart, six in ST2's five seconds, inside ST2's count bound. Its named check
  was ST2 and ST2b and is now ST2b alone. Section CS fails the same edit
  (`counter_limit_500ms_cs`).
- **`ctr-notify-one-window`** goes from 3 to 4: K15 x2, K16 and K17.
  - The interface's own stamp now follows its round's jobs, so STREAM_INPUT 0's window opens
    first.
  - Under this control, that selection restarts every window. AVB_INTERFACE 0 is held a
    further second, past K15's 1,300 ms and into K17.
- **Figures only.** Four other ctr arms quote K14's late push at 1,018 ms instead of 1,000
  (same checks). In the d3 and aecp_dispatch logs, an unbound `%d` (`d3_phases.hpp:2963`,
  `:2993`) prints garbage at base and at head alike.

**Tests and controls.**

| Check | `main` | Head | Controls that fail it |
|---|---|---|---|
| CS1 x3 (premise) | pass | pass | `registry_holds_15_cs` |
| CS2a (ST's phase) | pass, 99,994 | pass, 115,077 | `counter_limit_500ms_cs`, `registry_holds_15_cs` |
| CS2b (+30 clocks) | **FAIL**, 99,854 | pass, 115,070 | `counter_spacing_from_selection`, both above |
| CS2c (+95 clocks) | **FAIL**, 99,590 | pass, 115,077 | the same three |
| TW1 | **FAIL**, ms 3005 | pass, ms 3603 | `counter_spacing_from_selection_tw`, `counter_stamp_first_job_only` |
| TW2 | **FAIL**, ms 6508 | pass, ms 7507 | `counter_spacing_from_selection_tw`, `counter_stamp_at_send_only`, `counter_stamp_first_job_only` |

`counter_spacing_from_selection` is the assignment's control: it removes the new stamp line,
so the limit restarts at the round's selection.

**Parent consumer set** at milan-fpga dev `6c22d3ca` with the c8, p2-p1, c10 and 232 patches
(each `git apply --check` clean), processor at base and at head. All rc 0 at both, results
identical, except gate 15 at head (below).

| # | Gate | Result |
|---:|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | every ratchet held |
| 3, 3b, 4 | `check_rtl_source_lists.py` (and `--selftest`), `pp_srcs.py --check --selftest` | 108 files, 4 of 4 lists, processor 42/42 tops; self-test 50 of 50 |
| 5 | `check_port_contracts.py` | processor 1,759 ports at base and head; undocumented 111 <= 111 |
| 6, 7, 8 | `measure_naming.py --check`, `measure_test_evidence.py --check`, `docs_check.py` | 95 recorded; within ratchets; 0 findings |
| 9 | `xvlog_gate.py --check` (under the Vivado lock, nothing else of the lane running) | PASS, 2 findings == ratchet (the two #22 lines) |
| 10 | `sw/builder/test_builder.py` | Make 4.4.1: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11's mf48 tree) at both; Make 4.3 at head also leaves gate 1b's arm unexercised |
| 11 | `lint_rtl.py --check` | 90 <= 90 |
| 12, 13, 14 | `pp_shadow -j8`, `nvm_cosim lint`, `quick` | 606, 606, 646 and 311 checks, 0 failures; 315 of 315 |
| 15 | `milan_dp -j8 VERILATOR_JOBS=3` | base rc 0, every leg; head rc 2 with the four patches, rc 0 with the fifth (below) |
| 16 | `milan_dp_render -j8` | 65 + 245 checks, 0 failures; leg defects 5 of 5; all 107 result lines identical at base and head |

**Gate 15 and the one parent adoption line.** At head, with the four patches, the timed notify
leg fails `[NOTIFY-CRF] ...nor to A` (got 1, want 2), and `sim_pool` starts no further leg.
- **Cause.** A probe in a scratch copy of the bench shows the processor sent A's second push.
  The harness's `drain_tx` (`tb/verilator/milan_dp/sim_nxn.cpp`) returned after 48 bytes of
  it: its frame buffer is local to each call, and the section calls it in 10 ms windows, so
  the next call began mid-frame and dropped the rest.
- **Why only at head.** The head's round starts after the previous round's last send, about
  12 ms later here, and A's frame straddles a window edge.
- **The patch.** `parent-adoption-148-6c22d3ca.patch` makes `drain_tx` read a frame still on
  the trunk at its last cycle to its end, bounded at 2,048 cycles, with no state across
  calls.
- **With it.** Gate 15 passes at head (rc 0, every leg, render mutants 6 of 6, gmstep
  controls 6 of 6). Its leg lines are identical to base's but one, the bench's own reading of
  #148: `CRF row pushes to B 997 ms apart` at base and `1012 ms` at head. At base the
  patch changes nothing: every leg line is identical with and without it.

## Parent-visible list

- No port, parameter or register change: the parent's port gate counts 1,759 processor ports
  at base and head.
- One parent adoption line, `parent-adoption-148-6c22d3ca.patch` (gate 15's harness, above),
  applied after the four existing patches, which apply unchanged at dev `6c22d3ca`. Without
  it, gate 15 fails at this head because the harness drops a frame the processor sent.

## What remains

- **Finding outside #148, not fixed.** A parked expiry drained between two jobs of any round
  (a TIME_LIMITED expiry, or a failed CONTROLLER_AVAILABLE retry) corrupts the rest of the
  round. The single-shot DEREGISTER overwrites `em_kind_r`, `em_dt_r`, `em_di_r` and
  `em_arg*_r`, and the resumed round does not restore them. Every remaining controller then
  receives a DEREGISTER_UNSOLICITED_NOTIFICATION (descriptor 0000:0) instead of the round's
  notification. Reproduced at `main` and at the head with a scratch probe in
  `tb/aecp_notify` (the lane's handoff carries the probe and its logs). Filed as
  [processor #158](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/158); unchanged here.
- **Residual.** The stamp is taken at the frame's grant. A MAC that stalls a frame after its
  grant shortens the wire gap by that stall. The departure tap that would see the last byte is
  built only with `P-EN-IDENTIFY-NOTIFICATION`, and using it would be a top-level change.

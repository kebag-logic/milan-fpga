# [A532] HANDOFF: #148, counter-notification spacing measured from the send

Status: **REVIEW READY — round 1b amended complete.** Current head
`bed5f47785839800bb640d7c747f5435f84ab5a3` (README correction), after `4ed463b410b2f24ecaa215188ca22fe6d7cd7850`, the
`--no-ff` merge of processor `main` `ead80360` (PR #155) on top of `415a9fdda8808501d4ea5c8afa32125632f50a5b`
(the merge of `b0a74196`, PR #157). Round 1's REVIEW READY head was
`a369cddd29f0dac3ad7b076d8e5e903bf3c20dfb`.

The processor working tree is clean and unpushed. All required suites, builds and ten
campaigns pass at base and head, and parent gate 15 passes at the current head.
Interrupted runs without a final return code are replaced by complete passing reruns.
Final [REVIEW READY comment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/148#issuecomment-5988331719) posted for this head. The receipt is recorded in `evidence/round-1b/review-ready-receipt.json`.

## Round 1b (assignments: #148 comments 5985998608 and 5986055260)

One re-measure over the union of #148, #157 and #155, at base `ead80360` and head
`bed5f477`; compiled inputs are identical to `4ed463b4`. All required return codes are 0.

- `415a9fd`: `--no-ff` merge of `b0a74196` (PR #157), textually clean.
- `4ed463b`: `--no-ff` merge of `ead80360` (PR #155). One conflict, in
  `tb/pp_top/sim_main.cpp`'s `main()`: this lane's `--spacing-only` flag and #155's
  `--arm-queue-only` flag were declared on the same line, and both were added to the same
  `one_section` line. The union keeps both flags and lists both in `one_section`. `git diff ead80360 4ed463b`
  is exactly this lane's nine files, and `git diff 415a9fd 4ed463b` is exactly #155's twelve.

Results (base `ead80360` / head `4ed463b`, each from `git archive`, pinned Verilator 5.050):
- `aecp_mutants.py --jobs 2`: rc 0 at both; 6 controls PASS (`timer-defaults` among them), 61
  KILLED; 67 of 67 records identical.
- `notify_mutants.py --jobs 2`: rc 0 at both; base 47 of 47 KILLED with 6 goldens PASS, head 53
  of 53 with 7, as in round 1. 46 of the 47 shared arms fail the same checks (in
  `entry_seq_not_advanced`, ST2c counts other figures). `counter_limit_500ms` is 12 to 7 (ST2
  x5 dropped), as in round 1. The six new arms fail exactly the checks the README records.
- `./scripts/run_suites.sh`: rc 0 at both; 33 suites; base 1,021,627 checks, head 1,021,640.
  Only `aecp_notify` 30 to 34 (TW) and `pp_top` 10,435 to 10,444 (CS) move. That is the union:
  `main` moved 1,021,485 to 1,021,627 (#157 and #155), and this lane adds 13, as in round 1
  (1,021,485 to 1,021,498). `acmp_listener` 3,111 at both.
- `./scripts/lint_hdl.sh`: 41 LINT OK at both, logs byte-identical.
- `./syn/yosys/run.sh`: 42 tops, `all.v` parsed once; verdict lines identical; the logs differ
  only in `all.v` line numbers past `KL_aecp_notify`.
- `make check` and `gen_matrix.py --check`: outputs identical (1,136 links, 115 REQ rows with
  17 GAP, 94 matrix rows, 0 untested, 28 parameters).
- `tb/pp_top`'s six builds, re-run from the suite's binaries with their output kept
  (`run_suites.sh` discards it): vid 20, identify 178, line 231, timebase 56 and defaults
  (TD) 3 checks, output identical at both; TD reads 60,003 ms and 300,002 ms, 6 probes.
  Default build 9,947 to 9,956 checks (CS's 9). Only these lines move: CS (new: 115,077,
  115,070 and 115,077 clocks, as in round 1), ST2's and ST3's info lines (the same figures as
  round 1: 4 rounds each, closest 115,100/115,077 clocks; worst ACMP 249 to 485 clocks), and
  AQ's first coverage line, 8,280 to 8,283 arms (below). AQ's drive line and HZ's lines are
  identical.
- **AQ's arm count, the one figure that is not the plain union.** #155's README records
  "71,258,305 edges and 8,270 arms" for `--arm-queue-only` at the #639 head. At base
  `ead80360` the run gives exactly that; at head it gives 71,258,305 edges and **8,273** arms.
  In the full default run the counts are 8,280 at base and 8,283 at head. The other AQ
  figures are identical at both: 28 clocks with two faces held, 4,288 pass-through pushes in `--arm-queue-only` (4,291 in the full run), and none deep, full or dropped. AQ1 and AQ2 pass at both.
  - **Method.** A scratch copy of the bench (not in the tree) printed every arm the model
    issued and pushed, at base and head.
  - **Where the +3 come from.** All three are on face 2 (ADP). Every other face issues the
    same number of arms.
  - **Where the runs diverge.** At edge 2,489,836, right after U9c/U9d. From there the notify,
    monitor and listener faces' arms run exactly 1,800 clocks (18 ms) later at head.
  - **Why U9 ends later.** It pulses a counter, receives the round at both controllers, and
    pulses again. Its deferred update now leaves a second after the round's last send (the
    second controller's job), not a second after its selection. That is #148's rule, and
    the 18 ms is the same one-job gap the ctr arms show (K14's 1,000 to 1,018 ms).
  - **Why that moves ADP's count.** The F08.2 PRNG (`KL_pp_prng`) advances every cycle, so
    every later draw differs: `T-NOTIF-MONITOR` intervals and `T-ADP-DELAY`. ADP's
    re-advertise schedule in section V and after it takes three more advertise-timer
    arms. A second scratch run, with each check stamped with its edge, placed the first
    ADP difference inside V (GET_AVB_INFO / GET_AS_PATH and their triggers).
  - **Why it is left as is.** The README figure is stated for the #639 head, so it stays.
- `tb/aecp_notify`: default build 26 to 30 (TW), identify build 4 at both.
- Docs fix `bed5f47` (README section count and TD invocation): `notify_phases.hpp` holds seven sections at the
  union (ID, ID0, NP, ST, CS, RN and #157's TD). `main` said five, which #157's TD had already
  made stale; this lane's round 1 said six. `make check` and `gen_matrix --check` re-ran at
  `bed5f47`, output identical.

The current run's evidence is under `evidence/round-1b/`. `source-provenance.txt`
checks all 558 tracked files in each saved export against its recorded commit.
Every compiled input at `4ed463b` equals the final head's; only the README changed.
The interrupted runs remain in scratch under `logs/r1c-*`; their missing return codes
are not counted as passing. Their complete reruns use `logs/r1d-*` and `camp/r1d-*`.
ADP and MAAP accept the compiler through the environment, not a `--verilator`
option. Launches with that unsupported option exit 2 before any test. Corrected
full runs are under `logs/r1e-*` and `camp/r1e-*`; those are the required runs.
Independent campaigns and parent gate 15 ran concurrently. Compilation admission was
bounded to three jobs at once, with the pinned compiler and 16-way make; simulations
retained each campaign's `--jobs` concurrency. No synthesis run overlapped this batch. Peak service memory was 10.01 GiB within the 12 GiB cap.

Round 1b suite and build results (all return codes 0):

| Gate / build | Base `ead80360` | Head `bed5f477` (compiled inputs of `4ed463b`) |
|---|---:|---:|
| `scripts/run_suites.sh` | 33 suites; 1,021,627 checks | 33 suites; 1,021,640 checks |
| `scripts/lint_hdl.sh` | 41 LINT OK | 41 LINT OK; identical log |
| `syn/yosys/run.sh` | 42 tops | 42 tops; identical verdicts |
| `make check` / `gen_matrix.py --check` | 1,136 links; 115 REQ, 17 GAP; 94 matrix rows, 0 untested; 28 parameters | identical; repeated at the final head |
| `pp_top` default | 9,947 checks | 9,956 checks; CS +9 |
| `pp_top` vid | 20 | 20 |
| `pp_top` identify | 178 | 178 |
| `pp_top` line | 231 | 231 |
| `pp_top` timebase | 56 | 56 |
| `pp_top` timer defaults | 3; 6 probes | 3; 6 probes |
| `aecp_notify` default / identify | 26 / 4 | 30 / 4; TW +4 |
| `acmp_listener` | 3,111 | 3,111 |

The full 33-row suite union is `evidence/round-1b/suite-union.tsv`.

Round 1b campaign comparisons (all return codes 0):

| Campaign | Base `ead80360` | Head (`4ed463b` inputs) | Comparison |
|---|---|---|---|
| notify, jobs 2 | rc 0; 6 goldens, 47 KILLED | rc 0; 7 goldens, 53 KILLED | one changed shared failure count (`counter_limit_500ms`, 12 to 7), six new mutants and their golden |
| ctr, jobs 2 | rc 0; 1 control, 17 KILLED | rc 0; same | `ctr-notify-one-window`, 3 to 4; four K14 messages, 1,000 to 1,018 ms |
| aecp, jobs 2 | rc 0; 6 controls, 61 KILLED | rc 0; same | all 67 records agree; includes TD and HZ |
| acmp, jobs 2 | rc 0; 4 goldens, 33 KILLED | rc 0; same | all 37 records and failing-check lines agree; includes nine AQ and five listener arms |
| name write | rc 0; golden, restored and decode arm PASS | rc 0; same | all 3 records agree |
| AECP dispatch, jobs 4 | rc 0; 4 controls, 40 KILLED | rc 0; same | all 44 result records identical; two D3C printf messages have unbound numeric arguments |
| D3, jobs 8 | rc 0; 6 controls, 110 KILLED | rc 0; same | all 116 keyed records agree, except unbound final integers in nine D3C3/D3C4 diagnostic messages |
| GSI, jobs 2 | rc 0; golden, restored, 20 detected | rc 0; same | all 22 result records identical |
| ADP, jobs 2 | rc 0; 2 controls, 41 KILLED | rc 0; same | all 43 driver records and failing-check lines identical |
| MAAP, jobs 2 | rc 0; 3 controls, 29 KILLED | rc 0; same | all 32 driver records and failing-check lines identical |

The docs agree: 06 section 7 preserves the one-second limit from the last send and
#232's storage; 09 section 8.3 and the README retain TD's real timeout defaults and
HZ's full hazard coverage. CS's shifted phases and TW's held jobs remain unchanged.
The README section-count correction at `bed5f47` is the only post-merge fix.
`make -j16 check` and `gen_matrix.py --check` at that exact head both return 0.

Parent gate 15: all five patches reversed and reapplied in the required order
(c8, p2-p1, c10, 232, 148), each `git apply --check` passing; the resulting working
diff is byte-identical. The scratch parent remains at `6c22d3ca`, with its processor
pin set to `bed5f477` in the index only. The complete gate passes at this pin, rc 0 in 3,945.31 s (`make -j16`,
`VERILATOR_JOBS=3`, `SIM_JOBS=2`): every simulation leg, render controls 6 of 6 and
gmstep controls 6 of 6. All 11,466 check, info and verdict lines match the original accepted head exactly; the leg-summary diff is empty. The earlier interrupted union run reached all
simulation legs before interruption during the render controls. Neither the parent nor its patches have been committed or pushed.

| Current parent consumer gate | Parent / processor pin | Result |
|---|---|---|
| Gate 15, full `milan_dp` | `6c22d3ca` / `bed5f477`, five patches applied in order | rc 0; 3,945.31 s; all simulation legs; render 6/6; gmstep 6/6; all 11,466 check/info/verdict lines identical to original accepted head |

`evidence/round-1b/raw-file-manifest.tsv` records SHA-256 and byte sizes for 1,082
raw files. Large logs and generated products remain in scratch; every output artifact
is at most 200,000 bytes. `evidence/vivado/raw-file-manifest.tsv` also verifies the
14 retained original OOC files against their recorded hashes and sizes.

The OOC 1x1 result below is the original #148 before/after measurement, retained
under the targeted round-1b re-measure assignment; it is not a new synthesis of the
merged main changes. `KL_aecp_notify` is byte-identical to the original measured head.

- Processor: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch
  `pp148-notify-spacing` from `main` `07b1469d`. Not pushed.
- Assignment: processor #148 comment 5982500256. TAKEN posted as comment 5982507671; REVIEW READY posted as comment 5985981334.
- Reviewers: [R476] (internal) and [R477] (external).

| Commit | Item |
|---|---|
| `abbe55b` | 1, red first: `tb/pp_top` section CS and `tb/aecp_notify` section TW (fail on `main`'s RTL) |
| `82e1664` | 2, the fix: `KL_aecp_notify` holds a GET_COUNTERS stamp at the clock while its job waits; 06 section 7 |
| `5f458aa` | the four planted controls in `notify_mutants.py`; TW prints its send figures; ST's comment drops the selection stamp |
| `221fd63` | the records: both READMEs, 09 section 8.4; `counter_limit_500ms`'s named check becomes ST2b alone (section 7) |
| `a369cdd` | two more controls for CS1 and CS2a; the ctr campaign's record at the head |

**Acceptance (#148).**
1. The spacing is measured from send to send. Every GET_COUNTERS job's send moves its
   descriptor's stamp, so a round starts at least the bound after the previous round's
   last send. CS grades every row on the wire at #148's shifted timing; TW grades a job
   held 600 ms and 1.5 s for the TX slot.
2. CS2b, CS2c, TW1 and TW2 fail on today's RTL. `counter_spacing_from_selection` (and its TW
   twin), which restarts the spacing at selection, fails them at the head.
3. Every processor suite and campaign is green at base and head. Two campaign records move
   with the fix, each still KILLED (section 7). The parent set passes with one new adoption
   line for a harness defect in gate 15 (section 8).
- **No STOP.** No port, parameter or register change. The OOC 1x1 delta is -14 LUT and
  +1 FF (section 5).

## 1. Red run (at `abbe55b`, `main`'s RTL)

`tb/aecp_notify` `make`: rc 2.
```
FAIL: TW1: ... whose last job waited for the TX slot until ms 2600 ... next round at ms 3005, want 3600 to 3608
FAIL: TW2: ... waited for the TX slot until ms 6500, goes out a second after the round's last send at ms 6504: next round at ms 6508, want 7504 to 7512
[build default] 30 checks, 2 failures
```
`tb/pp_top` `--spacing-only`: rc 1.
```
[i] CS2a: churn 0 clocks after ST's phase, closest rounds 99994 clocks apart (row 15, descriptor 0006:0)
FAIL: CS2b: churn started 30 clocks after ST's phase ... closest 99854 clocks (row 0, descriptor 0006:0), want at least 99900
FAIL: CS2c: churn started 95 clocks after ST's phase ... closest 99590 clocks (row 0, descriptor 0005:1), want at least 99900
CS: 9 checks, 2 failures
```
Logs: `evidence/red-abbe55b-*.log`. Phase sweep at `main` (`evidence/base-07b1469d-cs-phase-sweep.txt`):
starts 27 to 98 clocks after ST's phase (of every 100) fall below 99,900 clocks
(99,854 at 27..62; 99,613 down to 99,587 at 63..98); 0..26 and 99 pass.

## 2. Change (`82e1664`; line numbers at the head, whose HDL is `82e1664`'s)

`hdl/aecp/KL_aecp_notify.sv`, +9 -1:
- `:469` `em_ctr_ix_r` (`CTX_W_C` bits, 3 at 1x1): the claimed GET_COUNTERS round's
  descriptor slot. `:1043` resets it with the other `em_*` registers.
- `:1297` latches `pick_ctr_ix_w` when the round is claimed (`N_IDLE`, beside the existing
  selection stamp).
- `:1438-1443`, `N_EMIT_WAIT`:
  `if (em_kind_r == PP_UNS_CTRS_C) ctr_last_r[em_ctr_ix_r] <= now_ms_i;`
  While a GET_COUNTERS job waits for the engine and the TX slot, its descriptor's stamp
  follows the clock; in the cycle the engine retires the job (`uns_done_i`, the TX arbiter's
  grant of its frame) it takes that send's ms and then holds it. Every job of the round does
  this, so the stamp ends at the round's last send, and the existing window
  (`:1099-1101`, `now_ms_i - ctr_last_r[c] >= 1000`) opens a second after it.
- `:136` the banner's sentence: "their one-second limit runs from a round's last send".

Kept as they were: #232's storage (the stamps in flops without reset, `ctr_sent_r` as their
valid bit), the selection stamp (`:1299-1302`, which closes the window between a round's
selection and its first job), the window check, every port, parameter and register. The
selection stamp's comment is unchanged because `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch`
uses it as context; every campaign patch into this file still applies (`git apply --check`).
`docs/architecture/06_aecp_engine.md` section 7 says the same in one sentence.

Why the stamp follows a waiting job rather than being written at its send alone: a change
made while a job waits more than a second would otherwise open the window inside the round
and go out right after it (TW2; control `counter_stamp_at_send_only`). Why every job and not
only the first: each controller's notifications must be a second apart, and a later job of a
round can be the one that waits (TW1; control `counter_stamp_first_job_only`).

"Send" is the engine's retirement of the job, which is the TX arbiter's grant of the frame
(`KL_aecp_engine` `uns_done_o`). Its last byte follows a frame's serialization later; the
departure tap the identify sequencer uses (`uns_tx_busy_i`) is built only with
`P-EN-IDENTIFY-NOTIFICATION`, so measuring counters from the last byte would need a top-level
change, which this lane may not make. A MAC that stalls a frame after its grant can shorten
the wire gap by that stall; nothing in this lane's benches stalls the MAC during a counter
round (residual, recorded here only).

## 3. Tests and their failing mutants

| Check | Where | What it grades | At `main` (red, `abbe55b`) | At head |
|---|---|---|---|---|
| CS1 x3 | `tb/pp_top` `--spacing-only`, `notify_phases.hpp` `CounterSpacingPhase` | premise: sixteen controllers register | pass | pass |
| CS2a | same | ST's churn at ST's phase: every row's rounds of each descriptor >= 99,900 clocks apart, >= 3 rounds each | pass, 99,994 | pass, 115,077 |
| CS2b | same | the churn 30 clocks later (#148's shifted timing) | **FAIL, 99,854** (row 0, STREAM_OUTPUT 0) | pass, 115,070 |
| CS2c | same | the churn 95 clocks later | **FAIL, 99,590** (row 0, STREAM_INPUT 1) | pass, 115,077 |
| TW1 | `tb/aecp_notify` (default build) | a round whose last job waits 600 ms for the TX slot: the next round a second after that send | **FAIL, ms 3005** (want 3600..3608) | pass, ms 3603 |
| TW2 | same | a change made while a job waits 1.5 s: the next round a second after the round's last send | **FAIL, ms 6508** (want 7504..7512) | pass, ms 7507 |

Source locations at `bed5f477`: CS is `tb/pp_top/notify_phases.hpp:1303`, its three
starts are at `:1663`; TW is `tb/aecp_notify/sim_main.cpp:468`; the six controls
are in `tb/pp_top/notify_mutants.py:307`.

Planted controls (`tb/pp_top/notify_mutants.py`, new tuple `COUNTER_SPACING`), each KILLED
at head with every named check failing:

| Control | Planted | Suite | Failing checks |
|---|---|---|---|
| `counter_spacing_from_selection` | the `N_EMIT_WAIT` stamp removed: the limit restarts at the round's selection (`main`'s rule, the assignment's mutant) | `--spacing-only` | 2: CS2b, CS2c |
| `counter_spacing_from_selection_tw` | the same edit | `tb/aecp_notify` `make run` | 2: TW1 (ms 3005), TW2 (ms 6508) |
| `counter_stamp_at_send_only` | the stamp written at the job's retirement alone (`&& core_done_w`) | `tb/aecp_notify` | 1: TW2 (ms 6508) |
| `counter_stamp_first_job_only` | the stamp follows only row 0's job (`&& (em_ix_r == '0)`) | `tb/aecp_notify` | 2: TW1 (ms 3007), TW2 (ms 7503) |
| `counter_limit_500ms_cs` (`a369cdd`) | `counter_limit_500ms`'s edit (the limiter at 500 ms) | `--spacing-only` | 3: CS2a, CS2b, CS2c (75,504 clocks at each start) |
| `registry_holds_15_cs` (`a369cdd`) | `registry_holds_15`'s edit (the last row never claimed) | `--spacing-only` | 6: CS1 x3 (15 of 16), CS2a, CS2b, CS2c (row 15 receives no round) |

So every new check has a control that fails it: CS1 (`registry_holds_15_cs`), CS2a
(`counter_limit_500ms_cs`, `registry_holds_15_cs`), CS2b and CS2c (all three CS controls),
TW1 and TW2. TW's two REGISTERs and CS's restore premise are the benches' existing helper
checks ("registry accepts controller tuple", "notify bench: blank NVM, both restore walks
reach done"), called again.

The phase sweep behind the choice of CS's starts (a scratch copy of the bench, not in the
tree): at `main` every start 27..98 clocks after ST's phase (of every 100) falls below the
bound, and with the fix every start 0..199 leaves at least 115,036 clocks
(`evidence/base-07b1469d-cs-phase-sweep.txt`, `evidence/candidate-fix-cs-phase-sweep.txt`).

## 4. Scope: other notification kinds

Only GET_COUNTERS (`PP_UNS_CTRS_C`) has this spacing logic. The throttle state
(`ctr_dirty_r`, `ctr_pend_r`, `ctr_sent_r`, `ctr_last_r` and the window at `:1099-1101`) is read
and written for the counter class alone. The other kinds do not share it:
- IDENTIFY_NOTIFICATION (`gen_ident`, `:769-930`) has its own spacing, T-IDENT-BURST and
  T-IDENT-REARM, on a separate code path that already measures every gap from the frame's
  departure (`dep_w` on `uns_tx_busy_i`), graded by `tb/pp_top` ID and `tb/aecp_notify` FT.
- The command-class queue, lock, map, AVB_INFO, AS_PATH, STREAM_INFO and the targeted
  DEREGISTER are not rate-limited: they coalesce per class or descriptor and go out when the
  walk picks them (06 section 7: "No GET_COUNTERS rate limit applies to GET_STREAM_INFO").
Nothing else is fixed in this lane, and there is nothing of the same kind to list.

**Finding outside #148 (not fixed; filed as processor #158).** A parked expiry drained
between two jobs of any round corrupts the rest of that round. `N_IDLE` drains a TIME_LIMITED
expiry or a failed CONTROLLER_AVAILABLE retry (`pd_any_w`) before the next job, and the
single-shot DEREGISTER then overwrites `em_kind_r`, `em_dt_r`, `em_di_r` and `em_arg*_r`
(`:1252-1264`). On resume (`em_active_r`, `:1311-1313`) they are not restored, so every
remaining controller of the round receives a DEREGISTER_UNSOLICITED_NOTIFICATION (kind 0,
descriptor 0000:0) instead of the round's notification, and misses that notification.
Reproduced at `main` and at head with a probe in a scratch copy of `tb/aecp_notify`
(`evidence/probe-dereg-mid-round.diff` and its two logs): job 1 GET_COUNTERS 0009:0 to C;
C's registration expires; C gets its DEREGISTER (correct); D, the round's next row, gets
kind 0, descriptor 0000:0. #148's stamp follows `em_kind_r`, so such a corrupted round's
remaining jobs do not move the counter stamp either.

## 5. Original-round OOC 1x1 before/after (#638's recipe)

Scratch parent `$VALIDATION_STORAGE/pp148-a532/parent` (never committed or pushed): milan-fpga
dev `6c22d3ca` with the four patches (section 8), processor submodule at `07b1469d` for base
and `5f458aa` for head (the head's HDL is the final head's). Recipe
`docs/testing/PP_SHADOW_BASELINE_RECIPE.md` as it stands at that dev: the ax7101 export
(LiteX, `--build` omitted, firmware compiled), the RTL elaboration of the 1x1 script
(`synth_design -rtl -rtl_skip_mlo`) as the `--integrated-log`, then `pp_baseline.py
--integrated-clock` (20 ns) and `baseline_ooc.tcl`. Vivado 2026.1, `xc7a100t-fgg484-2`, every
run under `flock /tmp/milan-vivado.lock`, with this lane's campaigns stopped (SIGSTOP) from
20:25 to 21:23 so nothing heavy of the lane ran beside it. The two exports are identical but
for LiteX's timestamps and the order of its hierarchy comment (ROM hashes `23cc67ee...` and
`518b900c...` at both); the 21 bound parameters are identical.

| `KL_pp_shadow` standalone 1x1 | LUT (logic + memory) | FF | F7 / F8 | RAMB36 / 18 | DSP | WNS (estimate) |
|---|---:|---:|---:|---:|---:|---:|
| base `07b1469d` | 23,448 (21,174 + 2,274) | 20,968 | 335 / 10 | 21 / 3 | 8 | -3.136 ns |
| head `5f458aa` | 23,434 (21,160 + 2,274) | 20,969 | 335 / 10 | 21 / 3 | 8 | -3.162 ns |
| **delta** | **-14** | **+1** | 0 / 0 | 0 / 0 | 0 | |

**Within the STOP limits (40 LUT, 60 FF).** The hierarchy report's `u_notify` row moves
2,273 to 2,314 LUT (+41, all logic) and 1,255 to 1,256 FF. Five rows whose RTL did not change
move the other way by 55 LUT (`u_originator` -27, `u_timer` -16, `u_ucpu` -6, `u_ca_builder`
-4, `u_pp` glue -2): under the default rebuilt hierarchy the attribution moves across
boundaries. A diagnostic outside the recipe, `KL_aecp_notify` synthesized alone out of
context with the same directive, clock and the 1x1 binding read from the elaboration log
(16 controllers, 2 in, 2 out, 61 timer slots): base 2,508 LUT / 1,277 FF, head 2,474 / 1,280
(-34 LUT, +3 FF, the three bits of `em_ctr_ix_r`). The LUT figures move by tens either way
with the netlist; the flops are the change's exact cost.

#638's gate against its recorded A (`pp_resource_gate.py check ... --endpoint ooc-1x1`):
base rc 0, head rc 0, both "re-baseline recommended" (LUT -884 / -898, FF -4,377 / -4,376
against A). Every log has zero `Synth 8-7186` and `Synth 8-4445` diagnostics, five
`Synth 8-6901`, no error or critical warning, and the same 266 warnings at base and head.
Reports, gate output, the module diagnostic and the script: `evidence/vivado/`, with
`SHA256SUMS.txt` for the logs and checkpoints' inputs kept in the scratch directory.

## 6. Original-round processor suites (base / head)

Each from a `git archive` of the commit (base `07b1469d`, head `221fd63`, whose code is the
final head's: `221fd63..a369cdd` changes `notify_mutants.py` and one README only), pinned
Verilator 5.050 first on PATH; `make check` and `gen_matrix.py --check` in the tree at the
commit. All rc 0.

| Gate | Base `07b1469d` | Head |
|---|---|---|
| `./scripts/run_suites.sh` | 33 suites, 1,021,485 checks, 0 failing | 33 suites, 1,021,498 checks, 0 failing; only `aecp_notify` 30 to 34 (TW: two REGISTERs, TW1, TW2) and `pp_top` 10,416 to 10,425 (CS: 3 restores, 3 CS1, CS2a-c) move |
| `./scripts/lint_hdl.sh` | 41 LINT OK | 41 LINT OK, log byte-identical |
| `make check` | 18 wavedrom blocks, 1,131 links, 115 REQ rows (17 GAP), 94 matrix rows, 0 untested, 28 parameters | the same (at `221fd63` and at `a369cdd`) |
| `python3 scripts/gen_matrix.py --check` | OK (94 rows, 0 untested) | the same |
| `./syn/yosys/run.sh` | 42 tops, `all.v` parsed once | the same verdict lines |

`tb/pp_top` output that moves with the fix (every check passes at both): ST2's info line
(rounds 5,5,5,4,4 to 4 each; closest 100,000/99,994 to 115,100/115,077 clocks) and ST3's
worst GET_RX_STATE latency (249 to 485 clocks, bound 50,001). `--counters-only` (K9-K17)
output is byte-identical.

## 7. Campaigns (base / head)

Every campaign that builds `KL_aecp_notify.sv`: the eight `tb/pp_top` drivers and the
`tb/pp_top` arms of `tb/adp_engine` and `tb/maap` (the other drivers build no file this lane
changes). Each from its commit's `git archive`, `TMPDIR` on disk, pinned Verilator 5.050.
"Head" is `a369cdd` for notify, `221fd63` for d3 and `5f458aa` for the rest; between them and
the final head only `notify_mutants.py` and Markdown differ, and none of those drivers reads
either. Records compared arm by arm (verdict, then each failing check with figures masked).

| Driver (`--jobs`) | Base `07b1469d` | Head | Records |
|---|---|---|---|
| `notify_mutants.py` (2) | rc 0: 47 of 47 KILLED, 6 goldens PASS | rc 0: 53 of 53 KILLED, 7 goldens PASS | 46 of 47 identical; `counter_limit_500ms` 12 to 7 (below); six new arms |
| `ctr_mutants.py` (2) | rc 0: control PASS, 17 of 17 KILLED | rc 0: the same | 16 of 17 identical; `ctr-notify-one-window` 3 to 4 (below); four arms' K14 message reads 1,018 ms for 1,000 |
| `d3_mutants.py` (4) | rc 0: 110 of 110 KILLED, 6 goldens PASS | rc 0: the same | 116 of 116 identical (seven arms' D3C3/D3C4 messages print the unbound `%d`'s garbage, here with a different sign) |
| `aecp_mutants.py` (2) | rc 0: 5 controls PASS, 55 KILLED | rc 0: the same | 60 of 60 identical |
| `aecp_dispatch_mutants.py` (2) | rc 0: 4 controls PASS, 40 KILLED | rc 0: the same | 44 of 44 identical (two arms' D3C3/D3C4 messages print an unbound `%d`, `d3_phases.hpp:2963` and `:2993`, a garbage figure at both) |
| `acmp_mutants.py` (2) | rc 0: 19 of 19 KILLED, 3 goldens PASS | rc 0: the same | 22 of 22 identical |
| `gsi_mutants.py` (2) | rc 0: 20 detected, golden and restored PASS | rc 0: the same | 22 of 22 identical |
| `name_wr_mutant.py` | rc 0: decode killed, golden and restored PASS | rc 0: the same | 3 of 3 identical |
| `tb/adp_engine/mutants.py` (2) | rc 0: 2 controls PASS, 41 KILLED | rc 0: the same | 43 of 43 identical |
| `tb/maap/mutants.py` (2) | rc 0: 3 controls PASS, 29 KILLED | rc 0: the same | 32 of 32 identical |

**The two records the fix moves** (both still KILLED by a named check; both recorded in the
`tb/pp_top` README):
- `counter_limit_500ms` (the limiter at 500 ms): base 12 (ST2 x5, ST2b x5, ST3, ST3b), head 7
  (ST2b x5, ST3, ST3b). The limit now runs from a round's last send, so half a second leaves
  rounds 75,504 clocks apart: six in ST2's five seconds, inside ST2's count bound. ST2 was one
  of its two named checks, so at `5f458aa` the arm SURVIVED (rc 1, the first head run);
  `221fd63` names ST2b alone. Section CS fails the same edit too (`counter_limit_500ms_cs`).
- `ctr-notify-one-window` (one emission starts every descriptor's window): base 3 (K15, K16,
  K17), head 4 (K15 x2, K16, K17). The interface's own stamp now follows its round's jobs, so
  STREAM_INPUT 0's window opens a few ms first, and its selection, which under this control
  restarts every window, holds AVB_INTERFACE 0 a further second, past K15's 1,300 ms and into
  K17 (2 pushes, not 1).

## 8. Original-round parent consumer set (17) at milan-fpga dev `6c22d3ca`

Scratch parent `$VALIDATION_STORAGE/pp148-a532/parent` (never committed or pushed): a clone of
kebag-logic/milan-fpga detached at `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`; submodules
`external` `efeb541a`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`
(each at its gitlink, from its `.gitmodules` URL) and `protocol-processor` cloned from this
lane's repository; its gitlink set in the index only (`git update-index --cacheinfo`),
`rev-parse --show-toplevel` checked before every git command in it (`switch.sh`). The four
patches, each `git apply --check` clean and then applied, in this order:

| Patch | sha256 |
|---|---|
| `parent-adoption-c8-bbf704ec.patch` | `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c` |
| `parent-adoption-p2-p1-1269cdaf.patch` | `d3034e89dba34862a0c8534472043212fd1f56412a90397997dcce3441613d84` |
| `parent-adoption-c10-1269cdaf.patch` | `55e62329f52e352bdd56b6d37bf2877aa952063f43221bb3f1d8583274ea34b9` |
| `parent-adoption-232-241f9184.patch` | `88ee5e9643a453f8c31dc76e5f8d57e8deec89bcbbf9d4a4a8ca005757b72560` |

The pinned Verilator 5.050 first on PATH; processor at base `07b1469d` and at the final head
`a369cdd`. GNU Make 4.3 (another lane's build, the earlier lanes' convention) was first on PATH
for gates 1-9, 11-16 and the head's gate 10. That build's directory was removed while this
lane ran, so the base's gate 10 and the five-patch gate 15 runs used the host's Make 4.4.1.
Gate 10 ran at the head with both makes, so base and head compare at 4.4.1. The scripts are
`pgates.sh` and `gate15.sh` in the scratch directory; every log is under
`$VALIDATION_STORAGE/pp148-a532/pgates/{base,head,head5,base5}`.

| # | Command | Base `07b1469d`: rc, s | Head `a369cdd`: rc, s | Result (identical at both unless stated) |
|---:|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | 0, 3 | 0, 4 | every ratchet held (long function 0 <= 0, multi-declarator 0 <= 0, ...) |
| 2 | `scripts/check_py_idiom.py` | 0, 6 | 0, 13 | every ratchet held (over-long line 0 <= 0, too many parameters 7 <= 7, ...) |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 0 | 108 files, 4 of 4 consumer lists; protocol-processor 42/42 tops, 0 recorded |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 0 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 0 | sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | 0 | 3,824 first-party ports, **protocol-processor 1,759** (no port change); undocumented 111 <= 111 |
| 6 | `scripts/measure_naming.py --check` | 0 | 0 | 95 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 0 | 72 <= 77, 10 <= 10 unseeded draw sites, 0 <= 0, 3 <= 3 |
| 8 | `scripts/docs_check.py` | 0 | 0 | 0 findings, 188 md + 984 scrubbed files |
| 9 | `flock /tmp/milan-vivado.lock scripts/xvlog_gate.py --check` | 0, 213 | 0, 261 | PASS, 2 findings == ratchet (the two #22 lines in `KL_pp_originator.sv` and `KL_pp_rx_validator.sv`); output identical but for the pinned sha. These are the final runs, made with nothing else of the lane running. A first pair (0, 163 and 0, 152) ran beside the builder test and the base heavy gates, with the same result |
| 10 | `sw/builder/test_builder.py` | 0, 1,157 (Make 4.4.1) | 0, 1,201 (Make 4.3); 0, 1,198 (Make 4.4.1) | 4.4.1: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, the mf48 tree) at both; 4.3: also gate 1b's `MAKEFLAGS += -e` arm, as in earlier lanes |
| 11 | `scripts/lint_rtl.py --check` | 0 | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0, 314 | 0, 434 | legs 606, 606, 646 and 311 checks, 0 failures |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0, 1 | 0, 1 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0, 32 | 0, 31 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0, 2,735 | **2**, 1,112 (four patches) | see below |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0, 800 | 0, 885 | two-stream leg 65 and shipping leg 245 checks, 0 failures; leg defects 5 of 5; all 107 check and info lines identical (the T30 laws' first-event delays among them, so the boot timing did not move) |

**Gate 15 at the head fails in the parent's harness, not in the processor.**
- **What fails.** Base, four patches: every leg passes, rc 0. That is the datapath harness
  236, notify 383, crflic 416, the three 4x4 legs 1,961 each, 8x8 3,746, prune 33, the
  shipping Alinx shape 233, aclk 193, render mutants 6 of 6 and gmstep controls 6 of 6.
  Head, four patches: one check fails, the notify leg's `[NOTIFY-CRF] ...nor to A`
  (got 1, want 2). `sim_pool` then starts no further leg, so eight legs and the two mutant
  steps never ran.
- **Why.** A probe in a scratch copy of the bench (`evidence/parent-gate15/`) shows the
  cause. The processor sent A's second push at t1 + 1,003.5 ms, but `drain_tx`
  (`tb/verilator/milan_dp/sim_nxn.cpp:893`) returned after 48 of its bytes. Its frame
  buffer is local to each call, and the section calls it in 10 ms windows. The next call
  began mid-frame, so the frame failed the EtherType test and was dropped.
  - At base the push left inside one window.
  - At head the round starts after the previous round's last send. That is about 12 ms
    later at this bench, so B's second push lands at t1 + 1,012 ms and A's straddles a
    window edge.
- **The fix.** `parent-adoption-148-6c22d3ca.patch` (sha256
  `bbd0301dc7e576f51f92d24c8d140eda0666f9c6699806649365110e7ecfea83`) makes `drain_tx` read a
  frame still on the trunk at its last cycle to its end, bounded at 2,048 more cycles. It
  carries no state across calls, because the bench has seven other trunk readers with
  buffers of their own. With it, the notify leg passes at head: A 2, B 2, 383 checks,
  0 failures.

**Gate 15 with the fifth patch** (`git apply --check` clean after the four; Make 4.4.1):
- **Head `a369cdd`:** rc 0 in 1,879 s, every leg and both mutant steps. Notify 383 checks with
  `[NOTIFY-CRF] ...nor to A = 0x2`, render mutants 6 of 6, gmstep controls 6 of 6.
- **Base `07b1469d`:** rc 0 in 1,855 s. Its leg lines are identical to the four-patch base
  run, so the patch changes nothing at base.
- **Head against base:** every leg line is identical but one, the bench's own reading of
  #148: `CRF row pushes to B 997 ms apart` at base, under a second, and `1012 ms apart` at
  head.
- **Light gates.** Gates 1-8, 3b and 11 re-ran at head with the five patches: all rc 0, every
  summary identical to base's.
- **For the manager.** The patch is a parent-side change, for the parent's own lane to adopt
  with this processor pin. Section 8's evidence is in `evidence/parent-gate15/`.

## 9. Scratch, evidence and what remains

- Scratch: `$VALIDATION_STORAGE/pp148-a532/` holds the base and head exports, campaign outputs
  (`camp/`), logs (`logs/`), the parent (`parent/`, five patches applied, processor at the
  head, nothing committed) and the measurement trees (`meas/`). Nothing there is in the tree.
- Output directory: this file, `PR-BODY.md`, `parent-adoption-148-6c22d3ca.patch` and
  `evidence/` (red runs, phase sweeps, the DEREGISTER probe, Vivado reports with
  `SHA256SUMS.txt`, gate 15's probe and excerpts).
- **What remains.**
  - The DEREGISTER mid-round finding (section 4) is filed as
    [processor #158](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/158); it is outside this lane and remains unchanged.
  - The parent adoption patch.
  - The residual MAC-stall gap (section 2).
  - A pre-existing `%d` with no argument in `tb/pp_top/d3_phases.hpp:2963` and `:2993`
    prints garbage in two D3C messages (compiler warning at every build); not touched.

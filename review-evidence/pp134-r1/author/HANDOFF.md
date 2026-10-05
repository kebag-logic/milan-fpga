# [A538] HANDOFF — processor #134 (a withdrawal meets an LV registrar after a LeaveAll)

Status: REVIEW READY. Every gate ran at base and head, all rc 0: the processor suites, both
campaigns that build a changed file, and the parent consumer set of 17. Every record matches
base except the ones the assignment names: the new group, its control and two mutants, and the
counts that grow with them. No STOP: the arm shows the RTL behaving as Table 10-4 requires.
Every acceptance item of #134 is met, so PR-BODY.md says "Closes #134".

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Branch: `pp134-lv-leave`, base `main` `ead8036035affd53ef4b29979190f2f4f67084c0`
- Head: `5ab43bd98209ef3cde206b325c06f0e7405e1e86` (two commits, not pushed)
  - `68b0e615` Grade a withdrawal that meets an LV Listener registrar after a LeaveAll (#134)
  - `5ab43bd9` State the LV-case withdrawal behaviour in 10 section 6.5 (#134)
- Assignment: processor #134 comment 5988316116. Ruling: milan-fpga #608 comment 5885808887.
- TAKEN: processor #134 comment 5988324405
- REVIEW READY: processor #134 comment 5990196588 (head `5ab43bd9`)
- Changed files (`git diff --stat ead8036..5ab43bd`, 6 files, +235/-4):
  `docs/architecture/10_srp_engine.md` +19, `tb/srp_top/README.md` +58/-2,
  `tb/srp_top/mutants.py` +4/-1, `tb/srp_top/mutations/lv-never-ends.patch` (new, 10 lines),
  `tb/srp_top/mutations/lv-second-lv-ends.patch` (new, 25 lines), `tb/srp_top/sim_main.cpp`
  +121/-1. There is no file under `hdl/`: no RTL, port, parameter or register-map change.

## 1. The arm (file:line, at the head)

`tb/srp_top` already drives the Listener registrar (the talker-side FSM's registrar of the
Listener attribute) with a real T-MRP-LEAVE slot on a real `KL_pp_timer_service`
(1 ms = 40 clocks), so the arm is a new group there.

| What | Where |
|---|---|
| Group comment (clause, bench case) | `tb/srp_top/sim_main.cpp:773-783` |
| `LEAVE_TIME_MS = 5000`, `BENCH_GAP_CLOCKS = 56` (1.390 ms) | `tb/srp_top/sim_main.cpp:784-785` |
| `listener_rejoins()` (the bridge's re-join vectors) | `tb/srp_top/sim_main.cpp:788-795` |
| `check_withdrawal_meets_an_lv_registrar()`: 8 cases, S1-S3, one `LV_LEAVE` line each | `tb/srp_top/sim_main.cpp:796-871` |
| S1 / S2 / S3 checks | `tb/srp_top/sim_main.cpp:847-850`, `:855-859`, `:861-865` |
| ACTIVE edge (STREAM_START / STREAM_STOP) and `LISTENER_REG_CHANGE` counters, every clock, outside reset | `tb/srp_top/sim_main.cpp:354-362`, `:385-393`, reset `:459` |
| Group dispatch `RUN_ARGS=lvleave` | `tb/srp_top/sim_main.cpp:617`, accepted group list `:2843` |
| Campaign rows; coverage now requires S1-S3 | `tb/srp_top/mutants.py:153-155`, `:248` |
| Suite README section | `tb/srp_top/README.md:497-549` |
| Docs | `docs/architecture/10_srp_engine.md:548-565` (anchor `sec-10-lv-withdrawal`) |

Cases: an own and a peer LeaveAll, × Ready and ReadyFailed, × target source 0 and 7. Each
starts from `leaveall_setup()`: sources 0, 3 and 7 declared, each with a Listener registration
and ACTIVE, and sinks 0 and 7 registered.

- **Own LeaveAll.** Wait for the real leavealltimer and its accepted `sLA` (LV entry = the
  `sLA` clock). 1.390 ms after the LeaveAll MRPDU's last byte, the bridge sends one MRPDU:
  JoinIn for the other two sources' Listener registrations and for sink 0's Advertise and sink
  7's Failed, and `Lv` for the target.
- **Peer LeaveAll.** The bridge's LeaveAll on every MSRP type: Listener first, re-joining every
  registration but the target's, plus the Talker re-joins and a Domain LeaveAll-only vector.
  LV entry = the decoded Listener lane, with no own action. 1.390 ms later, its `Lv` for the
  target.
- Both: the `Lv` repeats at LeaveAll + 2500 ms.
- S1: the LeaveAll happened (one `sLA`, or the peer lane with no own action), the registrar is
  LV before each `Lv` and after it, and at LeaveAll + 4999 ms the registration is published,
  ACTIVE is high, and the case has had no ACTIVE edge and no `LISTENER_REG_CHANGE`.
- S2: at LeaveAll + 5002 ms, exactly one ACTIVE fall and one `LISTENER_REG_CHANGE`, each
  5000 or 5001 ms after the LeaveAll. The registrar is MT, `lstn_reg_state` is 0 and ACTIVE is
  low.
- S3: at LeaveAll + 7000 ms, still one STREAM_STOP, no STREAM_START, one
  `LISTENER_REG_CHANGE`.

Measured (`LV_LEAVE` lines; identical in the scratch trial, the campaign control and the head
suite):

| Cause | fp | Source | LeaveAll ms | `Lv` decoded by (ms) | Close ms | Leave time | STREAM_STOP / START |
|---|---|---|---:|---|---:|---:|---|
| own | Ready | 0 | 14200 | 14216, 16700 | 19200 | 5000 ms | 1 / 0 |
| own | Ready | 7 | 14200 | 14216, 16700 | 19200 | 5000 ms | 1 / 0 |
| own | ReadyFailed | 0 | 14200 | 14216, 16700 | 19200 | 5000 ms | 1 / 0 |
| own | ReadyFailed | 7 | 14200 | 14216, 16700 | 19200 | 5000 ms | 1 / 0 |
| peer | Ready | 0 | 705 | 711, 3205 | 5705 | 5000 ms | 1 / 0 |
| peer | Ready | 7 | 705 | 711, 3205 | 5705 | 5000 ms | 1 / 0 |
| peer | ReadyFailed | 0 | 705 | 711, 3205 | 5705 | 5000 ms | 1 / 0 |
| peer | ReadyFailed | 7 | 705 | 711, 3205 | 5705 | 5000 ms | 1 / 0 |

Group control: `24 checks: 24 PASS, 0 FAIL`.

## 2. Clause and leave-timer reading

- 802.1Q-2014 Table 10-4 (Registrar state table, p. 185): one row
  `rLv! || rLA! || txLA! || Re-declare!`. IN: "Start leavetimer", LV. LV: `-x-`. MT: `-x-`.
  Row `leavetimer!`: LV: "Lv", MT. Row `rNew!` / `rJoinIn! || rJoinMt!`: LV: "Stop
  leavetimer", IN.
- Milan v1.2 4.2.7.2.2 (Δ13): only `IN / rLv! -> (Start leavetimer) -> LV` becomes
  `IN / rLv! -> (Lv) -> MT`. The LV column is the standard's.
- So, as the ruling reads it: after a LeaveAll the registrar is LV, a further rLv! changes
  nothing, and the registration and the talker's licence end at leavetimer!.
- RTL, unchanged: `hdl/srp/KL_srp_talker_fsm.sv:729-740`. rLv on IN goes to MT (`:731`, Δ13);
  on LV nothing happens (`:733`, "table 10-4 rLv on LV is -x-"); the LeaveAll on IN goes to LV
  and arms the slot (`:735-736`); the expiry on LV goes to MT (`:739`). The arm deadline is
  `now_ms + LEAVE_MS_P` (`:716`).
- Leave-timer value: `LEAVE_MS_P` = 5000 (`KL_srp_talker_fsm.sv:86`, `KL_srp_top.sv:106`,
  "F08.1: 5000, coupled to Δ13"). `protocol_processor_top.sv` does not override it. F08.1
  (`docs/architecture/08_timing.md:40`): T-MRP-LEAVE 5000 ms (4500-7500), Milan Table 4.3.
- Milan v1.2 Table 4.3 (MRP Timer Tolerances): LeaveTime tolerance +50 %/-10 %, default
  5000 ms, min 4500 ms, max 7500 ms. Measured 5000 ms in all eight cases: the default, inside
  the range. S2 allows 5000 or 5001 ms, because the deadline counts from the clock the arm
  issues (one clock after LV entry, or a few clocks later behind lower-index sources), which
  can fall in the next ms. The timer service fires in the sweep of the ms where
  `now >= deadline` (`KL_pp_timer_service.sv:160`).

## 3. Mutants and their failing runs

Both patches are new, distinct from every existing patch, rows of `mutants.py`, and recorded
in `tb/srp_top/README.md` (section "A withdrawal that meets an LV registrar").

| Mutant | Edit (`hdl/srp/KL_srp_talker_fsm.sv`) | Campaign run at the head (`lvleave`) | Complete base suite, planted |
|---|---|---|---|
| `lv-second-lv-ends` | one flop per source: the first rLv in LV is let pass, the second ends the registration (cleared at each LV entry) | rc 2, 16 of 24 FAIL, tags S1,S2, KILLED (close at 2500 ms: the second `Lv`) | rc 0, 2200 of 2200 + storage 4 × 15: no existing check fails |
| `lv-never-ends` | an rLv in LV cancels the leave-timer slot | rc 2, 16 of 24 FAIL, tags S2,S3, KILLED (no close, 0 STREAM_STOP) | rc 0, 2200 of 2200 + storage 4 × 15: no existing check fails |

Failing lines (campaign receipts `lv-second-lv-ends.log`, `lv-never-ends.log`), e.g.:
`FAIL: S1: own LeaveAll fp=2 src=0: both Lvs meet LV, and the registration and ACTIVE stay until the leave timer expires`,
`FAIL: S2: own LeaveAll fp=2 src=0: the registration and ACTIVE close at the leave timer's expiry (2500 ms; Table 4.3 LeaveTime 5000 ms)`;
`FAIL: S2: ... (0 ms; ...)`, `FAIL: S3: own LeaveAll fp=2 src=0: STREAM_STOP counted exactly once (0), no STREAM_START (0)`.
Every S check fails under at least one mutant: S1 (first), S2 (both), S3 (second). The
campaign's coverage check requires S1-S3 and reads 83/83.

Cross-check, not campaign rows: the existing one-line forms of the same defects, run through
the group in a scratch copy of the head's `tb/srp_top` (byte-identical to the committed file):
`talker-strict-lv` 16 of 24 FAIL (S1,S2; close 14 ms / 5 ms after the LeaveAll, at the first
`Lv`), `talker-no-expiry` 16 of 24 FAIL (S2,S3; no close).

## 4. Suite table (base `ead80360` vs head `5ab43bd9`, the lane tree, pinned Verilator 5.050)

| Gate | Base | Head | Difference |
|---|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1531 s, 1,021,627 checks, 0 failing | rc 0, 1068 s, 1,021,651 checks, 0 failing | 2 lines: `srp_top (2200 ...)` -> `(2224 checks: 2224 PASS, 0 FAIL)` and the total (+24) |
| `scripts/lint_hdl.sh` | rc 0, 41 LINT OK | rc 0, 41 LINT OK | identical |
| `make check` | rc 0 | rc 0 | 1 line: `links: 1136` -> `1140` (the four new links); 41 mermaid + 18 wavedrom, 115 REQ, 94 rows, 28 parameters identical |
| `scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | rc 0 | identical |
| `syn/yosys/run.sh` | rc 0, 42 tops | rc 0 | identical |

## 5. Campaign table (the campaigns that build a changed file: both build `tb/srp_top/sim_main.cpp`)

| Campaign | Base | Head | Difference |
|---|---|---|---|
| `python3 tb/srp_top/mutants.py --jobs 6` | rc 0, 711 s, `128 checks: 128 PASS, 0 FAIL`, coverage 80/80 | rc 0, 692 s, `131 checks: 131 PASS, 0 FAIL`, coverage 83/83 | summary: + `control srp_top lvleave: rc=0 PASS`, + the two arms (above), the coverage and tally lines; every other line identical. Receipts: 122 of 122 base receipts identical after normalising scratch paths and build lines; 3 new |
| `python3 tb/srp_admission/mutants.py --jobs 3` | rc 0, 485 s, `12 checks: 12 PASS, 0 FAIL` | rc 0, 505 s, the same | summary identical. Its four full `srp-top` receipts each add the eight `LV_LEAVE` lines and 24 passing checks (2200 -> 2224, the same FAIL counts 0/90/205/105); the other 8 receipts identical |

## 6. Parent consumer table (17)

Scratch parent: `https://github.com/kebag-logic/milan-fpga.git` cloned to
`$VALIDATION_STORAGE/pp134-a538/parent`, detached at dev
`e617275074e370cec342af99b929e2588fc8d43f`; `gptp-processor` `5dce647a`, `external`
`efeb541a`, `third_party/verilog-axis` `48ff7a7e` (its pins). Each submodule's
`rev-parse --show-toplevel` was checked before git commands in it. The processor checkout was
fetched from the lane and set to base `ead80360`, then head `5ab43bd9`, with the gitlink
staged by `git update-index --cacheinfo` only. The four patches were applied in order with
`git apply --check` then `git apply`:

| Patch | sha256 |
|---|---|
| `parent-adoption-c8-bbf704ec.patch` | `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c` |
| `parent-adoption-p2-p1-1269cdaf.patch` | `d3034e89dba34862a0c8534472043212fd1f56412a90397997dcce3441613d84` |
| `parent-adoption-c10-1269cdaf.patch` | `55e62329f52e352bdd56b6d37bf2877aa952063f43221bb3f1d8583274ea34b9` |
| `parent-adoption-232-241f9184.patch` | `88ee5e9643a453f8c31dc76e5f8d57e8deec89bcbbf9d4a4a8ca005757b72560` |

Nothing was committed or pushed. Between the runs, the base run's 46 ignored build products
(45 in the parent, 1 `__pycache__` in the processor) were moved aside to
`$VALIDATION_STORAGE/pp134-a538/aside-base/`, not deleted, so the head run rebuilt from clean.
GNU Make 4.4.1, pinned Verilator 5.050 first on PATH, `MAKEFLAGS=-j16` in the environment for
both runs.

| # | Command | Base rc / s | Head rc / s | Result | Base vs head |
|---:|---|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 / 2 | 0 / 2 | every count 0 <= 0 (it scans `protocol-processor/tb/` C++: the new 76-line function, no cast, no multi-declarator) | identical |
| 2 | `scripts/check_py_idiom.py` | 0 / 5 | 0 / 5 | every ratchet held | 1 line: 199,505 -> 199,508 lines (`mutants.py` +4/-1) |
| 3 | `scripts/check_rtl_source_lists.py` | 0 / 1 | 0 / 1 | 108 files, 4 of 4 lists; processor 42/42 tops | identical |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 / 4 | 0 / 4 | 50 of 50 | identical |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 / 0 | 0 / 0 | 46 tracked sources derived, self-test passed | identical |
| 5 | `scripts/check_port_contracts.py` | 0 / 3 | 0 / 3 | 1,759 processor ports, 111 <= 111; 317 test-only hierarchical observations | identical |
| 6 | `scripts/measure_naming.py --check` | 0 / 0 | 0 / 0 | 95 recorded | identical |
| 7 | `scripts/measure_test_evidence.py --check` | 0 / 15 | 0 / 15 | 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 | identical |
| 8 | `scripts/docs_check.py` | 0 / 6 | 0 / 6 | 0 findings, 189 md + 988 files | identical |
| 9 | `scripts/xvlog_gate.py --check` (Vivado 2026.1 xvlog, under `/tmp/milan-vivado.lock`) | 0 / 142 | 0 / 140 | `PASS (2 finding(s) == ratchet; 0 hdl/, 2 pinned processors)`: `KL_pp_originator.sv:194`, `KL_pp_rx_validator.sv:383` | identical but the pin line (`protocol-processor@ead80360` / `@5ab43bd9`) |
| 10 | `sw/builder/test_builder.py` | 0 / 1386 | 0 / 1246 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the mf48 build tree is not on disk) | 27 of 27 verdict lines identical |
| 11 | `scripts/lint_rtl.py --check` | 0 / 9 | 0 / 9 | 90 <= 90 | identical |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 / 378 | 0 / 299 | legs 606, 606, 646, 311 checks, 0 failures | the same legs; 2168 `[PASS]`, 0 `[FAIL]` in each (the `-j8` log interleaves build lines, so not compared line by line) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 / 0 | 0 / 0 | | identical but two Verilator walltime lines |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 / 30 | 0 / 30 | `RESULT: PASS` | identical |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 / 1970 | 0 / 2016 | 9 benches `RESULT: PASS`, 4 render mutants caught, gmstep 104 checks | 11,512 of 11,512 verdict lines identical |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 / 763 | 0 / 770 | 65 and 245 checks, 0 failures | 111 of 111 verdict lines identical |
| 16b | `python3 tdm8_render_mutants.py --leg-defects` | 0 / 449 | 0 / 458 | 5 of 5 | identical |
| 17 | `scripts/check_sh_idiom.py` | 0 / 0 | 0 / 0 | every count held | identical |

No OOM kill in the unit (`memory.events` `oom_kill 0`).

## 7. Notes

- The assignment asks for "a mutant that ends the registration on the second `Lv`". The arm
  sends the peer's `Lv` twice while LV, so a defect that ends the registration on either `Lv`
  fails it. The planted `lv-second-lv-ends` is the literal reading: one `Lv` in LV is let
  pass, the second ends the registration. The other reading, the LeaveAll's rLA! as the first
  leave and the peer's `Lv` as the second, is `talker-strict-lv`, an existing patch; it fails
  the group too (16 checks, section 3). That was measured once, not added as a campaign row.
- Both new mutants survive every existing group (run through the complete base suite planted,
  2200 of 2200), so only this arm catches them.
- `/tmp` on this host is tmpfs, so campaign scratch was `TMPDIR=$VALIDATION_STORAGE/pp134-a538/tmpdir`.
- The parent's xvlog gate needs the shared Vivado lock. Other lanes' integrated Vivado runs
  held it for most of this lane, so gate 9 ran base and head in one hold, 09:34:17 to
  09:38:59 (`$VALIDATION_STORAGE/pp134-a538/bin/xvlog_both.sh`), with no other build of this
  lane running. It staged the gitlink at base, ran, staged head, ran. The scratch
  parent is left at head.
- Scratch, all outside the tree and the output directory: `$VALIDATION_STORAGE/pp134-a538/`
  (`base/`, `head/` processor logs and receipts; `pc-base/`, `pc-head/` parent consumer
  logs; `try/` the draft trials and planted full-suite runs; `std/` text extracts of the two
  standards; `parent/` the scratch parent).

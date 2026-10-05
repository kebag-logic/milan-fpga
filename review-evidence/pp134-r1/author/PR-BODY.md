[A538] Grade the talker stop when a withdrawal meets an LV Listener registrar after a LeaveAll

Closes #134

Branch `pp134-lv-leave`, two commits on `main` `ead80360`; head `5ab43bd9`. No RTL, port,
parameter or register-map change: only `tb/srp_top` and `docs/architecture/10_srp_engine.md`.

## The case

milan-fpga #608 cycle 22, ruled in its comment 5885808887: the DUT's own LeaveAll crossed the
wire 1.390 ms before the bridge's `Lv` for a stream whose listener had withdrawn. The Listener
registrar was already LV when the `Lv` arrived, and the talker streamed on through the 2 s hold.

802.1Q-2014 Table 10-4 puts `rLv! || rLA! || txLA! || Re-declare!` in one row: in IN, "Start
leavetimer" and LV; in LV, `-x-`. `leavetimer!` in LV is Lv and MT. Milan v1.2 4.2.7.2.2 (Δ13)
replaces only the IN cell (`IN / rLv! -> (Lv) -> MT`). The RTL already does this
(`hdl/srp/KL_srp_talker_fsm.sv:729-740`); nothing graded the close at the leave timer's expiry.

## What changes

- **The arm.** `tb/srp_top` group `lvleave` (`make RUN_ARGS=lvleave`), checks S1-S3, eight
  cases: an own and a peer LeaveAll, Ready and ReadyFailed, source 0 and 7. The own case
  waits for the real leavealltimer and its accepted `sLA`; 1.390 ms after the LeaveAll
  MRPDU's last byte, the bridge re-joins every other registration and sends `Lv` for the
  target. The peer case feeds the bridge's LeaveAll on every MSRP type (re-joining all but the
  target), then its `Lv` 1.390 ms later. In both, the `Lv` repeats 2.5 s in. The harness now
  counts ACTIVE edges (what the integrator's STREAM_START / STREAM_STOP counters count) and
  `LISTENER_REG_CHANGE` strobes on every clock.
  - S1: both `Lv`s meet LV; the registration (Ready or ReadyFailed) and ACTIVE stay, with no
    ACTIVE edge and no `LISTENER_REG_CHANGE`, up to the last ms before the timer can expire.
  - S2: they close at the leave timer's expiry, 5000 or 5001 ms after the LeaveAll (the
    deadline counts from the clock the arm issues).
  - S3: over the case, exactly one STREAM_STOP, no STREAM_START, one `LISTENER_REG_CHANGE`.
- **Leave-timer value.** `LEAVE_MS_P` = 5000 ms (F08.1 T-MRP-LEAVE; the processor top keeps the
  default). Milan v1.2 Table 4.3 LeaveTime: default 5000 ms, 4500-7500 ms. Measured 5000 ms
  from the LeaveAll to the close in all eight cases.
- **Mutants.** `tb/srp_top/mutations/lv-second-lv-ends.patch` (the registrar lets one `Lv` in
  LV pass and ends the registration on the second) and `lv-never-ends.patch` (an `Lv` in LV
  stops the leave timer, so the registration never ends). Both are rows of `mutants.py`, and
  the coverage check now requires S1-S3. Neither fails any check of the base suite (2200 of 2200
  each, run in scratch copies); each fails 16 of the group's 24 checks.
- **Docs.** `10_srp_engine.md` section 6.5, "A withdrawal that meets LV", states the behaviour
  with Table 10-4, Δ13's scope and Table 4.3. The suite README records the group, the
  measured values and both mutants.

## Validation

Pinned Verilator 5.050. Base `ead80360` and head `5ab43bd9`, the same tree and commands.

| Gate | Base | Head | Difference |
|---|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,021,627 checks, 0 failing | rc 0, 1,021,651 checks, 0 failing | srp_top 2200 -> 2224 (the group's 24); every other line identical |
| `scripts/lint_hdl.sh` | rc 0, 41 LINT OK | rc 0, 41 LINT OK | identical |
| `make check` | rc 0 | rc 0 | links 1136 -> 1140 (the new links); the rest identical |
| `scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | rc 0 | identical |
| `syn/yosys/run.sh` | rc 0, 42 tops | rc 0 | identical |
| `tb/srp_top/mutants.py --jobs 6` | rc 0, 128 of 128, coverage 80/80 | rc 0, 131 of 131, coverage 83/83 | + control `srp_top lvleave`, + the two arms (16 failures each: S1,S2 and S2,S3); 122 of 122 base receipts identical after path normalisation |
| `tb/srp_admission/mutants.py --jobs 3` | rc 0, 12 of 12 | rc 0, 12 of 12 | summary identical; its four full srp_top receipts add the eight `LV_LEAVE` lines and 24 passing checks, with the same failures |

The two older one-line forms of these defects (`talker-strict-lv`, `talker-no-expiry`) also fail
the group: 16 checks each.

### Parent consumers

milan-fpga dev `e6172750` with the c8, p2-p1, c10 and 232 adoption patches applied in that
order, the processor gitlink staged (`git update-index --cacheinfo`) at base `ead80360`, then
at head `5ab43bd9`. Nothing committed. The base run's ignored build products were moved
aside before the head run, so both built from clean.

| # | Gate | Base | Head | Difference |
|---:|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | rc 0 | rc 0 | identical (every count 0; the new function is 76 lines) |
| 2 | `scripts/check_py_idiom.py` | rc 0 | rc 0 | +3 lines (`mutants.py`) |
| 3 | `scripts/check_rtl_source_lists.py` (+ `--selftest`) | rc 0 | rc 0 | identical |
| 4 | `scripts/pp_srcs.py --check --selftest` | rc 0 | rc 0 | identical |
| 5 | `scripts/check_port_contracts.py` | rc 0 | rc 0 | identical |
| 6 | `scripts/measure_naming.py --check` | rc 0 | rc 0 | identical |
| 7 | `scripts/measure_test_evidence.py --check` | rc 0 | rc 0 | identical |
| 8 | `scripts/docs_check.py` | rc 0 | rc 0 | identical |
| 9 | `scripts/xvlog_gate.py --check` | rc 0 | rc 0 | identical but the pin line; 2 findings == ratchet, both in files this PR does not touch |
| 10 | `sw/builder/test_builder.py` | rc 0 | rc 0 | identical verdicts; ALL GATES PASS EXCEPT 1 NOT RUN (gate 11's mf48 build tree is not on this host) |
| 11 | `scripts/lint_rtl.py --check` | rc 0 | rc 0 | identical |
| 12 | `make -C tb/verilator/pp_shadow -j8` | rc 0 | rc 0 | the same four legs (606, 606, 646, 311 checks, 0 failures) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | rc 0 | rc 0 | identical but walltimes |
| 14 | `make -C tb/verilator/nvm_cosim quick` | rc 0 | rc 0 | identical |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | rc 0 | rc 0 | 11,512 of 11,512 verdict lines identical |
| 16 | `make -C tb/verilator/milan_dp_render -j8` (+ `tdm8_render_mutants.py --leg-defects`) | rc 0 | rc 0 | identical verdicts; 5 of 5 |
| 17 | `scripts/check_sh_idiom.py` | rc 0 | rc 0 | identical |

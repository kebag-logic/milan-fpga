# [A729] HANDOFF — processor issue #212 (SRP Listener: a Talker registered before the settle)

**Status: REVIEW READY at head `04856e48619866e08ccaf5ffc34cf1636d8c5b74`.** Every acceptance item
is met, so PR-BODY.md carries "Closes #212". The STOP condition was not met. Nothing was pushed.

- Repository: the processor repository, branch `212-srp-presettle-talker`. Before the first
  commit, `git remote get-url origin` was the processor repository and HEAD was `a9e84b66`.
- Base: processor main `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`.
- Head: `04856e48619866e08ccaf5ffc34cf1636d8c5b74`. There are nine commits, each with a one-line
  subject and no body or trailer (`receipts/records/processor-records.txt`).
- Where the gates ran:
  - The campaigns ran at code head `913214a`.
  - The full sweep, lint, yosys, elaboration guards and executed traceability ran at
    `0b5e988`.
  - `make check` ran at the head.
  - From `913214a` to the head, `hdl/` changed only in comments (one banner paragraph). `tb/`
    changed only in REQ-tag name strings and placement, one campaign arm's named check, and
    READMEs. From `0b5e988` to the head, only docs and READMEs changed. The records file
    shows these diffs.
- Posts on #212: TAKEN (issuecomment-6634869361) and REVIEW READY with the head (issuecomment-6642069818).
- STOP check: `hdl/top/protocol_processor_top.sv` is unchanged, so there is no top-level port or
  parameter change. There is no register-map change. Every RTL change is inside
  `KL_srp_listener_fsm`, and its new storage is sized by that module's existing `N_SINKS_P`.

## Design and clauses

**The defect.** The sink's registrar started MT at the A15 settle and registered only events
seen after it. Consider a Talker attribute registered on the port before the settle: the
talker's and the bridge's applicants sit in QA, and periodic transmission is off. Such an
attribute was applied only after the next LeaveAll made the talker re-declare, 10 to 15 s later.

The fix follows the assignment's suggested shape.

1. **Port Talker registrars.** There are N = `N_SINKS_P` (P-N-STREAM-IN) entries: the port's
   existing budget of Talker registrars, one per sink.
   - Each entry registers one Talker Advertise/Failed value, whether or not a sink is settled
     on it (802.1Q-2022 §10.7 and §10.7.8: a full participant keeps a registrar per value
     registered).
   - Each runs the sink registrar's own Table 10-4 with Δ13 (Milan v1.2 §4.2.7.2.2), on the
     matcher's exact {stream_id, DA, VLAN} (Milan v1.2 §5.3.8.9).
   - It ages on the LeaveAll lane of the type it holds and on the own LeaveAll. Its
     `LEAVE_MS_P` leavetimer (Milan v1.2 Table 4.3 LeaveTime) is compared wrap-safe on
     `now_ms_i`.
   - The priority is the sink registrar's: a registering event, then leavetimer!, then rLv,
     then LeaveAll.
   - A value whose VLAN field is not a 12-bit VID is never held.
   - The bound follows 802.1Q-2022 §35.2.7, which leaves the number of values held to the
     implementation. A value registered while all N entries are registered is not held, and
     keeps the old behaviour.
2. **The seed.** An A15 settle on a held value starts the sink's registrar in the entry's next
   state, so a LeaveAll or leavetimer! on the settle's own clock applies too.
   - It takes the type, latency and FailureInformation, and raises EVT_TK_REGISTERED and the
     declaration request at once (Milan v1.2 §5.3.8.5, §5.5.3.5.18 step 4).
   - An LV seed arms the sink's leave slot on the next clock with the entry's deadline, ahead
     of the pend queue, so registrar timing does not change. Until that arm issues, an expiry
     of the slot is the old registration's and is ignored.
   - The old registration's expiry on the settle's clock strobes nothing.
3. **A re-bind that settles before its old Leave went out.** Milan v1.2 §5.5.3.5.43 probes at
   once, so a re-bind can settle while the old stream's Lv is still owed. Issue #188 parked
   that Lv and made the new stream's New wait one more walk.
   - The two stream_ids are two attribute values, each with its own applicant and tx!
     (802.1Q-2022 §10.7.7, Table 10-3). So the walk whose tx! sends the parked Leave also
     applies the waiting New! and sends the New on its second pass, in the same MRPDU.
   - The exception: if another sink declares the new stream or holds its applicant, that
     group's applicant takes the request, as before.
   - A registrar indication of the sink on the walk's clock holds the walk one clock.
   - Effect: a re-bind declares within one T-MRP-JOIN of its settle (acceptance item 2).
4. **Rejected: a LeaveAll at the settle.** Table 10-5 issues sLA only from Active, and only
   leavealltimer! enters Active: either its random 10 to 15 s expiry (802.1Q-2022 §10.7.4.3,
   Milan Table 4.3) or a Flush! (§10.7.5.2). A settle is neither, and the peer's
   re-declaration would take more than one T-MRP-JOIN.

**What acceptance item 2's "REGISTERING_FAILED / FAILED counters" covers.** Milan v1.2 Tables
5.16 and 5.17 define no SRP counter. The rows therefore grade:
- the REGISTERING_FAILED flag (GET_RX_STATE, Tables 5.23 and 5.39);
- the FAILED registration (`tk_reg_state`);
- GET_STREAM_INFO's failure code and bridge;
- at the unit, the sink's latched failure code and system id.

## Changes (file:line at head, clause)

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `hdl/srp/KL_srp_listener_fsm.sv:28`, `:88` | banner: the port registrars and the seed; the walk that sends a parked Leave declares the settled stream | 802.1Q-2022 §10.7, §10.7.7, §10.7.8, §35.2.7 |
| 2 | `hdl/srp/KL_srp_listener_fsm.sv:478`, `:490` | storage: `PT_N_C` = `N_SINKS_P` entries `pt_*` (state, value, type, latency, FailureInformation, deadline); the seeded leave timer `sdl_*` | §35.2.7; Milan v1.2 Table 4.3 |
| 3 | `hdl/srp/KL_srp_listener_fsm.sv:592`, `:626` (`pt_match`), `:661` (`pt_next`) | match, allocation, and the entries' Table 10-4 + Δ13 next state | 802.1Q-2022 §10.7.8, Table 10-4; Milan v1.2 §4.2.7.2.2, §5.3.8.9 |
| 4 | `hdl/srp/KL_srp_listener_fsm.sv:689` (`pt_seed`) | the seed: the entry's next state at the settle | Milan v1.2 §5.3.8.5, §5.5.3.5.18 step 4 |
| 5 | `hdl/srp/KL_srp_listener_fsm.sv:1137` | the settle requests the declaration at once, of the seed's type | §5.3.8.5 |
| 6 | `hdl/srp/KL_srp_listener_fsm.sv:1412`, `:1344`, `:1435` | the sink registrar seeded (state, type, payloads, EVT_TK_REGISTERED, latency strobe, the old expiry silent); LV: the slot armed with the entry's deadline ahead of the pend queue | Table 10-4 timing unchanged; Table 4.3 |
| 7 | `hdl/srp/KL_srp_listener_fsm.sv:1444` (`pt_plane`), `:1452` (`pt_data`) | the entries' flops (state reset by Begin!; data written with a registration) | 802.1Q-2022 Table 10-4 Begin! |
| 8 | `hdl/srp/KL_srp_listener_fsm.sv:826` (`park_hold`), `:872`, `:1040` (`park_retire_declare`), `:1212` | the walk that sends a parked Leave applies the waiting New! and leaves the slot unmarked for its second pass; the hold on a same-clock indication | 802.1Q-2022 §10.7.7, Table 10-3; Milan v1.2 §5.5.3.5.43 |
| 9 | `hdl/srp/KL_srp_listener_fsm.sv:566` | the FailureInformation comparator's invariant includes a seeded candidate | — |
| 10 | `docs/architecture/10_srp_engine.md:41`, `:192`, `:222`, `:223`, `:259`, `:602`, `:665`, `:676`, `:753` | contract, state, storage rows and measured cost, F10.5 arcs, the owed-Leave row and paragraph, the new subsection "A Talker registered before the settle" (the bound `:778`, why no LeaveAll `:803`) | as above |
| 11 | `docs/architecture/02_interfaces.md:298`, `docs/architecture/05_acmp_engine.md:301`, `docs/00_MILAN_COMPLIANCE_REVIEW.md` REQ-ACMP-018 row | the class-C event, the A15 row, the requirement's realization | Milan v1.2 §5.3.8.5 |
| 12 | `tb/srp_stream_fsms/sim_main.cpp:179` | the harness's `now_ms_i` is settable (PS7 to PS9 move time) | — |
| 13 | `tb/srp_stream_fsms/sim_main.cpp:2542` to `:3030` | section PS, PS1 to PS15 | acceptance 1 to 3 |
| 14 | `tb/srp_stream_fsms/sim_main.cpp:1178`, `:1252`, `:1326` | RB1, RB4, RB6, RB7: the old Lv and the new New in one walk (design item 3) | 802.1Q-2022 Table 10-3 |
| 15 | `tb/srp_stream_fsms/sim_main.cpp:1101`, `:1106`, `:1763`, `:1792` | L9 registers eight other values first, so its late sink still starts MT; SH14 and SH15 withdraw the talker before the joiner settles. Each keeps its premise | — |
| 16 | `tb/pp_top/sim_main.cpp:10542`, `:10584`, `:10628`, `:10648`, `:10699` | AS7 one MRPDU; a vector-aware Listener lookup (value k = FirstValue + k, 802.1Q-2022 §35.2.2.8); a GET_STREAM_INFO helper; AS8; AS9 | acceptance 1, 2 |
| 17 | `tb/srp_top/mutants.py:281`; `tb/srp_top/mutations/` (19 new patches, `listener-retire-skips-group-mark` re-cut with its edit unchanged) | the PS arms; the coverage group PS1-PS15; `listener-park-never-retires`' walk arm names `WK12: push` | acceptance 5 |
| 18 | `tb/pp_top/acmp_mutants.py:352` | `presettle_seed_dropped`, `presettle_park_declares_next_walk`; `park_never_retires` names its renamed AS7 check | acceptance 5 |
| 19 | `tb/srp_stream_fsms/README.md:203`, `tb/srp_top/README.md:832` (and the #193 table), `tb/pp_top/README.md:2295`, `:2365` | sections, counts, controls | — |

## New checks (planted arm, failing words)

**Unit** (`tb/srp_stream_fsms`, section PS; the SRP campaign `tb/srp_top/mutants.py`). The full
run at `913214a` scored 246 of 247; the one UNPROVEN arm is described below the table. The
coverage check passed, 157 of 157:

| Check | Acceptance | Planted arm | Named failing words | Failing checks |
|---|---|---|---|---:|
| PS1 | 1 | `pt-seed-dropped` | `PS1:` | 22 |
| PS1 | 1 | `seed-no-registered-strobe` | `PS1: a Talker Advertise` | 17 |
| PS2 | 1 | `pt-never-holds` | `PS2:` | 22 |
| PS2 | 1 | `seed-type-advertise` | `PS2:` | 8 |
| PS3 | 2 | `pt-seed-dropped` | `PS3:` | 22 |
| PS4 | 2 | `seed-drops-failure-information` | `PS4:` | 5 |
| PS4, RB1 | 2 | `park-retire-declares-next-walk` | `PS4:`, `RB1:` | 5 |
| PS6 | 3 | `pt-rlv-ignored` | `PS6:` | 6 |
| PS7 | 3 | `pt-leavetimer-never-expires` | `PS7:` | 4 |
| PS7 | 3 | `pt-leaveall-ignored` | `PS7:` | 9 |
| PS7 | 3 | `pt-leaveall-any-lane` | `PS7: a LeaveAll on the other lanes` | 1 |
| PS8 | timing | `seed-lv-fresh-deadline` | `PS8:` | 2 |
| PS9 | timing | `seed-from-current-state` | `PS9:` | 2 |
| PS10 | exact match | `pt-match-ignores-da`; `pt-vid-high-bits-ignored` | `PS10:` | 1; 1 |
| PS11 | bound | `pt-allocation-overwrites-entry-0` | `PS11:` | 4 |
| PS13 | #193 | `park-retire-ignores-group` | `PS13:` | 1 |
| PS14 | hold | `park-retire-without-hold` | `PS14:` | 2 |
| PS15 | expiry | `seed-keeps-expiry-strobe`; `seed-lv-unguarded` | `PS15: the old registration`; `PS15: the leave slot` | 1; 1 |

PS5 and PS12 fail under `pt-seed-dropped` (22 failures in all). The campaign's coverage check
requires every PS tag to fail under a killed arm. For acceptance 3, removing the pre-settle path
would apply nothing and so leave the rows passing. Its rows are therefore killed by arms that
break that path's withdrawal handling instead: rLv, leavetimer! and LeaveAll.

**The one UNPROVEN arm, `listener-park-never-retires` (walk shapes, an issue #188 arm).** It was
caught: 34 failures in WK8, WK10 and WK12. It did not fail its named check,
`WK12: the listener walk pushes`. With design item 3, the parked sink's walk now declares the
third stream, carrying the parked stream_id, so the push count matches and the content check
`WK12: push N carries its sink's settled stream_id` fails instead. The named check was changed
to `WK12: push` (`0b5e988`) and the arm re-run: both its trials KILLED, controls PASS, 4 of 4
(`receipts/campaigns/srp-pnr-rerun-0b5e988/`).

**Processor** (`tb/pp_top`, section AC; `tb/pp_top/acmp_mutants.py`: 103 of 103 KILLED at
`913214a`, 8 goldens PASS):

| Check | Acceptance | Planted arm | Named failing words |
|---|---|---|---|
| AS8: a re-bind onto a declared Talker Failed. At the settle, before any MRPDU: FAILED, one TK_ATTR_REGISTERED, GET_RX_STATE REGISTERING_FAILED (flags 0x0042, byte-exact), and GET_STREAM_INFO failure code and bridge. Then the next MRPDU, at most 240 ms later with no LeaveAll: the old stream's Lv and New Asking Failed | 2 | `presettle_seed_dropped`; `presettle_park_declares_next_walk` | `AS8: a re-bind onto a stream whose Talker Failed`; `AS8: the next MRPDU` |
| AS9: a Talker declared before the first settle. Registered at the settle; Ready New at most 240 ms later, with no talker frame and no LeaveAll | 1 | `presettle_seed_dropped` | `AS9: a Talker Advertise registered before the sink's first settle` |
| AS7: one MRPDU carries the old Lv and the new New | 2 | `presettle_park_declares_next_walk`; `rebind_abandons_leave`; `park_never_retires` | `AS7: a rebind settled`; `AS7: a rebind settled`; `AS7: the MRPDU after it goes on with the new stream` |

**Counts that moved.** The new rows add failures under six issue #193 arms. They were
re-measured, and the `tb/srp_top/README.md` table now carries them (at main: 35, 14, 65, 13, 7
and 2):
- `listener-settle-compare-dropped` 40;
- `listener-handover-drops-state` 15;
- `listener-teardown-keeps-declaring` 74;
- `listener-group-order-reversed` 14;
- `listener-walk-ends-owing-a-transmit` 12;
- `listener-walk-done-before-second-pass` 3.

The 19 PS rows in the README match the full campaign exactly.

## Area (the processor's yosys flow)

The flow is sv2v, then yosys 0.66 `synth_xilinx -family xc7 -flatten`: the lowering of
`syn/yosys/run.sh` and its Xilinx regression flow (`receipts/area/`).

| Shape | LUT | INV | FF | RAM | CARRY4 |
|---|---|---|---|---|---|
| `KL_srp_top` 2 sources, 2 sinks (shipping) | 11,475 → 12,690 (+1,215) | 2,811 → 2,944 (+133) | 4,812 → 5,372 (+560) | 114 → 114 | 457 → 491 (+34) |
| `KL_srp_top` 8, 8 (default) | 23,046 → 27,399 (+4,353) | 3,483 → 4,411 (+928) | 9,236 → 11,376 (+2,140) | 179 → 179 | 506 → 588 (+82) |
| `KL_srp_listener_fsm` 2 sinks | 4,532 → 5,471 (+939) | 443 → 651 (+208) | 933 → 1,493 (+560) | 0 → 0 | 79 → 113 (+34) |
| `KL_srp_listener_fsm` 8 sinks | 9,839 → 15,026 (+5,187) | 1,509 → 2,363 (+854) | 2,963 → 5,103 (+2,140) | 32 → 32 | 103 → 185 (+82) |

- The flip-flop delta is exactly N × 263 + (1 + log2 N + 32).
- I also measured a variant with one shared deadline adder and no clear-at-allocation of the
  FailureInformation. It came within +22 LUT at 2x2 and -401 LUT at 8x8, so it was not taken
  (`receipts/area/opt-variant/`).
- No Vivado run was made. The parent's shipping-route slice budget must be re-measured at
  adoption (PR-BODY "Limits").

## Processor gate table

Every command ran unpiped, with its rc recorded, in a disposable clone. Tools:
- the pinned Verilator 5.050 for the sweep and the campaigns (Verilator 5.052 for the second
  lint);
- yosys 0.66;
- sv2v v0.0.13, the latest release that the processor CI installs.

| Gate | Head | Result | Receipt |
|---|---|---|---|
| `make check` | `04856e4` | rc 0 (40 s): req-tags 115 rows, 266 tags; AECP command self-test 231 of 231; ids, figures, links, matrices OK | `processor/head-04856e4/` |
| `make check` | `0b5e988` | rc 0 | `processor/head-0b5e988/` |
| `bash scripts/lint_hdl.sh` (Verilator 5.052; pinned 5.050) | `0b5e988` | rc 0 both: 41 modules LINT OK each | same |
| `./syn/yosys/run.sh` | `0b5e988` | rc 0: 42 tops, all.v parsed once; `KL_aecp_engine` Xilinx OK | same |
| `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | `0b5e988` | rc 0: 93 checks, 0 FAIL | same |
| `bash scripts/run_suites.sh` (REQ_TAG_LOG set, MAKEFLAGS=-j8) | `0b5e988` | rc 0: **1,030,959 checks, 0 failing**. pp_top 11,064 (main: 11,060); srp_stream_fsms 1,468 (1,435); srp_top 8,669 | same |
| `python3 scripts/check-req-tags.py --suites ... --evidence ...` | `0b5e988` | rc 0: 266 evidence lines, 14 suites | same |
| `bash scripts/run_suites.sh` | `913214a` | rc 0: 1,030,959 checks, 0 failing | `processor/code-head-913214a/` |
| SRP campaign `tb/srp_top/mutants.py --jobs 6` | `913214a` | rc 1, then resolved (UNPROVEN arm above): 246 of 247, coverage 157 of 157. Re-run of that arm at `0b5e988`: 4 of 4 | `campaigns/srp-913214a/`, `campaigns/srp-pnr-rerun-0b5e988/` |
| `tb/pp_top/acmp_mutants.py --jobs 4` | `913214a` | rc 0: 103 of 103 KILLED, goldens PASS | `campaigns/acmp-913214a/` |
| `aecp_mutants.py --jobs 4` | `913214a` | rc 0: 67 checks PASS | `campaigns/aecp-913214a/` |
| `gsi_mutants.py --jobs 4` | `913214a` | rc 0: 30 detected, golden and restored PASS | `campaigns/gsi-913214a/` |
| `ctr_mutants.py --jobs 4` | `913214a` | rc 0: 18 checks PASS | `campaigns/ctr-913214a/` |
| `name_wr_mutant.py` | `913214a` | rc 0: decode killed, golden and restored PASS | `campaigns/name-wr-913214a/` |
| `aecp_dispatch_mutants.py --jobs 4` | `913214a` | rc 0: 105 checks (5 controls, 100 arms KILLED); every count equals its README cell (100 of 100) | `campaigns/aecp-dispatch-913214a/` |
| `notify_mutants.py --jobs 4` | `913214a` | rc 0: 137 of 137 KILLED, goldens PASS | `campaigns/notify-913214a/` |
| `d3_mutants.py --jobs 4` | `913214a` | rc 0: 110 of 110 KILLED, goldens PASS | `campaigns/d3-913214a/` |

Not run: the elaboration-guard mutation campaign and the ADP, MAAP and AECP-commands
campaigns. They plant into modules this change does not touch and build no SRP listener. Their
suites run in the sweep.

## Scratch-parent consumer gate table

**The scratch parent.** It is a local clone of milan-fpga dev `604899c0`, on a local branch,
with the push URL `DISABLED-never-push`; it was never pushed (`receipts/records/parent-records.txt`).
- Gitlink commits:
  - `e1d49e27`: protocol-processor → `0b5e988`;
  - `220f0b73`: ROM digests for that pin, equal to main's (ltn `23cc67ee…`, ucode `49a993be…`);
  - `b71d561a`: protocol-processor → `04856e4`;
  - `d9ac431b`: its ROM digests, the same values.
- Submodules came from local clones holding their pinned commits. Every git command inside
  `protocol-processor` was preceded by a top-level identity check.
- Tools follow the parent's CI pins: Verilator 5.050, yosys 0.66, sv2v v0.0.12, a CPython
  3.12.3 venv of `ci/constraints-ci.txt`, and GoogleTest 1.14.0 with its headers on the system
  include path, as the distribution package installs them.

**At pin `0b5e988`.** Every rtl-fast job's run steps were run (yosys-tool only provisions
yosys), plus milan_dp. All rc 0 (`receipts/parent/pin-0b5e988/`):

| Consumer gate (rtl-fast job) | Command | Result |
|---|---|---|
| changes | `scripts/ci_scope.py --selftest`; classify the diff from `604899c0` | rc 0; `true` (RTL relevant) |
| verilator-lint | `scripts/lint_rtl.py --check --self-test --jobs 2`; `scripts/pp_srcs.py --check --selftest` | rc 0: 89 violations ≤ ratchet 89; rc 0 |
| bdd-conformance | `cd tests && behave --no-capture -f plain` | rc 0: 14 features, 508 scenarios, 2,330 steps passed |
| yosys-elaboration | `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow`; the OOC read-set steps; `ooc_selftest.py`; `guard_selftest.py`; `cache_selftest.py` | rc 0 each: baseline PASS, 75 refusal arms, 36 guard controls, cache OK |
| publication-census | `sw/mailbox/publication_census.py --check --selftest --jobs 2` | rc 0: 0 of 31 rules no arm proves |
| firmware-unit | `tally_selftest.py`; `fw_rv32_selftest.py --require-rv32`; `test_ctrl_firmware.py ... --shard 0/4`; `test_ctrl_nvm.py`; `fw_coverage.py --selftest`; `fw_coverage.py --check` | rc 0 each: 18 of 18; 17 checks; PASS; 435 tests over 5 shapes; 29 of 29; 30 files |
| firmware-control-mutants | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 3 --shard 1/4` | rc 0: PASS |
| firmware-aecp-mutants | the same, `--shard 2/4` | rc 0: PASS |
| **firmware-srp-mutants (the SRP campaigns)** | the same, `--jobs 2 --shard 3/4` | rc 0: PASS, 0 escaped |
| firmware-boundary | `ctrl_boundary.py --require-rv32 --selftest --without verilator` | rc 0: PASS |
| firmware-verilator | `ctrl_boundary.py --require-rv32 --selftest --only verilator` | rc 0: PASS |
| **milan_dp** | `make -C tb/verilator/milan_dp SIM_JOBS=2` (`-j2`) | rc 0: 12,075 `[ok]`, 1,301 `[PASS]`, 0 failures (`milan_dp.summary.txt`) |

**At the final pin `04856e4`** (only processor docs differ from `0b5e988`), in
`receipts/parent/pin-04856e4/`:
- changes: `true`;
- verilator-lint: rc 0, 89 ≤ 89; pp_srcs rc 0;
- bdd: rc 0, 508 scenarios;
- yosys-elaboration: rc 0, with the OOC read-set step, `ooc_selftest`, `guard_selftest` and
  `cache_selftest` each rc 0 (75 refusal arms, 36 guard controls, cache OK).

**Superseded first attempts** (`receipts/superseded/`):
- The first `ooc_selftest`/`guard_selftest` refused because the pin had no ROM digest rows yet.
  The parent's pin-bump step records them.
- The first SRP firmware shard escaped 40 arms on compile errors. This environment's
  GoogleTest headers were on `-I`, where `-Werror` turned the header's sign-compare warning
  into an error. Re-run with them on the system include path: PASS.
- The first census, and the first yosys and BDD runs, used sv2v v0.0.13 from the user PATH.
  The census refused it by name, and they were all re-run with the pinned v0.0.12.

Not run: the parent's Vivado resource gate (`syn/ooc/pp_resource_gate.py check`, a Vivado
route) and its docs workflow (`check_submodule_docs.py` and the SUBMODULES pin row, which an
adoption records).

## Findings for the manager

- The issue #230 walk-arm per-shape counts in `tb/srp_top/README.md` were already stale at
  main `a9e84b66`: the same arms measure the same counts at base and at this head. Examples:
  `wtsp-first-open-only` 5/8/11/29 at both, against the table's 4/6/8/20;
  `walk-ignores-leave-copy` 2/4/10/18 at both, against 1/2/5/9. They grew with later walk rows
  (WK12, WK13). I did not change them, as they are not this issue's
  (`receipts/campaigns/base-walk-arms/`).
- The shipping-route area: `KL_srp_top` 2x2 grows by +1,215 LUT and +560 FF under yosys. The
  parent's last recorded slice headroom was small, so a Vivado route at adoption decides.

## Process notes

- **Memory.** `memory.peak` of this unit reads 10.75 GB, over the 10 GB working limit, under
  the 12 GB cap.
  - Most of it was page cache. It happened before the governor reclaimed cache: when two
    pp_top builds and a 21-arm campaign overlapped (10.6 GB), and during the first sweep's
    pp_top builds (10.75 GB).
  - The highest anonymous-memory sample was 8.08 GB, during the chains' compile-heavy
    stretch.
  - Since 20:18 the governor also asks the kernel to reclaim cache above 9.0 GB
    (`memory.reclaim`).
  - Samples and the governor's log are in `receipts/records/memory/`.
- **Governor pauses.**
  - The first governor read memory.current and paused the SRP campaign for 19 min.
  - The second read anonymous memory at 7.5 GB and deadlocked on the stopped compilers' own
    memory, pausing both campaign chains for 24 min. It was retuned (8.5/6.5 GB) and the
    builds capped at 1 compile job, then 2.
  - No campaign driver counts wall time, and every result was read by verdict.
- **Restarted runs.**
  - The first ACMP start was stopped after 14 arms to split the campaigns into two chains.
    Its log is in `receipts/superseded/acmp-first-start/`.
  - The final-head gates first ran at `982e51b` and `c8baee8`. `make check` found the three
    REQ-tag placements, fixed in `c8baee8`. The run at `c8baee8` was stopped when `0b5e988`
    renamed an arm's check, and everything was re-run there. The `982e51b` logs are in
    `receipts/superseded/processor-982e51b/`.
- **Development mirror.** A development pp_top run lost its ROM images to this lane's own mirror
  sync mid-run. It was a development run only; the gate runs above are clean clones.

## Not done (by the assignment's rules)

- No push, no PR creation or edit, no merge or rebase.
- No edit of any comment. The only posts on #212 are TAKEN and REVIEW READY.
- No hardware or bench access, no flashing, no Vivado run. No sub-agents.

## Receipts

`receipts/INDEX.md`, and an `INDEX.md` in every directory, are generated from the files present
(`receipts/tools/receipt.py index`).
- Host paths are replaced by placeholders: `<lane>`, `<scratch>`, `<runs>`, `<gates>`,
  `<tools>`, `<tmp>`, `<parent>`, `<parent-source>`, `<lanes>`, `<toolchain>`, `<venv>`,
  `<home>`, `<out>`, `<mgmt>`.
- A file over 200 KB is listed with its size and full sha256 in a `RAW-RECORDS.txt` beside the
  copies.

| Directory | Holds |
|---|---|
| `records/` | `processor-records.txt` (origin, base, head, commits, diffs, no top-level change), `parent-records.txt`, `tool-versions.txt`, `memory/` |
| `processor/head-04856e4/`, `head-0b5e988/`, `code-head-913214a/` | the gates above, with cmd/log/rc/start/end each |
| `campaigns/` | one directory per campaign; `srp-ps-arms-working-tree/` (the 21 PS arms before the commits); `srp-pnr-rerun-0b5e988/`; `base-walk-arms/` (the drift finding) |
| `parent/pin-0b5e988/`, `parent/pin-04856e4/` | the consumer gates |
| `area/` | base, head, the delta, the variant |
| `superseded/` | the first attempts named above |
| `tools/` | the scripts that ran the gates, cut the patches and wrote the receipts |

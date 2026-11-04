[A729] SRP Listener: apply a Talker attribute registered before the sink's ACMP settle (issue #212)

## The defect

A Stream Input's Listener declared nothing for a Talker attribute that the port registered
before the sink's ACMP settle (CONNECT_TX success). The sink's registrar started MT at the A15
settle and saw only events after it. So Listener Ready, or Asking Failed for a Talker Failed,
came only after the next LeaveAll made the talker re-declare, 10 to 15 s late. This was seen on
the wire after power-on and on a re-bind to an already declared Talker Failed.

- Milan v1.2 §5.3.8.5: a settled, SRP-bound Stream Input with a matching registered Talker
  Advertise declares Listener Ready; Asking Failed is allowed for a Talker Failed.
- Milan v1.2 §5.5.3.5.18 step 4: on a successful PROBE_TX_RESPONSE the Listener starts the SRP
  reservation.
- IEEE 802.1Q-2022 §10.7 and §10.7.8: a full participant keeps a registrar per attribute value
  registered. Its state does not depend on when the application became interested.

## The design

Everything is inside `KL_srp_listener_fsm`. There is no top-level port, parameter or
register-map change: `hdl/top/protocol_processor_top.sv` is unchanged.

1. **Port Talker registrars.** There are N = `N_SINKS_P` (P-N-STREAM-IN) entries, the port's
   existing budget of Talker registrars (one per sink).
   - Each entry registers one Talker Advertise/Failed value, whether or not a sink is settled
     on it.
   - It runs the sink registrar's own Table 10-4 with Milan v1.2 §4.2.7.2.2 (rLv on IN is MT at
     once), on the exact {stream_id, DA, VLAN} (Milan v1.2 §5.3.8.9). It uses the LeaveAll lane
     of the type it holds and the own LeaveAll. Its `T-MRP-LEAVE` leavetimer (Milan v1.2 Table
     4.3) is compared on `now_ms_i`, with the sink registrar's priority.
   - The bound: 802.1Q-2022 §35.2.7 leaves the number of values held to the implementation. A
     value registered while all N entries are registered is not held. A sink that settles on
     it registers on the talker's next declaration, as before.
2. **The settle takes the registration.** An A15 settle on a held value starts the sink's
   registrar in the entry's state after the events of the settle's own clock.
   - It takes the type, latency and FailureInformation, raises EVT_TK_REGISTERED and requests
     the declaration at once.
   - So `tk_reg_state`, the failure code and bridge, GET_RX_STATE's REGISTERING_FAILED and the
     ACMP listener's SETTLED_RSV_OK all follow at the settle, and the next tx! sends the New.
   - An LV entry starts the sink LV, and the sink's leave slot is armed with the entry's
     deadline, so no registrar timing changes.
3. **A re-bind that settles before its old Leave went out.** Milan v1.2 §5.5.3.5.43 probes the
   new source at once. Issue #188 parks the owed Lv, and until now the new stream's New waited
   one more walk.
   - The two stream_ids are two attribute values, each with its own applicant and tx!
     (802.1Q-2022 §10.7.7, Table 10-3). So the walk that sends the parked Lv also applies the
     waiting New! and sends the New on its second pass, in the same MRPDU.
   - If another sink declares the new stream or holds its applicant, that group's applicant
     takes the request as before (issue #193).
4. **Not done: a LeaveAll at the settle.** Table 10-5 issues sLA only from Active, and only
   leavealltimer! enters Active: the timer's random 10 to 15 s expiry (§10.7.4.3, Milan Table
   4.3), or a Flush! (§10.7.5.2). A settle is neither, and the peer's re-declaration would take
   more than one T-MRP-JOIN.

## Acceptance

| Item | Met by |
|---|---|
| 1. A Talker Advertise or Failed registered before a sink settles is applied at the settle, with Ready / Asking Failed declared New within one join period | `tb/srp_stream_fsms` PS1 (Advertise) and PS2 (Failed): registered at the settle, New on the first tx! after it. `tb/pp_top` AS9: after a reset the talker's Advertise registers before the bind; the settle registers it, and Ready New follows at most 240 ms later with no talker frame and no LeaveAll |
| 2. A re-bind with the Talker declared: the same within one join period, with the failure state and code at once | PS3 (the same stream, before and after the old Lv), PS4 (another stream, its Talker Failed declared, the old Lv still owed: Lv and New Asking Failed in one tx!), PS5 (after the old Lv). AS8: FAILED, GET_RX_STATE REGISTERING_FAILED and GET_STREAM_INFO's failure code and bridge before any MRPDU; then the old Lv and New Asking Failed in the next MRPDU, at most 240 ms after the settle |
| 3. A Talker withdrawn before the settle (rLv, or a LeaveAll with no re-declaration) is not applied | PS6 (rLv, Advertise and Failed); PS7 (a received LeaveAll on its lane or the own LeaveAll, then T-MRP-LEAVE); PS9 (a settle on the leavetimer!'s own clock) |
| 4. The bound stays the existing per-port budget; no top-level or register-map change | N = `N_SINKS_P`; PS11 grades the bound; no top-level file changed |
| 5. Rows with a mutant failing them by name; every suite green; the parent consumer gate passes | 19 PS arms in the SRP campaign and two arms in the ACMP campaign, each failing its named check. For item 3 the arms break the pre-settle path's withdrawal handling (rLv, leavetimer!, LeaveAll), since removing the path would leave it passing. Every suite and campaign passes (below), and so does the scratch-parent consumer gate with this head as its gitlink |

## Changes

- `hdl/srp/KL_srp_listener_fsm.sv`:
  - the port registrars `pt_*` (`pt_match`, `pt_next`) and the seed (`pt_seed`);
  - the seeded sink registrar and its leave-slot arm (`sdl_*`);
  - the walk's one-pass declaration after a parked Leave (`park_hold`,
    `park_retire_declare`);
  - the banner and the comparator note.
- `docs/architecture/10_srp_engine.md`: contract, state, storage rows and measured cost, F10.5
  arcs, the owed-Leave rule, and a new subsection "A Talker registered before the settle".
- `docs/architecture/02_interfaces.md`, `05_acmp_engine.md` and
  `docs/00_MILAN_COMPLIANCE_REVIEW.md` (REQ-ACMP-018).
- `tb/srp_stream_fsms`:
  - section PS (PS1 to PS15) and a settable `now_ms_i`;
  - RB1, RB4, RB6 and RB7 expect the old Lv and the new New in one tick;
  - L9, SH14 and SH15 keep their premises (L9 fills the port registrars first; SH14 and SH15
    withdraw the talker before the joiner settles).
- `tb/pp_top`: AS8, AS9, AS7 (one MRPDU), a Listener lookup that reads value k of a vector
  as its FirstValue plus k (802.1Q-2022 §35.2.2.8), and a GET_STREAM_INFO helper.
- Campaigns:
  - `tb/srp_top/mutants.py` and 19 patches;
  - `tb/pp_top/acmp_mutants.py` (`presettle_seed_dropped`, `presettle_park_declares_next_walk`);
  - one patch re-cut with the same edit;
  - two named checks renamed where the behaviour moved them: `park_never_retires` (AS7) and the
    walk arm of `listener-park-never-retires` (`WK12: push`; the walk now declares the third
    stream, on the parked stream_id).
- READMEs:
  - the PS and AS rows and the new controls;
  - six issue #193 arm counts re-measured: the new rows add failures under them.

## Validation

- At `0b5e988`, the last code change before this head (only docs and READMEs differ since), in
  a disposable clone:
  - `bash scripts/run_suites.sh`: rc 0, 1,030,959 checks, 0 failing (pp_top 11,064, was
    11,060; srp_stream_fsms 1,468, was 1,435; srp_top 8,669);
  - the executed REQ-tag check: rc 0, 266 evidence lines;
  - `scripts/lint_hdl.sh` under Verilator 5.052 and the pinned 5.050: rc 0, 41 modules each;
  - `./syn/yosys/run.sh`: rc 0, 42 tops;
  - `tb/elab_guards/guards.py --frontend yosys`: rc 0, 93 checks.
- At this head: `make check` rc 0.
- Campaigns, at the code head, pinned Verilator 5.050:

  | Campaign | Result |
  |---|---|
  | SRP (`tb/srp_top/mutants.py`) | 246 of 247 with coverage 157 of 157. The one arm caught by other names (above) was re-named and re-run: 4 of 4 |
  | ACMP | 103 of 103 KILLED |
  | AECP | 67 PASS |
  | GSI | 30 detected |
  | CTR | 18 PASS |
  | name write | PASS |
  | AECP dispatch | 105 of 105; every README count cell unchanged |
  | notification | 137 of 137 |
  | D3 | 110 of 110 |

- Area, with sv2v then yosys 0.66 `synth_xilinx -family xc7 -flatten`, main against this head:

  | `KL_srp_top` shape | LUT | FF |
  |---|---|---|
  | 2 sources, 2 sinks | 11,475 → 12,690 (+1,215) | 4,812 → 5,372 (+560) |
  | 8 and 8 | 23,046 → 27,399 (+4,353) | 9,236 → 11,376 (+2,140) |

  No RAM changes. The flip-flops are N × 263 + (1 + log2 N + 32).

## Scratch-parent consumer gate

The scratch parent is milan-fpga dev `604899c0` with this head as the protocol-processor
gitlink, committed locally and never pushed. ROM digests are recorded for the pin; both equal
main's.

- At pin `0b5e988`, every rtl-fast job's run steps and milan_dp, all rc 0:
  - changes: `true`;
  - lint_rtl: 89 ≤ ratchet 89; pp_srcs;
  - behave: 14 features, 508 scenarios;
  - the yosys elaboration of `milan_datapath`, `KL_pp_shadow` and `KL_gptp_shadow`, with the
    OOC read-set, refusal, guard and cache self-tests;
  - the publication census;
  - firmware-unit, firmware-boundary and firmware-verilator;
  - the control, AECP and SRP firmware mutation campaigns (shards 1 to 3 of 4);
  - `tb/verilator/milan_dp`: 12,075 `[ok]`, 1,301 `[PASS]`, 0 failures.
- At this head's pin: changes, lint, behave and the whole yosys-elaboration job, all rc 0.

## Limits and open risks

- **The bound.** The port holds N Talker values, one per sink. On a port that registers more
  Talker values than that, a value registered while all N are held is not held. A sink that
  settles on it waits for the talker's next declaration, at the latest its re-join after a
  LeaveAll, as before this change (PS11).
- **Area.** At the shipping shape `KL_srp_top` grows by about 1,200 LUT and 560 FF under yosys.
  The integrator's slice budget must be re-measured with its own Vivado route at adoption;
  none was run here.
- **Behaviour change outside the issue.** A re-bind whose old Leave is still owed now sends the
  new stream's New in the same walk (design item 3). This replaces issue #188's one-walk delay;
  RB1, RB4, RB6, RB7 and AS7 grade it.
- **The pin bump.** It needs the parent's ROM-digest rows (recorded, unchanged values) and its
  documented-pin update, which the parent's docs workflow checks.

Closes #212

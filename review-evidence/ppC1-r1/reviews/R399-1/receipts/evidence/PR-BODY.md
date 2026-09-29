[A437]

Closes #29
Closes #108
Closes #64
Closes #65

Lane C1 of the PP program: SRP/MVRP timers and LeaveAll (assignment: #108 comment 5883702094). Branch `c1-srp-mrp-timers` from `main` `c951a9ff`, four commits, one or more per item:

| Commit | Item |
|---|---|
| `6356352` | 1. #29 = #108: a received LeaveAll restarts the leavealltimer and goes Passive |
| `45836ad` | 2. #64: MRP timers graded in `tb/srp_top` against Milan Table 4.3 |
| `bff4417` | 3. #65: MVRP join before the stream, both halves |
| `81b8d6d` | the parent C++ idiom gate (Rule 11) on the new test code: two functions split, spacing pairs named |

No port or parameter of `protocol_processor_top` or `KL_srp_top` changes.

## 1. Received LeaveAll: Start leavealltimer, Passive (#29, #108)

**Clause.** 802.1Q-2014 Table 10-5 (10.7.9) maps rLA! to "Start leavealltimer, Passive" in both states; 10.6: "Reception of a LeaveAll message from another Participant causes the timer to be restarted without generating a message". 10.7.4.3: a start draws LeaveAllTime < T < 1.5 LeaveAllTime, per Port, per Participant.

**Per-Attribute-Type interpretation.** rLA! occurs for a state machine when the PDU "contains a Message in which the Attribute Type is the type associated with the state machine" (10.7.5.20 b)2)); #106 applies that to applicants and registrars, one type each. The LeaveAll machine has no type of its own: it "operates on a per-application (not per-Attribute Type) basis" and issues a LeaveAll "for each Attribute Type supported by the application" (10.7.5.20 NOTE). Every Attribute Type of the application is therefore associated with it: a LeaveAll lane of any MSRP type (`dec_la_msrp_w`) is rLA! for the MSRP machine, the VID lane (`dec_la_mvrp_w`) for the MVRP machine, never across (10.7.5.20 b)1)).

**Change (`hdl/srp/KL_srp_top.sv`).**
- Start leavealltimer: both lanes now request a fresh kind-3 draw (`need_draw_r`), which re-arms that application's slot from the peer's LeaveAll. While that re-arm is outstanding, an expiry of the superseded deadline is ignored (`la_rearm_w`); a genuine expiry disarms its slot, so it never meets the condition.
- Passive: the unaccepted own MSRP action is dropped (unchanged from #127). MVRP gets the same Active state: the own MVRP expiry still re-joins every held VID, but its LeaveAll flag now waits in `la_mvrp_pend_r` for the next MVRP drain with content, and a peer MVRP LeaveAll before that drops it. Before, the flag was latched in the encoder and could not be dropped.
- `docs/architecture/10_srp_engine.md` section 6.5 drops the deviation and states the interpretation; `docs/10_RESOURCE_AND_EFFORT.md` item 11 now credits this spec with the restart; the F08.1 `T-MRP-LEAVEALL` row names the three starts.

**Tests (`tb/srp_top`, group `restart`).** P1: F4's bridge shape every second for 20 cycles (past the 15 s ceiling): no own MSRP LeaveAll, every peer restarts the deadline to 10-15 s after it, and the own LeaveAll resumes 10-15 s after the last peer (+11.1 s). P2: the MVRP mirror. P3: the restart pinned per lane (MVRP and MSRP types 1-4): only that application's timer, the superseded deadline passes silently, the restarted one fires once 13.2-14.0 s after the peer. P4-P6: MVRP Passive while Active, with a VID held and with none, and the MVRP lane at -1/0/+1 clocks of the real expiry. M4 and M10 are updated (before #108 they asserted no restart); F4's pins move from 18/4 to the measured 17/4 (the own burst's frame no longer lands). The new tests against the base `KL_srp_top.sv` fail 29 checks.

**Mutants.** `expiry-only-redraw` (the expiry-only re-draw restored) 15 (P1, P3); `mvrp-expiry-only-redraw` 6; `stale-expiry-honoured` 1 (M10); `mvrp-stale-expiry-honoured` 1 (P6); `mvrp-passive-lost` 4; `mvrp-flag-at-expiry` 6. The round-1 arm `peer-restarts-timer` planted exactly this behavior and is retired; five arms whose context moved are regenerated with the same edit and re-measured.

## 2. MRP timers against Milan Table 4.3 (#64, REQ-SRP-001)

Every captured MRPDU is timestamped (`now_ms` at its last byte). Group `timers`, from one reset (Begin! arms both leavealltimers):
- Q1 joinTime 180-240 ms: the Table 10-3 ladder New, New, JoinMt of one declaration is 200, 200 ms apart.
- Q2 periodictimer 900-1500 ms: the quiet Talker Advertise JoinMt, the Domain JoinIn and the MVRP VID JoinIn each recur every 1000 ms (9 each).
- Q3 leavealltimer 10-15 s, no peer LeaveAll: first own MSRP and MVRP LeaveAll at +14.2 / +10.6 s after arming; consecutive own LeaveAlls 10.0-12.8 s (MSRP) and 11.0-13.2 s (MVRP) apart.
- Q4 after item 1: the next own LeaveAll comes 11.0 s (MSRP) and 14.5 s (MVRP) after a peer's.

Mutants recorded in `tb/srp_top/README.md`: `JOIN_MS_P = 400` 2 (Q1, Q2); `PERIODIC_MS_P = 3000` 1 (Q2); `draw_kind_o = 3'd0` 6 (Q1-Q4).

## 3. MVRP join before the stream (#65, REQ-SRP-006)

**Requirement.** Milan v1.2 4.3.2: a Talker PAAD "shall join the relevant VLAN via MVRP prior to sending any Stream frames"; 4.4.1: a Listener PAAD "shall declare an MVRP VID attribute for each VLAN used by its settled sinks"; 4.2.7.3.

**Talker half: the licence waits for the join.** `KL_srp_encoder` strobes `tx_mvrp_o` when the TX arbiter accepts an MVRP MRPDU. `KL_srp_vlan` records per live VID whether a New or JoinIn of it has been in such an MRPDU since the VID was allocated (MVRP pushes wait while an MVRP drain runs, so a push accepted before a drain started is in that MRPDU). `KL_srp_talker_fsm` ANDs "the entry holding my VID is sent" into ACTIVE. "Transmitted" is the arbiter's acceptance, the last point the engine observes. The design was written first and checked against the lane's STOP conditions: no new top-level port, no parent change needed, and the MSRP and MVRP join ticks run in lock-step with the MVRP drain first, so the VID New leaves ahead of the first Talker Advertise and a Ready that answers the Advertise never waits; the worst case (a Ready registered before the VID's first MVRP MRPDU) waits at most one T-MRP-JOIN.

**Listener half.** The settle already declares the VID (New, JoinIn on the cadence, Lv on the last user); no RTL change.

**Tests.** `tb/srp_top` group `join`: R1 a Ready at 1 ms, before the first tick: no licence until the BFM accepts the VID 2 New, then ACTIVE one clock later (200 ms), within one join-paced MRPDU, and the New is accepted ahead of the first Talker Advertise; R2 a second source on the joined VID is licensed at once; R3 a move to VID 7 waits for VID 7's own New; R4 DECLARE_LISTENER on VID 7 (no source): byte-exact MVRP New, JoinIn every 1000 ms, WITHDRAW_LISTENER: byte-exact Lv. Unit checks in `tb/srp_stream_fsms` (the VID term) and `tb/srp_encoder` W1-W5 (the strobe and the sent tracking). H and I (#112) registered a Ready about 2 ms after reset, which is this very case: they now let the join leave first and assert it (their LATENCY, CROSS and WINDOW measurements are byte-identical).

**Mutants.** `licence-ignores-join` srp_top 3 (R1, R3) and srp_stream_fsms 3; `join-sent-at-handover` srp_top 3 and srp_encoder 3; `count-up-unsends` srp_top 3 (R2, R3) and srp_encoder 2; `tx-strobe-any-app` srp_encoder 1; `listener-lane-cut` (`vu_sel_ls_w` forced 0) srp_top 3 (R4).

## 4. Parent-visible, for the pin-adoption lane

- **No interface change.** No port, parameter or register of `protocol_processor_top` or `KL_srp_top` changes. The new ports are internal to `KL_srp_encoder` (`tx_mvrp_o`), `KL_srp_vlan` (`mvrp_tx_i`, `vid_sent_o`, `vid_val_o`) and `KL_srp_talker_fsm` (`N_VIDS_P`, `vid_sent_i`, `vid_val_i`); no parent bench instantiates these modules at `13eda870`. The `JOIN_MS_P`/`PERIODIC_MS_P`/`LEAVE_MS_P` defaults and PRNG kind 3 that `sw/builder/test_declarations.py` reads are unchanged.
- **`srp_active_o` gains the Milan 4.3.2 term.** The licence also requires the stream VID's MVRP join to have left through the processor's TX arbiter. It differs from before only when a Listener Ready registers before that VID's first MVRP MRPDU, and then by at most one T-MRP-JOIN. Wire order between that MRPDU and the fabric's stream frames past the processor's TX port is the parent's egress path.
- **Fewer own LeaveAlls.** While a peer sends LeaveAlls more often than every 10 s, this station sends none; otherwise one LeaveAll per cycle serves both ends. Bench captures will show the DUT's cadence stretched accordingly.
- **One consumer-gate expectation to re-base.** `tb/verilator/milan_dp` `obj_crflic` phase [C] (`sim_crf_licence.cpp` lines 953 and 956) asserts at least 4 DUT and 4 switch LeaveAll MRPDUs in its 76 s window. Its switch model sends one 9.99 s after each DUT LeaveAll, and the DUT now restarts on it (DUT LeaveAlls 13.0, 10.4 and 10.2 s after the switch's), so the window holds 3 of each. With `>= 3` in those two lines (scratch only) the full `milan_dp` is rc 0. The adoption lane can also assert the restart itself: every DUT LeaveAll at least 10 s after the preceding switch LeaveAll.
- **Parent documents to update at adoption:** `docs/traceability/ieee8021q.md` MRP-5 (records the #108 restart as an open deviation: now implemented), MRP-4 (ACTIVE's terms), MRP-6/MRP-7 (join, periodic and leavealltimer are now graded by `tb/srp_top` Q1-Q4); `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.2.7.1 (Table 4.3) and 4.2.7.3/4.4.1 (MVRP), which can cite the new grading and the 4.3.2 licence term.
- Every other consumer command is rc 0 as is (table below).

## Validation

Verilator 5.050 (the CI pin).

Processor, at `81b8d6d`:

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,016,000 checks, 0 failing (srp_top 2149, srp_stream_fsms 1219, srp_encoder 581, pp_top 7751) |
| `./scripts/lint_hdl.sh` | 0 | every module |
| `make check` | 0 | lint, WaveDrom, links, both matrices, parameters, stale |
| `python3 scripts/gen_matrix.py --check` | 0 | |
| `./syn/yosys/run.sh` | 0 | 34 tops and the Xilinx memory-map check |
| `make -C tb/nvm_port figures` | 0 | with merged PR #13's objects fetched read-only for its provenance check |
| `make -C tb/srp_top mutants` | 0 | 10 controls pass, 72 arms killed by their named assertions, assertion coverage 63/63 (K L M N O P Q R) |
| `tb/srp_admission/mutants.py`, `tb/pp_top/gsi_mutants.py`, `tb/pp_top/name_wr_mutant.py`, `tb/acmp_talker/retry_mutants.py` | 0 each | not in CI; run because their suites contain the SRP engine |
| `git diff --check c951a9ff..81b8d6d` | 0 | |

Parent consumer set: a scratch parent exported from milan-fpga dev `13eda870` with its submodules at their pins and the `protocol-processor` gitlink staged at `81b8d6d`:

| Command | rc | Note |
|---|---:|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | at `bff4417` it failed on this lane's new test code (Rule 11); fixed in `81b8d6d` |
| `python3 scripts/check_py_idiom.py` | 0 | |
| `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, none in files this lane touches |
| `python3 scripts/check_rtl_source_lists.py` | 0 | |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | |
| `python3 sw/builder/test_builder.py` | 0 | |
| `make -C tb/verilator/pp_shadow -j8` | 0 | 635 checks, 0 failures |
| `python3 scripts/check_port_contracts.py` | 0 | |
| `python3 scripts/measure_naming.py --check` | 0 | |
| `python3 scripts/measure_test_evidence.py --check` | 0 | |
| `python3 scripts/docs_check.py` | 0 | |
| `make -C tb/verilator/nvm_cosim lint` | 0 | no PINMISSING |
| `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| `make -C tb/verilator/milan_dp -j8` | **2** | `obj_crflic` [C]: 2 of 415 fail, the LeaveAll counts above. Attribution: item 1. The same leg passes 415/415 with the processor at `c951a9ff`, and at `81b8d6d` with only the MSRP restart reverted; with the two counts re-based (scratch) every leg passes |
| `make -C tb/verilator/milan_dp_render -j8` | 0 | 65/65, 152/152 |

## What remains

- No hardware was used. The bench effect of item 1 (DUT LeaveAll cadence against the reference switch) and of item 3 (first-bind latency, parent #606) is parent evidence for #76.
- Found here, not fixed (outside this lane): a DECLARE_TALKER on a source that is already declaring enqueues another VLAN user++ for the same VID, and WITHDRAW_TALKER removes only one, so that VID's membership never reaches Lv after a re-declaration. It needs its own issue.
- An MVRP drain has no LeaveAll-only form, so with no VID held the own MVRP LeaveAll waits for the first VID declaration (now droppable by a peer MVRP LeaveAll); unchanged behavior, documented in section 6.5.
- The public record of the parent consumer set lists fifteen commands; the manager's set is sixteen. The sixteenth could not be identified from public material, so it is not in the table.

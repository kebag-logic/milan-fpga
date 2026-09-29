[A437]

Closes #29
Closes #108
Closes #64
Closes #65

Lane C1 of the PP program: SRP/MVRP timers and LeaveAll (assignment: #108 comment 5883702094). Branch `c1-srp-mrp-timers` from `main` `c951a9ff`, four commits in round 1, one or more per item, and three in round 2 (section "Round 2" below):

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
- **`srp_active_o` gains the Milan 4.3.2 term.** The licence also requires the stream VID's MVRP join to have left through the processor's TX arbiter (docs 10 section 6.2). It differs from before only when a Listener Ready registers before that VID's first MVRP MRPDU, and then by at most one T-MRP-JOIN plus any time that MRPDU waits for a TX slot or for the TX arbiter; the licence rises one clock after the arbiter's acceptance.
  - **A VLAN-table overflow holds the licence closed until re-declaration.** A VID beyond the engine's membership table (four entries; the supported steady state is one VID, two across a Domain-VID change) is refused and the join dropped. The source's licence stays closed with a Ready and admission, and stays closed after an entry frees; once one is free, re-declaring the source (withdraw, declare) opens it as a fresh declaration does. The refusal is visible only on the engine's `dbg_vlan_err_o` strobe, which the processor top does not export. Before this PR such a source streamed without an MVRP join.
  - **Ordering the parent must keep.** The licence rises one clock after the arbiter grants the MRPDU carrying the VID's declaration, while that MRPDU is still serializing through the processor's TX port onto the parent's egress. The declaration precedes the first stream frame on the wire only if the parent's egress does not let a licensed stream frame overtake a control frame already granted.
- **Fewer own LeaveAlls.** While a peer sends LeaveAlls more often than every 10 s, this station sends none; otherwise one LeaveAll per cycle serves both ends. Bench captures will show the DUT's cadence stretched accordingly.
- **One consumer-gate expectation to re-base.** `tb/verilator/milan_dp` `obj_crflic` phase [C] (`sim_crf_licence.cpp` lines 953 and 956) asserts at least 4 DUT and 4 switch LeaveAll MRPDUs in its 76 s window. Its switch model sends one 9.99 s after each DUT LeaveAll, and the DUT now restarts on it (DUT LeaveAlls 13.0, 10.4 and 10.2 s after the switch's), so the window holds 3 of each. With `>= 3` in those two lines (scratch only) the full `milan_dp` is rc 0. The adoption lane can also assert the restart itself: every DUT LeaveAll at least 10 s after the preceding switch LeaveAll.
- **Parent documents to update at adoption:** `docs/traceability/ieee8021q.md` MRP-5 (records the #108 restart as an open deviation: now implemented), MRP-4 (ACTIVE's terms), MRP-6/MRP-7 (join, periodic and leavealltimer are now graded by `tb/srp_top` Q1-Q4); `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.2.7.1 (Table 4.3) and 4.2.7.3/4.4.1 (MVRP), which can cite the new grading and the 4.3.2 licence term; `tb/verilator/milan_dp/README.md` (blob `3f05559f` at parent dev `57b8c867`), the README of the bench whose count is re-based above: the `[C]` row (line 443, "76 s bound across five DUT and five switch LeaveAll MRPDUs") becomes the re-based bound, at least three DUT and three switch LeaveAll MRPDUs; and the "What it cannot show" sentence (lines 528-530, "This station's leavealltimer does not restart on a received LeaveAll (processor issue 108), and nothing here measures that.") is now implemented: the leavealltimer restarts on a received LeaveAll (processor docs 10 section 6.5), and the bench can measure it with the restart check suggested above.
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
- The public record of the parent consumer set lists fifteen commands; the manager's set is sixteen. The sixteenth could not be identified from public material, so it is not in the table. (Round 2 ran all sixteen; the sixteenth is `python3 scripts/lint_rtl.py --check`.)

## Round 2

[A443], on #108 comment 5886235840: R398-1 (NEGATIVE on one MINOR, F1) and R399-1 (POSITIVE; S1-S3 taken). Head `412efeb`, three commits on `81b8d6d`:

| Commit | Item |
|---|---|
| (PR body) | 1. R398-1 F1: the parent-visible list names `tb/verilator/milan_dp/README.md` (section 4) |
| `e2c631d` | 2. R399-1 S1 with R398-1 S2: a LeaveAll-slot expiry is stale until the restarted deadline, whatever the arm-path latency |
| `c9584bc` | 3. R399-1 S2 = R398-1 S1, plus S3: the licence's added wait, the VLAN-table overflow and the egress order (docs 10 section 6.2, section 4) |
| `412efeb` | 4. R399-1 S3: per-application restart against per-type aging (docs 10 section 6.5) |

No port or parameter of `protocol_processor_top` or `KL_srp_top` changes.

### 2. The stale-expiry guard, independent of arm-path latency

**Clause.** 802.1Q-2014 Table 10-5 rLA!: "Start leavealltimer, Passive"; 10.7.5.22: leavealltimer! occurs "when the leavealltimer associated with that state machine expires". After rLA! the associated timer is the restarted one, so an expiry of the superseded deadline is no leavealltimer! and must not produce sLA.

**Change (`hdl/srp/KL_srp_top.sv`, `la_rearm_w`).** The guard used to end when the restarted deadline's arm was *issued* (`cad_pend_r`). The processor top queues that arm behind other faces, so with more than two clocks of arm latency the superseded deadline could still fire and act (R399-1 S1). That term is now "`now_ms` is before the intended deadline `cad_dl_r[slot]`" (wrap-safe, the timer service's own compare), beside the exact draw-path terms (draw requested, draw in flight). `cad_dl_r` is written only when the draw lands, 10-15 s ahead, and is the value the arm carries, so a genuine expiry, at or after it, is never stale. Docs 10 section 6.5 ("Start leavealltimer") states this.

**Tests (`tb/srp_top`).**
- P8 (new group `armdelay`, also in the default run) commits R399-1's delayed-arm probe. A tb-only delay line (wrapper input `arm_delay_i`, default 0) delays every timer arm N clocks. At N = 3, 4, 8 and 16, one reset scenario per offset puts a peer MVRP LeaveAll around the own MVRP expiry, then a peer MSRP LeaveAll around the own MSRP expiry, from -(N+12) to +2 clocks: no offset sends an own LeaveAll of either application.
- M10 and P6 sweep the peer from -12 to +1 clocks (was -1/0/+1), across the draw request, the PRNG's rejection retries and the arm; placement is graded against the calibrated expiry clock.
- P7 (new) is the MVRP equal edge: a peer MVRP LeaveAll at -1/0/+1 clocks of the join tick that would carry the own flag. The flag is dropped at -1 and 0, and goes out at +1 (that tick was already tx!).
- The default run is now 185,012,669 DUT clocks (P8 53.3 M), so its hang guard moves from 200 M to 300 M clocks.

**Mutants (checked-in, `mutants.py`).**

| Arm | Failing checks |
|---|---|
| `rearm-at-issue` (the issue-time guard restored) | P8: 8. Own MSRP LeaveAll at 4, 4, 7 and 15 offsets for delays 3, 4, 8 and 16 (peer at -11..-8, -11..-8, -14..-8, -22..-8: exactly R399-1's receipts), own MVRP LeaveAll at 2, 2, 6 and 14. M10 and P6 stay green: on the direct path the old guard holds |
| `r-rearm-no-inflight` (R398-1's `rvw-rearm-no-inflight`, same edit) | M10: 3 (peer at -4..-2); P6: 6 (-7..-2) |
| `r-rearm-no-deadline` (R398-1's `rvw-rearm-no-cadpend`, re-based: the term that replaced `cad_pend_r` removed) | M10: 3 (-7..-5); P8: 8 |
| `r-flag-ignores-edge-peer` (R398-1's, same edit) | P7: 1 (the equal edge) |

`draw-kind-0` is regenerated with the same edit (its context held the replaced line). The eight existing arms whose counts the wider sweeps and P7 changed are re-measured in `tb/srp_top/README.md`.

### 3. The licence: added wait, VLAN-table overflow, egress order (docs 10 section 6.2)

The same three statements are in the parent-visible list (section 4):
- **Added wait.** Only for a Ready registered before the VID's first MVRP MRPDU: at most one T-MRP-JOIN plus any wait for a TX slot or the TX arbiter. The licence rises one clock after the acceptance.
- **VLAN-table overflow.** The licence stays closed until the source is re-declared once an entry is free. R399-1's S7 probe, reproduced at this head: closed with a Ready and admission, still closed after an entry frees, open 149 ms after the re-declaration. The refusal is visible only on `dbg_vlan_err_o`, which stays unconnected at the processor top (no new port).
- **Residual ordering assumption.** The licence rises one clock after the arbiter grant, while the MRPDU is still serializing onto the parent's egress; the parent's egress must not let a licensed stream frame overtake it.

### 4. A peer that flags only some types (docs 10 section 6.5)

The restart is per application, the aging per Attribute Type. A peer MSRP LeaveAll that flags only some types restarts the MSRP timer but ages only those types' registrars. The others are then aged only by this participant's own LeaveAlls: about every other cycle against a peer drawing from the same range, never against a faster peer. Such a peer departs from 802.1Q-2014 10.7.5.20 as #106 applies it (NOTE: a LeaveAll for "each Attribute Type supported by the application"), so there is no RTL change.

### Round 2 validation

Verilator 5.050 (the CI pin). Processor at `412efeb`:

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,016,051 checks, 0 failing (srp_top 2200, srp_stream_fsms 1219, srp_encoder 581, pp_top 7751) |
| `./scripts/lint_hdl.sh` | 0 | 40 modules |
| `make check` | 0 | |
| `python3 scripts/gen_matrix.py --check` | 0 | |
| `./syn/yosys/run.sh` | 0 | 35 tops and the Xilinx memory-map check |
| `make -C tb/nvm_port figures` | 0 | |
| `make -C tb/srp_top mutants` | 0 | 11 controls pass, 78/78 arms killed by their named assertions, assertion coverage 65/65 (K L M N O P Q R) |
| `tb/srp_admission/mutants.py`, `tb/pp_top/gsi_mutants.py`, `tb/pp_top/name_wr_mutant.py`, `tb/acmp_talker/retry_mutants.py` | 0 each | not in CI; their suites contain the SRP engine |
| `git diff --check c951a9ff..412efeb` | 0 | |

Both reviewers' round-1 probes, unmodified, at `412efeb`:

| Probe | Result |
|---|---|
| R399-1 delayed-arm probe, arm delays 0, 2, 3, 4, 8, 16 | 0 of 83 offsets send an own MSRP LeaveAll at every delay (at `81b8d6d`: 0, 0, 4, 4, 7, 15) |
| R399-1 licence probe | 8/8, every line identical to its receipt |
| R398-1 V1/V2 probes | PASS, lines identical to its receipt; `rvw-sent-survives-removal` is still killed by V1 |
| R398-1 mutants | the four killed in srp_top at `81b8d6d` still killed (R3; M4, P2, P3, P8; P3; P5); `rvw-flag-ignores-edge-peer` now killed (P7); the two `sent` arms survive srp_top and are killed at unit level (srp_encoder W3/W4), as before; the two `rearm` arms no longer apply and are re-based above |

Parent consumer set: a scratch parent exported from milan-fpga dev `57b8c867`, its submodules at their pins, the `protocol-processor` gitlink at `412efeb` and the declared crflic edit (`sim_crf_licence.cpp:953,956`, `>= 4` to `>= 3`) committed locally in the scratch repository only. The manager's sixteen commands, in its order:

| Command | rc | Note |
|---|---:|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet holds with the new test code |
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
| `python3 scripts/lint_rtl.py --check` | 0 | 90 <= ratchet 90 |
| `make -C tb/verilator/nvm_cosim lint` | 0 | no PINMISSING |
| `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| `make -C tb/verilator/milan_dp -j8` | 0 | every leg passes; `obj_crflic` 415/415, `[C]` 3 DUT and 3 switch LeaveAll MRPDUs |
| `make -C tb/verilator/milan_dp_render -j8` | 0 | 65/65, 152/152 |

16/16 rc 0 with the declared edit. Attribution: with only that edit reversed, `make -C tb/verilator/milan_dp crflic` fails exactly its two LeaveAll counts (2 of 415, 3 and 3 counted), as the manager's gitlink-only run did at `81b8d6d`.

### Round 2: what remains

- Hosted checks at `412efeb` and the delta reviews.
- Pin adoption: the declared crflic edit and the parent documents in section 4, now including `tb/verilator/milan_dp/README.md`.
- The processor top's arm queue drops the newest arm on overrun (counted, never silent). A dropped cadence arm stops that slot; this is pre-existing and common to every cadence slot. With the new guard a dropped LeaveAll re-arm leaves that timer idle until the next received LeaveAll or reset, where the old guard let the superseded deadline act. A possible follow-up: re-issue the intended deadline when a stale expiry arrives with no draw outstanding.

The round-1 sections above remain the round-1 record, except section 4, which round 2's items 1 and 3 amend.

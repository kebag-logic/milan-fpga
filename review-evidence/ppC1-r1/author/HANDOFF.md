# [A437] Lane C1 handoff: SRP/MVRP timers and LeaveAll

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
Branch: `c1-srp-mrp-timers` from `main` `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`
Assignment: issue #108 comment 5883702094 (covers #29 = #108, #64, #65)
Parent reference: milan-fpga dev `13eda870` (read-only)

Status: REVIEW READY at `81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b` (not pushed; no PR created). TAKEN posted: #108 comment 5883708685. REVIEW READY posted: #108 comment 5885542437. PR body: `PR-BODY.md` in this directory.

## Reconstruction

- Read: README, docs/README, docs/architecture/09_verification.md, 10_srp_engine.md,
  hdl/srp (top, talker/listener FSMs, VLAN, encoder, decoder banner), hdl/common/KL_pp_prng.sv,
  KL_pp_timer_service.sv, tb/srp_top (harness, wrapper, README, mutants.py, mutations/),
  tb/srp_stream_fsms, tb/srp_encoder, tb/pp_top (SRP parts).
- Issues #29, #108, #64, #65 in full; PR #107 R270-1 (comment 5801267950); PR #28 external review.
- Standards: IEEE 802.1Q-2014 10.6, 10.7.4.3, 10.7.5.20 (b and NOTE), 10.7.9 Table 10-5,
  10.8.2.6; Milan v1.2 4.2.7.1.1 Table 4.3, 4.2.7.3, 4.3.2, 4.4.1.
- Parent consumer set: the public definition is the fifteen-command list in milan-fpga
  `review-evidence/pp131-r1/author-r4/gates.py` (PR #132 packet, "the manager's fifteen-command
  consumer set"); the manager's current set is 16 commands (milan-fpga #415 comment 5883685470)
  but the 16th is not published. See the gate table for what was run.
- Toolchain: Verilator 5.050 (the CI pin, `.github/workflows/hdl.yml` VERILATOR_VERSION) from the
  shared install `$VALIDATION_TOOLS/verilator-v5.050`, first on PATH for every run.

## Item 1: #29 = #108 received LeaveAll restarts the leavealltimer (Table 10-5 rLA!)

Commit `6356352`.

**Clause.** 802.1Q-2014 Table 10-5 (10.7.9): rLA! = "Start leavealltimer, Passive" in both
the Active and Passive states; 10.6: "Reception of a LeaveAll message from another Participant
causes the timer to be restarted without generating a message". 10.7.4.3: the timer is per
Port, per Participant, and a start draws LeaveAllTime < T < 1.5 LeaveAllTime.

**Per-Attribute-Type interpretation (stated in docs 10 section 6.5 and the KL_srp_top banner).**
10.7.5.20 b)2) makes rLA! occur for a state machine when the PDU "contains a Message in which the
Attribute Type is the type associated with the state machine". #106 applied that to applicants and
registrars (one type each). The LeaveAll machine has no type of its own: it "operates on a
per-application (not per-Attribute Type) basis" and issues a LeaveAll "for each Attribute Type
supported by the application" (10.7.5.20 NOTE). So every Attribute Type of the application is
associated with it: any `dec_la_msrp_w` lane (Talker Advertise, Talker Failed, Listener, Domain)
is rLA! for the MSRP machine, `dec_la_mvrp_w` for the MVRP machine, and never across (b)1): DA and
EtherType select the application). Several flagged types in one MRPDU restart once per lane.

**Change** (`hdl/srp/KL_srp_top.sv`; line numbers at the final head `81b8d6d`):
- `:1221-1232` the peer block: `|dec_la_msrp_w` now also sets `need_draw_r[0]` (fresh kind-3
  draw re-arms `CAD_LA_MSRP`); new `dec_la_mvrp_w` block sets `need_draw_r[1]` and drops the
  pending MVRP flag. The existing MSRP Passive (drop unaccepted own action, #127) is unchanged.
- `:1015-1024` `la_rearm_w`: while a restart's re-arm is outstanding (draw requested, in flight,
  or arm pending), an expiry of that slot is the superseded deadline and is ignored
  (`:1206-1218`). A genuine expiry disarms the slot, so it never meets the condition.
- `:333`, `:1189-1201`, `:1212-1218` MVRP Active/Passive: own MVRP expiry still re-joins every
  held VID at once, but its LeaveAll flag is kept in `la_mvrp_pend_r` and handed to the encoder
  at the next MVRP join tick whose drain has content (no LeaveAll-only MVRP form exists); a peer
  MVRP LeaveAll before that drops it. Before, the flag was latched inside the encoder at expiry
  and could not be dropped (and with no VID held it waited indefinitely).
- Banner `:53-57`, `:79-90`.

**Tests** (`tb/srp_top`, group `restart`, `sim_main.cpp:1156-1368`; wrapper probes
`srp_top_wrap.sv`):
- P1 (`:1167`) F4-style probe: F4's bridge shape every 1 s for 20 cycles (past the 15 s ceiling):
  no own MSRP action or flagged MRPDU; every peer restarts the deadline to 10-15 s after it; MVRP
  keeps its own cycle; own LeaveAll resumes 10-15 s after the last peer (measured +11092 ms).
- P2 (`:1202`) the MVRP mirror.
- P3 (`:1235`) the restart pinned per lane (MVRP and MSRP types 1-4): only that application's
  deadline redrawn from the peer; superseded deadline silent; restarted one fires once,
  >= 10 s after the peer (measured 13.2-14.0 s).
- P4-P6 (`:1276`, `:1305`, `:1333`) MVRP Passive while Active (VID held / no VID held) and the MVRP
  lane at -1/0/+1 clocks of the real MVRP expiry.
- Updated: M4 (`:826-830`, restart for MSRP lanes, unchanged for MVRP), M10 (`check_peer_at_own_expiry`, `:866-889`, the -1
  case is now Passive: the superseded deadline is stale), M12 (reads the restarted deadline), F4
  pins 18 -> 17 (the own burst's one frame no longer lands; measured 4,3,3,3,2,2).
- Failing arm, the base RTL: the new suite against `c951a9ff`'s `KL_srp_top.sv` (scratch copy,
  the one new wrapper probe mapped to the base's encoder latch `u_encoder.la_pend_r[1]`) fails
  29 of 2020: P1 x3, P2 x2, P3 x15, P4 x2, P5 x2, P6 x3, M10 (delta -1) and F4 (18 > 17).
  M4's restart check does not discriminate in its own scenario (an own expiry redraws the timer
  10-250 ms before the peer); P1 and P3 are the pins.

**Mutants** (checked-in patches, `mutants.py`): expiry-only-redraw 15 (P1,P3);
mvrp-expiry-only-redraw 6 (P2,P3,P6); stale-expiry-honoured 1 (M10);
mvrp-stale-expiry-honoured 1 (P6); mvrp-passive-lost 4 (P4,P5,P6); mvrp-flag-at-expiry 6
(P4,P5,P6). Retired `peer-restarts-timer` (it planted exactly the required behavior).
Regenerated for moved context, same edits: expiry-outranks-peer 1 (M10), mvrp-supersedes-msrp 8
(M1-M4), pending-peer-ignored 15 (M1,M2,M3,M10), reset-retains-intent 1 (K10), my-expiry-pulse 62.

**Docs.** 10_srp_engine.md section 6.5 (`:523-526`, `:540-543`, `:578-612`, at the final head) drops the deviation
and states the interpretation; 10_RESOURCE_AND_EFFORT.md item 11 now credits this spec with the
restart; 08_timing.md F08.1 T-MRP-LEAVEALL row names the three starts.

Suites at this commit: srp_top 2020/2020, pp_top 7751/7751, lint OK, make check OK.

## Item 2: #64 MRP timer grading in tb/srp_top (Milan Table 4.3)

Commit `45836ad`. REQ-SRP-001; Milan v1.2 4.2.7.1.1 Table 4.3 (joinTime 180-240 ms,
periodictimer 900-1500 ms, leavealltimer 10-15 s; Milan's tolerance column allows 9.5-15.5 s).
Test-only change (no RTL).

- Timestamps: `tb/srp_top/sim_main.cpp:394-395` every captured MRPDU gets `now_ms_o` at its last
  byte (`archive_ms`) and the BFM acceptance clock (`archive_accept`).
- Group `timers` (`:1475-1630` at the final head, split into four functions by `81b8d6d`), one bring-up from reset (Begin! arms both leavealltimers at
  reset release):
  - Q1 (`check_join_time`, `:1530`) joinTime: the Table 10-3 ladder New, New, JoinMt of one fresh Talker Advertise
    is one MRPDU per tick: spacing in 180-240 ms (measured 200, 200).
  - Q2 (`check_periodic_time`, `:1553`) periodictimer: the quiet Talker Advertise JoinMt, the Domain JoinIn and the MVRP
    VID JoinIn each recur every 900-1500 ms, >= 5 each before the first LeaveAll (9 x 1000 ms).
  - Q3 (`check_leaveall_time`, `:1578`) leavealltimer, no peer LeaveAll: first own MSRP and MVRP LeaveAll >= 10 s after
    arming (+14206 / +10601 ms); consecutive own LeaveAlls 10-15 s apart, >= 3 per application
    (MSRP 10000-12800, MVRP 11000-13200 ms).
  - Q4 (`check_leaveall_after_peer`, `:1606`) after item 1: a peer LeaveAll 5 s after the latest own one; the next own
    LeaveAll of that application is 10-15 s after the peer's (MSRP +11000, MVRP +14495 ms).
- Mutants (checked-in patches, `mutants.py`, recorded in `tb/srp_top/README.md`):
  `join-ms-400` 2 (Q1,Q2); `periodic-ms-3000` 1 (Q2); `draw-kind-0` 6 (Q1-Q4).

Suite at this commit: srp_top 2027/2027.

## Item 3: #65 MVRP join before the stream (design first)

### Design (written before implementation)

**Requirements.** REQ-SRP-006. Milan v1.2 4.3.2: "A Talker PAAD shall join the relevant VLAN
via MVRP prior to sending any Stream frames." 4.4.1: "A Listener PAAD shall declare an MVRP VID
attribute for each VLAN used by its settled sinks." 4.2.7.3: a PAAD shall support MVRP.

**Talker half: gate the licence.** Today `active_o[s]` (`KL_srp_talker_fsm.sv:800-803`) =
declaring Advertise AND Listener Ready/ReadyFailed registered AND admitted; nothing says the
MVRP declaration of `vid_r[s]` has left. Add one term: `vok[s]` = the VLAN membership that holds
`vid_r[s]` has been declared in an MVRP MRPDU that the TX arbiter accepted.
- `KL_srp_encoder`: new output `tx_mvrp_o`, a one-cycle strobe when an MVRP MRPDU's request is
  accepted (`E_TXREQ && txreq_ready_i && cur_app == MVRP`). "Transmitted" is taken at the TX
  arbiter's acceptance: it is the last point the engine observes, and the arbiter serializes the
  frame without preemption from there.
- `KL_srp_vlan`: per entry, `queued` (a New/JoinIn of the entry was accepted by the encoder since
  the last MVRP transmission) and `sent` (the entry's declaration has been in a transmitted MVRP
  MRPDU since the entry was allocated). New input `mvrp_tx_i`: `sent |= queued`, `queued = 0`.
  Allocation and retirement clear both. Pushes are blocked while an MVRP drain is running, so a
  push accepted before a transmission's drain start is in that MRPDU, and a later push waits for
  the next one. New outputs: per-entry `vid_sent_o` (= active and sent) and the entry VID
  `vid_val_o` (a flop copy of the VID written at allocation; the RAM keeps {vid, refcount} for
  the serial scan unchanged).
- `KL_srp_talker_fsm`: new parameter `N_VIDS_P`, inputs `vid_sent_i`/`vid_val_i`;
  `vok[s] = OR_e (vid_sent_i[e] && vid_val_i[e] == vid_r[s])`, and `active_o[s] &= vok[s]`. It is a
  live function of VLAN state, so a same-VID re-declaration keeps it, a close/reopen that never
  left keeps it, and a new VID waits for its own transmission.
- `KL_srp_top`: internal wiring only (encoder `tx_mvrp_o` to VLAN, VLAN outputs to the talker).
  No top-level port or parameter changes; `protocol_processor_top` untouched.

**Listener half.** The settle already enqueues VLAN user++ with the settled VID
(`KL_srp_listener_fsm`), and the VLAN declares a new VID with New and later JoinIn, and Lv on
the last user. Milan 4.4.1 sets no ordering for listeners, so no RTL change: tests only.

**Tests (both halves, each with a mutant).**
- Talker (srp_top): a Listener Ready injected right after DECLARE_TALKER, before the first join
  tick: `active_o` must stay low until the cycle after the BFM accepts the MVRP MRPDU carrying VID
  New, then rise; a second source on the same, already transmitted VID is licensed at once;
  a withdraw/re-declare on a new VID waits again. Mutant: the `vok` term removed.
- Talker unit (srp_stream_fsms): the term against driven `vid_sent_i`/`vid_val_i` (no entry, other
  VID, sent/unsent). Mutant: same.
- Listener (srp_top): DECLARE_LISTENER on VID 7 (no source holds it): byte-exact MVRP VID 7 New,
  then JoinIn on the periodic cadence; WITHDRAW_LISTENER of the last user: MVRP Lv of VID 7.
  Mutant: `vu_sel_ls_w` forced 0 (the #65 acceptance arm).
- Existing checks that inject a Listener Ready within ~2 ms of reset (H and I, issue #112) are
  exactly the case the gate closes; they get a setup that lets the MVRP join leave first (their
  per-clock ACTIVE equation then holds as written, since the VID term stays 1 in the window).

**STOP evaluation.**
1. New top-level port: none (only internal module ports of the encoder, VLAN and talker FSM; no
   parent bench instantiates those modules: parent grep at `13eda870` finds only textual reads of
   `KL_srp_top.sv`/`KL_pp_prng.sv` parameters in `sw/builder/test_declarations.py`).
2. Parent-visible change: `srp_active_o` keeps its name and meaning (the streaming licence) and
   gains the 4.3.2 term. No parent code change is needed. The only parent reader of the licence
   itself is `tb/verilator/milan_dp/sim_crf_licence.cpp` (via `milan_datapath`), whose switch
   declares Listener Ready seconds after the DUT's Talker Advertise, after the MVRP join. The
   consumer gates are the check; any failure would be reported with its attribution.
3. First talker bind delay: the MSRP and MVRP join slots are armed at the same deadline and
   re-armed from the same `now_ms` at every expiry, and the MVRP drain starts on its tick while
   the MSRP drain waits for its walks, so the MVRP New leaves in the same tick as, and ahead of,
   the first Talker Advertise New. A Listener Ready that answers our Advertise therefore finds
   the term already true: no added latency. The worst case (a Ready registered before the VID's
   first MVRP MRPDU, or a gate open a few clocks before a tick) waits for the next MVRP drain:
   at most one T-MRP-JOIN, one join-paced MRPDU. Neither STOP condition is met.

### Implementation

Commit `bff4417`, as designed. One addition the design text did not list: the description
comment of `srp_active_o` in `hdl/top/protocol_processor_top.sv` now names the new term (a
comment only; the port list and parameters are unchanged). Line numbers at the final head.

- `hdl/srp/KL_srp_encoder.sv:125,781` `tx_mvrp_o` strobe (MVRP request accepted).
- `hdl/srp/KL_srp_vlan.sv:72-76` new ports; `:99-101` `queued_r`/`sent_r`/`vid_q_r`;
  `:208-211` transmission moves queued to sent; `:257-259` allocation clears and records the VID;
  `:270-271` retirement clears; `:286` a fresh entry's New queued at hand-over; `:309` re-join
  JoinIn queued; `:329-330` outputs. Banner `:24-42`.
- `hdl/srp/KL_srp_talker_fsm.sv:90-91` `N_VIDS_P`; `:150-151` inputs; `:804-812` `vid_ok_w`;
  `:824` ACTIVE term. Banner `:27-33`.
- `hdl/srp/KL_srp_top.sv:400-402,441-443,562-563,768` internal wiring; banner `:61-66`; the
  `active_o` port comment. `hdl/top/protocol_processor_top.sv` `srp_active_o` comment only.
- Docs: `docs/architecture/10_srp_engine.md:239-249` (section 6.2, "Join before the stream"),
  `:271-274` (section 6.3 ACTIVE equation); `docs/guides/integrator.md:330`.

**Tests.**
- Talker, end to end (`tb/srp_top`, group `join`, `sim_main.cpp:1386`): R1 Ready at 1 ms, before
  the first tick: registered, admitted, not ACTIVE; ACTIVE rises 1 clock after the BFM accepts
  the VID 2 New (200 ms), within one join-paced MRPDU; the VID New is accepted ahead of the first
  Talker Advertise. R2 second source on the joined VID: ACTIVE at once. R3 re-declare on VID 7:
  waits for VID 7's own New; VID 2 not withdrawn.
- Listener, end to end (`:1437`): R4 DECLARE_LISTENER VID 7 (no source): byte-exact MVRP New, then
  JoinIn 3 x 1000 ms, WITHDRAW_LISTENER: byte-exact MVRP Lv, no membership left.
- Talker unit (`tb/srp_stream_fsms/sim_main.cpp:600-612,643-646`): the VID term against a driven
  VLAN view (unsent, other VID, sent, gone). Encoder/VLAN unit (`tb/srp_encoder/sim_main.cpp:1266`):
  W1 strobe per MVRP MRPDU only; W2-W5 sent tracking.
- Existing H and I (issue #112) registered a Ready ~2 ms after reset, i.e. the #65 case: 184 of
  their checks fail against the gated licence (96 H, 88 I; the failing arm of the old setup).
  They now wait 250 ms after the first declaration and assert VID 2's join was captured
  (`:2221`, `:2352`; +112 checks). Every LATENCY/CROSS/WINDOW measurement line is byte-identical
  to the baseline run.
- Mutants (checked-in patches): `licence-ignores-join` srp_top 3 (R1,R3) and srp_stream_fsms 3;
  `join-sent-at-handover` srp_top 3 (R1,R3) and srp_encoder 3 (W2,W3,W4); `count-up-unsends`
  srp_top 3 (R2,R3) and srp_encoder 2 (W4); `tx-strobe-any-app` srp_encoder 1 (W1);
  `listener-lane-cut` (`vu_sel_ls_w` forced 0) srp_top 3 (R4).

Suites at this commit: `run_suites.sh` rc 0, 33 suites, 1,016,000 checks (srp_top 2149,
srp_stream_fsms 1219, srp_encoder 581, pp_top 7751); lint rc 0; make check rc 0.

## Extra commit: parent C++ idiom (Rule 11)

Commit `81b8d6d`. The parent consumer gate `check_cpp_idiom.py` scans the processor's test C++:
at `bff4417` it failed (multi-declarator 4 > 0, long function 2 > 0), all in this lane's new
`tb/srp_top` code (the four `lo, hi` pairs; `check_pending_leaveall_supersession` grew to 107
lines with the M4/M12 edits, the Q function was 102). Fixed with a `Gaps` struct and by
splitting both functions (M9/M10 into `check_peer_at_own_expiry`, Q into four); every printed
measurement line is identical before and after. Parent scanner re-run: 0 findings.

## Item 4: parent-visible list (for the pin-adoption lane; also in PR-BODY.md)

1. No interface change: no port, parameter or register of `protocol_processor_top` or
   `KL_srp_top`. New ports are internal to `KL_srp_encoder` (`tx_mvrp_o`), `KL_srp_vlan`
   (`mvrp_tx_i`, `vid_sent_o`, `vid_val_o`) and `KL_srp_talker_fsm` (`N_VIDS_P`, `vid_sent_i`,
   `vid_val_i`); no parent bench instantiates these at `13eda870`. The defaults
   `sw/builder/test_declarations.py` reads textually are unchanged.
2. `srp_active_o` gains the Milan 4.3.2 term (the stream VID's MVRP join accepted by the
   processor's TX arbiter). Differs only when a Listener Ready registers before that VID's first
   MVRP MRPDU, by at most one T-MRP-JOIN. Wire order past the processor's TX port is the parent's
   egress path.
3. Fewer own LeaveAlls (item 1). **Consumer-gate effect:** `tb/verilator/milan_dp` `obj_crflic`
   phase [C] (`sim_crf_licence.cpp:953,956`) asserts >= 4 DUT and >= 4 switch LeaveAll MRPDUs in its
   76 s window. Its switch model sends one 9.99 s after each DUT LeaveAll; the DUT now restarts on
   it (DUT LeaveAlls 13.0, 10.4, 10.2 s after the switch's), so the window holds 3 of each. The
   pin-adoption lane re-bases the two counts (measured: `>= 3` makes the full `milan_dp` rc 0) and
   can add the restart itself as a check (each DUT LeaveAll >= 10 s after the preceding switch
   LeaveAll).
4. Parent documents at adoption: `docs/traceability/ieee8021q.md` MRP-5 (records #108 as an open
   deviation), MRP-4 (ACTIVE's terms), MRP-6/MRP-7 (now graded by `tb/srp_top` Q1-Q4);
   `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.2.7.1 (Table 4.3) and 4.2.7.3/4.4.1 (MVRP), which
   can cite the new grading and the 4.3.2 term.

## Gates

All at the final head `81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b`, Verilator 5.050. Logs are in
scratch (`$VALIDATION_STORAGE/c1-a437/{proc,parent,attr}-logs`, not in this directory); each row
records size and SHA-256 (first 16 hex). Commands longer than ten minutes ran through the same
one-command runner started detached and were waited on in the foreground until exit.

### Processor entry points and suites

| Command | rc | s | Log bytes | Log SHA-256 |
|---|---:|---:|---:|---|
| `./scripts/run_suites.sh` | 0 | 328.1 | 1,645 | `c670a1f478d04373` |
| `./scripts/lint_hdl.sh` | 0 | 9.0 | 1,028 | `49e02975050b914d` |
| `make check` | 0 | 29.3 | 225 | `e0ea0ab212185e3b` |
| `python3 scripts/gen_matrix.py --check` | 0 | 0.0 | 33 | `98e5ebd5eedcc618` |
| `./syn/yosys/run.sh` | 0 | 79.3 | 25,185 | `d647b0524ff9b435` |
| `make -C tb/nvm_port figures` | 0 | 245.1 | 3,613 | `e597dffc5a880884` |
| `make -C tb/srp_top mutants` | 0 | 1506.2 | 5,390 | `f9dd011b34d9565b` |

`run_suites.sh`: 33 suites, 1,016,000 checks, 0 failing (srp_top 2149, srp_stream_fsms 1219,
srp_encoder 581, pp_top 7751; base `c951a9ff` had 1987 / 1215 / 562 / 7751). Lint: 40 modules OK.
Yosys: 34 tops + the Xilinx memory-map check. `nvm_port figures` first returned 2 on provenance
only (all figures `[ok]`; "cannot read dc354be~1 / 62d96d6~1"): those commits are in merged PR #13's
history, fetched read-only (`git fetch origin pull/13/head`, objects only), then rc 0, as the
earlier banks did.

### Mutants

`make -C tb/srp_top mutants` (the campaign, CI's mutation step): 10 positive controls pass, all
72 arms KILLED by their required named assertions, assertion coverage 63/63 (K12 L4 M12 N13 O8
P6 Q4 R4), `83 checks: 83 PASS, 0 FAIL`. This lane's arms (item: arm, failing checks): item 1
expiry-only-redraw 15, mvrp-expiry-only-redraw 6, stale-expiry-honoured 1, mvrp-stale-expiry-honoured 1,
mvrp-passive-lost 4, mvrp-flag-at-expiry 6; item 2 join-ms-400 2, periodic-ms-3000 1, draw-kind-0 6;
item 3 licence-ignores-join 3 + 3 (stream FSMs), join-sent-at-handover 3 + 3 (encoder),
count-up-unsends 3 + 2 (encoder), tx-strobe-any-app 1 (encoder), listener-lane-cut 3.

The tree's other mutation drivers (not in CI; they target unrelated modules but build suites that
contain the changed SRP engine), each rc 0 at `81b8d6d`:

| Command | rc | s | Log SHA-256 | Summary |
|---|---:|---:|---|---|
| `python3 tb/srp_admission/mutants.py --output <scratch>` | 0 | 485.5 | `6977d367d954c85c` | 12/12, including the srp_top controls |
| `python3 tb/pp_top/gsi_mutants.py --output <scratch> --verilator <pinned>` | 0 | 730.0 | `5f6d67707db7bfed` | 20 detected by named checks; golden and restored PASS |
| `python3 tb/pp_top/name_wr_mutant.py --output <scratch>` | 0 | 36.4 | `055560a7d55d359d` | decode killed; golden and restored PASS |
| `python3 tb/acmp_talker/retry_mutants.py --logs <scratch>` | 0 | 381.5 | `7bda8adf83703e45` | 62 killed, 7 equivalence and 1 performance controls |

`git diff --check c951a9ff..81b8d6d`: clean.

### Parent consumer gates

Scratch parent: `git archive` of the trusted checkout at `13eda870`, submodules exported at their
pins (`external` efeb541a, `gptp-processor` 5dce647a, `third_party/verilog-axis` 48ff7a7e, fetched
read-only from their public URLs into scratch), each made a repository at its pin, `protocol-processor`
at this head; all four gitlinks staged in a scratch index (964 tracked files, as the trusted
checkout) and `git submodule init` (config only). The public set has fifteen commands
(milan-fpga `review-evidence/pp131-r1/author-r4/gates.py`); the manager's sixteenth is not public.

| Command | rc | s | Log bytes | Log SHA-256 | Attribution |
|---|---:|---:|---:|---|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | 1.2 | 315 | `3673d5b75f37a526` | at `bff4417` rc 1 on this lane's test code; fixed in `81b8d6d` |
| `python3 scripts/check_py_idiom.py` | 0 | 3.4 | 461 | `0626d39868735288` | |
| `python3 scripts/xvlog_gate.py --check` | 0 | 138.4 | 1,320 | `34cd004adc90ed8f` | 4 findings == ratchet, all in files this lane does not touch |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 1.4 | 390 | `1dd83081ba29241f` | |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.2 | 955 | `fb4b6d8cc0ca4895` | |
| `python3 sw/builder/test_builder.py` | 0 | 916.2 | 96,804 | `eea174389eef2881` | |
| `make -C tb/verilator/pp_shadow -j8` | 0 | 45.4 | 300,662 | `c00311a94b50ca58` | 635 checks, 0 failures, no PINMISSING |
| `python3 scripts/check_port_contracts.py` | 0 | 2.3 | 421 | `b69a0fd2817413f5` | |
| `python3 scripts/measure_naming.py --check` | 0 | 0.4 | 36,572 | `bee3051c403aa565` | |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 5.6 | 11,253 | `02b91ce2d5607aa9` | |
| `python3 scripts/docs_check.py` | 0 | 4.5 | 127 | `aaa28df396cb6680` | |
| `make -C tb/verilator/nvm_cosim lint` | 0 | 0.3 | 29,629 | `773c214ab09705b1` | 84 warnings, no PINMISSING |
| `make -C tb/verilator/nvm_cosim quick` | 0 | 29.3 | 388 | `b9deae15fb50d23f` | 315/315 |
| `make -C tb/verilator/milan_dp -j8` | **2** | 366.0 | 1,778,740 | `4a1bf5e9897b0c5b` | `obj_crflic` [C] 2 of 415 fail: item 1 (see parent-visible item 3); every other leg run passes |
| `make -C tb/verilator/milan_dp_render -j8` | 0 | 310.8 | 158,648 | `22662eb6ab727ab0` | 65/65, 152/152 |

Attribution runs of the `milan_dp` failure (a copy of the scratch parent):

| Processor in the copy | Command | rc | s | Log SHA-256 | Result |
|---|---|---:|---:|---|---|
| base `c951a9ff` | `make -C tb/verilator/milan_dp crflic` | 0 | 62.7 | `8a04a39c1311e578` | 415/415; 5 DUT, 5 switch LeaveAlls |
| `81b8d6d` minus the MSRP restart (`expiry-only-redraw.patch`) | same | 0 | 61.1 | `a3b5ee14ae30aa32` | 415/415; 5 and 5 |
| `81b8d6d`, parent edit `>= 4` -> `>= 3` at `sim_crf_licence.cpp:953,956` (scratch only) | `make -C tb/verilator/milan_dp -j8` | 0 | 1408.3 | `41d29ab397fc0462` | every leg passes |

So the failure is item 1's required behavior against a count written for the old cadence; items
2 and 3 do not touch it.

## What remains

- No hardware was used. Bench evidence for item 1 (DUT LeaveAll cadence against the reference
  switch) and item 3 (first-bind latency, parent #606) belongs to parent #76.
- Pin adoption: the `obj_crflic` [C] count re-base and the parent documents in item 4.
- Found here, not fixed (outside this lane): a DECLARE_TALKER on a source that is already
  declaring enqueues another VLAN user++ for the same VID (`KL_srp_talker_fsm` VLAN op plane,
  unchanged from `c951a9ff`), and WITHDRAW_TALKER removes one, so after a re-declaration the VID
  never reaches Lv. Reproduced at this head with a scratch-only probe of `tb/srp_top`: declare
  VID 7, re-declare, withdraw: VID 7 still live, no MVRP Lv (control, one declaration: Lv, no
  membership). Needs its own issue.
- An MVRP drain has no LeaveAll-only form: with no VID held the own MVRP LeaveAll waits for the
  first VID declaration (now droppable by a peer MVRP LeaveAll). Unchanged, documented in 10
  section 6.5.
- The sixteenth command of the manager's consumer set is not public; the fifteen public ones ran.

## Scratch (outside this directory, not in the tree)

`$VALIDATION_STORAGE/c1-a437`: logs, the scratch parent and its attribution copy, the gate runner
`gate.py`, the patch generators `gen_patches_item{1,2,3}.py` (exact textual edits turned into the
checked-in unified diffs), the base-RTL failing-arm copy and the leak probe.

[A661] SRP listener: sinks settled on one stream_id share one declaring Listener applicant, by owner election in the per-sink plane (#193)

Closes #193

Three commits on main 21601694 (round 1b), the merge of main 08023123, five commits answering
the two reviews of round 1b (round 2, below), six answering those of round 2 (round 3), the
merge of main 859b537b, and three answering those of round 3 (round 4).
The round-1 measurement (on #193) found two Listener VectorAttributes with the same
FirstValue in one MRPDU when two sinks were settled on one StreamID, and a Leave for the
value when one of them unbound. The ruling on #193 asked for
one declaring applicant per StreamID by owner election inside the existing per-sink plane;
this PR implements it.

## Behaviour

IEEE 802.1Q-2018 10.7.7 gives each attribute value one Applicant, and the 35.2.6 NOTE allows
at most one Listener Declaration per StreamID per port. The Listener attribute's value is the
stream_id alone, so the sinks settled on one stream_id now share one applicant, kept in one
of their existing per-sink slots:

| Role | Which sink | Its applicant slot |
|---|---|---|
| Owner | the lowest-index sink declaring the stream_id (its talker registered) | holds the applicant; only it transmits |
| Rider | every other sink settled on the stream_id | VO: no event (received value, LeaveAll, periodic!, tx!), no message, no Lv on its own teardown |

- **Requests and the declared type.** A sink's declaration request (Ready, or Asking Failed on
  a Talker Failed) sets only that sink's own type. The applicant declares the sum of the
  declaring sinks' types: Ready with Asking Failed is Ready Failed (802.1Q-2018 35.1.2.2 a-c,
  Table 35-14; Milan v1.2 4.2.7). New! is applied for the first declarer, and for a changed
  sum, as a change in place (35.2.6).
- **Handover.** When the owner stops declaring while another sink still declares, the next
  of them takes the applicant with its state. The owner may stop by A8, by A15, or because its
  talker withdrew. There is no Lv! and no New! unless the sum changed (35.1.2.2: Lv only for
  streams no longer wanted). On an A15 of the sink holding the applicant, the applicant goes
  to another sink whose record holds the stream_id, instead of being parked.
- **One transmit per walk (round 3).** Each applicant has one transmit opportunity per walk,
  of the walk's kind (tx!, or txLA! after an own LeaveAll), whichever slot holds it (Table
  10-3). The walk marks every slot it passes and every member of a group whose applicant it
  serves, and a handover carries the applicant's mark, so a handover during a walk never gives
  it two. A walk ends only when every slot holds the mark: a slot handed an applicant after the
  walk passed it, from a slot the walk had not reached, makes the walk go round again from
  slot 0, so that applicant has the walk's own tx! or txLA! in that walk.
- **The last declarer.** Its withdrawal is Lv!, and the #188 rules (the owed Leave, the park,
  the settle arms) apply to it unchanged.
- **Unchanged per sink.** The matcher, the registrar (with the Milan 4.2.7.2.2 IN-to-MT rule),
  the EVT_TK_* strobes and the per-sink outputs. `lstn_decl_state` reports the sink's own type
  while its stream's applicant declares, so each sink's GET_RX_STATE is its own.
- **A parked Leave (round 2).** A parked applicant (#188) stays the one applicant of the
  value it holds and is in that value's group. A sink that settles on the parked stream_id is
  a rider of it, and the group's first declaration takes the applicant over: LA or LO + New!
  is VN, the #188 re-probe rule. So one New goes out and no Lv, and the parked sink's own new
  stream is declared. While no sink on the value declares, the owed Lv goes out as before.

The election runs from registered state: a request, a teardown or a handover reaches the
applicant one clock after it is accepted. A group operation waits out any clock that accepts
a settle or a teardown. The cost per sink is two 64-bit comparators (the settle against each
sink's stream_id and against each leave copy), a 64-bit flip-flop copy of the leave copy
(from two sinks), three flip-flops (own type, walk mark) and the election logic, plus an N(N-1)/2-bit same-stream map and an N(N-1)-bit
leave-copy map. No top-level port, parameter or register-map change. The issue #193
implementation changes RTL only inside `KL_srp_listener_fsm`, whose ports are unchanged; the
branch also includes the main merges for #192 and #199.

Area, in the parent's out-of-context synthesis of `KL_pp_shadow` at the module defaults (8
Stream Inputs and 8 Stream Outputs), against processor main 08023123: LUT 56,743 -> 58,046
(+1,303, about 2.3 %) and flip-flops 26,331 -> 26,949 (+618). Of that, round 3 is -32 LUTs
and 0 flip-flops (round 2's head measured 58,078 / 26,949). LUTRAM, block RAM, DSP and carry
are unchanged. This was measured on parent dev 78ca9bdf with the four adoption patches, where
main gives the same figure as in round 2. No 1x1 figure of `KL_pp_shadow` was measured here;
the 4th pin adoption's route-1x1 measures the shipped cost. For the listener FSM alone at one
sink (the same synthesis of that module only): main 2,898 LUTs and 454 flip-flops, this head
2,786 and 455, so -112 LUTs and +1 flip-flop (round 2 alone had measured 2,729 -> 2,798, +69
LUTs, flip-flops unchanged, from 6ddfcda4).

Documented in the design banner and in `docs/architecture/10_srp_engine.md` §5.1 and §6.4
("Sinks on one stream share one declaration").

## Checks (each new check fails under a planted control)

`tb/srp_stream_fsms`, section SH. Every expectation comes from the suite's Table 10-3 model of
ONE applicant.

| Check | Case |
|---|---|
| SH1 | two sinks on one stream: every tx! sends what one applicant sends; the owner holds it and the rider is VO; a received LeaveAll draws no Empty from the rider |
| SH2 | unbind the owner first: the rider takes the applicant in its state, no Lv and no New, periodic! re-joins it; then unbind the rider: one Lv |
| SH3 | the reverse order |
| SH4 | three sinks, each unbind handing the applicant down; the last sends one Lv |
| SH5 | a rider unbinds and settles on another stream: the owner's declaration goes on, the rider declares the new stream |
| SH6 | Ready with Asking Failed: one New, Ready Failed; the Ready owner's unbind hands over with New, Asking Failed; the last unbind: one Lv |
| SH7 | a handover in the middle of a tx! walk: one New in that walk |
| SH8 | the owner's A8 and A15 on consecutive clocks: handed over, not parked |
| SH9 | the owner's A8, then the rider's A15 on the next clock: the first stream gets one Lv |
| SH10-SH13 | a sink alone on the stream re-binds (A15 at once, or A8 then A15) and parks its owed Lv; the other sink settles on the stream and declares before the next tx! (both index orders): it takes the parked applicant over (LA + New! = VN); three ticks each send one New or JoinMt and no Lv; the parker declares its new stream; a peer Registrar fed the pushes stays IN |
| SH14 | the same park, no sink on the stream declaring, a LeaveAll received: the parked Lv goes out once and the rider sends nothing |
| SH15 | the walk sends the parked Lv, then a sink on the stream declares before the walk reaches it: its New waits for the next tx! |
| SH16 | a sink re-binds onto the stream while it owes its own Leave; the stream's declarer then parks the stream: after its own Lv, the sink declares and takes the parked applicant over, so no Lv goes out for the stream, and the walk goes back to it for the New in that walk |
| SH17 | a parked sink re-binds again while another sink declares the stream it re-bound to first: it keeps the pairs of the value it holds, so the next tx! sends that value's one Lv and the other stream goes on as one applicant |
| SH18 | an own LeaveAll's walk passes sink 0, then sink 0 takes the QA applicant over from sink 5 or 7 (clocks 1, 2 and 3): the walk goes back to sink 0 and sends one JoinMt, Ready (QA on txLA! is sJ); the next tx! nothing |
| SH19 | the same in a tx! walk with an AN applicant: the walk sends its New, the next tx! the JoinMt |
| SH20 | an own LeaveAll's walk passes sink 0, then the holder re-binds and hands the applicant to sink 0, which withdraws it: LA on txLA! is LO, so nothing in that walk and Empty, not Lv, at the next tx! |
| SH21 | the walk sends the last declarer's Lv, then a rider ahead of the walk declares: its New waits for the next tx! |
| SH22 | a sink settles on the stream after the walk sent its JoinMt, ahead of the walk: the walk passes it and ends |
| SH23 | two parked Leaves, one on the value the other's matcher is on: an own LeaveAll's walk keeps both parked (LO), and the next tx! sends each one's Empty, no Lv |

`tb/srp_top`, group `share`, through the real decoder, encoder and slot pool:

| Check | Case |
|---|---|
| SW1 | two sinks on one stream: the frame carries ONE Listener VectorAttribute, New Ready, byte-exact against the independent builder |
| SW2 | a Milan v1.2 4.2.7.2.2 peer Registrar model fed every frame: it never deregisters while a sink wants the stream; the last unbind sends one Lv |
| SW3 | Ready with Asking Failed: New with FourPacked Ready Failed, byte-exact; each sink reports its own type |
| SW4-SW7 | the SH10-SH13 forms on the wire: the first frame is the builder's one-value frame (New Ready, no Lv), byte-exact; the next three carry the value once each; the peer Registrar stays IN with no deregistration and no Lv |

Round 1b: twelve new controls in `tb/srp_top/mutants.py` (srp_top campaign), each required to
fail its named check, and the coverage set extended to SH1-SH9 and SW1-SW3 (round 2 adds five
controls and SH10-SH16, SW4-SW7, below). Nine issue #188 controls are
re-anchored on the moved lines with their edits unchanged; `listener-declaration-not-held` now
drops the park term of the declaration grant, which is where a new stream's request is held
while a Leave is parked. Against the base RTL, 26 of the 42 round-1b stream-FSM checks and all 5
wire checks fail.

One existing control changes its edit (round 1b, commit 3). `gsi_mutants.py`'s
`failure-change-redeclares` planted "a FailureInformation change raises a declaration request".
A request now only sets the sink's own type, and New! is applied for a first declarer or a
changed type sum, so that edit no longer changes the wire. The control now plants the same
defect where the New! is decided (a FailureInformation change forces the group's New!), and it
fails the same named check. The behaviour change behind it: a single sink's request of the type
it already declares no longer re-sends New. That is reachable only when a withdrawal and a
re-registration meet before the request is granted.

## Records (round 1b)

Base 21601694 and head 67b90c17 (commits 1-2). Commit 3 changes only `tb/pp_top/gsi_mutants.py`
and `tb/pp_top/README.md`, and the gates that read either were run again at 788425db. The
tools are at the versions the CI and the parent pin.

| Processor gate | Base | Head |
|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,030,237 checks | rc 0, 1,030,284: only `srp_stream_fsms` 1,361 -> 1,403 and `srp_top` 8,660 -> 8,665 |
| `check-req-tags.py --suites --evidence` | rc 0 | rc 0, identical |
| `scripts/lint_hdl.sh`, `scripts/gen_matrix.py --check`, `make check` | rc 0 | rc 0 (also at 788425db); `make check` adds the new links and patch files |
| the portability elaboration of every top, and the elaboration guards graded on it | rc 0 | rc 0, identical but for the converted netlist's line numbers |

| Campaign | Base | Head |
|---|---|---|
| `tb/srp_top/mutants.py` | 179 of 179, coverage 101/101 | 196 of 196, coverage 113/113; the 161 common arm runs keep their verdicts and failing tags |
| `acmp_mutants.py`, `notify_mutants.py`, `aecp_mutants.py`, `aecp_dispatch_mutants.py`, `ctr_mutants.py`, `name_wr_mutant.py`, `tb/name_state` and `tb/elab_guards` mutants | rc 0 | rc 0, identical |
| `d3_mutants.py` | 110 of 110 | 110 of 110, identical |
| `gsi_mutants.py` | 20 detected | 20 detected at 788425db, identical (at 67b90c17 the old edit survived: the reason for commit 3) |

Processor main has since moved to 08023123 (#197), which also edits `tb/pp_top/gsi_mutants.py`
and `tb/pp_top/README.md`; the branch merges with it without conflict, and on that merge
`tb/pp_top` passes (10,721 checks) and the gsi campaign detects all 23 of its controls.

Consumer gates on a scratch parent (milan-fpga dev e26f1816 with the three adoption patches,
the processor gitlink at each pin): every gate is rc 0 at base and head except
`check_submodule_docs`, which fails identically at both ("documented pin differs from Git").
`milan_dp` keeps 10,465 `[ok]` and 1,127 `[PASS]`, 0 `[FAIL]`, with identical check lines;
`pp_shadow` keeps 2,184 checks, 0 failures; the ROM digests are unchanged. The parent's resource
gate that needs a place-and-route measurement was not run.

## Round 2

Five commits on 6ddfcda4, answering the two reviews of the round-1b head.

- **A parked Leave and a new declarer of its stream (both reviews' F1).** A sink alone on a
  stream re-binds away and parks its owed Lv (#188); another sink settles on that stream and
  declares it before the next tx!. The parked applicant was in no group, so the new sink
  created a second applicant for the value: one MRPDU carried New and Lv for it, and a Milan
  4.2.7.2.2 peer registrar deregistered it while the sink wanted it. The parked applicant is now
  in the group of the value it holds (by its leave copy). The new sink is a rider of that
  group, and its first declaration takes the applicant over through the existing handover:
  LA + New! = VN, the #188 re-probe rule. When no sink on the value declares, the owed Lv goes
  out unchanged. When it has gone out in a walk, the sinks on the value take its walk mark,
  so a declaration later in that walk waits for the next tx!. The banner and 10 §6.4 ("A
  parked Leave") describe it.
- **The area figure's shape (F2).** Stated above, beside the figure: the module defaults, 8
  Stream Inputs and 8 Stream Outputs. No 1x1 figure was measured here; the 4th pin
  adoption's route-1x1 measures the shipped cost.
- **Citations and labels (F3, F4).** The two type-sum test comments cite 35.1.2.2 and
  35.2.4.4.3 (Table 35-14), keeping 35.2.6 for the change in place, and the two new check
  labels in source comments are gone.
- **A handover to a slot the walk has passed (S2).** Probed with an AN holder in a tx! walk:
  the message went at the next tx!. R679-2 (F1) found that in a txLA! walk the LeaveAll
  re-declaration was lost instead, and corrects it (below); the banner and 10 §6.4 no longer describe a delay.
- **The leave-copy write (commit 4).** The first form wrote the compare copy at a variable
  index of a packed array, which synthesized as a shifter. One enable per sink brings the
  listener alone at 8 sinks from +2,251 to +322 LUTs over 6ddfcda4.
- **README counts (commit 5).** The srp_top README's failing totals of three shared-stream
  controls now count the new checks too.

Both reviews' parked-Leave probes now pass on the head: every variant gives one value per
tick, no Lv while the joiner declares, and the peer IN with no deregistration. On 6ddfcda4
they fail as reported.

New checks SH10-SH16 and SW4-SW7 (tables above) fail against the 6ddfcda4 RTL: all 7 and all 4.
Five new controls in the srp_top campaign, each required to fail its named check:
`listener-parked-outside-groups` (SH10-SH16, SW4-SW7), `listener-settle-skips-leave-copies`
(SH10-SH15, SW4-SW7), `listener-merge-keeps-park` (SH10-SH13), `listener-retire-skips-group-mark`
(SH15), and `listener-park-drops-matcher-pairs` (SH16). One control,
`listener-settle-compare-dropped`, is re-anchored with its edit unchanged. The coverage set is
now SH1-SH16 and SW1-SW7.

Round 2 records: base 6ddfcda4, head 57fb7dd2 (commits 1-4). Commit 5 (7b424cdf) changes only
`tb/srp_top/README.md`, and the gates that read it were run again there: all identical. The
tools are at the versions the CI and the parent pin.

| Processor gate | Base 6ddfcda4 | Head |
|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,030,356 checks | rc 0, 1,030,367: only `srp_stream_fsms` 1,403 -> 1,410 and `srp_top` 8,665 -> 8,669 |
| `check-req-tags.py --suites --evidence` | rc 0 | rc 0, identical |
| `scripts/lint_hdl.sh`, `scripts/gen_matrix.py --check`, `make check` | rc 0 | rc 0 at both heads; `make check` counts the five new patch files |
| the portability elaboration of every top, and the elaboration guards graded on it | rc 0 | rc 0, identical |

| Campaign | Base | Head |
|---|---|---|
| `tb/srp_top/mutants.py` | 196 of 196, coverage 113/113 | 203 of 203, coverage 124/124; every base arm keeps its verdict and tags (nine gain tags of the new checks) |
| `acmp_mutants.py`, `notify_mutants.py`, `aecp_dispatch_mutants.py`, `ctr_mutants.py`, `gsi_mutants.py`, `name_wr_mutant.py`, `tb/name_state` and `tb/elab_guards` mutants | rc 0 | rc 0, identical |
| `d3_mutants.py`, `aecp_mutants.py` | rc 0, 110 of 110; 67 | rc 0, 110 of 110; 67, identical |

Consumer gates on a scratch parent (milan-fpga dev 78ca9bdf with the four adoption patches,
the processor gitlink at each pin): every gate is rc 0 at the base and the head except
`check_submodule_docs`, which fails identically at both ("documented pin differs from Git").
`milan_dp` keeps 10,559 `[ok]` and 1,127 `[PASS]`, 0 `[FAIL]`, with identical check lines.
`pp_shadow` keeps 2,184 checks with 0 failures, and the ROM digests are unchanged. The parent's
place-and-route resource gate was not run.

## Round 3

Six commits on 7b424cdf, answering the two reviews of the round-2 head.

- **A handover behind the walk (R679-2-F1).** In an own LeaveAll's walk (txLA!), a QA
  applicant handed over to a slot the walk had already passed, from a slot it had not reached,
  had no transmit in that walk, and the next walk's plain tx! sends nothing from QA: the
  LeaveAll re-declaration (QA on txLA! is sJ, 802.1Q-2018 Table 10-3) was lost until the next
  periodic!. In a plain tx! walk the same handover sent an AN or VN applicant's New a tick
  late. Now each applicant has one transmit opportunity per walk, of the walk's kind,
  whichever slot holds it. The walk mark means "the walk has passed this slot, or its
  applicant has had its transmit", and a handover still carries it; so once the walk has
  passed every slot, a slot without the mark is one that took an applicant not yet served
  after the walk passed it. A walk ends only when every slot holds the mark; otherwise it goes
  round again from slot 0, each marked slot passing in one clock, and serves that slot with
  the walk's own tx! or txLA!. An ordinary walk ends exactly as before.
  Why this form: carrying an owed txLA! into the passed slot needs a flip-flop per sink and
  still sends the transmit a tick late; serving the taker at the giver's slot fails when the
  giver leaves the group in that clock (an A15 handover, a parked takeover) and needs the
  taker's index kept per slot. The walk mark already says which slots the walk still owes.
- **A rider declaring after the last declarer's Lv (found in this round).** The walk sent the
  last declarer's Lv, then a rider ahead of the walk declared before the walk reached it, and
  that walk sent New beside the Lv for the same StreamID. The walk now marks every member of a
  group whose applicant it serves (round 2 did so for a retired park only), so the New waits
  for the next tx!, as one applicant's would. A txLA! that leaves the applicant LO leaves it
  where it is, and a handover from there carries the mark.
- **A second park (F2).** SH17 commits R679-2's re-park case, with the edit it names as its
  control.
- **The README row (R1)** is corrected as written.
- **Two parks (S1).** SH23 pins the both-parked exclusion, with a control.
- **The two-sink compares (S2).** Measured and not kept: reading `lsid_r` at two sinks gave
  `KL_pp_shadow` at 2 Stream Inputs x 8 Stream Outputs +99 LUTs and -128 flip-flops, so it is
  not area-neutral; commit 5 takes it out again (at 8 sinks the RTL is the same either way).
- **A test comment (R680-2-S1)** no longer carries two check IDs.

Area: the figures under Behaviour above (8x8 `KL_pp_shadow` 58,046 LUTs, 26,949 flip-flops;
+1,303 and +618 against main, -32 and 0 against round 2's head).

New checks (tables above): SH16 now expects the New in the walk that serves the takeover, and
SH17-SH23 are new. Against the 7b424cdf RTL, SH16, both SH18 checks, SH19, SH20 and SH21 fail;
SH17 and SH23 guard terms the base already has, and SH22 guards the end of a walk, which the
base cannot miss. Five new controls, each required to fail its
named check: `listener-walk-ends-owing-a-transmit` (SH16, SH18, SH19, SH20),
`listener-walk-marks-only-served-slots` (SH22: the walk never ends),
`listener-walk-marks-group-only-on-retire` (SH21), `listener-repark-takes-matcher-pairs` (SH17)
and `listener-two-parks-grouped` (SH23). `listener-retire-skips-group-mark` and
`listener-park-never-retires` are re-anchored with their edits unchanged. The coverage set is
now SH1-SH23 and SW1-SW7. Seven shared-stream controls fail more checks now, and their
README counts say so.

One existing control changes its named check. `listener-rider-not-quiet` (every rider takes
events) was required to fail SH1's received-LeaveAll check, where the rider sits above the
owner. The owner's transmit now marks that rider, so its Empty cannot go out in that walk,
and SH1 no longer sees the edit. The control is now required to fail SH14, which grades the
same rule with the rider below the parked holder; it fails 12 checks in all.

R679-2's own probes on the head: `s2_probe.py` gives MATCH in every row (both holders, tx! and
txLA!, the handover at clocks 1-3, and both controls); on 7b424cdf its six txLA! handover rows
read DIFF as reported. `repark_probe.py` gives MATCH, and with its planted edit the suite now
fails (SH17). Its control campaign now kills its re-park and both-parked arms in the
stream-FSM suite.

Round 3 records: base 7b424cdf (round 2's head records, the same executable inputs), head
324ac9a7. The processor gates ran at 65d39b0c, and the gates that read the docs ran again at
324ac9a7, identical; 324ac9a7 changes only `tb/srp_top/README.md` and one required tag in
`tb/srp_top/mutants.py`. Every campaign ran at 324ac9a7. The tools are at the versions the CI
and the parent pin.

| Processor gate | Base 7b424cdf | Head |
|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,030,367 checks | rc 0, 1,030,375: only `srp_stream_fsms` 1,410 -> 1,418 |
| `check-req-tags.py --suites --evidence` | rc 0 | rc 0, identical |
| `scripts/lint_hdl.sh`, `scripts/gen_matrix.py --check`, `make check` | rc 0 | rc 0; `make check` counts the five new patch files |
| the portability elaboration of every top, and the elaboration guards graded on it | rc 0 | rc 0, identical |

| Campaign | Base | Head |
|---|---|---|
| `tb/srp_top/mutants.py` | 203 of 203, coverage 124/124 | 208 of 208, coverage 131/131. 174 arm runs keep their verdict and tags; nine gain tags of the new checks; one fails one more line of the same checks; `listener-rider-not-quiet` now names SH14; five new arm runs |
| `acmp_mutants.py`, `notify_mutants.py`, `d3_mutants.py`, `aecp_mutants.py`, `aecp_dispatch_mutants.py`, `ctr_mutants.py`, `gsi_mutants.py`, `name_wr_mutant.py`, `tb/name_state` and `tb/elab_guards` mutants | rc 0 | rc 0, identical |

The parent's consumer gates were not run in this round; the manager runs them. The area
figures above are the parent-side records of this round.

## Round 4

Three commits on 47434635 (round 3's head with the merge of main 859b537b), answering the two
reviews of round 3. Tests and docs only: the RTL logic is unchanged (one commit edits comment
lines of `KL_srp_listener_fsm.sv`; the listener converted to Verilog at 47434635 and at the
head is byte-identical), so the area figures above stand.

- **The done strobe's wait for the second pass (R679-3-F1).** SH24 checks that a walk's
  Listener pushes all come before its done strobe. Sink 4 takes sink 7's applicant over at
  clock 1 to 12 of a tx! walk (AN) or an own LeaveAll's walk (QA): ahead of the walk, behind it
  (the second pass from slot 0 needs more than 2 clocks to reach sink 4) or after it ended.
  Each walk must send one message for the stream, the model's, before the strobe, and nothing
  in the 60 clocks after it, since `KL_srp_top` drains the encoder on the strobe. Its control,
  `listener-walk-done-before-second-pass`, is the edit the finding names (`txop_done_o <=
  1'b1` in W_DONE, the second pass kept), required to fail SH24. R679-3's order probe reports
  LATE 0 in its 72 rows at the head, and LATE 32 with the control planted.
- **A review round named in a README (R679-3-R1)** is corrected as written.
- **The finder of the S2 case (R679-3-R2)** is corrected as written, in the Round 2 section.
- **The group mark's LA/LO exception (R679-3-S1)** is now stated in the banner and 10 §6.4.
- **SH1's rider (R679-3-S2).** SH1's received-LeaveAll check runs one more tick. With
  `listener-rider-not-quiet` planted, that alone does not fail: the rider above the owner goes
  to LO and stays there, and its Empty never goes out, because the owner's transmit marks the
  group in every walk. So SH1 also requires the rider to stay VO after those ticks. With the
  edit SH1 fails again ("rider LO"). The control stays required to fail SH14 and fails 15
  checks.
- **The implementation's scope (R680-3-R1).** The sentence under Behaviour now separates the
  issue's RTL edits from the main merges, and the opening lists the merge of main 859b537b.

Round 4 records: base 47434635, head 4f57e220, each gate run in a clean clone at each, with
the tools at the versions the CI pins.

| Processor gate | Base 47434635 | Head |
|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,030,395 checks | rc 0, 1,030,399: only `srp_stream_fsms` 1,418 -> 1,422 (SH24 x2, SH1 +2) |
| `check-req-tags.py --suites --evidence` | rc 0 | rc 0, identical |
| `scripts/lint_hdl.sh`, `scripts/gen_matrix.py --check`, `make check` | rc 0 | rc 0; `make check` counts the new patch file |
| the portability elaboration of every top, and the elaboration guards graded on it | rc 0 | rc 0, identical |

| Campaign | Base (324ac9a7's records; the merge changes nothing it builds) | Head |
|---|---|---|
| `tb/srp_top/mutants.py` | 208 of 208, coverage 131/131 | 209 of 209, coverage 132/132. 182 arm runs keep their verdict and tags; six fail more checks (SH24, and SH1 for three of them), and the README counts say so; the new control is KILLED on SH24 |

The pp_top, name_state and elaboration-guard campaigns and the parent's consumer gates were
not run in this round; they build the listener, whose change is comment lines only, and the
manager runs the banks.

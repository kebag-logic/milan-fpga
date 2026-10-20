[A661] SRP listener: sinks settled on one stream_id share one declaring Listener applicant, by owner election in the per-sink plane (#193)

Closes #193

Three commits on main 21601694. The round-1 measurement (on #193) found two Listener
VectorAttributes with the same FirstValue in one MRPDU when two sinks were settled on one
StreamID, and a Leave for the value when one of them unbound. The ruling on #193 asked for
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
  to another sink whose record holds the stream_id, instead of being parked. The applicant
  carries its walk mark, so a handover in the middle of a tx! walk never gives it two tx!.
- **The last declarer.** Its withdrawal is Lv!, and the #188 rules (the owed Leave, the park,
  the settle arms) apply to it unchanged.
- **Unchanged per sink.** The matcher, the registrar (with the Milan 4.2.7.2.2 IN-to-MT rule),
  the EVT_TK_* strobes and the per-sink outputs. `lstn_decl_state` reports the sink's own type
  while its stream's applicant declares, so each sink's GET_RX_STATE is its own.

The election runs from registered state: a request, a teardown or a handover reaches the
applicant one clock after it is accepted. A group operation waits out any clock that accepts
a settle or a teardown. The cost per sink is one 64-bit comparator (the settle against each
sink's stream_id), three flip-flops (own type, walk mark) and the election logic, plus an
N(N-1)/2-bit same-stream map. No top-level port, parameter or register-map change: every RTL
edit is inside `KL_srp_listener_fsm`, and its ports are unchanged. In the parent's
out-of-context synthesis of `KL_pp_shadow` the election costs 1,037 LUTs and 50 flip-flops (LUT
56,501 -> 57,538, about 1.8 %); LUTRAM, block RAM, DSP and carry are unchanged.

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

`tb/srp_top`, group `share`, through the real decoder, encoder and slot pool:

| Check | Case |
|---|---|
| SW1 | two sinks on one stream: the frame carries ONE Listener VectorAttribute, New Ready, byte-exact against the independent builder |
| SW2 | a Milan v1.2 4.2.7.2.2 peer Registrar model fed every frame: it never deregisters while a sink wants the stream; the last unbind sends one Lv |
| SW3 | Ready with Asking Failed: New with FourPacked Ready Failed, byte-exact; each sink reports its own type |

Twelve new controls in `tb/srp_top/mutants.py` (srp_top campaign), each required to fail its
named check, and the coverage set extended to SH1-SH9 and SW1-SW3. Nine issue #188 controls are
re-anchored on the moved lines with their edits unchanged; `listener-declaration-not-held` now
drops the park term of the declaration grant, which is where a new stream's request is held
while a Leave is parked. Against the base RTL, 26 of the 42 new stream-FSM checks and all 5 wire
checks fail.

One existing control changes its edit (commit 3). `gsi_mutants.py`'s
`failure-change-redeclares` planted "a FailureInformation change raises a declaration request".
A request now only sets the sink's own type, and New! is applied for a first declarer or a
changed type sum, so that edit no longer changes the wire. The control now plants the same
defect where the New! is decided (a FailureInformation change forces the group's New!), and it
fails the same named check. The behaviour change behind it: a single sink's request of the type
it already declares no longer re-sends New. That is reachable only when a withdrawal and a
re-registration meet before the request is granted.

## Records

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

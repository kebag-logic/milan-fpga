[A661] #193: STOP at the measurement step. No change proposed; do not open a PR from this branch.

The branch `193-shared-listener-leave` has no commits over processor main 21601694, so
there is nothing to merge. This file records the outcome for whoever opens the follow-up
lane. It does not close #193.

## Measurement (assignment item 1)

Two sinks were settled on one StreamID in the srp_top suite bench (real KL_srp_top,
encoder and TX slot pool). The DUT's MSRP frame then carries **two** Listener
VectorAttributes with the same FirstValue:

```
01 80 c2 00 00 0e 0a 0b 0c 0d 0e 0f 22 ea 00 03 08 00 1a
00 01 11 22 33 44 55 66 00 01 00 80
00 01 11 22 33 44 55 66 00 01 00 80
00 00 00 00
```

This is New, Ready twice for stream_id 11:22:33:44:55:66:00:01. The JoinMt frame that
follows repeats the value the same way. The transmit path does not merge the two:

- each sink owns a Table 10-3 applicant (`hdl/srp/KL_srp_listener_fsm.sv:365-374`);
- the walk pushes one event per sink (`:731-736`);
- the encoder folds only +1 successors into a run (`hdl/srp/KL_srp_encoder.sv:186-214`),
  so an equal value becomes a second VectorAttribute.

This conflicts with IEEE 802.1Q-2018 10.7.7 (one Applicant per attribute value) and the
35.2.6 NOTE (at most one Listener Declaration per StreamID per port). The assignment
routes that case to a STOP: the fix is a one-applicant-per-StreamID redesign of the
listener applicant plane, which is a manager decision.

The same run also reproduces the reported behaviour. Unbinding one of the two sinks
sends a Lv for the value. The remaining sink re-declares it only with the next periodic
JoinMt, about 0.6 s later in the bench, and a Milan v1.2 4.2.7.2.2 peer registrar
deregisters in between.

## Acceptance items of #193

- Teardown withdraws only when no other settled sink declares the StreamID: not done (STOP).
- Suite cases for two sinks on one stream, each with a planted mutant: not done (STOP).
- Processor suites and consumer gates: not run, because nothing changed.

[A529]

## Contents

- **[Status](#status)** -- STOP at item 1; no PR is opened from this lane.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What was measured and why nothing is proposed for merge.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Commands to reproduce the base trace.
- **[How to validate](#how-to-validate)** -- Exact commands and the expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

STOP. No commit, no PR: `653-unbind-order` is still at dev `fea346e7` (processor pin `631eeb34`).

The base trace does not reproduce the reported order. Item 1 of the lane says
to STOP in that case.

## Linked Issue / roles

Relates to #653

Executor: `[A529]`
Internal cleared-context reviewer: `[R470]`
External reviewer: `[R471]`

## Description

A bench section, `[UNB]`, was added locally to the timed notify leg of
`tb/verilator/milan_dp` (the shipping AX 1x1 shape). It was not committed.
For the AAF input 0 and the CRF input 1 it does the following:

- binds, settles the probe and locks off real PDUs;
- keeps the talker live;
- waits until the row's one-second limiter is open, then unbinds;
- stamps every event cycle, from the UNBIND_RX command's last byte.

| Event | AAF sink 0 | CRF sink 1 |
|---|---|---|
| response queued by the listener | +193 | +193 |
| debounced bind level falls | +199 | +199 |
| MEDIA_UNLOCKED written | +204 | +9,818,177 (100 ms silence timeout) |
| UNBIND_RX response leaves | +277 | +277 |
| GET_STREAM_INFO push to A / B | +887 / +1,497 | +887 / +1,497 |
| GET_COUNTERS push reporting the unlock, to A / B | +2,294 / +3,057 | +9,819,137 / +9,819,900 |

On both inputs the response leaves first. The order is structural at this
pin:

- the listener queues the response (`KL_pp_acmp_listener.sv:1378-1379`)
  before the debounced bind level can fall
  (`protocol_processor_top.sv:948-952`);
- every unlock source reads that level;
- ACMP holds the top TX class (`protocol_processor_top.sv:4453`) on the
  processor's single TX stream.

Separately, the CRF input violates the Section 5.3.8.10 pair for up to 100 ms
after an unbind:

- `KL_crf_rx` counts the unlock only at its silence timeout
  (`KL_crf_rx.sv:533-536`);
- a GET_COUNTERS right after the response reads MEDIA_LOCKED 1 and
  MEDIA_UNLOCKED 0.

This is reported for a decision, not fixed here.

## Authoritative references

- Milan v1.2 Section 5.3.8.10 (Table 5.6), Section 5.4.5 (Table 5.22), Section 5.4.5.3
- #653 and its lane comment (issuecomment-5980090994)

## How to get into the same state

```sh
git checkout fea346e76c2a57ed5cd131af8fc68dfeff57f877
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
git apply 653-unb-repro-sim_nxn.patch   # from the lane's output directory
```

## How to validate

```sh
cd tb/verilator/milan_dp
make notify-build VERILATOR_JOBS=16    # Verilator 5.050
./obj_notify/Vmilan_dp_notify | grep '\[UNB\]'
```

Expected result:

- `checks: 417 failures: 1`, exit 1;
- the one failure is the CRF U3 check;
- the two `[i] [UNB] ... trace` lines carry the cycles in the table above.

## Known limitations / out of scope

- No fix (item 2), CRF fix (item 3), committed test, planted control or area
  figure (items 4-5): item 1's STOP precedes them.
- The bench sees the DUT's MAC TX, not the controller. A port capture of one
  disconnect on the bench is what would discriminate the report.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

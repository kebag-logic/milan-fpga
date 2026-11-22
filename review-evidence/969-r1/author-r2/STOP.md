[A817] STOP: round 2 at ecd5bf411a69e9e5cb37c99ec357b48ee8d3bfa4. The CPU budget needs an owner decision: a record that registers Talkers is past the stated SRP unit at 1x1/1if and 8x8/1if, the kept ones as the bound ones the base already registers, and restating the unit breaks owner bounds

Branch `pf-969-1` (PR #971's `969-srp-kept-talkers`): 12 local commits on `f863258d`, not pushed. Round 2 answers R886-1 and R885-1. Three findings are fixed with evidence. The fourth, R885-1-F1, is now measured, and the measurement needs a decision before this PR can be review-ready.

**Fixed**

- **R886-1-F1 / R885-1-F3 (the stale kept count).**
  - `count_kept` now counts again before a receive when a binding changed, or when one kept may have ended and a pool block was returned since. `SRP_KEPT_PENDING` is set by a Talker kept now, by an unbound registration's end, and by a counted one whose Registrar left.
  - `reset_interface` zeroes the count with the participants it destroys. The zeroing grows that hot function by 16 B, so the 152 hot functions after it each start 16 B later. Nothing else in the hot section moves.
  - Both reviewers' reset and reclaim probes, and three new tests, fail at `f863258d` and pass at the head, at 1x1 and 8x8 with one and two interfaces. The fresh, flood and UNBIND/BIND controls pass at both.
  - Five plants cover the count's triggers. The reviewers' reset probes alone would also pass on the pending flag, so the head's reset test refreshes the kept one first: only the zeroing passes it, and its plant is caught. That plant escaped the gate's first run before this fix.
- **R886-1-F2 / R885-1-F4.** The 8x8/1if SRP campaign plants all 16 early defects. Shard 3 shows 48 early-plant results, 16 at each of 1x1 with one interface, 1x1 with two, and 8x8/1if, each line naming its shape.
- **R886-1-F3 / R885-1-F2.** Every memory-doc line both rounds list now states the ledger's figures.
- **Gates.** The firmware is final since `f02d44cd`.
  - Firmware gate shards 0 and 3 PASS at the head (88 arms; 591 caught, 0 escaped). Shards 1 and 2 PASS at `f02d44cd` (827 of 827; 385 caught). Nothing those shards read changed after `f02d44cd`.
  - Coverage PASS (`srp_mbx.c` 861/861 lines, 779/779 branches).
  - plat_ledger and test_ctrl_memory PASS (45.5 / 46 / 58.5 / 63.5 RAMB36). The twin and its plants PASS.
  - Docs workflow: 99 of 103, the 4 CI-environment rows failing as on the base.
  - Routes at 1x1/1if and 8x8/1if meet #818's floor (worst WNS +0.128 and +0.096 ns).
  - flip_grade, load_grade and shape_costs PASS on the stated figures.

**The STOP (R885-1-F1).** A new arm-A group, `srp-kept` (`kept_window.py`, graded by `kept_grade.py`), runs the changed paths at both points. A scratch group (not committed) binds every input first and then sends the same MRPDU. That is the bound path the base has, measured on the same image: #969 adds to that record only the one count the bindings owe, a visit of the participant's few attributes at that point. Each SRP record (`srp_mbx:receive`) is converted by the stated rule:

| Point | Record | CPU cycles | By the rule | `CTRL_LOOP_SRP_UNIT_US` |
|---|---|---:|---:|---:|
| 1x1/1if | every input's Talker Advertise, no binding (kept) | 34,497 | 365 µs | 285 µs |
| 1x1/1if | the count again after a freed block, Talkers past the bound in the same record | 32,224 | 340 µs | 285 µs |
| 1x1/1if | every input's Talker Failed after a reset (kept) | 36,859 | 390 µs | 285 µs |
| 1x1/1if | every input's Talker Advertise, every input bound (scratch; the bound path) | 38,956 | 410 µs | 285 µs |
| 8x8/1if | every input's Talker Advertise, no binding (kept) | 137,352 | 1,445 µs | 375 µs |
| 8x8/1if | the count again after a freed block, Talkers past the bound in the same record | 68,692 | 725 µs | 375 µs |
| 8x8/1if | every input's Talker Failed after a reset (kept) | 142,909 | 1,505 µs | 375 µs |
| 8x8/1if | every input's Talker Advertise, every input bound (scratch; the bound path) | 153,208 | 1,610 µs | 375 µs |

The harness's own grading refuses the bound records too. At 1x1/1if: `an SRP record's apply of 38,625 CPU cycles, over its stated 28,500`. At 8x8/1if: `152,856 ... over its stated 37,500`, and `a tier-2 slice of SRP's records of 157,372 CPU cycles, over the stated slice 147,500`.

Each Talker attribute lwSRP registers costs on average about 15,000 to 17,000 CPU cycles. So a record that registers more than one or two Talkers is past the unit, whether they are bound (a bridge re-declaring them after any LeaveAll, as at the base) or kept (#969, before the bindings, a cheaper record than the bound one). The stated unit never covered a registration: the harness had never sent a peer Talker.

Restated by the stated rule to the group's dearest record (a scratch copy only, nothing committed), 1x1/1if's "last" row becomes 185.89 ms, past its 130 ms bound and the owner's 140 ms. 8x8/1if's load becomes 1.309 against its 0.75 ceiling, and its 1,505 µs record no longer fits the 1,475 µs slice. Those are owner bounds, and this task may not move them.

The rest of the group is within its statements:

- The build that answers the LeaveAll with In for every kept Talker (2 and 9 values) is the heaviest build pass: 39,123 of 73,500 and 82,768 of 147,500 CPU cycles. The LeaveAll itself goes out at its first transmit opportunity.
- No work pass exceeds the 2 ms share.
- Round 1's five groups, against the base, keep the same 7 owed backlog-owed misses and no others.

**Decision requested** (no change made toward any option):

1. Rule that the cost of a record registering Talkers is a pre-existing gap of the CPU budget's statements, measured on the bound path and owed to an Issue of its own (a restated unit and load model, or a cheaper lwSRP registration), and that #969 may proceed, since its kept records are cheaper than the bound records the base already makes. If so, round 2 becomes review-ready with the srp-kept group as the measurement, and the bound group could be committed beside it.
2. Require #969's records within the present unit. That needs a redesign: keep the kept Talkers' values in the adapter instead of as lwSRP attributes, as the release processor's port registrars hold {stream_id, DA, VLAN} (`KL_srp_listener_fsm.sv`, protocol-processor #212), and register the one Talker a binding takes when the binding is made. The kept values would have to age with the talker's Leave and LeaveAll, and the registration would reach lwSRP as a synthesized JoinIn through `mrp_rx` outside callbacks. That is a decision on synthesized registrations.
3. Bound how many Talkers one record keeps, and let the rest wait. The refused ones are lost until the talker's next declaration (the #969 symptom for them), unless lwSRP's storage-refusal replay splits the record, which is an allocator-level change.

The receipts (failing-first, plants, ledger, firmware shards, coverage, twin, docs, routes, the CPU budget groups and their gradings, the scratch bound group and the scratch restatement) are in round 2's packet for the manager.

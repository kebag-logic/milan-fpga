[A817]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**Green**, ready for review at `c113018d`, stacked on PR #960's head `dd163e41`. The cost of a record that
registers Talkers is **owed to #977** by the owner's ruling on #969 (2026-11-22): both CPU budget groups that measure
it are graded as owed, under the conditions below, and no unit or row is restated (Known limitations, CPU budget).
Firmware gate 4 of 4 shards, coverage, ledger, twin and plants, docs workflow (99 of 103, the 4 rows that need the
CI environment as on the base), routes at 1x1/1if and 8x8/1if meeting #818's floor. Round 3 changes only the CPU
budget grader `kept_grade.py` and three documents; no firmware source has changed since `f02d44cd`.
`969-srp-kept-talkers` -> `dev-soft-core`.

## Linked Issue / roles

Closes #969
Relates to #665

Executor: `[A817]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

**Cause.** ACMP asks SRP to bind a STREAM_INPUT only once the talker answers its probe (Milan v1.2 5.5.3.5.18
step 4; tsn-c-stack `acmp.c` `probe_response`), after a power-on settle of a saved binding and after BIND_RX alike.
Until then the sink has no SRP binding, and the MSRP receive filter (`srp_mbx.c` `interested_msrp`) refused every
Talker attribute of a StreamID no binding held, before lwSRP allocated anything. A Talker declared before the
binding was therefore never in the registrar. The walk a binding owes found nothing, and the talker's applicant
stays quiet (QA, IEEE 802.1Q-2018 Table 10-3) until a LeaveAll, so the Listener waited up to a LeaveAll period.
UNBIND_RX then BIND_RX worked only because the old binding's registration was still held. The release processor
keeps N port registrars for exactly this (`KL_srp_listener_fsm.sv`, protocol-processor #212); the split firmware
did not.

**Fix (split firmware only; no mailbox-contract, lwSRP or RTL change).**

| Piece | Change |
|---|---|
| `srp_mbx.c` `interested_msrp`, `keep_talker` | A Talker of a StreamID none of the interface's bindings holds is kept: one already kept, or while the interface keeps fewer than `SRP_KEPT_TALKERS`, one per STREAM_INPUT of the shape (the processor's count). Past the bound the old behaviour. One kept now leaves the count pending (`SRP_KEPT_PENDING`): it may end with no registration. |
| `srp_mbx.c` `count_kept`, `kept_visited`, `apply_receive` | The kept count is made again before a receive, outside lwSRP's callbacks, when a binding changed since the last count (`SRP_KEPT_BOUND`), or when one counted or kept since may have ended and a pool block was returned since (`SRP_KEPT_PENDING`: a kept one kept now, a registration of an unbound StreamID that ended, a counted one whose Registrar left). It counts every Talker the participant does not declare whose StreamID no binding holds, registered or left with its block not yet freed. So a receive starts from exactly the kept attributes the participant holds, below the bound as at it, and with nothing pending a returned block owes no count. The walk neither reads nor writes it, so the walk's schedule (#930) moves no filter answer. |
| `srp_mbx.c` `talker_changed` | A StreamID no binding holds is held (#925's `srp_held`) from a registration it is kept for, with the kind registered latest, so a binding made later takes the latest of two kinds (the #925 ruling). An unbound StreamID's indication owes no walk; its registration's end leaves the kept count pending. |
| `srp_mbx.c` `reset_interface` | The kept count is zeroed with the participants a reset destroys, beside the release of the interface's held StreamIDs. |
| `srp_mbx.c` `srp_mbx_bind` | A binding change owes the next receive's count. |
| `srp_mbx.h` | `SRP_KEPT_TALKERS`, `struct srp_kept`, the kept tables and `kept_due` before `held` (which stays last so the code reading the rest compiles as before), `SRP_HELD_STREAMS` grown by half the kept bound. The pool is unchanged: its fixed 16 medium blocks an interface fund the kept beside the Domain's and the default VID's (a static assertion holds the sum). |
| `sw/litex/ctrl_memory*.py`, `test_ctrl_memory.py` | The platform's 8x8 images at 58.5 and 63.5 RAMB36 (872 and 408 B of `rom` past 58.0 and 63.0), refused at 59.0 and 64.0, `ctrl_plat` as measured, by the owner's rule of 2026-11-15 (ROM debt owed to S14). |
| CPU budget harness | Two groups in arm A at every point (`kept_window.py`): `srp-kept` runs the changed paths, and `srp-bound`, the bound path the base has, sends the same MRPDU with every input bound. `kept_grade.py` grades both as owed to #977 under the ruling's conditions, each read from the logs it grades (THE SHARE too, never a result file beside them), and `run.py` gives its STATED and SHARE lines the same disposition (`kept_grade.Disposition`). Its `--selftest` (19 checks) breaks every condition in synthetic logs, through `held`, `Disposition` and the standalone entry point. |
| Docs | `srp/README.md` (filter, pool, held, the kept Talkers and their count's exactness, processor comparison D4), `plat/README.md`, `SPLIT_CONTROL_MEMORY.md` (entries, planted ledgers, figures), `ctrl_memory_ledger.py`'s docstring, `ctrl_split_boot/README.md`. |

**Tests.**

| Test | What it holds |
|---|---|
| `srp_mbx.cpp` `SrpEarlyTalker.*` (1x1 and 8x8, one and two interfaces) | On every STREAM_INPUT: registration then binding at a power-on's spacing (Advertise -> Ready, Failed -> Asking Failed) in THE TRANSMIT's next MRPDU within a JoinTime, and ACMP's copy; binding then registration with the kept at their bound; BIND_RX while bound to a stream declared all along; the latest of two kinds; a JoinIn replacement; an ended registration (Lv, an unanswered LeaveAll, a reset) declares nothing; the bound; an unbinding's registration kept and counted; a kept one that left counted until its block is freed |
| `test_plat_sinks.cpp` `Early.S13` (8x8/1if, 1x1/1if) | Every STREAM_INPUT's saved binding restored at a power cut; the talker declares (Advertise, then Failed) before it is discovered and probed, then is quiet; once each probe is answered the Listener is declared in THE TRANSMIT's next MRPDU within a JoinTime, and GET_STREAM_INFO shows REGISTERING (flags_ex) and REGISTERING_FAILED (flags) (Milan v1.2 Tables 5.9, 5.10) |
| `test_plat_sinks.cpp` `Early.S14` | The same after BIND_RX while bound to another stream whose Talker was declared all along |
| `srp_mbx.cpp` `SrpEarlyTalker` (1x1 and 8x8, one and two interfaces), the count's exactness | One receive of every input's Talker, one vector of them or a message each, kept whole: into a fresh registrar; after a reset with one kept below the bound; after a kept one left and its block was freed, 400 ms and 5.1 s after its Leave; after a Leave kept for a StreamID never registered; beside a kept one refreshed in one receive and across receives. Controls: 1,000 unbound Talkers at the receive rate keep at most the bound, refuse nothing and owe no walk, and every input bound later declares; UNBIND_RX then BIND_RX on every input. The reset and freed-block cases are both reviewers' probes. |
| Restated: `Srp.ReadyFailedAndUninterestingStreamsAreSeparated`, `SrpTalkerKinds.AHeldStreamEndsWithEitherRegistrationOrAReset` | An unbound Talker now takes one block; a held stream's registration ends by an unanswered LeaveAll (a JoinIn now replaces the other kind, 35.2.6) |

Planted defects: 16 in `srp_early_mutants.py`, one for each order and each rule, the count's five triggers among
them (`feedback-early-reset-counted`, `-end-unowed`, `-unregistered-unowed`, `-left-seen-unowed`,
`-refresh-counted-again`), planted by the SRP campaign at the 1x1 entity with one and with two interfaces and at
8x8/1if, each result line naming its shape; and `early-talker-ignored` in `sink_mutants.py` (control campaign, S13
and S14 at both shapes). Two existing plants re-anchored (`feedback-latest-held-past-a-leave`,
`listener-copy-talker-indication-unwalked`). Before this round the 8x8/1if campaign planted no early defect, though
the round's text said it did; it plants all 16 now.

## Authoritative references

- Milan v1.2 5.3.8.5 (a settled Stream Input declares Listener Ready while a matching Talker Advertise is being
  received), 5.5.3.5.18 step 4 (reservation initiated at the probe's success), Tables 5.9 and 5.10
  (REGISTERING_FAILED, REGISTERING)
- IEEE 802.1Q-2018 10.7.7 and 10.7.8 NOTEs (state kept for attributes of immediate interest "as a Member or as a
  likely future Member"), Table 10-3 (a declared attribute's applicant is quiet in QA), 35.2.6 (replacement)
- The #925 ruling (the latest Talker kind decides)
- `sw/firmware/ctrl/srp/README.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` section 5

## How to get into the same state

```sh
git fetch origin 969-srp-kept-talkers && git checkout 969-srp-kept-talkers
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4 .. 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <dir>
(cd sw/litex && python3 test_ctrl_memory.py)
make -C tb/verilator/milan_dp twin twin-plants
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -I tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -I tb/verilator/ctrl_service_budget/shape_costs.py --check
python3 tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --groups srp-kept,srp-bound   # and 8x8-1if
python3 -I tb/verilator/ctrl_service_budget/kept_grade.py --selftest
python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <dir>
```

Expected result / pass criteria: every command exits 0; each campaign reports every plant caught; `kept_grade.py
--selftest` reports 19 checks passed; `run.py` and `kept_grade.py` print the registration cost's lines as `OWED #977`
and no finding (both logs finished, every probe with its record, kept <= bound, no `srp-kept` work pass or idle run
over THE SHARE, every build pass within its stated cost).

## Known limitations / out of scope

- **The bound.** Each interface keeps the Talkers of StreamIDs no binding holds up to one per STREAM_INPUT of the
  shape (2 at 1x1, 9 at 8x8), the release processor's count. Past it, a Talker no binding holds is ignored as
  before #969, and a binding made later declares with the talker's next declaration (its re-declaration after a
  LeaveAll, at most a LeaveAll period). At the bound, a JoinIn of the other kind of a kept StreamID is not kept
  either, so the old kind stays until the talker's Leave of it or a LeaveAll ends it.
- **The pool is not grown.** The kept are funded from the pool's fixed 16 medium blocks per interface, which hold
  the Domain's and the default VID's attributes (at most four while a Domain is adopted). A static assertion holds
  `SRP_KEPT_TALKERS + 4 <= 16`. The assumption is that those 16 hold nothing else; peer Domain floods already
  exceed the pool, as `srp/README.md` states. Growing the pool by the bound instead (2,592 B at 8x8/1if) would take
  the size fixture's 8x8/1if image, the split SoC's stand-in, past 56 RAMB36 with no ledger entry to hold it.
- **Block RAM.** The shipping images' `rom` takes half a tile more at 1x1/1if (45.0 to 45.5, 400 B past 45.0,
  within 56) and at 8x8/1if (58.0 to 58.5, 872 B past 58.0, its entry raised by the owner's rule of 2026-11-15);
  8x8/2if to 63.5 (408 B past 63.0). The size fixture's 8x8/1if stand-in stays at 56.0 with 112 B of `rom` left.
  The hot section: `reset_interface` grows 16 B at its own offset (it zeroes the kept count with the
  participants a reset destroys). Of the hot list's 261 functions in the 1x1/1if and 8x8/1if platform images, 152
  change in offset or size: `reset_interface` resized, and the 151 after it each 16 B later at their own size; the
  109 before it do not move. The CPU budget's own images (266 hot functions) show the same shape: 155, that is
  `reset_interface` and the 154 after it.
- **CPU budget: owed to #977.** A record that registers more than one or two Talkers is past
  `CTRL_LOOP_SRP_UNIT_US` (285 µs at 1x1/1if, 375 µs at 8x8/1if). Each Talker lwSRP registers costs about 15,000 to
  17,000 CPU cycles. That is the bound path the base already has (a bridge re-declaring the bound Talkers after
  any LeaveAll), and the kept Talkers make the same registrations before the bindings. By the owner's ruling on
  #969 (2026-11-22, option 1), that cost is #977's, fixed on the product shapes in its own lane; this PR restates
  no unit and no row. Measured on one image at the final head:

  | Point | Record | `srp-kept`, CPU cycles (by the rule) | `srp-bound`, the same MRPDU bound | Unit |
  |---|---|---:|---:|---:|
  | 1x1/1if | every input's Talker Advertise | 34,497 (365 µs) | 38,956 (410 µs) | 285 µs |
  | 1x1/1if | the count again after a freed block, Talkers past the bound | 32,224 (340 µs) | | 285 µs |
  | 1x1/1if | every input's Talker Failed after a reset | 36,859 (390 µs) | | 285 µs |
  | 8x8/1if | every input's Talker Advertise | 137,352 (1,445 µs) | 153,208 (1,610 µs) | 375 µs |
  | 8x8/1if | the count again after a freed block, Talkers past the bound | 68,692 (725 µs) | | 375 µs |
  | 8x8/1if | every input's Talker Failed after a reset | 142,909 (1,505 µs) | | 375 µs |

  `kept_grade.py` and `run.py` name each such record, and the bound group's walk, polls base and work pass over
  THE SHARE, as `OWED #977` with the issue's link, and fail the run if any condition of the ruling breaks, each
  breach a finding by name:
  - both groups' logs are present and finished (no incomplete simulation, trap or bus error), and every probe the
    point makes is marked, none other, each with its record;
  - every kept record costs no more than the bound record of its own interface, that record present (kept <=
    bound);
  - no work pass of `srp-kept` is over THE SHARE (2 ms; its worst 0.53 ms at 1x1/1if, 1.63 ms at 8x8/1if), nor
    any idle run's longest pass in either group (an idle pass makes no registration, so none is owed). THE SHARE
    is read from the logs graded, so a stale, empty or absent result file neither clears nor hides it;
  - every build pass of both groups is within its stated cost. The LeaveAll itself carries no kept value (its
    txLA! takes each kept attribute to LO, IEEE 802.1Q-2018 Table 10-3); the next MRPDU answers it with In for
    each from LO, 2 values at 1x1/1if and 9 at 8x8/1if, and is the build that encodes them: 39,123 of 73,500 and
    82,768 of 147,500 CPU cycles (srp-bound's heaviest: 53,970 and 101,786);
  - both groups are graded together, on one image.

  Regraded by the round-3 grader on the same runs (no re-measurement): PASS at both points, the same figures and
  the same `OWED` lines.

  `srp-bound`'s own pass over THE SHARE at 8x8/1if (224,540 CPU cycles, 2.245 ms: the bound path's registrations and ACMP's response
  to them) is named owed to #977 too. The share condition is held on `srp-kept`, the change under review.
  Round 1's five groups (srp, acmp-cmd, fixture, backlog, backlog-owed) against the base keep the same 7 owed
  backlog-owed misses and no others.
- **Routes.** Routed at 1x1/1if and 8x8/1if with the final firmware (`f02d44cd`) and the gating recipe's first
  directive (ExtraPostPlacementOpt): #818's floor met at every signoff corner, worst WNS +0.128 ns and WHS
  +0.032 ns at 1x1/1if (81 of 135 BRAM tiles), +0.096 ns and +0.036 ns at 8x8/1if (94.5 of 135), 0 routing errors,
  image identity passing. The base's images had +0.131 and +0.176 ns at the same directive. The other two
  directives were not run.
- **Bench.** No bench access here; the manager's bench re-run after merge is the physical check of the acceptance.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (host model; the bench re-run is the manager's, after merge)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

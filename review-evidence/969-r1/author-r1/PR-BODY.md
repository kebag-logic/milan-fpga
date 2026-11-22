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

**Green**, ready for review at `f863258d`, stacked on PR #960's head `dd163e41`. Firmware gate 4 of 4 shards (88 arms;
plants 827 + 385 + 565 caught, 0 escaped), coverage, ledger, twin and plants, CPU budget graders, docs workflow (99
of 103, the 4 rows that need the CI environment as on the base), routes at 1x1/1if and 8x8/1if meeting #818's floor.
`pf-969-1` -> `dev-soft-core`.

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
| `srp_mbx.c` `interested_msrp`, `keep_talker` | A Talker of a StreamID none of the interface's bindings holds is kept: one already kept, or while the interface keeps fewer than `SRP_KEPT_TALKERS`, one per STREAM_INPUT of the shape (the processor's count). Past the bound the old behaviour. |
| `srp_mbx.c` `count_kept`, `kept_visited`, `apply_receive` | The kept count is made again before a receive, outside lwSRP's callbacks, when a binding changed since the last count, or, at the bound, when a pool block was returned. It counts every Talker the participant does not declare whose StreamID no binding holds, registered or left with its block not yet freed. The walk neither reads nor writes it, so the walk's schedule (#930) moves no filter answer. |
| `srp_mbx.c` `talker_changed` | A StreamID no binding holds is held (#925's `srp_held`) from a registration it is kept for, with the kind registered latest, so a binding made later takes the latest of two kinds (the #925 ruling). An unbound StreamID's indication owes no walk. |
| `srp_mbx.c` `srp_mbx_bind` | A binding change owes the next receive's count. |
| `srp_mbx.h` | `SRP_KEPT_TALKERS`, `struct srp_kept`, the kept tables before `held` (which stays last so the code reading the rest compiles as before), `SRP_HELD_STREAMS` grown by half the kept bound. The pool is unchanged: its fixed 16 medium blocks an interface fund the kept beside the Domain's and the default VID's (a static assertion holds the sum). |
| `sw/litex/ctrl_memory*.py`, `test_ctrl_memory.py` | The platform's 8x8 images at 58.5 and 63.5 RAMB36 (720 and 256 B of `rom` past 58.0 and 63.0), refused at 59.0 and 64.0, `ctrl_plat` as measured, by the owner's rule of 2026-11-15 (ROM debt owed to S14). |
| Docs | `srp/README.md` (filter, pool, held, the kept Talkers, processor comparison D4), `plat/README.md`, `SPLIT_CONTROL_MEMORY.md`, `ctrl_split_boot/README.md`. |

**Tests.**

| Test | What it holds |
|---|---|
| `srp_mbx.cpp` `SrpEarlyTalker.*` (1x1 and 8x8, one and two interfaces) | On every STREAM_INPUT: registration then binding at a power-on's spacing (Advertise -> Ready, Failed -> Asking Failed) in THE TRANSMIT's next MRPDU within a JoinTime, and ACMP's copy; binding then registration with the kept at their bound; BIND_RX while bound to a stream declared all along; the latest of two kinds; a JoinIn replacement; an ended registration (Lv, an unanswered LeaveAll, a reset) declares nothing; the bound; an unbinding's registration kept and counted; a kept one that left counted until its block is freed |
| `test_plat_sinks.cpp` `Early.S13` (8x8/1if, 1x1/1if) | Every STREAM_INPUT's saved binding restored at a power cut; the talker declares (Advertise, then Failed) before it is discovered and probed, then is quiet; once each probe is answered the Listener is declared in THE TRANSMIT's next MRPDU within a JoinTime, and GET_STREAM_INFO shows REGISTERING (flags_ex) and REGISTERING_FAILED (flags) (Milan v1.2 Tables 5.9, 5.10) |
| `test_plat_sinks.cpp` `Early.S14` | The same after BIND_RX while bound to another stream whose Talker was declared all along |
| Restated: `Srp.ReadyFailedAndUninterestingStreamsAreSeparated`, `SrpTalkerKinds.AHeldStreamEndsWithEitherRegistrationOrAReset` | An unbound Talker now takes one block; a held stream's registration ends by an unanswered LeaveAll (a JoinIn now replaces the other kind, 35.2.6) |

Planted defects: 11 in `srp_early_mutants.py` (SRP campaign, both interface counts and 8x8/1if), one for each
order and each rule, and `early-talker-ignored` in `sink_mutants.py` (control campaign, S13 and S14 at both
shapes). Two existing plants re-anchored (`feedback-latest-held-past-a-leave`,
`listener-copy-talker-indication-unwalked`).

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
git fetch origin pf-969-1 && git checkout pf-969-1
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
```

Expected result / pass criteria: every command exits 0; each campaign reports every plant caught.

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
- **Block RAM.** The shipping images' `rom` takes half a tile more at 1x1/1if (45.0 to 45.5, 248 B past 45.0,
  within 56) and at 8x8/1if (58.0 to 58.5, 720 B past 58.0, its entry raised by the owner's rule of 2026-11-15);
  8x8/2if to 63.5 (256 B past 63.0). `.text` grows by 792 B (1x1/1if) and 780 B (8x8/1if): four functions grow and
  one is new; 54 cold symbols after them move; no hot-list function moves or changes size.
- **CPU budget.** Re-measured on the five groups that run the changed paths (srp, acmp-cmd, fixture, backlog,
  backlog-owed) at 1x1/1if and 8x8/1if, base against head, not on every arm and group: this host's load (about 150
  on 96 CPUs) put a full re-measure, about 240 groups a point, past the day. No stated cost or row bound moved.
- **Routes.** Routed at 1x1/1if and 8x8/1if with the gating recipe's first directive (ExtraPostPlacementOpt), the
  images carrying the final head's rom and sram banks: #818's floor met at every signoff corner, worst WNS +0.437 ns
  and WHS +0.017 ns at 1x1/1if (81 of 135 BRAM tiles), +0.058 ns and +0.036 ns at 8x8/1if (94.5 of 135), 0 routing
  errors, image identity passing. The other two directives were not run. The base's images at the same directive
  had +0.131 and +0.176 ns, so the 8x8/1if slack is 0.118 ns thinner, still above the floor; the rom's one added
  2 KiB bank (a RAMB18) at each shape is the netlist change.
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

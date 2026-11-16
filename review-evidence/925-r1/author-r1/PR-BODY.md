[A790]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> base.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED on a route decision (#925, the lane's STOP): the split images at 1x1/1if and 8x8/1if miss the +0.030 ns
floor on all three directives by 6 to 22 ps, as the base's own 1x1/1if image does (16 ps on hold). Every other gate
run passes (below). `925-srp-ta-tf` -> `dev-soft-core`, stacked on #901's review head `16ba667d` until #901 merges.

## Linked Issue / roles

Closes #925
Relates to #665

Executor: `[A790]`
Internal cleared-context reviewer: `[R<n>]` (to be named by the manager)
External reviewer: `[R<n>]` (to be named by the manager)

## Description

**The defect (#925, finding 18 of #665's replica report).** When a talker replaces its Talker Failed with a Talker
Advertise, it sends the Advertise as New. lwSRP withdraws a registered Talker of the other type only for a received
JoinIn or JoinMt (`mrp_mad.c` `rx_on_attr`, `msrp_attr_replaces`) and leaves a conflicting New to the host's
precedence rule, so both stay registered until the talker's next MRPDU. The split SRP adapter resolved both
registered as Failed first, in the receive filter (`interested_msrp`) and in the registrar walk (`registrations`), so
the Listener stayed Asking Failed until that next MRPDU (2.1 s on the bench, where the scenario wants 1 s). The
release's processor sets a sink's registered type at every registering event (`KL_srp_listener_fsm.sv`, the in-place
swap), so there the latest wins.

**The rule.** A talker declares one of the two Talker attributes for a stream (IEEE 802.1Q-2018 35.2.4), and a
registration of the other kind replaces the one held (35.2.6). So, per binding, the kind registered latest decides the
Listener declaration (Ready for an Advertise, AskingFailed for a Failed, 35.2.2.7.2) and the kind ACMP sees, while it
stays registered; once it leaves, the other one decides. The order comes from lwSRP's indications (New! on rNew in
every registrar state, Join! on MT to IN), which the adapter records per binding. A Talker Advertise's New over a
registered Talker Failed is now declared Ready within a JoinTime, as a first registration is. No SRP timer or bound
changes.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/srp/srp_mbx.h` | `srp_sink.latest_kind`: the kind of the StreamID's latest Talker registration indicated while bound |
| `sw/firmware/ctrl/srp/srp_mbx.c` | `listener_kind`: the latest decides while registered, else the remaining kind, Failed first only for a binding that saw neither; used by the receive filter and at the walk's end; `talker_changed` records the latest for every binding of the StreamID; `srp_mbx_bind` gives a new binding the StreamID's latest |
| `sw/firmware/ctrl/srp/README.md` | the rule and its clauses; the processor comparison's "conflicting New registrations retain Failed precedence" replaced |
| `sw/firmware/ctrl/test/srp_mbx.cpp` (`SrpTalkerKinds`), `srp_feedback.hpp` | both replacements within a JoinTime, leave of either in both orders, coincident registrations in one MRPDU in both orders, a later binding, the fallback, and the ACMP view and its intra-MRPDU withdrawal |
| `sw/firmware/ctrl/test/srp_kind_mutants.py` | ten planted defects, one a rule, each caught by name at both interface counts; `srp_mutants.py`'s `failed-listener-ready` moved to the new site |
| `sw/litex/ctrl_memory_ledger.py`, `ctrl_memory.py`, `docs/design/SPLIT_CONTROL_MEMORY.md` | `ctrl_plat` at 8x8 with two interfaces 20,352 -> 20,416 B (the field, padded), the same 60.5 RAMB36 |

**ROM, area and timing.** Platform image `rom` (`plat_ledger.py`): 1x1/1if +88 B (117,576 B, 43 RAMB36), 1x1/2if
+88, 8x8/1if +32 (130,232 B, still 56.0 within the budget), 8x8/2if +32 (60.5, its ledger's). The exported gateware
equals the base's at both shapes apart from LiteX's comment tree; only the ROM's contents differ, so there is no logic
area delta. Routes (S9's recipe; Slow WNS / Fast WHS, ns):

| Shape | ExtraPostPlacementOpt (recipe) | ExtraTimingOpt | AltSpreadLogic_high |
|---|---|---|---|
| 1x1/1if | +0.024 / +0.036 | +0.008 / +0.023 | +0.177 / +0.023 |
| 8x8/1if | +0.011 / +0.034 | +0.171 / +0.014 | +0.215 / +0.014 |
| 1x1/1if at `16ba667d` (comparison) | +0.208 / +0.014 | +0.260 / +0.014 | |

The release image is byte-identical (`bios.bin` and the stripped ELF at both configs).

## Authoritative references

- #925; #665 issuecomment-6904803181 (finding 18) and issuecomment-6904832963 (the decision).
- IEEE 802.1Q-2018 35.2.4, 35.2.6, 35.2.2.7.2, 35.2.2.8; Milan v1.2 4.2.7.2.2 (rapid leave, unchanged).
- `sw/firmware/ctrl/srp/README.md` (the Listener rules); `third_party/lwSRP/doc/developer.md` (New conflicts left to
  the host); `protocol-processor/hdl/srp/KL_srp_listener_fsm.sv` (the release's registrar swap).
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 3 (the ledger); FR_NFR 3.4.1 (the service budget, unchanged bounds).

## How to get into the same state

```sh
git fetch origin 925-srp-ta-tf && git checkout --detach 1be0a6c4
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4, 2/4, 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <dir>
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir> --record-budget-findings --record-share-findings
```

Expected result / pass criteria: every firmware shard PASS (control 716 of 716, AECP 299, SRP 441 caught, 0
escaped), `fw_coverage` PASS (`srp_mbx.c` 741/741, 671/671), `plat_ledger` PASS at every point. The budget at 1x1/1if
exits 0 (96 groups, 0 refusals, 0 passes over the share; the 7 `backlog-owed` misses recorded at the base too). At
8x8/1if it exits 1 on STATED lines only, for the polls' base and ACMP's item and declined offer (not SRP's). The
flip check at 1x1/1if (`flip_grade.py --check --point 1x1/1if`) and `load_grade.py --check` PASS.

## Known limitations / out of scope

- A binding that saw neither registration's indication (bound while both kinds are registered, with no other binding
  of the StreamID bound, which needs all of them unbound and one bound again inside the conflict window) keeps
  Failed first until the talker's next MRPDU leaves one kind. Every registration lwSRP holds was indicated, so a
  binding made before the registrations, or beside another binding of the StreamID, always has the order.
- The bench acceptance (the scenario reaches Listener Ready within 1 s of the Talker Advertise) is the gating run's.
- `srp_mbx.cpp` at the 8x8 entity, a shape no gate runs that suite at, fails two startup tests at `16ba667d` too
  (`StartupDeclaresTalkersDomainAndVlan`, `OneLoopOwnsTheGlobalCentisecondDispatch`); not changed here.
- lwSRP, the mailbox contract and RTL are unchanged.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (desk gates here; the bench acceptance is the gating run's)
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

[A760]

## Contents

- **[Status](#status)** — Green, test tally, and `665-s9-split-image` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN on every #870 acceptance item; the round 4 ruling's items 1 to 5 are done, with one open question (below). The head is `a69fc0f5`, seventeen commits on `dev-soft-core` `1d6bf555`: round 1's eight, round 2's four, round 3's two, round 4's three. Round 4 changes tests and docs only: no RTL, generator, contract, recipe or routed file. `665-s9-split-image` -> `dev-soft-core`.

Round 4's gates, on clean clones of `a69fc0f5`, all rc 0 (the ruling's item 5):
- `test_builder.py --require-rv32`, gate 23p included: the two good images and the bound-bitstream control pass, and 13 planted images each fail by their kind;
- the three planted copies of the identity gate, each failing gate 23p (`if True:`, `have == bound`, the manifest-ident rule removed), run on a clone whose tree is `a69fc0f5`'s. At `a91fb27d` the first and third pass gate 23p;
- `make -C tb/verilator/mbx`, and its full mutant campaign: 546 / 591 checks, cosim 32, 553 / 598 at two interfaces, the model 490, 0 failures; 231 of 231 arms caught;
- docs.yml on its verifier: 64 steps, 31 not run with a reason, 0 bad;
- `git diff --check` against the merge base.

Round 3's evidence is reused for everything round 4 cannot reach: the route, the all-fabric endpoint, the split boots, S2's harness, the sweep and the other workflows. Their inputs (the RTL, the generator, the contract, the firmware, the SoC and the builder recipe) are unchanged since `a2690e68` and `a91fb27d`.

| # | Acceptance item (#870) | Result |
|---|---|---|
| 1 | Route WNS >= +0.030 ns, WHS >= 0 at every corner, #818's three directives | **Met** (round 3's route, not re-run). All three directives come from one synthesis checkpoint and meet WNS and WHS >= +0.030 ns at every corner. Best, the recipe's `ExtraPostPlacementOpt`: slow WNS +0.274 ns, fast WHS +0.036 ns |
| 2 | All-fabric endpoint unchanged | Met: the exports at `a2690e68` equal the base's at 1x1 and 8x8 (21/21 files each); builder outputs byte-identical (round 1) |
| 3 | Ledger rows at the four points | Met: `docs/design/MARK_II_AREA_PLAN.md`, "M8a-2: the integrated split route" |
| 4 | Whole image vs 121.5 tiles and 38,040 LUT | Met: 29,377 LUT, 39,235 FF, 72 tiles; 8,663 LUT below the bar |
| 5 | Bound-talker term at 1 and 2 interfaces and in the route, D7 close-out row | Met (round 3): 349 / 93 and 754 / 151 out of context; the close-out row |
| 6 | A planted negative control per identity mismatch, split + DDR3, all-fabric + mailbox | Met: 13 planted images, now including a manifest whose ident is not the image's, and a positive control with a bound bitstream (round 4) |

Every routable net is routed in every directive of every round, none with an error. At the recipe's directive: 66,578 of 66,578, then 66,913 of 66,913, then 67,358 of 67,358 (67,354 and 67,333 at the other two directives in round 3).

## Linked Issue / roles

Closes #870
Relates to #665

Executor: `[A760]`
Internal cleared-context reviewer: `[R827]` (round 3, NEGATIVE on MINORs; round 4 delta to be assigned)
External reviewer: `[R828]` (round 3, NEGATIVE on MINORs; round 4 delta to be assigned)

## Description

Round 4 (three commits), the ruling on #870 (issuecomment-6796161767) on the two round 3 reviews: tests and docs only.

| Piece | Change |
|---|---|
| Identity gate controls (`sw/builder/test_builder.py`, gate 23p) | A positive control: a copy of the good split image whose manifest binds a fixture bitstream that its `gateware/*.bit` matches, which the gate must pass, as a split `--build` writes it. A plant: the manifest's `ident` set to the all-fabric ident while the image's stays split, which must fail with `FINDING manifest:` |
| Check IDs (`tb/verilator/mbx`) | The head-publication check, previously a second `H0`, is `U0`, an ID no other check uses. Updated in `suite.hpp`, its mutant needle in `mutants.py`, the bench README and `MAILBOX_SPLIT.md` |
| Docs | `MARK_II_AREA_PLAN.md`: the routed nets per directive, in the ruling's words, and the bus clock's setup paths. These are the 10 worst within the bus clock and the 10 worst into it from the Ethernet receive clock that the route's timing report lists per directive, none in `KL_mbx/u_rx`. `MAILBOX_SPLIT.md`: gate 23p's control and its thirteenth plant |

Each new control has its planted defect:
- `if have != bound:` replaced by `if True:` in `check_image_identity.py` fails the positive control ("the gate refused an image that agrees with its identity"). At `a91fb27d` gate 23p passed it.
- `have == bound` fails the positive control, and the existing "another bitstream" plant.
- The manifest-ident rule removed fails the new plant ("the gate did not find it by its manifest rule"). At `a91fb27d` gate 23p passed it.

S2 of R827-1 (a default transition for the receive FSM's unused codes) is declined in this round because it moves RTL after signoff. The ruling sends it to #495 as residue for the next `KL_mbx` change.

Earlier rounds, unchanged here:
- Round 1 (eight commits): the builder's split recipe; the SoC ident naming the placement, the split image manifest and its identity gate; DDR3 and the processor memory bridges removed from the split (D4); the M0s recipe's full-split inventory; the out-of-context firmware memory mapper for a ledgered point; the ledger.
- Round 2 (four commits): the register read decoded from an offset registered at its request, the bound-talker read-back read from a registered address, the receive ring write port and the published head registered.
- Round 3 (two commits, issuecomment-6788700325): three more logic cuts inside `KL_mbx`, for timing only (the ring write port's address and word without the write decision, the receive verdict registered, the register read multiplexer as a generated AND-OR of one-hot selects), with checks W0, V0, V1 and S0, and the third route.

## Authoritative references

- #870 (acceptance 1 to 6), the round 3 ruling (issuecomment-6788700325) and the round 4 ruling (issuecomment-6796161767).
- #818 (a route set judged on its three placement directives).
- `docs/design/MARK_II_AREA_PLAN.md`, Target (the +0.030 ns WNS floor) and "M8a-2: the integrated split route".
- `docs/design/MAILBOX_SPLIT.md`: Rings records and events, The ingress filter, Bus adapters and the hard core, Measured area.
- `sw/mailbox/mailbox.yaml` (the contract, unchanged), Wishbone B4 (ACK any cycle after the request), AMBA AXI IHI0022H A3.1.1 and A3.2.1.
- The plan's decisions D2, D4 and D7 (a) on #665.

## How to get into the same state

```sh
git fetch origin 665-s9-split-image
git checkout a69fc0f597355a0a200ec5be6bb134b897e97ff5
git submodule update --init third_party/verilog-axis third_party/tsn-c-stack third_party/lwSRP protocol-processor gptp-processor
```

The pinned Verilator 5.050, the LiteX tree that `docs/ENDSTATION_BUILDER.md` names, and the RV32 SDK that `scripts/ci_rv32_sdk.py` installs are assumed on `PATH`.

## How to validate

```sh
python3 sw/builder/test_builder.py --require-rv32
python3 sw/builder/test_builder.py --gates test_image_identity_gate
make -C tb/verilator/mbx
make -C tb/verilator/mbx mutants
git diff --check 1d6bf5556a HEAD
```

Expected result / pass criteria:
- `test_builder.py` prints `ALL GATES PASS`. Gate 23p's line reads "the good split and all-fabric images and 1 bound-bitstream control pass the identity gate; 13 planted images each fail it by their kind". It lists "a bound bitstream the image holds: passes" and "the manifest's ident changed: FINDING manifest: the manifest's ident ... is not the image's ...".
- Planting `if True:` or `have == bound` for `if have != bound:` in `sw/litex/check_image_identity.py` fails gate 23p on "a bound bitstream the image holds". Deleting the two lines of the `claimed["ident"] != got["ident"]` rule fails it on "the manifest's ident changed".
- `make` exits 0, with 12 of 12 quick arms caught; `make mutants` prints `mbx mutants: 231 of 231 caught`, the head-publication arm failing `U0 no receive ring word is written under the head the core sees`.
- `git diff --check` prints nothing.
- Round 3's commands (generator, split boots, S2's harness, the route) are unchanged and give round 3's results, since their inputs did not change.

## Known limitations / out of scope

- The resource gate on the selected route still exits 1 for RAMB18 +5 (27 to 32), as in rounds 1 and 2; it recommends the re-baseline that only M9 takes. Its timing figures pass.
- The bound-talker term at one interface reads 349 LUT by the out-of-context recipe, 49 over its target. D7 (a) closes it as measured, and its trigger for (b) is not met.
- T_svc misses are recorded, not graded (S2b, #810).
- Out of scope, per #870: ring geometry and the 32x32 shape (#859), the firmware loop (S2b, #810), the bench (S12), the VERSION bump (S13).
- Open question for the manager: two pre-existing ID pairs remain shared between `suite.hpp` and `suite_face.hpp`, as they are on `dev-soft-core` `1d6bf555`. `F0`-`F2` is the adp channel's checks and also the face block's. `T0`-`T1` is the token bucket and also the face block's timing. The ruling moved only the new check, so these are not renamed here; renaming the face block's IDs touches another lane's checks and needs its own Issue.
- R827-1 S2 is declined in this round; it goes to #495 (the ruling).
- S1 asked for the 15 worst bus-clock paths per directive. Round 3's reports do not enumerate 15. The route's timing report lists the 10 worst within the bus clock and the 10 worst into it from the Ethernet receive clock, and each slow signoff corner lists 5 of each. All of them are published with the review evidence, none is in `KL_mbx/u_rx`, and the plan's sentence now says that instead of "the 15 worst".

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

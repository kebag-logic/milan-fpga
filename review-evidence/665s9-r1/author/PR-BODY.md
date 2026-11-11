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

GREEN on every #870 acceptance item. The head is `a91fb27d`, fourteen commits on `dev-soft-core` `1d6bf555`: round 1's eight, round 2's four, round 3's two. `665-s9-split-image` -> `dev-soft-core`.

Gates at `a91fb27d`, on clean clones, all rc 0:
- every `run:` step of the four pull_request workflows: 69 job instances, 497 steps; 110 not run, each with its reason;
- docs.yml on its verifier: 88 steps, 7 not run with a reason, 0 bad;
- the full sweep in four shards: 65 of 65 suites, 2,192,983 checks, 0 failures;
- the firmware self-test and mutant campaigns (570 of 570), `fw_coverage.py --check`, both boundary halves;
- `test_builder.py --require-rv32`, behave (508 scenarios) and `git diff --check`;
- the mailbox suite and its 231 mutants; the generator's check, cross-check and self-test.

The route, the out-of-context term, the all-fabric export compare, the split boots and S2's harness ran at `a2690e68`; the last commit changes two design documents only, so their inputs are unchanged.

| # | Acceptance item (#870) | Result |
|---|---|---|
| 1 | Route WNS >= +0.030 ns, WHS >= 0 at every corner, #818's three directives | **Met.** Round 3's route, all three directives from one synthesis checkpoint, meets WNS and WHS >= +0.030 ns at every corner. Best, the recipe's `ExtraPostPlacementOpt`: slow WNS +0.274 ns, fast WHS +0.036 ns. Round 1 reached +0.002 ns and round 2 +0.021 ns |
| 2 | All-fabric endpoint unchanged | Met: the exports at `a2690e68` equal the base's at 1x1 and 8x8 (21/21 files each); the all-fabric image reads no mailbox source; builder outputs byte-identical (round 1) |
| 3 | Ledger rows at the four points | Met: `docs/design/MARK_II_AREA_PLAN.md`, "M8a-2: the integrated split route" |
| 4 | Whole image vs 121.5 tiles and 38,040 LUT | Met: 29,377 LUT, 39,235 FF, 72 tiles (round 3's route); 8,663 LUT below the bar |
| 5 | Bound-talker term at 1 and 2 interfaces and in the route, D7 close-out row | Met: re-measured at round 3's RTL, 349 / 93 and 754 / 151 out of context; the close-out row updated |
| 6 | A planted negative control per identity mismatch, split + DDR3, all-fabric + mailbox | Met (round 1): 12 planted images |

## Linked Issue / roles

Closes #870
Relates to #665

Executor: `[A760]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

Round 1 (eight commits, unchanged here):
- the builder's split recipe;
- the SoC ident naming the placement, the split image manifest, and its identity gate with twelve planted images;
- DDR3 and the processor memory bridges removed from the split (D4);
- the M0s recipe's full-split inventory;
- the out-of-context firmware memory mapper for a ledgered point;
- the ledger.

Round 2 (four commits): the register read decoded from an offset registered at its request, the bound-talker read-back read from a registered address, the receive ring write port and the published head registered.

Round 3 (two commits), the ruling on #870 (issuecomment-6788700325): three more logic cuts inside `KL_mbx`, for timing only, with the recipe unchanged, no pblocks and no floor exception.

| Piece | Change |
|---|---|
| (a) Ring write port (`KL_mbx_rx.sv`) | Only the write enable carries the write decision (the channel, the free space, max_frame_bytes); the address and the word follow the receive state alone. No added cycle |
| (b) Receive verdict (`KL_mbx_rx.sv`) | Taken once the last byte's word has drained, into four registers; it acts a mailbox clock later (a new state, VRD_S) on RX_DROP, RATE_DROP, FILTER_MISMATCH, the frame's clean-up and the header writes |
| (c) Register read multiplexer (`sw/mailbox/mailbox_skeleton.py`, `mailbox_face.py`, `gen_mailbox.py`; `KL_mbx.sv` regenerated) | Generated as the AND-OR of 114 one-hot selects (`rd_hit_w`), no priority chain. The generator computes every read term's offsets from the contract and refuses any offset two terms share; the cross-check requires the AND-OR form in the tracked skeleton. No added cycle |
| Tests (`tb/verilator/mbx`) | W0: a word the free space cannot hold still reaches the port at its slot, unwritten. V0: twelve frames back to back across every verdict, none lost or counted twice. V1: the verdict's latency to the clock. S0: every word of the host window read, and no read of any check with two selects set. Six planted arms (twelve quick in the default make) and five generator arms |
| Docs | `MAILBOX_SPLIT.md`: the port, the verdict and its cost, the AND-OR and its proofs, the term at round 3's RTL, the route. `MARK_II_AREA_PLAN.md`: the third route, its slack by directive, its paths, the term rows, the resource gate. The mbx README |

Each cut is undone by a planted defect that its own check catches:
- the port's address and word zeroed by the decision again fails W0 alone;
- the verdict acting in the cycle it is taken fails V0 and V1;
- the read multiplexer turned back into a priority chain fails the generator's cross-check. A priority chain over one-hot selects reads the same values, so no simulation can tell them apart; a select overlapping another's offset fails S0 in the RTL, and a window laid over another fails the generator's one-hot proof.

The cost of the cuts:
- one mailbox clock per received frame (10 ns at 100 MHz): the next frame's first byte is taken 6 clocks after a committed frame's last byte and 4 after any other's, where it was 5 and 3; none per host access;
- 75 LUT and 6 FF on the route, 228 slices fewer.

S2's harness, re-measured against round 2: 36 T_svc misses at 1x1/1if and 63 at 8x8/2if, the same probes as round 2, each within 0.001 ms.

## Authoritative references

- #870 (acceptance 1 to 6) and the round 3 ruling, issuecomment-6788700325.
- #818 (a route set judged on its three placement directives).
- `docs/design/MARK_II_AREA_PLAN.md`, Target (the +0.030 ns WNS floor) and "M8a-2: the integrated split route".
- `docs/design/MAILBOX_SPLIT.md`: Rings records and events, The ingress filter, Bus adapters and the hard core, Measured area.
- `sw/mailbox/mailbox.yaml` (the contract, unchanged), Wishbone B4 (ACK any cycle after the request), AMBA AXI IHI0022H A3.1.1 and A3.2.1.
- The plan's decisions D2, D4 and D7 (a) on #665.

## How to get into the same state

```sh
git fetch origin 665-s9-split-image
git checkout a91fb27dd39483e4694e193504da1dbe06208807
git submodule update --init third_party/verilog-axis third_party/tsn-c-stack third_party/lwSRP protocol-processor gptp-processor
```

The pinned Verilator 5.050, the LiteX tree that `docs/ENDSTATION_BUILDER.md` names, and the RV32 SDK that `scripts/ci_rv32_sdk.py` installs are assumed on `PATH`.

## How to validate

```sh
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
make -C tb/verilator/mbx
make -C tb/verilator/mbx mutants
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/boot-1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/boot-8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
```

Expected result / pass criteria:
- `gen_mailbox: 0 finding(s)`; the self-test prints `selftest: 0 arm(s) failed`, its overlap arms each naming two registers and one offset.
- `make` exits 0, with 12 of 12 quick arms caught; `make mutants` prints `mbx mutants: 231 of 231 caught`.
- Both boots print `ctrl_split_boot: PASS`.
- The budget runs print 36 and 63 T_svc misses.
- The route reproduces the ledger's three directives from one synthesis checkpoint, each at or above +0.030 ns WNS and WHS at every corner. It follows the M0s recipe at `full-split` in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.

## Known limitations / out of scope

- The resource gate on the selected route still exits 1 for RAMB18 +5 (27 to 32), as in rounds 1 and 2; it recommends the re-baseline that only M9 takes. Its timing figures pass.
- The bound-talker term at one interface reads 349 LUT by the out-of-context recipe, 49 over its target. D7 (a) closes it as measured, and its trigger for (b) is not met.
- T_svc misses are recorded, not graded (S2b, #810).
- Out of scope, per #870: ring geometry and the 32x32 shape (#859), the firmware loop (S2b, #810), the bench (S12), the VERSION bump (S13).

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

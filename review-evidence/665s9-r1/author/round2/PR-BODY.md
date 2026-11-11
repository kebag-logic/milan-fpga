[A760]

## Contents

- **[Status](#status)** — Blocked on one acceptance item, test tally, and `665-s9-split-image` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED on #870 acceptance item 1 (the route's timing floor) after the round 2 ruling's two `KL_mbx` timing cuts. Items 2 to 6 are met. The head is `72f596b8`, twelve commits on `dev-soft-core` `1d6bf555`: round 1's eight, then round 2's four. `665-s9-split-image` -> `dev-soft-core`.

Gates at `72f596b8`, on clean clones, all rc 0:
- every `run:` step of the four pull_request workflows: 69 job instances, 497 steps; 110 not run, each with its reason;
- docs.yml on its verifier;
- the full sweep in four shards: 65 of 65 suites, 2,192,919 checks, 0 failures;
- the firmware self-test and mutant campaigns, `fw_coverage.py --check`, both boundary halves;
- `test_builder.py --require-rv32`, behave (508 scenarios) and `git diff --check`;
- the mailbox suite and its 225 mutants.

S2's harness and the split boots ran at `3ba76ae7`, whose inputs the later commits leave unchanged.

| # | Acceptance item (#870) | Result |
|---|---|---|
| 1 | Route WNS >= +0.030 ns, WHS >= 0 at every corner, #818 best of three | **Not met.** Round 1 reached +0.002 ns. Round 2 cut the two failing mailbox paths and reached +0.021 ns at `ExtraTimingOpt`, 0.009 under the floor. WHS is met everywhere, and at that directive it is +0.030 ns or more as well |
| 2 | All-fabric endpoint unchanged | Met: exports equal the base's at 1x1 and 8x8 (21/21 files each); the all-fabric image reads no mailbox source; builder outputs byte-identical (round 1) |
| 3 | Ledger rows at the four points | Met: `docs/design/MARK_II_AREA_PLAN.md`, "M8a-2: the integrated split route" |
| 4 | Whole image vs 121.5 tiles and 38,040 LUT | Met: 29,302 LUT, 39,229 FF, 72 tiles (round 2's route) |
| 5 | Bound-talker term at 1 and 2 interfaces and in the route, D7 close-out row | Met: re-measured at the cut RTL, 474 / 89 and 707 / 154 out of context, the close-out row updated |
| 6 | A planted negative control per identity mismatch, split + DDR3, all-fabric + mailbox | Met (round 1): 12 planted images |

In round 2 every path under +0.030 ns is inside `KL_mbx` at the 100 MHz bus clock. There are two families:
- the receive block's verdict and drain decision: `u_rx/ch_r` to the new write registers' resets, to the term fields' reset and to RX_DROP's enable;
- the register read multiplexer's depth.

The next cut is posted on #870.

## Linked Issue / roles

Relates to #870
Relates to #665

This PR does not close #870: acceptance item 1 (the route's timing floor) is not met; see Status.

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

Round 2 (four commits), the ruling on #870 (issuecomment-6779934014): two logic cuts inside `KL_mbx`, for timing only.

| Piece | Change |
|---|---|
| Register read (`sw/mailbox/mailbox_skeleton.py`, `mailbox_face.py`; `KL_mbx.sv` regenerated) | The read multiplexer decodes an offset registered at the read's request, through its own copy of the bound-talker, publication and face decodes. A register read is answered two mailbox clocks after its request, a ring read and a write one. GM_LO's snapshot is taken in the cycle its word is sampled |
| Bound-talker read-back (`KL_mbx_rx.sv`) | Read the cycle after the request from an address registered at it; the copier also yields that cycle |
| Receive ring write (`KL_mbx_rx.sv`) | The ring write port is registered. The head the core sees is published a cycle after the commit, once the last header word is in the ring |
| Tests (`tb/verilator/mbx`) | Noise on the host port in every cycle without a request, so a mailbox decoding a later cycle's bus answers from it. H0, every clock: no ring word written under the head the core sees. G1: GM_LO and GM_HI one identity, whichever cycle it changes in. Eighteen planted arms, nine in the default make. A window's refusals are graded in its second request, so its first answer stays inside the 64-cycle wait bound. The noise and probes exist only under `BENCH_P`, which the suite's recipe sets |
| Docs | `MAILBOX_SPLIT.md`: the latency, the head after its data, the term at the cut RTL. `MARK_II_AREA_PLAN.md`: the second route, its slack by directive, the paths left, the next cut, the term rows. The mbx and S2 harness READMEs |

The cost of the cuts:
- one mailbox clock per register read (10 ns at 100 MHz), none per ring read or write;
- 25 LUT and 169 FF on the route.

S2's harness, re-measured: 36 T_svc misses at 1x1/1if (round 1: 34) and 63 at 8x8/2if (round 1: 63).

## Authoritative references

- #870 (acceptance 1 to 6) and the round 2 ruling, issuecomment-6779934014.
- #818 (a route set judged on its best of three placement directives).
- `docs/design/MARK_II_AREA_PLAN.md`, Target (the +0.030 ns WNS floor) and "M8a-2: the integrated split route".
- `docs/design/MAILBOX_SPLIT.md`: Bus adapters and the hard core, Rings records and events, Measured area.
- `sw/mailbox/mailbox.yaml` (the contract, unchanged), Wishbone B4 (ACK any cycle after the request), AMBA AXI IHI0022H A3.1.1 and A3.2.1.
- The plan's decisions D2, D4 and D7 (a) on #665.

## How to get into the same state

```sh
git fetch origin 665-s9-split-image
git checkout 72f596b8f375407a4b8ac6d15868b7f975c18850
git submodule update --init third_party/verilog-axis third_party/tsn-c-stack third_party/lwSRP protocol-processor gptp-processor
```

The pinned Verilator 5.050, the LiteX tree that `docs/ENDSTATION_BUILDER.md` names, and the RV32 SDK that `scripts/ci_rv32_sdk.py` installs are assumed on `PATH`.

## How to validate

```sh
python3 sw/mailbox/gen_mailbox.py --check
make -C tb/verilator/mbx
make -C tb/verilator/mbx mutants
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/boot-1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/boot-8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
```

Expected result / pass criteria:
- `gen_mailbox: 0 finding(s)`.
- `make` exits 0, with 9 of 9 quick arms caught; `make mutants` prints `mbx mutants: 225 of 225 caught`.
- Both boots print `ctrl_split_boot: PASS`.
- The budget runs print 36 and 63 T_svc misses.
- The route reproduces the ledger's three directives from one synthesis checkpoint, best `ExtraTimingOpt` +0.021 ns. It follows the M0s recipe at `full-split` in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.

## Known limitations / out of scope

- Acceptance item 1 is not met: the floor misses by 0.009 ns after both cuts. The next cut needs a decision: the receive block's verdict and write registers, and the read multiplexer's structure.
- The bound-talker term at one interface reads 474 LUT by the out-of-context recipe (285 in round 1). D7 (a) closes it as measured, and its trigger for (b) is not met.
- Out of scope, per #870: ring geometry and the 32x32 shape (#859), the firmware loop (S2b, #810), the bench (S12), the VERSION bump (S13).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (item 1 not met)
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

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

BLOCKED on #870 acceptance item 1 (the route's timing floor); items 2 to 6 are met. Gates at `ad2ed0e3`, on clean clones, all rc 0: every `run:` step of the four pull_request workflows (69 job instances, 497 steps; 110 not run, each with its reason), the full sweep in four shards (65 of 65 suites, 2,192,899 checks, 0 failures), the firmware self-test and mutant campaigns, `fw_coverage.py --check`, S2's harness at 1x1 and 8x8, `test_builder.py --require-rv32`, behave and `git diff --check`. `665-s9-split-image` -> `dev-soft-core`.

| # | Acceptance item (#870) | Result |
|---|---|---|
| 1 | Route WNS >= +0.030 ns, WHS >= 0 at every corner, #818 best of three | **Not met.** Best `ExtraTimingOpt`: slow-corner WNS +0.002 ns (0.028 under the floor); WHS met everywhere |
| 2 | All-fabric endpoint unchanged | Met: exports equal the base's at 1x1 and 8x8 (21/21 files each), builder outputs of the five configs byte-identical (50 files), no all-fabric manifest; its route passes the gate |
| 3 | Ledger rows at the four points | Met: `docs/design/MARK_II_AREA_PLAN.md`, "M8a-2: the integrated split route" |
| 4 | Whole image vs 121.5 tiles and 38,040 LUT | Met: 29,277 LUT, 39,060 FF, 72 tiles |
| 5 | Bound-talker term at 1 and 2 interfaces and in the route, D7 close-out row | Met |
| 6 | A planted negative control per identity mismatch, split + DDR3, all-fabric + mailbox | Met: 12 planted images, each refused by its kind |

Every path under +0.030 ns, in all three directives, is inside `KL_mbx` at the 100 MHz bus clock: the host register read (LiteX's AXI-Lite-to-Wishbone bridge through the bound-talker table's read-back to `reg_rdata_r`) and the receive block's ring write. Closing it needs a mailbox RTL change or a bus register stage, a decision posted on #870.

## Linked Issue / roles

Relates to #870
Relates to #665

This PR does not close #870: acceptance item 1 (the route's timing floor) is not met; see Status.

Executor: `[A760]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

The split image build, its identity and the first integrated route of the complete split (#665 S9), with S10 closed by decision D7 (a).

| Piece | Change |
|---|---|
| Builder recipe | `endstation_builder.py <cfg> --placement split` builds a shipped config at the split placement without editing it; its shape artifacts are the all-fabric build's byte for byte, and it writes no tracked file (gate 23o) |
| Identity (D2) | The SoC ident ends in `split` for a split image; VERSION stays `0x0002_0060`; `KL_mbx`'s `ID` gives the contract major and minor |
| Manifest | A split build writes `image_manifest.json`: placement, ident, VERSION, mailbox contract, firmware ELF sha256, bitstream payload sha256 and part. An all-fabric build writes none |
| Identity gate | `sw/litex/check_image_identity.py` refuses, by kind, a manifest, ident, firmware, bitstream or placement that disagrees with the image, a split image carrying DDR3, and an all-fabric image carrying a mailbox. A split build runs it on what it wrote (gate 23p, 12 planted images) |
| M8a-2 (D4) | `--ctrl-mailbox` builds no DDR3, no main RAM and none of the three processor memory bridges; `--ctrl-mailbox --with-dram` is refused. The all-fabric build is unchanged |
| Route recipe | Under `full-split` the M0s inventory reads the split firmware's rom banks as banks (two planted mutants) |
| Ledger tooling | `ctrl_memory_ooc.py --ledgered TAG=POINT` maps the 59.0-tile ledgered point out of context; `test_ctrl_memory.py` grades it with three planted mutants |
| Ledger | The area plan's new M8a-2 section: route, timing by directive, block RAM by owner, the firmware ledger at four points, the five largest BSS consumers, reconciliation against 121.5, the bound-talker term and D7's close-out |

No HDL source, firmware, mailbox contract, ring, shape geometry or VERSION change. The split's generated SoC changes (no DDR3, main RAM or processor memory bridge); the all-fabric's does not.

## Authoritative references

- #870 (the task) and #665 (the Mark II split plan, stages S9 and S10; decisions D2, D4 and D7 (a)).
- [NFR-RES-01](docs/reference/FR_NFR.md#35-resource-reliability-and-the-rest): at most 38,040 LUTs.
- `docs/design/MARK_II_AREA_PLAN.md`: Target (WNS >= +0.030 ns, WHS >= 0; #818's best of three placement directives), the firmware and block RAM ledger and its checkpoint evidence.
- `docs/design/SPLIT_CONTROL_MEMORY.md` sections 4 to 6: the split's memory, no BIOS, the 56-RAMB36 allocation and the ledgered point (#665 ruling 6505997821).
- `docs/design/MAILBOX_SPLIT.md`: the placement switch, Measured area (the bound-talker term), the split image's identity.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: Integrated and Selected-placement measurements (the M0s recipe).

## How to get into the same state

```sh
git clone https://github.com/kebag-logic/milan-fpga.git
cd milan-fpga
git fetch origin 665-s9-split-image
git checkout --detach ad2ed0e3ab3daa9697bdf42ae504b4504bfd04aa
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
```

The builder and SoC steps run in the LiteX environment (`sw/litex/litex_pins.txt`); the firmware steps need the pinned RV32 SDK (`python3 scripts/ci_rv32_sdk.py`).

## How to validate

```sh
python3 sw/builder/test_builder.py --require-rv32                 # gates 23o and 23p among the rest
python3 sw/litex/test_ctrl_memory.py                                # the mapper arm and its three mutants
python3 syn/ooc/pp_baseline.py --selftest
python3 syn/ooc/pp_baseline_mutants.py
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml --placement split
python3 tb/verilator/ctrl_split_boot/run.py --build-dir "$WORK/boot-1x1"
python3 tb/verilator/ctrl_split_boot/run.py --build-dir "$WORK/boot-8x8" --shape endstation_ax7101_8x8
python3 sw/litex/check_image_identity.py "$IMAGE"
python3 scripts/check_nvm_capture.py
git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD
```

Expected result / pass criteria:

- Every command exits 0; the identity gate prints `image identity: a split image whose manifest, ident, firmware, bitstream and placement agree, with no DDR3`.
- Gate 23p's twelve planted images each fail by their kind (`FINDING ident:`, `manifest:`, `placement:`, `ddr3:`, `firmware:`, `bitstream:`).
- The split boot reaches `ready` with 0 findings at both shapes.
- The route figures and timing are in the area plan's M8a-2 section; the integrated route itself needs Vivado and follows the M0s recipe with `--placement full-split`.

## Known limitations / out of scope

- **Acceptance item 1 is not met** (see Status). Closing it is a `KL_mbx` timing change or an SoC bus register stage, neither in this lane's scope; the decision is posted on #870.
- The 8x8 two-interface firmware image is 1.5 tiles over the 56-tile allocation as mapped (3.0 as planned), ledgered at 59.0 and owed to lane S14 (#665 ruling 6505997821).
- The largest image's 8x8 datapath is not routed; the route is the shipping 1x1 shape.
- Ring geometry and the 32x32 shape (#859), the firmware loop (S2b), the bench (S12) and the VERSION bump (S13) are out of scope.
- The two-interface mailbox misses 10 ns out of context with and without the bound-talker term; no image builds it.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (item 1 is not; see Status)
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

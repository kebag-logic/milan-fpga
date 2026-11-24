[A835]

## Contents

- **[Status](#status)** — Gate tally, both release routes, and `994-gptp-pin-1213ac5b` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, dependency and environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN — `994-gptp-pin-1213ac5b` -> `dev-soft-core`, head `bbfdb6746d585e490508783dc8a88c79fbab02c0`, four commits on `300da99beed5bb1c77e4b04af0bb4f9369856e0d`.

- Both release routes fit and meet the #818 floor at every corner: 8x8/1if 46,246 LUT (-375 against the base), 1x1/1if 32,639 LUT (-41). BRAM and DSP equal at both shapes.
- Full sweep, four shards: 65 suites, 2,715,829 checks, 0 in-suite failures. 64 pass in the sweep; `mbx` passes re-run with the CI's `--no-print-directory` (its mutation harness parses make's output, and the local run lacked that flag).
- `tsn_fuzz` with its field campaigns: gPTP/802.1AS 675 pass and AAF/AVTP 164 pass, both equal to the tracked results.
- milan_dp `gptp` and `gptp-lat` 212/212 each, `[CA]` 0x22 and 0xFE on the wire. The physical `milan_dp_gptp` suite passes, 205 checks.
- Builder legs and union: ALL GATES PASS EXCEPT 1 NOT RUN in each leg (dev's two), 113 gates exactly once. `plat_ledger` 0 findings; the 24 firmware image digests equal the base's.
- Every `run:` step of the docs workflow at the head: 56 rc 0, 24 not run with a recorded reason (installs and hosted recorders), 3 refused by this host's RV32 SDK install-verify (no provenance receipt, as on the base).
- The whole-tree lint, the Yosys elaboration of `milan_datapath`, `KL_pp_shadow` and `KL_gptp_shadow`, the open synthesis of the four gPTP plane tops and `milan_datapath`, `ooc_selftest.py` and `split-cdc` pass at the head.

## Linked Issue / roles

Closes #994

Executor: `[A835]`
Internal cleared-context reviewer: to be named
External reviewer: to be named

## Description

Moves the `gptp-processor` gitlink from `1616fc8f` to FPGA-gPTP main `1213ac5b9e09b8759ba76cc70c53652b5e108996`, the merge of FPGA-gPTP PR #108, and carries the new pin to every pin site.

`1213ac5b`'s tree is `7b579e33`, the tree of PR #108's reviewed head `331e27de`, which both its reviews passed (R905-2 and R906-2, each `POSITIVE` at that exact head). It fast-forwards `1616fc8f` on the donor's `main` through three merges:

| Donor issue | Merged PR | Parent-visible result |
|---|---|---|
| #102 | #103 | Test infrastructure only: the engine mutation arm runs its mutants at once. No `hdl/` or `syn/` change |
| #104 | #105 | Test infrastructure only: the engine builds compile through ccache. No `hdl/` or `syn/` change |
| #106 | #108 | The handler that takes the grandmaster role sends the first Announce and arms the 1 s cadence from it (IEEE 802.1AS-2011 Figure 10-15). Before, it armed a 2 ms beat, and an Announce at the receipt-timeout instant re-elected its grandmaster first, so the aged port's mastership never reached the wire. The role, asCapable and transmit-credit gates stay. The ROM shrinks by two words, to 1,013 of 1,024 |
| #107 | #108 | Taking the role always writes rate 0, so a mastership runs on this oscillator, the LocalClock (IEEE 802.1AS-2020 10.1.2.1). Before, the write applied only during a slew, so a mastership kept the slave's last trim, which a phase transient can wind to the +200 ppm rail. scaledLastGmFreqChange is the negated slave estimate, 0 when no slave rate was written since reset or since the last mastership (10.2.8.2.1 l), 11.4.4.3.9) |

No engine port, parameter or generator option changes, so no top-level port, parameter, register, builder or configuration change.

| Commit | Piece | Change |
|---|---|---|
| `973f2f20` | Gitlink | `1616fc8f` -> `1213ac5b`. The release routes ran at this commit; the two later commits change no synthesis input |
| `39e9c9d2` | Pin sites | The pin row in `docs/reference/SUBMODULES.md`; every engine-guide permalink (`GPTP_PLANE.md`, `TIME_SYNC.md`, the four `docs/guides/gptp/` pages, `docs/traceability/ieee8021as.md`, the SUBMODULES conflict list); both pin-bearing diagrams through `submodule_boundaries.gen.py` and `timesync_chain.gen.py`; the `gptp_ucode.hex` row of `syn/yosys/rom_digests.tsv` by `ooc.sh --record-rom-digests`, equal to the donor's tracked image (`4eb21cef...`) |
| `8c5a51e1` | Behaviour and records | `GPTP_PLANE.md` (the mastership's PHC write), `GM_LOSS_RECOVERY.md` (the first Announce at once and the mastership on this oscillator), `STRICTER_READINGS.md` (the Announce-at-the-instant row at `1213ac5b`), the #994 adoption record with the route figures in `SUBMODULES.md`, and the CHANGELOG |
| `bbfdb674` | Style | The same records within the audience style's ten-word sentence (the docs style gate's 18 findings at `8c5a51e1`) |

Historical measurement records that name `1616fc8f` (the CHANGELOG's earlier entries, the earlier SUBMODULES records, `AREA_BUDGET.md`, the #234 baseline finding, `pp_resource_baseline.json`'s `measured` strings, the `milan_dp` README's pre-#883 rows) stay as they are.

### The release routes

The release recipe (the split image, one interface) at 1x1/1if and 8x8/1if, at most two routes at once. Each takes the first placement directive that meets the build floor (#818: WNS >= +0.030 ns and WHS >= 0 at every signoff corner) in the recipe's order, ExtraPostPlacementOpt, ExtraTimingOpt, AltSpreadLogic_high. At 1x1 the first missed, as it does on the base, so all three were routed and the best is selected. The base is `300da99b`, whose image inputs were routed at `c2b2ba1a`: between the two only text and tests move, and the 24 firmware image digests at this head equal the base's.

| Image, directive | WNS / WHS, worst corner | LUT | FF | Slice | BRAM tiles | DSP |
|---|---|---:|---:|---:|---:|---:|
| 8x8/1if base, ExtraPostPlacementOpt | +0.105 / +0.036 ns | 46,621 | 53,338 | 15,570 | 98.5 | 13 |
| 8x8/1if, ExtraPostPlacementOpt, selected | +0.066 / +0.036 ns | 46,246 | 53,381 | 15,622 | 98.5 | 13 |
| 1x1/1if base, ExtraTimingOpt | +0.384 / +0.036 ns | 32,680 | 42,805 | 14,297 | 80.5 | 13 |
| 1x1/1if, ExtraPostPlacementOpt, misses the floor | +0.007 / +0.036 ns | 32,555 | 42,803 | 13,598 | 80.5 | 13 |
| 1x1/1if, ExtraTimingOpt, selected | +0.170 / +0.024 ns | 32,639 | 42,805 | 14,147 | 80.5 | 13 |
| 1x1/1if, AltSpreadLogic_high | +0.072 / +0.024 ns | 32,633 | 42,803 | 14,142 | 80.5 | 13 |

| Figure | 8x8/1if change | 1x1/1if change |
|---|---:|---:|
| LUT | -375 | -41 |
| FF | +43 | 0 |
| Slice | +52 | -150 |
| BRAM tiles / DSP | 0 / 0 | 0 / 0 |
| WNS / WHS, worst corner | -0.039 / 0 ns | -0.214 / -0.012 ns |

The qualifying images at each signoff corner (WNS / WHS, ns):

| Image | Slow_85C | Slow_0C | Fast_85C | Fast_0C |
|---|---|---|---|---|
| 8x8/1if, ExtraPostPlacementOpt | +0.066 / +0.102 | +0.066 / +0.102 | +1.660 / +0.036 | +1.660 / +0.036 |
| 1x1/1if, ExtraTimingOpt | +0.170 / +0.102 | +0.170 / +0.102 | +1.636 / +0.024 | +1.636 / +0.024 |

- Every route completes with 0 failing endpoints and no routing error, and every image passes the split image identity gate.
- Both selected images meet the #818 floor at every corner.
- The worst setup paths are outside the gPTP plane: `KL_mbx` read data at 8x8 (16 levels), the SoC bus bridge into the UART FIFO at 1x1 (11 levels). The 1x1 image's worst hold path, +0.024 ns, is a zero-level `chan_map_render` register pair on `clkout1`.
- Where the LUTs move at 8x8, by the placed hierarchy: the gPTP plane is -294 LUT net (the engine cell +912, the wrapper's own logic -1,397, logic synthesis moved across that boundary), `KL_mbx_cdc` +627, `milan_datapath`'s `stream_table` -439 and `csr` -269.

**The owner's exception.** FPGA-gPTP PR #108 measured the 8x8/1if image at +455 LUT against a parent base with the older pin. The owner [accepted that growth as a recorded exception](https://github.com/Mister-M-alt/FPGA-gPTP/pull/108#issuecomment-7121892317) on 2026-11-24 and left fit and the #818 floor gating the image that carries this pin. On this base the growth does not appear: the 8x8/1if image is 375 LUTs smaller and the 1x1/1if image 41 smaller, and both meet the floor. Nothing in this PR recovers area; the difference is in synthesis mapping of the composed train.

## Authoritative references

- IEEE 802.1AS-2020 10.1.2.1 (LocalClock entity), 10.2.4.14, 10.2.8.2.1 l), 10.3 (BMCA and port state machines), 10.6.3 (announce receipt timeout), 11.4.4.3.9, B.1.1
- IEEE 802.1AS-2011 Figures 10-13 (with Cor1) and 10-15
- Milan v1.2 4.2.6.2.3 and Table 4.2
- #994 scope and acceptance; FPGA-gPTP #106, #107 and its D1/D2/D3 ruling; FPGA-gPTP PR #108, its two `POSITIVE` reviews at `331e27de` and the [owner decision of 2026-11-24](https://github.com/Mister-M-alt/FPGA-gPTP/pull/108#issuecomment-7121892317)
- #818 (the build floor and the best of the three directives); `docs/integration/BUILDING.md` section 5
- `docs/design/GPTP_PLANE.md` (the integration contract), `docs/reference/SUBMODULES.md`

## How to get into the same state

```sh
git fetch origin 994-gptp-pin-1213ac5b
git checkout --detach bbfdb6746d585e490508783dc8a88c79fbab02c0
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
git submodule status
```

`git submodule status` shows `gptp-processor` at `1213ac5b9e09b8759ba76cc70c53652b5e108996`.

## How to validate

```sh
suite_logs=$(mktemp -d)
bash scripts/run_all_suites.sh "$suite_logs" --wait --shard 0/4
bash scripts/run_all_suites.sh "$suite_logs" --physical-gptp
make -C tb/verilator/milan_dp gptp
make -C tb/verilator/milan_dp gptp-lat
python3 sw/builder/test_builder.py --require-rv32
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$(mktemp -d)"
python3 scripts/docs_inventory.py --check
python3 scripts/check_gptp_docs.py
python3 scripts/check_submodule_docs.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --check
(cd syn/yosys && ./ooc.sh --record-rom-digests) && git diff --exit-code syn/yosys/rom_digests.tsv
git diff --check 300da99beed5bb1c77e4b04af0bb4f9369856e0d HEAD
```

Run the sweep line for each shard 0/4 to 3/4.

Expected result / pass criteria: every command exits 0. The four shards total 65 suites with 0 in-suite failures. `--physical-gptp` passes `milan_dp_gptp` (allow it more than its 6,900 s default on a loaded host). The gptp leg prints `[CA] 4 DUT Announce frame(s); last clockQuality 0xF822436A` and gptp-lat `... 0xF8FE436A`, each `212 checks: 212 PASS, 0 FAIL`. The builder bank ends `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's MAKEFLAGS arm and gate 11's absent calibration tree, as on the base). `plat_ledger` prints `plat_ledger: PASS (0 finding(s))`. `ooc.sh --record-rom-digests` leaves `rom_digests.tsv` unchanged. Run the suites with `MAKEFLAGS=--no-print-directory`, as CI does, and with `TSN_GEN_ROOT` set, so `tsn_fuzz` runs its field campaigns.

The routes follow the release recipe for each shape: `endstation_builder.py <config> --placement split`, the split boot's runtime, the platform image linked against a stand-in export's CSR map at one interface, then `milan_soc.py` with the builder's argv, `--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive <directive>` and `--build`. Each selected image is read at the four signoff corners and checked by `sw/litex/check_image_identity.py`.

## Known limitations / out of scope

- Area recovery of the 8x8/1if image stays with the optimisation line (#994 out of scope; the owner's decision). On this base there is no growth to recover.
- The resource gate's endpoints (`route-1x1`, `ooc-1x1`, `ooc-8x8`) are not re-measured. `route-1x1` measures the all-fabric image; this issue's acceptance names the release images, which are recorded above. The standalone tops, `KL_pp_shadow`, hold no gPTP logic.
- The firmware gate's four shards were not run: no firmware input moves. The 24 image digests (ELF, stripped and loadable, at the eight ledger points) equal the base's.
- No platform test is added. The behaviour is graded in the donor (engine phases 57 to 61 and nine planted defects), and the platform's consumers and legs pass unchanged. The donor review's suggestion to adopt a takeover phase (a mastership from a +-100 ppm grandmaster) into the parent's regression is follow-up work for a new Issue, not done here.
- Nothing here measures the board: the bench runs after the merge.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
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

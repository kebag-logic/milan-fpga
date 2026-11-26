[A850]

## Contents

- **[Status](#status)** — Gate tally, the two donor-caused gate failures, routes, and `1013-pins` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, dependency and environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN, local gates — `1013-pins` -> `dev-soft-core`, head `e5d8a71b6fa90352eca72314c7bd2275a1b20285`. The branch merges `dev-soft-core` at `c34e7d8b` (PR #987) as `d0483d08`, with no conflict. Round 2 (`e5d8a71b`) changes only test harnesses, their controls and documents.

- **The gPTP pin is FPGA-gPTP `3ce71b768a2f6f6a5274c127080146e755d02275`, the merge of its PR #110 (its issue 109).** That is the ruling on #1013. The issue first named `3009f9a2`, the next merge (its PR #112). That merge changes only the engine's test runner (`tb/verilator/engine/Makefile`, `pass_run.py`, `passes_test.py`, `docs/TEST_DEVELOPER.md`). Its two Python files exceed two of this repository's ratchets: the Python idiom budget, and the count of suite files that use host time or process deadlines. Neither budget moves, so the runner waits for a later pin.
- **At the head `e5d8a71b`:**
  - `scripts/check_py_idiom.py` and the test evidence ratchet pass with their budgets unchanged.
  - `gptp_plane`: 102 checks, `phc-step` 8/8 arms, `link_delay.py` 9/9.
  - `gptp_shadow`: 490 checks, its campaign 16/16, and the lifecycle.
  - The `milan_dp` legs `gptp` and `gptp-lat`: 242/242 each.
  - The docs workflow's `run:` steps of its gate jobs: 56 pass, 24 are skipped (installs and the hosted runner's recorders), and 3 fail. The 3 are the RV32 SDK install-verify in three jobs, which refuses on this host for want of a provenance receipt, as on the base.
- **The image inputs are identical to `3009f9a2`'s.** `hdl/` (the microcode generator included) and `syn/` have the same tree hashes at both commits. The `gptp_ucode.hex` ledger row has the same digest (`52293128...`). So the gates and routes below, run at `d0483d08` with the `3009f9a2` gitlink, stand for every image input. Only the gitlink and the records naming the pin changed after them.
- **At `d0483d08`:**
  - The complete firmware gate: four shards, rc 0, 847 of 847 planted defects caught, the five ADP length plants among them.
  - The stack boundary gate, both CI legs (`--without verilator` and `--only verilator`): PASS.
  - `gptp_tables` 36 checks and 26/26 controls; `gptp_txts` 95 checks and 13/13 controls.
  - `tsn_fuzz` (gPTP field campaign 675 pass); `milan_dp_gm_steps` 196 checks and its controls.
  - The physical `milan_dp_gptp` leg: 151 checks, plus its abort and recentre controls.
  - The egress ledger at 8x8-1if: PASS, its seven rows equal the base's to the 10 ns grade. Its self-test catches 18 of 18 mutants.
  - `plat_ledger`: PASS, every point's ROM, SRAM and tiles equal the base's.
- **Routes**: each selected release image equals its base pair in every reported figure, and meets the #818 floor at every corner. 8x8/1if ships on ExtraTimingOpt, as the base would: the first directive misses there too.

## Linked Issue / roles

Closes #1013

Executor: `[A850]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Moves both gitlinks to merged `main` commits:

| Gitlink | From | To | Parent-visible result |
|---|---|---|---|
| `gptp-processor` | `1213ac5b` | `3ce71b768a2f6f6a5274c127080146e755d02275`, the merge of FPGA-gPTP PR #110 | FPGA-gPTP #109 (PR #110): a negative computed link delay of any magnitude is a good exchange. The Sync path and the engine's publication use it signed, floored at -800 ns. 800 ns is good; 801 ns clears asCapable, as before. The ROM is word-neutral, 1,013 of 1,024 |
| `third_party/tsn-c-stack` | `715589c1` | `a795471c0abc4e38f7e5146b4e539dd607b6f501`, the merge of tsn-c-stack PR #38 | tsn-c-stack #37: an ENTITY_DISCOVER whose control_data_length is above 56 is read by its first 56 octets after entity_id. Below 56 it is discarded and counted, as before. Between the two pins only `src/adp.c` (one comparison) and `examples/rv32/smoke.c` change outside tests and documents |

No engine port, parameter or generator option changes, so no top-level port, parameter, register, builder or configuration change. The public bank's clamp to 0 (`KL_gptp_shadow.sv`, the unsigned CSR `GPTP_PDELAY` and the GET_AVB_INFO field) is unchanged, and is the only clamp to 0. The published and used delays differ by design, as the donor ruling records.

| Commit | Piece |
|---|---|
| `40f1a0e8` | Both gitlinks (gPTP at `3009f9a2` first; `a6864a49` moves it to `3ce71b76`) |
| `941bc2d9` | The stack consumer: `test_adp.cpp` and `ctrl_mutants.py`, the stack PR's prepared consumer patch, unchanged |
| `9b40757e` | Pin sites: the pin rows, every permalink to either pin, both diagrams through `submodule_boundaries.gen.py` and `timesync_chain.gen.py`, the `gptp_ucode.hex` ledger row by `ooc.sh --record-rom-digests`, the adoption records in `SUBMODULES.md`, `GPTP_PLANE.md`'s link delay table, and the change log |
| `1a76c9de` | The gPTP platform regression (below) |
| `d0483d08` | Merge of `dev-soft-core` `c34e7d8b` (PR #987), no conflict |
| `37a98e17` | The route record in `SUBMODULES.md` and the change log |
| `a6864a49` | The gPTP gitlink at `3ce71b76`, by the ruling on #1013: the pin sites, both diagrams and the ROM ledger row by their generators, the adoption record and the change log |
| `e5d8a71b` | Phase 22's graded pair carries its own 400 ns offset, so a pair not used or a stale public offset fails by name; two controls for that; the coverage statements in `GPTP_PLANE.md`, `SUBMODULES.md` and the change log restricted to what was measured |

Historical measurement records that name `715589c`, such as `SPLIT_CONTROL_MEMORY.md`'s and the service budget's, stay as they are.

### The stack consumer

`AdpAdapter.PinRejectsWrongDiscoveryControlLength` expected 57 and 2047 to be refused. It is replaced by two tests:

- `PinRejectsShortDiscoveryControlLength`: 0 and 55, with valid_time 0 and 31.
- `PinAcceptsLongDiscoveryThroughMailbox`: 57, 84 and 102 with the surplus present and absent, and 256 and 2047 with it absent. A 2047 is a truncated 82-octet frame, accepted.

Five plants in `ctrl_mutants.py`, each caught by its named test in the firmware gate's campaign:

| Plant | Named test |
|---|---|
| the check removed | `PinRejectsShortDiscoveryControlLength` |
| valid_time counted as length | `PinRejectsShortDiscoveryControlLength` |
| the mask narrowed to 0x00FF | `PinAcceptsLongDiscoveryThroughMailbox` |
| the previous exact comparison | `PinAcceptsLongDiscoveryThroughMailbox` |
| 56 refused | `PinAcceptsCompleteDiscoveryThroughMailbox` |

The patch was prepared against `dev-soft-core` at `5de21ff3`, whose stack pin is `715589c1` (the stack review's S3). That is this PR's base, and the patch applies unchanged. The review's S1 and S2 are suggestions for the stack's own tests and its RV32 smoke image. They are not taken here: the parent cannot carry them without changing the stack.

### The gPTP platform regression

Three suites grade #109 where the product sees it: through the parent's transport and the real PHC. Each was run against the 1213ac5b generator (only `milan_dp`'s `gptp` leg, not `gptp-lat`). Each is red there and green at this head.

| Suite | Trials | Graded | At the 1213ac5b generator |
|---|---|---|---|
| `tb/verilator/gptp_plane` phase 6 | -3, -80, -81, -263, -800, -801, -5,000,000 ns, then 800 and 801 ns | The engine against the real counter, to the nanosecond. The peer's clock is this one plus a constant, so neighborRateRatio is exactly 1 and the residence sets the delay. Each negative trial: asCapable kept; the engine's word is the delay floored at -800 ns; the next Follow_Up is used and its offset is exact; no PHC step; the grandmaster stays. 800 is good; 801 clears asCapable and its next Follow_Up is not used | 32 of 102 checks fail, from -81 on |
| `tb/verilator/gptp_shadow` phase 22 | -3, -80, -81, -263, -801, -5,000,000 ns, then 800 and 801 ns | The slice: the tap's stamps, the frame FIFO, the ledger, the real counter and the public bank. The peer answers from the plane's own t1 and the tap's own t4, so the delay is exact. Each negative trial reads 0 in the public bank. A graded Sync/Follow_Up pair then follows, built 400 ns off where the background pairs are built at 0. Its offset must move by those 400 ns, within 64 ns, which it does only when the plane uses that pair with the delay floored at -800 ns. A pair the plane does not use, or a bank that keeps a stale offset, fails. No PHC step. 800 reads 800 | 25 of 490 checks fail, from -81 on, among them `#109 -81 ns: the graded Follow_Up is used: its offset is fresh` |
| `tb/verilator/milan_dp` `gptp` and `gptp-lat` | -3, -80, -81, -263, -5,000,000 ns | The product datapath: the CSR `0x6E4` reads 0, asCapable holds, and GET_AVB_INFO's propagation delay reads 0, each trial | `gptp`: 3 of 242 checks fail, `[#109] delay -81 ns: asCapable kept`, and -263 and -5,000,000 |

Planted defects, each caught by name:

| Defect | Where | Named check that fails |
|---|---|---|
| the -80 ns floor restored (the 1213ac5b window) | `link_delay.py` | `link delay -81: asCapable kept`, and -263, -800, -801, -5,000,000 |
| no floor | `link_delay.py` | `link delay -801: its offset uses the delay exactly`; `link delay -5000000: no PHC step` |
| the used delay clamped to 0 | `link_delay.py` | `link delay -3: its offset uses the delay exactly`, and -80, -81, -263 |
| a floor at 0 | `link_delay.py` | `link delay -263: its offset uses the delay exactly`, and its publication |
| a floor at -799 ns | `link_delay.py` | `link delay -800: its offset uses the delay exactly`, and its publication |
| publication before the floor | `link_delay.py` | `link delay -801` and `-5000000: the engine publishes the used delay` |
| 801 ns good | `link_delay.py` | `link delay 801: asCapable clears` |
| 800 ns bad | `link_delay.py` | `link delay 800: asCapable kept` |
| the public clamp removed | `gptp_shadow/mutants.py` | `#109 -263 ns: the public bank reads 0` |
| the public bank keeps a stale offset | `gptp_shadow/mutants.py` | `#109 -263 ns: the graded Follow_Up is used: its offset is fresh` |
| the harness sends no graded Follow_Up (a control on the harness) | `gptp_shadow/mutants.py` | `#109 -263 ns: the graded Follow_Up is used: its offset is fresh` |

`link_delay.py` plants each defect in the pinned generator, one image each. It runs them on the binary `make run` built, with the phase alone (`+link-delay-only`); the unplanted image must pass every check. It is part of `gptp_plane`'s default target and takes about 40 s here. The same three defects the issue names also fail by name through `gptp_shadow`, as disposable probes:
- the -80 floor: `#109 -263 ns: asCapable kept`;
- no floor: `#109 -5000000 ns: no PHC step`;
- the clamp removed: `#109 -263 ns: the public bank reads 0`, which reads `0xFFFFFEF9`.

### The engine's test runner

FPGA-gPTP PR #112 (its issue 111) runs the engine suite's four passes as make jobs of their own. It is not adopted here. At `3009f9a2` its two new Python files fail this repository's Python idiom budget: 1 unannotated and 7 undocumented public functions, and a function with 7 parameters, one over its budget. `passes_test.py` is also a fourth suite file using host time or process deadlines, against a budget of 3. Both budgets may only go down. A later pin adopts the runner once a donor change brings it inside both. The engine's own suite at `3ce71b76` runs its four passes in sequence, as at `1213ac5b`.

### The release routes

The release recipe (the split image, one interface) at 1x1/1if and 8x8/1if, at most two routes at once, directives in the recipe's order. The head is the merge `d0483d08`, and the base is `dev-soft-core` at `c34e7d8b`, routed alike. The head's gPTP gitlink was `3009f9a2`, whose `hdl/` and `syn/` trees equal `3ce71b76`'s, so these images are this pin's. They differ only in ROM contents: the gPTP image and the control firmware.

| Image, directive | WNS / WHS, worst corner | LUT | FF | Slice | RAMB36 / tiles | DSP |
|---|---|---:|---:|---:|---:|---:|
| 1x1/1if base, ExtraPostPlacementOpt | +0.178 / +0.021 ns | 32,582 | 42,803 | 13,590 | 63 / 80.5 | 13 |
| 1x1/1if, ExtraPostPlacementOpt, selected | +0.178 / +0.021 ns | 32,582 | 42,803 | 13,590 | 63 / 80.5 | 13 |
| 8x8/1if base, ExtraPostPlacementOpt, misses the floor | +0.008 / +0.036 ns | 45,920 | 53,383 | 15,603 | 82 / 98.5 | 13 |
| 8x8/1if base, ExtraTimingOpt | +0.283 / +0.036 ns | 45,810 | 53,378 | 15,600 | 82 / 98.5 | 13 |
| 8x8/1if, ExtraPostPlacementOpt, misses the floor | +0.008 / +0.036 ns | 45,920 | 53,383 | 15,603 | 82 / 98.5 | 13 |
| 8x8/1if, ExtraTimingOpt, selected | +0.283 / +0.036 ns | 45,810 | 53,378 | 15,600 | 82 / 98.5 | 13 |
| 8x8/1if, AltSpreadLogic_high, no base pair | +0.146 / +0.036 ns | 45,814 | 53,381 | 15,594 | 82 / 98.5 | 13 |

- Three head routes have a base route at the same directive: 1x1 ExtraPostPlacementOpt, and 8x8 ExtraPostPlacementOpt and ExtraTimingOpt. Each equals its pair in every reported figure: the four corners' WNS and WHS, and the utilization. The head's 8x8 AltSpreadLogic_high route has no base pair.
- Against the base, the selected images change LUT, FF and RAMB36 by 0 at both shapes.
- The bitstreams, ROM images and firmware ELFs of head and base differ, as they must. Placements were not compared beyond these reported figures.
- 8x8/1if misses the floor on its first directive at the base too (+0.008 ns), so the miss comes with the base. All three directives were routed, and the best worst-corner WNS ships (#818).
- The selected 8x8 image also meets WHS >= +0.030 ns. The 1x1 image's worst WHS is +0.021 ns, which the #818 floor (WHS >= 0) accepts, as on the base.
- Every route completes with 0 failing endpoints and no routing error. Every image passes the split image identity gate.

## Authoritative references

- IEEE 802.1AS-2011 11.2.2 b), Figure 11-8 (with Cor1), 11.2.13.2.1 f), 11.2.15.2.4
- IEEE 802.1AS-2020 11.2.2, 11.2.13.7, 11.2.14.2.1, 11.2.19.3.4
- Milan v1.2 4.2.6.1.1, 4.2.6.2.7, 5.6.3.1 and Table 5.50
- IEEE 1722.1-2021 6.2.2.6 and 6.2.7.1.3; IEEE 1722-2016 4.4.5.4
- #1013 scope, acceptance and its ruling on the pin; FPGA-gPTP #109 and its ruling, PR #110, #111 and PR #112; tsn-c-stack #37 and PR #38
- #818 (the build floor and the best of three directives)
- `docs/reference/SUBMODULES.md`, `docs/design/GPTP_PLANE.md` (the link delay verdict), `tb/verilator/gptp_plane/README.md`, `tb/verilator/gptp_shadow/README.md`

## How to get into the same state

```sh
git fetch origin 1013-pins
git checkout --detach e5d8a71b6fa90352eca72314c7bd2275a1b20285
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
git submodule status
```

`git submodule status` shows `gptp-processor` at `3ce71b768a2f6f6a5274c127080146e755d02275` and `third_party/tsn-c-stack` at `a795471c0abc4e38f7e5146b4e539dd607b6f501`.

## How to validate

```sh
export MAKEFLAGS=--no-print-directory
make -C tb/verilator/gptp_plane
make -C tb/verilator/gptp_shadow
make -C tb/verilator/gptp_tables
make -C tb/verilator/gptp_txts
make -C tb/verilator/milan_dp gptp
make -C tb/verilator/milan_dp gptp-lat
for k in 0 1 2 3; do python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard $k/4; done
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$(mktemp -d)"
python3 scripts/check_doc_style.py
python3 scripts/check_gptp_docs.py
python3 scripts/check_submodule_docs.py
python3 scripts/check_py_idiom.py
python3 scripts/measure_test_evidence.py
(cd syn/yosys && ./ooc.sh --record-rom-digests) && git diff --exit-code syn/yosys/rom_digests.tsv
```

Expected result / pass criteria:
- `gptp_plane` prints `102 checks: 102 PASS, 0 FAIL`, `phc_step campaign: 8 checks` and `link_delay campaign: 9 checks: 9 PASS, 0 FAIL`.
- `gptp_shadow` prints `490 checks: 490 PASS, 0 FAIL` and `controls: 16   failures: 0`, with `public_bank_publishes_a_negative_delay: caught by "#109 -263 ns: the public bank reads 0"`, and `public_bank_keeps_a_stale_offset` and `graded_follow_up_not_sent` each caught by `"#109 -263 ns: the graded Follow_Up is used: its offset is fresh"`.
- Each `milan_dp` leg prints `242 checks: 242 PASS, 0 FAIL` and five `[#109]` lines.
- The firmware shards exit 0, the campaign printing `mutants: 847 of 847 caught`. Both boundary legs print `ctrl_boundary: PASS`, and `plat_ledger` prints `PASS (0 finding(s))`.
- `check_py_idiom.py` and `measure_test_evidence.py` exit 0, with `scripts/py_idiom.budget` and `scripts/test_evidence.budget` unchanged.

To see the regression go red, replace `gptp-processor/hdl/ucode/gen_gptp_ucode.py` with 1213ac5b's and run `make -C tb/verilator/gptp_plane run` (32 FAIL) and `make -C tb/verilator/gptp_shadow run` (15 FAIL).

## Known limitations / out of scope

- FPGA-gPTP PR #112's test runner waits for a later pin (above).
- The `adp` mailbox channel's 128-octet frame limit is unchanged: a discover of up to 102 octets of control data in a complete frame reaches the firmware. A longer frame is dropped and counted in RX_DROP (#1013 out of scope).
- The stack review's S1 and S2 belong to the stack's own tests (above).
- `gptp_shadow`'s default target builds and runs the simulation 17 times now (the run and 16 controls), against 14. Its hosted window on dev-soft-core was 478 s. `scripts/suite_shards.py` registers 393 s and `gptp_plane` 784 s, against a hosted 900 s. Phase 22 adds about 10 s to each shadow run here, and `gptp_plane` about 50 s in all. The registered figures are measured data and are left as they are: replace them from this head's hosted window (`suite_shards.py --measure`).
- The RV32 SDK install-verify step refuses on this host for want of a provenance receipt, as on the base. The other docs steps ran with the host's pinned SDK.
- The firmware, boundary, ledger, tables, txts, fuzz, gm-steps and physical-leg results are `d0483d08`'s. Between that commit and the head only the gPTP gitlink moves, from `3009f9a2` to `3ce71b76`, with identical `hdl/` and `syn/`, plus records and one comment in `link_delay.py`.
- Nothing here measures the board: the bench runs after the merge.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (the gPTP pin as ruled on #1013)
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

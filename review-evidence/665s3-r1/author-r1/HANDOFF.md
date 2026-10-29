# [A697b] #665 S3 — the target platform firmware: handoff

STATUS: **STOP** posted at head `5edbba1d`: issuecomment-6505966612 (text in `STOP-COMMENT.md`). Every gate the
change touches passed at that head, rc 0 (gate table below); four decisions are needed ("Decisions asked").

- Lane: S3 of the Mark II split (#665), assignment [A10] issuecomment-6493622258, plan [A678] PLAN.md section S3.
- Branch `665-s3-platform`, head `5edbba1d333dbebfaca4bfc4ab85debdac1c7e55`, base `origin/dev-soft-core`
  `f4c9ad4f06f185378fd2646298aab51dd108e86f` (an ancestor of the head; `origin/dev-soft-core` has not moved).
  Origin verified `https://github.com/kebag-logic/milan-fpga.git`. No submodule pin moved; no git command run in a
  submodule.
- [A697] wrote the code (15 commits); its unit was OOM-killed at 24 GB. [A697b] (this session) changed no tracked file:
  it re-ran the gates at the head in separate 10 GB units and resolves the open item by STOP.
- [A697]'s TAKEN: issuecomment-6493758126. Its handoff and receipts stay in `../665s3-a697/`; what this session keeps
  is under `receipts/` (index generated from the files present).
- Nothing pushed; no PR created or edited; no issue or PR comment edited. No RTL changed (no `hdl/`, `milan_soc.py`,
  `.github/`), so the full sweep is not run. `milan_baremetal.c` is read, never edited.

## Why STOP (the open item, resolved)

The 8x8 two-interface platform image plans **59.0 RAMB36** (rom 125,040 B in 126,976; sram 113,936 B in 114,688).
Ruling 6425357821 item 1: "STOP if any other point goes over 56, or if the ledgered point goes over 57.5." The
override (`sw/litex/ctrl_memory.py:206`, `LEDGERED`) recognises the size fixture's image by its symbols and plans it
to 57.5; it refuses the platform's image (it does not carry `image_allocation`), and at 59.0 the platform would be
over 57.5 even if it did.

It cannot be brought to 57.5 inside S3's files. Banks are power-of-two RAMB18 granules per region
(`ctrl_memory.py:51`). The fixture's own sram (113,008 B) already needs 28.0 tiles, and 27.5 holds 112,640 B, so the
sram half cannot shrink without cutting shared state. With sram at 28.0, rom must fit 29.5 tiles (120,832 B):
a cut of 4,208 B from the platform's 5,216 B of rom, leaving about 1 KB for the boot, the CSR policy, the
console and the ports. The three other points fit: 39.0, 42.0, 52.0.

## Changes (file:line, reason)

### Firmware (`sw/firmware/ctrl/`)

| Where | What | Why |
|---|---|---|
| `app/ctrl_app.c:87` `ctrl_app_open_held`, `:93` `ctrl_app_release_adp`, `:74`, `:40`; `app/ctrl_app.h:99` | The open with ADP held, and ADP's start after it. `ctrl_app_open`'s text is unchanged but one line: ADP's enable reads `!app->adp_held`, false unless the held open set it. | Boot step 9 (Milan v1.2 5.6.1): ADP starts only once AECP and ACMP accept requests. A configuration field was tried first (`74eddc47`) and broke every positional `ctrl_app_config` in the tests; `8e55b1ae` replaced it. |
| `plat/ctrl_plat.c:226` `ctrl_plat_boot` | Steps 2 to 9 in order: identity, policy, MAAP's one-owner report (`:179`), the AEM image's CRC, composition (`:194`) with the console's poll (`:251`), the saved state (`:257`), the held open (`:259`), SRP, AECP's release (`:267`), ADP last (`:271`). A refused stage prints one line and leaves only the console. | ARCHITECTURE_HW_SW_SPLIT.md section 2; the assignment. |
| `plat/ctrl_plat.c:54`, `:66`, `:92`, `:139`, `:147` | MAAP's `maap_csr_port` on interface 0's window (another interface's writes dropped and counted); the allocation recorded after the window has it; ACMP's talker source port from the identity and that allocation (Milan v1.2 5.5.4.1); SRP's sources from the generated streams; the licence port. | maap/README.md "Integration"; srp/README.md "Integration still owed". |
| `plat/ctrl_plat.c:275` `ctrl_plat_step` | A loop step once ready, else the console alone. | The all-fabric image keeps its console when its fabric stays disabled. |
| `plat/ctrl_plat_csr.c:28` `ctrl_plat_csr_policy`, `:21`, `:51`, `:70` | `configure_fabric()`'s fifteen writes in its order; the identity check; the status reads in `milan_status_handler()`'s order; the bounded time-of-day read. | REQUIREMENTS.md:22-23; the acceptance's trace. |
| `plat/ctrl_plat_console.c:174` `ctrl_plat_console_poll`, `:139`, `:157`, `:102`, `:89`, `:57`, `:49` | D6's console: `milan_status` and `milan_gettime` in `milan_baremetal.c`'s lines, `?` for anything else; at most 16 bytes in and out per pass, one command per pass, only with ring room. | D6; #397's tick rule. |
| `plat/ctrl_plat_mmio.c`, `plat/ctrl_plat_io.h` | The two-call bus port for the CSR window and the UART. | One seam the tests answer. |
| `plat/ctrl_plat_main.c:27` | `main`: the generated words, the LiteSPI flash port, the endless step loop. | `ctrl_split_start.S` calls `main`. |
| `plat/ctrl_plat_gen.py:88`, `:127`, `:72` | The policy header from `boot_policy.fabric_constants()` and the lwSRP table; the bus map from the SoC's `csr.csv`, refusing a UART that pops on its read. | Generated, never hand-written. |
| `plat/README.md` | The platform's page. | |

### Tests and gates (`sw/firmware/ctrl/test/`, `sw/firmware/gtest/`)

| Where | What |
|---|---|
| `test_plat.cpp`, `test_plat_mmio.cpp`, `plat_bus.{hpp,cpp}` | C1-C4 (CSR window), K1-K6 (console), I1-I2 (MMIO) on a host bus logging every access. |
| `test_plat_boot.cpp` | B1-B9: the boot in step order and each refused stage on the mailbox model, F1's flash model and the host bus, one access order for all three; at one and two interfaces. |
| `plat_trace.py` | The CSR policy's writes against `milan_baremetal.c`'s `configure_fabric()` (builder gate 35's host run) for every shipped config, and three plants. |
| `plat_arms.py` | The arms `plat`, `platboot` (1, 2), `platrv32`, `plattrace`. |
| `plat_mutants.py` | 37 planted defects in the control campaign. |
| `ctrl_plat_image.py`, `ctrl_plat_csr.csv` | The platform image's link through `ctrl_srp_image.py`'s link, audits and plan; the BSS report with `ctrl_plat` by member; the fixture map. |
| `test_ctrl_firmware.py` (shared) | The arms in the suites and the coverage run. |
| `ctrl_mutants.py` (shared) | The table, `NAMED_SOURCES` and the three arms. |
| `acmp_review_mutants.py` (shared) | `APP_OPEN`'s ADP line follows `ctrl_app_open`'s one changed line. |
| `ctrl_configs.py`, `ctrl_runs.py` (shared) | The boundary gate: the image builder known and run on the fixture map at both shapes and interface counts; the other new builders classified. |
| `sw/firmware/gtest/README.md` (shared) | Three coverage exclusion rows for `ctrl_plat.c`'s unreachable module refusals. |
| `sw/firmware/gtest/coverage.ratchet` (shared) | The five platform files, through `fw_coverage.py --write`. |

### Simulation (`tb/verilator/ctrl_split_boot/`)

`boot_soc.py` (the CPU budget harness's SoC, imported read only, plus the CSR window and UART on pads), `sim_main.cpp`,
`run.py` (build, run, grade, `--regrade`, `--self-test` with two plants), `README.md`.

### Docs

`docs/ARCHITECTURE_HW_SW_SPLIT.md` section 5; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 4 and 5;
`sw/firmware/ctrl/README.md` (layout, linked size, arm table); `maap/README.md`, `srp/README.md` (integration).

Shared files touched, for the parallel lanes (S2b edits several of them): `ctrl_mutants.py`,
`acmp_review_mutants.py`, `test_ctrl_firmware.py`, `test_ctrl_firmware_shards.py` (`f27d08e3`: the platform arms
stood in for the shard dispatch proof), `ctrl_configs.py`, `ctrl_runs.py`, `gtest/README.md`,
`coverage.ratchet`, `app/ctrl_app.{c,h}`, `SPLIT_CONTROL_MEMORY.md`. Each edit is additive except the one line of
`ctrl_app_open` and its anchor.

## New checks, planted mutants and failing words

### The arms (`sw/firmware/ctrl/test/plat_arms.py`, run by `test_ctrl_firmware.py`)

| Arm | Tests | What each proves |
|---|---|---|
| `plat` | `Plat.C1`-`C4`, `Plat.K1`-`K6`, `PlatMmio.I1`-`I2` | C1 identity (`MILN` or refused, VERSION read, no write); C2 the fifteen writes in order from the policy, the two enables clear; C3 the status read order; C4 the time of day (snapshot first, a torn read retried, refused after three); K1 `milan_status`'s lines field for field, AEM loaded/disabled; K2 `TAI_NS`, or none on a torn read; K3 line ends, `?`, an overflowed line dropped whole; K4 the per-pass bound (16 in, 16 out, never into a full FIFO, one command, only with room, no input while a line waits, a full slice owed); K5 the ring's drop count; K6 the number formats |
| `platboot` (1 and 2 interfaces) | `Boot.B1`-`B9` | B1 step order: identity read first, the policy, MAAP's one owner, then the mailbox; the face commit before ADP's first timer; one banner, the ready line last. B2-B6 each refused stage stops where it must. B7 only a ready boot services the loop. B8 the ports. B9 SRP's sources |
| `platrv32` | one check | the whole platform cross-compiled freestanding for RV32I: ABI, instruction set, runtime closure |
| `plattrace` | 8 checks | five shipped configs' CSR writes equal to `milan_baremetal.c`'s `configure_fabric()` (gate 35's host run), and three plants caught |

### The control campaign's 37 platform defects (`plat_mutants.py`)

Each must make the named test fail with the named words (`ctrl_mutants.campaign`).

| Plant | File | Arm | Test | Failing words |
|---|---|---|---|---|
| `plat-policy-write-skipped` | `plat/ctrl_plat_csr.c` | plat | `Plat.C2PolicyIsConfigureFabricsFifteenWritesInOrder` | `C2 configure_fabric's writes, in its order, from the policy` |
| `plat-policy-writes-reordered` | `plat/ctrl_plat_csr.c` | plat | `Plat.C2PolicyIsConfigureFabricsFifteenWritesInOrder` | `C2 configure_fabric's writes, in its order, from the policy` |
| `plat-policy-word-wrong` | `plat/ctrl_plat_csr.c` | plat | `Plat.C2PolicyIsConfigureFabricsFifteenWritesInOrder` | `C2 configure_fabric's writes, in its order, from the policy` |
| `plat-policy-advertiser-left-on` | `plat/ctrl_plat_csr.c` | plat | `Plat.C2PolicyIsConfigureFabricsFifteenWritesInOrder` | `C2 no fabric advertiser beside the core` |
| `plat-identity-unchecked` | `plat/ctrl_plat_csr.c` | plat, platboot1 | `Plat.C1IdentityIsMilnAndReadsVersion`; `Boot.B2ForeignWindowStopsAtIdentity` | `C1 any other ID is refused`; `B2 a foreign window stops the boot` |
| `plat-status-pair-high-first` | `plat/ctrl_plat_csr.c` | plat | `Plat.C3StatusIsReadInMilanStatusOrder` | `C3 each pair low then high` |
| `plat-tod-no-snapshot` | `plat/ctrl_plat_csr.c` | plat | `Plat.C4TimeOfDayIsSnapshotThenAgreeingHighWords` | `C4 the snapshot strobe comes first` |
| `plat-tod-torn-accepted` | `plat/ctrl_plat_csr.c` | plat | `Plat.C4TimeOfDayIsSnapshotThenAgreeingHighWords` | `C4 the agreeing high word` |
| `plat-status-aem-inverted` | `plat/ctrl_plat_console.c` | plat | `Plat.K1MilanStatusAnswersTheGradersLines` | `K1 milan_status's lines, field for field` |
| `plat-tod-torn-printed` | `plat/ctrl_plat_console.c` | plat | `Plat.K2MilanGettimeAnswersTaiNs` | `K2 a torn read prints no number` |
| `plat-prefix-is-a-command` | `plat/ctrl_plat_console.c` | plat | `Plat.K3LinesEndOnceAndOthersAreRefused` | `K3 a prefix is no command` |
| `plat-overflow-kept` | `plat/ctrl_plat_console.c` | plat | `Plat.K3LinesEndOnceAndOthersAreRefused` | `K3 an overflowed line is dropped whole` |
| `plat-dec-leading-zeros` | `plat/ctrl_plat_console.c` | plat | `Plat.K6NumbersAtTheirEdges` | `K6 no leading zeros` |
| `plat-hex-seven-digits` | `plat/ctrl_plat_console.c` | plat | `Plat.K6NumbersAtTheirEdges` | `K6 eight lower-case digits` |
| `plat-ring-drop-uncounted` | `plat/ctrl_plat_console.c` | plat | `Plat.K5TextPastTheRingIsDroppedAndCounted` | `K5 the ring holds TX_BYTES and drops the rest` |
| `plat-tx-unbounded` | `plat/ctrl_plat_console.c` | plat | `Plat.K4EachPassIsBounded` | `K4 at most TX_PER_PASS bytes out` |
| `plat-rx-unbounded` | `plat/ctrl_plat_console.c` | plat | `Plat.K4EachPassIsBounded` | `K4 at most RX_PER_PASS bytes in` |
| `plat-tx-into-full-fifo` | `plat/ctrl_plat_console.c` | plat | `Plat.K4EachPassIsBounded` | `K4 never into a full FIFO` |
| `plat-command-without-room` | `plat/ctrl_plat_console.c` | plat | `Plat.K4EachPassIsBounded` | `K4 a command runs only with room for the longest response` |
| `plat-input-while-waiting` | `plat/ctrl_plat_console.c` | plat | `Plat.K4EachPassIsBounded` | `K4 no input is taken while a line waits` |
| `plat-slice-not-owed` | `plat/ctrl_plat_console.c` | plat | `Plat.K4EachPassIsBounded` | `K4 a full slice of input is owed another pass` |
| `plat-mmio-read-neighbour` | `plat/ctrl_plat_mmio.c` | plat | `PlatMmio.I1ReadIsTheWordAtTheAddress` | `I1 a read returns the word at the address` |
| `plat-mmio-write-neighbour` | `plat/ctrl_plat_mmio.c` | plat | `PlatMmio.I2WriteIsTheWordAtTheAddressAlone` | `I2 a write lands in the word at the address` |
| `plat-adp-before-aecp` | `plat/ctrl_plat.c` | platboot1 | `Boot.B1ReachesReadyInStepOrder`; `Boot.B6UnacknowledgedFaceStopsAtAecp` | `B1 ADP's first timer after the face commit`; `B6 ADP never starts` |
| `plat-adp-not-held` | `plat/ctrl_plat.c` | platboot1 | `Boot.B1ReachesReadyInStepOrder` | `B1 ADP's first timer after the face commit` |
| `app-adp-hold-ignored` | `app/ctrl_app.c` | platboot1 | `Boot.B1ReachesReadyInStepOrder`; `Boot.B6UnacknowledgedFaceStopsAtAecp` | `B1 ADP's first timer after the face commit`; `B6 ADP never starts` |
| `plat-no-one-maap-owner` | `plat/ctrl_plat.c` | platboot1 | `Boot.B1ReachesReadyInStepOrder`; `Boot.B3RefusedImageStopsAtImage` | `B1 the mailbox only after the policy and the one MAAP owner`; `B3 after the policy and the one MAAP owner` |
| `plat-maap-port-unrefused` | `plat/ctrl_plat.c` | platboot1 | `Boot.B4RefusedStreamCountStopsAfterThePolicy` | `B4 MAAP's port refuses nine AAF outputs` |
| `plat-image-unchecked` | `plat/ctrl_plat.c` | platboot1 | `Boot.B3RefusedImageStopsAtImage` | `B3 a refused image stops the boot` |
| `plat-mailbox-unchecked` | `plat/ctrl_plat.c` | platboot1 | `Boot.B5OtherContractStopsAtMailbox` | `B5 another contract stops the boot` |
| `plat-aecp-unchecked` | `plat/ctrl_plat.c` | platboot1 | `Boot.B6UnacknowledgedFaceStopsAtAecp` | `B6 no acknowledgement, no AECP` |
| `plat-loop-before-ready` | `plat/ctrl_plat.c` | platboot1 | `Boot.B7OnlyAReadyBootServicesTheLoop` | `B7 and never services the loop` |
| `plat-source-past-count` | `plat/ctrl_plat.c` | platboot1 | `Boot.B8PlatformPortsAnswerAsDocumented` | `B8 a source past the reported count` |
| `plat-source-address` | `plat/ctrl_plat.c` | platboot1 | `Boot.B8PlatformPortsAnswerAsDocumented` | `B8 source n holds base + n` |
| `plat-window-interface-ignored` | `plat/ctrl_plat.c` | platboot2 | `Boot.B8PlatformPortsAnswerAsDocumented` | `B8 and nothing reaches interface 0's` |
| `plat-licence-sticky` | `plat/ctrl_plat.c` | platboot1 | `Boot.B8PlatformPortsAnswerAsDocumented` | `B8 a revocation clears it` |
| `plat-source-vid` | `plat/ctrl_plat.c` | platboot1 | `Boot.B9SrpSourcesCarryTheGeneratedStreams` | `B9 on the SR class VID` |

### `plattrace`'s own plants (`plat_trace.py`)

| Plant | Caught by |
|---|---|
| a write skipped (`LWSRP_VID`) | the shipping config's write list differing from `configure_fabric()`'s |
| two writes reordered (`ADP_EID_LO`/`HI`) | the same |
| a wrong word (`LWSRP_CTRL` without the admission enable) | the same |

### The boot simulation's plants (`tb/verilator/ctrl_split_boot/run.py --self-test`)

| Plant | Must be graded |
|---|---|
| `csr-write-skipped` (the `LWSRP_VID` write out of `ctrl_plat_csr.c`) | a `TRACE:` finding |
| `console-blocks` (a spin of 700,000 turns, about 0.7 s, before `milan_status`'s response; `5edbba1d`) | a `UART:` finding: the duty past #397's 500 ms tick rule |

## Gate table

Every gate at `5edbba1d`, each in a fresh clone of the head (submodules at their gitlinks) and its own transient
unit (MemoryMax 10G, a CPU range of its own); the tree was clean after every one. Receipts:
`receipts/gates-at-5edbba1d/` (this session) and `receipts/kept-from-a697-at-5edbba1d/` ([A697]'s complete logs at
the same head, kept rather than re-run).

| Gate | Command | Result | rc | s | Receipt |
|---|---|---|---:|---:|---|
| firmware unit, tally | `python3 sw/firmware/gtest/tally_selftest.py` | pass | 0 | 10 (with the next) | `fw_rv32_and_tally_selftest.log` |
| firmware unit, RV32 | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 17 checks PASS | 0 | | same |
| firmware self-test, shard 0 (suites) | `test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4` | PASS; arms `plat`, `platboot` x2, `platrv32`, `plattrace` (3 plants caught) | 0 | 326 | `selftest-shard0.log` |
| firmware self-test, shard 1 (control campaign) | `... --shard 1/4 --jobs 4` | 565 of 565 caught, the 37 platform defects among them | 0 | 1145 | `selftest-shard1.log` |
| firmware self-test, shard 2 (AECP campaign) | `... --shard 2/4 --jobs 4` | 137 caught | 0 | 792 | kept: `selftest-shard2.log` |
| firmware self-test, shard 3 (SRP campaigns, pin controls) | `... --shard 3/4 --jobs 4` | 278 caught, 2 pin controls | 0 | 1131 | kept: `selftest-shard3.log` |
| saved-state store | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | OK, 5 shapes, 435 tests | 0 | 88 | `ctrl_nvm.log` |
| saved-state store mutants | `... --require-rv32 --self-test --jobs 8` | all 109 planted defects reddened | 0 | 1390 | `ctrl_nvm-selftest.log` |
| coverage ratchet | `fw_coverage.py --selftest` then `--check --jobs 8` | `firmware coverage: PASS (35 files)` | 0 | 256 | `fw_coverage.log` |
| MAAP differential mutants | `python3 -B sw/firmware/ctrl/test/maap_differential.py --self-test` | 17/17 caught | 0 | 160 | `maap_differential-selftest.log.excerpt` (whole log 13.5 MB, sha256 in `WHOLE-LOGS.txt`) |
| TSN stack boundary, without Verilator | `ctrl_boundary.py --require-rv32 --selftest --without verilator` | `ctrl_boundary: PASS` | 0 | 1019 | `ctrl_boundary-without-verilator.log` |
| TSN stack boundary, Verilator | `ctrl_boundary.py --require-rv32 --selftest --only verilator` | `ctrl_boundary: PASS` | 0 | 694 | `ctrl_boundary-only-verilator.log` |
| end-station builder | `python3 sw/builder/test_builder.py --require-rv32` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, the calibration report of a local Arty build, as at the base) | 0 | 1452 | `builder_require_rv32.log` |
| docs, scope, idiom, harness self-test, CPU options, `git diff --check`, rtl-fast bdd-conformance | `scripts/gates_s3.py` (96 gates, one at a time) | 0 of 96 nonzero; behave 14 features, 406 scenarios, 1977 steps passed | 0 | | `docs/summary.md`, one log per gate |
| split boot, 1x1 | `python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <work>/boot-1x1` | `ctrl_split_boot: PASS (0 finding(s))` | 0 | 41 | `split_boot-1x1.log` |
| split boot, 8x8 | `... --build-dir <work>/boot-8x8 --shape endstation_ax7101_8x8` | `ctrl_split_boot: PASS (0 finding(s))` | 0 | 60 | `split_boot-8x8.log` |
| split boot plants | `... --build-dir <work>/boot-plants --self-test` | 2 of 2 plants caught | 0 | 366 | kept: `split_boot-selftest.log` |
| CPU budget harness, 1x1 | `tb/verilator/ctrl_service_budget/run.py --point 1x1 --record-budget-findings --jobs 4` | 18 groups graded, 0 refusals, 34 T_svc misses (13 of 81 paths, 34 of 141 instances), the counts of the README's split-cache row | 0 | 2020 | `s2_harness-1x1.log` |
| CPU budget harness at the base `f4c9ad4f`, 1x1 (comparison) | same command, `--jobs 16`, in a clone of the base | 18 groups, 0 refusals, 35 misses (14 of 81 paths, 35 of 141) | 0 | 1997 | `s2_harness-1x1-at-base-f4c9ad4f.log` |
| CPU budget harness at the base `f4c9ad4f`, 8x8 (comparison) | same command, `--jobs 16` | 17 groups, 0 refusals, 62 misses (30 of 129 paths, 62 of 182) | 0 | 2145 | `s2_harness-8x8-at-base-f4c9ad4f.log` |
| CPU budget harness, 8x8 | `... --point 8x8 --record-budget-findings --reuse-build --jobs 8` | 17 groups graded (the 8x8 point has no `fixture` group, as at the base), 0 refusals, 62 T_svc misses (30 of 129 paths, 62 of 182 instances); see the base comparison below | 0 | 2606 | `s2_harness-8x8.log` |
| linked images (measurement) | `images.sh`: `ctrl_plat_image.py` and `ctrl_srp_image.py --with-aecp --layout split` at four points, one runtime | platform 39.0 / 42.0 / 52.0, and **refused at 59** at 8x8 two interfaces (rc 2, the STOP), refused again with the fixture's override named (rc 2); fixture 37.0 / 40.5 / 50.5 / 57.5 (rc 0) | 0 / 2 | | `image-*.log`, `images-at-5edbba1d/` |

The 8x8 harness first ran at `--jobs 2` (each Vsim needs about 21 MB, so the cap was needlessly low); after 4 of 18
groups it was stopped and re-run on its own build with `--reuse-build --jobs 8` (the harness checks the reused build
is the same point and configuration). The two rc-2 image runs are the measured refusal this STOP is about, not a gate.

Not run: the full Verilator sweep (no RTL changed); Vivado (no route is owed by S3).

## Measurements at `5edbba1d`

Identical to [A697]'s at `f27d08e3`/`aa818a21` (the firmware has not changed since `f27d08e3`).

### Linked image against 56 tiles (one runtime for both: sha256 in `image-runtime.sha256`)

| Point | Platform rom / sram, B | Platform RAMB36 | Fixture rom / sram, B | Fixture RAMB36 | Delta rom / sram |
|---|---|---:|---|---:|---|
| 1x1, one interface (shipping) | 109,552 / 47,168 | 39.0 | 104,448 / 46,272 | 37.0 | +5,104 / +896 |
| 1x1, two interfaces | 111,192 / 58,592 | 42.0 | 106,032 / 57,648 | 40.5 | +5,160 / +944 |
| 8x8, one interface | 123,296 / 87,760 | 52.0 | 118,168 / 86,848 | 50.5 | +5,128 / +912 |
| 8x8, two interfaces | 125,040 / 113,936 | **59.0, refused** | 119,824 / 113,008 | 57.5 (ledgered) | +5,216 / +928 |

Five largest `.bss` objects (`ctrl_plat` counted by member; the refused point measured from the image it leaves, by
`ctrl_plat_image.largest_bss`, `scripts/bss5.py`):

| Point | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 1x1, one interface | `arena` (lwSRP pool) 9,920 | `ctrl_plat.app` 8,880 | `ctrl_plat.srp` 4,824 | `values` (descriptor image) 4,527 | `ctrl_plat.aecp` 3,352 |
| 1x1, two interfaces | `arena` 19,840 | `ctrl_plat.app` 10,064 | `ctrl_plat.srp` 5,032 | `values` 4,527 | `ctrl_plat.aecp` 3,352 |
| 8x8, one interface | `arena` 24,032 | `nvm_stage` 13,264 | `values` 11,753 | `ctrl_plat.app` 8,880 | `ctrl_plat.srp` 5,256 |
| 8x8, two interfaces | `arena` 48,064 | `nvm_stage` 13,264 | `values` 11,753 | `ctrl_plat.app` 10,064 | `ctrl_plat.srp` 5,896 |

### Boot to ready against the 20 s ADP valid time (Milan v1.2 5.6.2/5.6.3)

| Point | Ready, bus cycles (100 MHz) | CPU cycles (50 MHz) | ms | Banners |
|---|---:|---:|---:|---:|
| 1x1, one interface | 8,438,856 | 4,219,428 | 84.389 | 1 |
| 8x8, one interface | 18,460,988 | 9,230,494 | 184.610 | 1 |

### UART duties against #397's 500 ms tick rule and T_svc = 10 ms

| Point | Command | Bytes | Span ms | To first byte ms | Longest gap between bytes ms |
|---|---|---:|---:|---:|---:|
| 1x1 | `milan_status` | 305 | 21.632 | 1.963 | 1.273 |
| 1x1 | `milan_gettime` (worst of two) | 27 | 2.536 | 1.236 | 1.275 |
| 8x8 | `milan_status` | 305 | 40.209 | 2.853 | 2.204 |
| 8x8 | `milan_gettime` (worst of two) | 27 | 4.047 | 2.125 | 1.858 |

### The CPU budget harness against the base, both measured on this host today

The harness links the size fixture, so S3's only firmware change in its image is `ctrl_app.c`'s held open: `.text`
+24 B and `.bss` +8 B at both points (92,168 -> 92,192 and 93,944 -> 93,968 B of `.text`). Same harness, same
options, base `f4c9ad4f` and head `5edbba1d`:

| Point | Base: paths / instances missing T_svc | Head | Shared misses, head minus base | Misses that move |
|---|---|---|---|---|
| 1x1 | 14 of 81 / 35 of 141 | 13 of 81 / 34 of 141 | 34 shared, -13.22 to +0.05 ms | `acmp.get_tx_state.if0` misses at base (11.132 ms), fits at the head |
| 8x8 | 30 of 129 / 62 of 182 | 30 of 129 / 62 of 182 | 61 shared, -4.35 to +2.21 ms; worst 593.523 -> 593.729 ms | `acmp.unbind_rx.if0` 12.332 -> 1.350 ms (fits); `acmp.get_tx_state.if0` 1.170 -> 16.561 ms (misses) |

Each point is deterministic for its image (the head's 1x1 equals [A697]'s run at `f27d08e3` instance for instance).
The README's cache sweep row for the split cache (1x1 13 of 81 / 34 of 141; 8x8 34 of 129 / 66 of 182) matches the
head at 1x1 and neither run at 8x8. The misses are the harness's measurement (S2b's work); no group refused.
Receipts: `s2_harness-*-at-base-f4c9ad4f.log` and each run's `table.md` (`*-table.md.txt`).

## Decisions asked in the STOP

1. The largest point (59.0): (a) ledger the platform image at 59.0, owed to S14; (b) D3 (b); (c) keep the refusal.
   Recommended (a): S5 measures with S3's firmware at the largest point, which is the harness's `8x8` point (two
   interfaces).
2. The graders on a split image: `fabric-enabled` fails by design; the #396 campaign
   (`tb/tools/torture_campaign.py`) requires exactly one BIOS pass per cold cut, and the split has no BIOS.
   Recommended: accept both as listed differences; the graders' split mode is owed to S12.
3. SRP's live stream configuration: needs an `srp_mbx` entry (outside `plat/`, `app/`; S2b edits `srp_mbx.c`).
   Recommended: a later S3 round once S2b's `srp_mbx.c` is on `dev-soft-core`.
4. The plan's `scripts/run_litex_sims.sh` gate: not extended (CI change frozen until #784 step 2). Recommended:
   accept the `tb/` recipe until then.

## Other open risks / notes

- Not done here: ACMP's asking-failed source flag (false); GET_AS_PATH (unavailable); F1's LiteSPI addresses (S4);
  the product `--ctrl-mailbox` build stops at its AECP stage (the face acknowledgement is idle until S6).
- The UART grade uses the smoke grader's own `grade()` on the transcript, not its tty `Console` class.
- Shared files with S2b (`origin/665-s2b-cycles` at `bf1773c0`): `docs/ARCHITECTURE_HW_SW_SPLIT.md`,
  `SPLIT_CONTROL_MEMORY.md`, `sw/firmware/ctrl/README.md`, `srp/README.md`, `acmp_review_mutants.py`,
  `ctrl_configs.py`, `ctrl_mutants.py`, `test_ctrl_firmware.py`, `coverage.ratchet`, `gtest/README.md`. A trial
  `git merge-tree` of the two heads conflicts in several files, mostly because S2b branched before S1 merged (merge
  base `e0bb857a`); S2b's current round merges `dev-soft-core`.
- S2b's branch approves T_svc = 20 ms (`FR_NFR.md` 3.4.1); at this base it is 10 ms, which the UART grade uses.
- Host memory: during this session about 31 GB of tmpfs was held by other lanes' stale `/tmp/mbx-mutants-*` trees
  (10-26, 10-28) with swap full; both were removed later, not by this lane. This lane's own stale `/tmp` scratch
  from [A697] (636 MB) was deleted, and its units now build under the lane's scratch on disk (`TMPDIR`).
- Scratch left on disk for reproduction: `$VALIDATION_STORAGE/665s3-a697b` (2.9 GB: the clones at the head and the
  base, the simulation and harness builds, the images). Nothing of this lane's is left in tmpfs `/tmp`.

# [A697] #665 S3 — the target platform firmware: handoff

STATUS: IN PROGRESS — gates running at the head named in the gate table; final state at the end of this file.

- Lane: S3 of the Mark II split (#665), assignment [A10] issuecomment-6493622258, plan [A678] PLAN.md section S3.
- Worktree: the lane worktree `665-s3-platform`; branch `665-s3-platform`. The worktree was created on a local
  branch named `s3-platform`; it was renamed to the assignment's name before any commit.
- Base: `origin/dev-soft-core` `f4c9ad4f06f185378fd2646298aab51dd108e86f` (not dev). Origin verified as
  `https://github.com/kebag-logic/milan-fpga.git`. No submodule pin moved; no git command was run inside a submodule.
- TAKEN posted: issuecomment-6493758126.
- Nothing pushed. No PR created or edited. No issue or PR comment edited.
- No RTL changed (no `hdl/`, no `milan_datapath.sv`, no `milan_soc.py`, no `.github/`), so the full sweep was not run.
- `milan_baremetal.c` is read, never edited.

## Decisions read

- D6 (manager, 6409738976): the split console keeps only what the release graders read
  (`baremetal_uart_smoke.py` and the #396 plan).
- D2: split images before the flip keep VERSION `0x0002_0060`.
- D3 (owner): hybrid XIP in S14; the ledgered point 8x8-two-interfaces is planned at 57.5 RAMB36, owed to S14
  (6412739248, 6425357821).

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
`acmp_review_mutants.py`, `test_ctrl_firmware.py`, `ctrl_configs.py`, `ctrl_runs.py`, `gtest/README.md`,
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
| `console-blocks` (a spin of about 0.6 s before a command's response) | a `UART:` finding: the duty past #397's 500 ms tick rule |

## Gate table

(filled at the end)

## Measurements

All at the lane's head (firmware identical from `f27d08e3`), receipts under `receipts/`.

### Linked image against 56 tiles (`ctrl_plat_image.py`, the boot SoC's `csr.csv`; fixture `ctrl_srp_image.py --with-aecp --layout split`, same runtime, same head)

| Point | Platform rom / sram, B | Platform RAMB36 | Fixture rom / sram, B | Fixture RAMB36 | Delta rom / sram |
|---|---:|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 109,552 / 47,168 | 39.0 | 104,448 / 46,272 | 37.0 | +5,104 / +896 |
| 1x1, two interfaces | 111,192 / 58,592 | 42.0 | 106,032 / 57,648 | 40.5 | +5,160 / +944 |
| 8x8, one interface | 123,296 / 87,760 | 52.0 | 118,168 / 86,848 | 50.5 | +5,128 / +912 |
| 8x8, two interfaces | 125,040 / 113,936 | **59.0 (refused: over 56; the 57.5 override recognises the fixture only)** | 119,824 / 113,008 | 57.5 (ledgered) | +5,216 / +928 |

The five largest .bss consumers (with `ctrl_plat` counted by member):

| Point | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 1x1, one interface | `arena` (lwSRP pool) 9,920 | `ctrl_plat.app` 8,880 | `ctrl_plat.srp` 4,824 | `values` (descriptor image) 4,527 | `ctrl_plat.aecp` 3,352 |
| 1x1, two interfaces | `arena` 19,840 | `ctrl_plat.app` 10,064 | `ctrl_plat.srp` 5,032 | `values` 4,527 | `ctrl_plat.aecp` 3,352 |
| 8x8, one interface | `arena` 24,032 | `nvm_stage` 13,264 | `values` 11,753 | `ctrl_plat.app` 8,880 | `ctrl_plat.srp` 5,256 |

The console's state is 588 B of `sram` (`ctrl_plat.console`).
The held open (`ctrl_app_open_held`) adds 24 B of rom and 16 B of sram to the fixture too; at the shipping point the
fixture's rom then fills its last granule exactly (104,448 = 51 x 2,048), still 37.0.

### Boot to ready against the 20 s ADP valid time (Milan v1.2 5.6.2/5.6.3), boot simulation

| Point | Ready, bus cycles (100 MHz) | CPU cycles (50 MHz) | ms |
|---|---:|---:|---:|
| 1x1, one interface | 8,438,856 | 4,219,428 | 84.389 |
| 8x8, one interface | 18,460,988 | 9,230,494 | 184.610 |

Blank flash (BLANK terminal); each face commit acknowledged at the contract's bound.

### UART duties against #397's 500 ms tick rule and T_svc = 10 ms

| Point | Command | Bytes | Span ms | To first byte ms | Longest gap between bytes ms |
|---|---|---:|---:|---:|---:|
| 1x1 | `milan_status` | 305 | 21.632 | 1.963 | 1.273 |
| 1x1 | `milan_gettime` (worst) | 27 | 2.536 | 1.236 | 1.275 |
| 8x8 | `milan_status` | 305 | 40.209 | 2.853 | 2.204 |
| 8x8 | `milan_gettime` (worst) | 27 | 4.047 | 2.125 | 1.858 |

The console's per-pass share is bounded by construction: at most 104 bus accesses (48 receive, 24 for a status
command, 32 transmit) and one response's formatting; K4 and the planted defects prove the slices.

## Open risks / questions

1. **Decision: the 8x8 image with two interfaces plans 59.0 RAMB36.** Over the 56 budget, and its ledger's 57.5
   override recognises the fixture's image only. Options: the plan's D3 (b) (gate the flip on one-interface shapes,
   report two-interface links), or S14's cold code in flash (the boot code is cold). The other three points fit.
2. **Decision: the graders on a split image.** `baremetal_uart_smoke.py`'s `fabric-enabled` fails on any split image
   (the split never sets `ADP_CTRL[0]`/`PP_CTRL[0]`); the #396 plan counts BIOS passes, and the split's one banner is
   the firmware's (`Milan split control firmware: boot`).
3. **Decision: SRP's live stream configuration.** Needs an entry in `srp/srp_mbx.c` (re-declare a source MAAP has
   allocated); outside S3's files, and S2b edits that file. Until then the sources declare Talker Failed.
4. **Not done here:** ACMP's asking-failed source flag (false); GET_AS_PATH (unavailable); F1's LiteSPI addresses
   (S4); the product `--ctrl-mailbox` build stops at its AECP stage (the face acknowledgement is idle until S6).
5. **The plan's `scripts/run_litex_sims.sh` gaining a split boot** was not done: the hosted aggregate treats a
   skipped member as a failure (exit 90), and the split boot needs the RV32 SDK and the runtime archives in that job,
   a CI change frozen until #784 step 2. The simulation is a recipe under `tb/` the plan also names.
6. The UART grade uses the smoke grader's own `grade()` on the transcript, not its tty `Console` class.

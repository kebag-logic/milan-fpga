[A697]

## Contents

- **[Status](#status)** — REVIEW READY: the split placement's target platform boots to ready in simulation, with its CSR writes equal to `milan_baremetal`'s and the graders' commands answered. `665-s3-platform` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions needed.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GATES_LINE

- **The boot.** `ctrl_split_start.S` now calls a real `main` (`sw/firmware/ctrl/plat/`). It runs steps 2 to 9 of the architecture's boot sequence in the order Milan v1.2 5.6.1 sets: the CSR window's identity, the generated identity and static policy, MAAP's one-owner report, the AEM image's CRC, the composition of F0-F5 and F1, the saved state, the mailbox with ADP held, SRP, AECP's release at an accepted terminal, and ADP last.
- **The CSR initialisation** writes exactly what `milan_baremetal.c`'s `configure_fabric()` writes for the same shape: fifteen writes in its order, from the same derivation (`boot_policy.fabric_constants`). It is checked for every shipped config against `milan_baremetal.c` itself, compiled on the host as builder gate 35 compiles it, and on the split CPU in simulation. A skipped, reordered or wrong write is caught.
- **The console** (decision D6) answers `milan_status` and `milan_gettime` in `milan_baremetal.c`'s lines. It is a loop poll bounded per pass: 16 bytes in, 16 out, one command, never into a full FIFO.
- **The ports.** MAAP's `maap_csr_allocation` runs on the CSR window. ACMP's talker sources report their stream and the MAAP address. SRP's sources take the generated streams, and its licences are recorded. The AECP ports are S1's.
- **Simulation** (`tb/verilator/ctrl_split_boot`): the CPU budget harness's split SoC with the CSR window and UART on testbench pads. Ready at 84.392 ms (1x1) and 184.708 ms (8x8, one interface), against the 20 s ADP valid time. The CSR trace equals `configure_fabric()`'s. The smoke grader's own parse reads every answer.
- **Linked size:** 39.0 / 42.0 / 52.0 / **59.0** RAMB36 at the four points (the fixture: 37.0 / 40.5 / 50.5 / 57.5). The 8x8 image with two interfaces is over 56 and over its 57.5 ledger: **a decision is needed** ([Known limitations](#known-limitations--out-of-scope)).

## Linked Issue / roles

Relates to #665

Executor: `[A697]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

| Commit | Piece | What and why |
|---|---|---|
| `74eddc47`, `8e55b1ae` | `sw/firmware/ctrl/app/ctrl_app.{c,h}` | `ctrl_app_open_held` opens the mailbox with ADP held, and `ctrl_app_release_adp` starts it: boot step 9 (Milan v1.2 5.6.1). `ctrl_app_open`'s text keeps every line but one, ADP's enable now reading `!app->adp_held`. A configuration field was tried first and broke every positional `ctrl_app_config` in the tests; `8e55b1ae` replaced it. |
| `a7690ddb` | `sw/firmware/ctrl/plat/` | `ctrl_plat.c`: the boot (steps 2 to 9), the composition of F0-F5 and F1, MAAP's allocation port on the CSR window, the ACMP talker sources, SRP's sources and licences, and the console-only state of a refused stage. `ctrl_plat_csr.c`: identity, `configure_fabric()`'s fifteen writes, the status reads and the bounded time-of-day read. `ctrl_plat_console.c`: D6's two commands, bounded per pass. `ctrl_plat_mmio.c` and `ctrl_plat_io.h`: the bus port. `ctrl_plat_main.c`: `main`. `ctrl_plat_gen.py`: the policy header and the bus map, generated. |
| `ac7f46d8` | `sw/firmware/ctrl/test/`, `sw/firmware/gtest/README.md` | The arms `plat`, `platboot` (one and two interfaces), `platrv32` and `plattrace` (`plat_arms.py`). Their tests: `test_plat.cpp`, `test_plat_mmio.cpp`, `test_plat_boot.cpp`, `plat_bus.{hpp,cpp}`; `plat_trace.py`, the differential against `milan_baremetal.c`; and 37 defects in the control campaign (`plat_mutants.py`). `ctrl_plat_image.py` links the image. Three coverage exclusion rows cover the module refusals no input reaches. |
| `6380c8cd`, `068df85a`, `5edbba1d` | `tb/verilator/ctrl_split_boot/` | The boot simulation: the CPU budget harness's split SoC (imported read only), with the CSR window and UART on testbench pads; its grade (BOOT, TRACE, UART, the smoke grader's checks); `--self-test` with two plants. |
| `f4a839eb` | `ctrl_configs.py`, `ctrl_runs.py`, `ctrl_plat_csr.csv`, `plat_trace.py` | The TSN stack boundary gate: the image builder is a known builder, run on the fixture map at both shapes and interface counts; the other new builders are classified. A build-only run does not run the trace arm's programs. |
| `65ffbc85`, `a497091f` | the new Python and C++ | The idiom gates and `git diff --check`. |
| `c787a3ce` | `sw/firmware/gtest/coverage.ratchet` | The five platform files at 100 %, through `fw_coverage.py --write`. |
| `f27d08e3` | `test_ctrl_firmware_shards.py` | The shard dispatch proof stands the platform arms in, as it does the other arm modules', so a sharded run builds nothing into its working directory. |
| `f2825ec2`, `754099ea`, `aa818a21` | docs | `sw/firmware/ctrl/plat/README.md`, `tb/verilator/ctrl_split_boot/README.md`; the architecture's section 5; `SPLIT_CONTROL_MEMORY.md` sections 4 and 5 (the console, the linked size beside the fixture); the control firmware's layout, linked size and arm table; MAAP's and SRP's integration notes. |

Shared files, for the parallel lanes: `ctrl_app.{c,h}`, `ctrl_mutants.py`, `acmp_review_mutants.py` (the `APP_OPEN` anchor's one ADP line), `test_ctrl_firmware.py`, `test_ctrl_firmware_shards.py`, `ctrl_configs.py`, `ctrl_runs.py`, `gtest/README.md`, `coverage.ratchet` and `SPLIT_CONTROL_MEMORY.md`. Each edit is additive but the one line of `ctrl_app_open` and its anchor.

`milan_baremetal.c` is read and never edited. No RTL, `milan_soc.py`, `.github/` or CI generator changed.

## Authoritative references

- #665 lane S3: the assignment (issuecomment-6493622258) and the plan's section S3; decisions D2, D3 and D6 (issuecomment-6409738976).
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1 (one owner per function) and section 2 (the boot sequence); Milan v1.2 5.6.1 (readiness order), 5.6.2/5.6.3 (the ADP valid time), 5.5.4.1 (a talker's destination).
- `REQUIREMENTS.md:22-23` (firmware boot policy, CSR initialisation, identity and UART diagnostics).
- `docs/design/SPLIT_CONTROL_MEMORY.md` sections 4 and 5; `sw/firmware/ctrl/maap/README.md` "Integration"; `sw/firmware/ctrl/srp/README.md` "Integration still owed".
- `sw/litex/boot_policy.py` and builder gate 35 (`sw/builder/test_builder.py`); `scripts/baremetal_uart_smoke.py`; #397's tick rule (`docs/findings/397_SERVICE_BUDGET.md`).
- IEEE 1722.1-2021 7.2.3 (a STREAM_OUTPUT's stream_id).

## How to get into the same state

```sh
git fetch origin
git checkout HEAD_SHA
git submodule update --init external protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The firmware gates need host C/C++ compilers, GoogleTest, GoogleMock, PyYAML and the pinned RV32 SDK (`scripts/ci_rv32_sdk.py`).
The simulation needs the CPU budget harness's prerequisites (`tb/verilator/ctrl_service_budget/README.md`, "Run and reproduce"): the product LiteX tree, the RV32 SDK, Verilator, and the offline CPU generator (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`).

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/builder/test_builder.py --require-rv32
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $BUILD/split-boot-1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $BUILD/split-boot-8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $BUILD/split-boot-plants --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir $BUILD/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $BUILD/budget-8x8 --record-budget-findings
(cd tests && behave)
```

Expected result / pass criteria:

- the firmware gate ends `test_ctrl_firmware: PASS`, with `[ok] arm plat`, `platboot` (twice), `platrv32` and `plattrace`, and the control campaign catching every defect (the 37 platform defects among them);
- coverage ends `firmware coverage: PASS`, the five platform files at 100 % of lines and branches after the three named exclusions;
- the boundary gate ends `ctrl_boundary: PASS`; the builder gate passes as at the base;
- each simulation point ends `ctrl_split_boot: PASS (0 finding(s))`, and the self-test `2 of 2 plants caught`;
- the CPU budget harness runs with `0 refusals` at both points (its misses are its measurement).

## Known limitations / out of scope

- **Decision needed: the 8x8 image with two interfaces plans 59.0 RAMB36.** The platform adds 5,064 to 5,184 B of `rom` and 912 to 944 B of `sram` at each point. That point was ledgered at 57.5 for the size fixture, and the ledger's override recognises the fixture's image by its symbols, so it refuses this one. Options: the plan's D3 (b), gating the flip on one-interface shapes and reporting two-interface links; or S14's move of cold code, the boot among it, to flash. The three other points are within 56 (39.0 / 42.0 / 52.0).
- **Decision needed: the graders on a split image.** The smoke grader's `fabric-enabled` check needs `ADP_CTRL[0]` and `PP_CTRL[0]`, which the split never sets, because the core owns ADP and AECP. So a split image fails that check on any board. The #396 plan counts BIOS passes; the split has no BIOS, and its one banner is the firmware's (`Milan split control firmware: boot`). Both need the graders' ruling for split images (D6 kept the commands; it did not rule these two readings).
- **SRP's live stream configuration** is not done. `srp_mbx.c` copies its sources at init, and nothing re-declares a source whose destination MAAP has since allocated. So the sources stay unallocated (Talker Failed) until an SRP adapter entry takes the allocation. That entry is in `srp/`, outside this lane's files, and S2b edits `srp_mbx.c`. It needs a ruling on where it lands.
- ACMP's asking-failed source flag reads false: the SRP adapter exposes no per-source Listener Asking Failed registration. GET_AS_PATH answers unavailable.
- F1's flash port keeps its fixture addresses: lane S4 generates them from the SoC's `csr.csv`.
- At this base the product `--ctrl-mailbox` build holds the face acknowledgement idle, so AECP does not open on it, and the boot stops at its AECP stage there. The simulation uses the CPU budget harness's SoC, which acknowledges at the contract's bound. S6 connects the faces.
- The CPU generator's region decode of #791 is covered in simulation as the CPU budget harness covers it.
- The plan's `scripts/run_litex_sims.sh` does not gain the split boot: its hosted step fails on a skipped member, and the split boot needs the RV32 SDK and the runtime archives there, a CI change frozen until #784 step 2. The simulation is a recipe under `tb/`, run locally.
- The UART grade uses the smoke grader's own parse and `grade()` on the simulated transcript, not its tty console.
- No RTL changed; the full sweep was not run.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

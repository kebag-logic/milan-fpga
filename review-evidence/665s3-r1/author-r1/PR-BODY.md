[A697b]

## Contents

- **[Status](#status)** — BLOCKED (STOP, decisions needed): the split placement's target platform boots to ready in simulation, with its CSR writes equal to `milan_baremetal`'s and the graders' commands answered; the 8x8 two-interface image plans 59.0 RAMB36. `665-s3-platform` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions needed.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED (STOP) at `5edbba1d`: four decisions are needed ([Known limitations](#known-limitations--out-of-scope)). Every gate the change touches passes at that head, rc 0: the firmware self-test's four shards (control campaign 565 of 565, AECP 137, SRP 278 and 2 pin controls), the saved-state store and its 109 planted defects, coverage (35 files), the MAAP differential's 17 mutants, both TSN stack boundary legs, the builder bank (one NOT RUN, as at the base), 96 docs, scope and idiom gates with `behave` (406 scenarios), the split boot at both points and its 2 plants, and the CPU budget harness at both points (0 refusals).

- **The boot.** `ctrl_split_start.S` now calls a real `main` (`sw/firmware/ctrl/plat/`). It runs steps 2 to 9 of the architecture's boot sequence in the order Milan v1.2 5.6.1 sets: the CSR window's identity, the generated identity and static policy, MAAP's one-owner report, the AEM image's CRC, the composition of F0-F5 and F1, the saved state, the mailbox with ADP held, SRP, AECP's release at an accepted terminal, and ADP last.
- **The CSR initialisation** writes exactly what `milan_baremetal.c`'s `configure_fabric()` writes for the same shape: fifteen writes in its order, from the same derivation (`boot_policy.fabric_constants`). It is checked for every shipped config against `milan_baremetal.c` itself, compiled on the host as builder gate 35 compiles it, and on the split CPU in simulation. A skipped, reordered or wrong write is caught.
- **The console** (decision D6) answers `milan_status` and `milan_gettime` in `milan_baremetal.c`'s lines. It is a loop poll bounded per pass: 16 bytes in, 16 out, one command, never into a full FIFO.
- **The ports.** MAAP's `maap_csr_allocation` runs on the CSR window. ACMP's talker sources report their stream and the MAAP address. SRP's sources take the generated streams, and its licences are recorded. The AECP ports are S1's.
- **Simulation** (`tb/verilator/ctrl_split_boot`): the CPU budget harness's split SoC with the CSR window and UART on testbench pads. Ready at 84.389 ms (1x1) and 184.610 ms (8x8, one interface), against the 20 s ADP valid time. The CSR trace equals `configure_fabric()`'s. The smoke grader's own parse reads every answer.
- **Linked size:** 39.0 / 42.0 / 52.0 / **59.0** RAMB36 at the four points (the fixture at the same head: 37.0 / 40.5 / 50.5 / 57.5). The 8x8 image with two interfaces is over 56 and over its 57.5 ledger, which is the STOP.

## Linked Issue / roles

Relates to #665

Executor: `[A697]`, continued by `[A697b]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

| Commit | Piece | What and why |
|---|---|---|
| `74eddc47`, `8e55b1ae` | `sw/firmware/ctrl/app/ctrl_app.{c,h}` | `ctrl_app_open_held` opens the mailbox with ADP held, and `ctrl_app_release_adp` starts it: boot step 9 (Milan v1.2 5.6.1). `ctrl_app_open`'s text keeps every line but one, ADP's enable now reading `!app->adp_held`. A configuration field was tried first and broke every positional `ctrl_app_config` in the tests; `8e55b1ae` replaced it. |
| `a7690ddb` | `sw/firmware/ctrl/plat/` | `ctrl_plat.c`: the boot (steps 2 to 9), the composition of F0-F5 and F1, MAAP's allocation port on the CSR window, the ACMP talker sources, SRP's sources and licences, and the console-only state of a refused stage. `ctrl_plat_csr.c`: identity, `configure_fabric()`'s fifteen writes, the status reads and the bounded time-of-day read. `ctrl_plat_console.c`: D6's two commands, bounded per pass. `ctrl_plat_mmio.c` and `ctrl_plat_io.h`: the bus port. `ctrl_plat_main.c`: `main`. `ctrl_plat_gen.py`: the policy header and the bus map, generated. |
| `ac7f46d8` | `sw/firmware/ctrl/test/`, `sw/firmware/gtest/README.md` | The arms `plat`, `platboot` (one and two interfaces), `platrv32` and `plattrace` (`plat_arms.py`). Their tests: `test_plat.cpp`, `test_plat_mmio.cpp`, `test_plat_boot.cpp`, `plat_bus.{hpp,cpp}`; `plat_trace.py`, the differential against `milan_baremetal.c`; and 37 defects in the control campaign (`plat_mutants.py`). `ctrl_plat_image.py` links the image. Three coverage exclusion rows cover the module refusals no input reaches. |
| `6380c8cd`, `068df85a`, `5edbba1d` | `tb/verilator/ctrl_split_boot/` | The boot simulation: the CPU budget harness's split SoC (imported read only), with the CSR window and UART on testbench pads; its grade (BOOT, TRACE, UART, the smoke grader's checks); `--self-test` with two plants, a skipped CSR write and a console that spins about 0.7 s before its response. |
| `f4a839eb` | `ctrl_configs.py`, `ctrl_runs.py`, `ctrl_plat_csr.csv`, `plat_trace.py` | The TSN stack boundary gate: the image builder is a known builder, run on the fixture map at both shapes and interface counts; the other new builders are classified. A build-only run does not run the trace arm's programs. |
| `65ffbc85`, `a497091f` | the new Python and C++ | The idiom gates and `git diff --check`. |
| `c787a3ce` | `sw/firmware/gtest/coverage.ratchet` | The five platform files at 100 %, through `fw_coverage.py --write`. |
| `f27d08e3` | `test_ctrl_firmware_shards.py` | The shard dispatch proof stands the platform arms in, as it does the other arm modules', so a sharded run builds nothing into its working directory. |
| `f2825ec2`, `754099ea`, `aa818a21` | docs | `sw/firmware/ctrl/plat/README.md`, `tb/verilator/ctrl_split_boot/README.md`; the architecture's section 5; `SPLIT_CONTROL_MEMORY.md` sections 4 and 5 (the console, the linked size beside the fixture); the control firmware's layout, linked size and arm table; MAAP's and SRP's integration notes. |

Shared files, for the parallel lanes: `ctrl_app.{c,h}`, `ctrl_mutants.py`, `acmp_review_mutants.py` (the `APP_OPEN` anchor's one ADP line), `test_ctrl_firmware.py`, `test_ctrl_firmware_shards.py`, `ctrl_configs.py`, `ctrl_runs.py`, `gtest/README.md`, `coverage.ratchet` and `SPLIT_CONTROL_MEMORY.md`. Each edit is additive but the one line of `ctrl_app_open` and its anchor.

`milan_baremetal.c` is read and never edited. No RTL, `milan_soc.py`, `.github/` or CI generator changed, so the full sweep was not run.

## Authoritative references

- #665 lane S3: the assignment (issuecomment-6493622258) and the plan's section S3; decisions D2, D3 and D6 (issuecomment-6409738976); the ledger rulings 6412739248 and 6425357821.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1 (one owner per function) and section 2 (the boot sequence); Milan v1.2 5.6.1 (readiness order), 5.6.2/5.6.3 (the ADP valid time), 5.5.4.1 (a talker's destination).
- `REQUIREMENTS.md:22-23` (firmware boot policy, CSR initialisation, identity and UART diagnostics).
- `docs/design/SPLIT_CONTROL_MEMORY.md` sections 4 and 5; `sw/firmware/ctrl/maap/README.md` "Integration"; `sw/firmware/ctrl/srp/README.md` "Integration still owed".
- `sw/litex/boot_policy.py` and builder gate 35 (`sw/builder/test_builder.py`); `scripts/baremetal_uart_smoke.py`; #397's tick rule (`docs/findings/397_SERVICE_BUDGET.md`).
- IEEE 1722.1-2021 7.2.3 (a STREAM_OUTPUT's stream_id).

## How to get into the same state

```sh
git fetch origin
git checkout 5edbba1d333dbebfaca4bfc4ab85debdac1c7e55
git submodule update --init external protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The firmware gates need host C/C++ compilers, GoogleTest, GoogleMock, PyYAML and the pinned RV32 SDK (`scripts/ci_rv32_sdk.py`).
The simulation needs the CPU budget harness's prerequisites (`tb/verilator/ctrl_service_budget/README.md`, "Run and reproduce"): the product LiteX tree, the RV32 SDK, Verilator, and the offline CPU generator (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`).

## How to validate

```sh
python3 sw/firmware/gtest/tally_selftest.py
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check
python3 -B sw/firmware/ctrl/test/maap_differential.py --self-test
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 sw/builder/test_builder.py --require-rv32
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$BUILD/split-boot-1x1"
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$BUILD/split-boot-8x8" --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$BUILD/split-boot-plants" --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$BUILD/budget-1x1" --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir "$BUILD/budget-8x8" --record-budget-findings
(cd tests && behave)
```

The linked size, at each point, with the simulation's runtime (`$BUILD/split-boot-1x1/runtime`) and the boot SoC's map for the shape (`$BUILD/split-boot-<shape>/soc/csr.csv`):

```sh
python3 sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_8x8.yaml --interfaces 2 \
  --csr-csv "$BUILD/split-boot-8x8/soc/csr.csv" --output "$OUT/plat-8x8-2" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml --interfaces 2 \
  --with-aecp --layout split --ledgered-point 8x8-two-interfaces --output "$OUT/fix-8x8-2" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
```

Expected result / pass criteria:

- each firmware shard ends `test_ctrl_firmware: PASS`, with `[ok] arm plat`, `platboot` (twice), `platrv32` and `plattrace`, and the control campaign catching every defect (the 37 platform defects among them); the saved-state store gate ends with all 109 planted defects reddened;
- coverage ends `firmware coverage: PASS (35 files)`, the five platform files at 100 % of lines and branches after the three named exclusions;
- the MAAP differential's mutants are all caught; both boundary legs end `ctrl_boundary: PASS`; the builder gate passes as at the base, with its one NOT RUN (the calibration gate needs a local Arty build report);
- each simulation point ends `ctrl_split_boot: PASS (0 finding(s))`, and the self-test `2 of 2 plants caught`;
- the CPU budget harness runs at both points (its misses are its measurement);
- the platform image links and plans at three points; at 8x8 with two interfaces it is refused (exit 2) at 59 RAMB36, and refused again if the fixture's override is named.

## Known limitations / out of scope

- **Decision needed: the 8x8 image with two interfaces plans 59.0 RAMB36** (rom 125,040 B in 126,976; sram 113,936 B in 114,688). Ruling 6425357821 says to stop if that point goes over 57.5. The platform adds 5,104 to 5,216 B of `rom` and 896 to 944 B of `sram` to the fixture at each point. The ledger's override recognises the fixture's image by its symbols, so it refuses this one. It cannot reach 57.5 within the platform's files: the fixture's own `sram` already needs 28.0 tiles, so `rom` would have to drop to 120,832 B, a cut of 4,208 B from the platform's 5,216. The other three points are within 56 (39.0 / 42.0 / 52.0). Options: (a) ledger the platform image at that point at 59.0, owed to S14 under D3 (the boot and the CSR policy are cold code, which D3 moves to flash); recommended, because S5 measures with S3's firmware at the largest point, the CPU budget harness's two-interface `8x8`; (b) D3 (b): gate the flip on one-interface shapes and report two-interface links; (c) keep the refusal, so that point waits for S14.
- **Decision needed: the graders on a split image.** The smoke grader's `fabric-enabled` check needs `ADP_CTRL[0]` and `PP_CTRL[0]`, which the split never sets, because the core owns ADP and AECP. So a split image fails that check on any board. The #396 campaign (`tb/tools/torture_campaign.py`) requires exactly one BIOS pass per cold cut; the split has no BIOS, and its one banner is the firmware's (`Milan split control firmware: boot`). Both need the graders' ruling for split images (D6 kept the commands; it did not rule these two readings).
- **Decision needed: SRP's live stream configuration** is not done. `srp_mbx.c` copies its sources at init, and nothing re-declares a source whose destination MAAP has since allocated. So the sources stay unallocated (Talker Failed) until an SRP adapter entry takes the allocation. That entry belongs in `srp/`, outside this lane's files (`plat/`, `app/`), and S2b edits `srp_mbx.c`. It needs a ruling on where it lands.
- **Decision needed: the plan's `scripts/run_litex_sims.sh` gate.** It does not gain the split boot: its hosted step fails on a skipped member, and the split boot needs the RV32 SDK and the runtime archives there, a CI change frozen until #784 step 2. The simulation is a recipe under `tb/`, run locally.
- **The CPU budget harness moves with the held open.** The harness links the size fixture, so S3's only firmware change in its image is `ctrl_app.c`'s held open: 24 B of `.text` and 8 B of `.bss`. Measured against the base on one host: at 1x1 the shared misses move by -13.22 to +0.05 ms, and `GET_TX_STATE.if0` fits (11.132 ms at the base), leaving 13 of 81 paths missing T_svc where the base misses 14. At 8x8 the count is unchanged (30 of 129). The instances move by -4.35 to +2.21 ms, and one miss changes place, `UNBIND_RX.if0` to `GET_TX_STATE.if0`. No group refused. The misses are the harness's measurement, which S2b answers.
- ACMP's asking-failed source flag reads false: the SRP adapter exposes no per-source Listener Asking Failed registration. GET_AS_PATH answers unavailable.
- F1's flash port keeps its fixture addresses: lane S4 generates them from the SoC's `csr.csv`.
- At this base the product `--ctrl-mailbox` build holds the face acknowledgement idle, so AECP does not open on it, and the boot stops at its AECP stage there. The simulation uses the CPU budget harness's SoC, which acknowledges at the contract's bound. S6 connects the faces.
- The CPU generator's region decode of #791 is covered in simulation as the CPU budget harness covers it.
- The UART grade uses the smoke grader's own parse and `grade()` on the simulated transcript, not its tty console.

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

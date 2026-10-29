[A698]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**BLOCKED on a decision: on the split CPU, the saved-state store's capture misses its 24.5 ms bound at both points. Everything else in the scope passes at both points.**

| Point | Capture, CPU cycles | ms | Bound |
|---|---:|---:|---|
| 1x1 | 1,361,143 | 27.22 | over by 11 % |
| 8x8 | 5,161,328 | 103.23 | over, 4.2 times |

- Every record of the shape is dirty, and each record is latched from its real owner.
- The cost decomposes into a fixed cost per step plus a cost per payload byte: 11,062 + 263.7 per byte at 1x1, and 16,500 + 205.5 per byte at 8x8.
- At 8x8 the bytes alone cost 48.9 ms.
- Every step of the commit is within T_svc = 10 ms. The longest at 8x8 is 2.64 ms.
- The decision's options are in the STOP comment on #665: (a) rule the hold-derived bound off for F1, which holds no owner; (b) a lane that makes F1 capture several records per step; (c) keep the bound for the shipping writer only. The recommendation is (a).
- Passing at both points:
  - the boot with valid, absent, torn and wrong-version slots;
  - D3's apply order on the real owners;
  - the flash region guard;
  - the commit and its read-back.
- Every planted control is caught.
- Gates at the head: every gate rc 0. At `9c2f12a8`, 99 gates: the docs workflow's, both firmware-boundary modes, the generator, target and harness self-tests, the idiom and evidence gates, and behave (406 scenarios). At `19d79844`, the nine long gates the last commit does not touch: the builder bank (one registered NOT RUN), the store gate (435 tests, 109 of 109 defects), the firmware campaigns (1,006 plants caught, none escaped), coverage at 100 % and its self-test, `nvm_cosim` (465 checks, 39 of 39 mutants) and its lint, the census, and the split control memory test. Also: the S2 harness at 1x1 (18 groups, 0 refusals) and at 8x8 (17 groups, 0 refusals); `nvm_capture_cpu` at 8x8 and 50 MHz, at most 13.863 ms with traffic and 13.690 ms without, with both negative controls caught.

`665-s4-f1-target` -> `dev-soft-core`, head `9c2f12a80494b9ee95441ca7f9c606ee6cfe617f`: five commits on `dev-soft-core` `f4c9ad4f`.

## Linked Issue / roles

Relates to #665

Executor: `[A698]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

The S4 lane of the Mark II split ([A10] issuecomment-6493622258): F1's flash and saved-state ports on the target.

| Piece | What changed |
|---|---|
| `sw/firmware/ctrl_nvm/plat/gen_flash_port.py` (new) | It generates the flash port's `generated/csr.h` and `generated/mem.h` from a split SoC export, so the port never compiles against a hand-written address. The addresses come from `csr.csv`; the field offsets come from the same export's LiteX `csr.h`, which `csr.csv` does not carry; every shared address is compared between the two. Eight named rules refuse an export: data width, registers, header, fields, flash window, journal, slots and clock. The journal must be `milan_soc.py`'s `FLASHBOOT_RESERVED` journal, which the store is built with. It must be two one-erase-block slots (the A/B geometry `check_nvm_record_space.py` check 5 sizes containers against), aligned, inside the device, and clear of the bitstream, the AEM, the user slot and every image the SoC publishes. |
| `sw/firmware/ctrl/test/ctrl_srp_image.py` | `--flash-map DIR` puts the generated headers ahead of the RV32 stand-ins, and refuses a map whose clock is not the shape's. `--nvm-source DIR` takes a planted copy of the store. Both default to today's behaviour. |
| `tb/verilator/ctrl_service_budget/` | `build.flash_map` exports the split SoC with the point's one-interface image, generates the map, then exports it again with the image linked against the map, and refuses two different maps. The image is linked against the map. `split_soc` places the flash and `timer0` from the map, with LiteSPI's bank laid out as `add_spi_flash` builds it. `map_deviations` refuses a test-SoC `csr.csv` that places any port register, or the window, elsewhere. The testbench gains passive SPAN lines (a traced function's entry to its return) and CALL lines (the owners' and the port's entries), and a journal preload and dump. `build.Plant` and `build.Variant` let a client pass its own planted defect or arm. The self-test refuses reuse after a changed flash map. |
| `tb/verilator/nvm_split_target/` (new) | The store's cases on the split CPU, graded from the SPAN and CALL lines: the commit, its capture and phases, and the boots with valid, absent, torn and wrong-version journals and their AECP and ACMP answers. It also grades D3's apply order, the guard probe, three planted defects and the capture bound's control. A portable self-test has 29 checks and 7 grader mutants. |
| `sw/firmware/ctrl/test/ctrl_configs.py` | The boundary gate's OUTSIDE list gains the two new files that name the firmware tree. The reasons for the harness's `build.py` and `split_soc.py` are updated. |
| Docs | `ctrl_nvm/README.md` (the generated map, the owners and the measured CPU time), both harness READMEs, and `ARCHITECTURE_HW_SW_SPLIT.md` section 5. |

No firmware function changes, so the unit-test rule adds no units. The store, the port and the owners are unchanged, and `fw_coverage.py --check` holds the ratchet.

Measured, beside the capture:

- The image plans equal the ledger (`SPLIT_CONTROL_MEMORY.md` section 5): 37.0 tiles at 1x1 and 57.5 at 8x8 with two interfaces. `nvm_stage` is 3,344 B and 13,264 B. The generated map moves no planned byte.
- `nvm_store_boot`'s CPU time on the split CPU: 100.5 ms valid, 165.1 torn, and 10.1 absent or wrong-version at 1x1; 488.5, 745.1 and 34.9 ms at 8x8. The boot runs before the loop, and its time to ready is the target platform firmware's measurement.

## Authoritative references

- #665 [A10] issuecomment-6493622258, S4; the plan's section S4.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 2: the boot sequence, steps 6 to 8; bindings, then formats, maps, the settle step and names (Milan v1.2 5.6.1).
- `sw/firmware/ctrl_nvm/README.md`: "The flash port", "Boot" items 5 to 9, "Write-back" and "The service bound".
- `tb/verilator/nvm_capture_cpu/README.md`: the 24.5 ms bound, half the hold's 49 ms floor; `scripts/check_nvm_capture.py`.
- `sw/litex/milan_soc.py` `FLASHBOOT_LAYOUT` and `FLASHBOOT_RESERVED`; `scripts/check_nvm_record_space.py` check 5.
- `docs/reference/FR_NFR.md` 3.4.1 (T_svc = 10 ms).
- IEEE 1722.1-2021 7.2.1, 7.4.5 and 8.2.1, and Milan v1.2 5.5.3.5, for the two questions the cases ask.

## How to get into the same state

```sh
git fetch origin
git checkout 9c2f12a80494b9ee95441ca7f9c606ee6cfe617f
git submodule update --init --recursive
# the product LiteX tree with its patches, the pinned RV32 SDK and Verilator, as
# tb/verilator/nvm_capture_cpu/README.md "Run" describes; then
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
```

## How to validate

```sh
python3 sw/firmware/ctrl_nvm/plat/gen_flash_port.py --self-test
python3 -B tb/verilator/nvm_split_target/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/nvm_split_target/run.py --point 1x1 --build-dir /tmp/nvm-target-1x1 --record-budget-findings
python3 -B tb/verilator/nvm_split_target/run.py --point 8x8 --build-dir /tmp/nvm-target-8x8 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/builder/test_builder.py --require-rv32
make -C tb/verilator/nvm_cosim
(cd tests && behave)
```

Expected result / pass criteria:

- The three self-tests exit 0.
- Each `nvm_split_target` point exits 1, on the commit case's capture bound alone:
  - `CASE commit FAIL: the capture takes 27.223 ms, over its 24.5 ms bound` at 1x1, and 103.227 ms at 8x8;
  - every other case prints `pass`;
  - every control prints `caught`.
- Every other command exits 0.

## Known limitations / out of scope

- **The capture bound is not met**, by the decision described above. No interpretation was chosen to pass it.
- The flash model's erase and program waits are zero, so the commit's elapsed time is the store's pacing, not a part's.
- The mailbox's address is still the fixture's placeholder. The target platform firmware (S3) owns it.
- The image is the size fixture's composition, not the target platform's own `main`.
- The harness's traced lines and journal switches are passive, and the CPU budget's figures are not measured again here.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (not met: the capture bound; decision requested)
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

[A698d]

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

**GREEN: every gate and run is rc 0 at the head. That is 108 gates, the saved-state cases at both points, the CPU budget harness at both points, and the current flash writer's 24.5 ms check with its removal planted. Every control, plant and mutant is caught.**

Round 4 answers R738-F2 (MINOR: a refused run in a reused output directory left an earlier run's success table beside its refused record).

- A run first removes the earlier run's `results.json`, `table.md` and `refused.json` from its output directory.
- It validates the record before it writes anything, then writes `results.json` and `table.md` together.
- A refused run (exit 2) leaves only `refused.json`, which holds the refusal's words and the refused record and is shaped like no accepted record.

Round 3 answered R738-F1 (MINOR: the generated timing evidence dropped its clocks).

- `results.json` keeps the CPU and bus clocks its builds recorded.
- `table.md` names them beside every table.
- A record with a clock missing, a figure not converted at its CPU clock, or clocks that are not its builds' is refused.

The owner ruled on round 1's STOP on 2026-10-29 19:05: option (c) ([A10] issuecomment-6504551000). The split writer F1 is not held to D5's 24.5 ms capture bound, each F1 step stays bounded by T_svc, and the capture's total time is measured and recorded. D5's 24.5 ms stays on the current flash writer, gated by `check_nvm_capture.py`.

On the split CPU, at both points, with the CPU at 50 MHz (50,000,000 Hz) and the bus at 100 MHz (100,000,000 Hz), the clocks each point's builds recorded and its `results.json` carries:

| Point | Capture, CPU time | Capture, elapsed | Longest step, any phase | Against T_svc |
|---|---:|---:|---:|---|
| 1x1 | 1,361,143 cycles, 27.223 ms | 534.905 ms | 2.022 ms (a page program) | every step within |
| 8x8 | 5,161,328 cycles, 103.227 ms | 1,638.061 ms | 2.639 ms (a capture step) | every step within |

- Every case passes at both points:
  - the commit, with its capture of every record from its real owner;
  - the boots with valid, absent, torn and wrong-version slots;
  - D3's apply order;
  - the flash region guard.
- Every control is caught: the two reordered applies, the removed guard, a real step spun past T_svc, and the per-phase step control.
- The current flash writer's capture: at most 13.863 ms at 8x8, with the CPU at 50 MHz and the bus at 100 MHz, under its 24.5 ms (round 2's measurement; that writer and its harness are unchanged since). Removing its 24.5 ms check fails `check_nvm_capture.py` and this harness's self-test.

`665-s4-f1-target` -> `dev-soft-core`, head `4d9b901cd42fb21ac7c05432b88bb6c00061064a`: twelve commits on `dev-soft-core` `f4c9ad4f`, five from round 1, two from round 2, three from round 3 and two from round 4. It merges onto `dev-soft-core` `5b5f4336` with no conflict.

**It does not merge cleanly onto the live `dev-soft-core` `a68536fa`.** There are two conflicts, both in the CPU budget harness: `tb/verilator/ctrl_service_budget/split_soc.py` and its `README.md`. On `dev-soft-core`, #814's stage wraps the harness's LiteSPI PHY with `milan_soc.stage_spi_phy` (`dcd56703`). Round 1 of this PR gave the same PHY the generic PHY's CSRs and divisor, with the command master in LiteSPI's own bank (`0d61b327`). Resolving it needs a merge commit, and the stage adds bus cycles to every flash access, so both points would be re-measured at the merged head. That merge is left for a ruling; see [Known limitations](#known-limitations--out-of-scope).

## Linked Issue / roles

Relates to #665

Executor: `[A698d]` (round 1: `[A698]`, round 2: `[A698b]`, round 3: `[A698c]`)
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

The S4 lane of the Mark II split: F1's flash and saved-state ports on the target ([A10] issuecomment-6493622258). Round 2 applies the owner's ruling on the capture bound ([A10] issuecomment-6504551000). Round 3 answers R738-F1 ([A10] issuecomment-6511289316). Round 4 answers R738-F2 ([A10] issuecomment-6514339158).

| Piece | What changed |
|---|---|
| `sw/firmware/ctrl_nvm/plat/gen_flash_port.py` (new, round 1) | It generates the flash port's `generated/csr.h` and `generated/mem.h` from a split SoC export, so the port never compiles against a hand-written address. The addresses come from `csr.csv`; the field offsets come from the same export's LiteX `csr.h`, which `csr.csv` does not carry; every shared address is compared between the two. Eight named rules refuse an export: data width, registers, header, fields, flash window, journal, slots and clock. The journal must be `milan_soc.py`'s `FLASHBOOT_RESERVED` journal, which the store is built with. It must be two one-erase-block slots (the A/B geometry `check_nvm_record_space.py` check 5 sizes containers against), aligned, inside the device, and clear of the bitstream, the AEM, the user slot and every image the SoC publishes. |
| `sw/firmware/ctrl/test/ctrl_srp_image.py` (round 1) | `--flash-map DIR` puts the generated headers ahead of the RV32 stand-ins, and refuses a map whose clock is not the shape's. `--nvm-source DIR` takes a planted copy of the store. Both default to today's behaviour. |
| `tb/verilator/ctrl_service_budget/` (round 1) | `build.flash_map` exports the split SoC with the point's one-interface image, generates the map, then exports it again with the image linked against the map, and refuses two different maps. `split_soc` places the flash and `timer0` from the map, with LiteSPI's bank laid out as `add_spi_flash` builds it; `map_deviations` refuses a test-SoC `csr.csv` that places any port register, or the window, elsewhere. The testbench gains passive SPAN lines (a traced function's entry to its return) and CALL lines (the owners' and the port's entries), and a journal preload and dump. `build.Plant` and `build.Variant` let a client pass its own planted defect or arm. |
| `tb/verilator/nvm_split_target/` (new; round 2 regrades it) | The store's cases on the split CPU, graded from the SPAN and CALL lines: the commit and its phases; the boots with valid, absent, torn and wrong-version journals and their AECP and ACMP answers; D3's apply order; and the guard probe. Round 2: every service step of every case is graded against T_svc, and a step over it fails its case. The capture's CPU time and elapsed time are recorded with no bound of their own. The 24.5 ms capture bound, its one-page-past control and `--record-budget-findings` are removed. New: the `slow-step` plant (a real first step spun to 30 ms), the per-phase `step-over-t-svc` control, and a self-test check that the current flash writer's own grader still refuses a capture over 24.5 ms, with the mutant that deletes that check. Round 3:
  - `results.json` is a record: the point, its shape, `cpu_hz`, `sys_hz`, T_svc and the results.
  - The clocks are the ones every arm's `build.json` records; builds that disagree are refused.
  - `table.md` names both clocks, in MHz and in hertz, on the line above each of its tables.
  - The run is refused (exit 2) when the record lacks a clock, when a figure is not its CPU cycles at the record's CPU clock, or when the clocks are not its builds'.
  - The self-test checks all of this on a synthetic run at CPU 62.5 MHz and bus 125 MHz, and through `run.py`'s own `main`, with eight new mutants.

  Round 4:
  - `results.json` and `table.md` are one validated run's. A run removes the earlier run's pair and refusal before it builds (`run.clear`), and writes the pair only once the record is validated (`run.accept`).
  - A refused run leaves `refused.json` alone in their place (`run.refuse`): `refused`, its words, and `record`, the refused record or `null`.
  - The self-test runs `run.py`'s `main` twice in one directory: a success, then each refusal (a build without its CPU clock, builds that disagree, clocks that are not its builds', results misconverted), and a refusal, then a success. It checks `accept` and `refuse` directly too, with five new mutants. The fresh-directory controls stay.
  - The self-test has 73 checks: 48 checks and 25 mutants. |
| `sw/firmware/ctrl/test/ctrl_configs.py` (round 1) | The boundary gate's OUTSIDE list gains the two new files that name the firmware tree. The reasons for the harness's `build.py` and `split_soc.py` are updated. |
| Docs | `ctrl_nvm/README.md`: the generated map, the owners, the measured CPU time and, in round 2, the capture's time by the owner's decision. `ARCHITECTURE_HW_SW_SPLIT.md` sections 2, 5 and 6: F1's capture contract and which writer 24.5 ms covers. Both capture harnesses' READMEs. Round 3: the split-CPU figures in `ARCHITECTURE_HW_SW_SPLIT.md` section 5, `ctrl_nvm/README.md` and the target harness's Results name their CPU and bus clocks, and its README describes the clocks its results carry and the new checks. Round 4: the target harness's README describes its one-run output directory, its refusal record, and the new checks and mutants. |

No firmware function changes, so the unit-test rule adds no units. The store, the port and the owners are unchanged, and `fw_coverage.py --check` holds the ratchet. RTL is unchanged.

**T_svc.** The cases grade against the CPU budget harness's `scenario.T_SVC_MS`. At `dev-soft-core` `f4c9ad4f` that is still the 10 ms proposal; the owner approved 20 ms, graded per family as `min(T_svc, ceiling)`, on 2026-10-29 (issuecomment-6495692075), and the change that makes it normative edits FR_NFR 3.4.1 and `scenario.py`. 10 ms is under every family's bound, so a step within it is within each, and the cases take 20 ms with no edit here once that change lands.

Measured, beside the capture:

- The image plans equal the ledger (`SPLIT_CONTROL_MEMORY.md` section 5): 37.0 tiles at 1x1 and 57.5 at 8x8 with two interfaces. `nvm_stage` is 3,344 B and 13,264 B. The generated map moves no planned byte.
- `nvm_store_boot`'s CPU time on the split CPU at 50 MHz: 100.5 ms valid, 165.1 torn, and 10.1 absent or wrong-version at 1x1; 488.5, 745.1 and 34.9 ms at 8x8. The boot runs before the loop, and its time to ready is the target platform firmware's measurement.
- The capture decomposes into a fixed cost a step and a cost a payload byte: 11,062 + 263.7 a byte at 1x1, and 16,500 + 205.5 at 8x8. The fixed cost is mostly the port's 64-bit clock conversion.

## Authoritative references

- #665 [A10] issuecomment-6493622258 (S4) and issuecomment-6504551000 (the owner's decision of 2026-10-29 19:05, option (c)); the plan's section S4, restated by that decision.
- #665 [A10] issuecomment-6495692075: `T_svc` = 20 ms approved, graded per family.
- #665 issuecomment-6508235352: at this base the split CPU runs at 50 MHz and the bus at 100 MHz; a timing figure names its CPU clock.
- #665 [A10] issuecomment-6514866239 (the owner's decision of 2026-10-30 05:17): the product split CPU clock is 100 MHz, on `sys`, made by the S2b change. Its words for this PR: "S4's figures are recorded at the clocks its builds name, and that stays valid".
- #665 [A10] issuecomment-6511289316 and PR #812 issuecomment-6510793657: R738-F1.
- #665 [A10] issuecomment-6514339158 and issuecomment-6514335214: R738-F2.
- `docs/reference/FR_NFR.md` 3.4.1 and NFR-SCOUT-03.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 2: the boot sequence, steps 6 to 8; bindings, then formats, maps, the settle step and names (Milan v1.2 5.6.1); F1's capture contract.
- `sw/firmware/ctrl_nvm/README.md`: "The flash port", "Boot" items 5 to 9, "Write-back" (DR2a) and "The service bound".
- D5 on the current flash writer: `tb/verilator/nvm_capture_cpu/README.md` (the 24.5 ms bound, half the hold's 49 ms floor) and `scripts/check_nvm_capture.py`.
- `sw/litex/milan_soc.py` `FLASHBOOT_LAYOUT` and `FLASHBOOT_RESERVED`; `scripts/check_nvm_record_space.py` check 5.
- IEEE 1722.1-2021 7.2.1, 7.4.5 and 8.2.1, and Milan v1.2 5.5.3.5, for the two questions the cases ask.

## How to get into the same state

```sh
git fetch origin
git checkout 4d9b901cd42fb21ac7c05432b88bb6c00061064a
git submodule update --init --recursive
# the product LiteX tree with its patches, the pinned RV32 SDK and Verilator, as
# tb/verilator/nvm_capture_cpu/README.md "Run" describes, with the LiteX environment's
# python3 ahead of the SDK's bin on PATH; then
export LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
```

## How to validate

```sh
python3 -B tb/verilator/nvm_split_target/run.py --self-test
python3 sw/firmware/ctrl_nvm/plat/gen_flash_port.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 scripts/check_nvm_capture.py
python3 -B tb/verilator/nvm_split_target/run.py --point 1x1 --build-dir /tmp/nvm-target-1x1
python3 -B tb/verilator/nvm_split_target/run.py --point 8x8 --build-dir /tmp/nvm-target-8x8
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir /tmp/nvm-capture-8x8-50-on
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic off --build-dir /tmp/nvm-capture-8x8-50-off
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/builder/test_builder.py --require-rv32
make -C tb/verilator/nvm_cosim
(cd tests && behave)
```

To see the current writer's check fail when removed, delete the three lines of `grade_rows` that raise `worst measured copy exceeds half the 49 ms hold floor` in `tb/verilator/nvm_capture_cpu/run.py` and run `python3 scripts/check_nvm_capture.py`. It prints `FAIL: OFF timing limit was ignored` and exits 1. Restore the file afterwards.

Expected result / pass criteria:

- The self-tests exit 0; `nvm_split_target`'s prints `checks: 73   failures: 0`.
- Each `nvm_split_target` point exits 0:
  - every case prints `pass`;
  - every control prints `caught`, `slow-step` with `step 0 (idle) takes 30.2216 ms of CPU time, over T_svc 10.0 ms` at 1x1 (30.2139 ms at 8x8);
  - the report records the capture's CPU and elapsed time, "measured (no bound of its own)";
  - `results.json` carries `"cpu_hz": 50000000` and `"sys_hz": 100000000`, and `table.md` reads `Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).` above each of its three tables.
- A refused run in the same directory leaves only `refused.json`. For example, delete `cpu_hz` from `/tmp/nvm-target-1x1/capture-all/build.json` and run `python3 -B tb/verilator/nvm_split_target/run.py --point 1x1 --build-dir /tmp/nvm-target-1x1 --regrade`. It prints `REFUSED: the builds record different clocks ...` and exits 2, and `/tmp/nvm-target-1x1/results` then holds `refused.json` and neither `results.json` nor `table.md`. Restore the file, and the same `--regrade` exits 0 and writes the pair again.
- Every other command exits 0.

## Known limitations / out of scope

- **The capture's total time has no bound**, by the owner's decision. It is recorded: 0.53 s at 1x1 and 1.64 s at 8x8 elapsed, one record a 10 ms tick. A power loss inside it loses at most the unsaved change, because the previous slot stays valid.
- **T_svc's value.** At this base the cases grade against the 10 ms proposal. The approved 20 ms, graded per family (SRP's bound 18 ms), comes with the change that makes it normative.
- **The CPU clock.** Every figure here is at CPU 50 MHz and bus 100 MHz, the clocks this base's builds record. The product's 100 MHz on `sys` comes with the S2b change. After it, a re-run grades and labels at 100 MHz with no edit, because the harness reads each build's recorded clock. The target harness's README sentence on the CPU it runs ("at 50 MHz") and the lane's figures would then be restated from that run.
- **The merge onto the live base.** This head conflicts with `dev-soft-core` `a68536fa` in the CPU budget harness (see [Status](#status)). A resolution that keeps both sides would stage this PR's `FlashBoundary`, with its CSRs and divisor, through `milan_soc.stage_spi_phy` (which keeps the PHY's CSR names), and keep the command master and the placement checks. It is not made here, because it needs a merge commit this round was not given, and a re-measurement of both points.
- The flash model's erase and program waits are zero, so the commit's elapsed time is the store's pacing, not a part's.
- The mailbox's address is still the fixture's placeholder. The target platform firmware (S3) owns it.
- The image is the size fixture's composition, not the target platform's own `main`.
- `nvm_split_target`'s self-test, which holds the current writer's 24.5 ms check, runs in the lane gates, not yet in a hosted workflow. The hosted guard on that check is `check_nvm_capture.py` in the docs workflow, which is unchanged.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (the first item as the owner restated it on 2026-10-29)
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

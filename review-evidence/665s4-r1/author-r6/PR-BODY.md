[A698g]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).
- **[Round 5: merge of the split base](#round-5-merge-of-the-split-base)** — The merge of `a68536fa`, and the STOP it reached.
- **[Round 6: generated flash map in the platform boot](#round-6-generated-flash-map-in-the-platform-boot)** — Option (a), its figures, its gates and one open question.

## Status

**REVIEW READY at `7643aef613c5b87a246544f57d23ad9f1bf8311e`. Every gate and run of the round 6 assignment is rc 0 at this head, on clean clones. See [Round 6](#round-6-generated-flash-map-in-the-platform-boot); it carries the current figures and one open question on the SDK used for them.**

`665-s4-f1-target` -> `dev-soft-core`, whose tip is `a68536fa`, the one merge base. Nothing below this line in this section is current: it is round 4's status, kept as the record.

### Round 4 status (historical)

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

Executor: `[A698g]` (round 1: `[A698]`, round 2: `[A698b]`, round 3: `[A698c]`, round 4: `[A698d]`, round 5: `[A698e]`, round 6: `[A698f]`, `[A698g]`)
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
git checkout 7643aef613c5b87a246544f57d23ad9f1bf8311e
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
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-plants --self-test
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
  - every control prints `caught`, `slow-step` with `step 0 (idle) takes 30.2028 ms of CPU time, over T_svc 10.0 ms` at 1x1 (30.2724 ms at 8x8);
  - the report records the capture's CPU and elapsed time, "measured (no bound of its own)";
  - `results.json` carries `"cpu_hz": 50000000` and `"sys_hz": 100000000`, and `table.md` reads `Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).` above each of its three tables.
- A refused run in the same directory leaves only `refused.json`. For example, delete `cpu_hz` from `/tmp/nvm-target-1x1/capture-all/build.json` and run `python3 -B tb/verilator/nvm_split_target/run.py --point 1x1 --build-dir /tmp/nvm-target-1x1 --regrade`. It prints `REFUSED: the builds record different clocks ...` and exits 2, and `/tmp/nvm-target-1x1/results` then holds `refused.json` and neither `results.json` nor `table.md`. Restore the file, and the same `--regrade` exits 0 and writes the pair again.
- Each `ctrl_split_boot` shape prints `ctrl_split_boot: PASS (0 finding(s))`, ready at 84.372 ms at 1x1 and 184.622 ms at 8x8, and its self-test prints `6 of 6 native controls as required; 2 of 2 plants caught`.
- Every other command exits 0.

## Known limitations / out of scope

- **The capture's total time has no bound**, by the owner's decision. It is recorded: 0.54 s at 1x1 and 1.64 s at 8x8 elapsed, one record a 10 ms tick. A power loss inside it loses at most the unsaved change, because the previous slot stays valid.
- **T_svc's value.** At this base the cases grade against the 10 ms proposal. The approved 20 ms comes with the change that makes it normative. The owner has since relaxed SRP/MRP's bound from 18 ms to T_svc = 20 ms (issuecomment-6681686082). The tree still reads 18 ms beside the 10 ms it grades against, which stays under both.
- **The CPU clock.** Every figure here is at CPU 50 MHz and bus 100 MHz, the clocks this base's builds record. The product's 100 MHz on `sys` comes with the S2b change. After it, a re-run grades and labels at 100 MHz with no edit, because the harness reads each build's recorded clock. The target harness's README sentence on the CPU it runs ("at 50 MHz") and the lane's figures would then be restated from that run.
- **The SDK behind the figures.** They were measured with the gate environment's RV32 SDK, not the pinned build. The loaded images agree where compared; see [Round 6](#round-6-generated-flash-map-in-the-platform-boot).
- The flash model's erase and program waits are zero, so the commit's elapsed time is the store's pacing, not a part's.
- The mailbox's address is still the fixture's placeholder. The target platform firmware (S3) owns it.
- The saved-state cases' image is the size fixture's composition, not the target platform's own `main`. The split boot simulation runs the platform's image, on the generated flash map.
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

## Round 5: merge of the split base

Round 5 added merge `36d12bd373` of `dev-soft-core` `a68536fa`, then `65bbbe219c` to pass the store tree and the absent flash map explicitly in the platform image builder. The two shared CPU budget harness files retain both the generated address layout and #814's PHY stage. No rebase or force update.

The round stopped because S3's boot simulation still called `fixture_addresses()` without the now-required generated map. On `65bbbe21` it refused before simulation; on `a68536fa` it passed. [The STOP records the evidence and alternatives](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6677078898).

## Round 6: generated flash map in the platform boot

Relates to #665.

[The ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6677095110) selects option (a) in this PR. Four commits on `65bbbe219c`, with no rebase and no force. No RTL and no firmware C changes.

| Commit | Change |
|---|---|
| `93c6e9a544` | `ctrl_plat_image.py` gains `--flash-map` and forwards it to `aecp_inputs`. `ctrl_split_boot/run.py` builds its shape's map with `build.flash_map` and hands it to both image links and both exports. `boot_soc.build` calls `fixture_addresses(map)` and refuses a deviation, as `split_soc.build` does. `ctrl_configs.py`'s entry for `run.py` and both READMEs follow; S3's listed "F1's flash port" item is closed. |
| `400c7ca712` | Groups the two maps in `ImageMaps`, keeping the link helper within the parameter limit the Python idiom gate holds. Both images are byte-identical before and after. |
| `1de390e104` | Restates this lane's capture, boot and longest-step figures at the merged head. |
| `7643aef613` | Corrects `1de390e104` (below), and lists the flash map among `run.py`'s build steps. Documentation only. |

**What `7643aef613` corrects.** `1de390e104` overwrote the `valid`, `absent`, `torn` and `version` rows of `nvm_split_target/README.md`'s case table with boot measurements: the rows that state what each case must show. No gate reads that table. They are restored byte for byte from `65bbbe219c`, and the boots table keeps its figures. `400c7ca712` also dropped `ctrl_split_boot/README.md`'s control rows, the same tree with the PHY stage removed, instead of restating them. They are back, re-measured: the stage now costs 541 CPU cycles at 1x1 and 532 at 8x8, where the page had said 523.

**On "no F1 placeholder in any split image".** Both links the boot simulation makes use the generated map. `ctrl_plat_image.py` still accepts no map, for one caller: the boundary gate's compile (`ctrl_runs.py`), which is given absent runtime archives and stops at its link by design, so it produces no image.

### Figures at this head

S3's split boot, CPU 50 MHz and bus 100 MHz, the PHY staged. Both print `ctrl_split_boot: PASS (0 finding(s))`, and the self-test prints `6 of 6 native controls as required; 2 of 2 plants caught`.

| Shape | Boot to ready | CPU cycles | Trace | Earlier, on the stand-in addresses |
|---|---:|---:|---|---:|
| 1x1, one interface | 84.372 ms | 4,218,617 | 18 of 18 equal | 84.393 ms |
| 8x8, one interface | 184.622 ms | 9,231,088 | 18 of 18 equal | 184.658 ms |

This lane's cases, same clocks. Every case passes and every control is caught at both points, and `results.json` and `table.md` are byte-identical to those the restated documentation was taken from.

| Point | Capture, CPU time | Capture, elapsed | Longest step | `valid` / `absent` / `torn` / `version` boot, CPU cycles |
|---|---:|---:|---:|---|
| 1x1 | 1,367,366 cycles, 27.347 ms | 542.977 ms | 2.023 ms (a page program) | 5,050,293 / 506,900 / 8,300,664 / 504,932 |
| 8x8 | 5,168,647 cycles, 103.373 ms | 1,641.818 ms | 2.641 ms (a capture step) | 24,519,265 / 1,747,362 / 37,436,744 / 1,745,393 |

The merge moves these a little from round 4's (27.223 and 103.227 ms of capture), because the PHY stage adds bus cycles to each flash access.

### New check, and the checks repeated

| Check | Planted defect | Its words |
|---|---|---|
| `boot_soc.build`'s placement guard | `spiflash_master_cs` expected four bytes off, in a scratch map | `the boot SoC does not place the flash port's devices as the split SoC does`; with the guard removed, the same export succeeds, so the defect escapes |
| D5 on the current flash writer | its 24.5 ms check removed in a scratch clone | `FAIL: OFF timing limit was ignored`; unplanted it passes |
| The reuse probe | round 3's `run.py` | the stale table reproduced; the head leaves `refused.json` alone |
| The real refusal, at each point | `cpu_hz` deleted from a real build | exit 2, `REFUSED: the builds record different clocks`; restored, exit 0 and both outputs byte-identical |

### Gates

Every gate ran on a clean clone of `7643aef613c5b87a246544f57d23ad9f1bf8311e`, the tree checked clean after each.

| Gate | Result |
|---|---|
| The 97 short gates | `0 of 97 gates nonzero or left the tree dirty`, the same 97 names as round 4; behave under the CI constraints: 508 scenarios passed, 0 failed; `nvm_split_target` self-test `checks: 73   failures: 0` |
| The 11 long gates | `0 of 11 gates nonzero or left the tree dirty`, the same 11 as round 4; each is below |
| `test_builder.py --require-rv32` | `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11's calibration report, which needs a vendor build tree, as in every round |
| `test_ctrl_nvm.py --require-rv32 --self-test` | `OK across 5 shape(s), 435 tests, and all 109 planted defects reddened` |
| `test_ctrl_firmware.py --require-rv32 --self-test` | `test_ctrl_firmware: PASS`, 1,053 plants caught, none escaped |
| `fw_coverage.py --selftest`, `--check` | `29 of 29 planted cases read as planted`; `firmware coverage: PASS (35 files)`, 100 % lines and branches after the gate's exclusions |
| `firmware_boundary`, both modes | `ctrl_boundary: PASS` in each |
| `nvm_cosim` and its lint | `465 checks: 465 PASS, 0 FAIL`, `39 of 39 mutant(s) killed by their named check` |
| `publication_census --check --selftest` | `checks: 246   failures: 0`; `selftest: 0 of 139 arm(s) failed` |
| `ctrl_memory` | `test_ctrl_memory: 0 failure(s)` |
| S3's split boot, both shapes, and its self-test | rc 0, as above |
| `nvm_split_target`, both points | rc 0, as above |
| The CPU budget harness, 1x1 | rc 0: `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)`, its table byte-identical to round 5's |
| The CPU budget harness, 8x8 | rc 0: `17 groups graded, 0 refusals, 57 T_svc misses (57 of 182 probe instances, 29 of 129 paths)`; see below |
| The D5 plant and the probes | all as above |
| `docs.yml`, every job | 71 steps ran, each rc 0; 24 not run, each with its reason (below) |
| `git diff --check a68536fa`, merge bases | rc 0; one merge base, `a68536fa`, which is still `dev-soft-core`'s tip |

The `docs.yml` replay ran each job on its own fresh clone, with an empty `HOME` and a new virtual environment, as on a fresh hosted runner. So all three SDK steps downloaded the pinned archive, checked its digest and printed `SDK fresh installation: verified`, with no cache hit; neither the installer nor the workflow is changed. `gate_42` ran in a disposable container with no network, because it executes the candidate's `act_ci.py`. The 24 steps not run are the hosted-only ones: recording and verifying a hosted run's own step context, the fail-fast and cancel steps, and the `apt-get` and `sudo install` steps whose packages this machine already has. The builder legs print `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`: 15 of those are arms that need LiteX, as on a fresh runner, and the `test_builder.py` gate above runs with LiteX and covers them. Gate 11's calibration report needs a vendor build tree and is not run anywhere, as in every round.

This is local evidence; the hosted contexts on the pushed head remain mandatory.

### The CPU budget harness at 8x8

At 8x8 the harness now grades 57 of 182 instances over T_svc (29 of 129 paths). Its page, `tb/verilator/ctrl_service_budget/README.md`, records 66 of 182 (34 of 129) on the stand-in addresses, and round 4 measured 62 of 182 (30 of 129). 1x1 has not moved: 34 of 141, its table byte-identical to round 5's. This is the first complete 8x8 run at the merged base.

Against round 4, path by path: 5 of 123 common paths change verdict, in both directions, with a mean change of -0.114 ms and extremes near one loop pass (`acmp.disconnect_tx.if0` from 16.452 to 1.151 ms, `acmp.get_tx_state.if0` from 1.157 to 16.547 ms). That reads as probes landing in a different pass after the image changed, not as a slowdown, though that mechanism is inferred from the spread and not proved. No bound applies to this count and the run is rc 0. The page labels its figures as measured on the stand-ins, so it stays true as written, and it is not restated here: the ruling assigns S3's and this lane's figures, and that page is shared.

### Open question: the SDK behind the figures

The gate environment's RV32 SDK is not the pinned build. It identifies as Buildroot 2026.05 and the pinned archive as Buildroot 2021.11-18033-g83947c7bb6, both GCC 14.3.0 for the same target, and 1,680 of the 5,007 entries in the pinned install's receipt differ. Every round of this lane measured with it.

So each comparison below rebuilt from this head with the pinned SDK as the only RV32 toolchain reachable:

- S3's image at both shapes: every loaded section byte-identical, and the same ready time and cycles.
- This lane's `fixture`, `capture-all` and `guard-probe` images at both points: every loaded section byte-identical, and `results.json` and `table.md` byte-identical.
- In each image the two symbol tables hold the same symbols, in a different order. That is the only difference.

**No figure this PR states depends on the difference.** The CPU budget harness's images and the firmware campaigns were not compared. Whether the shared gate environment should move to the pinned SDK is a question for a maintainer; this PR changes nothing there.

# HANDOFF: lane M8a-1 for #640 (split placement's on-chip control memory)

Executor [A594]. Reviewers [R606] (internal), [R607] (external).
Branch `640-m8a` from dev `e8454e2751d05b02ee8e5a571857589ab358ab86`; the manager pushed `08b90b68` as PR #721, then round 2's `76605880` as its head. Round 3's commits are local, not pushed.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100371426
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100426002
STOP (round 1): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101473717 (its handoff and PR body are kept in `stop-round/`)
Ruling: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101485877
REVIEW READY (M8a-1): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6104411638

## Round 5 (M8a-1, answering R606-4 and R607-4)

Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6118560882 (scope ruling 6101485877 still applies).
Reviews answered: R606-4 (PR #721 comment 6118557490) and R607-4 (PR #721 comment 6118122865), both NEGATIVE on one MINOR (R606-4-F1 = R607-4-F1).
Base of this round: `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d` (PR #721's head; round 4 was the manager's merge of dev `c6bd08c6` into `ce10328c`). New commits only, no rebase or amend, not pushed.
REVIEW READY (round 5): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6119125404 (text in `evidence-r5/review-ready.md`)

**Status: REVIEW READY (M8a-1 round 5).** Head `42678ae2f77fbbef056f7fb99859e0193181e6d7`: one commit on `8ab2b539`, local, not pushed. Every A10 item is answered (R5.1), and every gate the change touches passes at the head, rc 0 (R5.8).

- `42678ae2` Re-measure the split control memory's fit on the firmware merged from dev c6bd08c6, 54 tiles mapped and 55.0 planned at the largest point, and carry it into both ledgers, 125 and 114 after the release (#640)

3 files, +50 / -44 (`git diff --stat 8ab2b539..42678ae2`), documentation only. No limit is exceeded, so no STOP: the largest point plans 55.0 of 56 RAMB36, and its flat span is 223,776 of the 229,376 B (224 KiB) limit.

- R5.1 Items and the change that answers each
- R5.2 Runtime
- R5.3 Linked spans at the four points
- R5.4 Primitive mapping, before and after
- R5.5 Ledger rows
- R5.6 Reviewers' probes re-run
- R5.7 Changes, with file:line
- R5.8 Gate table
- R5.9 Not done, and why

### R5.1 Items and the change that answers each

R606-4-F1 and R607-4-F1 are the same MINOR (R606-4: Conformance, Docs; R607-4: Conformance, Tests, Docs): dev `c6bd08c6` grew all four linked images, so the documented fit described the images of `ce10328c`.

| A10 item | Result |
|---|---|
| Re-measure the four linked-image points with a recorded runtime | Linked at `8ab2b539` by `ctrl_srp_image.py --with-aecp --layout split` (and `--layout flat`), both shapes, one and two interfaces; 12 links and 4 plans rc 0 (R5.3). Runtime recorded (R5.2). Control: the same runtime at `ce10328c` reproduces round 1's four split ELFs byte for byte |
| Isolated mapping on those images | `syn/ooc/ctrl_memory_ooc.py` on the four head ELFs, then its Vivado script under the exclusive lock: rc 0, 8 tops, every ROM `$readmem` read (R5.4) |
| Reconcile the documents | `SPLIT_CONTROL_MEMORY.md` section 5 (fit table, bank fill, headroom, logic-bank attribution, LUT figures, the 1.0-tile bound, the 114 total) and the section-3 SoC-control line; both ledgers' rows, arithmetic and headroom (R5.5, R5.7). Earlier figures kept only with their source named: `ce10328c` (the previous fit), `e8454e27` (BIOS and whole-image SRAM), `c20ed894` (the SoC-build controls) |
| Limits | 55.0 <= 56 planned; 54.0 as mapped; flat span 223,776 <= 229,376 B; split need 224,312 B and allocation 225,280 B, both <= 229,376 B. No STOP |
| Runtime workaround | R607-4's `runtime_probe.py`, unmodified, exactly as the reviewers used it (only `-fno-stack-protector` added to the runtime's compiles); recorded in R5.2. The fix is #723's |
| Re-run both reviewers' probes | R607-4 `run_fit.py` (head and `previous-` at `ce10328c`) and `compare_fit.py`: rc 0, PASS; R606-4 `link_points.sh` on both trees and `fit_summary.py`: rc 0, identical figures (R5.6) |
| R606-4-R1 residue (PR body) | `PR-BODY.md` Status: R606-4-R1's exact sentence applied; the manager edits the PR |

### R5.2 Runtime

- Recipe: `sw/firmware/ctrl/test/ctrl_image_runtime.py`, run through R607-4's `runtime_probe.py` unmodified (copy: `evidence-r5/runtime/runtime_probe.py.reviewer-copy`). It inserts `-fno-stack-protector` into the recipe's `gcc -c` calls and edits no source. That is #723's defect.
- Inputs: the pinned RV32 SDK `riscv32-ilp32d--glibc--stable-2025.08-1` (GCC 14.3.0; `ci_rv32_sdk.py --verify-only` rc 0, archive `d42680e9...`); picolibc and compiler-rt data and LiteX's `soc/software` from the pinned LiteX stack. Each source, dependency and command is in `evidence-r5/runtime/provenance.json`.
- Archives: `libc.a` `418259ffc5f184ee0652edc782aab4efadff18688e485c1d25d831394c39047f` (5,542 B), `libcompiler_rt.a` `9a4ec8ce80bec34bab63615f736a97b882b366435c448db0d0e9b1904452a630` (29,432 B).
- These hashes differ from R607-4's (`2fab1665...`, `e32cb0d0...`) and from this lane's round-1 archives (`431165b0...`, `e80334d9...`). `ar` records each member's build time and owner (`ar tv`). The linked images do not differ: at `ce10328c` this runtime links the four split ELFs round 1 mapped (`22521d14...`, `61c5c4d0...`, `611d57c0...`, `8a4d7fa9...`), the ones R606-4 also reproduced with its own runtime.

### R5.3 Linked spans at the four points

At `8ab2b539` (`evidence-r5/fit-head/`), bytes:

| Point | .text | .rodata | .data | .bss | stack | `rom` need | `sram` need | Sum | Flat span |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 84,616 | 11,950 | 56 | 37,508 | 8,192 | 96,624 | 45,776 | 142,400 | 142,256 |
| 1x1, two interfaces | 86,044 | 11,950 | 56 | 48,884 | 8,192 | 98,056 | 57,152 | 155,208 | 155,056 |
| 8x8, one interface | 84,732 | 25,158 | 448 | 77,684 | 8,192 | 110,344 | 86,336 | 196,680 | 196,144 |
| 8x8, two interfaces (largest) | 86,236 | 25,158 | 448 | 103,820 | 8,192 | 111,848 | 112,464 | 224,312 | 223,776 |

| Point | `rom` banks | `sram` banks | Planned tiles | Bank fill `rom` / `sram` | Byte floor | Headroom to 56 |
|---|---|---|---:|---|---:|---|
| 1x1, one interface | 64K+32K | 32K+8K+4K+2K | 35.5 | 98.3 / 97.2 % | 35 | 20.5 tiles |
| 1x1, two interfaces | 64K+32K | 32K+16K+8K | 38.0 | 99.7 / 99.7 % | 38 | 18.0 tiles |
| 8x8, one interface | 64K+32K+8K+4K | 64K+16K+4K+2K | 48.5 | 99.8 / 98.0 % | 48 | 7.5 tiles |
| 8x8, two interfaces | 64K+32K+8K+4K+2K | 64K+32K+8K+4K+2K | 55.0 | 99.3 / 99.8 % | 55 | 1.0 tile: 4,096 B of granules, 5,064 B with the bank slack |

- Inside the spans, unchanged: descriptor image `aecp_entity_image` 7,512 / 19,520 B; `nvm_stage` 3,344 / 13,264 B, equal to `ctrl_memory.stage_bytes` (each plan passes its shape's `--stage-bytes`); lwSRP pool `image_arena` 9,920 / 19,840 / 24,032 / 48,064 B.
- Against `ce10328c` (same runtime, `evidence-r5/fit-prev/`): `.text` +1,596 / +1,736 / +1,664 / +1,792; `.bss` +256 / +264 / +256 / +264; `.rodata` and `.data` unchanged. The `rom` need crosses a granule at the shipping point (35.0 -> 35.5; its `rom` goes from five banks to two) and at the largest (54.5 -> 55.0; a fifth `rom` bank, 2 KiB).
- Split ELFs at the head: `27dc78da...` (1x1/1), `dcd58b96...` (1x1/2), `7b9abdfa...` (8x8/1), `60190c0f...` (8x8/2) (`evidence-r5/fit-head/elf.sha256`). Each was linked three times, by `fit_r5.sh`, R607-4's `run_fit.py` and R606-4's `link_points.sh`, with identical bytes.
- An independent check (`evidence-r5/scripts/fit_table.py`) recomputes each plan's tiles from the needs (granules / 2) and its banks from the granule count's binary digits; all eight plans agree.

### R5.4 Primitive mapping, before and after

Out of context, `syn/ooc/ctrl_memory_ooc.py` with the bench LiteX interpreter, then `vivado -mode batch -nojournal -source ctrl_memory_ooc.tcl` (Vivado 2026.1, `xc7a100t-fgg484-2`, `-mode out_of_context -directive AreaOptimized_high`, `Synth 8-4445` promoted to an error). Exclusive lock held from 07:55:41 to 07:57:46 (+02:00) on 2026-10-12; rc 0; 8 of 8 `synth_design` completed; all 13 ROM `$readmem` files read; no ERROR or CRITICAL WARNING. `evidence-r5/map/` (`ctrl_memory_ooc.tsv`, `util/*.rpt`, `mapping-report-lines.txt`; the 238 KB Vivado log by sha256 in `large-logs.sha256.txt`).

Per region, at `8ab2b539`:

| Top | Banks | Planned RAMB36 / RAMB18 | As mapped RAMB36 / RAMB18 | LUT | FF | LUTRAM | In logic |
|---|---|---:|---:|---:|---:|---:|---|
| `s1i1_rom` | 64K+32K | 24 / 0 | 23 / 1 | 36 | 3 | 0 | none |
| `s1i1_sram` | 32K+8K+4K+2K | 11 / 1 | 11 / 1 | 92 | 5 | 0 | none |
| `s1i2_rom` | 64K+32K | 24 / 0 | 23 / 1 | 36 | 3 | 0 | none |
| `s1i2_sram` | 32K+16K+8K | 14 / 0 | 14 / 0 | 53 | 4 | 0 | none |
| `s8i1_rom` | 64K+32K+8K+4K | 27 / 0 | 25 / 1 | 327 | 37 | 0 | bank 3, 1,024 words |
| `s8i1_sram` | 64K+16K+4K+2K | 21 / 1 | 21 / 1 | 90 | 5 | 0 | none |
| `s8i2_rom` | 64K+32K+8K+4K+2K | 27 / 1 | 26 / 1 | 169 | 28 | 0 | bank 4, 512 words |
| `s8i2_sram` | 64K+32K+8K+4K+2K | 27 / 1 | 27 / 1 | 97 | 6 | 0 | none |

The ROM mapping report lists every `rom` bank except the one marked in logic; bank 0 maps as `16384x31` (a constant bit column trimmed) at every point. `report_utilization` gives 161 Slice LUTs for `s8i2_rom` and 314 for `s8i1_rom` (`ctrl_memory_ooc.py` counts LUT primitives: 169 and 327).

Per point, before (the images of `ce10328c`, mapped in round 1) and after (the images of `8ab2b539`):

| Point | Planned, before -> after | As mapped RAMB36 / RAMB18, before -> after | As mapped tiles, before -> after | LUT / FF, before -> after | Logic bank, before -> after |
|---|---|---|---|---|---|
| 1x1, one interface | 35.0 -> 35.5 | 33 / 2 -> 34 / 2 | 34.0 -> **35.0** | 212 / 32 -> 128 / 8 | 512 words -> none |
| 1x1, two interfaces | 38.0 -> 38.0 | 37 / 1 -> 37 / 1 | 37.5 -> **37.5** | 89 / 7 -> 89 / 7 | none -> none |
| 8x8, one interface | 48.5 -> 48.5 | 46 / 2 -> 46 / 2 | 47.0 -> **47.0** | 307 / 33 -> 417 / 42 | 1,024 words -> 1,024 words (fuller: 962 words used, was 546) |
| 8x8, two interfaces | 54.5 -> 55.0 | 52 / 2 -> 53 / 2 | 53.0 -> **54.0** | 328 / 40 -> 266 / 34 | 1,024 words -> 512 words (the 1,024-word bank is now full, in block RAM) |

- `sram` still maps exactly as planned at every point.
- The four points remain at their byte floor or within one tile of it as mapped (35 / 38 / 48 / 55 floor; 35.0 / 37.5 / 47.0 / 54.0 mapped).
- Planned minus mapped is 0.5 / 0.5 / 1.5 / 1.0 tiles: the trimmed bit column at every point, plus the logic bank at 8x8. That bounds what forcing the logic bank into block RAM can cost (at the largest point the 512-word bank is one RAMB18).

Before the split (unchanged, round 1, `e8454e27`): BIOS ROM 16 RAMB36, BIOS SRAM 2, identifier memory 1 RAMB18 (kept); one LiteX `wishbone.SRAM` of the whole 221,728 B image 64 RAMB36.

### R5.5 Ledger rows

`MARK_II_AREA_PLAN.md` (Firmware and block RAM ledger) and `AREA_BUDGET.md` (mirror):

| Item | Before (`ce10328c` images) | After (`8ab2b539` images) |
|---|---|---|
| Firmware allocation as mapped, 8x8 with two interfaces | +52 RAMB36, +2 RAMB18, +53 tiles, 122 after | +53, +2, **+54**, 123 after |
| M2 maximum additional allocation | 124 after | 125 after |
| Conditional release, split only | 113 after | **114** after |
| Arithmetic | `87.5 - 6.5 + 6 - 18 + 53 + 2 = 124` | `87.5 - 6.5 + 6 - 18 + 54 + 2 = 125` |
| Every bank in block RAM (planned) | 54.5: 125.5 and 114.5 | 55: 126 and 115 |
| Below 121.5 after the release | 8.5 (seven all in block RAM) | 7.5 (6.5) |
| Over 121.5 before the release | 2.5 | 3.5 |
| Keeping the BIOS memories | 142 and 131 | 143 and 132 |
| Partial placement, six AECP tiles kept | `124 + 6 = 130`, 8.5 over | `125 + 6 = 131`, 9.5 over |
| At the ruled 56 firmware tiles | 116, 5.5 below | unchanged |
| Wrapper storage gives way above | 50.5 firmware tiles | unchanged (`71 + F`) |

The 13.5-tile reserve is untouched in every row. These agree with R606-4's planned figures for the head (126 and 115).

### R5.6 Reviewers' probes re-run

| Probe | How run | rc | Result |
|---|---|---:|---|
| R607-4 `runtime_probe.py` | from the lane root, the recipe's own arguments | 0 | the runtime of R5.2 |
| R607-4 `run_fit.py PACKET python3` | from the lane at `8ab2b539`; `PACKET/scratch/runtime` holds the R5.2 archives | 0 | four links rc 0 |
| R607-4 `run_fit.py PACKET python3 previous-` | from an isolated clone at `ce10328c` with `third_party/lwSRP` `9197193e`, `protocol-processor` `2ad2f845` and `gptp-processor` `5dce647a` at their pins | 0 | four links rc 0 |
| R607-4 `compare_fit.py PACKET` | | 0 | `PASS reproduction: previous links match all four published rows; merged links change every span`; head 35.5 / 38.0 / 48.5 / 55.0; its "not the documented 6144" refers to the text at `8ab2b539`, which `42678ae2` replaces with 4 KiB (1.0 tile) |
| R606-4 `link_points.sh <tree> <out> python3 <runtime>` | for the `ce10328c` clone and for the lane | 0, 0 | 16 links and 8 plans rc 0 |
| R606-4 `fit_summary.py <ce10328c> <head>` | | 0 | every head figure of R5.3, headroom `5064 B` at the largest; the `ce10328c` side gives the documented round-1 figures |

Receipts: `evidence-r5/probes/R607-4/`, `evidence-r5/probes/R606-4/`. The probes are the published files, downloaded from the review-evidence branch into a scratch directory and run unmodified.

### R5.7 Changes, with file:line (at `42678ae2`)

| File:line | Change |
|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md:111` | The round-1 SoC-build controls named as linked at `c20ed894` |
| `docs/design/SPLIT_CONTROL_MEMORY.md:142` | The revision the figures link: `8ab2b539`, carrying dev `c6bd08c6` (F-INT's publication writers, lwSRP `08ee86e8`) |
| `docs/design/SPLIT_CONTROL_MEMORY.md:147-150` | Fit table: needs, planned, as mapped, LUT/FF at the head |
| `docs/design/SPLIT_CONTROL_MEMORY.md:153`, `:156-157` | Bank fill 97.2 to 99.8 percent; 2 tiles left as mapped; 4 KiB (1.0 tile) of banks, 5,064 B with the slack, before refusal |
| `docs/design/SPLIT_CONTROL_MEMORY.md:162`, `:164-166` | The logic banks (1,024 words at 8x8/1, 512 words at 8x8/2; none at 1x1); 327 of 417 and 169 of 266 LUT cells; 161 Slice LUTs |
| `docs/design/SPLIT_CONTROL_MEMORY.md:170-171` | Share of the 169; at most 1.0 tile |
| `docs/design/SPLIT_CONTROL_MEMORY.md:173-178` | The `ce10328c` figures with their source; dev `c6bd08c6`'s growth at the largest; BIOS and whole-image SRAM named to `e8454e27`; 114 tiles |
| `docs/design/MARK_II_AREA_PLAN.md:42` | M8a-1 maps 54 at the largest shape |
| `docs/design/MARK_II_AREA_PLAN.md:811-813` | Ledger rows: +53 / +2 / +54, 123; 125; 114 |
| `docs/design/MARK_II_AREA_PLAN.md:822-824` | 54 tiles, linked at `8ab2b539`; the 512-word bank, 169 LUT cells; 55 all in block RAM |
| `docs/design/MARK_II_AREA_PLAN.md:827-829`, `:834-836`, `:841` | 125 and 114; 126 and 115; 3.5 over, 7.5 and 6.5 below; 143 and 132 |
| `docs/design/MARK_II_AREA_PLAN.md:872-873` | Partial placement: `125 + 6 = 131`, 9.5 over |
| `docs/design/AREA_BUDGET.md:232` | M8a-1 maps 54 at the largest shape |
| `docs/design/AREA_BUDGET.md:246-248` | Ledger rows, as the plan |
| `docs/design/AREA_BUDGET.md:254`, `:259-262`, `:267-268`, `:283`, `:388` | 143 and 132; 54, 55, `... + 54 + 2 = 125`, 114; 3.5 over, 7.5 and 6.5 below; 131, 9.5 over; 54 out of context |

No code, test, configuration or gitlink changed. The default shipping behaviour and the register map are untouched.

### R5.8 Gate table

Every command unpiped with its own log and rc (`evidence-r5/`).

| # | Gate | Environment | Tree | rc | Result |
|---:|---|---|---|---:|---|
| G1 | Four points, split and flat, then `ctrl_memory.py plan` with each shape's `--stage-bytes` (`scripts/fit_r5.sh`) | host Python 3.14.7 (the fixture's builder needs PyYAML), pinned RV32 SDK verified, R5.2 runtime | `8ab2b539` (firmware identical at `42678ae2`) | 0 x 12, 0 x 4 | R5.3; tree clean before and after |
| G2 | The same, previous-source control | isolated clone at `ce10328c`, three submodules at its pins | `ce10328c` | 0 x 12, 0 x 4 | four split ELFs byte-identical to round 1's mapped images |
| G3 | `syn/ooc/ctrl_memory_ooc.py` on the four G1 ELFs | bench LiteX interpreter | `8ab2b539` | 0 | 8 tops; its plans equal G1's |
| G4 | Its Vivado script, out of context, under the exclusive lock | Vivado 2026.1 | G3's output | 0 | R5.4; 8 of 8 synthesised, 13 ROM images read, no ERROR or CRITICAL WARNING |
| G5 | R607-4 `runtime_probe.py`, `run_fit.py` (head, `previous-`), `compare_fit.py`; R606-4 `link_points.sh` (both trees), `fit_summary.py` | as G1 and G2 | both | 0 each | R5.6 |
| G6 | `.github/workflows/docs.yml`: every `docs-check` command in workflow order (80), `wire-accountability`, `docs-check-no-git` on the committed tree exported without `.git` (`scripts/docs_parity.sh`, round 3's, the workflow's command list unchanged) | CPython 3.12.3 venv with the job's installs only (hash-locked HDL reference parser and Markdown renderer, PyYAML, wavedrom 2.0.3.post3); sv2v v0.0.12; GNU make 4.3; a HOME holding only the pinned RV32 SDK; no LiteX interpreter; em-dash base `c6bd08c6` (the merge base with live `dev`) | `42678ae2` committed | 0 x 83 | 83 of 83. Among them: `docs_check.py` 0 findings over 205 pages; `check_em_dash.py --base c6bd08c6` 0 findings over 324 added lines; `gen_toc.py --selftest`/`--verify-anchors`/`--check`; `check_doc_paths.py` 969 paths; `check_doc_style.py`; `ci_events.py --check` OK (1,821 items) and `--selftest` PASS (2,530 arms); `act_ci.py --selftest`; the idiom, hygiene, TODO, fail-fast and test-evidence ratchets; `test_builder.py --require-rv32` `ALL GATES PASS EXCEPT 17 NOT RUN`: 15 LiteX arms (no LiteX interpreter in that job, by design), gate 11 (no bench report) and gate 1b's `MAKEFLAGS += -e` mutation. The test measures its make: GNU make 4.3, first on PATH here as on the hosted runner, does not honour the construct, so the arm would detect nothing. Round 3 had 14: dev added the gate 23m pair, and round 3's PATH put the host's GNU make 4.4.1 first, which honours it |
| G7 | `scripts/run_litex_sims.sh --selftest`, then the aggregate (`scripts/litex_aggregate.sh`) | `litex_pins.txt`-only CPython 3.12.3 venv (round 3's; pins and patches unchanged since), pinned Verilator 5.050, a HOME holding only the pinned SDK | working tree = `42678ae2`'s content | 0, 0 | 10 of 10; **7 of 7**; `test_ctrl_memory`: 0 failures, `RESULT: PASS`, 44 of 44 mutants caught, and `SPLIT_CONTROL_MEMORY.md section 3 lists the 17 rules of ctrl_memory.RULES in order` ok (the page is gate-read; this round edits one line of that section) |
| G8 | `scripts/ci_scope.py --selftest`; the three changed pages | CPython 3.12.3 `-I` | `42678ae2` | 0 | PASS; `SPLIT_CONTROL_MEMORY.md` true, `AREA_BUDGET.md` true, `MARK_II_AREA_PLAN.md` false |
| G9 | `syn/ooc/pp_resource_gate.py check-baseline` (the reader of `AREA_BUDGET.md`) | CPython 3.12.3, as `rtl-fast.yml:214` runs it | `42678ae2` | 0 | `baseline PASS: 3 endpoints` (a first try with `-I` failed to import its sibling module; the workflow runs it without `-I`) |
| G10 | Before the commit: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`/`--verify-anchors`, `check_doc_paths.py`, `pp_resource_gate.py check-baseline`, `git diff --check` | docs venv | working tree | 0 each | PASS |

Hosted runs at `8ab2b539`, read only at 06:38 UTC: `docs`, `elaborate`, `rtl-fast` and `rtl-full` completed with success (`evidence-r5/gates/hosted-8ab2b539.txt`). Their acceptance is the manager's; `42678ae2` is not pushed.

### R5.9 Not done, and why

- No integrated route and no boot: the assignment needs neither this round; both stay M8a-2's, after F-INT PR 2.
- The SoC-build controls of round 1 were not re-run on the merged image: section 3 now names the revision they linked (`c20ed894`). The standing controls in `test_ctrl_memory.py` (synthetic ELFs, the linked probe, the real SoC build) passed at this head (R5.8).
- `scripts/run_all_suites.sh`, `syn/yosys/run.sh`, `sw/builder/test_builder.py --require-elaboration` and the firmware host suites were not run: `42678ae2` changes three pages under `docs/design/` and nothing they read. The merge `8ab2b539` is the manager's, and its source bank belongs to the manager's merge-candidate validation, as both reviews record.
- The local Actions replica (`scripts/act_ci.py --pr 721`): it refuses anything but the exact remote PR head, and `42678ae2` is not pushed.
- R606-4-S1 (a standing gate that links the largest image and reports its margin): optional and not in A10's list. This round shows the erosion it describes: one dev merge cost 0.5 RAMB36 at the largest point.
- R606-4's observation on the plan's and budget's "Unpriced ... M6/M7" sentences: dev's text, outside this PR; not touched.
- Retained optional findings (R606-2-S1..S5, R606-3-S-a..S-c): unchanged, as both reviews list them; S5 is #723.

## Round 3 (M8a-1, answering R606-2 and R607-2)

Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6107088105 (scope ruling 6101485877 still applies).
Reviews answered: R606-2 (PR #721 comment 6107064124) and R607-2 (PR #721 comment 6107065061), both NEGATIVE.
Base of this round: `76605880a20005cbc2acad1b23ba2ccebde64ca8` (PR #721's head). New commits only, no rebase or amend, not pushed.
REVIEW READY (round 3): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6107961867 (text in `evidence-r3/review-ready.md`)

**Status: REVIEW READY (M8a-1 round 3).** Head `ce10328c3d89d81509e47836fa4a48b22ecdbc20`: five commits on `76605880`, local, not pushed. Every A10 item is answered (R3.1). The hosted-parity gate set A10 names passes at the committed head, every command rc 0 (R3.6). What was not taken is in R3.1 and R3.8.

- `22caf7351` Register the split control memory page as gate-read, since the elaborate job's test holds its rule table to the rules (#640) (item 1)
- `087df1447` Grade the split SoC arm in the elaborate job's interpreter by refusing LiteX's firmware data packages, and grade each mutant only against an arm that passes unmutated (#640) (item 2)
- `4a2608cdf` Refuse a split image whose load segments do not carry its sections' initial bytes or the reset word, the only bytes that program rom, with linked-image and SoC regressions and four mutants (#640) (item 3)
- `4a57b41df` Derive the partial placement's pre-release total from the current ledger rows, 124 + 6 = 130 and 8.5 over the ceiling at the measured 53, and name the ruled 56-tile allocation where the wrapper storage gives way (#640) (item 4)
- `ce10328c3` Say that the 2.5 tiles over 121.5 before the conditional release include M2's unused +2 allowance (#640) (item 5)

8 files, +179 / -45 (`git diff --stat 76605880..ce10328c`). The live remote `dev` tip is still `ac2c5e77`, which this head contains.

- R3.1 Items and the change that answers each
- R3.2 Changes, with file:line
- R3.3 Item 2: why the SoC arm does not resolve the firmware data packages
- R3.4 Item 3: load data, the rules and their regressions
- R3.5 Tests and the planted defect each catches
- R3.6 Gate table (round 3, hosted-parity set at the head)
- R3.7 Primitive mapping, resources and route
- R3.8 Not done, and why

### R3.1 Items and the change that answers each

| A10 item | Finding (reviewer's lenses) | Change |
|---|---|---|
| 1 | R606-2-F1 BLOCKER (Tests, Docs, Conformance): `SPLIT_CONTROL_MEMORY.md` is read by a gated test but not registered; `ci_scope.py --selftest` rc 1 and every hosted classifier step red | `GATE_READ_DOCS` lists the page, with a classification case; `CI_WORKFLOWS.md` says seven gate-read pages and names `test_ctrl_memory.py` as this one's reader. `ci_scope.py --selftest` rc 0; `ci_scope.py docs/design/SPLIT_CONTROL_MEMORY.md` prints `true` |
| 2 | R606-2-F2 MAJOR (Tests, Docs): the SoC arm resolves `pythondata_software_picolibc`, which `litex_pins.txt` does not install | The SoC child refuses every `pythondata_software_*` import in every interpreter and writes LiteX's headers without the firmware make inputs, as `sw/builder/test_shipping_clock_constraints.py` does (choice justified in R3.3). A mutant is graded only against an arm that passed unmutated in the same run. `CI_WORKFLOWS.md` and `TESTING.md` state the arm's real needs. In a `litex_pins.txt`-only CPython 3.12.3 interpreter: `RESULT: PASS`, aggregate 7/7, and both mutants R606-2 named are killed by their own checks (R3.5) |
| 3 | R607-2-F1 MINOR (Conformance, RTL, Robustness, Tests, Docs): reset-byte check reads section metadata, ROM is built from `p_filesz` bytes | New rule `load coverage` (`memory map`): every section with initial bytes must be carried by the load segments' file bytes. `entry bytes` also requires those bytes to carry the first word at the reset address, so the documented reset-byte rule is now true of the bytes that program ROM rather than reworded. Regressions on the test's ELFs, on the genuinely linked probe and through the real SoC build; four new mutants; the register has 17 rules. The four shipped split images plan and program identically (R3.4) |
| 4 | R606-2-F3 MINOR (Docs): partial-placement figure and give-way basis stale | Plan `:842`, `:870-871` and budget `:269`, `:279-280`: `124 + 6 = 130`, 8.5 over 121.5 at the measured 53; "What gives way for the ruled 56-tile firmware allocation" |
| 5 | R606-1-R1 residue (retained by R606-2 and R607-2) | The two exact texts: budget `:263`, plan `:832` |

Not taken (not in A10's list, all optional or another lane's): R606-2-S1 (sram sections outside the copied `[_fdata, _edata)` and `[_fbss, _ebss)` ranges), S2 (unnamed IndexError/ValueError for out-of-range `e_shstrndx`, symtab `sh_link`, or `sh_entsize` 0; fail-closed), S3 (`mtvec`), S4 (`rom_words` longer than the planned banks), S5 (the runtime's stack protector: the manager's separate Issue).

### R3.2 Changes, with file:line (at `ce10328c`)

| File:line | Change |
|---|---|
| `scripts/ci_scope.py:63-65`, `:69` | `GATE_READ_DOCS` gains `docs/design/SPLIT_CONTROL_MEMORY.md`, its reader named in the comment |
| `scripts/ci_scope.py:288-289` | Case: that page alone is RTL relevant, so the selftest's mutation arm can catch the table dropping it |
| `docs/testing/CI_WORKFLOWS.md:76`, `:94-97` | "Seven pages"; the reader and that no `docs-check` step runs it |
| `docs/testing/CI_WORKFLOWS.md:1188-1199` | The SoC arm's real needs: PyYAML, the pinned and patched LiteX, no firmware data package (refused, headers written without the firmware make inputs), one more VexiiRiscv argument set |
| `sw/litex/ctrl_memory.py:84-85` | Rule `load coverage` under `memory map`, after `loads outside rom` (17 rules) |
| `sw/litex/ctrl_memory.py:246-252` | `_carried(segments, start, end)`: whether the load segments' file bytes cover `[start, end)`, chaining adjacent and overlapping segments |
| `sw/litex/ctrl_memory.py:272-274` | `entry bytes`, second clause: no load segment carries the first word at the reset address |
| `sw/litex/ctrl_memory.py:283-285` | `load coverage`: a section with initial bytes not all in the load segments' file bytes |
| `sw/litex/test_ctrl_memory.py:4-53` | Docstring: arms 2, 4, 5 and 7 as changed |
| `sw/litex/test_ctrl_memory.py:315-318`, `:335-338` | Refusal arms: reset segment emptied, reset section moved in the section table (`entry bytes`); reset segment cut to one word, `.data`'s segment emptied (`load coverage`) |
| `sw/litex/test_ctrl_memory.py:548-556` | `filesz_at`: an independent program-header reader for the linked-image plants |
| `sw/litex/test_ctrl_memory.py:578-584`, `:594-604` | Link arm: rom words equal the toolchain's `objcopy -O binary`; three plants on the linked probe |
| `sw/litex/test_ctrl_memory.py:629-667` | `FirmwareDataRefused`; the SoC child inserts it and wraps `Builder._generate_includes` to `with_bios=False`, recording LiteX's own argument |
| `sw/litex/test_ctrl_memory.py:693-694`, `:723-724`, `:738-743` | `soc_case` records init files; the split export requires the include hook ran once with `True`; fourth SoC control (reset segment emptied, `entry bytes`); every control requires no Verilog and no init file |
| `sw/litex/test_ctrl_memory.py:807-816` | Mutants 8b, 10b, 10c, 10d (R3.5) |
| `sw/litex/test_ctrl_memory.py:928-937`, `:969-991` | `mutant_arms(green)`: a mutant of an arm that failed unmutated is a FAIL "not graded", never a kill; `main` records each arm's outcome |
| `docs/design/SPLIT_CONTROL_MEMORY.md:77`, `:89-91`, `:106-107` | Rule row; `rom` holds the load segments' file bytes only and what the two rules require of them; the fourth SoC control |
| `docs/testing/TESTING.md:697-719` | The linked probe's objcopy equality and load-segment plants; the fourth control; the data packages refused; 44 mutants; no mutant graded by a red arm |
| `docs/design/MARK_II_AREA_PLAN.md:832`, `:842`, `:870-871` | Residue text; give-way heading; `124 + 6 = 130`, 8.5 over |
| `docs/design/AREA_BUDGET.md:263`, `:269`, `:279-280` | The same three |

Ledger arithmetic, from the table rows in the same documents: `87.5 - 6.5 + 6 - 18 + 53 + 2 = 124`; partial placement keeps AECP's six tiles: `124 + 6 = 130`; `130 - 121.5 = 8.5` over. Pre-release firmware tiles `F` give `71 + F`, so the wrapper storage must give way above 50.5 tiles, inside the ruled 56.

### R3.3 Item 2: why the SoC arm does not resolve the firmware data packages

Chosen: do not resolve them, as `sw/builder/test_shipping_clock_constraints.py:20-27`, `:67-73` does (#607 F2). Not chosen: provisioning them in the job and the pins.

- **The arm needs none of them.** It exports with `--no-compile-software`. LiteX's `Builder` reads `pythondata_software_picolibc` and `_compiler_rt` in exactly one place that fails: `_generate_includes(with_bios=True)` writing `variables.mak` (their directories), `output_format.ld` and `regions.ld`, the make inputs of a software build (`litex/soc/integration/builder.py:285-310`, through `_get_variables_contents` at `:238-267`, at the pinned `a1e1c365`). `_create_build_bundle` reads them only under `try/except`. The headers the gateware needs (`soc.h`, `csr.h`, `mem.h`) are still written, and every property the arm checks reads the Verilog, its `.init` files, `csr.csv` and the inputs the `Builder` is handed, none of which a make input touches.
- **The arm grades the same in every interpreter.** The child refuses the import whatever is installed, so a host with the packages grades exactly as the hosted job. Round 2's 7/7 came from an interpreter that had them; this round the bench interpreter (`~/litex-milan`, packages present) and the `litex_pins.txt`-only interpreter produce the same 123 checks, line for line apart from temporary paths.
- **One pattern in the tree.** The sibling test settled the same question for the same job a lane earlier. A second answer would be a second thing to keep true.
- **Provisioning is wider than M8a-1.** It changes `sw/litex/litex_pins.txt` (two more git packages, picolibc with its submodules), the `elaborate` install step and its pip cache key, a CI contract other lanes share and `scripts/ci_events.py` pins, for packages no gate in this lane uses.
- **What it costs.** The arm does not exercise LiteX's make-input generation for the split SoC. Compiling software for the split image is M8a-2's boot, which builds real firmware and grades it there.

The check `the Builder writes the SoC headers once, without the firmware make inputs ([True])` holds the hook to LiteX's own call: it ran once, handed LiteX's `with_bios=True`. If a LiteX bump stopped calling `_generate_includes`, the hook would no longer be what writes the headers, and this check fails by name rather than letting the arm pass on a path it does not see.

### R3.4 Item 3: load data, the rules and their regressions

`rom_words` (`ctrl_memory.py:312-318`, unchanged) programs `rom` from each load segment's first `p_filesz` bytes. Before this round, `entry bytes` and the section loop read only the section table (`loaded` = not NOBITS), so an image whose segments carry fewer bytes than its sections claim was planned and exported with zeros where the code should be (R607-2's `probe_load_soc.py`: eight zero words at the reset address, build rc 0).

- `entry bytes` keeps its section clause and adds: the load segments' file bytes cover `[entry, entry + 4)`, the first instruction word at the reset address (`:272-274`).
- `load coverage`: every section with initial bytes has `[lma, lma + size)` covered by those file bytes (`:283-285`), checked after `loads outside rom` in the same per-section loop.
- Both run in `check_map`, so in `plan`, so in `add_ctrl_memory` before any Verilog or init file exists.
- The valid images are unchanged: the four shipped split ELFs (`22521d14...`, `61c5c4d0...`, `611d57c0...`, `8a4d7fa9...`, the round-1 fit images) give the same plan summary and the same `rom_words` sha256 before and after (`evidence-r3/rom-digest-before.txt`, `-after.txt`: identical; e.g. the largest, 27,514 words, `71c54cb0...`).

R607-2's probes, run unmodified with a fresh output directory each:

| Probe | At `087df144` (before) | At `4a2608cd` (after) |
|---|---|---|
| `probe_elf_loads.py` no-load-segments | REFUSED `loads outside rom` | REFUSED `entry bytes` |
| reset-segment-empty | ACCEPTED, first words `[0, 0]` | REFUSED `entry bytes` |
| reset-segment-short | ACCEPTED, first words `[403769859, 0]` | REFUSED `load coverage` |
| header cuts 6/7/16/20/40/51 | REFUSED `elf truncated` | the same |
| `probe_load_soc.py` (linked probe, reset `p_filesz` 0, real split export) | rc 0, `REPRODUCED`, 1 Verilog, eight zero words | rc 1 (its reproduction assertion fails): refusal `reset entry: no load segment carries the first word at the reset address 0x00000000, so rom would hold none there`, 0 Verilog |

`evidence-r3/scripts/probe_linked_soc.py` (this round) drives the same real export with the linked probe kept, emptied and cut to one word: valid control rc 0 with its eight reset words `10003117 d2010113 07c00293 10000317 ff430313 10000397 ff038393 00737c63` kept; emptied rc 1 `entry bytes`, cut rc 1 `load coverage`, each with 0 Verilog and 0 init files.

### R3.5 Tests and the planted defect each catches

| Test (file:line) | Planted defect it catches | Result |
|---|---|---|
| `ci_scope.py` case `SPLIT_CONTROL_MEMORY.md` -> relevant (`:288-289`) with the derivation arm | The page missing from `GATE_READ_DOCS` (the state at `76605880`) | `76605880`: selftest rc 1, `FAIL gate-read page docs/design/SPLIT_CONTROL_MEMORY.md (named at sw/litex/test_ctrl_memory.py:81) is relevant`; head: rc 0, and the mutation arm's `gate-read docs/design/SPLIT_CONTROL_MEMORY.md filed as docs-only is rejected` ok |
| SoC child's refusal and include hook (`test_ctrl_memory.py:629-667`) | The arm needing a firmware data package (the state at `76605880`) | at `22caf735` (test and `ctrl_memory.py` as at `76605880`) in the pins-only interpreter: `[FAIL] the split build exports (rc 1, ImportError: pythondata-software-picolibc ...)`, `RESULT: FAIL`, and the two named mutants "caught" by that ImportError; head: `RESULT: PASS` in both interpreters |
| SoC child's refusal, with the hook removed (control D1, R3.6) | The include hook not installed, on a host that has the packages | `[FAIL] the split build exports (rc 1, ImportError: pythondata-software-picolibc module not installed! ...)` in the bench interpreter too, `RESULT: FAIL` |
| Include-hook check (`:723-724`) | The hook bypassed while the export still succeeds (a LiteX that stopped calling `_generate_includes`) | holds `[True]` at the head; not plantable without editing LiteX |
| Mutant grading against green arms only (`:928-937`) | A mutant "caught" by the arm's own unmutated failure (R606-2: two SoC mutants killed only by the ImportError) | control D1: all six SoC mutants `[FAIL] ... is not graded: the soc arm fails unmutated`, none `caught` |
| `entry bytes`, section table moved (`:317-318`) | `entry bytes off` (mutant 8): the section clause removed | killed: refused by `addresses` instead |
| `entry bytes`, reset segment emptied (`:315-316`; linked `:595`; SoC `:738-739`) | `entry bytes read the sections only` (8b) | killed: refused by `load coverage` instead |
| `load coverage`, reset segment cut to one word (`:335-336`; linked `:596-597`) | `load coverage off` (10b); `load coverage reads the first byte only` (10c) | killed: accepted, expected `load coverage` |
| `load coverage`, `.data`'s segment emptied (`:337-338`; linked `:598`) | `load coverage off` (10b) | killed (also by the cut) |
| reset segment emptied, through `_carried` | `a segment carries bytes below its start` (10d) | killed: accepted, expected `entry bytes` |
| objcopy equality (`:578-584`) | rom words that differ from the toolchain's own load image of the linked probe | ok: 32 words, 128 bytes |

The SoC mutants in the pins-only interpreter at the head, each killed by its own property (first named FAIL):

| Mutant | Killed by |
|---|---|
| BIOS ROM built | the stage-size control, the first whose image plans and so reaches `add_module`: rc 1, `AssertionError` from LiteX's `assert not hasattr(self, name)` (`litex/gen/fhdl/module.py:87`), because the BIOS `rom` already exists when the control memory adds its own |
| BIOS SRAM built | the same, for `sram` |
| control memory not added | the over-budget control: rc 1, `AttributeError: 'MilanSoC' object has no attribute 'ctrl_image'` (no rule) |
| main() staging check removed | the stage-size control: `rc 0: None`, the 8x8 stage exported |
| flag pairing off | `--ctrl-mailbox alone is refused` (rc 1, the constructor's `ValueError`, not rc 2 with the pairing message) |
| shipping firmware linked | `the split build adds no shipping firmware` |

### R3.6 Gate table (round 3)

**Hosted-parity set at the committed head `ce10328c`** (A10's list), every command unpiped with its own log and rc:

| # | Gate | Environment | rc | Result |
|---:|---|---|---:|---|
| H1 | `.github/workflows/docs.yml` `docs-check`: all 80 commands, in workflow order (`evidence-r3/scripts/docs_parity.sh`, `evidence-r3/docs-parity/summary.tsv`) | CPython 3.12.3 venv with the job's installs only: the hash-locked HDL reference parser, PyYAML, the hash-locked Markdown renderer, wavedrom 2.0.3.post3; sv2v v0.0.12 (zip sha256 `ff8c9eea...`); GNU make 4.3; a HOME holding only the pinned RV32 SDK, installed fresh from the `d42680e9...` archive and verified; no LiteX interpreter; em-dash base the merge base with the live `dev` `ac2c5e77` | 0 each | 80 of 80 rc 0. Among them: `docs_check.py`, `check_em_dash.py --base ac2c5e77`, the doc-style, diagram, source-fact, submodule, wavedrom, PNG, feature-status and matrix gates, `make -C gptp-processor docs`, the RV32 SDK self-test and verification, `test_firmware_compiler.py` both modes, `test_builder.py --require-rv32` (`ALL GATES PASS EXCEPT 14 NOT RUN`: the LiteX arms, which have no interpreter in that job, and gate 11), the NVM, SoC-source, RTL-source, naming, port, fail-fast, TODO, test-evidence, hygiene, SV/C++/Python/shell idiom gates with self-tests, `ci_events.py --check`/`--selftest`, `act_ci.py --selftest`, `check_doc_paths.py`, archive, `gen_toc.py --selftest`/`--verify-anchors`/`--check`, AEM store, sweep/deploy/entity shape |
| H2 | `docs.yml` `wire-accountability`: `check_wire_accountability.py --self-test` | as H1 | 0 | PASS |
| H3 | `docs.yml` `docs-check-no-git`: `docs_check.py`, `check_feature_status.py` in the committed tree exported without `.git` | as H1 | 0 each | PASS |
| H4 | `scripts/ci_scope.py --selftest` | CPython 3.12.3 `-I` | 0 | `selftest: PASS`; the page's case, derivation and mutation lines all `ok` |
| H5 | `scripts/ci_scope.py docs/design/SPLIT_CONTROL_MEMORY.md` | CPython 3.12.3 `-I` | 0 | `true` |
| H6 | `scripts/ci_events.py --check`; `--selftest` | CPython 3.12.3 with PyYAML, `-I` | 0, 0 | `OK (1749 contract item(s) across 4 workflow files and docs/testing/CI_WORKFLOWS.md)`; `selftest: PASS (1749 contract items, 2374 arms)` |
| H7 | `scripts/run_litex_sims.sh --selftest`, then `scripts/run_litex_sims.sh <logs>` | `litex_pins.txt`-only CPython 3.12.3 venv (`evidence-r3/venv-freeze.txt`: the pins, PyYAML and their dependencies; no `pythondata_software_*`), `scripts/ci_litex_env.py` and `sw/litex/patches/apply.sh` run as `elaborate.yml` runs them, the CPU metadata cache restored as its cache step does; pinned Verilator 5.050; RV32 SDK at `$HOME` | 0, 0 | 10 checks PASS; **7 of 7 PASS**, 0 skipped; `test_ctrl_memory`: 123 checks, 0 failures, `RESULT: PASS`, 44 of 44 mutants caught |
| H8 | `sw/builder/test_builder.py --require-elaboration --require-rv32` (the `elaborate` job's other gate) | as H7 | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, the bench build tree; as in rounds 1 and 2); 17 min |
| H9 | `sw/litex/test_ctrl_memory.py` in the bench interpreter, which has both firmware data packages | bench LiteX venv, same SDK | 0 | `RESULT: PASS`; its log equals H7's member log line for line once temporary directory names are normalised (`ci-vs-bench.diff`: empty) |
| D1 | Control: H9 with the include hook removed (`Builder.build, Builder._generate_includes = build, generate_includes` to `Builder.build = build`), file restored with `git checkout` after, tree verified clean at the head | bench venv | 1 (planted) | `[FAIL] the split build exports (rc 1, ImportError: ...)`; six SoC mutants `not graded` (`control-D1-bench.log`) |

**Per-item gates at each commit** (logs under the lane's scratch directory; the deciding ones copied to `evidence-r3/gates/`):

| Commit | Gates | rc |
|---|---|---|
| `22caf735` (item 1) | `ci_scope.py --selftest` (CPython 3.12.3 `-I`) and the page's classification; `ci_events.py --check`/`--selftest`; `check_py_idiom.py`; `docs_check.py`; `gen_toc.py --check`; `check_doc_style.py`; `check_doc_paths.py`; `check_em_dash.py --base 76605880`; `git diff --check` | 0 each |
| `087df144` (item 2) | `test_ctrl_memory.py` in the pins-only venv and the bench venv (110 checks each, `RESULT: PASS`); `run_litex_sims.sh --selftest` and the aggregate in the pins-only venv (7 of 7); `check_py_idiom.py` (CPython 3.12.3 and the Markdown venv) and `--selftest`; test-evidence, hygiene, TODO, fail-fast ratchets; `ci_scope.py --selftest`; `ci_events.py --check`; docs gates and em-dash as above | 0 each |
| `4a2608cd` (item 3) | `test_ctrl_memory.py` in the pins-only venv (123 checks, 44 mutants, `RESULT: PASS`); the aggregate (7 of 7); R607-2's two probes and `probe_linked_soc.py` (R3.4); `rom_digest.py` on the four shipped split ELFs (identical); the same Python, ratchet, classifier and docs gates | 0 each (the reproducing probe now rc 1 by design) |
| `4a57b41d`, `ce10328c` (items 4, 5) | `docs_check.py`; `gen_toc.py --check`/`--verify-anchors`; `check_doc_style.py`; `check_doc_paths.py`; `syn/ooc/pp_resource_gate.py check-baseline` (`AREA_BUDGET.md` is gate-read: `baseline PASS: 3 endpoints`); `ci_scope.py --selftest`; `check_em_dash.py --base 76605880`; `git diff --check` | 0 each |

Not run this round, and why:

- `scripts/run_all_suites.sh` and `syn/yosys/run.sh`: no file under `hdl/`, `tb/` or `syn/` and no gitlink changed since `76605880`, where the sweep passed 61 of 61 and Yosys 58 of 58 (round 2, R2.7).
- The local Actions replica (`scripts/act_ci.py --pr 721`): it refuses anything but the exact remote PR head, and round 3 is not pushed. Hosted and replica acceptance at the pushed head belong to the manager.
- Vivado: nothing it maps changed (R3.7).

### R3.7 Primitive mapping, resources and route

Unchanged this round. `CtrlMemory`, the bank plan and `ctrl_split.ld`/`ctrl_split_start.S` are untouched, and the four shipped split images plan and program byte-identically under the new rules (R3.4), so round 1's out-of-context mapping stands: 33/2, 37/1, 46/2 and 52/2 RAMB36/RAMB18 (34.0, 37.5, 47.0, 53.0 tiles) against 35.0, 38.0, 48.5 and 54.5 planned. Before: the base BIOS ROM took 16 RAMB36 and its SRAM 2 (sections 5 and 6). The route through the M0s recipe is M8a-2's, after F-INT PR 2.

### R3.8 Not done, and why

- R606-2's S1 to S5: optional, or the manager's separate Issue (S5); listed in R3.1. S1 (sram sections outside the startup copy) and S2 (unnamed errors for out-of-range table indices) stay open as suggestions.
- The include hook relies on LiteX's private `Builder._generate_includes`, as the sibling test does. A LiteX bump that renames it makes the arm fail by name (the `ImportError`, or the `[True]` check), not pass.
- M8a-2 (boot, service checks, route) still waits for F-INT PR 2.

## Round 2 (M8a-1, answering R606-1 and R607-1)

Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105011666
Reviews answered: R606-1 (PR #721 comment 6104999232) and R607-1 (PR #721 comment 6105008317), both NEGATIVE on MINORs only.
Base of this round: `08b90b6859b0a7d7f172c7ae29745248895d9aa9` (`5d532e9d` plus the manager's merge of dev `ac2c5e77`). New commits only, no rebase or amend, not pushed.
REVIEW READY (round 2): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6106342513 (text in `evidence-r2/review-ready.md`)

**Status: REVIEW READY (M8a-1 round 2).** Head `76605880a20005cbc2acad1b23ba2ccebde64ca8`: three commits on `08b90b68`, local, not pushed. Every A10 item is answered (R2.1). Every gate the change touches passed, rc 0 (R2.7). R607-1's twelve mutants are all KILLED, and R606-1's `main()`-stage mutant turns the SoC test red (R2.5). What was not taken is listed in R2.1 and R2.8.

- `be431eec9a018f56e558bdbc97407255189b12ce` Register every split memory refusal rule, refuse writable data in rom and truncated ELFs by name, and require a named failure for each rule removed, the SoC build's controls and the whole decoded window (#640)
- `516d7fb87c530f16dcf512c85a528da6f76e14ea` State the 56-tile ledger total as 116 tiles leaving 5.5, the ruled firmware limit, and the 231 LUT cells as the rom region with its decode (#640)
- `76605880a20005cbc2acad1b23ba2ccebde64ca8` Say which split memory rules the SoC build runs while it builds the memory

9 files, +843 / -245 over the round (`git diff --stat 08b90b68..76605880`).

- R2.1 Findings and the change that answers each
- R2.2 Changes, with file:line
- R2.3 The rule registry and the standing mutation check
- R2.4 The SoC build test
- R2.5 Reviewer mutants and probes re-run
- R2.6 Docs and figures
- R2.7 Gate table (round 2)
- R2.8 Not done, and why

### R2.1 Findings and the change that answers each

| Finding | Lens (reviewer's) | Change |
|---|---|---|
| R606-1-F1: writable initialised data in `rom` accepted | Robustness, Tests | New rule `writable in rom` (`memory map`), `ctrl_memory.py:271-273`; `Section.writable` from `SHF_WRITE`; unit arm (`.data` linked to run in rom) and the link plant `} > sram AT > rom` to `} > rom` (R606-1's own edit) |
| R606-1-F2 / R607-1-F1: hole graded at one address; five mutants survive | Tests | Simulation at the largest image's sram banks (64+32+8+4+2 KiB) for both regions; 47 hole addresses per region from the first word past the banks to word `0xFFFF` (the 256 KiB decoded window, past 224 KiB), incl. `0x8000`, `0x8001`, `0x8000 + words - 1`, `0xDFFF`, `0xE000`; every answer must be err alone (ack, both or none fail); 215 alias cells read back; back-to-back read presented on the cycle after err must ack with its data, both regions |
| R607-1-F1: budget boundary, three refusals unarmed | Tests | 56.0 RAMB36 accepted and 56.5 refused (`BUDGET_BSS`); arms for NOBITS in rom, shared load address, no bytes at entry; every rule in `ctrl_memory.RULES` has an arm and a mutant, enforced by the test |
| A10 item 1: one list, a standing mutation check | Tests | `ctrl_memory.RULES` (16 rules); `test_ctrl_memory.py` register arm requires `SPLIT_CONTROL_MEMORY.md` section 3's table to equal it, every rule to have a refusal arm and a mutant; 40 mutants each rebuild one definition from its own source with one edit and must be killed by a named FAIL |
| R606-1-F3 / R607-1-S1: SoC hookup untested | Tests | SoC arm: `milan_soc.py`'s own `main()` in a child process on the shipping 1x1 config's argv, exporting with `--no-compile-software`: three controls refused by rule before any Verilog, both lone flags refused (rc 2, the pairing message), and the passing split export checked (banks, no BIOS memories, rom init = image, `csr.csv` regions, Builder handed no BIOS and no shipping firmware). R606-1's `main()`-stage mutant is mutant 38 and turns it red |
| R607-1-S2 (A10 item 3, required): truncated ELF unnamed | Robustness | Rule `elf truncated` (`memory map`): every header, table and symbol read via `_unpack` (`ctrl_memory.py:185-190`), names via `_string` (`:193-199`), load segments (`:216-219`); four arms (cut in header, cut to half, segment past end, name past end) |
| R606-1-F4 = R607-1-F2: 56-tile sentences, `AREA_BUDGET.md:382`, lane row | Docs | `MARK_II_AREA_PLAN.md:861-862` and `AREA_BUDGET.md:265`: 116 tiles, 5.5 below; `AREA_BUDGET.md:382-383`: the ruled limit, up to 56 RAMB36 as mapped, and 53 out of context; `MARK_II_AREA_PLAN.md:1046`: the ruled 56-tile allocation |
| R606-1-F5: 231-LUT attribution | Docs | `SPLIT_CONTROL_MEMORY.md:157-163` and `MARK_II_AREA_PLAN.md:821`: 231 LUT cells is the `rom` region (logic bank plus bank decode and read multiplexer); basis named (LUT primitives; 220 Slice LUTs in `report_utilization`); decode cost shown (36 LUT cells for two rom banks with none in logic, 97 for the largest sram); M8a-2 weighs the bank's share only |
| R607-1-F3 (= R606-1-R2): PR body stale | Docs | PR body names the round-2 head, the base `08b90b68` = `5d532e9d` + merge of dev `ac2c5e77`, and the aggregate 7 of 7 |
| R607-1-R1 | Docs (residue) | `SPLIT_CONTROL_MEMORY.md:149-150`: the exact text |
| R607-1-R2 | Docs (residue) | Column header `LUT cells / FF` (`SPLIT_CONTROL_MEMORY.md:139`); "most of each point's LUT cells: 231 of the largest point's 328" (`:157`); "in 231 LUT cells" (`MARK_II_AREA_PLAN.md:821`). Each sentence also carries F5's attribution, since the unit change alone keeps the attribution F5 refutes |

Not taken (not in A10's list): R606-1-R1 ("measured" wording with M2's unused +2 allowance, `AREA_BUDGET.md:263`, `MARK_II_AREA_PLAN.md:832`), R606-1-S1 (trap vector), R606-1-S2 (an assertion on `rom_words` length). R607-1-S3 is the manager's separate issue.

### R2.2 Changes, with file:line (round 2)

| File:line | Change |
|---|---|
| `sw/litex/ctrl_memory.py:24-28` | Docstring: RULES and the test's requirement |
| `sw/litex/ctrl_memory.py:59` | `_SHF_WRITE` |
| `sw/litex/ctrl_memory.py:64-94` | `Rule` (check, refuses) and `RULES`: 16 rules keyed by name, in the doc table's order |
| `sw/litex/ctrl_memory.py:97-104` | `Refusal(rule, detail)`: `.rule` and `.check` (looked up in RULES, so an unregistered rule cannot refuse); the message is unchanged, `"<check>: <detail>"` |
| `sw/litex/ctrl_memory.py:139` | `Section.writable` |
| `sw/litex/ctrl_memory.py:185-199` | `_unpack` and `_string`: bounds-checked reads, refused as `elf truncated` |
| `sw/litex/ctrl_memory.py:202-246` | `read_elf`: `elf class`, `elf machine`, every read bounds-checked, load segments checked, `writable` read |
| `sw/litex/ctrl_memory.py:243-249` | `_overlap(rule, spans)`: refuses by its rule (`regions`, `addresses`, `initial bytes`) |
| `sw/litex/ctrl_memory.py:253-276` | `check_map`: each refusal names its rule; new `writable in rom` (`:271-273`) |
| `sw/litex/ctrl_memory.py:288`, `:322-330` | `budget`; `stage symbol`, `stage size` |
| `sw/litex/milan_soc.py:2743` | `add_ctrl_memory`'s CPU check refuses as `cpu origins` (was `reset entry` as the only argument; the check name stays `reset entry`) |
| `sw/litex/test_ctrl_memory.py` | Rewritten around the rule register: arms 1-7 in the docstring (`:4-46`); `refused` matches rule and check and names any other exception (`:106-118`); `Layout`/`elf`/edits (`:199-272`); `FakeSoC` (`:275-292`); `refusal_arms` (`:295-336`); `check_arms` (`:339-373`); simulation (`:376-510`); link (`:515-559`); SoC build (`:564-680`); `PROPERTIES`, `MUTANTS` (`:683-790`); `mutated` (`:793-811`); register (`:824-844`); mutants (`:847-868`); `run_arm` (`:871-878`); `main` (`:881-906`) |
| `scripts/check_py_idiom.py:174-197` | `DYNAMIC_EXEC_INVENTORY` gains `sw/litex/test_ctrl_memory.py` with its guard (the edit matches once; `ast.parse` of the result is exactly one definition of that name; runs in that module's namespace); the comment counts the fourth entry |
| `docs/design/SPLIT_CONTROL_MEMORY.md:62-110` | Section 3: the per-rule table (= RULES), the boundary, the test's register, mutation check and SoC arm |
| `docs/design/SPLIT_CONTROL_MEMORY.md:139-163` | Section 5: `LUT cells / FF`; R607-1-R1 text; the 231 attribution and basis |
| `docs/design/MARK_II_AREA_PLAN.md:821, 861-862, 1046`; `docs/design/AREA_BUDGET.md:265, 382-383` | Ledger figures (R2.6) |
| `docs/testing/TESTING.md:697-714`; `docs/testing/CI_WORKFLOWS.md:1185-1190` | The test's arms; the SoC arm's needs in the hosted job (PyYAML; one more VexiiRiscv argument set) |

The register's existing check names are unchanged (`reset entry`, `memory map`, `memory-map overlap`, `allocation over budget`, `staging buffer`), so every log line and refusal message the reviews quote still reads the same; only the rule is added.

### R2.3 The rule registry and the standing mutation check

- `ctrl_memory.RULES` is the one list. `Refusal` takes a rule key and looks its check up there.
- The register arm (`test_ctrl_memory.py:830-844`) fails CI when:
  - `SPLIT_CONTROL_MEMORY.md` section 3's table differs from RULES in any row, column or order;
  - a rule has no refusal arm in `refusal_arms`;
  - a rule has no mutant in `MUTANTS`;
  - a mutant names neither a rule nor a listed property.
- A mutant (`mutated`, `:793-811`) rebuilds one function or class from `inspect.getsource` with one literal edit, which must match exactly once; the result must parse to that one definition. It is patched in for its arm (in-process for `banks`, `checks` and `sim`; in the SoC child for `soc`) and must produce at least one FAIL; the first one is printed by name. An edit that no longer matches its source is itself a FAIL.
- The 40 mutants, at `be431eec` (`test_ctrl_memory.step1.log`):

| # | Mutant | Rule or property | Edit (`file:definition`: old to new) | Arm | Killed by (first named FAIL) |
|---:|---|---|---|---|---|
| 1 | elf class weakened | elf class | `sw/litex/ctrl_memory.py:read_elf`: `if data[:6] != b"\x7fELF\x01\x01":` to `if data[:4] != b"\x7fELF":` | checks | an ELF64 file: accepted, expected 'memory map' rule 'elf class' |
| 2 | elf machine off | elf machine | `sw/litex/ctrl_memory.py:read_elf`: `if machine != _EM_RISCV:` to `if False:` | checks | an x86 ELF32 file: accepted, expected 'memory map' rule 'elf machine' |
| 3 | truncated fields read | elf truncated | `sw/litex/ctrl_memory.py:_unpack`: `if offset + struct.calcsize(layout) > len(data):` to `if False:` | checks | an ELF cut inside its header: raised error (unpack_from requires a buffer of at least 52 bytes for unpacking 36 bytes at offset 16 (actual buffer s... |
| 4 | truncated segments read | elf truncated | `sw/litex/ctrl_memory.py:read_elf`: `if offset + filesz > len(data):` to `if False:` | checks | a load segment past the end of the file: accepted, expected 'memory map' rule 'elf truncated' |
| 5 | unterminated names read | elf truncated | `sw/litex/ctrl_memory.py:_string`: `if end < 0:` to `if False:` | checks | a section name past the end of the file: accepted, expected 'memory map' rule 'elf truncated' |
| 6 | load address read as the run address | load address | `sw/litex/ctrl_memory.py:read_elf`: `return paddr + vma - vaddr` to `return vma` | checks | the good image is planned: raised Refusal (memory map: .data's initial bytes load at 0x10000000, outside rom, the only region the bitstream initial... |
| 7 | entry address off | entry address | `sw/litex/ctrl_memory.py:check_map`: `if image.entry != rom.origin:` to `if False:` | checks | an image entering away from the reset address: accepted, expected 'reset entry' rule 'entry address' |
| 8 | entry bytes off | entry bytes | `sw/litex/ctrl_memory.py:check_map`: `if not any(s.loaded and s.vma <= image.entry` to `if False and not any(s.loaded and s.vma <= image.entry` | checks | an image with no initial bytes at the reset address: accepted, expected 'reset entry' rule 'entry bytes' |
| 9 | outside regions off | outside regions | `sw/litex/ctrl_memory.py:check_map`: `if home is None:` to `if False:` | checks | a section outside rom and sram: accepted, expected 'memory map' rule 'outside regions' |
| 10 | loads outside rom off | loads outside rom | `sw/litex/ctrl_memory.py:check_map`: `if s.loaded and not rom.holds(s.lma, s.lma + s.size):` to `if False:` | checks | initial bytes of .data left in sram, which nothing initialises: refused by 'allocation over budget' rule 'budget' (allocation over budget: 65548.5 ... |
| 11 | nobits in rom off | nobits in rom | `sw/litex/ctrl_memory.py:check_map`: `if not s.loaded and home is rom:` to `if False:` | checks | .bss reserved in rom: refused by 'memory map' rule 'writable in rom' (memory map: .bss is writable and runs at 0x00002f44 in rom, which drops write... |
| 12 | writable in rom off | writable in rom | `sw/litex/ctrl_memory.py:check_map`: `if s.writable and home is rom:` to `if False:` | checks | .data linked to run in rom: accepted, expected 'memory map' rule 'writable in rom' |
| 13 | region overlap off | regions | `sw/litex/ctrl_memory.py:check_map`: `_overlap("regions", ` to `0 and _overlap("regions", ` | checks | PLANTED: a memory-map overlap (sram moved into rom): refused by 'memory map' rule 'outside regions' (memory map: .data [0x10000000, 0x10000040) is ... |
| 14 | address overlap off | addresses | `sw/litex/ctrl_memory.py:check_map`: `_overlap("addresses", ` to `0 and _overlap("addresses", ` | checks | PLANTED: a memory-map overlap (.bss over .data): accepted, expected 'memory-map overlap' rule 'addresses' |
| 15 | load-address overlap off | initial bytes | `sw/litex/ctrl_memory.py:check_map`: `_overlap("initial bytes", ` to `0 and _overlap("initial bytes", ` | checks | .data's initial bytes loading over .rodata's: accepted, expected 'memory-map overlap' rule 'initial bytes' |
| 16 | budget off | budget | `sw/litex/ctrl_memory.py:plan`: `if need.tiles > budget:` to `if False:` | checks | PLANTED: an allocation over budget (215,000 bytes of .bss: 58 RAMB36, each region inside its own): accepted, expected 'allocation over budget' rule... |
| 17 | budget refuses exactly 56 | budget | `sw/litex/ctrl_memory.py:plan`: `if need.tiles > budget:` to `if need.tiles >= budget:` | checks | an allocation of exactly 56 RAMB36 is accepted: raised Refusal (allocation over budget: 56 RAMB36 (rom 12068 bytes in 12288, sram 217088 bytes in 2... |
| 18 | budget half a tile slack | budget | `sw/litex/ctrl_memory.py:plan`: `if need.tiles > budget:` to `if need.tiles > budget + 0.5:` | checks | an allocation of 56.5 RAMB36, half a tile over: accepted, expected 'allocation over budget' rule 'budget' |
| 19 | budget 1.5 tiles slack | budget | `sw/litex/ctrl_memory.py:plan`: `if need.tiles > budget:` to `if need.tiles > budget + 1.5:` | checks | an allocation of 56.5 RAMB36, half a tile over: accepted, expected 'allocation over budget' rule 'budget' |
| 20 | stage symbol off | stage symbol | `sw/litex/ctrl_memory.py:check_stage`: `if STAGE_SYMBOL not in image.symbols:` to `if False:` | checks | an image with no nvm_stage: raised KeyError ('nvm_stage'), expected 'staging buffer' rule 'stage symbol' |
| 21 | stage size off | stage size | `sw/litex/ctrl_memory.py:check_stage`: `if size != stage:` to `if False:` | checks | PLANTED: a staging buffer sized for another shape (1x1 image, 8x8 stage): accepted, expected 'staging buffer' rule 'stage size' |
| 22 | stage accepts a larger buffer | stage size | `sw/litex/ctrl_memory.py:check_stage`: `if size != stage:` to `if size < stage:` | checks | PLANTED: a staging buffer sized for another shape (8x8 image, 1x1 stage): accepted, expected 'staging buffer' rule 'stage size' |
| 23 | stage accepts a smaller buffer | stage size | `sw/litex/ctrl_memory.py:check_stage`: `if size != stage:` to `if size > stage:` | checks | PLANTED: a staging buffer sized for another shape (1x1 image, 8x8 stage): accepted, expected 'staging buffer' rule 'stage size' |
| 24 | banks smallest first | bank order | `sw/litex/ctrl_memory.py:banks`: `reversed(range(granules.bit_length()))` to `range(granules.bit_length())` | banks | 840 needs: power-of-two granule banks, largest first, under one granule spare (first wrong: [4097, 4581, 5090]) |
| 25 | cpu origins off | cpu origins | `sw/litex/milan_soc.py:add_ctrl_memory`: `if (soc.cpu.reset_address, soc.mem_map["sram"]) != (ctrl_...` to `if False:` | checks | a CPU resetting away from rom's origin: accepted, expected 'reset entry' rule 'cpu origins' |
| 26 | cpu origins read the reset address only | cpu origins | `sw/litex/milan_soc.py:add_ctrl_memory`: `if (soc.cpu.reset_address, soc.mem_map["sram"]) != (ctrl_...` to `if soc.cpu.reset_address != ctrl_memory.ROM.origin:` | checks | a CPU whose sram is not at sram's origin: accepted, expected 'reset entry' rule 'cpu origins' |
| 27 | rom left uninitialised for the Builder | no BIOS build | `sw/litex/milan_soc.py:add_ctrl_memory`: `soc.integrated_rom_initialized = True` to `soc.integrated_rom_initialized = False` | checks | add_ctrl_memory tells LiteX's Builder that rom holds its contents, so it builds no BIOS |
| 28 | decode one bit short | decode width | `sw/litex/milan_soc.py:CtrlMemory`: `low = (region.size - 1).bit_length() - 2` to `low = (region.size - 1).bit_length() - 3` | sim | rom answers err alone at all 47 addresses from word 0x6e00 to the window's top 0xffff (first wrong: [('0x8000', 'ack'), ('0x8001', 'ack'), ('0x81f1... |
| 29 | hole compares one bit short | hole width | `sw/litex/milan_soc.py:CtrlMemory`: `slaves.append((lambda a: a[:low] >= first, hole))` to `slaves.append((lambda a: a[:low - 1] >= first, hole))` | sim | rom answers err alone at all 47 addresses from word 0x6e00 to the window's top 0xffff (first wrong: [('0x8000', 'none'), ('0x8001', 'none'), ('0x81... |
| 30 | hole starts a word late | hole start | `sw/litex/milan_soc.py:CtrlMemory`: `slaves.append((lambda a: a[:low] >= first, hole))` to `slaves.append((lambda a: a[:low] > first, hole))` | sim | rom answers err alone at all 47 addresses from word 0x6e00 to the window's top 0xffff (first wrong: [('0x6e00', 'none')]) |
| 31 | hole answers nothing | hole answer | `sw/litex/milan_soc.py:CtrlMemory`: `self.sync += hole.err.eq(hole.cyc & hole.stb & ~hole.err)` to `self.sync += hole.err.eq(0)` | sim | rom answers err alone at all 47 addresses from word 0x6e00 to the window's top 0xffff (first wrong: [('0x6e00', 'none'), ('0x6e01', 'none'), ('0x71... |
| 32 | err held a second cycle | err pulse | `sw/litex/milan_soc.py:CtrlMemory`: `hole.err.eq(hole.cyc & hole.stb & ~hole.err)` to `hole.err.eq(hole.cyc & hole.stb)` | sim | rom: a read presented on the cycle after an err acks with its own data ((('err', 0), ('err', 4175417604))) |
| 33 | rom banks from the image start | rom contents | `sw/litex/milan_soc.py:CtrlMemory`: `words[first:first + depth]` to `words[0:depth]` | sim | rom reads its image at the first, second and last word of each of 5 banks (64, 32, 8, 4, 2 KiB) |
| 34 | a writable rom | read-only rom | `sw/litex/milan_soc.py:CtrlMemory`: `read_only=words is not None` to `read_only=False` | sim | a write to rom changes nothing |
| 35 | BIOS ROM built | no BIOS memory | `sw/litex/milan_soc.py:MilanSoC`: `kwargs.update(integrated_rom_size=0, integrated_sram_size...` to `kwargs.update(integrated_sram_size=0)` | soc | SoC build: the 8x8 stage in the 1x1 build is refused by rule 'stage size' before any Verilog is written (rc 1: AssertionError: ) |
| 36 | BIOS SRAM built | no BIOS memory | `sw/litex/milan_soc.py:MilanSoC`: `kwargs.update(integrated_rom_size=0, integrated_sram_size...` to `kwargs.update(integrated_rom_size=0)` | soc | SoC build: the 8x8 stage in the 1x1 build is refused by rule 'stage size' before any Verilog is written (rc 1: AssertionError: ) |
| 37 | control memory not added | memory hookup | `sw/litex/milan_soc.py:MilanSoC`: `add_ctrl_memory(self, Path(ctrl_firmware))` to `None` | soc | SoC build: an allocation over budget is refused by rule 'budget' before any Verilog is written (rc 1: AttributeError: 'MilanSoC' object has no attr... |
| 38 | main() staging check removed | stage in main | `sw/litex/milan_soc.py:main`: `ctrl_memory.check_stage(soc.ctrl_image,` to `(soc.ctrl_image,` | soc | SoC build: the 8x8 stage in the 1x1 build is refused by rule 'stage size' before any Verilog is written (rc 0: None) |
| 39 | flag pairing off | pairing | `sw/litex/milan_soc.py:main`: `if args.ctrl_mailbox != (args.ctrl_firmware is not None):` to `if False:` | soc | SoC build: --ctrl-mailbox alone is refused, '--ctrl-mailbox and --ctrl-firmware go together' (rc 1: ValueError: --ctrl-mailbox needs --ctrl-firmwar... |
| 40 | shipping firmware linked | no shipping firmware | `sw/litex/milan_soc.py:main`: `if args.software_profile == "baremetal" and not args.ctrl...` to `if args.software_profile == "baremetal":` | soc | the split build adds no shipping firmware |

- The planted defects of the refusal arms, each refused by its own rule (34 lines in the `rules` arm); a refusal by another rule, an unnamed exception, or acceptance is a FAIL:
  entry 0x100 (`entry address`); `.text` at 0x100 (`entry bytes`); a CPU resetting to 0x100, and sram at 0x2000_0000 (`cpu origins`); a text file, an empty file, ELF64, big-endian (`elf class`); x86 (`elf machine`); cut to 40 bytes, cut to half, a segment of 1 MiB past the end, a section name at 2^30 (`elf truncated`); `.bss` at 0x4000_0000 (`outside regions`); `.data` loaded in sram (`loads outside rom`); `.bss` in rom (`nobits in rom`); `.data` running in rom (`writable in rom`); sram moved into rom (`regions`); `.bss` over `.data` (`addresses`); `.data` loaded over `.rodata` (`initial bytes`); 58 RAMB36 and 56.5 RAMB36 (`budget`); no `nvm_stage` (`stage symbol`); 1x1 image against the 8x8 stage and the reverse (`stage size`).
- Accepted: the good image, exactly 56.0 RAMB36 (`BUDGET_BSS` = 208,832 B of `.bss`: rom 12,288 + sram 217,088 = 229,376 B), the shape's own stage, and `add_ctrl_memory` on a `FakeSoC` with the right origins (rom rx and sram rwx as `CtrlMemory`, each 224 KiB, and `integrated_rom_initialized`).

### R2.4 The SoC build test

`soc_arms` (`test_ctrl_memory.py:658-680`), each case one child process (`soc_child`, `:582-610`) running `milan_soc.main()` on `endstation_builder.emit_soc_argv` for `configs/endstation_ax7101_1x1_tdm8.yaml` (after `endstation_builder.build`) plus `--output-dir <tmp> --no-compile-software`, `PYTHONHASHSEED=0`:

| Case | Extra argv | Required |
|---|---|---|
| allocation over budget | `--ctrl-mailbox --ctrl-firmware` an image of 58 RAMB36 | rc 1, rule `budget`, no Verilog |
| memory-map overlap | the same with `.bss` at `.data` | rc 1, rule `addresses`, no Verilog |
| wrong-shape staging | the 8x8 stage (13,264 B) in the 1x1 build | rc 1, rule `stage size`, no Verilog |
| `--ctrl-mailbox` alone | | rc 2, the pairing message, no Verilog |
| `--ctrl-firmware` alone | the good image | rc 2, the pairing message, no Verilog |
| the split build | `--ctrl-mailbox --ctrl-firmware` the good image | rc 0; the export's 32-bit memories are exactly `rom_bank0..` and `sram_bank0..` at the plan's depths, no `rom` or `sram` (the BIOS memories); the rom bank init files concatenate to `rom_words`; `csr.csv` maps rom `0x00000000` and sram `0x10000000`, 229,376 B each; the Builder is handed `integrated_rom_size` 0, `integrated_sram_size` 0 and `integrated_rom_initialized` True, and no `libmilan_baremetal` package or directory |

The child records what LiteX's `Builder.build` is handed and then calls it unchanged. `--no-compile-software` skips only LiteX's software compile; with it the Builder would compile no BIOS anyway, so the BIOS decision is read from the flag the Builder reads. Each case runs in about 3 s here; the six SoC mutants run the whole arm again.

### R2.5 Reviewer mutants and probes re-run

**R607-1's harness** (`review-evidence/640-m8a-r1/reviews/R607-1/scripts/mutants.py` from the `640-m8a-review-evidence` branch at `6609230f`, run unmodified as `mutants.py <this worktree> <out> <LiteX python> --jobs 1` at `be431eec`; one job because every mutant tree shares the builder output through the worktree's `sw/builder/out` link). Receipts: `evidence-r2/r607-mutants/` (`mutants.txt`, one log per mutant).

| Mutant | Round 1 | Round 2 | First named FAIL at `be431eec` |
|---|---|---|---|
| `budget_slack_1p5` | SURVIVED | KILLED (5) | an allocation of 56.5 RAMB36, half a tile over: accepted |
| `budget_ge` | SURVIVED | KILLED (6) | an allocation of exactly 56 RAMB36 is accepted: raised Refusal |
| `nobits_in_rom_off` | SURVIVED | KILLED (2) | .bss reserved in rom: refused by rule 'writable in rom' (expected 'nobits in rom') |
| `lma_overlap_off` | SURVIVED | KILLED (1) | .data's initial bytes loading over .rodata's: accepted |
| `no_bytes_at_entry_off` | SURVIVED | KILLED (2) | an image with no initial bytes at the reset address: accepted |
| `regions_overlap_off` | KILLED | KILLED (1) | sram moved into rom: refused by rule 'outside regions' |
| `lma_identity` | ERROR (crash, no FAIL line) | KILLED (18) | the good image is planned: raised Refusal |
| `stage_lt` | KILLED | KILLED (5) | 8x8 image, 1x1 stage: accepted; also the SoC build exports the 8x8 stage in the 1x1 build |
| `low_minus1` | SURVIVED | KILLED (5) | rom answers err alone ... first wrong `0x8000` ack |
| `hole_gt` | KILLED | KILLED (5) | rom ... first wrong `0x6e00` none |
| `rom_init_offset` | KILLED | KILLED (3) | rom reads its image ...; the rom banks' init files hold the image word for word |
| `err_held` | SURVIVED | KILLED (4) | rom: a read presented on the cycle after an err acks with its own data: `('err', ...)` |

All twelve are KILLED by a named FAIL line from a base arm; the harness's edit also stops one of the test's own mutants matching, which adds a FAIL line of its own.

**R606-1's mutants.** `low_minus_one` and `hole_narrow` are the test's mutants 28 and 29; `main() staging check removed` is mutant 38. All three are killed (table above).

**Probes, re-run at `516d7fb8`** (scripts from the same branch, untouched; receipts in `evidence-r2/probes/`):

| Probe | Round 1 head | This head |
|---|---|---|
| R606-1 `probe_writable_rom.py` (`.data` linked `} > rom`) | ACCEPTED | `REFUSED memory map: ... .data is writable and runs at 0x00000070 in rom, which drops writes` |
| R607-1 `probe_malformed.py` on the largest image | truncated-64, truncated-half: unnamed `struct.error` | all seven inputs `Refusal[memory map]`; 54.5 accepted at budget 54.5, refused at 54.0 |
| R607-1 `probe_ctrlmem_sim.py` on the largest image | PASS | PASS (A-E) |
| R606-1 `probe_region_top.py` | PASS | PASS (115 addresses, 0 non-err, 0 aliased) |

### R2.6 Docs and figures

- 56-tile line: `87.5 - 6.5 + 6 - 18 + 56 + 2 - 11 = 116`, leaving 5.5 below 121.5 (plan `:861-862`, budget `:265`).
- `AREA_BUDGET.md:382-383`: "The ruled firmware limit is up to 56 RAMB36 as mapped. M8a-1's 53 at the largest shape is an out-of-context mapping, not integrated consumption."
- `MARK_II_AREA_PLAN.md:1046`: "reconcile the ruled 56-tile firmware allocation and measured linked storage".
- 231: `ctrl_memory_ooc.tsv` column `LUT` (`PRIMITIVE_GROUP == LUT`) for `s8i2_rom`; `util/s8i2_rom_utilization.rpt` Slice LUTs 220; `s1i2_rom` 36 and `s8i2_sram` 97 LUT cells.
- R607-1-R1: "Every point is within the 56-RAMB36 budget. The largest leaves 3 tiles as mapped; the budget check reads the planned 54.5, so its image can grow 6 KiB (1.5 tiles) before it is refused."

### R2.7 Gate table (round 2)

Heads: `be431eec` (code, test, rule table, idiom inventory), `516d7fb8` (ledger and fit docs only), `76605880` (one prose sentence in `SPLIT_CONTROL_MEMORY.md` section 3, outside the rule table; final). Every gate unpiped, rc recorded; logs in `evidence-r2/`, scratch under the lane's scratch directory.

| # | Gate | Head | rc | Result |
|---:|---|---|---:|---|
| 1 | `sw/litex/test_ctrl_memory.py` (LiteX stack, pinned RV32 SDK) | `be431eec` | 0 | 109 checks, 0 failures, `RESULT: PASS`; all 40 mutants caught; 70 s wall, 0.73 GB peak |
| 2 | `scripts/run_litex_sims.sh --selftest` | `516d7fb8` | 0 | 10 checks PASS |
| 3 | `scripts/run_litex_sims.sh <logs>` (pinned Verilator 5.050 on PATH) | `516d7fb8` | 0 | 7 of 7 PASS, 0 skipped (`test_ctrl_memory` and M2's `test_retained_cdc_storage` among them) |
| 4 | R607-1 `mutants.py` (twelve mutants, unmodified) | `be431eec` | 0 | 12 of 12 KILLED by named FAIL lines (R2.5) |
| 5 | R606-1 `probe_writable_rom.py`, `probe_region_top.py`; R607-1 `probe_malformed.py`, `probe_ctrlmem_sim.py` | `516d7fb8` | 0 each | R2.5 |
| 6 | `ctrl_memory.py plan` under CPython 3.12.3 `-I`, largest image, `--stage-bytes 13264`, then `3344` | `516d7fb8` | 0, then 2 (expected) | 54.5 RAMB36; `REFUSED staging buffer: nvm_stage is 13264 bytes; the requested shape stages 3344` |
| 7 | `ctrl_srp_image.py`, four points, split and flat (`fit_r2.sh`) | `516d7fb8` | 0 (12 runs) | all eight ELFs byte-identical to round 1's (`fit/elf.sha256`); the four plans identical |
| 8 | `syn/ooc/ctrl_memory_ooc.py`, four points (emission only) | `516d7fb8` | 0 | 25 files identical to the inputs round 1 mapped, apart from LiteX's date stamps in the 8 `.v` files: the mapping of section 5 stands without a new Vivado run |
| 9 | Exports without Vivado, base `08b90b68` blobs of `milan_soc.py` and `ctrl_memory.py` swapped in and restored, against head (`exports.sh`) | `516d7fb8` | 0 | default 1x1: 22 files, 0 differ (normalized `alinx_ax7101.v` `82a70c638cdac9a7`); default 8x8: 22, 0 (`9b201e1ea6455fb3`); split 1x1: 24, 0 (`599ff66161596c3f`); split 8x8: 23, 0 (`f2787d47401369ce`); worktree status unchanged |
| 10 | `sw/builder/test_builder.py --require-elaboration --require-rv32` | `516d7fb8` | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11: the calibration's bench build tree is not on this host; the recorded reason, as in round 1) |
| 11 | `syn/yosys/run.sh` | `516d7fb8` | 0 | tops 58, pass 58, fail 0; TAP-PURITY PASS |
| 12 | `check_soc_sources.py` and `--selftest`; `sw/litex/iob_pack_selftest.py` | `516d7fb8` | 0 each | 43 modules, 77 sources; 25 checks; 22 arms, 21 mutants |
| 13 | `check_py_idiom.py` and `--selftest` (CPython 3.12.3); `check_hygiene.py --check` and `--selftest`; `check_todo_ownership.py`; `measure_fail_fast.py --check`; `measure_test_evidence.py --check`; `check_sh_idiom.py` | `76605880` | 0 each | at ratchet (`dynamic eval/exec: 0` with the inventory entry; long function 9 <= 9, long module 10 <= 10, over-long line 0) |
| 14 | `docs_check.py`; `check_em_dash.py --base 08b90b68` and `--selftest`; `gen_toc.py --check`, `--verify-anchors`, `--selftest`; `check_doc_paths.py`; `check_doc_style.py` and `--selftest`; `ci_events.py --check` and `--selftest`; `git diff --check 08b90b68 HEAD` | `76605880` | 0 each | PASS (pinned Markdown renderer) |
| 15 | `scripts/run_all_suites.sh <logs>` (VERILATOR_JOBS=2, -j8, launched with `setsid`) | `76605880` | 0 | 61 of 61 suites, 2,185,848 checks, 0 in-suite failures, 0 timed out; the same 4 declared `tsn_fuzz` skips as round 1 (tsn-gen absent); 06:40 to 08:39 |
| 16 | `sw/litex/test_ctrl_memory.py` | `76605880` | 0 | 109 checks, 0 failures, `RESULT: PASS`; 40 of 40 mutants caught; 72 s wall, 0.73 GB peak |

`be431eec` to `516d7fb8` changes `docs/design/` only, outside the rule table the test reads; `516d7fb8` to `76605880` changes one prose line of section 3. No round-2 commit touches `hdl/`, `tb/`, `syn/` or `protocol-processor`/`gptp-processor`; the suite sweep and Yosys still ran at a round-2 head because the PR head now carries M2's RTL through the dev merge.

### R2.8 Not done, and why

- No Vivado run this round: no mapped figure changed (`CtrlMemory` and the bank plan are unchanged, and the four split ELFs plan identically, R2.7).
- M8a-2 (boot, service checks, route) still waits for F-INT PR 2; primitive mapping and resource figures are round 1's (sections 5 and 6 below).

## Status (round 1)

**REVIEW READY (M8a-1).** Head `5d532e9dcd2bb8d19f8017cc0c2d6e02ec556d14`: four commits on dev `e8454e27`, local, not pushed.

- **Fit:** holds at all four points. As mapped, 34.0 / 37.5 / 47.0 / 53.0 tiles (RAMB36 + RAMB18/2) against the 56-RAMB36 budget, with no power-of-two waste.
- **Ledger:** 124 tiles before the split's conditional release, 113 after; 121.5 is the ceiling and the 13.5 reserve is untouched.
- **Planted controls:** all three fail by name, in the unit test and through the real SoC build.
- **Default:** the all-fabric default is digest-identical for both AX7101 shipping configs.
- **Gates:** every gate the change touches passed (section 11).
- **Open:** M8a-2 (boot, service checks, route) waits for F-INT PR 2.

## Contents

1. Scope of this round
2. Changes, with file:line
3. Memory map and instantiation
4. Linked spans at the four points
5. Primitive mapping, before and after
6. Ledger rows, measured
7. Planted controls, and the defect each test catches
8. Boot console and diagnostics; DDR3 at this base
9. All-fabric default: digest-identical
10. All-fabric image without DDR3 (measurement only)
11. Gate table
12. Not in this round, and open risks
13. Reproduction

## 1. Scope of this round

From the ruling (6101485877):

- the owner's 224 KB binds: up to 56 RAMB36 as mapped; the ledger takes the split's conditional release (-11 tiles) and stays at or under 121.5 with the 13.5 reserve untouched;
- no power-of-two waste; the four points at or near their floor; RAMB36 and RAMB18 reported as mapped;
- the firmware owns the reset entry in the split placement; no BIOS ROM or SRAM there; the all-fabric image keeps its BIOS;
- M8a-1 is the memory map and instantiation behind `--ctrl-mailbox`, the fit proof, the linked spans, the ledger rows, the three planted controls and the default digest-identical;
- M8a-2, after F-INT PR 2: the split-image simulation boot, `check_nvm_capture.py` 8x8, `nvm_cosim`, `nvm_capture_cpu` and the integrated route through the M0s recipe.

## 2. Changes, with file:line

Commits (one-line, no trailers):

- `c20ed894a3b577407588e30ff365480a7e7be26a` Build the split placement's firmware ROM and RAM from the linked image behind --ctrl-mailbox, in power-of-two banks with no BIOS (#640 M8a-1)
- `94190c36501cce6082b9fa93c916a8ecbaca0455` Give the split memory plan's and test's nested helpers the docstrings the Python idiom gate requires
- `a475ab5ab4e3eb75a1ab79f913cf9f6893f42d2b` Document the split placement's control memory and record M8a-1's measured firmware block RAM ledger rows (#640)
- `5d532e9dcd2bb8d19f8017cc0c2d6e02ec556d14` State the split ROM mapping default without process language, as the docs wording gate requires

18 files, +1,270 / -55.

| File:line | Change |
|---|---|
| `sw/litex/ctrl_memory.py:44-89` | New. The contract: 4,096 B per RAMB36, the 2,048 B RAMB18 granule, the 56-RAMB36 budget, `rom` at `0x0000_0000` and `sram` at `0x1000_0000`, each 224 KiB |
| `sw/litex/ctrl_memory.py:139` | `banks()`: the need in granules, its binary digits as banks, largest first |
| `sw/litex/ctrl_memory.py:151` | `read_elf()`: entry, allocated sections (address, load address, loaded or NOBITS), symbols, load segments of an RV32 ELF |
| `sw/litex/ctrl_memory.py:197` | `check_map()`: `reset entry`, `memory map` and `memory-map overlap` (sections, load addresses, regions) |
| `sw/litex/ctrl_memory.py:219` | `plan()`: the needs and banks; `allocation over budget` above 56 RAMB36 |
| `sw/litex/ctrl_memory.py:236` | `rom_words()`: the initial contents of `rom` |
| `sw/litex/ctrl_memory.py:245` | `stage_bytes()`: the shape's KLJ2 container (scripts' `inventory` and `klj2_assemble`) plus one record header, as `nvm_shape.h` derives `NVM_STAGE_BYTES` |
| `sw/litex/ctrl_memory.py:263` | `check_stage()`: `staging buffer` |
| `sw/litex/ctrl_memory.py:273, 281` | `regions_ld()` for the link; the CLI (`regions`, `plan`) |
| `sw/litex/milan_soc.py:44` | `import ctrl_memory` |
| `sw/litex/milan_soc.py:2578` | `CtrlMemory`: one region as banks of LiteX `wishbone.SRAM` behind a `wishbone.Decoder`; past the last bank, `err` at once |
| `sw/litex/milan_soc.py:2608` | `add_ctrl_memory()`: checks the CPU's reset address and `sram` origin, plans the image, adds `rom` (read-only, initialised) and `sram`, sets LiteX's `integrated_rom_initialized` so no BIOS is built |
| `sw/litex/milan_soc.py:2674, 2777-2781, 2808-2809` | `ctrl_firmware` parameter; under `ctrl_mailbox` no BIOS ROM or SRAM (`integrated_rom_size=0`, `integrated_sram_size=0`), then `add_ctrl_memory` right after `SoCCore.__init__` |
| `sw/litex/milan_soc.py:3683` | `--ctrl-firmware` |
| `sw/litex/milan_soc.py:3887` | `--ctrl-mailbox` and `--ctrl-firmware` refused apart |
| `sw/litex/milan_soc.py:4027` | passed to `MilanSoC` |
| `sw/litex/milan_soc.py:4066` | the split build adds no `libmilan_baremetal` (no BIOS to link into) |
| `sw/litex/milan_soc.py:4188` | the split build's staging check, before any export |
| `sw/firmware/ctrl/plat/ctrl_split.ld` | New. The split link: reset entry first in `rom`, `.data` in `sram` loaded from `rom`, `.bss`, 8 KiB stack |
| `sw/firmware/ctrl/plat/ctrl_split_start.S` | New. The reset entry: stack, `.data` copy, `.bss` clear, `main` |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:66, 92, 180` | `link()` extracted; `--layout split` links with the split script and reports the bank plan; the flat layout is unchanged (same four spans) |
| `sw/litex/test_ctrl_memory.py` | New. 33 checks (section 7) |
| `syn/ooc/ctrl_memory_ooc.py` | New. Emits both regions of each image as `CtrlMemory` builds them, and the OOC Vivado script |
| `scripts/run_litex_sims.sh:101` | `test_ctrl_memory` in the pinned inventory |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | New. The split placement's memory contract, refusals, boot and diagnostics, fit |
| `docs/design/MARK_II_AREA_PLAN.md`, `docs/design/AREA_BUDGET.md` | Ledger rows measured (section 6) |
| `docs/testing/TESTING.md`, `docs/testing/CI_WORKFLOWS.md`, `docs/design/MAILBOX_SPLIT.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/litex/LITEX_SOC.md`, `docs/README.md`, `sw/firmware/ctrl/README.md` | Cross-references |

## 3. Memory map and instantiation

| Region | Origin | Size | Holds | Built from |
|---|---|---:|---|---|
| `rom` | `0x0000_0000` (CPU reset address) | 224 KiB | reset entry, `.text`, `.rodata`, initial bytes of `.data` | banks of `wishbone.SRAM`, read-only, initialised from the ELF |
| `sram` | `0x1000_0000` | 224 KiB | `.data`, `.bss`, 8 KiB stack | banks of `wishbone.SRAM`, writable, uninitialised |

- Each region spans the whole budget, so the CPU netlist does not depend on the image: both split exports elaborate the same `VexiiRiscvLitex_dd10544c3ff1037f8a13f4ce3a3dd432`.
- Banks: the need rounded up to 2,048 B granules; the granule count's binary digits, largest first; each bank aligned to its own size; the decode compares high address bits (`slave_sel[0] = adr[15:14] == 0`, ... in the export).
- Past the last bank the region answers `err` in one cycle and writes nothing.
- Split vs base `--ctrl-mailbox` export (1x1): `csr.csv` differs only in `memory_region,rom` (131,072 to 229,376) and `memory_region,sram` (8,192 to 229,376). No CSR, CSR bank, interrupt or constant changes. `soc.h` identical except its timestamp; `mem.h` differs in `ROM_SIZE`/`SRAM_SIZE`.
- Split exports: `software/bios/` is empty (no `bios.bin`); the gateware carries `rom_bank0..4.init` (1x1) / `rom_bank0..3.init` (8x8) and the identifier's `mem.init`; no `sram.init`.

## 4. Linked spans at the four points

Linked at the lane head by `ctrl_srp_image.py --with-aecp --layout split` (pinned RV32 SDK `riscv32-ilp32d--glibc--stable-2025.08-1`, `-DNDEBUG`, `--gc-sections`, 8,192 B stack). Bytes:

| Point | .text | .rodata | .data | .bss | stack | `rom` need | `sram` need | Sum | Flat span (unchanged) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 83,020 | 11,950 | 56 | 37,252 | 8,192 | 95,032 | 45,520 | 140,552 | 140,400 |
| 1x1, two interfaces | 84,308 | 11,950 | 56 | 48,620 | 8,192 | 96,320 | 56,880 | 153,200 | 153,056 |
| 8x8, one interface | 83,068 | 25,158 | 448 | 77,428 | 8,192 | 108,680 | 86,080 | 194,760 | 194,224 |
| 8x8, two interfaces (largest) | 84,444 | 25,158 | 448 | 103,556 | 8,192 | 110,056 | 112,208 | 222,264 | 221,728 |

- The split need exceeds the flat span by the reset entry (88 B of `.text`), the second copy of `.data` (56 / 448 B) and alignment (8 / 0 B).
- Inside the spans: descriptor image `aecp_entity_image` 7,512 / 19,520 B (rodata); `nvm_stage` 3,344 / 13,264 B (bss), equal to `ctrl_memory.stage_bytes` for the shape; lwSRP pool `image_arena` 9,920 / 19,840 / 24,032 / 48,064 B (bss), counted once.
- The largest point uses 222,264 of 229,376 bytes (224 KiB), and its banks 54.5 of 56 RAMB36: 1.5 RAMB36 (6 KiB) of headroom.

## 5. Primitive mapping, before and after

**After** (out of context, `syn/ooc/ctrl_memory_ooc.py`, Vivado 2026.1, `xc7a100t-fgg484-2`, `-mode out_of_context -directive AreaOptimized_high`, `Synth 8-4445` promoted to an error, every ROM `$readmem` read successfully; Vivado rc 0, run 2026-10-11 03:28 to its release under the exclusive lock). Per region:

| Top | Banks, bytes | Planned RAMB36 / RAMB18 | As mapped RAMB36 / RAMB18 | LUT | FF | LUTRAM |
|---|---|---:|---:|---:|---:|---:|
| `s1i1_rom` | 64K+16K+8K+4K+2K | 23 / 1 | 22 / 1 | 120 | 27 | 0 |
| `s1i1_sram` | 32K+8K+4K+2K | 11 / 1 | 11 / 1 | 92 | 5 | 0 |
| `s1i2_rom` | 64K+32K | 24 / 0 | 23 / 1 | 36 | 3 | 0 |
| `s1i2_sram` | 32K+16K+8K | 14 / 0 | 14 / 0 | 53 | 4 | 0 |
| `s8i1_rom` | 64K+32K+8K+4K | 27 / 0 | 25 / 1 | 217 | 28 | 0 |
| `s8i1_sram` | 64K+16K+4K+2K | 21 / 1 | 21 / 1 | 90 | 5 | 0 |
| `s8i2_rom` | 64K+32K+8K+4K | 27 / 0 | 25 / 1 | 231 | 34 | 0 |
| `s8i2_sram` | 64K+32K+8K+4K+2K | 27 / 1 | 27 / 1 | 97 | 6 | 0 |

Per point:

| Point | Linked need, B | Allocated bytes (banks) | Used | Planned tiles | As mapped RAMB36 / RAMB18 | As mapped tiles | LUT / FF | Byte floor (flat span / 4,096, up) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, one interface | 140,552 | 143,360 | 98.0% | 35.0 | 33 / 2 | **34.0** | 212 / 32 | 35 |
| 1x1, two interfaces | 153,200 | 155,648 | 98.4% | 38.0 | 37 / 1 | **37.5** | 89 / 7 | 38 |
| 8x8, one interface | 194,760 | 198,656 | 98.0% | 48.5 | 46 / 2 | **47.0** | 307 / 33 | 48 |
| 8x8, two interfaces | 222,264 | 223,232 | 99.6% | 54.5 | 52 / 2 | **53.0** | 328 / 40 | 55 |

- `sram` maps exactly as planned. Its LUTs are the bank decode and the read multiplexer.
- `rom` maps below plan for two reasons. Vivado trims a bit column constant across a bank (`16384x31` becomes 15 RAMB36 and one RAMB18). It also maps a small or sparse bank into logic: the 512-word bank at s1i1 (77 LUT6) and the 1,024-word bank at s8i1/s8i2, absent from the block-RAM mapping report (`util/*.rpt`, `map.vivado.log`).
- Most ROM LUTs come from that bank: 231 at the largest point. LiteX's memory emitter writes no `ROM_STYLE`, so this round reports Vivado's default. Forcing block RAM would cost at most the planned-minus-mapped difference, 1.0 / 0.5 / 1.5 / 1.5 tiles, and save most of those LUTs; M8a-2's route weighs it.

**Before:**

| Configuration | RAMB36 | RAMB18 | Source |
|---|---:|---:|---|
| All-fabric (and base `--ctrl-mailbox`) BIOS ROM, 13,279 x 32 | 16 | 0 | route census at `e8454e27` (round 1) |
| BIOS SRAM, 2,048 x 32 | 2 | 0 | same |
| Identifier memory (stays in both placements) | 0 | 1 | same |
| One LiteX `wishbone.SRAM` of the largest image's whole span (221,728 B) | 64 | 0 | round 1 OOC mapping |
| ROM + RAM, one `wishbone.SRAM` each, largest image | 64 | 0 | round 1 OOC mapping |

In the split, the BIOS ROM and SRAM are not built (-18 RAMB36), and the firmware takes 52 RAMB36 + 2 RAMB18 at the largest point.

## 6. Ledger rows, measured

Recorded in `docs/design/MARK_II_AREA_PLAN.md` (Firmware and block RAM ledger) and mirrored in `docs/design/AREA_BUDGET.md`:

| Item | RAMB36 delta | RAMB18 delta | Tile delta | Image tiles after |
|---|---:|---:|---:|---:|
| Recorded route at `a5ca6e51` | 74 | 27 | 87.5 | 87.5 |
| L2 credited removals: AECP and SRP storage | -6 | -1 | -6.5 | 81 |
| Measured mailbox replacement | +1 | +10 | +6 | 87 |
| M8a-1: BIOS ROM and SRAM not built in the split, measured at `e8454e27` | -18 | 0 | -18 | 69 |
| M8a-1: firmware allocation as mapped, 8x8 with two interfaces | +52 | +2 | +53 | 122 |
| M2 maximum additional allocation | +2 | 0 | +2 | 124 |
| Conditional release of remaining wrapper storage, split only | -10 | -2 | -11 | 113 |

- `87.5 - 6.5 + 6 - 18 + 53 + 2 = 124`; after the release, 113: 8.5 below 121.5, reserve untouched.
- With every bank in block RAM (the plan bound 54.5): 125.5 and 114.5.
- At the shipping 1x1 with one interface (34.0): 105 and 94.
- The census's extra RAMB18 is the 49-byte identifier memory, which stays; the estimate row's -18.5 becomes -18.
- Keeping the BIOS memories would add 18: 142 and 131.

## 7. Planted controls, and the defect each test catches

**The three controls the assignment names, through the real SoC build** (`milan_soc.py` shipping export plus `--ctrl-mailbox --ctrl-firmware`, each refused before any export; logs in `evidence-m81/`):

| Control | Plant | Result |
|---|---|---|
| Allocation over budget | the 8x8 two-interface image linked from a scratch copy of the control tree whose `ctrl_split.ld` reserves a 16 KiB stack | rc 1, `allocation over budget: 56.5 RAMB36 (rom 110056 bytes in 110592, sram 120400 bytes in 120832) exceeds the 56-RAMB36 budget`; the fixture refuses the same image with the same words (rc 2) |
| Memory-map overlap | the 1x1 image linked from a copy whose `ctrl_split.ld` places `.bss` at `ADDR(.data)`; GNU ld accepts it | rc 1, `memory-map overlap: .bss at 0x10000000 lies inside .data [0x10000000, 0x10000038) (addresses)` |
| Staging buffer for another shape | the good 1x1 one-interface image in an 8x8 build | rc 1, `staging buffer: nvm_stage is 3344 bytes; the endstation_ax7101_8x8 shape stages 13264` |

Also refused (rc 2, by argparse): `--ctrl-mailbox` without `--ctrl-firmware`, and `--ctrl-firmware` without `--ctrl-mailbox`.

**`sw/litex/test_ctrl_memory.py`** (33 checks, RESULT: PASS; in `scripts/run_litex_sims.sh`):

| Arm | What it checks | Planted defect it catches |
|---|---|---|
| banks | 840 needs up to past the budget against an independent oracle (ceil(need/2,048) and its binary digits); zero need; RAMB18 counted half | any bank rounding or ordering change (the `banks smallest first` mutant turns 4 checks red) |
| checks | an ELF written by an independent writer: needs, `rom` contents at their load addresses, stage accepted | `the map check off` (5 red), `the budget check off` (1 red), `the staging check off` (2 red) |
| controls | over budget (215,000 B of .bss, 58 RAMB36, each region inside its own); overlap (.bss over .data; `sram` moved into `rom`); staging both ways (1x1 image vs 8x8 stage, 8x8 image vs 1x1 stage); entry at 0x100; .data's initial bytes in `sram`; a section at `0x4000_0000` | each must be refused by its named check |
| simulation | the real `milan_soc.CtrlMemory` in migen: `rom` reads its image at the first, second and last word of each of 3 banks; a write to `rom` changes nothing; `sram` byte lanes at every bank edge; past the last bank `err` at once in both regions; a hole write lands in no bank (each bank's aliasing cell read back) | `banks smallest first` (misaligned decode), `the hole answers nothing` (no `err`: 2 red), `a writable rom` (1 red) |
| link | a probe linked by the real `ctrl_split.ld` behind `ctrl_split_start.S` with the pinned SDK: entry 0 is `auipc sp`; `.data` runs in `sram` and its 7 loads from `rom`; the stack tops the `sram` need; `nvm_stage` passes | link-script plants: `.data` without `AT > rom` (refused `memory map`), `ENTRY(main)` (refused `reset entry`) |

Each mutant is a monkeypatch of the code under test for one arm; the arm must report at least one failure.

## 8. Boot console and diagnostics; DDR3 at this base

The split image loses: the LiteX BIOS and its console (banner, memory, flash, SDRAM and boot commands); the BIOS DDR3 initialisation (`sdram_init`); the shipping firmware's UART commands (`libmilan_baremetal` is not linked). It keeps the UART, `timer0`, `ctrl` (reset, scratch, bus errors), the identifier memory, the `ppmem` observer and every Milan CSR. Any console there is the control firmware's (F-INT PR 2). The all-fabric image keeps its BIOS (section 9).

DDR3 stays instantiated under `--ctrl-mailbox` at this base, because `KL_pp_shadow` (unconditional at `hdl/milan/milan_datapath.sv:8003`) and its three processor memory masters still reach the window in `main_ram`. With no BIOS the DFI never makes the 1 to 0 to 1 hand-back that `pp_mem_gate` (`sw/litex/milan_soc.py:2255`) waits for, so those masters stay refused (they answer errors, as before training). Removing DDR3 belongs with the wrapper's removal (F-INT PR 2) and is measured by M8a-2's route.

## 9. All-fabric default: digest-identical

Both AX7101 shipping configs exported (recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, no `--build`) with the base `milan_soc.py` (blob of `e8454e27`, swapped in and restored) and with the head. Normalization, and nothing else: LiteX timestamp lines, the export's own directory, the Verilog banner's Date line and LiteX's comment-only hierarchy tree.

| Config | Files compared | Differ | Normalized SHA-256 of `alinx_ax7101.v` |
|---|---:|---:|---|
| `ax7101` (1x1 TDM8) | 22 | 0 | `40e5304ae1fea35a02e5487f1096ed3c3bc4cdfa0732cd46e5332ce796586602` (base = head) |
| `ax8x8` | 22 | 0 | `fea8757e5546fa793dd76ac08800630fde4383ac8a289313f60b2b571b580e16` (base = head) |

The 22 files include the top `.v`, `.tcl`, `.xdc`, every `.init` (the BIOS ROM image among them), `bios.bin`, `csr.csv`, `csr.json`, the generated headers and `regions.ld`, the AEM image and manifest and `flashboot_layout.json`. Tables: `evidence-m81/digest-ax7101.txt`, `digest-ax8x8.txt`.

## 10. All-fabric image without DDR3 (measurement only)

Unchanged from round 1 (`stop-round/HANDOFF-stop.md` section 6): DDR3 holds only the processor window. Compacted, it is 14,792 B (4 RAMB36) at 1x1 and 46,640 B (12 RAMB36) at 8x8. Dropping DDR3 there would also need a compacted window and its constants, an on-chip memory on the CPU's DMA bus for the three processor masters, the removal of LiteDRAM, the PHY, `pp_mem_gate`'s DFI hold and the BIOS SDRAM init, and a pinned `spiflash` CSR location. Not done; the default flip decides it.

## 11. Gate table

Heads: `c20ed894` (first commit), `94190c36` (docstrings), `a475ab5a` (docs), `5d532e9d` (final, one doc line). Every gate unpiped, rc recorded (`evidence-m81/gates-*`).

| # | Gate | Head | rc | Result |
|---:|---|---|---:|---|
| 1 | `sw/litex/test_ctrl_memory.py` | `a475ab5a` | 0 | 33 checks, RESULT: PASS (link arm with the pinned SDK) |
| 2 | `scripts/run_litex_sims.sh --selftest` | `a475ab5a` | 0 | PASS |
| 3 | `scripts/run_litex_sims.sh <logs>` (pinned Verilator 5.050 on PATH) | `a475ab5a` | 0 | 6 of 6 PASS, 0 skipped |
| 4 | `ctrl_memory.py plan` on CPython 3.12.3 (largest image, `--stage-bytes 13264`) | `a475ab5a` | 0 | 54.5 planned |
| 5 | `check_py_idiom.py` and `--selftest` (CPython 3.12.3) | `a475ab5a` | 0, 0 | at ratchet (`c20ed894` was rc 1: two nested helpers without docstrings; fixed in `94190c36`) |
| 6 | `check_hygiene.py --check` and `--selftest`; `check_todo_ownership.py`; `measure_fail_fast.py --check`; `measure_test_evidence.py --check` | `a475ab5a` | 0 each | PASS |
| 7 | `docs_check.py`; `check_em_dash.py --base e8454e27`; `gen_toc.py --verify-anchors`, `--check`; `check_doc_paths.py`; `check_doc_style.py`; `ci_events.py --check` | `5d532e9d` | 0 each | PASS (`a475ab5a`: `docs_check.py` rc 1, process wording, fixed in `5d532e9d`) |
| 8 | `gen_toc.py --selftest`; `check_doc_style.py --selftest`; `ci_events.py --selftest` | `a475ab5a` | 0 each | PASS |
| 9 | `sw/builder/test_builder.py --require-elaboration --require-rv32` | `c20ed894` and `a475ab5a` (the tree reached `5d532e9d`, one doc line, during the run) | 0, 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the bench build tree for its calibration is not on this host; recorded reason) |
| 10 | `check_soc_sources.py` and `--selftest`; `sw/litex/iob_pack_selftest.py` | `c20ed894` | 0 each | PASS |
| 11 | `check_sweep_shape.py --self-test`; `check_deploy_shape.py --self-test`; `check_entity_shape.py --self-test` | `c20ed894` | 0 each | PASS |
| 12 | `syn/ooc`: `dp_srcs.py --selftest`, `ooc_tcl_selftest.py`, `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py`, `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py`, `pp_resource_gate.py check-baseline` | `c20ed894` | 0 | PASS |
| 13 | `ctrl_image_selftest.py --require-rv32` | `c20ed894` | 0 | 33 checks PASS |
| 14 | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | `c20ed894` | 0 | `test_ctrl_firmware: PASS` |
| 15 | `scripts/run_all_suites.sh <logs>` (VERILATOR_JOBS=2, -j8) | `94190c36` | 0 | 61 of 61 suites, 2,185,848 checks, 0 failures; 4 declared `tsn_fuzz` skips (tsn-gen absent). Two earlier attempts (rc 2) aborted in the preflight's hard-HUP control because they ran under `nohup`; relaunched with `setsid` only |
| 16 | `syn/yosys/run.sh` | `94190c36` | 0 | 58 of 58 tops PASS; TAP-PURITY PASS |
| 17 | Fixture, four points, split and flat (`fit_final.sh`) | `94190c36` | 0 (12 runs) | flat spans unchanged; split ELFs byte-identical to the mapped ones |
| 18 | Default exports, base vs head, both AX7101 configs (section 9) | head `milan_soc.py` = `c20ed894` blob | 0 | 22 files each, 0 differ |
| 19 | Split exports, both configs (`--ctrl-mailbox --ctrl-firmware`) | same | 0 | elaborate; no BIOS; one CPU netlist |
| 20 | Planted controls through the SoC build (section 7) | same | 1 (expected) | each refused by name |
| 21 | OOC mapping (Vivado, exclusive lock) | images of `94190c36` | 0 | section 5 |

The diff from `94190c36` to `5d532e9d` touches documentation only (`docs/`, `sw/firmware/ctrl/README.md`), which neither the suites, Yosys nor the fixture read. The diff from `c20ed894` to `94190c36` adds two docstrings.

## 12. Not in this round, and open risks

- M8a-2: the split-image simulation boot to the control application's ready state, the service checks and the integrated route (LUT, FF, RAMB deltas against M0s's split figure, WNS) wait for F-INT PR 2.
- The image linked here is the size fixture in the split layout. Its reset entry is exercised by the linked probe's layout checks, not by a CPU simulation.
- The bank decode and its data multiplexer sit on the CPU's bus path; their timing is measured only by M8a-2's route.
- Headroom at the largest point is 1.5 RAMB36 (6 KiB) under 56. Growth beyond that is refused by name.
- The split build needs its own VexiiRiscv netlist (`VexiiRiscvLitex_dd10544c3ff1037f8a13f4ce3a3dd432`), generated once for both shapes.
- DDR3 under `--ctrl-mailbox` at this base is instantiated and untrained (section 8).
- Worktree leftovers, none committed: the export recipe's three scratch symlinks (`sw/builder/out`, untracked; `configs/generated/ltn_rom.hex` and `ucode.hex`, ignored) point into the scratch work directory, and the gates' ignored build outputs (`tb/verilator/*/obj_*`, `__pycache__`, `.run_all_suites.lock`) remain. Removing them was declined by the session's permissions; `git status` shows only `?? sw/builder/out`.

## 13. Reproduction

Environment: the pinned RV32 SDK (`scripts/ci_rv32_sdk.py --verify-only`), the LiteX stack of `sw/litex/litex_pins.txt` with `sw/litex/patches/`, Vivado 2026.1, PyYAML on the host Python. Runtime archives as in round 1 (`stop-round/HANDOFF-stop.md` section 8).

```sh
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --output "$OUT" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/ctrl_app.elf" --stage-bytes 13264
python3 syn/ooc/ctrl_memory_ooc.py "$MAP" s8i2="$OUT/ctrl_app.elf"
cd "$MAP"
vivado -mode batch -nojournal -source ctrl_memory_ooc.tcl
python3 sw/litex/test_ctrl_memory.py
```

Default digest proof: the recipe in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (export without `--build`), once with `e8454e27`'s `sw/litex/milan_soc.py` and once with the head's, compared by `evidence-m81/digest.py`. Split export: the same argv plus `--ctrl-mailbox --ctrl-firmware <elf>` (`evidence-m81/split-*-argv.json`). Scripts used: `evidence-m81/export.py`, `fit_final.sh`, `run_map.sh`, `gates_*.sh`.

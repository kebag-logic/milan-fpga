[R607] NEGATIVE - exact head 08b90b6859b0a7d7f172c7ae29745248895d9aa9

# R607-1: external review of PR #721 (issue #640, Mark II lane M8a-1, plan L11a)

- Reviewer: [R607], external, cleared context. Round R607-1.
- Head: `08b90b6859b0a7d7f172c7ae29745248895d9aa9`, tree `35e198ffb5808ce77515e649cf752f4d73a6fed8`.
  That is the executor's head `5d532e9d` plus the manager's merge of dev `ac2c5e77` (M2, PR #710).
- Scope: the issue's frozen M8a-1 step under ruling 6101485877.
  That covers the map and instantiation behind `--ctrl-mailbox`, the fit at four points, the measured ledger rows, three planted controls and a digest-identical all-fabric default.
  M8a-2 (boot, service checks, route) is out of scope.
- Sources read: AGENTS.md, CONTRIBUTING.md sections 3, 5 and 6, docs/README.md, and the issue #640 body.
  Also the assignment 6100371426, the STOP 6101473717, the ruling 6101485877 and REVIEW READY 6104411638.
  Also the PR #721 body, the diff `e8454e27..08b90b68` and the lane diff `ac2c5e77..08b90b68`, the history, and the public evidence tree `f8cf8503:review-evidence/640-m8a-r1` (author receipts under `evidence-m81/`).
- Prior public review findings on this PR: none. At the end of my pass the PR held only the two manager "REVIEW STARTED" notices, so there is nothing to resolve or retain. The concurrent internal round was not read.

Verdict: **NEGATIVE**. Two MINOR findings are open: F1 (Tests) and F2 (Docs). A third MINOR, F3, is against the PR body at this head. Conformance, RTL and Robustness are covered clean. The product code is correct at every point I probed, including where the lane's own test cannot detect a defect.

## Findings

### R607-1-F1 - MINOR - Tests

`sw/litex/test_ctrl_memory.py:183`, `:271`, `:276`, `:287`, `:295` against `sw/litex/ctrl_memory.py:203`, `:213`, `:216`, `:228` and `sw/litex/milan_soc.py:2724`, `:2735`. **The lane test cannot fail for five defects inside the contract it and the docs claim to grade.**

- Authority/evidence:
  - AGENTS.md section 6, Tests lens: "Each new test can fail for the defect it claims to detect", plus positive, negative and boundary coverage.
  - The test's docstring (item 3) claims "an address past the last bank answers err in either region and writes no bank".
  - `docs/design/SPLIT_CONTROL_MEMORY.md:66-72` lists every refusal rule. `docs/testing/TESTING.md` says the test grades "its named refusals".
  - Twelve single-edit mutants ran in scratch copies (`scripts/mutants.py`, `receipts/mutants.head.txt`, `receipts/mutants/*.log`). Five stay `RESULT: PASS`:
    - `budget_slack_1p5`: `need.tiles > budget` becomes `> budget + 1.5`, so the owner's binding 56 RAMB36 becomes 57.5. The only budget arm plants 58 tiles (`:183`).
    - `budget_ge`: `>` becomes `>=`, which refuses exactly 56, though the ruling says "up to 56".
    - `nobits_in_rom_off`, `lma_overlap_off`, `no_bytes_at_entry_off`: removing the NOBITS-in-rom rule (`ctrl_memory.py:213`), the shared-load-address overlap (`:216`) or the no-initial-bytes-at-reset rule (`:203`). These are three of the documented refusals.
    - `low_minus1`: the region decodes one word-address bit short (`milan_soc.py:2724`). Addresses in the upper half of the decoded window then alias banks instead of answering err. The test probes only the first word past the last bank (`:271`, `:276`), on a 14 KiB bank set.
    - `err_held`: the hole holds err for a second cycle (`milan_soc.py:2735`). The next bank access then completes with a stale err. No arm issues an access straight after an err.
  - `lma_identity`, `regions_overlap_off`, `stage_lt`, `hole_gt` and `rom_init_offset` are killed.
  - The head code itself is correct:
    - An independent migen probe of the real `CtrlMemory` at the largest image's banks passes (`scripts/probe_ctrlmem_sim.py`, `receipts/probe_ctrlmem_sim.s8i2.log`). It samples 29 addresses per region past the last bank up to word `0xFFFF`, including 224-256 KiB, and runs back-to-back accesses after err.
    - The same probe fails `low_minus1` (20 of 29 addresses ack), `err_held` (stale err on the next access) and `hole_gt` (`receipts/probe_ctrlmem_sim.mutant-*.log`).
    - The budget is accepted at exactly the plan's tiles and refused 0.5 below (`receipts/probe_malformed.txt`).
- Impact: a regression that breaks the binding budget boundary, three documented refusals, the aliasing guarantee or the single-cycle err ships green. The aggregate and hosted `elaborate` job would report PASS.
- Required outcome:
  - The test pins the budget boundary: 56.0 is accepted and 56.5 is refused.
  - Each documented refusal rule has an arm that fails when the rule is removed.
  - The simulation covers addresses across the whole decoded window, beyond 224 KiB, at a bank set with a 64 KiB bank.
  - An access issued straight after an err must ack with its own data.
- Verification: rerun `scripts/mutants.py <tree> <out> <litex-python>`. All twelve mutants must be KILLED by a named FAIL line.

### R607-1-F2 - MINOR - Docs

`docs/design/MARK_II_AREA_PLAN.md:861-862`, `docs/design/AREA_BUDGET.md:265`, `docs/design/AREA_BUDGET.md:382`. **Ledger statements that depend on the rows this PR changed still carry the old arithmetic and the old budget.**

- Authority/evidence:
  - The PR replaces the estimated reuse row (-18.5) with the measured -18 and binds the firmware at "up to 56 RAMB36" (ruling 6101485877).
  - The unchanged sentences "At 56 firmware tiles, the conditional total becomes 115.5 tiles. It leaves six below the ceiling" (plan) and "At 56 firmware tiles, the conditional total is 115.5, leaving six." (budget) still use -18.5.
  - With the PR's own rows: `87.5 - 6.5 + 6 - 18 + 56 + 2 - 11 = 116`, which leaves 5.5 below 121.5.
  - `AREA_BUDGET.md:382`, "About 50 firmware tiles remains a budget, not measured consumption.", contradicts the ruling's 56-tile limit and the PR's measured 53 (`AREA_BUDGET.md:228`).
- Impact: the authoritative ledger gives two different capacity figures for the same 56-tile case. A later lane that budgets the remaining allowance from the 56-tile sentence over-credits half a tile.
- Required outcome: both 56-tile sentences give 116 tiles and 5.5 below the ceiling. Line 382 states the ruled limit (up to 56 RAMB36 as mapped) and that M8a-1's 53 is out of context, not integrated.
- Verification: the arithmetic in both files reproduces from the ledger table rows, and `docs_check.py`, `check_em_dash.py` and `gen_toc.py --check` stay green.

### R607-1-F3 - MINOR - Docs

PR #721 body, "Status" and "How to validate / Expected result". **The PR body describes the pre-merge head and the pre-merge aggregate count.**

- Authority/evidence:
  - The body says "REVIEW READY for M8a-1, head `5d532e9d...` (four commits on `dev` `e8454e27`)". Its expected result is "the aggregate passes 6 of 6".
  - The PR head is the merge `08b90b68`, which brings in M2's `test_retained_cdc_storage`. The aggregate now has seven members.
  - The hosted `elaborate` job at this head reports `simulations: 7 passed: 7` (`receipts/hosted-elaborate-litex-aggregate.txt`).
  - The body does not name the dev merge or its mechanical composition. I verified that composition: only `TESTING.md` conflicted, and `milan_soc.py` and `run_litex_sims.sh` are the plain merge result.
- Impact: a cold reviewer following the body expects 6 of 6 and gets 7 of 7, and cannot tell which head the gate table describes.
- Required outcome: the body names `08b90b68` as the reviewed head and the dev merge it carries, and states the aggregate as 7 of 7. The gate table keeps its per-head column.
- Verification: read the body against `git log -1 --format=%P 08b90b68` and the hosted aggregate line.

### R607-1-R1 - RESIDUE - Docs

`docs/design/SPLIT_CONTROL_MEMORY.md:121`. "the largest leaves 3 tiles" is the as-mapped margin. The budget check reads the planned 54.5, so the image can grow only 6 KiB before refusal. The PR body says 1.5.

Exact fix: "Every point is within the 56-RAMB36 budget. The largest leaves 3 tiles as mapped; the budget check reads the planned 54.5, so its image can grow 6 KiB (1.5 tiles) before it is refused."

### R607-1-R2 - RESIDUE - Docs

`docs/design/SPLIT_CONTROL_MEMORY.md:111` and `:128`, `docs/design/MARK_II_AREA_PLAN.md:821`, and the PR body fit table. The "LUT" figures are LUT primitive cells. The OOC script counts `PRIMITIVE_GROUP == LUT`. The utilization reports' Slice LUTs are 220 + 97 at the largest point, against 231 + 97 in the TSV. The numbers stay; only the unit changes.

Exact fix:
- Column header `LUT / FF` becomes `LUT cells / FF`.
- "most of each point's LUTs: 231 of the largest point's 328" becomes "most of each point's LUT cells: 231 of the largest point's 328".
- "in 231 LUTs" becomes "in 231 LUT cells".

### R607-1-S1 - SUGGESTION - Tests, Robustness

No repeatable gate elaborates `--ctrl-mailbox --ctrl-firmware`. The following are shown only by manual exports:
- `add_ctrl_memory`'s CPU-origin refusal (`milan_soc.py:2742`);
- the `main()` pairing refusal (`milan_soc.py:4019-4021`);
- the no-BIOS builder path;
- the staging check's placement before export.

I reproduced all of them here, but a later edit can break them silently until M8a-2's boot simulation. Consider one elaboration arm in the builder gate or the aggregate.

### R607-1-S2 - SUGGESTION - Robustness

`ctrl_memory.read_elf` raises an unnamed `struct.error` on a truncated ELF (`receipts/probe_malformed.txt`: `truncated-64`, `truncated-half`). Empty, non-ELF, ELF64, big-endian and wrong-machine inputs are refused by name. The build still stops. Wrapping header reads in `Refusal("memory map", ...)` would make "Every refusal names its check" hold for this input too.

### R607-1-S3 - SUGGESTION - Docs (pre-existing, separate Issue)

`SPLIT_CONTROL_MEMORY.md` section 6 and the PR's validate block build the runtime with `ctrl_image_runtime.py`. With the pinned SDK, which defaults to the stack protector, that runtime fails to link: `__umoddi3` needs `__stack_chk_guard`. It builds only with `-fno-stack-protector`, which `ctrl_build.RV32_FLAGS` carries and `ctrl_image_runtime.py` does not. This predates the lane; I reproduced with a compiler wrapper for the runtime only. The firmware link used the pinned SDK unwrapped.

## What was checked (evidence per lens)

### Conformance (clean)

- The ruling's items 1-4 against the head:
  - The binding limit is 56 RAMB36 at 4,096 B (`ctrl_memory.py:47-49`), and the four points fit as planned (35.0 / 38.0 / 48.5 / 54.5).
  - Every region is built from power-of-two RAMB18-granule banks, largest first, with under one granule of waste per region (96.6-99.6 percent full, recomputed).
  - The firmware owns the reset entry: entry `0x0`, `_start` first, and the auipc sp checked in the disassembly (`receipts/s8i2-elf-inspect.txt`).
  - No BIOS ROM or SRAM is built in the split. `software/bios/` is empty and `libmilan_baremetal` is absent (`receipts/split-exports.txt`).
  - The boot console and diagnostics statement holds. The split CSR map keeps `uart`, `timer0`, `ctrl`, `identifier_mem`, `ppmem`, `ctrl_mbx` and `milan_mac` (`receipts/split-csr-bases.txt`).
- Linked spans, reproduced with the pinned SDK (archive sha256 `d42680e9...`, `receipts/sdk-archive.sha256`):
  - All four split ELFs are byte-identical to the author's published hashes (`receipts/elf.r607.sha256` against `evidence-m81/elf.sha256`).
  - The rom/sram needs 95,032/45,520, 96,320/56,880, 108,680/86,080 and 110,056/112,208, the flat spans and the byte floors 35/38/48/55 all equal the PR table (`receipts/fit-table.r607.txt`).
  - The flat layout is byte-identical to live dev (`receipts/flat-*.sha256`).
- Mapped primitives: the author's TSV and the eight utilization reports agree tile for tile (34.0 / 37.5 / 47.0 / 53.0). The ROM trimming explanation fits the counts: a 64 KiB bank maps to 15 RAMB36 + 1 RAMB18; the 512-word bank at s1i1 and the 1,024-word bank at s8i2 go to logic. I did not run Vivado myself (see limits).
- Ledger: `87.5 - 6.5 + 6 - 18 + 53 + 2 = 124`, then 113 after the -11 release. That is 8.5 below 121.5 with the 13.5 reserve untouched, and 125.5 / 114.5 with every bank in block RAM. All recomputed. The stale dependent sentences are F2.
- Planted controls through the real SoC build at head (`receipts/soc-exports-and-controls.txt`). Each is refused by name, with rc 1 and no export directory written:
  - `allocation over budget: 56.5 RAMB36 ...`;
  - `memory-map overlap: .bss at 0x10000000 lies inside .data [0x10000000, 0x10000038)`;
  - `staging buffer: nvm_stage is 3344 bytes; the endstation_ax7101_8x8 shape stages 13264`.
  - `--ctrl-mailbox` alone and `--ctrl-firmware` alone are each refused (rc 2).
- All-fabric default: I exported both AX7101 shipping configs at head and at live dev `ac2c5e77` from launcher dry-runs (`receipts/digest-default-*.txt`, `receipts/digest-default-verilog.txt`).
  - Every gateware artifact matches: Verilog after removing LiteX's comment-only hierarchy tree, Tcl, XDC, ROM/SRAM/mem init and `bios.bin`, plus `csr.csv`, `csr.json`, `soc.h`, `mem.h`, `regions.ld`, `aem_desc.*` and the flashboot layout.
  - The only differing files are compiled software objects whose debug data embeds the export path. `bios.bin` is identical.
- Split CSR map against the dev `--ctrl-mailbox` export: equal except the `rom` and `sram` region sizes (131072/8192 become 229376/229376), at both shapes.

### RTL (clean)

- `milan_soc.py:2710-2737` `CtrlMemory`:
  - `low` = 16 word-address bits covers the SoC region's power-of-two decode (`socbushandler0_shared_adr[29:16]` in the export).
  - Largest-first banks keep each bank's start a multiple of its depth, so `a[s:low] == f >> s` is exact.
  - The hole covers `[first, 2**16)`, including 224-256 KiB.
  - err is a one-cycle answer and does not leak into the next access.
  - Upper address bits are ignored for `sram` at `0x1000_0000`.
  - The independent simulation probe passes A-E (`receipts/probe_ctrlmem_sim.s8i2.log`).
- ROM contents: the exported `alinx_ax7101_rom_bank*.init` files concatenate to the ELF's PT_LOAD image word for word, zero beyond, at both shapes (`scripts/check_rom_init.py`, `receipts/rom-init-*.txt`).
- `ctrl_split.ld` / `ctrl_split_start.S` in the largest image:
  - `.data` LMA `0x1ac28` is word-aligned, `_fbss` is 16-aligned and `_ebss` 4-aligned.
  - `.stack` is a NOBITS section inside the `sram` need.
  - There is no `__global_pointer$` and no orphan section.
  - The copy and clear loops use bounds from the linker symbols (`receipts/s8i2-elf-inspect.txt`).
- Elaborated split Verilog against the dev mailbox export (`receipts/split-vs-mbx-verilog-summary.txt`, `.diff`):
  - removed: only the BIOS ROM and SRAM and their two bus slots;
  - added: only the `CtrlMemory` banks and decoders, plus the CPU instance name.
  - Both split shapes use one VexiiRiscv netlist (`dd10544c...`).
- Merge composition: `git merge-tree 5d532e9d ac2c5e77` conflicts only in `TESTING.md`. The head tree equals that result with both suite paragraphs kept. `milan_soc.py`'s M2 hunks and M8a hunks are disjoint and auto-merged.
- Timing of the two-level bank decode is not measured. This is a declared M8a-2 item and not a finding.

### Robustness (clean)

- Malformed input: empty, non-ELF, ELF64, big-endian and x86 machine inputs are refused by name. A truncated ELF stops with an unnamed error (S2).
- Boundaries: exactly at budget is accepted and 0.5 tile over is refused. A zero need builds no bank.
- Configuration: the default path is byte-for-byte unchanged and the pairing guard works both ways. With no BIOS, `pp_mem_gate` (`milan_soc.py:2387-2411`) needs a 1-0-1 DFI edge that nothing drives, so the processor's memory masters stay gated, as documented.
- Reset: a CPU reset re-runs the `.data` copy and `.bss` clear. `CtrlMemory` holds only the err flag and the SRAM ack registers.

### Tests (UNCLEAN: F1)

- `python3 sw/litex/test_ctrl_memory.py` at head with the RV32 compiler: 33 checks, 0 failures, `RESULT: PASS` (`receipts/test_ctrl_memory.head.log`).
- Hosted `elaborate` at head: aggregate 7/7 with `test_ctrl_memory` PASS, not a skip.
- Mutation campaign: 12 mutants. Seven are killed: `lma_identity` by a crash, the other six by a named FAIL line. Five survive (F1).

### Docs (UNCLEAN: F2, F3)

- Read: `SPLIT_CONTROL_MEMORY.md` (all six sections against code and receipts), the plan and budget ledger diffs, and `MAILBOX_SPLIT.md`, `ARCHITECTURE_HW_SW_SPLIT.md`, `LITEX_SOC.md`, `CI_WORKFLOWS.md`, `TESTING.md`, `docs/README.md` and the `sw/firmware/ctrl/README.md` additions.
- Local gates at head, each rc 0 (`receipts/gates2/`, `receipts/gates-summary.txt`):
  - `docs_check`;
  - `check_em_dash --base ac2c5e77` and `--selftest`;
  - `gen_toc --check` and `--verify-anchors` with the pinned renderer;
  - `check_doc_paths`, `check_doc_style`;
  - `check_py_idiom` under CPython 3.12.3, `check_sh_idiom`;
  - hygiene, TODO and fail-fast ratchets;
  - `check_soc_sources`, `ci_events --check`, `check_feature_status`;
  - `git diff --check`.
- Hosted `docs` at head: success.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling 6101485877 items 1-4. `ctrl_memory.py:41-233`, `milan_soc.py:2706-2757, 2900-2941, 4019-4021, 4196-4201, 4318-4322`. Four reproduced ELFs and plans. Author TSV and eight utilization reports. Ledger rows in both docs. Three SoC-level planted controls and two pairing refusals. Default digest against live dev. Split CSR map. | R607-1 | `08b90b6859b0a7d7f172c7ae29745248895d9aa9` |
| RTL | CLEAN | `milan_soc.py:2710-2737`, the elaborated split `alinx_ax7101.v` at both shapes, ROM bank init files, `ctrl_split.ld`, `ctrl_split_start.S`, the largest ELF's sections and disassembly, the merge-tree composition | R607-1 | `08b90b6859b0a7d7f172c7ae29745248895d9aa9` |
| Robustness | CLEAN | `ctrl_memory.py:151-233` on seven malformed inputs and the budget boundary, `main()` pairing guard, `pp_mem_gate` with no BIOS, the reset entry's re-entry, the default path | R607-1 | `08b90b6859b0a7d7f172c7ae29745248895d9aa9` |
| Tests | UNCLEAN (F1) | `test_ctrl_memory.py` run at head, 12 mutants, independent probe and its own mutant controls, hosted aggregate | R607-1 | `08b90b6859b0a7d7f172c7ae29745248895d9aa9` |
| Docs | UNCLEAN (F2, F3) | the 12 documentation files in the diff, the PR #721 body, 16 local documentation and quality gates | R607-1 | `08b90b6859b0a7d7f172c7ae29745248895d9aa9` |

RESIDUE R1 and R2 do not affect coverage. S1-S3 are optional.

## Real limits

- No Vivado run of mine. The out-of-context primitive counts are the author's. I checked that their inputs are byte-identical to my ELFs, which give identical plans, and that the TSV, reports and plan agree. I did not re-synthesise.
- I did not run the full suite sweep, the Yosys bank or the builder gate: they are outside this review's allowance. No act or hosted runner was used.
- No CPU executes the reset entry; that is M8a-2's boot simulation. The physical bench is NOT RUN, and the skipped hosted context ("Physical gPTP") is not evidence.
- The default-digest comparison normalized only the source and export paths, LiteX's dated header and the comment-only hierarchy tree. Software object files were compared through `bios.bin` and the ROM init.
- The runtime archives were built with a `-fno-stack-protector` compiler wrapper (S3). The firmware link used the pinned SDK compiler unwrapped.

## Pending manager duties

- Hosted acceptance at this head. I read, without writing, `rtl-fast`, `docs`, `elaborate` and `rtl-full`, all completed success at 2026-10-11 (`receipts/hosted-check-runs.tsv`, `receipts/hosted-workflow-runs.tsv`). "Physical gPTP" is skipped.
- Validation of the current-dev merge candidate (builder and native banks) at the merge turn. No manager source bank ran at this head, and none is claimed here.
- Carry R607-1-R1 and R607-1-R2 to the residue checklist.
- F3 is against the PR body, which the manager's merge made stale.

R607-1 FINISHED

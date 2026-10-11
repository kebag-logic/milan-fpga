[R606] NEGATIVE - exact head 08b90b6859b0a7d7f172c7ae29745248895d9aa9

# R606-1: internal cleared-context review of PR #721 (issue #640, Mark II lane M8a-1 / plan L11a)

- Head `08b90b6859b0a7d7f172c7ae29745248895d9aa9`, tree `35e198ffb5808ce77515e649cf752f4d73a6fed8`. The head is the author's `5d532e9d` plus a manager merge of live dev `ac2c5e77`.
- Scope authority: the assignment (#640 comment 6100371426) and the ruling on the STOP (6101485877, which defines step M8a-1). The ruling sets four terms: the owner's 224 KB binding, up to 56 RAMB36 as mapped; the split's conditional wrapper release counted; no power-of-two waste; and the firmware owning the reset entry in the split placement only.
- Boot, service and route belong to M8a-2, after F-INT PR 2.
- All five lenses were applied. Five MINOR findings are open under Robustness, Tests and Docs, so the verdict is NEGATIVE. Conformance and RTL are covered clean.
- **Prior public review findings on this PR:** none exist. The only PR comment is the manager's review-start notice, and the PR has no review objects. Nothing needed to be resolved or retained.
- **Source-head execution evidence:** this is the author's published gate receipts plus the reviewer runs listed below. No manager source bank was run at this head, and none is claimed.

## What was reproduced independently at this head

Every receipt below is under `receipts/`. Scripts are under `scripts/`.

| Claim | Reviewer evidence | Result |
|---|---|---|
| The four linked split images | Pinned Bootlin SDK, freshly installed and verified (`env_sdk_verified.txt`). The runtime was built from Picolibc `6a13ccce` and compiler-rt `6eb76609`. All four points were linked with `ctrl_srp_image.py --with-aecp --layout split` (`link-*.log`, rc 0). | All four ELFs are **byte-identical** to the author's published `elf.sha256` (`split_elf.sha256`). |
| Spans, banks and planned tiles | `scripts/xcheck_plan.py` recomputes rom/sram need, banks and tiles from `readelf`, not from `ctrl_memory.read_elf` (`xcheck_plan.txt`). | 95,032+45,520 / 96,320+56,880 / 108,680+86,080 / 110,056+112,208 B. Planned 35.0 / 38.0 / 48.5 / 54.5. `nvm_stage` is 3,344 / 13,264 B. All points are within 56. |
| As-mapped fit (author's Vivado TSV) | The arithmetic was re-derived from `ctrl_memory_ooc.tsv` and the s8i2 utilization report. | 33/2, 37/1, 46/2 and 52/2 RAMB36/RAMB18, i.e. 34.0 / 37.5 / 47.0 / 53.0 tiles. LUT/FF are 212/32, 89/7, 307/33 and 328/40. ROM trim: 64 KiB bank to 15.5 tiles, plus one bank in logic, gives 25.5 for s8i2_rom. **Vivado was not re-run** (none on this host). |
| Ledger arithmetic | Hand check. | 87.5-6.5+6-18+53+2 = 124, then 113 after the -11 release, which is 8.5 under 121.5. With every bank in block RAM: 125.5 and 114.5. Keeping the BIOS: 142 and 131. Correct, except finding F4. |
| The dev merge composes mechanically | `composition_milan_soc.txt`, `composition_merge3.txt` | The PR's 89 `milan_soc.py` change lines are identical before and after the merge. A three-way `merge-file` of base/ours/theirs reproduces the head exactly for `milan_soc.py`, `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md` and `run_litex_sims.sh`. `TESTING.md` was a 1-hunk conflict, resolved by keeping both paragraphs (M2's and M8a's). Every other merged file equals dev's blob. |
| All-fabric default is digest-identical | Shipping AX7101 1x1 launch argv (`dry-ax7101.log`) exported without Vivado, from a dev `ac2c5e77` tree copy and from the head. Compared with my own normalizer (`scripts/digest_compare.py`), which normalizes only the out/tree roots, stamps, the Date line and the hierarchy comment. | **22 common files, 0 differ**, none one-sided (`digest_default_dev_ac2c5e77_vs_head.txt`). Same CPU netlist `VexiiRiscvLitex_f5f08b17…`. |
| Split export, no BIOS | Head export with `--ctrl-mailbox --ctrl-firmware` s1i1 (`split_export_summary.txt`) | `rom` and `sram` are 229,376 B each. The `.v` holds only `rom_bank0..4` (16384/4096/2048/1024/512 words) and `sram_bank0..3`, plus the 49-line identifier memory. There is no BIOS ROM/SRAM, `software/bios` is empty, and `rom_bank4.init` holds the 206 words that end the image. Exported SoC decode: region `adr[29:16]`; banks `adr[15:14]`, `[15:12]`, `[15:11]`, `[15:10]` and `[15:9]`; hole `adr[15:0] >= 0x5e00`. |
| CSR map unchanged | Dev `--ctrl-mailbox` export against the head split export (`csr_map_dev_mailbox_vs_head_split.txt`) | `csr.csv` and `csr.json` differ only in the `rom` (131,072 to 229,376) and `sram` (8,192 to 229,376) region sizes. |
| One CPU netlist for both shapes | 1x1 and 8x8 split exports (`netlists.txt`) | Both use `VexiiRiscvLitex_dd10544c…`. The 8x8 export re-ran no generator. |
| Planted controls through the real SoC build | My own plants (`scripts/make_plants.py`, `plants_offline.txt`, `soc_plants.txt`, `soc-plant-*.excerpt.txt`) | **Over budget:** 120,000 B rodata plus 110,000 B bss, each inside its own region, refused `allocation over budget: 59.5 RAMB36`. **Overlap:** `.bss ADDR(.data)` refused `memory-map overlap`. **Wrong shape:** the 8x8 image in the 1x1 build refused `staging buffer: nvm_stage is 13264 bytes; the endstation_ax7101_1x1_tdm8 shape stages 3344`. Each exits rc 1 before any export and before CPU netlist generation. `--ctrl-mailbox` alone and `--ctrl-firmware` alone are each refused by argparse (rc 2). |
| PR test and LiteX aggregate | `test_ctrl_memory.head.log` (33 ok, `RESULT: PASS`, link arm ran). `run_litex_sims.sh --selftest` rc 0. Aggregate `litex_sims.log`. | **7 of 7 PASS** at this head; M2's `test_retained_cdc_storage` joined via the merge. |
| Docs and idiom gates | `gates_docs_local.txt` (pinned Markdown renderer) | `docs_check`, `check_doc_paths`, `check_doc_style`, `gen_toc --check` / `--verify-anchors`, `check_em_dash --base ac2c5e77` and `check_py_idiom` all rc 0. |
| Hosted at exact head | `hosted_checks_08b90b68.tsv`, `hosted_elaborate_litex_sims_excerpt.txt` | Every executed context succeeded: `rtl-fast`, `docs-check`, `elaborate`, the Verilator shards 0-4/5, the Yosys shards and `yosys-elaboration`. The `elaborate` job's LiteX aggregate reads `PASS test_ctrl_memory` and `simulations: 7 passed: 7 … skipped: 0`. `Physical gPTP` is **skipped** (a context skip, not hardware proof). The manager owns hosted and act acceptance. |

## Findings

### F1 - MINOR - Robustness, Tests - `sw/litex/ctrl_memory.py:205-214` (`check_map`) - writable initialised data placed in read-only `rom` is accepted

- **Authority/evidence:**
  - `check_map` refuses a NOBITS section in `rom` because "the firmware cannot write" it.
  - It does not refuse an initialised writable (`SHF_WRITE`) section whose run address is in `rom`. `read_elf` drops section flags, so the case cannot be seen.
  - Probe `scripts/probe_writable_rom.py` (`receipts/probe_writable_rom.txt`) links the PR's own probe program with the PR's `ctrl_split.ld`, changing only `} > sram AT > rom` to `} > rom`. `ctrl_memory.plan` **accepts** it, with `.data` at `0x70` in `rom`.
  - The `rom` banks are read-only `wishbone.SRAM`s that ack and drop writes (the test's own "a write to rom changes nothing").
  - The real images carry 56 to 448 bytes of `.data`.
- **Impact:** a link-script regression builds and passes every named check. It then ships a split image whose initialised globals silently never change when written, and the reset entry's copy loop copies `rom` onto itself.
- **Required outcome:** the `memory map` check refuses, by name, a writable section whose run address lies in `rom`. A test arm plants that link-script edit.
- **Verification:** the probe reports `REFUSED memory map`, and the new arm turns red when the check is removed.

### F2 - MINOR - Tests - `sw/litex/test_ctrl_memory.py:247-297` (`sim_arms`) - the "past the last bank answers err" claim is graded at one address only

- **Authority/evidence:**
  - The test docstring (lines 24-25) and `SPLIT_CONTROL_MEMORY.md:53` claim that an address past the last bank answers err and writes no bank.
  - The arm reads one address, the first word past a 14 KiB bench.
  - Two decoder mutants of `milan_soc.CtrlMemory` leave `test_ctrl_memory` at `RESULT: PASS` (`receipts/mutations_decoder.txt`, `mut-*.test.log`):
    - `low` one bit narrower;
    - the hole compare on one fewer bit.
  - Against the largest image's sram banks, my probe `scripts/probe_region_top.py` finds 97 of 115 sampled addresses in `[0x20000, 0x38000)` that, under those mutants:
    - acknowledge and alias writes onto populated banks; or
    - never answer, which wedges the bus master.
  - At the head the same probe passes (`probe_region_top.head.txt`).
- **Impact:** a decode regression in the upper half of the 224 KiB window would corrupt live sram or hang the CPU, and the suite would stay green. The head code is correct; the gap is in the test.
- **Required outcome:** the arm grades err (and no write) across the region up to its last word, including addresses at and above half the region, at a bank plan that reaches the shipped sizes.
- **Verification:** both mutants turn the arm red.

### F3 - MINOR - Tests - `sw/litex/milan_soc.py:4019`, `:2740-2756`, `:4318-4322` - the SoC-level hookup has no self-checking test

- **Authority/evidence:**
  - The changed `main()` and `MilanSoC` behaviour has no automated check. It covers:
    - the `--ctrl-mailbox`/`--ctrl-firmware` pairing;
    - BIOS suppression (`integrated_rom/sram_size=0`, `integrated_rom_initialized`, no shipping firmware);
    - the `reset entry` refusal;
    - the staging check called in `main()`.
  - `test_ctrl_memory`'s "staging check off" mutant patches only the module function used inside the test.
  - With the `main()` staging call removed (`receipts/mutation_main_stage.txt`), `test_ctrl_memory` still passes and the real SoC build **exports** the 8x8 image into the 1x1 build. At the head, that same build is refused (`soc-plant-wrong-shape.excerpt.txt`).
  - `SPLIT_CONTROL_MEMORY.md:78` says the controls fail "in the SoC build itself". That is evidenced only by one-off receipts.
  - All three refusals fire before CPU netlist generation (no generator ran in any plant), so a real-build test is practical.
- **Impact:** a later edit to the hookup can silently drop a ruled control or rebuild the BIOS in the split, with every gate green.
- **Required outcome:** a self-checking test, in the LiteX aggregate or the builder's elaboration gate, that drives the real `milan_soc` build path and checks:
  - the three planted controls refused by name;
  - the two flag pairings refused;
  - (optionally) a passing split elaboration that contains no BIOS memory.
- **Verification:** the `main()`-stage mutant above turns it red.

### F4 - MINOR - Docs - `docs/design/MARK_II_AREA_PLAN.md:861-862`, `docs/design/AREA_BUDGET.md:265` (also `MARK_II_AREA_PLAN.md:1046`) - stale ledger figure at the ruled ceiling

- **Authority/evidence:**
  - Both docs still say "At 56 firmware tiles, the conditional total is/becomes 115.5 … leaving six".
  - That is the old arithmetic with the estimated -18.5 reuse row. The PR replaced that row with the measured -18.
  - With the PR's own rows: 87.5-6.5+6-18+56+2-11 = **116**, leaving **5.5**.
  - Separately, the lane-sequence row at `MARK_II_AREA_PLAN.md:1046` still says "reconcile 50-tile firmware allocation", where the ruling binds 56.
- **Impact:** the headroom stated at the ruling's own limit is wrong by half a tile in both authoritative ledgers.
- **Required outcome:** the 56-tile line reads 116 tiles, leaving 5.5, in both documents, and the lane row names the ruled 56-tile limit.
- **Verification:** re-derive from the table rows. The doc gates stay green.

### F5 - MINOR - Docs - `docs/design/MARK_II_AREA_PLAN.md:821`, `docs/design/SPLIT_CONTROL_MEMORY.md:126-128` (PR body "231 of the largest point's 328") - the 231-LUT figure is attributed to the logic ROM bank alone

- **Authority/evidence:**
  - 231 is the LUT-primitive count of the whole `s8i2_rom` top in `ctrl_memory_ooc.tsv`. That top includes the region's four-way bank decode and 32-bit read multiplexer.
  - For the same top, `report_utilization` gives 220 Slice LUTs.
  - The decode/mux cost is not zero:
    - `s1i2_rom`, two banks with none in logic, takes 36 LUTs;
    - `s8i2_sram`, five banks all in block RAM, takes 97.
  - The plan says Vivado "puts one sparse 1,024-word ROM bank in 231 LUTs". The split doc says that logic is "231 of the largest point's 328".
- **Impact:** the figure M8a-2's route is told to "weigh … against at most 1.5 tiles" overstates what forcing that bank into block RAM would recover.
- **Required outcome:** state 231 as the `rom` region's LUTs including its decode and the bank in logic, or measure the bank's own share. Name the counting basis (LUT cells or Slice LUTs).
- **Verification:** the figure matches a named column of the published TSV or report.

## Residue (wording only; does not affect the verdict or lens coverage)

- **R1** - `docs/design/AREA_BUDGET.md:263` and `docs/design/MARK_II_AREA_PLAN.md:832` say the "measured" total is 2.5 tiles over 121.5. That total carries M2's +2 allowance, which the plan itself records as unused (`MARK_II_AREA_PLAN.md:699`). Exact fix:
  - "With M2's unused +2 allowance, the ledger is 2.5 tiles over 121.5 before conditional reclamation." (AREA_BUDGET)
  - "Before the conditional release, with M2's unused +2 allowance, the total is 2.5 tiles over 121.5." (plan)
- **R2** - The PR body is stale after the manager's merge. Exact fix:
  - "REVIEW READY for M8a-1, head `5d532e9d…`" becomes "head `08b90b68…` (`5d532e9d` plus a merge of dev `ac2c5e77`)";
  - under "Expected result", "the aggregate passes 6 of 6" becomes "the aggregate passes 7 of 7 at `08b90b68`".

## Suggestions (optional)

- **S1:** `sw/firmware/ctrl/plat/ctrl_split_start.S` installs no trap vector, where the LiteX BIOS start-up installs one. Section 4 of `SPLIT_CONTROL_MEMORY.md` could say what a trap (for example the hole's `err`) does before the firmware sets `mtvec`, or M8a-2 could set one.
- **S2:** `CtrlMemory` slices `words[first:first+depth]`, so `rom_words` longer than the planned banks would be silently truncated. An assertion in `add_ctrl_memory` would close that.
- **S3:** `read_elf` on a truncated file raises `struct.error`/`IndexError` rather than a named `Refusal`. This fails closed, but without a name.

## Lens coverage (reviewer-owned ledger)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 6101485877 items 1-4 and assignment 6100371426 against: `sw/litex/ctrl_memory.py:43-49,87-89` (56 RAMB36 at 4,096 B; rom at 0x0, sram at 0x1000_0000); `milan_soc.py:2740-2756,2900-2914,4019,4194-4199`; byte-identical relinks at four points; `xcheck_plan.txt`; `ctrl_memory_ooc.tsv`; ledger rows `MARK_II_AREA_PLAN.md:803-811`; default digest vs dev; no-BIOS split export; CSR-map diff; planted controls through the real build; `SPLIT_CONTROL_MEMORY.md` §4 (console/diagnostics) | R606-1 | `08b90b6859b0a7d7f172c7ae29745248895d9aa9` |
| RTL | CLEAN | `milan_soc.py:2710-2737` (`CtrlMemory`: `low`, bank decode `a[s:low]`, hole err pulse, read-only banks); exported `alinx_ax7101.v` selects (region `adr[29:16]`, banks `[15:x]`, hole `>= 0x5e00`); `probe_region_top` over the largest sram plan; `pp_mem_gate` (`milan_soc.py:2387-2411`) for the DDR3 claim; ROM trimming against the utilization report. Timing is out of scope (M8a-2) | R606-1 | `08b90b6859b0a7d7f172c7ae29745248895d9aa9` |
| Robustness | UNCLEAN (F1) | `ctrl_memory.py:151-233` (malformed/foreign ELF, entry, sections, overlap, budget, stage); flag pairing; CPU reset re-entry (`ctrl_split_start.S`); feature-off digest; writable-in-rom probe | R606-1 | `08b90b6859b0a7d7f172c7ae29745248895d9aa9` |
| Tests | UNCLEAN (F1, F2, F3) | `sw/litex/test_ctrl_memory.py` (33 checks run at head, link arm included); decoder and `main()` mutants; `run_litex_sims.sh` 7/7; hosted `elaborate` aggregate | R606-1 | `08b90b6859b0a7d7f172c7ae29745248895d9aa9` |
| Docs | UNCLEAN (F4, F5) | `docs/design/SPLIT_CONTROL_MEMORY.md`; `MARK_II_AREA_PLAN.md:766-870`; `AREA_BUDGET.md:221-282`; `MAILBOX_SPLIT.md:813-831`; `LITEX_SOC.md`, `ARCHITECTURE_HW_SW_SPLIT.md`, `docs/README.md`, `TESTING.md` (merge resolution), `CI_WORKFLOWS.md` (SDK path matches `fw_rv32.CANDIDATES`), `sw/firmware/ctrl/README.md`; local doc gates; PR body | R606-1 | `08b90b6859b0a7d7f172c7ae29745248895d9aa9` |

## Real limits

- **Vivado not re-run.** No Vivado is installed on this host. The as-mapped RAMB36/RAMB18/LUT figures are the author's single out-of-context run (Vivado 2026.1). I checked their arithmetic and consistency with the utilization reports, not their reproduction.
- **Ruling vehicle for M8a-1.** Per the ruling, there was no route, timing, split boot, `check_nvm_capture.py`, `nvm_cosim` or `nvm_capture_cpu` at this step. The reset entry is checked by link layout, not by a CPU simulation. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Runtime build.** To link the size fixtures, my runtime build needed `-fno-stack-protector` appended through a compiler wrapper. Without it, the pinned SDK's compiler-rt objects reference `__stack_chk_guard`. The PR does not change `ctrl_image_runtime.py`. The resulting ELFs match the author's bytes.
- **Digest scope.** The default-digest reproduction covers the shipping AX7101 1x1 configuration only. The default path change is board-independent by inspection (every new branch is gated by `ctrl_mailbox`/`ctrl_firmware`).
- **Banks not run.** No parent, PP, gPTP, Yosys or builder bank was run. The Verilator binary was not used.
- **Clone state.** `third_party/lwSRP` was initialized at its recorded gitlink to link the firmware. The tracked bytes, modes, index and all five gitlinks were verified equal to the head (`final_tree_verification.txt`).

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and publish its receipts.
- Accept the hosted and act evidence on the exact head.
- Carry R1 and R2 to the residue checklist.
- Check the external review.
- Coordinate with F-INT PR 2 (#704): after this PR, `--ctrl-mailbox` is refused without `--ctrl-firmware`, and the split builds no shipping firmware.
- Re-review the fixes for F1-F5 at the new head.

R606-1 FINISHED

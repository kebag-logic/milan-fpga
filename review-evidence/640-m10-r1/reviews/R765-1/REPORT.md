[R765] NEGATIVE - exact head 3f8ed303e01285f1bad0641f4ebc05764f162467

# R765-1: internal cleared-context review of PR #835 (issue #640)

- Head: `3f8ed303e01285f1bad0641f4ebc05764f162467`, tree `580d876cd9f7f973d1407d3da5759a23822a24d0`.
- Base: dev `503bc97cd4f24ad07596c17e7188f2024617972d`, the merge of PR #828.
- Delta: seven one-line commits, four Markdown pages, docs only.
- The pages: `docs/design/MARK_II_AREA_PLAN.md`, `docs/design/AREA_BUDGET.md`, `docs/design/MAILBOX_SPLIT.md` and `docs/findings/README.md`.

All five lenses were applied. Three lenses are unclean: Conformance, RTL and Docs. Robustness is unclean too, from F5. Tests is clean.

Five MINOR findings are open. Most concern the new LiteX block census:

- it misplaces two blocks against `sw/litex/milan_soc.py`;
- it leaves some LiteX blocks without a row;
- one stage 1 measurement has no public source;
- the page leaves out the console buffer's dependency on unmerged S2b work.

The lever 4 accounting recomputes exactly. So do the #828 residue fixes, D18 to D21 and the UART arithmetic.

## How this round reconstructed the task

Sources were read in this order:

1. `AGENTS.md` and `CONTRIBUTING.md`.
2. #640's body and every comment from 2026-10-30 on:
   - the owner's decisions of 2026-10-31;
   - the stage 1 probes, issuecomment-6555550136 and issuecomment-6556743957;
   - the owner and manager decisions D18 to D21, issuecomment-6575277828;
   - both TAKEN and REVIEW READY pairs.
3. The cited #665 comments: 6569635407, 6514866239 and 6495692075.
4. The #495 residue, issuecomment-6573412222.
5. The diff `503bc97c..3f8ed303` and its seven commits.
6. `sw/litex/milan_soc.py`, the firmware sources, `SPLIT_CONTROL_MEMORY.md`, `ARCHITECTURE_HW_SW_SPLIT.md` and the 649 hierarchy map.
7. Last, the public evidence tree `review-evidence/640-m10-r1` at `b4578f5c`.

**Prior review findings on PR #835.** There are none to resolve or retain. The PR has no review, no inline comment, and only the two review-start comments.

## Executed checks (receipts in this packet)

These ran on this clone at the exact head:

| Check | Result | Receipt |
|---|---|---|
| `scripts/docs_check.py` | rc 0, 0 findings over 213 pages | `receipts/gates/docs_check.*` |
| `scripts/check_em_dash.py --base 503bc97c` | rc 0, 0 over 194 added lines | `receipts/gates/em_dash.*` |
| `scripts/check_doc_style.py` and `--selftest` | rc 0 and rc 0 | `receipts/gates/doc_style*.*` |
| `scripts/gen_toc.py --selftest`, `--verify-anchors`, `--check` (pinned renderer) | rc 0 each; 582 cross-page fragments | `receipts/gates/toc_*.*` |
| `scripts/check_doc_paths.py` | rc 0, 1,084 paths | `receipts/gates/doc_paths.*` |
| `scripts/check_feature_status.py` | rc 0 | `receipts/gates/feature_status.*` |
| `docs/traceability/gen_module_matrix.py --check` | rc 0 | `receipts/gates/module_matrix.*` |
| `git diff --check 503bc97c HEAD` | rc 0 | `receipts/gates/diff_check.*` |
| `check_doc_style.analyze()` on every changed block of the four pages | rc 0, 0 findings | `scripts/style_changed_blocks.py`, `receipts/gates/style_changed_blocks.*` |
| Gate reader of `AREA_BUDGET.md`: `syn/ooc/pp_resource_gate.py check-baseline` | rc 0, "baseline PASS: 3 endpoints" | `receipts/gates/resource_check_baseline.*` |
| Gate reader of `MAILBOX_SPLIT.md`: `ctrl_service_bounds.arm_service_bounds` | rc 0, 47 checks, 0 failures, 38/38 planted controls | `scripts/service_bounds_reader.py`, `receipts/gates/service_bounds_reader.*` |
| Every derived figure the PR adds, recomputed from the cited rows | 29 of 29 PASS | `scripts/recompute_figures.py`, `receipts/recompute_figures.*` |

**The author's published gate receipts.** `author/a720k/evidence/gates` at the exact head holds 54 rc files, all 0. That includes both builder legs; leg 1 has 16 NOT RUN by its own skip rules.

**Hosted runs at this head.** They were in progress when sampled: 3 success, 20 queued or in progress (`receipts/hosted_check_runs.tsv`). This round claims none of them.

**Clone restore.** Two submodules were initialised for the reader, then deinitialised. Worktree and index equal HEAD. Index modes, blobs and paths equal the tree, and all six gitlinks match (`receipts/restore_verification.txt`).

## Focus items

1. **Lever 4: met.**
   - `milan_soc.py` adds no CPU under `ctrl_mailbox`. #665 issuecomment-6569635407 records "The split placement already has one hart".
   - 52,008 - 24,354 - 481 + 3,948 + 3,102 = 34,223.
   - 34,223 - 3,249 = 30,974.
   - Running totals: 30.0k, 29.0k, 27.2k, 27.2k, 26.2k, 21.0k.
   - Both chains reach 27,224 after lever 4.
   - The ranges give 19.8k to 22.4k. At 32x32: 21.75k, from 18.5k to 25.45k; the central miss is 1.75k.
   - No page elsewhere in `docs/` still carries 34.2k, 21.45k, 20.7k or 3.55k.
2. **Census: not met.** See F1, F2 and F3.
   - These rows match the code: interrupts (no firmware enables one), `ctrl`, `identifier_mem`, `timer0` (its one reader is `nvm_flash_litespi.c`), the UART FIFO depth, MDIO, `ICAPE2`, the LiteSPI PHY stage, the processor's memory paths and the LEDs.
   - Firmware greps found no reader of `ctrl_*`, `identifier_mem` or the interrupt masks.
3. **UART: arithmetic met, stated dependency not met.** See F5.
   - D20 is quoted exactly: first-party, TX and RX only, no RTS/CTS.
   - 86.806 µs per character; 24 completions in a 2.0 ms gap; 32 bytes cover 2.778 ms.
   - The loss figures match the probe comment.
4. **Stage 1: met, except one figure.** See F4.
   - D18 and D21 match issuecomment-6575277828 word for word in substance.
   - Open decision 4 and every "layout unchanged" statement are gone.
   - `QSPI_FLASHBOOT.md` is not edited.
   - The DMA hang is stated as a measurement, not a diagnosis.
5. **#828 residue: met.**
   - `AREA_BUDGET.md:129` and `:180`, `MAILBOX_SPLIT.md:13`, `:134` and the optional `:43`, and `findings/README.md:26` each carry their fix.
   - Where the exact text broke `check_doc_style.py`'s 10-word sentence or 20-word paragraph limit, it was split with the same content. The `AREA_BUDGET.md:130` rewording ("must use" to "needs") is part of that split.
6. **Style and sourcing.**
   - The style gate and the changed-block probe are clean.
   - One measured figure has no public source (F4).
   - No source file is changed, so the owner's 2026-10-15 comment rule has no instance in this delta.

## Findings

### F1. MINOR: the census places the BIOS ROM and SRAM at stage 1, but the split build lane 1 ships already drops them

**Lenses:** Conformance, Docs.

**Where:** `docs/design/MARK_II_AREA_PLAN.md:315-316`, and the census scope at `:292`.

**Authority and evidence:**
- `sw/litex/milan_soc.py:3170-3176`: under `ctrl_mailbox`, `integrated_rom_size=0, integrated_sram_size=0`. The BIOS ROM and SRAM are not built; `add_ctrl_memory` builds `rom` and `sram` from the firmware.
- `docs/design/SPLIT_CONTROL_MEMORY.md:7-8` and `docs/ARCHITECTURE_HW_SW_SPLIT.md:252` say the same.
- So does the plan's own ledger at `:1268`: "BIOS ROM and SRAM not built in the split".
- Lane 1, the switch-over (`:397`), integrates that split before lane 2 runs stage 1.
- The SRAM row's own fate names `ctrl_memory`, the lane 1 mechanism, yet its stage reads 1.
- The split image's own LiteX parts have no row:
  - `CtrlMailbox`'s `EventManager` and CSR bank (`milan_soc.py:2896-2901`, `:2959-2964`) and its Wishbone window;
  - `CtrlMemory`'s LiteX `wishbone.SRAM` banks and `wishbone.Decoder` (`:2990-3001`).
- Yet D19's consequence reads "no LiteX block remains" (`:382`).

**Impact:** The census is the record D19 relies on. It misstates which lane removes the BIOS memory. It also leaves without a fate the LiteX parts that the stages actually face on the image lane 1 ships.

**Required outcome:**
- The BIOS ROM and SRAM rows say the switch-over removes them, with `ctrl_memory`'s banks in their place.
- Stage 1 then replaces the configuration-initialised `rom` image with the flash copy (D18).
- The split image's LiteX parts each get a stage and a fate. The alternative is for the census to state that its scope is the all-fabric basis and list those parts as owed.

**Verification:** Read the rows against `milan_soc.py:2878-3018` and `:3170-3176`.

### F2. MINOR: the census removes the IDELAYCTRL with DDR3 at stage 1, but Ethernet also builds it, and its clock drives the audio MMCM's phase shift

**Lenses:** Conformance, RTL, Docs.

**Where:** `docs/design/MARK_II_AREA_PLAN.md:314`, the DDR3 row: "...; the `IDELAYCTRL` | ... | 1 | Removed, nothing in its place: main memory is on chip (D4)".

**Authority and evidence:**
- `milan_soc.py:466-472`: `_CRG` builds the 200 MHz `idelay` clock and `S7IDELAYCTRL` whenever `with_dram or with_eth`.
- The shipping SoC passes `with_eth=with_mac`, and the census itself lists the LiteEth MAC as present until stage 2. So dropping DDR3 at stage 1 leaves the IDELAYCTRL in place.
- `milan_soc.py:402` and `:421`: the same `idelay` clock is the audio MMCM's `PSCLK`, its fine phase-shift clock, whenever `with_dram or with_eth`.

**Impact:**
- The row credits stage 1 with a removal it does not make.
- A lane that follows the row and drops the `idelay` domain changes the media-clock MMCM's phase-shift clock without the plan saying so.

**Required outcome:**
- The IDELAYCTRL and the `idelay` clock sit under the block that builds them (`_CRG`, stage 3) or under the Ethernet row.
- Their fate keeps or replaces the audio MMCM's `PSCLK` source.

**Verification:** Read the row against `milan_soc.py:396-472`.

### F3. MINOR: two MilanMAC LiteX CSRs have no census row, including the one the firmware uses to publish link state

**Lenses:** Conformance, Docs.

**Where:** `docs/design/MARK_II_AREA_PLAN.md:308` and `:310`, where no row names them, and `:382`, "no LiteX block remains".

**Authority and evidence:**
- `milan_soc.py:1958`: `MilanMAC.link_status`, a `CSRStorage`, carries the software-published link, speed and duplex into the datapath (MAC_STATUS, REQ-MAC-03).
- The shipping firmware writes it at `sw/firmware/milan_baremetal/milan_baremetal.c:1064`, `:1073` and `:1080`.
- `milan_soc.py:1896-1935`: `MilanMAC.loopback`, a `CSRStorage`, and its TX-to-RX mux.
- Neither is LiteEth or first-party RTL, and the page mentions neither.
- The census states that it lists every block, and focus item 2 requires that no block be unnamed.

**Impact:** After D19 removes every LiteX CSR, the path that tells the datapath the negotiated link state (the 1 Gb/s admission input) has no planned home.

**Required outcome:** Rows for `link_status` and `loopback`, each with a stage and a fate. For example, folded into `milan_csr` or the first-party top.

**Verification:** Read the rows against `milan_soc.py:1591-2192`.

### F4. MINOR: "311 of 311 reads were answered" on the SoC bus has no public source

**Lenses:** Conformance, Docs.

**Where:** `docs/design/MARK_II_AREA_PLAN.md:281`. The same figure is in the PR body, item 4.

**Authority and evidence:**
- The cited probe, #640 issuecomment-6556743957, gives only the DMA-port figure, "3 issued, 0 acked, 3 abandoned".
- A repository search for "311 of 311" finds only PR #835 itself. No #640 comment contains the number.
- The author's published handoff traces it to an unpublished probe report ("A722b REPORT sections 4 and 7").
- AGENTS.md section 2: a cold reviewer must be able to reconstruct the task from GitHub and the repository alone.

**Impact:** A measured figure in a design page cannot be checked or reproduced.

**Required outcome:** Cite a public source carrying the figure, or remove the figure.

**Verification:** Open the cited source and find 311 of 311.

### F5. MINOR: the console buffer's 2.0 ms bound depends on the unmerged S2b share, and the page does not say so

**Lenses:** Conformance, Robustness, Docs.

**Where:** `docs/design/MARK_II_AREA_PLAN.md:336`, "2.0 ms: one pass, and every work pass fits the per-pass share | Bound", and `:340`.

**Authority and evidence:**
- The share comes from the S2b lane, PR #810. That PR is OPEN against `dev-soft-core` and unmerged.
- At this head the only mention of a per-pass share anywhere in the tree is this row (`receipts/public_source_searches.txt`).
- #665 issuecomment-6569635407 estimates the longest pass at 32x32, the Mark II shape, as 1.7, 3.0 and 5.9 ms over the share.
- The PR body states both points under "Known limitations", but the page that merges does not.
- Focus item 3 requires the dependency to be stated. AGENTS.md section 8: never hide a material assumption.

**Impact:** After the merge, dev carries a "Bound" whose premise is neither on dev nor met at 32x32, with nothing saying so.

**Required outcome:** The page states two things:
- the share is the S2b lane's and not yet on dev;
- at 32x32 the share is estimated exceeded, so the 32-byte figure holds where every pass fits it, and the loss rule covers the rest.

**Verification:** Read the page text against PR #810's state and the #665 comment.

## Suggestions (non-blocking)

- **S1** (Docs), `MARK_II_AREA_PLAN.md:167`. No public source shows the netlist identifier `VexiiRiscvLitex_7ee512a1cb1c336731b7f28188c9814f`. The cited comment carries 3,948 and 3,543 but not the identifier. Cite where it is recorded, or drop it.
- **S2** (Conformance), `:166-168`. The net change uses 3,948, the CPU behind the clock crossing. Since the owner's 2026-10-30 decision, the product split CPU is on `sys`, where #665 measured 3,543, a net change of +294. The page notes 3,543. One sentence on which figure the start uses, and why, would close the question.
- **S3** (Docs), `:334`. The author's handoff says the console-loss receipt is probe image A, the image with the DMA-port route. Naming the image would let a reader judge how representative the loop timing is.

## Residue

None.

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4, F5) | #640 decisions D18 to D21 and focus items 1 to 6; `MARK_II_AREA_PLAN.md:40-47, 110-213, 224-347, 378-403, 417-440` against `milan_soc.py`, #665 comments 6569635407, 6514866239 and 6495692075, #495 comment 6573412222 and #640 comment 6575277828; `receipts/recompute_figures.log` | R765-1 | `3f8ed303e01285f1bad0641f4ebc05764f162467` |
| RTL | UNCLEAN (F2) | The page's clock, CDC, interrupt and bus-master claims (`:278-285, 298-317`) against `milan_soc.py:218-472` (`_CRG`), `:789-815` (`milan_axil_cdc`), `:1591-2192` (`MilanMAC`), `:2878-3018` and `:3051-3320`, and `sw/firmware/ctrl/plat/mbx_plat_mmio.c` (no interrupt enabled) | R765-1 | `3f8ed303e01285f1bad0641f4ebc05764f162467` |
| Robustness | UNCLEAN (F5) | UART boundaries: 16-, 24- and 32-character windows and the gap beyond the bound (`:330-346`); the D21 slot rules (not in the bitstream tail, erase-aligned, not reserved); the 32x32 behaviour of the console bound | R765-1 | `3f8ed303e01285f1bad0641f4ebc05764f162467` |
| Tests | CLEAN | No test changes in the diff. Gate readers of both gate-read pages pass at the head (`receipts/gates/resource_check_baseline.*`, `receipts/gates/service_bounds_reader.*`, 47 checks and 38 controls). The docs gates' rc files are all 0 (`receipts/gates/*.rc`). The author's 54 rc files at this head are all 0 (`author/a720k/evidence/gates`). Every derived figure recomputes, 29 of 29 | R765-1 | `3f8ed303e01285f1bad0641f4ebc05764f162467` |
| Docs | UNCLEAN (F1, F3, F4, F5) | The four changed pages; stale-figure sweep over `docs/`; consistency with `SPLIT_CONTROL_MEMORY.md:1-12` and `:115-135` and `ARCHITECTURE_HW_SW_SPLIT.md:248-256`; PR body against page; the #495 residue list | R765-1 | `3f8ed303e01285f1bad0641f4ebc05764f162467` |

## Real limits

- **The basis build's reports are outside the repository.** That applies to the placed rows this round could not open (`vexiis_0_logic_core` 1,150, `peripheral_toAxiLite4_logic_bridge` 227, `dma_bridge_*` 105 and 176, `mem_toAxi4_logic_bridge` 225, the width adapter 136). The plan records their SHA-256 digests. Only their names and the top-level structure were checked, against the 649 map of an earlier route.
- **The census was checked against `milan_soc.py` at this head.** The basis was built from qualification commit `40b77bbd`, which is not on dev, and was not checked out.
- **This round did not re-run everything.** It skipped the full docs workflow, the builder legs, the compiler-SDK gate and act. For those it relies on the author's published receipts, which were read, not re-executed.
- **No manager source bank ran at this head**, and none is claimed. Hosted runs were still in progress when sampled.
- **Physical calibration NOT RUN.** No hardware was used. Silicon claims (the DMA hang, the console loss) are taken from #640's public comments.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks), at source base and live dev `503bc97c`.
- Accept the hosted and act evidence. `scripts/ci_scope.py` classes `AREA_BUDGET.md` and `MAILBOX_SPLIT.md` as gate-read, so the exact-head `verilator-suites` and `yosys-portability` gates apply once the PR is ready.
- Route F1 to F5 to the author, and publish this report and the listed receipts.

R765-1 FINISHED

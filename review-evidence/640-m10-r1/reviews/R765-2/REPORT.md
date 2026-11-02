[R765] POSITIVE - exact head 30eb4834e0d258668a7bdfece187f9d7d9fccd0b

# R765-2: internal cleared-context re-review of PR #835 (issue #640)

- **Head:** `30eb4834e0d258668a7bdfece187f9d7d9fccd0b`
- **Tree:** `81f7e650087b8445b45b6fec2f1c8921f7e48626`
- **Source base and live dev:** both `503bc97cd4f24ad07596c17e7188f2024617972d`
- **Round 2 delta:** `3f8ed303..30eb4834`, five commits, documentation only.
  - `docs/design/MARK_II_AREA_PLAN.md`: +46 / -17.
  - `docs/design/MAILBOX_SPLIT.md`: one line.
  - `AREA_BUDGET.md` and `docs/findings/README.md` are unchanged since round 1.
- **Branch as a whole (`503bc97c..30eb4834`):** four documentation pages and no source, RTL, test or generated file. So the source-comment rule has no new instance to check.

All five lenses were applied at this head, and all five are clean. There are no open BLOCKER, MAJOR or MINOR findings. All eight round 1 findings are resolved at their cause:

- R765-1 F1 to F5;
- R766-1 F1 to F3, and R766-1-R1.

This round adds two RESIDUE items and four SUGGESTIONs. None of them affects the verdict.

## How this round reconstructed the task

1. **Contract and decisions.** Read AGENTS.md and the #640 body, including the 2026-10-31 owner target and acceptance. Then the D18 to D21 decision comment (issuecomment-6575277828), and the author's round 2 takeover and handoff comments (6577649057, 6578986708).
2. **Authorities.**
   - `sw/litex/milan_soc.py` at the head: `_CRG` at 218-475, `MilanMAC` at 1591-2192, `CtrlMailbox` and `CtrlMemory` at 2878-3018, the split-build branches at 3160-3205, and the audio MMCM servo port at 3331-3340.
   - `sw/litex/ctrl_memory.py:128-129`.
   - `docs/reference/FR_NFR.md` 3.4.1 and NFR-SCOUT-03.
   - `REQUIREMENTS.md` REQ-MAC-03.
   - `docs/design/REBOOT_RESET.md` section 1.
   - `docs/design/SPLIT_CONTROL_MEMORY.md` sections 1 and 5.
   - #665 issuecomments 6495692075 (owner T_svc = 20 ms), 6514866239 (the 2.0 ms share) and 6569635407 (S2b figures and the 32x32 estimate).
   - The stage 1 probe comment on #640 (issuecomment-6556743957).
   - PR #810's state and its FR_NFR patch.
3. **Diff and history.** Read `git diff 503bc97c..30eb4834` and the round 2 commits one by one.
4. **Executable evidence.**
   - The author's round 2 packet in the evidence tree at `5f8bd017`. All `author-r2` files match `MANIFEST.json` `published_sha256` and `author-r2/evidence/SHA256SUMS`.
   - Then this round's own probes, listed below.
5. **Prior findings.** The round 1 findings (PR #835 issuecomments 6577388726 and 6577608536) were read only after the independent pass over the delta.

## Executed checks (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| The author's census coverage check, re-run at this head against the published basis hierarchy, CSR map and placed excerpt | rc 0, `RESULT: PASS`, 23 rows. Output is byte-identical (after the first line) to the published `census_coverage.out` | `receipts/census_coverage_rerun_head.{out,rc}`, `scripts/census_coverage_author_r2.py` |
| Placed LUT figures new in the census against `basis_place_top_excerpt.rpt` | `ioBus_to_peripheral_bus_cc` 166 and `dma_filter_down_to_unified_mBus_cc` 104 match. The earlier 1,150, 34, 55, 3, 227, 105, 176, 225 and 136 also match. The full report's digest `ec345a49…` is the one the plan records | Packet excerpt (verified digest) |
| IDELAY use of the pinned LiteEth GMII PHY (`276c9e37`, from `ci/image/sources.lock.json`) and of the two local GMII patches | 0 IDELAY or ODELAY lines. The only primitives are 2 BUFG. This supports "GMII uses none" | `receipts/liteeth_gmii_no_idelay.txt` |
| Console UART arithmetic | 86.806 µs per character. Times for 23, 24, 32, 115, 116 and 128 characters are 1.997, 2.083, 2.778, 9.983, 10.069 and 11.111 ms. Gaps of 2 ms and 10 ms give 24 → 32 and 116 → 128 | `receipts/console_arith.out` |
| Docs gates at the head: `docs_check.py`, `check_doc_style.py` (and `--selftest`), `check_feature_status.py`, `gen_toc.py --selftest / --verify-anchors / --check`, `git diff --check 503bc97c 30eb4834` | All rc 0. `gen_toc` ran with the pinned renderer from `tools/markdown/requirements.txt`, installed into a disposable virtual environment under `scratch/` | `receipts/gate_*.{log,rc}` |
| Style findings introduced by the delta: `analyze()` on each page at both revisions, compared by (reason, text) | 0 introduced for round 2 (`3f8ed303`) on both pages. 0 introduced for the branch (`503bc97c`) on all four pages | `receipts/style_round2_delta.*`, `receipts/style_branch_delta.*`, `scripts/style_changed_blocks.py` |
| Planted control for that comparison: a 13-word sentence in the round 2 console prose | CAUGHT | `receipts/style_planted_control.out` |
| Gate-read page readers | Neither the changed `MAILBOX_SPLIT.md` line before nor after contains any string `ctrl_service_bounds.py` matches (0 hits). `AREA_BUDGET.md` is unchanged in round 2. `syn/ooc/pp_resource_gate.py check-baseline`: "baseline PASS: 3 endpoints", rc 0 | `receipts/reader_unaffected.out`, `receipts/gate_pp_resource_check_baseline.*` |
| Hosted contexts at the exact head (read only) | 21 runs when last read: 4 completed with success, 9 in progress and 8 queued. None failed. Not acceptance evidence | `receipts/hosted_check_runs_30eb4834.tsv` |
| Clone restored | HEAD, tree, index modes, blobs and paths equal HEAD. No untracked or ignored files after removing the probe's bytecode caches. All six gitlinks are at their recorded commits | `receipts/final_integrity.txt` |
| Public sources read | sha256 of each fetched comment and PR body | `receipts/public_sources.sha256.txt` |

## Focus items

### 1. The census is re-derived, and every LiteX block has a stage and a non-LiteX fate

**Holds.** The row set covers the basis build's tree and CSR map, and the split build's two additions (`MARK_II_AREA_PLAN.md:297-306, 308-332`). The re-run coverage check maps the following to exactly one row each, with a stage and a fate, and lists no row without an object:

- every depth-0 node;
- every depth-1 node under `cpu`, `crg`, `milan` and `milan_mac`;
- every CSR register and base;
- every placed child of the CPU wrapper;
- every split-only part.

This round also checked the deeper `milan_mac` and `milan` subtrees by hand: `phy.crg.hw_reset`, `phy.mdio`, `core.*`, `tx_sf`, the two MAC crossings, and the `descmem`, `respmem` and `nvmmem` crossings. Each falls in a named row.

**The rows the focus names:**

- **IDELAYCTRL and the 200 MHz clock (`:313`).** These agree with the source:
  - `_CRG` builds both when `with_dram or with_eth` (`milan_soc.py:466-472`);
  - `audio_ps_clk` is the `idelay` clock in that case (`:402`);
  - it drives the MMCM's `PSCLK` (`:421`) and the servo's `i_ps_clk` (`:3335`);
  - stage 1 keeps Ethernet, so it keeps both.

  The basis-netlist count of 32 IDELAYE2, all DDR3 DQ, comes from the author's recorded netlist digest (`basis_sources.txt`). Its GMII half is independently supported by the pinned LiteEth source (no IDELAY).

  The fate keeps today's `PSCLK`. That rests on the issue's acceptance that function is unchanged and on D15, and the PR names it as an open risk.

- **`link_status` (`:322`).** These agree with `milan_soc.py:1958-1988, 2177-2186`:
  - three fields;
  - a 2-flop `MultiReg` on link and duplex;
  - `speed` synchronised in the datapath;
  - REQ-MAC-03.

- **`loopback` (`:323`).** `CSRStorage(1)` resets to 0 (`:1896-1897`). No code in the repository writes `milan_mac_loopback`, which was checked by search; `gen_mac_tx_model.py`'s `loopback` is that model's own signal.

- **BIOS ROM and SRAM (`:328-329`).** These now sit at the switch-over, lane 1. `--ctrl-mailbox` sets `integrated_rom_size=0, integrated_sram_size=0` (`:3172-3176`). `SPLIT_CONTROL_MEMORY.md:8` says "No BIOS ROM or BIOS SRAM is built there."

  The note at `:235-236`, the basis row `:112` and the ledger sentence ("All 47 are gone once LiteX stage 3 ends") follow from that.

- **`ctrl_memory` (`:331`).** The `wishbone.SRAM` banks, the `Decoder` and the error answer past the last bank match `CtrlMemory` (`milan_soc.py:2973-2999`). The 35.0 tiles match `SPLIT_CONTROL_MEMORY.md:147`.

- **`ctrl_mbx` (`:332`).** These match `CtrlMailbox`: `EventManager`, the CSR bank and `ms_tick`. The firmware under `sw/firmware/ctrl` references no `ctrl_mbx` CSR.

**Fates are grounded.** Every fate cites a recorded decision or requirement: D4, D15, D18, D19, D20, REQ-MAC-03, or REBOOT_RESET section 1 (the PHY reset hold, `milan_soc.py:2127-2132`). No fate names a LiteX block (`:306`).

**One supporting detail:** `sys4x` is 4 × the 100 MHz default `sys` (`milan_soc.py:461-463, 3972`), so "two 400 MHz `sys4x` clocks" holds.

### 2. The console buffer states its dependency (`:351-370`)

**Holds.**

- The 2.0 ms share and T_svc = 20 ms are stated as #665 S2b work, PR #810, not merged. PR #810 was read as open and not merged.
- Dev's FR_NFR 3.4.1 and NFR-SCOUT-03 still read "T_svc = 10 ms, proposed" (`FR_NFR.md:329, 339`).
- Under 10 ms the page derives 128 bytes, and its arithmetic is exact.
- "32 bytes holds only while passes fit the share", with "derive the buffer again" if the share changes.
- At 32x32, the "1.7 to 5.9 ms over the share" matches 6569635407 ("longest pass, 2.0 ms share: 1.7 / 3.0 / 5.9"), and the loss rule applies there.

See S1 and RESIDUE-1 for two precision points.

### 3. 311-of-311 is gone (`:281-287`)

**Holds.** No instance of 311 remains. The replacement text matches the cited probe comment exactly:

- "3 issued, 0 acked";
- image B on the SoC bus: ENTITY_AVAILABLE;
- "all 33 descriptors byte-identical".

The text claims no cause, which matches the comment's "Not established: the hang's cause".

### 4. The other two changes are justified

- **`MAILBOX_SPLIT.md:151`.** "Its sources also include fabric timer expiries, tagged by arm." The subject can no longer be read as the grandmaster changes. The only meaning change is the shortening "with their arm" to "by arm", which keeps the tag semantics.
- **`MARK_II_AREA_PLAN.md:167`.** The netlist identifier `7ee512a1…` is absent from the cited #665 comment (0 occurrences). That comment does carry 3,948 and 3,543 ("3,543 LUTs … against 3,948 … behind the crossing"), so dropping the identifier and keeping the citation is correct.

### 5. Style and the gate-read pages' readers

**Holds.** No style finding is introduced (with a planted control). The TOC and anchors are clean. The `ctrl_service_bounds` reader is untouched by construction, and `pp_resource_gate.py check-baseline` passes.

## Prior findings, resolved or retained at this head

| Finding | Required outcome (abridged) | At `30eb4834` | Status |
|---|---|---|---|
| R765-1-F1 | BIOS ROM/SRAM at the switch-over, with `ctrl_memory`'s banks in their place; stage 1 replaces the configuration-initialised `rom` with the flash copy | Stage "Switch-over, lane 1" (`:328-329`); `ctrl_memory` has its own row naming the `rom` and `sram` banks, and "Stage 1 already fills `rom` from the flash copy" (`:331`); note `:235-236` | Resolved. The placement is by a separate row, not "in their place" wording; see S2 |
| R765-1-F2 | IDELAYCTRL and `idelay` under `_CRG`/stage 3 or Ethernet; fate keeps or replaces `PSCLK` | Own row, stage 3, keeps 200 MHz `PSCLK`; removed from the DDR3 row (`:313, 327`) | Resolved |
| R765-1-F3 | Rows for `link_status` and `loopback` with stage and fate | `:322-323` | Resolved |
| R765-1-F4 | Cite a public source for 311 of 311, or remove it | Removed; the replacement text traces to 6556743957 | Resolved |
| R765-1-F5 | State that the share is S2b and not on dev; at 32x32 the share is exceeded and the loss rule covers it | `:351-370` | Resolved |
| R766-1-F1 | Every LiteX block has a row; the BIOS SRAM fate names a first-party block, or `ctrl_memory` has its own stage and fate; state whether split-build blocks are covered | All three met (`:300-301, 306, 322-323, 329, 331-332`) | Resolved |
| R766-1-F2 | Share and 20 ms are #665 decisions carried by unmerged S2b; FR_NFR still says 10 ms proposed; derive again if the share changes | `:351, 355, 359-366` | Resolved; see S1 |
| R766-1-F3 | Publish and cite 311 of 311, or remove it | Removed | Resolved |
| R766-1-R1 (RESIDUE) | The pronoun fix | `MAILBOX_SPLIT.md:151` | Resolved |
| R765-1-S1, R766-1-S1 | Drop or source the netlist identifier | Dropped | Taken |
| R765-1-S2, S3 and the remaining R766-1 suggestions | Optional | Not taken; the PR body gives reasons | Remain optional; they do not affect coverage |

## Findings

There are no BLOCKER, MAJOR or MINOR findings.

### RESIDUE-1: the console prose drops the table's assumption for the 10 ms figure

- **Lenses:** Docs, Conformance.
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:363`.
- **Evidence:** The table row `:355` says "Taking 10 ms as the gap … the buffer would be 128 bytes". The prose says flatly "Under 10 ms, the buffer would be 128 bytes."

  Under dev's 10 ms, the gap is set by a per-pass share that dev does not state. The whole 10 ms is the conservative case, not the derived one.
- **Impact:** None to any figure. A reader of the prose alone may take 128 bytes as derived rather than as an upper bound.
- **Exact fix:** Replace `:363` with "Taking 10 ms as the gap gives 128 bytes." That is eight words, within the style limit.
- **Verification:** Read `:363` against `:355`, and run `check_doc_style.py`.

### RESIDUE-2: a future stage written in the present tense

- **Lenses:** Docs.
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:331`, the last sentence of the fate cell.
- **Evidence:** "Stage 1 already fills `rom` from the flash copy, not the configuration image." Stage 1 is lane 2 and has not been built. Today the split build fills `rom` at configuration (`milan_soc.py:3012, 3018`).
- **Impact:** A reader may take the flash-copy boot as present behaviour.
- **Exact fix:** "From stage 1, `rom` is filled from the flash copy, not the configuration image."
- **Verification:** Read the cell.

### S1 (SUGGESTION): the page does not say that T_svc = 20 ms is owner-approved

- **Lenses:** Conformance, Docs.
- **Where:** `MARK_II_AREA_PLAN.md:351, 359-360`.
- **Evidence:** The page frames both the share and T_svc = 20 ms as "#665's S2b work … not merged". But the cited 6495692075 records the owner's 2026-10-29 approval of 20 ms. PR #810's FR_NFR patch writes "approved by the owner on 2026-10-29".

  What is unmerged is the FR_NFR text and the share, not the approval.
- **Suggested change:** Name the 20 ms as owner-approved on 2026-10-29, with its FR_NFR amendment carried by PR #810. This keeps "dev still proposes 10 ms" as the statement of the document's state.

### S2 (SUGGESTION): link the BIOS memory rows to the row that takes their addresses

- **Lenses:** Docs.
- **Where:** `:328-329`.
- **Evidence:** "Removed, nothing in its place" is consistent with `SPLIT_CONTROL_MEMORY.md:8`. But the split build's `ctrl_memory` builds regions named `rom` and `sram` at the same origins (`ctrl_memory.py:128-129`), which `:331` states.
- **Suggested change:** Add "the split build's `ctrl_memory` takes the `rom` and `sram` origins (row below)", so the two framings read as one.

### S3 (SUGGESTION): the stage table still lists the BIOS removal under stage 1

- **Lenses:** Docs.
- **Where:** `:231` (stage table, row 1, "Removes … BIOS ROM and SRAM, 18 RAMB36 measured") and the lane table's lane 2 scope ("Drop DDR3 and the BIOS ROM").
- **Evidence:** The note at `:235-236` reconciles this with the census. A stage 1 routed measurement will not see those 18 RAMB36 leave.
- **Suggested change:** Add "already gone at the switch-over" in the stage 1 "Removes" cell. The owner's stage wording can stay as it is.

### S4 (SUGGESTION): say that the sub-row LUT figures sit inside the CPU wrapper's 3,249

- **Lenses:** Docs.
- **Where:** `:310, 321, 324, 326-327`.
- **Evidence:** The CPU wrapper row carries 3,249. Other rows also cite children of that wrapper: 227 + 166, 105 + 176 + 104, 225 + 136, and 34 + 55 + 3. Those children are inside the 3,249 (`basis_place_top_excerpt.rpt:12-46`).
- **Suggested change:** One sentence under "LUT figures are the basis's placed rows". For example: "Figures inside the CPU wrapper are part of its 3,249." This stops a reader who sums the column from double counting.

## Per-lens results

```text
[R765] PASS Conformance — docs/design/MARK_II_AREA_PLAN.md:231-236, 281-287, 297-332, 351-370 at 30eb4834 — census fates against D4/D15/D18-D21 (#640 issuecomment-6575277828), REQ-MAC-03, REBOOT_RESET §1; console bound against #665 6495692075/6514866239/6569635407, FR_NFR.md:329,339 and PR #810 state; stage 1 text against #640 issuecomment-6556743957
[R765] PASS RTL — sw/litex/milan_soc.py:218-475, 1896-1988, 2127-2132, 2177-2186, 2878-3018, 3160-3205, 3331-3340 and pinned liteeth/phy/gmii.py@276c9e37 — census clock, IDELAYCTRL/PSCLK, sys4x, CDC (link_status MultiReg, PHY-reset hold), bus and memory-region claims against the generator and pinned LiteEth; no RTL in the diff
[R765] PASS Robustness — docs/design/MARK_II_AREA_PLAN.md:347-370 and receipts/console_arith.out — 24/32/116/128-character boundaries, the bound's condition, the 32x32 over-share case and the loss rule; loopback reset value 0; error answer past the last ctrl_memory bank (milan_soc.py:2997-2999)
[R765] PASS Tests — receipts/census_coverage_rerun_head.out, gate_*.rc, style_round2_delta.out with style_planted_control.out, reader_unaffected.out, gate_pp_resource_check_baseline.log — the census coverage check reproduces PASS; docs gates rc 0; style delta 0 with a caught control; gate-read pages' readers unaffected; no test file in the diff
[R765] PASS Docs — git diff 503bc97c..30eb4834 (four pages) and PR #835 body (equal to the published author-r2 PR-BODY.md but for a final newline) — round 1 F1-F5 and R766-1 F1-F3/R1 resolved at cause; anchors and TOC clean; RESIDUE-1/2 and S1-S4 recorded, none blocking
```

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `MARK_II_AREA_PLAN.md:231-236, 281-287, 297-332, 351-370`; D4, D15, D18-D21; REQ-MAC-03; FR_NFR 3.4.1 and NFR-SCOUT-03; #665 6495692075, 6514866239, 6569635407; #640 6556743957; PR #810 | R765-2 | `30eb4834e0d258668a7bdfece187f9d7d9fccd0b` |
| RTL | CLEAN | `milan_soc.py` `_CRG`, `MilanMAC`, `CtrlMailbox`, `CtrlMemory`, split branches, servo port; `ctrl_memory.py:128-129`; pinned LiteEth `gmii.py` and patches 0002 and 0007 | R765-2 | `30eb4834e0d258668a7bdfece187f9d7d9fccd0b` |
| Robustness | CLEAN | Console UART table and prose `:347-370`; arithmetic receipt; loopback reset; `ctrl_memory` error answer | R765-2 | `30eb4834e0d258668a7bdfece187f9d7d9fccd0b` |
| Tests | CLEAN | Census coverage re-run; docs gates; style delta and planted control; `ctrl_service_bounds` reader strings; `pp_resource_gate.py check-baseline` | R765-2 | `30eb4834e0d258668a7bdfece187f9d7d9fccd0b` |
| Docs | CLEAN | All four branch pages; PR #835 body; the round 1 findings at their cause | R765-2 | `30eb4834e0d258668a7bdfece187f9d7d9fccd0b` |

## Real limits

- **The basis build's full reports stay outside the repository.**
  - The 32-IDELAYE2 count, the IDELAYCTRL's `REFCLK` and the `PSCLK` net are taken from the author's recorded digest of `alinx_ax7101.v` (`basis_sources.txt`), not re-read.
  - The hierarchy, the CSR map and the placed rows were checked against the published, digest-verified excerpts.
- **The evidence-tree commit `5f8bd017` is unsigned.** Integrity rests on the matching `MANIFEST.json` and `SHA256SUMS` digests, which this round verified.
- **LiteX is not installed here.**
  - The LiteEth GMII PHY was read from the pinned upstream revision.
  - LiteDRAM's IDELAYE2 placement was not re-read.
- **No firmware build was run.** The `ctrl_service_bounds` arm was not executed. Its independence from the changed line is shown by string match, and its execution receipt is the author's.
- **Not run:** no manager source bank, and no builder, native, Verilator or Yosys bank.
- **Not exercised:** physical calibration and hardware. Field skips are not hardware proof.
- **Hosted contexts were still running when read.** They are not relied on.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head. When last read, 4 of 21 runs had completed with success, and 17 were in progress or queued.
- The current-dev merge-candidate validation (builder and native banks) at the merge turn, on source base `503bc97c`, with live dev equal to it.
- Carry RESIDUE-1 and RESIDUE-2 to the residue checklist. Route S1 to S4 to the author at their discretion.
- Publish this report and the files in `MANIFEST.sha256`.

R765-2 FINISHED

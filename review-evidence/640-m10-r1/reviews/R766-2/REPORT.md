[R766] NEGATIVE - exact head 30eb4834e0d258668a7bdfece187f9d7d9fccd0b

# R766-2: external review of PR #835 (issue #640), round 2

- Head: `30eb4834e0d258668a7bdfece187f9d7d9fccd0b`, tree `81f7e650087b8445b45b6fec2f1c8921f7e48626` (verified in the review clone).
- Base: `503bc97cd4f24ad07596c17e7188f2024617972d` (live `dev` at review time).
- Round 2 delta: `3f8ed303..30eb4834`, five commits. All five are docs only (`git diff --raw`): `docs/design/MARK_II_AREA_PLAN.md` and one line of `docs/design/MAILBOX_SPLIT.md`.
- Commit form: each of the five messages is one line with no trailers.
- Verdict: NEGATIVE on one MINOR (F1).
  - F1 is the remaining part of R765-1-F1's cause: the plan still disagrees with itself about which lane removes the BIOS memory, and about what takes its place.
  - Every other round 1 finding is resolved at its cause, including the residue.
  - RTL, Robustness and Tests are CLEAN. Conformance and Docs stay UNCLEAN on F1 alone.

## How this round reconstructed the task

1. I read `AGENTS.md`, `CONTRIBUTING.md` (by reference) and the issue #640 body.
2. I read the owner and manager comments the delta rests on:
   - D18 to D21: [issuecomment-6575277828](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6575277828);
   - the staged LiteX removal: [6545999204](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545999204);
   - the stage 1 probes: [6555550136](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6555550136) and [6556743957](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6556743957);
   - the 65 µs decision: [6558021030](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558021030);
   - the author's round 2 TAKEN and REVIEW READY: [6577649057](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6577649057) and [6578986708](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6578986708).
3. I read the #665 comments the page cites: 6569635407, 6514866239 and 6495692075.
4. I checked PR #810's state: OPEN, against `dev-soft-core`, not merged.
5. I read the round 2 delta in full (`receipts/delta_3f8ed303_30eb4834.diff`) and checked every new claim against these sources:
   - `sw/litex/milan_soc.py`, `sw/litex/ctrl_memory.py` and `sw/litex/liteeth-ax42-ext-reset.patch`;
   - `sw/firmware/milan_baremetal/milan_baremetal.c`;
   - `docs/reference/FR_NFR.md` 3.4.1, `REQUIREMENTS.md` REQ-MAC-03, `docs/design/SPLIT_CONTROL_MEMORY.md` 4 and 5, and `docs/design/REBOOT_RESET.md` 1;
   - the author's published round 2 evidence.
6. I read the round 1 findings (R765-1 and R766-1 on PR #835) only after that independent pass. I then checked each one at its cause, in the table below.
7. I read no other reviewer's round 2 report, no private author material, and no lane scratchpad.

## Executed checks (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| Published evidence `review-evidence/640-m10-r1/author-r2` at `5f8bd017`: every file's bytes against `MANIFEST.json`; every `SHA256SUMS` entry against the manifest's original hash (17 logs are path-redacted at publication) | 141 files, 0 mismatches, 0 missing | `receipts/verify_evidence.out`, `scripts/verify_evidence.py` |
| The author's `census_coverage.py`, read before running, on the head page | rc 0, PASS. 165 objects (55 tree nodes, 88 CSR entries, 14 placed CPU children, 9 split-only parts, less one first-party datapath). Byte-identical to the published `census_coverage.out` | `receipts/census_coverage_head.out` |
| The same check on the round 1 page (`3f8ed303`), as a control | rc 1, 9 MISSING. These are exactly the IDELAYCTRL, `loopback`, `link_status`, three `ctrl_memory` parts and three `ctrl_mbx` parts | `receipts/census_coverage_3f8ed303.out` |
| Independent reading of the published basis hierarchy excerpt | 1 `IDELAYCTRL`, under `crg.idelayctrl`. All 32 `IDELAYE2` are under `ddrphy`; `milan_mac` has none. `milan_mac` is `LiteEthPHYGMII`. Placed rows: `ioBus_to_peripheral_bus_cc` 166 LUTs, `dma_filter_down_to_unified_mBus_cc` 104 | `basis_soc_hierarchy.txt`, `basis_place_top_excerpt.rpt` in the author's evidence |
| Console table arithmetic, recomputed | 86.806 µs per character. A 2.0 ms gap needs 24 and gets 32 B (2.778 ms). A 10 ms gap needs 116 (115 chars = 9.983 ms, 116 = 10.069 ms) and gets 128 B (11.111 ms). All match the page | `receipts/console_arith.out`, `scripts/console_arith.py` |
| `check_doc_style.analyze()` on head findings absent at the base, for the round 2 pages against `3f8ed303` and the four PR pages against `503bc97c` | 0 new findings | `receipts/style_delta_r2.out`, `receipts/style_delta_pr.out`, `scripts/style_delta.py` |
| `check_doc_style.py --selftest`; `docs_check.py` | rc 0; rc 0 (0 findings, 213 md files) | `receipts/gate_*` |
| `gen_toc.py --check`, `--verify-anchors`, and `check_em_dash.py --base 503bc97c`, with the pinned renderer in a disposable venv | rc 0 for all three: TOC OK; 586 cross-page fragments reproduced; 0 em-dash findings over 225 added lines | `receipts/gate_venv_*` (the first attempts without the renderer exited 2 with "renderer not installed" and are kept as `receipts/gate_python3__I_scripts_gen_toc_*` and `..._check_em_dash_*`) |
| In-page anchors the delta adds or uses (`#litex-block-census`, `#console-uart`, `#mark-ii-decisions`, `#stage-1-boot-and-bus`); cross-page `SPLIT_CONTROL_MEMORY.md#5-fit`, `REBOOT_RESET.md#1-the-decision`, `FR_NFR.md#341-...` | All target headings present: `MARK_II_AREA_PLAN.md:262, 292, 337, 398`, `SPLIT_CONTROL_MEMORY.md:138`, `REBOOT_RESET.md:24`, `FR_NFR.md:336` | heading search at the head |
| `git diff --check 503bc97c HEAD` | rc 0, clean | `receipts/gate_git_diff_*` |
| Gate-read reader of `AREA_BUDGET.md`: `syn/ooc/pp_resource_gate.py check-baseline` | rc 0, "baseline PASS: 3 endpoints" | `receipts/reader_check_baseline.*` |
| Gate-read reader of `MAILBOX_SPLIT.md` (`ctrl_service_bounds.py`), statically | 13 reader-anchored lines, identical at `3f8ed303` and the head. The single changed line holds none of the reader's keys. The author's published run is 47 checks, 0 failures, 38/38 planted controls | `receipts/service_bounds_static.out`, `scripts/service_bounds_static.py`; author `gates/logs/reader_service_bounds.log` |
| Exact-head hosted contexts, snapshot | Completed with success: `wire-accountability`, `docs-check-no-git`, `changes`, `bdd-conformance`. The rest were in progress or queued at the snapshot. No conclusion is drawn from them | `receipts/hosted_checks_30eb4834.tsv` |
| Restore | Every tracked blob was byte- and mode-identical to the index after the probes (1,460 blobs, 0 mismatches). Worktree and index match HEAD. Tree `81f7e650`. All six gitlinks are unchanged. My `__pycache__` directories were removed. Nothing is untracked or ignored | `receipts/restore_check.out`, `scripts/restore_check.py` |

## Round 1 findings at their cause

| Finding | State at `30eb4834` | Evidence |
|---|---|---|
| R765-1-F1: BIOS ROM and SRAM at stage 1, but lane 1's split already drops them; the split's LiteX parts have no rows | **Retained in part, as R766-2-F1.** Resolved: the census rows now say "Switch-over, lane 1" (`MARK_II_AREA_PLAN.md:328-329`). A note follows the stage table (`:235-236`). The `ctrl_memory` and `ctrl_mbx` parts have rows (`:331-332`). Not resolved: lane 2's scope still says it drops the BIOS ROM (`:427`). The BIOS rows say "nothing in its place", though the split builds `ctrl_memory`'s `rom` and `sram` at the same origins. R765-1-F1's required outcome asked for those banks to be named in their place | `milan_soc.py:3168-3176`, `:2971-3018`; `ctrl_memory.py:128-129` |
| R765-1-F2: IDELAYCTRL removed with DDR3, but Ethernet builds it and its clock is the audio MMCM's `PSCLK` | **Resolved.** It has its own row under `_CRG`, stage 3 (`:313`). Stage 1 removes neither. The fate keeps the 200 MHz `PSCLK` for the MMCM and the servo, and builds an IDELAYCTRL only if the stage 2 MAC uses an `IDELAYE2` | `milan_soc.py:402`, `:421`, `:466-472`, `:3335`; hierarchy: 32 of 32 `IDELAYE2` under `ddrphy` |
| R765-1-F3 / R766-1-F1 (MilanMAC CSRs): `link_status` and `loopback` have no row | **Resolved.** `link_status` (`:322`): three fields feed the same three datapath inputs; the firmware writes them from MDIO; link and duplex get a 2-flop crossing (REQ-MAC-03). `loopback` (`:323`): no writer anywhere in the repository (`git grep milan_mac_loopback` finds none), and its reset value is 0 | `milan_soc.py:1896-1935`, `:1958-1988`, `:2184`; `milan_baremetal.c:1064-1080` |
| R766-1-F1 (split parts, LiteX fate): the BIOS SRAM's fate names a LiteX block; `ctrl_memory` and `ctrl_mbx` have no rows | **Resolved by its own terms.** `ctrl_memory` and `ctrl_mbx` have their own rows with stage 3 and non-LiteX fates. "No fate below is a LiteX block" (`:306`) holds. The tick is the millisecond `ms_tick`. No firmware reads a `ctrl_mbx` CSR (`git grep` finds none). See F1 for the BIOS rows' wording | `milan_soc.py:2895-2965`, `:2972-3001` |
| R765-1-F4 / R766-1-F3: "311 of 311" has no public source | **Resolved.** The figure is gone. "311" occurs on no changed page except an unrelated FF count at `:657`. The new text (`:284-287`) states only what [6556743957](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6556743957) shows: ENTITY_AVAILABLE, and all 33 descriptors byte-identical | Comment body checked: "33 descriptors" and "ENTITY_AVAILABLE" present, "311" absent |
| R765-1-F5 / R766-1-F2: the console bound rests on the unmerged S2b share and T_svc = 20 ms, against dev's 10 ms | **Resolved.** The page states all of: the share and 20 ms are S2b work, PR #810, not merged; dev's FR_NFR.md proposes 10 ms; under 10 ms the buffer would be 128 B; 32 B holds only while passes fit the share; derive the buffer again if the share changes; and the 32x32 estimate of 1.7 to 5.9 ms over the share, where the loss rule applies (`:351-369`) | `FR_NFR.md:329`, `:339`; #665 6569635407 line "longest pass, 2.0 ms share: 1.7 / 3.0 / 5.9"; PR #810 OPEN; arithmetic receipt |
| R766-1-R1 (residue): "They" ambiguous in the event record | **Resolved.** The line now reads "Its sources also include fabric timer expiries, tagged by arm." (`MAILBOX_SPLIT.md:151`). Shortening "tagged with their arm" to "tagged by arm" keeps the meaning and fits the 10-word limit, which the exact fix (11 words) would have broken | style receipt |
| R765-1-S1 / R766-1-S1: unsourced netlist identifier | **Taken and justified.** Comment 6569635407 carries 3,948 and 3,543 but not `7ee512a1`. The page now cites only the comment (`:167`) | search of the fetched comment |
| R765-1-S2, S3; R766-1-S2, S3 | Not taken. They are optional, and the author gave reasons in the published handoff. No coverage effect | - |

## Findings

### R766-2-F1 MINOR: the plan still disagrees about which lane removes the BIOS memory and what takes its place

- **Lenses:** Conformance, Docs. These are R765-1-F1's lenses; this is the part of its cause that remains.
- **Where:**
  - `docs/design/MARK_II_AREA_PLAN.md:427`, the lane 2 scope: "LiteX stage 1, lever 1 | Drop DDR3 and the BIOS ROM; ...".
  - `:328`, the BIOS ROM fate: "Removed, nothing in its place: the split build runs no BIOS ...".
  - `:329`, the BIOS SRAM fate: "Removed, nothing in its place: the split build builds none".
- **Authority and evidence:**
  - The census at `:328-329` and the note at `:235-236` place the BIOS memory's removal at the switch-over, lane 1.
  - Lane 2's scope, which depends on lane 1, still lists "the BIOS ROM" as something lane 2 drops. The stage table's owner wording is reconciled by the note; the lane sequence table is not.
  - The split build rebuilds both regions under the same names at the same origins. `ctrl_memory.py:128-129` defines `ROM = Region("rom", 0x0000_0000, ...)` and `RAM = Region("sram", 0x1000_0000, ...)`. `milan_soc.py:3005-3014` refuses any other origin and adds them with `add_ctrl_memory`. The page's own row at `:331` lists them as "LiteX `wishbone.SRAM` banks for `rom` and `sram`".
  - So "the split build builds none" is not true of `sram`. "nothing in its place" is not true of either memory. What the split drops is the BIOS's integrated ROM and SRAM and the BIOS itself (`milan_soc.py:3168-3176`).
  - R765-1-F1's required outcome was that these rows say the switch-over removes them "with `ctrl_memory`'s banks in their place".
- **Impact:**
  - The census is the record D19 relies on, and the lane table is the next lanes' public scope.
  - A stage 1 lane reading `:427` is told to drop a ROM that lane 1 has already removed.
  - A reader of `:329` is told the split has no `sram`, while the split's writable firmware memory is exactly that region (45,776 B needed at 1x1, `SPLIT_CONTROL_MEMORY.md:147`).
- **Required outcome:**
  - The BIOS rows say the switch-over removes the BIOS and its integrated ROM and SRAM, and that `ctrl_memory`'s `rom` and `sram` banks hold those regions until stage 3 (the row at `:331`). From stage 1, the boot loader fills `rom` (D18).
  - Lane 2's scope says it drops DDR3 and fills `rom` from the flash copy. It no longer says it drops the BIOS ROM, or it says the BIOS memory already went at lane 1.
  - One possible wording, not prescribed:
    - `:328` fate: "Removed at the switch-over: the split runs no BIOS. `ctrl_memory`'s `rom` banks hold the reset entry until stage 3 (row below). From stage 1 the boot loader fills them (D18)".
    - `:329` fate: "Removed at the switch-over: the split builds no BIOS SRAM. `ctrl_memory`'s `sram` banks take its address until stage 3 (row below)".
    - `:427` scope: "Drop DDR3 (lane 1 already drops the BIOS memory); ...".
- **Verification:** Read `:328-329`, `:331` and `:427` against `ctrl_memory.py:128-129` and `milan_soc.py:3005-3014`, `:3168-3176`. Re-run the author's `census_coverage.py` to confirm the rows still map.

## Suggestions (non-blocking)

- **R766-2-S1 (Conformance, Docs), `MARK_II_AREA_PLAN.md:351` and `:359-363`.** The cited [#665 issuecomment-6495692075](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6495692075) records T_svc = 20 ms as an owner decision of 2026-10-29, "approved". Only its FR_NFR amendment rides on the unmerged S2b work.
  - "The share and the 20 ms budget come from S2b" can be read as 20 ms being unapproved. Consider: "The owner approved T_svc = 20 ms on 2026-10-29. Its FR_NFR amendment and the share are S2b's unmerged work."
  - The page gives the 10 ms alternative, but a pass over the share under the approved 20 ms is the more likely case. By the page's own rule that gives 231 characters and a 256-byte buffer (`receipts/console_arith.out`). One row would close it.
  - R766-1-F2 also named NFR-SCOUT-03 (`FR_NFR.md:329`) beside 3.4.1. The page cites 3.4.1 only, which is enough.
- **R766-2-S2 (Docs), `:279-287` and `:349`.** The stage 1 probe, the DMA hang, the SoC-bus result and the console-loss figure were all measured on the Arty A7-100T at 80 MHz, the AX7101's FPGA. The probe comment says the AX7101 is not verified. Naming the board in one sentence would stop a reader taking these as AX7101 silicon results.
- **R766-2-S3 (RTL, Docs), `:319`.** `MilanMAC` carries first-party Migen glue that is in no census row, because it is neither a tree node nor a CSR. It includes:
  - the `KL_link_guard` liveness toggles;
  - the `macsys` reinit reset with its eth-first release;
  - the guard's `eth_rst` into the PHY clock domains, deliberately not the PHY pin;
  - the keep/`last_be` conversion.

  Silicon wedges that the code comments date to 2026-07-19 and 2026-07-24 rest on these. When the stage 2 MAC replaces LiteEth, they must be carried over. A clause in the Ethernet row's fate would keep them from being lost (`milan_soc.py:1712-1760`, `liteeth-ax42-ext-reset.patch`).

## Residue

None in this delta. R766-1-R1 is resolved as above. The delta adds no source comment, so the comment rule has nothing to apply to.

## Per-lens results

| Lens | Result | Evidence |
|---|---|---|
| Conformance | MINOR F1 open | D18 to D21 and D19's census applied to `MARK_II_AREA_PLAN.md:231-236`, `:279-332`, `:337-373` and `:405-430`. Checked against `milan_soc.py` (`_CRG`, `MilanMAC`, `CtrlMailbox`, `CtrlMemory`, the BIOS build switch), `ctrl_memory.py`, FR_NFR 3.4.1, REQ-MAC-03, and the #665 and #640 comments cited. Every other claim in the delta was verified |
| RTL | PASS | The delta changes no RTL. Its RTL-bearing claims were verified at the head: the `idelay` clock and `IDELAYCTRL` built for DDR3 or Ethernet; `PSCLK` and the servo's `ps_clk_i` from `audio_ps_clk` (`milan_soc.py:402`, `:421`, `:3335`); 32 of 32 `IDELAYE2` under `ddrphy`; `link_status`'s 2-flop crossing of link and duplex only (`:1984-1988`); `loopback`'s reset value 0 path (`:1896-1935`); the PHY reset pin driven only by the start-up pulse and the CSR storage the reboot hold sets, `ext_reset` deliberately off the pin (`:2116-2132`, the AX42 patch); the two `sys4x` clocks only with DRAM (`:457-463`); placed rows 166 and 104 |
| Robustness | PASS | The console bound's failure paths are now stated: share not met, dev's 10 ms, 32x32 over the share, and the loss rule (`:351-369`). The arithmetic was recomputed. The `loopback` removal is safe at its reset value, and the PHY reset fate keeps both pin uses. R765-1-F5's Robustness cause is resolved |
| Tests | PASS | The coverage check was reproduced at the head (PASS) and fails on the round 1 page with exactly the 9 named objects, so it can fail. The `AREA_BUDGET.md` reader passes at the head. The `MAILBOX_SPLIT.md` reader's 13 anchored lines are unchanged and the single changed line holds none of its keys; the author's run is 47/0 with 38/38 controls. Style, TOC, anchors, em-dash, docs_check and diff-check are all rc 0 |
| Docs | MINOR F1 open | Both changed pages were read in full over the delta. Style is 0 new findings, anchors resolve, and the residue fix is applied. F1 is a census fate and lane-scope inconsistency, and it is not wording-only. See the Conformance row |

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R766-2-F1) | `docs/design/MARK_II_AREA_PLAN.md:231-236, 279-332, 337-373, 405-430`; `docs/design/MAILBOX_SPLIT.md:151`; `sw/litex/milan_soc.py:215-472, 1591-2192, 2878-3018, 3160-3215, 3326-3340`; `sw/litex/ctrl_memory.py:128-129`; `docs/reference/FR_NFR.md:329, 336-355`; `REQUIREMENTS.md:307`; #640 comments 6575277828, 6556743957, 6555550136; #665 comments 6569635407, 6514866239, 6495692075; PR #810 state | R766-2 | `30eb4834e0d258668a7bdfece187f9d7d9fccd0b` |
| RTL | CLEAN | `sw/litex/milan_soc.py:396-472, 1888-1990, 2110-2170, 2895-2965, 3335`; `sw/litex/liteeth-ax42-ext-reset.patch`; `hdl/common/csr/milan_csr.sv:885-895`; author evidence `census/basis_soc_hierarchy.txt`, `basis_place_top_excerpt.rpt`, `basis_csr.csv` | R766-2 | `30eb4834e0d258668a7bdfece187f9d7d9fccd0b` |
| Robustness | CLEAN | `MARK_II_AREA_PLAN.md:337-373` (console table and text), `:319`, `:322-323`; `receipts/console_arith.out` | R766-2 | `30eb4834e0d258668a7bdfece187f9d7d9fccd0b` |
| Tests | CLEAN | `receipts/census_coverage_head.out`, `receipts/census_coverage_3f8ed303.out`, `receipts/reader_check_baseline.log`, `receipts/service_bounds_static.out`, `receipts/style_delta_*.out`, `receipts/gate_*`; author `gates/logs/reader_service_bounds.log` (verified against the publication manifest) | R766-2 | `30eb4834e0d258668a7bdfece187f9d7d9fccd0b` |
| Docs | UNCLEAN (R766-2-F1) | `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/MAILBOX_SPLIT.md` over `3f8ed303..30eb4834`; the four PR pages over `503bc97c..30eb4834` for style and em-dash; anchor and TOC gates | R766-2 | `30eb4834e0d258668a7bdfece187f9d7d9fccd0b` |

Code that the delta does not touch keeps its round 1 lens verdicts unless the delta changes what it depends on. This delta changes only the two pages above.

## Real limits

- **Basis build sources.** The basis build's `litex.log`, `alinx_ax7101.v` and the full hierarchical placement report are not published. I checked the published excerpts and the recorded digests for consistency with each other, but not against the originals.
  - The count of 32 `IDELAYE2`, all DDR3's, rests on the hierarchy excerpt. The author's netlist count is recorded in `basis_sources.txt` but not reproducible here.
- **Coverage rules.** The census coverage check maps objects by rules the author wrote. I read every rule and judged it sound. An object outside the hierarchy, the CSR map and the placed CPU children (for example `MilanMAC`'s Migen glue, S3) is outside its reach by design.
- **Service-bounds reader.** I did not execute `ctrl_service_bounds.py`, because this clone has no initialised submodules. I proved statically that the delta touches none of its inputs, and relied on the author's published run.
- **Packet signature.** The evidence commit `5f8bd017` is unsigned, and the tree holds no signature file. Packet integrity was checked through `MANIFEST.json` and `SHA256SUMS` only.
- **Hosted contexts.** The exact-head hosted contexts were mostly in progress or queued when I took the snapshot. No hosted or act result is claimed.
- **Hardware.** I ran no hardware. Physical calibration is NOT RUN. The probe figures the page cites are the author's and the manager's bench reports, not hardware proof from this round.
- **No manager source bank.** None runs at this head, and none is claimed or inferred.

## Pending manager duties

- Carry R766-2-F1 to the author. A fix round must be re-reviewed for Conformance and Docs at its new head.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn (source base `503bc97c`), and link its receipts on the PR.
- Own hosted and act acceptance at the exact head. Most contexts were still running at this review's snapshot.
- Publish this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

R766-2 FINISHED

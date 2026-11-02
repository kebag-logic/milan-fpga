[R766] NEGATIVE - exact head 3f8ed303e01285f1bad0641f4ebc05764f162467

# R766-1: external review of PR #835 (issue #640), Mark II charter follow-up

- Exact head: `3f8ed303e01285f1bad0641f4ebc05764f162467`, tree `580d876cd9f7f973d1407d3da5759a23822a24d0`.
- Base: dev `503bc97cd4f24ad07596c17e7188f2024617972d`, the PR #828 merge; live dev is the same commit.
- Delta: seven commits, four Markdown pages, 194 lines added and 50 removed. The pages are `docs/design/MARK_II_AREA_PLAN.md`, `docs/design/AREA_BUDGET.md`, `docs/design/MAILBOX_SPLIT.md` and `docs/findings/README.md`.
- Context used, in this order: AGENTS.md and CONTRIBUTING.md; docs/README; #640's body; the decision comments the PR cites; the author's TAKEN comments on #640, which give the interpreted scope; `docs/reference/FR_NFR.md`; `sw/litex/milan_soc.py`; the diff and its history; the public evidence tree at `b4578f5c`. That tree holds two author passes and no reviewer material.
- Prior public review findings on PR #835: none. Before this round the PR carried only two review-start notices, one for the internal round and one for this round. No other reviewer's report was read.

Verdict: NEGATIVE. Three MINOR findings are open, under the Conformance, RTL and Docs lenses. The Tests and Robustness lenses are clean.

## Findings

### R766-1-F1 MINOR: the LiteX block census leaves LiteX-built blocks without a stage and fate, and names a LiteX block as a fate

- **Lenses:** Conformance, RTL, Docs.
- **Where:**
  - `docs/design/MARK_II_AREA_PLAN.md:289-317`, the census;
  - `:310`, the `MilanMAC` row;
  - `:316`, the BIOS SRAM row;
  - `:382`, D19's consequence, "no LiteX block remains".
- **Authority and evidence:**
  - D19 ([#640 issuecomment-6575277828](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6575277828)) says every LiteX peripheral is removed.
  - The author's TAKEN scope covers "every LiteX block the shipping 1x1 SoC builds". The page says "Each block below names its stage and its fate".
  - At this head, `sw/litex/milan_soc.py` builds two LiteX CSRs inside `MilanMAC` that no census row names (`receipts/census_probe.txt`):
    - `:1896` `self.loopback = CSRStorage(...)`, the MAC-TX to MAC-RX loopback switch.
    - `:1958` `self.link_status = CSRStorage(...)`, MAC_STATUS 0x110. It feeds the datapath's link, speed and duplex inputs (REQ-MAC-03): `:2184` `i_i_mac_speed = self.link_status.fields.speed`, with `:1986-1987` crossing link and duplex into the Milan clock. The firmware writes it from the MDIO result (`sw/firmware/milan_baremetal/milan_baremetal.c:1080`).
  - The `MilanMAC` row (`:310`) lists only `KL_gptp_gmii_launch`, `KL_mac_rmon_events` and the `ICAPE2` port. The MDIO row covers the bit-bang pair only. No row names the link-status register or the loopback switch.
  - The BIOS SRAM row (`:316`) gives its fate as "Replaced by the firmware's own block RAM banks (`ctrl_memory`)". Those banks are LiteX blocks: `CtrlMemory` builds LiteX `wishbone.SRAM` banks behind a LiteX `wishbone.Decoder` (`milan_soc.py:2991`, `:3000`). The census gives `ctrl_memory` no stage or fate of its own.
  - The same holds for the mailbox's LiteX `EventManager` and its `ctrl_mbx` CSR bank (`milan_soc.py:2957-2959`), which the split placement adds.
  - So the required shape, removed or a named first-party replacement, is not met for these blocks. D19's consequence, "no LiteX block remains", is not shown.
- **Impact:** The census is the plan's record that D19 is complete, and it is not. A stage 3 lane working from the census has no named home for REQ-MAC-03's link, speed and duplex inputs. It may also keep LiteX block RAM banks while the page reports none left.
- **Required outcome:**
  - Every LiteX-built block on the shipping 1x1 path has a census row, a stage and a fate. That includes the `link_status` register, which carries the datapath's link, speed and duplex inputs and their crossing, and the `loopback` switch.
  - The BIOS SRAM's fate names a first-party block, or `ctrl_memory` gets its own stage and fate.
  - The page states whether the census also covers the blocks the split placement adds (`ctrl_memory`, the `ctrl_mbx` event manager and CSR bank). If it does not, it states where they are tracked.
- **Verification:** Re-run `scripts/census_probe.py` against the corrected head. Every basis row should show "as a block". Check that the BIOS SRAM row's fate is a first-party block or that `ctrl_memory` has its own row.

### R766-1-F2 MINOR: the console UART derivation rests on T_svc = 20 ms and the 2.0 ms per-pass share, but the page does not say these are not on dev or that dev's requirements still say 10 ms

- **Lenses:** Conformance, Docs.
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:336`, the "Worst-case gap" row, and `:338-345`, the buffer and its rule.
- **Authority and evidence:**
  - The 32-byte buffer follows from a 2.0 ms worst-case gap. The page gives that gap as "The share, 18 ms / 9 passes (#665 ...), under T_svc = 20 ms (#665 ...)".
  - At this head the normative text says otherwise (`receipts/source_checks.txt`):
    - `docs/reference/FR_NFR.md:339`: "Proposed project budget: `T_svc = 10 ms`."
    - `:329`, the NFR-SCOUT-03 row: "T_svc = 10 ms, proposed for owner approval".
  - The gate-read `MAILBOX_SPLIT.md` service figures print "Neither fits T_svc = 10 ms" (`receipts/ctrl_service_bounds_arm.txt`).
  - "Per-pass share" appears nowhere in the current docs except this new row. The share and the 20 ms approval come from the S2b lane (PR #810), which has not merged.
  - The PR body says so under "Known limitations". The author's handoff also notes that a different gap would change the buffer. The page, the durable artifact, says neither.
  - AGENTS.md section 2 requires a conflict between a decision and a requirement to be published, not resolved silently.
- **Impact:** A cold reader of the plan sees a 20 ms budget and a 2.0 ms share stated as settled, while FR_NFR says 10 ms proposed. If the share lands differently, nothing on the page signals that the 32-byte figure must be derived again.
- **Required outcome:** The page states three things:
  - the 2.0 ms share and T_svc = 20 ms are #665 decisions carried by the unmerged S2b lane;
  - FR_NFR 3.4.1 and NFR-SCOUT-03 still state 10 ms as proposed at this revision;
  - the buffer size is derived again if the share changes.
- **Verification:** Read the corrected rows against `FR_NFR.md:329,339` at the reviewed head.

### R766-1-F3 MINOR: "311 of 311 reads were answered" has no public source

- **Lenses:** Docs, Conformance.
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:281`.
- **Authority and evidence:**
  - The paragraph cites the stage 1 silicon probe, [#640 issuecomment-6556743957](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6556743957). That comment gives "3 issued, 0 acked, 3 abandoned" for the DMA-port route but no read count for the SoC-bus route.
  - None of the 130 comments on #640 contains "311 of 311" (`receipts/source_checks.txt`).
  - The author's public handoff traces the figure to the probe's own report, which is not published.
  - AGENTS.md section 2 says a cold reviewer must be able to reconstruct the work from GitHub and the repository alone. The scope also requires every claim to cite a source.
- **Impact:** A measured figure that supports the "masters use the SoC bus" rule cannot be checked.
- **Required outcome:** The 311-of-311 count is published where the page can cite it, for example on #640, and the page cites it. Otherwise the figure is removed and the page keeps only what the cited comment states.
- **Verification:** Open the cited source and find the count.

### R766-1-R1 RESIDUE: an ambiguous pronoun in the event-record bullet

- **Where:** `docs/design/MAILBOX_SPLIT.md:151`.
- **Problem:** In "The gPTP plane publishes the latter until #665 lane F6. They also include fabric timer expiries, tagged with their arm.", "They" can be read as the grandmaster changes.
- **Exact fix:** Replace "They also include fabric timer expiries, tagged with their arm." with "Its sources also include fabric timer expiries, tagged with their arm."
- This is wording only. It changes no figure or claim.

### Suggestions

These are optional and do not affect the verdict.

- **R766-1-S1, Docs:** `MARK_II_AREA_PLAN.md:167` names the netlist `VexiiRiscvLitex_7ee512a1cb1c336731b7f28188c9814f`. The cited #665 comment states 3,948 and 3,543 but not that identifier. Cite a public source for it, or drop it.
- **R766-1-S2, Docs:** Lever 4 is now worth 0, but two parts of the page still read as if it removes a core:
  - its "Why" cell (`:193`) still argues that one core adds boot, capture and NVM duties;
  - lane 7 (`:403`) is a zero-saving lane that gates lanes 8 and 9.

  Consider recasting lane 7 as the 32x32 service-bound check, which is what remains of it. That needs the owner, since the cell is the owner's text.
- **R766-1-S3, Conformance:** The stage 1 probe ([issuecomment-6555550136](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6555550136)) measured -3,758 LUT at one recipe, against lever 1's ~1.0k credit. The plan cites that probe for other facts. Recording its area figure beside the lever 1 credit would help whoever measures stage 1.

## Focus checks

1. **Lever 4 accounting:** holds.
   - `milan_soc.py:4298` refuses any `--cpu-count` other than 1 for the bare-metal profile, and `--ctrl-mailbox` adds no CPU (`:3172-3205`). So the split CPU replaces the SoC CPU, and adding 3,948 on top of 3,249 was a double count.
   - Every derived figure recomputes from the cited rows and appears verbatim on the page, 24 of 24 checks (`receipts/recompute.txt`):
     - the chain: 34,223, then 30,974 and +699;
     - after levers 1 to 3: 27,224 by both chains;
     - the overstatement: 301, about 0.3k;
     - the running totals: ~30.0k, ~29.0k, ~27.2k, ~27.2k, ~26.2k, ~21.0k;
     - the 1x1 range: 19,774 to 22,374, shown as 19.8k to 22.4k;
     - 32x32: 21.75k, ranging 18.5k to 25.45k, a 1.75k miss.
   - A two-value mutant of the page is caught (`receipts/recompute_mutant.txt`).
   - No stale 34.2k, 20.7k, 21.45k, 26.9k or 1.45k remains outside history.
   - The end point after lever 4 is unchanged at 27,224, as claimed.
2. **LiteX block census:** not complete; see F1.
   - Every other block `milan_soc.py` builds on the basis path has a row with a stage and a fate (`receipts/census_probe.txt`). The sub-row names match the hierarchy the repository's resource map records for the same CPU wrapper (`docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md`).
   - The fates are backed at this head:
     - `timer0` has one reader, `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c:84-85,264-267`;
     - no firmware reads `ctrl_*` or `identifier`;
     - the split firmware polls, since `CTRL_MBX_WFI` is a platform opt-in;
     - the processor has three masters, `milan_desc_mem`, `milan_resp_mem` and `milan_nvm_mem`;
     - no LED or GPIO block exists; `user_led0` is driven from `milan.identify`.
3. **UART:** the arithmetic holds; the authority statement is missing (F2).
   - The UART is first-party, transmit and receive only, with no RTS/CTS, as D20 says.
   - The line is 115,200 baud, which is `milan_soc.py:4255`'s default. A character takes 86.806 µs.
   - The figures recompute: at most 24 completions in any 2.0 ms window; 32 bytes as the next power of two; 2.778 ms of coverage.
   - The measured loss (17 of 300 lines at 22 characters, 0 of 300 at 14) matches the cited comment.
4. **Stage 1:** holds, apart from the unsourced 311 count (F3).
   - D18 is cited correctly. The DMA-route hang is stated as a measurement with its cause not established.
   - D21 matches the manager's decision of 2026-11-02, point by point.
   - `QSPI_FLASHBOOT.md` is not in the delta. Its `#layout-baremetal---shipping-ax7101` anchor resolves.
   - No "layout unchanged" or open decision 4 text remains at the head.
5. **#828 residue from #495:** holds.
   - `AREA_BUDGET.md:129` and `MAILBOX_SPLIT.md:13` (now `:22`) are exact.
   - `AREA_BUDGET.md:180` keeps the exact text's content split into two sentences, for the 10-word limit.
   - `findings/README.md:26` now reads "the gap to NFR-RES-01's former 60 % target". The F record's gap of 11,917 makes the "tenth" still true.
   - The event record and the fabric paragraph say "until #665 lane F6".
   - The rewritten `MAILBOX_SPLIT.md` status paragraph keeps its content, apart from dropping the word "bare-metal".
   - The items not taken are listed in the PR body.
6. **Style and citations:**
   - Every changed block passes the style analyser (`receipts/style_probe_changed_blocks.txt`).
   - The em-dash, table-of-contents, anchor and path gates pass.
   - Every in-page and cross-page fragment resolves (`receipts/anchor_probe.txt`). A mutant is caught (`receipts/anchor_probe_mutant.txt`).
   - Prose numbers are decimal.
   - Citations are complete except for F2 and F3.
   - Comment rule: no source file is in the delta, so there is no new instance.

## Per-lens results

| Lens | Result | Artifact at the head | What was checked |
|---|---|---|---|
| Conformance | UNCLEAN: F1, F2, F3 | `MARK_II_AREA_PLAN.md:150-245,259-345,378-385` | Against D18 to D21 (issuecomment-6575277828), the owner's lever tables, FR_NFR 3.4.1 and NFR-SCOUT-03 |
| RTL | UNCLEAN: F1 | `MARK_II_AREA_PLAN.md:287-320` against `sw/litex/milan_soc.py` at 3f8ed303 | One hart (`:4298`), the CPU clock crossing (`:3250-3256`), IDELAYCTRL's conditions (`:466-472`), the three masters (`:3582,3637,3747`), `MilanMAC`'s CSRs (`:1896,1958,2184`), `CtrlMemory` (`:2973-3019`), `milan_axil_cdc` (`:802`) |
| Robustness | CLEAN | `MARK_II_AREA_PLAN.md:322-346` and `:259-285` | The 23 and 24 character boundary; overflow beyond the bound accepted by rule; the 14 and 22 character loss boundary; the DMA-hang timeout path stated as a measurement; the D21 slot kept out of `journal`, `user` and the bitstream tail |
| Tests | CLEAN | `receipts/docs_gates_renderer.txt`, `docs_gates.txt`, `pp_resource_gate_check_baseline.txt`, `ctrl_service_bounds_arm.txt`, `recompute.txt`, `anchor_probe.txt`, and the author's `a720k/evidence/gates/run_all.out` | A docs-only delta with no test changed. The two readers of the gate-read pages pass: "baseline PASS: 3 endpoints", and 47 checks with 0 failures and 38 of 38 planted controls caught. The probes are shown able to fail by their mutants. All of the author's 54 gate steps are rc 0 |
| Docs | UNCLEAN: F1, F2, F3; R1 is RESIDUE | The four pages in the diff at 3f8ed303 | Style, anchors, paths and citations; the PR body against the page; no obsolete text restored |

`receipts/docs_gates.txt` records three rc 2 results. Those are the gates that refused to run under an interpreter without the pinned renderer. They passed when rerun with the pinned renderer, in `docs_gates_renderer.txt`.

## Ledger

The reviewer owns this ledger.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | `MARK_II_AREA_PLAN.md` delta; #640 decision comments 6575277828, 6545523624, 6545540394, 6545999204, 6551164172, 6555550136, 6556743957; #665 6569635407, 6514866239, 6495692075; #495 6573412222; `FR_NFR.md:329,339` | R766-1 | 3f8ed303e01285f1bad0641f4ebc05764f162467 |
| RTL | UNCLEAN (F1) | Census against `sw/litex/milan_soc.py`; `milan_baremetal.c:1080`; `nvm_flash_litespi.c`; `mbx_plat_mmio.c` | R766-1 | 3f8ed303e01285f1bad0641f4ebc05764f162467 |
| Robustness | CLEAN | Console UART table and rule; stage 1 bus and slot text | R766-1 | 3f8ed303e01285f1bad0641f4ebc05764f162467 |
| Tests | CLEAN | Docs gates; `pp_resource_gate check-baseline`; `ctrl_service_bounds` arm; recompute, anchor and census probes with mutants; the author's gate receipts | R766-1 | 3f8ed303e01285f1bad0641f4ebc05764f162467 |
| Docs | UNCLEAN (F1, F2, F3) | The four pages in the diff; PR #835 body; the public evidence tree at b4578f5c | R766-1 | 3f8ed303e01285f1bad0641f4ebc05764f162467 |

## Limits

- **Basis reports not examined.** The basis build's placement reports are outside the repository and not on this host. So the placed sub-row figures the census adds could not be re-read: 1,150, 34, 55, 3, 227, 105, 176, 225 and 136. Their row names do match the repository's resource map for the same CPU wrapper.
- **LiteX defaults taken as known.** LiteX is not installed here. The 16-byte UART FIFO is taken from LiteX's default `uart_fifo_depth`, which `milan_soc.py` does not override.
- **Verilator not needed.** No RTL is in the delta, so no Verilator or synthesis run was made, and the scoped Verilator binary was not used.
- **Submodules.** Two submodules, `third_party/tsn-c-stack` and `third_party/lwSRP`, were initialised at their gitlinks for the service-bounds arm. Tracked bytes, modes and the index equal the head tree (`receipts/clone_integrity.txt`).
- **Not done:** no manager source bank, no candidate build, no hardware, no Docker or local CI replica, and no GitHub writes.
- **No hardware proof.** Physical calibration was not run, and field skips are not hardware proof.

## Pending manager duties

- Hosted contexts at the exact head were still queued or running when read (`receipts/hosted_check_runs.tsv`). Only `changes`, `wire-accountability` and `bdd-conformance` had completed, all with success. Hosted and local replica acceptance belongs to the manager.
- The current-dev merge-candidate validation (builder and native banks) is due at the merge turn, on source base 503bc97c, with live dev equal to it.
- Carry R766-1-R1 to the residue checklist.
- Re-review is needed after F1 to F3 are fixed.

## Receipts

All receipts are under this packet and listed in `MANIFEST.sha256`:

- `receipts/diff.patch`
- `receipts/docs_gates.txt`
- `receipts/docs_gates_renderer.txt`
- `receipts/style_probe_changed_blocks.txt`
- `receipts/anchor_probe.txt`
- `receipts/anchor_probe_mutant.txt`
- `receipts/pp_resource_gate_check_baseline.txt`
- `receipts/ctrl_service_bounds_arm.txt`
- `receipts/recompute.txt`
- `receipts/recompute_mutant.txt`
- `receipts/census_probe.txt`
- `receipts/source_checks.txt`
- `receipts/hosted_check_runs.tsv`
- `receipts/clone_integrity.txt`

The scripts are `scripts/recompute.py`, `scripts/census_probe.py` and `scripts/anchor_probe.py`. `scripts/service_bounds_arm.py` is a copy of the author's public evidence wrapper.

R766-1 FINISHED

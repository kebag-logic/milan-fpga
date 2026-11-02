[R766] NEGATIVE - exact head 545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2

Round R766-4, external cleared-context review of issue #640 / PR #835.
Head `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2`, tree `94e8b7052d4f4d03b578891691a3df96d2273043`, source base `503bc97cd4f24ad07596c17e7188f2024617972d`.

## Summary

- **Verdict: NEGATIVE on one MINOR, R766-4-F1.**
- **R765-3-F1 is resolved at its cause.** Stage 1's "Removes" cell no longer gives stage 1 the BIOS ROM and SRAM or their 18 RAMB36. It books them to the switch-over and links M8a-1. The note now says "Stage 1's Change cell keeps the owner's words", which is true. No stage in the table now credits a RAMB36, and the stage LUT credits split the LiteX top without double-booking anything.
- **R766-4-F1 is new, in the same commit.** It changes stage 3's "Removes" cell to "The generated FIFOs leave earlier, each with its block". The census itself places two blocks that own generated FIFOs at stage 3:
  - the UART's `tx_fifo` and `rx_fifo` (`:322`);
  - `milan_axil_cdc`'s five async FIFOs (`:330`). Its W and R payloads are one RAMB18 each in the basis.

  The author's own evidence supports a narrower claim: none of the **29 RAMB36** belongs to a stage 3 row. That claim is true; the cell's general one is not.
- RTL, Robustness and Tests are CLEAN at this head. Conformance and Docs are UNCLEAN, on F1 only.
- Earlier residues that this round did not take are retained (listed below). R766-3-RESIDUE-1 is resolved.

## Order of reconstruction

1. `AGENTS.md`, `CONTRIBUTING.md` (by reference) and `docs/README.md`.
2. The issue #640 body, with its frozen 2026-10-31 acceptance criteria. The owner's stage comment, issuecomment-6545999204: stage 1 is "Drop DDR3 and the BIOS ROM", and stage 3 says "The Wishbone and CSR-bank glue disappears".
3. The interface authorities the delta relies on:
   - the plan's stage table `:229-241`;
   - the census `:297-340`;
   - the Block RAM ledger `:382-401`;
   - the M8a-1 ledger `:1260-1319`;
   - `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:271-297`;
   - `sw/litex/milan_soc.py:784-813`.
4. The delta `d52e966b..545ac9cb` (one commit, three lines, in `docs/design/MARK_II_AREA_PLAN.md`), within the full range `503bc97c..545ac9cb`.
5. The public evidence at `9b06a2ff`, `review-evidence/640-m10-r1`.
6. Only after my own pass over the delta: the prior public findings (R765-3, R766-3), resolved below. I did not read the parallel round of this head.

## Executed checks (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| Delta bytes against the author's published `round4.diff` | identical | `receipts/delta_d52e966b_545ac9cb.diff` |
| Evidence packet: every file of `MANIFEST.json` (871 entries) against its `published_sha256`; files on disk not listed | 0 mismatches, 0 unlisted | `receipts/manifest_verify.log`, `scripts/verify_manifest.py` |
| `author-r4/evidence/SHA256SUMS` | 15 mismatches. Each one is a manifest entry with `path_redacted: true` whose `original_sha256` equals the SUMS line, so 0 unexplained | same |
| The author's round 4 gate receipts | 55 rc files, all 0; `review_ready.md` names commit `545ac9cb…`; the recorded gitlinks equal the head's | `receipts/author_r4_gates_summary.txt`, `receipts/gitlinks_head.txt` |
| Commit signatures | the head and the evidence commit are both unsigned (`verified: false`, `unsigned`). No detached signature is published; integrity rests on the manifest's hashes | `receipts/head_commit_verification.json`, `receipts/evidence_commit_verification.json` |
| Doc gates at the head, run with the pinned renderer from `tools/markdown/requirements.txt` installed by hash into a disposable environment: `docs_check`, `check_em_dash --base 503bc97c`, `check_doc_style` and `--selftest`, `gen_toc --selftest/--verify-anchors/--check`, `check_doc_paths` | all rc 0 | `receipts/*.log`, `receipts/*.rc`, `receipts/renderer_versions.txt` |
| `git diff --check 503bc97c HEAD` | rc 0, empty | `receipts/diff_check.log` |
| `syn/ooc/pp_resource_gate.py check-baseline` | `baseline PASS: 3 endpoints` | `receipts/check_baseline.log` |
| The PR's changed-block style probe, copied verbatim from the PR body | prints nothing, rc 0 | `scripts/style_probe.py`, `receipts/style_probe.log` |
| The published `census_coverage.py`, rerun at the head on the published basis excerpts | `RESULT: PASS`, byte-identical to the author's `census_coverage_worktree.out` | `receipts/census_coverage.log` |
| F1's exact fix, applied in memory and run through `check_doc_style.analyze()` | 0 new findings | `scripts/fix_probe.py`, `receipts/fix_probe.log` |
| Stage 3 FIFO owners | see F1 | `receipts/stage3_fifo_evidence.txt` |
| Hosted checks for the exact head, read at the time of this review | 9 runs; 8 queued and 1 in progress, none finished. No conclusion is drawn from them | `receipts/hosted_check_runs.tsv` |
| Clone restored after the checks | HEAD and tree exact; `git status --porcelain --ignored` empty after removing this round's bytecode caches; every tracked blob and mode re-hashed; six gitlinks unchanged | `receipts/restore_check.txt` |

## R765-3-F1 at its cause

R765-3-F1 said stage 1's "Removes" cell credited stage 1 with the BIOS ROM and SRAM, "18 RAMB36 measured". The note `:238`, census rows `:333-334`, lane 2's scope, M8a-1 `:1302` and `AREA_BUDGET.md` all book that memory to the switch-over.

| Place | Text at `545ac9cb` | Agrees with the switch-over booking? |
|---|---|---|
| `:231`, stage 1 Removes | "LiteDRAM controller and PHY. The BIOS ROM and SRAM, 18 RAMB36 measured, already left at the switch-over ([M8a-1](#firmware-and-block-ram-ledger))" | Yes. The anchor resolves to `### Firmware and block RAM ledger` at `:1260`, whose `:1302` books -18 RAMB36 to M8a-1 |
| `:231`, stage 1 Change | "Drop DDR3 and the BIOS ROM; …": the owner's words open the cell (issuecomment-6545999204), followed by the plan's D18, D21 and SoC-bus additions | Yes. It is the owner's text, which the note now names |
| `:235`, note | "Stage 1's Change cell keeps the owner's words." | Yes. R766-3-RESIDUE-1's alternative fix, taken verbatim |
| `:236-241` | The census places the BIOS at the switch-over; `ctrl_memory`'s banks hold the regions until stage 3 | Yes (unchanged) |
| `:333-334`, `:1302`, `:387-388` | Switch-over; -18 at M8a-1; "All 47 are gone once LiteX stage 3 ends" (a bound, not a stage credit) | Yes (unchanged) |

**Double-booking, re-read across the whole stage table and its sources:**

- **RAMB36.**
  - No stage cell now credits a RAMB36. The BIOS's 18 are booked once, at M8a-1 `:1302`.
  - The 29 generated FIFO RAMB36 are credited to no stage anywhere. The ledger `:1297-1305` has no per-stage FIFO line.
  - The published `fifo_owners.txt` assigns the 29 as follows: 16 to the DDR3 row (stage 1), 5 to Ethernet (stage 2) and 8 to the processor memory paths (switch-over).
- **LUT.**
  - Stage 1 is "Lever 1, ~1.0k".
  - Stage 2 is "Part of the -1.75k".
  - Stage 3 is "Lever 2, ~1.0k, and the rest of the -1.75k".
  - The -1.75k is the `:211` row "LiteX stages 2 and 3 beyond levers 1 and 2", from the LiteX top's 5,119 LUTs. The three credits are disjoint and total about 3.75k, less than 5,119. Stages 2 and 3 split the 1.75k, so neither counts it twice.
  - The CPU-wrapper sub-rows that the census places at stages 1 and 3 (`:329`, `:332`) sit inside the 3,249 the start already subtracts (`:152`). No stage cell credits them. That point is the carried R765-2-S4 and is not a new finding.

**R765-3-F1: resolved.** The same commit introduces F1 below in the neighbouring cell.

## Findings

### R766-4-F1 MINOR: stage 3's cell says every generated FIFO leaves before stage 3, but the census puts the UART's and the CSR crossing's FIFOs at stage 3

- **Lenses:** Conformance, Docs.
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:233`, stage 3 Removes: "Wishbone and CSR-bank glue. The generated FIFOs leave earlier, each with its block ([census](#litex-block-census))".
- **Evidence** (`receipts/stage3_fifo_evidence.txt`):
  - **Census `:322`.** The UART (`RS232PHY`, 16-byte FIFOs) is stage 3. The published basis hierarchy (`author-r2/evidence/census/basis_soc_hierarchy.txt:107-112`) builds `uart/tx_fifo` and `uart/rx_fifo` as LiteX `SyncFIFO`s. These are generated FIFOs.
  - **Census `:330`.** `milan_axil_cdc`, the CPU-to-`milan_csr` crossing, is stage 3. The same hierarchy (`:641-666`) builds it under `milan (MilanNIC)` as five `ClockDomainCrossing`/`AsyncFIFO`s.
  - **`sw/litex/milan_soc.py:791-813`.** The crossing has "one 4-deep async FIFO per channel". The W and R payloads go to block RAM, "one RAMB18 each", a change made in `4177835c` (2026-10-10), before the 2026-10-31 basis.
  - **The author's own `author-r4/evidence/fifo_owners.txt`.** It lists `storage_32_reg 4x36` and `storage_34_reg 4x34` under `milansoc_milannic_…`, each with 1 RAMB18 and 0 RAMB36.
    - Their depth matches the crossing's 4-deep channels, and they are the only 4-deep `milannic` rows. The other 4-deep rows, `w_cdc` and `r_cdc`, are the CPU memory-port crossing the receipt books to DDR3. Their widths match W (32 data + 4 strobe) and R (32 data + 2 response).
    - Every other MilanNIC crossing is 16 deep (`_AXIS_CDC_DEPTH = 16`, `milan_soc.py:1413`).
    - So these two RAMB18 are the crossing's W and R FIFOs. This is derived; the receipt records writer signals, not instance paths.
    - The same receipt says "RAMB18 here … 9" and books only RAMB36 by stage ("Stage 3 rows: none 0").
  - **The PR body's round 4 row** gives the reason for the edit: "none of the 29 belongs to a stage 3 row". That claim is about the 29 RAMB36, and it is true. The cell drops that qualifier and says it of all the generated FIFOs.
  - **Census note `:339-340`.** "The 29 generated FIFO RAMB36 … Each leaves with the block that owns it." The note agrees with the narrower claim, so `:233` is now the only statement that overstates it.
- **Why MINOR, not RESIDUE:**
  - The cell assigns measured block RAM to a stage. As written, stage 3's routed measurement should show no generated FIFO leave, but the CSR crossing's two FIFO RAMB18 and the UART's FIFOs leave there.
  - This is the same kind of claim as R765-3-F1: a stage attribution of measured resources, not wording only.
  - It contradicts the page's own census rows `:322` and `:330`, the deliverable of D19.
- **Impact:**
  - A reader of the stage table expects stage 3 to remove no FIFO storage.
  - A stage 3 lane that reconciles its routed image against the table would find two RAMB18, and the UART's and the crossing's LUT-RAM FIFOs, with no stage booked for them.
  - No LUT figure in the table changes.
- **Required outcome:** the stage 3 cell must not deny FIFO storage owned by stage 3 blocks. Either:
  - limit the "leave earlier" claim to the 29 RAMB36; or
  - name the stage 3 blocks' FIFOs as removed at stage 3.
- **Exact fix (probed, 0 new style findings):** replace the `:233` Removes cell with "Wishbone and CSR-bank glue; the FIFOs of stage 3 blocks. The 29 generated FIFO RAMB36 leave earlier, each with its block ([census](#litex-block-census))".
- **Verification:**
  - Read `:233` against `:322`, `:330` and `:339-340`.
  - Run `check_doc_style`, `gen_toc --check` and the PR's style probe.
  - The census coverage check should be unchanged, since the stage table lies outside the census section.

### Residue and suggestions

No new residue. Retained items, unchanged at this head:

- **R765-3-R1 / R766-3-RESIDUE-2 (RESIDUE, Docs).** `:239`, "`ctrl_memory`'s `rom` and `sram` banks hold them until stage 3.": "them" takes "the BIOS and its ROM and SRAM" (`:238`) as its antecedent.
  - Exact fix: "Until stage 3, `ctrl_memory`'s banks hold both regions."
  - Alternatively, R765-3's fix: "… hold those regions until stage 3."
- **R765-2-RESIDUE-1 (RESIDUE, Docs).** `:368`, "Under 10 ms, the buffer would be 128 bytes.". Exact fix as published: "Taking 10 ms as the gap gives 128 bytes."
- **R765-2-RESIDUE-2 (RESIDUE, Docs).** `:336`, "Stage 1 already fills `rom` from the flash copy, …" is in the present tense. Exact fix as published: "From stage 1, `rom` is filled from the flash copy, not the configuration image."
- **SUGGESTION (Docs), new, optional.** When F1 is fixed, the PR body's round 4 row could also say "none of the 29 RAMB36", to match the cell.

Carried suggestions, optional, with no coverage effect:

- R765-3-S1 (where stage 1's loader runs);
- R765-2-S1 / R766-2-S1;
- R766-2-S2;
- R766-2-S3;
- R765-2-S4.

### Comment rule

The delta adds no source comment, so the rule has nothing to apply to. "M8a-1" in the plan is a measurement label in a design page, not a source comment.

## Prior public findings at this head

| Finding | State at `545ac9cb` | Evidence |
|---|---|---|
| R765-3-F1 (MINOR; Conformance, Docs) | **Resolved at its cause** | the agreement table above |
| R766-3-RESIDUE-1 (note vs Removes cell) | **Resolved.** Both its preferred fix (the Removes cell now says "already left at the switch-over"; R765-2-S3's text) and its alternative (the note) were taken | `:231`, `:235` |
| R765-2-S3 | **Taken** | `:231` |
| R765-3-R1 / R766-3-RESIDUE-2, R765-2-RESIDUE-1, R765-2-RESIDUE-2 | **Retained as residue**; the PR body says they were not taken this round | `:239`, `:368`, `:336` |
| R766-2-F1, R765-1-F1 to F5, R766-1-F1 to F3, R766-1-R1 | Resolved at earlier heads, as recorded by R765-3 and R766-3. The delta touches only `:231`, `:233` and `:235`, which none of those resolutions rests on except R766-2-F1's BIOS statements, which the agreement table covers. **Still resolved** | `receipts/delta_d52e966b_545ac9cb.diff` |
| Carried suggestions | Not taken; optional | - |

## Per-lens results at `545ac9cb`

```text
[R766] MINOR Conformance — docs/design/MARK_II_AREA_PLAN.md:233 — R766-4-F1: stage 3's cell says every generated FIFO leaves before stage 3; census rows :322 (UART FIFOs) and :330 (milan_axil_cdc, two FIFO RAMB18) are stage 3
[R766] MINOR Docs — docs/design/MARK_II_AREA_PLAN.md:233 against :322, :330, :339-340 and author-r4/evidence/fifo_owners.txt — R766-4-F1: the cell overstates the evidence's "none of the 29 RAMB36" as "the generated FIFOs"
[R766] PASS RTL — receipts/delta_d52e966b_545ac9cb.diff (one Markdown page, 3 lines; no HDL, generator, constraint or gitlink) and sw/litex/milan_soc.py:784-813, 1413 read unchanged — the delta changes nothing the prior RTL verdict at d52e966b depends on; the CSR crossing's FIFO structure is read only as evidence for F1
[R766] PASS Robustness — receipts/check_baseline.log ("baseline PASS: 3 endpoints"); delta touches neither gate-read page (AREA_BUDGET.md, MAILBOX_SPLIT.md) — no gate-read line, layout, bound or failure-path claim changes in the delta
[R766] PASS Tests — receipts/census_coverage.log (PASS, byte-identical to author-r4's), receipts/style_probe.log (empty), doc gates rc 0, receipts/manifest_verify.log (0 unexplained) — the author's executable evidence reproduces at the head; no test or gate changed
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R766-4-F1) | owner comment 6545999204; issue #640 body and acceptance; `MARK_II_AREA_PLAN.md:211`, `:229-241`, `:297-340`, `:382-401`, `:1260-1319`; `649_RESOURCE_MAP_AND_SENSITIVITY.md:271-297`; `fifo_owners.txt`; `basis_soc_hierarchy.txt` | R766-4 | `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2` |
| RTL | CLEAN | delta diff; full diffstat (four Markdown pages); `sw/litex/milan_soc.py:784-813, 1413`; gitlinks | R766-4 | `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2` |
| Robustness | CLEAN | `check_baseline.log`; delta against the gate-read pages | R766-4 | `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2` |
| Tests | CLEAN | `census_coverage.log`; the doc gate logs and rc files; `style_probe.log`; `manifest_verify.log`; `author_r4_gates_summary.txt` | R766-4 | `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2` |
| Docs | UNCLEAN (R766-4-F1; residues retained) | `MARK_II_AREA_PLAN.md:229-241`, `:322`, `:330`, `:336`, `:339-340`, `:368`; PR body "Round 4"; style, TOC, anchor, path and em-dash gates | R766-4 | `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2` |

## Real limits

- The basis utilization and synthesis reports are outside the repository. The two RAMB18 are tied to `milan_axil_cdc` from the published `fifo_owners.txt`, by depth, width and module prefix together with `milan_soc.py`'s docstring. That tie is derived, not read from an instance path. F1 holds without it: the UART's and the crossing's FIFOs are generated FIFOs in stage 3 rows in any case.
- Neither the evidence commit nor the head is signed. Integrity was checked against the published manifest's hashes, not a signature.
- No source bank, builder or hosted run was executed by this round, and none is claimed. At the time of this review the hosted checks had no conclusion.
- Physical calibration NOT RUN. No hardware claim is made.

## Pending manager duties

- Fix R766-4-F1, then re-review. Conformance and Docs must be covered again at a head that includes the fix.
- Carry R765-3-R1 / R766-3-RESIDUE-2, R765-2-RESIDUE-1 and R765-2-RESIDUE-2 to the residue checklist.
- Hosted and act acceptance of the exact head, and the current-dev merge candidate (source base `503bc97c`, live dev `e61a4afa`): builder and native banks, with receipts linked on the PR.

R766-4 FINISHED

[R765] NEGATIVE - exact head 545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2

# R765-4: internal cleared-context review of PR #835 (issue #640), round 4

- Head `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2`, tree `94e8b7052d4f4d03b578891691a3df96d2273043`. Source base `503bc97cd4f24ad07596c17e7188f2024617972d`. Live dev at review time `e61a4afaa54a598ceec08b7b5879285256cc60b6`.
- Verdict: **NEGATIVE**, on one MINOR (F1).
- **R765-3-F1 is resolved at its cause.** Stage 1's "Removes" cell no longer credits stage 1 with the BIOS ROM and SRAM or their 18 RAMB36. It books them to the switch-over through M8a-1, and the note now names stage 1's Change cell.
- F1 is new in this delta and sits in the same table. The stage 3 fix overreaches: "The generated FIFOs leave earlier" is true for the 29 generated-FIFO RAMB36. It is false for generated FIFOs that the page's own census places at stage 3. Those are the CSR crossing `milan_axil_cdc`, whose W and R FIFOs take two RAMB18, and the UART's FIFOs.
- RTL, Robustness and Tests are CLEAN at this head. Conformance and Docs are UNCLEAN on F1.

## How this round reconstructed the task

Order followed: AGENTS.md and CONTRIBUTING.md, docs/README.md, issue #640's body (frozen acceptance 2026-10-31, the Block RAM line "the LiteX FIFOs (today 29 + 18 RAMB36)"), and the owner's stage comment (#640 issuecomment-6545999204: "Drop DDR3 and the BIOS ROM ... This also frees Block RAM"). Then the plan page's stage table, census, Block RAM ledgers and the generator source the census rests on (`sw/litex/milan_soc.py`). Then `git diff d52e966b..545ac9cb` (one commit, 3+/3- in `docs/design/MARK_II_AREA_PLAN.md:231,233,235`) and the author's round 4 evidence. I wrote my own draft (`receipts/independent_draft_before_prior_findings.txt`) before reading any earlier review comment.

Code outside the delta keeps its round 3 lens verdict, because the delta changes nothing it depends on. The diff touches one Markdown page, and no RTL, generator, firmware, gate, test or configuration file.

## Executed checks (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| Delta and author diff | `git diff d52e966b..545ac9cb` is byte-identical to the author's `round4.diff` | `receipts/delta_d52e966b_545ac9cb.diff`, `receipts/evidence_verify.txt` |
| Published author evidence | I fetched 136 blobs from tree `9b06a2ff` by git blob id, with 0 mismatches. All 135 `author-r4/` entries match `MANIFEST.json`'s `published_sha256`. All 132 `SHA256SUMS` lines equal `original_sha256`. The 15 `sha256sum -c` failures are all path-redacted files. All 55 rc files read 0, and the gate logs bind head `545ac9cb` | `receipts/evidence_verify.txt` |
| Signature | No detached signature file is in the published tree. Integrity rests on the blob ids under commit `9b06a2ff` plus the manifest | - |
| `docs_check.py` (system and pinned venv) | rc 0, 0 findings across 213 md files | `receipts/docs_check.*`, `receipts/venv_docs_check.*` |
| `check_doc_style.py` and `--selftest` | rc 0 / rc 0 | `receipts/doc_style*.*` |
| `check_em_dash.py --base 503bc97c` (pinned venv) | rc 0, 0 findings over 231 added lines | `receipts/venv_em_dash.*` |
| `gen_toc.py --check`, `--verify-anchors`, `--selftest` (pinned venv) | rc 0 / rc 0 / rc 0 (1501/1501 arms) | `receipts/venv_toc_*.*`, `receipts/venv_freeze.txt` |
| `check_doc_paths.py` | rc 0 | `receipts/doc_paths.*` |
| `git diff --check 503bc97c 545ac9cb` | rc 0, empty | `receipts/diff_check.*` |
| In-page anchors on the changed lines | All 6 fragments on `:231-236` resolve to GitHub heading slugs, including the new `#firmware-and-block-ram-ledger` (`:1260`). The mutant control `#firmware-and-block-ram-ledgerx` is reported MISSING | `scripts/anchor_probe.py`, `receipts/anchor_probe.*` |
| Generated-FIFO ownership | I cross-checked the author's synthesis mapping against the generator source and the census | `receipts/stage3_fifo_owners_crosscheck.txt` |
| Live PR body | Matches the author's published `PR-BODY.md` except for one trailing blank line | `receipts/pr_body_live_vs_author.diff` |
| Hosted contexts at the exact head | Snapshot: 8 queued and 1 in progress, none completed. Not hosted proof; owned by the manager | `receipts/hosted_check_runs_545ac9cb.tsv`, `receipts/hosted_statuses_545ac9cb.tsv`, `receipts/hosted_snapshot_time.txt` |
| Restore | HEAD and tree are exact, the porcelain status is empty, the index tree equals HEAD's, and all 6 gitlinks match the author's `final_submodules.txt`. No file in the clone was modified | `receipts/restore_verify.txt` |

I ran no RTL simulation, synthesis or build. The delta has no executable scope.

## R765-3-F1 at its cause

| Required outcome (R765-3-F1) | At `545ac9cb` | Result |
|---|---|---|
| Stage 1's "Removes" no longer credits stage 1 with the BIOS ROM and SRAM or their 18 RAMB36 | `:231`: "LiteDRAM controller and PHY. The BIOS ROM and SRAM, 18 RAMB36 measured, already left at the switch-over ([M8a-1](#firmware-and-block-ram-ledger))" | Met |
| The owner's "Change" wording may stay | The Change cell is byte-unchanged and still reads "Drop DDR3 and the BIOS ROM ..." | Met |
| The note names which cell keeps the owner's words | `:235`: "Stage 1's Change cell keeps the owner's words." | Met |
| The booking agrees everywhere else | `:238` (switch-over removes the BIOS and its ROM and SRAM), `:333-334` (census: switch-over), `:1302` (M8a-1, -18), `AREA_BUDGET.md:301` (M8a-1, -18), and lane 2's scope (`:432`) all agree | Met |
| No other per-stage RAMB36 or LUT credit double-books a block | LUT: lever 1 goes to stage 1, lever 2 to stage 3, and the -1.75k (`:211`, "beyond levers 1 and 2") is split between stages 2 and 3, so no LUT credit is booked twice. RAMB36: the table now credits none to any stage. The 29 generated-FIFO RAMB36 go to their owning rows: 16 DDR3 at stage 1, 5 Ethernet at stage 2, 8 processor memory paths at the switch-over. The 18 BIOS RAMB36 go to the switch-over | Met. The stage 3 wording that removes the old double booking introduces F1 |

## Findings

### R765-4-F1 MINOR: stage 3 is said to remove no generated FIFO, but the census removes the CSR crossing's and the UART's FIFOs at stage 3

- **Lenses:** Conformance, Docs.
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:233`, stage table, row 3, "Removes": "Wishbone and CSR-bank glue. The generated FIFOs leave earlier, each with its block ([census](#litex-block-census))". This text is new in `545ac9cb`.
- **Authority and evidence:**
  - The page's own census places `milan_axil_cdc`, "the CPU-to-`milan_csr` crossing", at stage 3 (`:330`). It also places the UART, "`RS232PHY`, 16-byte FIFOs", at stage 3 (`:322`). Both are FIFOs that LiteX generates.
  - The generator builds `milan_axil_cdc` as "one 4-deep async FIFO per channel" and puts the W and R payloads in "one RAMB18 each" (`sw/litex/milan_soc.py:792-813`, `:1878`). It does so inside `MilanNIC` (`:477`, `:854`, `:3505`).
  - The author's synthesis mapping (`author-r4/evidence/fifo_owners.txt`) shows them as `storage_32_reg` and `storage_34_reg`, `milansoc_milannic_array_write_memory0/2`, 4 deep, 1 RAMB18 each. The same file's reconciliation covers only the RAMB36 ("Stage 3 rows: none"). Its RAMB18 total of 10 has no per-stage split.
  - So the sentence holds for the 29 generated-FIFO RAMB36, the group the page names at `:112`, `:339` and `:387`. It does not hold for "the generated FIFOs" as written. Stage 3 does remove generated FIFOs: two RAMB18, one tile, plus LUTRAM FIFOs.
- **Why MINOR, not RESIDUE:** this is the class of defect R765-3-F1 was. A stage table cell assigns block RAM to a stage, here by negation. The two RAMB18 are measured, and the sentence moves them out of the stage that removes them. That is a stage-attribution claim, not only wording.
- **Why not RTL:** the generator and its census rows describe the FIFOs correctly. The defect is in the plan's stage accounting, and no RTL or interface contract is misdescribed.
- **Impact:**
  - A stage 3 lane reading its row would expect to remove no generated FIFO storage. It would also expect no block RAM change from the generator's FIFOs. Its routed measurement will show the CSR crossing's two RAMB18 leave there, or the first-party crossing replace them.
  - The row also contradicts `:322` and `:330` of the census it links to.
- **Required outcome:** stage 3's "Removes" cell limits "leave earlier" to the 29 generated-FIFO RAMB36, or otherwise stops saying that every generated FIFO leaves before stage 3. Neither the stage table nor the census may then say that stage 3 removes no generated FIFO. Not prescribed, one possible wording: "Wishbone and CSR-bank glue, and the CSR crossing's and the UART's FIFOs. The 29 generated-FIFO RAMB36 leave earlier, each with its block ([census](#litex-block-census))". This may need splitting to pass `check_doc_style`.
- **Verification:**
  - Read `:233` against `:322`, `:330`, `:339-340` and `fifo_owners.txt`.
  - Run `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, and `check_em_dash.py --base 503bc97c`.
  - Re-run `scripts/anchor_probe.py docs/design/MARK_II_AREA_PLAN.md 233`.

### R765-4-S1 SUGGESTION: say that the M8a-1 link goes to the Mark I history ledger

- **Lenses:** Docs.
- **Where:** `MARK_II_AREA_PLAN.md:231`, `[M8a-1](#firmware-and-block-ram-ledger)`.
- **Evidence:** the anchor resolves to `### Firmware and block RAM ledger` (`:1260`). That heading sits under `## Mark I plan history` (`:476`), which calls the sections below it "measurement and decision history". The current section is `## Mark II Block RAM ledger` (`:382`). The link is correct as evidence, because the M8a-1 -18 row (`:1302`) exists only in the history ledger. A reader may still take it for the current ledger.
- **Suggestion:** point the link at `SPLIT_CONTROL_MEMORY.md#5-fit`, where M8a-1's mapping is reported. Alternatively, name the target, e.g. "(M8a-1, [Mark I ledger](#firmware-and-block-ram-ledger))". No coverage effect.

### Comment rule

The delta adds no source comment, so the rule has nothing to apply to. "Lane 2" and "lane 1" in the plan name the plan's own lane sequence (`:420-435`). They are not bench lane labels in source.

## Prior public findings at this head

| Finding | State at `545ac9cb` | Evidence |
|---|---|---|
| R765-3-F1 (MINOR; Conformance, Docs): stage 1 "Removes" credits the BIOS memory's 18 RAMB36 | **Resolved at its cause** (table above) | `:231`, `:235`, `:238`, `:333-334`, `:1302`, `AREA_BUDGET.md:301` |
| R766-3-RESIDUE-1: the note says stage 1's row keeps the owner's words | **Resolved.** The alternative exact fix was applied verbatim at `:235`, and the preferred fix in substance at `:231` | `:231`, `:235` |
| R765-3-R1 / R766-3-RESIDUE-2: "`ctrl_memory`'s `rom` and `sram` banks hold them until stage 3." takes the BIOS as its object | **Retained as residue.** `:239` is unchanged. Exact fixes as published: "... hold those regions until stage 3." (R765-3) or "Until stage 3, `ctrl_memory`'s banks hold both regions." (R766-3, style-checked) | `:238-239` |
| R765-2-RESIDUE-1: "Under 10 ms, the buffer would be 128 bytes." | **Retained as residue.** `:368` is unchanged. Exact fix as published: "Taking 10 ms as the gap gives 128 bytes." | `:368` |
| R765-2-RESIDUE-2: "Stage 1 already fills `rom` ..." in the present tense | **Retained as residue.** `:336` is unchanged. Exact fix as published: "From stage 1, `rom` is filled from the flash copy, not the configuration image." | `:336` |
| R765-3-S1 (say where stage 1's loader runs and how `rom` becomes writable) | Not taken; optional. **Retained** | `:241`, `:333`, `:336` |
| R765-2-S1 / R766-2-S1, R766-2-S2, R766-2-S3, R765-2-S4, R765-1-S2/S3, R766-1-S2/S3 | Not taken; optional. **Retained**, with no coverage effect | - |
| R766-2-F1, R765-2-S2, R765-2-S3 | Resolved at `d52e966b` (R765-3, R766-3). The S3 cause was closed by this round | - |
| R765-1-F1 to F5, R766-1-F1 to F3, R766-1-R1 | Resolved at `30eb4834`. The round 4 hunk (`:231-235`) touches none of the lines those resolutions rest on | `receipts/delta_d52e966b_545ac9cb.diff` |

## Per-lens results

```text
[R765] MINOR Conformance — docs/design/MARK_II_AREA_PLAN.md:233 — R765-4-F1: stage 3 "Removes" says every generated FIFO leaves earlier, against census :322 and :330 and fifo_owners.txt (CSR crossing W/R, 2 RAMB18, stage 3)
[R765] MINOR Docs — docs/design/MARK_II_AREA_PLAN.md:233 — R765-4-F1: the cell contradicts the census it links to
[R765] PASS RTL — receipts/delta_d52e966b_545ac9cb.diff; sw/litex/milan_soc.py:789-813,1865-1880 — the delta changes no RTL, generator or interface file. Its FIFO-ownership claims were checked against the generator's crossings and the author's synthesis mapping. The round 3 RTL verdict holds, since nothing it depends on changed
[R765] PASS Robustness — receipts/delta_d52e966b_545ac9cb.diff; docs/design/MARK_II_AREA_PLAN.md:231-241 — doc-only delta with no configuration-dependent, reset, timeout or malformed-input behaviour. The stage table's DDR3-only and switch-over bookings are consistent across the configuration-dependent rows (:318, :331-336)
[R765] PASS Tests — receipts/venv_*.log, receipts/docs_check.log, receipts/anchor_probe.log, author-r4 gates (55 rc 0) — no test changed. The applicable doc gates pass at the head. The anchor probe resolves the new link and its mutant control fails. The plan page is read by no gate (author handoff), so no gate is weakened
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **UNCLEAN** (R765-4-F1 open) | `MARK_II_AREA_PLAN.md:224-241, :297-340, :382-401, :1260-1330`; `AREA_BUDGET.md:301`; #640 body and issuecomment-6545999204; `fifo_owners.txt` | R765-4 (not covered clean) | `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2` |
| RTL | CLEAN | delta diff; `sw/litex/milan_soc.py:477, :789-813, :854, :1865-1880, :3505`; `fifo_owners.txt` | R765-4 | `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2` |
| Robustness | CLEAN | delta diff; `MARK_II_AREA_PLAN.md:231-241, :318, :331-336` | R765-4 | `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2` |
| Tests | CLEAN | own gate re-runs; anchor probe and its mutant control; author-r4 gate receipts (55 rc 0, manifest-verified) | R765-4 | `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2` |
| Docs | **UNCLEAN** (R765-4-F1 open; residues carried) | `MARK_II_AREA_PLAN.md:231-241, :322, :330, :339-340, :368, :336, :476, :1260`; live PR body vs `PR-BODY.md` | R765-4 (not covered clean) | `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2` |

## Real limits

- I did not reproduce the basis synthesis mapping (`fifo_owners.txt`). Its RAMB36 split is taken from the author's published, manifest-verified receipt. The two RAMB18 in F1 also follow from the generator source alone (`milan_soc.py:792-813`).
- The published packet has no detached signature. Integrity rests on git blob ids under commit `9b06a2ff` plus `MANIFEST.json`.
- Hosted contexts at the exact head were queued or in progress at the snapshot, so they prove nothing here.
- No manager source bank ran at this head, and none is claimed. Source-head execution evidence is the author's published gate receipts plus my doc-gate re-runs.
- Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.

## Pending manager duties

- Validate the current-dev merge candidate (source base `503bc97c`, live dev `e61a4afa`) with the builder and native banks, and link the receipts on the PR. Re-run the census coverage check there, since dev's movement touches `sw/litex/milan_soc.py`, which the census reads. Dev is 18 commits ahead of the base and does not touch the plan page (`receipts/dev_movement_503bc97c_e61a4afa.txt`).
- Own hosted and local CI acceptance at the exact head once the queued contexts finish.
- Carry the retained residues (R765-3-R1 / R766-3-RESIDUE-2, R765-2-RESIDUE-1, R765-2-RESIDUE-2) to the residue checklist.
- Re-review after F1 is fixed. Conformance and Docs must be covered clean at a head that contains the fix.

R765-4 FINISHED

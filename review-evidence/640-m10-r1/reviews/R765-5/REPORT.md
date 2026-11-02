[R765] POSITIVE - exact head d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73

# R765-5: internal cleared-context review of PR #835 (issue #640), round 5

- Head `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73`, tree `7117c798eca686f6023287b32a07af72baf81c0f`.
- Source base `503bc97cd4f24ad07596c17e7188f2024617972d`. Live dev at review time `e61a4afaa54a598ceec08b7b5879285256cc60b6` (`receipts/live_dev.txt`).
- Previously reviewed head `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2`.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR, MINOR or RESIDUE is open at this head. All five lenses are CLEAN.
- **R765-4-F1 / R766-4-F1 is resolved at its cause.**
  - Stage 3's "Removes" cell (`:233`) is R766-4-F1's exact fix, byte for byte.
  - It names the FIFOs of stage 3 blocks as removed at stage 3.
  - It limits "leave earlier" to the 29 generated-FIFO RAMB36, and the basis mapping places each of those at stage 1, stage 2 or the switch-over.
- **The three retained residues are applied verbatim**, and each still reads true in context: R766-3-RESIDUE-2 / R765-3-R1 at `:239`, R765-2-RESIDUE-1 at `:368` and R765-2-RESIDUE-2 at `:336`.
- **R765-4-S1 is taken.** The link reads "(M8a-1, [Mark I ledger](#firmware-and-block-ram-ledger))". Its target lies under the page's Mark I history.
- **Nothing else changed.** The delta is five one-line commits with no body or trailer, 5+/5- in `docs/design/MARK_II_AREA_PLAN.md`.

## How this round reconstructed the task

1. I read `AGENTS.md` (which defers to `CONTRIBUTING.md`) and the issue #640 body, including its frozen 2026-10-31 acceptance criteria. Its Block RAM line reads "the LiteX FIFOs (today 29 + 18 RAMB36)".
2. I read the round 5 public TAKEN and REVIEW READY comments on #640 and the PR body's "Round 5" section.
3. I read these plan sections at the head:
   - the stage table and its notes (`:224-265`);
   - the census (`:297-340`);
   - the console UART section (`:342-380`);
   - the Mark II Block RAM ledger (`:382-401`);
   - the Mark I history banner (`:476-482`);
   - the Mark I `## Ledger` and its `### Firmware and block RAM ledger` (`:1075`, `:1260-1312`).
4. I diffed `545ac9cb..d85da329` within `503bc97c..d85da329`.
5. Then the published evidence at commit `266f9f36` (`review-evidence/640-m10-r1`): `author-r5/` in full, and `author-r4/evidence/fifo_owners.txt` and `census_coverage_worktree.out`.
6. I read the prior public findings (R765-4 and R766-4) only after my own pass over the five changed lines.

Code and pages outside the delta keep their round 4 lens verdicts unless the delta changes something they depend on. The delta touches one Markdown page and no source, generator, gate, script, workflow, gate-read page or gitlink (`receipts/delta_scope.txt`).

## Executed checks (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| Delta scope | 1 file, 5+/5-. Five commits, each a single line with 0 body lines and no trailer. The full branch range still touches only the four Markdown pages. `AREA_BUDGET.md`, `MAILBOX_SPLIT.md`, `docs/findings/README.md`, `sw`, `hdl`, `syn`, `scripts` and `.github` are unchanged since `545ac9cb` | `receipts/delta_scope.txt`, `receipts/delta_545ac9cb_d85da329.diff` |
| Author's diff | The published `author-r5/evidence/round5.diff` is byte-identical to `git diff 545ac9cb..d85da329` (sha256 `8afec932…`) | `receipts/delta_vs_author.txt` |
| Published evidence integrity | All 143 files checked out under `author-r5/`, plus `author-r4/evidence/fifo_owners.txt`, match `MANIFEST.json`'s `published_sha256`: 0 mismatches, 0 unlisted. Of `author-r5/evidence/SHA256SUMS`'s 139 lines, 16 match `original_sha256` of path-redacted entries; 0 are unexplained | `scripts/verify_evidence.py`, `receipts/evidence_verify.log` |
| Signatures | The head and the evidence commit `266f9f36` are both unsigned. No detached signature is published, so integrity rests on the manifest hashes under that commit | `receipts/head_commit_verification.json` |
| Author's round 5 gate receipts | 56 rc files, all 0. `clone_head.txt` binds head `d85da329…` and tree `7117c798…`. `final_submodules.txt` matches the head's six gitlinks. The inverted census control records rc 0 with "RESULT: FAIL", as documented in `gate_table.md:57` | `author-r5/evidence/gates/` (manifest-verified), `receipts/restore_verify.txt` |
| Census coverage | The author's round 5 `census_coverage_head.out` is byte-identical to the round 4 `census_coverage_worktree.out` and to the round 5 gate log ("RESULT: PASS"). The delta changes only a Fate cell (`:336`), not a row name | `receipts/census_spotcheck.txt` |
| Docs gates at the head, run with the hash-pinned renderer from `tools/markdown/requirements.txt` in a disposable environment | All rc 0: `docs_check.py` (0 findings, 213 md); `check_em_dash.py --base 503bc97c` (0 findings, 231 added lines); `check_doc_style.py` and `--selftest`; `check_doc_paths.py`; `gen_toc.py --selftest`, `--verify-anchors` (586 links) and `--check` | `receipts/*.log`, `receipts/*.rc`, `receipts/venv_freeze.txt` |
| `git diff --check 503bc97c d85da329` | rc 0, empty | `receipts/diff_check.*` |
| Style on the changed blocks | `check_doc_style.py` does not list the plan page, so I ran its `analyze()` directly. `:231`, `:233` and `:336` are table rows. `:239` sits in the paragraph from `:238` and `:368` in the paragraph from `:367`; both have 0 findings. The whole-page count is 407 at both `545ac9cb` and the head, so the delta adds none. A planted 15-word sentence at `:368` is caught (control) | `scripts/style_delta_probe.py`, `receipts/style_delta_probe.log` |
| In-page anchors on changed lines | All fragments on `:231`, `:233`, `:236` and `:336` resolve. `#firmware-and-block-ram-ledger` goes to `:1260`, under `## Ledger` (`:1075`), which is below the `## Mark I plan history` banner (`:476`). The mutant `#firmware-and-block-ram-ledgerx` is MISSING (control) | `scripts/anchor_check.py`, `receipts/anchor_check.log` |
| Live PR body | Identical to the published `author-r5/PR-BODY.md` | `receipts/pr_body_live_vs_author.diff` (empty) |
| Hosted contexts at the exact head | Snapshot only. Most are queued or in progress. Completed with success: `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, `bdd-conformance`, `verilator-lint`, `Prepare pinned Yosys`. "Physical gPTP (nightly and manual)" was skipped, which is not an executed job. No conclusion is drawn; hosted acceptance belongs to the manager | `receipts/hosted_check_runs.tsv`, `receipts/hosted_statuses.tsv`, `receipts/hosted_snapshot_time.txt` |
| Restore | HEAD, tree and index tree are exact. `git diff --quiet HEAD` passes. 1,460 tracked entries were re-checked for mode with 0 mismatches. The six gitlinks are unchanged. One bytecode cache written by this round's style probe (`scripts/__pycache__/`, untracked, ignored) was removed, after which `git status --porcelain --ignored` is empty | `receipts/restore_verify.txt` |

I ran no simulation, synthesis or build, because the delta has no executable scope.

## Check (1): R765-4-F1 / R766-4-F1 at its cause

The `:233` "Removes" cell at the head reads: "Wishbone and CSR-bank glue; the FIFOs of stage 3 blocks. The 29 generated FIFO RAMB36 leave earlier, each with its block ([census](#litex-block-census))". This equals R766-4-F1's published exact fix character for character.

| Required outcome | At `d85da329` | Result |
|---|---|---|
| The cell no longer denies FIFO storage owned by stage 3 blocks | "the FIFOs of stage 3 blocks" are named as removed at stage 3 | Met |
| It agrees with census `:322` | `:322` places the UART (`RS232PHY`, 16-byte FIFOs) at stage 3. Those FIFOs are stage 3 FIFOs, now removed by stage 3's cell | Met |
| It agrees with census `:330` | `:330` places `milan_axil_cdc` at stage 3. In the basis mapping, its W and R FIFOs are `storage_32_reg` (4x36) and `storage_34_reg` (4x34) under `milannic`, each with 1 RAMB18 and 0 RAMB36. Stage 3 now removes them | Met |
| "Leave earlier" is limited to the 29 generated-FIFO RAMB36 and is true for them | `fifo_owners.txt`, re-added from its rows: DDR3 `w_cdc`, `r_cdc`, `write_w_buffer` and `read_r_buffer` give 4+4+4+4 = 16 (stage 1). Ethernet `tx_cdc`, `rx_cdc`, `packetfifo` and two `array_write_memory` give 5 x 1 = 5 (stage 2). Processor crossings `d/r/n` `req`/`rsp`/`wr` give 8 x 1 = 8 (switch-over). The total is 29, and no stage 3 row holds a RAMB36. Stage 1 and the switch-over both precede stage 3 (`:231` "already left at the switch-over") | Met |
| Neither the stage table nor the census says stage 3 removes no generated FIFO | In the current Mark II sections (`:1-475`) the FIFO statements are `:112`, `:212`, `:233`, `:322`, `:324`, `:339-340`, `:354-355` and `:387`. None denies stage 3 FIFO removal. `:339-340` ("belong to rows above. Each leaves with the block that owns it") and `:387-388` ("All 47 are gone once LiteX stage 3 ends") agree with the cell | Met |
| No figure moves | The LUT credit column is unchanged. No RAMB36 is credited to any stage | Met |

**R765-4-F1 / R766-4-F1: resolved at its cause.**

## Check (2): the three retained residues

| Residue | Published exact fix | At the head | Still true in context? |
|---|---|---|---|
| R766-3-RESIDUE-2 / R765-3-R1, `:239` | "Until stage 3, `ctrl_memory`'s banks hold both regions." | `:239` is identical | Yes. `:238` says the switch-over removes the BIOS and its ROM and SRAM. "Both regions" are the `rom` and `sram` regions, which census `:333-334` says `ctrl_memory`'s banks hold until stage 3. The sentence no longer makes the removed BIOS the banks' content |
| R765-2-RESIDUE-1, `:368` | "Taking 10 ms as the gap gives 128 bytes." | `:368` is identical | Yes. It follows "Dev's FR_NFR.md still proposes T_svc = 10 ms" (`:367`) and matches table row `:360`. 10 ms at 86.806 µs a character completes 116 characters (115 take 9.983 ms, 116 take 10.069 ms), and the next power of two is 128. The round 5 style probe finds the paragraph within limits |
| R765-2-RESIDUE-2, `:336` | "From stage 1, `rom` is filled from the flash copy, not the configuration image." | `:336` Fate cell, final sentence, is identical | Yes. It agrees with `:241` ("Stage 1 … fills `rom` from flash (D18)") and with `:333` ("From stage 1 the boot loader fills `rom` from the flash copy"). Before stage 1, the split build's `rom` comes from the configuration image, so "already" is gone without losing that distinction |

All three are applied verbatim and resolved.

## Check (3): R765-4-S1

`:231` now reads "(M8a-1, [Mark I ledger](#firmware-and-block-ram-ledger))". The target `### Firmware and block RAM ledger` (`:1260`) sits under `## Ledger` (`:1075`). That section is below `## Mark I plan history` (`:476`), whose banner reads "Below is the Mark I plan against 38,040 LUTs. They are measurement and decision history". The current section is the separate `## Mark II Block RAM ledger` (`:382`). So the label names the target correctly, and M8a-1's -18 RAMB36 row (`:1302`) is in that target. **Taken; resolved.**

## Check (4): nothing else changed; gates

- The diff is exactly the five hunks above (`receipts/delta_545ac9cb_d85da329.diff`), one per commit. It matches the author's `round5.diff`.
- Docs workflow gates, the em-dash check, the style check and its selftest, TOC check, TOC selftest, anchor verification, doc paths and `git diff --check 503bc97c` all pass at the head (table above).

## Comment rule

The delta adds no source comment, so the rule does not apply. "M8a-1", "Mark I ledger" and "lane 1" are plan and measurement labels in a design page, not source comments.

## Findings

None open. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is raised at this head.

## Prior public findings at this head

| Finding | State at `d85da329` | Evidence |
|---|---|---|
| R765-4-F1 / R766-4-F1 (MINOR; Conformance, Docs): stage 3 said every generated FIFO leaves earlier | **Resolved at its cause** | Check (1); `:233`, `:322`, `:330`, `:339-340`, `fifo_owners.txt` |
| R765-4-S1 (SUGGESTION; Docs): name the M8a-1 link's target | **Taken; resolved** | Check (3); `:231`, `receipts/anchor_check.log` |
| R766-4 suggestion: the PR body's round 4 row should also say "none of the 29 RAMB36" | **Taken in substance.** The live round 4 row says "none of the 29 RAMB36 belongs to a stage 3 row … round 5 narrows it to the 29 RAMB36" | The live PR body equals `author-r5/PR-BODY.md` (`receipts/pr_body_live_vs_author.diff`) |
| R766-3-RESIDUE-2 / R765-3-R1 (RESIDUE; Docs), `:239` | **Resolved**, exact fix applied verbatim | Check (2) |
| R765-2-RESIDUE-1 (RESIDUE; Docs), `:368` | **Resolved**, exact fix applied verbatim | Check (2) |
| R765-2-RESIDUE-2 (RESIDUE; Docs), `:336` | **Resolved**, exact fix applied verbatim | Check (2) |
| R765-3-F1, R766-3-RESIDUE-1, R765-2-S3 | Resolved at `545ac9cb`, as recorded by R765-4 and R766-4. The delta changes only the link text in `:231`. "Already left at the switch-over" and the note `:235` are unchanged. **Still resolved** | `receipts/delta_545ac9cb_d85da329.diff` |
| R766-2-F1, R765-2-S2; R765-1-F1 to F5, R766-1-F1 to F3, R766-1-R1 | Resolved at earlier heads, as recorded by R765-3, R766-3, R765-4 and R766-4. Of the delta's lines, only `:239` and `:336` touch the BIOS and `rom` statements R766-2-F1 rests on, and Check (2) reads both true against `:333-334`. **Still resolved** | Check (2) |
| Optional suggestions R765-3-S1, R765-2-S1 / R766-2-S1, R766-2-S2, R766-2-S3, R765-2-S4, R765-1-S2/S3, R766-1-S2/S3 | Not taken; optional. **Retained**, with no coverage effect | PR body "Round 5", last line |

## Per-lens results

```text
[R765] PASS Conformance — docs/design/MARK_II_AREA_PLAN.md:231,:233,:239,:336,:368 against census :322,:330,:333-334,:339-340, ledger :387-388, :1302 and author-r4/evidence/fifo_owners.txt (manifest-verified) — stage 3's cell removes stage 3 blocks' FIFOs; the 29 generated-FIFO RAMB36 split 16/5/8 to stage 1, stage 2 and the switch-over; no stage credit or figure moves; issue #640 frozen acceptance unaffected
[R765] PASS RTL — receipts/delta_scope.txt (sw, hdl, syn, scripts and .github unchanged since 545ac9cb) and fifo_owners.txt rows storage_32_reg/storage_34_reg (milannic, 4-deep, 1 RAMB18 and 0 RAMB36 each) — the delta changes no RTL, generator, constraint or gitlink, and its FIFO claims match the basis mapping; the round 4 RTL verdict holds because nothing it depends on changed
[R765] PASS Robustness — receipts/delta_scope.txt (gate-read AREA_BUDGET.md and MAILBOX_SPLIT.md unchanged since 545ac9cb); author-r5 reader_check_baseline.log "baseline PASS: 3 endpoints" and reader_service_bounds.log "RESULT: PASS"; MARK_II_AREA_PLAN.md:360,:367-368 — no configuration-dependent, reset, bound or failure-path claim changes; the 10 ms alternative bound's arithmetic (116 characters, 128 bytes) still holds
[R765] PASS Tests — receipts/docs_check.log, em_dash.log, doc_style*.log, doc_paths.log, toc_*.log, diff_check.log (all rc 0); receipts/style_delta_probe.log and receipts/anchor_check.log, each with a control that fails as it must; receipts/census_spotcheck.txt; receipts/evidence_verify.log (author-r5 56 rc 0, manifest 0 mismatches) — no test or gate changed, and the applicable gates pass at the exact head
[R765] PASS Docs — docs/design/MARK_II_AREA_PLAN.md:231,:233,:238-239,:336,:367-368,:476,:1075,:1260 against the published exact fixes in R766-4-F1, R766-3-RESIDUE-2, R765-2-RESIDUE-1/-2 and R765-4-S1; live PR body equals author-r5/PR-BODY.md — every fix is applied verbatim and reads true in context; the link label names its Mark I target; no residue remains open
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #640 body and frozen acceptance; `MARK_II_AREA_PLAN.md:112`, `:224-241`, `:297-340`, `:382-401`, `:1260-1312`; `fifo_owners.txt`; `receipts/head_lines_MARK_II_AREA_PLAN.txt` | R765-5 | `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73` |
| RTL | CLEAN | `receipts/delta_scope.txt`; `receipts/delta_545ac9cb_d85da329.diff`; `fifo_owners.txt` (`milannic`, `milanmac` and DDR3 rows); the six head gitlinks | R765-5 | `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73` |
| Robustness | CLEAN | `receipts/delta_scope.txt`; author-r5 `reader_check_baseline.log` and `reader_service_bounds.log`; `MARK_II_AREA_PLAN.md:342-380` | R765-5 | `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73` |
| Tests | CLEAN | own doc-gate re-runs (`receipts/*.rc`); style and anchor probes with controls; census spot-check; author-r5 gate receipts (56 rc 0, manifest-verified) | R765-5 | `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73` |
| Docs | CLEAN | `MARK_II_AREA_PLAN.md:231`, `:233`, `:235-241`, `:333-336`, `:360-371`, `:476-482`, `:1075`, `:1260`; live PR body vs `author-r5/PR-BODY.md`; round 5 TAKEN and REVIEW READY comments on #640 | R765-5 | `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73` |

## Real limits

- I did not reproduce the basis synthesis mapping. The 29-RAMB36 split comes from the author's published `fifo_owners.txt`, verified against the manifest. Its writer-signal attribution of the two stage 3 RAMB18 to `milan_axil_cdc` rests on depth, width and module prefix, as R766-4 noted. The resolution does not depend on that tie, because the cell names "the FIFOs of stage 3 blocks" generically.
- I did not re-run `census_coverage.py` myself. I verified that the author's round 5 output is byte-identical to the round 4 output that both round 4 reviewers reproduced. The delta changes only a Fate cell, not a census row.
- Neither the head nor evidence commit `266f9f36` is signed, so integrity rests on `MANIFEST.json` hashes and git object ids.
- No manager source bank ran at this exact head, and none is claimed or inferred. Source-head execution evidence is the author's published gate receipts plus this round's doc-gate re-runs.
- Hosted contexts were a snapshot with most jobs queued or in progress. The skipped "Physical gPTP" context is not an executed job. None of this is hosted proof.
- Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head, once the queued and in-progress contexts finish.
- Validate the current-dev merge candidate (source base `503bc97c`, live dev `e61a4afa`) with the builder and native banks, and link the receipts on the PR. Re-run the census coverage check there, because dev's movement touches `sw/litex/milan_soc.py`, which the census reads.
- Pair this round with the external reviewer's round 5 verdict at the same head, for the CONTRIBUTING two-review bar.
- The author's open risks (c) are outside this PR's scope and left for their lanes:
  - #640's body still shows the 34.2k chain;
  - D21's flash offset and budget wait for the stage 1 lane;
  - the switch-over ledger's omitted credit for the 8 processor-crossing RAMB36 is left to that lane.
- No residue from this round goes to the residue checklist. The three earlier residues are applied at this head.

R765-5 FINISHED

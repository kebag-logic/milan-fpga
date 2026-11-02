[R766] POSITIVE - exact head d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73

# R766-5: external cleared-context review of issue #640 / PR #835, round 5

- Head `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73`, tree `7117c798eca686f6023287b32a07af72baf81c0f`. Source base `503bc97cd4f24ad07596c17e7188f2024617972d`. Previously reviewed head `545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2`. Live dev, per the manager: `e61a4afaa54a598ceec08b7b5879285256cc60b6`.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR, MINOR or RESIDUE is open at this head.
- **R765-4-F1 / R766-4-F1 is resolved at its cause.** Stage 3's Removes cell (`:233`) is R766-4-F1's exact fix, byte for byte. It agrees with census rows `:322` (UART) and `:330` (`milan_axil_cdc`). It also agrees with the 16 + 5 + 8 split of the 29 generated-FIFO RAMB36. No sentence in the stage table or the census now says that stage 3 removes no generated FIFO.
- **The three retained residues are applied verbatim** (`:239`, `:368`, `:336`), and each reads true in context. **R765-4-S1 is taken** (`:231`).
- Nothing else changed. The round delta is five one-line commits, 5+/5- lines, all in `docs/design/MARK_II_AREA_PLAN.md`.
- All five lenses are CLEAN at this head.

## Order of reconstruction

1. `AGENTS.md`, with `CONTRIBUTING.md` taken by reference, then `docs/README.md`.
2. Issue #640's frozen acceptance and scope decisions, as carried in R766-4's reconstruction. That includes the owner's stage comment, issuecomment-6545999204: stage 1 "Drop DDR3 and the BIOS ROM", and stage 3, where "the Wishbone and CSR-bank glue disappears".
3. The interface authorities the delta relies on, read at the head:
   - the stage table `MARK_II_AREA_PLAN.md:224-265`;
   - the census `:297-340`;
   - the console UART section `:342-380`;
   - the Mark II Block RAM ledger `:382-401`;
   - the page's section tree `:476-1260`;
   - the M8a-1 ledger row `:1296-1306`;
   - `649_RESOURCE_MAP_AND_SENSITIVITY.md:279-297`.
4. `git diff 545ac9cb..d85da329`, inside `503bc97c..d85da329`, and the five commit messages.
5. The public evidence at `266f9f36`, `review-evidence/640-m10-r1/author-r5/` and `MANIFEST.json`, plus `author-r4/evidence/fifo_owners.txt`.
6. **Only after my own pass over the delta**: the prior public findings, from R766-4 (issuecomment-6582620684) and R765-4 (issuecomment-6584004136). They are resolved below. I did not read the parallel round on this head before writing this verdict.

My own pass, before I read the earlier findings, raised one question. Does any of the 29 FIFO RAMB36 belong to a stage 3 block? If one did, "leave earlier" would be false. The published owner receipt settles it: 16 go to DDR3 (stage 1), 5 to Ethernet (stage 2) and 8 to the processor memory paths (switch-over), with none at stage 3 (`fifo_owners.txt:33-37`). So the question is closed, not a finding.

## Executed checks (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| Round delta against the author's published `round5.diff` | Byte-identical. 1 file, 5+/5- | `receipts/delta_545ac9cb_d85da329.diff` |
| Full range `503bc97c..d85da329`, raw | 4 Markdown pages, modes `100644`, no gitlink or code path | `receipts/raw_diff_base_head.txt` |
| Commit messages | Five one-line subjects, each ending `(#640)`, no body, no trailer | `git log 545ac9cb..HEAD`, quoted under Docs |
| Evidence `author-r5/` plus `MANIFEST.json`, fetched by git blob id from tree `266f9f36` | 143 blobs, 0 blob-id mismatches. 142 checked against `published_sha256`: 0 mismatches, 0 unlisted | `scripts/fetch_verify_evidence.py`, `receipts/evidence_verify.log` |
| `author-r5/evidence/SHA256SUMS` | 16 lines differ from the published bytes. Each is a `path_redacted` manifest entry whose `original_sha256` equals the SUMS line, so 0 are unexplained | `scripts/sums_redaction_check.py`, `receipts/sha256sums_redaction_check.log` |
| The author's round 5 gate receipts | `clone_head.txt` names head and tree exactly. 56 rc files, all 0. `review_ready.md` names commit `d85da329…`. The largest log (`gate_41`) is withheld and listed by hash in `LARGE_LOGS.txt` | `receipts/evidence_verify.log`, plus the fetched `gates/` tree (not republished) |
| `author-r4/evidence/fifo_owners.txt`, fetched by blob id | 0 mismatches. Split `:33-37`: DDR3 16 (stage 1), Ethernet 5 (stage 2), processor memory paths 8 (switch-over), stage 3 rows none | `receipts/fifo_owners_fetch.log` |
| Doc gates at the head. Pinned renderer installed by hash from `tools/markdown/requirements.txt` into a disposable venv | `docs_check`, `check_em_dash --base 503bc97c` (0 findings over 231 added lines), `check_doc_style` and `--selftest`, `check_gptp_docs`, `gen_toc --selftest/--verify-anchors/--check`, `check_doc_paths`, `check_archive`, `DOC_MAP.gen.py --check`, `check_feature_status`: all rc 0 | `receipts/*.log`, `receipts/*.rc`, `receipts/renderer_versions.txt` |
| `git diff --check 503bc97c HEAD` | rc 0, empty | `receipts/diff_check.log`, `receipts/diff_check.rc` |
| `syn/ooc/pp_resource_gate.py check-baseline` (the reader of `AREA_BUDGET.md`) | `baseline PASS: 3 endpoints` | `receipts/check_baseline.log` |
| `check_hygiene.py --check` | rc 2, refused: the clone's submodules are not initialized. I did not initialize them. This is an environment precondition, not a head result. The author's receipt at this head, with submodules, is rc 0 (`35 checks: 35 PASS`) | `receipts/hygiene.log`, `receipts/hygiene.rc` |
| Changed-line probe: `check_doc_style.analyze()` on the page at head against `545ac9cb`, and every in-page fragment on `:231`, `:233`, `:336` | 0 new style findings (407 at both heads: the page is outside the gate's 23 current documents, and the delta adds none). A planted 11-word sentence at `:239` is caught. All 6 fragments resolve to heading slugs. The mutant `#firmware-and-block-ram-ledgerx` is MISSING, as it must be | `scripts/delta_probe.py`, `receipts/delta_probe.log` |
| Live PR body against the author's `PR-BODY.md` | Identical except one trailing blank line. PR open, not draft, base `dev`, head `d85da329` | `receipts/pr_body_live_vs_author.diff`, `receipts/pr_state.tsv` |
| Hosted check runs for the exact head, snapshot 2026-11-02T19:58:37Z | 12 success, 1 skipped, 20 in progress, 16 queued. The run was not finished, so I draw no conclusion | `receipts/hosted_check_runs.tsv`, `receipts/hosted_snapshot_time.txt` |
| Commit signature | Head is unsigned (`false`, `unsigned`), and so is evidence commit `266f9f36`. Integrity rests on blob ids and the manifest's hashes | `receipts/head_commit_verification.tsv` |
| Clone restore | HEAD and tree exact; the index tree equals the head tree; `status --porcelain --ignored` empty. 1,460 tracked blobs re-hashed and their modes checked, 0 mismatches. 6 gitlinks equal the base's | `receipts/restore_check.txt`, `receipts/gitlinks_head.txt` |

## Focus checks

### (1) R765-4-F1 / R766-4-F1: stage 3's Removes cell

| Place at `d85da329` | Text | Agrees? |
|---|---|---|
| `:233`, stage 3 Removes | "Wishbone and CSR-bank glue; the FIFOs of stage 3 blocks. The 29 generated FIFO RAMB36 leave earlier, each with its block ([census](#litex-block-census))" | Matches R766-4-F1's published exact fix character for character |
| `:322`, census UART | Stage 3, "`RS232PHY`, 16-byte FIFOs" | Yes: these are "the FIFOs of stage 3 blocks" |
| `:330`, census `milan_axil_cdc` | Stage 3, the CPU-to-`milan_csr` crossing, two FIFO RAMB18 by R766-4's evidence | Yes: these too are "the FIFOs of stage 3 blocks" |
| `:339-340`, census note | "The 29 generated FIFO RAMB36 belong to rows above. Each leaves with the block that owns it." | Yes |
| `fifo_owners.txt:33-37` | 16 at stage 1, 5 at stage 2, 8 at the switch-over, 0 at stage 3. Total 29 | Yes: all 29 leave before stage 3, so "leave earlier" is true |
| `:112`, `:387-388` | "47 RAMB36 are 29 generated FIFOs and 18 BIOS ROM and SRAM"; "All 47 are gone once LiteX stage 3 ends" | Yes: a bound, not a stage credit |

A search of `docs/` for "leave earlier", "no generated FIFO" and "FIFOs of stage" finds only `:233`, so neither the table nor the census denies stage 3's FIFOs anywhere. **Resolved at its cause.** No LUT or tile figure moves.

### (2) The retained residues, applied verbatim

| Residue | Line | Text at head | Published exact fix | Reads true in context |
|---|---|---|---|---|
| R766-3-RESIDUE-2 / R765-3-R1 | `:239` | "Until stage 3, `ctrl_memory`'s banks hold both regions." | R766-3's fix, identical | Yes. "Both regions" takes the ROM and SRAM of `:238`, not the BIOS. Census `:333-334` says the `rom` and `sram` banks each "hold the region until stage 3" |
| R765-2-RESIDUE-1 | `:368` | "Taking 10 ms as the gap gives 128 bytes." | Identical | Yes. It follows `:367`'s T_svc = 10 ms and matches table row `:360`: 116 characters complete, so 128 bytes |
| R765-2-RESIDUE-2 | `:336` | "From stage 1, `rom` is filled from the flash copy, not the configuration image." | Identical | Yes. It agrees with `:241` ("Stage 1 … fills `rom` from flash") and `:333` ("From stage 1 the boot loader fills `rom` from the flash copy") |

### (3) R765-4-S1: the M8a-1 link

- `:231` now reads "(M8a-1, [Mark I ledger](#firmware-and-block-ram-ledger))". That is R765-4-S1's alternative wording, taken verbatim.
- The target `### Firmware and block RAM ledger` (`:1260`) sits under `## Ledger` (`:1075`).
- `## Ledger` comes after `## Mark I plan history` (`:476`), whose text says "Below is the Mark I plan … They are measurement and decision history."
- Every Mark II section precedes `:476`, including `## Mark II Block RAM ledger` at `:382`. So "Mark I ledger" names the target correctly and tells it apart from the current ledger.
- The M8a-1 -18 RAMB36 row is at `:1302`. The anchor resolves (see `delta_probe.log`).

### (4) Nothing else changed; gates

- The delta is the five lines above and nothing more.
- No figure, link target, heading or gate-read page changed in the delta.
- The doc gates, the TOC and anchor checks and `diff --check` all pass (see the table above).
- The PR body's Round 5 rows 15 to 19 describe the delta accurately. Its round 4 row now says round 5 "narrows it to the 29 RAMB36", which takes R766-4's optional PR-body suggestion in substance.

## Findings

None open at this head.

- **New in this round:** no BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION.
- **Comment rule:** the delta adds no source comment, so the rule has nothing to apply to. "M8a-1" and "Mark I ledger" are measurement and section names in a design page. Neither is a bench lane label, review round, reviewer ID or comment ID.

## Prior public findings at this head

| Finding | State at `d85da329` | Evidence |
|---|---|---|
| R766-4-F1 / R765-4-F1 (MINOR; Conformance, Docs) | **Resolved at its cause** | Focus check (1) |
| R766-3-RESIDUE-2 / R765-3-R1 | **Resolved**, verbatim | `:239` |
| R765-2-RESIDUE-1 | **Resolved**, verbatim | `:368` |
| R765-2-RESIDUE-2 | **Resolved**, verbatim | `:336` |
| R765-4-S1 (SUGGESTION) | **Taken** | `:231` |
| R766-4 SUGGESTION (PR body round 4 row) | **Taken** in substance | PR body row 14 |
| R765-3-F1, R766-3-RESIDUE-1, R766-2-F1, R765-1-F1 to F5, R766-1-F1 to F3, R766-1-R1 | **Still resolved.** The delta touches only `:231` (an added link label inside the parenthesis), `:233`, `:239`, `:336` and `:368`. R765-3-F1's switch-over booking at `:231` is unchanged in substance | `receipts/delta_545ac9cb_d85da329.diff` |
| R765-3-S1, R765-2-S1 / R766-2-S1, R766-2-S2, R766-2-S3, R765-2-S4 | Not taken. Optional, **retained**, no effect on coverage | PR body "Not taken, optional" |

## Per-lens results at `d85da329`

```text
[R766] PASS Conformance — docs/design/MARK_II_AREA_PLAN.md:231, :233, :239, :322, :330, :333-340, :360, :367-368, :387-388; author-r4/evidence/fifo_owners.txt:33-37; owner comment 6545999204 — stage 3's cell names stage 3 blocks' FIFOs and limits "leave earlier" to the 29 RAMB36, which the owner split puts at stages 1 and 2 and the switch-over; BIOS memory stays booked to the switch-over; console 128-byte figure matches :360
[R766] PASS RTL — receipts/raw_diff_base_head.txt and receipts/delta_545ac9cb_d85da329.diff (Markdown only, no HDL, generator, constraint or gitlink; gitlinks_head.txt equals base) — the delta changes nothing the prior RTL verdict (R766-4 at 545ac9cb) depends on; FIFO structure in sw/litex/milan_soc.py unchanged and read only via R766-4's evidence
[R766] PASS Robustness — receipts/check_baseline.log ("baseline PASS: 3 endpoints"); raw diff shows AREA_BUDGET.md and MAILBOX_SPLIT.md untouched since 545ac9cb — no gate-read line, bound, reset, timeout or configuration-dependent claim changes in the delta; the 32-byte/128-byte console conditions at :360-371 are unchanged in substance
[R766] PASS Tests — receipts/delta_probe.log (0 new style findings, planted control caught, 6/6 fragments resolve, mutant anchor MISSING), receipts/evidence_verify.log (0 mismatches), author-r5 gates (56 rc 0, clone_head exact), own doc gates rc 0 — no test or gate changed; the author's executable evidence binds this head and reproduces where re-run
[R766] PASS Docs — docs/design/MARK_II_AREA_PLAN.md:231-241, :336, :339-340, :368, :476, :1075, :1260; live PR body vs author-r5/PR-BODY.md; commit messages 545ac9cb..d85da329 — every changed sentence is the published fix verbatim and reads true in context; the link label names the Mark I section correctly; commits are one-line with no trailers; em-dash, style, TOC, anchors, paths and diff --check clean
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `MARK_II_AREA_PLAN.md:224-241, :297-340, :342-380, :382-401, :1296-1306`; `fifo_owners.txt:33-37`; `649_RESOURCE_MAP_AND_SENSITIVITY.md:279-297`; owner comment 6545999204 | R766-5 | `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73` |
| RTL | CLEAN | `raw_diff_base_head.txt`; `delta_545ac9cb_d85da329.diff`; `gitlinks_head.txt`; `restore_check.txt` | R766-5 (delta); code unchanged since R766-4's RTL coverage | `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73` |
| Robustness | CLEAN | `check_baseline.log`; raw diff of the gate-read pages; `:360-371` | R766-5 | `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73` |
| Tests | CLEAN | `delta_probe.log`; own doc-gate logs and rc files; `evidence_verify.log`; `sha256sums_redaction_check.log`; author-r5 `gates/` receipts | R766-5 | `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73` |
| Docs | CLEAN | `MARK_II_AREA_PLAN.md:231-241, :336, :339-340, :367-368, :476-484, :1075, :1260`; the live PR body; commit messages; em-dash, style, TOC, anchor, path and `diff --check` gates | R766-5 | `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73` |

## Real limits

- **Hygiene was not re-run here.** The mechanical hygiene ratchet refused, because this clone's submodules are uninitialized. I relied on the author's manifest-verified receipt at the exact head instead. The delta touches no file that the ratchet scans.
- **The FIFO split is the author's.** The 16/5/8 split of the 29 FIFO RAMB36 comes from the author's published, hash-verified synthesis mapping. I did not reproduce it from the basis reports, which are outside the repository.
- **No signatures.** Neither the head nor the evidence commit is signed. Integrity rests on the git blob ids and `MANIFEST.json`.
- **Hosted runs prove nothing yet.** They were unfinished at the snapshot, and no conclusion is drawn from them.
- **No manager source bank** ran at this head, and none is claimed. Source-head execution evidence is the author's published gate receipts plus my doc-gate re-runs.
- **No builder, simulation, synthesis, Docker or act run** was made by this round.
- **No hardware.** Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Own hosted and act acceptance at the exact head once the in-progress and queued contexts finish.
- Validate the current-dev merge candidate (source base `503bc97c`, live dev `e61a4afa`) with the builder and native banks, and link the receipts on the PR. Re-run the census coverage check there, since dev's movement touches `sw/litex/milan_soc.py`, which the census reads.
- Close the completion bar's remaining bullets: the second independent positive, candidate-merge validation, explicit maintainer authorization to merge, post-merge containment, and the issue's close and move to `Done`.
- Carry the optional suggestions (R765-3-S1, R765-2-S1 / R766-2-S1, R766-2-S2, R766-2-S3, R765-2-S4). They have no effect on coverage.

R766-5 FINISHED

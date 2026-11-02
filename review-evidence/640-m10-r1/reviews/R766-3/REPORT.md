[R766] POSITIVE - exact head d52e966bb7258184e33702a9edd9ca11b4b1362c

# R766-3: external independent re-review of PR #835 (issue #640)

- Exact head `d52e966bb7258184e33702a9edd9ca11b4b1362c`, tree `4f12d77661d545c8bd5676ceaa1654328d79ce94`, merge base and live `dev` `503bc97cd4f24ad07596c17e7188f2024617972d`.
- Round 3 delta: `30eb4834..d52e966b`, one commit, `docs/design/MARK_II_AREA_PLAN.md` only (+10 / -5). Receipt: `receipts/delta_30eb4834_d52e966b.diff`.
- Verdict: POSITIVE. There are no open BLOCKER, MAJOR or MINOR findings.
  - R766-2-F1 is resolved at its cause.
  - All five lenses are CLEAN at this head.
  - Two RESIDUE items are recorded below, and earlier suggestions are carried. None affects the verdict.

## How the task was reconstructed

1. `AGENTS.md`, then #640's body. The body holds the owner's target, the stages and the acceptance of 2026-10-31.
2. The owner's LiteX stages comment (#640 issuecomment-6545999204). Its stage 1 words are "Drop DDR3 and the BIOS ROM ... This also frees Block RAM." It says nothing of the BIOS SRAM or of 18 RAMB36.
3. PR #835's body and the round 3 REVIEW READY (#640 issuecomment-6580708443).
4. The authorities behind the BIOS statements:
   - `sw/litex/milan_soc.py:3166-3177`: under `--ctrl-mailbox`, `integrated_rom_size=0, integrated_sram_size=0`, and the split runs no BIOS.
   - `sw/litex/ctrl_memory.py:7-14, 127-129`: `rom` at the reset address holds the load image; `sram` holds .data, .bss and the stack.
   - `docs/design/SPLIT_CONTROL_MEMORY.md:8, 56, 109`.
5. The delta, then the whole plan and the other pages searched for every BIOS statement (`receipts/bios_statements_at_head.txt`).
6. Only after that pass: the prior public findings (R765-1, R766-1, R765-2, R766-2) were read and resolved below.

## Executed checks (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| Docs gates at the head, run with the pinned Markdown renderer from `tools/markdown/requirements.txt`, installed by hash into a disposable environment: `docs_check`, `check_em_dash --base 503bc97c`, `check_doc_style` and `--selftest`, `gen_toc --selftest/--verify-anchors/--check`, `check_doc_paths` | all rc 0 | `receipts/docs_gates.rc`, `receipts/scripts_*.log`, `receipts/renderer_versions.txt` |
| `git diff --check 503bc97c HEAD` | rc 0, empty | `receipts/diff_check.log` |
| `syn/ooc/pp_resource_gate.py check-baseline`, the gate-read reader | `baseline PASS: 3 endpoints`, rc 0 | `receipts/check_baseline.log` |
| PR's changed-block style probe (`style_probe.py`, copied verbatim from the PR body) | prints nothing | `receipts/style_probe.log`, `receipts/style_probe.rc` |
| In-page anchor probe (`anchor_probe.py`) on the four PR pages | 0 missing anchors on each | `receipts/anchor_probe.log` |
| Sensitivity of both probes | a planted 11-word sentence at `:238` is reported; a planted bad anchor at `:241` fails with rc 1 | `receipts/probe_sensitivity.txt` |
| Mutation against the stock gates (see the limits) | neither the bad anchor nor the 11-word sentence fails `docs_check`, `gen_toc --verify-anchors` or `check_doc_style` | `receipts/mutations.txt`, `receipts/mut*.log` |
| Proposed residue fixes applied in memory | 0 new style findings | `fix_style_probe.py`, `receipts/fix_style_probe.txt` |
| Author round 3 receipts (`review-evidence/640-m10-r1/author-r3` at `2d4e9e21`) | see below | `verify_manifest.py`, `receipts/author_r3_manifest_verify.txt`, `receipts/author_r3_sha256sums_check.txt` |
| Hosted contexts at the head (read-only snapshot) | 4 completed success; 7 in progress; 10 queued; 0 statuses | `receipts/hosted_check_runs.tsv`, `receipts/hosted_statuses.tsv`, `receipts/hosted_snapshot_time.txt` |
| Restore after probes | head, index tree `4f12d776`, worktree equal to HEAD, 0 porcelain lines, index modes and blobs equal to the HEAD tree, six gitlinks unchanged | `receipts/restore_verify.txt` |

The author's round 3 receipts were verified as follows:

- All 135 files under `author-r3/` match `published_sha256` in the evidence `MANIFEST.json`.
- The author's own `SHA256SUMS` has 16 mismatches. Every one is a file the manifest marks `path_redacted`, and its `original_sha256` equals the author's digest. None is unexplained.
- The gate log names `Source revision: d52e966bb7258184e33702a9edd9ca11b4b1362c`.
- All 55 `.rc` files read 0. The gitlinks in `final_submodules.txt` equal this head's six gitlinks.
- The builder legs report items NOT RUN: `gate_24` has 1, and `gate_25_1` has "ALL GATES PASS EXCEPT 16 NOT RUN". Those items are not execution evidence.

## R766-2-F1 at its cause

R766-2-F1 required two things:

- The BIOS rows say the switch-over removes the BIOS and its integrated ROM and SRAM; `ctrl_memory`'s `rom` and `sram` banks hold those regions until stage 3; from stage 1 the boot loader fills `rom` (D18).
- Lane 2 no longer claims the BIOS ROM.

Every BIOS statement at the head was checked against that outcome. The plan is `docs/design/MARK_II_AREA_PLAN.md`.

| Where | Statement at the head | Agrees |
|---|---|---|
| Plan `:333`, BIOS ROM row | "Removed at the switch-over: the split build runs no BIOS and builds no integrated ROM ... `ctrl_memory`'s `rom` banks hold the region and the reset entry until stage 3, then first-party Block RAM ... From stage 1 the boot loader fills `rom` from the flash copy (D18)" | Yes. `milan_soc.py:3176` sets `integrated_rom_size=0`; `ctrl_memory.py:12-13, 128` puts `rom` at the reset address with the load image |
| Plan `:334`, BIOS SRAM row | "Removed at the switch-over: the split build builds no integrated SRAM. `ctrl_memory`'s `sram` banks hold the region until stage 3" | Yes. The false "builds none" is gone; `ctrl_memory.py:13, 129` |
| Plan `:336`, `ctrl_memory` row | Stage 3, first-party Block RAM, filled by the boot loader (D18) | Yes, and the BIOS rows point to it |
| Plan `:432`, lane 2 scope | "Drop DDR3 (lane 1 already drops the BIOS memory); a boot loader filling `rom` from the firmware's QSPI flash copy (D18)" | Yes. No BIOS ROM claim remains |
| Plan `:235-241`, note under the stage table | The switch-over removes the BIOS and its ROM and SRAM; the banks hold them until stage 3; stage 1 drops DDR3 and fills `rom` from flash | Yes. See RESIDUE-1 and RESIDUE-2 for two wording points |
| Plan `:112`, basis row | "The switch-over and LiteX stages 1 to 3; ... 18 BIOS ROM and SRAM" | Yes |
| Plan `:299`, `:416`, D19 | "beyond DDR3 and the BIOS" | Yes. These lines name no stage |
| Plan `:387-388`, Block RAM ledger | "18 BIOS memory. All 47 are gone once LiteX stage 3 ends" | Yes |
| Plan `:1302`, `:1312`, `:1335`, M8a-1 | "BIOS ROM and SRAM not built in the split", -18 | Yes. This is the only Block RAM credit for the 18 |
| `AREA_BUDGET.md:301-310` | Same M8a-1 statement | Yes |
| `MAILBOX_SPLIT.md:1152` | The split "builds no BIOS ROM or BIOS SRAM, and builds `rom` and `sram` block RAM from that image" | Yes |
| `SPLIT_CONTROL_MEMORY.md:8, 56, 109`; `ARCHITECTURE_HW_SW_SPLIT.md:252` | Not in this PR | Yes |
| Plan `:231`, stage table row 1 | Change: "Drop DDR3 and the BIOS ROM" (the owner's words). Removes: "LiteDRAM controller and PHY; BIOS ROM and SRAM, 18 RAMB36 measured" | Reconciled by the note directly below it. R766-2 accepted this reading, and this round keeps it. The note's own description of the row is imprecise (RESIDUE-1) |

So R766-2-F1 is **resolved**:

- The census fates no longer say "nothing in its place".
- The SRAM row no longer denies the split's `sram`.
- Lane 2 no longer drops a ROM that lane 1 removed.
- Every other site agrees.

The `ctrl_memory` banks and the stage 1 fill are also checked. The rows say that `rom` holds the reset entry and that from stage 1 the boot loader fills `rom`. These two claims are consistent with `:336` and D18. Where the boot loader itself sits in or beside `rom` is the stage 1 lane's design, and the plan does not need to fix it here.

## Prior findings, resolved or retained at this head

| Finding | Status at `d52e966b` |
|---|---|
| R766-2-F1 (MINOR; Conformance, Docs) | **Resolved**, as above |
| R765-1-F1 to F5; R766-1-F1 to F3; R766-1-R1 | Resolved at `30eb4834` (R766-2's table). The delta touches only the BIOS rows, the note and lane 2's scope, so it changes nothing those resolutions depend on. **Still resolved** |
| R765-2-RESIDUE-1 (`:368`, "Under 10 ms, the buffer would be 128 bytes.") | **Retained, unchanged.** Carried by the manager's residue checklist |
| R765-2-RESIDUE-2 (`:336`, "Stage 1 already fills `rom` ...", present tense) | **Retained, unchanged.** The new BIOS ROM row writes the same fact correctly as "From stage 1 the boot loader fills `rom`", so applying RESIDUE-2's exact fix would make `:333` and `:336` read alike |
| R765-2-S2 (link the BIOS rows to the `ctrl_memory` row) | **Taken by the delta** (`:333-334` name "the `ctrl_memory` row") |
| R765-2-S3 (stage table row 1's Removes cell) | **Open; folded into RESIDUE-1**, because the delta's new note now describes that row inaccurately |
| R765-2-S1 / R766-2-S1 (T_svc = 20 ms is owner-approved) | Not taken; optional. **Retained as a suggestion** |
| R766-2-S2 (name the probe board) | Not taken; optional. **Retained** |
| R766-2-S3 (`MilanMAC`'s first-party glue in the census) | Not taken; optional. **Retained** |
| R765-2-S4 (sub-row LUTs inside the CPU wrapper's 3,249) | Not taken; optional. **Retained** |
| R765-1-S2, S3; R766-1-S2, S3 | Not taken, with reasons in the PR body. No coverage effect |

## Findings

There are no BLOCKER, MAJOR or MINOR findings.

### R766-3-RESIDUE-1: the note says stage 1's row keeps the owner's words, but its Removes cell does not

- **Lenses:** Docs, Conformance.
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:235`, "Stage 1's row keeps the owner's words.", read against the `:231` Removes cell, "LiteDRAM controller and PHY; BIOS ROM and SRAM, 18 RAMB36 measured".
- **Evidence:**
  - The owner's stage 1 text (#640 issuecomment-6545999204) is "Drop DDR3 and the BIOS ROM". It names neither the SRAM nor 18 RAMB36.
  - So only the Change cell keeps the owner's words. The Removes cell is the plan's own text, and it places the 18 RAMB36 at stage 1.
  - The next lines of the note (`:236-241`), the census, lane 2's scope and M8a-1 all place the BIOS memory at the switch-over. The plan's attribution is therefore unambiguous once the note is read.
  - No sum credits the 18 twice: the stage table credits only LUTs (`Lever 1, ~1.0k LUTs`), and the Block RAM ledger credits no stage.
  - This is wording only. R765-2-S3 adds that a stage 1 routed measurement will not see those 18 RAMB36 leave.
- **Impact:** None to any figure. A reader who trusts the note's first sentence may take the whole row as the owner's text, the 18 RAMB36 included.
- **Exact fix (preferred):** make the Removes cell at `:231` read "LiteDRAM controller and PHY; BIOS ROM and SRAM, 18 RAMB36 measured, already gone at the switch-over". The note is then true as written. This is R765-2-S3's text.
- **Alternative exact fix:** change `:235` to "Stage 1's Change cell keeps the owner's words." (seven words).
- **Verification:** read `:231` and `:235-241` together, and run `check_doc_style.py`. With the preferred fix applied in memory, `fix_style_probe.py` reports 0 new findings.

### R766-3-RESIDUE-2: "them" can be read as the BIOS itself

- **Lenses:** Docs.
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:239`, "`ctrl_memory`'s `rom` and `sram` banks hold them until stage 3."
- **Evidence:** The antecedent at `:238` is "the BIOS and its ROM and SRAM". The banks hold the regions, not the BIOS, which the split does not run. The census rows at `:333-334` say "hold the region".
- **Impact:** None to any figure. A reader may take the BIOS to survive in `ctrl_memory` until stage 3.
- **Exact fix:** "Until stage 3, `ctrl_memory`'s banks hold both regions." (eight words). The exact form with "those regions" would be 11 words, over the limit.
- **Verification:** read `:238-239` and run `check_doc_style.py`. `fix_style_probe.py` reports 0 new findings for this text.

### Suggestions

There are no new suggestions this round. The carried suggestions are listed in the prior-findings table.

### Comment rule

The delta adds no source comment, so the rule has nothing to apply to. The plan's "lane 1" and "Lane 1" name the plan's own lane sequence (`:420-432`), not a bench lane label in source.

## Per-lens results at `d52e966b`

```text
[R766] PASS Conformance — docs/design/MARK_II_AREA_PLAN.md:112, 231-241, 299, 333-336, 387-388, 416, 432, 1302-1335; docs/design/AREA_BUDGET.md:301-310; docs/design/MAILBOX_SPLIT.md:1152 — every BIOS-memory statement checked against sw/litex/milan_soc.py:3166-3177, sw/litex/ctrl_memory.py:7-14, 127-129, SPLIT_CONTROL_MEMORY.md:8, 56, 109, D18 and the owner's stage text (#640 issuecomment-6545999204); R766-2-F1's required outcome met; RESIDUE-1 is wording only
[R766] PASS RTL — git diff 503bc97c..d52e966b (receipts/full_diffstat.txt: four Markdown pages, no HDL, generator, constraint or firmware file); the round 3 delta is one Markdown page; the split-build source the delta describes (milan_soc.py:3166-3177, ctrl_memory.py:127-129) is unchanged and agrees with the new rows
[R766] PASS Robustness — receipts/delta_30eb4834_d52e966b.diff: no executable, configuration or gate input changes; the gate-read pages' reader re-run at the head (receipts/check_baseline.log, baseline PASS: 3 endpoints); the rows' boot-path claims (reset entry in rom, the stage 1 fill from flash) checked against ctrl_memory.py:264-290 and D18/D21; no failure path changes
[R766] PASS Tests — receipts/docs_gates.rc (nine docs gates rc 0 at the head with the pinned renderer), receipts/style_probe.log, receipts/anchor_probe.log, receipts/probe_sensitivity.txt (both probes fail on planted faults), author-r3 receipts verified (receipts/author_r3_manifest_verify.txt: 135 published digests match, 16 author-digest differences all path-redacted, 55 rc files 0, head named)
[R766] PASS Docs — docs/design/MARK_II_AREA_PLAN.md over 30eb4834..d52e966b, and every BIOS statement on the four PR pages (receipts/bios_statements_at_head.txt); the PR #835 body's Round 3 section matches the delta; style, em-dash, TOC and anchors clean; RESIDUE-1 and RESIDUE-2 recorded with exact fixes
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `MARK_II_AREA_PLAN.md:112, 231-241, 299, 333-336, 387-388, 416, 432, 1302-1335`; `AREA_BUDGET.md:301-310`; `MAILBOX_SPLIT.md:1152`; `milan_soc.py:3166-3177`; `ctrl_memory.py:7-14, 127-129`; `SPLIT_CONTROL_MEMORY.md:8, 56, 109`; #640 issuecomment-6545999204 and -6575277828 (D18, D21). Other content: R766-2's coverage at `30eb4834`, untouched by the delta | R766-3 | `d52e966bb7258184e33702a9edd9ca11b4b1362c` |
| RTL | CLEAN | Full diffstat `503bc97c..d52e966b` (four Markdown pages); delta `30eb4834..d52e966b`; split-build source unchanged | R766-3 (R766-2 at `30eb4834` for the earlier content; no RTL-scope artifact changed since) | `d52e966bb7258184e33702a9edd9ca11b4b1362c` |
| Robustness | CLEAN | Delta; `check_baseline.log`; `ctrl_memory.py:264-290`; D18, D21 | R766-3 | `d52e966bb7258184e33702a9edd9ca11b4b1362c` |
| Tests | CLEAN | Docs gates, style and anchor probes with sensitivity proofs; author-r3 receipts at `2d4e9e21` | R766-3 | `d52e966bb7258184e33702a9edd9ca11b4b1362c` |
| Docs | CLEAN (RESIDUE-1, RESIDUE-2 carried, not blocking) | Delta in full; BIOS statements on all four PR pages; PR #835 body | R766-3 | `d52e966bb7258184e33702a9edd9ca11b4b1362c` |

## Real limits

- **No manager source bank** runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published round 3 receipts. Their 55 rc-0 steps were verified by digest, not re-executed. The builder legs' NOT RUN items (1 in `gate_24`, 16 in `gate_25_1`) are not execution evidence.
- **Hosted contexts** were still running at the snapshot time (`receipts/hosted_snapshot_time.txt`): 4 succeeded, 7 in progress, 10 queued. This round claims no hosted verdict.
- **Submodules** are not initialised in this clone. The docs gates here ran without them and passed. The author's clean-clone run with four submodules is the evidence for the submodule-reading steps.
- **The stock docs gates miss these faults on this page.** `docs_check.py`, `gen_toc.py --verify-anchors` and `check_doc_style.py` did not fail on a planted bad in-page anchor or an 11-word sentence in `MARK_II_AREA_PLAN.md` (`receipts/mutations.txt`). The style limit is enforced for this page only by the PR's changed-block probe, and the anchors only by this round's own probe. This gap existed before the PR and is not introduced by it. It is a candidate for a separate Issue, not a finding here.
- The anchor probe uses a simplified GitHub slug rule. It found 0 missing anchors, and it does fail on a planted fault.
- **Physical calibration NOT RUN.** No hardware was used. This is a documentation-only change.
- The census coverage check was not re-run: the delta changes no row's mapping key. The author's round 3 `census_coverage.out` is digest-verified as published.

## Pending manager duties

- Build and validate the current-`dev` merge candidate (base `503bc97c`) at the merge turn, and link the builder and native bank receipts on the PR.
- Own the hosted and local-replica acceptance at the exact head. The hosted contexts were not complete at this snapshot.
- Carry R766-3-RESIDUE-1 and RESIDUE-2, with R765-2-RESIDUE-1 and RESIDUE-2, to the residue checklist.
- Route the retained suggestions to the author at their discretion: R765-2-S1/S4 and R766-2-S1/S2/S3.
- Consider an Issue for the stock gates' blind spot on this page (in-page anchors and the style limit).

R766-3 FINISHED

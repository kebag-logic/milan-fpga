[R765] NEGATIVE - exact head d52e966bb7258184e33702a9edd9ca11b4b1362c

# R765-3: internal cleared-context review of PR #835 (issue #640), round 3

- Head: `d52e966bb7258184e33702a9edd9ca11b4b1362c`, tree `4f12d77661d545c8bd5676ceaa1654328d79ce94`, verified in the review clone (`receipts/restore_check.out`).
- Source base: `503bc97cd4f24ad07596c17e7188f2024617972d`. Live `dev` has since moved to `e61a4afa` (see pending manager duties).
- Round 3 delta: `30eb4834..d52e966b`, one commit. It touches `docs/design/MARK_II_AREA_PLAN.md` only, +10/-5, mode 100644 unchanged. The commit message is one line with no trailers (`receipts/commit_d52e966b.txt`).
- Verdict: **NEGATIVE** on one MINOR (F1).
  - F1 is the last part of R766-2-F1's cause. The stage table's stage 1 "Removes" cell still credits stage 1 with removing the BIOS ROM and SRAM, "18 RAMB36 measured". Every other statement on the page and on the linked pages says the switch-over removes them.
  - The census rows, the note and lane 2's scope are now correct. One residue item and one suggestion are below.
  - RTL, Robustness and Tests are CLEAN at this head. Conformance and Docs are UNCLEAN on F1 only.

## How this round reconstructed the task

1. `AGENTS.md`, plus `CONTRIBUTING.md` by reference, for the lenses, severities and ledger rule.
2. Owner comments the delta rests on, fetched read-only (`receipts/issuecomment-*.json`):
   - the staged LiteX removal, [6545999204](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545999204);
   - the 20k decision with the 18-RAMB36 BIOS figure, [6545523624](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545523624);
   - D18 to D21, [6575277828](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6575277828).
3. The author's round 3 TAKEN ([6579495587](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6579495587)) and REVIEW READY ([6580708443](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6580708443)).
4. The full round 3 diff. I then searched for every BIOS, `ctrl_memory`, switch-over and D18 statement in:
   - the plan;
   - the other three PR pages (`AREA_BUDGET.md`, `MAILBOX_SPLIT.md`, `docs/findings/README.md`);
   - the linked `SPLIT_CONTROL_MEMORY.md` and `ARCHITECTURE_HW_SW_SPLIT.md`.
5. Checked the new text against the source it describes: `sw/litex/milan_soc.py:3003-3018`, `:3167-3177`, and `sw/litex/ctrl_memory.py:128-129`.
6. Wrote my independent findings to `receipts/independent_draft_before_prior_findings.txt` (written 15:17 UTC). Only then did I read the prior public reviews on PR #835 (R765-1, R766-1, R765-2, R766-2). I read no round 3 report from another reviewer, no private author material and no lane scratchpad.

## Executed checks

| Check | Result | Receipt |
|---|---|---|
| Published round 3 evidence `review-evidence/640-m10-r1/author-r3` at `2d4e9e21`. Every file checked against `MANIFEST.json`'s published hash, and every `SHA256SUMS` entry against the manifest's original hash | 135 files, 0 mismatch, 0 missing. 132 SUMS entries, 0 bad, rc 0 | `receipts/verify_evidence_r3.out`, `scripts/verify_evidence.py` |
| Author's `round3.diff` against my `git diff 30eb4834 d52e966b` | byte-identical | `receipts/delta_30eb4834_d52e966b.diff` |
| Author's gate rc files (`author-r3/evidence/gates/logs/*.rc`) | 55 of 55 rc 0 | tallied from the extracted packet |
| Author's `census_coverage.py` (from `author-r2/evidence/census`, read before running) on the head page | rc 0, PASS, 23 rows, none unmapped. Byte-identical to the author's published `author-r3/evidence/census_coverage.out`. The BIOS rows map as "Switch-over, lane 1", and `ctrl_memory`'s parts map to stage 3 | `receipts/census_coverage_head.out` |
| `docs_check.py` | rc 0: 0 findings, 213 md files | `receipts/gate_docs_check.*` |
| `check_doc_style.py --selftest` | rc 0 | `receipts/gate_doc_style_selftest.*` |
| `check_doc_style.analyze()`: findings at the head that are absent at the base, by reason and text | Round 3 page vs `30eb4834`: 0 new. Four PR pages vs `503bc97c`: 0 new | `receipts/style_new_r3.out`, `receipts/style_new_pr.out`, `scripts/style_new.py` |
| `gen_toc.py --check`, `--verify-anchors`, and `check_em_dash.py --base 503bc97c`, using the pinned renderer in a disposable venv | rc 0, rc 0, rc 0. TOC OK; 586 cross-page fragments reproduced; 0 em-dash findings over 230 added lines | `receipts/gate_venv_*` |
| `git diff --check 503bc97c HEAD` | rc 0 | `receipts/gate_diff_check.*` |
| Source facts behind the new census text | All hold: the split sets `integrated_rom_size=0, integrated_sram_size=0` (`milan_soc.py:3176`) and `integrated_rom_initialized` (`:3018`), so no BIOS. `add_ctrl_memory` adds `rom` ("rx") and `sram` ("rwx") at the same origins (`:3011-3016`; `ctrl_memory.py:128-129`). `rom`'s first word is the reset entry (`:3004`) | source at the head |
| Exact-head hosted contexts, read-only snapshot | Completed with success: `bdd-conformance`, `changes`, `docs-check-no-git`, `wire-accountability`. 7 were in progress and 10 queued. I draw no conclusion from those | `receipts/hosted_checks_d52e966b.tsv` |
| Restore | Worktree and index equal HEAD, and the index matches the tree in mode, blob and path for all 1,466 entries. Nothing is untracked or ignored. Six gitlinks unchanged and identical at `503bc97c`, `30eb4834` and the head. Python ran with `-B`, so it wrote no bytecode | `receipts/restore_check.out` |

## R766-2-F1 at its cause: every statement of who removes the BIOS memory

| Location at the head | Says | Agrees? |
|---|---|---|
| `MARK_II_AREA_PLAN.md:231`, stage table, stage 1 "Change" | "Drop DDR3 and the BIOS ROM" | The owner's words ([6545999204](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545999204) item 1). The note at `:235` flags them as such. Acceptable |
| `:231`, stage table, stage 1 "Removes" | "LiteDRAM controller and PHY; BIOS ROM and SRAM, 18 RAMB36 measured" | **No: F1** |
| `:235-241`, note | The switch-over removes the BIOS and its ROM and SRAM. `ctrl_memory`'s banks hold them until stage 3. Stage 1 drops DDR3 and fills `rom` from flash (D18) | Yes (residue R1 on "them") |
| `:299`, `:416`, D19 | "beyond DDR3 and the BIOS" | Yes, as the owner's scope words |
| `:333`, BIOS ROM census row | Removed at the switch-over, lane 1. `ctrl_memory`'s `rom` banks hold the region and the reset entry until stage 3. From stage 1 the loader fills `rom` | Yes |
| `:334`, BIOS SRAM census row | Removed at the switch-over. `ctrl_memory`'s `sram` banks hold the region until stage 3 | Yes |
| `:336`, `ctrl_memory` row | Stage 3, then first-party Block RAM | Yes (retained residue R765-2-RESIDUE-2) |
| `:387` | 18 BIOS RAMB36 in the LiteX top; all 47 gone once stage 3 ends | Yes |
| `:432`, lane 2 scope | "Drop DDR3 (lane 1 already drops the BIOS memory); a boot loader filling `rom`..." | Yes |
| `:802`, basis `@own` row | The basis contents include the BIOS ROM and SRAM, but not as a lever's credit | Yes |
| `:1302`, Block RAM ledger | "M8a-1: BIOS ROM and SRAM not built in the split", -18 RAMB36 | Yes |
| `AREA_BUDGET.md:301`, `:306-310` | The same -18 at M8a-1. The split builds neither BIOS memory | Yes |
| `MAILBOX_SPLIT.md:1152`; `SPLIT_CONTROL_MEMORY.md:5-8`, `:56`, `:109`, `:176`; `ARCHITECTURE_HW_SW_SPLIT.md:252` | The split builds no BIOS ROM or SRAM | Yes |

## Findings

### F1 MINOR: the stage table still credits stage 1 with the BIOS memory's measured 18 RAMB36

- **Lenses:** Conformance, Docs.
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:231`, stage table, row 1, "Removes" cell: "LiteDRAM controller and PHY; BIOS ROM and SRAM, 18 RAMB36 measured", credited as lever 1.
- **Authority and evidence:**
  - The page says a routed-image measurement follows each stage (`:227`). It credits the same measured 18 RAMB36 to the switch-over's split build in its own Block RAM ledger (`:1302`, "M8a-1 ... -18") and in `AREA_BUDGET.md:301`.
  - Two lines below the cell, the round 3 note says "The switch-over removes the BIOS and its ROM and SRAM" (`:238`). Lane 2's scope (`:432`) now says lane 1 already drops it.
  - The note's reconciliation, "Stage 1's row keeps the owner's words" (`:235`), covers the "Change" cell. The owner's stage list says "Drop DDR3 and the BIOS ROM ... This also frees Block RAM". It does not say "BIOS ROM and SRAM, 18 RAMB36 measured". That figure is the plan's own measured attribution, from M8a-1 at `e8454e27`, and the plan books it to the split.
  - The author's handoff (6580708443) says every other statement of who removes the BIOS memory already agreed, and lists this cell only under "keeps the owner's stage wording".
- **Why MINOR, not RESIDUE:** the cell attributes a measured figure to a stage. Moving it changes which stage's routed measurement is expected to show the 18 RAMB36 leave. That is a figure claim, not only wording.
- **Prior position, corrected:** R765-2 raised this cell as S3 (SUGGESTION). That was too lenient for the same reason. R766-2-F1 asked that the BIOS removal be stated consistently, and this cell is the one statement that still disagrees.
- **Impact:**
  - The stage 1 lane would expect its routed image to free 18 RAMB36 against the switch-over image, and it will not.
  - A reader adding stage credits from the stage table would count the BIOS memory at stage 1, while the ledger counts it at the switch-over.
- **Required outcome:**
  - Stage 1's "Removes" cell no longer credits stage 1 with the BIOS ROM and SRAM or their 18 RAMB36. It may say that they already left at the switch-over (M8a-1).
  - The owner's "Change" wording may stay, and the note should name which cell keeps the owner's words.
  - One possible wording, not prescribed:
    - "Removes": "LiteDRAM controller and PHY. The BIOS ROM and SRAM, 18 RAMB36 measured, left at the switch-over (M8a-1)".
    - Note `:235`: "Stage 1's change keeps the owner's words."
- **Verification:**
  - Read `:231` against `:238`, `:333-334`, `:432`, `:1302` and `AREA_BUDGET.md:301`.
  - Re-run `census_coverage.py`. The stage table lies outside the census section, so the result should be unchanged.
  - Run `check_doc_style` on the changed blocks, plus `gen_toc --check` and `check_em_dash`.

### R1 RESIDUE: "hold them" takes the BIOS as its object

- **Lenses:** Docs.
- **Where:** `MARK_II_AREA_PLAN.md:239`: "`ctrl_memory`'s `rom` and `sram` banks hold them until stage 3."
- **Evidence:** the antecedent at `:238` is "the BIOS and its ROM and SRAM". The banks hold the regions and the firmware image, not the BIOS (`milan_soc.py:3003-3018`). The census rows say "the region" correctly.
- **Impact:** wording only. No figure or claim changes.
- **Exact fix:** "`ctrl_memory`'s `rom` and `sram` banks hold those regions until stage 3." `check_doc_style.analyze()` reports no finding on this sentence.
- **Verification:** read `:238-239`, then run `check_doc_style`.

### S1 SUGGESTION: say where stage 1's loader runs, since `rom` is read-only and holds the reset entry

- **Lenses:** RTL, Docs.
- **Where:** `MARK_II_AREA_PLAN.md:241`, `:333`, `:336` and `:432`, "the boot loader fills `rom`".
- **Evidence:**
  - Today `rom` is mapped "rx" and initialised from the configuration image (`milan_soc.py:3011-3016`; `SPLIT_CONTROL_MEMORY.md:55`).
  - Its first word is the CPU's reset entry (`SPLIT_CONTROL_MEMORY.md:25`; refusal `entry address`).
  - A loader that fills `rom` must run from somewhere else, and `rom` must become writable to it. D18 ("copies the firmware from QSPI flash into block RAM") leaves both to the stage 1 lane.
  - This interpretation predates the round (`:336` since `7f5ea1c8`) and is what R766-2-F1 asked for. It does not affect coverage.
- **Suggestion:** one clause, either in `### Stage 1 boot and bus` or in lane 2's scope, saying that the stage 1 lane settles the loader's own storage and the reset entry.

## Prior public findings at this head

| Finding | State at `d52e966b` | Evidence |
|---|---|---|
| R766-2-F1 (MINOR): which lane removes the BIOS memory, and what holds its place | **Resolved in the three places it named. Retained in cause as F1.** `:333` and `:334` now say "removed at the switch-over", and `ctrl_memory`'s banks hold the regions until stage 3. "Nothing in its place" and "builds none" are gone. Lane 2 (`:432`) no longer drops the BIOS ROM. The stage 1 "Removes" cell (`:231`) still credits stage 1 | see the agreement table |
| R766-2-S1, S2, S3 | Not taken (handoff (b)). They are optional, with no coverage effect | - |
| R765-2-RESIDUE-1: "Under 10 ms, the buffer would be 128 bytes." drops the table's assumption | **Retained as residue.** `:368` is unchanged. Exact fix as published: "Taking 10 ms as the gap gives 128 bytes." | `:360`, `:368` |
| R765-2-RESIDUE-2: "Stage 1 already fills `rom` ..." in the present tense | **Retained as residue.** `:336` is unchanged. Round 3's own text uses "From stage 1" (`:333`), so this cell is now the only present-tense outlier. Exact fix as published: "From stage 1, `rom` is filled from the flash copy, not the configuration image." | `:336` |
| R765-2-S1 (T_svc 20 ms owner-approved), S4 (sub-row LUTs inside 3,249) | Not taken. Optional | - |
| R765-2-S2 (link the BIOS rows to the row that takes their addresses) | Taken in substance: `:333-334` now name `ctrl_memory`'s banks and the `ctrl_memory` row | `:333-334` |
| R765-2-S3 (stage 1 "Removes" cell) | **Escalated to F1** | above |
| R765-1-F1 to F5, R766-1-F1 to F3, R766-1-R1, and their suggestions | Resolved at `30eb4834`, as recorded by R765-2 and R766-2. The round 3 hunks (`:232-241`, `:330-331`, `:429` of the base) touch none of the lines those resolutions rest on, except R765-1-F1's BIOS rows, which are covered above | `receipts/delta_30eb4834_d52e966b.diff` |

Comment rule: the delta adds no source comment, so there is nothing to apply it to. The page names lanes, which findings pages and plan text may do.

## Per-lens results

```text
[R765] MINOR Conformance — docs/design/MARK_II_AREA_PLAN.md:231 — F1: stage 1 "Removes" credits the BIOS memory's measured 18 RAMB36, which :238, :333-334, :432, :1302 and AREA_BUDGET.md:301 book to the switch-over
[R765] PASS RTL — sw/litex/milan_soc.py:3003-3018, :3167-3177; sw/litex/ctrl_memory.py:128-129; MARK_II_AREA_PLAN.md:238-241, :333-334 — the delta's RTL-bearing claims (no BIOS and no integrated ROM or SRAM in the split; rom and sram banks at the BIOS origins; rom holds the reset entry) checked against the SoC build at the head. No RTL or build source in the delta (git diff --raw)
[R765] PASS Robustness — receipts/delta_30eb4834_d52e966b.diff; MARK_II_AREA_PLAN.md:351-369 unchanged — the delta changes no failure, timeout, overflow or configuration-dependent claim. The split refuses a missing --ctrl-firmware (milan_soc.py:3172-3175) as the census row's "runs no BIOS" assumes
[R765] PASS Tests — receipts/census_coverage_head.out, receipts/verify_evidence_r3.out, receipts/gate_* — census coverage rerun PASS and byte-identical to the author's. The author's 55 gate rc files are 0 and its evidence hashes verify. My docs_check, style delta, TOC, anchor, em-dash and diff checks are all rc 0. The delta adds no test and changes no tested artifact
[R765] MINOR Docs — docs/design/MARK_II_AREA_PLAN.md:231, :235 — F1: the note says stage 1's row keeps the owner's words, but the "Removes" cell is the plan's measured attribution and contradicts the note. Residue R1 at :239
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | owner comments 6545999204, 6545523624, 6575277828; `MARK_II_AREA_PLAN.md:227-241`, `:299`, `:333-336`, `:387`, `:416`, `:432`, `:1302`; `AREA_BUDGET.md:301-310` | R765-3 | `d52e966bb7258184e33702a9edd9ca11b4b1362c` |
| RTL | CLEAN | `milan_soc.py:3003-3018`, `:3167-3177`; `ctrl_memory.py:128-129`; `SPLIT_CONTROL_MEMORY.md:25`, `:55`; delta `--raw` (docs only) | R765-3 | `d52e966bb7258184e33702a9edd9ca11b4b1362c` |
| Robustness | CLEAN | delta diff; `MARK_II_AREA_PLAN.md:351-369` (unchanged); `milan_soc.py:3172-3175` | R765-3 | `d52e966bb7258184e33702a9edd9ca11b4b1362c` |
| Tests | CLEAN | census coverage rerun; author-r3 evidence (135 files) verified; docs gates rc 0 | R765-3 | `d52e966bb7258184e33702a9edd9ca11b4b1362c` |
| Docs | UNCLEAN (F1; residue R1, and retained R765-2-RESIDUE-1 and -2 carried) | the four PR pages; `SPLIT_CONTROL_MEMORY.md`; `ARCHITECTURE_HW_SW_SPLIT.md:252`; style, TOC, anchor and em-dash gates | R765-3 | `d52e966bb7258184e33702a9edd9ca11b4b1362c` |

## Limits

- I ran no manager source bank and claim none. Source-head execution evidence is the author's published gate receipts, which I verified by hash, plus my own docs gates and census rerun at this head.
- I did not run the parent, PP, gPTP, Yosys or builder banks, Docker, act, or `act_ci` (not allowed). No physical calibration was run. Field skips are not hardware proof.
- Hosted contexts: 4 succeeded at the snapshot, and the rest were in progress or queued. I draw no conclusion from them, and the manager owns hosted and act acceptance.
- I read prior public reviews only after writing the independent draft. I did not read R766-3.

## Pending manager duties

- **Live `dev` moved.** At review time `dev` was `e61a4afa`, 18 commits past the stated base `503bc97c` (`receipts/live_dev.txt`, `receipts/dev_movement.txt`).
  - None of those commits touch the four PR pages.
  - They do change `sw/litex/milan_soc.py` (gPTP launch/observer parameters for the MII PHY model, with no new LiteX block or CSR seen in the patch) and `REQUIREMENTS.md` (`receipts/dev_movement_soc_req.patch`).
  - The merge candidate must be built and validated on the current `dev`. The census coverage check reads `milan_soc.py`, so re-run it on the candidate.
- Exact-head hosted `rtl-fast` and docs contexts, and act replication.
- The second independent positive review.
- Carry R1, R765-2-RESIDUE-1 and R765-2-RESIDUE-2 to the residue checklist.
- Re-review after F1 is fixed. Conformance and Docs must be covered again at a head that includes the fix.

R765-3 FINISHED

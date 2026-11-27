[R927] NEGATIVE - exact head 011aaa6f080321e0a89f915720ebb3ee14807a16

# R927-3: internal cleared-context re-review of PR #1004 (relates to #878)

Head `011aaa6f080321e0a89f915720ebb3ee14807a16`, tree `5b11a07de8c4f69999277424aa8d9b704c297a96`. The delta reviewed is `4adfa9dc..011aaa6f` (five commits). The author packet is `review-evidence/artysplit-r1/author-r8` at evidence commit `7ae7427b0d5a021db3387fa50833abde7bf18a82`.

- **Verdict: NEGATIVE.** Two MINOR findings are open, so `Conformance`, `Tests` and `Docs` are unclean. `RTL` and `Robustness` are clean at this head.
- **The main finding (F1):** the census extract as published does not regrade. The publication step rewrote 27 of its files, keeping their lengths, after the author's inventory was taken. The published bytes then fail the regrader's own integrity check in 24 cases. Even with the hashes re-bound to the published bytes, one case's grade no longer reproduces, so neither the cross-case step nor the `srp-bound` control can run on public bytes. The other 123 cases do reproduce from public bytes.
- **Everything else asked of this round holds at the head:**
  - #1022 owns the owed lines, and I reproduced the control derivation byte for byte.
  - The README points to the installed row's qualification, and the head's model equals it.
  - The paired identity, the post-route utilization and every listed residue are resolved.
  - The delta changes no firmware, RTL, row, image, submodule or generated configuration.

## The round's six items

| # | Item | Result at this head | Evidence |
|---|---|---|---|
| 1 | Census extract regrades all 147 cases and the cross-case step; the control without `srp-bound` is refused | **Not met on the published bytes (F1).** 123/147 cases reproduce. 24 fail with `part integrity failure`. After re-binding the hashes, 146/147 reproduce and `srp-talker` fails with `grade differs`, so neither the cross-case step nor the control's own refusal is reached | `receipts/inventory-check.log`, `publication-delta.log`, `percase-public.summary`, `probe-rebound-regrade.log`, `probe-rebound-control.log`, `probe-srp-talker-grade-diff.log` |
| 2 | Paired step-1/step-2 identity (8 executables and ELFs, 147 stimuli) and the `flash: null` explanation | Met (as an author receipt). Every pair is side by side, from each step's own files. All 147 stimulus hashes equal the extract's `stimulus` records. `build.py:906-921` writes `flash_image` only when `core.xip` is set | `receipts/identity-vs-extract.log`; `identity/paired-identity.json`; `recipes/paired_identity.py` |
| 3 | Post-route utilization of rounds 7 and 6 | Met. Both reports say `Design State : Physopt postRoute`. Both give 33015 LUT / 40369 FF / 13791 slices / 78 BRAM tiles, a delta of 0. The report bodies from "Slice Logic" on are identical. Between `49b534fc9` and `74f942be5`, the only firmware file that changed is `ctrl_loop.h` (no RTL), so equal totals are expected. The round-7 bitstream `24a782c5...` is the graded image (`timing-r7/graded-images.json`) | `route-utilization/*.rpt`, `r7-identity.txt`, `r6-identity.txt`; `git diff --stat 49b534fc9..74f942be5` |
| 4 | #969's owed lines owned by #1022, cited in section 15; control derivation (~225 ms) | Met. #1022 is open, blocked by #977, and its acceptance names `arty-1x1`, the bounds and the control. `SPLIT_CONTROL_MEMORY.md:3520-3525` cites it and states the row choice. At the head, the published `derive-own.py` recipe on the published `merged-no-disposition.json` gives a **byte-identical** `derive-no-disposition.json`: NO QUALIFIED MODEL, 52/52 candidates with an owner finding, least last notice 225.54 ms. Re-merging the published inputs gives equal contents. The step-2 model's two choices are (10 ms, 125 ms, 1250 us) and (10 ms, 130 ms, 950 us), and the stated sort picks the first. The ROM figures check: 64+32+16+8+4 KiB = 126976, and 126976 - 125572 = 1404 | `receipts/control-derivation-repro.txt`; `author-r7/receipts/derivation/model-installed-r7-step2.json` |
| 5 | README cites the installed row's qualification | Met. `README.md:208-211` cites `published-qualification.json` at `907764eb`. Its SHA256 `076e7cc7...` matches, it is PASS over 147 groups, and the head's `arty_grade.py` model equals its `model` | `receipts/arty-grade-model-vs-qualification.txt`, `arty-grade-head.log` |
| 6 | Every residue | All are resolved: RS-A, RS-B, RS-C, RS-D, R927-1 RS1/RS3/RS4/RS5/RS6 and R928-2-RS1. Two new residues are listed below | Delta read line by line; live PR body |

**No firmware, RTL, row or image change.** I verified this rather than taking it from the packet:
- The delta touches no file under `hdl/`, `sw/firmware/` (outside `ctrl/test`), `sw/litex/` or any submodule gitlink.
- The four Python files with comment or EOF edits are AST-identical to their round-7 versions. The fixture values are identical (8 names).
- The split YAML's parsed value is unchanged.
- The builder's outputs for `configs/endstation_arty_split.yaml` are identical at `4adfa9dc` and at the head: 22 files, default and `--placement split` (`receipts/comment-only-identity.txt`, `builder-split-identity.txt`).

## Findings

### F1. MINOR. The published census extract does not reproduce its grades or the cross-case step

This retains R928-1-F1 / R928-2-F1 in narrowed form.

- **Lenses:** `Conformance`, `Tests`, `Docs`.
- **Artifacts:**
  - `review-evidence/artysplit-r1/author-r8/receipts/census-extract/` at `7ae7427b`.
  - `review-evidence/artysplit-r1/MANIFEST.json` at `7ae7427b`.
  - `receipts/INDEX.md` "Compact census extract".
  - PR body "Reproduce and inspect", plus the Definition-of-done line "[x] A regradable census extract ... in the evidence packet".
- **Authority:**
  - AGENTS.md sections 1, 6 and 7 require evidence a cold reviewer can reconstruct.
  - R928-2-F1's verification asks you to "run the current regrader to reproduce all 147 grades and cross-case checks; run the missing-`srp-bound` control and require refusal".
- **Evidence:**
  - Against the packet's own `FILES.tsv`, 27 published files fail: same size, different SHA256 (`inventory-check.log`; its 28th line is the by-design unlisted `INDEX.md`).
  - All 27 are observation logs or parts across 24 cases.
  - The publisher's `MANIFEST.json` marks each `path_redacted: true`. Its `original_sha256` equals the author's inventory hash, and its `published_sha256` equals the bytes on disk (`publication-delta.log`). So the length-preserving rewrite happened at publication, after extraction and regrading.
  - The head's `receipt_regrade.py`, run case by case on the published extract, gives 123 PASS and 24 `part integrity failure` (`percase-public.summary`, `percase-public/`).
  - A disposable probe re-bound every manifest to the published bytes (`scripts/rebind_probe.py`; no tracked file touched). On that copy:
    - 23 of the 24 altered cases still grade as recorded.
    - `valid-destinations/srp-talker` gives `grade differs`. The one differing leaf is `/passes/polls/passes`: recorded 160456, regraded 160455 (`probe-srp-talker-grade-diff.log`).
  - The full run therefore stops before `qualify` (`probe-rebound-regrade.log`). The control copy without `srp-bound` exits 1 at the same case, before its cross-case refusal (`probe-rebound-control.log`).
  - The author's `proofs/extract-regrade.log` and `extract-control.log` were produced on the pre-publication bytes. They are consistent execution receipts, but the public bytes do not reproduce them.
- **Impact:**
  - The installed row's 147-case qualification, the conditional #969 exclusion and the cross-case PASS still rest on the author's execution only.
  - The packet and PR body claim a public reproduction that fails. The published bytes of one case carry a different poll count than its recorded grade.
- **Required outcome:**
  - Publish the census extract exactly as `FILES.tsv` lists it. No rewrite may touch observation text whose hashes the manifests bind.
  - If a rewrite is needed for privacy, apply it before extraction, then regenerate, regrade and re-bind the extract on the rewritten bytes.
  - Make the PR body and INDEX claims true of the published packet.
- **Verification:**
  - `scripts/verify_inventory.py <receipts>` gives `RESULT: PASS listed=814` (INDEX.md aside).
  - `receipt_regrade.py census-extract` exits 0 with 147 PASS and `RESULT: PASS cross-case ...`.
  - A copy without `srp-bound` is refused by the cross-case step with the #977 line.

### F2. MINOR. The receipt cited for "generated outputs unchanged" is empty

- **Lenses:** `Tests`, `Docs`.
- **Artifacts:**
  - `receipts/gates/builder-split.log`, which is 0 bytes.
  - `receipts/INDEX.md` "Gates at the head" ("The split configuration's generated outputs are unchanged by its comment edits ([gates/builder-split.log](...))").
  - PR body "Validation" (line 93).
  - `recipes/gates8.sh`, which has no builder step; `gates8.rc` has no `builder-split` line.
- **Evidence:** the cited receipt holds nothing, and the published recipe does not produce it. The claim itself is true: my own run is `receipts/builder-split-identity.txt`, with 22 outputs identical across `4adfa9dc` and the head, both placements.
- **Impact:** the packet's only evidence for a "no image input changed" claim is an empty file. A cold reader cannot confirm it from the packet.
- **Required outcome:** the cited receipt records the comparison (command, both heads, output hashes or diff, exit code). Alternatively, the packet cites a published receipt that does.
- **Verification:** the cited file is non-empty and shows identical outputs at `4adfa9dc` and `011aaa6f`.

### RESIDUE (wording only; exact fixes)

- **RS-1** `tb/verilator/ctrl_service_budget/census_extract.py:11` and `tb/verilator/ctrl_service_budget/README.md:217`. Both say `FILES.json` maps every file written. It maps the 759 case files, but not `census.json`, `published-qualification.json` or `FILES.json` itself. `published-qualification.json` is copied without an inventory check (`census_extract.py:140`). Its bytes equal the round-7 published `076e7cc7...`, which I checked out of band.
  - Fix, docstring: "FILES.json maps every case file written to the packet files it comes from and their SHA256, each checked against the packet's FILES inventory; census.json is new and published-qualification.json is copied."
  - Fix, README: "`FILES.json` maps every case file it writes to the packet files it comes from."
- **RS-2** `review-evidence/artysplit-r1/author-r8/receipts/INDEX.md:5` says "Prepared locally; nothing has been posted or pushed." The packet is now published. Fix: delete the sentence.
- No new source-comment instance of a lane label, review round, reviewer ID or comment ID is in the delta's added lines. The delta removes the two that R928-2-RS1 named.

### SUGGESTION

- **SG-1** `census_extract.py:120` self-regrades with `limit=PART_LIMIT`. Since `read_parts` refuses `len >= limit`, a part of exactly 14,000,000 bytes is refused there, while `receipt_regrade.py:192` (`part_limit + 1`) accepts it. The behaviour is fail-closed, but the two checks disagree. Use `PART_LIMIT + 1` in the extractor.
- **SG-2** `census_extract.py:63-71`. If one line exceeds `PART_LIMIT`, `rfind` returns -1, `end` becomes 0 and `start` resets to 0, so the loop writes parts forever. Refuse such a line explicitly.
- **SG-3** (R927-2 SG-2, retained and widened; the author's open risk) There are no planted-control self-tests for `census_extract.py` or for the regrader's stated limit. Candidates: an inventory hash mismatch, a part at and above the limit, a dropped read-label line, and a missing `part_limit`.
- **SG-4** Bind `published-qualification.json` in `FILES.json`, checked against the packet inventory. The cross-case step compares against it (with RS-1).
- **SG-5** The round-6 reference checkpoint and bitstream (`6c82a595...`, `b5068ecb...`) appear in no earlier public record. If a round-6 record exists, link it. The comparison stands as is, because round 6 to round 7 changed only `ctrl_loop.h`.
- **SG-6** This one is outside the delta, for a new issue. `docs/integration/QSPI_FLASHBOOT.md:85` ("Both boards carry ... the `N25Q128A13`") and `configs/endstation_arty_current.yaml:113` ("N25Q128 QSPI") disagree with `sw/litex/milan_soc.py`, which drives `S25FL128S` on the Arty and is what the split YAML now says.
- **Retained, optional:**
  - R927-2 SG-1 (the regrader's timing tie-break), SG-4 (step-2 build record) and SG-5 (out-of-tree derivation recipes).
  - SG-7, which is R927-1 SG1, SG3 and SG4.

## Prior findings at this head

| Prior finding | Disposition | Cause-level evidence |
|---|---|---|
| R927-2 F1 MINOR (#969 debt owner does not cover the Arty) | **CLOSED** | #1022's acceptance names `arty-1x1` and is blocked by #977. Section 15 cites it (`SPLIT_CONTROL_MEMORY.md:3520`). The control derivation is published and reproduces byte for byte |
| R927-2 F2 MINOR (README cites the superseded qualification) | **CLOSED** | `README.md:208-211`. The hash, 147 groups and model equal to the head's `arty_grade.py` |
| R928-1-F1 / R928-2-F1 MINOR (census not public; paired identity) | **Identity half CLOSED; regrade half RETAINED as F1** | Paired hashes from each step's own files; the stimuli cross-check against the extract; `flash: null` explained by `build.py:906-921`. The published extract does not regrade (F1) |
| R928-2-F2 MINOR (routed LUT comparison lacks routed evidence) | **CLOSED** | Post-route reports for both checkpoints with bound hashes; LUT delta 0 |
| R927-2 RS-A, RS-B, RS-C, RS-D | **CLOSED** | `CHANGELOG.md:334`; live PR body lines 65, 76 and 106 |
| R927-1 RS1, RS3, RS4, RS5, RS6 | **CLOSED** | `endstation_arty_split.yaml:113,256`; `ENDSTATION_BUILDER.md:22`; `BUILDING.md:358,361`; service `README.md:206`; `CLOCK_DOMAINS.md:382`; PR body line 65 |
| R928-2-RS1 (lane labels in `ctrl_mutant_fixtures.py`) | **CLOSED** | `ctrl_mutant_fixtures.py:7,28`. Comment-only; AST and values identical. NFR-SCOUT-08 (`docs/reference/FR_NFR.md:358`) is the ingress tagged-frame clause |
| R927-2 SG-3, SG-6; R928-2-SG1; R927-2 SG-8 | **Adopted / moot** | The row choice is stated. The ROM headroom line checks. `git diff --check 854bd723 011aaa6f` exits 0. The labels are removed |
| R927-2 SG-1, SG-2, SG-4, SG-5, SG-7 | Retained as optional | See SUGGESTION |

## Lens results at this head

```text
[R927] MINOR Conformance — review-evidence/artysplit-r1/author-r8/receipts/census-extract (7ae7427b) — F1: published extract does not regrade; the row's 147-case qualification and #969 exclusion are not publicly reproducible
[R927] PASS RTL — git diff --name-only 4adfa9dc..011aaa6f (no hdl/, sw/litex/, firmware or gitlink path); route-utilization/r7,r6-route-utilization.rpt (Physopt postRoute, 33015/40369/13791/78, delta 0); receipts/builder-split-identity.txt — no RTL or image input changed; the routed area comparison holds against the owner's ~50-LUT band
[R927] PASS Robustness — tb/verilator/ctrl_service_budget/receipt_regrade.py:33-47,191-192 and census_extract.py:47-124 at the head — limit capped at 15 MB, parts refused at or over the stated limit, hash and inventory checks fail closed, the regrade identity guards the line filter; SG-1/SG-2 are fail-closed or unreachable edges; #1022 now bounds the owed SRP cost (R927-2 F1's Robustness half)
[R927] MINOR Tests — receipts/percase-public.summary, probe-rebound-regrade.log, receipts/gates/builder-split.log (0 bytes) — F1 and F2
[R927] MINOR Docs — PR body "Reproduce and inspect" and Definition of done, author-r8/receipts/INDEX.md — F1 and F2; RS-1 and RS-2 are residue only
```

Gates I ran at the head all exit 0:
- `docs_check`, `check_doc_style`, `check_doc_paths`, `check_gptp_docs`, `docs_inventory --check`, `check_py_idiom` (covers the new extractor), `check_cpp_idiom`.
- `check_em_dash --base 4adfa9dc`: 0 findings over 22 added lines.
- `gen_toc --check` and `--verify-anchors`.
- `git diff --check` against both `4adfa9dc` and `854bd723`.
- `--selftest` of `rows_tiers`, `load_grade`, `egress_ledger`, `record_classes`, `arty_grade` and `kept_grade`.

The logs are in `receipts/gates/`. The em-dash and TOC gates ran with the pinned renderer in a private scratch environment.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #878 body and rulings 7097474930 and 7153532537; #1022; #977; section 15; published extract; control derivation; qualification `076e7cc7` | R927-3 (not covering) | 011aaa6f080321e0a89f915720ebb3ee14807a16 |
| RTL | CLEAN | delta path list; post-route reports r7/r6; checkpoint and bitstream identities; builder outputs at base and head | R927-3 | 011aaa6f080321e0a89f915720ebb3ee14807a16 |
| Robustness | CLEAN | `receipt_regrade.py` limit and integrity paths; `census_extract.py`; #1022 acceptance for the owed SRP records | R927-3 | 011aaa6f080321e0a89f915720ebb3ee14807a16 |
| Tests | UNCLEAN (F1, F2) | per-case and full regrade of the public extract; rebound probe; control probe; gate logs; empty builder receipt | R927-3 (not covering) | 011aaa6f080321e0a89f915720ebb3ee14807a16 |
| Docs | UNCLEAN (F1, F2) | PR body (live); author-r8 INDEX, REVIEW-READY and HANDOFF; README, section 15, BUILDING, ENDSTATION_BUILDER, CLOCK_DOMAINS, CHANGELOG and YAML comments | R927-3 (not covering) | 011aaa6f080321e0a89f915720ebb3ee14807a16 |

## Real limits

- The pre-publication extract bytes are not public. So I could not show which bytes were rewritten, or run the cross-case step and the control on the extract the author regraded. F1 is shown from the published bytes and the publisher's own manifest.
- The paired executable, ELF and checkpoint hashes are author-computed. The executables and checkpoints are not published, so I checked consistency, not bytes. The routed utilization is the author's Vivado run, which I did not rerun.
- The control derivation's first step (`census.py` over the raw round-7 traces) needs unpublished traces. I reproduced the merge and derive steps only.
- No manager source bank ran at this head, and none is claimed. Source execution evidence here is the author's receipts plus the reviewer runs listed above.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- At query time, the head had 0 hosted check runs and a commit status of `pending`. No hosted job executed at this exact head, and I accepted none.

## Pending manager duties

- Republish the census extract so its bytes match `FILES.tsv` (F1). The publication path's length-preserving rewrite of the 27 files is the cause.
- Run the separate integration round (merge of current `dev-soft-core`, live `e275d7950ef3385753e6a15d2e191ba855b171ed`) as its own delta, then the current-dev merge-candidate validation (builder and native banks).
- Hosted and local-replica acceptance at the final head; the residue checklist (RS-1, RS-2); maintainer merge authorization and post-merge containment.

## Reproduction (this packet)

- The evidence was fetched read-only at `7ae7427b` into a disposable scratch tree.
- `python3 -I scripts/verify_inventory.py <author-r8/receipts>` checks the packet inventory. `python3 -I scripts/publication_delta.py <author-r8/receipts> <artysplit-r1/MANIFEST.json>` compares it with the publisher's manifest.
- `scripts/percase_regrade.sh <head>/tb/verilator/ctrl_service_budget/receipt_regrade.py <census-extract> <out> 12` regrades every case.
- `python3 -I scripts/rebind_probe.py <census-extract> <copy> [none/srp-bound]`, then `receipt_regrade.py <copy>`, re-binds the hashes and regrades.
- `scripts/grade_diff_probe.py <head-tools> <copy>/census/valid-destinations/srp-talker/manifest.json` shows the one differing leaf.
- `scripts/extract_vs_r7_inventory.py` shows that all 759 `FILES.json` entries name sources listed in round 7's published inventory (22,866 files).
- The clone was restored: tracked index equals the HEAD tree (2001 entries, modes and blobs), the worktree is clean, the gitlinks are unchanged, and the interpreter caches this review created were removed (`receipts/clone-restore.txt`).

R927-3 FINISHED

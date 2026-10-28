[R725] NEGATIVE - exact head f87da064d7d03063d8eb0b95a6559463a1bd2a3f

Round R725-2, internal independent review of PR #802 (issues #799 and #790). This is a delta review of `ca39dc1b..f87da064`, one commit answering F1, R1 and R2 of R725-1 and R726-1. The source base is `97aab1d0`, head tree `d99488e452f602bc1343dc045341593395aa3363`.

The verdict is NEGATIVE on one new MINOR finding under `Docs` (F2). The delta's own census figures are correct. Nothing outside the two named files changed. The generator check is clean.

## Verdict summary

- **F1 (prior MINOR, Docs): resolved.** The figures at `docs/design/MAILBOX_SPLIT.md:990-993` and in the `:1102` row now equal the census at this head.
- **F2 (new MINOR, Docs): open.** The edited sentence still ends with a claim that the old text census found the same reads. That census was retired with 39 reads; this head has 41.
- **R1 (prior RESIDUE): resolved.**
- **R2 (prior RESIDUE): resolved.**
- **S1 (prior SUGGESTION): retained.** It is optional and the delta does not touch it.
- **S2 (new SUGGESTION): optional.** Reflow one short comment line.

## What the delta is

`git diff --name-status ca39dc1b f87da064` lists exactly two files (`receipts/delta.diff`):

- `docs/design/MAILBOX_SPLIT.md`: 4 lines.
  - `:990-993`: 25/39 becomes 26/41, and 10/14/15 becomes 11/14/16.
  - `:1102`: "the 39 reads of the 25 class-D nets" becomes "the 41 reads of the 26 class-D nets".
- `sw/mailbox/mailbox.yaml:63`: `# Minor 3 (#799, the ruling on its STOP, comment 6460917634; #665 decision` becomes `# Minor 3 (#799; #665 decision`.

Nothing else changed:

- No gitlink changed: all six gitlinks are identical to the parent (`receipts/restore_check.txt`).
- No RTL, test, script or generated artifact is in the delta.
- The commit's single parent is `ca39dc1b`.

## Checks run at this head

All runs used the clone at the exact head. The tools were sv2v v0.0.12 and Yosys 0.66, the rtl-fast pins:

- sv2v binary sha256 `b29952bc...`. It was extracted from a zip whose sha256 `ff8c9eea5bc0...` equals the pin in `.github/workflows/rtl-fast.yml:398`.
- The Yosys version string is `0.66`, which equals `YOSYS_VERSION`.

`scripts/delta_checks.sh` reproduces every run.

| Check | Command | Result | Receipt |
|---|---|---|---|
| census check | `python3 -I sw/mailbox/publication_census.py --check --jobs 6` | rc 0. `6 shape(s), checks: 246, failures: 0`; `26 class-D net(s) ..., 4 unread; 41 read(s) of 22 class-D net(s) in each shape; RESULT: PASS` | `receipts/census_check.log`, `.rc` |
| census list | `... --list` | rc 0. 26 population lines (4 unread) and 41 read lines; all six shapes 41 reads, 4 unread | `receipts/census_list.log`, `.rc` |
| reads by kind | parse of the list (in the script) | `{'field': 11, 'processor': 16, 'status': 14} 41`, which equals the page's 11 / 14 / 16 | `receipts/kind_counts.txt` |
| rules and plants on the page (`:996`, `:1001`, `:1102`) | static count of `census_rules.RULES`, `census_plants.PLANTS` | `rules 31 plants 116`. 116 + 2 table plants = 118 plants, as the page says; + 2 controls = 120 arms, as the author's self-test log says (`0 of 120 arm(s) failed`, `0 of 31 rule(s) no arm proves`) | `receipts/rule_plant_counts.txt` |
| generator | `python3 -I sw/mailbox/gen_mailbox.py --check` | rc 0, `gen_mailbox: 0 finding(s)`. The yaml comment edit reaches no generated output | `receipts/gen_mailbox_check.log`, `.rc` |
| doc style | `scripts/check_doc_style.py` | rc 0, OK (23 current documents) | `receipts/doc_style.*` |
| doc paths | `scripts/check_doc_paths.py` | rc 0, 1068 cited paths resolve | `receipts/doc_paths.*` |
| hygiene | `scripts/check_hygiene.py --check` | rc 0, PASS | `receipts/hygiene.*` |
| doc map | `docs/DOC_MAP.gen.py --check` | rc 0, OK | `receipts/doc_map.*` |
| TODO ownership | `scripts/check_todo_ownership.py` | rc 0, OK | `receipts/todo_owner.*` |
| em dash | `scripts/check_em_dash.py --base ca39dc1b`, with the pinned Markdown renderer's Python | rc 0, `0 finding(s) over 4 added line(s)` | `receipts/em_dash.*` |

**Evidence packet spot-check** (`review-evidence/799-r1` at `0829b8ae`). Four files were fetched from the published tree. Each one's sha256 equals its `published_sha256` in `MANIFEST.json` (`receipts/evidence_spotcheck.txt`):

- `REVIEW-READY.md`
- `docs-ca39dc1b/all.rc`
- `pre-commit-wt/census-check-wt.log`
- `pre-commit-wt/census-selftest-wt.log`

The author's census check log reports the same 26 / 4 / 41 as my run.

**Hosted checks at the exact head, snapshot at review time** (`receipts/hosted_checks_f87da064.tsv`): 43 check runs. 11 completed with success, 1 was skipped, 18 were in progress and 13 queued. `publication-census` was in progress. `docs-gates-2` and `docs-check-no-git` succeeded. This is a snapshot only: hosted and act acceptance belong to the manager. No manager source bank runs at this head, and none is claimed.

## Findings

### F2 - MINOR - Docs - `docs/design/MAILBOX_SPLIT.md:993` - the edited census sentence still says the old text census counted the same reads

- **Authority/evidence:**
  - The sentence the delta rewrote now reads: "At this head every shape has the same 26 population nets and the same 41 reads ... Of the 41 reads, 11 are on the wire ..., 14 are CSR status, and 16 are the answer face: the same reads and kinds the text census counted before."
  - That clause was written by `0058de8408` (2026-10-10), when the netlist census replaced the text census. The page then said 39 reads (10 / 14 / 15).
  - The text census no longer exists at this head. The only mention of it in a source file is `sw/mailbox/census_plants.py:440`, which describes the forms it refused.
  - The two reads that make 39 into 41 come from this PR:
    - `("pp_cd_src_stream_id_w", "tx_sid_w")`, a field read for `SRC_SID_LO.SID`;
    - `("pp_cd_src_stream_id_w", "gsi_osid_w")`, an answer-face read.
  - Both rows were added to `sw/mailbox/publication_census.py` in `8b76de6908`. `src_stream_id_o` is absent from `CLASS_D_PORTS` at `97aab1d0`.
  - So the text census never counted 41 reads or 11 / 16. The clause states a figure equality that is false at this head.
  - AGENTS.md section 6, `Docs`: "Changed contracts are reflected in authoritative docs." This is the same paragraph and the same figures F1 required corrected.
  - This is a claim about figures, a cross-check between two censuses. So it is not RESIDUE.
- **Impact:** the authoritative page presents the new 41-read census as confirmed by a census that never saw the two `src_stream_id_o` reads. A reader auditing the split placement would take the new `SRC_SID_LO` wire read as independently cross-checked, and it was not.
- **Required outcome:** `:993` makes no claim that the text census counted the head's 41 reads or the 11 / 16 split. Either of these is enough:
  - drop the clause, ending the sentence at "16 are the answer face.";
  - or keep the comparison scoped to the base. For example: "16 are the answer face. Before the text census was retired it counted 39 of them, with the same kinds; the other two are the reads of `src_stream_id_o` that contract 2.3 adds, one on the wire and one on the answer face."
- **Verification:**
  - Read `:990-994` against `python3 sw/mailbox/publication_census.py --check` and `--list` at the new head.
  - If a comparison is kept, it must name only the 39 base reads, and the two `src_stream_id_o` rows in `--list` must be the only reads that differ from the base.
  - `scripts/check_doc_style.py` and `scripts/check_em_dash.py` stay clean.

### S2 - SUGGESTION - Docs - `sw/mailbox/mailbox.yaml:63-64` - the R1 fix left a short line

- Line 63 now reads `# Minor 3 (#799; #665 decision`, and line 64 starts with `# 2 (a)): ...`. That splits "decision 2 (a)" across lines although line 63 has room for it.
- Optional: reflow to `# Minor 3 (#799; #665 decision 2 (a)): a source entry per talker stream in the` and rewrap the rest of the paragraph.
- Comment only. The generator check is unaffected either way.

## Prior public findings, resolved or retained at this head

| Prior finding | Status at f87da064 | Evidence |
|---|---|---|
| F1 MINOR Docs (R725-1, R726-1): census counts at `MAILBOX_SPLIT.md:990-992` and `:1102` stale | **Resolved** | `:990-993` and `:1102` state 26 nets, 41 reads, 11 / 14 / 16 and 4 unread. That equals `receipts/census_check.log` and `receipts/kind_counts.txt`. The trailing clause of the same sentence is newly reported as F2. |
| F1's out-of-scope note (R725-1): "116 defects, plants two more" and "118 plants" stale | **Not reproduced, not counted** | `PLANTS` holds 116 and the self-test adds 2 table plants, so 118 plants. With 2 controls that is the 120 arms the self-test log reports. The page is consistent with the code. |
| R1 RESIDUE: `sw/mailbox/mailbox.yaml:63` new comment ID | **Resolved** | The exact prescribed fix was applied. `git grep 6460917634` finds the ID in no source comment, only in docs pages and in the `measured` data strings of `syn/ooc/pp_resource_baseline.json`, which are outside the comment rule. `gen_mailbox.py --check` is clean. One cosmetic leftover is S2. |
| R2 RESIDUE: PR body `Relates to #790` | **Resolved** | The PR body reads `Closes #790`, followed by `Not "Closes" for #799: ...`. `closingIssuesReferences` is `[790]` (`gh pr view 802 --json closingIssuesReferences`). |
| S1 SUGGESTION Tests: sidmove8 named uid equals derived uid | **Retained, optional** | `tb/verilator/milan_dp/sim_sid_move.cpp` and the `Makefile` are not in the delta. |

## Comment-rule scan

- **The reviewed delta:** no comment ID, lane label, review round or reviewer ID was added to a source file. The delta removes one.
- **The whole PR diff** (`97aab1d0..f87da064`, non-Markdown): one comment ID, `sw/litex/milan_soc.py:2656-2657` `comment 6088423771`. It is a re-wrap of an existing instance, tracked by #746, so it is not counted. The `measured` strings in `syn/ooc/pp_resource_baseline.json` carry an issue-comment URL, but they are record data, not comments, and are outside this delta.

## Lenses applied to the delta

| Lens | Result | What was checked at f87da064 |
|---|---|---|
| Conformance | PASS | `sw/mailbox/mailbox.yaml:63` changes only a comment. The contract's fields, versions and layout are unchanged. `gen_mailbox.py --check` is clean (0 findings), so the generated SV, C and pages still equal the contract. No requirement, clause or field claim changed. The rest keeps the R725-1 and R726-1 Conformance verdicts from `ca39dc1b`, because the delta touches nothing they depend on. |
| RTL | PASS | The delta contains no HDL file and no gitlink change (`receipts/delta.diff`, `receipts/restore_check.txt`). The census elaborated the head's datapath in all six shapes, with 0 failures and 41 reads in every shape (`receipts/census_check.log`). The prior RTL verdicts at `ca39dc1b` still hold. |
| Robustness | PASS | No behaviour changed. The six-shape census agrees in every shape: population, unread nets and cone-end classes (`receipts/census_list.log`, the per-shape lines). The prior Robustness verdicts hold. |
| Tests | PASS | No test, gate or self-test source is in the delta. The page's test figures (31 rules, 116 + 2 plants, 120 arms) equal `census_rules.py`, `census_plants.py` and the author's self-test log, whose hash matches the manifest. The delta-relevant docs gates pass at this head. The prior Tests verdicts hold; S1 is optional. |
| Docs | FINDING (F2 MINOR) | `docs/design/MAILBOX_SPLIT.md:990-993`, `:1102`. The PR body is resolved (R2). `sw/mailbox/mailbox.yaml:63` is resolved (R1), with S2 optional. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sw/mailbox/mailbox.yaml` delta; `gen_mailbox.py --check` (0 findings); the census rows' fields; prior coverage of the unchanged scope by R725-1 and R726-1 | R725-2 (delta); R725-1 and R726-1 for scope the delta leaves untouched | `f87da064d7d03063d8eb0b95a6559463a1bd2a3f` (prior at ancestor `ca39dc1b`, untouched since) |
| RTL | CLEAN | delta file list (no HDL, gitlinks unchanged); six-shape census elaboration at head | R725-2; R725-1 and R726-1 | `f87da064d7d03063d8eb0b95a6559463a1bd2a3f` (prior at `ca39dc1b`, untouched since) |
| Robustness | CLEAN | six-shape census agreement at head; delta changes no behaviour | R725-2; R725-1 and R726-1 | `f87da064d7d03063d8eb0b95a6559463a1bd2a3f` (prior at `ca39dc1b`, untouched since) |
| Tests | CLEAN | `census_rules.py` / `census_plants.py` counts; author self-test and check logs (hash-verified); docs gates at head; S1 optional | R725-2; R725-1 and R726-1 | `f87da064d7d03063d8eb0b95a6559463a1bd2a3f` (prior at `ca39dc1b`, untouched since) |
| Docs | UNCLEAN | `docs/design/MAILBOX_SPLIT.md:990-993`, `:1102`; PR body; `mailbox.yaml:63`; docs gates | R725-2 | `f87da064d7d03063d8eb0b95a6559463a1bd2a3f`; F2 open |

## Real limits

- I ran no simulation, Verilator, Yosys portability, firmware, builder or Vivado bank at this head. The delta changes no input any of them reads.
- I did not run the census self-test at this head. Its figures are taken from the author's hash-verified log at the census source, which the delta does not change.
- I did not run the census at `97aab1d0`. The base figure of 39 reads comes from the page's text at `0058de8408` and `97aab1d0`, and from R725-1's published base receipt.
- The hosted checks at the exact head were still running when I took the snapshot. I make no hosted or act acceptance claim.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The final current-dev merge candidate (source base `97aab1d0`, live dev `5fcec84b1aa72c43048eff28bb63a982add830dd`) was not built or validated here.
- The evidence packet was spot-checked on 4 of its 581 manifest entries, not verified in full.

## Pending manager duties

- Carry F2 to the author. A re-review at the fixing head is needed to bank `Docs`.
- Build and validate the current-dev merge candidate (builder and native banks) and link the receipts on the PR.
- Own hosted and act acceptance at the final head.
- S1 and S2 are optional. There is no RESIDUE item from this round.

## Restoration

After all runs the clone is unchanged (`receipts/restore_check.txt`):

- `HEAD` is `f87da064d7d03063d8eb0b95a6559463a1bd2a3f`.
- `git write-tree` gives `d99488e452f602bc1343dc045341593395aa3363`, which equals the head tree.
- The worktree and the index are both clean against `HEAD`, and porcelain status is empty.
- The sha256 of the two delta files equals that of their head blobs.
- All six gitlinks are unchanged: `external` efeb541a, `gptp-processor` 55680bff, `protocol-processor` f65c8ff7, `third_party/lwSRP` 08ee86e8, `third_party/tsn-c-stack` 70936b77, `third_party/verilog-axis` 48ff7a7e.

R725-2 FINISHED

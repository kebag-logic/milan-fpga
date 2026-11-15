# HANDOFF round 4 — lane 897 (A776): GET_AS_PATH synced onto #902's round-13 review head

Status: **STOP** (2026-11-15 08:02 CET), posted once on #897 (issuecomment-6890794725, `STOP-COMMENT.md`). The composed platform image at 8x8/2if is 168 B past its 60.0 ledger entry, and `plat_ledger.py` refuses it. Every other image is within its cap and the 1x1/1if flip check passes. The full gate pass waits for the ruling.
Round 3: closed at `f098f893` (REVIEW READY #897 issuecomment-6875785531; R833-3 NEGATIVE on F1, an evidence-publication gap, then R833-4 POSITIVE, PR #898 issuecomment-6877202724).
Merged: `origin/894-tiers` at `234bc149ff888eb96659ecaaa5ce6e4fb27319d4` (#902 round 13, REVIEW READY #894 issuecomment-6890460677; rulings #894 issuecomment-6883864236, 6886633874, 6888782796). `dev-soft-core` still `cec88385`.
Head: `b58a54300726961745c4d39fe686b8c885094549` (the sync merge). Nothing pushed; the manager pushes.

## 1. Sync

- Start: HEAD `f098f893`, tree clean. `git fetch origin`: `894-tiers` `234bc149` (25 commits past `7398ec0a`, the merge base), `dev-soft-core` `cec88385`.
- `git merge --no-ff --no-commit 234bc149`, then one merge commit `b58a5430` ("Merge 894-tiers 234bc149 (#902 round 13, not merged) into the split's GET_AS_PATH lane, each conflict kept from both sides"), parents `f098f893` and `234bc149`.

| File | How | Resolution |
|---|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md`, section 13 before "What is left" | conflict: both sides added subsections | #902's four (the one-row edit, SET_CONFIGURATION's record, the SRP drain's record cost, the final pass's restatements), then this branch's "GET_AS_PATH through the face" |
| `sw/firmware/ctrl/test/aecp_mutants.py`, the `DEFECTS` join (`:873-874`) | conflict: both appended rows | `aecp_map_mutants` + `aecp_face_mutants` rows (this branch) on one continued line, then `aecp_configuration_mutants` rows (#902); 979 lines, within 1,000 |
| `sw/firmware/ctrl/test/test_aecp.cpp`, `struct Far` (`:3640-3656`) | conflict: both edited the GSI model's `answer()` | one `answer()`: it records every GSI request's selector (#902's `selectors`), then serves kind 2 from `path()` (this branch), else `word()` |
| `sw/firmware/ctrl/test/test_aecp.cpp`, after `Face.StreamAvbAndFormatAreTheDatapaths...` | conflict: both appended tests | this branch's GET_AS_PATH tests (closed by their own brace), then #902's `TheRunningCheckReadsOneWindowWordAStream` and `OnlyAMovedConfigurationIndexWritesTheStreamEntries` |
| `aecp_face.c`, `aecp_face.h`, `MAILBOX_SPLIT.md`, the AECP README, the harness README | merged, no conflict | both sides carried exactly |

Check (`merge_sides.py 7398ec0a f098f893 234bc149 b58a5430`, `receipts/sync/merge_sides-b58a5430.txt`): every file of both sides carries that side's own diff exactly, except the two code files. There the only lines not carried verbatim are the `DEFECTS` join line and the model's `answer()` line, which both sides edited (combined as above). The merge needed no design decision.

## 2. GET_AS_PATH against #902's restatements and record classes

Not reached: the ROM ledger failed first (section 3), and every cost figure depends on the composed images, which a ruling may change.

- #902's restatements are noted: the AECP timer slot 70 us, a LINK 155 us, a build of one 735 us, a TICK 55 us.
- So are `record_classes.py`'s classes (ordinary `record.aecp`, paced, long). A GET_AS_PATH command is an "other" record held to `record.aecp`, and no harness group sends one.
- So its record must be measured in a scratch `answering-ports` arm once the images are settled. The plan: send the `aecp` group's GET_AVB_INFO probe as GET_AS_PATH, with `path` reading nine words to the contract's bound and answering eight entries.
- #902's class lines are at their edge: the paced class 300 of 300 us, the largest legal notice 365 of 365. So `record_classes.py` should hold the composed image's records over the full one-interface legs, not only GET_AS_PATH's.

## 3. ROM ledger (the STOP)

`plat_ledger.py --self-test` and `fixtures3.sh`, each on a clean clone, at `234bc149` and `b58a5430` (`receipts/rom/`):

| Image, point | `234bc149` rom B | `b58a5430` rom B | Delta | RAMB36 | Limit | Verdict |
|---|---:|---:|---:|---|---:|---|
| fixture 1x1/1if | 111,024 | 111,344 | +320 | 41.0 | 56 | holds |
| fixture 1x1/2if | 112,312 | 112,632 | +320 | 41.5 | 56 | holds, 8 B before its next granule |
| fixture 8x8/1if | 124,528 | 124,848 | +320 | 54.0 | 56 | holds |
| fixture 8x8/2if | 125,792 | 126,112 | +320 | 59.0 | 59.0 entry | holds, 864 B before its next granule |
| platform 1x1/1if | 116,088 | 116,392 | +304 | 42.5 | 56 | holds |
| platform 1x1/2if | 117,392 | 117,704 | +312 | 43.5 | 56 | holds |
| platform 8x8/1if | 129,640 | 129,944 | +304 | 56.0 | 56 | holds, 1,128 B before its next granule |
| platform 8x8/2if | 130,928 | 131,240 | +312 | **60.5** | **60.0 entry** (cap 60.5) | **refused**: "TILES 8x8-if2: 60.5 RAMB36 past the 60 its override ledgers"; plat_ledger 3 of 7 controls, FAIL |

`sram` is unchanged at every point.

Where the 312 B are (`receipts/rom/b58a5430/objects-8x8-if2.txt`):
- `aecp_face.o` 3,396 -> 3,736 B (+340). `path()` is 280 B; `gsi()` is its own 136 B function.
- `ctrl_plat.o` 24,062 -> 24,042 B (-20, the removed stub).

The scratch cut (`receipts/rom/scratch-cut/`, `cl-cut.diff`, never committed): `path()` reads the same words in the same order through one `gsi()` call site. The platform's 8x8/2if image is then 131,224 B, 16 B less and still 60.5. So no cut in this branch's code recovers 168 B.

`plat_ledger.py` is a lane gate that no hosted job runs (`ctrl_configs.py:179`). The entry (`sw/litex/ctrl_memory.py:262-267`) reads "60.0, capped at 60.5, by the owner's decision of 2026-11-12 for the flip". Raising an entry within its cap took a ruling before (the size fixture's 58.5, #665 issuecomment-6831583372).

## 4. Gates at the composed head

Run so far at `b58a5430` (`receipts/early/`):
- `flip_grade.py --check --point 1x1/1if`: rc 0, RESULT PASS, with #902's figures (R4 13.10, R4L 188.48, ACMP 28.95, ADP 27.30, MAAP 27.42, first 14.66, R5 74.07, R6 69.86, last 127.21 of 130, tx 33.38, txL 48.43 of 49).
- `load_grade.py --check`: rc 0 (0.516, 0.512).
- `check_py_idiom.py`, `check_cpp_idiom.py` and `docs_check.py`: 0 each.

Not run: the firmware jobs, campaigns, coverage, docs gates, lane gates, harness legs and sweep. They wait for the ruling, which may change the images or the ledger.

## 5. Changes this round (file:line, reason)

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `b58a5430` | the conflicts in section 1 | both sides kept | the sync |

No other commit. Two residue items stay open, because the restatement of section 5's and section 13's GET_AS_PATH figures at the composed head, which fixes both, waits for the ruling:
- R833-3 R1: `SPLIT_CONTROL_MEMORY.md:488` and `:2483` say "at the merge of `894-tiers` `5b264bf2`".
- R833-3 R2: `:2487` should say "the nine answers' two data words each (18 reads)".

R3 (the PR body's reviewer lines) is applied in `PR-BODY.md`.

## 6. New checks (planted mutant, failing words)

None: no behaviour changed. The check that caught it is `plat_ledger.py`'s own link and tiles grading. Its seven planted controls report "3 of 7 as required" at the composed head, because the real 8x8-if2 image already fails their baseline.

## 7. Notes

- STOP posted on #897: issuecomment-6890794725 (2026-11-15, `STOP-COMMENT.md`).
- Scratch at the start: round 3's `r3/` (13 GB), the old `units/` and `tmp/` logs deleted (52 MB left). Now `r4/` holds the clones `cl-base` (`234bc149`), `cl-head` (`b58a5430`) and `cl-cut` (the scratch cut, never committed), and the ROM builds. Round 2's and round 3's shard clones under `$LANES` stay (outside scratch).
- Round 4's scripts: `scripts/r4/` (round 3's, re-pointed; `cut_rom.sh`), copied to the output directory's `scripts/`.
- No unit of this lane is left running. Nothing pushed, no PR edited, no comment edited or deleted.

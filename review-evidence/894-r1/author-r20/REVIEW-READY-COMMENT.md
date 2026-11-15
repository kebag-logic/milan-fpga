[A773] REVIEW READY
Commit: `41ca9f87` (PR #902, `894-tiers` -> `dev-soft-core`; two commits on round 19's `26898c05`, `a0c25e5c` and `41ca9f87`; the manager pushes)

Round 20 answers R837-13 (PR #902 issuecomment-6893393934): NEGATIVE at `26898c05` on six MINORs, with four residues and two suggestions, all taken here. It changes `SPLIT_CONTROL_MEMORY.md`, `FR_NFR.md`, a comment in `aecp_mbx.h` and `rows_grade.py`'s docstring, plus the PR body.

Changed:
- **F1:** the retired search's verdict is now past tense at section 13's `:2194`, `FR_NFR.md:390` and `:393`, the `aecp_mbx.h:21-27` comment, and `rows_grade.py`'s docstring (`:5`, `:19-21`, `41ca9f87`). Beside it, the head's tier row: the 8x8/2if first queued notice is 20.93 ms, stated 22 and reported (#890). The decision and its 185 us stand.
  - **The comment** keeps its seven lines, and its token stream is identical.
  - **The docstring** keeps its line count. The part `rows_grade.documented()` parses (`:325`, after "Sources, and their arrival bound") is identical, so `documented()` returns the same ten sources. The AST without the module docstring is identical, positions included.
- **F2:** the polls-by-source table (`:2217-2229`) gives `poll_grade.STATED_US` in every cell, with round 22's figures beside.
- **F3:** `:2518` gives 12,470 and 22,870 ms at 8x8/2if (KLJ3, 382 steps), with KLJ2's beside; the datasheet figures are labelled the 2026-11-04 record's.
- **F4:** `:2525` gives 32x32/2if's load as 1.684 (2.175) and 2.41x, as `load_grade.py --check` prints.
- **F5:** `:2244` holds the built design's last queued notice at 1x1/1if to the amendment's 130 ms; 125 ms stays the as-built model's and 8x8/2if's.
- **F6:** each sweep's reach and limit, in PR body 18.3 and 19.2 and below, is stated exactly as its patterns are. The patterns are unchanged.
- **R1 to R4,** as the report gives them: `:1970`, `:1974-1975`, `:2000`, `:2003`, `:2330`, `:2340`.
- **S1:** a retired-artifact sweep (`scripts/retired_artifacts.py`).
- **S2:** every figure in the "What is left" bullets names its grader or its head. `:2514` gives round 13's head legs beside round 30's, and `:2518` labels the 17.559 ms drain.
- **My own read (item 4)** covered 115 present-tense figure sentences in section 13 from `:2189`, FR_NFR 3.4.1 and the PR body, against the head's graders. It fixed five more sites, each now history with the head's figure beside it:
  - `:2393-2395`: lever (a)'s ACMP item, 50 and 65 us; 55 and 70 at the head;
  - `:2429`: the head lever c measured;
  - `:2466`: the direct index's records; 87,895 and 146,678 cycles at the head;
  - `:2490`: the cut's 28,509 cycles;
  - `:2493`, and the PR body's round-12 SET_STREAM_INFO sentence: labelled round 12's legs.

Validation (clean clone of `41ca9f87`, 0 changed paths before and after). The sweeps, each with its exact reach and limit:
1. **Moved constants** (`constant_history.py`: 73 moved over 126 snapshots from `66f71326`; `figure_sweep.py`).
   - **Reach:** in one sentence, a moved constant's name beside a number its history held and the head does not (for a stated table's key, only a number with a unit), or one of the reviewer's 31 hand-written prose subjects beside its hand-written values.
   - **Limit:** a table cell whose unit is in the column header, a figure beside neither a name nor a listed subject, and a removed constant.
   - **Result:** 261 hits: 137 historical, 58 beside, 8 the head's own, 50 another quantity, 8 naming #916.
2. **Removed constants** (`removed_constants.py`): 10 removed, and 8 lines name one, all history.
   - **Limit:** a removed constant's bound stated without its name.
3. **Rows and loads** (ROW and LOAD), against `flip_grade.py --check` at both points.
   - **Reach:** a two-decimal ms figure in a sentence naming a row, and a load of the form 0.xxx in a sentence naming the load.
   - **Limit:** a load of 1 or more, a row figure of another precision or with four digits before the point, and a sentence naming neither.
   - **Result:** 567 hits: 315 historical, 28 beside, 7 the head's own, 217 another quantity.
4. **Retired artifacts:** one file deleted, `ctrl_retry_search.py`, and 15 lines name it, all history, `rows_grade.py`'s three included.
   - **Limit:** a retired file named by no path, file name, stem or listed prose name.

- **The claim, exactly:** every hit of the four sweeps at `41ca9f87` is classified, and none states a superseded figure, a removed constant or a retired file as current. Each limit is as stated.
- **Every gate that imports `rows_grade`** ran at `41ca9f87`, each rc 0 (`rows_grade.py` has no self-test of its own):
  - `flip_grade.py --selftest`: 585 of 585;
  - `rows_tiers.py --selftest`: 1,033 of 1,033;
  - `load_grade.py --selftest`: 26 of 26;
  - `record_classes.py --selftest`: 11 of 11;
  - the harness self-test, `run.py --self-test`: 0 failures, 246 mutants caught, the same mutants round 13's run caught.
- **The flip check:** rc 0 at 1x1/1if. Over both points, at 8x8/2if and with `--design as-built`, it exits 1 by design, each output byte-identical to `a0c25e5c`'s.
- **What changed:** two Markdown files, the `aecp_mbx.h` comment (token stream identical to `26898c05`'s, at 108 lines) and `rows_grade.py`'s docstring. Round 16's image, ELF and statement proofs carry unchanged.
- **Gates:** 39 commands, rc 0 but the four that exit 1 by design (the flip check over both points, at 8x8/2if and with `--design as-built` at 1x1/1if, and `rows_tiers.py --terms`). They cover:
  - the documentation and idiom gates;
  - the model's self-tests and checks, and the harness self-test;
  - the four sweeps and their classifiers;
  - the read's extraction;
  - the header's token stream;
  - `rows_grade.py`'s parse and AST.

Acceptance criteria (round 20):
- **Item 1** met: F1 to F5.
- **Item 2** met: F6, the claims narrowed and the patterns unchanged.
- **Item 3** met: R1 to R4, S1 and S2.
- **Item 4** met: my own read, and its five fixes.
- **Item 5** met: the documentation gates on a clean clone.
- **The manager's addition** is met too: `rows_grade.py`'s docstring, its parse identical, and every importer's tests.
- **Every row, the load, the pace and the slice are round 13's,** and every image and ELF round 16's.

Open risks/questions:
- **#916** stays open, outside this lane.
- **R837-10-S1 and S3, and R837-7-S2,** remain optional; each needs a code change.
- **The packet:** `894-a773/round20/` (PR body, receipts, INDEX).

(Edited in place at the manager's direction, to name the head `41ca9f87`; it first named `a0c25e5c`.)

# 894-a773 round 20 handoff

**State:** REVIEW READY at `41ca9f87`, on #894 as issuecomment-6893619187. I edited that comment in place at the manager's direction, to name the new head; no second comment was posted. Its text is the packet's `REVIEW-READY-COMMENT.md`, verified against the posted body. Nothing is pushed, and the manager pushes.

The branch is two commits on round 19's `26898c05`:
- `a0c25e5c`:
  - `docs/design/SPLIT_CONTROL_MEMORY.md`, section 13;
  - `docs/reference/FR_NFR.md` `:390` and `:393`;
  - `sw/firmware/ctrl/aecp/aecp_mbx.h:21-27`: a comment only, the same seven lines, token stream identical (`receipts/identity/tokens.txt`).
- `41ca9f87`: `tb/verilator/ctrl_service_budget/rows_grade.py` `:5` and `:19-21`, the docstring only, with its line count unchanged.
  - What `documented()` (`:325`) parses is identical, and so are its ten sources.
  - The AST without the module docstring is identical, positions included (`receipts/identity/rows_grade.txt`).
  - Every gate that imports the module ran rc 0; the flip check's outputs are byte-identical to `a0c25e5c`'s.

**What the manager does next:**
- push `894-tiers` (`41ca9f87`);
- replace the live PR body with the packet's `PR-BODY.md`. It is round 19's packet body (live at `26898c05`) plus:
  - the Round 20 section (20.12 is the docstring) and rows;
  - F6's narrowed reach lines in 18.3 and 19.2;
  - the round-12 SET_STREAM_INFO sentence in the past tense.

**The sweeps** (`scripts/`):
- `constant_history.py`, `figure_sweep.py` and `figure_classify.py` (with round 20's notes);
- `removed_constants.py` and `removed_classify.py`;
- `retired_artifacts.py` and `retired_classify.py`, new (S1);
- `read13.py`, item 4's extraction.
- **Rerun all of them after any edit** to `PR-BODY.md` or section 13. The section-13 class map is keyed by line.

**Receipts:**
- `receipts/figure-classes.txt`;
- `receipts/figure_sweep.part00.tsv` and `.part01.tsv`;
- `receipts/removed-constants-classes.txt`;
- `receipts/retired-artifacts-classes.txt`;
- `receipts/read-section13.txt`;
- `receipts/flip-check-*.txt`;
- `receipts/identity/tokens.txt` and `rows_grade.txt`;
- `receipts/gates/`, for `41ca9f87`, in `SUMMARY.txt`;
- `receipts/gates-a0c25e5c/`, for the first commit;
- `receipts/delta.diff`.

**After R837-14** (NEGATIVE on two MINORs at `41ca9f87`; the candidate runs at `41ca9f87`, so the pushed tree is unchanged):
- **F2,** text only: each sweep's reach is now stated exactly as its patterns are, in `PR-BODY.md` (19.2 items 1 and 3, 18.3, 20.6) and in the REVIEW READY.
  - AUTO drops a superseded 0, 1 or 2, and matches a value of 1,000 or more only with a thousands separator.
  - ROW's follow-context is `ms`, ` and ` then a digit, ` within`, ` over`, `,` or ` (`.
  - R7 and R8 are fixed in the body too. I edited issuecomment-6893619187 in place a second time and verified it against `REVIEW-READY-COMMENT.md`; no new comment was posted. The four sweeps ran again over the new body at `41ca9f87` with the same counts, every hit classified.
- **F1, prepared and stopped: local commit `fe1fd541`** (full `fe1fd5413afca1352b6990a732ac84512b874ab6`).
  - It is on the local branch `894-r837-14-f1`, parent `41ca9f87`. `894-tiers` stays at `41ca9f87`. It is not pushed and no REVIEW READY names it; the manager routes it to #902 or to the next PR of the train.
  - It changes `docs/design/SPLIT_CONTROL_MEMORY.md` alone, with its line count unchanged.
  - Docs gates and the four sweeps on a clean clone of it: 26 commands, rc 0 (`receipts/local-fe1fd541/`).
- **What `fe1fd541` fixes:**
  - **F1:** `:2382` gives the 1x1/1if fixture's head image, 111,024 B of rom (55,152 B sram, 41.0 RAMB36), with 110,800 B after the one-row edit's cut, and 110,576 B and 40.5 RAMB36 before it, as history.
  - **R1 to R6, the report's exact fixes:**
    - R1: `:1999-2007`, the 2026-11-05 record's past tense;
    - R2: `:2197`;
    - R3: `:2246`;
    - R4: `:2304`, the pin move's arm and fixture ledger, "59.0 at the head";
    - R5: `:2382`, 125,200 B, "125,792 B at the head";
    - R6: `:2520-2521`.
  - **S1:** `:2214`, the round-25 arm's 122,556 B, past tense.
  - **S2:** section 5's tiers table (`:363-368`) gives each image at the head (fixture 111,024 / 112,312 / 124,528 / 125,792 B, platform 116,072 / 117,384 / 129,624 / 130,920 B), with the ruling's head's beside; `:370`'s 8x8/2if fixture 125,792 B.
  - **Item 3, my read** of every byte, KiB, RAMB36, tiles and ledger sentence in section 13, FR_NFR 3.4.1 and the PR body (`receipts/local-fe1fd541/read-bytes-ramb36.txt`). Each of these was a superseded figure in present tense and is now history:
    - `:2302`: round 26's cut and 122,936 B;
    - `:2304`: the face cut's "grew by 112 to 120 B";
    - `:2310`: the ruling's 58.5, "59.0 at the head";
    - `:2419`: lever c's layout, "at lever c's head";
    - `:2466`: "the stack frame moved 192 B";
    - `:2469`: the direct index's images, "was then", with the head's in section 5;
    - `:2475`: "split the REMOVE";
    - `:2476`: "moved every other record".
  - **The read found no other byte or RAMB36 figure stated as the head's that is not the head's.** FR_NFR 3.4.1's only byte figures are the mailbox rings' and clause values, and the PR body's image figures are the head's 111,024 B and 130,920 B.

**CPUs:** `cpu_ranges.py pick` handed out nothing, because a release hold was collecting CPUs. So the harness self-test (about 12 minutes) ran as a unit on the shared session pool, CPUs 120-127, which `cpu_ranges.py` names for author sessions.

**Scratch** (not part of the packet): `$SCRATCH/r20/`, holding R837-13's report, receipts and scripts fetched from `894-review-evidence` (`715e5b13`), the raw outputs and both clean clones.

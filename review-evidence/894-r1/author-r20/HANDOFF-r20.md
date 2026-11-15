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

**CPUs:** `cpu_ranges.py pick` handed out nothing, because a release hold was collecting CPUs. So the harness self-test (about 12 minutes) ran as a unit on the shared session pool, CPUs 120-127, which `cpu_ranges.py` names for author sessions.

**Scratch** (not part of the packet): `$SCRATCH/r20/`, holding R837-13's report, receipts and scripts fetched from `894-review-evidence` (`715e5b13`), the raw outputs and both clean clones.

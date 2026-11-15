# 894-a773 round 15 handoff

**State:** REVIEW READY at `6b759b30` posted on #894 as issuecomment-6891524339 (one comment, the packet's `REVIEW-READY-COMMENT.md`, verified against the posted body). Nothing is pushed, and the manager pushes. The branch `894-tiers` is one commit on round 14's `867faf1e`:
- `6b759b30`: `docs/design/SPLIT_CONTROL_MEMORY.md` and `docs/reference/FR_NFR.md` only (R837-8-F1, R837-8-R2, and R838-9's note on item 5's precondition).

**What the manager does next:**
- push `894-tiers` (`6b759b30`);
- replace the live PR body with the packet's `PR-BODY.md`. It is the live body at `867faf1e` (round 14's packet body), plus:
  - the Round 15 section and rows;
  - the R838-6-F2 row's `:2525`;
  - 14.1 made exact;
  - the status, validation and Definition of Done lines.

**Round 15 items:**
1. **R837-8-F1:** PR body 15.1. The receipt is `receipts/stale-rows-grep.txt`:
   - `scripts/stale_rows.py` lists every hit; `--tokens` gives the tokens, generated from the rows-history table and the load lines.
   - `scripts/stale_rows_classify.py` classifies each hit and exits 1 on any it does not classify.
   - The sweep includes the packet's own `PR-BODY.md`, so it must run again after any edit to that body. Its line numbers are classification keys.
2. **The residues:** R837-8-R1 (= R838-9-R1), R2 and R3 (PR body 15.2).
3. **The proof:** `receipts/delta.diff`, the two Markdown files only, and `receipts/gates/` (29 commands, clean clone of `6b759b30`). Round 14's cost grep also ran again there: `receipts/stale-figures-grep.txt`, from round 14's packet's `scripts/stale_grep.py` and `stale_classify.py`.

**Not taken:** R837-8-S2 (the face contract pointer), as the review allows.

**Scratch** (not part of the packet): `$SCRATCH/r15/`, holding the review files fetched from `894-review-evidence` (`ac442aab`), the raw sweep output and the clean clone.

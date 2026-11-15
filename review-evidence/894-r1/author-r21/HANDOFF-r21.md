# 894-a773 round 21 handoff

**State:** REVIEW READY at `07ed787e` posted on #894 as issuecomment-6897091854 (one comment, the packet's `REVIEW-READY-COMMENT.md`, verified against the posted body); its Commit line gives the full SHA. Nothing is pushed, and the manager pushes.

**The branch:** `894-tiers` is `07ed787e`, one commit on `fe1fd541`, which the manager fast-forwarded and pushed. The commit changes `docs/design/SPLIT_CONTROL_MEMORY.md` alone; no non-Markdown file changed after `41ca9f87`.
- **R837-15-F1:** `:370`, the head's 8x8/2if platform image, 130,920 B with 152 B before the 60.0 granule; 130,328 B and 744 B at the ruling's head.
- **S3:** three more sites in the section-5 paragraphs this PR writes, from the reviewer's `byte_sentences.py` (`receipts/s5-byte-sentences.tsv`):
  - `:335`: the pin move's `ctrl_plat` sizes. The head's are 17,536, 19,008, 18,176 and 20,288 B, measured with `nm -S` on the head's platform ELFs, which are byte-identical to round 16's.
  - `:346-347`: round 29's images.
  - `:348`: the round-25 arm's ledger.
- **R3:** `:2006`.

**What the manager does next:**
- push `894-tiers` (`07ed787e`);
- replace the live PR body with the packet's `PR-BODY.md`. It is round 20's packet body (live at `fe1fd541`) plus:
  - the Round 21 section and rows;
  - the head named throughout;
  - the R837-14-F1 row fixed at `fe1fd541`, linking round 20's `receipts/local-fe1fd541/`;
  - R1, R2 and S4.

**Receipts** (`receipts/`):
- `gates/`: 29 commands, clean clone of `07ed787e`;
- the four sweeps' outputs: `figure-classes.txt`, `figure_sweep.part0*.tsv`, `removed-constants-classes.txt`, `retired-artifacts-classes.txt`;
- `s5-byte-sentences.tsv`;
- `delta.diff`.

**Scripts:** round 20's, copied; the section-13 class map is keyed by line, so re-run every sweep after any edit to `PR-BODY.md` or section 13. `byte_sentences.py` is the R837-15 reviewer's, with a provenance line.

**Not taken:** R837-15-S1 and S2, which are base text outside the delta and optional.

**Scratch** (not part of the packet): `$SCRATCH/r21/`, holding R837-15's report and scripts fetched from `894-review-evidence` (`b737958f`), the raw outputs and the clean clone.

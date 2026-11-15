# 894-a773 round 19 handoff

**State:** REVIEW READY at `26898c05` posted on #894 as issuecomment-6893105270 (one comment, the packet's `REVIEW-READY-COMMENT.md`, verified against the posted body). Nothing is pushed, and the manager pushes. `26898c05` is one commit on round 18's `4ae887a1` and touches two files:
- `docs/design/SPLIT_CONTROL_MEMORY.md`: `:1970`, `:2010` to `:2016` and `:2522`;
- `tb/verilator/ctrl_service_budget/README.md`: `:1490`.

**What the manager does next:**
- push `894-tiers` (`26898c05`);
- replace the live PR body with the packet's `PR-BODY.md`. It is round 18's packet body (live at `4ae887a1`) plus:
  - the Round 19 section and rows;
  - R3's and R4's fixes.

**The sweeps** (`scripts/`):
- `constant_history.py` and `figure_sweep.py` are as in round 18.
- `figure_classify.py` is round 18's plus R5's override.
- `removed_constants.py` is the R837-12 reviewer's, with a provenance line.
- `removed_classify.py` is new.
- **Rerun all of them after any edit** to `PR-BODY.md` or section 13. The section-13 class map is keyed by line.

**Receipts:**
- `receipts/constant_history.txt`;
- `receipts/figure_sweep.part00.tsv` and `.part01.tsv` (`figure_sweep.README.txt`);
- `receipts/figure-classes.txt`;
- `receipts/removed_constants.tsv` and `removed-constants-classes.txt`;
- `receipts/flip-check-*.txt`;
- `receipts/gates/`: 27 commands, with the "by construction" grep in `by_construction.log`;
- `receipts/delta.diff`.

**Scratch** (not part of the packet): `$SCRATCH/r19/`, holding R837-12's report, scripts and receipts fetched from `894-review-evidence` (`c4a05b79`), the raw outputs and the clean clone.

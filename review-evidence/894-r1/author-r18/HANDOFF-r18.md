# 894-a773 round 18 handoff

**State:** REVIEW READY at `4ae887a1` posted on #894 as issuecomment-6892759365 (one comment, the packet's `REVIEW-READY-COMMENT.md`, verified against the posted body). Nothing is pushed, and the manager pushes. The branch is two commits on round 17's `478ff78c`, each changing `docs/design/SPLIT_CONTROL_MEMORY.md` alone:
- `6ef3be3b`: R837-11-F1 (`:2204-2207`), F2 (`:2477`), and R1 to R3 (`:2427`, `:2432`, `:2244`);
- `4ae887a1`: the sites found by reading the sweep's hits, `:2284`, `:2287`, `:2379`, `:2476`, `:2477` and `:2520`.

**What the manager does next:**
- push `894-tiers` (`4ae887a1`);
- replace the live PR body with the packet's `PR-BODY.md`. It is round 17's packet body (live at `478ff78c`) plus:
  - the Round 18 section and rows;
  - R4's fix;
  - every completeness claim made exact.

**The sweep** (R837-11-F3):
- `scripts/constant_history.py` is copied unchanged from R837-11's packet.
- `scripts/figure_sweep.py` is adapted from R837-11's: its rules, ROW and LOAD unchanged, plus one AUTO rule per moved constant (`auto_rules`). It takes `constant_history.txt` as a fifth argument.
- `scripts/figure_classify.py` classes every hit by line, by a read region, by this body's section, or by an override. It exits 1 on any hit it does not class.
- **Rerun after any edit** to `PR-BODY.md` or section 13. The section-13 map is keyed by line.
- **Receipts:**
  - `receipts/constant_history.txt`;
  - `receipts/figure_sweep.part00.tsv` and `.part01.tsv`, which `cat` reassembles (`figure_sweep.README.txt`);
  - `receipts/figure-classes.txt`;
  - `receipts/flip-check-1x1.txt` and `flip-check-8x8.txt`;
  - `receipts/gates/` (24 commands);
  - `receipts/delta.diff`.

**Scratch** (not part of the packet): `$SCRATCH/r18/`, holding R837-11's report and scripts fetched from `894-review-evidence` (`667032a0`), the raw outputs and the clean clone.

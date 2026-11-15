# 894-a773 round 17 handoff

**State:** REVIEW READY at `478ff78c` posted on #894 as issuecomment-6892298990 (one comment, the packet's `REVIEW-READY-COMMENT.md`, verified against the posted body). Nothing is pushed, and the manager pushes. `478ff78c` is one commit on round 16's `b6f5c638` and changes `docs/design/SPLIT_CONTROL_MEMORY.md` alone, at `:2004`, `:2260`, `:2357`, `:2377` and `:2442`.

**What the manager does next:**
- push `894-tiers` (`478ff78c`);
- replace the live PR body with the packet's `PR-BODY.md`. It is round 16's packet body (live at `b6f5c638`) plus:
  - the Round 17 section and rows;
  - the corrected 16.2 and 16.3 claims;
  - the status, validation, Known limitations and Definition of Done lines.
- route the `milan_dp` finding to an Issue of its own: `tb/verilator/milan_dp/srptx.hpp:83` has `kJoinCs = 20`, against `CTRL_LOOP_JOIN_CS` 19 (PR body 17.2).

**Receipts:**
- `receipts/statement-sweep.txt`: `scripts/statement_sweep.py` lists the hits, and `scripts/statement_classify.py` classifies each, exiting 1 on any it does not classify.
  - Line and sentence keys, PR body included: run it again after any edit to `PR-BODY.md`.
- The other three sweeps ran again at the head:
  - `receipts/stale-rows-grep.txt`: round 15's sweep, its PR-body keys moved to this body;
  - `receipts/stale-figures-grep.txt`: round 14's;
  - `receipts/comment-sweep.txt`: round 16's.
- `receipts/statements/RC.txt`: round 16's RC lines, with the record-classes line corrected (R837-10-R1).
- `receipts/gates/`: 23 commands.
- `receipts/delta.diff`.

**Scratch** (not part of the packet): `$SCRATCH/r17/`, holding the review report fetched from `894-review-evidence` (`27084bda`), the raw sweeps and the clean clone.

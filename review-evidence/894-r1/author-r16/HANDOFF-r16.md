# 894-a773 round 16 handoff

**State:** REVIEW READY at `b6f5c638` posted on #894 as issuecomment-6891884588 (one comment, the packet's `REVIEW-READY-COMMENT.md`, verified against the posted body). Nothing is pushed, and the manager pushes. The branch `894-tiers` is two commits on round 15's `6b759b30`:
- `eed2e40d`: `aecp_mbx.h:50`, a comment (R837-9-F1);
- `b6f5c638` (R837-9-F2, outcome 1):
  - `ctrl_loop.h:371` at 99u;
  - the controls in `rows_tiers.py:929-935` and `flip_grade.py:174-184`;
  - `SPLIT_CONTROL_MEMORY.md:2004`, `:2351` and `:2521`;
  - the harness README's check description.

**What the manager does next:**
- push `894-tiers` (`b6f5c638`);
- replace the live PR body with the packet's `PR-BODY.md`. It is round 15's packet body (live at `6b759b30`) plus:
  - the Round 16 section and rows;
  - the status, validation and Definition of Done lines;
  - the 8x8/2if status sentence.

**Receipts:**
- `receipts/identity/`: images and harness ELFs against `234bc149`, and token streams.
- `receipts/statements/`: every statement check at both points; `RC.txt` gives each command's rc.
  - Every stated table was compared by re-running round 11's `compare_point.py` with `b6f5c638`'s statements over round 13's extracted costs (`$SCRATCH/r13/an/final`, `final8`).
  - `record_classes.py` ran over round 13's 15 result sets (`$SCRATCH/r13/gates-out/builds`).
  - `run.py --regrade` was not used, since it refuses a build whose firmware sources changed.
- `receipts/comment-sweep.txt`, from `scripts/comment_sweep.py` and `comment_classify.py`, with its control at `6b759b30` beside it.
- `receipts/stale-rows-grep.txt`: round 15's sweep, its PR-body keys moved to this body by line content (`scripts/stale_rows_classify.py`). Run it again after any edit to `PR-BODY.md`.
- `receipts/gates/`: 35 commands. The firmware AECP and loop arms ran as a unit on CPUs 56-63 (picked), since ended.

**Facts worth keeping:**
- `rows_tiers.py` is at its 1,000-line cap. The control change is line-neutral.
- The objects carry no debug or macro sections, so a macro read only by a `_Static_assert` leaves every image identical.
- `flip_grade.py --check` at 8x8/2if exits 1 by design. That is why the two-interface statement survived three rounds; the planted controls now hold it.

**Scratch** (not part of the packet): `$SCRATCH/r16/`, holding the review files from `894-review-evidence` (`af0ea2b6`), the raw sweeps, the statements and the clean clone. Round 12's image clone and round 13's leg clone are left detached at `b6f5c638`.

# 894-a773 round 14 handoff

**State:** REVIEW READY at `867faf1e`, posted on #894 as issuecomment-6891277821 (one comment, the packet's `REVIEW-READY-COMMENT.md`, verified against the posted body). Nothing is pushed, and the manager pushes. The branch `894-tiers` is two commits on round 13's `234bc149`:
- `b25530f6`: section 13, FR_NFR 3.4.1, the SRP README, and the comments at `ctrl_loop.h:321` and `poll_grade.py:70` (R837-7-F1, R837-7-R1, R837-7-S1);
- `867faf1e`: the `edit_rows.py:3` docstring (R838-7-R1).

**What the manager does next:**
- push `894-tiers` (`867faf1e`);
- replace the live PR body with the packet's `PR-BODY.md`. It is the live body (lines 203 and 282 as the manager corrected them) plus round 14. One more fix there: the round-13 finding rows had been split off the table by a blank line, which GitHub renders as text, and they now render in it.

**Round 14 items:**
1. **R837-7-F1:** the sweep (PR body 14.1). The grep receipt is `receipts/stale-figures-grep.txt`: `scripts/stale_grep.py` lists the hits, and `scripts/stale_classify.py` classifies each one, failing on any it does not classify.
2. **R837-7-R1:** the `ctrl_loop.h` comment.
3. **R837-7-S1:** the precondition, in section 13 and `receipts/item5-no-late-completion.md`. LiteX's `xilinx_common.py:58-60` was read at the pinned revision `a1e1c365`, in the product LiteX tree's own checkout.
4. **The proof:**
   - `receipts/identity/`. The images were built by round 13's `scripts/scratch/qall.sh` and `image_sha.sh` (round 13's packet) on round 12's image clone. The harness ELFs were linked by `scripts/harness_fw.py` on round 13's leg clone, with round 13's leg build directories' `build.json` and flash maps.
   - The gates are in `receipts/gates/`, from a clean clone of `867faf1e`.
   - They also ran at `b25530f6` (all rc 0), before R838-7-R1 was taken. Only the final head's logs are kept.
5. **The PR body:** the packet's `PR-BODY.md`.

**Beyond the assignment:**
- **R838-7-R1** (a residue the reviews left on the manager's checklist) was taken, since it is a docstring and round 14 is documentation and comments. Its proof is the AST without the docstring, identical with positions included, and the docstring differing by the one phrase.
- **R837-7-S3** was taken in the packet: `scripts/sanitize.py` and `scripts/index.py` take their host prefixes as arguments, and `index.py` refuses any file carrying one.
- **R837-7-S2** and **R838-8-S1** are not taken; the reasons are in the PR body's rows.

**CPUs:** `cpu_ranges.py` showed all 128 booked for the whole round. The only work was qall's eight 5-second links and 14 harness-firmware links, each head in turn, at `nice 19` and in the foreground. No unit was started.

**Scratch** (not part of the packet): `$SCRATCH/r14/`, holding the raw hash lists, logs, token files and both clean clones. Round 12's image clone and round 13's leg clone are left detached at `867faf1e`.

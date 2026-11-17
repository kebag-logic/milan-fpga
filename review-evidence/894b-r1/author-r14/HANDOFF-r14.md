# HANDOFF — lane 894b (8x8/1if follow-up of #894), round 14, [A781]

Status: REVIEW READY at `e1ecce20` (comment text `REVIEW-READY-COMMENT.md`, posted once on #894 as issuecomment-6946628993 at 12:22 CET, its text the file's). PR text
`PR-BODY.md`, the full body, from the published round 13 body (Closes #930). Nothing pushed; no PR created or edited.
Under the owner's batch rule this is the last delta before #914 freezes.

- Start head: d0a2a160 (round 13, published; archive 48b6c3a2), tree clean, 11:40 CET. No unit of mine running.
- Assignment: the manager's round 14 RESUME. Fix, as commits on d0a2a160 and nothing else:
  1. R843-6-F1 (PR #914 issuecomment-6945680630): restate FR_NFR.md:420 at 2,027 cs, 75 ms and 74.26 ms, and sweep the tree so every remaining 69.84, 2,026, 2026 or 70 ms is explicitly historical.
  2. R843-6-S1: a self-test control and mutant proving `flip --check` calls `tx_held`, with the wiring unchanged.
  3. The wording residues of R843-6 and R844-5 (issuecomment-6945665282). Comments and docs only; the images byte-identical by hash.
  4. PR-BODY.md: drop "Nothing has been pushed", give the base as dev-soft-core, add round 14.

  Gates on a fresh clean clone of the new head: the harness self-test (mutant count up by one), flip `--check` at 1x1/1if and 8x8/1if and its self-test, the docs jobs, the image hashes, and the style and idiom gates for the touched files. No campaigns or legs. One REVIEW READY; round14/.

## Commits (on d0a2a160)

| Commit | What |
|---|---|
| `60389719` | FR_NFR.md:420, R843-6-F1's text. SPLIT_CONTROL_MEMORY.md:2816, R4's exact text, and :2821, which names the composed image (`d1c9023b`'s, historical) beside its `li a3,2026`. `srp_mbx.c:34-35`, R2's exact text on the same two lines. `srp_talker.cpp:53`, R3's exact text, now two lines. |
| `e1ecce20` | `flip_grade.py`: R1's exact comment, plus `CHECK_HELD_CONTROL` and `check_held_control`. The control runs `main` as `--check --point 8x8/1if` does, with the 70 ms plant only in the text `tx_held` reads; it is in `controls()` and `CONTROLS`, 616 controls. `selftest_mutants.py`: `_flip_check_without_tx_held`, which runs `main` with `tx_held` finding nothing for its duration, without `exec` (Rule 12), 260 mutants. The harness README names the control and adds the mutant's row. |

## Evidence (receipts/)

- `sweep-e1ecce20.txt` (`sweep.py`, over the tracked text): 19 hits, each one's scope stated; none gives 69.84, 2,026 or 70 ms as 8x8/1if's current figure. The first attempt, a `git grep -o` with context, ran past its time limit; the script replaced it.
- `gates/check-held-mutant-e1ecce20.txt` (`check_held_mutant.py`): the control refused at the wiring. Under the mutant only `the flip check refuses --check --point 8x8/1if with 8x8/1if's CTRL_LOOP_TX_MS planted at 70 ms` fails, the three earlier controls stay refused, and the control is refused again after.
- `images/img-identity-e1ecce20.txt` (`img_all8.py` against d0a2a160's receipt): all eight identical, 8x8/1if's among them.
- `gates/quick-checks-e1ecce20.txt`: 22 rc 0; 8x8/2if's flip check rc 1 by design; flip self-test 616 of 616; the comment scans over round 14's delta 0 lines.
- `gates/harness-selftest-e1ecce20.txt`: 932 PASS, 260 mutants caught, 0 failures, rc 0, the clone unchanged.
- `gates/verify-docs-yml-e1ecce20.txt`, `gates/workflow/`: 61 steps rc 0, 34 not run with a reason, 0 bad. docs-check-no-git's driver ends in a traceback, the runner's: the job deletes `.git` on purpose and the runner's git status after cannot run, as in round 13. Its steps are rc 0. The one log over 190 KB is excerpted, its raw size and sha256 in `raw-manifest.json`.

## Run history (CET)

- 11:40 resume; R843-6 and R844-5 read whole. The PR's base read: `dev-soft-core`, head d0a2a160.
- 11:4x the edits. The first version of the mutant used `exec` to drop the call from `main`. The Python idiom gate refuses `exec` (Rule 12), and the inner function had no docstring. Both were fixed before the commits; the mutant now wraps `main` instead.
- 11:46 the two commits. 11:47 the gates on clean clones (launchM.py, at most 4 units).
- 11:48 images and quick checks rc 0. 11:5x the mutant's record and the sweep on the quick checks' clean clone.
- 12:01 docs-gates-2 and docs-a rc 0; 12:14 docs-gates-1 and 12:15 docs-gates-0 rc 0; 12:21 the harness self-test rc 0.
- 12:2x the receipts, PR-BODY.md, the comment, the index; the REVIEW READY posted once on #894.

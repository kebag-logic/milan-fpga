# HANDOFF — lane 894b (8x8/1if follow-up of #894), round 13, [A781]

Status: REVIEW READY at `d0a2a160` (comment text `REVIEW-READY-COMMENT.md`, posted once on #894 as issuecomment-6945136249 at 11:15 CET, its text the file's). PR text
`PR-BODY.md`, the full body (Closes #930). Nothing pushed; no PR created or edited. Under the freeze rule this is
#914's last change; the composition lane takes `d0a2a160` on top of `8883d499`.

- Start head: 8883d499 (round 12, archive 88f4b944), tree clean.
- Assignment: two manager RESUMEs.
  - The first: R843-5 (PR #914 issuecomment-6940020752) F1, option (a) only. Hold 8x8/1if's CTRL_LOOP_TX_MS at or over its tx row by every source in the tree, the row derived in the tree, run by `flip_grade.py --check` at 8x8/1if without changing its other grading. Add planted controls refusing 60 and 69 ms by name. ctrl_loop.h, section 13 and the SRP README name the guard. Also the residues R1, R2 and R843-4-R1.
  - The second added R844-4 (PR #914 issuecomment-6940102979). F1 (MAJOR): restate the figure to the row rounded up, 75 ms, derived and not mirrored, with the hold-off 2,027 cs. Add a 74 ms control. Re-measure the affected 8x8/1if legs. Every 1x1/1if and 8x8/2if image must stay byte-identical. Refresh 69.84/70/2026 everywhere. F2 (MINOR): state each figure with its image.
  - Then the harness self-test and mutants, the flip and load gates, the docs jobs on a clean clone, one REVIEW READY, this file and PR-BODY.md. Push nothing; stop my own units by name.
- Host events: the manager stopped the session at 06:5x to add R844-4. The host was shut down at 07:25 and back at 08:00, now with 96 CPUs (session pool 64-95; cpu_ranges books 0-63). Three legs had no rc at the shutdown. They were treated as cut: their output was removed and they were re-run from 08:05. The fourth, the control, had ended rc 0 at 07:24 and was kept.

## Commits (on 8883d499)

| Commit | What |
|---|---|
| `a840c14d` | `rows_grade.ROW_COSTS` gets 8x8/1if (8x8/2if's LINK, `NEAREST`). `rows_grade.point_inputs` and `costs` read polls and notices at each point's shape: 8x8/1if's notices 40, where the header gave 12. `rows_tiers.point_inputs` takes the datapath events at the nearest point, and `LONG_NOTICE_US` covers 8x8/1if. `flip_grade.tx_held` holds 8x8/1if's figure apart from `REPORTED`; `TX_HELD_CONTROLS` add 60, 69 and 74 ms (615 controls). |
| `32a9242f` | `CTRL_LOOP_TX_MS` 75u in the (1, 9, 9) block; the hold-off becomes 2,027 cs there. Comments in `ctrl_loop.h` and `srp_mbx.c`, and the SRP README. |
| `d0a2a160` | Section 13: each figure with its image or derivation, and the re-measurement. MAILBOX_SPLIT: 0.9 ms. FR_NFR 3.4.1: R843-4-R1 in R843-5's wording, plus the head's 8x8/1if image. `load_grade.py`'s header (R843-5-R1). The harness README names `tx_held`. |

## Evidence (receipts/)

- `model/`:
  - `rows-8x8-1if-d0a2a160.txt`: the tree's own derivation. R4 21.39, R5 136.64, R6 132.93, first 18.98, last 387.95, R4L 208.55, ACMP 52.76, ADP 52.64, MAAP 53.91, tx 74.26, txL 159.82; load 0.735, and 1.034 with every command the largest legal one. It equals R844-4's `current-8x8-rows.txt`.
  - `tx-held-controls-d0a2a160.txt`: each control refused by name; the head unplanted has no finding.
  - `flip-selftest-d0a2a160.txt`: 615 of 615.
  - `graders-8883d499-against-d0a2a160.txt`: only the figure, the HELD line, the count and the header move.
- `reviews/`:
  - R844-4's probe at the head: PASS, 20,005.74 ms.
  - R843-5's probe with its plant pointed at the head's 75u: 60 ms refused by name, and 70 ms too. The reviewer's own copy plants over `70u` and refuses to run on this head, whose figure is 75u.
- `images/`:
  - `img-identity-d0a2a160.txt` (`img_r13.py`): the six at 1x1/1if, 1x1/2if and 8x8/2if identical; each 8x8/1if image one instruction apart (`li a3,2026` to `li a3,2027` at 9ef8 and 9ed4), every section's other bytes the same.
  - Its control, 8883d499 against itself, fails at 8x8/1if as it must.
- `harness/legs-32a9242f/`: VDh (`srp-talker-held`), VDt (`srp-talker`), VDl (`srp-talker-loss`) and CTA (the transmit-aged control), on a clean clone of 32a9242f.
  - Each rc 0, no STATED line.
  - `legs-against-46cf2a7d.txt` (`legs_compare.py`): every simulation log byte-identical to round 10's. The one grade value that differs is the stated reclaim limit, 40 us against 35 then.
  - `gate-8x8-1if-valid-destinations.txt`: every measured row within its bound; the only findings are the seven held-egress ledger rows, which these groups do not measure.
- `gates/`: the quick checks, 20 rc 0 and 8x8/2if's flip check rc 1 by design. The harness self-test: 931 PASS, 259 mutants caught, 0 failures. The docs workflow, verified: 61 steps rc 0, 34 not run with a reason, 0 bad. The SRP campaign: 436 caught, 0 escaped. firmware-unit: every step rc 0, coverage 39 files. `workflow/` holds every step's log and rc; the two logs over 190 KB are excerpted, their raw sizes and sha256 in `raw-manifest.json`.

## Run history (CET)

- After 06:00, round 13's first brief. The derivation in the tree showed 8x8/1if's tx row at 74.26 ms, against the 70 ms figure, so "the head passes" could not hold without a firmware change. The manager's second RESUME (after the 06:5x stop) then ordered the restatement.
- 07:06 commits a840c14d and 32a9242f. qimg on the tree: six identical, two one instruction apart. The four legs launched at 07:08.
- 07:24 the control leg ended rc 0. 07:25 the host shut down; the other three were cut.
- 08:05 the three relaunched on the new CPU layout. Doc edits meanwhile.
- 08:36 VDl, 09:51 VDh and 10:13 VDt ended, each rc 0.
- 10:14 commit d0a2a160.
- 10:15 the final gates on clean clones of it (launchM.py, at most 4 units). 10:15-10:47 the probes, the grader comparison and the image control in the foreground.
- 10:46 three of my running units were found at affinity 0-95, though each was started under `taskset` on its 8-CPU range: harness on 48-55, SRP campaign on 32-39, docs-gates-2 on 56-63. Re-pinned by `taskset -a -cp` over their own cgroups' processes, they were widened again within about 30 s, and firmware-unit's new unit too. The user manager has no cpuset controller (its subtree control is cpu, memory and pids), so a unit cannot hold its range. This is the host's doing, not the units'; I left them as they were.
- 10:47 harness self-test rc 0; 10:56 docs-gates-2 rc 0; 11:13 firmware-unit rc 0 (started 10:45 after a slot freed).
- 11:1x the receipts, PR-BODY.md, the comment, the index; the REVIEW READY posted once on #894.

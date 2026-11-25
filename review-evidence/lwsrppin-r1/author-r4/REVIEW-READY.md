[A834] EVIDENCE, round 4 (R913-4 F1 option (a), F2). Not review-ready: one decision is open (below)
Commit: 507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698 (unchanged, pushed; no commit this round)
Changed: nothing in the tree. `PR-BODY.md` is the full PR body at this head (F2). The harness was measured on the
merge head's images (F1), and so were the budget model and the egress ledger.

## F1: the CPU budget harness on the merge head's images

**Image identity** (`receipts/harness/identity.txt`, `variant-objects.txt`). Arm A's `ctrl_app.elf` is
`79c5326cba02dca37fd82946c2f2c13153d8ecf07875ab673536188107d43f89` at 1x1/1if and
`eed56acc86f3c48db1e537b06c72c5e78478e1dc79c1b0c3daeec3a8dd4771c0` at 8x8/1if. Those are the sha256 recorded in
`build.json`, hashed again from the file, and equal to round 3's ledger files
`endstation_ax7101_1x1_tdm8/split-soc/mapped/image/ctrl_app.elf` and
`endstation_ax7101_8x8/split-soc/mapped/image/ctrl_app.elf` at `507bce7f`, rehashed this round. The two variants'
images differ from arm A's in exactly one object of 37, the size fixture `ctrl_aecp_image.o`, which carries the
variant's test edits (`build.py` `VARIANTS`). `mrp_mad.o` is identical.

**Commands.** These are round 1's (`tools/harness1.sh`): `run.py --point {1x1,8x8-1if} --build-dir <scratch>
--variant {none,answering-every-port,answering-later} --record-budget-findings --record-share-findings`, from the lane
checkout at `507bce7f`, with porcelain 0 before and after. The six runs and `run.py --self-test` ran as seven
separate systemd user units in parallel, with MemAvailable 55 to 70 GB. The grading is round 1's
`harness_grade.py` and `la_window.py`, plus `share_census.py` (every pass over THE SHARE, named by group), the
train's `kept_grade.py <build-dir>` on arm A, and `egress_ledger.py --point 8x8-1if` (`tools/grade1.sh`).

| Run | rc | Groups | Over THE SHARE | Longest pass | MRPDU worst (49) | Misses | Other |
|---|---|---:|---|---:|---:|---|---|
| arm A 1x1/1if | 0 | 101 | 0 of 180,084 | 154,510 | 2.345 ms | the 7 held-egress rows | `kept_grade` PASS, 0 findings, 4 owed |
| arm A 8x8/1if | 0 | 101 | 1 of 325,929: `srp-bound` 210,174, owed to #977 by `kept_grade` | 175,919 outside `srp-bound` | 3.205 ms; own-LeaveAll 0.513 / 0.542 / 0.543 ms | the 7 held-egress rows | `kept_grade` PASS, 0 findings, 5 owed; **egress ledger FAIL** |
| every-port 1x1/1if | 0 | 16 | 0 of 27,884 | 154,723 | 1.039 ms | 0 | 192 notices within 130 ms, worst 21.42 |
| every-port 8x8/1if | 0 | 16 | 0 of 19,552 | 174,608 | 1.184 ms | 0 | 640 notices within 130 ms, worst 30.17 |
| later 1x1/1if | 0 | 8 | 0 of 18,298 | 151,821 | 0.858 ms | 0 | 8 notices within 20 ms, worst 8.24 |
| later 8x8/1if | 0 | 8 | 0 of 13,771 | 155,638 | 0.858 ms | 0 | 8 notices within 20 ms, worst 8.28 |
| `run.py --self-test` | 0 | | | | | | `self-test: 0 failures` |

- **Budget model at the head** (`receipts/budget/`): `load_grade.py --check` PASS, 0.512 (0.70) and 0.744 (0.75).
  `flip_grade.py --check` PASS: at 1x1/1if txL 47.98 ms (49), last queued notice 127.43 ms (140 owner), ACMP 29.15 ms
  (30); at 8x8/1if `CTRL_LOOP_TX_MS` 77 against 76.86 ms. All three outputs are byte-identical to `2509db68`'s, run
  this round in the train worktree.
- **The own LeaveAll** (`la-window-*.txt`). Every pass in the second after each LeaveAll timer run-out is within
  THE SHARE at both points. MSRP's LeaveAll MRPDU leaves 160.36 to 160.52 ms after its timer (the running join timer),
  and MVRP's 0.36 to 0.42 ms.
- **THE SHARE at 8x8/1if.** The one pass over it is `srp-bound`'s, the bound path's registrations. #969's amended
  ruling owes it to #977, `kept_grade` holds every condition of that disposition (0 findings), and the train's own
  record says the same ("No work pass is over THE SHARE but `srp-bound`'s"). On the train's own image the same pass
  is 216,785 cycles, so the merge's is 6,611 smaller. Against R913-4's wording ("0 passes may exceed THE SHARE"),
  this pass is owed by an existing ruling, not absent.

## The open decision: the egress ledger at 8x8/1if (`receipts/harness/egress-ledger-8x8-1if.log`, `egress-compare.txt`)

`egress_ledger.py --point 8x8-1if` exits 1 at the merge head: all 7 rows are over their ledger figures. Round 1 at
the pin passed. The ledger's rule (`docs/design/SPLIT_CONTROL_MEMORY.md:3042-3043`, #894's ledger ruling) is that a
larger miss fails the leg, and that a restatement needs a ruling. So no commit can settle it in this lane.

Attribution. The same two groups were run on the train's own image: `run.py --point 8x8-1if --groups
backlog-owed,srp-bound` in the train worktree at `2509db68` (porcelain 0). That image is `74f8d3c7…`, the round-3
ledger's `2509db68` mapped image, and it differs from the merge head's only in `mrp_mad.o`
(`train-2509db68/identity-base.txt`). Its rc is 1 only because `kept_grade`'s pair rule refuses `srp-bound` graded
without `srp-kept`, which is expected for a two-group run.

| Row | Pin `402834ac` | Train `2509db68` | Merge `507bce7f` | Merge - train | Ledger | Train over | Merge over |
|---|---:|---:|---:|---:|---:|---|---|
| `backlog.owed.if0` | 63.201 | 64.014 | 64.100 | +0.086 | 63.86 | yes | yes |
| `backlog.owed_behind0.if0` | 63.408 | 64.207 | 64.292 | +0.086 | 64.10 | yes | yes |
| `backlog.owed_behind1.if0` | 63.615 | 64.397 | 64.483 | +0.086 | 64.36 | yes | yes |
| `backlog.owed_behind2.if0` | 63.821 | 64.587 | 64.674 | +0.086 | 64.61 | no | yes |
| `backlog.owed_behind3.if0` | 64.027 | 64.778 | 64.864 | +0.086 | 64.86 | no | yes |
| `backlog-owed.service.acmp.last.if0` | 62.212 | 63.036 | 63.130 | +0.094 | 62.62 | yes | yes |
| `backlog-owed.service.aecp.last.if0` | 61.567 | 63.071 | 62.848 | -0.223 | 62.16 | yes | yes |

- The train lands with the leg failing at 8x8/1if: 5 of 7 rows over, by 0.037 to 0.911 ms. Its record of the
  composition lists the seven misses but not the ledger's verdict. The train grew every row by 0.75 to 1.50 ms over
  the pin's.
- The pin's lwSRP change on the composed image adds 0.086 to 0.094 ms to six rows and takes 0.223 ms off
  `service.aecp.last`. That takes two more rows over: `owed_behind2` by 0.064 ms and `owed_behind3` by 0.004 ms.
- `egress_ledger.py` is byte-identical at `2509db68` and `507bce7f`. Its self-test passes at the head (15 mutants).
- Choices for the owner: a ruling that restates the ledger at the composed measurement (the rule's figures derive
  from the largest measurement plus 5 %), or another disposition. The train-side failure probably wants its own
  Issue, since it exists on `dev-soft-core` without this PR.

## F2: the PR body

`PR-BODY.md` replaces the 05:49Z body (kept as `receipts/pr-body-before-r4.md`). It describes the sync merge (the
parents, the base, both conflicts and how both sides were kept, `git merge-tree` reproduced in
`receipts/merge/merge-facts.txt`). It gives every gate at `507bce7f` with its result. It gives the image deltas
against `2509db68` (`.text` +60 B, ROM +56/+56/+64/+64, tiles and SRAM unchanged) and against `30796098` (the train's
content), the merge-head route (-24 LUT, #818 floor met), the harness rows above, and the egress decision. Removed
are "stand from `402834ac`", "byte-identical to the previous head's", "the route stands for this head", the
`dbba60e6` route table and the pre-merge out-of-context LUT/FF table. The reproduction's red leg and the srptx counts
are kept, each labelled with the commit it was measured at.

Acceptance criteria (issue #991 AC2, harness part): met for the six harness runs and the self-test (rc 0, image
identity proven). **Not met** for the egress ledger leg at 8x8/1if, which is pending the decision above. The single
pass over THE SHARE is owed by an existing ruling.
Open risks/questions: the egress ledger decision. The R1 residue (the docstring's "sent as Lv") is unchanged; no
commit was in scope.

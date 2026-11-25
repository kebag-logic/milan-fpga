# [A839] CICD improvement — round 4 handoff

Status (2026-11-24 22:40 CET): ROUND 4 DONE: REVIEW READY at both heads. One acceptance item is a decision for the
owner (#1003, shard 17's 30.7 minutes on a 1.41× runner; see below). ETA: done. Nothing of mine is running.

**Heads**

- milan-fpga `cicd-3` = `45d5c35a4470057966a72c0e85e49af1921152a0`: three new commits on round 3's `13e6d869`:
  - `d95e95e8`: staging lock domain and root proof;
  - `59f4f478`: dealer figures;
  - `45d5c35a`: review wording.

  **Pushed** to kebag-logic/milan-fpga `cicd-3` (PR #1003) at 21:30 CET, only to trigger the hosted run.
  `push-privacy-check.py . 13e6d869d842…` reported 0 private lines first. The command ran bare.
- FPGA-gPTP `engine-run-passes-at-once` = `661e4c3a45904d2d8f3e061c67103a945651d9ff` (one new commit on `bbda770`),
  in /data-2/milan/tmp/cicd-a839/r3/fpga-gptp. **Not pushed.**
- No comments posted, no PR body edited, nothing merged.

**Results**

1. **#1003 R924-1-F1 and R923-1-F1, fixed** (`d95e95e8`).
   - The lock is now the slot directory's own inode: one lock domain for any TMPDIR, alias or user.
   - The root is proved before use (owner, mode, no link, inside the resolved TMPDIR, atomic `mkdir` 0700), or
     refused with its reason and staged cold.
   - Self-test: 17 controls, six with independent processes. 10/10 planted defects caught.
   - The probe reproduces both collisions at `13e6d869` and none at the head, with a real second uid.
   - Five drivers' logs are identical, with warm hits 100 %.
2. **#1003 R923-1-F2, attributed** (`59f4f478`).
   - It was runner speed. Identical builds took 1.36-1.41× as long in that job. On one host the head ran shard 1's
     pieces faster than the base: milan_dp__1 −13.7 %, equal instructions.
   - Shard 1 was the heaviest worker even at the base because `milan_dp` leg 1's figure was stale (508 s against
     995 s measured). The figures are now re-keyed from two complete hosted runs; none is lowered outside those
     legs.
   - Worst projection 1615 s, 185 s inside 30 min.
   - Hosted run 45481508309 at the head is green:
     - shard 1 took 16.1 min;
     - 18 of 19 workers took 12.7-27.4 min;
     - receipts 24/24 and verdict sets 83/83 are identical to both earlier runs.
   - **Open: shard 17 took 30.7 min** on a runner whose builds took 1.41× as long.
3. **FPGA-gPTP #112** (`661e4c3`).
   - Each pass is a make job, so the caller's `-j` and jobserver bound them.
   - Four `run::` rules replay the passes, so `-s`, `-i`, `-k` and signal names give the serial transcript. Fail
     fast and QUIT are taken.
   - `make passes-test` (63 checks, 96 s) is in `all`. 9/9 planted defects caught.
   - Real harness at `-j4`: 453 → 221 s and 653 → 221 s in two concurrent pairs, instructions +0.29 %. `-j1` keeps
     the serial time. Transcripts are IDENTICAL at matching flags. A planted abort gives the same transcript but
     for the line number.
4. **Proof sets.**
   - #1003: 36/36 gates at `45d5c35a`, plus the hosted run.
   - FPGA-gPTP: `make docs`, `make lint` and `passes-test`, plus the real-harness pairs.

**Written:** REPORT.md, PR-BODY-1003.md and PR-BODY-112.md (full replacement bodies), receipts/INDEX.md.

**For the manager**

- **Decision (Issue #998 acceptance 2).** Dealing cannot give a 30-minute margin against a 1.41× runner. Five
  indivisible pieces are 1309-1493 s; a 1.41×-proof worker must project at most about 1277 s. Choose one:
  - split those suites further and add workers, at a cost in runner-minutes;
  - accept "within 30 minutes on a runner of the base run's speed".

  I did not re-run jobs to draw a faster runner.
- **The native bank.** It must run `make -C gptp-processor all` with `-j4` (or under its jobserver) to keep the
  engine gain once #112 lands. Without `-j` the passes now run one at a time, honouring the budget.
- **PR #1003's title.** It could add "and refresh the dealer's figures".
- **PR #1003's base.** It still targets `dev-soft-core`, as the reviewers noted. The stacked source base is
  `fcbc31f3`.
- **Publishing receipts.** They carry this host's scratch paths (the lane's own directories); round 3's were
  published the same way.

**Said plainly**

- One FPGA-gPTP measurement batch was void: two arms shared one clone. Every timing was re-measured with one clone
  per arm. Its transcripts had compared IDENTICAL and are not relied on.
- I wrote my first plant runs onto the siblings of measuring arms. Those timings were discarded and re-run.
- Removals inside my own r4 scratch were logged to disk-cleanup.log after the fact, not before.
- Not run: the act replay, the full serial sweep, the milan_dp__0 piece replica (its code changed by one comment).

**Session notes:** booking found no free range all evening, so every arm ran in the session pool 64-95, on CPUs
named per receipt. Only the shared ccache was used. Scratch is /data-2/milan/tmp/cicd-a839/r4, 3.3 GB of 40.

REVIEW READY 45d5c35a4470057966a72c0e85e49af1921152a0 661e4c3a45904d2d8f3e061c67103a945651d9ff

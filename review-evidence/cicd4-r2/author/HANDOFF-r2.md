# [A839] CICD improvement, round 4, PR #1019 round 2 (#1008): handoff

**Status (2026-11-26, CET): REVIEW READY at `6841c5e3be` (lane `1008-ci-30min`). Nothing pushed, nothing
posted.** The PR body still says "Relates to #1008".

**ETA:** nothing of mine is running; the last unit was `milan-cicd4-a839-r2gates2`. The rest of #1008 is still
open (see below): about one more round, for a Verilator tool job.

**Resume note.** The restart cut my earlier session. The lane was clean at `5b5b0765` (the pushed PR head), with no
uncommitted work, so nothing needed recovering. No comment of mine was posted, so nothing risks being posted twice.

## Commits on `5b5b0765` (one-line subjects, no trailers)

1. `d13db4c7` F1: the contract holds each campaign job's command COUNT to its own matrix's leg count, and every
   other job to no campaign leg. The generator self-test holds the same, and the policy page states it.
2. `e1793704` F4, the suggestion: the dispatch proof derives each leg through the driver's own `campaign_leg`
   mapping, so the reviewer's P6 (the mapping removed) is now refused.
3. `d1b42005` F2/D1 and F3:
   - the policy page names `docs-gates-1` at 1302 s as docs' slowest worker, over the 1276 s budget, and
     recomputes the workflow total (1572 s, 26.2 minutes, 228 s inside 30);
   - the generator comment cites the table's 1237 s for worker 3.
4. `5780feb8` Merge dev-soft-core `4df125b8` (PR #1016), a merge commit with no conflicts. The workflows
   regenerate unchanged.
5. `2f5f5d31` `gptp_shadow` re-keyed to 679 s for the merged pin 3ce71b76. The 27 Verilator rows are re-stated;
   the largest regular worker is 1275 s.
6. `6841c5e3` the hosted failure's fix: `ctrl_configs.OUTSIDE` lists `scripts/ci_fast_legs_selftest.py`.

## The reviews, finding by finding

- **R947-1 F1, fixed at the root.**
  - `check_fast_legs` now reads every `--campaign-shard` in the generated graph and requires each campaign job to
    run exactly `--campaign-shard "${{ matrix.leg }}" N`, with N its own matrix's length. Any other job must run
    none.
  - 13 new arms are each caught: COUNT +1 and -1, a fixed index 0, the phase twice, and a campaign leg in
    `firmware-unit`. With these the event self-test's fast-leg stage has 35 arms.
  - The reviewer's probe P1 (the generator emits COUNT+1, workflow regenerated) is now refused by
    `ci_events.py --check` for all three campaign jobs, and by `ci_fast_legs_selftest.py`. The unplanted head
    passes, and the clone was restored (`receipts/probes/P1.txt`).
- **R947-1 F2 and R948-1 D1, fixed.** The paragraph now matches the table: `docs-gates-1` at 1302 s, with the
  workflow at 1302 + 60 + 60 + 120 + 30 = 1572 s. It states that 1302 s is over the per-job budget and that the
  workflow figure does not meet it.
- **R947-1 F3, fixed.** The comment states the table's rule and figures: worker 3 at 1237 s (961 s of steps and
  276 s of setup), and `docs-gates-1` at 1302 s.
  - The reviewer's 1244 s uses another setup figure. Mine is `docs-gates-1`'s sum of its setup steps' maxima, as
    the table's row was made.
  - In this PR's hosted run, `docs-gates-3` measured 671 s.
- **R947-1 F4 (suggestion), done.** The reviewer's P6 is now refused: the proof finds every control defect
  planted by every leg.
- **R948-1 T1, done.** The five original census receipts are in `receipts/census-receipts/`, with `SHA256SUMS`,
  at their execution head `530149b5` (tree `08e15b7d`). They are the files the judge read, not regenerated and not
  relabelled.
  - `replay.sh <clean clone at 530149b5> <scratch>` checks the hashes and the head, then replays the union (rc 0).
    Its output is byte-identical to the original `union.log`, apart from the summary line.
  - It then replays the seven planted faults, each refused (`replay.txt`).

## The PR's own hosted run (at `5b5b0765`, read for this round)

- **docs and elaborate succeeded.** **rtl-fast failed** in `firmware-boundary`. The head's fail-fast watcher then
  cancelled the rest of rtl-fast and rtl-full: rtl-full's unions failed on their cancelled shards.
- **The cause is this PR.** The boundary judge refused the new `scripts/ci_fast_legs_selftest.py`: it names the
  firmware's tree and was in no list (log `receipts/hosted/firmware-boundary-139800171201.log`, line 529).
  - My round-1 gates did not run the boundary judge, which needs the hosted captures.
  - I now run its text scan (`ctrl_configs.held`'s loop) as a gate. At `5b5b0765` it refuses exactly this file; at
    the head it passes (`receipts/probes/boundary-scan.txt`).
  - The file compiles nothing, so it goes in `OUTSIDE`.
- **Measured legs** (`receipts/hosted/windows.tsv`): every divided leg is within 1276 s.
  - control 573/712/517/502;
  - AECP 610/629;
  - SRP 751/980;
  - unit 973/209/587;
  - census legs 298-379, judge 36;
  - docs workers 456-717.
- **Untouched jobs** in that run, also within 1276 s:
  - `firmware-verilator` 1147 s;
  - `elaborate-gates-1` 1258 s;
  - rtl-full `Prepare pinned Yosys` 1163 s, a cold build;
  - the Verilator shards that finished, at most 987 s.
- Acceptance 1 of #1008 needs two runs, and this is one. The next push gives the second, and the first complete
  rtl-full at the merged content.

## For the manager

- **`gptp_shadow`.** One complete hosted run has the merged content exactly: 45755846909, at d3cb3cf1, 679 s. Run
  45735453538, at the same pin before that suite's last two edits, measured 672 s. #1008's rule wants two runs:
  please confirm 679 s, or wait for the next.
- **Verdict identity.** The serial comparisons were made at the pre-merge base. After the merge, the control table
  grows by 3, to 847, and the dispatch proof deals them 212/212/212/211 once each. I did not re-run the legs locally
  at the merged head; the host had 88 of 96 CPUs booked.
- **The bound.** I still read it as hosted ≤ 1276 s, as the issue states it (the round-1 question stands).

## Gates (`receipts/gates/summary`, a clean clone at the head, unit at CPUWeight 10, no free range)

40 of 40 commands rc 0 at the head, the boundary judge's text scan included. The event self-test passes 2409 contract items
and 6174 arms (round 1: 2390 and 6161). `ci_gate_workflows --check`, `ci_events --check`, the generator, leg,
dispatch and suite-shard self-tests, the code-quality and documentation gates and `check_em_dash` (base 4df125b8)
all pass.

## Said plainly

- **Not run:** a local act replay, a hosted injected failure, a push, and the rest of #1008. The Verilator tool job,
  the builder's single gate and Yosys shard 0 stay open; no time was left this round.
- **Removals.** Two removals were logged late in `disk-cleanup.log`, marked LATE:
  - 26 shard logs that the same command had just downloaded and dropped for holding no `gptp_shadow`;
  - a `dispatch-build/` in my own probe scratch.
- **Restarted gate run.** The first round-2 gate run (at `2f5f5d31`) was stopped when the hosted failure surfaced;
  its partial logs were removed (logged).

REVIEW READY 6841c5e3be

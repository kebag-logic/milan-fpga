# [A839] CICD improvement — round 3 handoff

Status (2026-11-24 19:15 CET): ROUND 3 DONE: REVIEW READY at 13e6d869. ETA: done. Nothing of mine is running.

- `cicd-3` (local, not pushed) = `13e6d869` on PR #1001's head `fcbc31f3`, three commits:
  `66b092e1` preflight once per head, `f6c11a25` stable mutant staging, `13e6d869` longest case first.
  `cicd-verilator-perf` was not touched. No comments were posted and nothing was pushed in either repository.
- Every gate this round touches passes at `13e6d869` in a clean clone (receipts/gates/summary, 36 entries),
  including `ci_events.py --selftest` (5755 arms) and both mutation-lifecycle and cancellation tests.
- Written: REPORT.md, REVIEW-READY.md, PR-BODY.md, smt-booking.patch, PROPOSAL-hosted-ccache.md,
  PR-BODY-fpgagptp.md, receipts/INDEX.md.

Results:
1. Preflight once per head:
   - The shard 9 replica started its first suite at +2 s instead of +535 s and used 134 CPU-s less.
   - Logs and receipts are IDENTICAL.
   - A failing, cancelled, skipped, wrong-SHA or missing preflight makes `verilator-suites` red (the generated
     step was executed).
   - Hosted: about −78 s per worker and −23 runner-minutes per run.
2. Longest case first: milan_dp__0 through its driver 3411.9 s → 2711.8 s wall (−20.5 %) at the same instructions; receipts IDENTICAL. aclk (1558 CPU-s) now starts first in milan_dp__0, and
   render-mutants first in milan_dp__1.
3. Stable mutant staging:
   - Warm-cache hits: crf_rx 79/115 → 115/115 (−25 % CPU), avtp_rxmon depkt 37/48 → 48/48 (−64 %), tcam 12/16 →
     16/16, rx_filter 6/8 → 8/8.
   - All logs are IDENTICAL, so every mutant is killed by the same named check.
   - Round 2's rx_filter finding 3 had the same cause and is fixed by this change.
4. SMT booking patch, for you to review and apply (`patch -p1` from 2026-09-23/; dry-run clean, live files
   unchanged): the measured before/after showed **no gain today**.
   - Cycles were equal, because the idle siblings were not idle.
   - `cpu_ranges.py show` (patched) lists ten units with affinity 0-95: seven sessions launched outside
     lane-queue's session_pool(), this one included, and three gate units (lwsrppin-a834-r4-h-1x1,
     lwsrppin-a834-r4-h-8x8-1if, qual1124-a840-chain8).
   - Those must be confined before whole-core booking can pay off.
5. FPGA-gPTP branch `engine-run-passes-at-once` (`bbda770`) in /data-2/milan/tmp/cicd-a839/r3/fpga-gptp, not
   pushed:
   - `make run` 2721.6 s → 974.6 s wall, +2.3 % CPU;
   - transcript IDENTICAL;
   - the TERM and failing-pass paths were checked by hand;
   - `make docs`/`lint` pass.
6. Proposal: delete the merged PRs' Actions caches now (206 entries, 3.64 GB, one command in the proposal). Then
   key the tool caches by recipe and save them only from dev, add ccache to the image through #737, run the shards
   in the image, and add a restored per-shard ccache.

For the manager:
- The SMT patch, and the ten unpinned units it names.
- Deleting caches is your call; the proposal has the exact command, and nothing was deleted.
- After #1001 merges, rebase cicd-3 onto dev, open the draft PR with PR-BODY.md, and run the act replay and a
  hosted run. Not done here, since this lane does not push.

Incomplete, said plainly:
- No act replay, no hosted run, no full serial sweep.
- The mmcm_servo slew-mutant arms were stopped (my own units) after its 3918 s cold run. Its warm runs would have
  taken ~3 h at this load. Its base-cold row stands, and the head's partial log matched it line for line.
- Two commits were amended after their measurements (the `dir` → `parent` rename; the cost table's final
  figures). Neither changes behaviour or start order, and REVIEW-READY says which SHA each measurement ran.

Session notes:
- Measurement jobs ran as this session's own `milan-cicd-a839e-*` systemd units, pinned with taskset and visible
  to cpu_ranges' busy(). They were polled from foreground commands; none outlived its purpose. I stopped only my
  own units.
- Scratch is /data-2/milan/tmp/cicd-a839/r3 (2.3 GB of the 40 GB allowance; every measurement clone is removed, and the FPGA-gPTP scratch clone with the branch is kept).

REVIEW READY 13e6d869d842fc06155ef5dae9b0347596d6d4df

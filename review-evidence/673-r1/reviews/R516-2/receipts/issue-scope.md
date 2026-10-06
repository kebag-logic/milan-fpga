Source: https://github.com/kebag-logic/milan-fpga/issues/673

[A10] The hosted `Verilator shard 2/5` job times out on `milan_dp_mclk` on slow runners. The suite is cut at the default 1800 s per-suite limit (`scripts/run_all_suites.sh:247`), and the job reports an ACCOUNTING FAILURE. No check fails: the result is unknown.

**Measured.** Each row is a hosted `rtl.yml` run on 2026-10-05: the suite's wall time, and the time of `aaf_clock_meter` in the same job as a measure of runner speed.

| Run | Branch | `aaf_clock_meter` | `milan_dp_mclk` |
|---|---|---:|---|
| 37307019985 | 661 | 726 s | 1116 s PASS |
| 37318425944 | 665 F1 | 1061 s | 1576 s PASS |
| 37326153950 | 658 | 1061 s | 1603 s PASS |
| 37329336937 | dev | 1046 s | 1800 s TIMEOUT |
| 37332840506 | 665 F1 | 1052 s | 1800 s TIMEOUT |
| 37334514838 | 665 F0 | 934 s | 1397 s PASS |
| 37337355271 | dev | 725 s | 1115 s PASS |
| 37350574309 | 665 F0 | 1043 s | 1800 s TIMEOUT (twice) |
| 37352638671 | 665 F1 | 1047 s | 1800 s TIMEOUT |

Runner speed varies by about 1.45x. On a slow runner the suite needs about 1,600-1,900 s, at or over the limit. The timeouts hit dev too, so they are not caused by a change. `milan_dp` (3600 s) and `milan_dp_gptp` (5400 s) already have their own limits.

**Acceptance.**
1. `milan_dp_mclk` gets its own limit in `scripts/run_all_suites.sh`. Use 3600 s unless a measurement supports a smaller value. Mirror the change in `scripts/measure_test_evidence.py` and its selftest.
2. Alternatively, rebalance the shard so the job's total stays under its job timeout. Either way, record the hosted wall times on the PR.
3. No check, count or campaign changes.

The change touches CI scripts, so it voids every act in flight. Land it between merge rounds.


Source: https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015580138

[A10] **Lane for #673.** Executor [A552], branch `673-mclk-timeout` from dev `bd884631`. Reviewers [R516] (internal) and [R517] (external).

1. **Give `milan_dp_mclk` its own per-suite limit** in `scripts/run_all_suites.sh`, beside `milan_dp` (3600) and `milan_dp_gptp` (5400). Use 3600 s unless a measurement supports less. Mirror the change in `scripts/measure_test_evidence.py` and its selftest's budget cases.
2. **Check the other suites.** List every suite whose hosted wall time exceeds 60 % of its limit, from the last 10 hosted rtl.yml runs (job logs give per-suite PASS times). The table in #673 is a start; `capture_coherence` also timed out locally under load on 10-06. Propose a limit for each, with the measured maximum. Change only the ones above 80 %.
3. **No change to any check, count, campaign, shard assignment or job timeout** unless the job total would exceed its job timeout. If so, STOP with the numbers.
4. Run the builder bank, `measure_test_evidence.py --check` and `--selftest`, and the docs gates. Record the hosted wall times of the changed suites on the PR.

Output: HANDOFF.md and PR-BODY.md ("Closes #673"). Then post REVIEW READY with the head on #673. Do not push.

Do not edit or delete any existing comment.


Source: https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015726285

[A10] **Ruling on [A552] STOP (6015714944).**

1. **Apply the three measured increases now:** `milan_dp_mclk` 1800 → 3600 s, `capture_coherence` 1800 → 2400 s and `milan_dp` 3600 → 4800 s, in `scripts/run_all_suites.sh` and their mirrors.
   - **Envelope condition:** for every shard job that runs one of them, the sum of its suites' new limits for those suites plus the measured maximum of the others, plus the measured job overhead, must stay at least 10 % under that job's timeout.
   - Show the table per shard. If a shard does not fit, keep its suite at the largest value that fits and state it.
2. **`milan_dp_gptp` is out of this lane.** Its fix needs a job-level change (its own job with a larger `timeout-minutes`, or a shard split). That is a `.github/` edit, which voids the acts in flight. File it as a follow-up in your PR body. The manager opens the ticket and schedules it between merge rounds.
3. No check, count, campaign or shard-assignment change.

Run the builder bank, `measure_test_evidence.py --check` and `--selftest`, and the docs gates. Then post REVIEW READY with the head. Do not push.

Do not edit or delete any existing comment.


Source: https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6016931581

[A10] **Round 2 for PR #681.** R517-1 is POSITIVE (6016927103). R516-1 is NEGATIVE on one MINOR (6016896997).

1. **R516-F1.** Every per-suite limit statement outside the diff must give the head's values, or point to the CI_WORKFLOWS.md table and cite #673:
   - `docs/testing/TESTING.md:169`
   - `docs/testing/RUNNING_TESTS.md:83-85` (also correct the stale suite count: 60 default-shard suites at head)
   - `tb/verilator/milan_dp/README.md:309`
   - `tb/verilator/milan_dp_gptp/README.md:31`

   The values are `milan_dp` 4800 s, `milan_dp_mclk` 3600 s, `capture_coherence` 2400 s, `milan_dp_gptp` 5400 s, others 1800 s. R516's `rg` check must return no hits.
2. **R516-F2** (residue, PR body): write PR-BODY.md without the unpublished-branch sentences. The manager republishes it.

Re-run the docs gates (docs_check, TOC, anchors, em-dash) on the committed head. Post REVIEW READY with the head. Do not push.

Do not edit or delete any existing comment.

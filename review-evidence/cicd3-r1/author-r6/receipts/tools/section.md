- **The runs.** I pushed at 02:50 CET. All four runs succeeded on their first attempt, so I used no
  re-run: rtl-full 45528738040, rtl-fast 45528738009, elaborate 45528738049 and docs 45528737977 (01:51-02:56Z).
- **The split, hosted** (receipts/hosted/run-9c625393/):

  | Job | Minutes | Its part of the step | Against the same part's 14 earlier windows |
  |---|---:|---|---|
  | `firmware-boundary-capture (0)` | 13.2 (792 s) | control gate build 711 s | 1.02 × median, 0.92 × slowest |
  | `firmware-boundary-capture (1)` | 14.1 (848 s) | five builders 774 s (coverage 560, store 127) | 1.54 × median, 1.30 × slowest |
  | `firmware-boundary` | 5.5 (328 s) | the step less its builds, 221 s; both downloads 9 s | 1.04 × median, 0.89 × slowest |

  - Leg 1 drew a slow runner. Its coverage build took 560 s, where 14 earlier windows took 433 s at most. Its
    job exceeded its 749-second projection by 99 s and still took 14.1 minutes.
  - Each capture uploaded as a 46 MB zip in about 5 s (2120 and 1914 files).
  - **Same verdict, hosted.** The judge printed `4032 compiled sources of 4325 recorded invocations (2464 the
    firmware's, 425 the stack's, 1143 test equipment's and builders' own) … 0 finding(s), 112 boundary, 192 pin
    and 4 figure controls, 0 misbehaved`, then `PASS`. Those are the counts of the last complete whole-step run,
    45481508222. Its step output equals that run's in every line but two kinds:
    - the eight builder lines, which the legs print;
    - one line's random temporary sysroot name (`/tmp/fw-rv32-…`).

    The diff is hosted-whole-vs-judge.diff.
- **Jobs over 30 minutes.** These are the stop condition.
  - rtl-fast `firmware-control-mutants`: **38.8 min** (2330 s, 45-minute limit). It is 1.39 times the median of
    its 14 earlier windows, and 0.99 times the slowest.
  - rtl-fast `publication-census`: **37.2 min** (2230 s, 45-minute limit). It is 1.12 times its median, and 0.84
    times the slowest.
  - So both are long on ordinary runners. The ruling did not split either.
  - The fail-fast watchers span their runs: rtl-full 64.7 min, rtl-fast 54.6, elaborate 38.3 (docs 26.3).
  - **The slowest job that is not a watcher** is `firmware-control-mutants`, with runner factor 1.39 against its
    median.
- **Every other job is within 30 minutes.** The next slowest:
  - Verilator shard 1/26: 27.7 min (1662 s, 1.33 times its projection of 1250 s);
  - `firmware-aecp-mutants` 26.3 (1.30 × median), shard 15/26 24.9, `elaborate-gates-4` 23.7 (1.52 ×),
    `docs-gates-2` 23.1 (1.43 ×), shard 24/26 22.8, `firmware-unit` 22.2, shard 8/26 21.9.
- **Round 5's deal, first hosted evidence.**
  - All 26 workers passed, in 389.0 job-minutes. Round 5 projected about 385; the run before took 353.8.
  - Each job's minutes over its projection ran from 0.41 to 1.33. Leg A took 845 s (14.1 min).
- **Suite by suite against run 45481508309** (round 5's comparison tool, suite-compare-…txt):
  - The verdict lines are identical for 63 of 65 suites.
  - The case receipts are identical for 5 of 6 suites that keep receipts: `capture_coherence` (43 cases, 4 → 8
    legs), `maap`, `milan_dp_mclk`, `milan_dp_render` and `pp_shadow`. `follow_ring` and `media_phase` are new
    case suites.
  - `capture_coherence`'s verdict lines differ by construction. They are per-leg tally lines, and the totals are
    equal: 44 checks in both runs (2 × 11 + 12 + 10, and 5 × 5 + 2 × 6 + 7).
  - **`milan_dp`'s cases `gptp` and `gptp-lat` differ.** Both pass in both runs. Each prints one diagnostic line
    that differs: `[#207] full-queue window: level 1, rp 0->0, wp 1->1` before, `rp 1->1, wp 2->2` now.
    - The earlier value is in every log I have from rounds 3-5, 26 occurrences, hosted and local. These
      include round 5's local 8-leg pieces 0/8 and 1/8, which run these two cases.
    - So the 8-leg deal alone did not change it locally. The cause is not established.
    - The receipts differ, so #998 acceptance 1 (identical outputs) is not shown for `milan_dp`. This is open.
- Every job's minutes are in the table at the end of this report (84 jobs; the nightly physical leg was skipped).

**Hosted runs at `9c625393`.** All four succeeded on their first attempt: rtl-full 45528738040, rtl-fast
45528738009, elaborate 45528738049, docs 45528737977. Every job's minutes are from the Actions jobs API
(`completed_at − started_at`). Each factor is the job over the median of its own earlier successful windows.

| Job | Minutes | Note |
|---|---:|---|
| `firmware-boundary-capture (0)` | 13.2 | the control gate's build 711 s (1.02 × its median) |
| `firmware-boundary-capture (1)` | 14.1 | five builders 774 s, on a slow runner (1.54 × median, 1.30 × the slowest earlier window) |
| `firmware-boundary` | 5.5 | `PASS` with the whole run's counts and controls |
| **`firmware-control-mutants`** | **38.8** | **over 30 minutes**: 1.39 × median, 0.99 × its slowest; 45-minute limit; not split here |
| **`publication-census`** | **37.2** | **over 30 minutes**: 1.12 × median, 0.84 × its slowest; 45-minute limit; not split here |
| Verilator shard 1/26 (the slowest worker) | 27.7 | 1.33 × its 1250-second projection |
| `firmware-aecp-mutants` | 26.3 | 1.30 × median |
| Verilator workers, all 26 | 389.0 job-minutes | round 5's projection about 385; 353.8 before. Leg A 14.1 minutes |
| Fail-fast watchers | 64.7, 54.6, 38.3, 26.3 | each waits for its whole run |

- **The judge's verdict matches the last whole-step run, 45481508222.** It printed the same counts, `4032 compiled
  sources of 4325 recorded invocations`, the same 112 boundary, 192 pin and 4 figure controls, and `PASS`. Its step
  output equals that run's, except the eight builder lines (printed by the legs) and one random temporary
  sysroot name.
- **firmware-boundary's runner-minutes.**
  - Before: 1461 s on average over fourteen runs, 1528 s at the previous head (26 billed minutes).
  - After: 792 + 848 + 328 = 1968 s, +35 % (35 billed minutes). The excess is two more setups and a slow leg-1
    runner; at the earlier runs' mean phases the cost is 1630 s, +12 %.
  - The family's wall span was 22.6 minutes, against 25.5.
- **Round 5's deal, suite by suite against 45481508309.**
  - Verdict lines are identical for 63 of 65 suites. `capture_coherence` differs only in its per-leg tallies, with
    44 checks in both runs; `follow_ring` and `media_phase` ran as new case suites.
  - Case receipts are identical for `capture_coherence` (4 → 8 legs), `maap`, `milan_dp_mclk`, `milan_dp_render`
    and `pp_shadow`.
  - **`milan_dp`'s `gptp` and `gptp-lat` receipts differ.** Both pass. One diagnostic line changed:
    `[#207] full-queue window: level 1, rp 0->0, wp 1->1` became `rp 1->1, wp 2->2`.
  - Every earlier log I have shows the first value, including local runs of the new 8-leg pieces 0/8 and 1/8.
    The cause is not established. Until it is, identical outputs are not shown for `milan_dp`.

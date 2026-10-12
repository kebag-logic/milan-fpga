# HANDOFF: lane 727, Verilator suite assignment by measured time

Role: executor [A604]. Issue: kebag-logic/milan-fpga#727.
Assignment: issue comment 6121794007. TAKEN: issue comment 6121909841.
REVIEW READY: issue comment 6122246247 (round 1), 6126250528 (round 2).
Branch `727-shard-balance` from dev `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
Internal review R626, external review R627 (per the assignment).

Status: ROUND 2 REVIEW READY at head
`61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3`, not pushed (the lane cannot
push); see "Round 2" at the end. Round 1 was REVIEW READY at head
`a57d384dc697249c2a69f80079b676875d4f7560`, pushed as PR #728 by the
manager. Acceptance 3's measured column waits for the PR's hosted run;
section 6 gives the command that reads it. Sections 1-7 are the round-1
record at `a57d384d` and are kept as they were, except where a Round 2
correction is attached.

Commits (one-line subjects, no body, no trailers):

| Commit | Subject |
|---|---|
| `111611fa9e366916f93ae8bb05f270648bb65dee` | Balance the Verilator workers by a measured per-suite duration table and hold each predicted worker to 60% of its timeout |
| `e2c4845ea3d071c397a2381ce550d45427341c9a` | Hold the specialized suites to their workers at any planted duration, so a dropped pin fails the selector self-test |
| `a57d384dc697249c2a69f80079b676875d4f7560` | Describe the measured-time Verilator split, its 60% gate and its refresh procedure in the CI workflow policy |

`git diff --numstat c6bd08c6 HEAD`: `scripts/suite_shards.py` +570/-78,
`docs/testing/CI_WORKFLOWS.md` +31/-19. No suite, testbench, RTL, firmware or workflow file
changed; `rtl.yml` is byte-identical to `c6bd08c6`.

## 1. Changes (file:line at the head)

`scripts/suite_shards.py`:

- `:2-48` module docstring: the measured-time rule, the dedicated and pinned
  workers, what `--selftest` holds the tree to, and the refresh procedure as
  plain shell (`:30-39`), with the measurement rule (`:41-48`). The block was
  extracted from the docstring and run verbatim (section 5): rc 0, and its
  `--measure` output equals the committed tables except `maap`, which is the
  #696 figure by design.
- `:74` `PINNED_SUITES = {"tsn_fuzz": 1, "chmap_capture": 3}`: the owners the
  workflow's ownership step proves (`rtl.yml:219-223`), pinned at the
  workflow's worker count.
- `:77` `HEADROOM_PERCENT = 60`.
- `:80-84` `HERE`, `ROOT`, `WORKFLOW`, `SUITE_ROOT`, `VERILATOR_JOB`: the tree
  the head arms read.
- `:90-156` `SUITE_SECONDS`: 62 entries, one per default suite (section 2).
- `:158` `WORKER_OVERHEAD_SECONDS = (83, 115, 80, 93, 80)`: per-worker job
  time outside the suite windows (section 2).
- `:187` `table_problems`: missing duration, duration naming no inventory
  suite, non-positive or non-integer duration.
- `:204` `balance`: dedicated suites on the last workers; at the workflow's
  worker count, overhead-seeded loads and the pins; the rest longest first to
  the least-loaded worker, ties by name and by lower worker. Refuses a table
  that disagrees with the inventory.
- `:242` `select_suites`: 0/1 returns the lexical inventory without a table
  (the serial local sweep and the cancellation fixture need none); a sharded
  split goes through `balance`.
- `:253` `verilator_job_limits`: reads `timeout-minutes` and `matrix.total`
  from the `verilator-shards:` job block of `rtl.yml` text, only at that
  job's indentation; anything but exactly one of each is refused. No YAML
  library, so it runs on the worker image and in the local preflight.
- `:281` `bound_seconds`, `:286` `headroom_problems`: the gate.
- `:307-405` `LogTimes`, `log_ticks`, `measure_log`, `measure_main`: the
  `--measure` reader (exact 100 ns ticks; a non-PASS result is refused; a log
  without its summary yields suites but no overhead).
- `:411`, `:449`, `:488` existing partition, dedicated and split arms, now
  fed synthetic durations (the hash-stability arm becomes "balanced owners
  unchanged" with the dedicated suite set aside).
- `:507` `measure_selftest`: the reader on a known log.
- `:541` `in_checkout`: the head arms run when this file is a tree's own
  `scripts/suite_shards.py`. `scripts/test_suite_cancellation.py:87-89` runs
  a renamed copy (`real_selector.py`) of this file's `--selftest` outside any
  checkout; that copy prints `skip head arms` and runs only the synthetic
  arms (case `t_renamed_copy` below). Every hosted and preflight invocation
  runs the in-tree file.
- `:559` `report`, `:565` `planted_selftest`: the planted defects (section 4).
- `:625` `head_selftest`: the head's own table, inventory and `rtl.yml`; the
  specialized owners and the pin-robustness arm (`:650-668`).
- `:697` `main`: `--measure LOG...`; a selection error (missing or stale
  duration) is a usage error, exit 2.

Removed from the self-test: the five-worker runtime landmarks
`pp_shadow: 1`, `mmcm_servo: 2`, `milan_dp_gm_steps: 3` (old `:183-194`).
They pinned the SHA-256 rule's own outputs, chosen for wall clock (#621); the
rule they pinned is the one #727 replaces, and the per-worker bound gate now
checks every worker's predicted time instead of three names. The specialized
owners `tsn_fuzz: 1`, `chmap_capture: 3` and `milan_dp: 4` (alone) are kept
and strengthened. This is a public decision for the reviewers, not a silent
change.

`docs/testing/CI_WORKFLOWS.md`:

- `:183-198`: the five-worker paragraph now says four workers split by
  measured hosted time (#727), and a new paragraph says what the selector
  records, how it places suites, what its self-test refuses (including the
  60% bound read from `rtl.yml`), where the refresh procedure is, and why
  (#696 on worker 1/5). "The hashed owners of every other suite are
  unchanged" (true only of the hash rule) is removed.
- `:200-212`: reflowed; "The shard selector pins those owners ..., its
  self-test proves them".
- `:324-326` (#621 history): "which the stable hash then gave worker 3/5";
  the false "`suite_shards.py` pins that owner among its five-worker
  landmarks" becomes "#727 replaced the hash with the measured-time split,
  which places the suite by its own recorded duration."

## 2. Duration table and its sources

Rule (assignment step 1): a suite's figure is the elapsed time between its
result line and the previous result line of the same worker; a worker's
first suite starts at that worker's `shard: I/5   selected suites: K` line,
so the setup before it is recorded separately as the worker's overhead.
Figures are rounded up to whole seconds. Log line numbers are those of
`gh run view <run> -R kebag-logic/milan-fpga --job <job> --log`.

Downloaded logs (scratch, not in the tree or here):

| Log | Bytes | sha256 |
|---|---:|---|
| run 38217650945 job 114706225351 (0/5) | 36230 | `d1590923260f65abee4d06013c36c3a09c2ac8fe986e016c22069bd5fdab8657` |
| run 38217650945 job 114706225444 (1/5) | 59459 | `00b29e70d370ca3073a02aaa69ce568b669ce4ba53c2d8e8bef4944332f1e5d6` |
| run 38217650945 job 114706225397 (2/5) | 36394 | `41ac4660e7480a8a92cda00ecf35c1e2a5c23dd129a00955622938c40d0445d1` |
| run 38217650945 job 114706225439 (3/5) | 48131 | `8438cbdff3827036f02c69f32e493c1a65f94b43abebbdda396f653c1f906a0a` |
| run 38217650945 job 114706225398 (4/5) | 34529 | `f9408efc3ff2539bd7685b8eeccc9801bedf3c3a4bf36202a0b72914b7b6556e` |
| run 38208503834 job 114677344710 (1/5, #696 head `26e2748f`) | 60371 | `3c2c7d4679826487921af10223d0e8a3e21580a9170452a2992c69799cd0df5d` |

Run 38217650945: `schedule` on dev, head `c6bd08c6`, all five Verilator
workers `success`. Run 38208503834: PR #706 head `26e2748f`, worker 1/5
cancelled at 120 min after 20 PASS lines; its `maap` window is complete.

Two figures differ from the issue's prose, both by the rule above:

- `milan_dp`: the issue says 2,868 s. The rule gives 2796.168 s (`shard:`
  line 236 to result line 237 of job 114706225398). The issue's figure runs
  from the sweep step's start (line 227, 07:26:13.772) and so includes the
  71.115 s preflight self-tests, which the rule puts in worker 4's overhead.
- `maap`: the issue says about 1,380 s. The rule gives 1374.177 s (line 452
  to line 453 of job 114677344710), recorded as 1375 s. With 1380 s the
  balance re-places some suites under 100 s and the busiest worker is 4207 s,
  still under 4320 s.

Sum of the table: 19243 s (320.7 min) with #696's `maap`; 18053 s with
dev's. Sum of overheads: 451 s.

### Per-suite figures

| Suite | Table s | Window s | Run | Job | Worker | From line | Result line (UTC) |
|---|---:|---:|---|---|---|---:|---|
| `aaf` | 73 | 72.940 | 38217650945 | 114706225397 | 2/5 | 248 | 249 (07:28:37.148) |
| `aaf_audio_loop` | 6 | 5.322 | 38217650945 | 114706225397 | 2/5 | 249 | 250 (07:28:42.470) |
| `aaf_clock_meter` | 1055 | 1054.370 | 38217650945 | 114706225397 | 2/5 | 250 | 251 (07:46:16.840) |
| `aaf_latency_tap_bank` | 16 | 15.366 | 38217650945 | 114706225351 | 0/5 | 247 | 248 (07:27:42.731) |
| `aaf_latency_taps` | 6 | 5.416 | 38217650945 | 114706225444 | 1/5 | 424 | 425 (07:28:04.743) |
| `adp_tx` | 12 | 11.820 | 38217650945 | 114706225439 | 3/5 | 358 | 359 (07:27:49.865) |
| `aes3` | 6 | 5.715 | 38217650945 | 114706225397 | 2/5 | 251 | 252 (07:46:22.556) |
| `avtp_parser` | 27 | 26.436 | 38217650945 | 114706225439 | 3/5 | 359 | 360 (07:28:16.301) |
| `avtp_rxmon` | 73 | 72.941 | 38217650945 | 114706225444 | 1/5 | 425 | 426 (07:29:17.684) |
| `avtp_stream` | 11 | 10.755 | 38217650945 | 114706225351 | 0/5 | 248 | 249 (07:27:53.486) |
| `capture_coherence` | 1737 | 1736.905 | 38217650945 | 114706225444 | 1/5 | 426 | 427 (07:58:14.590) |
| `cbs` | 6 | 5.514 | 38217650945 | 114706225444 | 1/5 | 427 | 428 (07:58:20.104) |
| `cdc` | 6 | 5.322 | 38217650945 | 114706225444 | 1/5 | 428 | 429 (07:58:25.426) |
| `chmap_capture` | 168 | 167.887 | 38217650945 | 114706225439 | 3/5 | 360 | 361 (07:31:04.188) |
| `chmap_render` | 6 | 5.488 | 38217650945 | 114706225397 | 2/5 | 252 | 253 (07:46:28.043) |
| `classifier` | 6 | 5.350 | 38217650945 | 114706225439 | 3/5 | 361 | 362 (07:31:09.538) |
| `clkvalid` | 16 | 15.608 | 38217650945 | 114706225444 | 1/5 | 429 | 430 (07:58:41.033) |
| `cls` | 6 | 5.323 | 38217650945 | 114706225351 | 0/5 | 249 | 250 (07:27:58.809) |
| `controller_rate` | 9 | 8.246 | 38217650945 | 114706225444 | 1/5 | 430 | 431 (07:58:49.279) |
| `crf_rx` | 832 | 831.367 | 38217650945 | 114706225444 | 1/5 | 431 | 432 (08:12:40.646) |
| `crf_tx` | 6 | 5.759 | 38217650945 | 114706225397 | 2/5 | 253 | 254 (07:46:33.802) |
| `csr` | 306 | 305.318 | 38217650945 | 114706225439 | 3/5 | 362 | 363 (07:36:14.856) |
| `datapath` | 6 | 5.716 | 38217650945 | 114706225444 | 1/5 | 432 | 433 (08:12:46.362) |
| `eth_tx_reset` | 6 | 5.145 | 38217650945 | 114706225351 | 0/5 | 250 | 251 (07:28:03.953) |
| `follow_ring` | 1158 | 1157.831 | 38217650945 | 114706225351 | 0/5 | 251 | 252 (07:47:21.785) |
| `fw_service_budget` | 2 | 1.756 | 38217650945 | 114706225444 | 1/5 | 433 | 434 (08:12:48.118) |
| `gptp_plane` | 784 | 783.942 | 38217650945 | 114706225444 | 1/5 | 434 | 435 (08:25:52.060) |
| `gptp_shadow` | 393 | 392.235 | 38217650945 | 114706225444 | 1/5 | 435 | 436 (08:32:24.295) |
| `gptp_txts` | 72 | 71.521 | 38217650945 | 114706225351 | 0/5 | 252 | 253 (07:48:33.306) |
| `i2spb` | 6 | 5.495 | 38217650945 | 114706225351 | 0/5 | 253 | 254 (07:48:38.801) |
| `ifg` | 6 | 5.337 | 38217650945 | 114706225351 | 0/5 | 254 | 255 (07:48:44.138) |
| `lat_history_ring` | 6 | 5.363 | 38217650945 | 114706225444 | 1/5 | 436 | 437 (08:32:29.658) |
| `link_guard` | 7 | 6.869 | 38217650945 | 114706225439 | 3/5 | 363 | 364 (07:36:21.725) |
| `maap` (dev, superseded) | - | 184.129 | 38217650945 | 114706225444 | 1/5 | 437 | 438 (08:35:33.787) |
| `maap` (#696) | 1375 | 1374.177 | 38208503834 | 114677344710 | 1/5 | 452 | 453 (07:03:51.234) |
| `mac_rmon` | 11 | 10.438 | 38217650945 | 114706225444 | 1/5 | 438 | 439 (08:35:44.225) |
| `mbx` | 82 | 81.576 | 38217650945 | 114706225397 | 2/5 | 254 | 255 (07:47:55.378) |
| `media_grid_align` | 255 | 254.656 | 38217650945 | 114706225439 | 3/5 | 364 | 365 (07:40:36.381) |
| `media_nco` | 17 | 16.132 | 38217650945 | 114706225444 | 1/5 | 439 | 440 (08:36:00.357) |
| `milan_dp` | 2797 | 2796.168 | 38217650945 | 114706225398 | 4/5 | 236 | 237 (08:14:01.055) |
| `milan_dp_gm_steps` | 926 | 925.356 | 38217650945 | 114706225439 | 3/5 | 365 | 366 (07:56:01.737) |
| `milan_dp_mclk` | 2038 | 2037.741 | 38217650945 | 114706225397 | 2/5 | 255 | 256 (08:21:53.118) |
| `milan_dp_render` | 1264 | 1263.445 | 38217650945 | 114706225351 | 0/5 | 255 | 256 (08:09:47.582) |
| `mmcm_servo` | 1145 | 1144.192 | 38217650945 | 114706225397 | 2/5 | 256 | 257 (08:40:57.311) |
| `mmcm_servo_autorepair` | 6 | 5.792 | 38217650945 | 114706225444 | 1/5 | 440 | 441 (08:36:06.149) |
| `nvm_backend` | 34 | 33.748 | 38217650945 | 114706225439 | 3/5 | 366 | 367 (07:56:35.485) |
| `nvm_cosim` | 775 | 774.463 | 38217650945 | 114706225444 | 1/5 | 441 | 442 (08:49:00.612) |
| `pair_fill` | 6 | 5.309 | 38217650945 | 114706225444 | 1/5 | 442 | 443 (08:49:05.920) |
| `pcmlpf` | 6 | 5.367 | 38217650945 | 114706225444 | 1/5 | 443 | 444 (08:49:11.288) |
| `pp_shadow` | 1251 | 1250.364 | 38217650945 | 114706225444 | 1/5 | 444 | 445 (09:10:01.652) |
| `ptp` | 26 | 25.032 | 38217650945 | 114706225351 | 0/5 | 256 | 257 (08:10:12.614) |
| `ptp_sync` | 11 | 10.637 | 38217650945 | 114706225397 | 2/5 | 257 | 258 (08:41:07.947) |
| `ptp_ts` | 127 | 126.229 | 38217650945 | 114706225397 | 2/5 | 258 | 259 (08:43:14.176) |
| `queues` | 6 | 5.747 | 38217650945 | 114706225351 | 0/5 | 257 | 258 (08:10:18.361) |
| `render_setpoint` | 93 | 92.188 | 38217650945 | 114706225397 | 2/5 | 259 | 260 (08:44:46.365) |
| `rx_filter` | 18 | 17.518 | 38217650945 | 114706225351 | 0/5 | 258 | 259 (08:10:35.880) |
| `shaper_core` | 6 | 5.985 | 38217650945 | 114706225397 | 2/5 | 260 | 261 (08:44:52.349) |
| `tcam` | 27 | 26.137 | 38217650945 | 114706225439 | 3/5 | 367 | 368 (07:57:01.622) |
| `tcam_csr` | 6 | 5.453 | 38217650945 | 114706225444 | 1/5 | 445 | 446 (09:10:07.104) |
| `tdm` | 6 | 5.633 | 38217650945 | 114706225439 | 3/5 | 368 | 369 (07:57:07.256) |
| `tdm_render` | 6 | 5.213 | 38217650945 | 114706225439 | 3/5 | 369 | 370 (07:57:12.468) |
| `tkdiag` | 28 | 27.500 | 38217650945 | 114706225439 | 3/5 | 370 | 371 (07:57:39.969) |
| `tsn_fuzz` | 60 | 59.947 | 38217650945 | 114706225444 | 1/5 | 446 | 447 (09:11:07.051) |

### Worker setup and overhead (dev run 38217650945)

| Worker | Job | First log line (UTC) | `shard:` line | Setup s | Last result line | Last log line | Tail s | Overhead s (table) | Suite windows s | Log span s | API wall clock s |
|---|---|---|---|---:|---|---|---:|---:|---:|---:|---:|
| 0/5 | 114706225351 | 1 (07:26:06.520) | 247 (07:27:27.365) | 80.845 | 259 | 326 (08:10:37.224) | 1.344 | 83 | 2588.515 | 2670.704 | 2673 |
| 1/5 | 114706225444 | 1 (07:26:07.443) | 424 (07:27:59.327) | 111.883 | 447 | 515 (09:11:09.308) | 2.257 | 115 | 6187.724 | 6301.865 | 6306 |
| 2/5 | 114706225397 | 1 (07:26:06.651) | 248 (07:27:24.208) | 77.557 | 261 | 328 (08:44:53.841) | 1.492 | 80 | 4648.141 | 4727.190 | 4729 |
| 3/5 | 114706225439 | 1 (07:26:07.528) | 358 (07:27:38.045) | 90.517 | 371 | 442 (07:57:42.131) | 2.163 | 93 | 1801.924 | 1894.604 | 1898 |
| 4/5 | 114706225398 | 1 (07:26:06.986) | 236 (07:27:24.886) | 77.900 | 237 | 304 (08:14:02.933) | 1.878 | 80 | 2796.168 | 2875.947 | 2878 |

### Old (SHA-256 digest) and new (measured-time) assignment

| Worker | Old suites (c6bd08c6) | Old predicted, maap 185 s | Old predicted, maap 1375 s | Old measured (API, run 38217650945) | New suites | New predicted | Bound |
|---|---|---:|---:|---:|---|---:|---:|
| 0/5 | 12: `milan_dp_render` 1264, `follow_ring` 1158 + 10 under 100 s (173 s) | 2678 s (44.6 min) | 2678 s (44.6 min) | 2673 s (44.5 min) | 15: `capture_coherence` 1737, `mmcm_servo` 1145, `gptp_plane` 784, `media_grid_align` 255 + 11 under 100 s (200 s) | 4204 s (70.1 min) | 4320 s (72.0 min) |
| 1/5 | 23: `capture_coherence` 1737, `maap` 1375, `pp_shadow` 1251, `crf_rx` 832, `gptp_plane` 784, `nvm_cosim` 775, `gptp_shadow` 393 + 16 under 100 s (242 s) | 6314 s (105.2 min) | 7504 s (125.1 min) | 6306 s (105.1 min) | 16: `maap` 1375, `follow_ring` 1158, `milan_dp_gm_steps` 926, `csr` 306, `ptp_ts` 127 + 11 under 100 s (198 s) | 4205 s (70.1 min) | 4320 s (72.0 min) |
| 2/5 | 13: `milan_dp_mclk` 2038, `mmcm_servo` 1145, `aaf_clock_meter` 1055, `ptp_ts` 127 + 9 under 100 s (289 s) | 4734 s (78.9 min) | 4734 s (78.9 min) | 4729 s (78.8 min) | 14: `milan_dp_mclk` 2038, `aaf_clock_meter` 1055, `nvm_cosim` 775 + 11 under 100 s (255 s) | 4203 s (70.0 min) | 4320 s (72.0 min) |
| 3/5 | 13: `milan_dp_gm_steps` 926, `csr` 306, `media_grid_align` 255, `chmap_capture` 168 + 9 under 100 s (153 s) | 1901 s (31.7 min) | 1901 s (31.7 min) | 1898 s (31.6 min) | 16: `milan_dp_render` 1264, `pp_shadow` 1251, `crf_rx` 832, `gptp_shadow` 393, `chmap_capture` 168 + 11 under 100 s (204 s) | 4205 s (70.1 min) | 4320 s (72.0 min) |
| 4/5 | 1: `milan_dp` 2797 | 2877 s (48.0 min) | 2877 s (48.0 min) | 2878 s (48.0 min) | 1: `milan_dp` 2797 | 2877 s (48.0 min) | 4320 s (72.0 min) |

### New per-worker suite lists (run order is lexical)

- 0/5 (15): `aaf` `avtp_parser` `capture_coherence` `cdc` `crf_tx` `gptp_plane` `ifg` `link_guard` `mac_rmon` `media_grid_align` `mmcm_servo` `nvm_backend` `pcmlpf` `rx_filter` `tdm`
- 1/5 (16): `aaf_audio_loop` `aaf_latency_tap_bank` `adp_tx` `aes3` `classifier` `csr` `eth_tx_reset` `follow_ring` `fw_service_budget` `gptp_txts` `maap` `milan_dp_gm_steps` `mmcm_servo_autorepair` `ptp_ts` `shaper_core` `tsn_fuzz`
- 2/5 (14): `aaf_clock_meter` `aaf_latency_taps` `avtp_rxmon` `cbs` `clkvalid` `cls` `i2spb` `milan_dp_mclk` `nvm_cosim` `pair_fill` `ptp` `ptp_sync` `render_setpoint` `tcam_csr`
- 3/5 (16): `avtp_stream` `chmap_capture` `chmap_render` `controller_rate` `crf_rx` `datapath` `gptp_shadow` `lat_history_ring` `mbx` `media_nco` `milan_dp_render` `pp_shadow` `queues` `tcam` `tdm_render` `tkdiag`
- 4/5 (1): `milan_dp`

### Old per-worker suite lists at c6bd08c6

- 0/5 (12): `aaf_latency_tap_bank` `avtp_stream` `cls` `eth_tx_reset` `follow_ring` `gptp_txts` `i2spb` `ifg` `milan_dp_render` `ptp` `queues` `rx_filter`
- 1/5 (23): `aaf_latency_taps` `avtp_rxmon` `capture_coherence` `cbs` `cdc` `clkvalid` `controller_rate` `crf_rx` `datapath` `fw_service_budget` `gptp_plane` `gptp_shadow` `lat_history_ring` `maap` `mac_rmon` `media_nco` `mmcm_servo_autorepair` `nvm_cosim` `pair_fill` `pcmlpf` `pp_shadow` `tcam_csr` `tsn_fuzz`
- 2/5 (13): `aaf` `aaf_audio_loop` `aaf_clock_meter` `aes3` `chmap_render` `crf_tx` `mbx` `milan_dp_mclk` `mmcm_servo` `ptp_sync` `ptp_ts` `render_setpoint` `shaper_core`
- 3/5 (13): `adp_tx` `avtp_parser` `chmap_capture` `classifier` `csr` `link_guard` `media_grid_align` `milan_dp_gm_steps` `nvm_backend` `tcam` `tdm` `tdm_render` `tkdiag`
- 4/5 (1): `milan_dp`

The model reproduces the old split's measured job times within 8 s
(in-sample: the same run supplies the figures): predicted 2678 / 6314 / 4734
/ 1901 / 2877 s against API wall clock 2673 / 6306 / 4729 / 1898 / 2878 s.
With #696's `maap`, the old worker 1/5 predicts 7504 s (125.1 min), past its
120-minute timeout, as run 38208503834 observed.

## 3. Old and new assignment per worker

See the assignment table above. Summary:

| Worker | Old (hash) predicted with #696 | New predicted | New minus bound |
|---|---:|---:|---:|
| 0/5 | 44.6 min | 70.1 min (4204 s) | -116 s |
| 1/5 | 125.1 min | 70.1 min (4205 s) | -115 s |
| 2/5 | 78.9 min | 70.0 min (4203 s) | -117 s |
| 3/5 | 31.7 min | 70.1 min (4205 s) | -115 s |
| 4/5 | 48.0 min | 48.0 min (2877 s) | -1443 s |

Bound: 60% of `timeout-minutes: 120` (`rtl.yml:152`) = 4320 s = 72.0 min.
Five workers meet it, so the STOP condition does not apply and `rtl.yml` is
unchanged. `milan_dp` stays alone on 4/5; `tsn_fuzz` stays on 1/5 and
`chmap_capture` on 3/5, so the ownership step's arms (`rtl.yml:219-223`, pinned
by `scripts/ci_events.py` `CANONICAL_OWNERSHIP_SCRIPT`) hold unchanged.

## 4. Gates, planted controls and mutants

Each case below has its control arm in `--selftest`, which prints `[ok]` at
the head (or `ok` for the head's own clean arms). The mutants are applied to
a structure-only copy of the head (the selector, `rtl.yml` and one empty
Makefile per suite directory) by `mutants_727.py` in this directory; its full
output is `mutants-final.txt` (sha256
`e3390cc8cacefb7abbab21bdcd2e1a2b3475a1f8d8315b4a3b588102d407c68e`, 4476
bytes, scratch prefix replaced by `<scratch>`). The harness sha256 is
`1be99e7aca775ea7970d9fef506996ebf1f3b73c0398e6fcadcab05358ebe899`. The
unmodified copy (`control`) passes: rc 0, every arm `ok`/`[ok]`.

Command (CPython 3.12.3, from the lane root):

```sh
python3 -I mutants_727.py "$PWD" <empty scratch directory>
```

| Case (assignment step 3) | Control at the head | Mutant | Result under mutant |
|---|---|---|---|
| a suite has no duration | `[ok] an inventory suite with no recorded duration is refused`; `[ok] a sharded selection refuses it too` (`:571-579`); head: 62 suites, 62 durations | `m_unmeasured_free`: the missing-duration check deleted and a missing suite costs 0 s in `balance` | rc 1: both arms `ESCAPED` |
| the table names a suite not in the inventory | `[ok] a recorded duration with no inventory suite is refused` (`:580-583`) | `m_stale_ignored`: the stale-entry check deleted | rc 1: `ESCAPED` |
| a predicted worker exceeds 60% of `timeout-minutes` read from `rtl.yml` | `[ok] rtl.yml timeout-minutes 116 (bound 4176 s) is refused for a 4205 s worker`; `[ok] and 117 minutes is not` (`:585-596`); head: five `ok head worker` lines, bound 4320 s | `m_timeout_mirrored`: `timeout, workers = 120, 5` instead of reading `rtl.yml` | rc 1: the 116-minute arm `ESCAPED` |
| | | `m_block_unbounded`: the job block runs into later jobs | rc 1: `FAIL head: ... has 5 timeout-minutes values, not one` |
| a planted heavy duration pushes a worker over | `[ok] milan_dp at 4240 s puts worker 4 exactly at the bound and passes`; `[ok] milan_dp at 4241 s puts it over and is refused`; `[ok] milan_dp_mclk grown by 464 s to 2502 s puts a balanced worker over and is refused` (`:598-621`) | `m_overhead_dropped`: overhead left out of the prediction | rc 1: the 4241 s arm `ESCAPED` |
| | | `m_mean_only`: only the mean worker held to the bound | rc 1: the 116-minute, 4241 s and grown arms `ESCAPED` |
| | | `m_at_bound_refused`: `>` became `>=` | rc 1: the at-bound control `ESCAPED` |

The grown-suite arm is a pigeonhole: 464 s is one more than the four balanced
workers' spare time together, so some worker must exceed the bound wherever
the rule places the suite.

Further mutants and tree-level plantings (same harness):

| Case | Change | Result |
|---|---|---|
| `m_pin_dropped` | `chmap_capture` unpinned | rc 1: `held at any planted duration=False`. At the head the balance alone happens to put it on 3/5; the pin-robustness arm plants each specialized suite at 1 s and at the heaviest + 1 s and requires its worker to hold (added in `e2c4845e` after this mutant first survived). |
| `m_tsn_pin_dropped` | `tsn_fuzz` unpinned | rc 1: same arm FAIL |
| `m_tsn_pin_moved` | `tsn_fuzz` pinned to 2 | rc 1: `specialized owners {'tsn_fuzz': 2, ...}` FAIL |
| `m_measure_from_job_start` | `--measure` starts the first suite at the job | rc 1: `log windows {'alpha': 71, ...}` FAIL |
| `t_unmeasured_suite` | tree gains `tb/verilator/new_unmeasured/Makefile` | rc 1: `FAIL head: new_unmeasured: inventory suite with no recorded duration` |
| `t_suite_removed` | `pcmlpf` loses its Makefile | rc 1: `FAIL head: pcmlpf: SUITE_SECONDS names a suite that is not in the inventory` |
| `t_heavy_entry` | real entry `gptp_plane` 784 s to 1284 s | rc 1: workers 0-3 predicted 4327-4333 s, FAIL |
| `t_timeout_lowered` | `rtl.yml` Verilator job `timeout-minutes: 116` | rc 1: workers 0-3 over 4176 s, FAIL |
| `t_worker_count` | `rtl.yml` matrix grows to six workers | rc 1: `WORKER_OVERHEAD_SECONDS describes 5 workers; rtl.yml runs 6` |
| `t_workflow_missing` | no `rtl.yml` | rc 1: `FAIL head: [Errno 2] ...` (fails closed) |
| `t_renamed_copy` | the selector renamed `real_selector.py` outside `scripts/` | rc 0: `skip head arms` (the cancellation fixture's case; see section 7) |

Run-time refusal (the sharded selection itself, not the self-test), on the
planted inventories above:

- `python3 scripts/suite_shards.py --suite-root <t_unmeasured_suite>/tb/verilator --shard 1/5`:
  rc 2, `error: new_unmeasured: inventory suite with no recorded duration in SUITE_SECONDS ...`;
  the same root with `--shard 0/1`: rc 0, 63 suites (serial needs no table).
- `... --suite-root <t_suite_removed>/tb/verilator --shard 4/5`: rc 2,
  `error: pcmlpf: SUITE_SECONDS names a suite that is not in the inventory`.

## 5. Gate runs (head `a57d384d`, all rc 0)

Interpreters: CPython 3.12.3 (the hosted version, a standalone build) and
the host's CPython 3.14.7. `ci_events.py` needs PyYAML, so it ran in a
scratch 3.12.3 virtual environment with PyYAML 6.0.3. The Markdown gates ran
with the pinned renderer environment (`tools/markdown/requirements.txt`).

| Gate | Interpreter | rc |
|---|---|---:|
| `python3 scripts/suite_shards.py --selftest` | 3.12.3 and 3.14.7 | 0 |
| `python3 scripts/ci_events.py --check` (1821 items) | 3.12.3 + PyYAML | 0 |
| `python3 scripts/ci_events.py --selftest` (1821 items, 2530 arms) | 3.12.3 + PyYAML | 0 |
| `python3 scripts/test_suite_cancellation.py` | 3.14.7 | 0 |
| `python3 scripts/check_py_idiom.py` | 3.12.3 | 0 |
| `python3 scripts/measure_naming.py --check` | 3.12.3 | 0 |
| `python3 scripts/measure_fail_fast.py --check` | 3.12.3 | 0 |
| `python3 scripts/check_hygiene.py --check` | 3.12.3 | 0 |
| `python3 scripts/check_todo_ownership.py` | 3.12.3 | 0 |
| `python3 scripts/measure_test_evidence.py --check` | 3.12.3 | 0 |
| `python3 scripts/suite_tally.py --selftest` | 3.12.3 | 0 |
| `python3 scripts/docs_check.py` | 3.14.7 | 0 |
| `python3 scripts/check_doc_style.py` | 3.14.7 | 0 |
| `python3 scripts/gen_toc.py --check` | renderer env | 0 |
| `python3 scripts/gen_toc.py --verify-anchors` | renderer env | 0 |
| `python3 scripts/check_em_dash.py --base c6bd08c6` (31 added lines, 339/339 arms) | renderer env | 0 |
| `python3 scripts/check_em_dash.py --selftest` | renderer env | 0 |
| `python3 scripts/check_doc_paths.py` | 3.14.7 | 0 |
| `python3 scripts/check_baremetal_only.py --check` | 3.14.7 | 0 |
| `python3 scripts/check_archive.py` | 3.14.7 | 0 |
| `scripts/run_all_suites.sh --shard I/5 --list`, I = 0..4 | system | 0 each (15, 16, 14, 16, 1 suites) |
| `scripts/run_all_suites.sh --list` | system | 0 (62 suites, identical to `c6bd08c6`'s list) |
| union of the five lists equals the `--list` inventory | `cmp` | 0 (62 = 62) |
| no suite listed twice | `cmp` against `sort -u` | 0 (62 listed, 62 unique) |
| shard 4/5 is exactly `milan_dp`; `tsn_fuzz` in 1/5; `chmap_capture` in 3/5 | `test`, `grep -Fx` | 0 |
| `git diff --check c6bd08c6 HEAD` and `git diff --check` | | 0 |
| docstring refresh block run verbatim (`TMPDIR` in scratch) | 3.14.7 | 0; tables equal the committed ones except `maap` (185 vs 1375, by design) |
| `mutants_727.py` | 3.12.3 | 0; 19 cases as in section 4 |

Not run, and why:

- The Verilator suites themselves: the assignment measures from hosted logs.
  CONTRIBUTING section 2 still requires the local serial sweep
  (`scripts/run_all_suites.sh "$suite_logs"`) and `syn/yosys/run.sh` to be
  recorded on the PR before it is marked validated. Both remain owed and
  were not run here, by instruction. The serial selection (`--shard 0/1`) is
  byte-identical to `c6bd08c6`'s, and the sweep's preflight runs this
  selector's `--selftest`, which passes.
- `scripts/act_ci.py --pr <N>`: there is no PR and the lane cannot push. It
  is the first step after the push (AGENTS.md section 5).
- `test_suite_cancellation.py` under the 3.12.3 standalone build fails at
  import, identically at the base `c6bd08c6` and at the head:
  `owned_process.Unsupported: unsupported process facilities: os.pidfd_open,
  signal.pidfd_send_signal`. That build lacks those calls, which is an
  interpreter limitation and has nothing to do with this change. It passes
  on 3.14.7, and the hosted runner's system 3.12.3 has them.

Tree state after the gates: `git status --short` is empty. The only untracked
artifact is the gitignored `scripts/__pycache__/` (`.gitignore:28`) that the
repository's own gate scripts write on import.

## 6. Acceptance status

1. **Headroom by construction: met.** `SUITE_SECONDS` (`:90-156`) and
   `WORKER_OVERHEAD_SECONDS` (`:158`) are measured from hosted logs (section 2)
   and drive the assignment. The gate fails closed when an inventory suite has
   no duration (`t_unmeasured_suite`, `m_unmeasured_free`), when a worker is
   predicted above 60% of `timeout-minutes` read from `rtl.yml` and not
   mirrored (`t_timeout_lowered`, `m_timeout_mirrored`, `t_heavy_entry`), and
   when the table and the inventory disagree (`t_suite_removed`,
   `m_stale_ignored`). The prediction includes #696's `maap` (1375 s).
2. **Existing guarantees: met.** Deterministic and disjoint: split arms at
   1, 2, 4, 5, 7 and 23 workers, plus the five `--list` runs with the union
   check. Inventory fail-closed: unchanged `sweep_suites`, plus the
   selection's own refusal. `milan_dp` dedicated: dedicated arms and the head
   arm, and `--shard 4/5 --list` prints `milan_dp` alone. Specialized owners:
   pinned, proven by the head arm and the pin-robustness arm, and the
   workflow's step is unchanged. Five workers, `rtl.yml` unchanged.
3. **Measured at the head: pending the push.** Predicted per worker:
   4204 / 4205 / 4203 / 4205 / 2877 s (70.1 / 70.1 / 70.0 / 70.1 / 48.0 min).
   Once the PR is marked ready and its rtl-full run completes, these commands
   read the measured column (job wall clock, started to completed) and the
   per-suite windows:

   ```sh
   gh run list -R kebag-logic/milan-fpga --workflow rtl.yml --branch 727-shard-balance --json databaseId,headSha,event,status,conclusion --limit 5
   run=<databaseId of the pull_request run at the PR head>
   gh run view "$run" -R kebag-logic/milan-fpga --json headSha,jobs --jq '.headSha, (.jobs[] | select(.name | startswith("Verilator shard")) | "\(.name)\t\(.conclusion)\t\((.completedAt | fromdate) - (.startedAt | fromdate)) s")'
   ```

   The second command, run on dev run 38217650945, printed 2673 / 6306 /
   4729 / 1898 / 2878 s, the API column in section 2. The docstring's
   refresh block, with `run=` set to the PR run, gives the per-suite figures.
   Acceptance 3 requires every worker at most 4320 s.
4. **Refresh procedure: met.** Module docstring `:27-48`, plain shell,
   executed verbatim (section 5).

## 7. Open items

- **Runner variance against acceptance 3.** The table is one sample (one dev
  run plus one PR window), as the assignment specifies. The balanced workers
  have 115-117 s spare against 4320 s, which is 2.7% of the bound. Between
  the two runs measured here, worker 1/5's shared suites above 60 s moved by
  up to 1.8% (`gptp_plane` 783.9 vs 769.8 s, `capture_coherence` 1736.9 vs
  1714.7 s). `docs/testing/CI_WORKFLOWS.md`
  records a much wider runner-class spread for `milan_dp` (1296-2460 s in
  one day). So a slow runner class on the PR run can put a worker above
  72 min, while the run stays far below the 120-minute timeout. If that
  happens, the remedy is a refresh from that run, not a rule change.
- **`rtl.yml:136-140` comment.** It still says "four hashed workers" and
  "Specialized setup is installed only on the stable shard". Acceptance 2
  freezes `rtl.yml` when five workers suffice, so the comment is not
  changed; it has no behavioural effect. A follow-up, or a decision to allow
  a comment-only edit, would fix it.
- **Renamed-copy skip.** The head arms skip when the file is not a tree's
  own `scripts/suite_shards.py`, because `test_suite_cancellation.py` runs a
  renamed copy outside any checkout, where no inventory or `rtl.yml` exists
  and the fixture's `alpha`/`omega` suites have no durations. In a checkout,
  a missing `rtl.yml` or suite root fails closed (`t_workflow_missing`).
- **Overhead assumes warm caches.** The overheads come from a run with
  Verilator, Yosys and tsn-gen cache hits. A cache miss adds a build to that
  worker's setup; the 40% left below the timeout absorbs it, but the 72-minute
  measurement would not.
  **Round 2 correction (R627-1-R2):** tsn-gen has no cache. `rtl.yml:278-292`
  clones and builds it on worker 1 in every run, so its build is already in
  worker 1's measured 115 s overhead. Corrected wording: "Overheads assume
  warm Verilator and Yosys caches; worker 1's overhead includes the tsn-gen
  build." No figure or prediction changes.
- **Removed runtime landmarks** (`pp_shadow`, `mmcm_servo`,
  `milan_dp_gm_steps`): see section 1. Reviewers may want to confirm that
  decision.
- **`maap` on refresh.** Until #696 merges, a refresh from a dev run must
  keep `"maap": 1375`; the docstring says so (`:46-48`).
- **New suites need a duration first.** A new suite directory makes both
  sharded selection and `--selftest` refuse, so the local serial sweep's
  preflight also aborts until a figure is recorded. That is what acceptance 1
  asks for. The first figure can come from a local run and be refreshed from
  the first hosted run.

## Round 2

Assignment: issue comment 6126048117 ([A10] Round 2). Reviews: PR #728
comments 6125953320 (R626-1, NEGATIVE) and 6126041660 (R627-1, NEGATIVE).
Both are NEGATIVE on one MINOR finding (F1, Tests). Base for this round:
`a57d384dc697249c2a69f80079b676875d4f7560`. New commits only: no rebase, no
amend. Nothing was pushed.

Status: REVIEW READY at head `61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3`,
posted as issue comment 6126250528 (its text is `r2-review-ready.md` in
this directory).

| Commit | Subject |
|---|---|
| `1d5f1c88ef50431ab5fcd2adb78b707a895d9321` | Check the applied bound against 36 s per timeout-minute without the bound formula, so a loosened 60% fails the selector self-test |
| `78cee0d67c9233883f49ac7a7e3e5db8b3818022` | Plant a zero duration and one more rtl.yml worker in the selector self-test, so weakening either refusal fails it |
| `61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3` | Name maap's pull-request run as the one exception to the dev run that supplies the selector's figures in the CI workflow policy |

`git diff --numstat a57d384d HEAD`: `scripts/suite_shards.py` +32/-8,
`docs/testing/CI_WORKFLOWS.md` +5/-3. Against the base `c6bd08c6` the lane is
now +594/-78 and +33/-19. `git diff --quiet c6bd08c6 HEAD -- .github hdl tb
firmware third_party` is rc 0, so `rtl.yml` is still byte-identical.

### R2.1 F1: an arm that fixes the 60% figure itself

Finding: R626-1 F1, retained as R627-1-F1. Assignment item 1 asks for an
arm that computes the expected bound without `bound_seconds` or
`HEADROOM_PERCENT`, as `timeout-minutes` x 36 s (4320 s at 120). The arm
must fail when the applied bound differs.

Change in `scripts/suite_shards.py`, commit `1d5f1c88`:

- `:596-599`: the existing 116/117-minute arm now keeps the bound that each
  of its two planted `rtl.yml` texts applied (`over_bound`, `under_bound`).
  Before this change it discarded them.
- `:604-611`: the new arm. `applied` maps each timeout to the bound that
  `headroom_problems` returned for it:
  - `rtl.yml`'s own `timeout-minutes` (120) to the head's bound;
  - the planted 116 to `over_bound`;
  - the planted 117 to `under_bound`.

  `expected` maps each of those minutes to `minutes * 36`. The arm reports
  `[ok]` only when the two maps are equal. Neither `bound_seconds` nor
  `HEADROOM_PERCENT` appears in `expected`. `bound_seconds` still picks
  which minutes to plant, through `tight`, but it does not supply the
  figure any of them is checked against.
- The head's timeout is still read through `verilator_job_limits`, the
  authoritative input that R627-1 asked to keep. The planted 116 and 117
  come from the planting, not from that reader, so a reader that mirrors 120
  fails this arm as well.

At the head the arm prints:
`[ok]    the bound applied at each timeout-minutes is 36 s a minute (60%): {116: 4176, 117: 4212, 120: 4320}, expected {116: 4176, 117: 4212, 120: 4320}`.

Verification uses R626-1's `mutate.py` (sha256
`571bd0aabb766efeec0f0274909d181e81ed6f25b609b76a5c9c0c2fffcfc031`, equal to
its `MANIFEST.sha256`). It was fetched from
`review-evidence/727-r1/reviews/R626-1/scripts/mutate.py` on
`727-review-evidence` at `def6801a` and run unmodified with CPython 3.12.3:

```sh
python3 -I mutate.py <lane checkout> <empty scratch directory>
```

| Case | At `a57d384d` (baseline) | At `61296ea1` | Failing arms at `61296ea1` |
|---|---|---|---|
| `headroom-75-percent` | rc 0, `selftest: PASS` | rc 1, `selftest: 1 FAILURE(S)` | the new arm `ESCAPED`: applied `{93: 4185, 94: 4230, 120: 5400}`, expected `{93: 3348, 94: 3384, 120: 4320}` |
| `headroom-100-percent` | rc 0, `selftest: PASS` | rc 1, `selftest: 1 FAILURE(S)` | the new arm `ESCAPED`: applied `{70: 4200, 71: 4260, 120: 7200}`, expected `{70: 2520, 71: 2556, 120: 4320}` |
| `bound-formula-div10` | rc 0, `selftest: PASS` | rc 1, `selftest: 1 FAILURE(S)` | the new arm `ESCAPED`: applied `{11: 3960, 12: 4320, 120: 43200}`, expected `{11: 396, 12: 432, 120: 4320}` |
| `tree-head` | rc 0, `selftest: PASS` | rc 0, `selftest: PASS` | none |

The new arm is the only failing arm in each of the three mutants. The
baseline column reproduces F1 at `a57d384d`.

### R2.2 Residue applied

- **R626-1-R1 = R627-1-R1** (`docs/testing/CI_WORKFLOWS.md:191-196`, commit
  `61296ea1`). The sentence "each worker's job overhead, measured from one dev
  run." now reads: "each worker's job overhead. All figures come from one
  dev run, except `maap`, which keeps #696's figure from its pull-request run
  until a dev run measures that change." It joins both reviewers' fixes.
  R627-1 supplied "All figures come from one dev run, except `maap`", and
  R626-1 supplied "until a dev run measures that change". The rest of the
  paragraph was reflowed and its words are unchanged. The code's own account
  (`scripts/suite_shards.py:46-48`, `:86-89`) already said this.
- **R627-1-R2** (the PR body's warm-cache bullet). PR-BODY.md now reads
  "Overheads assume warm Verilator and Yosys caches; worker 1's overhead
  includes the tsn-gen build." The evidence is `rtl.yml:278-292`, the step
  "Build the pinned tsn-gen field oracle on its suite owner". It clones and
  builds tsn-gen on `matrix.shard == 1` with no cache step. The same
  correction is attached to section 7 above, with the round-1 wording kept.
  The published round-1 receipt (`author/HANDOFF.md:443` on the evidence
  branch) is left as published, and this correction applies to it.

### R2.3 Optional S2 plants

Finding: R626-1-S2, retained by R627-1. Commit `78cee0d6`.

- `:548-557` `with_verilator_key(workflow, key, value)` replaces
  `with_verilator_timeout`. It sets one key of the Verilator job to `value`,
  where `key` is given with its indentation. It still sets `timeout-minutes`
  exactly as before, and now `matrix.total` as well.
- `:585-588`: the first inventory suite (`aaf`) is planted at 0 s, and the
  gate must report `aaf: recorded duration 0 is not a positive whole number
  of seconds`. At the head: `[ok]    a recorded duration of 0 s (aaf) is
  refused`.
- `:613-620`: `rtl.yml`'s Verilator `total: [5]` is planted as `[6]`, and the
  gate must report `WORKER_OVERHEAD_SECONDS describes 5 workers; rtl.yml runs
  6`. At the head: `[ok]    rtl.yml at 6 workers is refused for the 5-worker
  overhead table`.

| `mutate.py` case | At `a57d384d` | At `61296ea1` |
|---|---|---|
| `table-zero-duration-allowed` (`> 0` became `>= 0`) | rc 0, `selftest: PASS` | rc 1: `ESCAPED a recorded duration of 0 s (aaf) is refused`, the only failure |
| `worker-count-mirrored-5` (the reader returns 5) | rc 0, `selftest: PASS` | rc 1: `ESCAPED rtl.yml at 6 workers is refused for the 5-worker overhead table`, the only failure |

`--selftest` now prints eleven `[ok]` planted-defect lines; round 1 printed
eight.

### R2.4 Not changed

- `rtl.yml` stays byte-identical (assignment item 4). The stale comment at
  `rtl.yml:136-137` (R626-1-R2) goes to #495.
- No table, balance or selection change. The five `--shard I/5 --list`
  outputs and the serial `--list` are byte-identical to round 1's. The
  predictions are unchanged: 4204 / 4205 / 4203 / 4205 / 2877 s against
  4320 s.
- R626-1-S1 (the renamed-copy skip) is not in the Round 2 assignment.
  `head-arms-skipped` still exits 0, as it did at `a57d384d`.
- **Observation for a decision, not changed.** `mutate.py`'s case
  `nondeterministic-tie` breaks equal durations by `hash(suite)` instead of
  by name. It exits 0 at `a57d384d` and at `61296ea1`, and neither review
  reported it as a finding.
  - Why the self-test misses it: the in-process `deterministic=` arm
    compares two selections made under one hash seed. The hosted workers
    each run their own process, so the gap is real.
  - The head itself is deterministic: its tie-break is lexical, and the five
    lists hash identically (`357434fb...`) under `PYTHONHASHSEED` 0, 1, 2
    and 12345. R626-1's `hashseed.txt` agrees.
  - A fix would compare selections from two subprocesses with different
    seeds. That is outside Round 2's frozen scope, so it is published here
    rather than added.

### R2.5 Gates and mutants (head `61296ea1`, all rc 0)

Interpreters are the same as in section 5. These are CPython 3.12.3 (the
hosted version), the host's 3.14.7, a 3.12.3 virtual environment with
PyYAML 6.0.3, and the pinned renderer environment for the Markdown gates.

| Gate | rc |
|---|---:|
| `python3 scripts/suite_shards.py --selftest` (3.12.3 and 3.14.7): `selftest: PASS`, 11 `[ok]`, 0 `ESCAPED`/`FAIL` | 0 |
| `python3 scripts/ci_events.py --check` | 0 |
| `python3 scripts/ci_events.py --selftest` | 0 |
| `python3 scripts/test_suite_cancellation.py` (3.14.7) | 0 |
| `python3 scripts/check_py_idiom.py` (long function 9 <= 9, over-long line 0 <= 0) | 0 |
| `python3 scripts/measure_naming.py --check` | 0 |
| `python3 scripts/measure_fail_fast.py --check` | 0 |
| `python3 scripts/check_hygiene.py --check` | 0 |
| `python3 scripts/check_todo_ownership.py` | 0 |
| `python3 scripts/measure_test_evidence.py --check` | 0 |
| `python3 scripts/suite_tally.py --selftest` | 0 |
| `python3 scripts/docs_check.py` | 0 |
| `python3 scripts/check_doc_style.py` | 0 |
| `python3 scripts/gen_toc.py --check` | 0 |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 |
| `python3 scripts/check_em_dash.py --base c6bd08c6` (0 findings over 33 added lines, arms 339/339) | 0 |
| `python3 scripts/check_em_dash.py --selftest` (339 arms) | 0 |
| `python3 scripts/check_doc_paths.py` | 0 |
| `python3 scripts/check_baremetal_only.py --check` | 0 |
| `python3 scripts/check_archive.py` | 0 |
| `scripts/run_all_suites.sh --shard I/5 --list`, I = 0..4 (15, 16, 14, 16, 1 suites) | 0 each |
| `scripts/run_all_suites.sh --list` (62 suites) | 0 |
| union of the five lists equals the `--list` inventory, no suite twice (62 listed, 62 unique) | 0 |
| shard 4/5 is exactly `milan_dp`; `tsn_fuzz` in 1/5; `chmap_capture` in 3/5 | 0 |
| `git diff --check c6bd08c6 HEAD` and `git diff --check` | 0 |
| R626-1 `mutate.py`: 29 cases, 0 `DRIFT` | 0 |
| `mutants_727.py` (round-1 harness, unchanged): 19 cases | 0 |

Mutation receipts in this directory (scratch prefix replaced by
`<scratch>`):

| File | Bytes | sha256 |
|---|---:|---|
| `r2-mutate-review-harness-at-a57d384d.txt` (R626-1 `mutate.py` at the round-1 head) | 23187 | `40fa6af1009128db76d976b7bb4fc01aef5dfa297c40b672866f0bcc88b2238a` |
| `r2-mutate-review-harness.txt` (R626-1 `mutate.py` at `61296ea1`) | 28832 | `13ca8cf1e44c599c7e35a9ba88de95886dc4eec22e72c7b81f5abe2e2ea312b4` |
| `r2-mutants-final.txt` (`mutants_727.py` at `61296ea1`) | 4706 | `d3126d8801ae750b7cb6de3d3bcdec138eaf1369b55e0fd4cbc471f799db9063` |

R626-1's full case list at `61296ea1` follows. The 23 cases that exit 1
are:

- the source mutants `missing-duration-free`, `stale-entry-check-deleted`,
  `timeout-mirrored-120`, `worker-count-mirrored-5`, `overhead-dropped`,
  `bound-ge`, `mean-only`, `headroom-100-percent`, `headroom-75-percent`,
  `bound-formula-div10`, `pins-dropped`, `pin-moved-tsn_fuzz-0`,
  `dedicated-dropped`, `measure-from-job-start`, `measure-round-down` and
  `table-zero-duration-allowed`;
- the tree plantings `tree-unmeasured-suite`, `tree-removed-suite`,
  `tree-gptp_plane+500`, `tree-timeout-116`, `tree-six-workers`,
  `tree-missing-rtl.yml` and `tree-timeout-expression`.

The six cases that exit 0 are:

- `tree-head`, `tree-timeout-117`, `tree-step-timeout-added` and
  `tree-maap-1380`, which are expected to pass;
- `head-arms-skipped` (S1, not assigned);
- `nondeterministic-tie` (see R2.4).

Against `a57d384d`, five cases moved from rc 0 to rc 1, all intended: the
three headroom mutants, `table-zero-duration-allowed` and
`worker-count-mirrored-5`. `timeout-mirrored-120` now fails two arms: the
116-minute arm, as before, and the new 36 s arm. In `mutants_727.py`, only
`m_timeout_mirrored` changed: it now fails three arms (116 minutes, 36 s a
minute and 6 workers). Every other case is as in section 4.

Not run, as in round 1: the Verilator suites, `syn/yosys/run.sh`, the
serial sweep and the `act` replica. The lane cannot push, so it has no new
PR head to replicate.

### R2.6 Acceptance 3 at the new head

Round 2 changes no figure, assignment or prediction. Predicted per worker:
4204 / 4205 / 4203 / 4205 / 2877 s, bound 4320 s.

- **PR run at `a57d384d`.** rtl-full run 38258772791 (`pull_request`, head
  `a57d384d`) still had all five Verilator jobs `in_progress` at
  2026-10-12T14:22Z. They started between 13:53:32Z and 13:59:31Z. That run
  executes the same split.
- **New head.** `61296ea1` changes the self-test, so after the push the
  exact-head measurement comes from the new head's run.

Section 6's two commands read the measured column for either run.

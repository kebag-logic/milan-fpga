Status: REVIEW READY at `c0b625d17` (12:25). The bare-metal gate passes. All 67 CI jobs a pull request runs pass locally at the head. Every product ELF is byte-identical to `640699e6`'s, and the census extract and the egress row are unchanged.
ETA: none outstanding. Pushing, posting and the hosted run are owed.

[A829], round 11, PR #1004. Worktree `$LANES/arty-int-1127`, branch `arty-int-1127`, four commits on `640699e68`. Nothing pushed or posted; no bench; no job left running.

## Done

1. **The five bare-metal findings** (`ea73a3f74`), reworded with meaning kept. The gate finds 0 over 1,981 files at the head, and its self-test passes.
2. **Every CI gate at the head.** I ran the four workflows locally, step for step, since `act` replays only a pushed head and `act` is not installed here:
   - 67 jobs, 212 gate steps, all pass: docs 7, elaborate 5, rtl-fast 23, rtl-full 32 (27 Verilator and 4 Yosys shards).
   - On the way, three more real failures, all from this lane's earlier rounds, which hosted CI would have hit at `640699e6`:
     - the test-evidence ratchet: no disposition for `egress_mii.py`'s RTL read. Fixed in `22adb80ed`.
     - the firmware coverage ratchet: the `lat` console's stale record and one infeasible arc, confirmed identical under the CI image's gcc 13.3.0 and gcc 16.2.1. Fixed in `5469c8dc5` with an exclusion row and the console's record.
     - the register reference freshness gate: the generated `REGISTER_MAP.md` had been hand-edited in `248d85c14`. Fixed in `c0b625d17`: the prose moved into its source, and the page regenerates byte-identical plus three RTL parameter rows.
3. **Images.** The three shipping products are built from clean clones of `640699e6` and the head, and are byte-identical (Arty `f17d1a9d…`, AX 8x8 `0f1450ac…`, AX 1x1 tdm8 `6e0a5412…`). `ctrl_loop.h` is comment-stripped identical, 667 lines both.
4. **Consistency.** Round 10's published extract regrades at the head, line for line as round 10's (159/159). The egress row from it is 505.738 us. No re-measurement.

## Departures, recorded

- **The local CI runner** (`receipts/ci-runner/run_ci.py`):
  - It skips setup, cache, evidence and cancellation steps; the pinned tools stand in.
  - It maps CI's `/opt/verilator`, `/opt/yosys` and `/opt/sbt` onto the host's pinned builds.
  - It runs Python 3.12, in a venv built with CI's own install and patch commands.
  - It runs with `nproc` 4.
  - It does not run jobs that only read other jobs' artifacts.
  - It does not evaluate job-level `if:`, so it started `rtl/physical-gptp` (schedule and dispatch only); I stopped it. It is not a pull-request job.
- **Runner gaps fixed during the runs, not gate failures:** a relative `GITHUB_ENV`, Python 3.14 against CI's cp312 constraints, the em-dash step's event variables, submodule origins, the Markdown renderer, `GITHUB_PATH` and `/opt` paths. The affected jobs were rerun. The final run is clean at the head.
- **The base for the em-dash and scope steps** is the live `dev-soft-core`, `0b594023`, fetched read-only into a scratch mirror. The shared repository's `gh/dev-soft-core` is stale (`aa30d77f`).
- **`coverage.ratchet`:** only the console row changed. Fourteen other rows carry stale totals from earlier merges, all 100 % before and after, and are left as they are.
- **Disk:**
  - I removed round 9's raw census traces (159 logs, about 5 GB; logged first). They are superseded by round 10's census and packed in `round9/full-packet`.
  - The final CI ran on `$VALIDATION_STORAGE` so that `/data` kept its 18 GB.
  - Every removal is in the cleanup log. Two entries were written seconds after the removal they record:
    - the first `docs-check-no-git` copy's `.git`;
    - a one-line `/tmp` probe file.

## Open (unchanged from round 10)

The rings-at-capacity 2.65 ms figure against the 1 ms row; the ruling's TX_TAIL premise; the +62 routed LUTs; one more integration once #977 lands.

Files: [PR-BODY.md](PR-BODY.md), [REVIEW-READY.md](REVIEW-READY.md), [receipts/INDEX.md](receipts/INDEX.md).

REVIEW READY c0b625d1792e61b8e99944daea65b842e6b9dcde

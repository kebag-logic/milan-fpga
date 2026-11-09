# Round 3 evidence at f3e902f2a96bb27eac6ed7780c70905af34f389e

Every run below is on a fresh clean clone of this head; `*tree-after*` files record `git status` after each job.

## Workflow steps (`gates/verify.md`)

- The four workflows a pull_request to `dev-soft-core` triggers: `rtl-fast`, `elaborate`, `rtl` (as for a ready PR) and `docs`.
- 149 `run:` steps ran, all rc 0. 193 did not run, each with its reason in `gates/tools/not_run.json`. Table: `gates/verify.md` (verify_wf rc 0).
- Runner: `gates/tools/run_wf.py`, one job per clone, step by step; drivers `gates/tools/drive.sh` with the lists `gates/tools/final-*.txt` and `final2-*.txt`.
- First runs that were repeated, both logs kept:
  - `rtl.full-ci-gate__target`: rc 1 at its first run (`GITHUB_REF: unbound variable`, a gap in the local runner). The runner was fixed and the job's `target` and `gate` steps re-ran, rc 0, decision `run_full=true` both times.
  - The two `elaborate` scope steps re-ran with the fixed runner, rc 0; their output is byte for byte the first run's.
  - `elaborate.elaborate-gates-1__gate_19` (LiteX simulation aggregate): exit 92 at its first run, 6 PASS and 2 TIMEOUT (`test_retained_cdc_storage`, `test_soc_timing_cuts`) beside the sweep. Re-run alone, rc 0, 8 of 8 PASS (`gates/litex-sim-logs`).
- Jobs killed by the host reboot at 10:34 and re-run on fresh clones: `rtl-fast` `firmware-control-mutants` and `publication-census`. The partial logs are in `gates/killed-by-reboot`.

## Full sweep (`sweep/`)

- Four shard units, `scripts/run_all_suites.sh <logs> --wait --shard k/4`, spec `sweep/sweep-spec-final.json`. They ran on two CPUs each, beside the workflow drivers.
- 65 suites: 54 PASS, 0 FAIL, 11 TIMEOUT. The sweep reports a timeout as unknown, not a failure, and says to re-run those suites uncontended.
- The preflight passed in every shard, including suite cancellation.
- The 11 were re-run one by one on fresh clones, by `gates/tools/rerun_suites.sh`, with the sweep's own timeouts and masked-verdict check. Each ran in its own unit with four CPUs. All 11 PASS, 0 in-suite failures (`sweep/rerun-uncontended`):

| Suite | rc | Wall | Timeout |
|---|---:|---:|---:|
| milan_dp | 0 | 3004 s | 4800 s |
| milan_dp_gm_steps | 0 | 728 s | 1800 s |
| milan_dp_mclk | 0 | 1661 s | 3600 s |
| capture_coherence | 0 | 2270 s | 2400 s |
| aaf_clock_meter | 0 | 794 s | 1800 s |
| maap | 0 | 1088 s | 1800 s |
| reboot_ctrl | 0 | 263 s | 300 s |
| gptp_plane | 0 | 639 s | 1800 s |
| follow_ring | 0 | 1023 s | 1800 s |
| media_phase | 0 | 777 s | 1400 s |
| mmcm_servo | 0 | 1105 s | 1800 s |

- Re-runs started before the reboot and killed by it are in `sweep/killed-by-reboot`.

## Other gates

- `extra/extra.ctrl_nvm_selftest_final.log`: `test_ctrl_nvm.py --require-rv32 --self-test --jobs 4`, rc 0. It prints `OK across 5 shape(s), 474 tests, and all 123 planted defects reddened`.
- The builder bank (`test_builder.py --require-rv32`, and `--require-elaboration` in `elaborate`): the docs and elaborate legs, rc 0, and their unions in `gates/union` (106 gates exactly once).
- The saved-state writer gate: `docs.docs-gates-0__gate_28`, rc 0, `OK across 5 shape(s)`.
- `head/diff-check.txt`: `git diff --check` against the merge base `a9d69c77`, rc 0.
- `head/split-save-path.md`: the split store's flash path names neither the processor nor `KL_nvm_backend`.
- `split-memory/`: the split image's size at four points, base against head.

Files over 200 KB are listed in each directory's `LARGE.tsv` by bytes and sha256; `RAW.tsv` holds the digest of each source before host prefixes were replaced.

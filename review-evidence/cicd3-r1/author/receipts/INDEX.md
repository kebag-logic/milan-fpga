# [A839] round 3 receipts (text only, uncompressed, no file over 200 KB)

Raw logs, model builds and the clones stay in the lane's scratch, /data-2/milan/tmp/cicd-a839/r3/. Everything a
reviewer needs to re-check a figure in REPORT.md is here.

- perf files are `perf stat -x,` CSV.
- `.time` files are `/usr/bin/time` lines: wall, user, sys, then `rc=`.
- `start`/`end` files are epoch seconds.
- A `births` file lists each log's statx birth time.
- Identity verdicts come from tools/logcmp.py and tools/mutcmp.py.

| Path | What it holds | REPORT section |
|---|---|---|
| preflight/s9-pre/, preflight/s9-nopre/ | Shard 9/19 replica at 66b092e1 with and without preflight: time, perf, births, start/end, out.tail, both suite logs, maap__2.json receipt; s9-pre/preflight/ holds the shard's own eight preflight logs | 1.3 |
| preflight/preonly/ | `run_all_suites.sh --preflight-only` (the new job's command): time, perf, its eight preflight logs | 1.3 |
| preflight/binding-controls.txt | ci_suite_pieces_selftest's six executions of the generated verilator-suites preflight step | 1.2 |
| preflight/test_suite_cancellation-head.log | The cancellation test at the head, including every new preflight-only / no-preflight control's record | 1.2 |
| preflight/preflight-only-without-submodules.log | `--preflight-only` in a tree exported with no submodules (rc 0) | 1.1 |
| gates/negative-controls.txt | Two planted driver defects, each caught by the new controls | 1.2 |
| gates/summary, gates/*.log | Every gate run at 13e6d869 in a clean clone, one log each | all |
| piece/cost/ | Each milan_dp case's `exec-<case>` alone on one core: time, perf, output tail; TABLE.txt sorted by CPU | 2.2 |
| piece/p0-listorder/, piece/p0-longestfirst/ | milan_dp__0 through `ci_make_cases.py --shard 0/4 --jobs 2`: list order (f6c11a25) and longest first (0572488b), time, perf, start/end, receipts, transcript | 2.3 |
| piece/identity.txt | The two arms' receipts compared per case (outcome, return code, output_sha256) and their transcripts | 2.3 |
| mutants/embedded-path.txt | One RTL verilated from two directories: the generated C++ differs only in the embedded path | 3.2 |
| mutants/mut3-*.summary, mutants/mut3/ | crf_rx and avtp_rxmon depkt: base cold/warm, head cold/warm/second checkout (time, ccache stats, logs) | 3.3 |
| mutants/mut2-*.summary, mutants/mut2/ | rx_filter binding, tcam (complete) and mmcm_servo slew (base cold complete; the others stopped, partial) | 3.3 |
| mutants/identity.txt | Every driver's log in each run against the base cold run | 3.3 |
| mutants/crf_rx-third-checkout-misses.txt | ccache's log from a third checkout: the 15 misses, all harness compiles | 3.3 |
| mutants/finding3-rx_filter.txt | rx_filter's suite build through ccache (same and another checkout), and three verilations diffed | 3.4 |
| smt/s8-siblings/, smt/s8-wholecores/ | Shard 8/19, 2 cores both siblings vs 4 cores one thread each: time, perf, both suite logs | 4 |
| gptp/serial/, gptp/parallel/ | FPGA-gPTP `make -C tb/verilator/engine run` at 1213ac5 and at the branch: time, perf, transcript | 5 |
| gptp/identity.txt | The two transcripts compared (IDENTICAL, 170 lines) | 5 |
| gptp/term-test.log, gptp/fail-test.log | SIGTERM to the parallel recipe; a stub simulator failing in pass 1 | 5 |
| gptp/docs-gate.log | FPGA-gPTP `make docs` at the branch head | 5 |
| gptp/engine-run-passes-at-once.patch, gptp/branch.txt | The branch's one commit (`git format-patch`, author address removed) and its SHAs | 5 |
| caches/caches-now.tsv, caches/pr-states.txt | The repository's 326 Actions cache entries (key, ref, bytes, created, last used), read-only, 2026-11-24 17:10 CET; each PR's state | 6 |
| tools/ | The scratch scripts that produced the above: mkclone.sh, casecost.sh, shard3.sh, piece3.sh, mutrun2.sh, mutrun3.sh, gprun3.sh, gates.sh, codemod_stage.py, mutctl.py, logcmp.py, mutcmp.py, env.sh | all |

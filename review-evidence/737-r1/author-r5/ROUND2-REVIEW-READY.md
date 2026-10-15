[A614] REVIEW READY

Commit: `2658a64c408bf87ae36574f36a6deeb34b2f297f`
Branch: `737-ci-30min`. Clean worktree. No push or PR write occurred.

The scoped measurements authorized by 6172868895 are complete. Since the prior STOP head `21bd10cec1a999791c9cd2c6d37c52372fb1504e`, changes are limited to the measured resource documentation in `docs/testing/CI_WORKFLOWS.md:2320-2355` and the stale memory comment at `scripts/act_ci.py:153`. The runner AST is unchanged. The required dev merge and all earlier Round 2 corrections remain intact.

| Workload | Peak bytes at 16 CPUs | Peak bytes at 12 CPUs |
|---|---:|---:|
| Publication census, four workers | 5860151296 | 5201534976 |
| Heaviest synthesis shard | 3745005568 | 3391201280 |
| Firmware normal phase, required RV32 checks | 1365569536 | 1372815360 |
| Eight-stream datapath build and simulation | 3349397504 | 2697302016 |
| Capture campaign, four builds | 6047100928 | 5042556928 |
| Builder, required RV32 and elaboration | 3523665920 | 3172597760 |
| Standalone LiteX aggregate | 3745722368 | 3303358464 |

All fourteen measurements return zero, with every memory-event counter zero. The eight resumed workloads ran sequentially, one 8 GiB container at a time; their recorded start/finish intervals do not overlap. Each datapath run passes 3,751 checks, each capture run passes 32 checks, and each standalone run passes seven simulations plus ten runner controls without skips or timeouts. Actual JVM execution was observed in both builder and both standalone runs. The builder retains two existing NOT RUN arms: an inert Make environment mutation and the absent physical calibration report. Those arms are not claimed covered.

Sizing: retain the 8 GiB job cap, four-job admission and 36 GiB slot cap. The largest peak is 6047100928 bytes (5.632 GiB), leaving 2542833664 bytes (2.368 GiB), or 42.05% above that peak. Four 8-GiB caps plus 4 GiB overhead equal 36 GiB; `floor((36 - 4) / 8) = 4`. Four measured maxima plus overhead total 26.527 GiB; that arithmetic is not a measured simultaneous slot peak. Capture retains four workers with four/three compilers each at 16/12 CPUs; census retains its measured four-worker ceiling.

Resumed workload source: `21bd10cec1a999791c9cd2c6d37c52372fb1504e`; image: `sha256:94128cff4711ebfe6d3c5ac10bf88cdc9bac5caff4f4b28fc873fc83897d8427`, CPython 3.12.3, Verilator 5.050. Twelve CPUs measures width within the assigned die, not aligned fallback admission. The sixteen-CPU builder container was removed before configuration export: its retained launch command supplies cap/image settings, while final state and cgroup measurements were captured before removal. Other resumed receipts include directly inspected Docker limits.

Validation commands all return zero after the recorded environment prerequisites were supplied:

```sh
python3 scripts/check_py_idiom.py
python3 scripts/generate_ci_evidence_pins.py --check
python3 scripts/check_hygiene.py
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base fa820988
python3 scripts/check_em_dash.py --selftest
git diff --check
```

The punctuation gate passes all 339 controls. The complete runner self-test also passes, exclusively inside a disposable full CI container with CPython 3.12.3, no network, no Docker socket and a read-only candidate mount:

```sh
python3 -I scripts/act_ci.py --selftest --worktree "$PWD"
```

The initial missing-sudo and missing-Docker-CLI environment refusals are retained separately, as are the earlier ownership and SDK-selector attempts. No test assertion, case, timeout, firmware behavior or linked image was changed to get a pass.

Runner SHA-256 for coordinating repinning: `5ccbd700ece6f8ce0558767c77fa44435c9dbb2d37c48cc44269790ec64474dd`.

`HANDOFF.md` and `PR-BODY.md` contain the updated Round 2 result, file/line map, baseline/projection qualifications, resource arithmetic, commands and limitations. `round2-resumed-resource-summary.json` binds all fourteen receipts; `round2-resumed-artifacts/index.json` indexes workload artifacts. Oversized logs are represented by size and SHA-256. The final audit confirms clean source, one-line commits without bodies/trailers, no active measurement containers and no oversized output files.

Acceptance: the authorized fixes-only author work and scoped resource measurements are complete. Coordinating publication/repinning, complete candidate replay, hosted workflow timings including watcher/collector tail, live cancellation evidence and independent re-review remain required. Both round-one reviews remain NEGATIVE; this handoff is not a review verdict or merge authorization. No new owner-level decision is requested.

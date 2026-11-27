# Reviewer scripts (R955-2)

All scripts run from a tree extracted with `git archive 0f72ca69a0cd85ade9a3f1c42a325b23704cf625`
(`scratch/tree`, not published). Set `TOOLS` to the root holding the pinned `gtest-1.14.0`,
`clang-18` and `clang-tidy-18` trees before running them; `env.sh` refuses to run without it.

| Script | Purpose |
|---|---|
| `env.sh` | Pinned GoogleTest/GMock 1.14.0, Clang 18.1.3 wrappers and clang-tidy 18.1.3 on `PATH`; sanitizer options as in `scripts/validate.py`. |
| `run_gates.sh TREE OUT` | The quality job's command list (`scripts/validate.py`), continuing past a failure, plus the bare-metal job (`scripts/baremetal.py`). Source gates run first, then GCC with coverage, the host-Clang sanitizer arm, the mutation campaign and RV32 run side by side (3+3+8+2 = 16 jobs), then static analysis, mutation controls and graphs. |
| `run_probes.sh TREE OUT JOBS` | Runs the round-1 probe sets (`probes.json`, `probes2.json`) and the per-octet set through `probes_run.py`, using the campaign's baseline objects. |
| `octet_probes_gen.py TREE OUT` | Writes one probe per term of `record_moved`'s 20-octet comparison (term replaced by `0u`). |
| `probes_run.py TREE BASELINE PROBES WORK OUT JOBS` | Builds each probe against the `acmp`, `acmp_wide` and `acmp_walk` arms and runs every test in them. A probe that does not compile is listed as BUILD-FAILED in `receipts/probe-summary.txt`; it is not counted as killed. |
| `probes_gen.py`, `probes2_gen.py` | The round-1 generators of `probes.json` and `probes2.json` (unchanged; `src/` is unchanged since round 1). |

`license` and `privacy` read git history, so they were also run in a disposable clone checked out at the
exact head (`receipts/gates/license-gitclone.*`, `receipts/gates/privacy-gitclone.*`).

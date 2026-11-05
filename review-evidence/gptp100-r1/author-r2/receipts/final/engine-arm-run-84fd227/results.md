# final/engine-arm-run-84fd227

- Head: `84fd22781c95f7b7e65d7d18c99a5ed49a68e11c`
- Base: `5184fb36e34926d007f1ca4d5121863faf9b89fa`
- Finished: 2026-11-06T00:14:49.960099+01:00; runner exit 0
- Environment: the pinned Verilator 5.050, `VERILATOR_JOBS=4`, `MAKEFLAGS=-j4`, one unit, MemoryMax 10G.
- Log sha256 is of the original log; the copy here has host paths replaced by placeholders.

| # | Command | rc | Seconds | Log | Log sha256 |
|---:|---|---:|---:|---|---|
| 1 | `python3 <scratch>/tools/arm_jobs.py tb/verilator/engine <scratch>/arm-84fd227 --jobs 8 --budget-s 30000 --longest-s 900` | 0 | 4285.995 | [01.log](01.log) | `83e06227230a5035` |
| 2 | `git diff --exit-code --stat` | 0 | 0.018 | [02.log](02.log) | `e3b0c44298fc1c14` |
| 3 | `git status --porcelain` | 0 | 0.016 | [03.log](03.log) | `e3b0c44298fc1c14` |

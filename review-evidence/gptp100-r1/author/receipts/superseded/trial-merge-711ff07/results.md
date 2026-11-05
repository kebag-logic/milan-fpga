# superseded/trial-merge-711ff07

- Head: `ffb179c4fa08d7008d2d740810cc8d62ddafcd3b`
- Base: `5184fb3`
- Finished: 2026-11-05T18:39:05.777408+01:00; runner exit 0
- Environment: the pinned Verilator 5.050, `VERILATOR_JOBS=4`, `MAKEFLAGS=-j4`, one unit, MemoryMax 10G.
- Log sha256 is of the original log; the copy here has host paths replaced by placeholders.

| # | Command | rc | Seconds | Log | Log sha256 |
|---:|---|---:|---:|---|---|
| 1 | `make contract` | 0 | 0.054 | [01.log](01.log) | `cdc70d96a542ea1a` |
| 2 | `make -C tb/verilator/ucpu` | 0 | 7.466 | [02.log](02.log) | `5e2fc9789ac548ca` |
| 3 | `make -C tb/verilator/parser` | 0 | 243.81 | [03.log](03.log) | `b87539d22ae3a378` |
| 4 | `make -C tb/verilator/engine run` | 0 | 522.69 | [04.log](04.log) | `cfd38717014f93e3` |
| 5 | `make -C tb/verilator/gaskets` | 0 | 38.4 | [05.log](05.log) | `7998ec7db217a328` |
| 6 | `make -C tb/tsngen` | 0 | 42.528 | [06.log](06.log) | `8112cc26a5dd4e3b` |
| 7 | `make -C bench/arty test` | 0 | 6.535 | [07.log](07.log) | `1f9e5b049add2fb6` |
| 8 | `make lint` | 0 | 0.372 | [08.log](08.log) | `5606ba618c48d7aa` |
| 9 | `make docs` | 0 | 1.708 | [09.log](09.log) | `b06c7fc63eeca1a8` |
| 10 | `make diagrams-check` | 0 | 0.22 | [10.log](10.log) | `aaa064730c0f1e63` |
| 11 | `git diff --exit-code --stat` | 0 | 0.004 | [11.log](11.log) | `e3b0c44298fc1c14` |
| 12 | `git status --porcelain` | 0 | 0.005 | [12.log](12.log) | `e3b0c44298fc1c14` |

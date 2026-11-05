# final/trial-merge-3e3f041

- Head: `d5d3eb7fafeb474ebe101d27a80bfd503b3ea96d`
- Base: `5184fb36e34926d007f1ca4d5121863faf9b89fa`
- Finished: 2026-11-05T19:22:48.460315+01:00; runner exit 0
- Environment: the pinned Verilator 5.050, `VERILATOR_JOBS=4`, `MAKEFLAGS=-j4`, one unit, MemoryMax 10G.
- Log sha256 is of the original log; the copy here has host paths replaced by placeholders.

| # | Command | rc | Seconds | Log | Log sha256 |
|---:|---|---:|---:|---|---|
| 1 | `make contract` | 0 | 0.037 | [01.log](01.log) | `cdc70d96a542ea1a` |
| 2 | `make -C tb/verilator/ucpu` | 0 | 8.506 | [02.log](02.log) | `b9418eced661ce93` |
| 3 | `make -C tb/verilator/parser` | 0 | 242.626 | [03.log](03.log) | `5b5f65f1df9da3d5` |
| 4 | `make -C tb/verilator/engine run` | 0 | 500.045 | [04.log](04.log) | `82e2f58ca5987bcf` |
| 5 | `make -C tb/verilator/gaskets` | 0 | 33.18 | [05.log](05.log) | `61fef604df13761a` |
| 6 | `make -C tb/tsngen` | 0 | 43.937 | [06.log](06.log) | `1ea0c2c4a4eafafb` |
| 7 | `make -C bench/arty test` | 0 | 5.676 | [07.log](07.log) | `e8cace7348f2214a` |
| 8 | `make lint` | 0 | 0.351 | [08.log](08.log) | `77355efb9a995ecb` |
| 9 | `make docs` | 0 | 1.513 | [09.log](09.log) | `b06c7fc63eeca1a8` |
| 10 | `make diagrams-check` | 0 | 0.219 | [10.log](10.log) | `aaa064730c0f1e63` |
| 11 | `git diff --exit-code --stat` | 0 | 0.004 | [11.log](11.log) | `e3b0c44298fc1c14` |
| 12 | `git status --porcelain` | 0 | 0.005 | [12.log](12.log) | `e3b0c44298fc1c14` |

# final/parent-A-3e3f041

- Head: `94a9f1860f0bf5f64d34530c2a2a76f196a72394`
- Base: `604899c08ff1cd1830e1dd08b733109ef852400c`
- Finished: 2026-11-05T20:24:08.533120+01:00; runner exit 0
- Environment: the pinned Verilator 5.050, `VERILATOR_JOBS=4`, `MAKEFLAGS=-j4`, one unit, MemoryMax 10G.
- Log sha256 is of the original log; the copy here has host paths replaced by placeholders.

| # | Command | rc | Seconds | Log | Log sha256 |
|---:|---|---:|---:|---|---|
| 1 | `make -C tb/verilator/gptp_shadow -j8` | 0 | 422.935 | [01.log](01.log) | `c9a1f51988a13269` |
| 2 | `make -C tb/verilator/milan_dp gptp` | 0 | 415.613 | [02.log](02.log) | `e695c88c3a003701` |
| 3 | `make -C tb/verilator/milan_dp gptp-lat` | 0 | 369.504 | [03.log](03.log) | `deab1167ac1de677` |
| 4 | `make -C tb/verilator/gptp_plane` | 0 | 810.536 | [04.log](04.log) | `0c3f2b4519a0b93f` |
| 5 | `make -C tb/verilator/gptp_txts` | 0 | 174.265 | [05.log](05.log) | `4c7437a874249789` |
| 6 | `make -C tb/verilator/gptp_tables` | 0 | 738.919 | [06.log](06.log) | `de673be0dbe19d4b` |
| 7 | `make -C tb/verilator/tsn_fuzz ptp` | 0 | 8.533 | [07.log](07.log) | `f3526ce3fabbb879` |
| 8 | `make -C tb/verilator/milan_dp_gm_steps` | 0 | 714.61 | [08.log](08.log) | `ce5136078a916cd1` |
| 9 | `python3 scripts/check_cpp_idiom.py` | 0 | 1.925 | [09.log](09.log) | `8a80e135fafe8237` |
| 10 | `python3 scripts/check_py_idiom.py` | 0 | 5.353 | [10.log](10.log) | `8ca960bf8c58e1bd` |
| 11 | `python3 scripts/xvlog_gate.py --check` | 0 | 156.85 | [11.log](11.log) | `568364181a8b969d` |
| 12 | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.705 | [12.log](12.log) | `403a78cd6109c4d2` |
| 13 | `python3 scripts/check_port_contracts.py` | 0 | 2.939 | [13.log](13.log) | `aa3b2cf6bc78ca26` |
| 14 | `python3 scripts/measure_naming.py --check` | 0 | 0.606 | [14.log](14.log) | `21e1d7a07f3a35ca` |
| 15 | `python3 scripts/measure_test_evidence.py --check` | 0 | 9.155 | [15.log](15.log) | `f638eb7f544a9d30` |
| 16 | `python3 scripts/docs_check.py` | 0 | 7.252 | [16.log](16.log) | `1d0c5dcd2ec27c99` |
| 17 | `python3 scripts/lint_rtl.py --check` | 0 | 12.048 | [17.log](17.log) | `ef55a6d7cc8d4e55` |
| 18 | `python3 sw/builder/test_builder.py` | 0 | 1582.79 | [18.log](18.log) | `77df6ce9f99cc513` |
| 19 | `git status --porcelain` | 0 | 0.038 | [19.log](19.log) | `e3b0c44298fc1c14` |

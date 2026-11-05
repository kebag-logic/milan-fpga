# final/parent-A-84fd227

- Head: `2278661f248a99cb97e858ab138656d6c28fa538`
- Base: `604899c08ff1cd1830e1dd08b733109ef852400c`
- Finished: 2026-11-06T00:20:05.421118+01:00; runner exit 0
- Environment: the pinned Verilator 5.050, `VERILATOR_JOBS=4`, `MAKEFLAGS=-j4`, one unit, MemoryMax 10G.
- Log sha256 is of the original log; the copy here has host paths replaced by placeholders.

| # | Command | rc | Seconds | Log | Log sha256 |
|---:|---|---:|---:|---|---|
| 1 | `make -C tb/verilator/gptp_shadow -j8` | 0 | 264.004 | [01.log](01.log) | `2db78f6c63bdd368` |
| 2 | `make -C tb/verilator/milan_dp gptp` | 0 | 317.614 | [02.log](02.log) | `86f5e919dcdeea0a` |
| 3 | `make -C tb/verilator/milan_dp gptp-lat` | 0 | 321.297 | [03.log](03.log) | `75fd9fdbce9a7303` |
| 4 | `make -C tb/verilator/gptp_plane` | 0 | 628.072 | [04.log](04.log) | `8d5cfc1924cac600` |
| 5 | `make -C tb/verilator/gptp_txts` | 0 | 123.448 | [05.log](05.log) | `48fb9705b30415ae` |
| 6 | `make -C tb/verilator/gptp_tables` | 0 | 443.083 | [06.log](06.log) | `c6b9759a6ffa7c0c` |
| 7 | `make -C tb/verilator/tsn_fuzz ptp` | 0 | 5.68 | [07.log](07.log) | `19db46bd6636c83b` |
| 8 | `make -C tb/verilator/milan_dp_gm_steps` | 0 | 673.144 | [08.log](08.log) | `5a417b7512084084` |
| 9 | `python3 scripts/check_cpp_idiom.py` | 0 | 2.116 | [09.log](09.log) | `8a80e135fafe8237` |
| 10 | `python3 scripts/check_py_idiom.py` | 0 | 6.61 | [10.log](10.log) | `c94237de3cc11f06` |
| 11 | `python3 scripts/xvlog_gate.py --check` | 0 | 154.982 | [11.log](11.log) | `7a24cb511a65f53b` |
| 12 | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.676 | [12.log](12.log) | `403a78cd6109c4d2` |
| 13 | `python3 scripts/check_port_contracts.py` | 0 | 3.137 | [13.log](13.log) | `aa3b2cf6bc78ca26` |
| 14 | `python3 scripts/measure_naming.py --check` | 0 | 0.527 | [14.log](14.log) | `21e1d7a07f3a35ca` |
| 15 | `python3 scripts/measure_test_evidence.py --check` | 0 | 8.974 | [15.log](15.log) | `f638eb7f544a9d30` |
| 16 | `python3 scripts/docs_check.py` | 0 | 7.491 | [16.log](16.log) | `1d0c5dcd2ec27c99` |
| 17 | `python3 scripts/lint_rtl.py --check` | 0 | 11.265 | [17.log](17.log) | `ef55a6d7cc8d4e55` |
| 18 | `python3 sw/builder/test_builder.py` | 0 | 1623.577 | [18.log](18.log) | `36d3a2701dbe6cb7` |
| 19 | `git status --porcelain` | 0 | 0.044 | [19.log](19.log) | `e3b0c44298fc1c14` |
